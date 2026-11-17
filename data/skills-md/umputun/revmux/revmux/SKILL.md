---
name: revmux
description: Run a supervised multi-agent code review by composing a task directory and driving the revmux CLI, then report or act on the findings it returns. revmux spawns and watches parallel claude and codex subprocesses with stall detection, retry, per-agent progress and a full run archive; this skill is the caller that writes the review context, launches it, reads the JSON back, and re-runs it after fixes. It also triages a filed issue, proposal or discussion instead of a diff, running a four-way panel over it — grounding, the case for, the case against, and cost — and putting the maintainer's six answers to him with the arguments behind each. It also has a self mode that reads what past rounds produced and tells the user what the record says about the review itself — which stage is filtering, which lens rates hardest, whether rounds converge — then proposes one change to the local prompt text at a time, with the number behind it. It fetches a pull request into a throwaway worktree, reviews it there and cleans up after. Also answers questions about revmux itself — profiles, lenses, task directories, flags, the JSON shape, exit codes and the run archive. Activates on "revmux", "run revmux", "multi-agent review", "supervised review", "review with revmux", "revmux this branch", "revmux the last commit", "revmux pr 123", "revmux this PR", "review PR 123 with revmux", "run a revmux round", "re-review after fixes", "revmux it and show me", "revmux this, I want to watch", "run it visible", "show me the review", "triage this", "triage issue 123", "is this worth doing", "should we accept this", "should I close this", "revmux self", "self-improve revmux", "tune revmux", "revmux profiles", "revmux lenses", "what does revmux return", "revmux exit codes", "revmux task directory".
argument-hint: 'optional: what to review ("pr 123", "issue 123", a ref, a path), plus "show me" / "focused" / "final" / "triage" / "loop" / "lenses a,b"'
allowed-tools: [Bash, Read, Edit, Write, Grep, Glob, Agent, AskUserQuestion, Monitor, TaskStop]
---

# revmux — supervised multi-agent code review

revmux spawns and supervises parallel `claude --print` and `codex exec` subprocesses, watches each for
stalls, retries what hangs, and returns findings on stdout.

It does no scope detection, no git, no PR fetching, no source modification. This skill does that half.

| this skill | revmux |
|---|---|
| resolve what is under review | supervise, stagger, retry, degrade |
| run git, gather context | compose and archive prompts |
| write `scope.md`, `goal.md`, `context/` | merge, dedupe, verify |
| choose profile, lenses, flags | return findings on stdout |
| read the JSON, present, fix, re-run | inject prior rounds |

## Activation triggers

- "revmux", "run revmux", "review with revmux"
- "multi-agent review", "supervised review", "parallel agent review"
- "revmux this branch", "revmux the last commit", "revmux the uncommitted changes"
- "revmux pr 123", "revmux this PR", a pull-request URL — the checkout half, `references/pr.md`
- "triage this", "triage issue 123", "is this worth doing", "should we accept this", "should I close
  this", an issue or discussion URL — the panel over a filed item, `references/triage.md`
- "another revmux round", "re-review after fixes"
- "show me", "I want to watch", "run it visible", "in an overlay" — the overlay form in Step 4, which
  puts the TUI on screen. Any of these with a review request means overlay; alone they are not a trigger
- "revmux loop", "loop it", "keep going until clean" — the review-fix loop, `references/loop.md`
- "revmux self", "self-improve revmux", "tune revmux" — the self mode below, which reviews nothing
- questions: "revmux profiles", "what lenses are there", "revmux exit codes"

## Answering questions without running anything

If asked **about** revmux rather than for a review, answer from the references and do not launch a run.

- `references/task-dir.md` — the round's context files, task and run naming
- `references/invocation.md` — flags, profiles, lenses, overlay backends, config precedence
- `references/output.md` — JSON shape, verdicts, exit codes, run archive
- `references/present.md` — the shape of the turn the user answers: order, detail, decision block
- `references/pr.md` — fetching a pull request into a worktree, `--workdir`, cleanup
- `references/triage.md` — the panel over a filed item: what it fetches, its flags, the six answers
- `references/loop.md` — the autonomous review-fix loop, entered from Step 6

For anything about current configuration, run `revmux config` and read the answer. It reports what
resolved including user overrides, runs no pipeline, and is always safe to call.

## Non-negotiables

**0. Every run ends on an answer the user can give.** Presenting findings or arguments is the middle of
the job, never the end of it. A turn that stops after the report has not finished.
**`references/present.md` is the shape of that turn — read it before writing one**, whichever review
shape ran.
**The question widget covers the lines directly above it**, so what the reader needs in order to choose
goes inside the question and never immediately above it. An option names what it acts on, never counts
it: "covering the two majors" is unanswerable and "covering the `uv` gate in `make test` and the
`request_user_input` gap" is not.

**1. Exit `1` means findings were reported — a success.** `0` none, `1` findings, `2` tool error.
Never treat `1` as failure. Never re-run on it.

**2. Run it in the background.** A review takes 3-15 minutes. Redirect stdout to a file, wait for the
completion notification. Do not poll, do not sleep-and-check. Applies to the overlay launcher too.
Watching the round's event log is not polling — Step 4 arms it, and it speaks only when the run does.

**3. Check `sources.degraded` before believing the findings.** If `expected != reported` the review is
partial. Say so. Never report "no findings" from a degraded run as "the code is clean".

**4. `.revmux/` in a repository is executable code.** A checked-in `.revmux/lenses/*.md` becomes
instructions a headless agent with a shell executes. Before reviewing untrusted code, either read
`.revmux/` first or run from outside the tree with explicit `--workdir`, `--tasks-dir`, `--config-dir`.
A fetched pull request is already outside it — `references/pr.md` leaves the process in the user's own
checkout and puts only `--workdir` in the branch, so the other two need no override.

