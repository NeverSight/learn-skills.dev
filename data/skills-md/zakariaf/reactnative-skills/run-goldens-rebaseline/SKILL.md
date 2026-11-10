---
name: run-goldens-rebaseline
description: Runs the golden rebaseline ritual - assertions green first, triage, one-file jest -u runs, every diff inspected, recorded, orphans deleted, proof without -u. Use when many goldens must be re-accepted. Not for one golden (golden-and-snapshot-tests).
disable-model-invocation: true
---

# Run goldens rebaseline

The only sanctioned way to re-accept many goldens at once (after a renderer, font, token or Jest
upgrade, or an intended redesign): the real assertions are green first, a triage names the affected
set, each file is re-accepted alone, every changed golden is looked at and recorded, orphans go, and
the whole golden project passes twice without `-u`. `rebaseline.mjs` runs each step and writes the
evidence; `check-rebaseline.mjs` proves it. The developer approves twice.

## Rules that must hold

1. **Re-accept only for a named cause, after a full triage.** `--start --reason "<cause>"`, then the
   whole golden project without `-u` (`triage-first`); every failure must be what that cause predicts.
   Two unrelated causes are two rebaselines. Why: a golden that moved for another reason is a bug, and
   the triage is the only plan.
2. **The real assertions are green first.** Every Jest project except the golden one, complete and
   green, before the first update (`assertions-first`). Why: a golden asserts nothing about
   correctness; re-accepting over a red unit suite freezes the bug.
3. **Nothing but goldens changes once the rebaseline starts, and the install is the lockfile.** Code,
   tests, configs, the lockfile and frozen golden paths keep the hash `--start` recorded
   (`source-changed`); `node_modules` equals `package-lock.json` (`install-matches-lock`). Why: a fix
   made mid-way hides inside the re-accepted output, and a stale install writes goldens CI cannot
   reproduce.
4. **One file per `-u` run, path first, previewed, by hand.** `jest <file> --selectProjects golden
   --ci -u` after `--listTests` lists only that file (`update-one-file`). Never `-u` in package.json
   scripts, git or agent hooks, or CI; only this skill's runner, invoked by hand once per planned file,
   runs it. Why: after `--selectProjects` a path is read as a project name and every golden is
   rewritten (verified).
5. **Only files the triage shows failing or holding obsolete entries are updated** (`update-unplanned`).
   Why: updating anything else is how unrelated drift slips in under the cause.
6. **Goldens change only through a logged update run.** No hand edit of a `.snap*` or PNG; only
   orphans are deleted by hand (`golden-changed-unlogged`). A header-only rewrite after a Jest major is
   the one exception the checker recognises. Why: a hand edit records output the code does not produce.
7. **Every changed golden is inspected and recorded.** Read the `.snap` diff line by line; open each
   triage diff composite and each new PNG; one `inspection.json` entry per changed path with verdict
   `intended` or `orphan` and a note of at least 15 characters (`inspection-record`). Anything less
   than a clear yes means stop. Why: the look is the whole review; an unread golden freezes a bug.
8. **Contract entries are never re-accepted.** A failing `[contract]` assertion stops the ritual:
   stop and ask the reviewer; the runner refuses to update such a file and the checker compares every
   contract entry with its recorded hash (`contract-entry-changed`). Why: installed versions and kept
   files still expect the old output.
9. **Tolerances are out of scope.** The pixel matcher and `contracts/goldens.json` stay byte for byte
   (`tolerance-changed`); a raise goes through the reviewer in its own commit (golden-and-snapshot-tests).
   Why: a raised tolerance silently accepts every future regression below it.
10. **Orphans are deleted by hand, in the same change, before the proof.** No snapshot outlives its
    test, no PNG outlives the test that claims it (`orphan-golden`). Why: Jest never reports a
    `.snap.ios` orphan, and jest-image-snapshot only deletes unused images through its opt-in
    outdated-snapshot reporter, which deletes without a record and, on a one-file run, deletes other
    tests' live baselines (verified); so `JEST_IMAGE_SNAPSHOT_TRACK_OBSOLETE` stays unset for the whole
    ritual (`--update` refuses while it is set).
11. **Proven twice without the flag, over the whole golden project** (`proof-without-flag`): `--ci`,
    no `-u`, green, nothing written, no obsolete entry, every golden test ran, and no golden changed
    after it (`proof-goldens.json`). Why: the first run proves the new goldens reproduce, the second
    catches output that changes between runs.
