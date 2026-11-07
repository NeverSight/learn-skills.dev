---
name: work-wave
description: "Run N GitHub issues at once, one work-issue run per issue in its own worktree, with the footprints proved disjoint, the cross-lane coupling question answered and recorded, the merge order fixed, and the branches merged together and verified before any lane opens a pull request. Use ONLY when the user explicitly invokes work-wave. It never plans an issue, never merges one, and never advances a single issue: for one issue, use work-issue."
argument-hint: '<issue> <issue> [<issue>...] [--plan N=PATH ...] [--lane-model opus|fable] [--dry-run]'
disable-model-invocation: true
---

# work-wave

`work-issue` advances one issue and refuses a concurrent sibling at its gate, which is right for what it owns. Three issues, three worktrees, three agents, and one orchestrator holding the parts true across all of them is a shape it does not cover, and run by hand that orchestration loses the same four things every time: a coupling between two lanes that no diff shows, the merge test run last instead of first, a fact one lane learned and another paid to relearn, and a file handed back at a path the orchestrator could not read.

Width across lanes is safe under two conditions. No two lanes write the same path, and that gets **proved by a script before anything is dispatched**, the way `divvy-up` proves a wave. And no lane's change alters what another lane builds against, which no script can prove: two diffs in `core/` and `app/storage/` are disjoint and can still be about one thing. Disjoint paths prove two lanes cannot lose each other's writes. They do not prove the two lanes are independent, and this skill asks the second question on its own, records the answer per pair, and turns it into a merge order before a lane exists.

Cost is N `work-issue` runs plus a merge test, and the runs are the cost of the issues, not of this skill. What this skill spends beyond that is one worktree for the merge test and the orchestrator's own reading of N plans, and both are spent so that a coupling costs a merge-order row here instead of a rebase conflict, a reverted pull request, and a re-run later. Every judgment—footprints, coupling, order, what a lane's report means—stays on the session model; the lanes are dispatched at `opus`, because a lane is itself an orchestrator running gates.

Four skills cover four shapes of the same job. Reach for `agent-guild` when the work needs a written constitution and an independent checker per task. Reach for `divvy-up` when a plan is already approved and its tasks can be carved into disjoint file ownership in one tree. Reach for `work-issue` when one issue has one approved plan and should go all the way to an answered pull request. Reach for `work-wave` when two or more issues each have one, and they should go at the same time.

This skill is user-invoked (`disable-model-invocation: true`) because a misfire during ordinary planning spends a whole fan-out, while a missed trigger costs the user one word.

Where a step names a shell command, treat it as the intent and use your native shell or file tools.

Resolve once per invocation:

