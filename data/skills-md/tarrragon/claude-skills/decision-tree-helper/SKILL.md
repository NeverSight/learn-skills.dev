---
name: decision-tree-helper
description: "決策樹助手工具。快速評估任務複雜度，提供派發建議。Use when: (1) 任務複雜度快速評估, (2) 派發代理人建議, (3) 拆分策略建議, (4) 並行可行性評估"
metadata:
  version: 2.0.0
---

# 決策樹助手工具

## 核心功能

快速評估任務，提供派發和拆分建議。引用 `/cognitive-load` 的量化標準。

---

## 快速評估流程

### Step 1：任務識別

| 類型 | 識別關鍵字 | 下一步 |
|------|-----------|--------|
| 錯誤/失敗 | "failed", "error", "bug" | 強制派發 incident-responder |
| 新功能 | "實作", "建立", "新增" | SA 前置審查 |
| 修改 | "修改", "更新", "調整" | 複雜度評估 |
| 查詢 | "查詢", "進度", "狀態" | 直接回應 |

### Step 2：複雜度快速評估

回答以下問題（每題 0-2 分）：

| 問題 | 0 分 | 1 分 | 2 分 |
|------|------|------|------|
| 需要修改幾個檔案？ | 1-2 | 3-4 | 5+ |
| 跨越幾個架構層？ | 1 | 2 | 3+ |
| 依賴幾個模組？ | 0-1 | 2-3 | 4+ |
| 需要追蹤幾個狀態？ | 1-3 | 4-5 | 6+ |

**總分解讀**：

| 總分 | 複雜度 | 建議 |
|------|--------|------|
| 0-2 | 低 | 直接派發單一代理人 |
| 3-5 | 中 | 謹慎評估，考慮拆分 |
| 6-8 | 高 | 必須拆分後再派發 |

### Step 3：派發建議

根據任務類型和複雜度，提供派發建議。詳細派發決策樹見 `references/dispatch-decision-tree.md`。

---

## 派發決策（第零層明確性檢查）

二元判斷順序：

| 順序 | 判斷問題 | 是 | 否 |
|------|---------|----|----|
| 1 | 包含錯誤關鍵字？ | → 事件回應流程 | → 下一判斷 |
| 2 | 包含不確定性詞彙？ | → 確認機制 | → 下一判斷 |
| 3 | 複雜需求（3+ 代理人）？ | → 確認機制 | → 進入第一層 |

注意：決策樹最高優先為「Skill 匹配層」（已註冊 Skill 觸發條件匹配），其次為「第負一層」並行化評估，再進入第零層明確性檢查。完整派發決策樹見 `.claude/pm-rules/decision-tree.md`（v9.0.0 路由索引），派發閘門見 `.claude/pm-rules/dispatch-gate.md`。

---

## 代理人選擇指南

### 系統級代理人

| 代理人 | 觸發條件 | 優先級 |
|--------|---------|--------|
| incident-responder | 錯誤/失敗 | 最高 |
| system-analyst | 新功能/架構變更 | 高 |
| security-reviewer | 安全相關 | 高 |
| system-designer | UI 規範需求 | 中 |
| system-engineer | 環境/編譯問題 | 中 |

### TDD 階段代理人

| 階段 | 代理人 | 前置條件 |
|------|--------|---------|
| Phase 1 | lavender-interface-designer | SA 審查通過 |
| Phase 2 | sage-test-architect | Phase 1 完成 |
| Phase 3a | pepper-test-implementer | Phase 2 完成 |
| Phase 3b | parsley-flutter-developer | Phase 3a 完成 |
| Phase 4 | cinnamon-refactor-owl | Phase 3b 測試全過 |

---

## 拆分策略指南

本工具提供快速評估；詳細拆分策略見 `references/splitting-strategies.md`。

### 快速決策

- **按架構層**：跨多層時，由底層向上拆分
- **按功能模組**：涉及多模組時，共用模組先完成，獨立可並行
- **按操作類型**：混合重命名/邏輯修改時，機械操作可並行，邏輯需序列

---

## 並行派發判斷

### 快速檢查清單

- [ ] 任務間無檔案重疊
- [ ] 任務間無邏輯依賴
- [ ] 任務在同一架構層級
- [ ] 操作類型為機械性（重命名/格式化）
- [ ] 並行派發後執行 `git diff --stat` 驗證實際變更

### 並行適用情境

| 情境 | 範例 | 並行數量 |
|------|------|---------|
| 同層重命名 | 所有 Repository 檔案變數重命名 | 無上限 |
| 同層格式化 | 所有 Widget 檔案 lint fix | 無上限 |
| 獨立模組 | 各獨立 Feature 的相同修改 | 無上限 |
| 無依賴測試 | 各模組的獨立單元測試 | 無上限 |

### 不適用並行情境

| 情境 | 原因 | 處理方式 |
|------|------|---------|
| TDD 跨階段 | 階段有順序依賴 | 序列執行 |
| 跨架構層 | 可能有設計影響 | 序列執行 |
| 有共享狀態 | 競爭條件風險 | 序列執行 |
| 邏輯依賴 | 結果影響後續 | 按依賴序列 |

---

## 使用方式

### 任務評估

通過 `/decision-tree-helper assess "{任務描述}"` 快速評估：

1. 任務類型識別
2. 複雜度評估
3. 派發建議
4. 拆分建議（如需要）

### 派發確認

通過 `/decision-tree-helper confirm {代理人} "{任務描述}"` 確認派發：

1. 派發是否合適
2. 潛在問題
3. 替代建議（如有）

### 並行檢查

通過 `/decision-tree-helper check-parallel {Ticket1} {Ticket2}` 檢查並行可行性：

1. 並行安全性
2. 潛在衝突
3. 建議執行順序

---

## 相關文件

- [決策樹助手決策記錄格式](references/decision-record-template.md)
- [拆分策略詳細指南](references/splitting-strategies.md)
- [派發決策樹完整版](references/dispatch-decision-tree.md)
- 認知負擔量化標準：cognitive-load-assessment skill 的 thresholds.md（若已安裝）；未安裝時可參考 `.claude/rules/core/cognitive-load.md` 的量化標準表（指數閾值、任務拆分閾值）作替代
- [主線程決策樹](.claude/pm-rules/decision-tree.md)
- [任務拆分指南](.claude/pm-rules/task-splitting.md)

---

版本紀錄在同目錄的 `CHANGELOG.md`。
