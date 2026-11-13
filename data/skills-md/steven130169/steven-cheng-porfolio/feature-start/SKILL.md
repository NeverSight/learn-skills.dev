---
name: feature-start
description: "引導新功能開發啟動：需求確認、技術設計、分支建立、Gherkin 模板產生。觸發：「開始新功能」、「啟動功能開發」、「feature start」。輸出：feature branch、gherkin 模板、TODO 清單。(project)"
allowed-tools: Read, Grep, Glob, Write, Bash(git:*), AskUserQuestion, TodoWrite
---

# Feature Start - 功能開發啟動流程

## 目的
確保每個新功能開發都經過完整的需求分析、技術設計，並遵循專案的開發規範與安全原則。

---

## 前置條件

1. ✅ 已確認需求來源（使用者故事、Issue、產品需求文件）
2. ✅ 已確認當前在 `main` 分支且代碼是最新的
3. ✅ 本地環境沒有未提交的變更

---

## 執行步驟

### Step 1: 需求確認與分析

**執行動作：**
1. 與使用者確認功能需求的核心目標
2. 識別功能的使用者故事（User Story）
3. 確認驗收標準（Acceptance Criteria）
4. 識別潛在的技術風險與依賴項

**輸出：**
- 清楚的功能描述（1-2 句話）
- 驗收標準清單（至少 3 條）

**檢查清單：**
- [ ] 功能需求已明確定義
- [ ] 驗收標準可測試且可量化
- [ ] 已識別相關的現有模組或檔案

---

### Step 2: 技術設計評估

**執行動作：**
1. 評估功能是否需要：
   - 新的 API endpoint
   - 資料庫 schema 變更
   - 新的 React 元件
   - 第三方套件整合
2. 評估是否需要撰寫 ADR（Architecture Decision Record）
3. 識別需要修改的檔案清單

**決策點：**
- **簡單功能**（<3 個檔案變更）→ 直接進入 Step 3
- **複雜功能**（≥3 個檔案或涉及架構變更）→ 建議先撰寫 ADR

**檢查清單：**
- [ ] 已評估技術可行性
- [ ] 已識別需要變更的檔案
- [ ] 已確認是否需要 ADR

---

### Step 3: 建立功能分支

**執行動作：**
```bash
# 1. 確保在 main 分支
git checkout main

# 2. 拉取最新代碼
git pull origin main

# 3. 建立功能分支（命名規範：feature/功能簡述）
git checkout -b feature/<feature-name>
```

**分支命名規範：**
- `feature/blog-post-editor` - 新功能
- `fix/login-redirect-bug` - bug 修復
- `refactor/user-service` - 重構
- `test/event-ticketing-e2e` - 測試補充

**檢查清單：**
- [ ] 分支名稱符合命名規範
- [ ] 已成功切換到新分支
- [ ] 分支是從最新的 main 建立

---

### Step 4: 產生 Gherkin 模板

**執行動作：**
建立 Gherkin feature 檔案，儲存路徑：`e2e/specs/<feature-name>.feature`

```bash
# 確保 e2e/specs 資料夾存在
mkdir -p e2e/specs

# 建立 feature 檔案
touch e2e/specs/<feature-name>.feature
```

**Gherkin 模板內容：**
```gherkin
Feature: <功能名稱>
  作為 <角色>
  我想要 <功能>
  以便 <價值>

  Scenario: <第一個場景>
    Given <前置條件>
    When <執行動作>
    Then <預期結果>

  # TODO: 補充更多 scenarios
```

**範例：**
```gherkin
# e2e/specs/blog-post-editor.feature
Feature: 部落格文章編輯器
  作為 部落格作者
  我想要 編輯和發布文章
  以便 分享技術知識給讀者

  Scenario: 成功建立新文章
    Given 我已登入管理後台
    When 我建立一篇新文章，標題為 "TypeScript 最佳實踐"
    And 我輸入文章內容並點擊發布
    Then 文章應該出現在文章列表中
    And 文章狀態應該為 "已發布"

  # TODO: 補充編輯、刪除、草稿儲存等 scenarios
```

