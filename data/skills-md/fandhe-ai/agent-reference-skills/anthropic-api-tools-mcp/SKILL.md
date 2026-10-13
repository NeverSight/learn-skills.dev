---
name: anthropic-api-tools-mcp
description: >
  Claude API (platform.claude.com) の tool use / Agent Skills / MCP リファレンス。
  tool definition (JSON Schema), tool_use / tool_result, server tools（code execution,
  computer use, web search / web fetch, memory tool, tool search）,
  Agent Skills (SKILL.md), Skills API, MCP connector, mcp_servers, MCP tunnels, Tunnels API。
user-invocable: false
---

# anthropic-api-tools-mcp

Claude API (platform.claude.com) — Messages API における tool use（tool definition・client/server tool・
built-in server tools）、Agent Skills（SKILL.md パッケージと Skills API）、MCP connector / MCP tunnels を
カバーする公式リファレンス。

Messages API 本体（streaming / caching / thinking）は `anthropic-api-core`、Claude Code CLI の Skills / MCP 設定は
`anthropic-claude-code-extend`、Agent SDK の Skills / MCP は `anthropic-agent-sdk` を参照（本スキルは Claude API 側の
tool use / Agent Skills / MCP 定義を担当）。

## ディレクトリ構成

```text
skills/anthropic-api-tools-mcp/
  SKILL.md
  references/
    tool-use/
      README.md
      advisor-tool.md
      bash-tool.md
      build-a-tool-using-agent.md
      code-execution-tool.md
      computer-use-tool.md
      define-tools.md
      fine-grained-tool-streaming.md
      handle-tool-calls.md
      how-tool-use-works.md
      manage-tool-context.md
      memory-tool.md
      overview.md
      parallel-tool-use.md
      programmatic-tool-calling.md
      server-tools.md
      strict-tool-use.md
      text-editor-tool.md
      tool-combinations.md
      tool-reference.md
      tool-runner.md
      tool-search-tool.md
      tool-use-with-prompt-caching.md
      troubleshooting-tool-use.md
      web-fetch-tool.md
      web-search-tool.md
    agent-skills/
      README.md
      best-practices.md
      claude-api-skill.md
      enterprise.md
      overview.md
      quickstart.md
    mcp-connector/
      README.md
      mcp-connector.md
      remote-mcp-servers.md
    mcp-tunnels/
      README.md
      concepts.md
      console.md
      deploy-compose.md
      deploy-helm.md
      overview.md
      quickstart.md
      reference.md
      security.md
      troubleshooting.md
    endpoints/
      README.md
      admin-mcp-tunnels.md
      skills-create.md
      skills-delete.md
      skills-list.md
      skills-retrieve.md
      skills-versions-create.md
      skills-versions-delete.md
      skills-versions-download.md
      skills-versions-list.md
      skills-versions-retrieve.md
      tunnels-archive.md
      tunnels-certificates-archive.md
      tunnels-certificates-create.md
      tunnels-certificates-list.md
      tunnels-certificates-retrieve.md
      tunnels-create.md
      tunnels-list.md
      tunnels-retrieve.md
      tunnels-reveal_token.md
      tunnels-rotate_token.md
  samples/
    README.md
    custom-tool-definition.md
    tool-runner.md
    code-execution.md
    web-search-fetch.md
    structured-tool-use.md
    skill-package.md
    mcp-connector.md
    memory-tool.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md`（`samples/` は直下の README.md）を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| tool definition（JSON Schema）を書く・tool_use / tool_result を扱う・client/server tool の区別を知りたい | tool-use | [references/tool-use/README.md](references/tool-use/README.md) |
| server tools（code execution, computer use, web search / web fetch, memory tool, bash, text editor, tool search）を使いたい | tool-use | [references/tool-use/README.md](references/tool-use/README.md) |
| strict tool use・parallel tool use・fine-grained streaming・prompt caching との併用・tool エラーの troubleshooting を知りたい | tool-use | [references/tool-use/README.md](references/tool-use/README.md) |
| Agent Skills（SKILL.md パッケージ）を作る・authoring best practice・enterprise governance を知りたい | agent-skills | [references/agent-skills/README.md](references/agent-skills/README.md) |
| Messages API から remote MCP サーバーに接続する（mcp_servers, mcp_toolset）・third-party MCP directory を知りたい | mcp-connector | [references/mcp-connector/README.md](references/mcp-connector/README.md) |
| private network の MCP サーバーへ MCP tunnels で安全に接続する・Docker Compose / Helm デプロイ・証明書管理を知りたい | mcp-tunnels | [references/mcp-tunnels/README.md](references/mcp-tunnels/README.md) |
| Skills API（`/v1/skills`）・Tunnels API（`/v1/tunnels`）の個別エンドポイントのリクエスト・レスポンス仕様を確認したい | endpoints | [references/endpoints/README.md](references/endpoints/README.md) |
| 典型的な使い方を知りたい（tool 定義, tool runner, code execution, web search/fetch, structured tool use, skill package, mcp connector, memory tool） | samples | [samples/README.md](samples/README.md) |
