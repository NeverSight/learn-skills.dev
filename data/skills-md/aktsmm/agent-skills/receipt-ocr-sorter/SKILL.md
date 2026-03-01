---
name: receipt-ocr-sorter
description: "OCR領収書自動仕分けツール。画像(JPEG/PNG)/PDF/ZIP/動画(MP4/MOV)の領収書をOCRで読み取り、日付・金額・国・カード・用途を抽出して標準ファイル名にリネーム＆プロジェクト単位で仕分ける。Markdownサマリーレポート付き。D365 Expenseカテゴリマッピング・レシート添付連携対応。Use when: (1) 領収書の整理, (2) receipt sorting, (3) レシート仕分け, (4) 経費レシートをフォルダ整理, (5) OCRでリネーム, (6) D365経費カテゴリマッピング。Surya OCR + GPU(CUDA)対応。"
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Receipt OCR Sorter

OCR（Surya）を使った領収書の自動仕分け・リネーム・集計ツール。

## When to Use

- **領収書を仕分けて**, **レシートを整理して**, **receipt sorting**
- フォルダ内の領収書画像をプロジェクト単位で自動整理したい
- 大量のレシート写真に日付・金額・用途でファイル名を付けたい
- 出張経費の領収書を一括でリネーム＆集計したい

## Features

| 機能             | 説明                                                           |
| ---------------- | -------------------------------------------------------------- |
| **OCR抽出**      | 日付・金額・国・カード種別・店舗/用途を自動抽出                |
| **自動リネーム** | `YYYY-MM-DD-国-金額[-カード]-用途.ext` 形式                    |
| **動画対応**     | MP4/MOV → ffmpegでフレーム抽出 → OCR                           |
| **品質補正**     | 日付パターン拡張、金額誤読補正、上限チェック                   |
| **サマリー**     | PJフォルダにMarkdownレポート（合計・日付別・明細・日本語概要） |
| **GPU対応**      | CUDA PyTorch で高速処理                                        |

## Architecture

```
入力フォルダ（未仕分け/iCloud写真 等）
  │
  ├─ JPEG/PNG/PDF/ZIP → OCR → 抽出 → リネーム → PJフォルダへ移動
  ├─ MP4/MOV → ffmpeg → JPG → OCR → ...
  │
  ├─ カード不明 or テキスト不可 → 未分類フォルダ → 再仕分け可能
  │
  └─ 個人経費（D365対象外） → PJフォルダ/private/
```

> **`private/` フォルダ**: D365 に申請しない個人経費レシートを格納する。OCR後にユーザーが「個人経費」と判断した場合に移動する。

## Naming Convention

```
YYYY-MM-DD-国コード-金額[-カード]-分類.ext

例:
  2026-02-09-jpn-14320-amex-shinkansen.jpeg
  2026-02-11-us-272-amex-hotel.jpeg
  2026-02-12-us-190.38-meal.jpeg        ← カードなし
  2026-02-09-us-6.80-amex-meal-starbucks.jpeg
```

### 国コード

| コード | 国             |
| ------ | -------------- |
| jpn    | 日本           |
| us     | アメリカ       |
| cn     | 中国           |
| gb     | イギリス       |
| sg     | シンガポール   |
| kr     | 韓国           |
| au     | オーストラリア |
| xx     | 不明           |

### 分類（summary）

| 分類             | 日本語             | トリガーキーワード              |
| ---------------- | ------------------ | ------------------------------- |
| shinkansen       | 新幹線             | 新幹線, のぞみ, ひかり, EX予約  |
| hotel            | 宿泊               | ホテル, HOTEL, MARRIOTT, HILTON |
| airline          | 航空               | ANA, JAL, DELTA, UNITED         |
| transport        | 交通               | TRANSIT, METRO, Suica, PASMO    |
| taxi             | タクシー           | TAXI, UBER, LYFT                |
| meal-starbucks   | 食費（スタバ）     | STARBUCKS                       |
| meal-restaurant  | 食費（レストラン） | RESTAURANT, DINING              |
| meal-convenience | 食費（コンビニ）   | 7-ELEVEN, LAWSON, FAMILYMART    |
| meal-supermarket | 食費（スーパー）   | COSTCO, WHOLE FOODS, SAFEWAY    |
| meal             | 食費               | MEAL, LUNCH, DINNER             |
| seminar          | セミナー           | SEMINAR, CONFERENCE             |
| shopping         | 買い物             | AMAZON, APPLE STORE             |

## CLI Usage

