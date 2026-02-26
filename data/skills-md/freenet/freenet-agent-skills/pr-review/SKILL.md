---
name: pr-review
description: Executes comprehensive PR reviews following Freenet standards. Performs four-perspective review covering code-first analysis, testing, skeptical review, and big-picture assessment.
license: LGPL-3.0
---

# PR Reviewer

Execute a comprehensive PR review covering all four review perspectives from Freenet quality standards.

## When to Use

Use `/freenet:pr-review <PR-NUMBER>` after a PR is ready for review, before merging.

## Review Process

### Step 1: Gather PR Context

```bash
# Get PR details
gh pr view <NUMBER>

# Get the diff
gh pr diff <NUMBER>

# Check for linked issues
# Look for "Fixes #XXX" or "Closes #XXX" in description
gh issue view <ISSUE_NUMBER>  # if linked

# List affected files
gh pr diff <NUMBER> --name-only

# Check CI status
gh pr checks <NUMBER>
```

### Step 2: Code-First Review

Review the code **before** reading the PR description to form an independent understanding.

**Process:**
1. Read the diff without looking at the description
2. Answer: What does this code do? What problem does it solve?
3. Now read the PR description
4. Compare your understanding with stated intent
5. Flag any gaps or mismatches

**Look for:**
- Does the code do what I think it should?
- Are there hidden side effects?
- Is the implementation approach sound?

### Step 3: Testing Review

Analyze test coverage at all levels.

**Check for:**
- Unit tests for new/modified functions
- Integration tests for component interactions
- Simulation tests for distributed behavior (if applicable)
- E2E tests for user-facing changes

**Questions to answer:**
- Does the regression test fail without the fix and pass with it?
- Are edge cases covered?
- Are error paths tested?
- Would these tests catch similar bugs?

**Red flags:**
- No tests for bug fixes
- Tests that only check happy path
- Removed or weakened test assertions
- `#[ignore]` annotations

### Step 4: Skeptical Review

Adversarial review looking for bugs, race conditions, and edge cases.

**Attack vectors to explore:**
- Race conditions in concurrent code
- Integer overflow/underflow
- Null/None handling
- Resource leaks (memory, file handles, connections)
- Error propagation gaps
- State machine invalid transitions
- Timeout and retry edge cases

**For each change, ask:**
- What happens if this fails?
- What happens under high load?
- What happens with malicious input?
- What happens if called twice?
- What happens if called out of order?

**5 Recurring Bug Patterns (from Feb 2025 fix review — 25/25 bugs):**

Check if the PR introduces or touches code matching these patterns:

| Pattern | What to Look For |
|---------|-----------------|
| `biased;` select starvation | Per-iteration caps? Cancellation safety? Which arm starves? |
| Fire-and-forget spawns | JoinHandle stored? `try_send` on critical paths? Catch-all `_ =>` in metrics? |
| State cleanup on failure | ALL related maps cleaned up? Peer lists filtered to live connections? GC exemptions time-bounded? |
| Backoff without jitter | Jitter ±20%? Sleep interruptible via `select!`? Zero-connection re-bootstrap? Critical msgs retried? |
| Deployment gaps | Exit codes declared? Auto-update gated on release? Security tested against app needs? Unused deps? |

### Step 5: Big Picture Review

Ensure the PR actually solves the stated problem and doesn't exhibit "CI chasing" anti-patterns.

**Check for removed code:**
```bash
# Look for deleted tests or fix code
gh pr diff <NUMBER> | grep -E '^-.*#\[test\]|^-.*fn test_|^-.*assert'
```

**Anti-patterns to detect:**
| Anti-Pattern | What to Look For |
|--------------|------------------|
| Ignored tests | `#[ignore]`, `skip`, `@Ignore` |
| Weakened assertions | Looser tolerances, `.ok()` on Results |
| Commented code | Especially tests or validation |
| Magic numbers | Hardcoded values replacing logic |
| Error swallowing | `.unwrap_or_default()`, silent fallbacks |

