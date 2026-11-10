---
name: run-migration
description: Runs the release ritual for a SQLite schema version - snapshot proven, one pending step, shipped steps frozen in a ledger, every from-to path, a forced-failure drill. Use when shipping a migration. Not for writing steps (persistence-and-migrations).
disable-model-invocation: true
---

# Run migration

Ships one SQLite schema version so that no phone loses a row: the snapshot is proven before release,
only one version is pending, shipped steps and fixtures stay byte for byte as a ledger recorded them,
every from-to path and a forced-failure restore drill pass on Node, the upgrade is proven on iOS and
Android, and the version is recorded only after the developer confirms the release.

## Rules that must hold

1. **Snapshot first, proven before every release.** The open path copies the file
   (`VACUUM INTO '<file>.v<from>.bak'`) before the first pending step and migrates nothing without
   it; the restore drill proves it on real files (`restore-drill`). Why: the snapshot is the only way
   back from a step that committed but was wrong.
2. **One pending version per release (bump by one).** At most one step is newer than the ledger;
   while it is pending, change it in place and re-freeze its fixture; step files run 1..N without a
   gap and `MIGRATIONS` lists exactly those files in order (`bump-by-one`). Why: every shipped step runs on every future install forever, and a second
   pending step is a permanent version no phone ever needed.
3. **Shipped means frozen, and the ledger says what shipped.** `contracts/schema-ledger.json` lists
   each version that reached a device with the sha256 of its step file and fixture, as the build's
   git ref holds them (`--ref`); a shipped step or fixture never changes, not even a comment, a
   formatter rewrite or a lint autofix; the ledger only grows, and CI compares it with the target
   branch (`ledger`, `shipped-frozen`, `ledger-append-only`, `ref`). Why: the replay compares
   schemas, so an edited data move slips past it, and installed apps never rerun a step.
4. **The pending version is frozen before it ships:** its `db-vN.sql` is dumped from a database that
   version wrote and stamps `user_version = N` (`pending-fixture`). Why: the next step is tested on
   it, and the ledger pins it the day it ships.
5. **That fixture holds hostile rows:** an escaped apostrophe, a non-ASCII letter and an emoji
   (`hostile-rows`). Why: copy and transform steps mangle exactly those; `'test1'` survives everything.
6. **Every version from 2 has a content test** `test/sqlite/vNNNN-<name>.test.ts` that loads
   `db-v(N-1).sql`, migrates and compares stored values row by row, untouched tables included
   (`content-test`). Why: a schema or count check passes a step that rewrites every value wrong.
7. **Every from-to path is proven:** an empty file and every frozen fixture, upgraded to every later
   version, give that version's frozen schema, keep every row and pass integrity and foreign key
   checks, in Jest (`migration-paths.test.ts`) and in the checker (`every-path`, `path-tests`). Why:
   users skip updates, backups restore old files into new builds, and a step that works on a fresh
   install can fail on every phone that has data.
8. **The forced-failure drill passes:** a step failing halfway leaves the file's content as it was
   and its snapshot equal to it; a committed wrong step is undone by restoring the snapshot, which then opens as
   `ready`; the previous build opens the upgraded file as `newer-version` and leaves its bytes
   untouched, no `-wal` beside it (`restore-drill`, `migration-restore-drill.test.ts`). Why: the way back is the code path nobody runs until the day
   it is needed.
9. **Stop and ask before the version leaves the machine, then record it.** Any store, TestFlight,
   Play testing, EAS preview build or EAS Update on any channel (preview included) counts as shipped,
   with no exception; `record-shipped.mjs --yes` runs only after the developer confirmed the release
   and it left. Why: from that moment the step is permanent on someone's phone.
10. **Never send a phone back past a shipped version; fix forward.** Re-releasing older code, an
    older TestFlight build, `eas update:rollback` (or its alias `eas update:roll-back-to-embedded`),
    or reverting an EAS Update rollout (`eas update:revert-update-rollout`, `eas channel:rollout` End >
    Revert) puts code with N-1 steps on phones at version N; so does expo-updates by itself when an
    update crashes before its first screen on its first launch. Halting a store phased release or
    staged rollout is fine, and so is pausing the channel (`eas channel:pause <channel>`): neither
    sends anybody back. Those phones open `newer-version`, in memory, with none of the user's data.
    Why: a rollback cannot un-migrate a file; version N+1 can repair it.
