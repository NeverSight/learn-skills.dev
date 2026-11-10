---
name: data-export-and-restore
description: Builds data export and restore - a versioned, checksummed backup file, all-or-nothing restore, safe CSV. Use when adding backup, restore, import, export or CSV files. Not for the database (persistence-and-migrations).
---

# Data export and restore

A backup is a versioned, checksummed file of the user's tables that this app (and only a backup) can
restore; a restore checks the whole file first, keeps a safety copy, then replaces every table in one
transaction or changes nothing; a CSV export is guarded against broken rows and formula injection; files
leave or enter the app only through ports, from a press; tests prove the round trip byte for byte.

## Rules that must hold

1. **Backup and export are different features; restore accepts only the backup envelope.** A CSV or a
   report is lossy and never restorable (it fails as `not-a-backup`). Why: the moment a CSV restores, a
   format built for reading becomes someone's only copy, with no versions, types or checksum.
2. **Every backup is the envelope: `format`, `formatVersion`, `schemaVersion`, `appVersion`,
   `exportedAt` (UTC), `payloadSha256`, in that order, then the canonical payload last;
   `BACKUP_SCHEMA_VERSION = LATEST_DB_VERSION`.** Why: an unversioned file can only be misread, never
   refused, and header first lets a truncated file of ours be called damaged. (`envelope-header`,
   `schema-version`)
3. **A picked file climbs the whole ladder before anything is written**: size (the one
   `MAX_BACKUP_BYTES`, which export also refuses to exceed), readable, ours, strict
   header, checksum before any row, not newer than the build, every row through its schema (text bounds
   in code points, as SQLite counts), ids unique and parents present. The name and MIME type are never
   trusted. Why: a broken file must fail with its own reason, not half-way through the rows.
   (`checksum-first`, `newer-refused`)
4. **Restore is replace, all or nothing**: the user confirms a preview that names the policy and the
   counts (and the unreadable current rows the replace also removes); the current data is written to a
   private safety copy first (no copy, or one over the size limit, no restore); then one
   transaction deletes and inserts every backed-up table, ids kept; a preview restores once; never into
   a session running in memory. The app offers the copy back (`previewSafetyCopy`), because no picker
   can reach the private folder. Why: a half-restored database is worse than a failed restore, and the
   copy is the undo for restoring the wrong file. (`restore-transaction`, `safety-copy-first`)
5. **A backup covers every user table and never a protected one**: each table the migrations create is
   in `BACKUP_PAYLOAD` or in `BACKUP_EXCLUDED_TABLES` with its reason; entitlements, diagnostics and
   secrets are never backed up or restored. Why: a forgotten table is data lost on the next restore, and
   a restorable entitlement is a free purchase for anyone who edits the file. (`backup-coverage`,
   `restore-protected`)
6. **Older backups upgrade through frozen, pure JSON steps, one per migration, proven equal to the
   migrations by the parity test; every schema version has a frozen backup fixture.** Why: users hold
   files from every version, and two upgrade paths drift apart unless a test pins them together.
   (`upgrade-chain`, `backup-fixture`)
7. **The round-trip test passes on hostile data**: export, restore into an empty database, export again
   gives the same bytes; restoring twice gives the same rows; every refusal leaves the data unchanged.
   Why: `'test1'` survives everything and proves nothing. (`round-trip-test`)
8. **Machine formats hold canonical values only**: integers, `.` decimals, ISO-8601 UTC or epoch ms,
   date keys, codes, untranslated column names; localization happens on screen. Why: `12,5`, `١٢٫٥` and
   `12.5` are one number and three parses. (`canonical-values`)
9. **Every CSV goes through the one guarded encoder**: a text cell starting with `= + - @`, tab or CR
   gets an apostrophe, then RFC 4180 quoting (quotes doubled, spaces and newlines kept), CRLF, UTF-8 with
   a BOM for spreadsheets. Why: a hand-joined cell breaks on a comma and runs as a formula in the
   recipient's spreadsheet. (`csv-guard`, `csv-hand-rolled`)
10. **Files are published atomically**: a temp file in the same folder, moved over the published name,
    deleted on failure; free space checked first; shared exports live in the cache and are swept on the
    next export, never deleted when the share sheet closes. Why: a truncated file with a trusted name is
    the failure that surfaces months later. (`atomic-write`)
11. **The share sheet, the picker and the file system sit behind ports, and run only from a user's
    press**; these ports never upload. Why: Jest never touches native code, and a file leaves through
    them only when the user asks. An opt-in scheduled cloud backup is a separate feature with the same
    envelope and ladder. (`sdk-behind-port`, `user-action-only`)
