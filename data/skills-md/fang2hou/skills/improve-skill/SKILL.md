---
name: improve-skill
description: Audits and improves existing Agent Skills. Scores 8 quality dimensions, drafts an approval-gated plan, applies changes, and verifies them against a baseline run. Use when reviewing, refactoring, or upgrading a skill or a skill collection.
license: MIT
compatibility: Requires file read/write access to modify skills. Works with any agent supporting the Agent Skills standard.
metadata:
  author: fang2hou
  version: "1.3"
  sources: "agentskills.io specification, best practices, evaluating-skills, and optimizing-descriptions guides; Anthropic skill authoring best practices"
---

# Improve Skill

Analyze, score, and optimize existing Agent Skills to production quality, using an 8-dimension quality framework, approval gates, and baseline comparison.

## When to Use

- Reviewing an existing skill for improvement opportunities
- Upgrading a skill to meet the Agent Skills specification or current authoring guidance
- Refactoring a bloated, unclear, over-constrained, or under-triggering skill
- Auditing quality and trigger overlap across a skill collection

## When NOT to Use

- Creating a new skill from scratch (use create-skill, which includes its own validation)
- General code refactors unrelated to skills (use a code-focused refactoring skill instead)
- Situations where you cannot read the target skill files (this workflow is evidence-based)

## Inputs

| Input               | Required | Format                       | Examples                                |
| ------------------- | -------- | ---------------------------- | --------------------------------------- |
| Invocation argument | No       | Skill path or directory      | `agents/skills/my-skill`, `./my-skill/` |
| Invocation argument | No       | Skill name (resolver needed) | `my-skill`                              |
| Invocation argument | No       | Collection directory         | `skills/`                               |

**Cross-platform note**: Clients that expose an invocation argument (for example a `$ARGUMENTS` placeholder) pass the target through it. If no such argument is available or it does not resolve to a skill directory, ask the user for the target skill path.

## Hard Rules

1. **Preserve intent**: Never alter a skill's core purpose. Optimization improves how the skill works, not what it is for.
2. **User approval required**: Present the optimization plan and get explicit approval before modifying files. A user request that names the targets and asks you to apply improvements approves intent-preserving changes; renaming a skill, changing its `name`, removing a capability, or deleting a file still needs separate approval.
3. **Spec compliance**: All output conforms to the Agent Skills specification.
4. **No data loss**: Do not delete content without relocating it (to `references/` or restructuring), unless the content is agent-known, duplicated, or demonstrably harmful; record each such removal and its reason in the report.
5. **Measurable improvement**: Every optimization improves at least one quality dimension score.
6. **Gate discipline**: Do not proceed past a gate until all its conditions are met.
7. **Context-cost discipline**: Do not increase context cost without a corresponding capability gain; removing content the agent already knows is an improvement.

Rule 4's exception and Rule 7 work together: cutting agent-known or harmful text is allowed and encouraged, but cutting a domain fact, gotcha, or safety rule is data loss.

## Workflow

### Phase 0: Target Acquisition

1. If an invocation argument specifies a skill path or name, locate it
2. If currently inside a skill directory, use the current directory
3. Otherwise, ask which skill to optimize
4. Read `SKILL.md` completely
5. Inventory all supporting files (references/, scripts/, assets/, evals/)
6. Read key supporting files to understand full scope
7. Before editing, copy the skill directory to a separate baseline snapshot for the later trial run

**Collection mode**: When the target is a directory of skills, snapshot the whole collection, then list every skill's `name` and `description` side by side and flag pairs whose triggers overlap. Run Phases 1–5 per skill; the overlap list feeds each skill's Dimension 2 score. Keep cross-skill references (one skill naming another as the alternative) consistent after each skill's changes.

**Gate 0 (proceed only when all are true):**

- [ ] Target skill directory identified
- [ ] SKILL.md read completely
- [ ] Supporting file inventory complete
- [ ] Pre-improvement baseline snapshot created

_If gate fails_: Ask user for the skill path or name rather than guessing.

### Phase 1: Intent & Rules Extraction

Record what must not change; use Pattern 8 (Intent Card) in [references/exemplar-patterns.md](references/exemplar-patterns.md) for rationale.

1. **Core intent**: What problem does this skill solve? Who is the audience?
2. **Mandatory rules**: Which constraints must survive? (Hard rules, safety, compliance)
3. **Check gates**: What verification points exist? Where should they exist?
4. **Domain type**: Is this a workflow, expertise/reference, or hybrid?
5. **Platform dependencies**: What relies on specific agent capabilities or client-only frontmatter?
6. **Terminology set**: Which terms name recurring concepts, and what single term should be used for each?
7. **Script inventory**: Does the skill ship `scripts/`? If yes, record each script's interface and safety/portability assumptions.
8. **Side effects and siblings**: Which actions leave the workspace (publish, delete, change remote settings), and which sibling skills share its triggers?

