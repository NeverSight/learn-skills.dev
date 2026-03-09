---
name: gog
description: >
  Google Workspace CLI (gog v0.10.0) for Gmail, Calendar, Drive, Sheets, Docs, Contacts, Tasks.
  「メール送って」「カレンダー見せて」「ドライブにアップロード」「スプシ作成」「連絡先検索」「タスク追加」などで発火。
  認証済みアカウント: (gogで認証したアカウント)
---

# gog - Google Workspace CLI (v0.10.0)

Google サービスを操作するCLIツール。

**アカウント:** your-account@gmail.com (default)

**実行パス:** `gog`

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定（API応答待ちのため）
- 長いリスト取得は `--max` で制限

---

## Gmail

### メール検索

```bash
# 基本検索
gog gmail search "検索クエリ"
gog gmail search "from:someone@example.com"
gog gmail search "is:unread" --max 10
gog gmail search "subject:請求書 after:2026/01/01"

# 全ページ取得
gog gmail search "label:重要" --all
```

**検索クエリ例:**
- `is:unread` - 未読
- `from:xxx` - 送信者
- `to:xxx` - 宛先
- `subject:xxx` - 件名
- `has:attachment` - 添付あり
- `after:YYYY/MM/DD` - 日付以降
- `label:xxx` - ラベル

### メール取得

```bash
# メッセージ取得
gog gmail get <messageId>
gog gmail get <messageId> --body  # 本文込み

# 添付ファイルダウンロード
gog gmail attachment <messageId> <attachmentId>
```

### メール送信

```bash
# 基本送信
gog gmail send --to "recipient@example.com" --subject "件名" --body "本文"

# CC/BCC付き
gog gmail send --to "a@b.com" --cc "c@d.com" --bcc "e@f.com" --subject "件名" --body "本文"

# 添付ファイル付き
gog gmail send --to "a@b.com" --subject "件名" --body "本文" --attach "./file.pdf"

# スレッドに返信
gog gmail send --thread-id <threadId> --to "a@b.com" --subject "Re: 件名" --body "返信本文"

# 全員に返信
gog gmail send --reply-to-message-id <messageId> --reply-all --subject "Re: 件名" --body "返信"
```

**送信オプション:**
| オプション | 説明 |
|-----------|------|
| `--to` | 宛先（カンマ区切り） |
| `--cc` | CC |
| `--bcc` | BCC |
| `--subject` | 件名 |
| `--body` | 本文（プレーンテキスト） |
| `--body-html` | HTML本文 |
| `--body-file` | 本文ファイル |
| `--attach` | 添付ファイル（複数可） |
| `--thread-id` | スレッドID（返信時） |
| `--reply-to-message-id` | 返信元メッセージID |
| `--reply-all` | 全員に返信 |

### ラベル操作

```bash
# ラベル一覧
gog gmail labels list

# ラベル追加/削除
gog gmail thread modify <threadId> --add-labels "INBOX" --remove-labels "UNREAD"
```

---

## Calendar

### 予定一覧

```bash
# 今後の予定（デフォルト7日間）
gog calendar events
gog calendar events --max 20

# 期間指定
gog calendar events --from "2026-02-01" --to "2026-02-28"

# 特定カレンダー
gog calendar events primary
gog calendar events "user@example.com"
```

### 予定作成

```bash
# 通常の予定
gog calendar create primary --summary "ミーティング" --from "2026-02-15T10:00:00+09:00" --to "2026-02-15T11:00:00+09:00"

# 終日予定
gog calendar create primary --summary "休暇" --from "2026-02-20" --to "2026-02-21" --all-day

# 場所・参加者付き
gog calendar create primary --summary "会議" --from "2026-02-15T14:00:00+09:00" --to "2026-02-15T15:00:00+09:00" \
  --location "会議室A" --attendees "a@b.com,c@d.com"

# Google Meet付き
gog calendar create primary --summary "オンラインMTG" --from "2026-02-15T10:00:00+09:00" --to "2026-02-15T11:00:00+09:00" --with-meet

# リマインダー付き
gog calendar create primary --summary "MTG" --from "2026-02-15T10:00:00+09:00" --to "2026-02-15T11:00:00+09:00" --reminder "popup:30m" --reminder "email:1d"
```

**作成オプション:**
| オプション | 説明 |
|-----------|------|
| `--summary` | タイトル |
| `--from` | 開始時刻（RFC3339） |
| `--to` | 終了時刻（RFC3339） |
| `--all-day` | 終日予定 |
| `--location` | 場所 |
| `--description` | 説明 |
| `--attendees` | 参加者（カンマ区切り） |
| `--with-meet` | Google Meet作成 |
| `--reminder` | リマインダー（popup:30m, email:1d等） |
| `--rrule` | 繰り返し |

### 予定更新・削除

