---
name: search-tools-guide
description: "搜尋工具使用指南。用於：(1) 選擇正確的搜尋工具, (2) 三 MCP 工作流決策樹（cbm 概念搜尋 / codegraph 呼叫圖 / serena 型別感知), (3) rg 精確文字搜尋, (4) LSP/Serena 符號搜尋, (5) 工具安裝與故障排除"
metadata:
  version: 5.2.0
---

# 搜尋工具指南

---

## 工具總覽與選擇

本專案的搜尋工具經過系列比較測試驗證，各有明確定位。

### 工具定位

| 工具 | 類型 | 定位 | 獨佔能力 |
|------|------|------|---------|
| **Grep (rg)** | 文字（正則） | 日常主力搜尋 | 正則搜尋、PCRE2、壓縮檔、多編碼、分頁、統計 |
| **WebSearch** | 網頁搜尋 | 唯一網頁搜尋工具 | 技術文件查詢、API 用法、版本資訊 |
| **Grep+Glob+Read** | 多步組合 | 多步驟研究預設方案 | 架構追蹤、程式碼路徑分析 |
| **Serena / LSP** | 語意（符號感知） | 符號分析 | 符號定義/引用追蹤、重構、型別資訊（Dart 支援度最高） |
| **Dart MCP** | 語意（Dart 專用） | Dart 開發工具 | `analyze_files`、`dart_format`、`dart_fix` |
| **內建 Glob** | 檔名模式 | 檔案定位 | 按名稱找檔案 |
| **ToolSearch** | Meta-Tool | CC runtime 能力發現 | 發現 / 載入 deferred tools（TaskOutput/SendMessage/WebFetch 等） |

### 選擇決策樹

