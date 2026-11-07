---
name: review-loop
description: Use only when the user explicitly asks to review and fix in a loop until clean. Not for plain reviews (use review-code); never invoke proactively.
argument-hint: "[diff|pr <number>|all|<path>] [--commit each|end]"
user-invocable: true
---

# Review Loop

Review, fix, re-review until a round finds nothing worth fixing. Fixes are new code — they need their own review.

## Rules

1. **Review in a fresh subagent every round.** Invoke `review-code` with `<target> --sub` (default target `diff`). If `review-code` is missing, spawn a subagent to review for correctness, security, resource, and performance defects, rating each finding Yes / Judgment call / No for worth fixing. Never review your own fixes inline.

2. **Use `diff` from round 2 for every target, including paths.** GitHub does not see unpushed fixes, re-reviewing the whole codebase wastes context, and path-scoped reviews can miss fixes in related files. For `pr <number>`, run `gh pr checkout <number>` first.

3. **Fix every Yes; fix a Judgment call only if Trivial or Small.** Skip No. Do not re-fix or re-argue a skipped item when a later round raises it again.

4. **Run the repo's checks after each round's fixes** (`make build` / `make test` / `make lint`, else native commands). Fix breakage before the next review.

5. **Stop when a round has nothing new to fix.** Cap at 5 rounds; round 5 is review-only, even if it finds actionable issues. Do not edit after that review — hand the open findings to the user. If a fixed finding comes back in any round, stop fixing and report the open findings.

6. **Commit each fix unless told otherwise.** `--commit each` (default) — one commit per fixed finding. `--commit end` — one commit after the loop stops. Never push. On the default branch, branch before the first commit — otherwise `diff` anchors at HEAD and committed fixes drop out of the next review.

7. **Report at the end:** rounds run and why it stopped, fixes (`path:line` — what changed), skipped findings with a reason each, open findings, and check results.
