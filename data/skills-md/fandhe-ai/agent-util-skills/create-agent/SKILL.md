---
name: create-agent
description: "新規サブエージェント定義を scaffold する。カテゴリ選定・ファイル作成・model/tools 最小権限設定・品質チェックまでを一貫して自動化。「Agent 作って」「サブエージェント追加」「create-agent」などで使用。"
model: sonnet
user-invocable: true
argument-hint: "<category>/<agent-name> (例: create-agent quality/lint-runner)"
---

# create-agent

新規サブエージェント定義を `.claude/agents/<category>/<name>.md` として scaffold し、品質チェックまで自動化します。

## 使い方

```
/create-agent quality/lint-runner     # カテゴリ指定で作成
/create-agent research/doc-fetcher    # research カテゴリに追加
/create-agent author/template-writer  # author カテゴリに追加
/create-agent                         # 引数省略時はインタラクティブに確認
```

サブエージェントの雛形は本スキル同梱の `sample/agent.sample.md` を参照します。

## カテゴリと model 選定指針

| カテゴリ | パス | 役割 | 推奨 model |
|---------|------|------|-----------|
| research/ | `.claude/agents/research/` | 調査・情報収集・WebFetch | `sonnet` |
| author/ | `.claude/agents/author/` | 作成・編集（Edit/Write/Bash を使用） | `sonnet` |
| quality/ | `.claude/agents/quality/` | レビュー・lint・検証（読み取り専用） | `sonnet`（推論・レビュー）/ `haiku`（機械的 lint のみ） |

### model 詳細基準

| ユースケース | model |
|-----------|-------|
| 機械的・集計・lint・frontmatter 検証 | `haiku` |
| 読解・生成・レビュー・調査 | `sonnet` |
| 複雑な設計判断・アーキテクチャ | `opus` |

### tools 最小権限原則

| Agent カテゴリ | 許可ツール |
|-------------|-----------|
| 読み取り専用（research/・quality/） | `Read`・`Glob`・`Grep` のみ |
| 作成・編集（author/） | 上記 + `Edit`・`Write`・`Bash` |

読み取り専用 Agent には `Edit`・`Write`・`Bash` を **含めない**。

## subagent フォールバック（skills add 導入先向け）

本スキルが委譲する subagent（`agent-author`・`frontmatter-linter`）は Fandhe-AI/agent-cli-skills リポジトリの `.claude/agents/` 定義を前提とする。**導入先リポジトリに該当 subagent が存在しない場合は委譲せず、各 Step の委譲プロンプトに記載した入力・適用ルール・必須項目を main が直接実行して同じ成果物を作成する**。`frontmatter-linter` の代替としては Step 4 の検証観点の手動確認で足りる。適用ルール（`dotclaude-via-temp.md` 等）は導入先に存在するもののみ適用し、存在しない場合は `.claude/agents/` へ直接作成してよい。

## フロー

### Step 1: カテゴリと responsibilities を確認する

引数から `<category>/<agent-name>` を解析する。

- カテゴリが `research/`・`author/`・`quality/` のいずれかであることを確認する
- 上記以外のカテゴリが指定された場合はユーザーに確認して適切なカテゴリを選択する
- Agent の責務（担当スコープ、委譲される場面）をユーザーに確認する

### Step 2: agent-author に委譲してファイルを作成する

**agent-author（subagent_type: agent-author）**に委譲してファイルを作成させる（存在しない場合は「subagent フォールバック」に従い main が直接作成する）。

**重要**: `agent-author` は `dotclaude-via-temp.md` に従い、`_/dotclaude/agents/<category>/<name>.md` を経由して最終配置する（`.claude/agents/` への直接書き込みは行わない）。

委譲プロンプト例:

