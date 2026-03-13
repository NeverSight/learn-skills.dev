---
name: google-sheets-ops
description: >
  Google スプレッドシートの作成・読み書き・書式設定を gog CLI (v0.10.0) で行う。
  「スプシ作って」「スプレッドシートにデータ入れて」「シート操作」「スプシのテンプレ作成」
  「スプレッドシートを更新」「セルに書き込み」「シートを読み取り」などで使用。
  gog sheets コマンドの正しい使い方（パイプ区切り・タブ作成・書式設定）を提供する。
---

# Google Sheets 操作スキル (gog v0.10.0)

gog CLI を使ってGoogle スプレッドシートを操作する。

**実行パス:** `gog`

## Execution Notes

- `exec` ツールで実行時、`timeout: 60` を指定
- 大量データ書き込みは分割して実行

---

## 絶対に守るルール

### 1. セル区切りはパイプ `|`、行区切りはカンマ `,`

```bash
# ✅ 正しい：1行に3セル
gog sheets update "$ID" "シート1!A1:C1" "値1|値2|値3"

# ✅ 正しい：2行×3列
gog sheets update "$ID" "シート1!A1:C2" "行1列1|行1列2|行1列3,行2列1|行2列2|行2列3"

# ❌ 間違い：スペース区切りは全部1セルに入る
gog sheets update "$ID" "シート1!A1" "値1" "値2" "値3"
```

### 2. カンマ・パイプを含むデータは `--values-json`

```bash
gog sheets update "$ID" "シート1!A1:C2" --values-json '[
  ["名前", "金額", "備考"],
  ["田中", "500,000", "特記|なし"]
]'
```

### 3. 複数タブは create 時に `--sheets` で全部作る

```bash
gog sheets create "タイトル" --sheets "タブ1,タブ2,タブ3"
```

**⚠️ gogにタブの後追加・削除・リネーム機能はない**

### 4. 操作前にメタデータ確認

```bash
gog sheets metadata "$ID"  # シート名を確認（日本語ロケールでは「シート1」）
```

### 5. 書き込み後は確認

```bash
gog sheets get "$ID" "シート1!A1:C2" --json
```

---

## コマンドリファレンス

### 読み取り: `get`

```bash
gog sheets get <spreadsheetId> <range>

# 例
gog sheets get "$ID" "シート1!A1:C10"
gog sheets get "$ID" "シート1!A:A"      # A列全体
gog sheets get "$ID" "シート1!1:1"      # 1行目全体
gog sheets get "$ID" "シート1" --json   # JSON出力
```

### 書き込み: `update`

```bash
gog sheets update <spreadsheetId> <range> <values>

# オプション
--input="USER_ENTERED"      # 数式・日付を解釈（デフォルト）
--input="RAW"               # そのまま文字列として入力
--values-json='[[...]]'     # JSON形式で値指定
--copy-validation-from="Sheet1!A2"  # データ検証をコピー
```

**例:**

```bash
# 単一行
gog sheets update "$ID" "シート1!A1:C1" "名前|部署|役職"

# 複数行
gog sheets update "$ID" "シート1!A2:C4" "田中|営業|主任,佐藤|開発|リーダー,鈴木|総務|担当"

# JSON形式（推奨：特殊文字を含む場合）
gog sheets update "$ID" "シート1!A1:B2" --values-json '[["項目","金額"],["売上","1,000,000"]]'

# 数式
gog sheets update "$ID" "シート1!D2" "=SUM(B2:C2)"
```

### 追加: `append`

```bash
gog sheets append <spreadsheetId> <range> <values>

# 例：シート末尾に行追加
gog sheets append "$ID" "シート1" "新しい|データ|行"
```

### クリア: `clear`

```bash
gog sheets clear <spreadsheetId> <range>

# 例
gog sheets clear "$ID" "シート1!A2:C100"
```

### 書式設定: `format`

```bash
gog sheets format <spreadsheetId> <range> --format-json '<CellFormat>'

# オプション
--format-fields="userEnteredFormat(backgroundColor,textFormat)"
```

**書式例:**

```bash
# ヘッダー書式（青背景・白太字）
FMT='{"backgroundColor":{"red":0.2,"green":0.4,"blue":0.7},"textFormat":{"bold":true,"foregroundColor":{"red":1,"green":1,"blue":1}}}'
gog sheets format "$ID" "シート1!A1:D1" --format-json "$FMT"

# 太字のみ
gog sheets format "$ID" "シート1!A1:A10" --format-json '{"textFormat":{"bold":true}}'

# 背景色（薄い黄色）
gog sheets format "$ID" "シート1!A1:D1" --format-json '{"backgroundColor":{"red":1,"green":1,"blue":0.8}}'
```

