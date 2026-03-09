---
name: migrating-nango-deletion-detection
description: Migrates Nango syncs from deleteRecordsFromPreviousExecutions()/trackDeletes to trackDeletesStart/trackDeletesEnd for automated deletion detection (including checkpoint-based full refresh). Use when updating existing createSync code.
---

# Migrating Nango Deletion Detection

## Do this

1. Find legacy usage:
   - `deleteRecordsFromPreviousExecutions(`
   - `trackDeletes:` / `track_deletes`
2. For each sync + model that needs automatic deletion detection:
   - Add `await nango.trackDeletesStart('ModelName')` at the start of `exec` (before fetching/saving).
   - Replace `await nango.deleteRecordsFromPreviousExecutions('ModelName')` with `await nango.trackDeletesEnd('ModelName')`.
   - Keep `trackDeletesEnd` after all `batchSave`/`batchUpdate`/`batchDelete` calls.
3. Safety:
   - Only call `trackDeletesEnd` if the full dataset was fetched + saved between `trackDeletesStart` and `trackDeletesEnd` (otherwise you can cause false deletions).
   - Prefer letting exceptions bubble. If you `catch`, re-throw when data is incomplete.

## Checkpointed full refresh (multi-execution)

- Call `trackDeletesStart('ModelName')` at the beginning of each execution in the refresh window (it is safe/idempotent while the window is open).
- Call `trackDeletesEnd('ModelName')` only in the execution that finishes saving the full dataset.

## Tests

- Re-record mocks after code changes:
  - `nango dryrun <sync-name> <connection-id> --validate -e dev --no-interactive --auto-confirm`
  - `nango dryrun <sync-name> <connection-id> --save -e dev --no-interactive --auto-confirm`
  - `nango generate:tests && npm test`
- Never hand-edit `*.test.json`.

## Before/after

```ts
// Before
for await (const page of nango.paginate(cfg)) {
    await nango.batchSave(page, 'Ticket');
}
await nango.deleteRecordsFromPreviousExecutions('Ticket');
```

```ts
// After
await nango.trackDeletesStart('Ticket');

for await (const page of nango.paginate(cfg)) {
    await nango.batchSave(page, 'Ticket');
}

await nango.trackDeletesEnd('Ticket');
```
