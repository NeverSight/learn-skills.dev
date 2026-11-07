---
name: ds-ship
description: "Takes a change all the way from code to a merged pull request without supervision: build it, prove it, review it, file the PR, watch it and merge it. Use when the user says ship it, send it all the way, merge when green, or /ds-ship."
---

Own the work from its current state to a merged PR while nobody is watching.

Only act this way when the user clearly asked for it. The request grants three things: run the tests and app checks the proof needs without asking first, force-push this task's own branch with `--force-with-lease`, and merge once the gate below passes. It grants nothing else.

## Steps

1. If you are on the default branch, create a new branch.
2. Make the smallest change that meets the goal. Fix the case that was reported, not every case that might exist.
3. Prove every part of the diff. Reproduce the failure, apply the fix, and run the same reproduction again. Run the checks CI runs. For UI or runtime behavior, run the app and look. Paste the command and its output into your notes.
4. Review the change with `ds-review-loop`. Re-prove anything the review changed.
5. Rebase on the latest default branch, then file the PR with `ds-pr`. Add one line that says how you proved it.
6. Watch the PR with `ds-watch-pr`. Fix real findings and CI failures, prove each fix, push, and watch again.
7. Check the merge gate on the latest commit. Merge with the repo's usual method. Never use `--admin` or any other bypass.
8. Report the PR link, merge commit, proof, and every decision you made for the user.

Merge gate, all true on the latest head: proof covers the full diff, required checks are green, review bots are finished, each finding is fixed or answered with a reason, no human review asks for changes, and the branch is current and mergeable.

## Stop when

- The PR is merged and the report is written.
- You cannot prove the change, or the gate cannot pass and you cannot fix it. Ask the user.
- The next step deletes data, touches production, closes a PR, or pushes another branch. Ask the user.
- Six fix-and-watch cycles pass without a green gate. Stop and report what blocks it.

## Rules

- Do not end your turn while checks are pending. Wait with the watcher.
- Ask with the harness question tool, not a plain message. Put the PR link, the blocker and your recommended option in the question.
- If no question tool exists or nobody answers, leave the PR open and unmerged, and start your final message with the question.
- Evidence is output you saw in this session. A claim without output is not proof.
- Keep scope fixed. Decline extra work from reviews and list it as follow-ups.
