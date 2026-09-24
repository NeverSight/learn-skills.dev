---
name: create-skill
description: >
  新規スキルを skills/<name>/SKILL.md として scaffold する。命名・配置の重複確認、SKILL.md 作成、
  symlink 設定、品質チェック、CLAUDE.md 反映までを一貫して自動化。「スキル作って」「新しいスキルを追加」
  「create-skill」などで使用。Agent 定義の追加は create-agent、ドキュメント更新は update-docs を参照。
model: sonnet
user-invocable: true
argument-hint: "<skill-name> (例: create-skill summarize-pr)"
---

# create-skill

新規スキルを `skills/<name>/SKILL.md` として scaffold し、symlink と品質チェックまで自動化する。

## 使い方

```
/create-skill summarize-pr        # スキルを新規作成
/create-skill                     # 引数省略時はスキル名をインタラクティブに確認
```

| 引数 | 必須 | 説明 |
| --- | --- | --- |
| `skill-name` | 任意 | 作成するスキル名（kebab-case）。省略時は Step 1 の前にインタラクティブに確認する |

main（このスキル自身）は計画・委譲・統合・報告に徹し、SKILL.md の執筆やレビューは専門 Agent に委譲する（`.claude/rules/delegation.md` 準拠）。

スキルの雛形は本スキル同梱の `sample/SKILL.sample.md` を参照します。

## subagent フォールバック（skills add 導入先向け）

本スキルが委譲する subagent（`skill-explorer`・`skill-author`・`skill-reviewer`・`frontmatter-linter`）は Fandhe-AI/agent-cli-skills リポジトリの `.claude/agents/` 定義を前提とする。**導入先リポジトリに該当 subagent が存在しない場合は委譲せず、各 Step の委譲プロンプトに記載した確認観点・入力・必須項目を main が直接実行する**。`frontmatter-linter` の代替としては Step 4 の検証観点の手動確認で足りる。導入先ではスキル実体が `.agents/skills/` に置かれるため、検索対象・出力先のパスは導入先の配置に読み替える。

## フロー

### Step 1: 既存スキルの重複確認（skill-explorer に委譲）

**skill-explorer（subagent_type: skill-explorer）**に委譲して以下を確認させる（存在しない場合は「subagent フォールバック」に従い main が直接確認する。以降の Step も同様）。

```
subagent_type: skill-explorer
prompt: |
  目的: 指定された名前のスキルが既に存在しないか確認する
  入力:
    - 作成予定のスキル名: <skill-name>
    - 検索対象: skills/ 配下の全ディレクトリ、.claude/skills/ 配下の symlink
  確認観点:
    1. skills/<skill-name>/ が既に存在するか
    2. 類似名（例: kebab-case 変形や別表記）のスキルが存在するか
    3. 既存スキルで同等の機能が提供されていないか
  適用ルール: .claude/rules/delegation.md
  出力: 重複なし / 重複あり（ファイルパスと既存スキルの概要）
```

重複が見つかった場合はユーザーに通知し、新規作成か既存スキルの更新かを確認してから続行する。

### Step 2: frontmatter・本文の設計と SKILL.md 作成（skill-author に委譲）

**skill-author（subagent_type: skill-author）**に委譲して `SKILL.md` を作成させる。

委譲プロンプトには以下を含める:

```
subagent_type: skill-author
prompt: |
  目的: <skill-name> の SKILL.md を新規作成する
  入力:
    - スキル名: <skill-name>
    - ユーザーから受け取った役割説明・要件（あれば）
    - 雛形: 本スキル同梱の sample/SKILL.sample.md
    - 既存スキルの参考例: skills/contribute-skill/SKILL.md, skills/update-docs/SKILL.md
  出力先: skills/<skill-name>/SKILL.md
  適用ルール:
    - .claude/rules/skill-authoring.md（frontmatter・本文構成・model 選定・セキュリティ self-check）
    - .claude/rules/description-style.md（description の発火トリガー語・YAML 落とし穴）
    - .claude/rules/delegation-impl.md（委譲設計が必要な場合）
  必須項目:
    - frontmatter: name（ディレクトリ名と一致）, description（発火トリガー語を含む）, model, user-invocable
    - 本文: ## 使い方 → ## フロー（Step N）→ ## 検証 → ## 注意事項
    - description に # を含む場合はクォートで囲む
    - 作業を委譲する設計の場合は subagent_type を明記する
    - 同梱スクリプトを配置する場合はディレクトリ名を scripts/（複数形）とする
```

