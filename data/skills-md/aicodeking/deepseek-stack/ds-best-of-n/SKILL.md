---
name: ds-best-of-n
description: "Run N independent attempts at the same task in parallel, pick the strongest as the base, and graft the best parts of the others into it. Use when one attempt at a non-trivial artifact could land on the wrong shape, or for /ds-best-of-n, 'try a few versions', 'best of 3'."
---

# ds-best-of-n

One attempt is a sample, not an answer. DeepSeek is cheap enough that three to five attempts usually cost less than one round of fixing a bad first try.

## Steps

1. Frame the task. Write one prompt that every attempt gets unchanged. Write a private rubric of 3 to 6 concrete, checkable criteria. Attempts never see the rubric.
2. Pick N. Use 3 by default and 5 when the design space is wide. Give each attempt its own output location, such as a git worktree or a separate temp folder.
3. Spawn N subagents at once with the prompt, the shared context and their output path. Ask each for the artifact plus a short note on alternatives it rejected. If a harness cannot run subagents, run the attempts one after another in fresh contexts.
4. Check each attempt. Run its build, tests or a quick probe. Record pass or fail with output. Discard attempts that do not run.
5. Score the survivors against the rubric. Pick the one with the best overall structure as the base. Structure beats polish.
6. List the specific strong parts of the other attempts: a test, an edge case, a cleaner function. Graft only those into the base. Do not merge whole files.
7. Re-run the full checks on the grafted result and show the output.

## Stop when

- The grafted result passes every check and you have reported base, grafts and scores.
- Or no attempt passes after one re-run with a clarified prompt. Report what failed.

## Rules

- Never pick by reading the attempt's own summary. Pick by running it.
- Do not let one attempt see another before scoring.
- Keep the losing attempts until the final checks pass.
