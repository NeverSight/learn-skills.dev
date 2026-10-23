---
name: onboard-codebase
description: Deep codebase analysis — populate wiki with architecture, concepts, entities
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
---

# Skill: onboard-codebase

## WHAT

### Purpose và context
- **Purpose:** Analyze unmapped codebase, extract technical/business context, populate Wiki per project standards.
- **Trigger (when to use):**
  - Installing agentic setup into legacy/existing project.
  - Wiki outdated or has context gap from recent code changes.
- **Non-goals:** không sửa code dự án, không ghi đè trang wiki viết tay khi chưa kiểm `## Origin`, không lấy README/comment làm sự thật thay cho code.

### Mental model
`codebase → infrastructure audit → domain logic + patterns → (frontend style nếu có) → business rules → entities → wiki (entities · concepts · fe-style · AGENT-business.md) → index + log → lint`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | codebase dự án | có | đọc implementation để kiểm chứng mọi claim |
| Out | `llmwiki/wiki/entities/project-structure.md` | có | cấu trúc thư mục, stack, entry point, build/deploy |
| Out | `llmwiki/wiki/concepts/*.md` | có | concept domain + pattern |
| Out | `llmwiki/wiki/concepts/fe-style.md` | khi có frontend | giá trị thật (hex, px/rem, class) |
| Out | `AGENT-business.md` | có | user stories + business rules suy ngược từ code |
| Out | `llmwiki/wiki/entities/*` + index + log | có | services, external API, bảng DB |
| Out | draft output report | có | mục Delivery |

### Rules và capabilities
- RULE-01 (MUST): ALWAYS read implementation to verify business claims.
- RULE-02 (MUST): Cross-reference `README.md`/comments but prioritize truth in code.
- RULE-03 (MUST): Focus on "Why" and "How" at code level, not just "What".
- RULE-04 (MUST): NEVER overwrite existing manual wiki entries without checking `## Origin` section.
- RULE-05 (MUST): **OKF v0.1 (R9):** mọi trang wiki bắt đầu bằng YAML frontmatter (`---`) có `type` không rỗng (`concept`/`entity`/`source`) — copy `_template.md` tương ứng. Giữ `## Origin` (R2).
- RULE-06 (MUST): For `fe-style.md`: record actual values (hex codes, px/rem sizes, class names), not descriptions — goal is reproducible visual style without guessing.
- Capabilities: đọc toàn bộ codebase; ghi `llmwiki/wiki/` + `AGENT-business.md`; chạy lint wiki.

### Failure boundaries
- Không có frontend → bỏ bước 3, không tạo `fe-style.md` (**succeeded** hẹp).
- Trang wiki viết tay đã có mà `## Origin` không cho phép ghi đè → **clarify** trước khi sửa.
- Claim nghiệp vụ không kiểm được trong code → không ghi như sự thật; ghi rõ chưa xác minh.
- `lint` báo mâu thuẫn → sửa trang rồi chạy lại trước khi coi là xong.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | codebase | Infrastructure Audit | `project-structure.md` | — |
| W02 | judgment | code domain | Deep Code Analysis (services, models, patterns) | concepts | — |
| W03 | judgment | frontend | Frontend & Style Audit | `fe-style.md` | không có frontend → skip (B01) |
| W04 | judgment | code | Business Logic Extraction | `AGENT-business.md` | claim không kiểm được → không ghi |
| W05 | judgment | code | Entity Cataloging | entities | — |
| W06 | effect | kết quả W01–W05 | Knowledge Injection + index + log | wiki cập nhật | trang tay → kiểm `## Origin` |
| W07 | deterministic | wiki | Final Verification: `lint` | không mâu thuẫn | mâu thuẫn → sửa, lặp W07 |

Chi tiết từng bước (nguồn chân lý cho W01–W07):

1. **Infrastructure Audit**:
   - Map directory structure.
   - Identify tech stack, entry points, build/deploy scripts.
   - Store in `llmwiki/wiki/entities/project-structure.md`.
2. **Deep Code Analysis**:
   - Scan for core domain logic (Services, Models, Controllers).
   - Identify patterns (Repository, Event-driven, etc.).
   - Extract Concepts for `llmwiki/wiki/concepts/`.
