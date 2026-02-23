---
name: agent-teams-simplify-and-harden
description: "Implementation + audit loop using parallel agent teams with structured simplify, harden, and document passes. Spawns implementation agents to do the work, then audit agents to find complexity, security gaps, and spec deviations, then loops until code compiles cleanly, all tests pass, and auditors find zero issues or the loop cap is reached. Use when: implementing features from a spec or plan, hardening existing code, fixing a batch of issues, or any multi-file task that benefits from a build-verify-fix cycle."
---

# Agent Teams Simplify & Harden

## Install

```bash
npx skills add pskoett/pskoett-ai-skills/agent-teams-simplify-and-harden
```

A two-phase team loop that produces production-quality code: **implement**, then **audit using simplify + harden passes**, then **fix audit findings**, then **re-audit**, repeating until the codebase is solid or the loop cap is reached.

## When to Use

- Implementing multiple features from a spec or plan
- Hardening a codebase after a batch of changes
- Fixing a list of issues or gaps identified in a review
- Any task touching 5+ files where quality gates matter

## The Pattern

```
┌──────────────────────────────────────────────────────────┐
│                  TEAM LEAD (you)                          │
│                                                           │
│  Phase 1: IMPLEMENT (+ document pass on fix rounds)       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ impl-1   │ │ impl-2   │ │ impl-3   │  ...            │
│  │ (general │ │ (general │ │ (general │                 │
│  │ purpose) │ │ purpose) │ │ purpose) │                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│       │             │            │                        │
│       ▼             ▼            ▼                        │
│  ┌─────────────────────────────────────┐                 │
│  │  Verify: compile + tests            │                 │
│  └─────────────────────────────────────┘                 │
│       │                                                   │
│  Phase 2: SIMPLIFY & HARDEN AUDIT                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ simplify │ │ harden   │ │ spec     │  ...            │
│  │ auditor  │ │ auditor  │ │ auditor  │                 │
│  │ (Explore)│ │ (Explore)│ │ (Explore)│                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│       │             │            │                        │
│       ▼             ▼            ▼                        │
│  Exit conditions met?                                     │
│    YES → Produce summary. Ship it.                        │
│    NO  → back to Phase 1 with findings as tasks           │
│          (max 3 audit rounds)                             │
└──────────────────────────────────────────────────────────┘
```

## Loop Limits and Exit Conditions

The loop exits when ANY of these are true:

1. **Clean audit**: All auditors report zero findings
2. **Low-only round**: All findings in a round are severity `low` -- fix them inline (team lead or a single impl agent) and exit without re-auditing
3. **Loop cap reached**: 3 audit rounds have completed. After the third round, fix remaining critical/high findings inline and exit. Log any unresolved medium/low findings in the final summary.

**Budget guidance:** Track the cumulative diff growth across rounds. If fix rounds have added more than 30% on top of the original implementation diff, tighten the scope: skip medium/low simplify findings and focus only on harden patches and spec gaps.

## Step-by-Step Procedure

### 1. Create the Team

```
TeamCreate:
  team_name: "<project>-harden"
  description: "Implement and harden <description>"
```

### 2. Create Tasks

Break the work into discrete, parallelizable tasks. Each task should be independent enough for one agent to complete without blocking on others.

```
TaskCreate for each unit of work:
  subject: "Implement <specific thing>"
  description: "Detailed requirements, file paths, acceptance criteria"
  activeForm: "Implementing <thing>"
```

Set up dependencies if needed:
```
TaskUpdate: { taskId: "2", addBlockedBy: ["1"] }
```

### 3. Spawn Implementation Agents

Spawn `general-purpose` agents (they can read, write, and edit files). One per task or one per logical group. Run them **in parallel**.

```
Task tool (spawn teammate):
  subagent_type: general-purpose
  team_name: "<project>-harden"
  name: "impl-<area>"
  mode: bypassPermissions
  prompt: |
    You are an implementation agent on the <project>-harden team.
    Your name is impl-<area>.

    Check TaskList for your assigned tasks and complete them.
    After completing each task, mark it completed and check for more.

    Quality gates:
    - Code must compile cleanly (substitute your project's compile
      command, e.g. bunx tsc --noEmit, cargo build, go build ./...)
    - Tests must pass (substitute your project's test command,
      e.g. bun test, pytest, go test ./...)
    - Follow existing code patterns and conventions

    When all your tasks are done, notify the team lead.
```

### 4. Wait for Implementation to Complete

Monitor agent messages. When all implementation agents report done:

