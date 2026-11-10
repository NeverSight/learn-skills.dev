---
name: synthesise-reviews
description: "Deduplicate and reconcile multiple completed review reports into one prioritised revision plan with conflicts and dependencies made explicit. Use when parallel reviewers have returned findings that need a single action sequence. Not for running the reviews; use $review-cluster."
argument-hint: "[optional: path to reviews/ directory]"
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion
---

# Synthesise Reviews

> Combine multiple review reports into a single prioritised revision plan with cross-reviewer consensus ranking.

## Output Path

Per `rules/review-artefact-routing.md` (auto-loads in research projects (path-scoped to `paper-*/` and `paper/`)):

- **Source slug:** `synthesise-reviews`
- **Write reports to:** `reviews/<scope>/synthesise-reviews/YYYY-MM-DD-HHMM.md` inside the project, where `<scope>` is the paper slug (e.g. `paper-jtp`) or `_project` for project-level synthesis. Path is relative to the research project root, not the Task-Management repo.
- **Never** at project root (`./CRITIC-REPORT.md`-style filenames are forbidden — pre-rule layout).
- **Idempotency:** if today's file exists, append a same-day descriptor (`{date}-revision.md`, `{date}-r2.md`, `{date}-pre-submission.md`) — never overwrite.
- **Index update:** if `reviews/INDEX.md` exists, write a one-line entry under "Latest per source" pointing at the new file. Otherwise `review-recap` will rebuild the index next time it runs.
- **Infrastructure repos** (Task-Management, atlas-workspace, etc.): this section does not apply — the path-scoped rule won't load there.


## Purpose

After running parallel review agents (paper-critic, domain-reviewer, referee2-reviewer), this skill reads their internal reports, cross-references issues, and produces a unified synthesis grouped into workstreams by priority and theme. It decides the consolidated issue set; `strategic-revision --internal` is the separate step that turns a complex issue set into an executable DAG.

Inspired by APE Papers' `reviewer_response_plan_1.md` pattern — workstreams grouped by priority, each concern traced to its reviewer.

## When to Use

- After running 2+ review agents on a paper
- After a council review round
- When preparing a revision plan from multiple feedback sources
- Before an optional `strategic-revision --internal` handoff when the consolidated issues are interdependent

## When NOT to Use

- Before reviews exist — run the review agents first
- To run reviews — use the individual agents (`paper-critic`, `domain-reviewer`, `referee2-reviewer`)
- For a single review — just read the report directly
- For genuine venue referee reports or an R&R response — use `strategic-revision --external`

## Workflow

### Step 1: Discover Reports

Glob for review files in the project root. Scan the new canonical structure first, then fall back to legacy:

```
reviews/<scope>/<check>/YYYY-MM-DD*.md (canonical: e.g. reviews/paper-jtp/paper-critic/2026-06-28-1437.md)
reviews/<check>/YYYY-MM-DD*.md (legacy: e.g. reviews/paper-critic/2026-06-28-1437.md)
```

Where `<scope>` is a paper slug (e.g. `paper-jtp`) or `_project`.

If no reports found, ask the user where the reports are.

Present the discovered reports and their dates. If reports are from different dates, ask whether to synthesise all or just the most recent round.

### Step 2: Parse Issues

For each report, extract the issue list:

