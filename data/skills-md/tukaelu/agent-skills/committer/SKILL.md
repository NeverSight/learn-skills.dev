---
name: committer
disable-model-invocation: true
description: >
  gitコマンドで変更されたファイルを分析し、論理的な単位で適切な粒度のコミットを作成する。
  「/committer」「committer スキルを使って」「committer でコミットして」のように、
  スキル名（committer）を明示的に指定した場合のみ起動する。
  「コミットして」「git commit して」などの一般的なリクエストでは起動しない。
allowed-tools:
  - Bash(git *)
  - Glob
  - Grep
  - Read
  - AskUserQuestion
---

# Committer

変更ファイルを分析して関連する変更をグループ化し、適切な粒度でコミットを作成する。

## ワークフロー

### Step 1: 現在の状態を把握する

変更内容とプロジェクトのコミットスタイルを確認する：

```bash
git branch --show-current
git config --get commit.gpgsign
git status
git diff --stat HEAD
git log --oneline -10
```

**GPG 署名が有効な場合（`commit.gpgsign=true`）はフラグを立てておく。**
この時点ではユーザーへの確認は行わない。Step 4 の承認後、Step 5 の実行前に確認する。

**main / master ブランチの場合は必ずユーザーに確認する。**
現在のブランチが `main` または `master` であれば、コミットの前に AskUserQuestion で確認する：

```javascript
AskUserQuestion({
  questions: [{
    question: "現在 main ブランチにいます。このままコミットしますか？",
    header: "ブランチ確認",
    options: [
      { label: "main のままコミット",   description: "現在のブランチに直接コミットする" },
      { label: "作業ブランチを作成",     description: "新しいブランチを作成してからコミットする" }
    ],
    multiSelect: false
  }]
})
```

「作業ブランチを作成」を選んだ場合は、続けてブランチ名をテキストで質問し、指定された名前で `git checkout -b <branch>` を実行してから処理を続ける。

既にステージ済みのファイルがある場合は、ユーザーに意図を確認してから進む：
- そのままコミットする（Step 4 へ）
- 未ステージ分も含めて分析する（Step 2 へ）

### Step 2: 変更内容を読んで意図を把握する

Step 1 の stat で把握したファイルごとに差分を読んで変更意図を理解する。以下の観点で分析する：

- **変更の種類**: 機能追加 / バグ修正 / リファクタリング / テスト追加 / 設定変更 / ドキュメント更新
- **変更の目的**: なぜ変更したか（同じ目的に属するかどうかの判断軸）
- **ファイル間の関連性**: 一緒に変えると意味をなす組み合わせを探す

```bash
git diff HEAD -- <file>
```

未追跡の新規ファイルは `git diff HEAD` に含まれないため、Read で内容を確認する。

### Step 3: 変更をグループ化してコミット計画を立てる

以下の原則でグループ化する：

**まとめてよい変更**
- 同じ機能・目的に属するソースファイルとテスト
- 同じバグ修正の一連のファイル
- 同じリファクタリング対象

**別コミットにすべき変更**
- 目的が異なる（機能追加 vs バグ修正 vs リファクタリングなど）
- 独立している（一方が他方に依存しない）
- 影響範囲が違う（アプリコード / 設定 / ドキュメント / CI など）

1つの変更ファイルに複数の意図が混在する場合は、`git add -p` で部分ステージを検討する。

### Step 4: 計画をユーザーに提示して確認を取る

**実行前に必ず確認する**。以下の形式で提案する：

```
提案するコミット（N件）：

コミット 1: feat(auth): JWTトークンによる認証を実装
  対象ファイル:
    - src/auth/jwt.ts（新規）
    - src/auth/middleware.ts（変更）
    - tests/auth/jwt.test.ts（新規）

コミット 2: chore: ESLint設定を更新
  対象ファイル:
    - .eslintrc.json（変更）

この内容で進めますか？
```

修正を求められたらグループ分けを調整して再提案する。

### Step 5: グループごとにコミットを実行する

承認を得たら、コミット実行前に GPG フラグが立っている場合は AskUserQuestion で確認する：

```javascript
AskUserQuestion({
  questions: [{
    question: "GPG 署名が有効になっています。Claude Code はパスフレーズを入力できないため、このセッションでは --no-gpg-sign でコミットします。よいですか？",
    header: "GPG 署名",
    options: [
      { label: "--no-gpg-sign でコミット", description: "このセッションのみ GPG 署名をスキップする" },
      { label: "キャンセル",              description: "処理を中断する（ターミナルから手動でコミットしてください）" }
    ],
    multiSelect: false
  }]
})
```

「キャンセル」を選んだ場合、Step 4 で確認済みのコミット計画をコマンド形式で出力して処理を終了する：

```
GPG 署名が必要なため処理を中断しました。
ターミナルから以下のコマンドを実行してください：

# コミット 1
git add src/auth/jwt.ts src/auth/middleware.ts tests/auth/jwt.test.ts
git commit -m "feat(auth): JWTトークンによる認証を実装

既存のセッション認証を置き換える形で JWT を導入した。"

# コミット 2
git add .eslintrc.json
git commit -m "chore: ESLint設定を更新"
```

「--no-gpg-sign でコミット」を選んだ場合、グループ順にコミットを作成する。

**body が必要な場合**（変更の背景・理由・詳細を補足したいとき）：

```bash
git add <file1> <file2> ...
git commit [--no-gpg-sign] -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<変更の背景・理由・詳細>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

**body が不要な場合**（subject だけで意図が伝わるとき）：

```bash
git add <file1> <file2> ...
git commit [--no-gpg-sign] -m "$(cat <<'EOF'
<type>(<scope>): <subject>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

`[--no-gpg-sign]` は GPG フラグが立っておりユーザーが承認した場合のみ付与する。

全グループ完了後、`git log --oneline -N`（N はコミット数）で作成を確認してから一覧を報告する：

```bash
git log --oneline -3
```

```
✓ 2件のコミットを作成しました

  abc1234 feat(auth): JWTトークンによる認証を実装
  def5678 chore: ESLint設定を更新
```

---

## コミットメッセージの書き方

以下の形式を使う：

```
<type>(<scope>): <subject>

<body>
```

- **subject**: コミットの概要を1行で簡潔に記述する
- **body**: 変更の背景・理由・詳細が必要な場合のみ記載する。不要なら省略してよい

| type | 用途 |
|------|------|
| feat | 新機能 |
| fix | バグ修正 |
| refactor | リファクタリング（動作変更なし） |
| test | テストの追加・修正 |
| docs | ドキュメント変更 |
| chore | ビルド・CI・設定などの雑務 |
| style | フォーマット変更（動作変更なし） |

日本語プロジェクトでは日本語メッセージも適切。

---

## 注意事項

- **push はしない**: コミット作成のみ行う。push はユーザーが判断する
- **バイナリファイル**: 差分が読めないため、ファイル名と用途から意図を推測してユーザーに確認する
- **大量変更（50ファイル以上）**: まず変更の全体像を説明してからグループ化の方針を相談する
- **機密ファイル**: `.env` や認証情報を含むファイルはコミットに含める前に警告する
- **pre-commit hook が失敗した場合**: hook のエラー内容を確認して修正し、再度コミットを試みる。`--no-verify` はユーザーが明示的に要求した場合のみ提案する
- **コミット対象がない場合**: ステージ対象ファイルがない旨をユーザーに伝え、`git status` の結果を示す
