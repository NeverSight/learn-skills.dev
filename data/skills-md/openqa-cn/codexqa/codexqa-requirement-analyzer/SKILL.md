---
name: codexqa-requirement-analyzer
description: >
  Full quality-and-risk analysis of requirement documents (single- or multi-source),
  producing one gap/conflict register with executable P0/P1 verification.
  Triggers: requirements analyzer, requirement quality, gap register, 需求分析,
  需求分析器, 需求评审, 需求缺口. Not for writing a case library (that is
  codexqa-testcase-generator), constructing test data (codexqa-testdata-generator), or reviewing
  code (codexqa-defect-analyzer / codexqa-code-reviewer).
  Former skill name: requirements-analyzer.
license: Apache-2.0
---

# Requirements Analyzer

Human-facing install and method docs: `README.md`, `HOW_IT_WORKS.md`, `KNOWN_LIMITATIONS.md` (and `.zh-CN.md`). Do not load those at runtime.

## When to Use

- Need a complete quality and risk analysis of requirement documents, not just a scope scan or a gap list.
- Materials may be a single PRD or a multi-source pack (stories, APIs, plans, role reports).
- Need one reviewable, assignable, verifiable gap register that can hand off to strategy or case writing.

## Workflow

1. Read and follow the main prompt listed under Progressive disclosure (coverage, structure, quality bar).
2. Run the fixed pipeline: intake → short-input gate → structure inventory → input audit → quality/smell/NFR → success metrics → behavior plus UX states → trace and goal-feature alignment → dependency grid → single register → risk algorithm → testability and oracles → blockers and next actions. Do not write risks or a “TOP 3” list first.
3. Direct requirement materials remain sufficient for standalone use. If the user supplies role reports with a declared `source_role`, treat them as optional composition inputs and never require installing a role Skill.
4. Add only project context that changes the result: scope, environment, constraints, risks, dependencies, expected deliverable.
5. If input is incomplete, return a usable first draft and explicitly mark assumptions and gaps.
6. Default to Markdown; switch formats only when the user asks.

## Core Constraints

- Produce exactly one gap and conflict register; do not also write “Gaps and Ambiguities”, “Cross-Source Conflicts”, or “Core Analysis Items”.
- Audit credibility and comparability first; never mark stale or incomparable sources as `aligned`.
- Prioritize by risk / business impact — do not treat everything equally.
- Separate confirmed facts, role-report content, working assumptions, and hypotheses to verify.
- Do not invent endpoints, fields, SLAs, environments, or root causes the user did not provide; unknowns become questions.
- Do not fill business decisions for stakeholders, and do not judge whether the ask is worth building; keep both views and a suggested decider on conflicts. If an omission looks intentional, ask first.
- When using a role report, preserve `source_role` item by item; never flatten into anonymous consensus or present a role view as a PRD fact.
- Every P0/P1 item needs executable verification: preconditions, stimulus, expected result, required evidence, `VerifyMethod`, and `RiskClass`. Every P0 needs `FailureMode`.
- Items with no observable failure condition are `untestable` and must not be executable P0. Do not emit a fake RPN, a 0–100 score, or a six-dimension traffic-light scorecard.

## Progressive Disclosure

- Before producing output, read and follow `prompts/codexqa-requirement-analyzer.md` (minimum coverage, output structure, quality bar).
- When Excel/CSV/JSON/Word is requested: read `output-formats.md` and honor the format.
- When a ready-made template fits: use matching files under `output-templates/`.
- When the user wants examples or alignment with existing assets: read relevant `examples/`.
- For register fields, troubleshooting, or FAQ: read `references/register-fields.md`, `references/troubleshooting.md`, or `references/FAQ.md`.
- For quality-characteristic judgments: read `references/quality-attributes.md`.
- For vague/optional/loophole wording: read `references/requirement-smells.md`.
- For NFR completeness: read `references/nfr-quality-grid.md`.
- For the structure inventory (present/thin/absent): read `references/structure-inventory.md`.
- For success metrics / KPI: read `references/success-metrics.md`.
- For upstream/downstream owner and ready dates: read `references/dependency-grid.md`.
- For missing states/decisions/time/failure paths/UX states: read `references/behavioral-completeness.md`.
- For P0–P3 ranking: read `references/risk-scoring.md`.
- Do not load the whole `references/` directory.
- For format conversion or helper pre-parse: prefer existing TypeScript scripts in `scripts/` (`npx --yes tsx scripts/run_analysis.ts --input <file>`); do not rewrite them in Python.
- For evaluating/regressing this skill: use `evals/` with skill-up.
- For the shortest path: read `quick-start.md`.

## Pre-delivery Checklist

- [ ] Followed the main prompt's 7-section output structure; section 6 was not omitted
- [ ] Produced one register only; questions were not restated in section 7
- [ ] Covered the minimum checklist, or explained omissions
- [ ] High-risk items have P0–P3 with impact / likelihood / detectability
- [ ] Section 2 includes quality-characteristic hits, smell hits, the eight-cell NFR grid, structure inventory, success-metrics grid, and dependency grid
- [ ] P0/P1 items include preconditions, stimulus, expected, evidence, VerifyMethod, and RiskClass; P0 includes FailureMode
- [ ] Items without an oracle were not written as executable P0
- [ ] Did not invent details the user did not provide
- [ ] Assumptions and gaps are marked
- [ ] Role-report findings retain source roles; no role Skill internal file was linked

## Common Pitfalls

- Concatenating three old analysis outlines and repeating gaps, risks, questions, and next steps.
- Marking `aligned` when sources are stale or not comparable.
- Pretending completeness when scope or context is missing.
- Treating every item as equally important, or using filler (“improve communication”) instead of closable questions.
- Listing checkpoints for P0 items without verification steps.
- Writing a weak AC with no oracle as an executable P0, or using a score or traffic-light scorecard for false precision.
- Labeling a missing KPI as NFR, or treating “out of this iteration” as `missing`.
