---
name: bringhurst-typography
description: Apply Bringhurst-style typography principles from The Elements of Typographic Style to editorial pages, web UI, product surfaces, reports, slides, and books. Use when Codex must design, review, or improve hierarchy, measure, leading, spacing, punctuation, typeface selection/pairing, page geometry, and print-or-screen production quality.
---

# Bringhurst Typography

## Purpose

Use this skill to make typographic decisions that are structurally sound, readable, and consistent from macro layout down to punctuation and spacing details.

Prefer this skill whenever a task includes typography design, typography QA, or "why does this page feel off?" debugging.

## Core Workflow

1. Classify the task and medium.
- Identify whether the task is long-form reading, reference layout, UI copy, mixed-script composition, or production troubleshooting.
- Identify target medium: print, PDF, responsive web, or app UI.

2. Load the minimum needed references.
- Always read `references/book-map.md`.
- Read `references/rules-index.md` for precise rule numbers and chapter coverage.
- Read `references/workflows.md` for task-specific implementation flows.
- Read `references/checklists.md` before final recommendations or sign-off.

3. Diagnose before changing.
- Audit hierarchy, rhythm, line length, vertical spacing cadence, punctuation quality, and typeface coherence.
- Find structural failures before cosmetic changes.

4. Propose changes in ordered passes.
- Pass 1: page or viewport geometry and text block shape.
- Pass 2: typeface system and hierarchy.
- Pass 3: spacing and rhythm (measure, leading, paragraph logic, list/table logic).
- Pass 4: punctuation, symbols, and language-specific details.
- Pass 5: production checks for print or screen.

5. Explain tradeoffs.
- Keep recommendations tied to content purpose, reading mode, and output medium.
- State what improved and what was intentionally left unchanged.

## Output Format

When asked for a review or redesign plan, return:

1. Situation summary (content type, audience, medium).
2. Findings ordered by severity.
3. Recommended changes in execution order.
4. Rationale using rule numbers where useful (for example, `2.1.2` for measure).
5. Validation checklist for print or screen.

## Decision Rules

- Prefer readability and structural integrity over stylistic novelty.
- Treat punctuation and symbols as part of typography, not copyediting residue.
- Adjust one major parameter at a time when diagnosing quality regressions.
- Keep type choices minimal; add faces only with a clear role.
- Respect language and script conventions when composing multilingual text.

## Limits

- Do not imitate historical forms blindly; adapt principles to current constraints.
- Do not force print-era defaults onto small responsive screens without testing.
- Do not rely on OCR-noisy rule text when exact wording is unclear; use the canonical intent from the chapter context.

## Reference Files

- `references/book-map.md`: chapter and appendix map with topical scope.
- `references/rules-index.md`: consolidated rule index based on the book's recapitulation structure.
- `references/workflows.md`: practical workflows for UI, editorial, and production tasks.
- `references/checklists.md`: preflight and sign-off checklists.

## Invocation Examples

- "Audit this landing page typography and give fix order by impact."
- "Refactor our report template using Bringhurst-style spacing and hierarchy."
- "Choose and pair typefaces for a multilingual editorial PDF."
- "Check punctuation, dashes, quotes, and figure styles in this manuscript."
