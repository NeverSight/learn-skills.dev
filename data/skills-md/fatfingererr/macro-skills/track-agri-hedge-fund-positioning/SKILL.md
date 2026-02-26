---
name: track-agri-hedge-fund-positioning
description: 用 COT 非商業部位變化，量化對沖基金在農產品期貨的資金流向，並把出口需求、USDA 數據、美元/原油/金屬等宏觀風向整合成可交易的敘事與訊號。
---

<essential_principles>

<principle name="cot_as_flow_proxy">
**COT 週資料作為資金流代理**

CFTC Commitments of Traders 報告是追蹤對沖基金農產品部位的核心資料：
- **截止日**：每週二收盤
- **發布日**：每週五下午 3:30 ET
- **交易者分類**：非商業（投機/基金）、商業（避險）、非報告

資金流 = 本週淨部位 - 上週淨部位（以合約口數計）
</principle>

<principle name="group_aggregation">
**分組彙總邏輯**

使用 CFTC 原生分組（commodity_subgroup_name）：

| 群組     | CFTC 分組名稱           | 包含商品                          |
|----------|-------------------------|-----------------------------------|
| Grains   | GRAINS                  | Corn, Wheat (SRW/HRW/HRS), Oats   |
| Oilseeds | OILSEED and PRODUCTS    | Soybeans, Soybean Oil/Meal, Canola|
| Meats    | LIVESTOCK/MEAT PRODUCTS | Live Cattle, Lean Hogs, Feeder    |
| Softs    | FOODSTUFFS/SOFTS        | Coffee, Sugar, Cocoa, OJ          |
| Fiber    | FIBER                   | Cotton                            |
| Dairy    | DAIRY PRODUCTS          | Milk, Butter, Cheese              |

**Total Flow = Grains + Oilseeds + Meats + Softs + Fiber + Dairy**
</principle>

<principle name="firepower_definition">
**火力（Buying Firepower）量化**

火力衡量基金是否還有加碼空間：

```
net_pos_percentile = rank(current_net_pos, past_N_weeks)
firepower = 1 - net_pos_percentile
```

- **高火力（>0.6）**：部位處於歷史低檔，仍有大量買進空間
- **低火力（<0.3）**：部位已接近歷史高檔，擁擠風險高
</principle>

<principle name="macro_tailwind">
**宏觀順風評分**

整合三個風險偏好指標：

| 指標       | 訊號解讀                     |
|------------|------------------------------|
| 美元 (DXY) | 走弱（負報酬）= 利於商品     |
| 原油 (WTI) | 走強（正報酬）= 風險偏好上升 |
| 金屬       | 走強（正報酬）= 循環需求樂觀 |

**macro_tailwind_score = (DXY弱 + WTI強 + Metals強) / 3**
</principle>

<principle name="wed_fri_validation">
**週中回補驗證框架**

COT 只到週二，週三～週五需用代理證據：

1. **價格動能**：農產品/代理指數 Wed-Fri 累積報酬
2. **未平倉變化**：OI 擴張 = 新倉（非純換手）
3. **宏觀共振**：與 USD↓、油價↑、金屬↑ 同時性
</principle>

</essential_principles>

<objective>
追蹤對沖基金在農產品期貨的部位變化與資金流向：

1. **取得資料**：COT 週報、宏觀指標（DXY/WTI/金屬）、基本面觸發（出口/USDA）
2. **計算流量**：淨部位週變化，分組彙總（Grains/Oilseeds/Meats/Softs/Total）
3. **量化火力**：用歷史分位數估算基金加碼空間
4. **整合訊號**：判斷「基金回來買」+ 「宏觀順風」+ 「基本面支持」
5. **產出敘事**：將圖表標註（如 Strong Corn Demand）轉為可重複的規則

輸出：週流量時序、最新狀態、火力分數、宏觀評分、可交易註解。
</objective>

<quick_start>

**快速開始：分析最新 COT 資料**

```bash
cd .claude/skills/track-agri-hedge-fund-positioning/scripts
pip install pandas numpy requests yfinance pyarrow  # 首次使用
python analyze_positioning.py --start 2023-01-01
```

輸出範例（真實資料）：
```json
{
  "skill": "track-agri-hedge-fund-positioning",
  "as_of": "2026-01-20",
  "data_source": "CFTC Socrata API (real data)",
  "summary": {
    "call": "Funds continue selling",
    "all_signals": ["Funds continue selling", "Extreme short - watch for reversal", "Macro mood bullish"],
    "confidence": 0.90
  },
  "latest_metrics": {
    "flow_total_contracts": -24559,
    "flow_by_group_contracts": {"grains": -31279, "oilseeds": 11517, "meats": 18972, "softs": -23887, "fiber": 1607, "dairy": -1489},
    "buying_firepower": {"total": 0.86, "grains": 0.58, "oilseeds": 0.62, "meats": 0.31, "softs": 0.99, "fiber": 0.58, "dairy": 0.99},
    "macro_tailwind_score": 0.67
  }
}
```

**視覺化圖表**：
```bash
python visualize_flows.py --weeks 52
# 輸出：output/agri_fund_positioning_YYYY-MM-DD.png
```

</quick_start>

<intake>
需要進行什麼操作？