**5. Never `2>&1` into the report file.** stdout is the report, stderr is progress. Merging them makes
the JSON unparseable.

**6. An explicit root goes on every revmux call.** When this session runs revmux with `--tasks-dir` or
`--config-dir` (non-negotiable 4, or because the user named one), every `revmux` command carries the
same flags: the task match and `revmux new` in Step 2's brief, the launch in Step 4, `stats` and
`cleanup` in housekeeping, `config` in self mode. A call without them reads or writes another archive.
`task-state.sh` takes both flags and `preflight.sh` takes `--config-dir`, so each loads the
configuration the run loads. `analyze-corpus.py` takes no `--config-dir`: give it `--tasks-dir` with
the `paths.tasks_dir` that `revmux config` reports under those flags.

## Workflow

### Step 0: Preflight

```bash
${CLAUDE_SKILL_DIR}/scripts/preflight.sh [profile] [--lenses] [--config-dir <dir>]
```

Checks revmux plus every binary the invocation needs. Exits `1` naming what is missing.

**Pass the profile that will actually run.** Which executors are needed comes from that profile's
roster, and with no argument preflight checks the resolved *default* instead — so a run under a
profile the default does not share a roster with is never checked at all, and degrades mid-review over
a CLI that was missing the whole time. If the user named a profile in any form, resolve it to an exact
name first — that is Step 3's rule, and nothing in it depends on the scope, so it can be applied here.
A word passed through unresolved fails preflight as an unknown name. If he named none, run it bare and
run it again once Step 3 has chosen one.

**Pass `--lenses` when the run will use it.** That flag replaces the roster with one agent on the
profile's own base runner, so the binaries needed are that base plus the stages, and none of the
roster's own. Checked as an ordinary run, a `--lenses` invocation can pass preflight and then have its
only finder fail to launch; checked the other way round, an ordinary run can be refused over a binary
it never touches.

If revmux is absent:

```
brew install umputun/apps/revmux                   # macOS
go install github.com/umputun/revmux/app/revmux@latest
git clone https://github.com/umputun/revmux.git && cd revmux && make install
```

**In a linked worktree, tell the user what that means, once a session.** It is one when the two
paths `git rev-parse --path-format=absolute --git-dir --git-common-dir` prints differ. Then say two
separate things:

- **Only when the archive is inside it** — resolve the `paths.tasks_dir` from `revmux config`
  (non-negotiable 6 flags included) with `realpath`, or its nearest existing parent with the missing
  part appended while it does not exist yet: revmux keeps symlinks in that path and git resolves them.
  It is inside when it equals `git rev-parse --show-toplevel` or starts with it plus `/`. Then say
  this task's rounds, at that path, are deleted when the worktree is removed, and self mode loses them. Keeping the worktree, or reviewing
  from the main checkout, is what keeps them. Offer no copy: it is a write outside this checkout.
- **Always:** Git does not copy the other checkout's untracked `.revmux/` files into a new linked
  worktree, so local config and prompt overrides may differ from the main checkout's.

### Step 0.5: Offer the project profile, once per repository

`revmux config`'s `paths.profile_fallback` is `./.revmux/profile.md` when the repo has one. Every round
without its own `input/profile.md` inherits it, and nothing creates it — not `revmux init`, not this
skill on its own. An empty field means every review here runs on generic calibration.

When it is empty, say so in one line and offer to write it. **Only ever with the user's yes**, and never
from the diff: read the project's own rules — `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/`, the
linter config — and write what the software is, what a real failure looks like there, the blast radius,
the reporting bar, and which conventions are deliberate. A profile guessed from one change is the thing
this file exists to replace.

Offer it once. If he declines, do not ask again in the session, and do not write a round-local
`input/profile.md` instead — that wins over the project file and is exactly the substitution the round
brief forbids.

**Never on a fetched pull request or any tree that is not his**: `.revmux/` is checked-in configuration,
so authoring one there commits a review standard to somebody else's repository.

### Step 1: Resolve what is being reviewed

| the user says | scope |
|---|---|
| nothing, on a feature branch | `git diff <base>...HEAD` |
| nothing, on master with uncommitted work | `git diff` and `git diff --staged` |
| nothing, on master and clean | `git diff HEAD~1` |
| "the last N commits" | `git diff HEAD~N` |
| "since <ref>" | `git diff <ref>..HEAD` |
| "pr 123", "this PR", a PR URL | `references/pr.md` — resolve, fetch into a worktree, review it there |
| "issue 123", "triage this", an issue or discussion URL | `references/triage.md` — the panel over a filed item, not a diff |
| a bare number, kind unnamed | probe pull request, then issue, then discussion — the first that resolves decides which of the two rows above applies |
| a path | that subtree, as a diff plus a read list |

Two commands here, and no more git than this:

```bash
git branch --show-current && git status --short
git diff <range> --shortstat
```

**The shortstat goes into the brief.** It is one line in this session and it is the whole of step 1 for
the subagent, which otherwise spends three to five git calls arriving at the same three numbers — and
they are the numbers Step 4's announcement is built from either way. Everything past the scale is still
the subagent's: the full diff, the file list, what is worth reading.

**Two rows in the table above are not a single range, so the one command does not cover them.**
Uncommitted work on master is `git diff --shortstat` *plus* `git diff --staged --shortstat`, and the
scale handed over is the two added together — a bare `git diff --shortstat` reports nothing at all when
the work is fully staged. A path scope has no range: hand over the file count instead, or hand over
nothing and say so. Do not hand a number the commands in `scope.md` contradict, since the brief makes it
binding — "take the scale as given rather than measuring it again".

