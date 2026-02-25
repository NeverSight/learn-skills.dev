---
name: hegelian-review
description: Runs a two-pass adversarial review (critic + steelman defender) to produce calibrated verdicts distinguishing genuine issues from false alarms — use when reviewing specs, code, designs, architecture, or documents where a single critical pass would over-index on problems
tags:
  - critical-thinking
  - code-review
  - architecture-review
  - adversarial-review
---

# Hegelian Dialectical Review

Two-pass adversarial review: find problems (antithesis), then challenge those findings (synthesis). The calibrated verdict table is the deliverable — not either pass alone.

## Why Two Passes

A single adversarial review finds issues because that's its job, even when the original decision was sound. The second pass defends the artifact against the first pass's criticisms, producing verdicts that separate genuine issues from false alarms.

## Quick Reference

| Step | Agent | Job | Output |
|------|-------|-----|--------|
| 1 | — | Read the artifact fully | Understanding of scope |
| 2 | Adversarial Critic | Find problems, not praise | Categorized issues list |
| 3 | Steelman Defender | Push back where review is wrong | Per-issue verdicts |
| 4 | — | Combine into verdict table + prose summary | Final calibrated assessment |

## Process

### 1. Read the Artifact

Read everything being reviewed. Accept file paths, sets of files, or inline content.

### 2. Antithesis — Adversarial Review

Launch an independent agent as an adversarial critic. On platforms without subagent support, run each pass as a separate prompt with its own context. Instruct it to:

- Number each finding sequentially (1, 2, 3...)
- Find problems, not praise strengths
- Organize findings into categories matched to the artifact type (see table below)
- Be specific — reference file paths and line numbers
- Skip anything that's fine

If the adversarial pass finds no issues, skip the steelman pass and report "no significant issues found."

Adapt categories to the artifact:

| Artifact | Categories |
|----------|-----------|
| Spec/Design | Contradictions, underspecified behavior, YAGNI, complexity, API design |
| Code | Bugs, security, performance, maintainability, naming |
| Architecture | Coupling, scalability, single points of failure, operational cost |
| Document | Clarity, completeness, internal consistency, audience fit |
| Config/Infra | Security, drift risk, reproducibility, cost |

### 3. Synthesis — Steelman Defense

Launch a second independent agent. Provide it the artifact AND the full adversarial review. Instruct it to:

- Defend the artifact where the review is wrong or overstated
- Agree briefly with valid criticisms and move on
- For each issue, give a verdict: **Valid**, **Overstated**, or **Wrong** with justification

**Critical:** Run agents independently to avoid anchoring. The steelman must evaluate the artifact on its own merits, not be influenced by having generated the adversarial review in the same context. In single-context environments, complete the adversarial pass fully before beginning the steelman, and consciously evaluate each finding against the artifact rather than your own prior reasoning.

### 4. Present the Verdict Table

Combine both passes:

```
| # | Issue | Verdict | Notes |
|---|-------|---------|-------|
| 1 | [description] | Valid | [what to fix] |
| 2 | [description] | Overstated | [why not as bad as claimed] |
| 3 | [description] | Wrong | [why original is correct] |
```

The full output is:

- **Verdict table** — every finding from Step 2, each with a verdict
- **Prose summary** covering:
  - Counts by verdict (how many Valid / Overstated / Wrong)
  - Genuine issues that need fixing (Valid verdicts only)
  - Patterns in what the review got wrong (e.g., "repeatedly treated deliberate scope boundaries as defects")
  - Recommended next steps

The raw adversarial review and steelman defense are working artifacts — include them only if the consumer needs the full reasoning.

## Common Mistakes

- **Presenting the adversarial review as the output.** The verdict table is the deliverable. Neither pass alone is the answer.
- **Rubber-stamping all findings as Valid.** The steelman's job is to push back hard. If everything is Valid, the steelman isn't doing its job.
- **Anchoring the steelman on the adversarial context.** If both passes share a context, the steelman is biased by having generated the criticism. Use separate agents or separate prompts.
- **Binary verdicts only.** "Overstated" is where the most useful calibration happens — a real concern at exaggerated severity.

## Key Principles

- **Verdicts are ternary.** Valid / Overstated / Wrong. The middle ground is where calibration lives.
- **The steelman is not a rubber stamp.** It should spend effort on points where the review is genuinely wrong, not politely agree with everything.
- **The final synthesis is the deliverable.** Neither pass alone is the output.
