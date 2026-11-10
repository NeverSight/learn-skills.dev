---
name: causal-design
description: "Design or audit the identification strategy for an observational study. Use when the task concerns estimands, causal assumptions, threats to identification, or defensible research design rather than model implementation."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Task
argument-hint: "[project-path or tex-file] [--mode design|audit]"
agent-dependencies: [domain-reviewer]
skill-dependencies: [data-analysis, experiment-design, proofread]
---

# Causal Design

> Design and audit identification strategies for observational causal inference.

## Output Path

Per `rules/review-artefact-routing.md` (auto-loads in research projects (path-scoped to `paper-*/` and `paper/`)):

- **Source slug:** `causal-design`
- **Write reports to:** `reviews/<scope>/causal-design/<YYYY-MM-DD-HHMM>.md` inside the project, where `<scope>` is the paper slug (e.g. `paper-philtech`) for paper-level audits or `_project` for project-level reviews. Path is relative to the research project root, not the Task-Management repo.
- **Never** at project root (`./CRITIC-REPORT.md`-style filenames are forbidden — pre-rule layout).
- **Idempotency:** if today's timestamp exists, append a same-day descriptor to the path base (`{date}-HHMM-revision.md`, `{date}-HHMM-r2.md`, `{date}-HHMM-pre-submission.md`) — never overwrite.
- **Index update:** if `reviews/INDEX.md` exists, write a one-line entry under "Latest per source" pointing at the new file. Otherwise `review-recap` will rebuild the index next time it runs.
- **Infrastructure repos** (Task-Management, atlas-workspace, etc.): this section does not apply — the path-scoped rule won't load there.


## Modes

| Mode | What it does | Entry point |
|------|-------------|-------------|
| **Design** | Interview-driven strategy selection and memo production | "Design my causal strategy" / "What identification can I use?" |
| **Audit** | 4-phase causal inference check on existing paper/scripts | "Check my identification" / "Audit my econometrics" |

Default: **Design**. If the user points to an existing paper or estimation script, auto-select Audit mode.

## When to Use

- Choosing an identification strategy for an observational study
- Stress-testing whether an existing strategy is credible
- Verifying that code implements the claimed identification design
- Mapping causal claims to their identifying assumptions

## When NOT to Use

- Experimental design (RCTs, surveys, factorial) -- use `experiment-design`
- Running the analysis or generating results -- use `data-analysis`
- Literature search or citation gathering -- use an installed literature workflow or scholarly search
- Proofreading or compiling the paper -- use `proofread`, `latex`

## Shared References

- Method probing questions: `shared/method-probing-questions.md` — ask before running any analysis (DiD, IV, RDD sections)
- Validation tiers: `shared/validation-tiers.md` — declare tier before designing strategy
- Escalation protocol: `shared/escalation-protocol.md` — escalate when identification is vague or unsound

---

## Mode: Design

### Phase 1: Interview

Before opening the interview, confirm the project's validation tier per [`shared/validation-tiers.md`](../shared/validation-tiers.md) — Exploratory designs warrant lighter identification stress-testing than Publication-ready ones. Use [`shared/method-probing-questions.md`](../shared/method-probing-questions.md) as the interview backbone; the prompts below adapt those probes to causal identification specifically.

Conduct a structured interview to understand the research setting. Ask these questions (adapt to what the user has already shared):

1. **Causal question:** What causal effect are you trying to estimate? What is the treatment? What is the outcome?
2. **Variation:** What source of variation in treatment do you exploit? Is it natural, policy-driven, institutional?
3. **Confounders:** What are the main threats to identification? What unobservables worry you?
4. **Data structure:** Panel, cross-section, or repeated cross-section? What units and time periods?
5. **Institutional context:** Any thresholds, cutoffs, rollout dates, or instruments available?
6. **Prior literature:** What identification strategies have others used for similar questions?

Do not proceed until the causal question and data structure are clear.

### Phase 2: Strategy Selection

Read `references/design-decision-tree.md` and walk through the decision tree with the user's answers:

- Match the research setting to the strongest available strategy
- If multiple strategies are viable, rank them by credibility and discuss trade-offs
- If the setting does not support any strong strategy, say so explicitly -- do not force a weak design

### Phase 3: Strategy Memo

Write a strategy memo using `references/strategy-memo-template.md`. Save to `docs/causal-strategy.md` (or project-appropriate location).

The memo must specify:

1. **Estimand** -- the exact causal parameter being estimated, in formal notation
2. **Identification strategy** -- how variation is generated and why it is exogenous
3. **Key assumptions** -- each one stated, with a defence or test plan
4. **Threats and mitigations** -- what could go wrong and how to address it
5. **Diagnostics plan** -- which tests to run before trusting the estimates
6. **Robustness checks** -- pre-committed alternative specifications
7. **Alternative strategies considered** -- why they were rejected

This memo is what `data-analysis` Phase 3 checks for before allowing estimation. It locks the research design per the `design-before-results` rule.

