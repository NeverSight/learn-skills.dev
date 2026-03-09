---
name: vault-report
description: >-
  Generate comprehensive knowledge graph reports for Obsidian vaults.
  Combines multiple graph queries (vault-stats, hubs, bridges, orphans-rich)
  to produce a structured 4-module analysis report with data summary tables.
  Requires obsidian-graph-query skill installed. Use for: vault report,
  knowledge report, vault analysis, vault health, knowledge graph report,
  知識圖譜報告, vault 分析.
---

# Vault 知識圖譜報告

一次性產出全 vault 的結構化知識圖譜分析報告。組合 obsidian-graph-query 的多個查詢模板，產出四個分析模組 + 數據匯總。

---

## 前置條件

本 skill 依賴 **obsidian-graph-query** skill。執行前：

1. 確認 `obsidian-graph-query` skill 已安裝（檢查同層 `../obsidian-graph-query/SKILL.md` 是否存在）
2. 讀取 `../obsidian-graph-query/references/vault-config.md` 取得 CLI 路徑、vault 名稱、排除資料夾
3. 查詢模板在 `../obsidian-graph-query/references/query-templates.md`
4. 執行方式遵循 obsidian-graph-query 的「執行模式」章節（讀模板 → 代入參數 → 寫暫存檔 → CLI eval）

---

## 適用場景

- 「分析我的知識庫結構」
- 「產出我的 vault 的知識圖譜報告」
- 「我的筆記庫健不健康？」
- 「跟去年的分析報告比對一下」

---

## 報告框架（4 模組 + 數據匯總）

| 模組 | 內容 | 主要數據來源 |
|------|------|-------------|
| 一：Vault 全景概覽 | 規模、孤島率、連通性、資料夾分布 | vault-stats |
| 二：活躍度趨勢 | 月度產出、活躍高峰月 | vault-stats (monthlyCreation) |
| 三：知識重心與結構 | Hub Top 10、領域密度、跨域連結、孤島分布 | vault-stats + hubs + orphans-rich |
| 四：知識價值與風險 | 被引用最多、只出不進、Bridge 風險 | hubs + bridges + vault-stats |
| 數據匯總 | 結構化表格（供視覺化工具） | 以上全部 |

---

## 執行流程

```
步驟 1. vault-stats（query-templates.md §8，無參數）
   → 模組一：totalNotes, totalLinks, avgLinksPerNote, orphanCount/Ratio,
            componentCount, largestComponent/Ratio, folderStats
   → 模組二：monthlyCreation
   → 模組三：crossFolderLinks/Ratio
   → 模組四：outOnlyCount/Notes

步驟 2. hubs(TOP_N=10)（query-templates.md §5）
   → 模組三：Hub 筆記 Top 10
   → 模組四：被引用最多的筆記（同一結果按 inDegree 排序）

步驟 3. hubs(FOLDER_FILTER=X) × 主要資料夾
   → 從步驟 1 的 folderStats 取筆記數前 5 大的資料夾
   → 每個資料夾跑一次 hubs(TOP_N=5, FOLDER_FILTER='資料夾/')
   → 模組三：各領域連結密度比較（密度 = 該領域總連結 / 該領域筆記數）

步驟 4. orphans-rich（query-templates.md §6，無 FOLDER_FILTER）
   → 模組三：孤島分布（按資料夾統計）

步驟 5. bridges（query-templates.md §4，無參數）
   → 模組四：articulationPoints 前 10 + bridgesByFolder

步驟 6. Agent 彙整上述 JSON → 產出 Markdown 報告
```

> 步驟 1-2 可同時執行（無依賴）；步驟 3 依賴步驟 1 的結果。

---

## 報告產出格式

```markdown
# Vault 知識圖譜報告

> 產出時間：YYYY-MM-DD | Vault：<vault-name> | 筆記數：X

## 一、Vault 全景概覽

| 指標 | 數值 |
|------|------|
| 筆記總數 | X |
| 連結總數 | X |
| 平均每篇連結數 | X.XX |
| 孤島數量 | X（佔 XX.X%） |
| 連通分量數 | X |
| 最大分量涵蓋率 | XX.X% |

### 資料夾分布

| 資料夾 | 筆記數 | 連結數 | 孤島數 | 密度 |
|--------|--------|--------|--------|------|
| ... | ... | ... | ... | X.XX |

## 二、活躍度趨勢

| 月份 | 新增筆記數 |
|------|-----------|
| YYYY-MM | X |

活躍高峰月：YYYY-MM（X 篇）

## 三、知識重心與結構

### Hub 筆記 Top 10

| 排名 | 筆記 | 入度 | 出度 | 總連結 |
|------|------|------|------|--------|
| 1 | ... | ... | ... | ... |

### 各領域連結密度

| 領域 | 筆記數 | 連結數 | 密度 |
|------|--------|--------|------|
| ... | ... | ... | X.XX |

### 跨領域連結

跨資料夾連結數：X（佔總連結 XX.X%）

### 孤島分布

| 資料夾 | 孤島數 | 佔該資料夾 % |
|--------|--------|-------------|
| ... | ... | XX.X% |

## 四、知識價值與風險

### 被引用最多的筆記

（hubs 按 inDegree 排序前 10）

### 只出不進的筆記

outDegree > 0、inDegree = 0 的筆記共 X 篇

### Bridge 關鍵節點

（bridges articulationPoints 前 10，含 degree）

### Bridge 風險分布

| 資料夾 | Bridge 邊數 |
|--------|------------|
| ... | ... |

## 數據匯總

（前四模組的核心數據整理成 CSV-ready 表格，方便丟給視覺化工具）
```

---

## 延伸用法：與定性報告交叉驗證

產出報告後，可與既有的定性分析報告（如 NotebookLM 年度回顧）交叉驗證：

| 測試 | 做法 |
|------|------|
| **A：跨域連結驗證** | vault-stats `crossFolderLinks` → path（§2）找跨域路徑 → LLM 讀筆記判斷語意關係 |
| **B：Hub 語意理解** | hubs Top 10 → LLM 讀 hub 筆記內容 → 解釋在知識體系中扮演的角色 |
| **C：Bridge 風險解讀** | bridges 找關鍵節點 → LLM 讀 bridge + 兩側鄰居 → 解釋「如果移除會怎樣」 |
| **D：孤島關聯推理** | orphans-rich 找孤島 → neighbors（§1）找最近 connected → LLM 判斷「該不該連」 |
