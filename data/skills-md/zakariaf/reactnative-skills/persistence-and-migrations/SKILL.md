---
name: persistence-and-migrations
description: "Builds the expo-sqlite database: tables, repositories, migrations. Use when adding a table, column or saved data, leaving AsyncStorage, or data is lost after an update. Not for stores (state-management-zustand)."
---

# Persistence and migrations

App data lives in one SQLite file opened synchronously through a tiny `SqlDriver` port, reached only
through validated repositories that return typed Results, upgraded only by frozen forward-only steps
that are replayed against frozen fixture databases on Node, and never lost or crash-looped on;
scripts prove the code, the schema history and the file on a named iOS simulator and Android emulator.

## Rules that must hold

1. **One data layer.** SQLite and the `SqlDriver` port are imported only in `src/data/` (the drivers)
   and SQL, in any case, lives only there; statements run only in `sqlite-<area>-repository.ts` files
   and the open path, migrations, peeks and resets. Exceptions: the SQLite error log adapter in
   `src/services/error-log/` and the files the contract's `sqlAllowed` lists. Features and stores call a
   repository (`useAppData()` carries the database's status, never the driver). No second engine for
   app data (AsyncStorage, zustand `persist`, another SQLite binding); small preferences go to the one
   key-value store the contract names (`expo-sqlite/kv-store`, or the global `localStorage` its
   `expo-sqlite/localStorage/install` puts over the same store, installed by the first import of the
   `local-storage-<concern>-adapter.ts` that reads it), behind a port; secrets to
   `expo-secure-store`. Why: one file, one version number, one backup story.
2. **Open synchronously, version first, then `journal_mode = WAL`, `synchronous = FULL` and
   `foreign_keys = ON` on every open; every table is STRICT.** Why: a committed transaction survives a
   kill or power cut, SQLite ships with foreign keys off, and the journal-mode pragma writes the file.
3. **Never crash-loop and never touch a file the build cannot use.** A newer, damaged or unmigratable
   file, or one at `user_version` 0 whose schema is neither the baseline nor a declared variant, is left
   as it is; the session runs in memory with an outcome the first screen explains (a full disk is
   `storage-full`: "free up space"), and opening never throws. Why: a throw at startup repeats on every launch, and an existing database opened "fresh"
   hides every row the user had.
4. **Forward-only, frozen steps.** One `vNNNN-<name>.ts` per version with literal SQL, registered in
   order, each step and its `user_version` stamp in one transaction; no down steps, no stamping or
   BEGIN in a step, `rebuildsTables: true` on every step that drops or renames a table. Never edit a
   shipped step. Why: installed apps never rerun a step, so an edit splits fresh and upgraded installs
   forever; and with foreign keys on, dropping a parent table deletes its cascading children.
5. **Snapshot before migrating** a file that holds tables: `VACUUM INTO '<file>.v<from>.bak'`, reused
   while a step keeps failing, pruned to the newest two after a success; no snapshot, no migration.
   Why: the only way back from a step that committed but was wrong, without a new full copy per launch.
6. **Every shipped version has a frozen fixture database with a recorded checksum, and a fresh install
   and every upgraded fixture end with the same schema and every row the fixture held** (replayed on
   node:sqlite with foreign keys on, by the tests and by the checker; an adopted app also replays one
   `db-v0-<variant>` per legacy schema). Never edit a fixture or checksum. Why: old phones hold these files.
7. **Validate and convert at the boundary.** Repository methods return `Result<T, F>` with a `kind`
   union and never throw for a data reason: input is parsed with valibot first (invalid input is a
   typed failure, nothing written), values are bound parameters (never built into the SQL text), SQLite
   errors are converted once (the unexpected ones recorded raw), every row read goes through its row
   schema and an unreadable row is skipped and logged alone; statements stay in methods or the same-file
   helpers they call (`run` per statement, never `exec`). Why: a thrown expected failure crashes a
   release-build handler; error-handling-typed-results owns Results.
8. **A write of two or more statements, or one per item of a loop, is one transaction; transactions
   never nest** (both drivers throw on a nested one). Why: a kill must not leave half a change, and the
   two runtimes used to fail a nested BEGIN differently.
9. **Resets list each statement literally and never touch protected tables** (entitlements: a purchase
   ends only with a dated revocation; error_log: what support needs), in one transaction.
10. **Write nothing before startup decisions that can reload the runtime:** open on the root layout's
    first render, never at import time; a peek is read-only. Why: module code runs again after a reload,
    so an early write happens twice.
11. **Checkpoint the WAL (`wal_checkpoint(TRUNCATE)`) when the app goes to the background.** Why: a
    device backup (iCloud, Android Auto Backup) then copies one self-contained file.
12. **Test the real SQL on `node:sqlite` through `SqlDriver`, with foreign keys off until the app's
    pragma (as on the device), and finish write-path or startup changes with the kill test on iOS and
    Android** (or say in the report that it is owed). Why: Jest proves the SQL; only a kill proves the app.
13. **Appendix: a save document only for small app state** (`"mode": "document"` or `"both"`): strict
    schema validated on every load and before every write, `current`/`backup` slots written in one
    transaction, a refused write logged and never thrown (the backup stays due), damaged rows
    quarantined never deleted, protected sections guarded for every writer, pure frozen document steps.
    Why: state that is always read and written whole fits one validated value, and two slots keep a
    good copy when one write is damaged; anything that grows belongs in tables.

## Workflow

1. Read [references/tables-and-repositories.md](references/tables-and-repositories.md) (driver, open
   path, outcomes, snapshots, repositories and Results, validation, resets, key-value boundary, error
   log, file locations and backups, adopting an existing database).
2. New data layer: `npx expo install expo-sqlite expo-file-system`, `npm install -E valibot@1.5.0`
   and, if the app lacks it, `npm install -D -E fast-check@4.10.2` (stack table, verified 2026-10-03);
   copy `templates/src/data/` (without `document/` unless you chose the appendix, and without
   `peek-database.ts` until a reload decision calls it: copy it with that decision), `templates/test/sqlite/`
   (without `sqlite-document-store.test.ts`), `templates/src/services/`, `templates/src/core/` and
   `templates/contracts/` (skip a synced file the app already has from its owner skill). Replace the
   Tasks tables, schemas, failures and repository with the app's own (and their lines in `AppData` and
   `openDeviceData`); keep the drivers, runner, open path and snapshots. Fill `contracts/persistence.json`
   (mode, protected tables, reset modules). In the root layout: `useState(openOnce)` calling
   `openDeviceData`, `useCheckpointOnBackground(data.database)` and `<AppDataProvider>`, exactly as
   `examples/root-layout.tsx`; app-startup-and-bootstrap owns the full startup order.