Document this as an Intent Card:

```
Intent: [one sentence]
Domain: [workflow | expertise | hybrid]
Mandatory Rules: [list]
Existing Gates: [list or "none"]
Platform Dependencies: [list or "none"]
Terminology Set: [canonical term → meaning; list or "none"]
Ships Scripts: [yes (list scripts and interfaces) | no]
Side Effects: [list with confirmation points, or "none"]
Sibling Skills: [overlapping skills and the boundary, or "none"]
```

**Gate 1 (proceed only when all are true):**

- [ ] Intent card completed
- [ ] Mandatory rules identified and flagged as untouchable
- [ ] Domain type classified
- [ ] Terminology set, script inventory, side effects, and siblings captured

_If gate fails_: Re-read SKILL.md focusing on purpose statements and constraint sections.

### Phase 2: Quality Audit

Score the skill across 8 dimensions (1-5 each, max 40). Load [references/scoring-rubric.md](references/scoring-rubric.md) for detailed criteria and evidence guidance.

When a trial run is feasible, use [references/trial-run.md](references/trial-run.md) and grade objective assertions against improved and baseline runs; otherwise mark the scorecard static-evidence-only.

| #   | Dimension                         | What to Assess                                                                   |
| --- | --------------------------------- | -------------------------------------------------------------------------------- |
| 1   | Spec Compliance                   | Frontmatter fields, naming rules, directory structure, client constraints        |
| 2   | Description Quality               | Front-loaded use case, keywords, WHAT + WHEN, boundary against sibling skills    |
| 3   | Context Economy & Disclosure      | Agent-known content omitted, scoped references, one-level navigation             |
| 4   | Structural Clarity                | Section organization, logical flow, navigability                                 |
| 5   | Instruction Quality & Calibration | Fragility-matched specificity, reasons over emphasis, no conflicts, defaults     |
| 6   | Guardrails & Validation           | Validation loops, plan gates, side-effect confirmation, robust scripts           |
| 7   | Composability & Script I/O        | Structured output, stderr diagnostics, exit codes, retry-safe runs               |
| 8   | Cross-Platform Compatibility      | Portable instructions, paths, client-only fields isolated, no runtime assumption |

Present as a scorecard:

```
┌───┬───────────────────────────────────┬───────┬──────────────────────────────┐
│ # │ Dimension                         │ Score │ Key Finding                  │
├───┼───────────────────────────────────┼───────┼──────────────────────────────┤
│ 1 │ Spec Compliance                   │  ?/5  │ ...                          │
│ 2 │ Description Quality               │  ?/5  │ ...                          │
│ 3 │ Context Economy & Disclosure      │  ?/5  │ ...                          │
│ 4 │ Structural Clarity                │  ?/5  │ ...                          │
│ 5 │ Instruction Quality & Calibration │  ?/5  │ ...                          │
│ 6 │ Guardrails & Validation           │  ?/5  │ ...                          │
│ 7 │ Composability & Script I/O        │  ?/5  │ ...                          │
│ 8 │ Cross-Platform Compatibility      │  ?/5  │ ...                          │
├───┼───────────────────────────────────┼───────┼──────────────────────────────┤
│   │ TOTAL                             │ ??/40 │                              │
└───┴───────────────────────────────────┴───────┴──────────────────────────────┘
```

**Gate 2 (proceed only when all are true):**

- [ ] All 8 dimensions scored with evidence
- [ ] Top 3 improvement areas identified and ranked by impact
- [ ] No dimension scored without reading the relevant content
- [ ] Trial-run behavior is included when a trial run was performed; otherwise the scorecard is marked static-evidence-only

_If gate fails_: Re-assess weak evidence; read more source files. For new checkpoints, use Pattern 1's gate shape in [references/exemplar-patterns.md](references/exemplar-patterns.md).

### Phase 3: Optimization Plan

Record for each change: what changes (section/field/structure); rationale (best practice/spec); before/after; impact (expected score); risk (intent drift/reference breakage).

Cross-check the plan against known anti-patterns. See [references/anti-patterns.md](references/anti-patterns.md). Prefer removing or rewording an instruction over adding one: a plan that only adds text is a warning sign for Dimension 3.

Present the plan to the user. **Wait for explicit approval before proceeding** (see Hard Rule 2 for what counts as approval).

**Gate 3 (proceed only when all are true):**

- [ ] Plan presented with before/after examples
- [ ] User explicitly approved (full plan or approved subset)
- [ ] No approved change violates any Hard Rule

