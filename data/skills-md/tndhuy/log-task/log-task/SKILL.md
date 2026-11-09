---
name: log-task
description: Log completed work (from git commits, Claude history and checkpoints) into a project's declared platform (eoffice-api, lark, or manual). Use when the user runs /log-task or asks to log, report or book finished work to eOffice or Lark.
---

# log-task

Invoked via `/log-task`. Runs the 7-step procedure below every time -- do not
skip steps or shortcut the approval gate in step 6, even if the user seems
to be in a hurry.

## Step 1: Resolve the project

Run the script by absolute path from the user's own working directory
(`<skill-dir>` is the directory containing this SKILL.md). Do not `cd` into the
skill directory first; the script locates its skill directory itself:

    node <skill-dir>/scripts/resolve-project.mjs resolve --cwd "$(pwd)"

On exit code 2, show the stderr message and stop. If it says no project is
configured, or that `projects.json` was not found, show the user this template
to add to `projects.json`. That file lives in the data directory (`$LOG_TASK_HOME`,
else `~/.config/log-task`); when it is missing, the user creates it from
`<skill-dir>/assets/projects.json.example`, or runs `node <skill-dir>/scripts/init.mjs`
which creates the data directory, the config and the env file without overwriting anything.
Never create or guess the file yourself:

    "<absolute-path-to-project-root>": {
      "platform": "eoffice-api" | "lark" | "manual",
      "gitEmails": ["you@example.com"],
      "params": {}
    }

or, for a workspace holding several repos:

    "<absolute-path-to-group-root>": {
      "type": "group",
      "platform": "eoffice-api",
      "gitEmails": ["you@example.com"],
      "logDir": ".log-task",
      "children": { "<repo-relative-path>": { "params": { "project": "<eOffice project name>" }, "rules": {} } }
    }

Never guess a platform for an unlisted project.

The JSON on stdout has `mode` (`standalone`, `group-run`, or `child-run`),
`key`, `groupRoot` and `logRoot` (both null for standalone), and `targets`. Each target has `name`, `path`, `platform`, `gitEmails`, `params`,
`ledgerPath`, `rules` and `statePath`. `statePath` is the file to pass to
`--state`; `rules` is written to a temp rules.json. Steps 2-4 run once per target; in `group-run`, Steps 5-7 run
once for the whole group (see "Group runs" below).

## Step 2: Load the ledger

If `mode` is `group-run` or `child-run`, first run:

    node <skill-dir>/scripts/resolve-project.mjs migration-plan --cwd "$(pwd)"

(again by absolute path, without `cd` into the skill directory)

If `moves` is non-empty or `legacyRoot` is set, show the list and wait for
approval. Then, for each approved move whose `conflict` is `false`, run
`mv -n <from> <to>` after `mkdir -p` of the destination's directory. A move
with `conflict: true` is never executed; stop and ask. If the user declines a
planned move, stop: a run must not start from an empty ledger for a child whose
old ledger exists. A `legacyRoot` ledger
matches no child: ask whether to leave it or move it to
`<logRoot>/ledger/_legacy-root.json`; its fingerprints are never applied to a
child automatically.

Then read each target's `ledgerPath`. A missing file is `[]`. Reuse exactly
this path in Step 7 -- don't recompute it.

## Step 3: Gather evidence

