---
name: lint-fix
description: Run ESLint with --fix across the repo (or a scope), capture errors that could not be auto-fixed, group them by rule, store results in the KB, and scan for eslint-disable suppressions (which are covered-up errors, not fixes). Use this skill instead of running pnpm lint directly.
---

# /lint-fix — Lint, Fix, and Capture

## Who Should Call This

**Dev agents only** — specifically:
- `dev-implement-story` (via its verification phase)
- `dev-fix-story` (via its fix and verification phases)
- `dev-code-review` (via `code-review-lint.agent.md`)

**Never call `pnpm lint`, `pnpm eslint`, or `pnpm turbo run lint` directly.** Always go through `/lint-fix` so fixes are attempted, results are captured in the KB, and suppressions are tracked as debt.

## Gate Behavior (CRITICAL)

After auto-fix and manual fix attempts, if **any errors remain**:

```
VERDICT: FAIL
```

- **In code review context**: the story receives a `LINT FAIL` verdict. The orchestrator (`dev-code-review`) MUST move the story to `failed-code-review` and invoke `/dev-fix-story`. The dev agent MUST properly fix the root cause — `eslint-disable` suppressions are NOT an acceptable fix.
- **In implementation context**: the agent MUST fix all errors before committing. Do not suppress with `eslint-disable` unless a config-update candidate has been identified and documented in the KB.

**`eslint-disable` comments added during a story = automatic FAIL in code review.**
The suppression inventory (Phase 4) is diffed against the previous run to detect new suppressions introduced by the current story.

## Description

Runs ESLint with auto-fix across the monorepo, then:
1. Captures every error that could **not** be resolved automatically, grouped by rule
2. Scans the codebase for `eslint-disable` comments — these are **suppressed violations, not fixes** — and tracks them as technical debt in the KB
3. Stores the run summary, config candidates, and suppression inventory in the knowledge base for trend analysis

## Usage

```bash
# Full repo (most common)
/lint-fix

# Single package
/lint-fix --scope=@repo/gallery

# Multiple packages
/lint-fix --scope=@repo/gallery,@repo/api-client

# Audit only — no auto-fix, no KB writes, just show what would fail
/lint-fix --dry-run
```

## Parameters

- **--scope** - Comma-separated package names. Omit for full repo.
- **--dry-run** - Skip `--fix` and skip all KB writes. Terminal output only.

---

## EXECUTION INSTRUCTIONS

### Phase 1: Build the lint command

```
IF --scope provided:
  filters = "--filter=@repo/pkg1 --filter=@repo/pkg2"
  cmd = "pnpm turbo run lint --force --continue {filters} 2>&1"
ELSE:
  cmd = "pnpm turbo run lint --force --continue 2>&1"
```

### Phase 2: Run the linter and capture output

Run via Bash. Capture the full output.

Key output signals:
```
ERROR LINE:    "@repo/pkg:lint:   15:3  error  <message>  <rule-name>"
WARNING LINE:  "@repo/pkg:lint:   15:3  warning  <message>  <rule-name>"
SUCCESS:       " Tasks:    N successful, N total"
FAILED PKGS:   " Failed:    @repo/pkg1#lint, @repo/pkg2#lint"
```

**Rule name** = the final whitespace-delimited token on each error/warning line.

### Phase 3: Parse and group errors

Build two maps:

**By rule** (sorted descending by count):
```
rule_name → { count, severity, files: [up to 5 paths with line numbers] }
```

**By package** (sorted descending by error count):
```
package_name → { errors, warnings }
```

Also extract: total packages run, packages succeeded, packages failed (names), total errors, total warnings.

### Phase 4: Scan for eslint-disable suppressions

Suppressions are **errors that were silenced, not fixed**. They are technical debt.

```bash
# Find all suppression comments in source files
grep -rn "eslint-disable" . \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  | grep -v node_modules | grep -v "/dist/" | grep -v "/.turbo/" | grep -v "/tree/"
```

For each match, extract:
- `file` — relative path
- `line` — line number
- `type` — `file-level` (`/* eslint-disable ... */` at top), `next-line` (`// eslint-disable-next-line ...`), or `inline` (`// eslint-disable-line ...`)
- `rules` — the specific rules being suppressed (or `[all]` if no rule listed)
- `comment` — any explanatory text after the rule names

Group suppressions by rule name for reporting.

### Phase 5: Identify config update candidates

Apply this decision table to the by-rule error map.
**Threshold for reporting**: any rule with ≥ 3 unfixed occurrences.