- **ISSUES** — every issue number in the arguments: bare integers, `#N`, or issue URLs. Fewer than two stops the run with "one issue is `work-issue N`". There is no "issues from the conversation" mode, for the reason `work-issue` gives: a number inferred from context runs this entire wave against the wrong tickets.
- **REPO** — `gh repo view --json nameWithOwner --jq .nameWithOwner`
- **DEFAULT** — `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Never assumed to be `main`.
- **ROOT** — `git rev-parse --show-toplevel` of the invoking directory
- **COMMON** — `git rev-parse --git-common-dir`, made absolute
- **PROJECT** — ROOT's final path segment, lowercased to `a-z0-9-`
- **WAVE_ID** — ISSUES sorted ascending and joined by `-`: `113-114-115`. Derived from the inputs so the same set of issues lands on the same directory every time it is typed.
- **WAVE_DIR** — `<COMMON>/work-wave/wave-<WAVE_ID>/`. Subpaths: `lanes.md`, `harvest.md`, `footprint/issue-<N>.md`, `coupling.md`, `order.md`, `facts/issue-<N>.md`, `facts/wave.md`, `merge-test/<k>.md`, `reports/issue-<N>-<phase>.json`, `gate/issue-<N>.md`, `baseline.txt`. A finished wave moves to `<COMMON>/work-wave/closed/wave-<WAVE_ID>/`. Under the common dir for `work-issue`'s reasons: one location every lane's worktree can see, invisible to `git status`, and it outlives `git worktree remove`. It holds outputs, and nothing in it says which step the wave believes it reached.
- **HANDBACK** — WAVE_DIR, spelled absolute. It is the one path every lane is told to write to and to name in its report, and every location a lane reports—its `worktree` and its `run_dir`—is absolute or is refused, while `files_changed` stays repo-relative by the brief's contract: subagent shells reset their working directory between calls, so a worktree-relative path in a report addresses whatever tree the reader happens to be in.
- **PLAN[N]** — per issue, first hit wins: the `--plan N=PATH` argument; `<ROOT>/docs/plans/*issue-<N>*.md` or `<ROOT>/docs/plans/*-<N>-*.md`, newest by name; a path linked from the issue under a `Plan` heading. These are `work-issue`'s routes 1 through 3. Its route 4—the plan held in the conversation—is unreachable from a fresh subagent, so a plan that resolves only there is a missing plan here. Each hit is made absolute, and that absolute path is what the lane's argument line carries, as `work-issue`'s route 1.
- **LANE[N]** — the lane's derived names, all `work-issue`'s: BRANCH `issue-<N>`, WORKTREE `<ROOT>/../<PROJECT>-issue-<N>/`, RUN_DIR `<COMMON>/work-issue/issue-<N>/`.
- **LANE_MODEL** — `opus`, or `fable` from `--lane-model fable`. Never lower: a lane runs `divvy-up`'s gate, `code-review`, and a red-team on whatever model it was dispatched at, and that model is the judgment `divvy-up` keeps on the session model for a reason.
- **MERGE_TREE** — `<ROOT>/../<PROJECT>-wave-<WAVE_ID>-merge/`. Exists only while a merge test runs.
- **VERIFY_CMD**, **INSTALL_CMD** — harvested off disk the way `work-issue` harvests: manifest scripts first (`package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`); then runnable scripts under `tests/` or `scripts/`; then what `.github/workflows/` runs; then `absent`.
- **CONTRACT_PATHS** — the union, across every lane's plan, of paths `divvy-up` Step 1 would make wave-0 tasks: types, interfaces, schemas, migrations. A lane whose build report names one of these, in `files_changed` or in `contract_changed`, triggers a merge test at Step 5.
- **FLAGS** — `--dry-run` runs Steps 0 through 3, renders the confirmation, and dispatches nothing, creates no worktree, and pushes nothing.

`gh auth status` is a Step 0 preflight. Unauthenticated stops the run: the issues cannot be read, and route 3 of PLAN cannot be followed.

## Step 0 — Gate

1. Run the resume probe (see [Resume](#resume)) before anything is written under WAVE_DIR. Row 2 matches a fresh wave and a wave interrupted inside this step alike, and both run the rest of this step from item 2; any later row jumps there.
2. Resolve PLAN[N] for every issue. Any issue whose three routes all miss refuses the whole wave, naming every such issue at once: "Plan them first: `writing-plans`, then `work-wave <ISSUES> --plan N=PATH`." One refusal listing three missing plans beats three runs each finding one, and a wave that starts with two lanes of three is a different wave from the one the user asked for.
3. `gh issue view N --json title,url,body` for each, and write `WAVE_DIR/lanes.md` with one row per lane: `| Lane | Title | Plan | Worktree | Run dir |`, every path absolute.
4. In-flight `work-issue` runs. Any `<COMMON>/work-issue/issue-N/` for an N in ISSUES that is not under `closed/` is a lane already started. It stays in the wave: Step 1 proves its footprint on its `RUN_DIR/plan.md`, Step 3's collision check exempts its worktree, and Step 4's dispatch reaches it through `work-issue N`, whose own resume probe places it. Any `issue-M/` for an M not in ISSUES is a sibling this wave does not own, and Step 1 hands it to the script with `--runs` so its footprint is proved against every lane's.
5. Harvest VERIFY_CMD and INSTALL_CMD, and derive CONTRACT_PATHS by reading every plan for the contract shapes.
6. Last, after items 1 through 5, write `WAVE_DIR/harvest.md`: the already-started lanes and the in-flight siblings item 4 found, VERIFY_CMD, INSTALL_CMD, and CONTRACT_PATHS. It is the resume probe's only evidence that this step finished. `lanes.md` exists from item 3 on, so a run interrupted during items 4 or 5 leaves a WAVE_DIR with no `harvest.md`, and resume row 2 sends it back through this step rather than on to Step 1 without its siblings found or its commands harvested.

**Done when:** every issue in ISSUES has an absolute PLAN[N] on disk, `lanes.md` names every lane with absolute paths, `gh` is authenticated, VERIFY_CMD is resolved or `absent`, and `harvest.md`, written last, records item 4's runs, VERIFY_CMD, INSTALL_CMD, and CONTRACT_PATHS—or the run stopped at the refusal naming every issue without a plan, or at fewer than two issues.

## Step 1 — Footprint

For each lane, read PLAN[N] and write `WAVE_DIR/footprint/issue-<N>.md`: one bare repo-relative path per line, an exact file or a directory prefix ending in `/`, taken from every `Files:`, `**Files:**`, `owns:`, or `Files owned` line and from a `## Waves` table where the plan already carries one. Bare, with no backticks and no links, because the script refuses decoration rather than stripping it, and the reason it gives has to quote a string that is in the file.

A lane already started (Step 0 item 4) is proved on its `RUN_DIR/plan.md`, the copy its own `work-issue` builds from, never on PLAN[N]. Where the copy carries a `## Waves` table, pass `RUN_DIR/plan.md` itself as the lane's `--lane issue-N=` argument. Where it has none yet, derive `footprint/issue-<N>.md` from the copy's `Files:` lines and pass that file instead, never the tableless copy: the script reads a plan with no table as a bare path list, so its prose lines become paths and a real overlap passes. The lane's resume builds from the copy, so a source plan edited since then describes work nobody will do.

Then:

```
work-wave/scripts/check-footprints.py --lane issue-113=WAVE_DIR/footprint/issue-113.md --lane issue-114=WAVE_DIR/footprint/issue-114.md … --runs <COMMON>/work-issue
```

A non-zero exit is a hard stop, not a warning. Two lanes owning one path is two worktrees rewriting one file, and the rebase conflict that produces lands at a lane's Step 5 after the user has walked away. Its `pair:` lines on a pass are Step 2's worklist: exactly one per pair of lanes, so the coupling record has a row for every pair and cannot skip one.

Save the output to `WAVE_DIR/footprint/check.txt` on exit 0 only. A non-zero exit's output goes to `WAVE_DIR/footprint/check-failed.txt`, because resume row 4 reads any `check.txt` as a passed proof and would carry a failed one on to Step 2.

Every lane's own `work-issue` will run `check-inflight.py` again at its Step 0 item 6, and that is kept, not relied on. N lanes dispatched in one message write their `## Waves` tables within seconds of each other, and that script skips a sibling whose table is not there yet, so each lane's check can pass against siblings that have not written theirs. This step is the one check that holds every footprint at once, and Step 5 re-runs it over what the lanes actually derived.

So where that script skips, this one fails closed. An in-flight sibling with no parseable `## Waves` table, or whose table carries an entry the script rejects as malformed, prints an `unchecked:` line and exits 1, because its footprint is unknown and an unknown footprint can overlap any lane. A malformed entry voids the whole run's proof, since a backticked `` `src/a.py` `` reads as no overlap with a lane's bare `src/a.py`. A tableless in-flight sibling stops the wave until it writes its table, or until the user moves its run directory to `<COMMON>/work-issue/closed/` because the run is dead. A sibling with a malformed entry stops it until the run's plan spells that entry bare, or until the user moves a dead run to `closed/` the same way. Name the sibling and both ways forward; which one applies is the user's call.

**Done when:** `check-footprints.py` exited 0 over every lane's footprint, each already-started lane's taken from its `RUN_DIR/plan.md` copy, and every in-flight sibling run, each sibling's table read and compared, and its output, `pair:` lines included, is saved to `WAVE_DIR/footprint/check.txt`—or the run stopped at an overlap, or at an `unchecked:` sibling named with both ways forward, with the output in `footprint/check-failed.txt` and no `check.txt` written.

## Step 2 — Couple and order

Take each `pair:` line and ask the question the footprint proof cannot answer: would one lane's change alter what the other builds against? Read both plans against each other for the three shapes `divvy-up` names—both change behavior some third module reads, one fix may make the other unnecessary, both touch a runtime agreement that is neither a type nor a schema—and for the fourth that only appears across lanes: one lane's plan consumes, by name or by path, something the other lane's plan changes. A schema one lane relaxes and another lane's comparison depends on is that fourth shape, and its two diffs are disjoint.

`divvy-up` resolves a coupling inside one tree, by placing a task in a later wave or by merging two tasks into one. Neither exists here. Every lane bases on `origin/DEFAULT` and cannot build on a sibling's branch, and two issues cannot be merged into one task. What a wave can do is order the merges, keep a lane out, or refuse. Write one row per pair into `WAVE_DIR/coupling.md`:

```
| Pair | Answer | Evidence | Resolution |
```

`Answer` is one of `independent`, `directional A→B`, `mutual`, or `unclear`. `Evidence` quotes the plan lines that decided it, or says what was read and found nothing. `Resolution` follows from the answer:

| Answer | Resolution |
|---|---|
| independent | `none` |
| directional A→B, and B merely observes or tests what A changes | `order: B after A`. The merge test at Step 6 is what proves B still passes with A's change in front of it. |
| directional A→B, and B's tasks would write against the thing A changes | `hold: B until A merges`. B built against the old contract merges after A as a tree the merge test then reports red, which spends a lane to learn what both plans already said. B leaves this wave and is named in the final report as the next one. |
| mutual, or either may make the other moot | `refuse`. Two lanes each carrying half of one change are one issue planned twice; say which two, and stop. Serializing them does not fix it, because each lane's plan is still half. |
| unclear | `ask`: a question for Step 3, written down here rather than settled by a guess three lanes will build on. |

Then `WAVE_DIR/order.md`, the merge order:

```
| Order | Lane | After | Why |
```

Topological over every `order:` row, ties broken by issue number ascending, so two runs on one set of plans produce one order. `After` names the lanes this one merges behind, or `—`. `Why` quotes the coupling row or says `no coupling; number order`. A held lane appears with `Order` `held` and its `After` naming the lane it waits on. The order is also the sequence the merge test merges in, and the sequence the final report hands the human.

**Done when:** `coupling.md` has one row per `pair:` line, each with an answer, evidence, and a resolution from the table; `order.md` places every lane that stays, names every held lane and what it waits on; and every `unclear` pair is a written question—or the run stopped at a `refuse`.

## Step 3 — Confirm

Put every `ask` row to the user before anything else, and settle each one into `order`, `hold`, or `none` on its coupling row.

Then the collision check. For every lane that is not held, test whether its WORKTREE path from LANE[N] already exists, as a directory or as an entry in `git worktree list --porcelain`. Any hit refuses the wave here, naming every such path at once. A tree already sitting at a lane's own `<PROJECT>-issue-N` path lands that lane on `work-issue`'s isolation `ask` row, which an unattended lane cannot answer, and the table states no precedence between that row and `--isolate`'s pin. So the check runs whatever `--isolate` turns out to do. A lane already started (Step 0 item 4) is exempt when its WORKTREE is registered in `git worktree list --porcelain` on its own `issue-N` branch: `work-issue` made that tree, and its resume probe reads it rather than the isolation table.

Then one confirmation, in one message:

```
Wave 113-114-115: 3 lanes on opus, worktrees at `../skills-issue-113/`, `../skills-issue-114/`, `../skills-issue-115/`. Footprints disjoint (7 paths, checked 1 in-flight run). Coupling: 113→115 directional, so 115 merges after 113; 114 independent. Merge order: 113, 114, 115. Held: none. Merge test: baseline now, on any contract change, before any pull request, and before the final report. On yes: each lane runs `work-issue N <plan> --isolate --no-publish` unattended through its red-team, then, once the merge test is green, runs again without `--no-publish` to push `issue-N` and open a pull request against `main`. Never `main`. Go?
```

The shape line is the user's correction point, so the merge order and the held lanes are in it rather than in a file they would have to open. This confirmation answers each lane's `work-issue` Step 0 confirmation on the user's behalf, in two halves: the execute-and-commit half now, and the push-and-pull-request half only when Step 7 re-dispatches the lane after a green merge test. The lane brief says so, and `work-issue` does not ask again. `--dry-run` renders this message and stops.

**Done when:** every `ask` row is settled, no unheld lane's WORKTREE path exists outside the already-started exemption, and the user answered yes to the wave as shaped—or the run stopped at a collision naming every existing path, a no, or a dry-run, with nothing dispatched and no worktree made.

## Step 4 — Baseline and dispatch

Run the merge test once with no branches, per [references/merge-test.md](references/merge-test.md): `git worktree add --detach MERGE_TREE origin/DEFAULT`, INSTALL_CMD, VERIFY_CMD with its tail saved to `WAVE_DIR/baseline.txt` and the run recorded as `WAVE_DIR/merge-test/0.md`, then `git worktree remove --force MERGE_TREE`. Before any lane spends anything, this proves the mechanism—the install, the suite, the removal—and records what green looks like on DEFAULT, so a red merge later can be pinned on a lane rather than on the tree the wave inherited.

Then read [references/lane-brief.md](references/lane-brief.md) and instantiate it once per lane that is not held, with `{{PHASE}}` `build` and `{{GRANT}}` the build half. Dispatch every lane in a SINGLE message so they run concurrently—one dispatch per message is the serialization the wave exists to remove. Name LANE_MODEL on every dispatch. Each lane is a general-purpose subagent told to invoke `work-issue` by name with `<N> <PLAN[N]> --isolate --no-publish`, and nothing about its worktree, its branch, or its run directory is made here: `work-issue`'s Step 1 makes them, and `--isolate` is what keeps its isolation table from asking a question an unattended lane cannot answer. `--no-publish` stops the lane once its Step 4's Done-when holds, so the withheld push half holds at the lane even when the grant is misread.

Every git write on a lane's branch belongs to that lane's `work-issue`, and every git write on MERGE_TREE belongs to you. This skill itself never commits, never pushes, and never touches `issue-N` or DEFAULT.

Save every returned report verbatim to `WAVE_DIR/reports/issue-<N>-build.json`. A report that does not parse as the contract in the brief is re-prompted once with the contract restated; still unparseable, the lane is `failed`.

**Done when:** `merge-test/0.md` and `baseline.txt` exist and MERGE_TREE does not; every unheld lane was dispatched in one message at LANE_MODEL with the build grant; and every report is on disk verbatim.

## Step 5 — Gate a lane

As each build report returns:

1. **Facts.** The lane's `facts` array and its `WAVE_DIR/facts/issue-<N>.md` are the same list; where they differ, the file is the one the lane wrote as it went and wins. Nothing else to do: every other lane reads the directory, and the next dispatch inlines all of it.
2. **Footprint, again.** Re-run `check-footprints.py` with every returned lane's `RUN_DIR/plan.md` in place of its footprint file, the unreturned lanes still on their footprint files, and `--runs` as before. The lane's `## Waves` table is the footprint it actually wrote, and a lane whose derivation drifted onto a sibling's path is found here rather than at the merge.
3. **Contract change.** Any path in the lane's `files_changed` under CONTRACT_PATHS, or any path in its `contract_changed` (the wave-0-owned subset the lane reports), triggers a merge test now over every lane branch that has commits, returned or not: `git -C ROOT rev-parse --verify issue-M` for each. A schema relaxed in one lane is the change the others should meet while they still build, and they meet it early only when this lane returns ahead of them. The result goes into `WAVE_DIR/facts/wave.md`, the one facts file the orchestrator owns, as a line: `- [wave] merge test k: <green|red at issue-A × issue-B: paths>`. Every lane reads the whole `facts/` directory before each dispatch, so the line reaches every still-running lane.

   A red result is read against `coupling.md` the way Step 6 reads one: a pair recorded `independent` that is not gets its row corrected. Name the lane whose change broke the other in that `facts/wave.md` line, so its dependents still building meet the break at their next dispatch. The wave carries on to Step 6, and a red that persists there stops the wave with the pair named. Nothing publishes on a red.
4. **Route.** Before routing a build report, run `gh pr list --head issue-<N> --state all --json url --jq '.[].url'` for its lane. A non-zero exit stops the wave with its stderr quoted and writes no gate record for that report, because a failed command cannot answer "no pull request". The missing record sends the report back through this step on resume, so the check runs again once `gh` works.

| Report | Route |
|---|---|
| a `build` report whose `pr` is non-null, or for which `gh pr list --head issue-<N> --state all --json url --jq '.[].url'` prints a URL | The lane published before the merge test, against its withheld grant. Either signal stops the wave, with the lane and its pull-request URL named; whether that pull request stays open is the user's call. The lane fills `pr` itself, so GitHub's answer is the one that catches a lane that opened a pull request and reported `pr` as null. |
| the footprint re-check (item 2) exited non-zero | Stop the wave with the script's stderr lines quoted, the way Step 1 stops on a non-zero exit. Nothing proceeds to Step 6. |
| `done` | The lane waits at Step 6. |
| `stopped` | The lane's question is held for the user with the wave's next message. The lane is out of the merge set until `work-issue N` resumes it with the answer, and every lane ordered after it in `order.md` is moved to `held`. |
| `failed`, or `refused` at its own gate | The lane is out of the merge set; lanes ordered after it are moved to `held`; every other lane proceeds. No revert, because its writes are on its own branch in its own worktree and clobbered nothing; no rung-up retry, because `work-issue` has already applied `divvy-up`'s retry inside the lane and LANE_MODEL is already the rung a retry would reach. Its report is quoted in the final report, and `work-issue N` resumes it once a human has read that. |
| `worktree` or `run_dir` not absolute, or `head` not a SHA | Re-prompt once for the absolute form and the SHA. A relative path in a report is the round trip this skill exists to remove. |

5. **Gate record.** Last, after items 1 through 4, write `WAVE_DIR/gate/issue-<N>.md`: the route item 4 took (`done`, `stopped`, `failed` or `refused`, the early-publish stop, or the failed re-check stop), the footprint re-check's exit and output, and the contract-change merge test's `merge-test/<k>.md` path and result line, or `none` where nothing triggered one. Where item 4's `gh pr list` exited non-zero, the wave stops with no gate record for that report, so a resume runs the check again. The record is the resume probe's only evidence that this step finished for a report: a build report saved at Step 4 with no gate record beside it returned just before an interruption, and goes back through this step rather than past it. A gate record whose route is the early-publish stop or the failed re-check stop is a recorded stop, and the resume probe stops the wave again on it.

**Done when:** for every returned lane, its facts are on disk, the footprint re-check exited 0 or the wave stopped on it with the stderr lines quoted, a contract change ran the merge test and its result is a line in `facts/wave.md`, a red one naming the lane that broke the other with the pair's `coupling.md` row corrected where it said `independent`, no build report carries a `pr` and no `gh pr list` for a build lane printed a URL, the lane is `done` or is out of the merge set with its dependents held and the reason recorded, and its `gate/issue-<N>.md` records the route, the re-check, and the merge-test result, written after all of them—or a failed `gh pr list` stopped the wave with its stderr quoted and no gate record written. A recorded stop ends the wave here, with nothing proceeding to Step 6.

## Step 6 — Merge test before publish

Enter when every unheld lane has returned, every build report in the merge set has its `gate/issue-<N>.md`, and no gate record is a recorded stop; otherwise go back to Step 5. Run the merge test per [references/merge-test.md](references/merge-test.md) over the merge set in `order.md`'s order, one `git merge --no-ff --no-edit issue-N` at a time, then INSTALL_CMD and VERIFY_CMD, recorded as `WAVE_DIR/merge-test/<k>.md` with the `base:` it merged onto and the SHA of every branch merged.

A conflict names the branch that failed to merge and every branch it conflicts with: each branch already merged in this run whose own diff against the `base:` touches a conflicted path, or DEFAULT where none does. The branch merged just before it may have touched none of those paths. Record the `conflict:` line merge-test.md step 3 gives, `git merge --abort`, and stop the wave at this step with those branches named. A conflict after a passing footprint proof means a lane wrote outside the footprint it declared, and the lane's own `divvy-up` gate should have caught it; either way, resolving it is a judgment call no unattended run makes.

Red with a green baseline is the cross-lane coupling that every ownership proof passed. Read the failing output against `coupling.md`: a pair recorded `independent` that is not gets its row corrected, and the lane whose change broke the other is the one held. Stop with the evidence; nothing publishes. A red suite is not routed back to a lane for repair here, because the repair belongs to whichever issue the coupling makes it belong to, and that is the question the user answers.

Green, with `git -C MERGE_TREE diff --stat HEAD` and `git -C MERGE_TREE ls-files --others --exclude-standard` both empty, proceeds. The first catches a tracked file the suite changed, the second an untracked file it wrote, which `diff` never shows; either non-empty is `dirty after verify:` and red, the untracked paths listed. Neither is `git status`: the status read that once reported clean over a staged index ran in a copied tree whose index was shared, and `ls-files --others` reads MERGE_TREE's own index. Remove MERGE_TREE.

**Done when:** `merge-test/<k>.md` records its `base:`, every merged SHA, the merge result, and VERIFY_CMD's real tail; the result is green and both post-verify checks were empty; MERGE_TREE is gone—or the run stopped on a conflict naming the branches it is with, or on a red suite with the pair named, and nothing published.

## Step 7 — Publish

Check the base before any dispatch: `git -C ROOT fetch origin DEFAULT`, then compare `git -C ROOT rev-parse origin/DEFAULT` with the `base:` line of the newest green `merge-test/<k>.md`. Where they differ, DEFAULT moved after the merge test, and each lane's rebase at `work-issue`'s Step 5 would publish a combined tree no merge test saw. Run Step 6 again first. A merge onto the current tip tests the combined tree the lanes' clean rebases produce, not the SHAs they will publish; Step 8's re-test at the published HEADs covers those SHAs, after the pull requests exist. Dispatch only on its green, with the base checked again.

Read [references/lane-brief.md](references/lane-brief.md) again and instantiate it once per lane in the merge set, with `{{PHASE}}` `publish`, `{{GRANT}}` the full grant, and `{{FACTS}}` the directory's current contents. Dispatch every one in a SINGLE message at LANE_MODEL. Each lane invokes `work-issue <N> <PLAN[N]> --isolate` again, with `--no-publish` dropped; `work-issue`'s resume probe reads the red-team clean and no pull request and places the lane at its Step 5, and from there the lane rebases, pushes `issue-N`, opens its pull request, and runs its triage and repair as its own skill says, without asking.

Save every report verbatim to `WAVE_DIR/reports/issue-<N>-publish.json`. Route by the same table as Step 5; a lane that stopped with `triage/waiting` when `work-issue`'s review poll hit its cap is `done` for this wave's purposes, since resolving stays the reviewer's act and `work-issue N` continues it.

**Done when:** the fetched `origin/DEFAULT` equalled the `base:` of the newest green merge test at the moment of dispatch; every lane in the merge set was dispatched with the full grant in one message and its publish report is on disk verbatim; each is `done`, waiting on its reviewer, or out of the merge set with the reason recorded.

## Step 8 — Report

Where the HEAD of any lane in the merge set differs from its SHA in the newest `merge-test/<k>.md`—a repair round moved it—run the merge test once more, in order, before anything is reported. The order the human merges in has to have been tested at the SHAs they will merge.

Then the final report: the merge order as a numbered list of pull-request URLs with each lane's `After`; the held lanes and what each waits on; the failed or stopped lanes with their reports quoted; the path of the newest merge test and its result line; the coupling table; the fact count and the path of `facts/`; and the closing line, "a human merges, in this order", or "waiting on the reviewers" where every lane is answered but none has cleared. Then move WAVE_DIR to `closed/` only when every lane's own RUN_DIR has moved to its `closed/`: before that the wave is still resumable, and a wave directory under `closed/` is what the resume probe reads as finished.

**Done when:** the merge test is green at the current HEAD of every lane in the merge set and the report names the order, the held and failed lanes, the merge-test path, the coupling table, and the facts path, and ends on the line the state earns.

## Resume

The world outranks WAVE_DIR, and WAVE_DIR outranks memory. Each lane's state is `work-issue`'s to read, through its own resume probe, and this skill never guesses at a lane's phase: it asks by re-dispatching `work-issue N`, which resumes itself. WAVE_DIR says only what this skill has already produced. First match wins:

| # | Probe | Resume at |
|---|---|---|
| 1 | `<COMMON>/work-wave/closed/wave-<WAVE_ID>/` exists and no lane RUN_DIR is open | done; say so |
| 2 | no WAVE_DIR, or WAVE_DIR with `lanes.md` or `harvest.md` missing | Step 0 |
| 3 | `lanes.md` and `harvest.md`; no `footprint/check.txt` | Step 1 |
| 4 | `check.txt`; `coupling.md` or `order.md` missing, or a coupling row still `ask` | Step 2 |
| 5 | `order.md`; no `merge-test/0.md` | Step 3, the confirmation again, then Step 4 |
| 6 | `merge-test/0.md`; some saved build report has no `gate/issue-<N>.md`, or some gate record recorded a stop | Step 5 for the ungated reports only, then probe again; a recorded stop stops the wave again, naming the lane and its pull-request URL or the re-check's stderr lines, until the user rules on it |
| 7 | `merge-test/0.md`; some unheld lane has no `reports/issue-N-build.json` | Step 4 for those lanes only, in one message; a lane whose RUN_DIR exists is resumed by its own `work-issue`, and its build report is whatever it returns |
| 8 | every gate record; no `merge-test/<k>.md` with k > 0 whose recorded branches are exactly the merge set, each at its current HEAD | Step 6 |
| 9 | a green merge test over exactly the merge set at its current HEADs; some lane in the merge set has no `reports/issue-N-publish.json` | Step 7 for those lanes only, when the fetched `origin/DEFAULT` equals that merge test's `base:`; where it differs, Step 6, then Step 7 |
| 10 | every publish report; the HEAD of some lane in the merge set moved since the newest merge test | Step 8's re-test, then the report |
| 11 | every publish report; a merge test green over exactly the merge set at its current HEADs | Step 8's report |

A lane's `work-issue` may itself be mid-run on a herdr agent or a stranded worktree; those are its rows 2 and 3, and re-dispatching it is how they get read.

## Further Reading

- [references/lane-brief.md](references/lane-brief.md) — read at Steps 4 and 7 to instantiate each lane's dispatch and the report contract it returns
- [references/merge-test.md](references/merge-test.md) — read at Steps 4, 5, 6, and 8 to build the scratch tree, merge in order, verify, and remove it
- [scripts/check-footprints.py](scripts/check-footprints.py) — run at Step 1 to prove the lanes' footprints disjoint and list the pairs, and at Step 5 to prove it again over what the lanes derived: `work-wave/scripts/check-footprints.py --lane issue-N=PATH --lane issue-M=PATH [...] [--runs DIR]`