12. **Stop and ask twice, then one dedicated commit.** Before the first update (show the plan) and
    before the commit (show the record), wait for the developer's go-ahead. The commit holds the cause
    and the goldens only, names every re-accepted test and deleted orphan, and ends with a
    `Gate-Change:` trailer (`rebaseline-message`). Why: the agent that wrote the change should not be
    the only reviewer of its goldens, and the history must say what moved and why.

## Workflow

1. **Decide it is a rebaseline.** Read "When a rebaseline is the right tool" in
   [references/rebaseline-ritual.md](references/rebaseline-ritual.md). One golden moving with your
   change is golden-and-snapshot-tests' one-file flow; a contract entry or a tolerance is never this.
2. **Prepare** ("Before you start"): the cause final in the tree, unrelated work committed or stashed,
   goldens committed, `npm ci`, `JEST_IMAGE_SNAPSHOT_TRACK_OBSOLETE` unset.
3. **Start:** `node ${CLAUDE_SKILL_DIR}/scripts/rebaseline.mjs . --start --reason "<cause>"` (add
   `--dry-run` first to see the checks without writing). It refuses a stale install, uncommitted
   goldens or an orphan snapshot holding `[contract]` entries (settle that with the reviewer first),
   and lists orphans already present; fix and rerun.
4. **Assertions:** `node ${CLAUDE_SKILL_DIR}/scripts/rebaseline.mjs . --assertions --max-workers 2`.
   Red means stop: fix the code, then `--start --restart`.
5. **Triage:** `node ${CLAUDE_SKILL_DIR}/scripts/rebaseline.mjs . --triage`. Read every failure and
   open every composite it lists under `reports/rebaseline/triage-diffs/` (left baseline, red
   differences, right new render). Decide each with the triage table in the ritual reference.
6. **Stop and ask the developer before the first update:** show the plan
   ([examples/approval-requests.md](examples/approval-requests.md), part 1) and wait for the go-ahead.
7. **Update each planned file alone:** `node ${CLAUDE_SKILL_DIR}/scripts/rebaseline.mjs . --update
   <file>`. It previews with `--listTests`, runs `--ci -u` on that file and lists what changed.
8. **Inspect and record:** `git diff -- <snapshot>` line by line; open each new PNG next to its
   composite; fill each `todo` entry in `reports/rebaseline/inspection.json`
   ([examples/inspection.json](examples/inspection.json)). Not a clear yes: revert that path, stop, fix.
9. **Delete orphans:** `git rm` each snapshot whose test is gone and each PNG no test claims; record
   them with verdict `orphan`.
10. **Prove:** `node ${CLAUDE_SKILL_DIR}/scripts/rebaseline.mjs . --proof` (two runs; it records the
    goldens it ran against, so any golden touched afterwards means another `--proof`).
11. **Check:** `node ${CLAUDE_SKILL_DIR}/scripts/check-rebaseline.mjs .`; fix every FAIL (file, rule,
    fix) and rerun until `RESULT: PASS`. Rules, options and limits:
    [references/evidence-and-checker.md](references/evidence-and-checker.md); the Jest behaviour behind
    them: [references/jest-facts.md](references/jest-facts.md).
12. **Stop and ask the developer before the commit:** show the record and the PNGs (part 2 of the
    approval example) and wait for approval.
13. **Commit:** write `reports/rebaseline/commit-message.txt`
    ([examples/rebaseline-commit.txt](examples/rebaseline-commit.txt)), run
    `node ${CLAUDE_SKILL_DIR}/scripts/check-rebaseline.mjs . --message reports/rebaseline/commit-message.txt`,
    then `git commit -F reports/rebaseline/commit-message.txt`; delete `reports/rebaseline/`.

## Definition of done

