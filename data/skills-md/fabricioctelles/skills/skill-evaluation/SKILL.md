---
name: skill-evaluation
description: >
  Evaluate any agent skill against a merged framework — Anthropic's Claude Code
  best practices plus Matt Pocock's writing-great-skills methodology — across
  4 axes (Trigger, Structure, Steering, Pruning). Produces an evidence-cited
  scorecard (0–100), a weighted overall score, and diagnosed failure modes
  with prioritized fixes. Use when the user asks to evaluate, rate, or audit
  a skill ("evaluate this skill", "skill scorecard", "review SKILL.md"), or
  to compare two skills.
metadata:
  author: ft.ia.br
  version: "2.1.0"
  date: 2026-07-03
  repository: https://github.com/fabricioctelles/skills
  license: Apache-2.0
  category: code-quality-and-review
---

# Skill Evaluation

If you need the vocabulary and tests behind Axes 1, 3, and 4 (leading words,
completion criteria, context pointers, the deletion test, failure-mode
definitions), read `references/mechanics.md` before scoring those axes.

## Source

- [Lessons from building Claude Code: How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) — Anthropic, Jun 2026
- "The Missing Manual: How to Write Great Skills" — Matt Pocock, AI Engineer World's Fair 2026 ([video](https://www.youtube.com/watch?v=UNzCG3lw6O0)), and his `writing-great-skills` skill

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `target` | Path to skill directory or SKILL.md to evaluate | Ask user |
| `output` | Path to write the scorecard | `<target>/EVALUATION.md` |
| `compare` | Optional second skill to compare side-by-side | None |

Also runs unattended: in CI, point `target` at skills changed in a PR and
gate with `scripts/score.py --fail-below 60 ...` — non-zero exit below the
threshold fails the check.

## Criteria

18 criteria: 14 core, scored on every skill, plus 4 conditional criteria
scored only when the skill's category makes them apply — otherwise mark
**N/A** and exclude the criterion from both the numerator and denominator of
the weighted average. Every score is 0–100 with evidence citing file,
section, or line.

### Axis 1 — Trigger (invocation)

| # | Criterion | Weight | Key question |
|---|-----------|--------|---------------|
| 1 | Invocation design | 2x | Is model-invoked vs. user-invoked deliberate and fitting? Model-invoked pays **context load** (the description loads every turn); user-invoked pays **cognitive load** (the human is the index). A skill that only ever fires by hand should be user-invoked. |
| 2 | Description quality | 2x | Model-invoked: leading word up front, one trigger per branch (synonyms renaming the same branch are duplication), no identity that's redundant with the body. User-invoked (`disable-model-invocation: true`): a human-facing one-liner, no trigger list. Score against the mode the skill actually uses — never penalize a user-invoked skill for lacking trigger phrases. |

### Axis 2 — Structure

| # | Criterion | Weight | Key question |
|---|-----------|--------|---------------|
| 3 | Steps vs. reference clarity | 1x | Does the skill distinguish ordered steps from on-demand reference? All-reference and all-steps skills are both valid — score clarity, not the mix. Is related material co-located (definition, rules, caveats under one heading)? |
| 4 | Branch-aware disclosure & pointers | 2x | Is material every branch needs inline, and material only some branches need behind a context pointer? Does each pointer's wording say when to follow it ("if you need X, read Y")? A weakly worded pointer to must-have material is a variance bug. |
| 5 | Conciseness (no sprawl) | 2x | Is SKILL.md lean — under 500 lines as a ceiling, smaller is better — with every line earning its context cost? |
| 6 | Coherent scope | 1x | Does the skill do one thing and compose with others, rather than covering too much? |

### Axis 3 — Steering

| # | Criterion | Weight | Key question |
|---|-----------|--------|---------------|
| 7 | Leading words | 2x | Does the skill use compact, high-prior terms ("vertical slice", "tight", "red") to anchor behavior, repeated consistently? Could any verbose passage collapse into one? |
| 8 | Completion criteria & legwork | 2x | Skills with steps: does each step end on a checkable, exhaustive completion criterion? A vague one invites premature completion. Skills that are pure reference: is there an exhaustiveness bar over the reference itself ("every rule applied")? If neither applies, mark N/A. |
| 9 | Gotchas section | 2x | Is there explicit capture of failure points, edge cases, footguns? |
| 10 | Grounded in expertise | 2x | Does content come from observed failures and real project facts, or generic "best practices"? |
| 11 | Avoids railroading | 1x | Does the skill leave room to adapt — procedures over declarations, defaults over menus — without over-prescribing? |

### Axis 4 — Pruning

