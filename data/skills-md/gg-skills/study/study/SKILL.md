---
name: study
description: when configuring technical studies with evidence and decision rationale. Saves under .studies/. Handoff to planning, decisions, research skills. MCP-compatible. Not for completed studies.
---

# GG → Study → Mode

> **Snapshot age:** verified 2026-04-30.
> Verify release-sensitive answers with upstream documentation before responding with high confidence.

## Overview

Use this skill to produce structured, evidence-backed studies and persist them in a dedicated study workspace under the repository root `.studies/` directory.

This skill also serves as a deeper-analysis handoff when an agent-session inspection finds unresolved workflow, heuristic, or architecture questions that should not go straight into implementation planning.

For a direct command lookup, see [Quick Commands](#quick-commands) below.

## When to Use This Skill

**TRIGGER when:**
- The user asks to study, research, analyze, or evaluate a technical decision before implementation.
- A session inspection surfaced unresolved workflow, heuristic, or architecture questions.
- Evidence exists but the concrete change inventory, regression scope, or operator blast radius is still fuzzy.
- The user needs a structured comparison of options with tradeoffs and a recommendation.

**SKIP when:**
- The user is ready to implement and only needs a plan (use `plan/SKILL.md` directly).
- The task is a simple bug fix with a single obvious solution and no architectural uncertainty.
- The request is purely about creating or updating specs without prior analysis.

## Common Misconceptions

| # | Misconception | Correction | Key concept |
|---|---------------|------------|-------------|
| 1 | A study is just a long explanation. | A study is a decision artifact with options, tradeoffs, and a recommendation, not prose. | Decision artifact |
| 2 | Studies should be saved under `docs/`. | Studies go under `.studies/`; `docs/` is for human-facing documentation. | Workspace boundary |
| 3 | Open questions can be a shallow bullet list. | Each open question must be a decision-ready subsection with options and consequences. | Decision-ready format |
| 4 | Sub-agents are the default path. | Sub-agents are optional deepening helpers used only after explicit approval. | Optional deepening |
| 5 | A study can jump straight to implementation. | Planning via `plan/SKILL.md` is mandatory before implementation. | Planning gate |
| 6 | A study is complete when it has recommendations. | A complete study has evidence for every claim and paths to all referenced files. | Evidence anchoring |
| 7 | Any evidence is sufficient for a claim. | Evidence must be concrete: file paths, command outputs, test results—not assertions. | Evidence quality |
| 8 | Tradeoffs can be vague if the recommendation is clear. | Each tradeoff must quantify: complexity, risk, cost, or timeline impact. | Quantified tradeoffs |
| 9 | Open questions can wait until implementation. | Open questions block planning; document resolution paths or routing decisions. | Decision readiness |

## Quick Commands

```bash
# Initialize a new study workspace
# Runner alternatives: bunx tsx / pnpm dlx tsx / deno run -A npm:tsx / node --import tsx / yarn dlx tsx
npx tsx .agents/skills/study/scripts/init-study.ts \
  --slug "<slug>" --title "<title>"

# Commit and push a completed study
npx tsx .agents/skills/study/scripts/finalize-study.ts \
  --study-dir ".studies/<timestamp>-<slug>"

# Check study completeness (16-item checklist)
npx tsx .agents/skills/study/scripts/check-study-completeness.ts --latest
npx tsx .agents/skills/study/scripts/check-study-completeness.ts --study ".studies/<timestamp>-slug/"
npx tsx .agents/skills/study/scripts/check-study-completeness.ts --latest --json

# After any study markdown write: generate sibling HTML and print absolute paths
npx tsx .agents/skills/study/scripts/render-markdown-html.ts --input ".studies/<timestamp>-<slug>/study-<slug>.md"
npx tsx .agents/skills/study/scripts/render-markdown-html.ts --dir ".studies/<timestamp>-<slug>"
```

For the full script surface, see [Script Inventory](#script-inventory).

## Study Quality Checklist

Use this checklist before finalizing any study. Each item is a gate—the study is not complete until all required items are satisfied.

| # | Checklist Item | Why It Matters | Gate |
|---|---------------|---------------|------|
| 1 | **Objective clarity** — The study states a single clear decision or problem | Prevents unfocused analysis | Pre-draft |
| 2 | **Scope boundaries** — In-scope and out-of-scope items are explicitly listed | Prevents hidden assumptions | Pre-draft |
| 3 | **Current state documented** — Existing architecture/behavior with concrete file paths | Provides baseline for comparison | Draft |
| 4 | **Option set complete** — At least two viable options when feasible | Enables informed decision | Draft |
| 5 | **Tradeoffs quantified** — Each tradeoff has complexity, risk, cost, or timeline impact | Enables apples-to-apples comparison | Draft |
| 6 | **Recommendation grounded** — Chosen option has explicit evidence backing | Prevents opinion-based decisions | Draft |
| 7 | **Evidence anchored** — Every claim has file paths, command outputs, or test results | Provides traceability | Draft |
| 8 | **Migration plan exists** — Phase sequence, compatibility strategy, fallback plan | Enables safe rollout | Draft |
| 9 | **Risks documented** — Failure modes with safeguards or mitigations | Enables risk-aware planning | Draft |
| 10 | **Validation strategy** — Commands, tests, expected pass/fail signals | Enables verification | Draft |
| 11 | **Open questions decision-ready** — Each has options, consequences, and blocking impact | Enables planning gate | Draft |
| 12 | **Post-study proposals** — At least 3 context-adapted actions in SCREAMING_SNAKE_CASE | Provides actionable handoff | Closeout |
| 13 | **Cross-skill routing** — Next skill identified and outputs prepared | Completes the delivery loop | Closeout |
| 14 | **Appendixes complete** — File inventory, references, validation outputs included | Provides evidence trail | Closeout |
| 15 | **No contradictions** — Options, tradeoffs, and recommendation are internally consistent | Prevents confusion | Sanity-check |
| 16 | **Published** — Study folder committed and pushed | Enables team access | Closeout |

### Quality Tiers

| Tier | Criteria | Use When |
|------|----------|----------|
| **Minimal** | Items 1, 2, 4, 6, 12 | Quick decision with no uncertainty |
| **Standard** | Items 1-12, 13 | Multi-option decision with evidence and tradeoffs |
| **Deep** | All 16 items | Complex architecture with risks and migration |

### Pre-Publish Verification

Before finalizing a study, run through the checklist mentally:

```
□ Objective is clear and singular
□ In-scope / out-of-scope listed
□ Current state documented with file paths
□ At least 2 viable options (if applicable)
□ Tradeoffs quantified with numbers/impact
□ Recommendation has explicit evidence
□ All claims have file/command/test evidence
□ Migration plan exists
□ Risks documented with mitigations
□ Validation commands identified
□ Open questions are decision-ready
□ At least 3 post-study proposals
□ Next skill identified and outputs prepared
□ Appendixes complete
□ No contradictions found
□ Study committed and pushed
```

## Study Consistency Validator

Before finalizing a study, run these consistency checks. A study that fails any check must be fixed before finalizing.

### Consistency Check Matrix

| Check | What to Verify | How to Fix |
|-------|---------------|------------|
| **Options vs Tradeoffs** | Every option has corresponding tradeoffs | Add missing tradeoff rows |
| **Tradeoffs vs Recommendation** | Recommendation accounts for tradeoff analysis | Adjust recommendation or add evidence |
| **Evidence vs Claims** | Every major claim has file/command/test evidence | Add evidence or qualify claim as assumption |
| **Scope vs Current State** | Current state covers all in-scope items | Expand current state or narrow scope |
| **Migration vs Options** | Migration plan matches chosen recommendation | Align migration to chosen option |
| **Risks vs Migration** | Migration plan addresses identified risks | Add risk mitigations to migration |
| **Open Questions vs Scope** | Open questions are within in-scope, not out-of-scope | Move to out-of-scope or remove |
| **Proposals vs Open Questions** | Proposals address open questions or next steps | Add proposals or resolve questions |
| **Appendixes vs Body** | All body references to files/logs have appendix entries | Add to appendix or remove reference |
| **Tier vs Content** | Content matches declared quality tier | Upgrade tier or add missing content |

### Red Flags (Never Finalize)

A study with any of these must be fixed before finalizing:

- [ ] Major claim without any evidence (file path, command, test)
- [ ] Recommendation contradicts tradeoff analysis
- [ ] Open question that is actually out-of-scope
- [ ] Migration plan for option other than recommendation
- [ ] Contradictory statements in different sections
- [ ] Tradeoff without any quantification

## Study Generation Template

Use this template when the user asks to "study", "analyze", "evaluate", or "compare" a technical decision. Fill in each section with specific content.

### Phase 1: Define the Decision

```
# Study: [Clear decision or problem statement]
**Slug:** [slug]
**Created:** [date]
**Quality Tier:** [Minimal | Standard | Deep]

## Objective
One clear sentence stating the decision or problem.

## Scope and Constraints
### In-scope
- [ ] 
- [ ] 
### Out-of-scope
- [ ] 
- [ ] 
### Constraints
- [ ] 
```

### Phase 2: Document Current State

```
## Current State

### Existing Architecture/Behavior
[Describe what exists today with specific file paths]

### Relevant Files
| File | Purpose |
|------|--------|
| `path/to/file.ts` | What this file does |
```

### Phase 3: Generate Options

```
## Option Set

### Option A: [Name]
- **Summary:** One sentence
- **Approach:** How it works
- **Evidence:** File paths, command outputs, tests

### Option B: [Name]
[Same structure]
```

### Phase 4: Analyze Tradeoffs

```
## Tradeoff Analysis

| Dimension | Option A | Option B |
|-----------|----------|----------|
| Complexity | [0-5] | [0-5] |
| Risk | [0-5] | [0-5] |
| Migration Cost | [0-5] | [0-5] |
| Timeline Impact | [0-5] | [0-5] |
```

### Phase 5: Make Recommendation

```
## Recommendation: [Option A | Option B]

**Evidence:** Why this option is chosen

**Migration Plan:**
1. [Step]
2. [Step]

**Fallback:** What to do if this fails
```

### Phase 6: Document Risks and Validation

```
## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |

## Validation Strategy

- [ ] Command: `npm run test`
- [ ] Expected: Pass/fail signal
```

### Phase 7: Open Questions and Proposals

```
## Open Questions

The count is contextual. Record only the genuinely unresolved questions that block planning; if none remain, replace this section with `No unresolved open questions.` Do not pad with low-value questions to fill the section.

### Open Question 1: [Title]
- **Question:**
- **Options:** Option A vs Option B
- **Consequences:** What each choice means
- **Recommendation:**

## Post-Study Proposals

The count is contextual. One strong proposal beats several padded ones. Include only the next-step actions that are genuinely distinct and would each be useful to a downstream reader; if no clear follow-up exists, replace this section with `No follow-up actions proposed.`

- `WRITE_PLAN_FROM_STUDY` (Recommended): Create implementation plan
- `DEEPEN_WITH_RESEARCH`: Research external best practices
- `DECIDE_OPEN_QUESTIONS`: Resolve remaining open questions
```

### Phase 8: Final Review

Before finalizing, verify:

```
□ Study Quality Checklist complete (run through all 16 items)
□ All claims have file/command/test evidence
□ Tradeoffs are quantified (complexity, risk, cost, timeline)
□ Recommendation is grounded in evidence
□ Appendixes created (file inventory, references, validation)
□ Post-study proposals written (at least 3)
```

## Guidance Alignment

> Snapshot verified: 2026-04-30
>
> If guidance semantics have changed, run the `agents-sync` workflow before workflow closure.
> For current web information, prefer Firecrawl CLI via `research-online/SKILL.md` before the built-in `web` tool.

## Non-Negotiable Policy

1. Save new studies under `.studies/`, never under `docs/` unless explicitly requested. Use one timestamped folder per study.
2. Use `references/study-outline.md` to locate the right template before broad reading. Never reconstruct study structure, CLI flags, or shell commands from memory.
3. Keep claims tied to concrete evidence with repository-relative file paths.
4. Load only the subset of `references/` the task requires. Do not read every file by default.
5. After completing a study, propose context-adapted follow-up actions using `SCREAMING_SNAKE_CASE` names. Include at least one option for plan write-down, depth increase, and online research. The mandatory next step toward implementation is planning via `plan/SKILL.md`.
6. Unresolved open questions must be decision-ready subsections with viable options, concrete consequences, and blocking impact. When none remain, say so explicitly.
7. Sub-agent deepening is an opt-in extension. After explicit user approval, model the six-lane pass as six **tracked sub-tasks** (to-do entries or equivalent per-lane state), one lane at a time, no batch-level retry. Dispatch in parallel when the active harness allows; fall back to in-order dispatch when parallelism caps are hit, in the order `codepath → runtime-contract → implementation-change → regression-strategy → operator-surface → documentation-workflow`. Integrate each lane's findings as soon as its sub-task moves to `done`. Only retry the lanes whose sub-task lands in `failed` — never re-run a completed lane.
8. Commit and push the completed study folder immediately; scope must include only the study folder. For any answer about models, pricing, or current versions of external tools: treat bundled data as likely stale and verify with the research skill before stating specifics.
9. After creating or updating any study markdown file, generate its sibling HTML with `scripts/render-markdown-html.ts` and report the **absolute paths** of the markdown file(s) and the HTML page(s) to the user.

## Standard Output Layout

Inside each timestamped study folder:

| Artifact | Path |
|----------|------|
| Main study | `study-<slug>.md` |
| HTML twin | same basename with `.html` (next to each modified `.md`) |
| File inventory | `appendix-01-file-inventory.md` |
| References | `appendix-02-references.md` |
| Validation and tests | `appendix-03-validation-and-tests.md` |
| Log excerpts | `appendix-04-log-excerpts.md` |
| Charts and matrices | `appendix-05-charts-and-matrices.md` |
| Firecrawl raw | `firecrawl/raw/` (when used) |
| Firecrawl reports | `firecrawl/reports/` (when used) |
| UI spec | `ui-spec/` (when UI/page planning is in scope) |

Appendixes are optional; create only those that add value.

## Six-Lane Child Roles

The six canonical lane templates live in `references/subagents/`. Treat them as exemplars that this skill biases toward; the active harness decides how to invoke them and may substitute harness-specific variants for any lane without changing this skill.

- `references/subagents/codepath-cartographer.md`
- `references/subagents/runtime-contract-auditor.md`
- `references/subagents/implementation-change-auditor.md`
- `references/subagents/regression-strategy-auditor.md`
- `references/subagents/operator-surface-auditor.md`
- `references/subagents/documentation-workflow-auditor.md`

Recommended parent pattern:

1. **Set up six tracked sub-tasks** — one per lane — before any dispatch (to-do list, checklist, or equivalent per-lane state record). Each lane has its own status: `pending`, `in_progress`, `done`, or `failed`. Do not treat the six lanes as a single batch.
2. **Keep one parent writer and publisher** that owns the study file. Lanes return findings as JSON, prose, or scratch artifacts they explicitly own; the parent is the only writer to the main study until final closeout.
3. **Dispatch in parallel** by default when the active harness allows it; this is the fastest lane-to-lane composition for handoffs that have no inherent ordering.
4. **Fall back to in-order** dispatch if the harness caps parallel sub-agents (token limits, concurrency caps, host throttling, etc.). Use the canonical lane order: `codepath-cartographer → runtime-contract-auditor → implementation-change-auditor → regression-strategy-auditor → operator-surface-auditor → documentation-workflow-auditor`. A later lane starts only after the previous one has returned.
5. **Integrate per lane, as soon as it returns.** Update the sub-task to `done` and merge its findings into the study or the relevant appendix immediately. Do not wait for the whole batch to land.
6. **Retry only failed lanes.** A sub-task in `failed` can be retried independently (one retry path per lane); completed lanes are never re-run, even if their findings are later revised by another lane.
7. **Normalize overlaps or contradictions** only after every tracked sub-task reaches a terminal state (`done` or `failed-and-exhausted`).
8. **Re-run consistency** after the last integration pass.

## Workflow

1. **Define scope and slug.** Choose a concise slug that captures the decision topic.
2. **Initialize study workspace.** Run `init-study.ts` (see Quick Commands). If Firecrawl is part of evidence collection, write fetched payloads under `firecrawl/raw/` and notes under `firecrawl/reports/`.
3. **Collect evidence.** Gather affected files, command outputs, test results, and log excerpts.
4. **Write the main study.** Follow the outline in `references/study-outline.md`. Include problem framing, current state, options, tradeoffs, risks, recommendation, and migration plan. When UI/page implementation guidance is in scope, create a visible local UI spec artifact inside the study folder.
5. **Create appendixes.** Keep raw/verbose artifacts in appendixes; keep the main study decision-oriented. After any markdown write, run `render-markdown-html.ts` so each `.md` has a sibling `.html`.
6. **Verify consistency.** Ensure paths exist, options are internally consistent, and recommendation matches evidence.
7. **Propose post-study actions.** Adapt action names to context. Use `SCREAMING_SNAKE_CASE`. Include at least one option for plan write-down, depth increase, and online research.
8. **Finalize and publish.** Run `finalize-study.ts` (see Quick Commands). Do not skip this step by default.

For the detailed section outline and open-question template, see `references/study-outline.md`.

## Evidence Guidelines

1. For command-based evidence, record: command, key result summary, timestamp when relevant.
2. For logs, include concise excerpts with context around the signal lines.
3. For tests, include exact test commands and pass/fail outcomes.
4. For charts/tables, put high-density artifacts in appendixes and link from the main study.

## Completion Output Contract

When presenting a completed study, include a short proposal block with:

- The **absolute path** of each study markdown file that was created or updated, and the **absolute path** of its HTML twin.
- At least 3 context-adapted actions using `SCREAMING_SNAKE_CASE`, presented per `chooseable-options/SKILL.md` (printed tokens **and** the harness Ask User picker when available).
- One action for each default intent: plan write-down, depth increase, online research.
- `CREATE_SPECS_FOR_FINDINGS` when issues or opportunities were discovered.
- `DEEPEN_STUDY_WITH_SIX_SUBAGENTS` when the study is strong but the concrete change map is still fuzzy.
- `EXPLAIN_IMPLEMENTABLE_SCOPE` when the study already has a chosen direction and concrete implementation-ready change map.
- `EXPLAIN_FINDINGS_VISUALLY` when the study is too dense for fast comprehension.
- `DECIDE_OPEN_QUESTIONS` when unresolved user-choice items remain.
- Confirmation that study artifacts were committed and pushed (or report why publish failed).

## Cross-Skill Handoffs

| Trigger condition | Target skill | Handoff outputs |
|-------------------|--------------|-----------------|
| Study complete, user ready to execute | `plan/SKILL.md` | Study path, visible UI spec path when applicable, recommended execution sequence, risk/mitigation list, validation commands, `skills:rewire` requirement when skill files are in scope. |
| Unresolved user choices | `decisions/SKILL.md` | Study path, ordered open questions, candidate approaches with tradeoffs, recommended path, impacted files/tests/systems, evidence gaps. |
| Manual rollout or setup checklist | `step-by-step/SKILL.md` | Study path, ordered manual checklist, prerequisites and completion evidence, recommended first active step. |
| External best-practice research needed | `research-online/SKILL.md` | Focused research questions, target domains/sources, expected deliverable format. |
| Findings too dense for fast comprehension | `explain/SKILL.md` | Study path, exact question or part needing explanation, chosen direction and non-goals, concrete change inventory, regression scope, doc/operator follow-up. |
| Guidance drift in AGENTS.md or proxies | the `agents-sync` workflow | Identified drift areas, target repos/submodules for synchronization. |
| Multiple discrete issues found | `specs/SKILL.md` | Study path and appendixes, discovered issues with priority, observed behavior, key source files. |

## Blocking Gates

1. Do not start implementation directly from this skill without a planning handoff.
2. Do not claim execution readiness when no `.plans/...` execution plan exists.
3. Do not mark study output as execution-ready without explicit downstream handoff outputs.
4. Do not treat downstream tracking as resolved unless the handoff explicitly names the target tracking workflow or reports why tracking is intentionally out of scope.

## Common Pitfalls

1. **Using `docs/` instead of `.studies/`** -- Always save studies under `.studies/YYYY-MM-DD-HHmmss-<slug>/`. See `references/study-outline.md`.
2. **Forgetting to commit and push** -- Run `finalize-study.ts` immediately after completion. Do not leave artifacts uncommitted.
3. **Shallow open questions** -- Write full subsections with options and consequences, not bare fragments. See the template in `references/study-outline.md`.
4. **Jumping to implementation** -- Always hand off to `plan/SKILL.md` first. Implementation without a plan is a policy violation.
5. **Reading all references for every study** -- Load only `references/study-outline.md` unless the task specifically needs deeper reference material.
6. **Skipping HTML twins or relative-only paths** -- After any markdown write, generate sibling HTML and give the user absolute paths to both.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `init-study.ts` throws "Study folder already exists" | Slug collision or duplicate run | Use `--timestamp` override or choose a different slug. |
| `finalize-study.ts` throws "staged changes already exist" | Unrelated WIP is staged | Commit or unstage existing changes first. |
| `finalize-study.ts` reports "No study changes were staged" | Wrong study directory path | Verify the path exists under `.studies/` and matches the timestamp-slug format. |
| Study feels too thin | Missing evidence appendixes | Add `appendix-01-file-inventory.md` and `appendix-03-validation-and-tests.md` with concrete outputs. |
| User wants to skip planning | Policy misunderstanding | Explain that planning is mandatory per policy; do not begin implementation. |

## Script Inventory

| Script | Purpose |
|--------|---------|
| `scripts/init-study.ts` | Initializes `.studies/<timestamp>-<slug>/` with a main study file and standard appendix stubs. |
| `scripts/render-markdown-html.ts` | Writes a sibling `.html` for a markdown file or every `.md` in a study folder; prints absolute paths. |
| `scripts/finalize-study.ts` | Regenerates HTML twins, then stages only the specified study folder, commits it, and pushes the current branch. |

## Local Corpus Layout

The `references/` directory contains hand-authored study assets:

| Path | Description |
|------|-------------|
| `study-outline.md` | Reusable section outline and open-question template for the main study file. |
| `subagents/` | Canonical lane templates for the optional six-lane deepening pass; the active harness picks them up automatically. |

No vendored documentation snapshots. No captured corpus.

> **Snapshot age:** verified 2026-04-30.

[^rt]: `npx tsx` accepts any standard runner — `bunx tsx`, `pnpm dlx tsx`, `deno run -A npm:tsx`, `node --import tsx`, or `yarn dlx tsx`. The first five auto-fetch `tsx` on demand; only `node --import tsx` requires `tsx` to be installed locally first (`npm i -D tsx`, or `npm i -g tsx` if you cannot reach the npm registry). Bun users can also skip `tsx` entirely and run TypeScript directly via `bun <script>`. Pick whichever your project ships. The canonical runtime decision table lives in the `skills-manager` skill under `Runtime Selection` (only available when working in the full `gg-skills` monorepo).
