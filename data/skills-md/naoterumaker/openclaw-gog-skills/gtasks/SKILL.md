---
name: gtasks
description: >
  Google Tasks 操作（タスク追加・完了・一覧・削除）を gog CLI (v0.10.0) で行う。
  「タスク追加」「やることリスト」「タスク完了」「タスク一覧」「TODO確認」
  「タスクを作成」「タスクを消化」などで発火。
---

# Google Tasks 操作スキル (gog v0.10.0)

gog CLI でGoogle Tasksを操作する。

**実行パス:** `gog`

**認証アカウント:** (gogで認証したアカウント)

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定

---

## タスクリスト管理

### タスクリスト一覧

```bash
gog tasks lists list
gog tasks lists list --json
```

### タスクリスト作成

```bash
gog tasks lists create --title "新しいリスト"
```

### タスクリスト削除

```bash
gog tasks lists delete <tasklistId>
```

---

## タスク一覧

### リスト内のタスク取得

```bash
gog tasks list <tasklistId>
gog tasks list <tasklistId> --max 20
```

### 完了済み含めて取得

```bash
gog tasks list <tasklistId> --show-completed
```

### 期限付きタスクのみ

```bash
gog tasks list <tasklistId> --due-min "2026-02-01" --due-max "2026-02-28"
```

---

## タスク追加

### 基本

```bash
gog tasks add <tasklistId> --title "やること"
```

### 詳細付き

```bash
gog tasks add <tasklistId> \
  --title "報告書を作成" \
  --notes "月次報告書\n- 売上データ\n- 顧客分析"
```

### 期限付き

```bash
gog tasks add <tasklistId> \
  --title "請求書送付" \
  --due "2026-02-15"
```

### フルオプション

```bash
gog tasks add <tasklistId> \
  --title "プロジェクト計画書作成" \
  --notes "第1四半期の計画をまとめる" \
  --due "2026-02-20"
```

---

## タスク詳細取得

```bash
gog tasks get <tasklistId> <taskId>
```

---

## タスク更新

### タイトル変更

```bash
gog tasks update <tasklistId> <taskId> --title "新しいタイトル"
```

### メモ追加

```bash
gog tasks update <tasklistId> <taskId> --notes "追加メモ"
```

### 期限変更

```bash
gog tasks update <tasklistId> <taskId> --due "2026-02-28"
```

---

## タスク完了

### 完了にする

```bash
gog tasks done <tasklistId> <taskId>
```

### 未完了に戻す

```bash
gog tasks undo <tasklistId> <taskId>
```

---

## タスク削除

### 単一削除

```bash
gog tasks delete <tasklistId> <taskId>
```

### 完了済みをすべてクリア

```bash
gog tasks clear <tasklistId>
```

---

## 追加オプション一覧

| オプション | 説明 |
|-----------|------|
| `--title` | タスクタイトル |
| `--notes` | メモ・詳細 |
| `--due` | 期限（YYYY-MM-DD形式） |

---

## 一覧オプション

| オプション | 説明 |
|-----------|------|
| `--max N` | 最大N件 |
| `--show-completed` | 完了済みも表示 |
| `--due-min` | 期限開始日 |
| `--due-max` | 期限終了日 |

---

## 出力オプション

| オプション | 説明 |
|-----------|------|
| `--json` | JSON出力 |
| `--plain` | TSV出力 |

---

## タスクリストIDの取得

```bash
# リスト一覧からIDを取得
gog tasks lists list --json | jq '.[].id'
```

デフォルトのタスクリストは通常 `@default` や最初のリストID。

---

## 典型ワークフロー

### タスク一覧確認→新規追加→完了

```bash
# 1. リスト確認
RESULT=$(gog tasks lists list --json)
LIST_ID=$(echo "$RESULT" | jq -r '.[0].id')

# 2. タスク一覧
gog tasks list "$LIST_ID"

# 3. タスク追加
gog tasks add "$LIST_ID" --title "緊急: クライアントに連絡" --due "2026-02-05"

# 4. 完了後
gog tasks done "$LIST_ID" "<taskId>"
```

### 今週の期限タスク確認

```bash
LIST_ID="<tasklistId>"
gog tasks list "$LIST_ID" --due-min "2026-02-04" --due-max "2026-02-10"
```

### 完了済みをクリーンアップ

```bash
gog tasks clear "$LIST_ID"
```

---

## 注意事項

- **期限形式**: `YYYY-MM-DD`（時刻なし）
- **サブタスク**: gog CLIではサブタスクの階層管理は限定的
- **完了タスク**: デフォルトでは非表示、`--show-completed` で表示
- **clear**: 完了済みタスクのみ削除（未完了は残る）
