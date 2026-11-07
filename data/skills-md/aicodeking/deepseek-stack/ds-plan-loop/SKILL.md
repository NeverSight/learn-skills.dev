---
name: ds-plan-loop
description: "Write a numbered plan with an acceptance check for each step, critique it once in a fresh pass, revise it, then execute one step at a time. Use when a task touches more than one file, has unclear scope, or failed before because steps were missed. Invoke as /ds-plan-loop."
---

# ds-plan-loop

Plan before coding, check the plan once, then build the task one verified step at a time.

## Steps

1. Restate the goal in one sentence. List the files and commands you expect to touch. Read those files before you plan. Do not plan from memory.
2. Write a numbered plan. Each step gets one action and one acceptance check that a command or a direct observation can confirm, for example "`npm test -- auth` passes" or "`GET /health` returns 200". Keep each step small enough to verify in a single diff.
3. Write the plan to a file (PLAN.md, or the PROGRESS.md from ds-context-reset) so later steps and fresh sessions can read it.
4. Critique the plan in a fresh pass. Reread only the goal and the plan, as a reviewer who did not write it. If you can, run the critique in a subagent or new session. Answer three questions:
   - Which step is missing (setup, migration, config, tests, cleanup)?
   - Which assumption has not been checked against the code or docs?
   - Is there a simpler path that reaches the same goal with fewer steps?
5. Revise the plan. Check each risky assumption now by reading code or running a command. Do not carry it forward as a guess.
6. Execute step 1 only. Run its acceptance check and read the real output. Use ds-verify-loop when the check fails.
7. Mark the step done in the plan file, along with the evidence (command and result). Then move to the next step.
8. If a step shows that the plan is wrong, stop and revise the remaining steps before continuing. Do not improvise around it.

## Stop when

- Every step is marked done and its check passed, and the original goal holds when you check it end to end.
- You have done 2 critique rounds. A third round almost never finds anything new, so execute.
- A step fails its check twice in a row. Switch to ds-unstick.

## Rules

- No step without a check. "Looks right" is not a check.
- Do one step per diff. Do not batch steps to save time.
- Do not add steps that the goal does not need.
- Keep the plan short: about 3-10 steps. Split bigger work into separate plans.
