---
name: skill-creator
description: Create a Task Skill for a daily document task. Use when user wants to automate a repetitive task, says create skill, daily task, Task Skill, or needs to turn a dossier/folder workflow into a reusable skill.
---

# Skill Creator — grill → write

Turn one daily task into one Task Skill. Two phases, same session. No scaffolding for later.

## Phase 1 — grill

Run the `grilling` tree on the daily task. Frontier is every decision with prerequisites settled; ask the whole frontier in one round, with recommended answer, then wait.

Cover in order (keep general, no STT/dossier-specific jargon):
1. YAGNI — does this need a skill or does `officecli` + copy/manual cover it?
2. I/O — one concrete input (folder/file, e.g. `11. MS BỘ.../1. Hồ sơ thầu:1` as example) and one concrete output (`.docx/.xlsx/.pptx/.pdf` + path) — use real paths the user can `ls`.
3. Branches — distinct cases the skill handles (missing file, empty table row, different supplier/template). One trigger phrase per branch.
4. Leading word — shared word in prompts + code + docs that fires the skill.
5. Reference/Template — if L3 Fidelity is required, which real file is the Reference (full Format to clone) and which fields become `{{placeholder}}` in the Template. Read the Reference via `officecli read` + unzip check, list candidate placeholders (`w:t`/`a:t`/`v` values) for user to confirm. If no Reference exists, decide whether to create a Template from scratch (markdown → docx then inject placeholders) or to treat the task as L1 (markdown-only).

Completion: every branch has a named trigger phrase and I/O is concrete (real input listed, real output `officecli clone → substitute → accept` path for L3, or `officecli create` for L1). For L3 tasks a Reference path and placeholder map exist. No dossier/STT wording here — task-agnostic.

## Phase 2 — write

Write per `writing-for-agents` ladder (`SKILL-MECHANICS.md:10` for frontmatter):

1. `skills/<kebab-name>/SKILL.md` — frontmatter `name` + `description` (pointer: front-loaded leading word, one trigger per branch, no synonyms). Body: steps in order, each ends on a checkable completion criterion. Demand is exhaustive. For L3 tasks, steps are `clone Reference → substitute {{placeholders}} → accept`, not `create from markdown`.
2. Disclose reference behind a pointer when only some branches need it: `references/template.md`, `references/mapping.md`, or `references/grill-questions.md`. Inline what every branch needs; disclose what only some need. Put task-specific tables (e.g. dossier `STT→file` mapping) in references, not in this file. For L3, include `references/template.docx` (or `.xlsx/.pptx`) as the real Template ZIP with `{{placeholder}}` inside `w:t`/`a:t`/`v`, plus `references/placeholder-map.md` listing `placeholder → source field`.
3. Keep single source of truth; do not restate `package.json` scripts or `officecli` help.

Scaffold is 2-4 files (`SKILL.md` + `references/*.md` + optional `scripts/validate.mjs`). No `scripts/` until a branch needs code or validate needs deep check.

## Validate — 4 gates (run in Isolated Runtime, generic)

1. **Name & frontmatter** — `name` kebab-case matches folder, `description` front-loads leading word + one trigger per branch, no synonyms per `writing-for-agents:12`. Completion: `head -n 5 skills/<name>/SKILL.md` passes.
2. **Checklist coverage** — every branch/item the task requires has an entry in `references/*.md` (e.g. 22 STT for dossier per `Procurement Dossier:1` would be `grep "| STT"` 22 there, but for non-dossier tasks count the task's own rows). Completion: `grep "|"` counts match spec, no orphan.
3. **Office hygiene** — `officecli read` on each template returns markdown without `PK` spill. L1: `officecli create → accept`; L3: `officecli clone → substitute → accept` then `unzip -p word/document.xml | grep -c "<w:tr"` ≥ body rows, `officecli verify-l3` PASS, `file` type matches original (`.doc` stays `Composite` via `cp`, `.docx` stays `Word 2007+`). Completion: `bun tests/isolated-workspace/scripts/test-*.mjs:1` style PASS.
4. **Tracer Bullet** — `bun tests/isolated-workspace/scripts/tracer.mjs:1` for `docx|xlsx|pptx|pdf` PASS, `report.md:1` shows 4 PASS. No global install.

Skipped: deep XML font/header check — add `soffice --headless --convert-to pdf` visual diff when `w:tr` counts diverge >20%.

See `references/checklist.md` (grill) and `references/skill-template.md` (SKILL shell).