1. Run compile/type checks to verify clean build
2. Run tests to verify all pass
3. If either fails, fix or assign fixes before proceeding

Before spawning auditors, collect the list of files modified in this session:
```bash
git diff --name-only <base-branch>  # or: git diff --name-only HEAD~N
```
You will pass this file list to each auditor.

### 5. Spawn Audit Agents

Spawn `Explore` agents (read-only -- they cannot edit files, which prevents them from "fixing" issues silently). Each auditor covers a different concern using the Simplify & Harden methodology.

**Recommended audit dimensions:**

| Auditor | Focus | Mindset |
|---------|-------|---------|
| **simplify-auditor** | Code clarity and unnecessary complexity | "Is there a simpler way to express this?" |
| **harden-auditor** | Security and resilience gaps | "If someone malicious saw this, what would they try?" |
| **spec-auditor** | Implementation vs spec/plan completeness | "Does the code match what was asked for?" |

#### Simplify Auditor

```
Task tool (spawn teammate):
  subagent_type: Explore
  team_name: "<project>-harden"
  name: "simplify-auditor"
  prompt: |
    You are a simplify auditor on the <project>-harden team.
    Your name is simplify-auditor.

    Your job is to find unnecessary complexity -- NOT fix it. You are
    read-only.

    SCOPE: Only review the following files (modified in this session).
    Do NOT flag issues in other files, even if you notice them.
    Files to review:
    <paste file list here>

    Fresh-eyes start (mandatory): Before reporting findings, re-read all
    listed changed code with "fresh eyes" and actively look for obvious
    bugs, errors, confusing logic, brittle assumptions, naming issues,
    and missed hardening opportunities.

    Review each file and check for:

    1. Dead code and scaffolding -- debug logs, commented-out attempts,
       unused imports, temporary variables left from iteration
    2. Naming clarity -- function names, variables, and parameters that
       don't read clearly when seen fresh
    3. Control flow -- nested conditionals that could be flattened, early
       returns that could replace deep nesting, boolean expressions that
       could be simplified
    4. API surface -- public methods/functions that should be private,
       more exposure than necessary
    5. Over-abstraction -- classes, interfaces, or wrapper functions not
       justified by current scope. Agents tend to over-engineer.
    6. Consolidation -- logic spread across multiple functions/files that
       could live in one place

    For each finding, categorize as:
    - **Cosmetic** (dead code, unused imports, naming, control flow,
      visibility reduction) -- low risk, easy fix
    - **Refactor** (consolidation, restructuring, abstraction changes)
      -- only flag when genuinely necessary, not just "slightly better."
      The bar: would a senior engineer say the current state is clearly
      wrong, not just imperfect?

    For each finding report:
    1. File and line number
    2. Category (cosmetic or refactor)
    3. What's wrong
    4. What it should be (specific fix, not vague)
    5. Severity: high / medium / low

    If you notice issues outside the scoped files, list them separately
    under "Out-of-scope observations" at the end.

    Be thorough within scope. Check every listed file.
    When done, send your complete findings to the team lead.
    If you find ZERO in-scope issues, say so explicitly.
```

#### Harden Auditor

```
Task tool (spawn teammate):
  subagent_type: Explore
  team_name: "<project>-harden"
  name: "harden-auditor"
  prompt: |
    You are a security/harden auditor on the <project>-harden team.
    Your name is harden-auditor.

    Your job is to find security and resilience gaps -- NOT fix them.
    You are read-only.

    SCOPE: Only review the following files (modified in this session).
    Do NOT flag issues in other files, even if you notice them.
    Files to review:
    <paste file list here>

    Fresh-eyes start (mandatory): Before reporting findings, re-read all
    listed changed code with "fresh eyes" and actively look for obvious
    bugs, errors, confusing logic, brittle assumptions, naming issues,
    and missed hardening opportunities.

    Review each file and check for:

    1. Input validation -- unvalidated external inputs (user input, API
       params, file paths, env vars), type coercion issues, missing
       bounds checks, unconstrained string lengths
    2. Error handling -- non-specific catch blocks, errors logged without
       context, swallowed exceptions, sensitive data in error messages
    3. Injection vectors -- SQL injection, XSS, command injection, path
       traversal, template injection in string-building code
    4. Auth and authorization -- endpoints or functions missing auth,
       incorrect permission checks, privilege escalation risks
    5. Secrets and credentials -- hardcoded secrets, API keys, tokens,
       credentials in log output, unparameterized connection strings
    6. Data exposure -- internal state in error output, stack traces in
       responses, PII in logs, database schemas leaked
    7. Dependency risk -- new dependencies that are unmaintained, poorly
       versioned, or have known vulnerabilities
    8. Race conditions -- unsynchronized shared resources, TOCTOU
       vulnerabilities in concurrent code

    For each finding, categorize as:
    - **Patch** (adding validation, escaping output, removing a secret)
      -- straightforward fix
    - **Security refactor** (restructuring auth flow, replacing a
      vulnerable pattern) -- requires structural changes

    For each finding report:
    1. File and line number
    2. Category (patch or security refactor)
    3. What's wrong
    4. Severity: critical / high / medium / low
    5. Attack vector (if applicable)
    6. Specific fix recommendation

    If you notice issues outside the scoped files, list them separately
    under "Out-of-scope observations" at the end.

    Be thorough within scope. Check every listed file.
    When done, send your complete findings to the team lead.
    If you find ZERO in-scope issues, say so explicitly.
```

