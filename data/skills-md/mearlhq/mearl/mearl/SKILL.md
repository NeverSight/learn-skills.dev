---
name: mearl
description: 使用 Mearl 复用浏览器登录态，操作或调试网页及已开放 CDP 的 Electron 桌面应用界面，模拟设备、时区或 App 客户端环境（含 JSBridge 与容器栈），运行和验证本地微信小程序，发送 HTTP/Protocol 请求，管理本地、远端浏览器及外部浏览器或设备 Provider；也用于把网站操作或外部浏览器平台沉淀为 Mearl Skill/Provider，安装、更新或卸载 Mearl，以及排查浏览器连接和控制问题。用户未点名 Mearl、只描述这些目标时也应触发；App 客户端或容器模拟仅在明确要求时启用。
version: "3.0.0"
---

# Mearl

`mearl` 命令未安装时，执行 `npx --yes @mearl/setup --skip-skill` 安装本机 CLI 和 Native Host。

配置本机浏览器时，用 `mearl check` 验证连接。需要手动安装扩展时，运行 `npx --yes @mearl/setup extension --extract`，请用户在 `chrome://extensions/` 开启开发者模式并加载命令输出的解压目录。如果连接检查找不到浏览器，请用户在 Mearl Popup 的「设置 → 服务集成」中确认「Agent 服务」已开启，然后重新验证连接。

使用 Mearl 操作浏览器、准备测试环境或调试网络。用户已指定工具或任务正在其他浏览器工具中进行时，沿用其选择，按需补充 Mearl 能力。

操作 Electron 桌面应用时，先读 `mearl guide browsers` 的 Electron/CDP 接入说明；应用须开放 CDP，控制范围是其渲染页面，不包括原生菜单或系统弹窗。

首次使用当前 CLI 版本时读取同版本核心指南：

```bash
mearl guide
```

默认仅加载核心流程；`mearl guide --list` 列出专题，需要时读取单个专题。同一任务内复用已读内容，CLI 更新后重新读取。指南命令只读本地资源；具体参数和返回结构仍以 `mearl <action> --help`、SDK `mearl.help()` 或当前 MCP 工具 schema 为准。

输出缺少 `[mearl:guide] end` 结束行时，保存 stdout 到文件后分段读取，避免把截断内容当作完整指南。

仅能使用 MCP、无法执行 CLI 时，直接使用当前工具说明与 schema，不要求运行指南命令。

App、Provider 和插件的实际可用性以目标浏览器能力目录及已安装能力说明为准。仅在用户明确要求客户端、JSBridge 或容器模拟时启用 App 模式。

运行本地微信小程序或使用其他专用能力时，用 `mearl guide skills` 查阅专用 Skill 的选用和安装说明。用户明确要求执行对应任务且所需插件缺失时，按指南用 Mearl 安装器补装后继续。
