---
name: pr-resolution
description: "[v3] Resolve all PR comments using parallel agents with full workflow and verification gate"
argument-hint: "[optional: PR number, GitHub URL, or 'current']"
---

# Resolve PR Comments in Parallel (v3)

> **DEFAULT WORKFLOW** for resolving PR comments with parallel execution.

## Quick Reference

| Action | Command |
|--------|---------|
| Get comments | `~/.claude/skills/pr-resolution/bin/get-pr-comments PR_NUM` |
| Parse CodeRabbit | `~/.claude/skills/pr-resolution/bin/parse-coderabbit-review PR_NUM` |
| Check CI | `gh pr checks` |
| Resolve thread | `~/.claude/skills/pr-resolution/bin/resolve-pr-thread NODE_ID` |
| Resolve all threads | `~/.claude/skills/pr-resolution/bin/resolve-all-threads PR_NUM` |

## Workflow Overview

```text
Phase 0: Pre-Flight     → GoodToGo status check (if installed, otherwise skip)
Phase 1: Discovery      → Gather comments, parse bot formats, enumerate
Phase 2: Classification → Categorize by priority, group by file
Phase 3: Resolution     → Launch parallel agents by file group
Phase 4: Verification   → Local checks + GoodToGo gate (if installed)
Phase 5: Completion     → Commit, push, resolve threads
```

---

## Phase 0: Pre-Flight

**If `gtg` is installed**, run the GoodToGo pre-flight check (see `references/goodtogo.md`):

```bash
if command -v gtg &> /dev/null; then
  # gtg auto-detects repo from git remote
  GTG_RESULT=$(gtg $PR_NUM --format json 2>/dev/null)
  GTG_STATUS=$(echo "$GTG_RESULT" | jq -r '.status')
fi
```

Route based on status (or skip straight to Phase 1 if `gtg` is not installed):
- `READY` → Quick verify and commit (fast path — skip Phases 1-3)
- `CI_FAILING` → Fix CI first
- `ACTION_REQUIRED` → Continue with full workflow
- `UNRESOLVED_THREADS` → Continue with full workflow

---

## Phase 1: Discovery

1. **Gather comments** using scripts from `references/discovery.md`
2. **Parse bot formats** using rules from `references/bot-formats.md`
3. **Print enumeration** - counts MUST match before proceeding

---

## Phase 2: Classification & Grouping

1. **Classify each comment** using `references/classification.md`
2. **Group by file** for parallel execution:

```markdown
## Parallel Execution Plan

### Group A: src/api/route.ts (3 comments → 1 agent)
- #1 [blocking] Line 45 - Add error handling
- #3 [suggestion] Line 67 - Improve validation

### Group B: src/components/Button.tsx (1 comment → 1 agent)
- #2 [suggestion] Line 23 - Add prop types

### Group C: CI Failures (if any → 1 agent)
- Fix lint/type errors

Total: 3 parallel agents
```

---

## Phase 3: PARALLEL EXECUTION

**MANDATORY: Launch agents simultaneously using the Task tool:**

```markdown
Agent 1: "Fix comments on src/api/route.ts"
- Comment #1: Add error handling at line 45
- Comment #3: Improve validation at line 67

Agent 2: "Fix comments on src/components/Button.tsx"
- Comment #2: Add prop types at line 23

Agent 3: "Fix CI failures"
- Lint errors
- Type errors
```

**Parallel execution rules:**

| Condition | Execution |
|-----------|-----------|
| Same file | → Same agent (avoid conflicts) |
| Different files | → Parallel agents |
| CI failures | → Dedicated agent |
| Questions | → Ask human first |

Wait for all agents to complete.

---

## Phase 4: Verification Gate (MANDATORY)

1. **Run local checks** from `references/verification.md`
2. **If `gtg` is installed**, run final verification from `references/goodtogo.md` (deterministic READY/BLOCK signal)
3. **Verify all resolutions** - every comment needs explicit resolution

**DO NOT commit until all checks pass.**

---

## Phase 5: Completion (MANDATORY — DO NOT SKIP)

Follow steps from `references/completion.md`:

### 5a. Commit and push
1. Commit all fixes together
2. Push to remote

### 5b. Post resolution summary
3. Post resolution summary comment to PR

### 5c. Resolve ALL GitHub threads (MANDATORY)

**Run the resolve-all-threads script:**
```bash
~/.claude/skills/pr-resolution/bin/resolve-all-threads $PR_NUM
```

This script:
- Queries all unresolved threads on the PR
- Resolves each one via GraphQL mutation
- Verifies zero unresolved threads remain

**If the script reports failures or remaining threads: DO NOT mark workflow as complete. Fix manually with `bin/resolve-pr-thread THREAD_ID`.**

### 5d. Final verification
4. Confirm script output shows "All threads resolved"

**Workflow is NOT complete until all threads are resolved.**

---

## Example: PR with 6 Comments

```markdown
## Discovery
1. [blocking] src/api/route.ts:45 - Security issue
2. [suggestion] src/api/route.ts:67 - Add validation
3. [suggestion] src/components/Form.tsx:23 - Add types
4. [nitpick] src/utils/format.ts:12 - Typo
5. [question] src/lib/auth.ts:89 - "Handle null?"
6. CI: Lint error

## Parallel Plan (after asking human about #5)
- Agent 1: src/api/route.ts (#1, #2)
- Agent 2: src/components/Form.tsx (#3)
- Agent 3: src/utils/format.ts (#4)
- Agent 4: src/lib/auth.ts (#5 - if fix)
- Agent 5: CI fix (#6)

## Execution
Launch agents in parallel → Wait → Verify → Commit → Push
```

---

## Related

| Resource | Description |
|----------|-------------|
| `detailed-reference.md` | Single-threaded detailed reference |
| `/commit-commands:commit` | Clean commit workflow |
