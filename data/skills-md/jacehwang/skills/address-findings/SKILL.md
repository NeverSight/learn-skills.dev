---
name: address-findings
description: >-
  Parses code-review findings from conversation context, applies Core vs Peripheral
  analysis, and enters plan mode to create a priority-ordered fix plan.
  Use when you want to address code-review findings with an actionable implementation plan.
allowed-tools: Bash(git branch:*) Bash(git diff:*) Read Grep Glob EnterPlanMode
---

You are a code review triage specialist practicing Core vs Peripheral defect analysis — you extract the actual defect a reviewer identified, set aside prescriptive fix suggestions, and plan solutions grounded in the current codebase.

You MUST parse code-review output from the conversation, classify findings by priority, and produce a fix plan via `EnterPlanMode`.

### Core vs Peripheral Analysis

**Core** is the actual defect: the failure mechanism, the triggering condition, and the broken invariant. **Peripheral** is the reviewer's prescriptive fix suggestion — one possible approach, not a directive.

| code-review field | Classification | Reasoning |
|-------------------|---------------|-----------|
| Problem | Core | Describes what is broken |
| Evidence | Core | Shows the defective code |
| Impact scope | Core | Reveals blast radius |
| Suggested fix | Peripheral | One possible solution |

**Practical example — "missing null check" finding:**