**A pull request is a different shape, not a harder ref range.** revmux fetches nothing and checks
nothing out, so a PR has to be on disk before there is anything to review, and the checkout has to be
removed afterwards. Read `references/pr.md` and follow it — it covers steps 1 through 4 for that case
and hands back here at Step 5.

**A filed item is not a change at all**, so there is no range to measure and nothing for Step 2's brief
to read: it reads a diff and returns a shortstat, and a triage has neither. `references/triage.md`
**replaces Step 2 entirely** — it fetches the item, its thread and the author's history into `context/`,
writes the round, and hands back here at Step 5. A bare number goes through the probe in the table
above first; a number that turns out to be a pull request is `pr.md`, whatever the user called it.

Ask only when genuinely ambiguous — a feature branch with uncommitted work is the standard case. Use
AskUserQuestion, here and at the headless-versus-overlay choice in Step 4. **The question is always
this session's, never a subagent's**: a subagent cannot ask, and one that guesses reviews the wrong
thing at full cost.

### Step 2: Prepare the round — in a subagent

Everything between the resolved scope and a round ready to run is delegated: reading the diff,
matching the task, opening the round, and writing its context files. That is a dozen tool calls and
several screens of diff whose output answers nothing the user asked — and it buries the review it is
preparing for.

**It is also the wait the user sits through before the review starts, and the wait is generation.**
Measured over eight archived rounds it ran 65 to 156 seconds, and the wall-clock tracked output tokens
at a flat rate across all eight — so what makes it slow is prose written and turns taken, not tool
latency. The budgets and the prohibitions in the brief are load-bearing for that, not tidiness.

**Expand every path before handing the brief over.** The subagent does not have this skill loaded, so
`${CLAUDE_SKILL_DIR}` means nothing in its shell — substitute the resolved absolute path into the brief's text
rather than passing the variable through, or its `task-state.sh` step silently runs nothing.

**Say one line first, then spawn it:** `Preparing the round for <what is being reviewed>…` — the
subject in the user's own terms, "the branch against master", "PR 123", "the last 3 commits". Then
nothing further until the subagent returns: a delegated step the user was told about reads as work in
progress, while an unannounced pause reads as a stall.

Spawn **one** `general-purpose` agent. Hand it the resolved scope from Step 1 and this brief:

> Prepare a revmux review round. Write files; change no source, run no review, commit nothing.
>
> Every `revmux` command below, and `task-state.sh`, carries `<this session's --tasks-dir/--config-dir
> flags, or "no extra flags">`.
>
> **Write nothing outside the tree this session may write to, `revmux new` included.** If a guard
> rejects only how a command is written and names a compliant form of the same operation inside this
> tree (split it, quote it, run the plain command), follow that form once. Any other refusal, or a
> second refusal of the same operation, ends the preparation: put its text in `notes` and return. Do
> not retry it through another tool, a shell redirect, an API or a symlink.
>
> The scope is: `<the row resolved in Step 1, with its ref range>`, and its scale is
> `<the shortstat Step 1 printed>`. Take the scale as given rather than measuring it again.
> Exclusions the user has stated: `<list them, or "none">` — write these under the scope's
> explicit exclusions. They are decisions already taken, and the diff cannot show you one.
>
> 1. Read the change: the diff for that range, once, and the file list. That is the whole of the
>    exploration. Do not read source files in full, do not grep the tree, and do not run a further diff
>    per directory — naming a file worth reading is the reviewing agent's instruction, not a claim to
>    verify first, and the round exists because four of them are about to read it properly.
> 2. If this session handed you a task id, use it verbatim and go to step 3. Otherwise match an
>    existing task before minting one — a second id for one subject runs as a first round
>    with no history. `revmux config | jq '.paths.tasks'` lists them with `id`, `description`, `url`,
>    `branch`, `base` and `rounds`. Match on `url` or `branch` exactly, failing that on `description`
>    against the subject in hand, and reuse the matched `id` verbatim. Derive one only when nothing
>    matches: `pr-<number>`, `issue-<number>`, a branch name with `/` replaced by `-`,
>    `since-<short-sha>`, or `wip-<branch>`. No path separators, no `..`, no leading dot, not absolute.
> 3. Run `<the absolute path this session resolved for scripts/task-state.sh> <task-id>`, with the
>    flags named above when there are any. It exits 1 with a usage line without an id. It validates the
>    id and reports the `task.md` anchors, every round, and each round's `input/` state — `prepared` (never reviewed),
>    `claimed` (a review started and never finished) or `ran`. That is the inventory; do not `ls` the
>    task or a round to confirm what it already told you.
> 4. Name the round `NN-label` — `01-initial`, `02-after-fix`, `03-final` — with `NN` one past the
>    highest already there, and do not mix vocabularies across rounds of one task. Then
>    `revmux new --task <id> --run <NN-label>`, exactly as written and with no `--help` run before it.
>    It prints the absolute path of every file to write plus which of them it created.
> 5. Write to those paths and no others. Never join a path, never create a directory the output did
>    not name, and never write over an existing `scope.md` without reading it first. The one
>    exception is `context`, a directory the output names but does not create: write files inside it.
>    **Every file below is bullets, paths and command blocks — never paragraphs of prose.** Every agent
>    in the roster reads them and then reads the diff itself, so anything the diff already says is length
>    paid for twice, and writing it is most of what this round costs in wall-clock.
>    - `scope` — required, and **under 1500 characters**. What changed, the commands to see it, its
>      scale, which files to read in full, what to ignore. Write commands in plainest form:
>      `git diff master...HEAD`, never `git -c core.pager=cat diff ...` — a leading option defeats the
>      child's permission matching.
>    - `goal` — optional, and **under 1000 characters**. What the change is for, plus a "this is
>      correct only if…" list. **When the round is the last one before the branch merges, make it the
>      gate**: say the round exists to answer whether anything in this diff should not ship, and name
>      what qualifies — a defect in executable code, a change to a prompt, schema or shipped script
>      that would make a later run wrong, or a contradiction that would mislead an agent executing the
>      document. Say that finding nothing is a valid answer, or the round reads as owing findings and
>      manufactures them.
>    - `profile` — **do not write it.** What it holds is about the repository rather than this round, so
>      it lives in `./.revmux/profile.md` and revmux gives every round without a non-empty override the same one
>      with nothing copied forward. You see the diff and the file list, which is not enough to state a repo's conventions,
>      and a generated file here wins over the project's and silently replaces it.
>      Write it only when the user says this subject needs a different bar than the repo's.
>    - `context` — optional. Ticket text, design notes, commit list. Its path is a directory that is
>      reported but not created: create it, then write one or more files inside it
>      (`context/notes.md`). Never write the path itself as a file; revmux refuses the round.
>    - `task_file` — when `created` lists it, and also when it is already there but still the unfilled
>      template with every anchor empty. Read it first either way. `description`, plus `url`, `branch`
>      and `base` when known: that front matter is what the next session matches on, and a task.md left
>      as the blank template is what makes the next session mint a duplicate id.
> 6. Stop at the last write. A failed write returns an error, so there is nothing to confirm afterwards
>    — no `ls`, no `diff`, no second `task-state.sh`, no `git status`.
>
> **Do not read the previous round's `scope.md`, `goal.md` or `context/`.** revmux injects every prior
> round into every composed prompt itself, so reading them buys nothing and anchors this round's scope
> on the last one's wording. No round's `profile.md` is read either: the project file revmux resolves is not one of these.
>
> Return JSON only: `{"task": "", "run": "", "round_dir": "", "scope_path": "", "wrote": [],
> "files_changed": 0, "insertions": 0, "deletions": 0, "areas": [], "notes": ""}`. `areas` names the
> parts of the codebase the diff touches. Put anything that went wrong in `notes` and do not paper
> over it.

