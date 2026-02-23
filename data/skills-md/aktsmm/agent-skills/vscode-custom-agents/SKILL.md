---
name: vscode-custom-agents
description: "VS Code カスタムエージェントの配置ルール・アクセス制御・マルチエージェント設計のベストプラクティス。Triggers on 'custom agent', 'agent not found', 'subagent', 'user-invokable', 'エージェント設計', 'ピッカー'."
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
  verified: 2026-02-15
  vscode-version: "1.106+"
---

# VS Code Custom Agents — 配置・設計・アクセス制御

## When to Use

| Action    | Triggers                                                                     |
| --------- | ---------------------------------------------------------------------------- |
| **Create** | 新しい `.agent.md` 作成、マルチエージェント構成セットアップ                  |
| **Debug**  | "Agent not found" エラー、サブエージェント呼び出し失敗、ピッカーに表示されない |
| **Review** | frontmatter の妥当性チェック、アクセス制御の設計レビュー                      |

## 配置ルール（Critical）

### `.github/agents/` は直下のみスキャンされる

```
✅ 認識される
.github/agents/
├── orchestrator.agent.md
├── coding.executor.md
└── quality.reviewer.md

❌ 認識されない
.github/agents/
├── executors/
│   └── coding.executor.md    ← 無視される
└── reviewers/
    └── quality.reviewer.md   ← 無視される
```

> **根拠**: VS Code 公式ドキュメント (2026-02-15 時点)
> `"VS Code detects any .md files in the .github/agents folder of your workspace as custom agents."`
> サブディレクトリの再帰スキャンについて明記なし。実証テストでも非対応を確認。

### 配置場所の選択肢

| 場所 | 用途 |
| --- | --- |
| `.github/agents/` (ワークスペース) | チーム共有。そのワークスペースでのみ有効 |
| ユーザープロファイル | 個人用。全ワークスペースで有効 |
| `chat.agentFilesLocations` 設定 | 追加パスを指定。サブフォルダ指定にも使える |

### ファイル拡張子

| 場所 | 拡張子 |
| --- | --- |
| `.github/agents/` | `.agent.md` または `.md`（どちらも認識される） |
| `.claude/agents/` | `.md`（Claude Code 互換） |

## アクセス制御（3段階）

### frontmatter プロパティ

| プロパティ | デフォルト | 効果 |
| --- | --- | --- |
| `user-invokable` | `true` | `false` → ピッカー (ドロップダウン) に非表示 |
| `disable-model-invocation` | `false` | `true` → 他エージェントからサブエージェントとして呼ばれない |
| `agents` (親側) | `*` (全許可) | 特定エージェント名のリスト → そのサブエージェントのみ許可 |

> **重要**: `agents` リストに明示すると `disable-model-invocation: true` をオーバーライドできる。

### パターン早見表

```yaml
# 1. ユーザーが直接呼ぶ + サブエージェントとしても呼ばれる（デフォルト）
user-invokable: true    # (省略可)

# 2. サブエージェント専用（ピッカー非表示）
user-invokable: false

# 3. ユーザー専用（他エージェントから呼ばれない）
disable-model-invocation: true

# 4. 特定の親からのみ呼ばれるサブエージェント
user-invokable: false
disable-model-invocation: true
# → 親側の agents リストに明示して呼ぶ
```

### ⚠️ Deprecated プロパティ

| 旧 | 新 | 移行方法 |
| --- | --- | --- |
| `infer: true` | `user-invokable: true` (デフォルト) | 行を削除するか置換 |
| `infer: false` | `user-invokable: false` | 置換 |
| `target: vscode` | — | 削除（不要） |

## マルチエージェント設計パターン

### Orchestrator + Workers パターン

```yaml
# orchestrator.agent.md
---
name: orchestrator
user-invokable: true
disable-model-invocation: true
tools: ["codebase", "terminal", "agent"]  # "agent" が必須
agents:
  - coding-executor
  - quality-reviewer
  - auditor
---
```

```yaml
# coding.executor.md
---
name: coding-executor
user-invokable: false
tools: ["codebase", "terminal"]
---
```

**ポイント:**
- orchestrator に `agent` ツールを含めないとサブエージェント呼び出しが機能しない
- `agents` リストで呼び出せるサブエージェントを制限する
- `agents: []` で全サブエージェント利用を禁止
- `agents: '*'` で全許可（デフォルト）

## トラブルシューティング

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| エージェントがピッカーに出ない | サブフォルダに配置 | `.github/agents/` 直下に移動 |
| エージェントがピッカーに出ない | `user-invokable: false` | 意図的なら OK。変更するなら `true` に |
| `runSubagent` で "not found" | ファイルが VS Code に認識されていない | 直下に配置されているか確認 |
| サブエージェントが呼ばれない | 親に `agent` ツールがない | `tools` に `"agent"` を追加 |
| 意図しないエージェントが呼ばれる | `agents` リスト未指定 | 親側で `agents: [...]` を明示 |

## デバッグ方法

1. **Chat Diagnostics**: チャットビューで右クリック → Diagnostics で認識されているエージェント一覧を確認
2. **`runSubagent` テスト**: サブエージェントを直接呼び出して応答にカスタム指示が反映されているか確認
3. **セッションコンテキスト確認**: `<agents>` タグに何が注入されているかで認識状態を判定

## References

- [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Subagents in VS Code](https://code.visualstudio.com/docs/copilot/agents/subagents)
- [Customize AI in VS Code](https://code.visualstudio.com/docs/copilot/customization/overview)
