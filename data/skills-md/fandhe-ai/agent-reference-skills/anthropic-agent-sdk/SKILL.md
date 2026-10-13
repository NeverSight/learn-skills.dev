---
name: anthropic-agent-sdk
description: >
  Claude Agent SDK (code.claude.com/docs/en/agent-sdk) の TypeScript / Python リファレンス。
  query(), ClaudeAgentOptions / Options, custom tools (in-process MCP), createSdkMcpServer,
  hooks, permissions (canUseTool), subagents, sessions (resume / fork), streaming,
  structured outputs, slash commands, tool search, hosting / observability。
user-invocable: false
---

# anthropic-agent-sdk

Claude Agent SDK (code.claude.com/docs/en/agent-sdk) — TypeScript / Python でエージェントをビルドする公式 SDK の
リファレンス。`query()` によるエージェントループ実行、custom tools（in-process MCP）、外部 MCP 接続、hooks、
subagents、permissions（`canUseTool`）、セッションの永続化・再開・分岐、streaming、structured outputs、
本番ホスティングをカバーする。

Claude Code CLI 本体は `anthropic-claude-code` / `anthropic-claude-code-extend`、Messages API 直接呼び出しは
`anthropic-api-core`、Claude API 側の tool use / Agent Skills / MCP は `anthropic-api-tools-mcp` を参照
（本スキルは SDK 経由でエージェントをビルド・運用する側を担当）。

## ディレクトリ構成

```text
skills/anthropic-agent-sdk/
  SKILL.md
  references/
    getting-started/
      README.md
      agent-loop.md
      claude-code-features.md
      migration-guide.md
      overview.md
      quickstart.md
    api-reference/
      README.md
      python.md
      typescript.md
    extending/
      README.md
      custom-tools.md
      hooks.md
      mcp.md
      plugins.md
      skills.md
      slash-commands.md
      subagents.md
      tool-search.md
    sessions-io/
      README.md
      file-checkpointing.md
      session-storage.md
      sessions.md
      streaming-output.md
      streaming-vs-single-mode.md
      structured-outputs.md
      todo-tracking.md
    control/
      README.md
      modifying-system-prompts.md
      permissions.md
      user-input.md
    operations/
      README.md
      cost-tracking.md
      hosting.md
      observability.md
      secure-deployment.md
      troubleshooting.md
  samples/
    README.md
    minimal-agent.md
    custom-tools.md
    mcp-servers.md
    hooks.md
    permissions.md
    subagents.md
    sessions.md
    streaming.md
    structured-outputs.md
    system-prompts.md
  scripts/
    README.md
    setup.md
    runtime.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md`（`samples/` `scripts/` は直下の README.md）を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| Agent SDK の概要・エージェントループの仕組みを知りたい・インストールして最初のエージェントを作りたい・Claude Code SDK からの移行・SDK 内で Claude Code の機能（CLAUDE.md, Agent Skills, hooks）を使いたい | getting-started | [references/getting-started/README.md](references/getting-started/README.md) |
| `query()` や `ClaudeAgentOptions` / `Options` など TypeScript / Python の完全な型・関数シグネチャを確認したい | api-reference | [references/api-reference/README.md](references/api-reference/README.md) |
| custom tools（in-process MCP, `createSdkMcpServer`）を定義したい・外部 MCP サーバーに接続したい・hooks でツール呼び出しを制御したい・plugins / SKILL.md / slash commands / subagents / tool search を扱いたい | extending | [references/extending/README.md](references/extending/README.md) |
| セッションの永続化・再開・分岐（resume / fork）・外部ストレージへの保存・file checkpointing・todo 管理・streaming 出力・structured outputs を扱いたい | sessions-io | [references/sessions-io/README.md](references/sessions-io/README.md) |
| system prompt をカスタマイズしたい・permission mode や `canUseTool` で権限制御したい・ユーザー入力/承認フローを扱いたい | control | [references/control/README.md](references/control/README.md) |
| 本番環境へのホスティング・セキュアなデプロイ・OpenTelemetry での observability・コスト/トークン追跡・エラーのトラブルシューティングを知りたい | operations | [references/operations/README.md](references/operations/README.md) |
| 典型的な使い方を知りたい（最小エージェント, custom tools, MCP サーバー接続, hooks, permissions, subagents, セッション継続, streaming, structured outputs, system prompt カスタマイズ） | samples | [samples/README.md](samples/README.md) |
| SDK インストール・API キー設定・ホスティング用テレメトリー環境変数を知りたい | scripts | [scripts/README.md](scripts/README.md) |