```
subagent_type: agent-author
prompt: |
  目的: <category>/<agent-name> のサブエージェント定義を作成する
  入力:
    - Agent 名: <agent-name>
    - カテゴリ: <category>（research/author/quality/）
    - 役割・責務: <ユーザーから受け取った内容>
    - 雛形: 本スキル同梱の sample/agent.sample.md
    - 既存 Agent の参考: .claude/agents/ 配下の既存ファイル
  出力先: .claude/agents/<category>/<agent-name>.md
  適用ルール:
    - .claude/rules/agent-authoring.md（frontmatter・tools 最小権限・カテゴリ配置・本文骨子）
    - .claude/rules/dotclaude-via-temp.md（_/dotclaude/ 経由で作成して mv で最終配置）
  必須項目:
    - frontmatter: name（kebab-case）, description（委譲される場面を具体的に記載）,
                   model（選定基準に従う）, tools（最小権限の原則）
    - 本文: # Agent名 → ## 役割 → ## 対象スコープ → ## 遵守する規約 → ## 手順/観点 →
            ## 完了条件 → ## 報告フォーマット
    - 読み取り専用 Agent には Edit・Write・Bash を含めない
```

### Step 3: model 選定と tools 設定を確認する

`agent-author` の作成結果を確認し、以下を検証する。

- `model` がカテゴリ・用途に合った選定になっているか
- `tools` が最小権限原則を守っているか
- `quality/` カテゴリなのに `Edit`・`Write`・`Bash` が含まれていないか

### Step 4: frontmatter-linter で検証する

**frontmatter-linter（subagent_type: frontmatter-linter）**に委譲して検証させる（存在しない場合は下記観点の手動確認で代替する）。

検証観点:
- `name` が kebab-case で正しく設定されているか
- `model` が規定値（haiku/sonnet/opus）のいずれかか
- `tools` に最小権限を超えるものが含まれていないか
- `description` が委譲される場面を具体的に説明しているか
- `.claude/agents/<category>/` に正しく配置されているか

問題があれば `agent-author` に差し戻して修正させる。

### Step 5: CLAUDE.md の Sub-agents 表更新を案内する

Agent 追加が完了したら以下を案内する。

```
✅ .claude/agents/<category>/<agent-name>.md を作成しました。

Agent の frontmatter 概要:
  name: <agent-name>
  model: <model>
  tools: [<tool-list>]

CLAUDE.md の Sub-agents 表・構造ツリーを更新するには:
  /update-docs
を実行してください。

このサブエージェントを呼び出すには、スキル内で以下を使用します:
  subagent_type: <agent-name>
```

## 検証

1. `.claude/agents/<category>/<agent-name>.md` が正しいパスに存在することを確認する（`agent-author` が dotclaude-via-temp に従い `_/dotclaude/agents/` への一時作成から `.claude/agents/` への `mv` まで一貫して実行するため、`create-agent` 側で `mv` を別途実行する必要はない）
2. frontmatter の `name:` フィールドが `<agent-name>` と一致していることを確認する
3. `tools` リストがカテゴリの最小権限ポリシーを遵守していることを確認する
4. `subagent_type: <agent-name>` で呼び出せる状態になっているか確認する

## 注意事項

- **dotclaude-via-temp 必須**: `agent-author` は `.claude/agents/` に直接書き込まず、`_/dotclaude/agents/` への一時作成から `.claude/agents/` への `mv` まで一貫して実行する。`create-agent` 側で `mv` を別途実行する必要はない（詳細: `.claude/rules/dotclaude-via-temp.md`）
- **`rm -rf _/dotclaude` は禁止**: `rmdir` で空ディレクトリのみ削除する（他の並行作業との共有ディレクトリ）
- **読み取り専用 Agent の tools**: `research/` と `quality/` カテゴリには `Edit`・`Write`・`Bash` を含めない
- **name の解決**: `subagent_type:` による呼び出しは frontmatter の `name:` フィールドで解決される。カテゴリを移動しても呼び出しコードの変更が不要
- **update-docs の実行**: Agent 追加後は必ず `/update-docs` で `CLAUDE.md` を最新化する
