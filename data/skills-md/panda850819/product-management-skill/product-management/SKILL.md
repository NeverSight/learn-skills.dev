---
name: product-management
description: 協助撰寫 PRD、分析功能需求、規劃路線圖。Use when writing PRD, analyzing feature requests, planning roadmap, or need structured product thinking. Triggers on "PRD", "產品規格", "feature request", "roadmap", "功能分析".
allowed-tools: Read, Write, Edit, AskUserQuestion, TodoWrite
---

# Product Management

協助產品管理活動：PRD 撰寫、功能分析、路線圖規劃。

> **方法論來源**：
> - Marty Cagan (SVPG): Problem space vs solution space
> - Teresa Torres: Continuous Discovery, Opportunity Solution Trees
> - Clayton Christensen: Jobs to be Done
> - AI PRD Workflow: 定義邊界 + 審查邏輯 + 注入商業靈魂

**參考文件**：`references/ai-prd-workflow.md` - AI 協作流程、視角轉換、Prompt 庫

---

## When to Use

- 撰寫或更新 PRD
- 分析功能需求的影響、成本、優先級
- 綜合用戶研究發現
- 規劃產品路線圖
- 向團隊溝通產品決策

---

## Out of Scope

- 直接做最終產品決策（AI 提供資訊，人做決定）
- 技術實作細節（那是開發者的工作）
- 未經驗證的工作量估計

---

## AI 協作流程

> **核心轉變**：PM 從「寫文件」→「定義邊界 + 審查邏輯 + 注入商業靈魂」

```
1. PM 提供：策略/Context/邊界/必要條件
   ↓
2. AI 生成初稿
   ↓
3. PM 審查：場景、流程、邏輯、Edge Cases
   ↓
4. 重複 1-3 校正
   ↓
5. 視角轉換輸出（工程師版 / 老闆版）
```

### AI PRD 關鍵技巧

| 技巧 | 說明 |
|------|------|
| **Edge Cases 優先** | 要求 AI 列出邊緣案例，而非只寫 happy path |
| **代碼級規格** | 輸出 JSON Schema、Mermaid 時序圖、Swagger |
| **一致性檢查** | 術語、單位、角色命名全文一致 |
| **商業意圖** | 每個功能的「為什麼」與目標連結 |

### 視角轉換

| 受眾 | 關注點 | 輸出格式 |
|------|--------|----------|
| 工程師 | 精確規格、降低來回 | 時序圖、JSON Schema、sample code |
| CEO/Manager | 風險與機會、決策品質 | Risk Matrix、方案比較、商業影響 |

### 決策風險暴露

AI PRD 應主動回答這些問題：
- 成本會不會隨 usage 非線性成長？
- fallback 發生時影響體驗還是營收？
- agent 出錯時責任歸屬在哪？

> **詳細 Prompt 庫和範例**：見 `references/ai-prd-workflow.md`

---

## Integrations

```
upstream:
  - skill: spec-interviewer (深度需求探索)
  - skill: quant-analyst (數據分析支持決策)

downstream:
  - skill: frontend-design (UI 實作)
  - skill: pine-developer (交易相關功能)
  - skill: spec-sync (驗證實作符合規格)
```

---

## PRD Template

```markdown
# [Feature Name] PRD

## Overview
[一句話描述這個功能]

## Problem Statement (Problem-First)

> 💡 **Marty Cagan 原則**: 先充分理解問題，再討論解法。過早跳到解決方案是產品失敗的主因。

**用戶痛點**: [描述問題]
**影響範圍**: [受影響的用戶數/場景]
**當前狀態**: [現在怎麼解決]

### 5 Whys 根因分析
1. Why: [表面問題]
2. Why: [更深一層]
3. Why: [再深一層]
4. Why: [接近根因]
5. Why: [根本原因]

### Jobs to be Done
> 用戶雇用這個產品來完成什麼任務？

**When** [情境]
**I want to** [動機]
**So I can** [期望結果]

## Discovery Checklist

> 💡 **Teresa Torres 原則**: 在寫解決方案前，確保已充分探索問題空間。

- [ ] 已訪談 ≥3 位目標用戶
- [ ] 已記錄用戶的實際行為（非意見）
- [ ] 已繪製 Opportunity Solution Tree
- [ ] 已識別 ≥2 個可能的解決方向
- [ ] Problem space 已充分探索

## Goals
- [ ] 主要目標 1
- [ ] 主要目標 2

## Non-Goals
- 明確不做什麼
- 這個版本不包含什麼

## User Stories

### Primary User: [角色]
- As a [user], I want to [action] so that [benefit]

### Edge Cases
- As a [user], when [unusual situation], I expect [behavior]

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| [KPI 1] | X | Y | [how to measure] |

## Solution Design

### Option A: [Name]
- **Pros**: ...
- **Cons**: ...
- **Effort**: S/M/L

### Option B: [Name]
- **Pros**: ...
- **Cons**: ...
- **Effort**: S/M/L

### Recommended: Option [X]
**Rationale**: [why this option]

## Technical Considerations
- 依賴系統
- 效能影響
- 安全考量
- 資料需求

## Milestones

| Phase | Scope | Target |
|-------|-------|--------|
| MVP | [minimal feature set] | - |
| V1 | [full feature set] | - |
| V2 | [enhancements] | - |

## Open Questions
- [ ] 待確認事項 1
- [ ] 待確認事項 2

## Decision Log

| Decision | Rationale | Date | Owner |
|----------|-----------|------|-------|
| ... | ... | ... | ... |

## Appendix
- 相關文件連結
- 競品分析
- 用戶訪談摘要
```

