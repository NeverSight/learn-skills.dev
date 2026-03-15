---
name: pr-review
description: Review a PR linked to a kspec task, post findings as inline
  comments, and merge only when all quality gates pass. You NEVER fix code — you
  review and comment. If issues found, kick back to worker.
---
<!-- kspec-managed -->

# PR Review Skill

Review a PR linked to a kspec task, post findings as inline comments, and merge only when all quality gates pass. This skill runs in **subagent context** (spawned by the pr-reviewer agent). The goal is to find problems and verify quality — not to rubber-stamp merges.

## Reviewer Philosophy

**You own the merge.** When you approve a PR, you are personally vouching that the code is correct, complete, and ready for production. If something bad gets through, the review failed — not just the implementation. Your job is to be the last line of defense.

**When in doubt, block.** It is always better to kick back a PR for a trivial issue than to let a real problem through. A false positive costs one fix cycle. A false negative costs trust, debugging time, and potentially broken production. Default to MUST-FIX. Only downgrade to SHOULD-FIX or SUGGESTION when you are *certain* the issue is cosmetic and has zero correctness implications.

**Do not rationalize.** Do not invent reasons why something is acceptable. "Incremental implementation" is not a valid excuse for stubs that claim AC coverage. "Will be fixed later" is not a valid excuse for merging broken code. If the AC says the system does X, the code must actually do X — not pretend to do X with a no-op.

**Reproduce, don't just read.** Run the tests. Run the code paths. If the spec says "exit 0 on success," run the CLI command and verify the exit code. If the spec says "output valid JSON with --json flag," run the command with --json and parse the output. Read the diff, but also verify behavior empirically.

**Multiple review rounds are expected.** A PR that passes on the first review is fine if the investigation was thorough — but do not rush to approve. If you haven't completed the deterministic checks and analytical review described in review-principles, you haven't finished reviewing.

**Simple-looking PRs are where bugs hide.** A refactor, a rename, a test rewrite, or a "mechanical" change can silently change semantics. Refactors can break `Result<T>` error handling chains. Test rewrites can reduce coverage while appearing to improve it. Give these the same scrutiny as new feature code — do not fast-track based on perceived simplicity.

## Role Boundary

You are a REVIEWER. Your responsibilities:
- Review code quality, AC coverage (own + trait), spec alignment
- Post findings as inline PR comments with severity (MUST-FIX:, SHOULD-FIX:, SUGGESTION:)
- Merge the PR ONLY when all quality gates pass (no MUST-FIX or SHOULD-FIX)
- Complete the task after merge

You MUST NOT:
- Fix code issues
- Push commits to the PR branch
- Add or modify tests
- Make any code changes

If you find issues, post them as inline comments and transition the task to needs_work. The worker agent fixes them in the next iteration.

## Usage

```
/pr-review @task-ref
/pr-review #123
```

**Task reference is preferred** but not a hard gate. If a PR number is provided instead, the reviewer discovers spec context from the PR.

## CLI Lookups

Use CLI commands to resolve specs and traits. **Do NOT search `.kspec/` YAML files manually.**

| Need | Command |
|------|---------|
| Spec + all ACs (own + inherited) | `kspec item get @spec-ref` |
| Trait definition + ACs | `kspec item get @trait-slug` |
| Task details + spec_ref | `kspec task get @ref` |
| Search by keyword | `kspec search "keyword"` |
| All traits | `kspec trait list` |

**Resolving inherited traits:** When `kspec item get` shows "Inherited from @trait-slug", run `kspec item get @trait-slug` to see the full trait ACs. One command — never grep `.kspec/modules/*.yaml`.

## Quick Start

```bash
# With task ref (preferred)
kspec task get @task-ref           # Verify task exists
gh pr list --search "Task: @task-ref"  # Find linked PR

# With PR number (discovery mode)
gh pr view 123 --json title,body,commits

# Start the workflow
kspec workflow start @pr-review-loop
```

## Validation (Before Starting)

### 1. Resolve Task and PR Context

**If task ref provided:**
```bash
kspec task get @task-ref           # Verify task exists, get spec_ref
gh pr list --search "Task: @task-ref" --json number,url,title  # Find linked PR
```

**If PR number provided (or no task ref):**
Discover spec context using the dig-deeper pattern:
```bash
# 1. Check PR body for Task: or Spec: trailers
gh pr view <NUMBER> --json body | jq -r '.body'

# 2. Check commit messages for Task: or Spec: trailers
gh pr view <NUMBER> --json commits --jq '.commits[].messageHeadline,.commits[].messageBody' | grep -E '^(Task|Spec):'

# 3. Check changed files for // AC: annotations pointing to specs
gh pr diff <NUMBER> | grep '// AC: @'

# 4. Search recent tasks matching PR scope
kspec tasks list | grep -i "<keywords from PR title>"

# 5. If a task ref is found, resolve to spec_ref
kspec task get @task-ref --json | jq '.spec_ref'
# Then get the spec with ACs
kspec item get @spec-ref
```

