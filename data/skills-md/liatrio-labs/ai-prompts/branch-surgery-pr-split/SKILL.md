---
name: branch-surgery-pr-split
description: Split oversized or mixed-concern branches into smaller, reviewable PR stacks with safety refs, topology selection, parity audits, and merge sequencing. Use when a PR or branch is too large, difficult to review, mixed across concerns, conflict-prone, or needs to be decomposed without losing net changes.
---

# Branch Surgery PR Split

## Overview

Use this skill to turn a risky monolithic branch into a safe, auditable set of scoped PRs.
Treat topology as a decision, not a default recipe, and collaborate with the user before executing branch surgery.

## Workflow

1. Quantify branch shape before proposing solutions.
2. Always present the top two topology options with explicit tradeoffs.
3. Collaborate with the user to select one topology.
4. Produce a decision-complete split plan.
5. Execute with safety refs and strict scope boundaries.
6. Run parity and completeness audits.
7. Remediate drift and generate PR metadata.

## Step 1: Quantify Branch Shape

Collect objective signals first:

- Commit count and net churn versus base.
- Number of changed files and hotspot files.
- Mixed-commit prevalence (single commit touching unrelated concerns).
- Dependency density between concerns.
- Expected review risk and conflict risk.

If signals are incomplete, gather more evidence before recommending topology.

## Step 2: Generate Topology Options

Always provide the top two options with tradeoffs and a recommendation.
Use `references/topology-patterns.md` to select options.

For each option, include:

- Topology name.
- Why it fits this branch shape.
- Review ergonomics, merge complexity, and conflict risk.
- Failure modes and mitigations.
- Cost of execution (low/medium/high).

Do not skip tradeoffs.

## Step 3: Collaborate on Topology Selection

Use targeted discovery questions from `references/facilitated-discovery-questions.md`.
Confirm constraints before surgery:

- Must-merge-first dependencies.
- Parallel review goals.
- Tolerance for stacked PR depth.
- Documentation isolation preference.
- Release timing constraints.

If the user is unsure, recommend one option and explain what would change with the second option.

## Step 4: Produce a Decision-Complete Split Plan

Produce:

- Branch inventory with base branch mapping.
- Commit disposition map (keep, split, drop-as-superseded).
- Execution order.
- Merge order.
- Validation gates.
- Risk register and mitigations.

Use templates in `references/pr-stack-templates.md`.

## Step 5: Execute Branch Surgery Safely

Execution rules:

- Create backup refs first (tag and/or backup branch).
- Preserve explicit scope contracts per split branch.
- For mixed commits, use `cherry-pick -n` and stage only owned files/hunks.
- Keep shared-doc churn isolated when selected topology calls for it.
- Avoid hidden carryover changes by checking staged file lists before commit.

## Step 6: Audit Before Confidence

Run audit gates from `references/audit-gates.md`.
A split is incomplete until all gates pass or deviations are documented.

Mandatory checks:

- No missing files compared to original net diff.
- No unexpected extra files.
- Per-file parity or intentional documented divergence.
- Deletion semantics parity.
- Branch scope boundaries match PR intent.

## Step 7: Remediate and Package PRs

If audit finds issues:

1. Fix scope drift or ownership errors.
2. Re-run audits.
3. Remove redundant branches.

Then generate PR metadata and merge sequencing notes using `references/pr-stack-templates.md`.

## Output Standard

Always provide:

1. Chosen topology and why it won over the runner-up.
2. Branch plan and merge order.
3. Audit summary with pass/fail status per gate.
4. Remediation actions taken.

## References

- `references/topology-patterns.md`
- `references/facilitated-discovery-questions.md`
- `references/audit-gates.md`
- `references/pr-stack-templates.md`
