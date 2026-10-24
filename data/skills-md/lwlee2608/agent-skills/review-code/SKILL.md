---
name: review-code
description: Use when asked to review a local diff, a GitHub PR, or a whole codebase. Reports rated findings; never edits code.
user-invocable: true
argument-hint: "[diff|pr <number>|<base>...<head>|all|<path>] [--sub] [--second-opinion]"
---

# Review Code

Review a target and report findings. Each finding is rated by **severity** (how bad if it happens), **likelihood** (how often the bad path actually runs), and a **worth-fixing** verdict derived from both — plus a high-level fix when worth fixing. This skill **reports only**; it never edits code unless the user explicitly asks afterward.

## Resolve the target

Pick the target from the argument, ignoring any flags. Default to `diff` when no target is given.

1. **`diff` (default)** — local work on the current branch: uncommitted edits, unpushed commits, and already-pushed commits, reviewed together. Anchor on the base-branch fork point, **not** the branch's own remote — otherwise commits drop out of the diff once they are pushed. Include untracked files, which a plain diff omits.
2. **`pr <number>`** (or a PR URL; bare `pr` means the current branch's PR) — review a GitHub PR: its diff plus enough PR context (title, description, base branch) to judge intent. If the GitHub CLI is unavailable, say so and fall back to `diff`.
3. **`<base>...<head>`** — review that commit range.
4. **`all` / `codebase`** — review the whole repository. State the scope you can realistically cover and prioritize entry points, core logic, and recently changed files. Note anything skipped.
5. **`<path>`** — a file or directory argument scopes the review to that path.

For a diff, PR, or range, review the changed lines **plus enough surrounding context** to judge them (callers, related functions). A bug is in scope even if the changed line only exposes it.

## Where to run the review

Default is inline. With `--sub`, run the whole review in a subagent and relay its report verbatim — use it for `all`/`codebase` or a large diff, where reading the files would bloat the session. Never re-review or paste back what the subagent returns; the only exception is the final call under `--second-opinion`. If the harness has no subagents, say so and review inline.

## Second opinion

With `--second-opinion`, also get a review from another agent: pi, or Claude Code when you are in pi.

- **Start it first.** Run the `second-opinion` skill on the same target in the background, then review as normal without waiting. The main session starts it even with `--sub`, because a background job started by a subagent can die when the subagent exits. If the skill isn't available, say so and review alone.
- **Append it verbatim.** After your report, add a `---` rule and a `## Second Opinion (<agent>)` section holding the other agent's review. Demote its headings one level (`##` → `###`) so it reads as nested; change nothing else. Don't merge, dedupe, or re-rate its findings. If it fails, put the error there; your review stands and you skip the final call.
- **Make the final call.** Either review can be wrong, including your own subagent's. End with another `---` rule and a `## Final Call` section that decides which findings are actually worth fixing:
  - Pair up findings that describe the same issue across both reviews.
  - Check every finding rated Yes or Judgment call by either review, and every one the reviews rate differently, against the code at its cited `file:line`. Don't take either review's word, and don't treat agreement as proof.
  - Rule each one **Fix**, **Optional**, or **Skip**, with a one-clause reason. Skip false positives (misread code, wrong location, path that can't run) and say why.
  - Add no new findings here.

  ```
  | # | Finding | Source | Call | Reason |
  |---|---------|--------|------|--------|
  | 1 | <short title> | Main #2, Second #1 | Fix | <why> |
  | 2 | <short title> | Second #3 | Skip | <false positive: why> |
  ```

## Review lens (in priority order)

1. **Correctness** — logic errors, off-by-one, nil/null derefs, wrong conditionals, race conditions, unhandled errors, incorrect API usage, broken edge cases.
2. **Security** — injection, missing authz/authn, secrets in code, unsafe deserialization, path traversal, unvalidated input.
3. **Data & resources** — leaks (fd/memory/goroutine), unbounded growth, missing transaction boundaries, N+1 queries.
4. **Performance** — needless allocations, O(n²) on hot paths, blocking calls in loops.
5. **Codebase fit** — a second pattern for something the repo already solves (HTTP client, error style, config), logic in the wrong layer, or code size out of proportion to what it delivers. Favor a small surface: few methods, simple params, complexity hidden inside. Deletion test for new abstractions: if deleting one makes complexity vanish, it was a pass-through; if complexity reappears across callers, it earns its keep.
   - **No unnecessary Go `interface`s.** A small surface is a concrete type with few methods, not the `interface` keyword. Declare one only when two real implementations exist or the real dependency cannot run in a test (third-party API, remote service). Flag single-implementation interfaces as indirection.
6. **Maintainability** — duplication, dead code, unclear naming, missing-but-needed tests. Report these only when they materially hurt; do not pad the report with style nits.
7. **Tests** — too many unit tests are a liability, not an asset. Flag tests that mostly exercise mocks/fakes rather than real behavior, tests that pin implementation details so any refactor breaks them, and redundant cases that add maintenance cost without catching new bugs. Prefer fewer tests against real components (integration-style, in-memory DB, real HTTP handler) over many mock-heavy ones. Do not ask for more unit tests by default; ask only when a real bug path is uncovered. After a refactor, tests on pieces that became internal should be deleted, not kept beside the new ones. If the repo already uses `testify`, flag hand-rolled `if got != want { t.Fatal(...) }` blocks.

Do not invent problems. If the code is clean, say so. Prefer a few high-confidence findings over many speculative ones.

## Rating each finding

**Severity** — impact *if* the bad path executes:
- **Critical** — data loss/corruption, security breach, crash on a common path, wrong results affecting users or money.
- **High** — wrong results or crash under realistic conditions; security issue needing some precondition.
- **Medium** — degraded behavior, perf regression, or a correctness bug on a rare path.
- **Low** — style, readability, minor inefficiency with no functional impact.

Rate a test finding by the risk it hides (the real path left unverified), not by the test's own impact.

**Likelihood** — how often the triggering condition is actually met:
- **High** — hit by normal usage or common inputs.
- **Medium** — uncommon but realistic inputs/timing/config.
- **Low** — requires rare, adversarial, or near-impossible conditions.

**Worth fixing** — derived from severity × likelihood, adjusted for fix cost:

```
                    Likelihood
Severity     High           Medium         Low
Critical     Yes            Yes            Yes
High         Yes            Yes            Judgment call
Medium       Yes            Judgment call  No (note only)
Low          Judgment call  No             No
```

- **Yes** — recommend fixing; include a fix.
- **Judgment call** — explain the trade-off (fix effort vs. payoff) and give a recommendation; include a fix.
- **No** — note it for awareness; omit the fix or keep it to one line.

**Fix effort** — rate whenever a fix is included:
- **Trivial** — a few lines, one file, no design change.
- **Small** — localized change, under an hour of work.
- **Medium** — touches several files or needs new tests.
- **Large** — refactor, design change, or risky migration.

Bump a Judgment call to **Yes** when the fix effort is Trivial; drop toward **No** when it is Large or risky relative to payoff. State the reason when you override the matrix.

## Report format

Lead with a `## Summary` section: header bullets, then a table of every finding sorted by worth-fixing (Yes first), then severity. Then a `## Findings` section with one block per finding. Every location must be a `file:line` you actually read. If nothing is worth reporting, omit the table and `## Findings`.

For `diff`, `pr`, or a range, add a **Net effect** bullet: judge only the codebase's structural health, not the feature value. A new feature or capability is never an improvement on its own. Weigh what the change removes or simplifies against what it adds. It improves when callers learn less and changes land in one place; it degrades when it adds shallow layers or spreads one concern across callers. Default to Neutral without concrete evidence either way.

```
## Summary
- **Reviewed:** <target> — <N files, what was covered>
- **Verdict:** <one line: overall health + count of worth-fixing findings>
- **Net effect:** Improves | Neutral | Degrades — <one-line reason> (diff/pr/range only)

| # | Finding | Severity | Likelihood | Worth fixing | Fix effort |
|---|---------|----------|------------|--------------|------------|
| 1 | <short title> | High | High | Yes | Small |
| 2 | <short title> | Low | Medium | No | — |
```

Then:

```
## Findings

### 1. <short title>
- **Location:** `path/to/file.ext:42`
- **Category:** correctness | security | resources | performance | codebase-fit | maintainability | tests
- **Severity:** High — <why this impact>
- **Likelihood:** High — <what triggers it>
- **Worth fixing:** Yes
- **Issue:** <what is wrong and what goes wrong as a result>
- **Fix:** <high-level approach, not a full patch>
- **Fix effort:** Trivial | Small | Medium | Large — <one clause on what the fix touches>
```

## Common mistakes to watch for

- **Treating test count as quality.** A PR with many mock-based unit tests can still be untested where it matters. Judge tests by what real behavior they pin down, and call out mock/fake-heavy tests as a maintainability cost.
