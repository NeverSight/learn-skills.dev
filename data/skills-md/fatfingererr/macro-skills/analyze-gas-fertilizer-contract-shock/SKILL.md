---
name: analyze-gas-fertilizer-contract-shock
description: 用天然氣與化肥價格的日頻數據，檢驗「天然氣暴漲→化肥供應受限/毀約→化肥飆價」敘事是否成立，輸出可標註到圖上的關鍵轉折點與領先落後分析。
---

<essential_principles>

<principle name="narrative_verification">
**敘事驗證而非預測**

本技能專注於「用數據檢驗敘事」：
- 輸入：社群/新聞宣稱「天然氣暴漲導致化肥供應/價格異常」
- 輸出：時間序列上的因果假說檢驗結果

不做價格預測，只回答：「這個敘事在數據上是否有支撐？」
</principle>

<principle name="three_part_test">
**三段式因果檢驗**

敘事成立需要三段條件同時滿足：

| 階段 | 條件 | 檢驗方式 |
|------|------|----------|
| A 段 | 天然氣出現 shock regime | z-score 或斜率突破閾值 |
| B 段 | 化肥在 A 段後出現 spike | 同法檢驗，且起點晚於天然氣 |
| C 段 | 領先落後關係支持因果 | cross-correlation 顯示 gas 領先 fert |

若 A→B→C 成立，敘事有量化支撐；否則提供替代解釋。
</principle>

<principle name="regime_detection">
**Regime 偵測邏輯**

使用 rolling z-score + 斜率雙重確認：

```python
# z-score 偵測
z_t = (r_t - rolling_mean(r, window)) / rolling_std(r, window)
shock = z_t >= threshold_z  # 預設 3.0

# 斜率偵測（補充）
slope_t = (price_t / price_{t-k} - 1) / k
shock |= slope_t >= threshold_slope  # 預設 1.5%/day
```

連續 shock 日合併為 regime，輸出起點/終點/峰值。
</principle>

<principle name="lead_lag_interpretation">
**領先落後解讀**

Cross-correlation 結果解讀：

| lag 值 | 意義 | 敘事支撐度 |
|--------|------|-----------|
| lag > 0 | 天然氣領先化肥 | 高（符合預期） |
| lag ≈ 0 | 同時變動 | 中（共同驅動） |
| lag < 0 | 化肥領先天然氣 | 低（敘事較弱） |

合理領先期：1-8 週（7-56 天）
</principle>

<principle name="data_source_priority">
**數據來源優先順序**

主要：TradingEconomics（透過全自動 Chrome CDP 爬取）
備援：FRED Henry Hub + World Bank Pink Sheet

**全自動 Chrome CDP 爬取**：
腳本自動完成以下步驟，無需手動操作：
1. 自動啟動 Chrome 調試模式
2. 開啟 TradingEconomics 頁面並等待圖表載入
3. 透過 WebSocket 連接執行 JavaScript 提取 Highcharts 數據
4. 自動導航到多個商品頁面（如天然氣→化肥）
5. 完成後自動關閉 Chrome

完全繞過 Cloudflare，無需手動驗證。
</principle>

</essential_principles>

<objective>
檢驗「天然氣暴漲→化肥飆價」的因果假說。

輸出三層分析：
1. **Shock Regimes**: 天然氣與化肥的拋物線/暴衝區間
2. **Lead-Lag Test**: 領先落後相關分析
3. **Narrative Assessment**: 敘事可信度判斷
</objective>

<quick_start>

**全自動模式：一鍵完成數據抓取、分析與視覺化**

腳本會自動啟動 Chrome、抓取數據、關閉 Chrome，無需手動操作。

**Step 1：安裝依賴**
```bash
pip install requests websocket-client pandas numpy matplotlib scipy
```

**Step 2：全自動抓取數據**（自動啟動/關閉 Chrome）
```bash
cd scripts
python fetch_te_data.py --symbol natural-gas --symbol urea
```

**Step 3：執行因果假說分析**
```bash
python gas_fertilizer_analyzer.py \
  --gas-file ../data/cache/natural-gas.csv \
  --fert-file ../data/cache/urea.csv \
  --output ../data/analysis_result.json
```

**Step 4：生成視覺化圖表**（Bloomberg 風格）
```bash
python visualize_shock_regimes.py
# 自動輸出到: output/gas_fert_shock_YYYY-MM-DD.png
```

**輸出範例**：
```json
{
  "signal": "narrative_supported",
  "confidence": "medium",
  "gas_shock_regimes": [
    {"start": "2026-01-20", "peak": "2026-01-22", "regime_return_pct": 29.1}
  ],
  "fert_spike_regimes": [
    {"start": "2025-10-27", "peak": "2025-10-27", "regime_return_pct": 0.0}
  ],
  "lead_lag_test": {
    "best_lag_days_gas_leads_fert": 21,
    "best_corr": 0.131
  },
  "interpretation": "天然氣領先化肥約 21 天，敘事有量化支撐"
}
```

**注意**：首次執行時，Chrome 會自動啟動並在背景抓取數據（約 60 秒），完成後自動關閉。

</quick_start>

<intake>
需要進行什麼分析？

1. **快速檢查** - 查看最近是否有天然氣 shock 及化肥跟隨
2. **完整分析** - 執行三段式因果檢驗並生成報告
3. **合約對沖假說** - 輸入合約價格，計算價差壓力指標
4. **方法論學習** - 了解 shock 偵測與領先落後分析原理

**請選擇或直接提供分析參數。**
</intake>