| Condition | Candidate type | Suggested action |
|-----------|---------------|-----------------|
| `@typescript-eslint/no-unused-vars` fires AND variable names start with `_` | False positive | Confirm `varsIgnorePattern: '^_'` is set |
| `no-console` fires in `apps/api/**` or `scripts/**` | Wrong scope | Verify backend override has `'no-console': 'off'` |
| `import/order` fires ≥ 5× in same file | Structural pattern | File uses mid-file imports by design — add `/* eslint-disable import/order */` at file top |
| `import/no-duplicates` fires ≥ 3× in same file | Structural pattern | Consolidate imports from the same module |
| `prettier/prettier` fires ≥ 5× in a package | Missing --fix | Add `--fix` to that package's lint script |
| Any rule fires ≥ 10× across ≥ 3 packages | Global pattern | Consider a rule config change in root `eslint.config.js` |
| Any rule fires ≥ 3× in test/script/config files | Wrong scope | Add a file-glob override block in `eslint.config.js` |
| `no-constant-condition` in loop bodies | False positive | Add `{ checkLoops: false }` in backend rule config |
| `jsx-a11y/*` on same element pattern ≥ 3× | Presentational | Element needs `role="presentation"` + keyboard handler |

### Phase 6: Attempt manual fixes for remaining errors

For errors NOT identified as config-update candidates, attempt minimal fixes:

- `no-unused-vars` — prefix with `_` or remove if clearly dead code
- `no-console` in frontend — replace with `logger.info/warn/error` (add `@repo/logger` import if missing)
- `no-case-declarations` — wrap case body in `{ }` braces
- `no-useless-escape` — remove the unnecessary backslash
- `jsx-a11y/click-events-have-key-events` — add `onKeyDown` matching the `onClick`
- `jsx-a11y/no-static-element-interactions` — add `role="presentation"` if element is decorative

If a fix is unclear or risky, **skip and note it** rather than guessing.

After manual fixes, re-run affected packages to confirm they pass:
```bash
pnpm turbo run lint --force --continue --filter=@repo/affected-pkg 2>&1
```

### Phase 7: Persist to KB (skip if --dry-run)

Three writes to the KB — all via `mcp__knowledge-base__kb_add` or `mcp__knowledge-base__kb_update`.

---

#### 7a: Lint run summary

Search for an existing run note from today:
```
mcp__knowledge-base__kb_search({
  query: "lint run {YYYY-MM-DD}",
  tags: ["lint-run"],
  limit: 1
})
```

If none found, create a new entry. If found, skip (one run note per day is sufficient unless scope changes).

**`kb_add` payload** (`entry_type: 'note'`, `role: 'dev'`):
```
tags: ["lint-run", "eslint", "{YYYY-MM-DD}", "{PASS|FAIL}"]

content:
# Lint Run — {YYYY-MM-DD}

**Result:** PASS | FAIL
**Scope:** full-repo | {package list}
**Packages:** {N passed} / {N total}  ({N} failed)
**Errors:** {N}   **Warnings:** {N}
**Suppressions (eslint-disable):** {N total in codebase}  ({N new since last run if known})
**Config candidates identified:** {N}

## Errors by Rule

| Rule | Count | Example Files |
|------|-------|---------------|
| `rule-name` | N | file:line, file:line |

## Packages with Errors

| Package | Errors | Warnings |
|---------|--------|----------|
| @repo/pkg | N | N |

## Manual Fixes Applied

{bulleted list or "None"}

## Still Failing

{bulleted list or "None — all errors resolved."}
```

---

#### 7b: Config update candidates

For each candidate identified in Phase 5:

First, search for an existing constraint entry for this rule:
```
mcp__knowledge-base__kb_search({
  query: "ESLint config candidate {rule-name}",
  tags: ["eslint-config-candidate"],
  entry_type: "constraint",
  limit: 1
})
```

**If found**: call `kb_update` to increment the occurrence count and update `last_seen` in the content.

**If not found**: call `kb_add`:
```
entry_type: "constraint"
role: "dev"
tags: ["lint", "eslint-config-candidate", "eslint", "{rule-name}"]

content:
# ESLint Config Candidate: {rule-name}

**First seen:** {YYYY-MM-DD}
**Last seen:** {YYYY-MM-DD}
**Total occurrences:** {N}
**Runs where this appeared:** 1

## Why This Is a Candidate

{description from the decision table — e.g. "Fires 8× across 4 packages, suggesting a global config change"}

## Suggested Change

{concrete code snippet — e.g.:}
\`\`\`js
// eslint.config.js
'@typescript-eslint/no-unused-vars': ['error', {
  varsIgnorePattern: '^_',
  argsIgnorePattern: '^_',
}]
\`\`\`

## Affected Files (most recent run)

{file:line list}

## Status

open — not yet addressed
```

When a candidate is eventually resolved (config updated), update the entry's content to mark it `resolved` and describe the fix applied.

---

#### 7c: Suppression inventory

Suppressions are hidden errors. Track them as a single living inventory note.

Search for the existing suppression inventory:
```
mcp__knowledge-base__kb_search({
  query: "eslint-disable suppression inventory",
  tags: ["eslint-disable-inventory"],
  limit: 1
})
```