If a spec is found through any method, proceed with full AC validation.
If only a task ref is found (no spec_ref on it), the task is infra/internal — skip AC checks.
If no task or spec context is found after all discovery steps, proceed with pure code review (skip AC checks).

### 2. PR Must Exist

If reviewing by task ref and no PR is found:

```
Error: No PR found for task @task-ref.
Create a PR first with /pr, then run /pr-review @task-ref.
```

## Automatic MUST-FIX: Patterns That Always Block

The following patterns are **always MUST-FIX** — no exceptions, no downgrading, no "follow-up" deferrals:

### Stubs and No-ops Claiming AC Coverage
- `void` expressions, empty function bodies, TODO comments, or placeholder returns where the spec requires real behavior
- Any code path where the AC's core verb (parse, validate, output, persist, exit) is not actually executed
- A test that asserts on a hardcoded value rather than testing the actual behavior

### Test Integrity
- Tests that verify implementation internals (compiled source strings, parser state, AST shape) rather than user-visible behavior the AC describes
- Tests that pass regardless of whether the feature works (e.g., asserting a function exists rather than asserting its output)
- Tests that mock the thing being tested — if the AC says "CLI outputs JSON," mocking the output formatter and asserting the mock was called proves nothing
- Tests that claim AC coverage at the wrong abstraction layer (e.g., parser unit tests claiming CLI-level AC coverage)

### Build and Verification Config Changes
Any change to configuration files that affect build, typecheck, lint, or test verification requires the **utmost scrutiny**:
- **Adding excludes/ignores to tsconfig, Biome, or test configs** — if files are excluded from typecheck or lint to make the pipeline pass, that is MUST-FIX. Excluding files to suppress errors is not fixing them.
- **Loosening compiler strictness** — disabling `strict`, adding `skipLibCheck`, widening `any` allowances. Each must be individually justified with a concrete reason.
- **Disabling or weakening Biome rules** — adding rule overrides, ignoring files, downgrading errors to warnings.
- **Modifying test configuration** — changing test sharding, skipping test suites, altering vitest config to mask failures.

**The question to ask:** Does this config change make the pipeline report *fewer* problems? If yes, it is MUST-FIX unless there is a concrete, spec-justified reason.

### Worktree and Import Hygiene
- **Imports from unmerged branches** — if the PR depends on code that isn't on main yet, it must either rebase onto that branch or the dependency task must be set as a blocker. Do NOT merge code that will break on main
- **Hardcoded absolute paths** — `/home/user/project/...` in any file is MUST-FIX
- **Shadow branch corruption** — changes that could affect `.kspec/` state integrity, worktree isolation, or shadow branch metadata

### Test Rewrites That Reduce Coverage
- If original tests verified behavior X and the replacement no longer verifies X — even if it verifies Y better — that is MUST-FIX. Replacement tests must be a **superset** of original coverage, not a different set.
- Watch for: test names that describe the old behavior but assertions that test something else, E2E CLI tests replaced with unit tests that skip the CLI layer, structural assertions replacing behavioral ones.
- When tests are rewritten, explicitly compare what the originals tested vs what the replacements test. If any original guarantee is lost, flag it.

### Refactors and Mechanical Changes
- When code is refactored, verify the refactored version preserves all behavior of the original — not just the happy path. Check error handling, edge cases, and `Result<T>` chains.
- When shared utilities are extracted or consolidated, verify all call sites still get the same behavior. Parameter ordering, default values, and error propagation can silently change during extraction.

### Severity Consistency
- You MUST NOT downgrade a finding to a lower severity than what an identical finding received in a previous review on this repo
- If you are unsure of the severity, default to MUST-FIX
- SUGGESTION is reserved for pure style preferences with zero correctness implications (naming style, comment formatting). If it touches behavior or correctness in any way, it is at minimum SHOULD-FIX

### Dependency and Branch Hygiene
- PR branch must be up to date with main (or the base branch). If there are merge conflicts or the branch is behind, block until rebased
- If the PR depends on another PR that hasn't been merged, the task dependency must be declared and the PR must be blocked until the dependency merges

## Quality Gates

This skill enforces **four quality gates**. Assume there are problems to find.

### 1. AC Coverage (Own + Trait)

Every acceptance criterion MUST have test coverage — both own ACs and inherited trait ACs.