### 作成: `create`

```bash
gog sheets create <title> [--sheets "タブ1,タブ2"]

# 例
gog sheets create "新規スプレッドシート"
gog sheets create "プロジェクト管理" --sheets "概要,タスク,スケジュール"
```

### コピー: `copy`

```bash
gog sheets copy <spreadsheetId> <newTitle>

# 例
gog sheets copy "$TEMPLATE_ID" "請求書_202602_山田様"
```

### メタデータ: `metadata`

```bash
gog sheets metadata <spreadsheetId>
```

### エクスポート: `export`

```bash
gog sheets export <spreadsheetId> --format <csv|xlsx|pdf>

# 例
gog sheets export "$ID" --format csv
gog sheets export "$ID" --format xlsx --output "./backup.xlsx"
```

---

## 典型ワークフロー

### スプレッドシートをゼロから作成

```bash
# 1. 作成（タブ全部指定）
RESULT=$(gog sheets create "売上管理" --sheets "月次,年次,設定" --json)
ID=$(echo "$RESULT" | jq -r '.spreadsheetId')

# 2. ヘッダー書き込み
gog sheets update "$ID" "月次!A1:E1" "日付|商品|数量|単価|金額"

# 3. ヘッダー書式
FMT='{"backgroundColor":{"red":0.2,"green":0.4,"blue":0.7},"textFormat":{"bold":true,"foregroundColor":{"red":1,"green":1,"blue":1}}}'
gog sheets format "$ID" "月次!A1:E1" --format-json "$FMT"

# 4. サンプルデータ
gog sheets update "$ID" "月次!A2:E3" "2026/02/01|商品A|10|1000|=C2*D2,2026/02/02|商品B|5|2000|=C3*D3"

# 5. フォルダ移動（任意）
gog drive move "$ID" --parent "<フォルダID>"

echo "作成完了: https://docs.google.com/spreadsheets/d/$ID/edit"
```

### 大量データの一括書き込み

```bash
gog sheets update "$ID" "シート1!A1:D5" --values-json '[
  ["名前", "部署", "役職", "入社日"],
  ["田中太郎", "営業", "主任", "2024/04/01"],
  ["佐藤花子", "開発", "リーダー", "2023/01/15"],
  ["鈴木一郎", "総務", "担当", "2025/07/01"],
  ["山田次郎", "企画", "マネージャー", "2022/10/01"]
]'
```

### テンプレートからコピーして編集

```bash
# 1. コピー
RESULT=$(gog sheets copy "$TEMPLATE_ID" "請求書_202602_山田様" --json)
NEW_ID=$(echo "$RESULT" | jq -r '.id')

# 2. 編集
gog sheets update "$NEW_ID" "請求書!B6" "株式会社山田様"
gog sheets update "$NEW_ID" "請求書!D10" "コンサルティング業務"

echo "作成完了: https://docs.google.com/spreadsheets/d/$NEW_ID/edit"
```

---

## CellFormat リファレンス

### 背景色

```json
{"backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}}
```

RGB値は 0.0〜1.0

### テキスト書式

```json
{
  "textFormat": {
    "bold": true,
    "italic": false,
    "strikethrough": false,
    "underline": false,
    "fontSize": 12,
    "foregroundColor": {"red": 0, "green": 0, "blue": 0}
  }
}
```

### 配置

```json
{
  "horizontalAlignment": "CENTER",
  "verticalAlignment": "MIDDLE"
}
```

値: `LEFT`, `CENTER`, `RIGHT` / `TOP`, `MIDDLE`, `BOTTOM`

### 罫線

```json
{
  "borders": {
    "top": {"style": "SOLID", "color": {"red": 0, "green": 0, "blue": 0}},
    "bottom": {"style": "SOLID"},
    "left": {"style": "SOLID"},
    "right": {"style": "SOLID"}
  }
}
```

---

## gogでできないこと

以下は Sheets API batchUpdate が必要:

- タブの後追加・削除・リネーム
- 入力規則（ドロップダウン）
- 条件付き書式
- セル結合
- 列幅・行高調整
- 行/列の固定（フリーズ）
- フィルター・チャート

---

## よくあるミス

| ミス | 正しい方法 |
|-----|-----------|
| `update "A1" "a" "b" "c"` | `update "A1:C1" "a\|b\|c"` |
| カンマ入り数値 `1,000` | `--values-json` を使う |
| シート名間違い | `metadata` で確認 |
| 範囲指定なし | 必ず範囲を明示 |