**Big picture questions:**
1. Does this PR actually solve the stated problem?
2. Does it fully address the linked issue?
3. Does it conflict with other open PRs?
4. Does it introduce patterns that will cause future problems?
5. Is there scope creep?

### Step 6: Documentation Review

Check if documentation is complete:

- **Code docs:** Do new public items have doc comments?
- **Architecture docs:** Do changes require doc updates?
- **User docs:** Are CLI/config changes documented?
- **Stale docs:** Do any existing docs contradict the changes?

## Output Format

Produce a consolidated review report:

```markdown
## Comprehensive PR Review: #<NUMBER>

### Summary
- **PR Title:** <title>
- **Type:** <feat/fix/refactor/etc>
- **CI Status:** <passing/failing/pending>
- **Linked Issues:** <issue numbers or "none">

---

### Code-First Analysis
**Independent Understanding:** <what the code appears to do>
**Stated Intent:** <from PR description>
**Alignment:** <matches/partially matches/misaligned>
**Gaps:** <any discrepancies>

---

### Testing Assessment
**Coverage Level:** <adequate/insufficient/excessive>

| Test Type | Status | Notes |
|-----------|--------|-------|
| Unit | ✅/❌/⚠️ | <details> |
| Integration | ✅/❌/⚠️ | <details> |
| Simulation | ✅/❌/N/A | <details> |
| E2E | ✅/❌/N/A | <details> |

**Regression Test:** <present and valid / missing / insufficient>
**Missing Tests:** <list specific gaps>

---

### Skeptical Findings
**Risk Level:** <low/medium/high>

| Concern | Severity | Location | Details |
|---------|----------|----------|---------|
| <issue> | <high/med/low> | <file:line> | <explanation> |

---

### Big Picture Assessment
**Goal Alignment:** <yes/partial/no>
**Anti-Patterns Detected:** <list or "none">
**Removed Code Concerns:** <list or "none">
**Scope Assessment:** <focused/some creep/significant creep>

---

### Documentation
- Code docs: <complete/incomplete/missing>
- Architecture docs: <up-to-date/needs-update/n/a>
- User docs: <up-to-date/needs-update/n/a>

---

### Recommendations

#### Must Fix (Blocking)
1. <critical issues that must be addressed>

#### Should Fix (Important)
1. <significant issues that should be addressed>

#### Consider (Suggestions)
1. <minor improvements or style suggestions>

---

### Verdict
**Ready to Merge:** <Yes / No - needs changes / No - needs discussion>

<If not ready, summarize what's needed>
```

## Parallel Subagent Reviews

For deeper analysis, spawn the specialized review agents in parallel using the Task tool with `subagent_type="general-purpose"`. Include the agent definition (from `agents/`) in each prompt so the subagent follows the correct review methodology.

```
Spawn all four in parallel using Task tool (all use subagent_type="general-purpose"):

1. "You are a code-first-reviewer. [Include agents/code-first-reviewer.md instructions]
    Review PR #<NUMBER> in freenet/freenet-core"

2. "You are a testing-reviewer. [Include agents/testing-reviewer.md instructions]
    Review test coverage for PR #<NUMBER> in freenet/freenet-core"

3. "You are a skeptical-reviewer. [Include agents/skeptical-reviewer.md instructions]
    Do a skeptical review of PR #<NUMBER> in freenet/freenet-core"

4. "You are a big-picture-reviewer. [Include agents/big-picture-reviewer.md instructions]
    Do a big-picture review of PR #<NUMBER> in freenet/freenet-core"
```

## Quality Standards

- Be thorough but constructive
- Cite specific files and line numbers
- Explain WHY something is a problem, not just WHAT
- Suggest fixes, not just criticisms
- Acknowledge what's done well
- Don't nitpick style if it matches codebase conventions