### Phase 4: Adversarial Review

The reviewer follows [`shared/escalation-protocol.md`](../shared/escalation-protocol.md) — when identification is vague or assumptions are hand-waved, the reviewer escalates rather than accommodating.

Delegate an adversarial review to the `domain-reviewer` agent. Read `references/causal-audit-prompt.md` and pass it as the prompt to the fresh-context sub-agent mechanism:

```
Launch the domain-reviewer agent with this prompt:
"You are reviewing a causal identification strategy memo. [Insert contents of causal-audit-prompt.md, customised with the specific strategy chosen]. The memo is at [path]. Focus exclusively on identification credibility."
```

The agent will produce a report at `reviews/<scope>/domain-reviewer/<YYYY-MM-DD-HHMM>.md` in the project, where `<scope>` is the paper slug or `_project`.

### Phase 5: Iterate

Present the domain-reviewer's findings to the user. For each issue flagged:

- Discuss whether it is a genuine threat or can be addressed
- Update the strategy memo if the design changes
- If the strategy is fundamentally flawed, return to Phase 2

---

## Mode: Audit

### Phase 1: Extract Claims

Read the paper (`.tex` files) and/or estimation scripts to extract every causal claim:

- What effects does the paper claim to estimate?
- What language is used? ("causal", "effect of", "impact of", "leads to")
- Are claims hedged appropriately or overstated?

Produce a numbered list of claims with their locations (file:line).

### Phase 2: Map Estimands to Identification

For each causal claim, determine:

| Claim | Estimand | Strategy | Key Assumption | Stated? | Defended? |
|-------|----------|----------|----------------|---------|-----------|
| ... | ... | ... | ... | Yes/No | Yes/No |

Flag any claim where:
- The estimand is undefined or vague
- The identification strategy is not stated
- Key assumptions are not listed or defended
- The strategy does not match the claim (e.g., claiming ATE but estimating LATE)

### Phase 3: Assumption Diagnostics

For each identification strategy found, check whether the required diagnostics are present and passing:

**DiD / Event Study:**
- Pre-treatment parallel trends test (visual + formal)
- Staggered treatment handling (TWFE bias check, Callaway-Sant'Anna or Sun-Abraham if staggered)
- Anticipation effects check
- Treatment effect heterogeneity assessment

**IV:**
- First-stage F-statistic reported (> 10 for Stock-Yogo, > 104.7 for modern thresholds)
- Exclusion restriction argument (quality of narrative)
- Monotonicity discussion
- Over-identification test (if multiple instruments)
- Reduced form reported

**RDD:**
- McCrary density test (no bunching at cutoff)
- Bandwidth sensitivity (MSE-optimal + alternatives)
- Covariate balance at the cutoff
- Donut hole specification
- Placebo cutoffs

**Synthetic Control:**
- Pre-treatment fit quality (RMSPE)
- Donor pool selection justification
- Placebo tests (in-space, in-time)
- Leave-one-out robustness

**Event Study:**
- Pre-event coefficients jointly zero
- Dynamic treatment effects plotted
- Clean control group definition
- Anticipation effects addressed

### Phase 4: Code-Design Alignment

If estimation code exists, verify it implements the claimed design:

- Does the regression specification match the paper's equations?
- Are standard errors computed correctly for the design? (clustered at the right level, heteroskedasticity-robust)
- Are the treatment and control groups defined as claimed?
- Are the diagnostics actually run, not just mentioned?
- Do robustness checks exist in code, or only in the text?

### Audit Report

Produce an audit report at `reviews/<scope>/causal-design/<YYYY-MM-DD-HHMM>.md` (where `<scope>` is the paper slug or `_project`) with:

```markdown
# Causal Audit Report

**Document:** [filename]
**Date:** YYYY-MM-DD
**Mode:** Audit

## Claims Inventory

[Numbered list of causal claims with locations]

## Estimand-Identification Map

[Table from Phase 2]

## Diagnostics Assessment

| Strategy | Diagnostic | Present? | Passing? | Notes |
|----------|-----------|----------|----------|-------|
| ... | ... | ... | ... | ... |

## Code-Design Alignment

[Phase 4 findings, or "N/A -- no code found"]

## Critical Issues

[List of issues that threaten identification credibility]

## Recommendations

[Ordered list of fixes, from most to least important]
```

---

## Cross-References

| Resource | When read |
|----------|-----------|
| `references/design-decision-tree.md` | Design Phase 2 (strategy selection) |
| `references/strategy-memo-template.md` | Design Phase 3 (memo output) |
| `references/causal-audit-prompt.md` | Design Phase 4 (agent delegation prompt) |
| `design-before-results` rule | Both modes enforce this |
| `domain-reviewer` agent | Design Phase 4 (adversarial review) |
| `data-analysis` skill | Consumes the strategy memo |
| `experiment-design` skill | For experimental (not observational) designs |
| `experiment-design/references/identification-strategies.md` | Quick-reference for strategies (shared knowledge) |
