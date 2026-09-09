---
name: prd-writer-cn
description: Draft, clarify, rewrite, review, or complete Chinese PRDs in the user's team Markdown style from rich specs, sparse notes, chat logs, screenshots, or rough feature ideas. Use when Codex is asked to write a PRD, 产品需求文档, 需求说明, 需求要点确认, 埋点需求, 字符串表, 协作需求, lightweight requirement doc, or DingTalk-pasteable flow/prototype notes for mobile AI products, template workflows, ERP/backend tools, analytics, strings, and collaboration notes.
---

# PRD Writer CN

## Quick Start

Use this skill to produce team-style Chinese requirements, not generic product essays. Prioritize accurate `需求说明`: clear scope, before/after behavior, interaction flow, state rules, and implementation boundaries. The document may be lightweight; do not force every section to be long or fully populated.

Load these references only as needed:

- `references/prd-template.md` for the exact PRD skeleton.
- `references/style-guide.md` for tone, section rules, and common row patterns distilled from the user's PRDs.
- `references/drafting-modes.md` for sparse-input triage, confirmation-first drafting, and follow-up questions.
- `references/dingtalk-output.md` for one-click-paste flowcharts, prototype notes, and DingTalk-friendly formatting.
- `references/quality-checklist.md` before final delivery or when reviewing an existing PRD.
- `references/external-prd-principles.md` when a request asks for stronger generic PRD rigor beyond the local template.

## Workflow

1. Triage the input. Identify what is known, inferred, and missing. If the source is chat text or screenshots, extract the concrete pain point, affected page, trigger action, current behavior, desired behavior, and implementation owner.
2. Choose the output path:
   - If the user asks to `先确认`, information is sparse, or multiple interpretations are plausible: start with `需求要点确认` and 3-5 targeted questions.
   - If the user asks `直出`, `先给一版`, or the core behavior is clear: draft a PRD immediately and surface assumptions as `待确认`.
   - If the change is small: produce a lightweight PRD focused on `需求说明`; keep empty sections short or omit optional details when the user allows.
3. Ask questions only for blockers that change product behavior, implementation scope, or test expectations. Do not ask for polish-only details before giving useful output.
4. Draft the main specification in `需求说明`. Use the three-column table when it helps; for very small changes, a compact section with bullets is acceptable.
5. For each module, cover only relevant details: affected modules, entry points, page structure, states, user actions, system response, old/new logic, boundary rules, limits, storage, backend/ERP/STT/Firebase config, ad behavior, and dependencies.
6. Include DingTalk-friendly flow/prototype notes when the user asks for flowcharts, prototypes, or copy-paste output. Prefer plain-text flows and concise prototype annotations; add Mermaid only as an optional companion.
7. Preserve the local style: concise Chinese, bold key constraints, product terms in backticks or brackets, image/design links in the prototype column, and `:::` blocks for background/value or analytics owner notes.
8. Run the checklist before finalizing. Tighten vague statements, add state/edge cases, and isolate assumptions.

## Writing Rules

- Keep the document operational. Avoid motivational copy and broad strategy unless it directly explains the requirement.
- Prefer short, accurate, logically complete requirements over long, full-looking documents.
- Do not invent people, dates, data limits, event names, or translations. Use blanks or `待确认`.
- Keep existing behavior explicit: write `保留原有逻辑不变`, `不影响原有保存链路`, or `复用现有结果页逻辑` when compatibility matters.
- Separate `需求说明` from `交互逻辑` inside complex table cells.
- State rollout scope with phrases like `首期优先...`, `一期暂不...`, `后续可按配置复用...`.
- Treat analytics, strings, material preparation, AB experiments, commercial/ad requirements, and collaboration needs as first-class when relevant. If irrelevant, write `暂无` or omit in lightweight mode.

## Output Modes

- **Requirement Confirmation**: Summarize `我理解的需求要点`, `待确认问题`, and `默认假设`; use this before a full PRD when input is thin.
- **Lightweight PRD**: Produce a concise Markdown requirement doc focused on `需求说明`, suitable for small ERP/backend/UI copy changes.
- **Create**: Produce a complete Markdown PRD using `references/prd-template.md`.
- **Rewrite**: Keep the user's business meaning, then normalize structure, tone, and table formatting.
- **Review**: Lead with missing or ambiguous requirements, then provide targeted edits or a patched version.
- **Supplement**: Add specific sections such as 埋点需求, 字符串, 协作需求, or edge cases without rewriting unrelated content.
- **DingTalk Paste**: Produce plain Markdown headings, tables, text flowcharts, and prototype annotations that can be pasted into DingTalk online docs.
