---
name: gcal
description: >
  Google カレンダー操作（予定確認・作成・更新・削除）を gog CLI (v0.10.0) で行う。
  「今日の予定は？」「明日のスケジュール」「ミーティング入れて」「予定を登録」
  「カレンダー確認」「予定をキャンセル」「Google Meet作成」などで発火。
---

# Google Calendar 操作スキル (gog v0.10.0)

gog CLI でGoogleカレンダーを操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定
- 日時はRFC3339形式: `2026-02-15T10:00:00+09:00`

---

## 予定一覧

### 基本（今後7日間）

```bash
gog calendar events
gog calendar events --max 10
```

### 期間指定

```bash
gog calendar events --from "2026-02-01" --to "2026-02-28"
gog calendar events --from "2026-02-15T00:00:00+09:00" --to "2026-02-15T23:59:59+09:00"
```

### 特定カレンダー

```bash
gog calendar events primary                    # メインカレンダー
gog calendar events "user@example.com"         # 共有カレンダー
```

### 今日の予定

```bash
TODAY=$(date +%Y-%m-%d)
gog calendar events --from "${TODAY}T00:00:00+09:00" --to "${TODAY}T23:59:59+09:00"
```

---

## 予定作成

### 基本

```bash
gog calendar create primary \
  --summary "ミーティング" \
  --from "2026-02-15T10:00:00+09:00" \
  --to "2026-02-15T11:00:00+09:00"
```

### 終日予定

```bash
gog calendar create primary \
  --summary "休暇" \
  --from "2026-02-20" \
  --to "2026-02-21" \
  --all-day
```

### 場所・説明付き

```bash
gog calendar create primary \
  --summary "クライアントMTG" \
  --from "2026-02-15T14:00:00+09:00" \
  --to "2026-02-15T15:30:00+09:00" \
  --location "東京都渋谷区〇〇ビル 5F" \
  --description "議題:\n1. 進捗報告\n2. 次回スケジュール"
```

### 参加者追加

```bash
gog calendar create primary \
  --summary "定例会議" \
  --from "2026-02-15T10:00:00+09:00" \
  --to "2026-02-15T11:00:00+09:00" \
  --attendees "tanaka@example.com,sato@example.com"
```

### Google Meet付き

```bash
gog calendar create primary \
  --summary "オンラインMTG" \
  --from "2026-02-15T10:00:00+09:00" \
  --to "2026-02-15T11:00:00+09:00" \
  --with-meet
```

### リマインダー付き

```bash
gog calendar create primary \
  --summary "重要MTG" \
  --from "2026-02-15T10:00:00+09:00" \
  --to "2026-02-15T11:00:00+09:00" \
  --reminder "popup:30m" \
  --reminder "email:1d"
```

### 繰り返し予定

```bash
# 毎週月曜
gog calendar create primary \
  --summary "週次定例" \
  --from "2026-02-17T10:00:00+09:00" \
  --to "2026-02-17T11:00:00+09:00" \
  --rrule "RRULE:FREQ=WEEKLY;BYDAY=MO"

# 毎月15日
gog calendar create primary \
  --summary "月次報告" \
  --from "2026-02-15T10:00:00+09:00" \
  --to "2026-02-15T11:00:00+09:00" \
  --rrule "RRULE:FREQ=MONTHLY;BYMONTHDAY=15"
```

---

## 予定更新

```bash
gog calendar update primary <eventId> --summary "新しいタイトル"
gog calendar update primary <eventId> --from "2026-02-15T11:00:00+09:00" --to "2026-02-15T12:00:00+09:00"
gog calendar update primary <eventId> --location "オンライン"
```

---

## 予定削除

```bash
gog calendar delete primary <eventId>
gog calendar delete primary <eventId> --force  # 確認スキップ
```

---

## 予定検索

```bash
gog calendar search "ミーティング"
gog calendar search "MTG" --from "2026-02-01" --to "2026-02-28"
```

---

## カレンダー管理

