---
name: reinfolib-skill
description: "住所から国土交通省の不動産取引データで坪単価・一種単価を自動分析する。相場の確認や物件価格の妥当性チェックに対応。Triggers on: '坪単価', '一種単価', '相場を調べて', 'この土地は高い？', '不動産の値段', '地価を調べて', '取引事例', '土地の相場'. Do NOT use for: Google Maps検索(→gemini-maps-grounding), 用途地域確認(→mlit-geospatial MCPを直接使用)."
---

## MCPツールの準備

分析開始前に必ず ToolSearch で MCPツールを読み込む:

```
ToolSearch: "+mlit"
```

---

## 分析フロー（MCP 呼び出し順序）

### Step 1: 住所 → 座標変換

`scripts/geocode.py` を実行して緯度・経度を取得する:

```bash
python3 scripts/geocode.py '<住所>'
# 出力例: lat=35.681236, lon=139.767125
```

失敗時はエラー報告して終了。

### Step 2: 用途地域の確認

`mcp__mlit-geospatial-mcp__get_zoning_district` で用途地域・建蔽率・容積率を取得。タイムアウト時はスキップ可（後続の分析には必須ではない）。容積率は一種単価の計算に必要なので変数として保持する。

### Step 3: 地価公示・地価調査データの取得

`mcp__mlit-geospatial-mcp__get_land_price_point_by_location` で地価公示・調査データを取得。近隣の公示地価を参考値として記録。

### Step 4: 取引データの取得（3年分）

`mcp__mlit-geospatial-mcp__get_multi_api` を以下のパラメータで3回呼び出し（現在年・前年・前々年）:

```
target_apis: [1]
lat: (Step 1の緯度)
lon: (Step 1の経度)
save_file: false
year: 現在年, 前年, 前々年
```

3年分のデータを結合する。

### Step 5〜7: データ分析・異常値除外

`scripts/analyze_transactions.py` の関数を使用する:

```python
from scripts.analyze_transactions import analyze_land_only, analyze_land_with_building, exclude_outliers, summarize_by_use_district

# 土地のみ取引（主軸）
land_only = analyze_land_only(all_data)
land_only = exclude_outliers(land_only)   # 2パス目の異常値除外
summary = summarize_by_use_district(land_only)

# 建物込み取引（参考値）
land_with_building = analyze_land_with_building(all_data)
```

分析方法論・建物残価の詳細は `references/methodology.md` を参照。

### Step 8: 妥当性判定

| 乖離率 | 判定 |
|---------|------|
| ±10%以内 | 妥当（相場レンジ内） |
| 10-30% | 要精査（個別要因の可能性） |
| 30%超 | 異常値の可能性大（詳細調査が必要） |

---

## 出力フォーマット

```
## 不動産相場分析レポート: <住所>

### 基本情報
| 項目 | 値 |
|------|-----|
| 用途地域 | ... |
| 建蔽率 | ...% |
| 容積率 | ...% |
| 地価公示（最寄り） | ...円/㎡ |

### 土地取引の坪単価・一種単価レンジ（土地のみ取引）
| 用途地域 | 件数 | 坪単価(万円) | 一種単価(万円) |
|----------|------|-------------|---------------|
| ... | N件 | XX〜YY（中央値ZZ） | XX〜YY（中央値ZZ） |

### 建物込み取引からの推定土地坪単価（参考）
| 用途地域 | 件数 | 推定坪単価(万円) | 備考 |
|----------|------|-----------------|------|
| ... | N件 | XX〜YY（中央値ZZ） | 簡易推定・参考値 |

### 地価公示との比較
...

### 総合判定
...（妥当性の判定結果と根拠）

---
> このサービスは、国土交通省不動産情報ライブラリのAPI機能を使用していますが、提供情報の最新性、正確性、完全性等が保証されたものではありません。
> 建物込み取引の推定土地価格は、法定耐用年数に基づく簡易推定であり、リフォーム・個別品質・設備は未考慮です。参考値としてご利用ください。
```

---

## references / scripts 一覧

| ファイル | 内容 | 参照タイミング |
|---------|------|--------------|
| `scripts/geocode.py` | 住所 → 緯度経度変換 | Step 1 |
| `scripts/analyze_transactions.py` | 坪単価・一種単価・建物残価・異常値除外の全関数 | Step 5〜7 |
| `references/methodology.md` | 分析方法論・前提条件・法定耐用年数・法的免責文 | 詳細確認時 |