```
搜尋需求
    |
    v
需要搜尋什麼？
    |
    +-- 符號定義/引用/重構 --> Serena / LSP / Dart MCP
    |
    +-- 網頁資訊（技術文件、API、版本） --> WebSearch
    |
    +-- 跨檔案架構追蹤 --> Grep + Glob + Read 組合
    |   例：追蹤 Ticket 系統從 create 到 complete 的完整路徑
    |
    +-- 精確文字/正則模式 --> Grep（優先）或 rg（進階）
    |   例：`class\s+\w+\s+extends\s+StatelessWidget`
    |
    +-- 按檔名找檔案 --> 內建 Glob
    |   例：`**/*.dart`
    |
    +-- CC runtime 能力（觀察代理人、排程、用戶提問、網頁抓取） --> ToolSearch
        例：「我需要查背景代理人還在不在執行」「我要發送新指令給代理人」
```

### 什麼時候用什麼

| 場景 | 首選工具 | 備選 | 範例 |
|------|---------|------|------|
| 找某個類別定義 | Serena `find_symbol` | `rg "class ClassName"` | 找 BookRepository |
| 找某個方法的所有呼叫 | Serena `find_referencing_symbols` | `rg "\.methodName\("` | 找 fetchBooks 引用 |
| 找精確字串 | Grep / rg -F | - | 找 hardcoded 值 |
| 找正則模式 | Grep | rg（進階場景） | 找 import 模式 |
| PCRE2 (lookaround) | rg -P | 無替代 | 進階正則 |
| 搜尋壓縮檔 | rg -z | 無替代 | 搜尋 .gz |
| 查看符號型別 | Dart MCP `hover` | Serena `find_symbol` | 確認回傳型別 |
| 靜態分析 | Dart MCP `analyze_files` | 無替代 | 找 lint 問題 |
| 找檔案路徑 | 內建 Glob | rg -l | 找 *.test.dart |
| 技術文件查詢 | WebSearch | - | Flutter API、套件文件 |
| 跨檔案架構理解 | Glob + Grep + Read | - | 追蹤完整程式碼路徑 |
| 查詢背景代理人是否仍執行 | ToolSearch → TaskOutput | - | 非侵入性 status 查詢 |
| 向執行中的代理人發送指令 | ToolSearch → SendMessage | - | 即時控制背景代理人 |
| 派發背景任務 | ToolSearch → TaskCreate | Agent tool | 手動建立 background task |
| 停止失控代理人 | ToolSearch → TaskStop | - | 安全中止任務 |
| 抓取外部網頁 / 文件 | ToolSearch → WebFetch | WebSearch | 精準抓指定 URL |
| 排程定期任務 | ToolSearch → CronCreate | - | 定期觸發 |

---

## Code Intelligence MCP 三刀流

本專案配置三個 Code Intelligence MCP server（codebase-memory-mcp / codegraph / serena），各有不同定位：cbm 主打語言無關的概念（模糊）搜尋，codegraph 主打自動增量的呼叫圖追蹤，serena 主打型別感知的安全編輯（唯一支援 rename）。三者按需求切換，不同時使用。

完整九維度設計對照表、三刀流選擇決策樹、JS Chrome Extension 場景組合範例：`references/code-intelligence-mcp-tools.md`

---

## Claude Code Meta-Tools（平台能力發現）

### ToolSearch — Deferred Tools 發現機制

Claude Code runtime 將部分工具以 **deferred 模式** 提供。deferred tools 的 schema **不預先載入**，必須透過 `ToolSearch` 搜尋並載入後才能呼叫。每個 session 啟動時 runtime 會在 system-reminder 中列出所有 deferred tools 名稱。

**核心規則**：遇到「我想做 X 但不知道怎麼做」時，**在宣告「做不到」或選擇「限制性解法」（禁止、防護、規避）之前**，必須先執行 `ToolSearch` 搜尋是否有對應的 deferred tool（完整五問窮盡檢查見 `.claude/rules/core/tool-discovery.md`）。

```
# 精確載入指定工具（最常用）
ToolSearch(query="select:TaskOutput")
ToolSearch(query="select:TaskOutput,SendMessage,TaskCreate")

# 關鍵字搜尋（探索未知能力）
ToolSearch(query="background task status")
```

返回值會以 `<function>{...}</function>` 格式提供工具 schema，載入後即可如一般工具呼叫。Session 當下可用的 deferred tools 清單以 system-reminder 為準。

常見 deferred tools 用途對照表、發現工作流程圖、反模式清單、相關規則：`references/meta-tools-deferred-discovery.md`

---

## rg (ripgrep) - 日常主力搜尋

**ripgrep** 是基於 Rust 的高效能正則搜尋工具，是 Claude Code 內建 Grep 的底層引擎，比 GNU grep 快約 33 倍（Linux kernel 搜尋基準）且預設自動遵守 `.gitignore` 規則。一般搜尋用內建 Grep 即可，需要 PCRE2、壓縮檔搜尋、多編碼等進階功能時才需要以 bash 呼叫 rg。

安裝方式、rg vs 內建 Grep 完整功能對照、常用指令速查、語言框架範例、同義詞擴展的概念性搜尋技巧：`references/rg-ripgrep-usage.md`

---

## Serena / LSP / Dart MCP - 符號導航與程式碼理解

**Serena**、**LSP** 和 **Dart MCP** 提供語意感知的程式碼導航，理解符號定義、引用關係和型別系統，是唯一能做到精確重構的工具類別。適用於有 LSP 插件的語言（Dart / JavaScript / TypeScript / Python 等）；純文字檔（`.md` / `.txt` / `.yaml` / `.json`）無 LSP 結構優勢，應改用 Edit / Grep。日常搜尋無法用 Serena 完全取代 rg。

Serena / Dart MCP 完整工具表、`search_for_pattern` vs Grep 詳細比較、適用場景對照：`references/serena-lsp-symbol-navigation.md`

---

## 三 MCP 核心能力速查表（版本無關）

> **為何不列具體工具動詞名**：MCP server 跨版本會改名 / 增刪工具，安裝方式也決定 server 前綴（PC-173 三層漂移）。硬編碼工具動詞名必然與實機暴露漂移，讀者照抄會呼叫到不存在的工具而浪費回合。本速查表只列「server 前綴 + 能力分類」；**確切工具動詞名以 `ToolSearch` 當下發現為準**——session 啟動時 system-reminder 列出的 deferred tools 清單是唯一 ground truth。

### server 前綴對照

| MCP server | 本專案 server 前綴 | 安裝方式註記 |
|-----------|------------------|-------------|
| CodeGraph | `mcp__codegraph__*` | 專案層級 `.mcp.json` |
| codebase-memory-mcp (cbm) | `mcp__codebase-memory-mcp__*` | 專案層級 `.mcp.json`（注意前綴含連字號，非底線） |
| Serena | user-level 安裝為 `mcp__serena__*`；plugin marketplace 安裝為 `mcp__plugin_serena_serena__*` | 前綴依安裝方式而定，兩者工具子集不完全相同（部分工具僅 plugin 版有） |

### 能力 → server 對照（動詞名請 ToolSearch 發現）

| 能力 | 首選 server | 發現方式（取代硬編碼名） |
|------|-----------|----------------------|
| 索引就緒確認 / 重建 | CodeGraph | `ToolSearch(query="codegraph status index")` 取當前名 |
| 符號定義搜尋（跨語言精確） | CodeGraph / Serena | `ToolSearch(query="codegraph search")` / `ToolSearch(query="serena find symbol")` |
| 呼叫者 / 被呼叫者追蹤 | CodeGraph | `ToolSearch(query="codegraph callers callees")` |
| 影響分析（blast radius） | CodeGraph / Serena | `ToolSearch(query="codegraph impact")` |
| 語義 / 概念搜尋（模糊召回） | cbm | `ToolSearch(query="codebase memory search graph")` |
| 索引狀態 / 建立 | cbm | `ToolSearch(query="codebase memory index")` |
| 安全重命名 / symbol 編輯 | Serena [唯一] | `ToolSearch(query="serena rename replace symbol")` |
| 檔案符號總覽 | Serena | `ToolSearch(query="serena symbols overview")` |

**使用方式**：先用能力關鍵字 `ToolSearch` 發現當前確切工具名（或直接查 session system-reminder 的 deferred tools 清單），再以 `ToolSearch(query="select:<發現到的完整工具名>")` 載入 schema 後呼叫。**禁止從本文件複製硬編碼工具動詞名直接呼叫**——本表刻意不列動詞名以杜絕漂移。

> **終端 redaction 提醒**（PC-173）：bash `grep` / `rg` 輸出會把實機可呼叫的 MCP 工具名替換為 `n`（如 `mcp__codegraph__n`）。驗證 MCP 工具名引用時改用 Read 工具，勿單憑 bash grep 輸出判讀。

**cbm 深度參考**：CLI 用法、`.claude/` 不索引限制、cbm vs codegraph vs serena 分工速查 → `references/codebase-memory-tool.md`

---

## WebSearch - 網頁搜尋

### 核心特性

WebSearch 是 Claude Code 內建的網頁搜尋工具，零配置、穩定可用。

| 特性 | 說明 |
|------|------|
| 回應速度 | ~3 秒 |
| 英文查詢品質 | 4-5/5（API 用法、技術文件表現優秀） |
| 中文在地化品質 | 2-3/5（可能混入簡體中文或英文結果） |
| 整合度 | 原生整合到對話，自動提供結構化摘要和來源連結 |

### 中文查詢建議

- 搭配英文關鍵字提升搜尋精確度
- 注意搜尋結果可能混入簡體中文來源
- 重要的在地化資訊建議交叉驗證

---

## 多步驟研究方案

### Grep + Glob + Read 組合

多步驟程式碼架構研究的預設方案，無需任何外部依賴。

**實測結果**：
- 追蹤 Ticket 系統生命週期（8 個核心檔案）：~45 秒，完整度 5/5
- 追蹤 Hook 驗證邏輯（831 行 Python）：~20 秒，完整度 5/5

### 標準研究流程

```
步驟 1: Glob 定位相關檔案
    例：Glob **/*ticket*.py

