---
name: pre-push-review
description: Review unpushed commits before pushing to remote repository
---

# Pre-Push Code Review

Review and fix unpushed commits before they reach the remote repository.

## Phase 1: Identify Changes

Determine which commits haven't been pushed to the remote repository. Use `git diff origin/<branch>..HEAD` to get the full diff of unpushed changes. Show the user which commits will be reviewed.

If there is no remote tracking branch yet, diff against `origin/main`.

## Phase 2: Locate Relevant Specifications

Check if there's a spec for the feature being worked on:

- Examine the current branch name for feature indicators
- Look in the specs directory for matching feature folders
- Review all documents in the feature folder: requirements, design, tasks, and decision log
- If no spec exists, proceed with general review only

## Phase 3: Launch Review Agents in Parallel

Use the Agent tool to launch all agents concurrently in a single message. Pass each agent the full diff so it has the complete context.

### Agent 1: Code Reuse Review

For each change:

1. **Search for existing utilities and helpers** that could replace newly written code. Use Grep to find similar patterns elsewhere in the codebase — common locations are utility directories, shared modules, and files adjacent to the changed ones.
2. **Flag any new function that duplicates existing functionality.** Suggest the existing function to use instead.
3. **Flag any inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, ad-hoc type guards, and similar patterns are common candidates.

### Agent 2: Code Quality Review

Review the same changes for hacky patterns:

1. **Redundant state**: state that duplicates existing state, cached values that could be derived, observers/effects that could be direct calls
2. **Parameter sprawl**: adding new parameters to a function instead of generalizing or restructuring existing ones
3. **Copy-paste with slight variation**: near-duplicate code blocks that should be unified with a shared abstraction
4. **Leaky abstractions**: exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
5. **Stringly-typed code**: using raw strings where constants, enums (string unions), or branded types already exist in the codebase

### Agent 3: Efficiency Review

Review the same changes for efficiency:

1. **Unnecessary work**: redundant computations, repeated file reads, duplicate network/API calls, N+1 patterns
2. **Missed concurrency**: independent operations run sequentially when they could run in parallel
3. **Hot-path bloat**: new blocking work added to startup or per-request/per-render hot paths
4. **Unnecessary existence checks**: pre-checking file/resource existence before operating (TOCTOU anti-pattern) — operate directly and handle the error
5. **Memory**: unbounded data structures, missing cleanup, event listener leaks
6. **Overly broad operations**: reading entire files when only a portion is needed, loading all items when filtering for one

### Agent 4: Spec & Documentation Review (only if spec exists)

1. **Spec adherence**: Verify implementation matches requirements and design. Identify divergences. Ensure divergences are documented in the decision log.
2. **Documentation**: Check if README, CLAUDE.md, or other docs need updates to reflect the changes.
3. **Testing gaps**: Verify presence of appropriate tests for new/modified code. Check that tests test behavior, not implementation.

## Phase 4: Fix Issues

Wait for all agents to complete. Aggregate their findings and fix each issue directly.

**Constraints:**

- **Do not modify test files** unless fixing an actual bug (e.g., a test that tests the wrong thing or has a genuine error). Refactoring production code must not require test changes — if it would, reconsider the refactoring approach.
- If a finding is a false positive or not worth addressing, skip it without debate.

## Phase 5: Verify

After all fixes are applied:

1. Run the project's test suite (use Makefile commands if available). All tests must pass.
2. Run linters and validators as specified in project configuration.
3. If any test fails, investigate whether the fix introduced a regression and revert or adjust the fix — do not modify the test to make it pass.

## Phase 6: Generate Implementation Explanation (if spec exists)

Use the explain-like skill (invoke the Skill tool with skill="explain-like") to generate explanations of the implementation at multiple expertise levels. Write the output to `specs/{feature_name}/implementation.md`.

**Use the explanation as a validation mechanism:**

- If any requirement from the spec cannot be clearly explained, flag it as potentially incomplete.
- If the explanation reveals logic that doesn't align with the design, flag it as a divergence.
- Add a "Completeness Assessment" section summarizing: what's fully implemented, what's partially implemented, and what's missing.

## Phase 7: Summary

Provide a clear verdict: **Ready to push**, **Needs fixes** (with must-fix list), or **Requires discussion** (with architectural concerns).

List what was fixed automatically and what still needs attention.