<routing>
| Response                       | Action                                     |
|--------------------------------|--------------------------------------------|
| 1, "快速", "quick", "check"    | 閱讀 `workflows/quick-check.md` 並執行     |
| 2, "完整", "full", "analyze"   | 閱讀 `workflows/analyze.md` 並執行         |
| 3, "合約", "對沖", "hedge"     | 閱讀 `workflows/hedge-hypothesis.md` 並執行|
| 4, "學習", "方法論", "why"     | 閱讀 `references/methodology.md`           |
| 提供參數 (如日期/商品)          | 閱讀 `workflows/analyze.md` 並使用參數執行 |

**路由後，閱讀對應文件並執行。**
</routing>

<directory_structure>
```
analyze-gas-fertilizer-contract-shock/
├── SKILL.md                           # 本文件（路由器）
├── skill.yaml                         # 前端展示元數據
├── manifest.json                      # 技能元資料
├── workflows/
│   ├── analyze.md                     # 完整三段式分析工作流
│   ├── quick-check.md                 # 快速檢查工作流
│   └── hedge-hypothesis.md            # 合約對沖假說分析
├── references/
│   ├── data-sources.md                # Chrome CDP 爬蟲說明
│   ├── methodology.md                 # Shock 偵測與領先落後方法論
│   ├── input-schema.md                # 輸入參數定義
│   └── historical-episodes.md         # 歷史案例對照
├── templates/
│   ├── output-json.md                 # JSON 輸出模板
│   └── output-markdown.md             # Markdown 報告模板
├── scripts/
│   ├── fetch_te_data.py               # TradingEconomics CDP 爬蟲
│   ├── gas_fertilizer_analyzer.py     # 主分析腳本
│   └── visualize_shock_regimes.py     # Shock regime 視覺化
├── data/                              # 數據快取目錄
│   └── cache/                         # 快取檔案
└── examples/
    └── sample_output.json             # 範例輸出
```
</directory_structure>

<reference_index>

**方法論**: references/methodology.md
- Shock/Spike 偵測邏輯（z-score + 斜率）
- 領先落後相關分析
- Regime 合併演算法

**資料來源**: references/data-sources.md
- TradingEconomics Chrome CDP 爬蟲說明
- 天然氣與化肥商品代碼
- 備援數據源（FRED/World Bank）

**輸入參數**: references/input-schema.md
- 完整參數定義與預設值
- te_symbols、spike_detection、lead_lag 等

**歷史案例**: references/historical-episodes.md
- 2021-2022 歐洲天然氣危機
- 2022 俄烏衝突期間
- 季節性波動案例

</reference_index>

<workflows_index>
| Workflow            | Purpose               | 使用時機                   |
|---------------------|-----------------------|---------------------------|
| analyze.md          | 完整三段式因果分析     | 需要驗證敘事時             |
| quick-check.md      | 快速檢查最近 shock     | 日常監控或快速回答         |
| hedge-hypothesis.md | 合約對沖假說分析       | 給定合約價格計算價差壓力   |
</workflows_index>

<templates_index>
| Template           | Purpose                    |
|--------------------|----------------------------|
| output-json.md     | JSON 輸出結構定義           |
| output-markdown.md | Markdown 報告模板           |
</templates_index>

<scripts_index>
| Script                       | Command                                      | Purpose                    |
|------------------------------|----------------------------------------------|----------------------------|
| fetch_te_data.py             | `--symbol natural-gas --symbol urea`         | 全自動 CDP 爬取（自動啟動/關閉 Chrome） |
| gas_fertilizer_analyzer.py   | `--gas-file X.csv --fert-file Y.csv`         | 完整三段式因果分析          |
| visualize_shock_regimes.py   | （無參數，自動讀取快取）                      | Bloomberg 風格視覺化圖表    |
</scripts_index>

<input_schema>

<parameter name="start_date" required="true">
**Type**: string (ISO YYYY-MM-DD)
**Description**: 分析起始日期
**Example**: "2025-08-01"
</parameter>

<parameter name="end_date" required="true">
**Type**: string (ISO YYYY-MM-DD)
**Description**: 分析結束日期
**Example**: "2026-02-01"
</parameter>

<parameter name="te_symbols" required="true">
**Type**: object
**Description**: TradingEconomics 商品代碼
```json
{
  "natural_gas": "natural-gas",  // 或 "Natural Gas"
  "fertilizer": "urea"           // 或 "dap", "fertilizer"
}
```
</parameter>

<parameter name="spike_detection" required="false">
**Type**: object
**Defaults**:
```json
{
  "return_window": 1,
  "z_window": 60,
  "parabolic_threshold": {"z": 3.0, "slope_pct_per_day": 1.5}
}
```
</parameter>

<parameter name="lead_lag" required="false">
**Type**: object
**Defaults**:
```json
{
  "max_lag_days": 60,
  "method": "corr_returns"
}
```
</parameter>

</input_schema>

<output_schema>
參見 `templates/output-json.md` 的完整結構定義。

**摘要**：
```json
{
  "signal": "narrative_supported | narrative_weak | inconclusive",
  "confidence": "high | medium | low",
  "gas_shock_regimes": [...],
  "fert_spike_regimes": [...],
  "lead_lag_test": {
    "best_lag_days": 12,
    "best_corr": 0.41,
    "interpretation": "gas 領先 fert"
  },
  "narrative_assessment": "三段式檢驗結果摘要",
  "artifacts": {
    "charts": ["output/gas_fert_shock.png"]
  }
}
```
</output_schema>

<success_criteria>
分析成功時應產出：

- [ ] 天然氣與化肥的 shock/spike regime 清單
- [ ] 領先落後相關分析結果
- [ ] 三段式因果檢驗判斷
- [ ] 敘事可信度與替代解釋
- [ ] **Shock Regime 對比圖**（output/gas_fert_shock_YYYY-MM-DD.png）
- [ ] 可操作的宏觀解讀
- [ ] 明確標註資料限制與假設
</success_criteria>
