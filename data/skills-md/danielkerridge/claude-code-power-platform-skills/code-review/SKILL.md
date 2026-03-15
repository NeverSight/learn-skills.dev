---
name: code-review
description: >
  Deep code audit that finds dead wiring, silent failures, unfinished features,
  placeholder stubs, bloated files, and unnecessary complexity. Produces an actionable
  report with file:line references grouped by severity. Think of it as a senior dev
  doing a thorough PR review of the entire codebase.
  Triggers on: "code review", "audit the code", "review the code", "find dead code",
  "find placeholders", "check for stubs", "prune the code", "code cleanup",
  "implementation review", "completeness check", "find unused code".
license: MIT
compatibility: "Claude Code"
metadata:
  author: custom
  version: "1.0.0"
  platform: "Any codebase (TypeScript, JavaScript, C#, PowerShell, Python)"
  requires: "File system access (Read, Grep, Glob)"
---

# Code Review — Deep Codebase Audit Skill

You perform a thorough, multi-pass audit of a codebase looking for real problems —
not style nits. You find the gaps that cause bugs in production: functions nobody calls,
errors nobody sees, features half-built, and code that should be deleted.

## CRITICAL RULES

1. **Every finding must include `file:line` references.** No vague "somewhere in the code" findings.
2. **Categorize by severity.** CRITICAL > WARNING > PRUNE > INFO. Read `resources/severity-guide.md`.
3. **Run ALL passes.** Don't skip passes because early ones found nothing. Read `resources/audit-passes.md`.
4. **Never suggest adding code without showing what to remove.** This is a pruning exercise, not a feature request.
5. **Focus on real bugs, not style.** Don't flag formatting, naming conventions, or missing comments
   unless they actively cause confusion or bugs.
6. **Provide the fix, not just the finding.** Each finding should say what to do about it.

## Audit Architecture

The review runs 7 passes over the codebase. Each pass looks for a different class of problem.
The passes are ordered from most critical (broken functionality) to least critical (cleanup opportunities).

```
Pass 1: WIRING          — Is everything connected end-to-end?
Pass 2: ERROR HANDLING   — Can failures be seen and debugged?
Pass 3: COMPLETENESS     — Are features fully implemented?
Pass 4: DEAD CODE        — What can be deleted right now?
Pass 5: BLOAT            — What's too big, too complex, or redundant?
Pass 6: HARDCODING       — What should be configurable but isn't?
Pass 7: SECURITY         — Any obvious vulnerabilities?
```

Read `resources/audit-passes.md` for the detailed checklist for each pass.

## Workflow

### Phase 1 — Scope the Review

Before auditing, understand the codebase:

1. **What's the project?** Read README, CLAUDE.md, package.json, etc.
2. **What's the tech stack?** Framework, language, build tools
3. **What's the architecture?** Entry points, services, stores, components
4. **What was recently changed?** If there's git history, focus on recent additions

Build a mental map of the codebase:
- Entry point → Router → Pages → Components → Stores → Services → External APIs
- Trace the full data flow from user action to persistence and back

### Phase 2 — Run the 7 Audit Passes

For each pass, use Grep and Glob to systematically search for the patterns
described in `resources/audit-passes.md`.

**Use parallel agents when the codebase is large.** Spawn agents for independent passes:
- Agent 1: Passes 1-2 (Wiring + Error Handling) — these are related
- Agent 2: Passes 3-4 (Completeness + Dead Code) — these are related
- Agent 3: Passes 5-7 (Bloat + Hardcoding + Security) — lighter passes

### Phase 3 — Cross-Reference

After individual passes, cross-reference findings:
- Does a "dead code" finding explain a "wiring" gap? (function exists but never called)
- Does a "completeness" gap overlap with a "placeholder" finding?
- Deduplicate — one root cause might show up in multiple passes

### Phase 4 — Compile the Report

Output format (read `resources/report-format.md`):

```markdown
# Code Review Report — [Project Name]
Date: [date]
Files Scanned: [count]
Findings: [count] (X critical, Y warning, Z prune, W info)

## CRITICAL — Must Fix
These cause broken functionality, data loss, or security holes.

### CR-001: [Title]
**File:** `src/stores/game-store.ts:108`
**Pass:** Wiring
**Problem:** `submitGameSession()` is defined in dataverse.ts but never called.
Game results are never persisted to Dataverse.
**Fix:** Call `submitGameSession()` from the `endGame()` action in game-store.ts.

## WARNING — Should Fix
These cause degraded experience, silent failures, or maintainability issues.

## PRUNE — Consider Removing
Dead code, redundant logic, bloated files. Removing these makes the codebase
leaner and easier to maintain.

## INFO — Minor Observations
Nice-to-know items that don't require action.
```

### Phase 5 — Pruning Recommendations

After the main audit, generate a pruning plan. Read `resources/pruning-guide.md`.

The pruning plan should:
1. List files/functions/types that can be **safely deleted**
2. List files that should be **split** (too many responsibilities)
3. List abstractions that should be **inlined** (used only once)
4. List dependencies that can be **removed** from package.json
5. Estimate the total lines of code that would be removed

## Without Agent Teams

If running as a single agent, execute passes sequentially.
Prioritize passes 1-3 (Wiring, Error Handling, Completeness) as these
find the most impactful issues. Passes 4-7 are still valuable but can
be deferred if time-constrained.
