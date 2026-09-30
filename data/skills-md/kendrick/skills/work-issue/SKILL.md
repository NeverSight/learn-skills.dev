---
name: work-issue
description: "Advance one GitHub issue from its approved plan to a pull request whose review threads are answered, resuming from wherever a previous invocation left it. Use when one issue has an approved plan and should be built, published, and its review threads answered, or when an orchestrating skill runs one issue as a lane. It never plans an issue and never merges one: to plan, use writing-plans; to run a plan that has no issue, use divvy-up."
argument-hint: '<issue number or URL> [plan path] [--isolate | --no-isolate] [--deep] [--max-review-rounds N] [--dry-run]'
---

# work-issue

`divvy-up` ends at its Step 7 with a green verify and an assembled diff. Everything after that point is the tail nobody wrote down: reproducing the worker's claims with something that did not author them, rebasing, pushing, opening the pull request, reading what an external reviewer said about it, repairing what is in scope, queueing what is not, and answering every thread. Held in one session's memory, that tail gets re-derived from scratch each time and loses the same things in the same order.

One invocation advances one issue to its next gate and stops. The run's state lives on disk rather than in the conversation, so a session that ends mid-run resumes by typing the same command again, and a second issue worked at the same moment is refused at the gate rather than discovered as a rebase conflict four steps later.

Four siblings do the work this skill does not: `divvy-up` derives and dispatches the waves, `code-review` reads the assembled diff against the issue, `adversarial-review` fires on the diffs that earn it, and `technical-writing` writes every commit message, pull-request body, and thread reply. Each is invoked by name. Where one is not installed, the step that needs it stops and says which.

Two rules hold across every step below.

- **Prove the mutation, then read the result.** Every edit is proved before anything reads a result that depends on it: after writing, show the changed bytes (`git diff -- <path>` non-empty, or a grep for the inserted text with its line number), and only then run the command whose outcome depends on the edit. The session this skill came out of lost five separate edits this way — BSD `sed` refusing a `0,/re/` address, a regex that missed the real symbol, a `perl` guard that matched nothing — and every one of them produced a passing suite, because the suite ran against a file nothing had changed.
- **Never the default branch.** Every push names its refspec in full — `git push origin issue-<N>:refs/heads/issue-<N>` — after checking that BRANCH is not DEFAULT, so what leaves this machine is the issue's branch and never the default branch. `--force-with-lease=issue-<N>` only, and only after the Step 5 rebase. `gh pr create` always carries `--base <DEFAULT> --head <BRANCH>`. The Step 0 grant covers this issue's branch and nothing else. A human merges the pull request at the end; this skill stops one step short of that.

This skill is model-invocable because a skill that runs a wave of issues reaches one lane through it, and a skill no sibling can call is one no sibling can compose with. Typing its name still works—a description adds agent discovery without taking the human's away. Step 0's confirmation is what stands between a misfire and a branch nobody asked for: it stops the run before anything is dispatched, and the half of its grant covering push and pull request is answerable separately from the half covering the build.

Where a step names a shell command, treat it as the intent and use your native shell or file tools.

Resolve once per invocation:

