---
name: td-mcp-bootstrap
description: Automatically prepare new TouchDesigner projects with Kuanfu Weimu's local TDMCP component, start its service, and verify the MCP connection without dragging files or controlling the screen. Use before creating a new TD project or when TD MCP is disconnected.
---

# TD MCP bootstrap

Use this workflow automatically for agent-created TD projects. A skill is not a hook into TouchDesigner's File > New command. Do not promise that manually created projects already contain TDMCP.

Default source: `D:\Derivative\TouchDesigner.2025.32460\Samples\Palette\TDMCP.tox`.
Default executable: `D:\Derivative\TouchDesigner.2025.32460\bin\TouchDesigner.exe`.
Keep scratch, generated components, and projects on D. Never edit the source plugin or installed TD files. Do not use mouse/keyboard/UI automation. Launches use a hidden window and never close unrelated TD processes.

## New project

Run `D:\Python\python.exe <skill>/scripts/bootstrap.py --output-dir <new-project-folder> --name <project-name> --launch`.
The script expands a copy with TD's own tools, enables Active, disables viewport-follow/highlight to respect the no-screen-control preference, and preserves authentication settings. It checks the actual plugin save build against the installed build before launching. It will not overwrite existing files.

On success it initializes MCP, lists tools, calls read-only project_info, checks that this is the intended new project, then saves the new `.toe` via save_project. Inspect get_errors before beginning creative work. Retain the generated bootstrap JSON receipt. This method needs no pre-existing MCP connection.

If another process owns the configured port, stop instead of connecting to an arbitrary project. Existing-project work must use the already connected, identity-verified project or an authorized copy; never launch a new empty project and present it as the user's existing work. For a connected existing project, inspect whether TDMCP is already present before loading anything.

## Failures and authorization

- Version conflict: report the plugin save build and installed build; use a compatible installation/component. Never patch the saved build number to hide the conflict. Do not repeat launches or ask the user to drag the same file again.
- Authentication: preserve it; use the host's legitimate OAuth flow. A required consent cannot be bypassed. This local 1.1.54 file has Auth off by default, but do not assume future files do.
- Timeout: report only the created files and failed live verification. Do not claim connected or create duplicate processes. The returned PID identifies only the helper-created instance.
- A 200 response or open port is not proof of an MCP connection. Require initialize + tools/list + project_info and project identity before mutations.

For the film project, retain its stage and aesthetic approval gates; configuring this helper does not approve later film stages.

## Verified local state (2026-10-31)

Source TDMCP is 1.1.54, saved in 2025.33070, with Active default off. Installed TD is 2025.32460. An isolated launch hit `File load version conflict`; no MCP project_info succeeded. The isolated test process was stopped; the user's original TD process was left running. Offline preparation and version rejection are tested; live startup/save remain unverified until compatible versions are available.

Official utility documentation: https://docs.derivative.ca/Toeexpand and https://docs.derivative.ca/Toecollapse .

---

## 中文工作流

为助手创建的 TD 工程自动使用此流程。技能不是 TouchDesigner File > New 命令钩子，不要承诺手动新建工程已含 TDMCP。

默认源：`D:\Derivative\TouchDesigner.2025.32460\Samples\Palette\TDMCP.tox`。
默认程序：`D:\Derivative\TouchDesigner.2025.32460\bin\TouchDesigner.exe`。
临时文件、生成组件与工程放 D 盘；不修改原插件或 TD 安装文件。不用鼠标、键盘或 UI 自动化；隐藏窗口启动，不关闭无关 TD 进程。

### 新工程

运行 `D:\Python\python.exe <skill>/scripts/bootstrap.py --output-dir <new-project-folder> --name <project-name> --launch`。
脚本用 TD 工具展开副本，启用 Active，关闭视口跟随/高亮以符合不操作屏幕偏好，并保留认证设置。启动前比对实际插件保存构建与安装构建，不覆盖已有文件。

成功后初始化 MCP、列出工具、调用只读 project_info，核对目标新工程，再通过 save_project 保存 `.toe`。创作前检查 get_errors，保留生成的 bootstrap JSON 回执。该方法不需要事先已有 MCP 连接。

如配置端口已被其他进程占用，停止而非随意连接项目。已有工程工作必须使用身份已核实的现有连接或获准副本，不启动空工程冒充用户现有工程。已连接项目应先确认 TDMCP 是否存在，再决定是否加载。

### 失败与授权

- 版本冲突：报告插件保存构建和安装构建，使用兼容版本；不篡改保存版本号掩盖冲突，不反复启动或要求用户再次拖同一文件。
- 认证：保留认证并使用宿主正规 OAuth 流程，不能绕过必要同意。本地 1.1.54 的 Auth 默认关闭，不据此推断未来文件。
- 超时：仅报告已创建文件和实际验证失败，不宣称连接成功或创建重复进程。回执 PID 只代表辅助实例。
- HTTP 200 或端口开放不证明 MCP 已连接；修改前必须完成 initialize、tools/list、project_info 及工程身份核验。

电影项目仍保留其阶段与审美审批关卡；配置此辅助工具不代表后续电影阶段已获批。

### 已验证的本地状态（2026-10-31）

源 TDMCP 1.1.54 保存于 2025.33070，Active 默认关闭；安装 TD 为 2025.32460。隔离启动出现 `File load version conflict`，未成功调用 MCP project_info。只停止测试进程，保留用户原进程。离线准备及版本拒绝已验证；版本兼容前，实际启动/保存仍未验证。

官方工具文档：https://docs.derivative.ca/Toeexpand 和 https://docs.derivative.ca/Toecollapse 。
