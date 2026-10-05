---
name: pre-fix-eval
description: "修復前強制評估系統. Use for: (1) 測試失敗自動評估, (2) 編譯錯誤分類處理, (3) 強制 Ticket 開設流程"
metadata:
  version: 1.0.0
---

# 修復前強制評估 (Pre-Fix Evaluation)

錯誤發生時的強制閘門。確保在修復任何非語法問題前，都完成分析、開設 Ticket、正確分派代理人。

---

## 自動錯誤分類

PostToolUse Hook 自動識別四種錯誤類型：

| 錯誤類型 | 識別模式 | 開 Ticket | 流程 |
|---------|---------|----------|------|
| **SYNTAX_ERROR** | 括號、分號、拼字 | 不需 | 簡化流程，直接分派 mint-format-specialist |
| **COMPILATION_ERROR** | 類型、引用、導入 | 必須 | 完整六階段評估 |
| **TEST_FAILURE** | 斷言失敗、失敗計數 | 必須 | 完整六階段評估 |
| **ANALYZER_WARNING** | lint 警告、棄用 API | 必須 | 評估 + 延遲處理 |

分類優先級：`SYNTAX_ERROR > COMPILATION_ERROR > TEST_FAILURE > ANALYZER_WARNING`

正則表達式模式詳見：`references/error-patterns.md`

---

## 六階段強制評估流程

非語法錯誤必須完成全部六階段：

```
Stage 1: 錯誤分類 (Hook 自動完成)
    |
Stage 2: BDD 意圖分析 (Given-When-Then)
    |
Stage 3: 設計文件查詢 (需求/用例/工作日誌)
    |
Stage 4: 根因定位 (確定問題根本原因)
    |
Stage 5: 開 Ticket 記錄 (強制, /ticket create)
    |
Stage 6: 分派執行 (依 incident-response.md 派發對應表)
```

各階段詳細說明、輸出範例和 Ticket 模板：`references/six-stage-evaluation.md`

---

## Stage 6 分派規則

Stage 6 的代理人分派**依據 `.claude/pm-rules/incident-response.md` 的「派發對應表」**。

快速參考：

| 錯誤類型 | 預設代理人 |
|---------|----------|
| SYNTAX_ERROR | mint-format-specialist（無需 Ticket） |
| COMPILATION_ERROR | 依子分類，見 incident-response.md |
| TEST_FAILURE | 依子分類，見 incident-response.md |
| ANALYZER_WARNING | mint-format-specialist |

完整派發對應表（含子分類）：`.claude/pm-rules/incident-response.md`

---

## 修復決策矩陣

| 情況 | 測試狀態 | 程式狀態 | Ticket | 修復行動 |
|------|---------|---------|--------|---------|
| 語法錯誤 | - | 語法錯誤 | 不需 | 直接精確修復 |
| 程式實作不完整 | 失敗 | 缺少實作 | 必須 | 評估 -> 補完實作 |
| 程式邏輯錯誤 | 失敗 | 已實作 | 必須 | 評估 -> 修正邏輯 |
| 測試過時 | 失敗 | 正確 | 必須 | 評估 -> 驗證文件 -> 更新測試 |
| 設計變更 | 失敗 | 無實作 | 必須 | 評估 -> PM 審核 -> 實作 |
| 功能未實作 | 失敗 | 接口存在但未實作 | 必須 | 評估 -> 查文件 -> 開 TD Ticket 或刪除測試 |

各情況的詳細處理流程和範例：`references/common-scenarios.md`

---

## 禁止行為

1. **還沒做完六階段評估就分派修復** -- 任何非語法錯誤都必須完成 Stage 1-4
2. **非語法錯誤跳過 Ticket 開設** -- 所有編譯錯誤、測試失敗、Analyzer 警告都必須開 Ticket
3. **看到測試失敗就直接改測試** -- 必須先進行 BDD 分析和文件查詢，確認是程式問題還是測試過時
4. **進行大規模程式碼重寫** -- 修復應是最小化精確修改；需大幅重寫表示根因分析不足
5. **分派修復後不追蹤驗收結果** -- Ticket 開設後必須追蹤完成狀態

---

## 修復品質檢查清單

修復完成後驗證：

- [ ] 測試 100% 通過（沒有新增失敗）
- [ ] 修改範圍最小化（只改必要部分）
- [ ] 沒有引入新的問題
- [ ] 與設計文件一致
- [ ] Ticket 已更新為完成狀態
- [ ] 工作日誌已更新

---

## 自動化觸發

### Hook 觸發條件

| 命令 | 觸發 |
|------|------|
| `flutter test` 失敗 | 自動評估 |
| `dart analyze` 失敗 | 自動評估 |
| `dart run` 失敗 | 自動評估 |
| `mcp__dart__run_tests` 失敗 | 自動評估 |

### Hook 輸出行為

- **語法錯誤**：提示簡化流程，直接分派 mint-format-specialist，無需 Ticket
- **其他錯誤**：提示「必須開 Ticket」，引導執行 `/pre-fix-eval` 進入六階段評估

---

## 快速開始

1. 執行測試或編譯：`flutter test` 或 `dart analyze`
2. Hook 自動分類錯誤
3. 語法錯誤 -> 直接分派 mint-format-specialist
4. 其他錯誤 -> `/pre-fix-eval` -> 六階段評估 -> `/ticket create` -> 分派代理人

---

## 相關文件

- `references/six-stage-evaluation.md` - 六階段詳細說明和 Ticket 模板
- `references/common-scenarios.md` - 6 種常見情況處理指南
- `references/error-patterns.md` - 錯誤模式正則表達式
- `references/decision-matrix.md` - 修復決策矩陣詳細說明
- `.claude/pm-rules/incident-response.md` - 代理人派發對應表（Stage 6 的 Source of Truth）

---

版本紀錄在同目錄的 `CHANGELOG.md`。