```powershell
# Dry-run（確認のみ、ファイル移動なし）
python receipt_sorter.py --project "202602_TechConnect_Seattle" --dry-run

# 本実行
python receipt_sorter.py --project "202602_TechConnect_Seattle" --input "未仕分け\iCloud写真"

# ログ指定
python receipt_sorter.py --project "202602_TechConnect_Seattle" --input "未仕分け\iCloud写真" --log "result.csv"
```

### Options

| オプション  | 説明                         | デフォルト                                            |
| ----------- | ---------------------------- | ----------------------------------------------------- |
| `--project` | 出力PJフォルダ名（必須）     | -                                                     |
| `--input`   | 入力フォルダ                 | `未仕分け/`                                           |
| `--dry-run` | ファイル移動せず結果のみ表示 | false                                                 |
| `--log`     | 結果CSVパス                  | `<PJフォルダ>/csv/<PJ名>_dryrun.csv` or `_result.csv` |

## Markdown Summary Output

本実行後、PJフォルダに `<PJ名>_summary.md` が自動生成される。

含む内容:

- プロジェクト合計（通貨混在・参考値）
- 国コード別合計テーブル
- 日付×国コード別合計テーブル
- 全明細テーブル（日付・国・金額・カード・分類・日本語概要・ファイル名）

## Setup

→ **[references/setup-guide.md](references/setup-guide.md)**

## Script Reference

→ **[references/receipt_sorter.py](references/receipt_sorter.py)**

## D365 Expense カテゴリマッピング

OCR分類から D365 Finance Expense Report のカテゴリへの対応表。

| OCR分類        | D365 Expense Category         | 備考                     |
| -------------- | ----------------------------- | ------------------------ |
| shinkansen     | Ground Transportation         | 国内鉄道全般             |
| hotel          | Hotel                         |                          |
| airline        | Airfare \| International      | 国際線。国内線は Airfare |
| transport      | Ground Transportation         | 電車・バス等             |
| taxi           | Ground Transportation \| Taxi |                          |
| meal-\*        | Meals \| Employee Travel      | 全食費サブカテゴリ共通   |
| seminar        | Admin Services - Misc.        |                          |
| shopping       | Admin Services - Misc.        |                          |
| esim / telecom | Internet/Online Fees - Travel | eSIM・通信費             |

## D365 連携（Post-OCR）

OCR → リネーム後のファイルは D365 Finance Expense Report に添付可能。

### レシート添付手順

1. Expense line を選択 → Details 下の **Receipts** セクション → **Edit**
2. **Add receipts** → **Browse** → リネーム済みファイルを選択
3. Document Type: `File`（PDF）/ `Image`（JPEG/PNG）
4. **Upload** → **OK** → **Close**

### レシート差し替え手順

誤ったレシートが添付されている場合：

1. Expense line を選択 → Receipts の **Edit** を押す
2. 誤レシートのチェックボックスを選択 → **Remove** → **Yes**
3. **Add receipts** → **Browse** → 正しいファイルを選択 → **Upload** → **OK**
4. **Close** → **Save and continue**

### 添付時マッチング検証（MANDATORY）

レシート添付・差し替え時に以下を照合すること：

| チェック項目 | 照合対象 |
|-------------|----------|
| **金額** | ファイル名の金額 ≒ 経費行の Amount |
| **日付** | ファイル名の日付 ≒ 経費行の Date |
| **マーチャント** | ファイル名の分類/店名 ∈ 経費行の Merchant |

> ⚠️ 不一致のまま添付すると監査で差し戻される。

### カテゴリ変更手順

1. Expense line を選択 → **Edit** → Category コンボボックスにカテゴリ名を入力
2. `Tab` キーで確定 → **Close**

> **Tips**: D365 ブラウザ操作は **MCP Playwright tools**（`browser_type` / `browser_click` / `browser_snapshot`）が最も安定する。Node.js スクリプト（Playwright直接）による自動化は D365 の動的DOM で繰り返し失敗するため非推奨。

## Known Limitations

- OCRの精度はSuryaモデルに依存（手書きや歪みが大きい領収書は誤読あり）
- 金額は最大候補を採用するが、複数明細のあるレシートでは個別明細は取れない
- **金額連結誤読**: OCRが改行をまたいで数字を結合し巨大整数を返すことがある（例: `14520` + `300` → `14520300`）。上限チェック（500万超は除外）で防御しているが、完全ではない
- 動画は中間フレーム1枚のみ抽出（最適フレーム選択は未実装）
- 日本語の漢字店名はスラッグ化時にASCII変換で落ちる（カタカナはローマ字化される）
- **Windows PIL ファイルロック**: `Image.open()` がハンドルを保持し `shutil.move()` が `WinError 32` で失敗する。`with` + `img.copy()` + リトライで対応済み
