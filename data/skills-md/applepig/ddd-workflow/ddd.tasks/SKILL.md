---
name: ddd.tasks
description: >
  任務拆解：將已確認 spec.md 的 Milestones 就地細化為 task 列表，
  或將過大的 scope 拆成 semver-like 子編號資料夾。
  spec 確認後、milestone 不夠清楚或要標平行工作線時使用；milestone 已夠清楚直接走 /ddd.work。
  Trigger: "細化 milestones", "拆分 sprint", "break down tasks",
  "create a task list", "split into sub-sprints", /ddd.tasks。
---

# ddd.tasks — 細化 Milestones ／ 拆分 Sprint

任務拆解階段。任務來源永遠是 `spec.md` Milestones；`/ddd.tasks` 做的是把特定 milestone 在 spec.md 內就地展開，或在 scope 過大時拆分 sprint。拆解建立在已對齊的規格上——spec.md 未經使用者確認前不拆任務（底線第 1 條的同一道理）。

> 歷史註記：舊版曾支援 optional `tasks.md` 作為獨立執行計畫，已淘汰；既有專案裡的 legacy tasks.md 僅供歷史參考，不作任務來源。

## Decision Gate

讀取 spec.md 後，判斷下一步：

- **不需要細化**：Milestone 已夠清楚、沒有平行工作線、沒有複雜匯合點、task 總數約 10 個以內 → 不改檔案，直接引導 `/ddd.work`。
- **細化 Milestones**：需要展開 task、補範圍／驗證、或標記平行工作線 → 在 spec.md 內就地更新。
- **拆分 Sprint**：預期超過 5 個 milestone、超過約 15 個 task，或涵蓋多個可獨立交付的子系統 → 拆成 semver-like 子編號資料夾。scope 過大時先拆，不用過大的 spec 硬撐。

## 細化 Milestones

將 spec.md 的 Milestone 就地展開為 task 列表。每個 task 遵循 Agentic TDD：測試與實作分離、原子性（一個 task 專注一個行為）。細化後的 spec.md 仍要容易閱讀——task 列表若把 spec 撐成執行手冊，代表該走拆分 Sprint。

### 細化後的 Milestone 格式範例

```markdown
### Milestone 2: API + 前端
> 範圍：`server/routes/auth/`、`components/auth/`
> 驗證：`vitest run server/routes/auth/ components/auth/`
> 預期結果：使用者可透過前端表單登入，取得有效 session token

#### 🔀 可平行工作線

**[A] Backend API** — `isolation: worktree`
> 範圍：`server/routes/auth/`、`server/services/auth/`
> 依賴：M1 完成的 User model + session store
> 介面契約：POST /auth/login → LoginResponse { token, user }
> 驗證：`vitest run server/routes/auth/` 全過
- [ ] 撰寫 POST /auth/login endpoint 測試 (Red)
- [ ] 實作 login endpoint (Green)

**[B] Frontend Form** — `isolation: worktree`
> 範圍：`components/auth/`、`composables/useAuth.ts`
> 依賴：LoginRequest/LoginResponse type 定義
> 介面契約：LoginForm emit `submit` 帶 LoginRequest payload
> 驗證：`vitest run components/auth/` 全過
- [ ] 撰寫登入表單元件測試 (Red)
- [ ] 實作登入表單元件 (Green)

#### 🔗 匯合點
> 驗證：`vitest run tests/integration/auth/` 全過
- [ ] 合併 [A]、[B] 分支，解決衝突
- [ ] 前後端整合測試 (Red → Green)
```

## 平行工作指引

若 task 總數不超過 4 個且只涉及 1–2 個檔案，直接序列執行，跳過平行分析。

- **切分標準**：兩條工作線互不修改同一檔案，且透過明確介面（API contract / shared types）銜接，即可平行；共用全域狀態、需要同時改同一檔案、或介面尚未確定時，先用序列 task 確立介面再分線。
- **介面先行**：銜接介面在分線前確定。
- **匯合點必測**：合併後以整合測試驗證銜接正確。
- 每條工作線標題下的 blockquote 是 worker 的上下文卡片；欄位定義與擷取方式見 `/ddd.work` 的「工作線上下文卡片（格式 SSOT）」。

## 拆分 Sprint

scope 過大時，拆成 semver-like 子編號資料夾：

```
docs/18-user-auth/          # 父 sprint：保留為索引或決策脈絡
docs/18.1-data-layer/
    └── spec.md
docs/18.2-auth-api/
    └── spec.md
docs/18.3-auth-ui/
    └── spec.md
```

拆分後，父 sprint 不再承載可執行任務；`/ddd.work`、`/ddd.xreview`、`ddd-developer`、`ddd-reviewer` 都以各子 sprint 的 `spec.md` 作為任務來源。

## Self-Review

以新鮮眼光對照 spec 自我檢查，發現問題直接修正：

1. **Spec 覆蓋度**：逐條掃描 spec 的目標、驗收條件、邊界案例，確認每項都反映在 Milestones 中。列出遺漏並修正。
2. **Task 完整性**：是否有模糊描述、測試與實作混在同一 task、缺少 Red/Green 標記、milestone 缺少預期結果或驗證方式。
3. **依賴一致性**：平行工作線的介面契約是否在分線前確立？Milestone 間的依賴方向是否合理？
4. **輕量維持**：細化只落在 Milestones，需求與驗收條件不動；若細化只是把 spec 機械轉成更長的 checklist，回退維持原本的輕量 Milestones。

## 產出

- 不需要細化：不新增檔案，直接引導 `/ddd.work`
- 細化：更新 `docs/<編號>-<名稱>/spec.md` 的 Milestones
- 拆分：建立 `docs/<編號>.<子編號>-<名稱>/spec.md`

## 結束條件

呈現更新後的任務來源（該輪最終訊息），等待使用者確認；確認後引導執行 `/ddd.work`。