**If found**: call `kb_update` with refreshed content.
**If not found**: call `kb_add`.

```
entry_type: "note"
role: "dev"
tags: ["lint", "eslint-disable-inventory", "technical-debt", "eslint"]

content:
# ESLint Suppression Inventory

Last updated: {YYYY-MM-DD}
Total suppressions: {N}

> These are lint violations that have been silenced with eslint-disable comments.
> They are NOT fixes — they are deferred errors. Each one represents real technical
> debt. The goal is to drive this number toward zero by fixing root causes and
> updating ESLint config to eliminate false positives.

## Suppressions by Rule

| Rule | Count | Type | Notes |
|------|-------|------|-------|
| `rule-name` | N | file-level / next-line / inline | any comment text |

## All Suppressions

### `{rule-name}` ({N} suppressions)

| File | Line | Type | Comment |
|------|------|------|---------|
| path/to/file.ts | 42 | next-line | intentional: mid-file import pattern |
| path/to/other.ts | 1 | file-level | WIP: upload page not yet wired up |

### `{rule-name-2}` ...

## Trend

{If previous inventory exists, compare counts:}
- `rule-name`: {N} → {N} ({+N | -N | no change})
- Net: {+N | -N} suppressions since last run

## How to Reduce Suppressions

For each rule appearing here:
1. If it's a false positive → update `eslint.config.js` rule config (see Config Candidates)
2. If it's a real error being hidden → fix the underlying code and remove the disable comment
3. If it's a structural pattern (e.g. mid-file imports) → add a targeted file-level disable
   with a clear comment explaining WHY
```

---

### Phase 8: Terminal output

Always print to terminal regardless of --dry-run.

```
═══════════════════════════════════════════════════════
  /lint-fix — {date}
═══════════════════════════════════════════════════════

Result: {PASS | FAIL}
Packages: {N passed} / {N total}  ({N} failed)
Errors:   {N}   Warnings: {N}

{If PASS:}
✓ All packages lint clean.

{If errors remain:}
── Errors by Rule ──────────────────────────────────────
  {count}×  {rule-name}
             {file:line, file:line, ...}

── Packages with Errors ────────────────────────────────
  @repo/pkg1    {E} errors  {W} warnings

── Config Update Candidates ────────────────────────────
  {rule-name} — {count}×
    → {one-line suggestion}
    KB: {entry_type} written/updated

  {or "None"}

── Suppressions (eslint-disable) ───────────────────────
  Total in codebase: {N}
  By rule:
    {count}×  {rule-name}  ({file-level|next-line|inline})
  KB: suppression inventory updated

── Manual Fixes Applied ────────────────────────────────
  {file — what changed}
  {or "None"}

── Still Failing ───────────────────────────────────────
  {file:line  rule-name  (reason not fixed)}
  {or "None — all errors resolved."}

── New Suppressions Introduced (vs previous run) ───────
  {file:line  rule-name  (eslint-disable added this story)}
  {or "None"}

── KB Writes ───────────────────────────────────────────
  ✓ Lint run summary stored
  ✓ {N} config candidate(s) written/updated
  ✓ Suppression inventory updated ({N} total suppressions)

── GATE VERDICT ────────────────────────────────────────
  {If no errors and no new suppressions:}
  ✅ LINT PASS — story may proceed

  {If any errors remain OR new eslint-disable added:}
  ❌ LINT FAIL — story must return to /dev-fix-story
     Reason: {N errors remaining | N new suppressions added}
     eslint-disable is NOT an acceptable fix. Fix the root cause.

═══════════════════════════════════════════════════════
```

---

## KB Entry Reference

| What | `entry_type` | Tags | When created |
|------|-------------|------|-------------|
| Run summary | `note` | `lint-run`, `eslint`, `YYYY-MM-DD` | Every run (once per day) |
| Config candidate | `constraint` | `lint`, `eslint-config-candidate`, `{rule-name}` | When rule hits ≥3 occurrences |
| Suppression inventory | `note` | `lint`, `eslint-disable-inventory`, `technical-debt` | First run; updated each run |

## Integration Notes

- All workflow skills (`/dev-implement-story`, `/dev-fix-story`, `/qa-verify-story`) should call `/lint-fix` rather than `pnpm lint` directly.
- Config candidates accumulate in the KB over time. When the same candidate appears in 3+ runs, that is a strong signal to update `eslint.config.js` permanently — search the KB for `tags: ["eslint-config-candidate"]` to review open candidates.
- The suppression inventory is the single source of truth for technical debt hidden by `eslint-disable`. Review it before adding new suppressions.

## Config files to update when acting on candidates

| File | What to change |
|------|---------------|
| `eslint.config.js` | Rule configs, ignore patterns, file-glob overrides |
| `packages/*/package.json` | Add `--fix` to lint script |
| `CLAUDE.md` Common Pitfalls | Document new conventions |