### カレンダー一覧

```bash
gog calendar calendars
```

### 空き時間確認

```bash
gog calendar freebusy "primary,user@example.com" \
  --from "2026-02-15T09:00:00+09:00" \
  --to "2026-02-15T18:00:00+09:00"
```

### 予定の衝突確認

```bash
gog calendar conflicts --from "2026-02-15" --to "2026-02-21"
```

---

## 特殊イベント

### フォーカスタイム

```bash
gog calendar focus-time primary \
  --from "2026-02-15T14:00:00+09:00" \
  --to "2026-02-15T17:00:00+09:00"
```

### 外出中（Out of Office）

```bash
gog calendar out-of-office primary \
  --from "2026-02-20" \
  --to "2026-02-21"
```

### 勤務場所設定

```bash
gog calendar working-location primary \
  --from "2026-02-15" \
  --to "2026-02-16" \
  --type "home"
```

---

## 作成オプション一覧

| オプション | 説明 |
|-----------|------|
| `--summary` | タイトル |
| `--from` | 開始日時（RFC3339） |
| `--to` | 終了日時（RFC3339） |
| `--all-day` | 終日予定 |
| `--location` | 場所 |
| `--description` | 説明 |
| `--attendees` | 参加者（カンマ区切り） |
| `--with-meet` | Google Meet作成 |
| `--reminder` | リマインダー（popup:30m, email:1d等） |
| `--rrule` | 繰り返しルール |
| `--event-color` | 色（1-11） |
| `--visibility` | 公開設定（default/public/private） |
| `--transparency` | 表示（opaque=予定あり/transparent=空き） |
| `--send-updates` | 通知（all/externalOnly/none） |
| `--guests-can-invite` | ゲスト招待許可 |
| `--guests-can-modify` | ゲスト編集許可 |

---

## 日時形式

### RFC3339形式

```
2026-02-15T10:00:00+09:00   # 日本時間
2026-02-15T01:00:00Z        # UTC
```

### 終日イベントの日付

```
2026-02-15   # 開始日
2026-02-16   # 終了日（翌日を指定）
```

---

## 典型ワークフロー

### 今日の予定確認→ミーティング追加

```bash
# 1. 今日の予定確認
TODAY=$(date +%Y-%m-%d)
gog calendar events --from "${TODAY}T00:00:00+09:00" --to "${TODAY}T23:59:59+09:00"

# 2. 空き時間確認
gog calendar freebusy "primary" --from "${TODAY}T09:00:00+09:00" --to "${TODAY}T18:00:00+09:00"

# 3. 予定作成（Google Meet付き）
gog calendar create primary \
  --summary "緊急MTG" \
  --from "${TODAY}T15:00:00+09:00" \
  --to "${TODAY}T16:00:00+09:00" \
  --with-meet \
  --attendees "team@example.com"
```

### 来週の予定確認

```bash
START=$(date -v+1d +%Y-%m-%d)  # macOS
END=$(date -v+7d +%Y-%m-%d)
gog calendar events --from "$START" --to "$END"
```

---

## 招待への返答（RSVP）

```bash
gog calendar respond primary <eventId> --status accepted
gog calendar respond primary <eventId> --status declined
gog calendar respond primary <eventId> --status tentative
```

---

## カレンダーの色一覧

```bash
gog calendar colors
```

---

## 単一イベント取得

```bash
gog calendar event primary <eventId>
gog calendar event primary <eventId> --json
```

---

## アクセス制御 (ACL)

```bash
# ACL一覧
gog calendar acl primary

# ACL追加
gog calendar acl primary --add "user@example.com" --role reader

# ACL削除
gog calendar acl primary --remove "user@example.com"
```

---

## 注意事項

- **タイムゾーン**: `+09:00` を必ず付ける（日本時間）
- **終日イベント**: `--to` は終了日の翌日を指定
- **参加者通知**: デフォルトで招待メールが送信される
- **繰り返し削除**: 単発だけ削除するか全部削除するか確認される
