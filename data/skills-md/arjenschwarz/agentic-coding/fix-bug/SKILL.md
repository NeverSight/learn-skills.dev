---
name: fix-bug
description: Systematic bug investigation, resolution, and documentation. Use when fixing bugs that need thorough analysis, test coverage, and a formal bugfix report. Applies systematic debugging methodology, creates regression tests, and generates a standardized report in specs/bugfixes/<bug-name>/. For complex bugs, spawns competing implementation agents (including alternative harnesses like Kiro) and selects the best solution. Triggers on requests like "fix this bug", "debug and document this issue", or when a bug needs both resolution and documentation.
---

# Bug Fix Workflow

Fix bugs systematically while ensuring proper test coverage and documentation. Simple bugs are fixed directly; complex bugs get multiple competing implementations to find the best solution.

## Transit Integration

If a `T-[number]` ticket is mentioned (e.g., `T-42`), track it throughout the workflow:
- Extract the display ID from the reference
- Automatically create a branch named `T-{number}/bugfix-{bug-name}` (no user prompt needed)
- Move the ticket to `in-progress` status after branch creation. Add a comment: "Starting bugfix — investigating on branch T-{number}/bugfix-{bug-name}"
- Move the ticket to `ready-for-review` status after the PR is created. Add a comment: "Fix ready for review — PR #{pr-number}"

Use `mcp__transit__update_task_status` with the display ID to update status. Always include a comment when changing status.

If no Transit ticket is mentioned, skip all Transit-related steps.

## Workflow

### 1. Bug Name

Determine a concise, descriptive bug name (kebab-case) for the report directory. Derive from the issue description or ask the user if unclear.

### 2. Branch Creation

**When a Transit ticket is present:** If the current branch already matches `T-{number}/bugfix-*` (e.g., in a worktree), skip branch creation. Otherwise, automatically create a branch named `T-{number}/bugfix-{bug-name}` and switch to it. Do not ask for permission. Move the ticket to `in-progress` status.

**When no Transit ticket is present:** Use AskUserQuestion to offer branch naming options:
- `bugfix/{bug-name}` - Standard bugfix branch
- Skip branch creation

### 3. Systematic Investigation

Invoke the `systematic-debugger` skill to perform structured root cause analysis:
- Phase 1: Initial Overview (problem statement)
- Phase 2: Systematic Inspection (identify defects)
- Phase 3: Root Cause Analysis (Five Whys)
- Phase 4: Solution & Verification (proposed fixes)

Capture findings for the bugfix report.

### 4. Create Regression Tests

Before implementing the fix, write tests that prove the bug exists:
1. Write one or more failing tests that reproduce the bug
2. Run the tests to confirm they fail as expected — this is the "red" in red/green TDD
3. These tests become the acceptance criteria: the bug is fixed when they pass

The tests should:
- Be minimal and focused on the specific bug
- Include a descriptive name referencing the bug
- Document the expected vs actual behaviour in comments

Do not implement the fix yet. The tests must fail at this point.

### 5. Generate Initial Bugfix Report

Create `specs/bugfixes/<bug-name>/report.md` using the template in `references/report-template.md`. At this stage the "Resolution" section will be empty — it gets filled in after the fix is implemented.

### 6. Commit Investigation Checkpoint

Commit everything so far (failing tests + report + any investigation artifacts) using the `/commit` skill. This creates a clean baseline that competing implementations can branch from.

The commit message should indicate this is the investigation phase, e.g.: `T-42: Add investigation report and failing regression tests for {bug-name}`

### 7. Assess Difficulty

Evaluate the bug's complexity based on the investigation findings. Consider:

- **Number of files affected** — single file vs cross-cutting changes
- **Root cause clarity** — straightforward logic error vs subtle interaction
- **Risk of side effects** — isolated change vs changes near critical paths
- **Multiple valid approaches** — one obvious fix vs several plausible strategies

**Simple bugs** (single clear fix, low risk, few files): proceed to Step 8A.
**Complex bugs** (multiple possible approaches, higher risk, cross-cutting, or subtle root cause): proceed to Step 8B.

When in doubt, prefer the complex path — the overhead is small and you get better solutions compared to the risk of a naive fix for something subtle.

### 8A. Simple Fix (Direct Implementation)

For straightforward bugs:
1. Implement the fix
2. Run the regression tests to confirm they now pass (the "green")
3. Run the full test suite to ensure no breakage
4. Run linters/validators as per project conventions
5. Skip to Step 10.

### 8B. Complex Fix (Competing Implementations)

For complex bugs, spawn multiple agents that independently implement the fix. Each agent works in an isolated worktree branched from the current commit (which has the failing tests).

#### 8B.1 Prepare Implementation Brief

Write a concise implementation brief that all agents receive. Include:
- The root cause from the investigation (Phase 3 findings)
- The proposed solution(s) from Phase 4
- Paths to the failing test files so agents can verify their fix
- The project's test/lint commands (from Makefile or project conventions)
- Any constraints or areas to avoid

#### 8B.2 Spawn Competing Agents

Launch 3 agents in parallel, each in its own worktree. Use the exact tools specified below — do not substitute different tools or MCP agents for Agents 1 and 2.

**Agent 1 — Primary approach:** Call the **Agent tool** (not an MCP tool) with `isolation: "worktree"` and `subagent_type: "general-purpose"`. This spawns a Claude subagent in an isolated git worktree. Prompt it to implement the fix following the primary approach from the investigation's Phase 4.