3. **Frontend & Style Audit** *(skip if no frontend)*:
   - Identify UI framework (Next.js, React, Vue, etc.) and CSS approach (Tailwind, CSS Modules, styled-components, SCSS).
   - Extract design tokens: color palette, typography scale, spacing, breakpoints — from `tailwind.config.*`, CSS variables, or theme files.
   - Identify component library (shadcn/ui, MUI, Ant Design, Radix, Headless UI, etc.) and local wrappers.
   - Trace global styles: `globals.css`, base layout files, font loading strategy.
   - Document component naming conventions (PascalCase, feature-folder, colocated stories, etc.).
   - Note UI state management (Zustand, Jotai, Context, Redux, etc.) and data-fetching pattern (React Query, SWR, server actions, etc.).
   - Capture routing conventions (file-based, nested layouts, auth guards).
   - Store in `llmwiki/wiki/concepts/fe-style.md`.
4. **Business Logic Extraction**:
   - Reverse-engineer user stories and business rules from code.
   - Generate/Update `AGENT-business.md`.
5. **Entity Cataloging**:
   - List internal services, external APIs, database tables.
   - Create entries in `llmwiki/wiki/entities/`.
6. **Knowledge Injection**:
   - Synthesize into Wiki structure.
   - Update `llmwiki/wiki/index.md` and `llmwiki/wiki/log.md`.
7. **Final Verification**:
   - Run `lint` on generated wiki — check for contradictions.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | dự án có frontend | chạy bước 3 Frontend & Style Audit | không có frontend → skip | W04 |
| B02 | conditional_required | trang wiki đích đã tồn tại, viết tay | đọc `## Origin` trước; chỉ cập nhật khi không đè nội dung thủ công | không chắc → hỏi user | W06 |

### Validation và stopping
Tất định: `lint` wiki không còn mâu thuẫn; mọi trang có frontmatter `type` + `## Origin` (R2/R9). Cần review: claim nghiệp vụ phải truy về code đã đọc. Dừng sau W07 xanh + output report.

### Examples
- **Positive:** onboard một repo Next.js + Go → `project-structure.md` (stack, entry, build), concepts domain, `fe-style.md` ghi `#0F172A`, `text-sm`/`14px`, shadcn/ui, `AGENT-business.md`, entities bảng DB → `lint` sạch → draft report.
- **Boundary/failure:** repo chỉ có backend Go → bỏ bước 3, không tạo `fe-style.md`; README nói "hỗ trợ refund" nhưng code không có handler refund → không ghi vào `AGENT-business.md` như sự thật.

### Delivery — Output Report

After all main skill tasks complete, write a propose draft to the wiki.

#### Steps

**1. Build the filename:**
- Format: `DDMMYY-<ten>.md`
- `DDMMYY` = today (e.g., `020626` for 2 June 2026)
- `<ten>` = 2–4 kebab-case words summarising what was done (e.g., `landing-page-coteccons`, `brand-kit-fintech`, `ingest-auth-spec`)

**2. Write** `llmwiki/wiki/sources/draft/DDMMYY-<ten>.md`:

```
---
type: draft
title: "DDMMYY-<ten>"
status: proposed
tags: [<skill-name>, output-report]
timestamp: YYYY-MM-DD
---

# DDMMYY-<ten>
**Type:** draft
**Status:** proposed
**Tags:** <skill-name>, output-report
**Proposed:** YYYY-MM-DD

## What
<One sentence — what this skill invocation produced or decided>

## Output
<Key artefacts, files created/modified, or decisions made>

## Files
| File | Action |
|------|--------|
| `path/to/file` | created / modified |

## Notes
- Invoked via: `/<skill-name>` skill

## Origin
- **Draft:** `wiki/sources/draft/DDMMYY-<ten>.md`
- **Commit:** _(filled by verify-before-commit)_
- **Date promoted:** _(filled by verify-before-commit)_
```

**3. Update wiki index & log:**
- `llmwiki/wiki/index.md` — append one row: `| [DDMMYY-<ten>](sources/draft/DDMMYY-<ten>.md) | draft | YYYY-MM-DD |`
- `llmwiki/wiki/log.md` — append: `## YYYY-MM-DD — <skill-name> — <ten>`

> Skip only when the skill produces zero artefacts and zero decisions (e.g., a pure display mode like `/caveman-stats`).
