---
name: gdrive
description: >
  Google ドライブ操作（ファイル検索・アップロード・ダウンロード・共有）を gog CLI (v0.10.0) で行う。
  「ドライブで検索」「ファイルアップロード」「フォルダ作成」「ファイル共有して」
  「ドライブから取得」「ファイル移動」「ドライブの一覧」などで発火。
---

# Google Drive 操作スキル (gog v0.10.0)

gog CLI でGoogleドライブを操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定
- 大きなファイルのアップロード/ダウンロードは `timeout: 300` 推奨

---

## ファイル一覧

### ルートフォルダ

```bash
gog drive ls
gog drive ls --max 20
```

### 特定フォルダ

```bash
gog drive ls --parent <folderId>
```

### 詳細出力

```bash
gog drive ls --json
```

---

## ファイル検索

### テキスト検索

```bash
gog drive search "レポート"
gog drive search "プロジェクト計画"
```

### 高度な検索（Driveクエリ構文）

```bash
# ファイルタイプで絞り込み
gog drive search "mimeType='application/pdf'"
gog drive search "mimeType='application/vnd.google-apps.spreadsheet'"
gog drive search "mimeType='application/vnd.google-apps.document'"

# 特定フォルダ内
gog drive search "name contains '請求書' and '<folderId>' in parents"

# 所有者
gog drive search "name contains 'report' and 'user@example.com' in owners"
```

### MIMEタイプ一覧

| タイプ | MIMEタイプ |
|-------|-----------|
| PDF | `application/pdf` |
| Googleスプレッドシート | `application/vnd.google-apps.spreadsheet` |
| Googleドキュメント | `application/vnd.google-apps.document` |
| Googleスライド | `application/vnd.google-apps.presentation` |
| フォルダ | `application/vnd.google-apps.folder` |
| 画像 | `image/jpeg`, `image/png` |
| Word | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| Excel | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |

---

## ファイル操作

### メタデータ取得

```bash
gog drive get <fileId>
```

### ダウンロード

```bash
gog drive download <fileId>
gog drive download <fileId> --output "./local-file.pdf"
```

### Googleドキュメントのエクスポート

```bash
# スプレッドシート → CSV
gog drive download <spreadsheetId> --export-format csv

# ドキュメント → PDF
gog drive download <docId> --export-format pdf

# スライド → PPTX
gog drive download <slideId> --export-format pptx
```

### アップロード

```bash
gog drive upload "./local-file.pdf"
gog drive upload "./file.xlsx" --parent <folderId>
```

### コピー

```bash
gog drive copy <fileId> "コピー名"
gog drive copy <fileId> "コピー名" --parent <folderId>
```

### 移動

```bash
gog drive move <fileId> --parent <newFolderId>
```

### リネーム

```bash
gog drive rename <fileId> "新しい名前"
```

### 削除

```bash
gog drive delete <fileId>
gog drive delete <fileId> --force  # 確認スキップ
```

---

## フォルダ操作

### フォルダ作成

```bash
gog drive mkdir "新しいフォルダ"
gog drive mkdir "サブフォルダ" --parent <parentFolderId>
```

### フォルダ内一覧

```bash
gog drive ls --parent <folderId>
```

---

## 共有

### 共有設定

```bash
# 閲覧者として共有
gog drive share <fileId> --email "user@example.com" --role reader

# 編集者として共有
gog drive share <fileId> --email "user@example.com" --role writer

# コメント権限
gog drive share <fileId> --email "user@example.com" --role commenter
```

### 権限一覧

```bash
gog drive permissions <fileId>
```

### 共有解除

```bash
gog drive unshare <fileId> <permissionId>
```

### 共有ロール

| ロール | 説明 |
|-------|------|
| `reader` | 閲覧のみ |
| `commenter` | コメント可 |
| `writer` | 編集可 |
| `owner` | オーナー |

---

## URL取得

```bash
gog drive url <fileId>
gog drive url <fileId1> <fileId2> <fileId3>
```

---

## コメント

```bash
# コメント一覧
gog drive comments list <fileId>

# コメント追加
gog drive comments add <fileId> --content "コメント内容"
```

---

## 共有ドライブ

```bash
# 共有ドライブ一覧
gog drive drives
```

---

## 出力オプション

| オプション | 説明 |
|-----------|------|
| `--json` | JSON出力 |
| `--plain` | TSV出力 |
| `--max N` | 最大N件 |

---

## 典型ワークフロー

### ファイル検索→ダウンロード

```bash
# 1. 検索
gog drive search "月次レポート" --json

# 2. ダウンロード
gog drive download <fileId> --output "./月次レポート.pdf"
```

### フォルダ作成→アップロード→共有

```bash
# 1. フォルダ作成
RESULT=$(gog drive mkdir "プロジェクトX資料" --json)
FOLDER_ID=$(echo "$RESULT" | jq -r '.id')

# 2. アップロード
gog drive upload "./proposal.pdf" --parent "$FOLDER_ID"

# 3. 共有
gog drive share "$FOLDER_ID" --email "client@example.com" --role reader

# 4. URL取得
gog drive url "$FOLDER_ID"
```

### スプレッドシートをCSVでダウンロード

```bash
gog drive download <spreadsheetId> --export-format csv --output "./data.csv"
```

---

## FileId の取得方法

URLから抽出:
- `https://docs.google.com/spreadsheets/d/<ID>/edit` → `<ID>` 部分
- `https://drive.google.com/file/d/<ID>/view` → `<ID>` 部分
- `https://docs.google.com/document/d/<ID>/edit` → `<ID>` 部分

---

## ゴミ箱に移動

```bash
gog drive trash <fileId>
```

---

## ブラウザで開く

```bash
gog open <fileId>           # ブラウザでファイルを開く
gog open <url>              # URLを開く
```

---

## トップレベル download / upload

```bash
gog download <fileId>                          # Drive からダウンロード
gog download <fileId> --output "./file.pdf"
gog upload "./local-file.pdf"                  # Drive にアップロード
gog upload "./file.xlsx" --parent <folderId>
```

`gog drive download` / `gog drive upload` と同等のショートカット。

---

## 注意事項

- **ゴミ箱**: `delete` はゴミ箱に移動（完全削除ではない）
- **Google形式**: スプシ/ドキュメントはダウンロード時にエクスポート形式を指定
- **共有ドライブ**: `--shared-drive` オプションが必要な場合あり
- **大きなファイル**: タイムアウトを長めに設定