_If gate fails_: Revise the plan based on user feedback. Present again.

### Phase 4: Execute with Self-Correction

Apply approved changes by increasing risk: frontmatter fixes (lowest risk) → description improvements → structural reorganization → content splits to `references/` → new sections (verification, guardrails, failure handling) → content rewrites (highest risk).

**Self-correction triggers during execution:**

| Trigger                                            | Automatic Action                                            |
| -------------------------------------------------- | ----------------------------------------------------------- |
| SKILL.md exceeds 500 lines after edit              | Split overflow content into references/                     |
| Description exceeds 250 chars                      | Tighten to front-load the key use case                      |
| Description or name contains `<` or `>`            | Remove the angle brackets                                   |
| `name` doesn't match directory name                | Fix name field to match directory                           |
| File reference points to nonexistent file          | Create the missing file or remove the reference             |
| Score regresses on any dimension                   | Stop, identify the cause, fix before continuing             |
| Mandatory rule accidentally altered                | Immediately revert that specific change                     |
| An edit adds ALL-CAPS or an unexplained MUST/NEVER | Rewrite as a plain instruction plus its reason              |
| Two instructions now conflict                      | State precedence or qualify one condition                   |
| A client-only frontmatter field is introduced      | Remove it unless the skill already targets that client      |
| A time-sensitive statement is introduced           | Replace it with a timeless rule or Old patterns section     |
| An option menu has no selected default             | Choose one default and keep alternatives as an escape hatch |
| A reference chain goes deeper than one level       | Link directly from SKILL.md or flatten the chain            |
| A path contains a backslash                        | Rewrite it as a forward-slash relative path                 |
| Gotchas are moved out of SKILL.md                  | Restore trigger-critical Gotchas to SKILL.md                |

After each major edit, re-read the modified file to verify correctness.

**Gate 4 (proceed only when all are true):**

- [ ] All approved changes applied
- [ ] No self-correction trigger left unresolved
- [ ] All file references resolve to existing files
- [ ] SKILL.md is under 500 lines

_If gate fails_: Apply the relevant self-correction rule. If stuck after 2 attempts, report to user.

### Phase 5: Verify & Report

1. **Re-audit**: Run Phase 2 scoring on the optimized skill
2. **Compare**: Build before/after scorecard
3. **Validate spec**: Check all Agent Skills spec rules. See [references/spec-rules.md](references/spec-rules.md). Run the project's own skill validator too, when one exists.
4. **Check references**: Verify all linked files exist and are non-empty
5. **Trial run**: For each realistic task, launch the improved skill and the pre-improvement snapshot at the same time, each in its own fresh context (a subagent or new session with no memory of this edit). Read both execution traces and record assertions that pass only with the improved version. Follow [references/trial-run.md](references/trial-run.md) when designing cases and grading evidence; run a trigger eval whenever the description changed.
6. **Token and line estimate**: Record the approximate token cost and line-count delta for SKILL.md

The baseline is the snapshot copied before editing, not a reconstruction after the fact. The context that performed the edit is not fresh; if no fresh-context mechanism exists, say so and label the evidence same-context. If a trial run is infeasible (for example every realistic task has external side effects that cannot be sandboxed), state the concrete reason and the static evidence used instead.

Output the final report:

```
┌──────────────────────────────────────┬────────┬───────┬────────┐
│ Dimension                            │ Before │ After │ Change │
├──────────────────────────────────────┼────────┼───────┼────────┤
│ 1. Spec Compliance                   │  X/5   │  Y/5  │  +Z    │
│ 2. Description Quality               │  X/5   │  Y/5  │  +Z    │
│ 3. Context Economy & Disclosure      │  X/5   │  Y/5  │  +Z    │
│ 4. Structural Clarity                │  X/5   │  Y/5  │  +Z    │
│ 5. Instruction Quality & Calibration │  X/5   │  Y/5  │  +Z    │
│ 6. Guardrails & Validation           │  X/5   │  Y/5  │  +Z    │
│ 7. Composability & Script I/O        │  X/5   │  Y/5  │  +Z    │
│ 8. Cross-Platform Compatibility      │  X/5   │  Y/5  │  +Z    │
├──────────────────────────────────────┼────────┼───────┼────────┤
│ TOTAL                                │ XX/40  │ YY/40 │ +ZZ    │
└──────────────────────────────────────┴────────┴───────┴────────┘

Estimated tokens: ~NNNN (SKILL.md) + ~NNNN (references)
SKILL.md lines: BEFORE N → AFTER M (delta ±D)
Spec compliance: PASS / FAIL [details]
File integrity: All references resolve / [broken refs]
Trial-run evidence: [task, baseline comparison, assertions flipped, cost/latency delta] / NOT FEASIBLE [reason]
```

