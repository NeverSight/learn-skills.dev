---
name: gmail
description: >
  Gmail操作（検索・送信・返信・ラベル管理）を gog CLI (v0.10.0) で行う。
  「メール送って」「〇〇からのメール探して」「未読メール確認」「メールに返信」
  「メール検索」「添付ファイル付きで送信」「メール一覧」などで発火。
---

# Gmail 操作スキル (gog v0.10.0)

gog CLI でGmailを操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定
- 大量検索は `--max` で制限

---

## メール検索

### 基本検索

```bash
gog gmail search "<query>"
gog gmail search "is:unread" --max 10
gog gmail search "from:someone@example.com"
```

### 検索クエリ一覧

| クエリ | 説明 |
|-------|------|
| `is:unread` | 未読 |
| `is:starred` | スター付き |
| `is:important` | 重要 |
| `from:xxx` | 送信者 |
| `to:xxx` | 宛先 |
| `cc:xxx` | CC |
| `subject:xxx` | 件名に含む |
| `"キーワード"` | 完全一致検索 |
| `has:attachment` | 添付ファイルあり |
| `filename:pdf` | PDFファイル添付 |
| `larger:5M` | 5MB以上 |
| `smaller:1M` | 1MB以下 |
| `after:YYYY/MM/DD` | 指定日以降 |
| `before:YYYY/MM/DD` | 指定日以前 |
| `older_than:7d` | 7日より前 |
| `newer_than:3d` | 3日以内 |
| `label:xxx` | 特定ラベル |
| `in:inbox` | 受信トレイ |
| `in:sent` | 送信済み |
| `in:trash` | ゴミ箱 |
| `in:anywhere` | すべて（ゴミ箱含む） |

### 複合検索例

```bash
# 田中さんから今週届いた未読メール
gog gmail search "from:tanaka is:unread newer_than:7d"

# 請求書関連の添付ファイル付きメール
gog gmail search "subject:請求書 has:attachment"

# 2026年1月以降のPDF添付メール
gog gmail search "filename:pdf after:2026/01/01"
```

---

## メール取得

### スレッド・メッセージ取得

```bash
# メッセージ詳細（本文込み）
gog gmail get <messageId>

# メタデータのみ
gog gmail messages get <messageId> --format metadata
```

### 添付ファイルダウンロード

```bash
gog gmail attachment <messageId> <attachmentId>
gog gmail attachment <messageId> <attachmentId> --output "./download.pdf"
```

---

## メール送信

### 基本送信

```bash
gog gmail send \
  --to "recipient@example.com" \
  --subject "件名" \
  --body "本文テキスト"
```

### CC/BCC付き

```bash
gog gmail send \
  --to "main@example.com" \
  --cc "copy1@example.com,copy2@example.com" \
  --bcc "hidden@example.com" \
  --subject "件名" \
  --body "本文"
```

### 添付ファイル付き

```bash
gog gmail send \
  --to "recipient@example.com" \
  --subject "資料送付" \
  --body "添付ファイルをご確認ください。" \
  --attach "./report.pdf" \
  --attach "./data.xlsx"
```

### HTML本文

```bash
gog gmail send \
  --to "recipient@example.com" \
  --subject "HTMLメール" \
  --body-html "<h1>見出し</h1><p>本文です。</p>"
```

### ファイルから本文読み込み

```bash
gog gmail send \
  --to "recipient@example.com" \
  --subject "長文メール" \
  --body-file "./email_body.txt"
```

---

## 返信

### スレッドに返信

```bash
gog gmail send \
  --thread-id "<threadId>" \
  --to "original-sender@example.com" \
  --subject "Re: 元の件名" \
  --body "返信本文"
```

### メッセージに直接返信

```bash
gog gmail send \
  --reply-to-message-id "<messageId>" \
  --to "original-sender@example.com" \
  --subject "Re: 元の件名" \
  --body "返信本文"
```

### 全員に返信

```bash
gog gmail send \
  --reply-to-message-id "<messageId>" \
  --reply-all \
  --subject "Re: 元の件名" \
  --body "全員への返信"
```

---

## ラベル操作

### ラベル一覧

```bash
gog gmail labels list
```

### ラベル追加/削除

```bash
# ラベル追加
gog gmail thread modify <threadId> --add-labels "重要"

# ラベル削除
gog gmail thread modify <threadId> --remove-labels "UNREAD"

# 既読にする
gog gmail thread modify <threadId> --remove-labels "UNREAD"

# アーカイブ
gog gmail thread modify <threadId> --remove-labels "INBOX"
```

---

## 送信オプション一覧

| オプション | 説明 |
|-----------|------|
| `--to` | 宛先（必須、カンマ区切りで複数可） |
| `--cc` | CC（カンマ区切り） |
| `--bcc` | BCC（カンマ区切り） |
| `--subject` | 件名（必須） |
| `--body` | 本文（プレーンテキスト） |
| `--body-html` | HTML本文 |
| `--body-file` | 本文ファイル（`-` でstdin） |
| `--attach` | 添付ファイル（複数指定可） |
| `--thread-id` | 返信先スレッドID |
| `--reply-to-message-id` | 返信先メッセージID |
| `--reply-all` | 全員に返信 |
| `--from` | 送信元アドレス（送信エイリアス） |
| `--reply-to` | Reply-Toヘッダー |

---

## 出力オプション

| オプション | 説明 |
|-----------|------|
| `--json` | JSON出力 |
| `--plain` | TSV出力 |
| `--max N` | 最大N件 |
| `--all` | 全ページ取得 |

---

## 典型ワークフロー

### 未読メール確認→返信

```bash
# 1. 未読検索
gog gmail search "is:unread" --max 5 --json

# 2. 詳細確認
gog gmail get <messageId>

# 3. 返信
gog gmail send \
  --reply-to-message-id "<messageId>" \
  --to "sender@example.com" \
  --subject "Re: 件名" \
  --body "ご連絡ありがとうございます。..."
```

### 添付ファイル検索→ダウンロード

```bash
# 1. 検索
gog gmail search "from:client has:attachment" --json

# 2. メッセージ取得（添付ID確認）
gog gmail get <messageId> --json

# 3. ダウンロード
gog gmail attachment <messageId> <attachmentId> --output "./downloaded.pdf"
```

---

## メッセージ一覧

```bash
gog gmail messages                      # 受信メッセージ一覧
gog gmail messages --max 20 --json
```

---

## スレッド操作

```bash
# スレッド取得（スレッド内の全メッセージ）
gog gmail thread <threadId>
gog gmail thread <threadId> --json

# スレッドのラベル変更
gog gmail thread modify <threadId> --add-labels "重要"
gog gmail thread modify <threadId> --remove-labels "UNREAD"
```

---

## 下書き操作

```bash
# 下書き一覧
gog gmail drafts list
gog gmail drafts list --json

# 下書き作成
gog gmail drafts create \
  --to "recipient@example.com" \
  --subject "件名" \
  --body "本文"

# 下書き送信
gog gmail drafts send <draftId>

# 下書き削除
gog gmail drafts delete <draftId>
```

---

## トップレベル send コマンド

`gog send` はメール送信のショートカット:

```bash
gog send --to "recipient@example.com" --subject "件名" --body "本文"
```

`gog gmail send` と同等。

---

## 注意事項

- **長い本文**: `--body-file` を使う
- **特殊文字**: シェルエスケープに注意
- **大量送信**: レート制限に注意
- **返信時**: 件名に「Re: 」をつける