11. **Restore only with the app stopped, the replaced files kept, and the developer's yes.**
    `restore-snapshot.mjs` checks the copy, moves `app.db`, `-wal` and `-shm` into `kept-<time>/`,
    and reads the result back; afterwards only a fixed build launches. Why: a leftover `-wal` replays
    newer pages into the restored file, and the same build reruns the same step.
12. **Prove the upgrade over the previous release on iOS and Android** (a named simulator and
    emulator: the previous build, data, the new build over it) before the stop-and-ask. Why: Node
    proves the SQL; only a device proves the build carries the step and finds the real file.
13. **A schema step ships in a store build, unless its update follows the variant channels.** An
    EAS Update with a step needs rule 12's proof first (a Release build of the same JavaScript over
    the previous release's data, crash-free to the first screen), then goes to the preview channel
    (that publish ships the version: stop and ask, then record it), runs crash-free on a preview build
    that holds data, and only then goes to production with a staged rollout (ota-updates' channel
    model: one channel per variant, published per channel). Why: the open path migrates before the
    first render, so a crash before it makes expo-updates roll the phone back to N-1 code over a
    version-N file, with no one deciding it.

## Workflow

1. Read [references/release-ritual.md](references/release-ritual.md) (what shipped means, the ledger,
   one pending version, the order, rollbacks). The data layer comes from persistence-and-migrations;
   without `src/data/migrations/migrations.ts` this skill does not apply.
2. First time only: copy `templates/contracts/` and `templates/test/sqlite/`. An app that already
   shipped versions runs `node ${CLAUDE_SKILL_DIR}/scripts/record-shipped.mjs . --adopt --build '<first build>' --ref <newest release tag>`,
   shows the entries to the developer (stop and ask: are these all out?), then reruns with `--yes`.
3. Baseline: `node ${CLAUDE_SKILL_DIR}/scripts/check-migration.mjs .` prints `RESULT: PASS` before
   any change; fix a red baseline first.
4. Write the content test first, then the step, following persistence-and-migrations' "Adding
   version N+1"; imitate `examples/v0002-pending/` (step, list, frozen fixture, checksums, content
   test, ledger with v1 shipped). Read [references/proofs-and-drills.md](references/proofs-and-drills.md)
   for the content test and hostile rows.
