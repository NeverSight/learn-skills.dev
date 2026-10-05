---
name: tech-debt-capture
description: "Automated Phase 4 technical debt capture and Ticket creation. Parses work-log evaluation reports, extracts TD (Technical Debt) items, and creates Atomic Tickets using Single Responsibility Principle. Use: Extract technical debts from Phase 4 evaluation → Auto-map to target versions → Create tickets → Update todolist."
metadata:
  version: 1.1.0
---

# Tech Debt Capture

Automated technical debt capture from Phase 4 evaluation reports and conversion to Atomic Tickets.

## 核心功能

**目的**: 將 Phase 4 重構評估識別的技術債務自動轉換為可執行的 Ticket

**工作流程**:

1. 解析工作日誌中的技術債務表格
2. 根據風險等級決定目標版本
3. 建立 Atomic Ticket 檔案
4. 更新 todolist.yaml 技術債務追蹤區塊

> 完整技術債務處理流程：`.claude/pm-rules/tech-debt.md`

## 前置條件

| 條件               | 說明                     | 驗證方式                      |
| ------------------ | ------------------------ | ----------------------------- |
| **Phase 4 已完成** | 重構評估必須完成         | 工作日誌有 Phase 4 章節       |
| **技術債務已記錄** | 工作日誌中有標準格式表格 | 表格包含 ID、描述、風險、時機 |
| **表格格式正確**   | 遵循標準格式             | 可被腳本自動解析              |

### 工作日誌技術債務記錄格式

```markdown
## 技術債務評估

| ID     | 描述                                              | 風險等級 | 建議處理時機 | 影響範圍     |
| ------ | ------------------------------------------------- | -------- | ------------ | ------------ |
| TD-001 | book_tags 表缺少 book_id 索引，大量資料查詢效能低 | 低       | 下一版本     | database     |
| TD-002 | BookRepository 和 TagRepository 錯誤處理邏輯重複  | 低       | 可選         | repositories |
```

### 什麼應該被記錄為技術債務

| 應記錄                   | 不應記錄               |
| ------------------------ | ---------------------- |
| 架構違反（層級依賴錯誤） | 當前版本範圍內的 Bug   |
| 重複程式碼               | 已在當前版本修復的問題 |
| 效能最佳化機會           | 功能需求變更           |
| 測試覆蓋缺口             | 使用者回報的功能問題   |
| 文件缺失                 | 新功能需求             |

## 風險等級與版本對應

**風險等級分類**:

| 風險等級 | 說明 |
| -------- | ---- |
| **高** | 可能影響使用者體驗或效能的重大問題 |
| **中** | 影響維護成本但不嚴重的問題 |
| **低** | 程式碼品質或架構改進 |
| **極低** | 非功能性風格問題 |

### 版本推進規則 (UC-Oriented)

| 風險等級 | 版本規則                     | 範例                                        |
| -------- | ---------------------------- | ------------------------------------------- |
| **高**   | 當前 UC 完成後的版本         | UC-08 v0.19.8 的高風險 TD -> v0.20.0 (UC-09) |
| **中**   | 當前 UC 完成後的版本         | UC-08 v0.19.8 的中風險 TD -> v0.20.0 (UC-09) |
| **低**   | 當前 UC 版本系列的後續小版本 | UC-08 的低風險 TD -> v0.20.x 或更後          |
| **極低** | 可選改進，不強制排期         | TD-003 可選清理                             |

**決策邏輯**:

```
1. 判斷技術債務來自哪個 UC 版本系列（Example: v0.19.8 = UC-08）
2. 根據風險等級選擇目標版本
   ├─ 高/中 -> 下一個 UC (v0.20.x)
   └─ 低/極低 -> 當前 UC 版本系列或後續版本
3. 如果未指定 --target-version，自動推導
```

## Ticket 建立規則

技術債務 Ticket 使用特殊格式，包含 `ticket_type: "tech-debt"` 和來源版本資訊。

> 完整 Ticket frontmatter 範本：`references/ticket-template.md`
> 若專案已採用 `ticket` skill：通用 Ticket 格式規範以該 skill 的建立指令說明為準，本 skill 的範本只補充技術債務特有欄位，詳見 ticket skill（若已安裝）。若未採用，`references/ticket-template.md` 已含完整可用的 frontmatter 範本，失去的是與通用格式的一致性保證——欄位若日後與專案其他 ticket 分歧，無共同權威可對照

### Ticket ID 格式

```
{TargetVersion}-TD-{Seq:03d}
```

**範例**: `0.20.0-TD-001`, `0.20.0-TD-004`

### 儲存位置

```
docs/work-logs/v{TargetVersion}/tickets/
```

## TodoList 更新規則

在 `docs/todolist.yaml` 末尾新增或更新技術債務追蹤區塊：

```markdown
## 技術債務追蹤

| Ticket ID     | 描述                        | 來源版本 | 目標版本 | 風險 | 狀態    |
| ------------- | --------------------------- | -------- | -------- | ---- | ------- |
| 0.20.0-TD-001 | 新增 book_tags.book_id 索引 | v0.19.8  | v0.20.0  | 低   | pending |
```

## 使用方式

### 互動模式（推薦）

```bash
/tech-debt-capture
```

引導式交互：選擇工作日誌 -> 確認 TD 清單 -> 確認版本對應 -> 建立 Ticket 並更新 todolist

### 批量模式

```bash
uv run .claude/skills/tech-debt-capture/scripts/tech_debt_capturer.py capture \
    docs/work-logs/v0.19.8-phase4-final-evaluation.md
```

> 更多 CLI 範例（預覽模式、初始化、列出）：`references/cli-examples.md`

## 功能特性

1. **表格解析**: 自動解析 Phase 4 工作日誌中的技術債務 Markdown 表格
2. **版本決策引擎**: UC-Oriented 版本推導，支援 `--target-version` 手動覆蓋
3. **Atomic Ticket 產生**: 單一職責設計，自動填充 5W1H 和 frontmatter
4. **文件更新**: 自動更新 todolist.yaml 和建立版本目錄

## 前置條件

- `python3.10+`
- `pyyaml` 套件（UV 自動安裝）
- 完成 Phase 4 重構評估報告

## 相關資源

- `/ticket create` - 手動建立 Atomic Ticket
- `/ticket track` - 追蹤和更新 Ticket 狀態
- `.claude/pm-rules/tech-debt.md` - 技術債務處理流程
- `.claude/methodologies/atomic-ticket-methodology.md` - 單一職責原則

---

版本紀錄在同目錄的 `CHANGELOG.md`。
