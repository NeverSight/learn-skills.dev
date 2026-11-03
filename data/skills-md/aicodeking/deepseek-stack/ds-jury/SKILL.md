---
name: ds-jury
description: "Gets independent reviews of a change from two or three different models or providers and loops on fixes until they agree. Use when the user says jury, panel review, second opinions, ask other models, or /ds-jury."
---

Get two or three independent reviewers to judge the same change, then fix until they agree.

## Steps

1. Get the work ready first. Answer open PR comments, fix known issues and run the relevant checks. Skip this only if the user wants to throw the code away.
2. Pick the jurors. Use models the user named. Otherwise pick the strongest available model from two or three different providers, at high reasoning effort.
3. Find a way to reach them in this harness: team workers or subagents with a model setting, a second agent CLI in the terminal (for example a Codex or Claude CLI), or an API call. If only one model is available, start two or three fresh-context subagents of that model, each with a different persona: correctness, security and edge cases, simplicity and scope.
4. Write one brief for all jurors: repo path, base SHA, diff command, goal in one sentence, out-of-scope items and check results. Tell them to review only and change nothing.
5. Ask each juror for: a verdict (APPROVE or CHANGES), a score out of 10 and findings as `id severity file:line claim fix`. Severity is blocker, should or nit.
6. Run the jurors in parallel. Wait for all of them. A timeout or error is not approval.
7. Check each finding against the code yourself. Fix the ones you agree with, with the smallest change. Write a one-line reason for each one you reject.
8. Re-run checks. Start a new round with the same brief, your answers and the new diff.
9. Report the result. If there is a PR, edit its description and add a table: juror, model, score per round. Write `no score` when a juror gave none. If there is no PR, put the table in your final reply.

## Stop when

- Every juror returns APPROVE with no open blocker or should finding.
- Three rounds are done. Report the open disagreements, with both sides in two lines each. The user decides.
- A round returns only nits. Stop without another round.

## Rules

- Jurors are read-only. They do not edit, push, comment or start their own subagents.
- Say which jurors are the same model as each other. Do not claim a provider you did not reach.
- Never invent a score or verdict.
- Guard the scope. Decline new features and list them as follow-ups.