3. The app already ships a database (unversioned tables, its own `user_version` numbering, Drizzle,
   SQLiteProvider, or AsyncStorage data): follow "Adopting in an existing app" in the same reference
   before the first release with this layer (`BASELINE` in `migrations.ts`, one frozen `db-v0-<variant>.sql`
   per legacy schema). Never let it open as `fresh`.
4. A feature needs to save something: add a repository method (`v.safeParse` input, a typed failure,
   `attempt` around the driver call, row schema on read, one transaction for several statements) and
   call it from the model hook or store (`useAppData().tasks`; `useAppData().database` is only the
   status: outcome, `isPersistent`, `checkpoint`); never SQL or the driver in a feature, and never a
   statement in another data file (a sibling `task-rows.ts` escapes every repository rule). A new column
   or table is a new version.
5. The schema changes: read [references/migrations-and-fixtures.md](references/migrations-and-fixtures.md)
   and follow "Adding version N+1" in order, imitating `examples/migration-v2/` (step, test on the old
   fixture, new frozen fixture made with `inspect-database.mjs --dump`, checksum, FIXTURES entry). For a
   release, also run the run-migration ritual. A new version is permanent once shipped: name it in the report.
6. Small app state as one document: read [references/save-document.md](references/save-document.md),
   set `"mode": "both"` (or `"document"`), copy `templates/src/data/document/` and its SQL test, paste
   `DOCUMENT_SLOTS_DDL` into a new table step, and imitate `examples/document-v2/` for document versions.