| # | Criterion | Weight | Key question |
|---|-----------|--------|---------------|
| 12 | No-ops (deletion test) | 2x | Running the deletion test sentence by sentence: if removing a sentence leaves behavior unchanged, it's a no-op — including restatements of what the model already does by default. Cite line numbers for candidates. |
| 13 | Single source of truth | 1x | Does each meaning live in exactly one place? Duplication between SKILL.md and references/ counts too. |
| 14 | Relevance & sediment | 1x | Are there stale lines, accumulated layers, or material that no longer influences what the skill does? |

### Conditional criteria

Score only when the skill's category (from `references/categories.md`) makes
the criterion apply; otherwise mark N/A and drop it from the weighted
average entirely.

| # | Criterion | Weight | Applies to category |
|---|-----------|--------|----------------------|
| 15 | Setup flow | 1x | library-and-api-reference, data-fetching-and-analysis, ci-cd-and-deployment, infrastructure-operations |
| 16 | Memory mechanism | 1x | business-process-automation, data-fetching-and-analysis, runbooks |
| 17 | Scripts & libraries | 1x | product-verification, code-scaffolding-and-templates, code-quality-and-review, data-fetching-and-analysis, infrastructure-operations |
| 18 | On-demand hooks | 1x | code-quality-and-review, ci-cd-and-deployment |

Override this table with judgment, in either direction: score a criterion
for a skill outside these categories when it would clearly benefit (e.g., a
non-`product-verification` skill that obviously needs a helper script), and
mark it N/A even within an applicable category when the pattern doesn't fit
the skill's shape (e.g., a pure-reference vocabulary skill filed under
`code-quality-and-review` has nothing for a hook to enforce). Explain the
override in the scorecard either way.

### Overall score

```
overall = sum(score × weight) / sum(weight)
```

N/A criteria are excluded from both sums — never scored as 0, never counted
as weight.

## Scoring Guide

| Score | Meaning |
|-------|---------|
| 0 | Not present at all |
| 1–25 | Minimal/token effort, barely addresses the criterion |
| 26–50 | Partially addressed but with significant gaps |
| 51–75 | Solid implementation with room for improvement |
| 76–90 | Strong implementation, minor gaps only |
| 91–100 | Exemplary — would use as a reference for others |

## Grade Scale

| Grade | Range | Meaning |
|-------|-------|---------|
| A | 80–100 | Production-quality, reference skill |
| B | 60–79 | Good skill, minor improvements needed |
| C | 40–59 | Functional but significant gaps |
| D | 20–39 | Needs substantial rework |
| F | 0–19 | Skeleton only, not production-ready |

## Workflow

1. **Read the target skill** — SKILL.md, its frontmatter (check for
   `disable-model-invocation`), and every file in the skill directory.
2. **Read `references/mechanics.md`** — the vocabulary and tests Axes 1, 3,
   and 4 depend on, including what makes a context pointer's wording
   effective.
3. **Classify** — use `references/categories.md` and its decision tree to
   assign a category. The category determines which conditional criteria
   apply.
4. **Score all applicable criteria** — **cite-or-cut**: a criterion is only
   scored once its justification cites specific evidence (file, section, or
   line); no citation, no score. Mark N/A wherever the conditional table, or
   your own judgment, says a criterion doesn't apply. Done when every
   applicable criterion carries a score and a citation, and every N/A a
   reason.
5. **Trigger eval** — empirical test of whether the skill's description
   actually causes invocation. See the **Trigger Eval** section below for
   the full mechanic. Skip this step for user-invoked skills
   (`disable-model-invocation: true`) — they have no description to test.
6. **Diagnose failure modes** — done when every mode in the table below has
   been checked against the skill and either cited (file:line) or dismissed.
7. **Assess bonus patterns** — the 4 carried over from v1, plus a fifth:

   | Bonus | Applies when | What to look for |
   |-------|-------------|-----------------|
   | Validation loops | Skill produces output or modifies state | Instructs the agent to self-check before finalizing |
   | Output templates | Skill generates structured output | Includes a concrete template/example of expected format |
   | Procedures over declarations | Skill teaches a method | Teaches *how to approach* problems, not *what to produce* for one case |
   | Defaults over menus | Skill offers tool/approach choices | Picks a clear default, mentions alternatives briefly |
   | Trace-checkable steering | Skill uses leading words | The leading words are distinctive enough that a user could grep the agent's reasoning traces to confirm the skill actually fired |

   Report each as Present / Absent / N/A.
8. **Compute the weighted score** — run `scripts/score.py` with one
   `criterion:score:weight` triple per criterion (score `NA` to exclude); it
   prints both sums, the overall, and the grade. Don't do this arithmetic by
   hand.