**檢查清單：**
- [ ] `e2e/specs/` 資料夾已建立
- [ ] Gherkin feature 檔案已建立（檔名對應分支名稱）
- [ ] Feature 描述已填寫（作為...我想要...以便...）
- [ ] 至少包含 1 個 Scenario
- [ ] Scenario 使用 Given-When-Then 格式

---

### Step 5: 建立開發計畫

**執行動作：**
建立 TODO 清單文件，儲存路徑：`docs/todos/<feature-name>.md`

```bash
# 建立 todos 資料夾（如不存在）
mkdir -p docs/todos

# 建立功能專屬的 TODO 檔案
touch docs/todos/<feature-name>.md
```

**TODO 檔案內容範本：**
```markdown
# Feature: <功能名稱>

## 功能描述
<1-2 句話描述功能>

## 驗收標準
- [ ] 標準 1
- [ ] 標準 2
- [ ] 標準 3

---

## 開發任務（TDD 順序）

### 1. BDD & E2E 測試準備
- [ ] 建立 Gherkin feature 檔案（`e2e/specs/<feature-name>.feature`）
- [ ] 將 feature 檔案綁定 E2E 測試案例（`e2e/tests/<feature-name>.spec.ts` - Cucumber step definitions）

### 2. 測試撰寫
- [ ] 撰寫單元測試案例
- [ ] 撰寫整合測試案例
- [ ] 實作 E2E 測試的 step definitions（如適用）

### 3. 功能實作
- [ ] 實作核心邏輯
- [ ] 實作 API endpoints（如適用）
- [ ] 實作 UI 元件（如適用）

### 4. 測試驗證
- [ ] 所有單元測試通過
- [ ] 所有整合測試通過
- [ ] 所有 E2E 測試通過

---

## 文件任務
- [ ] 更新相關文件（如適用）
- [ ] 撰寫 ADR（如需要）

```

**檔案命名規範：**
- `docs/todos/blog-post-editor.md` - 對應 `feature/blog-post-editor` 分支
- `docs/todos/login-redirect-bug.md` - 對應 `fix/login-redirect-bug` 分支

**檢查清單：**
- [ ] `docs/todos/` 資料夾已建立
- [ ] TODO 檔案已建立（檔名對應分支名稱）
- [ ] TODO 內容已填寫完整
- [ ] 任務優先順序已排序
- [ ] 已評估完成時間

---

### Step 6: 安全與規範檢查

**執行動作：**
在開始開發前，確認以遵循 `core.md` 的規範：

**開發規範：**
- [ ] 不使用 `any` 類型
- [ ] 不使用 `as` 進行不安全的型別轉換
- [ ] 不使用非空斷言 `!`（除非邏輯上絕對存在）
- [ ] 所有異步操作必須 `await` 或 `.catch()`

**安全規範：**
- [ ] 不在代碼中硬編碼 API 金鑰或敏感資訊
- [ ] 不在 Log 中輸出 PII（個人識別資訊）
- [ ] 防止 SQL/Shell Injection（不串接字串組合指令）

**測試規範：**
- [ ] 單元測試不發起真實網絡請求
- [ ] E2E 測試不使用生產環境數據

---

## 完成條件

- ✅ 功能需求已明確定義
- ✅ 技術設計已評估
- ✅ 功能分支已建立
- ✅ Gherkin 模板已產生（`e2e/specs/<feature-name>.feature`）
- ✅ 開發計畫（TODO）已建立
- ✅ 已確認遵循 `core.md` 的安全規範

---

## 下一步

完成 Feature Start 後，執行 `/develop` skill 開始 TDD 開發流程：
- 讀取 Gherkin 案例並進入 Plan Mode 規劃單元測試
- 啟動 Wallaby 即時測試監控
- 遵循 Red-Green-Refactor TDD 流程
- 撰寫測試先行，實作功能邏輯
- 反覆執行重構迴圈確保程式碼品質
- Commit 並 Push 符合 commitlint 規範

---

## 參考資料

- 專案最高指導原則：`.aiassistant/rules/core.md`
- 分支策略：參考 `.github/workflows/` 中的 CI/CD 設定
- 測試標準：參考專案的測試配置檔案
