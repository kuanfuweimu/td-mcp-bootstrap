# TD MCP bootstrap

Codex skill for preparing a new TouchDesigner project with the locally installed TDMCP component. All generated data goes on D. No plugin binary is redistributed.

Install `skill/` as `D:\Codex\.codex\skills\td-mcp-bootstrap`. Invoke automatically before new TD projects, or with $td-mcp-bootstrap. The local td-general skill also links this workflow.

The script prepares an enabled component copy using Derivative toeexpand/toecollapse, checks builds, and optionally launches and verifies MCP before saving a new project. It preserves authentication and refuses occupied ports and existing output files.

Current validation: offline preparation passes; original plugin SHA256 unchanged; version guard passes. Live startup/save not verified: supplied plugin 1.1.54 was saved in TD 2025.33070, while installed TD is 2025.32460. A test launch showed File load version conflict. Use compatible versions before live use. This is not a global File > New hook.

---

## 中文说明

这是使用本地已安装 TDMCP 组件准备新 TouchDesigner 工程的 Codex 技能。生成数据按原工作流放在 D 盘，不再分发插件二进制。

将 `skill/` 安装到 `D:\Codex\.codex\skills\td-mcp-bootstrap`。创建 TD 工程前自动使用，或通过 `$td-mcp-bootstrap` 调用。本地 td-general 技能也链接了此流程。

脚本使用 Derivative 的 toeexpand/toecollapse 准备启用状态的组件副本，检查构建版本；可选择启动、验证 MCP 后保存新工程。保留认证配置，拒绝被占用的端口和已存在的输出文件。

原记录的验证状态：离线准备通过，原插件 SHA256 不变，版本检查通过。实际启动/保存未验证：提供的 1.1.54 插件保存于 TD 2025.33070，安装的 TD 为 2025.32460，测试启动出现 File load version conflict。实际使用前需匹配版本。它不是全局 File > New 钩子。