5. Freeze the pending fixture with hostile rows (persistence-and-migrations' `inspect-database.mjs --dump`),
   record its checksum and `FIXTURES` entry.
6. Run `npx jest test/sqlite --ci --maxWorkers=2` and `node ${CLAUDE_SKILL_DIR}/scripts/check-migration.mjs .`;
   fix, rerun until both pass.
7. Prove the upgrade on a named iOS simulator and Android emulator ("Upgrade over the previous
   release" in release-ritual.md); hand the file check and kill test to persistence-and-migrations.
8. Commit the step, test, fixture, checksum and repository change together with a `Gate-Change:`
   trailer (git-commits-and-reporting); CI runs `node ${CLAUDE_SKILL_DIR}/scripts/check-migration.mjs . --base origin/main`.
9. Stop and ask: "This release makes schema version N permanent on every phone that installs it:
   <what changes>. Ship it?" For an EAS Update add: "The Release build of this code ran crash-free
   over the previous release's data (and, for production, on the preview update <id>). If it crashes
   before its first screen, expo-updates sends phones back to the previous update, and a rollout
   revert or `eas update:rollback` does the same; those phones then run without their data until a
   fix-forward update arrives." Only on a yes does the build or update go out
   (eas-build-and-submit, ios-release-testflight, android-release-play, ota-updates).
10. After it left: `node ${CLAUDE_SKILL_DIR}/scripts/record-shipped.mjs . --build '<build>' --ref <the build's commit or tag>`
    (dry run; `--ref` hashes what shipped and fails when the working tree differs), then `--yes`;
    commit the ledger.
11. A pending step went wrong on a developer or QA device: read
    [references/restore-on-device.md](references/restore-on-device.md), run
    `node ${CLAUDE_SKILL_DIR}/scripts/restore-snapshot.mjs --udid <udid> --bundle-id <id>` (or
    `--serial <serial> --package <id>`, or `--dir <folder>`), show the plan, stop and ask, then rerun
    with `--yes`. A shipped step that went wrong is fixed forward in version N+1, never restored.
12. Finish with `node ${CLAUDE_SKILL_DIR}/scripts/check-migration.mjs .` until it prints `RESULT: PASS`.

## Definition of done

- [ ] `contracts/schema-ledger.json` lists every shipped version with both hashes; no entry changed; at most one pending version, and step files run 1..N.
- [ ] No shipped step or fixture changed by a single byte (check-migration `shipped-frozen`).
- [ ] The pending version has its frozen `db-vN.sql` (hostile rows included), checksum and `FIXTURES` entry, and its content test loads `db-v(N-1).sql` and compares values.
- [ ] `test/sqlite/migration-paths.test.ts` and `migration-restore-drill.test.ts` are present; `npx jest test/sqlite --ci` passes.
- [ ] The upgrade over the previous release ran on a named iOS simulator and Android emulator, or the report says it is owed.
- [ ] The developer confirmed the release before it left; `record-shipped.mjs --ref <build ref> --yes` ran after it left and the ledger is committed (or the report says the version is still pending).
- [ ] A step shipped by EAS Update went to the preview channel first (recorded as shipped), and the report cites rule 12's Release-build proof and says its first-render path was crash-free on the preview update before production.
- [ ] No rollback or rollout revert past a shipped version was done or planned; a wrong shipped step has its fix-forward version.
- [ ] Any restore ran only after the developer's yes, with `kept-<time>/` left in place.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-migration.mjs .` prints `RESULT: PASS` (in CI with `--base <target branch>`). Expected only before persistence-and-migrations built the open path: `SKIP src/data/app-database.ts [restore-drill] not yet created (persistence-and-migrations creates it)`. An app without `src/data/migrations/migrations.ts` prints `NOT APPLICABLE: ...` and has nothing to ship.

## Anti-patterns

- **"It's only a comment" in a shipped step.** The ledger hash fails, and the next edit will not be a
  comment; restore the file and change the schema in a new version.
- **Two steps in one release.** v2 and v3 both pending: fold them into one v2 (nothing shipped).
- **Re-dumping a shipped fixture because a test fails.** It is the database phones hold; fix the step.
- **A content test that compares counts or the schema.** Read the values back, row by row.
- **Fixtures of `'test1'` rows.** Freeze apostrophes, non-ASCII letters and emoji, or the next copy
  step's mangling goes unseen.
- **Testing only fresh install to latest.** The phone with list 1 already in it is the one that fails;
  every fixture to every later version.
- **Recording a version "now, before the build", or never.** Record after it left: early, a still
  changing step looks frozen; never, and the next edit of a shipped step is invisible.
- **`eas update:rollback`, `eas update:roll-back-to-embedded`, reverting an update rollout, or
  re-releasing the previous code after a migration.** Phones at version N open in memory with none of
  their data; pause the channel (`eas channel:pause`) and fix forward.
- **A schema step sent as an EAS Update straight to production.** A crash before the first screen
  makes expo-updates roll phones back on its own; prove it on a Release build and on the preview
  channel first, or ship the step in a store build.
- **A private "staging" channel or a runtime channel override for the proof.** ota-updates' variant
  model allows neither; the preview channel is the proof, and publishing there ships the version.
- **Recording from whatever is checked out today.** Without `--ref`, an edit made after the release
  is pinned as "shipped" and the real bytes never are.
- **Restoring a snapshot with the app open, or deleting `-wal` and the old file.** Stop the app, move
  them aside, keep them until the case is closed.
- **Restoring users' phones.** Nothing reaches them; a repair is a new version.
- **Proving the upgrade on a booted or shared simulator.** Create `<project>-migration`, name it in
  every command, delete it afterwards.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/release-ritual.md](references/release-ritual.md) | What shipped means, the ledger, frozen files and formatters or linters, one pending version, merging two branches, the ritual in order, the upgrade over the previous release on iOS and Android, EAS Update, error recovery and rollbacks, adopting the ledger, CI, owners, multi-package | Workflow steps 1-3 and 7-10 |
| [references/proofs-and-drills.md](references/proofs-and-drills.md) | What each proof catches, the content test, hostile rows, every from-to path, the restore drill, how the checker runs app code, the rule table, pitfalls, limits | Workflow steps 4-6, and when a rule fails |
| [references/restore-on-device.md](references/restore-on-device.md) | When to restore or fix forward, what a snapshot is, the restore in a folder, on an iOS simulator, on Android, physical phones, pitfalls | Workflow step 11 |
| `templates/contracts/schema-ledger.json` | The empty ledger (copied once; record-shipped fills it) | Workflow step 2 |
| `templates/contracts/schema-ledger.schema.json` | The ledger's JSON schema | Workflow step 2 |
| `templates/test/sqlite/migration-paths.test.ts` | Every from-to path in Jest, generated from the fixtures folder | Workflow step 2 |
| `templates/test/sqlite/migration-restore-drill.test.ts` | The forced-failure drill (halfway failure, committed wrong step undone) through `openAppDatabase` | Workflow step 2 |
| `templates/test/sqlite/database-content.ts` | Helper: a database's whole content, its rows in a stable order, row counts, lost rows | Workflow step 2 (copied with the tests) |
| `templates/test/sqlite/restore-snapshot-files.ts` | Helper: the snapshot restore on node:fs, the same steps restore-snapshot.mjs takes on a device | Workflow step 2 (copied with the tests) |
| `examples/v0002-pending/` | A pending v2 (list sort order): step, list, frozen hostile `db-v2.sql`, checksums, content test, fixtures test, ledger with v1 shipped | Workflow step 4 |
| `scripts/check-migration.mjs` | The ritual checker (ledger, frozen shipped files, one pending version, fixture, hostile rows, content test, path tests, every-path and restore drill on node:sqlite); options `--base`, `--base-ledger`, `--no-replay`, folder options | Workflow steps 3, 6, 8 and 12 |
| `scripts/record-shipped.mjs` | Appends the pending version to the ledger after the same rules pass; `--ref` hashes the release's commit and fails when the working tree differs; dry run unless `--yes`; `--adopt` for versions shipped before the ledger | Workflow steps 2 and 10 |
| `scripts/restore-snapshot.mjs` | Restores `<db>.v<N>.bak` in a folder, on a named simulator or on Android (run-as: a debuggable build); checks first on copies, keeps the replaced files, dry run unless `--yes` (and the dry run leaves the folder exactly as it was) | Workflow step 11 |
| `scripts/lib/` | Helpers: the ledger and static rules, the shared ritual, the node:sqlite replay and drill, device file access, and the synced `app-modules.mjs` (do not edit that one here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves the three scripts pass the good repo and catch every planted bug | After changing a script, a template or the example |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/` | The base app (persistence-and-migrations' open path, runner and v1) and overlay fixtures for the three scripts (`record-shipped-ref/` cases become a git repo at run time, as each `git-setup.json` says) | When adding a rule |

## Related skills

- `persistence-and-migrations` - the runner, open path, snapshots, step files, fixtures, inspect-database and kill test this ritual builds on.
- `error-handling-typed-results` - outcomes such as newer-version and migration-failed are typed results, never resets.
- `git-commits-and-reporting` - the Gate-Change trailer and the release report naming the new version.
- `ci-pipeline-and-gates` - the CI job running check-migration with `--base`.
- `eas-build-and-submit`, `ios-release-testflight`, `android-release-play` - the release builds that make a version shipped.
- `ota-updates` - updates that can carry a step, and why they are not rolled back past it.
- `ios-simulator-build`, `android-emulator-build` - the Release builds for the upgrade proof.
- `data-export-and-restore` - user-facing backups (the envelope, never the file) and the support copy of the database file.
- `golden-and-snapshot-tests` - the review policy for frozen files.