Read `references/task-dir.md` yourself only if the subagent reports something it could not resolve.

**Nothing else moves into a subagent.** The profile choice, the launch, the report and how it is
presented all stay in this session — they are the decisions the user is waiting on, and a summary of
a decision already made is not the same thing.

**Check what comes back before launching.** A missing `round_dir` or an empty `wrote` means no round
is ready and the run would fail on a missing scope; fix that here rather than launching into it.
**An unresolved refusal in `notes` blocks the launch even when `wrote` is not empty**: the round holds
only part of its context. A command-form retry that went through is reported there too and blocks
nothing. Tell the user what was refused and where, and launch nothing until it is resolved. The
scale numbers are what Step 4's one-line announcement is built from.

### Step 3: Choose profile and flags

| profile | roster | when |
|---|---|---|
| `comprehensive` (default) | `bugs+impl`, `arch+quality`, `docs+tests`, codex peer | real change, real risk |
| `focused` | one `bugs` agent plus codex peer | small or time-boxed |
| `final` | `bugs+impl` plus codex peer, nothing below major | pre-merge |
| `claude-only` | the same four lens splits, all on claude | no codex available |
| `codex-only` | the same four lens splits on codex, and synthesis and verify with them | no claude available |
| `grill-me` | `bugs+impl` and `architecture+quality`, each once on claude and once on codex, all reading against the change | the user wants it torn apart |
| `expert` | two agents at xhigh, codex `gpt-6-astra:xhigh` and claude `fable:xhigh`, each carrying all eight lenses | a plan, or a change nobody wants to get wrong. Slow and expensive; pick it when he says so, not by default |
| `triage` | `facts` (grounding + precedent), `thesis`, `antithesis`, `cost` on codex | a filed item rather than a diff; needs `--no-synthesis --verify-group-by source`, `references/triage.md` |

**Never choose `expert` on your own.** It is two agents at `xhigh` each applying every lens, so it costs
several times what `comprehensive` does, and no property of the subject justifies reaching for it — not a
plan, not a large diff, not a risky one. Pick it only when the user asked for it in words, and say that
is why. Every other profile reviews whatever it is pointed at, a plan included; `expert`'s severity bar
is simply written so a proposal reads as naturally as a diff.

**A profile word is not a profile name.** Map whatever the user said onto the profiles `revmux config`
reports, matching the name first and the `description` second. revmux rejects an unknown `--profile` at
load and never guesses, so resolving is this skill's job — passing his word through unresolved just
fails the run.

| the user says | profile |
|---|---|
| full, everything, deep, thorough, the works | `comprehensive` |
| short, quick, fast, light, small, time-boxed | `focused` |
| last, pre-merge, before merge, strict | `final` |
| claude only, no codex, skip codex | `claude-only` |
| codex only, no claude, codex alone | `codex-only` |
| grill me, tear it apart, be brutal, no mercy, adversarial | `grill-me` |
| expert, best models, highest effort, spare no expense, use astra and fable | `expert` — and only on words like these, never inferred from the subject |
| triage this, is this worth doing, should we accept this, should I close this | `triage`, and the subject is a filed item rather than a diff — `references/triage.md`, which owns the flags it needs |

Examples, not the list. Match on intent — breadth wants `comprehensive`, speed wants `focused`, a merge
gate wants `final` — and read the resolved catalog rather than this table, since a user with his own
profiles has names it does not carry. Name the profile picked and the word it came from. Ask only when
two are genuinely close, as "quick, before I merge" is between `focused` and `final`.