12. **Export, pick and restore return typed Results with one failure kind per reason; backup code never
    throws.** Why: "Restore failed" alone cannot be told apart from data loss. (`typed-failures`)

## Workflow

1. Read [references/envelope-and-ladder.md](references/envelope-and-ladder.md) (the file, the checksum,
   the ladder, upgrades, fixtures) and [references/restore-policy.md](references/restore-policy.md)
   (replace, the transaction, the safety copy, the confirmation, excluded tables).
2. Prerequisites: the app database from persistence-and-migrations (`SqlDriver`, migrations,
   `contracts/persistence.json`, `AppData`) and the Result module from error-handling-typed-results. Then
   `npx expo install expo-file-system expo-sharing expo-document-picker` (SDK 57: `~57.0.7`,
   `~57.0.22`, `~57.0.3`; verified 2026-10-10; re-verify with `npx expo install --check`).
3. Stop and ask the developer to classify the two new SDKs (an architecture decision): merge
   `examples/contracts/architecture.json` into the app's `contracts/architecture.json` and add both to
   `VENDOR_SDK_PATHS` in `eslint.config.mjs` in the same commit
   ([references/platform-behaviour.md](references/platform-behaviour.md), section 7).
4. Copy the templates: `templates/src/core/portable/`, `templates/src/data/backup/` (with
   `fixtures/backup-v1.json`), `templates/src/services/{export-files,share-sheet,file-picker}/`,
   `templates/test/portable/`, `templates/test/sqlite/{sqlite-backup-repository,backup-round-trip}.test.ts`
   (skip the synced files the app already has from their owners). Replace `__APP_SLUG__` (the format
   marker and file names). Replace the Tasks tables with the app's own in `backup-schema.ts`, the SQLite
   backup repository (literal SELECT/DELETE/INSERT per table, children of a skipped parent left out in
   `readAll`), `consistencyFailure`, `tasks-csv.ts`, the frozen fixture and the tests; list every other
   table in `BACKUP_EXCLUDED_TABLES` with its reason. Set `FIRST_BACKUP_SCHEMA_VERSION` in
   `backup-envelope.ts` to the app's current `LATEST_DB_VERSION` (the template's `1` fits only an app
   whose database is still at version 1); it never changes after the first release with backups. No
   upgrade steps or fixtures exist for versions before it: never invent them to satisfy the checker.
5. Make the frozen fixture for the current schema (N = `FIRST_BACKUP_SCHEMA_VERSION`): export with the
   app over hostile rows (quotes, `=1+2`, CRLF, RTL with marks, emoji at the maximum length, blanks, a
   gap in ids) and commit it as `src/data/backup/fixtures/backup-v<N>.json` with its FIXTURES entry,
   replacing the template's `backup-v1.json` when N > 1. Never edit it afterwards.
6. Compose once: the three adapters in `createDeviceServices` (fakes in `createTestServices`), and
   `backup: createBackupService({ ..., isPersistent: database.isPersistent })` in the data layer's device
   opener as a member of `AppData` (platform-behaviour.md, section 7).
7. Build the screen from `examples/src/features/backup/` (model, pure view, one message per failure
   kind): one action at a time with the busy state painted first, an iPad anchor per share button, the
   confirmation naming "replace", both counts and the date formatted on screen, the "Restore the data
   from before your last restore" row, `skippedRows` and `currentSkippedRows` shown, a failed phase
   when a job throws (never stuck on working), and the restore run through the store
   layer's `updateAndPublish` so every store re-reads. CSV and reports:
   [references/csv-and-formats.md](references/csv-and-formats.md).
8. A table changes later: follow "Adding schema version N+1" in envelope-and-ladder.md, imitating
   `examples/backup-v2/`, in the same change as the migration.
9. Run the tests ([references/testing-and-checker.md](references/testing-and-checker.md)):
   `npx jest src/core/portable src/data/backup src/services/export-files src/services/share-sheet src/services/file-picker test/sqlite --ci`
   and `npm run typecheck`.
10. After an adapter change, run the export-share-restore drill on a named iOS simulator and Android
    emulator (platform-behaviour.md, section 8), or say in the report that it is owed.
11. Run `node ${CLAUDE_SKILL_DIR}/scripts/check-backup.mjs .`; fix every `FAIL` line and rerun until it
    prints `RESULT: PASS`. For a user's file: `node ${CLAUDE_SKILL_DIR}/scripts/inspect-backup.mjs <file> --format <slug>.backup --schema <N>`.

## Definition of done

