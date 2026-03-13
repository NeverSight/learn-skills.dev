---
name: cosense
description: "Cosense（旧Scrapbox）のページ読み取り・検索・新規作成・編集を行うスキル。環境変数COSENSE_SIDとCOSENSE_PROJECTを使用してAPIを操作する。「Cosenseのページを読みたい」「Cosenseで検索」「Cosenseにページを作成」「Cosenseのページを編集」「スクボ」「scrapbox」などの依頼時に使用。"
---

# Cosense操作スキル

## 前提条件

環境変数が設定されていること：
- `COSENSE_SID` — connect.sidクッキーの値
- `COSENSE_PROJECT` — 操作対象のプロジェクト名
- `COSENSE_BACKUP_DIR`（任意） — バックアップ保存先（デフォルト: `/tmp/cosense_backups`）

**注意**: Claude Codeのシェル環境では `~/.zshrc` の `export` が反映されない場合がある。スクリプトは未設定時に `~/.zshenv` → `~/.zshrc` → `~/.bashrc` の順で自動読み込みを試みるが、確実にするには `~/.zshenv` に記述するのを推奨。

## データ安全ルール（必ず遵守）

1. **書き込み前に必ずユーザーに確認する** — import/safe-importを実行する前に、変更内容をユーザーに提示し、明示的な承認を得る
2. **既存ページの編集には必ず`safe-import`を使う** — `import`ではなく`safe-import`を使うことで自動バックアップされる
3. **新規ページ作成前にタイトル重複を確認する** — `get-page`で同名ページが存在しないことを確認してから作成する。存在する場合はユーザーに警告する
4. **編集時は全行を保持する** — Import APIは全行上書き。変更対象以外の行も必ず含める。行の欠落は絶対に避ける
5. **変更前後のdiffを提示する** — 編集内容をユーザーに見せてから実行する

## 使い方

`scripts/cosense_api.sh` を使って全操作を実行する。API詳細は `references/api.md` を参照。

### ページ読み取り

```bash
bash scripts/cosense_api.sh get-page "ページタイトル"
bash scripts/cosense_api.sh get-page-text "ページタイトル"
bash scripts/cosense_api.sh list-pages 100 0 updated
```

### 検索

```bash
bash scripts/cosense_api.sh search "検索キーワード"
```

### ページ新規作成（安全手順）

```bash
# 1. 同名ページが存在しないことを確認
bash scripts/cosense_api.sh get-page "新しいページ"
# → "lines"が空 or エラーなら新規作成OK
# → 既存ページがあればユーザーに警告して確認

# 2. 内容をユーザーに提示して承認を得る

# 3. 作成実行
bash scripts/cosense_api.sh safe-import '{"pages":[{"title":"新しいページ","lines":["新しいページ","本文1行目","本文2行目"]}]}'
```

### ページ編集（安全手順）

```bash
# 1. 現在の全内容を取得
bash scripts/cosense_api.sh get-page "対象ページ"

# 2. 変更箇所のdiffをユーザーに提示して承認を得る

# 3. safe-importで自動バックアップ＋書き込み（全行を含める）
bash scripts/cosense_api.sh safe-import '{"pages":[{"title":"対象ページ","lines":["対象ページ","既存行1","変更行","既存行3"]}]}'
```

### バックアップ・リストア

```bash
# 手動バックアップ
bash scripts/cosense_api.sh backup "ページタイトル"

# バックアップ一覧
bash scripts/cosense_api.sh list-backups

# リストア（バックアップファイルから復元）
bash scripts/cosense_api.sh restore "/tmp/cosense_backups/project_page_20240101_120000.json"
```

## 注意事項

- Import APIは同タイトルの既存ページを**完全に上書き**する
- `lines`の最初の要素は必ず`title`と一致させる
- 1リクエスト最大30MB
- Cosense記法の詳細は `references/api.md` 末尾を参照
