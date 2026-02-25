---
name: fetch
description: 使用 fetch 服务器获取网页内容并将内容转换为 Markdown。当需要从互联网获取实时信息或阅读特定网页内容时使用该技能。
---

# MCP Fetch 技能

此技能允许 Agent 使用 Python 脚本调用 Model Context Protocol (MCP) 的 fetch 服务器来抓取网页内容。它特别适合于获取网页内容并将其作为上下文提供给 AI。

## 核心功能

- **自动化抓取**: 自动启动并连接到 `@smithery/mcp-fetch` 服务器。
- **内容提取**: 能够从指定 URL 获取文本内容。
- **无需额外 Python 依赖**: 使用 Python 标准库实现，无需安装额外的 pip 包（只需系统环境中安装了 `node/npx` 和 `python`）。

## 使用指令

1.  **确定目标 URL**: 识别用户需要获取内容的网址。
2.  **调用脚本**: 在项目根目录下，于终端运行以下命令：
    ```bash
    python fetch/fetch.py "https://example.com"
    ```
3.  **处理输出**: 脚本将直接在标准输出中打印网页内容的文本。

## 技术细节

- **通信协议**: 使用 JSON-RPC 2.0 通过标准输入/输出 (stdio) 与 MCP 服务器通信。
- **服务器启动**: 使用 `npx -y @smithery/mcp-fetch` 启动服务器。
- **初始化过程**: 脚本发送 `initialize` 请求并处理 `notifications/initialized` 通知以建立符合 MCP 规范的连接。
- **工具调用**: 通过 `tools/call` 方法调用 `fetch` 工具，支持 `maxLength` 和 `raw` 参数（脚本中默认使用 `maxLength: 20000`）。