### Step 3: symlink を作成する

`skill-author` の完了後、シンボリックリンクを作成する。

```bash
ln -s ../../skills/<skill-name> .claude/skills/<skill-name>
```

symlink 作成後に以下で確認する。

```bash
ls -la .claude/skills/<skill-name>
```

### Step 4: 品質チェック（skill-reviewer と frontmatter-linter に委譲）

**skill-reviewer（subagent_type: skill-reviewer）**と **frontmatter-linter（subagent_type: frontmatter-linter）**に並列委譲して検証させる。

```
subagent_type: skill-reviewer
prompt: |
  目的: 新規作成した SKILL.md の品質をレビューする
  入力:
    - 対象ファイル: skills/<skill-name>/SKILL.md
  観点:
    - `skill-authoring.md` 規約への準拠（frontmatter 項目、本文構成）
    - セキュリティ self-check（APIキーのハードコード、フック回避コマンドの不在）
    - トリガー語・引数ヒントの適切さ
    - 同梱スクリプトのディレクトリ名が `scripts/`（複数形）になっているか
  適用ルール: .claude/rules/skill-authoring.md, .claude/rules/security.md
```

```
subagent_type: frontmatter-linter
prompt: |
  目的: 新規作成した SKILL.md の frontmatter・symlink を機械検証する
  入力:
    - 対象ファイル: skills/<skill-name>/SKILL.md
    - symlink: .claude/skills/<skill-name>
  観点:
    - `name` がディレクトリ名と一致しているか
    - `model` が規定値（haiku/sonnet/opus）のいずれかか
    - `user-invocable` の有無と symlink の整合性
    - `description` 内の `#` がクォートで囲まれているか
  適用ルール: .claude/rules/skill-authoring.md
```

レビュー結果に問題があれば `skill-author` に差し戻して修正させる。

### Step 5: update-docs での CLAUDE.md 更新を案内する

スキル追加が完了したら以下を案内する（ユーザーの指示があれば `update-docs` スキルをそのまま呼び出してもよい）。

```
✅ skills/<skill-name>/SKILL.md を作成しました。
✅ .claude/skills/<skill-name> → ../../skills/<skill-name> の symlink を作成しました。

CLAUDE.md のスキル一覧・構造ツリーを更新するには:
  /update-docs
を実行してください。
```

### Step 6: コミットする（任意）

ユーザーからコミットの指示があれば `create-commit` スキルでコミットを作成する。指示がない場合は変更をステージしたまま報告のみ行う。

## 検証

- [ ] `ls skills/<skill-name>/SKILL.md` でファイルが存在することを確認する
- [ ] `ls -la .claude/skills/<skill-name>` で symlink が正しいリンク先を指すことを確認する
- [ ] `head -10 skills/<skill-name>/SKILL.md` で frontmatter が正しく記述されていることを確認する
- [ ] skill-reviewer と frontmatter-linter の検証が PASS していることを確認する
- [ ] 同梱スクリプトがある場合は `scripts/`（複数形）ディレクトリに配置されていることを確認する

## 注意事項

- **symlink の相対パス**: `.claude/skills/<name>` からの相対パスは `../../skills/<name>` とする（絶対パス不可）
- **ディレクトリ名と name の一致**: frontmatter の `name:` はディレクトリ名と完全一致させる
- **`#` を含む description**: YAML コメント扱いを防ぐためクォートで囲む（規約 e83e1bb 参照）
- **スクリプト同梱時の命名**: スキルにスクリプトを同梱する場合はディレクトリ名を `scripts/`（複数形）に統一する（`script/` は使用しない）
- **update-docs の実行**: スキル追加後は必ず `/update-docs` で `CLAUDE.md` を最新化する
- **委譲の連鎖**: `skill-author` が別の Agent をさらに委譲する場合がある。承認フローが必要なスキルは事前に要件を確認する

## 関連

**Agents**: skill-explorer, skill-author, skill-reviewer, frontmatter-linter

**Rules**: delegation, skill-authoring, description-style

**Skills**: create-agent, update-docs, create-commit