Ask the user for the date window if not already given (e.g. "log everything
since my last run" or an explicit range).

**Git commits**, run inside the target's `path`, once per email in the target's `gitEmails`.
`--since`/`--until` filter by COMMITTER date ONLY, regardless of whether you
also pass `--author` or `--committer` -- they do NOT implement an
author-date check, so they can't be trusted to bound the window on either
side: a commit authored inside the window but rebased or re-committed
earlier or later (committer date now outside the window in either
direction) would otherwise be silently invisible. So: use `--since` only as
a widened (~14 days early), coarse pre-filter purely to keep the output
small -- do NOT pass `--until` at all, since it would just as silently clip
off commits whose committer date has drifted past the window on the other
side. Do the real window check yourself, client-side, on both dates,
after the git call:

    git log --all --since="<window-start minus 14 days>" \
      --author="<email>" --date=iso-strict \
      --pretty=format:'%H|%ad|%cd|%an|%s'

    git log --all --since="<window-start minus 14 days>" \
      --committer="<email>" --date=iso-strict \
      --pretty=format:'%H|%ad|%cd|%an|%s'

Union the two passes by commit hash (dedupe), then, from that combined set,
keep ONLY commits where the author date (`%ad`) OR the committer date
(`%cd`) falls within the REAL requested window
(`<window-start>`..`<window-end>`). This client-side OR-check is the ONLY
thing enforcing both the lower AND upper bound of the window -- neither
`--since` nor `--until` do real date-bounding work here, `--since` is
purely an output-size pre-filter. This is what catches the rebase/cherry-
pick case in either direction.

**Claude prompt history**, filtered to this project and window:

    jq -c --arg proj "<target path>" \
      'select(.project == $proj)' ~/.claude/history.jsonl

  Then filter the results to the window by comparing each entry's
  `.timestamp` (epoch milliseconds) against the window's start/end.

**Checkpoint / daily notes**, if present:

    ls <target path>/.remember/today-*.done.md <target path>/.checkpoint/*.md 2>/dev/null

  Read whichever of these fall inside the window.

## Step 4: Normalize and dedupe

From the raw evidence, synthesize candidate tasks: a short name, an inferred
estimate range, the actual evidence date range, a status if not clearly
"Done", and which evidence backs it. This is judgment, not a script -- group
tasks by module and give each one Estimate / Actual evidence / Suggested log
window / Status / Evidence, with a sources footer at the end.

Before fingerprinting, normalize the task name so a fresh run's wording
doesn't silently miss a match: lowercase it, strip any leading layer tag
(`[BE]`, `[FE]`, etc.), and collapse repeated whitespace.

For each candidate, compute a fingerprint over its full set of backing
commit hashes, sorted and comma-joined (not just the oldest/newest -- a
squashed or partially cherry-picked evidence set should still match):

    echo -n "<target-path>|<normalized-task-name>|<sorted-comma-joined-commit-hashes>" | shasum -a 1 | cut -d' ' -f1

For a standalone project the target path equals the config key, so existing
fingerprints are unchanged.

Drop any candidate where EITHER:
- its fingerprint already appears in the loaded ledger (**fingerprint
  match**), OR
- ALL of its backing commit hashes are found within a SINGLE existing
  ledger entry's `evidenceCommits` array -- i.e. one ledger entry's
  `evidenceCommits` is a superset of this candidate's commit set
  (**commit-subset match**; this still catches a match even if the
  synthesized name drifted between runs). Do NOT drop a candidate whose
  commits are merely scattered across the `evidenceCommits` of *multiple*
  different ledger entries -- that's a genuinely new cross-cutting task, not
  a duplicate, since one commit can legitimately back more than one logged
  task.

List every dropped candidate in your working notes together with which rule
dropped it (fingerprint match vs. commit-subset match, and which ledger
entry/fingerprint it matched) -- never drop one silently. If, after this
pass, no candidates remain, report "nothing new to log" (including the
dropped-candidate list, mirroring nova's own task-log convention of an
explicit "excluded because already logged" section) -- never produce an
empty draft. In a group-run, record "nothing new" for this target and continue
with the next target; stop only when no target has new candidates (see "Group
runs"). In a standalone or child-run, stop here.

## Step 5: Format the draft

Read `references/<platform>.md` for the resolved platform and follow its
"Draft format" section exactly.

## Step 6: Get approval

Show the full draft to the user. Wait for explicit approval or edits. Never
proceed to Step 7 without it, regardless of how the request was phrased.

## Step 7: Write

Follow `references/<platform>.md`'s "Write procedure" section exactly. After
it completes (fully, partially, or not at all -- manual's "write" is just
saving a file), append every successfully-logged task to the same ledger
file resolved in Step 2 (the target's `ledgerPath`), with the fingerprint
computed in Step 4 and an `evidenceCommits` array of every backing commit
hash (needed for Step 4's commit-anchored dedup check on future runs), then
write the file back.

End the run with a report that lists each task with its `link` (when the platform
returns one). A ledger entry keeps `externalId` only; links are derived at display
time. When a created task is later removed, keep its entry and set `deletedAt` (plus
`excluded` with the reason when the work is out of scope); a recreated task
gets the new `externalId` and `replaces: <old id>` on the same entry.

## Group runs

Applies when Step 1 returns `mode: "group-run"`. `child-run` follows the normal
7 steps with one target.

- Ask the date window once; use it for every target.
- Steps 2-4 per target, reporting dropped candidates per target. If no target
  has new candidates, report "nothing new to log" and stop.
- Step 5-6: one draft grouped target -> module -> task, following
  the target platform's reference file (`references/<platform>.md`), showing each target's `params.project`. List
  targets with nothing new as "nothing new". After approval, save the draft to
  `<logRoot>/drafts/<window-start>_<window-end>_<HHmmss>.md` (never overwrite).
  This draft save and the `.gitignore` prompt below apply to any run with a
  non-null `groupRoot` (group-run and child-run).
- Step 7: follow each target's platform reference. For `eoffice-api` targets use one `batch.json`, one rules file and one state file PER TARGET, run `create --dry-run` for EVERY target first and stop the whole group if any dry-run fails, and only then run `--apply` per target (each needing its own approval naming the host). Never retry a failed task with altered data and ledger only confirmed tasks. Append a task to its **own target's**
  ledger only after every required step for that task succeeded; a failure in
  one target does not block ledgering the others.
- Ledger writes use a temp file + rename, as always.
- If `groupRoot` is itself a git repo and does not ignore `.log-task/`, ask
  before adding it to that repo's `.gitignore`.

## eoffice-api platform

When a target's `platform` is `eoffice-api`, replace the platform-specific
parts of Steps 5-7 with `references/eoffice-api.md` ("Draft format" and
"Procedure"). Everything else (evidence, per-target ledger, group runs, approval
gates) is unchanged. Never read the env file (`<data-dir>/eoffice.env`); the scripts load it themselves.
Run `node <skill-dir>/scripts/doctor.mjs` to check Node, git, the config and the
variables (names only). A token is never printed or stored.
