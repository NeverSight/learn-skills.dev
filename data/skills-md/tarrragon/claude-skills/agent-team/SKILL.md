---
name: agent-team
description: "Agent Teams 協作派發指南。Use when: (1) Agent A 的發現會改變 Agent B 正在進行的工作, (2) 用戶要求使用 team/swarm, (3) 多代理人需即時協商共用介面或 API 契約。涵蓋 team 建立、Ticket-Task 橋接、teammate 入職、生命週期管理。"
metadata:
  version: 1.2.0
---

# Agent Teams 協作派發指南

Agent Teams 是 Claude Code 的實驗性功能，允許多個 Claude 實例組成團隊、共享任務清單、即時通訊。本 Skill 指導 PM 在使用 Agent Teams 時如何讓 teammates 遵循 Ticket 規範。

> **定位**：Agent Teams 是混合模式中的一個選項，不取代現有 Task subagent。

---

## 快速決策表

**核心判斷**：「Agent A 的發現會改變 Agent B 正在進行的工作嗎？」

- **否** → Task subagent
- **是** → 3-4x 成本合理嗎？合理 → Agent Teams；不合理 → Task subagent + PM 中轉

### Task Subagent 場景（各 Agent 獨立完成）

| 具體情境 | 判斷理由 |
|---------|---------|
| 獨立模組各自實作（Widget/Repository/Controller） | 各自獨立，無交互需求 |
| 批量重命名/導入路徑修正/格式化 | 純機械操作 |
| 多視角分析（各視角獨立產出報告） | 各報告不互相依賴，PM 事後彙整 |
| 多來源外部研究（各來源獨立） | 各自查詢不同網站，結論不互相依賴 |
| 測試失敗分析（單一明確原因） | incident-responder 單一代理人足夠 |
| 標準 TDD Phase 開發 | Phase 順序天然序列 |

### Agent Teams 場景（Agent A 的發現會改變 Agent B 的工作）

| 具體情境 | 判斷理由 |
|---------|---------|
| 跨模組測試失敗（大量失敗、原因不明） | 一個代理人的發現會改變另一個的調查方向 |
| 前後端同時開發共用 API | API 契約需雙方即時協商 |
| 元件 + ViewModel 共同設計介面邊界 | 介面契約在工作中定義，非預先確定 |
| 架構審查 + 安全審查（涉及認證/授權） | SA 架構發現可能改變安全評估範圍 |
| 多來源研究（結論相互依賴） | 一個來源的發現影響另一個的查詢策略 |
| 除錯：多假設平行測試（原因不明） | 一個假設被否定後要即時通知其他代理人調整方向 |
| QA 批量測試（多 URL/多頁面/多端點驗證） | 純平行加速，社群驗證有效 |
| 大型重構：多模組同時修改共用介面 | 共用介面變更需即時同步，避免衝突 |

### 「多視角分析」特別說明

| 狀況 | 推薦方式 | 理由 |
|------|---------|------|
| 各視角獨立產出，PM 事後彙整 | Task subagent | 現有方法論標準流程 |
| 一個視角的發現會改變另一視角方向 | Agent Teams | 需即時調整分析範圍 |

**成本提醒**：Agent Teams 約 3-4 倍 Token 成本。僅在「Agent A 的發現會改變 Agent B 正在進行的工作」時使用。

---

## Team 生命週期

5 個階段：

| 階段 | 名稱 | 執行者 | 核心動作 |
|------|------|--------|---------|
| 1 | Plan | PM | 確認 Ticket、設計任務分解、並行安全檢查 |
| 2 | Create | PM | TeamCreate → TaskCreate → spawn teammates |
| 3 | Coordinate | Team | Teammates 認領 Task + claim Ticket、PM 監控 |
| 4 | Converge | PM | 收集結果、驗證驗收條件、派發 auditor |
| 5 | Shutdown | PM | SendMessage shutdown → TeamDelete → ticket complete |

> 詳細操作指引：references/team-lifecycle.md

---

## Ticket-Task 橋接

**核心原則**：Ticket 是 Source of Truth，Task 是 ephemeral 協調層。

| 原則 | 說明 |
|------|------|
| Ticket 持久化 | Ticket .md 檔案跨 session 存在 |
| Task 臨時性 | Agent Teams Task List 隨 session 消失 |
| 映射關係 | 每個 Task 必須關聯一個 Ticket |
| 更新責任 | Teammate 負責更新 Ticket 進度日誌 |
| Complete 權限 | 只有 PM 可以 `ticket track complete` |

> 詳細規則：references/ticket-task-bridge.md

---

## Teammate 入職

PM 在 spawn teammate 時，必須提供入職指令，包含：

| 項目 | 說明 |
|------|------|
| 身份識別 | team name、role、assigned ticket |
| Ticket 操作 | claim、append-log、禁止 complete |
| 通訊協定 | SendMessage 目標、阻塞升級 |
| 品質標準 | implementation-quality.md、FLUTTER.md |

> 完整模板：references/teammate-onboarding-protocol.md

---

## 回退策略

若 team 協作失敗：

1. Shutdown teammates（SendMessage + TeamDelete）
2. 改用 Task subagent 繼續
3. Ticket 狀態不受影響（Ticket 是持久的）

**停用方式**：刪除 `.claude/skills/agent-team/` 即完全停用。

---

## 使用範例

### 範例 1：跨模組測試失敗（適合 Agent Teams）

用戶說：「30 個測試同時失敗，原因不明，涉及 3 個模組」

判斷：一個代理人的發現（如「根因在共用的 EventBus」）會改變其他代理人的調查方向 → Agent Teams

動作：
1. Plan 任務分解（每個模組一個 teammate）
2. TeamCreate + TaskCreate
3. Teammates 各自調查，透過 SendMessage 共享發現
4. Converge 彙整根因報告

### 範例 2：多視角分析（適合 Task subagent）

用戶說：「分析這個 PR 的架構影響和安全風險」

判斷：架構分析和安全分析各自獨立產出報告，PM 事後彙整 → Task subagent

動作：
1. 並行派發 saffron（架構）+ clove（安全）
2. 各自獨立完成分析報告
3. PM 彙整兩份報告做決策

---

## 社群驗證的最佳實踐

以下經驗來自社群實際使用回饋（Anthropic Engineering Blog, Addy Osmani, claudefa.st）：

| 實踐 | 說明 |
|------|------|
| **Plan First, Then Swarm** | 先用 Plan Mode 定義任務分解，再啟動 Team。避免 team 在模糊目標下浪費 token |
| **明確檔案所有權** | spawn 時指定每個 teammate 負責的檔案/目錄，避免衝突 |
| **CLAUDE.md 作為共享契約** | 每個 teammate 都會載入 CLAUDE.md，利用此機制傳遞共享規範 |
| **Delegate Mode** | team-lead 用 Shift+Tab 進入委派模式（僅協調，不實作），降低 token 消耗 |

---

## 相關文件

- .claude/pm-rules/decision-tree.md - 決策樹路由索引
- .claude/pm-rules/dispatch-gate.md - 派發閘門（第負一層並行化評估）
- .claude/pm-rules/parallel-dispatch.md - 並行派發指南
- .claude/pm-rules/ticket-lifecycle.md - Ticket 生命週期
- .claude/methodologies/parallel-evaluation-methodology.md - 並行評估 + 多視角分析（Task subagent 方式）

---

版本紀錄在同目錄的 `CHANGELOG.md`。