```bash
# 更新
gog calendar update primary <eventId> --summary "新タイトル"

# 削除
gog calendar delete primary <eventId>
```

### 検索

```bash
gog calendar search "ミーティング"
```

### カレンダー一覧

```bash
gog calendar calendars
```

---

## Drive

### ファイル一覧

```bash
# ルートフォルダ
gog drive ls

# 特定フォルダ
gog drive ls --parent <folderId>

# 件数制限
gog drive ls --max 20
```

### 検索

```bash
gog drive search "レポート"
gog drive search "mimeType='application/pdf'"
```

### ダウンロード・アップロード

```bash
# ダウンロード
gog drive download <fileId>
gog drive download <fileId> --output "./local-file.pdf"

# アップロード
gog drive upload "./local-file.pdf"
gog drive upload "./file.pdf" --parent <folderId>
```

### フォルダ作成・移動

```bash
# フォルダ作成
gog drive mkdir "新フォルダ"
gog drive mkdir "サブフォルダ" --parent <parentFolderId>

# 移動
gog drive move <fileId> --parent <newFolderId>

# リネーム
gog drive rename <fileId> "新しい名前"
```

### コピー

```bash
gog drive copy <fileId> "コピー名"
gog drive copy <fileId> "コピー名" --parent <folderId>
```

### 共有

```bash
# 共有
gog drive share <fileId> --email "user@example.com" --role reader
gog drive share <fileId> --email "user@example.com" --role writer

# 権限一覧
gog drive permissions <fileId>

# 共有解除
gog drive unshare <fileId> <permissionId>
```

---

## Sheets

### 読み取り

```bash
gog sheets get <spreadsheetId> "シート1!A1:C10"
gog sheets get <spreadsheetId> "シート1!A:A"  # 列全体
```

### 書き込み

```bash
# パイプ区切りで複数セル
gog sheets update <spreadsheetId> "シート1!A1:C1" "値1|値2|値3"

# JSON形式（カンマ・パイプを含むデータ）
gog sheets update <spreadsheetId> "シート1!A1:C2" --values-json '[["名前","金額"],["田中","500,000"]]'
```

### 追加（末尾に行追加）

```bash
gog sheets append <spreadsheetId> "シート1" "値1|値2|値3"
```

### クリア

```bash
gog sheets clear <spreadsheetId> "シート1!A1:C10"
```

### 書式設定

```bash
FMT='{"backgroundColor":{"red":0.2,"green":0.4,"blue":0.7},"textFormat":{"bold":true}}'
gog sheets format <spreadsheetId> "シート1!A1:C1" --format-json "$FMT"
```

### 作成・コピー

```bash
# 新規作成
gog sheets create "新しいスプレッドシート"
gog sheets create "タイトル" --sheets "シート1,シート2,シート3"

# コピー
gog sheets copy <spreadsheetId> "コピー名"
```

### メタデータ・エクスポート

```bash
gog sheets metadata <spreadsheetId>
gog sheets export <spreadsheetId> --format csv
gog sheets export <spreadsheetId> --format xlsx
```

---

## Contacts

### 検索・一覧

```bash
gog contacts list
gog contacts list --max 50
gog contacts search "田中"
```

### 取得・作成

```bash
gog contacts get <resourceName>
gog contacts create --name "山田太郎" --email "yamada@example.com" --phone "090-1234-5678"
```

### 更新・削除

```bash
gog contacts update <resourceName> --name "新しい名前"
gog contacts delete <resourceName>
```

---

## Tasks

### タスクリスト

```bash
gog tasks lists list  # リスト一覧
```

### タスク操作

```bash
# 一覧
gog tasks list <tasklistId>

# 作成
gog tasks add <tasklistId> --title "やること"
gog tasks add <tasklistId> --title "タスク" --notes "詳細メモ" --due "2026-02-20"

# 完了
gog tasks done <tasklistId> <taskId>

# 未完了に戻す
gog tasks undo <tasklistId> <taskId>

# 更新
gog tasks update <tasklistId> <taskId> --title "新タイトル"

# 削除
gog tasks delete <tasklistId> <taskId>

# 完了済みをクリア
gog tasks clear <tasklistId>
```

---

## 共通オプション

| オプション | 説明 |
|-----------|------|
| `--json` | JSON出力 |
| `--plain` | TSV出力 |
| `-a, --account` | アカウント指定 |
| `--max` | 最大件数 |
| `--force` | 確認スキップ |
| `-n, --dry-run` | 実行せずプレビュー |

## Tips

1. **SpreadsheetId**: URL `https://docs.google.com/spreadsheets/d/<ID>/edit` から取得
2. **FileId**: URL `https://drive.google.com/file/d/<ID>/view` から取得
3. **CalendarId**: `primary` でメインカレンダー、または共有カレンダーのメールアドレス
4. **TasklistId**: `gog tasks lists list` で確認
