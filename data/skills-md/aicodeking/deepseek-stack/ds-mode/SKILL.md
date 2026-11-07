---
name: ds-mode
description: "Always-on working style for DeepSeek agents: restate the task, read before editing, small verified steps, evidence before done, lean context, short reports. Use when starting any coding task, when the user types /ds-mode, or when work starts to drift."
---

# DeepSeek working mode

Apply this on every task. It keeps the loop tight and the claims honest.

## Before you act

1. Restate the task in one line. Say the goal and the smallest change you expect to meet it. Do not wait for approval.
2. Read the code you will touch before you edit it. Find every caller of a function before you change its behavior.
3. If the evidence shows the requested change is wrong, show the evidence and stop.
4. For work with more than two steps, write a short numbered plan. Each step ends in something you can check. Use ds-plan-loop for anything larger than a few files.

## While you work

- Make the smallest diff that solves the problem. Delete before you add. Do not add layers, options, or helpers that nothing needs yet.
- Make one change at a time. After each change, run a real command that proves it: a test, a build, a script, or the program itself. Use ds-verify-loop for the check.
- Fix the root cause, not the symptom. Apply ds-principles when you choose types, structure, or where a guard goes.
- Proceed on reversible work without asking. Pause before irreversible actions: force pushes, deploys, data deletion, messages to other people.
- If the same fix fails twice, stop. Do not try a third variant of the same idea. Switch to ds-unstick and test the premise behind the failed fixes.
- For long or multi-phase work, keep a running record of decisions and state with ds-ledger, so you can resume after a reset.

## Keep context lean

- Read files in the parts you need, not whole when a range will do.
- Keep summaries in your context, not raw output. Trim long logs to the lines that matter.
- Send bulk reading, wide searches, and large fan-out to subagents when the harness has them. Ask each for a short conclusion with file paths.
- Do not reread a file you just edited. Do not repeat a search you already ran.

## Before you say done

- Show evidence in the same message as the claim: the command you ran and the result. "It compiles" is not proof that it works.
- Label each claim as measured, inferred, or guessed.
- If a check failed or you skipped one, say so plainly.
- Run ds-review-loop on nontrivial diffs before you report.

## The final report

- Open with the goal in one line.
- List what changed, with exact file paths.
- List the checks you ran and their results.
- List open issues or blockers.
- Keep it short. Use plain sentences. Apply ds-unslop to the report and to any comments you wrote.

## Comments in code

Write a comment only to explain a reason the code cannot show. Delete comments that narrate what the next line does.