`--lenses a,b` produces **one** agent carrying both lenses and drops the codex peer, losing every
cross-source confidence boost. Prefer a profile unless narrowing is specifically wanted.

Also useful: `--min-confidence=70` for actionable-only, `--no-verify` when a human reads everything.

### Step 4: Run it — headless or overlay

Both return the same report on stdout and the same exit code.

**Headless — the default:**

```bash
revmux --task <id> --run <name> --no-tui > /tmp/revmux-<id>-<run>.json 2> /tmp/revmux-<id>-<run>.log
```

Launch in the background, wait for the notification.

Reviewing a fetched pull request adds `--workdir <worktree>` and changes nothing else — including that
the command is still run from the session's own checkout, which is what keeps the archive out of the
directory the cleanup deletes. `references/pr.md` has the reasoning.

**Before yielding, tell the user three things** — otherwise they sit for 10+ minutes with no signal:

1. what is running (task, profile, roster size) and the rough duration
2. the stderr log path, and that `tail -f <path>` shows live per-agent progress
3. that they can ask for status any time

On a status request, read the tail of the stderr log and `events.jsonl` in the round directory. Report
the stage, which agents are active, and elapsed. Never guess.

**Then arm the progress feed, before yielding — headless only.** A `Monitor` over the round's own
`events.jsonl`:

```bash
tail -n +1 -F <round_dir>/events.jsonl \
  | grep -E --line-buffered '"kind":"(stage|agent_started|agent_done|agent_retried|agent_degraded|dropped|rate_limit)"'
```

`timeout_ms` of `1800000` and `persistent` false, and `TaskStop` it when the run's own completion
notification arrives — `tail -F` never ends by itself. `references/invocation.md` says why those seven
kinds and not the log.

**Speak at most once a minute, and only about what happened.** Fold every event since the last relay
into one short line — the stage that opened, the agents that started or finished — rather than one
line each: a roster launches four agents within seconds of each other, and four consecutive messages
saying so is the same noise from the other direction. A retry, a degrade or a rate limit goes out when
it arrives instead of waiting for the minute; those change what the user would do next.

**Never report a quiet interval.** No heartbeat, no "no change since the last check", no restating a
milestone already relayed — a feed that speaks when nothing happened is the one the user turns off.
The monitor is woken by the file, so silence costs nothing and needs no announcing.

**The feed belongs to this form alone.** It exists because a headless run says nothing for ten minutes
and the user has no other signal. An overlay run is that signal, on screen, live.

**Overlay — when the user wants to watch:**

```bash
${CLAUDE_SKILL_DIR}/scripts/launch-revmux.sh --task <id> --run <name> [any revmux flag]
```

Detects the terminal (agterm, tmux, zellij, herdr, kitty, wezterm/kaku, cmux, ghostty, iTerm2, Emacs
vterm), runs revmux with its TUI in an overlay, returns the report on stdout. Under agterm: floating
panel at 80% of the pane, or a pane overlay when the session is split, which leaves the sibling pane
live. Either shape is tinted blue. Do not pass `--no-tui`; the script rejects it.

- it blocks for the whole review, so background it and wait for the completion notification
- **no progress feed, and none of the three-things announcement.** The TUI is the progress feed: a
  `Monitor` here narrates in prose what the user is already watching render, once a minute, and the
  three lines about `tail -f` point at a log he does not need. Say what is running in one line and
  yield.
- **its exit codes: `0`/`1`/`2` are revmux's, `3` is a launcher failure, `127` is revmux not
  installed.** A `3` means no review happened — that is the one to retry.
- overrides: `REVMUX_AGTERM_PERCENT` (80, and forces the floating panel in a split),
  `REVMUX_POPUP_WIDTH`/`HEIGHT` (90%), `REVMUX_AUTO_EXIT`
  (30s; `0` waits for the reader to quit), `REVMUX_TMUX_WINDOW=1` for a disconnect-resilient tmux window

**Choose headless** unless the user asked to watch or is clearly at the terminal.

**If the launcher dies after a run completed, the report is not lost** — it is in the round directory
as `findings.json` and `report.md`. Read from there rather than re-running. A killed run wrote no
report, and most `2`s wrote none either — but the report reaches stdout only after the round is
archived, so a `2` whose stderr names a failure writing it leaves a complete round. Check the round's
`manifest.json` for content before re-running.

`--run` is required. A round that has already run is an error, not an overwrite — but a round whose
review never finished is not one of those, so a retry after exit `2` reuses the same name and the same
`input/`. That holds only while the dead review wrote nothing into the round, which is narrower than it
sounds: the pipeline opens `events.jsonl` as its first act, so anything interrupted after it started is
refused under its own name, and the answer is a new round with the `input/` copied across. It may not
be named `task.md`.

### Step 5: Read the result

Read `references/output.md` for the full shape.

1. **Exit code.** `2` means nothing usable — read the stderr log, which names the cause. If that cause
   is a failure writing the report to stdout, the round is complete and its `findings.json` is on disk;
   read it. Otherwise fix the cause and re-run: the same `--run` while that round holds nothing but its
   `input/`, a new round with the `input/` copied across once revmux refuses the name. `0` and `1` both
   completed.
2. **`sources`.** Non-empty `degraded` means partial; lead with that.
3. **`findings`.** Group by severity.
4. **`open_questions`**, **`pre_existing`** and **`immaterial`** — report each separately.

`sources` holds **agent names** and is the only evidence of independent corroboration. `lenses` holds
lens names and is informational. One agent flagging under two lenses is still one source.

### Step 6: Present, then propose