**From paper-critic CRITIC-REPORT.md:**
- Parse the Deductions table (columns: #, Issue, Tier, Deduction, Category, Location)
- Extract Critical (C*), Major (M*), Minor (m*) issue details from the detailed sections

**From domain-reviewer DOMAIN-REVIEW.md:**
- Parse each Lens section's issue table (columns: #, Issue, Severity, Location)
- Map: CRITICAL → Critical, MAJOR → Major, MINOR → Minor

**From referee2-reviewer REFEREE2-REPORT.md:**
- Parse the structured findings from each audit dimension
- Extract severity-tagged issues

### Step 2.5: Spot-verify findings against their cited location (integrity gate)

Per [`_shared/audit-integrity.md`](../_shared/audit-integrity.md) Rule 2, a review sub-agent's finding is not trusted until its evidence is confirmed — reviewers can emit plausible findings with a fabricated `path:line`. Before synthesising, **spot-verify a random sample** of the parsed issues (≥3, or 20% — whichever is larger, weighted toward Critical/Major):

1. For each sampled issue, open its cited `Location` (`path:line`) and confirm the quoted text/code is actually there and the issue follows from it.
2. **Any sample miss** (cited line doesn't exist, quote isn't there, or the claim doesn't follow) ⇒ that report is suspect: widen the check to all of that reviewer's findings and **drop** every one that can't be grounded.
3. Findings with **no `Location`/quotable anchor at all** are dropped, not synthesised — a finding you cannot point at is inadmissible.

Record a one-line `Integrity: N sampled, M dropped` note in the synthesis output. If reports lack locations entirely and nothing can be verified, say so rather than silently trusting them.

### Step 3: Cross-Reference and Consensus Escalation

Match issues across reports by semantic similarity (same underlying problem, possibly described differently):

| Consensus | Priority |
|-----------|----------|
| Flagged by 3/3 reviewers | **Critical** (regardless of individual severity) |
| Flagged by 2/3 reviewers | **Major** (or higher if any reviewer rated Critical) |
| Flagged by 1/3 reviewers | Keep original severity |

**Important:** Consensus can only escalate severity, never reduce it. If one reviewer says Critical and two say Minor, it stays Critical.

### Step 4: Group into Workstreams

Cluster issues by theme:

| Theme | What belongs here |
|-------|-------------------|
| **Identification & Methodology** | Research design, estimation strategy, assumptions, causal claims |
| **Mathematical Rigour** | Derivations, proofs, notation consistency, formal claims |
| **Empirical Analysis** | Data, results, robustness, replication |
| **Literature & Positioning** | Citations, positioning, literature gaps, framing |
| **Presentation & Structure** | Writing quality, organisation, clarity, flow |
| **Technical (LaTeX)** | Compilation, references, formatting, figures, tables |

Within each workstream, sort by priority (Critical → Major → Minor).

### Step 5: Output Synthesis Report

Write to `reviews/<scope>/synthesise-reviews/YYYY-MM-DD-HHMM.md` in the project, where `<scope>` is the paper slug (e.g. `paper-jtp`) or `_project` for project-level synthesis. This report contains the consolidated revision plan synthesised from all input reports.

```markdown
# Revision Plan

**Date:** YYYY-MM-DD
**Reports synthesised:** [list of report files with dates]
**Total issues:** N (C: X, M: Y, m: Z)

## Positive Consensus

Issues/strengths noted positively by multiple reviewers:

- [Strength 1] — noted by [reviewers]
- [Strength 2] — noted by [reviewers]

## Workstream 1: [Theme Name]

| # | Priority | Issue | Flagged by | Action | Source |
|---|----------|-------|------------|--------|--------|
| 1 | Critical | [description] | paper-critic (C1), domain-reviewer (A2), referee2 | [suggested action] | [file:line] |
| 2 | Major | [description] | paper-critic (M3), domain-reviewer (D1) | [suggested action] | [file:line] |
| 3 | Minor | [description] | paper-critic (m2) | [suggested action] | [file:line] |

## Workstream 2: [Theme Name]

[Same table format]

...

## Summary

| Workstream | Critical | Major | Minor | Total |
|------------|----------|-------|-------|-------|
| Identification & Methodology | X | Y | Z | N |
| Mathematical Rigour | X | Y | Z | N |
| ... | | | | |
| **Total** | **X** | **Y** | **Z** | **N** |

## Recommended Order

1. [First workstream to tackle and why]
2. [Second workstream]
3. ...

## Consensus Statistics

- Issues confirmed by all reviewers: N
- Issues confirmed by majority (2/3): N
- Issues from single reviewer: N
- Total unique issues: N
```

### Step 6: Optionally Hand Off to Internal Strategic Revision

If the synthesis contains multiple blocking or interdependent workstreams, offer `strategic-revision --internal <synthesis-path>`. That skill creates the executable task DAG and retains this synthesis as a source in its manifest. Do not invoke it when a ranked synthesis is sufficient.

Never generate a venue response letter from internal review material. Genuine referee comments and rebuttal scaffolds belong to `strategic-revision --external` and remain under the venue correspondence package.

## Anti-Patterns

- **Do NOT run reviews** — only synthesise existing reports
- **Do NOT modify source reports** — they are read-only inputs
- **Do NOT escalate severity beyond consensus rules** — if only one reviewer flagged something, keep their severity unless it's confirmed by others
- **Do NOT invent issues** — only report what the reviewers found
- **Do NOT merge issues that are genuinely different** — only merge when the same underlying problem is described differently
- **Do NOT produce venue correspondence or response letters** — this skill consolidates internal review evidence only
