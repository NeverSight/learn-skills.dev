---
name: openai-agents
description: >
  OpenAI API (developers.openai.com) の Agents SDK (Python / TypeScript) リファレンス。
  Agent, Runner, handoffs, guardrails, tracing、
  built-in tools（web search, file search, computer use, code interpreter, image generation）、
  function tools, vector stores, MCP (Model Context Protocol) connectors,
  background mode, multi-agent orchestration、
  SandboxAgent（隔離実行環境）。
user-invocable: false
---

## スコープ

Nous Research の `hermes-agent`（サードパーティ AI CLI）とは別物。Responses API 本体は `openai-api-core` スキル、Codex CLI は `openai-codex` スキルが担当する（本スキルは Agents SDK / built-in tools / MCP / orchestration に特化）。本スキルの MCP は Agents SDK から MCP サーバー・connectors を消費する側であり、MCP サーバーを ChatGPT アプリとして公開する側（`window.openai`, `registerAppTool`, ChatGPT UI コンポーネント）は `openai-apps-sdk` スキルが扱う。クロススキル参照は名前のみで行い、相対リンクは張らない。

## ディレクトリ構成

```text
skills/openai-agents/
  SKILL.md
  references/
    agents-sdk/
      README.md
      overview.md
      quickstart.md
      define-agents.md
      models-and-providers.md
      running-agents.md
      results-and-state.md
      sandboxes.md
    tools/
      README.md
      tools-overview.md
      web-search.md
      file-search.md
      vector-stores.md
      code-interpreter.md
      computer-use.md
      image-generation.md
      shell.md
      local-shell.md
      apply-patch.md
      function-tools.md
      tool-search.md
      programmatic-tool-calling.md
      skills.md
    mcp/
      README.md
      mcp-and-connectors.md
      agents-sdk-integration.md
      realtime-sessions.md
      secure-mcp-tunnel.md
    orchestration/
      README.md
      handoffs-and-agents-as-tools.md
      multi-agent.md
      guardrails-and-human-review.md
      background-mode.md
      tracing.md
  samples/
    README.md
    single-agent-function-tool.md
    web-search-tool.md
    file-search-tool.md
    remote-mcp-server.md
    multi-agent-handoffs.md
    input-guardrails.md
    streaming-output.md
  scripts/
    README.md
    install.md
    environment.md
    tracing.md
    run.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Agent の定義・実行・conversation state・streaming を知りたい | agents-sdk | [references/agents-sdk/README.md](references/agents-sdk/README.md) |
| モデル/provider の選択、SDK 全体像を知りたい | agents-sdk | [references/agents-sdk/README.md](references/agents-sdk/README.md) |
| SandboxAgent でファイルシステム/shell 等の隔離実行環境を使いたい | agents-sdk | [references/agents-sdk/README.md](references/agents-sdk/README.md) |
| web search / file search / code interpreter / computer use 等の built-in tool を使いたい | tools | [references/tools/README.md](references/tools/README.md) |
| function tool の定義や vector store の作成・検索を知りたい | tools | [references/tools/README.md](references/tools/README.md) |
| shell tool に Agent Skills（SKILL.md バンドル）をアタッチしたい | tools | [references/tools/README.md](references/tools/README.md) |
| remote MCP server / connectors への接続・認証を知りたい | mcp | [references/mcp/README.md](references/mcp/README.md) |
| Agents SDK からの MCP tool 統合や Realtime セッションでの MCP 利用を知りたい | mcp | [references/mcp/README.md](references/mcp/README.md) |
| handoffs / agents-as-tools でマルチエージェント構成を組みたい | orchestration | [references/orchestration/README.md](references/orchestration/README.md) |
| guardrails・human review・tracing・background mode を設定したい | orchestration | [references/orchestration/README.md](references/orchestration/README.md) |
| 典型的な使い方を知りたい | samples | [samples/README.md](samples/README.md) |
| インストール・環境変数・トレーシング設定・実行コマンドを知りたい | scripts | [scripts/README.md](scripts/README.md) |
