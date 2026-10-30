# TD MCP bootstrap

Codex skill for preparing a new TouchDesigner project with the locally installed TDMCP component. All generated data goes on D. No plugin binary is redistributed.

Install `skill/` as `D:\Codex\.codex\skills\td-mcp-bootstrap`. Invoke automatically before new TD projects, or with $td-mcp-bootstrap. The local td-general skill also links this workflow.

The script prepares an enabled component copy using Derivative toeexpand/toecollapse, checks builds, and optionally launches and verifies MCP before saving a new project. It preserves authentication and refuses occupied ports and existing output files.

Current validation: offline preparation passes; original plugin SHA256 unchanged; version guard passes. Live startup/save not verified: supplied plugin 1.1.54 was saved in TD 2025.33070, while installed TD is 2025.32460. A test launch showed File load version conflict. Use compatible versions before live use. This is not a global File > New hook.
