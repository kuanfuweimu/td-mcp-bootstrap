# Development log

## 2026-10-31
- Created automatically discoverable td-mcp-bootstrap skill and Python helper.
- Linked installed td-general workflow to the helper.
- Inspected the user-specified local plugin: 1.1.54, save build 2025.33070, Active default off.
- Verified copy/expand/enable/repack without modifying source; observed toeexpand returns 1 even on successful expansion, so validate output artifacts.
- Skill validator passed. Version rejection passed against TD 2025.32460.
- Isolated live launch encountered File load version conflict; stopped only that helper process. Original user TD process preserved. Live MCP/save unverified.
- No plugin binaries, private projects, tokens, or extracted proprietary code included.

---

## 中文开发记录

### 2026-10-31
- 创建可自动发现的 td-mcp-bootstrap 技能及 Python 辅助脚本。
- 将已安装 td-general 工作流连接到辅助脚本。
- 检查用户指定的本地插件：1.1.54，保存构建 2025.33070，Active 默认关闭。
- 在不修改原件的情况下验证复制、展开、启用及重打包；观察到 toeexpand 即使展开成功也返回 1，因此以输出文件校验结果。
- 技能校验通过；针对 TD 2025.32460 的版本拒绝检查通过。
- 隔离实例启动遇到 File load version conflict，仅停止辅助实例，保留用户原 TD 进程。实际 MCP/保存未验证。
- 未包含插件二进制、私有工程、令牌或提取的专有代码。
