---
name: gdocs
description: >
  Google ドキュメント操作（作成・読み取り・書き込み・挿入・検索置換・エクスポート）を gog CLI (v0.10.0) で行う。
  「ドキュメント作って」「Docsに書いて」「ドキュメント読んで」「ドキュメントをエクスポート」
  「ドキュメントコピーして」「テキスト置換して」などで発火。
---

# Google Docs 操作スキル (gog v0.10.0)

gog CLI で Google ドキュメントを操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定
- ドキュメントIDは URL `https://docs.google.com/document/d/<docId>/edit` から取得可能

---

## コマンドリファレンス

### ドキュメント作成

```bash
gog docs create "<title>"
gog docs create "<title>" --parent "<folderId>"    # 特定フォルダに作成
gog docs create "<title>" --file "./content.md"     # Markdownファイルからインポート
```

### ドキュメント情報取得

```bash
gog docs info <docId>
gog docs info <docId> --json
```

### ドキュメント読み取り（プレーンテキスト）

```bash
gog docs cat <docId>
gog docs cat <docId> --tab "<tabTitle>"      # 特定タブのみ
gog docs cat <docId> --all-tabs              # 全タブ表示
gog docs cat <docId> --max-bytes 0           # 制限なし（デフォルト2MB）
```

### ドキュメント書き込み

```bash
# 末尾に追記（デフォルト）
gog docs write <docId> "追加テキスト"
gog docs write <docId> --file "./content.txt"
echo "テキスト" | gog docs write <docId> --file -

# 全体を置換
gog docs write <docId> "新しい内容" --replace
gog docs write <docId> --file "./content.md" --replace --markdown
```

### テキスト挿入（位置指定）

```bash
gog docs insert <docId> "挿入テキスト" --index 1          # 先頭に挿入
gog docs insert <docId> "挿入テキスト" --index 50         # 50文字目に挿入
gog docs insert <docId> --file "./snippet.txt" --index 1
```

### テキスト削除（範囲指定）

```bash
gog docs delete <docId> --start 1 --end 100
```

### 検索置換

```bash
gog docs find-replace <docId> "検索文字列" "置換文字列"
gog docs find-replace <docId> "old" "new" --match-case    # 大文字小文字区別
```

### ドキュメントコピー

```bash
gog docs copy <docId> "コピーのタイトル"
gog docs copy <docId> "コピーのタイトル" --parent "<folderId>"
```

### エクスポート（ダウンロード）

```bash
gog docs export <docId>                              # PDF（デフォルト）
gog docs export <docId> --format docx                # Word形式
gog docs export <docId> --format txt                 # テキスト形式
gog docs export <docId> --format pdf --out "./out.pdf"
```

### タブ一覧

```bash
gog docs list-tabs <docId>
gog docs list-tabs <docId> --json
```

### コンテンツ更新（update）

```bash
gog docs update <docId> --content "新しい内容"                    # 全体置換
gog docs update <docId> --content "追加テキスト" --append          # 末尾追記
gog docs update <docId> --content-file "./doc.md" --format markdown  # Markdown変換
```

---

## 出力オプション

| オプション | 説明 |
|-----------|------|
| `--json` / `-j` | JSON出力 |
| `--plain` / `-p` | TSV出力（パース向け） |
| `--results-only` | JSON時、結果のみ出力 |
| `--select "field1,field2"` | JSON時、フィールド絞り込み |
| `--dry-run` / `-n` | 変更せず意図を表示 |

---

## 典型ワークフロー

### 新規ドキュメント作成→書き込み

```bash
# 1. 作成（IDを取得）
gog docs create "議事録 2026-02-15" --json

# 2. 内容を書き込み
gog docs write <docId> --file "./minutes.md" --replace --markdown
```

### ドキュメント読み取り→編集

```bash
# 1. 内容確認
gog docs cat <docId>

# 2. テキスト置換
gog docs find-replace <docId> "旧プロジェクト名" "新プロジェクト名"
```

### エクスポート

```bash
# PDF出力
gog docs export <docId> --format pdf --out "./report.pdf"

# Word出力
gog docs export <docId> --format docx --out "./report.docx"
```

### テンプレートからコピー

```bash
# 1. テンプレートをコピー
gog docs copy <templateDocId> "新しいドキュメント" --json

# 2. プレースホルダーを置換
gog docs find-replace <newDocId> "{{NAME}}" "田中太郎"
gog docs find-replace <newDocId> "{{DATE}}" "2026年2月15日"
```

### タブ操作

```bash
# タブ一覧を確認
gog docs list-tabs <docId>

# 特定タブの内容を読む
gog docs cat <docId> --tab "Sheet1"

# 全タブの内容を一括表示
gog docs cat <docId> --all-tabs
```

---

## 注意事項

- **ドキュメントの一覧取得**: `gog docs` にはlist コマンドがない。Drive経由で検索する: `gog drive ls --query "mimeType='application/vnd.google-apps.document'"`
- **write のデフォルトは追記**: 全体を書き換える場合は `--replace` を必ず付ける
- **Markdown変換**: `--markdown` は `--replace` と併用が必要（write）。update では `--format markdown` を使う
- **insert の index**: 1始まり。ドキュメント先頭は index=1
- **delete の範囲**: `--start` と `--end` は必須。事前に `cat` で内容を確認してからインデックスを指定
- **大きなドキュメント**: `cat` のデフォルト上限は2MB。`--max-bytes 0` で無制限
- **特殊文字**: シェルエスケープに注意（引用符、改行など）
- **長い本文**: `--file` オプションまたは stdin (`--file -`) を使う
