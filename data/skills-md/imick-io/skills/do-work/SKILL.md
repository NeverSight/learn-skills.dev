---
name: do-work
description: Implements the approved plan from the same Claude Code session, executing per the plan's declared Approach (RGR or direct). Runs the project's typecheck and test commands with a self-fix loop capped at 5 attempts. Never commits, never changes branches. Use when user types /do-work after approving a /plan-work plan in the same session.
---

# Implement the planned work

The project's validation commands (typecheck, test) should have been provided to you — run `/setup-imick-skills` if not.

## Preconditions

- An approved plan from `/plan-work` must exist in this session's conversation context, including the resolved issue reference and title. If you cannot locate it, stop and ask the user to run `/plan-work <issue>` first.
- The user has already created and checked out the branch they want to work on. Do not create or switch branches.

## Workflow

1. **Re-read the plan** from conversation context. Confirm the declared **Approach** (RGR or direct) and the test ordering / files to touch.
2. **Execute**:
   - **RGR**: For each test in the plan's ordering, write ONE failing test (RED), then the minimal code to pass it (GREEN), then refine. One test → one implementation → repeat. Never write all tests up front.
   - **Direct**: Make the changes described in the plan without test-first cycles.
3. **Validate** when the plan is fully executed, using the project's typecheck and test commands from setup.
4. **Self-fix loop** on failures, cap = 5 attempts total across typecheck + test:
   - Read the failure output.
   - Make a targeted fix.
   - Re-run the failing command.
   - If attempts reach 5 and tests are still red, go to Failure mode.
5. **Report** what changed (files modified, tests added) and stop.

## Failure mode

If typecheck or test is still red after 5 self-fix attempts:

- Stop. Do not commit, do not revert.
- Report the latest failure output verbatim.
- Tell the user: "Working tree is dirty. Inspect with `git diff`, or abandon with `git restore .`."

## Invariants

- **Never commit.** The user commits manually after reviewing the diff.
- Never create, switch, or rebase branches.
- Never delete or weaken existing tests to make new code pass.
- Never `git add` or stage files — leave the working tree dirty for human review.
- Never modify the issue's triage state on the issue tracker (status, labels, inline `Status:` line, comments). The user manages issue state manually.
