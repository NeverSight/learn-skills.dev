---
name: review
description: >-
  Principle-grounded review of code changes, PRs, or plans. Use when asked to review, critique,
  or assess quality of work — "review", "review this", "code review", "check this".
---

# Review

Thorough review grounded in project principles. **Do NOT make changes — the review is the deliverable.**

**Use Tasks to track progress.** Create a task for each step below (TaskCreate), mark each in_progress when starting and completed when done (TaskUpdate). Check TaskList after each step.

## Step 1 — Load Principles

Read `brain/principles.md`. Follow every `[[wikilink]]` and read each linked principle file. These principles govern review judgments — refer back to them when evaluating issues.

**Do NOT skip this. Do NOT use memorized principle content — always read fresh.**

## Step 2 — Determine Scope

Infer what to review from context — the user's message, recent diffs, or referenced plans/PRs. If genuinely ambiguous (nothing to infer), ask.

Auto-detect review mode from change size:
- **BIG CHANGE** (50+ lines changed, 3+ files, or new architecture) — all sections, at most 4 top issues per section
- **SMALL CHANGE** (under those thresholds) — one issue per section

## Step 3 — Gather Context

For **SMALL CHANGE** reviews, read files directly in the main context — delegation overhead exceeds the cost of reading a few files.

For **BIG CHANGE** reviews, delegate exploration to subagents via the `Task` tool.

Spawn exploration agents (subagent_type: `Explore`) to:
- Read the code or plan under review
- Identify dependencies, callers, and downstream effects
- Map relevant types, tests, and infrastructure

Run multiple agents in parallel when investigating independent areas.

## Step 4 — Gather Domain Skills

Check installed skills (`.agents/skills/`, `.claude/skills/`) for any that match the review's domain.

**Invoke matched skills now** — read their output and use domain guidance to inform your review.

For domains not covered by installed skills, use `find-skills` to search for a relevant skill.

## Step 5 — Assessment Pipeline

Work through all sections in order. For each section, check against loaded principles.

### 1. Scope Check

If the review targets work against a plan phase:
- Read the plan phase that was assigned.
- Run `git diff --stat` and `git log --oneline` for the relevant commits.
- Flag files changed outside the plan phase's stated scope as scope violations.

If no plan phase applies, skip this subsection.

### 2. Architecture
- System design and component boundaries
- Dependency graph and coupling
- Data flow patterns and bottlenecks
- Security architecture (auth, data access, API boundaries)

### 3. Code Quality
- Code organization and module structure
- DRY violations — be aggressive
- Error handling patterns and missing edge cases (call out explicitly)
- Over-engineering or under-engineering relative to principles; consider redesign-from-first-principles
- Technical debt hotspots

### 4. Tests
- Coverage gaps (unit, integration, e2e)
- Test quality and assertion strength
- Missing edge case coverage — be thorough
- Untested failure modes and error paths
- New behavior must have new tests. Tests must assert outcomes, not implementation details.

### 5. Performance
- N+1 queries and database access patterns
- Memory-usage concerns
- Caching opportunities
- Slow or high-complexity code paths

### Principle Compliance

For each changed file, check against loaded principles. Common violations:
- Bolted-on changes instead of redesign (redesign-from-first-principles)
- Missing verification (prove-it-works)
- Unnecessarily added complexity (subtract-before-you-add)

## Step 6 — Issue Format

**NUMBER** each issue (1, 2, 3...). For every issue:

- Describe the problem concretely with file and line references
- Assign severity: **high** (blocks acceptance), **medium** (worth fixing, multiple may block), **low** (style/minor)
- Present 2–3 options with **LETTERS** (A, B, C), including "do nothing" where reasonable
- For each option: implementation effort, risk, impact on other code, maintenance burden
- Give a recommended option and why, mapped to principles
- Ask whether the user agrees or wants a different direction

### Severity Guide

- **high**: Incorrect behavior, missing tests for new behavior, scope violation on core files, principle violation that changes architecture.
- **medium**: Worth fixing but not blocking on its own. Multiple mediums may trigger rejection.
- **low**: Style, documentation, minor improvements. Note but don't block on these.

When using `AskUserQuestion`, label each option with issue NUMBER and option LETTER. Recommended option is always first.

## Step 7 — Verdict

After presenting all issues, give an overall verdict:

- **Accept**: All checks pass, scope clean, tests present and passing.
- **Accept with notes**: Low-severity issues only. List them for optional follow-up.
- **Revise**: High-severity issues found. Include specific actionable feedback — reference the exact file, line context, and principle violated.

## Interaction Rules

- Do not assume priorities on timeline or scale
- Do not make changes — present findings and wait for direction
- Present all sections together, then ask for feedback once at the end
- Per prove-it-works: if something can be tested, note how in the issue description
