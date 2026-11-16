---
name: harness
description: >
  Set up or run the long-running-agent harness: initialize the durable state
  files (.agents/features.json, .agents/progress.md), then run the fixed
  startup and end-of-session loop. Use when the user says "/harness", "init the
  harness", "start a session", "hand off", or when .agents/progress.md or
  .agents/features.json exists and a session starts or ends.
---

The repository is the system of record. Chat is not. State that must survive a session lives in files; a fresh session recovers it by reading them, not by guessing. Based on [Learn Harness Engineering](https://github.com/walkinglabs/learn-harness-engineering).

## Init (once per repo, skip files that already exist)

Copy from `templates/` next to this file, then adapt — never leave placeholders:

1. `.agents/progress.md` — session log + current verified state.
2. `.agents/features.json` — every user-visible feature with `id`, `priority`, `status`, `verification` steps and `evidence`. Write real features from the repo's README/issues/code; all start `not_started`.
3. Optional for large sessions: `templates/session-handoff.md` → `.agents/handoff.md`.

Dependencies are installed by the devcontainer features, not here; the baseline is the CI status on the repo's dev forge (GitHub, GitLab, Azure DevOps), which the hook prints. Put each feature's real verification steps in `.agents/features.json`. Commit the files as one change. Once `.agents/progress.md` or `.agents/features.json` exists, the `SessionStart` hook prints the state and the `Stop` hook checks the handoff.

## Session start

1. `pwd` — confirm the repo root.
2. Read the repo's own rules: `CLAUDE.md`, `AGENTS.md`, `.agents/instructions/*.instructions.md` (the `SessionStart` hook lists which exist). They stay authoritative for commit format, PR base/title, scope limits and tooling; the harness adds the loop around them, it never overrides them.
3. Read `.agents/progress.md`, then `.agents/features.json`.
4. `git log --oneline -5`. The `SessionStart` hook already printed the state and the forge CI status of the branch.
5. CI red on the branch? That is the baseline: fix it first. No new work on a broken start.
6. Pick the highest-priority unfinished feature. Set it `in_progress`. One at a time.

## While working

- Follow the repo's rules while working (minimal-change discipline, commit/PR format, CI naming). A rule conflict with the harness: the repo rule wins; record it in the progress log.
- Stay inside the selected feature. A blocker may justify one narrow supporting fix.
- `passing` needs the feature's `verification` steps actually run, with evidence recorded (command + result, not "looks fine").
- Never reword, delete or weaken a feature or test to make it pass. Never loosen verification mid-feature.
- Declared done? Run the `harness-evaluator` agent: fresh context, tries to refute the claim.

## Session end

1. Update `.agents/progress.md`: verified state, what ran, evidence, known risk, next best step.
2. Update `.agents/features.json` statuses and evidence.
3. Walk `templates/clean-state-checklist.md`.
4. Commit once the repo is safe to resume, using the repo's commit and PR conventions from its rules. CI on the branch must be green or explained in the progress log; the next session must start without manual repair.

## Boundaries

Do not invent features, evidence or verification results. Do not mark `passing` without a run. Do not hide unfinished work by editing the list.