#### Spec Auditor

```
Task tool (spawn teammate):
  subagent_type: Explore
  team_name: "<project>-harden"
  name: "spec-auditor"
  prompt: |
    You are a spec auditor on the <project>-harden team.
    Your name is spec-auditor.

    Your job is to find gaps between implementation and spec/plan --
    NOT fix them. You are read-only.

    SCOPE: Only review the following files (modified in this session).
    Do NOT flag issues in other files, even if you notice them.
    Files to review:
    <paste file list here>

    Fresh-eyes start (mandatory): Before reporting findings, re-read all
    listed changed code with "fresh eyes" and actively look for obvious
    bugs, errors, confusing logic, brittle assumptions, and
    implementation/spec mismatches before running the spec checklist.

    Review each file against the spec/plan and check for:

    1. Missing features -- spec requirements that have no corresponding
       implementation
    2. Incorrect behavior -- logic that contradicts what the spec
       describes (wrong conditions, wrong outputs, wrong error handling)
    3. Incomplete implementation -- features that are partially built
       but missing edge cases, error paths, or configuration the spec
       requires
    4. Contract violations -- API shapes, response formats, status
       codes, or error messages that don't match the spec
    5. Test coverage -- untested code paths, missing edge case tests,
       assertions that don't verify enough, happy-path-only testing
    6. Acceptance criteria gaps -- spec conditions that aren't verified
       by any test

    For each finding, categorize as:
    - **Missing** -- feature or behavior not implemented at all
    - **Incorrect** -- implemented but wrong
    - **Incomplete** -- partially implemented, gaps remain
    - **Untested** -- implemented but no test coverage

    For each finding report:
    1. File and line number (or "N/A -- not implemented")
    2. Category (missing, incorrect, incomplete, untested)
    3. What the spec requires (quote or reference the spec)
    4. What the implementation does (or doesn't do)
    5. Severity: critical / high / medium / low

    If you notice issues outside the scoped files, list them separately
    under "Out-of-scope observations" at the end.

    Be thorough within scope. Cross-reference every spec requirement.
    When done, send your complete findings to the team lead.
    If you find ZERO in-scope issues, say so explicitly.
```

### 6. Process Audit Findings

Collect findings from all auditors. For each finding:

- **Critical/High**: Create a task and assign to an implementation agent
- **Medium**: Create a task, include in next implementation round
- **Low/Cosmetic**: Include in next round only if trivial to fix; otherwise note in the final summary and skip

**Refactor gate:** For findings categorized as **refactor** or **security refactor**, evaluate whether the refactor is genuinely necessary before creating a task. The bar: "Would a senior engineer say the current state is clearly wrong, not just imperfect?" Reject refactor proposals that are style preferences or marginal improvements.

**Exit check:** If all findings in this round are severity `low`, fix them inline and skip re-auditing (see Loop Limits).

When creating fix tasks, bundle a **document pass** into each implementation agent's work:

> After fixing your assigned issues, add up to 5 single-line comments
> across the files you touched on non-obvious decisions:
> - Logic that needs more than 5 seconds of "why does this exist?" thought
> - Workarounds or hacks, with context and a TODO for removal conditions
> - Performance choices and why the current approach was picked
>
> Do NOT comment on the audit fixes themselves -- only on decisions
> from the original implementation that lack explanation.

This keeps the document pass lightweight and scoped. Auditors in subsequent rounds should not flag these comments as findings.

### 7. Loop

If there are findings to fix:

1. Create tasks from findings (include document pass instructions)
2. Spawn implementation agents (or reuse idle ones via SendMessage)
3. Wait for fixes
4. Run compile + test verification
5. Check loop limits (see "Loop Limits and Exit Conditions")
6. If not exiting: spawn audit agents again (fresh agents, not reused -- clean context)
7. Repeat

### 8. Final Verification and Summary

When exit conditions are met:

1. Compile / type check -- must be clean
2. Tests -- must all pass
3. No `// TODO` or `// FIXME` comments introduced without corresponding tasks

Produce a final summary for the session:

```
## Hardening Summary

**Audit rounds completed:** 2 of 3 max
**Exit reason:** Clean audit (all auditors reported zero findings)

### Findings by round

Round 1:
- simplify-auditor: 4 cosmetic, 1 refactor (rejected -- style preference)
- harden-auditor: 2 patches, 1 security refactor (approved)
- spec-auditor: 1 missing feature

Round 2:
- simplify-auditor: 0 findings
- harden-auditor: 0 findings
- spec-auditor: 0 findings

### Actions taken
- Fixed: 6 findings (4 cosmetic, 2 patches, 1 security refactor, 1 missing feature -- rejected refactor excluded)
- Skipped: 1 refactor proposal (reason: style preference, not a defect)
- Document pass: 3 comments added across 2 files

### Unresolved
- None

### Out-of-scope observations
- <any out-of-scope items auditors flagged, for future reference>
```

Adapt the format to your context. The goal is a clear record of what was found, what was fixed, what was skipped and why, and what remains.

### 9. Cleanup

Send shutdown requests to all agents, then delete the team:

```
SendMessage type: shutdown_request to each agent
TeamDelete
```

## Agent Sizing Guide

| Codebase / Task Size | Impl Agents | Audit Agents |
|----------------------|-------------|--------------|
| Small (< 10 files) | 1-2 | 2 (simplify + harden) |
| Medium (10-30 files) | 2-3 | 2-3 |
| Large (30+ files) | 3-5 | 3 (simplify + harden + spec) |

More agents = more parallelism but more coordination overhead. For most tasks, 2-3 implementation agents and 2-3 auditors is the sweet spot.

## Tips

- **Implementation agents should be `general-purpose`** -- they need write access
- **Audit agents should be `Explore`** -- read-only prevents them from silently "fixing" things, which defeats the purpose of auditing
- **Fresh audit agents each round** -- don't reuse auditors from previous rounds; they carry context that biases them toward "already checked" areas
- **Task descriptions must be specific** -- include file paths, function names, exact behavior expected. Vague tasks produce vague implementations.
- **Run compile + tests between phases** -- don't spawn auditors on broken code; fix compilation/test errors first
- **Keep the loop tight** -- if auditors find only 1-2 low-severity cosmetic issues, fix them yourself instead of spawning a full implementation round
- **Assign tasks before spawning** -- set `owner` on tasks via TaskUpdate so agents know what to work on immediately
- **Simplify-first posture** -- when processing audit findings, prioritize cosmetic cleanups that reduce noise before tackling refactors. Cleanup is the default, refactoring is the exception
- **Security over style** -- when budget or time is constrained, prioritize harden findings over simplify findings
- **Pass the file list** -- always give auditors the explicit list of modified files. Don't rely on them figuring out scope on their own.

## Example: Implementing Spec Features

```
1.  Read spec, identify 8 features to implement
2.  TeamCreate: "feature-harden"
3.  TaskCreate x8 (one per feature)
4.  Spawn 3 impl agents, assign ~3 tasks each
5.  Wait → all done → compile clean → tests pass
6.  Collect modified file list (git diff --name-only)
7.  Spawn 3 auditors: simplify-auditor, harden-auditor, spec-auditor
8.  Simplify-auditor finds 4 cosmetic + 1 refactor proposal
9.  Harden-auditor finds 2 patches + 1 security refactor
10. Spec-auditor finds 1 missing feature
11. Team lead evaluates refactors (approve security refactor,
    reject simplify refactor), creates fix + document tasks
12. Spawn 2 impl agents for fixes
13. Wait → compile clean → tests pass
14. Round 2: Spawn 3 fresh auditors
15. Auditors find 0 issues → exit condition met
16. Produce hardening summary
17. Shutdown agents, TeamDelete
```

## Quality Gates (Non-Negotiable)

These must pass before the loop can exit:

1. Clean compile / type check -- zero errors
2. Tests -- zero failures
3. Exit condition met (clean audit, low-only round, or loop cap reached with critical/high findings resolved)
4. No `// TODO` or `// FIXME` comments introduced without corresponding tasks