步驟 2: Grep 搜尋關鍵字
    例：Grep "ticket.*create|lifecycle"

步驟 3: Read 深度閱讀核心檔案
    例：Read ticket.py -> 理解入口和分發

步驟 4: 重複步驟 2-3 追蹤呼叫鏈
    例：Grep "TicketLifecycle" -> Read lifecycle.py
```

---

## 環境檢查與故障排除

### 安裝狀態檢查

```bash
rg --version
```

### rg 常見問題

| 問題 | 原因 | 解決 |
|------|------|------|
| command not found | 未安裝 | `brew install ripgrep` |
| 搜尋結果不完整 | .gitignore 排除 | `rg --no-ignore "pattern"` |
| PCRE2 不可用 | 編譯時未啟用 | `cargo install ripgrep --features pcre2` |

### 三 MCP 已知限制速查

| 限制 | 影響 | Workaround |
|------|------|----------|
| cbm MCP namespace（2026-06-24 起已曝光於 ToolSearch deferred） | 預設可直接呼叫 `mcp__codebase-memory-mcp__*`；僅某些環境（fresh subprocess / headless）ToolSearch 可能找不到 | 首選 MCP deferred tools；不可用時 fallback CLI：`codebase-memory-mcp cli <tool> '<json>'`（詳見 `references/codebase-memory-tool.md` §1）。前綴以實機 deferred 清單為準（正確形含連字號 `mcp__codebase-memory-mcp__`，非底線） |
| cbm 對 `.claude/` 不索引（v0.6.1 hardcoded） | `.claude/` 範圍搜尋 cbm 結果為空 | `.claude/` 範圍改用 `rg` + 必要時 serena（詳見 `references/codebase-memory-tool.md` §2） |
| codegraph 冷啟動需載 embedding model | fresh subprocess 30-60s 不可用 | 用 CC runtime 內已暖機的 `mcp__codegraph__*` deferred tools |

---

## 比較測試結論總覽

本指南的工具定位和建議基於以下比較測試結論：

| 比較項目 | 核心結論 |
|---------|---------|
| WebSearch 網頁搜尋效果 | WebSearch 是唯一推薦的網頁搜尋工具 |
| 多步驟研究效果 | Grep+Glob+Read 組合是預設選擇 |
| 語意搜尋 vs 文字搜尋 | rg 精確度 ~90-94%，同義詞弱點可用多 Pattern 改善 |
| Serena 結構化導航 | Serena LSP 對配置 LSP 的語言（Dart / JS / TS / Python via pyright）皆有效；非符號級操作（如純文字搜尋）Grep 步驟數更少 |
| rg vs Serena search_for_pattern | 日常搜尋無法用 Serena 取代 rg |

---

版本紀錄在同目錄的 `CHANGELOG.md`。