- [ ] Backup and CSV are separate actions; the envelope's header comes first in the order of rule 2, the
      payload is canonical JSON and `payloadSha256` its SHA-256; `BACKUP_SCHEMA_VERSION = LATEST_DB_VERSION`.
- [ ] `readBackup` runs the whole ladder with one failure kind per reason, the checksum before any row,
      newer files refused; the picked file's size is checked before it is read, and export refuses a
      backup above the same `MAX_BACKUP_BYTES` or one that fails rung 7.
- [ ] Restore shows a preview naming "replace" and the counts, writes the safety copy first, replaces in
      one transaction (ids kept), restores a preview once, refuses a session in memory; stores re-read
      afterwards; the screen offers the safety copy back through `previewSafetyCopy`.
- [ ] Every migrated table is backed up or excluded with its reason; no protected table, secret or
      preference is in a backup.
- [ ] `FIRST_BACKUP_SCHEMA_VERSION` is the database version of the first release with backups; every
      schema version since has its upgrade step and its frozen `backup-vN.json` in FIXTURES; the parity
      test runs for every older fixture.
- [ ] Every CSV goes through `toCsv`; machine formats hold canonical values only.
- [ ] The three SDKs are imported only by their adapters, classified in `contracts/architecture.json`
      and ESLint; export, share, pick and restore run only from presses.
- [ ] The tests of workflow step 9 pass; after an adapter change the drill passed on iOS and Android, or
      the report says it is owed.
- [ ] `node ${CLAUDE_SKILL_DIR}/scripts/check-backup.mjs .` prints `RESULT: PASS`. Expected only before
      the database layer exists: `SKIP src/data/migrations [upgrade-chain] not yet created
      (persistence-and-migrations creates it)` and the same for `[backup-fixture]`. An app with no backup
      folder and no share, pick or CSV code prints `NOT APPLICABLE: no src/data/backup/, and no source
      file imports expo-sharing or expo-document-picker or writes text/csv`.

## Anti-patterns

- **CSV as the backup.** No versions, no types, no checksum, and formulas run on open; offer the
  envelope for backup and keep CSV an export.
- **Restoring straight into the tables row by row, or in several transactions.** A failure half-way
  leaves a database nobody can describe; validate everything, then one transaction.
- **Swapping database files while the app holds the connection.** Repositories keep the old handle and
  `-wal` sidecars corrupt the new file; replace inside one transaction.
- **A "Restore" button that runs at once.** The user expected "add back" and loses a week; preview,
  name the policy and the counts, keep a safety copy.
- **Restoring entitlements from a backup.** Anyone who edits the file owns Premium; purchases come back
  through the store.
- **`v.maxLength` on backed-up text.** It counts UTF-16 units; a 200-emoji title the table holds can
  never be restored. Count code points.
- **An upgrade step that imports today's constants or schemas.** Tomorrow's change rewrites yesterday's
  upgrade; literal names only, and the parity test.
- **Writing straight to the published file name, or deleting the export when `shareAsync` resolves.**
  A crash publishes a truncated "backup"; a receiving Android app may read the file after the sheet
  closed. Temp file plus move; sweep on the next export.
- **Trusting the picked file's name or MIME type, or filtering the picker by `application/json`.**
  Providers label files differently; open with `*/*` and let the envelope decide.
- **`useEffect(() => exportBackup())`, or uploading through these ports.** A file leaves without the
  user asking. Export from a press; an opt-in cloud backup is its own feature
  (networking-and-server-state, privacy-and-store-declarations).
- **Pointing the user at a picker to undo a restore.** No picker reaches the private folder (Android's
  document picker never, the iOS Files picker only with file sharing on); offer `previewSafetyCopy`.
- **"Backup saved" after the share sheet closes.** `shareAsync` does not report where the file went; say
  "Shared" or nothing.
- **A generic "Import failed".** The user cannot tell a wrong file from lost data; map each failure kind
  to its message.

## Files in this skill