**Read `references/present.md` now, and write the turn to its code-review skeleton.** It carries the
order of the turn, the one law of detail, the decision block and the rules for the question itself.
The shape of the turn is defined there and nowhere else; what follows here is only what a code review
adds to it.

**Tag every finding with its surface and severity in one bracket before the title:** `[code, minor]`.
The first value is the surface: `code` for executable logic, `comments` for a comment or doc comment
inside a source file, `docs` for a project document, `tests` for test code, or another lowercase word
when none fits (`config`, `build`). revmux returns no surface field, so derive it from `file` and what
the body argues: a `.go` path whose body is about stale godoc is `comments`, not `code`. The second
value is the finding's exact `severity` field. Never omit either value or split them into separate
tags. Format the heading `[surface, severity] Title — file:line, conf N`.

Carry the same combined tags into the counts. "3 findings" says nothing about where the risk is;
"2 [code, major], 1 [docs, minor]" does.

Actionable is `findings` alone — what revmux kept. Report the other three, and keep them out of the
count: `immaterial` is real and judged not worth the fix, `pre_existing` is real and not this change's,
`open_questions` wants a decision rather than an edit.

Recommend the option that fits the outcome:

| the run came back | recommend |
|---|---|
| `sources.degraded` non-empty | re-run the missing source first — a partial review's silence is not evidence, so nothing else is worth deciding yet |
| any `critical` or `major` | fix those, then a new round on the same task — or the loop below, if the user wants it run to the end |
| `minor` only, verdicts not `unverified` | fix now, or note for later — verification weighed each fix's cost against its consequence, so what is left is a question of timing |
| `minor` only, verdicts `unverified` | say nothing was checked, and weigh each one before acting — `--no-verify` drops nothing and produces no `immaterial` list |
| `open_questions` non-empty, no findings | answer them — they are decisions, and the review found nothing to edit |
| nothing actionable | done, and `--profile final` if a merge is next |

Rows are tried in order and the first match wins, so a degraded run outranks whatever it did report.

Put it as an AskUserQuestion, the recommendation first and marked `(Recommended)`.

**Never start fixing because the findings look clear.** A review produces findings; editing is a
separate decision, and this is where the user makes it.

**Offer the loop as a third way out of that question**, alongside stopping and fixing-then-one-more-round:
review, fix, commit, re-review, until a round comes back with nothing gating. It is for the user's own
branch, never a fetched PR, and it commits without pushing. `references/loop.md` is the whole procedure —
read it when he picks it, not before.

Once he answers with anything other than another round, run the archive check below.

### Step 7: Fix and re-run, if asked

1. Agree which findings to act on. An `immaterial` verdict means revmux already dismissed it — it is in
   its own list, not in `findings`. A `rejected` one appears nowhere at all: the verifier judged it not
   real and dropped it, so only the archive's stage snapshots still hold it.
2. Make the fixes.

**Before committing a fix, do these three checks, in this order.**

**1. Sweep for the shape, not the site.** Name the defect the finding demonstrates as a *construct* —
"a switch over a three-value enum that only tests one end", "a sentence asserting a shape regardless of
the counts", "a phrase that must match a list beside it" — then grep the repo for that construct and fix
every occurrence in the same commit. Grep for the pattern rather than the literal string: a phrase
wrapped across a line break survives a search for the phrase.

This check exists because the other two cannot catch what it catches. Three times in one archived task
a fix landed at the site the finding quoted and left the identical defect elsewhere — once in a file
the same commit was already editing, once in the file beside it, and once **four lines below, inside
the same diff hunk**, in a commit whose own message stated the general rule. Knowing the rule does not
substitute for running the search.

**2. Enumerate what you touched.** Name the input space of the thing you changed and confirm every
member is handled *and* that a test tells them apart:

- an enum or a set of string constants — every value, and every transition between them if direction
  matters
- a struct being folded, copied or serialized — every field, not the ones the change was about
- a platform, a filesystem or an executor the code branches on — each branch
- an error class the code distinguishes — absent, unreadable, malformed, present-but-empty
- a ratio — that the numerator and the denominator are drawn from the same population

The recurring failure is not carelessness on many fronts. It is writing the fix for the case that
prompted it and a test pinning that same case, so the test cannot catch what was left out.

**3. Re-read the finding, then read your fix against it.** Fix the mechanism the finding names, not the
example it happens to use to illustrate it. A finding that says "the switch cannot express a change that
skips `minor`" is not answered by adding one more case to the switch.

Then run the tests and the linter. A fix that breaks the build is not committed.
3. Open the next round on the same task and write its own `scope` — the fixes and the range they land
   in. **That is Step 2's subagent again**, with the same one-line announcement, the task id it
   already returned, every exclusion the earlier rounds carried, and a fresh `--shortstat` for the
   fixes, so a re-review costs the session no more
   output than the first round did — and the brief's step 2 is skipped outright, since the id is not in
   question on a round of a task that already has rounds. Then run it:

```bash
revmux --task <id> --run 02-after-fix --profile <picked> --no-tui \
    > /tmp/revmux-<id>-02-after-fix.json 2> /tmp/revmux-<id>-02-after-fix.log
```

revmux injects the prior rounds itself. **Do not paste prior findings into the scope** — it
duplicates the injection and anchors agents on conclusions they should re-derive.

A pull request re-reviewed after the author pushed is fetched again first, and carries `--workdir`
again: `references/pr.md`, step 6.

**Pick this round's profile from what the fixes touched, not from the round number.** A re-review is
not automatically smaller: round 1's findings may have been fixed by a redesign, and a narrower roster
cannot catch a regression in an area its lenses do not cover.