7. Startup, checkpoint or kill-test work: read [references/startup-and-kill-test.md](references/startup-and-kill-test.md).
8. Run the tests: `npx jest src/data src/core src/services test/sqlite --ci` and `npm run typecheck`.
9. After a change to the open path, a migration, a repository's writes or the startup, with a Release
   build on a dedicated device: `node ${CLAUDE_SKILL_DIR}/scripts/kill-test.mjs --udid <udid> --bundle-id <id> --expect-version <N>`
   (iOS) and `node ${CLAUDE_SKILL_DIR}/scripts/kill-test.mjs --serial <serial> --package <id> --expect-version <N>`
   (Android) must print `RESULT: PASS`. Without builds, say in the report that the kill test is owed.
10. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-persistence.mjs .` from the repo root; fix every `FAIL`
    line and rerun until it prints `RESULT: PASS`.

## Definition of done

- [ ] SQLite and `SqlDriver` imports and SQL text appear only in `src/data/`, `test/`, `scripts/`, the SQLite error log adapter and `sqlAllowed`; statements run only in repository files and the open path's own files; no feature reaches `.driver`; no AsyncStorage (outside a listed `legacyImports` importer), zustand `persist` or second engine; kv-store, the `localStorage` install and `localStorage` reads only in a `src/services/<concern>/*-adapter.ts`.
- [ ] `app-database.ts` reads `user_version` and the file's tables before `APP_DB_PRAGMAS`, never opens a version-0 file with tables as fresh (adopting only the `BASELINE` schema or a declared variant), snapshots to `<file>.v<from>.bak` before migrating, prunes old snapshots, and never throws; every table is STRICT.
- [ ] Every version 1..N has its `vNNNN` step registered in order, its `db-vN.sql` fixture, its checksum and its `FIXTURES` entry (adopting: each legacy schema its `db-v0-<variant>.sql` in `LEGACY_FIXTURES`); a step that drops or renames a table says `rebuildsTables: true`; no shipped step, fixture or checksum was edited.
- [ ] Every repository method returns a `Result`, `v.safeParse`s its input before writing (itself or through a helper), binds every value as a parameter, converts driver errors once, wraps several statements (or a loop, its helpers included) in one transaction, and passes what every read returns (not only its input) through `safeParse`; each SQLite repository has a node:sqlite test.
- [ ] Resets list their statements literally and keep the contract's protected tables; the root layout opens the data layer on its first render (`useState(openOnce)`, never at import time or as a call in the render body) and calls `useCheckpointOnBackground` once.
- [ ] `npx jest src/data src/core src/services test/sqlite --ci` passes and `npm run typecheck` is clean; device-only files carry their `// device-only: covered by ...` line.
- [ ] Appendix only: document schemas strict, `LATEST_*` names the highest version, every version has its step, test and both frozen JSON fixtures, and `update()` validates, guards Premium, respects `isReadOnly` and never throws for a refused write.
- [ ] After a write-path, migration or startup change: the kill test printed `RESULT: PASS` on iOS and on Android, or the report says it is owed.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-persistence.mjs .` prints `RESULT: PASS`. Expected only before the root layout exists: `SKIP src/app/_layout.tsx [no-background-checkpoint] not yet created (app-startup-and-bootstrap creates it)`. An app that keeps only preferences (no contract, no `src/data/`) prints `NOT APPLICABLE: no app database: no contracts/persistence.json, no src/data/, and expo-sqlite is not imported, or only as expo-sqlite/kv-store or expo-sqlite/localStorage/install (preferences); the repo-wide rules passed`.

## Anti-patterns

- **"Just add a column" to `v0001-...` after it shipped.** Fresh installs get it, upgraded ones never
  do; the replay fails. Add `v0002` instead.
- **Editing a fixture or checksum to make a test pass.** The fixture is what old phones hold; fix the
  step, or add a new version.
- **A step that imports a table-name constant, a schema or today's defaults, or reads the clock.**
  Tomorrow's change would rewrite yesterday's upgrade; write literal SQL.
- **`PRAGMA foreign_keys = OFF` inside a step, or a rebuild without `rebuildsTables: true`.** The
  pragma is a no-op inside a transaction, and a parent rebuild with foreign keys on deletes every
  cascading child while the schema still matches; mark the step `rebuildsTables: true`.
- **`throw` when the file is newer, or deleting a file that does not open.** Every launch then crashes,
  or the user's data is gone; run in memory, tell the user, keep the file.
- **Shipping this layer over an existing database without a baseline, or with one baseline when old
  builds left several schemas.** Migration 1 collides, the app opens "fresh", or one population opens in
  memory forever; adopt every variant (`BASELINE.variants`, a rebuild after it) or backfill steps.
- **Pragmas before the version check.** Setting WAL writes a newer build's file before it is recognised.
- **A snapshot named by the time, never pruned.** Every failing launch adds a full copy, and the copies
  fill device backups (Android's limit is 25 MB per app); name it per version, reuse it, prune it.
- **A repository that throws on invalid input or lets an SQLite error escape.** A release-build
  handler crashes; return the typed failure, record the unexpected one with the raw error.
- **A transaction inside a transaction, or a bulk method of autocommits.** The inner BEGIN fails (on a
  device it used to roll back the outer change); one outer transaction per change.
- **Opening the database at import time, or awaiting an async open before the first render.** Open
  once, synchronously, in the root layout after the reload decisions.
- **AsyncStorage or zustand `persist` "for one small value".** No transaction, no version, no backup;
  add a column, a repository method, or a kv-store preference behind a port.
- **Handing the driver to features** (`AppData.database.driver`, a "maintenance" hook that runs one
  DELETE). Every repository rule is skipped; add a repository method instead.
- **Trusting rows from SQL.** A row from an older build or a bypassed constraint crashes a screen;
  parse it, skip and log what does not parse.
- **A value built into SQL (`` `... WHERE id = ${id}` ``).** A quote breaks it and input can run its own
  SQL; bind it (`?`).
- **Tests on a mock driver only, or a test driver with foreign keys on.** The device enforces nothing
  until the app's pragma; test the real SQL on node:sqlite with the device's defaults.
- **Opening the app's live `app.db` in place from the computer.** It can checkpoint or lock the file;
  `inspect-database` copies it first.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/tables-and-repositories.md](references/tables-and-repositories.md) | Driver port and its contract, the open path and outcomes, snapshots and backups, repositories and Results, validation, transactions, resets, key-value and secrets, error log, file locations, adopting an existing database, multi-package, alternatives, rules | Workflow steps 1-4 |
| [references/migrations-and-fixtures.md](references/migrations-and-fixtures.md) | Forward-only rules, the runner, step files, adding version N+1, table rebuilds, frozen fixtures, dumps, the replay, failures | Workflow step 5 |
| [references/startup-and-kill-test.md](references/startup-and-kill-test.md) | Startup order, the peek, opening in the root layout, the checkpoint, node:sqlite tests, the kill test on iOS and Android, inspect-database, what is verified | Workflow steps 7 and 9 |
| [references/save-document.md](references/save-document.md) | Appendix: the save document, slots, codec, load plan, the single writer and its write results, protected sections, document versions and fixtures, its tests | Workflow step 6 |
| `templates/src/data/sql-driver.ts`, `expo-sqlite-sql-driver.ts`, `migrations/migration-runner.ts` | The port, the device driver and the runner, synced from the library (do not edit here) | Workflow step 2 |
| `templates/src/data/` (other files) | Open path (with adoption), schema reader, snapshots and the `DatabaseFiles` port with its device adapter (`expo-file-system-database-files-adapter.ts`), SQLite error mapper, migration list (with `BASELINE`) and v1 step, frozen `db-v1.sql` and checksums, checksum, Tasks schemas, failures and repository (SQLite and fake), reset, peek, checkpoint hook, the `AppData` context, the device composition (`openDeviceDatabase`, `openDeviceData`), and tests | Workflow steps 2-5 |
| `templates/src/data/document/` | Appendix: schemas, slot store (SQLite and fake), tables SQL, codec, load plan, service, resets, migrations, peek, hydrate, frozen JSON fixtures, and tests | Workflow step 6 |
| `templates/src/core/` | `result.ts` and its test (error-handling-typed-results' Result module) and `dates/date-key.ts` with its test (the clock port's date type), synced (do not edit here) | Workflow step 2 |
| `templates/src/services/` | The clock port and system clock adapter, the error log port, memory adapter and fake, with tests (architecture-and-boundaries' files, synced; do not edit here), and this skill's SQLite error log adapter | Workflow step 2 |
| `templates/test/sqlite/` | node:sqlite driver, temp folder, runner test and driver contract test (synced), file listing, schema helper, and the SQL tests (the fixtures test replays every fixture with foreign keys on and counts every table's rows) | Workflow steps 2 and 8 |
| `templates/contracts/` | `persistence.json` (the app's facts) and its JSON schema | Workflow step 2 |
| `examples/migration-v2/` | A complete v1 to v2 table change: step, list, frozen `db-v2.sql`, checksums, fixtures test, the step's test | Workflow step 5 |
| `examples/document-v2/` | A complete document v1 to v2 change: sections, schema, defaults and their pinned test, step and its fast-check test, list, fixtures, checksums | Workflow step 6 |
| `examples/root-layout.tsx` | The startup wiring in an Expo Router root layout, using only this skill's templates (the self-test runs the checker on it) | Workflow step 2 |
| `scripts/check-persistence.mjs` | Static checker plus the migration replay on node:sqlite; reads `contracts/persistence.json`; options `--data-dir`, `--contract`, `--no-replay` | Workflow step 10, and at the end |
| `scripts/inspect-database.mjs` | Health check of a database, a .sql dump, or the app's file on a named simulator or emulator (physical damage reported as `integrity`); `--dump` freezes a fixture | Workflow steps 3, 5 and 9, and when data looks wrong |
| `scripts/kill-test.mjs` | Kill test on a named iOS simulator (`--udid`, `--create`) or Android emulator (`--serial`; launches with `am start -W`, `--activity`, `--step-ms` per platform), then one clean launch left running `--settle-ms` before the inspection | Workflow step 9 |
| `scripts/lib/` | The checkers' helpers (database health and dumps, device copies, the migration replay, the source model, the rule sets) and the synced `app-modules.mjs` and `source-scan.mjs` (do not edit those two here) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Pins the checksum vectors and proves both checkers pass good input and catch every planted bug | After changing a checker or a template |
| `assets/shared.json` | Declares the shared files this skill copies in | When adding a shared file |
| `tests/` | Overlay fixtures (planted bugs) for check-persistence in tables and both modes (rebuilds, helpers, adoption variants included) and for inspect-database, with their bases | When adding a checker rule |

## Related skills

- `error-handling-typed-results` - the Result type, failure design, catches and the error net.
- `state-management-zustand` - stores that call repositories and publish after the commit.
- `run-migration` - the release ritual for a schema migration (snapshot, every path, restore drill).
- `data-export-and-restore` - portable backups and imports of the same data.
- `app-startup-and-bootstrap` - the full startup order around opening the database.
- `architecture-and-boundaries` - ports, the composition root, the clock and error log services.
- `networking-and-server-state` - server state, the persisted query cache and the offline outbox's sync.
- `auth-and-secure-storage` - tokens and secrets in expo-secure-store.
- `settings-and-preferences` - what is a preference and where it is saved.
- `in-app-purchases` - the entitlement and its dated revocation.
- `rtl-and-direction` - the direction decision that runs before the database opens.
- `ios-simulator-build`, `android-emulator-build` - the Release builds the kill test installs.
- `e2e-maestro` - mid-session kill flows on a named device.
- `golden-and-snapshot-tests` - the review policy for frozen files.