| File | What it is | Read/run when |
|---|---|---|
| [references/envelope-and-ladder.md](references/envelope-and-ladder.md) | Backup vs export, the file and its fields, canonical JSON and SHA-256 (with measured speed), the two versions, the ladder, code-point bounds, upgrades and parity, adding version N+1, frozen hostile fixtures, decisions | Workflow steps 1, 5 and 8 |
| [references/restore-policy.md](references/restore-policy.md) | Replace, one transaction vs a file swap, the safety copy, the confirmation, excluded tables, after the restore, in-memory sessions, merge and copies (fenced) | Workflow steps 1 and 7 |
| [references/platform-behaviour.md](references/platform-behaviour.md) | The three ports, SDK 57 APIs, iOS and Android behaviour, folders and device backups, classification and composition, the drill on named devices | Workflow steps 3, 6 and 10 |
| [references/csv-and-formats.md](references/csv-and-formats.md) | Choosing a format, the two CSV escapes, BOM and CRLF, canonical values, one encoder, reports, pitfalls | Workflow step 7 |
| [references/testing-and-checker.md](references/testing-and-checker.md) | The shipped tests, hostile data and refusals, every check-backup rule with its fix, configuration, inspect-backup, limits | Workflow steps 9 and 11 |
| `templates/src/core/` | `portable/`: `sha256.ts`, `utf8.ts`, `canonical-json.ts`, `csv.ts` and their tests (pure); `result.ts` (+test) synced from error-handling-typed-results (do not edit here) | Workflow step 4 |
| `templates/src/data/backup/` | Schema and excluded tables, failures, envelope, upgrade step and list, reader (ladder), repository type, SQLite and fake repositories, CSV export, service, frozen `fixtures/backup-v1.json`, and tests | Workflow steps 4-5 |
| `templates/src/data/sql-driver.ts` | The SqlDriver port, synced from persistence-and-migrations (do not edit here) | Workflow step 4 |
| `templates/src/data/migrations/migration-runner.ts` | The migration runner, synced from persistence-and-migrations (do not edit here) | Workflow step 4 |
| `templates/src/services/` | `export-files/`, `share-sheet/`, `file-picker/`: the three ports, their device adapters, their fakes with tests | Workflow steps 4 and 6 |
| `templates/test/` | `portable/parse-csv.ts` (a strict RFC 4180 reader), `sqlite/sqlite-backup-repository.test.ts` and `sqlite/backup-round-trip.test.ts` (real SQL: excluded tables, idempotence, rollback, round trip, fixtures, parity), and the synced `sqlite/node-sqlite-sql-driver.ts` and `sqlite/temp-database-folder.ts` (do not edit here) | Workflow steps 4 and 9 |
| `examples/src/features/backup/` | Model hook (press-only actions one at a time, busy state, phases, the safety-copy row, `updateAndPublish`), pure screen with an iPad anchor per share button and the confirmation, one message per export and restore failure kind | Workflow step 7 |
| `examples/contracts/architecture.json` | The two vendor SDK entries to merge | Workflow step 3 |
| `examples/backup-v2/` | A complete schema 2 change: migration, upgrade step and list, schema, repository, frozen `backup-v2.json`, FIXTURES | Workflow step 8 |
| `scripts/check-backup.mjs` | The checker (18 rules; options `--backup-dir`, `--json`; config key `backupDir`) | Workflow step 11, and at the end |
| `scripts/inspect-backup.mjs` | Checks one backup file on the computer and prints its header and rows | Support, fixtures, the drill |
| `scripts/lib/` | The checker's rules and the Node envelope check (`backup-rules.mjs`, `repo-rules.mjs`, `backup-envelope.mjs`), and the synced `source-scan.mjs` (do not edit) | Never by hand |
| `scripts/check-lib.mjs` | Shared script helper, synced from the library (do not edit here) | Never by hand |
| `scripts/selftest.mjs` | Proves both scripts pass the templates and examples and catch every planted bug | After changing a script, a template or an example |
| `assets/shared.json` | The shared files this skill copies in | When adding a shared file |
| `assets/template-placeholders.json` | The `__APP_SLUG__` value used to verify the templates | When adding a placeholder |
| `tests/` | The base app and the overlay fixtures of both scripts (one planted bug per rule) | When adding a rule |

## Related skills

- `persistence-and-migrations` - the database, repositories, migrations and the frozen database fixtures.
- `error-handling-typed-results` - the Result type and failure design.
- `architecture-and-boundaries` - ports, adapters, SDK classification, the composition root.
- `state-management-zustand` - re-reading stores after a restore.
- `i18n-strings-and-catalogs` - the failure messages and on-screen formatting.
- `rtl-and-direction` - showing bidi text; files keep it byte for byte.
- `value-objects-money-and-units` - canonical money and units in files.
- `dates-streaks-and-statistics` - date keys and instants.
- `in-app-purchases` - restoring purchases through the store.
- `auth-and-secure-storage` - secrets that never enter a backup.
- `settings-and-preferences` - preferences, outside the backup by default.
- `privacy-and-store-declarations` - what exporting and sharing mean for privacy answers.
- `networking-and-server-state` - an opt-in cloud backup (same envelope and ladder).
- `media-images-and-files` - photos and attachments.
- `unit-and-component-tests`, `e2e-maestro` - test conventions and device flows.
- `ios-simulator-build`, `android-emulator-build` - the builds the drill installs.