| the fixes were | profile |
|---|---|
| contained edits inside what round 1 flagged | `final` — `bugs+impl` is the fix-confirmation shape, and it reports nothing below major |
| spilled into tests or structure **the review has not seen** | `comprehensive` — that surface is genuinely new |
| documentation only | `final` — a doc fix is new prose, and `comprehensive` would review it |
| time-boxed, correctness only | `focused` |

**Default to `final` and make `comprehensive` argue for itself.** Across the archived rounds, roughly three quarters of
everything found is `minor` and minors never converge — they arrive at roughly three a round whatever
the gating count is doing, including on rounds where gating had already been zero twice over. `final`
reports nothing below major, and the re-review rounds run under it produced the shortest actionable
lists in the corpus. A fix that touched a test file is not by itself a new surface; the row above wants
a surface the review genuinely has not looked at.

The round-2 failure worth spending a roster on is a fix that does not address the finding, or addresses
it in the wrong place. That is the `impl` lens, which `focused` does not carry — so a re-review narrows
to `final` rather than to `focused`.

Documentation is the one surface a re-review does **not** widen to cover. Every other spill is code the
round before never looked at; a doc fix is a sentence this loop just wrote, and running the `docs` lens
over it produces a finding about that sentence round after round while the code stands still.

Put it as an AskUserQuestion, the matching row first and marked `(Recommended)`.
Never narrow the roster silently: a user who does not notice gets a smaller review than the one he
thinks he asked for. Skip the question when he named a profile himself.

## Archive housekeeping

Every round keeps each agent's verbatim stream, so the archive grows by roughly half a megabyte per
round and revmux prunes nothing on its own. Check it once a session, after the last round is presented —
never between rounds, and in loop mode only after the loop exits.

```bash
revmux stats
```

`totals.size_mb` is the whole archive. Under **20MB**, say nothing and move on: disk has no place in a
report about findings. Over it, propose getting back to roughly **10MB**.

The proposal is oldest first by `last_run`, whole tasks, and never the task this session reviewed. Each
`tasks` entry carries the `id`, `description`, `rounds`, `size_mb` and `last_run` a choice is made from.

**A task with no `last_run` at all is not the oldest — it is undated**, and sorting it first offers up a
task whose rounds never completed ahead of ones that did. Order those by `id` after the dated ones, and
say in the option that they carry no completed round.

Put it as one AskUserQuestion before anything is removed:

- the oldest tasks that together get under ~10MB as the first option, marked `(Recommended)`
- the single largest task as a second option, when the first is not already just that task
- keeping everything as the last option

Every option names the megabytes it frees and, for each task it removes, that task's `description` and
`rounds` — an option that says only "clean up old tasks", or names ids without saying what they
reviewed, is not a choice the user can weigh.

**Say what is lost in the question itself:** a removed task takes its rounds with it, so `revmux stats`
and self mode's corpus both shrink by that much evidence.

Then remove exactly what he picked, one call per task:

```bash
revmux cleanup --task <id>
```

It removes that task and prints what went. It is the only thing in revmux that deletes anything, and it
deletes only the task it is named: a path, a round name or a typo is an error that removes nothing, and
a task a running review still holds is refused. Never remove a task directory any other way, and never
widen the set he chose.

## Debugging a review that looks wrong

The archive is the round directory `revmux new` reported, beside the `input/` it was run against:

| question | where |
|---|---|
| why did this agent report nothing? | `agents/<name>.jsonl` |
| did an agent stall or get retried? | `events.jsonl`; a `<name>.retry.jsonl` means it did |
| did synthesis drop something? | `stages/1-found.json` vs `2-synthesized.json` |
| did verify reject wrongly? | `stages/2-synthesized.json` vs `3-verified.json` |
| what was this agent asked? | `prompts/agents/<name>.md` |
| which lens text, from which layer? | `manifest.json` |

## Self mode — tune the configuration from the record

Triggered by "revmux self", "self-improve revmux", "tune revmux". **It reviews nothing**: no round is
opened, no agent is spawned, and the code in the working directory is never read. It reads what past
rounds produced and proposes changes to the review configuration itself.

**Your job is to hand him conclusions and one concrete change. Not a dashboard.**

### Step S1: Run the analysis

```bash
${CLAUDE_SKILL_DIR}/scripts/analyze-corpus.py
```

It walks the archive and prints numbered conclusions with the numbers behind each, then the tables they
rest on. Read-only, runs no model, safe during a review. `--tasks-dir` points it elsewhere; `--json`
gives the full measurements if you need to reason past what it printed.

**Do not re-derive any of this by hand.** The script encodes readings that were got wrong the first
time — verification looking inert because reclassification is invisible in stage in/out, `tokens`
meaning different things per executor, per-agent rounds being over-counted. Ad-hoc `jq` over the
archive reproduces those mistakes.

Then, for what a proposal would edit rather than what the review did:

```bash
revmux config > /tmp/revmux-config.json
```

**Propose against that, never against the shipped defaults.** A user with his own `comprehensive.md`
runs a roster this skill has never seen.

### Step S2: Decide where the change would be written

**`./.revmux/` and nowhere else.** Never `~/.config/revmux/`, which is the user's cross-project layer.
Never the embedded tree, which is inside the binary — unless the working directory *is* the revmux
repo, where the lens and profile text ships from `app/prompt/defaults/` and a local override would fork
it from what ships.

**Only the file the change edits goes there, and only once he says apply.** Prompt files resolve one
file at a time, so a file absent from `./.revmux/` keeps following the shipped text as revmux upgrades.
`revmux init` writes every resolved file, which freezes the whole tree at this version to change one
file of it — never run it here.