1. **快速檢查** - 查看最新一週的基金部位變化與狀態
2. **完整分析** - 指定日期範圍的資金流向分析與回測
3. **視覺化圖表** - 生成分組柱狀圖與火力時序圖
4. **監控模式** - 設定週度更新與訊號警報
5. **方法論學習** - 了解 COT 分析與火力計算邏輯

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                       | Action                                                    |
|--------------------------------|-----------------------------------------------------------|
| 1, "快速", "quick", "latest"   | 執行 `python scripts/analyze_positioning.py`              |
| 2, "分析", "analyze", "full"   | 執行 `python scripts/analyze_positioning.py --start DATE` |
| 3, "視覺化", "chart", "plot"   | 執行 `python scripts/visualize_flows.py --weeks 52`       |
| 4, "監控", "monitor", "weekly" | 閱讀 `workflows/monitor.md` 並執行                        |
| 5, "學習", "方法論", "why"     | 閱讀 `references/methodology.md`                          |
| 提供參數 (如日期範圍、商品)    | 使用參數執行 `analyze_positioning.py`                     |

**所有腳本使用 CFTC Socrata API 取得真實資料，無模擬數據。**
</routing>

<reference_index>
**參考文件** (`references/`)

| 文件                | 內容                                   |
|---------------------|----------------------------------------|
| methodology.md      | COT 分析方法論、火力計算、訊號邏輯     |
| data-sources.md     | CFTC COT、FRED、Yahoo Finance 資料來源 |
| input-schema.md     | 完整輸入參數定義                       |
| contracts-map.md    | 期貨合約與商品群組對照表               |
| macro-indicators.md | 宏觀指標定義與代理序列                 |
</reference_index>

<workflows_index>
| Workflow       | Purpose              | 使用時機           |
|----------------|----------------------|--------------------|
| analyze.md     | 完整資金流向分析     | 需要深度分析時     |
| visualize.md   | 生成視覺化圖表       | 需要重建新聞圖表時 |
| monitor.md     | 週度監控與警報       | 每週五 COT 更新後  |
| cross-check.md | 宏觀與基本面交叉驗證 | 驗證敘事一致性時   |
</workflows_index>

<templates_index>
| Template           | Purpose            |
|--------------------|--------------------|
| output-json.md     | JSON 輸出結構定義  |
| output-markdown.md | Markdown 報告模板  |
| annotations.md     | 圖表標註規則對照表 |
</templates_index>

<scripts_index>
| Script                 | Command                           | Purpose                         |
|------------------------|-----------------------------------|---------------------------------|
| fetch_cot_data.py      | `--start 2023-01-01 --summary`    | 從 CFTC Socrata API 抓取 COT    |
| fetch_macro_data.py    | `--start 2025-01-01 --summary`    | 抓取宏觀指標（Yahoo/FRED）      |
| analyze_positioning.py | `--start 2023-01-01`              | 主分析腳本（自動抓取+計算）     |
| visualize_flows.py     | `--weeks 52`                      | 生成 Bloomberg 風格視覺化圖表   |
</scripts_index>

<input_schema_summary>

**必要參數**

| 參數          | 類型   | 說明                            |
|---------------|--------|---------------------------------|
| date_start    | string | 起始日期 (YYYY-MM-DD)           |
| date_end      | string | 結束日期 (YYYY-MM-DD)           |
| cot_report    | string | COT 類型 (legacy/disaggregated) |
| trader_group  | string | 交易者分類 (noncommercial)      |
| contracts_map | object | 合約→群組對照表                 |

**選用參數**

| 參數                     | 類型   | 預設值 | 說明                      |
|--------------------------|--------|--------|---------------------------|
| position_metric          | string | net    | 部位衡量 (net/long/short) |
| lookback_weeks_firepower | int    | 156    | 火力計算視窗（週）        |
| macro_indicators         | object | {...}  | 宏觀指標設定              |
| fundamental_inputs       | object | {...}  | 基本面資料設定            |
| event_window_days        | int    | 3      | Wed-Fri 事件視窗          |
| output_mode              | string | both   | 輸出格式 (markdown/json)  |

完整參數定義見 `references/input-schema.md`。

</input_schema_summary>

<output_schema_summary>
```json
{
  "skill": "track-agri-hedge-fund-positioning",
  "as_of": "2026-01-21",
  "summary": {
    "call": "Funds back & buying",
    "confidence": 0.72,
    "why": ["COT 週部位由負轉正", "分組同步改善", "宏觀順風"],
    "risks": ["COT 只到週二", "USDA 報告可能反轉"]
  },
  "latest_metrics": {
    "cot_week_end": "2026-01-21",
    "flow_total_contracts": 58,
    "flow_by_group_contracts": {
      "grains": 35, "oilseeds": 25, "meats": 5, "softs": 0
    },
    "buying_firepower": {
      "total": 0.63, "grains": 0.58, "oilseeds": 0.67
    },
    "macro_tailwind_score": 0.67
  },
  "annotations": [
    {"label": "macro_mood_bullish", "rule_hit": true, "evidence": ["USD down", "crude up"]}
  ]
}
```

完整輸出結構見 `templates/output-json.md`。
</output_schema_summary>

<success_criteria>
執行成功時應產出：

- [ ] 週流量時序（Grains/Oilseeds/Meats/Softs/Fiber/Dairy/Total）
- [ ] 最新一週的流量與淨部位
- [ ] 各群組的火力分數（buying_firepower）
- [ ] 宏觀順風評分（macro_tailwind_score）
- [ ] 可交易呼叫（call）與信心水準
- [ ] 圖表標註（annotations）與規則觸發
- [ ] 風險提示與下一步建議
- [ ] Bloomberg 風格視覺化圖表（output/agri_fund_positioning_YYYY-MM-DD.png）
</success_criteria>