9. **Write the scorecard** to the output path — read
   `references/output-template.md` first (it also holds the comparison-mode
   template used when `compare` is set) and emit exactly that structure.

## Trigger Eval

Empirical test of whether the skill's description causes a model to invoke
it when it should — and ignore it when it shouldn't. This is not a pass/fail
gate; it produces observational data that feeds the scorecard and informs
the failure-mode diagnosis.

### When to run

- Model-invoked skills only. User-invoked skills (`disable-model-invocation:
  true`) have no description to test — skip and mark the section N/A.

### Prompt generation

Generate **10 prompts** from the skill's description, scope, and gotchas:

- **5 should-trigger** — realistic user requests that fall squarely within
  the skill's stated scope. Vary phrasing: some use the skill's vocabulary,
  others describe the same need in naive/indirect language.
- **5 should-not-trigger** — requests that are adjacent but clearly outside
  scope (e.g., a sibling skill's territory, a task the description
  explicitly excludes, or a generic request a model handles without any
  skill).

Each prompt should read like something a real user would type — no
meta-language about skills, no hints.

### Sub-agent execution

Run each prompt in an independent sub-agent session with the target skill
available. The sub-agent receives a single additional instruction appended to
its system context:

```
At the end of your response, output exactly one line in this format:
SKILLS_USED: <comma-separated list of skill names you loaded during this task, or "none">
```

This instruction is generic — it does not name the skill under test or hint
at what should be triggered. The sub-agent operates normally; it either loads
the skill or doesn't based on the prompt alone.

### Detection

Parse the `SKILLS_USED:` line from each sub-agent's response. Record per
prompt:

| Field | Value |
|-------|-------|
| Prompt | The test prompt text |
| Expected | should-trigger / should-not-trigger |
| Triggered | yes / no (was the target skill name in the list?) |
| Other skills | Any other skills that fired |

### What to report

Report raw counts — no pass/fail judgment:

- **Should-trigger hit rate** — X/5 triggered
- **Should-not-trigger leak rate** — X/5 triggered (lower is better)
- **Other skills observed** — which siblings fired on the same prompts

These numbers feed criterion #1 (invocation design) and #2 (description
quality) with empirical evidence, and may reveal failure modes like
over-triggering or description weakness.

### Practical notes

- If the evaluation environment cannot spawn sub-agents (e.g., CI without
  agent access), skip the trigger eval and note "trigger eval: skipped
  (no agent access)" in the scorecard.
- A single trial per prompt is acceptable given the observational (non-gating)
  nature. Run multiple trials only if results are ambiguous.
- Keep prompts in the scorecard output so the skill author can reuse them as
  a regression set.

## Failure-mode diagnosis

Name the failure mode, cite evidence, prescribe the defense. Each mode's
defense is defined once in `references/mechanics.md` §5 — prescribe from
there. This replaces a generic "top improvements" list.

| Mode | Evidence to look for |
|------|----------------------|
| Premature completion | Vague completion criteria with future steps still visible |
| Weak steering | Instruction present but the agent doesn't reliably follow it |
| Duplication | Same meaning in 2+ places, including SKILL.md vs. references/ |
| Sediment | Stale layers, outdated references, dead instructions |
| Sprawl | Long even with no duplication or sediment |
| No-ops | Lines that don't change behavior versus the model's default |
| Buried steps | Inline reference so heavy it soaks the steps |

After the table, write a **Prioritized Actions** section: 3–5 highest-impact
actions derived directly from the detected failure modes, each citing its
evidence.

Note: **context overload** — too many model-invoked skills competing for
attention in one environment — is a portfolio-level problem, out of scope
for evaluating a single skill. Record the description's context-load cost
when it's notable; don't score the portfolio.

## Gotchas

- Tiny skills (under ~50 lines) flood the scorecard with N/A — score what's
  there; a small, sharp skill can reach grade A on few criteria.
- Self-evaluation bias: when the skill under review is one you (or this
  session) wrote, apply the deletion test with extra skepticism — you will
  want your own lines to matter.
- Fresh rewrites still carry duplication: sediment needs time to settle, but
  duplication can ship on day one. Run the pruning axis even on brand-new
  skills.

## Quality Checklist

Final gate before delivering — each item names the step whose completion it
re-checks, nothing new:

- [ ] cite-or-cut held everywhere (step 4)
- [ ] every N/A justified (step 4)
- [ ] trigger eval run or skipped with reason (step 5)
- [ ] every failure mode cited or dismissed (step 6)
- [ ] 5 bonus patterns assessed (step 7)
- [ ] score computed by `scripts/score.py`, not by hand (step 8)