**Gate 5 (optimization complete when all are true):**

- [ ] Total score improved (or maintained if already high quality)
- [ ] No dimension score regressed from Phase 2 baseline
- [ ] Spec compliance passes all checks
- [ ] All file references resolve to existing, non-empty files
- [ ] Trial-run evidence includes the improved-vs-baseline task and assertions, or an explicit reason the trial run was not feasible

_If gate fails_: Return to Phase 4 to fix regressions. Maximum 2 correction cycles before escalating to user.

## Self-Correction Protocol

The gates and triggers above handle known failures. For everything else:

1. **Escalation**: If the same gate fails twice after correction attempts, stop and report to user with which gate failed, what correction was attempted, and what manual input is needed.
2. **Regression guard**: If any quality dimension drops during optimization, revert the change that caused it and report the regression.
3. **Scope lock**: If during execution you discover the skill needs changes beyond the approved plan, do not apply them. Note them as "Deferred Recommendations" in the final report.
4. **Plateau check**: If repeated additions stop improving trial results, try removing instructions instead; an over-constrained skill improves when rules that do not apply are cut.

## Key Patterns to Apply

When optimizing, draw from these proven patterns. Full catalog with examples at [references/exemplar-patterns.md](references/exemplar-patterns.md).

| #   | Pattern                       | When to Apply                                          |
| --- | ----------------------------- | ------------------------------------------------------ |
| 1   | Gate Checkpoints              | Multi-step workflow with failure risk                  |
| 2   | Output Contract               | Skill produces artifacts others consume                |
| 3   | Hard Rules Section            | Skill has non-negotiable constraints                   |
| 4   | Progressive Reference Loading | SKILL.md > 300 lines or detailed criteria              |
| 5   | Failure Handling Section      | Skill has steps that can fail                          |
| 6   | Self-Correction Rules         | Execution may drift from intent                        |
| 7   | Validation Checklist          | Multi-category validation would clutter the workflow   |
| 8   | Intent Card                   | Any existing skill is about to be modified             |
| 9   | When to Use Section           | Every skill; prevents false activation                 |
| 10  | Input Documentation           | Skill assumes implicit inputs                          |
| 11  | Validation Loop               | A script or checklist can objectively verify work      |
| 12  | Plan-Validate-Execute         | Batch or destructive operations need a safe plan       |
| 13  | Progress Checklist            | Workflow has several ordered steps or gates            |
| 14  | Output Format Template        | Outputs vary or another skill consumes the result      |
| 15  | Worked Input/Output Examples  | A step has ambiguous inputs or expected outputs        |
| 16  | Calibrated Instruction Block  | Some steps are fragile while others allow choice       |
| 17  | Bundled Script Interface      | Repeated logic merits a tested, non-interactive script |
| 18  | Old Patterns Section          | Superseded guidance must remain discoverable           |
| 19  | Reasoned Constraint           | A rule relies on emphasis instead of its reason        |
| 20  | Explicit Precedence           | Two instructions can apply with different outcomes     |

Numbers match the pattern numbers in [references/exemplar-patterns.md](references/exemplar-patterns.md). A skill that lacks a verification step needs Pattern 11 (Validation Loop), not a prose "verification" section.

## Output Contract

On completion, always return:

1. Before/after scorecard (table format as shown in Phase 5)
2. Summary of changes made (bulleted list), including content removed and why
3. List of files modified and created
4. Trial-run evidence: realistic task, baseline comparison, assertions that flipped, and cost/latency delta
5. `SKILL.md` token estimate and line-count delta
6. Deferred recommendations (low-priority items not addressed)

Keep the human-readable report primary. Downstream consumers may rely on these stable fields, in this order:

```yaml
output_fields:
  - before_after_scorecard
  - changes_summary
  - files_modified_and_created
  - trial_run_evidence
  - skill_token_estimate_and_line_count_delta
  - deferred_recommendations
```

Report findings and evidence, not internal deliberation.

## References

- [Scoring Rubric](references/scoring-rubric.md): load in Phase 2 for the 1–5 criteria of all 8 dimensions
- [Spec Validation Rules](references/spec-rules.md): load in Phase 5 for spec and client-constraint checks
- [Anti-Patterns](references/anti-patterns.md): load in Phase 3 to review the plan against known failure modes
- [Exemplar Patterns](references/exemplar-patterns.md): load when an approved change needs a pattern template
- [Trial-Run Procedure](references/trial-run.md): load in Phase 5 for baseline comparison, assertions, trace analysis, trigger evals, or cross-configuration coverage
