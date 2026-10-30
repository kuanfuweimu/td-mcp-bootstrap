"""Prepare a local, enabled TDMCP copy; optionally start and save a NEW project."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import socket
import subprocess
import time
import urllib.request

DEFAULT = Path(r'D:\Derivative\TouchDesigner.2025.32460')

def rpc(url, method, params, headers, ident=1):
    payload = {'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        session = response.headers.get('Mcp-Session-Id')
        if session:
            headers['Mcp-Session-Id'] = session
        body = response.read().decode()
    if body.startswith('event:') or body.startswith('data:'):
        messages = [json.loads(line[5:].strip()) for line in body.splitlines() if line.startswith('data:')]
        result = next(m for m in messages if m.get('id') == ident)
    else:
        result = json.loads(body)
    if 'error' in result:
        raise RuntimeError(str(result['error']))
    return result['result']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--td', type=Path, default=DEFAULT/'bin/TouchDesigner.exe')
    ap.add_argument('--tox', type=Path, default=DEFAULT/'Samples/Palette/TDMCP.tox')
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--name', default='NewProject')
    ap.add_argument('--launch', action='store_true')
    a = ap.parse_args()
    out = a.output_dir.resolve()
    if out.drive.upper() != 'D:':
        raise ValueError('Choose a D-drive output directory.')
    if not re.fullmatch(r'[\w -]+', a.name):
        raise ValueError('Project name must contain letters, numbers, spaces, hyphens or underscores.')
    a.td = a.td.resolve(); a.tox = a.tox.resolve()
    if not a.td.is_file() or not a.tox.is_file():
        raise FileNotFoundError('TD executable or source TDMCP is missing.')
    out.mkdir(parents=True, exist_ok=True)
    target = out/(a.name+'.toe')
    copied = out/'TDMCP_bootstrap.tox'
    if target.exists() or copied.exists():
        raise FileExistsError('Use a fresh output directory; existing projects are never overwritten.')
    source_hash = hashlib.sha256(a.tox.read_bytes()).hexdigest()
    shutil.copy2(a.tox, copied)
    expansion = subprocess.run([str(a.td.parent/'toeexpand.exe'), str(copied)], capture_output=True)
    expanded = Path(str(copied)+'.dir')
    if not (expanded/'.build').is_file() or not (expanded/'TDMCP.parm').is_file():
        raise RuntimeError(f'Expansion failed: {expansion.stdout!r} {expansion.stderr!r}')
    build_text = (expanded/'.build').read_text()
    saved = re.search(r'build\s+(\d+)\.(\d+)', build_text)
    installed = re.search(r'TouchDesigner\.(\d+)\.(\d+)', str(a.td))
    if not saved or not installed:
        raise RuntimeError('Cannot determine builds; inspect installation before launching.')
    parm = expanded/'TDMCP.parm'
    lines = parm.read_text(encoding='utf-8').splitlines()
    changes = {'Active':'on', 'Followactive':'off', 'Animatenodes':'off'}
    lines = [line for line in lines if line.split(' ',1)[0] not in changes]
    lines[1:1] = [f'{key} 0 {value}' for key,value in changes.items()]
    parm.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    collapse = subprocess.run([str(a.td.parent/'toecollapse.exe'), str(copied)], capture_output=True)
    if not copied.is_file() or hashlib.sha256(copied.read_bytes()).hexdigest() == source_hash:
        raise RuntimeError(f'Collapse failed: {collapse.stdout!r} {collapse.stderr!r}')
    assert hashlib.sha256(a.tox.read_bytes()).hexdigest() == source_hash
    compatible = tuple(map(int, installed.groups())) >= tuple(map(int, saved.groups()))
    receipt = {'source':str(a.tox), 'source_sha256':source_hash, 'prepared':str(copied),
               'plugin_save_build':'.'.join(saved.groups()), 'td_build':'.'.join(installed.groups()),
               'status':'prepared' if compatible else 'blocked_version', 'live_verified':False}
    receipt_path = out/'bootstrap-result.json'
    def record():
        receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    record()
    if not a.launch or not compatible:
        print(json.dumps(receipt,indent=2)); return
    # Derive the effective port without changing it or the Auth setting.
    match = re.search(r'^Port \d+ (\d+)$', parm.read_text(), re.M)
    port = int(match.group(1)) if match else 13316
    with socket.socket() as sock:
        if sock.connect_ex(('127.0.0.1',port)) == 0:
            raise RuntimeError('Port occupied: inspect that project rather than launch a second server.')
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    proc = subprocess.Popen([str(a.td),str(copied)],cwd=out,startupinfo=startup)
    receipt['pid'] = proc.pid; record()
    url = f'http://127.0.0.1:{port}/mcp'
    headers = {'Content-Type':'application/json','Accept':'application/json, text/event-stream'}
    try:
        deadline = time.monotonic()+45
        while True:
            try:
                rpc(url,'initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'codex-td-bootstrap','version':'1.0'}},headers)
                break
            except (OSError,TimeoutError):
                if time.monotonic() >= deadline or proc.poll() is not None: raise
                time.sleep(1)
        notification = urllib.request.Request(url,data=json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'}).encode(),headers=headers)
        with urllib.request.urlopen(notification,timeout=5): pass
        listed = rpc(url,'tools/list',{},headers,2)
        names = {t['name'] for t in listed['tools']}
        if not {'project_info','save_project'} <= names: raise RuntimeError('Expected tools unavailable.')
        info = rpc(url,'tools/call',{'name':'project_info','arguments':{}},headers,3)
        if info.get('isError'): raise RuntimeError(str(info))
        # Only save when the new project's working folder is confirmed.
        texts = '\n'.join(c.get('text','') for c in info.get('content',[]))
        details = json.loads(texts)
        if Path(details['folder']).resolve() != out:
            raise RuntimeError('Project identity mismatch; refusing save.')
        result = rpc(url,'tools/call',{'name':'save_project','arguments':{'path':str(target)}},headers,4)
        if result.get('isError') or not target.is_file(): raise RuntimeError('Project save not verified.')
        receipt.update(status='connected_and_saved',live_verified=True,project=str(target),project_info=details)
    except Exception as exc:
        receipt.update(status='live_check_failed',error=str(exc))
    record(); print(json.dumps(receipt,indent=2))

if __name__ == '__main__':
    main()
