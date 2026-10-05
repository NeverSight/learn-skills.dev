---
name: bulk-evaluate
description: "子任務拆分與 Context 卸載工具。將可拆分的大型任務分成 N 個子 Ticket，各由 Agent 獨立執行，結論直接寫入 Ticket 不回報主線程。Use for: 批量檔案評估, 大型審查任務拆分, 任何需要讀取大量資料但結果可落地到 Ticket 的任務"
metadata:
  version: 1.0.0
---

# 子任務拆分與 Context 卸載工具

> 例外情況的批次計算公式: references/context-budget-formula.md

## 核心概念

**問題**：主線程的 context 有限。當一個任務需要讀取大量資料（N 個檔案、N 個模組、N 個報告），全部由主線程處理會溢出 context。

**解法**：把「讀取 + 分析 + 記錄」整包卸載給 Agent，主線程只負責拆分和統計。

**關鍵設計**：**Ticket 既是任務指派，也是分析報告的載體**。Agent 把結論直接寫入子 Ticket，主線程不接收完整內容 — 只看 Ticket 狀態和摘要統計。

```
傳統模式（主線程 context 溢出）:
  主線程讀取 N 個檔案 → 分析 → 產出報告 → context 爆炸

卸載模式（本 Skill）:
  主線程建立 N 個子 Ticket → 派發 Agent → Agent 寫入 Ticket → 主線程只看統計
```

## 適用場景

| 場景 | 子任務單位 | 每個子 Ticket 的內容 |
|------|-----------|-------------------|
| Agent/Skill 合規掃描 | 1 個定義檔案 | 評估結論 + 具體問題 |
| 規則一致性檢查 | 1 個規則檔案 | 衝突發現 + 建議修正 |
| 測試品質批量審查 | 1 個測試檔案/目錄 | 品質評分 + 改善建議 |
| 大型重構影響分析 | 1 個模組/目錄 | 影響範圍 + 遷移方案 |
| 多模組效能掃描 | 1 個效能熱點 | 瓶頸分析 + 優化建議 |

**通用判斷**：只要任務可以表述為「對 N 個獨立單位各做一次相同的分析」，就適用本 Skill。

## 與 `/parallel-evaluation` 的區別

| 維度 | `/parallel-evaluation` | `/bulk-evaluate` |
|------|----------------------|-----------------|
| 並行軸 | N 個視角 x 1 組目標 | 1 個標準 x N 個單位 |
| 產出物 | 彙整報告（回到主線程） | N 個子 Ticket（不回主線程） |
| Context 影響 | 主線程接收彙整結果 | 主線程只看統計摘要 |
| 目的 | 多角度快速評估 | 批量處理 + context 卸載 |

## 核心流程（5 步）

### Step 1: 識別子任務單位

確定每個子任務的處理單位和分析標準。

```
問自己：
1. 這個任務可以拆成幾個「對 X 做同一件事」的子任務？
2. 每個子任務的輸入是什麼？（一個檔案？一個模組？一個報告？）
3. 每個子任務的產出寫在哪？（Ticket 的哪個欄位？）
4. 分析標準是什麼？（參考文件？檢查清單？評估維度？）
```

### Step 2: 建立 Ticket 結構

```
/ticket create → 父 Ticket（匯總任務，type: ANA）
  |-- /ticket create --parent → 子 Ticket 1（單位 A 的分析）
  |-- /ticket create --parent → 子 Ticket 2（單位 B 的分析）
  └── ...
```

每個子 Ticket 的驗收條件統一為:
- [ ] 已讀取目標內容
- [ ] 已對照分析標準完成檢查
- [ ] 結論已寫入本 Ticket
- [ ] 具體發現已列出（如有）

### Step 3: 派發策略（單一職責原則）

**預設**: 1 個子任務 = 1 個 Agent

```
59 個評估目標 → 59 個獨立 Agent
每個 Agent 只負責 1 個目標
```

**為什麼不批次處理**:

| 維度 | 批次處理 | 1:1 派發 |
|------|---------|---------|
| 認知負擔 | Agent 需同時理解多個目標 | 只專注一個目標 |
| 判斷品質 | 目標間資訊互相干擾 | 零干擾，判斷最精準 |
| 失敗隔離 | 一批失敗影響多個子任務 | 單點失敗不擴散 |

這就是 context 卸載的核心目的：**讓每個 process 的任務目標清晰明確，避免額外資訊干擾判斷**。

> 例外：僅當平台限制無法派發足夠 Agent 時，才參考 references/context-budget-formula.md 計算合理批次大小。

### Step 4: 並行派發

每個 Agent 的 prompt 包含：

- 分析標準（參考文件路徑）
- 負責的 1 個子 Ticket（ID + 對應的輸入內容路徑）
- 產出要求（結論直接寫入子 Ticket）

Agent **不需要知道**：其他目標的存在、總共有幾個子任務、其他 Agent 的結論。

**Agent 類型選擇**:

| 需要寫入 Ticket | 推薦 Agent |
|----------------|-----------|
| 是 | general-purpose |
| 否（只讀分析） | Explore / Plan |

### Step 5: 彙整統計

所有 Agent 完成後，主線程只做統計（不讀取子 Ticket 全文）：

```
## 批量評估結果

**父 Ticket**: {ID}  **子任務總數**: {N}  **完成**: {M}/{N}

| 結論類別 | 數量 | 佔比 |
|---------|------|------|
| [類別 A] | X | X% |
| [類別 B] | X | X% |

### 需關注的子任務
| # | 子 Ticket | 結論 | 簡要 |
|---|----------|------|------|
```

更新父 Ticket 狀態，流程結束。

## 執行範例

### 範例: 59 個 Agent/Skill 合規掃描

```
Step 1: 子任務單位 = 每個 agent/skill 定義檔案
        分析標準 = design-guide (~25KB)
Step 2: 父 Ticket + 59 個子 Ticket
Step 3: 預設 1:1 → 59 個獨立 Agent
Step 4: 並行派發 59 個 general-purpose Agent，各處理 1 個子 Ticket
        每個 Agent 只讀取: design-guide + 自己負責的 1 個定義檔案
Step 5: 統計 59 個子 Ticket 結論 → 更新父 Ticket
```

**主線程 context 消耗**: 只有 Step 2（建 Ticket）和 Step 5（統計），不讀取 59 個定義檔案。
**每個 Agent context 消耗**: ~25KB 標準 + ~17KB 目標 = ~42KB，遠低於 context 上限。

## 相關文件

- references/context-budget-formula.md - 例外情況的批次計算公式
- parallel-evaluation skill（若已安裝）- 多視角並行評估（正交工具）；未安裝時仍可用本 skill 的批次評估機制，只是少了多視角正交評估這個互補工具
- .claude/pm-rules/parallel-dispatch.md - 並行派發指南
- .claude/pm-rules/task-splitting.md - 任務拆分指南

---

版本紀錄在同目錄的 `CHANGELOG.md`。
