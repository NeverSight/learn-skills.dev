---
name: impl
description: Spec.mdのTODOリストに基づき実装を進める。各タスク完了後にreview→check→commitを実行。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite, Skill, AskUserQuestion
---

# 実装ワークフロー (Implementation Workflow)

`/spec` で作成されたTODOリストに基づき、順番に実装を進めるスキル。

## 前提条件

- `/spec` によりSpec.mdが作成済み
- TodoWriteでタスクが登録済み

---

## Step 0: 初期設定（初回のみ）

実装を開始する前に、**AskUserQuestion** でreviewとcheckの方法を確認する。

### 質問1: Review方法

```
header: "Review"
question: "コードレビューはどのように行いますか？"
options:
  - label: "セルフレビュー（デフォルト）"
    description: "DRY、複雑性、仕様準拠、セキュリティの観点でチェック"
  - label: "/review スキルを使用"
    description: "プロジェクトのreviewスキルを呼び出す"
  - label: "スキップ"
    description: "レビューせずに進める"
```

### 質問2: Check方法

```
header: "Check"
question: "コミット前のチェックコマンドを教えてください"
options:
  - label: "自動検出"
    description: "package.json, Makefile等から検出"
  - label: "npm run lint && npm run test"
    description: "標準的なnpmスクリプト"
  - label: "make check"
    description: "Makefileのcheckターゲット"
```

ユーザーが「Other」を選んだ場合は、具体的なコマンドを入力してもらう。

---

## ワークフロー

各TODOに対して以下のサイクルを実行:

```
implement → review → check → commit → next
```

### 1. Implement（実装）

- TodoWriteの次のpendingタスクをin_progressに変更
- Spec.mdの該当Acceptance Criteriaを参照
- 必要なコードを実装

### 2. Review（レビュー）

Step 0で選択された方法に従う:

#### セルフレビュー（デフォルト）

| 観点 | チェック内容 |
|------|-------------|
| DRY | コードを無駄にコピペしていないか |
| 複雑性 | やりたいことに対して複雑すぎる手段ではないか |
| 仕様準拠 | Spec.mdの要件を満たしているか |
| Adhoc回避 | 場当たり的な対応になっていないか |
| セキュリティ | OWASP Top 10等のアンチパターンを踏んでいないか |

#### /review スキル使用

`/review` スキルを呼び出す。

### 3. Check（検証）

Step 0で指定されたコマンドを実行。

**判断基準**:
- エラー → 修正して再実行
- 以下は許容（ただしcommitメッセージに明記）:
  - ハリボテ実装による一時的な失敗
  - TDDのRed状態（テスト先行で実装がまだ）
  - 後続タスクで解決予定のエラー

### 4. Commit（コミット）

`/commit` スキルを呼び出してコミット。

**Checkでエラーを許容した場合**のコミットメッセージ例:
```
feat(auth): ログイン画面の雛形を追加

WIP: テストは後続タスクで実装予定のため一部失敗
```

### 5. Next（次へ）

- 完了したタスクをcompletedに更新
- 次のpendingタスクへ進む
- 全タスク完了まで繰り返す

---

## 実行例

```
/impl
```

## 中断・再開

- 途中で中断してもTodoWriteの状態は保持される
- 再度 `/impl` を呼び出すと、in_progressまたは次のpendingから再開
- 再開時はStep 0の設定を再度確認する

## Check コマンドの自動検出（参考）

「自動検出」を選んだ場合の検出元:

| ファイル | 検出するコマンド |
|----------|-----------------|
| `package.json` | scripts内のlint, typecheck, build, test |
| `Makefile` | lint, check, build, test ターゲット |
| `pyproject.toml` | ruff, mypy, pytest等 |
| `Cargo.toml` | cargo check, cargo test, cargo clippy |