- [ ] The cause is named in `before.json` and every re-accepted golden is explained by it.
- [ ] The developer approved the plan before the first update and the record before the commit.
- [ ] No `[contract]` entry, pixel matcher or `contracts/goldens.json` changed; no tolerance moved.
- [ ] Every changed golden has an `intended` or `orphan` entry with a real note; orphans are deleted.
- [ ] One commit holds the cause and the goldens, names every re-accepted file, ends with `Gate-Change:`.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-rebaseline.mjs . --message reports/rebaseline/commit-message.txt` prints `RESULT: PASS` (no SKIP lines are expected)

## Anti-patterns

- **`npx jest -u` to make a red suite green.** It rewrites every differing golden, bugs included. Read
  the failures, fix the code, re-accept only the planned files.
- **`npx jest --selectProjects golden <file> -u`.** The path becomes a project name and every golden is
  rewritten. Put the path first; let `--update` preview it.
- **Following Jest's "To remove it, run `npm test -- -u`".** That updates the whole project. Use
  `--update <file>` on the file with the obsolete entry.
- **Fixing a bug found during the rebaseline and carrying on.** The fix is then hidden in re-accepted
  output. Revert the goldens, fix, `--start --restart`.
- **Re-accepting a subset of the failures "for now".** The rest fail on the next run and get accepted
  unread later. Plan the whole affected set, or fix what is not the cause.
- **Reading the diffstat instead of the diffs.** "12 PNGs changed" says nothing. Open each composite
  and each new image; an unrelated surface that moved is what the ritual exists to catch.
- **Raising `failureThreshold` because the upgrade is noisy.** CanvasKit renders are deterministic;
  a tolerance raise needs the reviewer and its own commit.
- **Running the ritual in CI or a hook.** A gate that rewrites what it checks asserts nothing. CI runs
  `jest --ci` and only proves.
- **Committing the evidence or a diff image.** `reports/` is git-ignored; the record lives in the
  commit message and the pull request.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/rebaseline-ritual.md](references/rebaseline-ritual.md) | When to rebaseline, preparation, every step and why, reading data and pixel diffs, triage table, the two stop-and-ask moments, the commit, Jest majors, renamed tests, Skia upgrades, screenshot baselines, iOS and Android, multi-package | Workflow steps 1, 2, 5 and 13 |
| [references/jest-facts.md](references/jest-facts.md) | Verified Jest 29.7 / jest-expo 57 / jest-image-snapshot 6.5.2 behaviour: path order, `--ci -u`, obsolete entries, orphans, image updates, the `--json` result, Jest majors, with re-verify commands | When a Jest fact matters or after a Jest upgrade |
| [references/evidence-and-checker.md](references/evidence-and-checker.md) | The evidence folder, `before.json` and `inspection.json` formats, the runner's modes and refusals, the checker's rules, config keys, expected output, limits, troubleshooting | Workflow steps 3 to 11 |
| [examples/inspection.json](examples/inspection.json) | A filled inspection record for one cause, a Skia upgrade (pixel goldens, an orphan) | Workflow step 8 |
| [examples/approval-requests.md](examples/approval-requests.md) | What to show the developer before the first update and before the commit (the same Skia upgrade) | Workflow steps 6 and 12 |
| [examples/rebaseline-commit.txt](examples/rebaseline-commit.txt) | Rebaseline commit messages (the same Skia upgrade, a Jest-major header rewrite) | Workflow step 13 |
| `scripts/rebaseline.mjs` | Runs one step (`--start`, `--assertions`, `--triage`, `--update <file>`, `--proof`) and writes its evidence; refuses out-of-order or unsafe steps | Workflow steps 3 to 10 |
| `scripts/check-rebaseline.mjs` | Proves the ritual from the evidence and the tree (13 rules), and with `--message` the commit message | Workflow steps 11 and 13, the definition of done |
| `scripts/lib/rebaseline-lib.mjs` | Shared logic: layout and config, inventory and hashes, snapshot parsing, image claims, Jest results, lockfile comparison | When a script changes |
| `scripts/selftest.mjs` | Proves both scripts against the fixtures (the bases are built with the real `--start`) | After changing a script or a fixture |
| `scripts/check-lib.mjs` | Shared script library (synced; do not edit here) | Never by hand |
| `assets/shared.json` | Declares the synced check-lib | When adding a shared file |
| `tests/bases/` | `before/` (a small Tasks app with data and pixel goldens), `after/` (the re-accepted state), `evidence/` (Jest results and the record), `runner/` (a fake Jest for the runner suite) | When the fixture base changes |
| `tests/fixtures/` | Overlay suites for both scripts: `good/`, one or more `bad-*` per rule, `pass-*` and `error-*` cases; a case's `ENV.txt` sets an environment variable for that case only | When adding a rule or a refusal |

## Related skills

- `golden-and-snapshot-tests` - the golden policy, the one-file flow, contracts, tolerances and the history checker for the commit.
- `unit-and-component-tests` - the Jest projects and the assertions that must be green first.
- `e2e-maestro` - simulator and emulator screenshot baselines and their compare run.
- `skia-canvas-rendering` - the drawn surfaces whose pixel goldens move with a renderer upgrade.
- `design-system-structure` - token changes that move drawn surfaces.
- `dependency-management` - the dependency bump that is often the cause, and `npm ci`.
- `expo-sdk-upgrade` - SDK moves that bring Jest majors and renderer upgrades.
- `seeded-determinism-and-golden-vectors` - golden vectors, which are never re-accepted.
- `git-commits-and-reporting` - the commit format and the Gate-Change trailer.
- `quality-gates` - gated paths and the commit-msg hook that asks for the trailer.
- `ci-pipeline-and-gates` - CI runs `jest --ci` and only proves goldens.