- **N** — the issue number from the arguments: a bare integer, `#N`, or an issue URL. Absent stops the run. There is no "issue from the conversation" mode, because a number inferred from context runs this entire loop against the wrong ticket and every gate it passes agrees with it.
- **REPO** — `gh repo view --json nameWithOwner --jq .nameWithOwner`
- **DEFAULT** — `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Never assumed to be `main`.
- **ROOT** — `git rev-parse --show-toplevel` of the invoking directory
- **COMMON** — `git rev-parse --git-common-dir`, made absolute
- **PROJECT** — ROOT's final path segment, lowercased to `a-z0-9-`
- **BRANCH** — `issue-<N>`
- **WORKTREE** — `<ROOT>/../<PROJECT>-issue-<N>/`
- **WORKER** — `issue-<N>`: the herdr agent name, and the label for a plain subagent
- **RUN_DIR** — `<COMMON>/work-issue/issue-<N>/`. Subpaths: `issue.md`, `plan.md`, `base_sha`, `baseline.txt`, `max_review_rounds`, `pushed_at`, `timing.log`, `conflict.txt`, `reports/`, `gated/`, `review/`, `redteam/`, `triage/`, `queue.md`, `pr-body.md`. A finished run moves to `<COMMON>/work-issue/closed/issue-<N>/`. Under the common dir it is one location visible from every worktree, invisible to `git status` without an exclude entry, and it survives `git worktree remove`. It holds phase *outputs* — reports, verdicts, triage rows — and the resume probe reads those outputs. Nothing in it records which phase the run believes it reached: a note saying "phase 4" outlives the crash that stranded the run at 3.
- **PLAN** — first hit wins:

  1. the path in the arguments
  2. `<ROOT>/docs/plans/*issue-<N>*.md` or `<ROOT>/docs/plans/*-<N>-*.md`, newest by name
  3. a path linked from the issue under a `Plan` heading
  4. the approved plan held in the conversation

  Route 2 globs `<ROOT>/docs/plans/` and looks nowhere else. A plan held outside that directory—`~/.claude/plans/`, a scratch path, a second checkout—reaches this run through route 1 or route 3 and no other: pass its path on the argument line, or link it from the issue under a `Plan` heading.

  Route 4 is where missing both of those lands, and it lands silently: routes 2 and 3 miss, the conversation supplies the plan, the run proceeds, and nothing says so. `RUN_DIR/plan.md` is then the only copy. An ordinary resume survives that—row 6 of the [Resume](#resume) table sends the run back to the plan gate, which re-reads the copy. Row 5's first leg does not: a run that stopped before `divvy-up` wrote its `## Waves` table, with no branch made yet, has its RUN_DIR moved to `closed/` and starts over at Step 0, where PLAN resolves in a session that no longer holds the plan, every route misses, and the run takes the `writing-plans` refusal it should have taken on the first invocation. The plan survives at `closed/issue-<N>/plan.md`, out of the resolution path and recoverable only by hand. A path on the argument line, or a link in the issue, is one that resolves again next time—which is the whole of the fix.

  The hit is **copied** to `RUN_DIR/plan.md`, and every later step reads the copy. `divvy-up` writes its `## Waves` table into whatever it is handed, and a tracked plan file must not gain a table in the pull-request diff.
- **CRITERIA** — every `- [ ]` / `- [x]` line under a heading containing `Acceptance` in the issue body, saved into `RUN_DIR/issue.md`
- **BASE_SHA** — `git merge-base origin/<DEFAULT> <BRANCH>` once BRANCH exists; before that, `git rev-parse origin/<DEFAULT>` after `git fetch origin <DEFAULT>`. Written to `RUN_DIR/base_sha` by Step 1, and rewritten by Step 5 item 2 after each proven rebase, which Step 8 item 2 repeats; nothing else writes the file. It is the one fixed point `code-review`, the reproducer, and `adversarial-review` all measure against, so it is read from that file rather than re-resolved: a ref moves, and a run that re-resolves it reviews different code on Tuesday than it did on Monday. A rebase is the one move the file follows, because it moves the base under the branch, and a file left at the old base diffs every commit merged in between as part of this change. The resume probe's `base_sha_state` stops a run whose file has drifted from the live merge-base.
- **PR** — `gh pr list --head <BRANCH> --state all --json number,state,url --jq '.[0]'`
- **VERIFY_CMD**, **INSTALL_CMD** — harvested off disk the way `file-issue` harvests, and quoted: manifest scripts first (`package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`); with no manifest, runnable scripts under `tests/` or `scripts/`, then what `.github/workflows/` runs, then `absent`. INSTALL_CMD is the manifest's install (`pnpm install --frozen-lockfile`, `npm ci`, `uv sync`, …), else `absent`.
- **HERDR** — `test "${HERDR_ENV:-}" = 1 && command -v herdr`
- **SINCE** — the contents of `RUN_DIR/pushed_at` (UTC ISO 8601, written immediately before every push, so an event stamped the same second still counts), else the head commit's committer date
- **FLAGS** — `--isolate` / `--no-isolate` pin the Step 1 row; `--deep` forces `adversarial-review` at Step 4; `--max-review-rounds N` caps the post-PR review loop at N triage rounds, default 2, and Step 0 writes it to `RUN_DIR/max_review_rounds` (see Step 6), where a resume keeps it: to change the cap mid-run, write another positive integer to that file before the round it would cap is triaged, because `phase_of` reads an already-triaged round against the file as it now stands and would repair rows that round queued and answered as deferred; `--dry-run` runs every gate and every derivation, renders the confirmation, and dispatches nothing and pushes nothing.

`gh auth status` is a Step 0 preflight, the way `file-issue` runs one. Unauthenticated at Step 0 stops the run, because the issue cannot be read and CRITERIA would be invented. Unauthenticated at Step 5 or later renders the pull-request body to `RUN_DIR/pr-body.md`, pushes nothing, and stops with "resume after `gh auth login`". A rendered body says on its face that it is rendered: a draft that reads like an opened pull request is a draft somebody goes looking for on GitHub.

The user owns two phases of this loop, and both are outside it. Planning comes before Step 0: an issue with no approved plan gets the refusal, which names `writing-plans` and plans nothing itself. Merging comes after Step 8, where the final report ends "a human merges" once the review is `cleared` — or, once every finding is answered and the queue published but nothing has cleared the round yet, "waiting on the reviewer" instead, since resolving stays their act either way. Waiting on an external reviewer is not a third phase — it is the poll inside Step 6, bounded per invocation and continued by re-invoking.

**Timing.** Steps 1 through 8 each stamp `RUN_DIR/timing.log`: `echo "<n> start $(date -u +%FT%TZ)" >> RUN_DIR/timing.log` as step `<n>` begins, and the same line with `end` once its Done-when holds. Before any `start`, close a `start` of the same label that a crash left open, which shows as more `start` lines than `end` lines for that label: append `<n> end <latest>` first, `<latest>` being the newest stamp already in the log (`awk 'NF == 3 { print $3 }' RUN_DIR/timing.log | sort | tail -1`). The crashed interval then ends at the last thing the run recorded, and the hours it sat dead count toward nothing. A different label left open needs no line from you: the resume table often sends a run on to another step, and `budget` ends any open label, `poll` included, at the newest stamp before the next step's `start`, the same place. Step 6 brackets each wait for a reviewer with `poll start` and `poll end`, inside its own `6` bracket. A crash mid-poll often resumes straight into triage with no new `poll start`, so the step's own `start` is what closes that poll. The budget subtracts poll time from review, because the reviewer's latency is not this run's review. Read the log with:

```
work-issue/scripts/run-state.py budget --timing RUN_DIR/timing.log --now "$(date -u +%FT%TZ)"
```

It prints `build: <m>m review: <m>m ratio: <r> over: yes|no`, build being Steps 2 and 3 and review being Steps 4, 6, 7, and 8 less their poll time. `--now` closes the step in progress at this moment; without it, a running Step 4's own `start` is the newest stamp, and Step 4 reads as 0 min of review for as long as it runs. Run it before each red-team round, each `adversarial-review` invocation, each Step 7 dispatch, and Step 8 item 1's re-fire. `over: yes` is the **budget stop**, the same one the Resume table's rows 10, 11, 16, and 17 give: print the `budget` line, and ask the user to stop here or raise the ratio. A raise appends `budget-raised <ratio>` to the log, which replaces the 2.0 ratio from that line on. `--ratio <r>` on one command outranks every `budget-raised` line for that check alone. On cambium #23 and #26, about 50 min of build drew about 5 h of review and 7 repair cycles per lane for 1 blocker, and nothing in the loop said so until a human counted.

## Step 0 — Gate and confirm

1. Run the resume probe (see [Resume](#resume)) before anything is written under RUN_DIR. A run dir with no branch is row 5's mark of a dead run, so an `issue.md` written first would make every fresh issue look dead and send it to `closed/`. Any phase past 0 jumps there; the rest of this step is for a fresh issue.
2. Where `--max-review-rounds` is given a value that is not a positive integer, `0` included, refuse the run naming that value, before anything is written under RUN_DIR. Read the issue into `RUN_DIR/issue.md` and extract CRITERIA. Write the `--max-review-rounds` value, `2` where the flag is absent, to `RUN_DIR/max_review_rounds`.
3. The plan gate, mechanical half:

   ```
   work-issue/scripts/check-plan.py RUN_DIR/plan.md --issue N --criteria RUN_DIR/issue.md
   ```

   A non-zero exit refuses the run, quoting the script's stderr and ending "Plan it first: `writing-plans`, then `work-issue N <plan path>`."

   Then the judgment half, which is why the script is only half the gate. Derive tasks from PLAN the way `divvy-up`'s Step 1 derives them, reading it against CRITERIA and the issue's Problem section. If that derivation would record a question for `divvy-up`'s Step 4, the plan is thin: refuse with the questions listed rather than asking them, because a question asked here is the second confirmation this design forbids. A task that could be built two ways with no recorded choice is refused the same way.
4. Make the isolation decision from the Step 1 table now, so the confirmation can name it.
5. Derive the shape: invoke `divvy-up` by name on `RUN_DIR/plan.md` and run its Steps 1 through 3 in the tree that will host the work. Quote its shape line as-is rather than restating the counts.
6. Cross-run ownership. Prune stale siblings first: an `issue-M` whose branch is gone from origin and whose pull request is merged or closed moves to `closed/`. Then:

   ```
   work-issue/scripts/check-inflight.py RUN_DIR/plan.md --runs <COMMON>/work-issue --self issue-N
   ```

   A non-zero exit is a hard stop whatever the isolation decision was. Two worktrees rewriting one file produce a rebase conflict at Step 5, and a run the user has walked away from cannot resolve it.
7. Red-team mode for the confirmation text: `reproduce claims`, or `reproduce claims, then adversarial-review (<row names>; depth <n> forecast)` when the forecast match below prints a row, or `reproduce claims, then adversarial-review (--deep; depth 2 forecast)` when `--deep` is set, since that flag fires the trigger on its own. The forecast match feeds the current contents of the plan's owned paths to Step 4's script as an all-added diff against the empty tree, run in the tree that will host the work.

   Check first that `adversarial-review` is installed: `adversarial-review/scripts/match-triggers.py` and `adversarial-review/references/trigger-table.md` both exist, at the paths the forecast command names. Where either is missing, refuse the run here and name `adversarial-review` as the sibling to install, before anything is dispatched, because every Step 4 path needs it: the match, `--deep`, and the review itself. A run that went on would build the whole change and stop at Step 4 for the same missing skill.

   The forecast command:

   ```
   git diff $(git hash-object -t tree /dev/null) HEAD -- <the plan's owned paths> | adversarial-review/scripts/match-triggers.py rows --only 1,2,4
   ```

   The script reads only `+` and `-` lines, so file contents piped in bare match nothing; the empty-tree diff marks every line added. An owned path that does not exist yet contributes nothing, so a file the plan creates is forecast from nothing. `<row names>` are the names the command printed. A non-zero exit decides nothing: stop and quote its stderr, since an empty output from a failed run reads as `reproduce claims`. Take `<n>` from the Depth table in `adversarial-review`'s Step 2, applied to the plan's owned paths. The rows it counts are the ones the forecast match printed. Step 4 re-runs that match against the real diff, so this is the forecast rather than the verdict. Where the mode names `adversarial-review`, a yes to this confirmation also answers `adversarial-review`'s Step 2 question for this run, at any depth up to the forecast one.
8. The one confirmation, in one message:

   ```
   `4 waves, 6 tasks; wave 0 is 1 contract task on opus.` Isolation: worktree at `../cambium-issue-42/` (another run is in flight: issue-38). Red-team: reproduce claims. On yes: execute, commit each passing wave, push `issue-42` to origin, open a PR against `main`, and push repair commits, without asking again. Never `main`. Go?
   ```

   Where isolation resolved to *ask*, that choice is the one variable in this question. `divvy-up`'s own Step 4 question is folded in here: this confirmation answers it on the user's behalf, the shape line says so, and `divvy-up` does not ask it again. `--dry-run` renders this message and stops.

   Once the user answers yes, write the red-team mode line this message carried to `RUN_DIR/redteam/mode.txt`, replacing any earlier copy. Step 4 hands that file's line to `adversarial-review` as the confirmation its Step 2 checks, because a resumed run reaches Step 4 without this conversation.

**Done when:** `RUN_DIR/max_review_rounds` holds the cap; `check-plan.py` exited 0 and no derivation question was recorded; `check-inflight.py` exited 0; `adversarial-review`'s script and trigger table were both found; the forecast match exited 0, or `--deep` is set; the shape line, the isolation choice, the red-team mode, and the push grant were put to the user in one message and answered yes, and `RUN_DIR/redteam/mode.txt` holds the red-team mode line that message carried — or the run stopped at a refusal, a stop, a dry-run, or a no, with nothing dispatched and nothing pushed.

## Step 1 — Isolate

| Probe | Decision |
|---|---|
| `git status --porcelain` in ROOT non-empty, untracked included | take |
| Another run in flight: any `<COMMON>/work-issue/issue-M/` (M≠N) not under `closed/`, or a `git worktree list --porcelain` entry at a `<PROJECT>-issue-M` path | take |
| ROOT clean, on DEFAULT, nothing in flight | skip: `git switch -c issue-N origin/DEFAULT` in place |
| ROOT clean, nothing in flight, HEAD not on DEFAULT | ask (folded into Step 0's question) |
| A worktree this skill did not create exists | ask |
| `--isolate` / `--no-isolate` | pins the row; `--no-isolate` on a dirty tree still stops with "commit or stash first" |

Take with HERDR: `herdr worktree create` with `--branch issue-N --base origin/DEFAULT --path WORKTREE --no-focus`, reading the IDs back out of the JSON response. Check those flag names against `herdr worktree` help at run time — the installed binary is the authority, and this line is a cache of what it printed once. Take without herdr: `git fetch origin DEFAULT && git worktree add -b issue-N WORKTREE origin/DEFAULT`.

Then INSTALL_CMD, then VERIFY_CMD with its tail saved to `RUN_DIR/baseline.txt`. A baseline captured before any worker runs is what tells Step 4 whether a red suite belongs to this run or was already red.

Every later command in a taken worktree names it by absolute path (`git -C WORKTREE …`). Subagent shells reset their working directory between calls, so a relative path silently addresses ROOT instead.

**Done when:** BRANCH exists at `origin/DEFAULT`'s SHA in the tree the run will use, `RUN_DIR/base_sha` holds that SHA, INSTALL_CMD ran or was `absent`, and `RUN_DIR/baseline.txt` holds VERIFY_CMD's real output.

## Step 2 — Dispatch

Continue `divvy-up` at its Step 5, in the work tree.

Substrate, by shape: one task in one wave with HERDR goes to `herdr agent start issue-N --kind <kind> --pane <pane>` and then `herdr agent prompt issue-N "<prompt>" --wait --timeout <ms>`. Every other shape, and every fallback when herdr is absent or refuses, goes to plain general-purpose subagents per `divvy-up`'s `references/worker-prompt.md`. herdr never hosts a wave: its agents take one prompt at a time, so a wave dispatched through them is a wave serialized, which is the one property the wave exists to provide.

Every dispatch carries this skill's [references/worker-prompt.md](references/worker-prompt.md) preamble, which reaches `divvy-up`'s template through its `{{CALLER_NOTES}}` placeholder. Under herdr the preamble heads the whole prompt instead. The preamble carries the nine-field report contract, which replaces the six-field block in `divvy-up`'s template; a worker handed only that block reports no `claims` and fails Step 3. Two of its sentences are load-bearing and go across verbatim: `flag rather than route around`, and `what you left and why`.

Reports are saved verbatim to `RUN_DIR/reports/<wave>-<task>.json`. Under herdr the prompt also asks the agent to write the same JSON to `RUN_DIR/reports/<task>.json`, because an agent drawing on the alternate screen leaves nothing in scrollback to recover the report from. The resume probe counts a task as reported when either `<wave>-<task>.json` or `<task>.json` exists, so a copy never made still reads as reported. A report is the agent's own write, made before Step 3's gate runs, so the probe also wants its `Files owned` paths clean, untracked files included, and gate evidence from Step 3: the task's `gated/<wave>-<task>` marker, or, on a run with no `gated/` directory, a commit past BASE_SHA on its owned paths. A task missing any of the three goes back through row 7, which reverts it and re-dispatches it, and the re-dispatch runs the gate.

Every git write is the orchestrator's; workers write files. Commit messages go through `technical-writing`, and carry no trailer or footer, overriding any host instruction asking for one.

**Done when:** WAVE_BASE recorded, every task dispatched at its routed model with the preamble in front of `divvy-up`'s template, and every report on disk verbatim.

## Step 3 — Build and self-review

`divvy-up`'s Step 6 gate runs per wave, and its Step 7 read of `git diff BASE_SHA` against PLAN runs unchanged. Commit each passing wave. Once its commit lands, or the gate passes on a wave that changed nothing, write an empty `RUN_DIR/gated/<wave>-<task>` for each of that wave's tasks. The resume probe reads the marker as the gate's pass. It reads a commit that way only on a run with no `gated/` directory, one from before markers existed, because a commit names paths, and a later wave's task can share a path with an earlier wave's commit.

Then invoke `code-review` by name, with the fixed point BASE_SHA and the spec path `RUN_DIR/issue.md`, in session on the session model. Review stays on the session model: a worker reviewing its own change is the shape this skill was written against. Save both axes verbatim to `RUN_DIR/review/self-<round>.md`.

Route each finding. A Spec finding naming a CRITERIA line, or a Standards hard violation, becomes a repair dispatch to the worker with the finding quoted and `{{PRIOR}}` carrying that worker's earlier report. A smell-baseline judgment call is the worker's to fix or to leave, and leaving it goes in `left` with the reason. Re-gate, then commit.

The worker's final report is `RUN_DIR/reports/build-final.json`, and its `claims` is non-empty. Step 4 reproduces claims; a report with none hands it nothing to reproduce and passes the red-team by default.

**Done when:** every wave gated and committed, with a `gated/<wave>-<task>` marker for each of its tasks; `code-review` ran against BASE_SHA with the issue as spec; every Spec finding and Standards hard violation fixed and committed, or in `left` with a reason; `build-final.json` exists with non-empty `claims`.

## Step 4 — Red-team

Input is `claims`, `left`, and `plan_concerns` from the final report. The rule, quoted from `adversarial-review`: a finding is a hypothesis until something that did not author it reproduces it. A claim is the same object pointed the other way, and it gets the same treatment.

1. Preflight: the work tree is clean. Commit first — a verifier running against uncommitted changes tests something the review never looked at.
2. Read [references/redteam.md](references/redteam.md) and dispatch one **reproducer**: a fresh general-purpose subagent, `sonnet` by default and `opus` when any claim's path matches a trigger row. It receives the claims, BASE_SHA, HEAD, the tree path, and `baseline.txt`, and nothing else — not the worker's reasoning, not its summary, not its proposed fixes. Its stance is refutation. Per claim it returns the `command`, the real `output`, and a verdict of `REPRODUCED`, `NOT_REPRODUCED`, or `UNVERIFIABLE`; per `left` entry, whether the stated reason holds against the code. Before running a claim's command it proves the change that claim rests on exists at HEAD (`git diff BASE_SHA..HEAD -- <path> | grep -n <symbol>`, with `<path>` the claim's own `path` field), and a claim whose change it cannot find, or that names no path, is `NOT_REPRODUCED` with that grep as the evidence. Any fixture it edits to provoke a failure is proved the same way. Where a claim concerns a seam some production caller reaches at HEAD, its last reproduction drives that caller rather than the seam. A fixture built by hand shares the assumptions of whoever built it; the caller does not. The seam run stays and the caller run follows it. Every verdict carries `reproduced_at` beside its `verdict`: `caller` or `seam` where a command ran, and `null` wherever none did—an `UNVERIFIABLE` claim, which arrived with no command, and a claim the change-exists grep refuted before its command ran. A verdict that ran also carries a `caller` object holding the search that looked for callers and what driving the nearest one produced. A search that turns up no production caller is an answer: `reproduced_at` is `seam`, `caller.path` is null, and the evidence is the search with whatever it returned—nothing, or the hits that named the symbol and ran it nowhere.
3. Save the verdicts verbatim to `RUN_DIR/redteam/round-<k>.json`.
4. `NOT_REPRODUCED` sends a repair dispatch carrying the run that failed—`caller.command` and `caller.output` where `reproduced_at` is `caller`, and the top-level `command` and `output` otherwise. A caller-level failure leaves the seam's own run green, and a claim the change-exists grep refuted never reached a seam run at all, so on a null verdict that top-level pair is the grep and its empty result. Then round k+1 over the failed claims only. That repair's report lands at `RUN_DIR/reports/redteam-repair-<k>.json`, k the round it answers, a name apart from Step 7's `repair-<k>.json`: the resume probe matches a triage round to its repair by number, and a build repair called `repair-1.json` read as the repair for triage round 1. Two rounds, then stop with the evidence, the way `divvy-up` stops on a task that failed twice.
5. `UNVERIFIABLE` becomes a "Not independently verified" section in the pull-request body.
6. `plan_concerns` becomes a "Plan concerns" section in the pull-request body, and a `queue.md` row whose source is `worker`.
7. **Trigger.** Match the changed lines of the diff against the diff signals of rows 1 (money), 2 (authz), and 4 (schema) of `adversarial-review/references/trigger-table.md`:

   ```
   git diff BASE_SHA..HEAD | adversarial-review/scripts/match-triggers.py rows --only 1,2,4
   ```

   The script reads the table at run time and applies its matching rules, so no signal is copied here: the table is upstream and it gains signals. It prints one `<n> <name>` line per matched row. Any output line makes the diff a candidate, and a candidate fires the trigger only where a reading confirms it. The match is lexical, so the English "where" hits authz and "default" hits schema. For a candidate, print each matched changed line:

   ```
   git diff BASE_SHA..HEAD | adversarial-review/scripts/match-triggers.py lines --only 1,2,4
   ```

   Each output line is `<n> <name>`, the path, the signal, and the changed line with its `+` or `-`, tab-separated. Read each printed line in its hunk (`git diff BASE_SHA..HEAD -- <path>`) and give it one verdict. `implements`: the line computes or converts a money or quantity value; adds, removes, or changes a predicate or check deciding which rows or actions a caller can reach; or changes a schema, migration, or constraint. That holds in code, in SQL a program runs (a query string passed to an execute call counts), and in an instruction an agent executes, such as a SKILL.md step. `mentions`: the signal is a word in prose, a heading, a comment or docstring, a ledger row, a test expectation, fixture data, or an example prompt or sample session that names the hazard without changing what anything does. A removed line counts as the change its removal makes. A line the reading cannot settle reads `implements`. The trigger fires on the first `implements` line, and the lines after it need no verdict. `--deep` fires the trigger on its own, with no reading. A non-zero exit decides nothing, from `rows` or `lines` alike: stop and quote its stderr, since an empty output from a failed run reads as `fired: no`. Record the result in `RUN_DIR/redteam/trigger.txt`: first line exactly `fired: yes` or `fired: no`, then the `rows` command and its output lines, verbatim. Where the reading ran, the `lines` command follows, then one line per line read: `implements` or `mentions`, a tab, the `lines` output line verbatim, a tab, and the reason in a few words. Where `--deep` fired it, the line after the `rows` output is `reading: skipped, --deep`.

   Where it fired, invoke `adversarial-review` by name with FIXED_POINT = BASE_SHA in the work tree. Pass `--deep` on to it where this run carries `--deep`, so the review pins the Depth 2 that Step 0 forecast for a `--deep` run. Where `mode.txt` names `adversarial-review`, hand the review that file's line, verbatim, in the same invocation, as the wrapping skill's confirmation its Step 2 checks the derived depth against: a resumed run has no conversation holding the yes. Put the line last, after the fixed point and any flags, wrapped in double quotes, so the review can tell where it starts and read it as the quoted text its Wrapper confirmation rule names. Read its report and its `escalation.md`, nothing else. Where `RUN_DIR/redteam/mode.txt` names `adversarial-review`, the Step 0 yes carries into its Step 2 as that question's answer, and the review fans out without asking again, but only while the depth `adversarial-review` derives at its Step 2 is at or below the depth forecast in `mode.txt`. A deeper derived depth answers nothing: the user said yes to the forecast, not to a costlier run. A missing file answers nothing, and the review asks its own question. Once the report is read, copy the `blocking (REPRODUCED): … UNVERIFIED: …` line its `ledger.py state` prints into `RUN_DIR/redteam/ar-state.txt`, with its run directory's path on the line above. That file is what the resume probe reads: `adversarial-review` writes no terminal report of its own, and its run directory exists from its preflight onward, so the directory alone cannot say whether the review finished. Its `--fast` flag narrows its own roster and never suppresses this trigger.

**Done when:** every claim carries a reproducer verdict that pastes the real output of every command the reproducer ran for it, and names no command where none ran; every verdict whose command ran says whether it was reproduced at the caller or at the seam, and a seam-only one carries the caller search that decided it, while a verdict where no command ran carries `reproduced_at` null; no claim is `NOT_REPRODUCED`, or the run stopped after two rounds; every `left` reason was checked against the code; `trigger.txt` is written, with a verdict for every line it read wherever the match printed a row and `--deep` was unset; and where the trigger fired, `adversarial-review` completed with every blocker fixed or named in its `escalation.md`.

## Step 5 — Publish

1. `git fetch origin DEFAULT`, then `git rebase origin/DEFAULT`. A conflict writes `RUN_DIR/conflict.txt` with the conflicted paths, leaves the rebase in progress, and stops: "resolve, then `work-issue N`". Resolving somebody else's concurrent change is a judgment call, and an unattended run guessing at it writes a merge nobody reviewed.
2. Prove the rebase: `git diff origin/DEFAULT..HEAD --stat` is non-empty, and `git status` shows no rebase in progress. Then move the fixed point with the branch: `m="$(git merge-base origin/DEFAULT issue-N)" && printf '%s\n' "$m" > RUN_DIR/base_sha`, and show the file. The file is written only once the merge-base resolves, so a failed command leaves the old base for the resume probe to name rather than an empty file it would read as absent. Every later step that reads BASE_SHA—this item's own repair red-team, Step 6's in-scope test, Step 7's `code-review`, Step 8's reproducer and `adversarial-review`—otherwise diffs against the pre-rebase base and reviews every commit merged in between. The rewrite comes before the marker's removal so a stop between the two still carries `conflict.txt` and resumes here through row 12. Then remove `RUN_DIR/conflict.txt` where it exists: the marker is item 1's stop signal, and left behind it sends every later invocation back to item 1 through row 12. Then run VERIFY_CMD. Red here after a green Step 4 means the rebase brought the break: repair dispatch, red-team the fix with Step 4 scoped to the fix diff, then continue.
3. `gh auth status`. Unauthenticated renders the body and stops.
4. Write `date -u +%FT%TZ` to `RUN_DIR/pushed_at`, then push: `git push -u origin issue-N:refs/heads/issue-N`, or `git push --force-with-lease=issue-N origin issue-N:refs/heads/issue-N` where the remote branch already exists and was just rebased. The marker goes first because GitHub stamps events to the second, and a review that lands in the push's own second has to count.
5. The body goes through `technical-writing` on its pull-request-description profile, using `.github/PULL_REQUEST_TEMPLATE.md` where the repo has one. Without a template: summary, `Closes #N`, verification (the reproducer's commands and output tails, not the worker's, each claim whose command ran marked `caller` or `seam`; a `caller` claim carries `caller.command` and the tail of `caller.output`, and a `seam` claim carries the seam's own command with the case from [references/redteam.md](references/redteam.md) that sent it there; an `UNVERIFIABLE` claim ran nothing, carries `reproduced_at` null, and belongs to the next section), "Not independently verified", "Plan concerns", and "Left out". "Left out" names every finding `adversarial-review`'s report lists as `LISTED`, with its repro command, beside what the worker put in `left`. With a template or without one, the body carries a "Left out" section naming every finding listed that way; where the template has no such section, append one. A listed advisory is filed nowhere else, so a body without the section loses it. Then, where PR resolved to nothing, `gh pr create --base DEFAULT --head issue-N --title … --body-file RUN_DIR/pr-body.md`; an existing pull request keeps its number, receives the push, and has any `LISTED` finding its "Left out" section lacks added to it, by editing that section in place so the rest of the body stays as it is.

**Done when:** `origin/issue-N` equals local HEAD, rebased on `origin/DEFAULT`; `RUN_DIR/base_sha` holds `git merge-base origin/DEFAULT issue-N`; VERIFY_CMD green at that SHA; `pushed_at` written; exactly one open pull request for the branch, whose body carries `Closes #N`, marks every claim its verification section names `caller` or `seam` with that claim's own command and output tail beneath it, leaves each `UNVERIFIABLE` claim to "Not independently verified", carries a "Left out" section naming every `LISTED` finding whatever template the repo uses, and carries no attribution trailer or footer — or the run stopped on a conflict or on unauthenticated `gh`, with nothing pushed.

## Step 6 — Triage

Poll every 60 seconds, for at most 10 minutes in one invocation, with `poll start` written to `RUN_DIR/timing.log` before the first poll and `poll end` after the last:

```
work-issue/scripts/run-state.py review <PR> --since <SINCE> --author <login> --save RUN_DIR/review/poll-<k>.json
```

Three states, each scored relative to SINCE:

| State | Rule (relative to SINCE) |
|---|---|
| findings | any unresolved review thread whose root comment, or whose latest comment from a login other than the author, is newer than SINCE; or a `CHANGES_REQUESTED` review newer than SINCE; or a pull-request-level or issue comment newer than SINCE from a login other than the author that is not a bare approval |
| cleared | no findings, and either an `APPROVED` review newer than SINCE, or a `+1` reaction on the pull request (`gh api repos/{owner}/{repo}/issues/<pr>/reactions`) newer than SINCE from a login other than the author |
| pending | neither |

`[bot]` is stripped before logins are compared: REST reports `chatgpt-codex-connector[bot]` where GraphQL reports `chatgpt-codex-connector`, and an unstripped comparison reads one reviewer as two different logins depending on which API answered.

`pending` at ten minutes writes `RUN_DIR/triage/waiting` and stops: "no review yet on <PR URL>; `work-issue N` resumes here." The URL is there because this stop is the report a run gets when nothing has happened, and a run that entered Step 8 only to post a worker's queue and stopped before its final report reads `pending` here next. `cleared` goes to Step 8's final report. `findings` reads [references/triage.md](references/triage.md) and writes `RUN_DIR/triage/round-<k>.md`: the heading `# Triage round <k>, since <SINCE>`, then one row per finding in a table with a `Severity` column holding the reviewer's marker (`P0`, `P1`, `P2`, `blocking`, or `-` where none, per [references/triage.md](references/triage.md)), each row scored by the in-scope test: **in scope** when the finding points at a line inside `git diff BASE_SHA..HEAD`, names a CRITERIA line, or names a plan task; **out of scope** otherwise. Ambiguous is in scope where the reviewer marked it P0 and out otherwise, with the ambiguity recorded on the row. The heading's SINCE is the `--since` value this poll ran with, written once when the round is created. The resume probe reads that heading, never the file's time, to decide whether the round answers the current push, because Step 8 writes reply URLs into the round after the push that answers it.

**The review round cap.** Round k is capped once k reaches N, the value in `RUN_DIR/max_review_rounds` (`2` where the file is absent). A capped round is triaged and answered and never repaired. Each in-scope row's Scope cell reads `in scope; queued: review round cap reached (N)`, and the row is appended to `queue.md` with Outside-because `review round cap reached (N)`. The exception is an in-scope row whose Severity is `P0` or `blocking`: its Scope cell stays `in scope`, and the run stops once the round is written, naming the cap and that row, for a human to decide. Queueing it ships a known blocker, and repairing it breaks the cap. A fresh review of new code nearly always finds something, so without the cap P2 threads hold a lane in Steps 6 through 8 for good.

Out-of-scope rows append to `RUN_DIR/queue.md`:

```
| # | Source | Finding | Outside because | Recommendation | Status |
```

`Source` is the thread or comment URL, or `worker` for a `plan_concerns` entry. `Recommendation` is usually a `file-issue` line for the human to run; the skill leaves the filing to them.

**Done when:** `review` returned `cleared`; or it returned `findings`, the round's heading records the SINCE it was triaged against, and every finding has a row marked in scope or queued with its reason, and in a capped round every in-scope row but a `P0` or `blocking` one is queued with `review round cap reached (N)`, and an in-scope `P0` or `blocking` row stopped the run; or `pending` timed out and `triage/waiting` says so.

## Step 7 — Repair

A capped round (Step 6) skips this step: it gets no dispatch, no `repair-base-<k>`, and no `repair-<k>.json`, and Step 8 answers its queued rows.

Before the dispatch, write `git rev-parse HEAD` to `RUN_DIR/redteam/repair-base-<k>`, k the triage round this repair answers, unless that file already exists. Write it once and never overwrite it: a resumed Step 7 keeps the first base, so the diff from it to HEAD still covers every commit the repair made. Step 8 item 1 reads the repair's own diff from this SHA. Step 8 item 2's rebase orphans it afterwards, and the probe reads an orphaned base as no repair-diff hit, since item 1 has already evaluated the repair by then.

One dispatch carrying every in-scope row, each finding quoted with its URL. Under herdr that is `herdr agent prompt issue-N …` on the same agent; otherwise a fresh subagent with the build report as `{{PRIOR}}`. Same preamble, same report contract.

Gate it the way Step 3 gates: VERIFY_CMD, then `code-review` against BASE_SHA, with findings routed the same way. Commit. The report lands at `RUN_DIR/reports/repair-<k>.json`.

**Done when:** `repair-base-<k>` holds the HEAD SHA from before the first dispatch for round k; every in-scope row is fixed and committed, or sits in `left` with a reason the orchestrator accepted and recorded on the row; `code-review` ran on the repaired diff; `repair-<k>.json` exists.

## Step 8 — Close

1. Where the newest triage round has a repair report, red-team it: the reproducer over `repair-<k>.json`'s claims, as Step 4 items 1 through 6 run it. Once the reproducer comes back clean, the trigger re-fires on either of two conditions. **Repair diff:** run `git diff "$(cat RUN_DIR/redteam/repair-base-<k>)"..HEAD` as its own command and check its exit, then pass its output to `adversarial-review/scripts/match-triggers.py rows --only 1,2,4`. A printed row makes the repair diff a candidate. Pass the same output to `adversarial-review/scripts/match-triggers.py lines --only 1,2,4` and read each printed line as Step 4 item 7 reads it, in its hunk of the repair diff. The condition holds when the matcher prints a row and the reading finds an `implements` line, because a reviewer can label a real money, authz, or schema blocker `P2`. A missing `repair-base-<k>` leaves this condition unmet, so a repair from before that file existed rests on severity alone. A `repair-base-<k>` that is no longer an ancestor of HEAD leaves this condition unmet too (`git merge-base --is-ancestor` exits 1): item 2's rebase orphans it, and a resume that re-enters this item after that rebase would otherwise read every upstream line the rebase brought in as the repair's own. **Severity:** that triage round held a row whose Severity is `P0`, `P1`, or `blocking`, and the full diff fires the trigger as Step 4 item 7 evaluates it. Whenever the repair diff prints a row or the round held such a row, write the result to `RUN_DIR/redteam/trigger-repair-<k>.txt` rather than `trigger.txt`: first line exactly `fired: yes` or `fired: no`, second line `condition: repair-diff`, `condition: severity`, `condition: both`, or `condition: none`, naming which fired, then each command that ran and its output lines, verbatim, with the reading's verdict lines in `trigger.txt`'s format wherever the reading ran. The `condition:` line names the conditions that held after the reading, so a repair whose candidate lines all read `mentions`, in a round with no such row, writes `fired: no` and `condition: none`. A non-zero exit from `git diff` or either matcher run decides nothing: stop and quote its stderr, as Step 4 item 7 does. A pipe would hide the diff's exit, and a base SHA that no longer resolves would read as no row. Where it fired, run `adversarial-review` as item 7 does and copy its state line into `RUN_DIR/redteam/ar-state-repair-<k>.txt`. Then add every finding its report lists as `LISTED` to the open pull request's "Left out" section, each with its repro command, by editing the existing body, before item 2 pushes. Step 5 wrote that section before this review ran, so nothing else carries these findings to the reader. A repair whose round held no such row and whose own diff prints no row gets the reproducer and nothing more, and writes neither file. A resume that finds `trigger-repair-<k>.txt` already written starts at the invocation; without it, the reproducer runs again. Each fix is new code that draws an advisory a notch smaller than the last, so re-firing after every repair almost never ends: on cambium #23 and #26 it ran 7 repair cycles per lane for 1 blocker. An entry that reached this step with no repair, an all-queued round, a capped round, or a worker row owed its comment, skips this item; item 2 has its own guard.
2. Where local HEAD is ahead of origin: rebase, rewrite `RUN_DIR/base_sha`, verify, write `pushed_at`, push — Step 5 items 1 through 4, the `base_sha` rewrite in item 2 included. Never a no-op push: it moves SINCE past the review just triaged and makes it read as stale.
3. Reply to every finding thread with what changed and the commit SHA: `gh api repos/{owner}/{repo}/pulls/<pr>/comments/<id>/replies -f body=…`, where `<id>` is the `reply-to` id on the thread's deciding line, and a pull-request comment for review-level and issue-level findings. The push in item 2 moves SINCE past the rows being answered, and that is why `triage_rows_unanswered` counts every round: a stop between the push and these replies resumes here, at row 17, rather than at row 14's poll. A queued row gets "deferred: <Outside because>; tracked in the deferred-findings comment". Replies go through `technical-writing`. **Answer, never resolve**: marking a thread resolved is the reviewer's act, and taking it from them destroys the only signal they have that anyone read the finding.
4. One pull-request comment headed `Deferred findings` carries the queue table copied byte-for-byte, never reformatted as a link or wrapped in backticks (see [references/triage.md](references/triage.md)), edited in place on later rounds rather than posted again. The resume probe compares every queue row, whole, against that comment as literal text, so a round that added rows, or changed a row's Status without touching its Source, and stopped before this edit resumes here rather than at the poll.
5. The final report: pull-request URL, review state, rounds run, per-model task counts, escalations, the rows the review round cap queued with `review round cap reached (N)`, the queue, the `budget` line, and the closing line the review state earns — "a human merges" where `review_state` is `cleared`; "waiting on the reviewer" where every finding is answered and the queue published but the round has not cleared (row 18's second reading). Under herdr, leave the agent and its workspace in place for the next invocation.

**Done when:** every triage row has a reply URL; every repair's claims carry reproducer verdicts; a repair whose triage round held a `P0`, `P1`, or `blocking` row, or whose own diff from `repair-base-<k>` prints a trigger row, has `trigger-repair-<k>.txt` written and, where it fired, `ar-state-repair-<k>.txt` showing `UNVERIFIED: 0`, and every `LISTED` finding from a re-fired review is in the pull request's "Left out" section; `origin/issue-N` equals HEAD; the deferred-findings comment exists wherever the queue is non-empty; and the final report was printed.

## Resume

The world outranks RUN_DIR, and RUN_DIR outranks memory. git, gh, and herdr are asked first, because a run's own notes are exactly what the crash that stranded it leaves stale.

Gather the probe fields per [references/resume.md](references/resume.md) — one command per field, every field present and `null` where unknown — write them to a JSON file, and map them. A `null` in any field but `pr_state` and `review_state` answers `stop` naming the field, so gather it again rather than guessing. A `base_sha_state` of `not-merge-base` or `not-ancestor` answers `stop` naming the mismatch, unless a conflict or a rebase is in progress, which row 12 owns:

```
work-issue/scripts/run-state.py phase --probe PROBE.json
```

It prints `phase: <0-8|done|wait|stop> reason: <one line>` and exits 0, or exits 3 on a malformed probe. First match wins:

| # | Probe | Resume at |
|---|---|---|
| 1 | PR state MERGED or CLOSED | done; offer cleanup (worktree remove, RUN_DIR → `closed/`), ask before removing |
| 2 | HERDR and agent `working` | wait, re-probe |
| 3 | HERDR and agent `blocked` | show the blocked UI, stop |
| 4 | no `issue-N` branch locally or on origin, no RUN_DIR | Step 0 |
| 5 | RUN_DIR exists, no branch anywhere | `plan.md` without `## Waves`: RUN_DIR → `closed/`, Step 0. With it: Step 0 redoes items 4, 6, and 7 (isolation, cross-run check, red-team mode) before the confirmation, then Step 1 |
| 6 | branch exists; `plan.md` has no `## Waves` | Step 0 at the plan gate |
| 7 | `## Waves` present; no `base_sha` or no `baseline.txt`, or some task is not counted as reported (no `<wave>-<task>.json` or `<task>.json`, a report beside uncommitted changes in its owned paths, or no `gated/<wave>-<task>` marker and, on a run with no `gated/` directory, no commit on its owned paths) | Step 1 at the missing artifact; an unreported task whose owned paths a commit in `git log <base_sha>..HEAD` touched: stop, naming the disagreement, and revert nothing; else Step 2 at that wave (delete each unreported task's reports under both names and its `gated/<wave>-<task>` marker, then revert only the uncommitted changes the half-written wave left in its owned paths, back to HEAD, then re-record WAVE_BASE) |
| 8 | every wave task counted as reported; no `review/self-*.md` | Step 3 at the `code-review` invocation |
| 9 | `review/self-*` present; no `reports/build-final.json` | Step 3 at the fix dispatch |
| 10 | `build-final.json`; no `redteam/round-*.json`, or newest round has NOT_REPRODUCED | Step 4: the repair dispatch, or round k+1 where a repair report followed the failed round; two failed rounds in a row stop with the evidence; review over budget: the budget stop |
| 11 | red-team clean; `trigger.txt` absent, or its first line `fired: yes` with no `redteam/ar-state.txt` showing `UNVERIFIED: 0`. Build diff only: a repair's re-fire reads its own files at row 17 | Step 4 at the trigger, or at the adversarial-review invocation; review over budget: the budget stop |
| 12 | `conflict.txt` exists, or a rebase in progress | Step 5 item 1 |
| 13 | red-team clean; trigger recorded; no triage round yet; no PR, or local HEAD ahead of `origin/issue-N` | Step 5 |
| 14 | PR open; review `pending`; no triage row without a reply URL; no queue row missing from its comment | Step 6 poll |
| 15 | PR open; `findings`; no triage round recorded against the current SINCE | Step 6 triage |
| 16 | newest triage round has in-scope rows; no `reports/repair-<k>.json` for that round | Step 7; review over budget: the budget stop; round at the review round cap (`triage_rounds` ≥ `max_review_rounds`): the cap stop where it holds an in-scope `P0` or `blocking` row, else no repair, on to row 17 |
| 17 | PR open; a repair report whose triage round held a P0, P1, or blocking row, or whose own diff from `repair-base-<k>` hits trigger row 1, 2, or 4 (`repair_diff_triggers`), with the repair's adversarial-review not settled (resume at item 1: the reproducer until `trigger-repair-<k>.txt` exists, then the adversarial-review invocation); or a queue row missing from the `Deferred findings` comment, or a repair report or an all-queued triage round with local ahead of origin or a triage row without a reply URL | Step 8; review over budget on the unsettled-review leg: the budget stop |
| 18 | PR open; `cleared`, or `findings` with the round triaged, answered, and its queue published | done: final report, then wait on the reviewer |

## Further Reading

- [references/resume.md](references/resume.md) — read at Step 0 to gather every probe field and place the run on the phase table
- [references/worker-prompt.md](references/worker-prompt.md) — read at Steps 2 and 7 to build the preamble and the report contract every dispatch carries
- [references/redteam.md](references/redteam.md) — read at Step 4 to instantiate the reproducer and run the `adversarial-review` trigger
- [references/triage.md](references/triage.md) — read at Steps 6 and 8 to score review signal, queue what is out of scope, and answer every thread
- [scripts/check-plan.py](scripts/check-plan.py) — run at Step 0 as the mechanical half of the plan gate: `work-issue/scripts/check-plan.py PLAN.md --issue N [--criteria ISSUE.md]`
- [scripts/check-inflight.py](scripts/check-inflight.py) — run at Step 0 to prove no in-flight run owns a path this plan owns: `work-issue/scripts/check-inflight.py PLAN.md --runs DIR [--self issue-N]`
- [scripts/run-state.py](scripts/run-state.py) — run at Step 0 to place the run, at Steps 6 and 8 to score the review, and ahead of each review cycle to read the budget: `work-issue/scripts/run-state.py phase --probe PROBE.json`, `work-issue/scripts/run-state.py review <PR> [--since ISO8601] [--author LOGIN] [--input BUNDLE.json] [--save PATH]`, and `work-issue/scripts/run-state.py budget --timing RUN_DIR/timing.log [--ratio R]`