---

## Quick PRD vs Full PRD

> 根據功能規模選擇適當的深度

| 情況 | 模板 | 內容 |
|------|------|------|
| **小功能優化** | Quick PRD | Problem + Solution + Metrics |
| **新功能開發** | Full PRD | 完整模板 |
| **策略性產品** | Full PRD + Discovery | 完整模板 + 用戶訪談 + 機會樹 |

### Quick PRD Template

```markdown
# [Feature] Quick PRD

## Problem
[一句話描述問題]

## Solution
[一句話描述解法]

## Success Metrics
| Metric | Target |
|--------|--------|
| ... | ... |

## Scope
- ✅ 做：...
- ❌ 不做：...
```

---

## Feature Analysis Framework

分析功能請求時使用這個框架：

### Impact vs Effort Matrix

```
         High Impact
              │
    Quick     │    Strategic
    Wins      │    Bets
              │
──────────────┼──────────────
              │
    Fill      │    Money
    Ins       │    Pit
              │
         Low Impact

    Low Effort ────────► High Effort
```

### RICE Scoring

```
RICE = (Reach × Impact × Confidence) / Effort

Reach: 影響多少用戶 (per quarter)
Impact: 影響程度 (0.25/0.5/1/2/3)
Confidence: 信心程度 (20%/50%/80%/100%)
Effort: 人月
```

### Analysis Checklist

- [ ] **用戶需求驗證**: 這真的是用戶要的嗎？
- [ ] **問題根因**: 我們在解決根本問題還是症狀？
- [ ] **替代方案**: 有更簡單的方法嗎？
- [ ] **技術可行性**: 工程團隊評估過了嗎？
- [ ] **商業影響**: 對收入/成本的影響？
- [ ] **風險評估**: 最壞情況是什麼？

---

## Roadmap Planning

### Quarterly Planning Template

```markdown
## Q[X] [Year] Roadmap

### Theme: [主題]

### Must Have (P0)
- [ ] Feature A - [owner]
- [ ] Feature B - [owner]

### Should Have (P1)
- [ ] Feature C - [owner]
- [ ] Feature D - [owner]

### Nice to Have (P2)
- [ ] Feature E
- [ ] Feature F

### Dependencies
- [dependency 1]
- [dependency 2]

### Risks
- [risk 1]: [mitigation]
```

---

## Communication Templates

### Stakeholder Update

```markdown
## [Feature] Status Update

**Status**: On Track / At Risk / Blocked
**Progress**: [X]% complete

### Completed This Week
- ...

### Next Week
- ...

### Blockers
- ...

### Decisions Needed
- ...
```

### Launch Announcement

```markdown
## [Feature] Launch

### What's New
[簡短描述]

### Who It's For
[目標用戶]

### How to Use
[快速指南]

### Known Limitations
[已知限制]

### Feedback
[回饋管道]
```

---

## Safety and Escalation

- **AI 提供分析，人做決定** - 不自動做產品決策
- **技術假設需驗證** - 工作量估計需與工程確認
- **數據驅動** - 重大決策需有數據支持
- **跨團隊影響** - 涉及其他團隊時先溝通

---

## Implementation Checklist

- [ ] 定義清楚問題
- [ ] 收集用戶反饋
- [ ] 分析競品
- [ ] 評估技術可行性
- [ ] 撰寫 PRD
- [ ] 團隊 Review
- [ ] 確定優先級
- [ ] 分解為可執行任務