```typescript
// Own AC
// AC: @spec-ref ac-1
it('should validate task ref is provided', () => { ... });

// Trait AC (use the trait ref, not the spec ref)
// AC: @trait-cli-command ac-1
it('should exit 0 on success', () => { ... });
```

**Check for gaps:**
- Run `kspec item get @spec-ref` — shows own ACs and inherited trait ACs (under "Inherited from @trait-slug")
- Search test files for `// AC: @spec-ref ac-N` (own) and `// AC: @trait-slug ac-N` (trait) across `tests/` and `packages/`
- Run `kspec validate` — any "inherited trait AC(s) without test coverage" for this spec is MUST-FIX
- Confirm annotation refs match AC text (not just matching `ac-N` numbers)
- Ensure annotations are standalone line comments (`// AC:` or `# AC:`), not inside block/JSDoc comments
- Flag any uncovered ACs (own or trait)

### 2. Spec Alignment

Implementation must match spec intent, not just pass tests:

- Read the spec description and ACs
- Read the implementation code
- **Verify behavior empirically** — run the CLI commands, feed real inputs, check actual outputs. Do not trust that "the code looks right." Prove it works.
- Check for undocumented behavior or spec deviations
- Check for stubs or no-ops where real behavior is required (see Automatic MUST-FIX section)

**This is NOT just "do tests pass"** — it's verifying the implementation actually does what the spec says. If the spec says "exit 0 on success," run the command and verify. If the spec says "output contains all displayed data as JSON," run with --json and verify every field.

**Coverage quality, not just coverage existence.** A test that claims to cover an AC but only tests implementation internals (parser state, compiled source strings, internal data structures) rather than the user-visible behavior the AC describes is MUST-FIX. The test must prove the AC, not just touch the code path.

### 3. Code Quality

Review the code with the scrutiny of a senior engineer who will be paged at 3 AM when this breaks. Local review (step 1) covers detailed criteria; here, focus on PR-level concerns:

- **Shared code awareness** — if the diff adds a utility that already exists in `src/`, flag it. kspec has extensive shared helpers (`testUlid()`, `setupTempFixtures()`, `kspec()` runner, `Result<T>` error handling) — ignoring them is MUST-FIX.
- **Consistency with codebase** — naming, error patterns, import organization match neighboring files. If adjacent files handle errors with `Result<T>`, new code should too.
- **Unnecessary complexity** — extra abstractions or premature generalization beyond what the spec requires
- **Schema validation** — Zod schemas in `src/schema/` are the source of truth. New code that bypasses Zod validation or creates parallel validation is MUST-FIX.
- **Shadow branch integrity** — changes touching `.kspec/` state, worktree management, or shadow branch operations need extra scrutiny for data corruption risks
- **Test helpers in production code** — test-only exports from `src/` modules are MUST-FIX. Test infrastructure belongs in `tests/`.

### 4. Regression Check

Run `npm test` and verify zero failures. New code must not break existing spec or trait AC tests. If the PR touches shared code, verify downstream consumers still work.

## Workflow

This skill delegates all behavior to `@pr-review-loop` workflow:

```bash
kspec workflow start @pr-review-loop
```

The workflow handles:
1. Run local review (`/local-review`) — covers own + trait AC coverage, test quality, code quality
2. Verify spec alignment (implementation matches spec intent)
3. Review code quality (DRY, consistency, shared code usage)
4. Verify no regressions (`npm test` passes fully)
5. Post all findings as inline PR comments (MUST-FIX:, SHOULD-FIX:, SUGGESTION:)
6. If MUST-FIX or SHOULD-FIX found: transition task to needs_work, exit without merging
7. Wait for CI to pass
8. **Post a structured GitHub review** (see below)
9. Merge only if all quality gates pass (no MUST-FIX or SHOULD-FIX items)

### REQUIRED: Post a GitHub Review with Inline Comments

You MUST post a GitHub review with **inline comments** on specific findings. This creates an actionable audit trail — reviewers and authors can see exactly which lines have issues.

**Step 1: Build a review JSON file with inline comments.**

For each finding (missing AC, code quality issue, etc.), add an inline comment on the relevant file and line:

```bash
# Write review body with inline comments to a temp file
cat > /tmp/pr-review-body.json << 'REVIEWEOF'
{
  "event": "APPROVE",
  "body": "## Review Summary\n\n**Task:** @task-ref\n**Spec:** @spec-ref\n\n### Own AC Coverage\n- [x] ac-1: <description> — test at <file:line>\n- [x] ac-2: <description> — test at <file:line>\n\n### Trait AC Coverage\n- [x] @trait-slug ac-1: <description> — test at <file:line>\n- [x] @trait-slug ac-2: <description> — test at <file:line>\n_(omit this section if spec has no traits)_\n\n### Code Quality\n<findings or 'No issues found'>\n\n### Quality Gates\n- [x] All tests pass (no regressions)\n- [x] Own AC coverage verified\n- [x] Trait AC coverage verified (or N/A — no traits)\n- [x] Code quality reviewed\n- [x] Spec alignment verified",
  "comments": [
    {
      "path": "src/example.ts",
      "line": 42,
      "body": "**MUST-FIX**: This reimplements `formatRef()` from `src/utils/refs.ts:15`. Use the existing utility."
    },
    {
      "path": "tests/example.test.ts",
      "line": 10,
      "body": "**MUST-FIX**: Missing trait AC coverage. `@trait-json-output ac-2` (JSON contains all displayed data) has no test. Add: `// AC: @trait-json-output ac-2`"
    }
  ]
}
REVIEWEOF
```

**Step 2: Post the review.**

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  --method POST \
  --input /tmp/pr-review-body.json
```

**Review event decision:**
- **MUST-FIX or SHOULD-FIX present** → use `"event": "COMMENT"`, do NOT merge, transition task to needs_work
- **Only SUGGESTION or no findings** → use `"event": "APPROVE"`, proceed to merge

**Inline comment guidelines:**
- Every MUST-FIX finding gets an inline comment on the relevant line
- Use severity prefix: `**MUST-FIX**:`, `**SHOULD-FIX**:`, `**SUGGESTION**:`
- For missing AC coverage, comment on the test file where the annotation should be added
- For code quality issues, comment on the specific line with the problem
- Do NOT use `REQUEST_CHANGES` since the review is posted from the repo owner's account

**Never merge without posting a review.** Even a brief APPROVE review with no inline comments is better than no review.

### When Issues Are Found (Kick Back to Worker)

If your review finds MUST-FIX or SHOULD-FIX items:

1. Post the review with `"event": "COMMENT"` and inline comments
2. Transition task: `kspec task needs-work @task-ref --reason "MUST-FIX: <summary>"`
3. Exit — do NOT merge, do NOT fix code

The worker agent picks up the `needs_work` task in the next iteration and addresses the findings.

### CRITICAL: CI Re-verification

**After ANY push, you MUST re-verify CI from the beginning.** Prior CI checks are invalidated by new commits. Never merge without fresh CI verification on the current HEAD.

## Re-review After Fix Cycle

When reviewing a PR that was previously reviewed and had fixes pushed:

1. Review the FULL PR (not just new commits)
2. Focus feedback on changes since last review
3. Verify previous MUST-FIX and SHOULD-FIX findings were addressed
4. Check for regressions introduced by fixes
5. If all resolved: APPROVE and merge
6. If issues remain or new issues: post comments, kick back again

## Unfixed SHOULD-FIX Tracking

If a SHOULD-FIX item persists after re-review (worker chose not to fix):
- Create an inbox item: `kspec inbox add "SHOULD-FIX from PR #N: <description>"`
- If the issue is well-defined enough: create a task directly
- This ensures the finding is tracked even if the PR is merged

## Subagent Context

This skill runs in **ACP subagent context**:
- Spawned by the pr-reviewer agent for PR review
- Runs sequentially (agent dispatch waits for completion)
- No human interaction expected
- Auto-resolves decisions based on quality gate outcomes

**Role boundary:** This skill reviews and merges. It NEVER fixes code, adds tests, or pushes commits. If issues are found, they are posted as comments and the task is transitioned to needs_work for the worker.

## Exit Conditions

- **PR merged** - Success, quality gates passed (no MUST-FIX or SHOULD-FIX)
- **Issues found** - Posted as inline comments, task transitioned to needs_work
- **CI failed** - Tests don't pass
- **PR not found** - Validation failed, no PR for task

## Example

```
/pr-review @task-reflect-loop-skill

[Validates task exists]
[Finds PR #234 linked to task]
[Starts @pr-review-loop workflow]
[Runs local review - checks AC coverage]
[Verifies spec alignment]
[Posts review with findings]
[If clean: waits for CI, merges PR, completes task]
[If issues: posts COMMENT review, transitions to needs_work, exits]
```

## Task Completion

**CRITICAL: You MUST complete the task after merging the PR.**

The `@pr-review-loop` workflow includes task completion as the final step (ac-7). After the PR is merged:

```bash
kspec task complete @task-ref --reason "Merged in PR #N. <summary>"
```

Include in the reason:
- PR number
- Summary of what was implemented
- Any notable changes or deviations
- AC coverage confirmation

Do NOT exit after merge without completing the task.
