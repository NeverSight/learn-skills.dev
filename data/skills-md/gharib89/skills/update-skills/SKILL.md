---
name: update-skills
description: "Refresh this repo's skills in one PR: the Gharib89/skills skills, every skill they compose at its pinned ref, and any other repo-scoped skill the owner picks; report upstream drift to the source repo and summarise what changed. In the source repo, move the drifted pins instead. Attended only."
disable-model-invocation: true
metadata:
  version: 0.7.2
---

# update-skills

Refresh a repo's skills as one PR the repo's own CI, reviewers and merge gate
see, with a body that says what moved. The **source repo** is
`Gharib89/skills`, where these skills are written; a **consumer repo** holds
**derived copies** installed from it, the source repo included. A composed
skill's **pinned ref** is the upstream commit the source repo tested, and
**upstream drift** is that upstream moving past it.

The one part a Ship run follows without invoking this skill is
[In a Ship run](#in-a-ship-run), for an upstream-drift issue in the source repo.

**This skill calls Ship's generic mechanics by path** from the worktree: `$S`
below stands for `.claude/skills/ship/scripts` and `$U` for
`.claude/skills/update-skills/scripts`. Each mechanic answers `--help` with its
flags. Plan files and body files go in your scratchpad, outside the repo. `$S`
and `$U` are notation: write the paths out.

## Process

### 1. Isolate

From the main checkout, `$S/isolate.sh none chore update-skills-<YYYYMMDD>`,
the run's date as `date +%Y%m%d` prints it, then work from the path it prints.
A second run the same day is refused by isolation, and nothing is deleted to
make room. Note `git rev-parse HEAD` there as `<old>`: the tree
before the refresh, which the plan reads as the old side.

### 2. Refresh the source-repo skills

In a consumer repo, reinstall the four skills Ship needs and every other skill
the lock records from `Gharib89/skills`, in any case: one left out keeps its old
version, and step 3 then reads it as unmoved.

```sh
flags=$(jq -er '[.skills | to_entries[] | select(.value.source | ascii_downcase == "gharib89/skills") | .key] + ["ship", "cloud-ship", "setup-skills", "update-skills"] | unique | map("--skill " + @sh) | join(" ")' skills-lock.json) && eval "npx skills add Gharib89/skills $flags --agent claude-code -y"
```

In the source repo, whose `skills-lock.json` records `ship`'s source as `.`,
run the refresh line its CLAUDE.md carries instead. Project scope always: no
`-g`.

### 3. Plan

```sh
$U/heads.sh . > <scratch>/heads.json
$U/plan.sh . <scratch>/heads.json --old <old> > <scratch>/plan.json
```

In the source repo, whose many upstreams reach the anonymous rate limit, run
`heads` as `GH_TOKEN=$(gh auth token) $U/heads.sh .`. Its `unreachable` rows are
skills whose upstream did not answer: no head, so never drift or an offered
update. Carry them to step 8. `heads` exits 1 with the count on stderr when
every upstream failed: nothing was read, so stop and tell the owner. The plan's
fields drive every later step; the header comment in `plan.sh` defines each one.

Nothing moved (every `source_skills` entry at its old version, every
`composed` entry's `old_ref` equal to its `pin`, `drift`, `others` and
`sections` empty, and no `unreachable` row): tell the owner the repo is
current, run `$S/cleanup.sh none` from the main checkout, and stop.

### 4. Composed skills at their pins

Run every `composed[].install` line, then `$S/preflight.sh none` and keep its
`reasons`. Preflight exiting 1 with only a `worktree exists` reason naming this
run's own worktree is the expected answer, not a failure. A profile reason is
step 6's; any other carries the line that repairs it: run that, then preflight
again. A consumer repo never installs a drift row's `head`: that version is one
nobody tested Ship against, and the row reaches the source repo in step 7
instead.

### 5. Other skills

`others` lists the repo-scoped lock entries, neither from the source repo nor
composed, whose upstream moved. Non-empty, outside the source repo (step 9
moves every row there): ask once, in multi-select questions of four skills,
four to an AskUserQuestion call, each option the skill's name described by
`<old_ref, or "no ref"> → <head>`; run the ticked `install` lines.

### 6. setup-skills sections, then retired terms

`/setup-skills` re-runs when step 4's `reasons` carry `profile missing` or
`profile invalid`, or `sections` is non-empty. Follow it by hand in this
session, with no second session or subagent: read
`<worktree>/.claude/skills/setup-skills/SKILL.md`, the refreshed copy (the main
checkout's predates the refresh), and take its path from there. A `profile
missing` takes its `## Process` alone, which writes every section. A `profile
invalid` takes its `## Re-run`, and `sections` its "A setup section re-run",
redoing for each section only the item its template feeds; when both hold, the
`## Re-run` first, then the sections. Its step 1 re-checks what steps 2 and 4
installed and the parent docs this run never writes, so run it as a check: a
failure skips the re-run, recorded as `setup-skills needed: <section or profile
reason>` per item it would have redone, with what step 1 printed beside it, and
the step goes on to the retired terms. Its own preflight calls read step 4's
expected answer as expected. Its proposals and
interview questions go to the owner from this session, with AskUserQuestion,
and writes land on confirm as setup-skills says.

| `section` | setup-skills item |
|---|---|
| `pr-template` | **PR template** |
| `reviewer-scaffolding` | **Reviewer scaffolding** |
| `local-gate` | **Self-contained local gate** |
| `local-gate-harness` | **Local gate over the harness** |
| `coding-standards` | **Coding standards** |
| `dimension-labels` | **Triage labels on the host** and **The `## Dimension labels` section** |
| `ado-tracker-doc` | step 1.1's Azure DevOps tracker doc |
| `ship-block` | **The `### Ship` sub-block** |
| `cloud-bootstrap` | **Cloud bootstrap** |

When the re-run is done, run `$S/preflight.sh none` again:
the step is done when step 4's expected answer is all that is left, unless the
re-run was skipped. Note the profile schema
move for step 8: the `Schema:` line of `docs/agents/ship.md` at `<old>` against
the one now.

**Retired terms**, whether or not setup-skills re-ran. Each `retired` row is a
word a source-repo skill stopped using inside the range this refresh crosses.
In a consumer repo, find it in the repo's own files, never the derived copies:
both commands below exclude `.claude/skills/<name>/` for each skill in
`skills-lock.json`, so a skill the repo wrote itself is swept.
A term that is a file name (a Term cell ending in an extension, such as
`CONTEXT.md`) is renamed first: `git mv` every tracked file of that name to the
row's `replacement` in the same directory. List them with:

```sh
bash -c 'T=$1; shift; L=$(jq -er ".skills | keys[]" skills-lock.json) || exit 2; for s in $L; do set -- "$@" ":!.claude/skills/$s/"; done; git ls-files -- ":(glob)**/$T" "$@"' _ '<term>'
```

Three cases rename nothing, each listed for step 8's Needs attention: a file
that is not the one the row means, such as a test fixture or a vendored
document, as `<path>: not renamed, not the <term> the row means`; a file whose
target already exists, as `<path>: not renamed, <replacement> exists`; and every
file of a row whose replacement is null. Then sweep the references:

```sh
bash -c 'T=$1; shift; L=$(jq -er ".skills | keys[]" skills-lock.json) || exit 2; for s in $L; do set -- "$@" ":!.claude/skills/$s/"; done; git grep -n -w -F -e "$T" -- . "$@"' _ '<term>'
```

Replace each hit with the row's `replacement` where it reads correctly in that
sentence. A record of the past, such as a changelog entry or an ADR, keeps the
word and is no hit. A hit that names a file this step left in place keeps the
word too. List it, every other hit that was not replaced, and every hit of a
row whose `replacement` is null, for step 8's Needs attention as
`<path>:<line>: <term>`.
In the source repo there is nothing to sweep.

### 7. Report upstream drift

`drift` non-empty, or in the source repo `others` non-empty: the source repo
keeps one open issue for it. `$U/drift-body.sh <scratch>/plan.json` prints the
issue's `table`, one row per `drift` entry and, in the source repo alone, per
`others` entry: a consumer's other skills are its own. Write a body file holding
a `## Drift` section with that table, then a `## Moving the pins` section of one
sentence: `A Ship run moves these pins by the "In a Ship run" section of
update-skills' SKILL.md.` The source repo is public, so the body carries skill
names and refs only: not this repo's name, nor anything else about it. Then:

```sh
$S/file-issue.sh --repo Gharib89/skills --title "Upstream drift: composed skills" --body-file <body> --label needs-triage
```

- `filed: true`: that is the drift issue.
- `filed: false`: the candidate titled exactly
  `Upstream drift: composed skills` is the drift issue. Rewrite its table in
  place, with a file holding the table alone, then write `Moving the pins` the
  same way from a file holding its one sentence (a section the issue lacks is
  added):

  ```sh
  $S/update-issue-body.sh <n> --repo Gharib89/skills --section Drift --body-file <table>
  ```

  With no candidate of that exact title, re-run `file-issue` with
  `--distinct-from` naming every candidate.
- Exit 1: the source repo is unreachable from here, which is every Azure
  DevOps repo without GitHub credentials. Print the answer's `command` for the
  owner, verbatim, and carry it to step 8. No retry.

### 8. Summary and PR

Commit the refresh, every setup-skills write and every retired-term edit. Run
the profile's `## Local gate` `Location:` from the worktree and keep its
`verdict`. The body takes the sections of the repo's PR template (the profile's
`## PR` `Template:`) in its order, or these headings where it has none; each
section carries the content below either way:

- `## Why the change`: one sentence naming the refresh.
- `## Change outline`: `Shape: none, mechanical (skills refresh).`, then:
  1. One version table, `| Skills | Move |`. A `source_skills` entry whose
     version moved reads `<old_version> → <new_version>`, a null `old_version`
     `new at <new_version>`. A `composed` entry whose `old_ref` differs from its
     `pin` reads `<old_ref> → <pin>`, and each skill step 5 took `<old_ref> →
     <head>`, as 7-character shas, each linked to
     `https://github.com/<source>/commit/<sha>`, a null `old_ref` reading
     `unpinned`. Skills with the same move share one row.
  2. **What changes for this repo**: a plain-words list of what a maintainer
     here now meets (an exit word renamed, a profile line to add, a refusal a
     run now makes), drawn from the changelogs and subjects, not restating them.
  3. **Repo-owned files**: the files the refresh changed outside the derived
     copies (each lock-listed skill's folder) and outside the lock itself, as
     this lists them:

     ```sh
     bash -c 'O=$1; shift; L=$(jq -er ".skills | keys[]" skills-lock.json) || exit 2; for s in $L; do set -- "$@" ":!.claude/skills/$s/"; done; git diff --name-only "$O" -- . ":!skills-lock.json" "$@"' _ '<old>'
     ```
- `## Special things to note`:
  1. `- Door: <one-way|two-way>. Blast radius: <one clause>.`, two-way unless
     setup-skills changed host state a revert does not undo.
  2. One line folding every empty outcome among other skills, upstream drift
     and unreachable upstreams, e.g. `- No other skills moved, no upstream
     drift, every upstream answered.` Each non-empty one gets its own line
     instead: an `unreachable` row as `drift not checked: <skill>: <error>`,
     drift as its rows, held at their pins in a consumer repo and moved in the
     source repo.
  3. The sections step 6 re-ran and the profile schema move, only when there
     are any.
- `## Needs attention`: the drift issue's link or step 7's printed command,
  every retired-term hit step 6 listed, a local gate `verdict` other than
  `pass`, every `setup-skills needed` line step 6 recorded, and any to-do left
  to the owner, one line each; `None.` when empty.
  The PR opens either way: the owner decides.
- `## Verification`: the last preflight's `reasons` (step 6's, else step 4's),
  the expected `worktree exists` reason, and the local gate `verdict`.
- `## Review`: `None.`: no reviewer loop runs here.
- `## Attribution`: the environment's footer, last.
- A bare `Closes #` line: dropped in a consumer repo, `Closes #<n>` in the
  source repo (step 9). Any other template section: what its comment asks for.

Between the last content section and `## Attribution`, one collapsed block per
`source_skills` entry whose version moved,
`<details><summary><skill> <old_version> → <new_version></summary>`: the
sections of the file at its `changelog` path above `old_version` up to
`new_version`, verbatim, breaking changes first. A null `old_version` is a skill
new to this repo: its version alone. A refresh whose new `changelog` carries the
**The renumber to 0.x.** note, where the old copy's lacked it, crosses that
renumber: the sections above `old_version` under the old numbers, then
the renumbered ones up to `new_version`. One more block holds each composed and
other skill that moved, with the upstream commit subjects that touched its
folder between the two refs; a null `old_ref` has no subjects.

The subjects are a read, not a gate: the folder is the lock's `skillPath`
without `/SKILL.md`, and the commits are those of
`https://api.github.com/repos/<source>/commits?sha=<new>&path=<folder>` whose
sha is among the `commits` of `.../compare/<old_ref>...<new>`, every page of
both read: ancestry, not date, since a merged branch brings commits dated
before the old ref. A read that fails writes "subjects unavailable" and goes
on.

Open it with `$S/open-pr.sh none --title "<subject>" --body-file <body>`, a
Conventional-Commit subject honouring the profile's `Subject constraints:`
(`chore(skills): refresh derived skills` where it has none), then
`$S/read-pr.sh <pr>`. Hand the owner the link, and
`.claude/skills/ship/scripts/cleanup.sh none` to run from the main checkout
after the merge, and stop: the PR merges the way the repo merges anything.

### 9. Source-repo mode

`mode` is `source`: this is Gharib89/skills, and each `drift` and `others` row
is a pin to move, in this one PR. It runs before step 7, which then files or
finds the drift issue this PR closes; steps 6 and 8 run unchanged. Per row:

1. Read what moved:
   `https://api.github.com/repos/<source>/compare/<from>...<head>`, `<from>`
   a `drift` row's `pin` or an `others` row's `old_ref`, the files under the
   skill's folder with their patches.
2. A `drift` row: re-add the skill at `#<head>` on its install line and move
   the pin on the `composes` line naming it (`skills/ship/SKILL.md` or
   `skills/setup-skills/SKILL.md`, the composing skill). An `others` row: run
   its `install` line. Either row: move the sha on every printed install line
   under `skills/` that installs it, splitting a line whose skills' pins part.
3. Judge the upstream diff for a **break**: for a `drift` row, a change breaking
   a reliance of the composing skill's prose on it; for an `others` row, a
   change to or removal of something this repo's own files (`skills/`, `docs/`,
   `CLAUDE.md`, `AGENTS.md`) name. A row that breaks is **held back**, with no
   prose reworked: re-run its install line at `#<from>` (a null `old_ref`
   restores its folder and lock entry from `<old>`), put `<from>` back on each
   line step 2 edited, and record `held back: <skill>: <reliance it breaks>`.

Then the refresh line, and `scripts/local-gate.sh`, whose `derived-copies` gate
holds every pin to the lock. A gate red at the new pins holds back the row whose
skill or folder its failing output names, or every moved row where it names
none, the failing gate as the reliance; then refresh and gate again. In step 8
the PR body opens with `Closes #<n>`, the drift issue step 7 filed or found, or
`Refs #<n>` with a row held back, and `## Needs attention` lists each `held
back` line. With every row held back, open no PR: hand the owner those lines and
run `$S/cleanup.sh none` from the main checkout. The title is scoped to the
composing skill, so the release run records the move in its CHANGELOG, or for
`others` rows alone to the skill whose printed line moved, else it reads
`chore(skills): move <skills> to <short sha>`. A pin moved on ship's `composes`
line breaks ship, since preflight refuses every consumer still at the old ref
(`skill off pin`). While ship is 0.x that grades minor: the title is
`feat(ship): move <skill> to <short sha>`, with no `!`, no `BREAKING CHANGE:`
footer in any commit, since `bump-guard` reads commits too, and no `major`
label. State the break in plain words in the commit body and under
`## Special things to note`. A pin moved on setup-skills' line or on a printed
line alone refuses nothing and takes no `!` either.

## In a Ship run

A Ship run cannot invoke this skill (`disable-model-invocation`), so on an
upstream-drift issue in the source repo it follows the steps below by hand, in
the worktree `isolate` made. `$S` and `$U` are as above. Steps 1, 7 and 8 are
Ship's: `isolate` is the worktree, the issue shipped is the drift issue step 7
would file, and phase 6 opens the PR with `Closes #<issue>` but for a hold-back.

1. `<old>`: `git rev-parse HEAD` in the worktree, before the first edit.
2. Step 2's source-repo refresh line, from the source repo's CLAUDE.md.
3. Step 3, with its source-repo token. A `heads` exit 1 is retried once, then
   stops the run `red-after-retry: heads`.
4. Step 9 per `drift` and `others` row, then its refresh line. The local gate
   is Ship's phase 5, where a red gate at the new pins is step 9's hold-back,
   not a fix-and-retry; step 9's title rule is phase 6's title.

A held-back row hands the issue back to the owner. With some rows moved, phase
6 runs `open-pr none --title <t> --body-file <f>`, `<f>` saying `Refs #<issue>`,
then `manage-issue <issue> handback "<reason>"` naming each `held back` line,
before the merge gate; `merge` takes `<pr> none`, `cleanup` keeps `<issue>`.
With every row held back there is no PR: hand back, `cleanup <issue>`, and stop.

Where a step would ask the owner, the run takes the conservative answer and
writes it to the Run file's deviations log, which lands in the merge summary:

| Step asks | The run records |
|---|---|
| Step 6, re-running `/setup-skills`, which interviews | not re-run; `setup-skills needed: <section or profile reason>` per item |
| Step 3, an `unreachable` row | `drift not checked: <skill>: <error>` |