**Agent 2 — Alternative approach:** Call the **Agent tool** (not an MCP tool) with `isolation: "worktree"` and `subagent_type: "general-purpose"`. This spawns a Claude subagent in an isolated git worktree. Prompt it to implement the fix using an alternative strategy — if Phase 4 identified alternatives, use one; otherwise instruct it to find its own approach that differs from Agent 1's.

**Agent 3 — Kiro (independent perspective):** This is the only agent that uses an MCP tool. Call `mcp__devtools__kiro-agent` with `agent: "kiro"` and `yolo-mode: true`. The `agent: "kiro"` parameter gives Kiro access to all its skills rather than just the default agent. Since Kiro operates in the current working directory, first create a worktree manually for it:
```bash
git worktree add ../{repo-name}-worktrees/fix-{bug-name}-kiro -b fix-{bug-name}-kiro HEAD
```
Then pass a prompt that includes the implementation brief and instructs Kiro to work in the worktree directory, implement the fix, run the regression tests, and run the full test suite.

To be explicit: Agents 1 and 2 use the Agent tool (subagent_type: "general-purpose", isolation: "worktree"). Only Agent 3 uses mcp__devtools__kiro-agent. Do not use mcp__devtools__codex-agent, mcp__devtools__gemini-agent, or any other MCP agent tool for Agents 1 and 2.

Each agent's prompt should follow this structure:
```
You are implementing a fix for a bug. Work in {worktree_path}.

## Bug Summary
{root cause from investigation}

## Your Approach
{specific approach for this agent}

## Failing Tests
The following tests reproduce the bug and must pass after your fix:
{test file paths and how to run them}

## Requirements
1. Implement the fix
2. Run the regression tests — they must pass
3. Run the full test suite — no regressions allowed
4. Run linters/validators: {lint commands}
5. Commit your changes with a descriptive message
```

#### 8B.3 Compare Solutions

After all agents complete, evaluate each solution. Read the diffs and test results from each worktree.

**Evaluation criteria** (in priority order):
1. **Correctness** — do the regression tests pass? Does the full test suite pass?
2. **Minimality** — fewer changed lines and files is better, all else being equal
3. **Code quality** — readable, follows project conventions, no hacks or workarounds
4. **Safety** — low risk of side effects, no changes to unrelated code
5. **Maintainability** — would a future developer understand this change easily?

Disqualify any solution where:
- The regression tests don't pass
- The full test suite has new failures
- Linting errors were introduced

If all solutions are disqualified, fall back to Step 8A (implement directly using the best partial solution as guidance).

#### 8B.4 Select and Report

Write a short comparison report at `specs/bugfixes/<bug-name>/solution-comparison.md`:

```markdown
# Solution Comparison: {bug-name}

## Candidates

### Agent 1 (primary approach)
- **Files changed:** {list}
- **Lines changed:** +X / -Y
- **Tests:** {pass/fail}
- **Approach:** {one-line summary}

### Agent 2 (alternative approach)
- **Files changed:** {list}
- **Lines changed:** +X / -Y
- **Tests:** {pass/fail}
- **Approach:** {one-line summary}

### Agent 3 (Kiro — independent perspective)
- **Files changed:** {list}
- **Lines changed:** +X / -Y
- **Tests:** {pass/fail}
- **Approach:** {one-line summary}

## Selected: Agent {N}

**Reason:** {2-3 sentences explaining why this solution was chosen}
```

#### 8B.5 Integrate Chosen Solution

Cherry-pick or rebase the winning agent's commits onto the working branch:

```bash
# From the main working directory (not a worktree)
git cherry-pick <commit-hash-from-winning-worktree>
```

If the winning solution has multiple commits, use:
```bash
git cherry-pick <first-commit>^..<last-commit>
```

After integrating, verify everything still works:
1. Run the regression tests
2. Run the full test suite
3. Run linters/validators

#### 8B.6 Cleanup Worktrees

Remove all competition worktrees:
```bash
git worktree remove ../{repo-name}-worktrees/fix-{bug-name}-kiro
# Agent tool worktrees with isolation: "worktree" are cleaned up automatically
```

Also delete the temporary branches:
```bash
git branch -D fix-{bug-name}-kiro
```

### 9. (Skipped — handled in 8A or 8B)

### 10. Update Documentation

Review and update any affected documentation:
- Code comments if behaviour changed
- README or docs if user-facing
- API docs if interface changed

### 11. Finalize Bugfix Report

Update `specs/bugfixes/<bug-name>/report.md` — fill in the Resolution section now that the fix is implemented. If the complex path was used, reference the solution comparison report.

### 12. Commit and PR (Transit bugs only)

When a Transit ticket is present, after all checks pass:
1. Commit all changes using the `/commit` skill
2. Push the branch to the remote
3. Create a PR using `gh pr create` with:
   - Title: `Fix T-{number}: {bug-name-in-title-case}`
   - Body: Summary of the bug, root cause, and fix (reference the bugfix report)
4. Move the Transit ticket to `ready-for-review` status. Add a comment with the PR URL.

When no Transit ticket is present, do not commit or create a PR unless asked.

### 13. Automated Review Fix (Transit bugs only)

After the PR is created, wait 10 minutes for CI checks and automated reviews to come in, then run the `/pr-review-fixer` skill to address any feedback from the first round automatically.

## Output

Upon completion:
1. Bug is fixed and verified
2. Regression test exists and passes
3. Full test suite passes
4. Report exists at `specs/bugfixes/<bug-name>/report.md`
5. If complex path was used: comparison report at `specs/bugfixes/<bug-name>/solution-comparison.md`
6. If a Transit ticket was tracked: changes committed, PR created, first review round addressed, ticket moved to `ready-for-review`
7. If no Transit ticket: code is ready for commit (do not commit unless asked)