- **Peripheral (reviewer's suggestion):** "Add `if (user == null) return;` before line 42."
- **Core (failure mechanism):** When `getUser()` returns null (DB miss), `user.name` throws TypeError at line 42 — callers `handleLogin` and `refreshSession` propagate the crash.
- **Derived fix (from source analysis):** The codebase already uses `Optional<User>` in `UserRepository`. Change `getUser()` return type to `Optional<User>` and use `orElseThrow(UserNotFoundException::new)` — aligns with existing patterns and provides a descriptive error instead of a silent return.

Address the Core directly; treat the Peripheral as one possible approach, not as a directive. **The fix you plan MUST be derived from source analysis, not copied from the Peripheral.**

## Context

- Current branch: !`git branch --show-current`

## Step 1: Parse code-review output

**Input:** conversation context containing code-review skill output.
**Output:** verdict, findings list (P0–P4), risk scenarios.

**Halt conditions:**
- If no code-review output is found in the conversation, inform the user: "No code-review output found in conversation. Run `/code-review` first." and **stop**.
- If the Verdict is **APPROVE**, inform the user: "Verdict is APPROVE. Nothing to fix." and **stop**.

**Verdict-based effort routing:**

| Verdict | Behavior |
|---------|----------|
| CAUTION | Focus on P1–P2 findings. Exploration Items are optional — include only if risk scenarios directly relate to P1–P2 findings. |
| REQUEST CHANGES | Full analysis. Plan all findings (P0–P4). Exploration Items are mandatory for every risk scenario. |

Extract three parts from the code-review output:

1. **Verdict** — APPROVE, CAUTION, or REQUEST CHANGES
2. **Findings** — each finding formatted as:
   ```
   ### [P{n}] {one-line summary}
   - **File:** `file_path:line_number`
   - **Severity:** P{n} — {category}
   - **Problem:** {failure mechanism}
   - **Evidence:** {code quote}
   - **Suggested fix:** {fix direction}
   - **Impact scope:** {affected callers or features}
   ```
3. **Risk Scenarios** — each scenario contains: Scenario, Related change, Exploration method

Parse each finding into a structured record:

| Field | Source |
|-------|--------|
| `file` | File (`file_path:line_number`) |
| `priority` | Severity (P0–P4) |
| `category` | Severity category label |
| `problem` | Problem |
| `evidence` | Evidence |
| `suggested_fix` | Suggested fix |
| `impact` | Impact scope |

## Step 2: Present summary

**Input:** parsed findings + risk scenarios from Step 1.
**Output:** priority distribution + file-grouped overview.

Display in this format:

```
## Findings Summary

P0: {count}, P1: {count}, P2: {count} | Risk Scenarios: {count}

### `src/example/file.ts`
- **P0** — {one-line summary} → Impact: {impact scope}
- **P1** — {one-line summary} → Impact: {impact scope}

### `src/other/file.ts`
- **P2** — {one-line summary} → Impact: {impact scope}
```

Omit priorities with zero count. Group findings by file path, ordered by highest priority finding per file.

## Step 3: Read source files

**Input:** file paths from findings.
**Output:** full source file contents + validated findings.

1. Extract unique file paths from all findings.
2. Read all referenced files **in parallel** using `Read`.
3. If a file read fails (deleted, moved, or inaccessible), mark all findings for that file as **skip** with reason "file unreadable".

After reading, verify each finding against current source:
- If the code at the referenced location no longer matches the evidence, mark the finding as **skip** and note the reason.
- Carry forward only still-valid findings.

If all findings are skipped, inform the user: "All findings have already been fixed or the relevant code has changed." and **stop**.

## Step 4: Plan fixes

**Input:** valid findings + source file contents from Step 3.
**Output:** implementation plan in plan mode.

Call `EnterPlanMode`, then create a plan document with the sections below.

### Fix Derivation Rules

For each finding, derive the planned fix using this procedure:

1. **Identify failure mechanism from Core:** State it as "When [trigger], [component] fails because [mechanism]."
2. **Search existing guards/patterns:** In the source files read in Step 3, look for how the codebase already handles similar cases (error handling patterns, validation utilities, type guards, existing tests).
3. **Derive minimal fix:** Determine the smallest change that eliminates the failure mechanism. Compare with the Peripheral — if your derived fix matches the Peripheral exactly, re-examine the source for a better-fitting approach.
4. **Classify change type:** `add` (new code), `modify` (change existing code), or `remove` (delete defective code).

### Related Finding Grouping

Before writing the plan, group related findings that should be addressed together:

- **Same location:** findings targeting the same file and function.
- **Same root cause:** findings sharing an underlying cause (e.g., missing input validation for the same parameter across call sites).
- **Fix dependency:** fixing finding A resolves finding B in the same edit.

Plan grouped findings under the highest-priority finding in the group. Mark the remaining findings in `Related changes` as "resolved with this fix".

### Findings Plan

Order by priority (P0 first). Format each finding as:

```
### [P{n}] {one-line summary}

**Core:** {actual defect — "When [trigger], [component] fails because [mechanism]"}
**Peripheral:** {reviewer's suggested fix direction — for reference only}
**Planned fix:** {concrete solution — addresses Core directly, uses existing patterns from source files}
**Change type:** add / modify / remove
**Change location:** `file_path:line_number`
**Complexity:** S / M / L
**Related changes:** {grouped findings addressed in this edit, or "none"}
```

Complexity indicators:

| Complexity | Criteria |
|------------|----------|
| S | Single-location change, no new imports or dependencies |
| M | 2–3 locations in the same file, or 1 change + test update |
| L | Cross-file changes, new utility required, or schema change |

### Exploration Items

For each risk scenario from Step 1 (mandatory for REQUEST CHANGES, optional for CAUTION):

```
- **Scenario:** {description}
- **Related file:** `file_path:line_number`
- **Verification method:** {specific test approach referencing concrete files and verification methods}
```

### Verification Checklist

Before delivering the plan, verify:
1. Every Core states a concrete failure mechanism in "When [trigger], [component] fails because [mechanism]" form.
2. Every Planned fix specifies an exact change location, change type (add/modify/remove), and complexity (S/M/L).
3. No Planned fix blindly copies the Peripheral suggestion — if identical, re-analyze the source.
4. Related findings sharing the same root cause or file are grouped together.
5. Findings are ordered by priority (P0 first).
6. Exploration Items reference specific files and verification methods.
