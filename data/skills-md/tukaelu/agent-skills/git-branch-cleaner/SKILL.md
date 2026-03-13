---
name: git-branch-cleaner
argument-hint: "[local|remote|both]"
disable-model-invocation: true
description: >
  指定した起点ブランチにマージ済みの作業ブランチをローカル・リモートから一括削除する。
  「/git-branch-cleaner」「git-branch-cleaner スキルを使って」「git-branch-cleaner で掃除して」のように
  スキル名（git-branch-cleaner）を明示的に指定した場合のみ起動する。
  「ブランチを削除」「merged ブランチを消して」などの一般的なリクエストでは起動しない。
  引数に local / remote / both を指定してスコープを制御できる（省略時は local）。
allowed-tools:
  - Bash(git *)
  - AskUserQuestion
---

# Git Branch Cleaner

起点ブランチにマージ済みの作業ブランチを安全に一括削除する。

## 保護ブランチ

以下のブランチは**いかなる場合も削除しない**：

- `main`, `master`, `develop`, `development`, `staging`, `production`
- 起点ブランチ自身
- 現在チェックアウト中のブランチ（`git branch --show-current` の結果）

このリストに該当するブランチが削除対象に含まれていた場合は、**処理を即座に中断してユーザーに報告する**。削除は一切実行しない。

## スコープの決定

`$ARGUMENTS` に渡された値でスコープを決定する：

| `$ARGUMENTS` | スコープ |
|---|---|
| 空 / `local` | ローカルのみ |
| `remote` | リモートのみ |
| `both` | 両方 |

## ワークフロー

### Step 1: 現在の状態を確認する

現在のブランチとリモートの設定を確認する：

```bash
git branch --show-current
git remote
```

リモートが存在する場合は、マージ済み判定を正確にするために `git fetch --prune` の実行を提案する。未実施だと起点ブランチが古く、削除すべきブランチが検出されない（削除漏れ）可能性がある。ユーザーが同意した場合のみ実行する：

```bash
git fetch --prune
```

### Step 2: 起点ブランチを決定する

ユーザーが起点ブランチを明示していない場合は、以下の順で自動検出を試みる：

1. `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null` でデフォルトブランチを確認
2. `main` → `master` → `develop` の順に `git branch --list` で存在確認

自動検出できた場合はその結果をユーザーに伝えてから続行する。
どれも見つからない場合は AskUserQuestion でユーザーに入力を求める。

### Step 3: マージ済みブランチを検出する

スコープに応じて対象を取得し、冒頭の「保護ブランチ」リストに該当するものをすべて除外する。

**ローカル（scope: local / both）：**

リモートがある場合は `git fetch --prune` 済みのリモート追跡ブランチを基準にすると正確：

```bash
git branch --merged origin/<base-branch>   # リモートがある場合
git branch --merged <base-branch>          # ローカルのみのリポジトリの場合
```

`*` 付きの現在のブランチと保護ブランチをリストから除外する。

**リモート（scope: remote / both）：**

```bash
git branch -r --merged origin/<base-branch>
```

`origin/HEAD` や `origin/<base-branch>` を除外する。表示には `origin/` プレフィックスを除いたブランチ名を使う。

削除対象が 0 件の場合は「削除すべきブランチはありません」と伝えて終了する。

### Step 4: 削除対象をユーザーに提示して確認を取る

**ブランチの削除は取り消しが難しいため、必ず実行前にユーザーの確認を取る。**

以下の形式で一覧を提示する（スコープに応じてセクションを表示）：

```
削除対象ブランチ（N件）：

[ローカル]
  - feature/add-login
  - fix/typo-in-readme

[リモート]
  - feature/add-login
  - fix/api-timeout

起点ブランチ: main
スコープ: both

この内容で削除しますか？
```

### Step 5: ブランチを削除する

確認を得たら、削除実行前に**保護ブランチの二重チェック**を行う。削除対象リストに保護ブランチが1件でも含まれていた場合は処理を即座に中断し、該当ブランチ名とともにユーザーに報告する。削除は一切実行しない。

二重チェックが通過した場合のみ、スコープに応じて削除を実行する。

**ローカルブランチの削除（scope: local / both）：**

マージ済みであることが確認済みなので `-d`（安全削除）を使う。`-D` は使わない：

```bash
git branch -d <branch1> <branch2> ...
```

**リモートブランチの削除（scope: remote / both）：**

部分失敗を正確に把握するため、1ブランチずつ実行して結果を逐次確認する：

```bash
git push origin --delete <branch1>
git push origin --delete <branch2>
...
```

### Step 6: 完了を報告する

削除完了後にブランチ一覧を確認してから報告する（スコープに応じて実行）：

```bash
git branch          # ローカル確認（scope: local / both）
git branch -r       # リモート確認（scope: remote / both）
```

削除結果を報告する：

```
✓ ブランチの削除が完了しました

[ローカル] 2件削除
  - feature/add-login
  - fix/typo-in-readme

[リモート] 2件削除
  - feature/add-login
  - fix/api-timeout
```

---

## 注意事項

- **強制削除は使わない**: `-D` や `--force` は使用しない。`git branch --merged` で確認が取れたブランチのみ削除する
- **現在のブランチ**: チェックアウト中のブランチは削除対象から除外し、ユーザーに通知する
- **リモート名**: デフォルトで `origin` を使用する。`git remote` の結果が複数ある場合または `origin` が存在しない場合は、ユーザーに使用するリモートを確認する
- **ネットワークエラー**: リモート削除が失敗した場合はエラー内容を報告し、成功した分のみ完了として扱う