The path is the file's place in the prompt tree, `lenses/<name>.md` or `prompts/profiles/<name>.md`.
If `./.revmux/<path>` exists, edit it in place. Otherwise copy the text that resolves today — the
user layer's file when it has one, the embedded one when not — and edit the copy:

```bash
f=lenses/adversarial.md   # the file the change edits
if [ ! -e ".revmux/$f" ]; then
  mkdir -p ".revmux/$(dirname "$f")"
  if [ -e "$HOME/.config/revmux/$f" ]; then
    cp "$HOME/.config/revmux/$f" ".revmux/$f"
  else
    d=$(mktemp -d /tmp/revmux-defaults.XXXXXX) && revmux --dump-defaults "$d" && cp "$d/$f" ".revmux/$f"
  fi
fi
```

`--dump-defaults` skips any file already present, so it goes into a new empty directory every time; a
reused one can hold superseded text. When `.revmux/` is tracked in git, say so if he hesitates:
`git checkout` reverts anything he regrets.

### Step S3: Say what it found, briefly

Lead with the conclusions the script printed, in your own words, **two or three sentences each**. Cut
any the user cannot act on. Do not paste the tables — they are there for you, and he asked what to do,
not what the numbers are.

State the sample size once: "24 rounds over 7 tasks, all on this codebase" is a caveat he can weigh.

**Quote a per-lens number only with the ambiguity beside it**, which the script's own last table shows
and `revmux stats` reports as `ambiguous`: a
finding's lenses are model-supplied, and an agent carrying two lenses often names both. A lens whose
ambiguous share is most of its raised count cannot carry a suggestion on its own — report it and propose
nothing. The script's own per-lens demotion column is already narrowed to findings naming a single lens,
for the same reason.

**If the script says the corpus is too thin, stop there.** That is a real answer. Inventing a
suggestion from four rounds is worse than saying there is nothing yet.

### Step S4: Propose one change

One. The most supported, with:

1. **what to change** — `./.revmux/<path>` as Step S2 describes it, and the edit in concrete terms
2. **the number behind it** — the one the script printed, quoted
3. **how you would know it worked** — the measurement that moves if it did, on the next round

Then AskUserQuestion: apply it, skip it, or stop. Act on the answer, then offer the next one the same
way. Stop when he says stop or the conclusions run out. Never batch edits, never apply one unasked.

**A conclusion is not automatically a change.** Several are worth knowing and not worth acting on —
say so and move on rather than manufacturing an edit to go with each.

## Example sessions

```
User: "revmux this branch"
→ preflight.sh → all present
→ git branch --show-current + git status --short → on tui-rework, clean
→ git diff master...HEAD --shortstat → 22 files, +840/-310, handed to the brief as the scale
→ "Preparing the round for the branch against master…"
→ one subagent: reads the diff once, matches no existing task, derives `tui-rework`, opens
  01-initial, writes task.md/scope/goal → returns round_dir, wrote[3]
→ revmux --task tui-rework --run 01-initial --no-tui > /tmp/…json  (background)
→ tell user: ~9 min, tail -f /tmp/…log for live progress
→ Monitor on <round_dir>/events.jsonl, milestone kinds only; one folded line a minute, silence between
→ exit 1, sources 4/4, degraded []
→ 6 findings: 1 major, 5 minor; 2 corroborated across bugs+impl and adversarial
```

```
User: "fix the major one and run it again"
→ fix applied
→ "Preparing the round for the fixes…" → same subagent, handed task `tui-rework` and the fixes'
  shortstat so it neither matches a task nor re-measures; opens 02-after-fix and writes its own
  scope; the profile is the repo's and revmux resolves it
→ revmux --task tui-rework --run 02-after-fix --no-tui
→ exit 0, nothing above threshold
```

```
User: "revmux the branch, I want to watch it"
→ subagent prepares 01-initial and returns its paths
→ launch-revmux.sh --task tui-rework --run 01-initial > /tmp/…json  (background)
→ agterm: split session, so a pane overlay on the agent's own pane, TUI live, self-closes 30s after the report
→ no Monitor and no status lines: he is watching it
→ same JSON, same exit code, Step 5 onward identical
```

```
User: "revmux pr 123"
→ preflight.sh → all present
→ gh repo view → umputun/revmux; gh pr view 123 → head `feature/oauth`, base master, +410/-95, 12 files
→ revmux config → .paths.tasks has no entry with that url; derive `pr-123`
→ git fetch origin pull/123/head:revmux-pr-123; git worktree add /tmp/revmux-pr-123 revmux-pr-123
→ merge-base origin/master revmux-pr-123 → 4ed3259
→ subagent opens pr-123/01-initial and writes task.md (url, branch, base), scope, goal, context
→ revmux --task pr-123 --run 01-initial --workdir /tmp/revmux-pr-123 --no-tui > /tmp/…json  (background,
  from the repo root — the archive belongs to it, not to the worktree)
→ exit 1, 4 findings; report them
→ git worktree remove /tmp/revmux-pr-123 --force; git branch -D revmux-pr-123
```

```
User: "what lenses does revmux have?"
→ no run; `revmux config`, report .lenses[] with descriptions
```

```
User: "revmux self"
→ analyze-corpus.py → 24 rounds over 7 tasks, five numbered conclusions
→ say three of them in a sentence each: verification demotes 21 and rejects 2, so it is a severity
  corrector; adversarial rates 61% major+ and holds most of the attributable demotions; three quarters is minor
→ revmux config → the roster actually running
→ propose one: the adversarial lens's severity text, quoting the 61%, measurable by whether the
  demotion count falls next round
→ AskUserQuestion: apply / skip / stop. Then the next one, or stop.
```
