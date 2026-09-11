---
name: hrt-backlog-reconcile
description: "User-invoked maintenance for openspec/BACKLOG.md. Reconciles deferred-slice entries against the shipped specs in openspec/specs/, proposes deleting entries now covered, and edits the file only on the user's per-entry confirmation. Not part of the tempa-spec pipeline. Run it by hand, ideally right after openspec archive."
---

# hrt-backlog-reconcile

`openspec/BACKLOG.md` holds slices deferred while planning other changes (written by `hrt-change-size-gate`). Entries are removed only when someone does it by hand, so shipped work covers some but they linger, and `discovery` keeps reading them as stale interview context. This skill reconciles the backlog against what has actually shipped.

No `schema.yaml` instruction invokes this — it is user-invoked only (`/hrt-backlog-reconcile`). Best run right after `openspec archive <change>`, when `openspec/specs/` has just absorbed a change's delta specs, but it works any time.

## Procedure

1. Read `openspec/BACKLOG.md`. If it is missing or has no entries, say so and stop.
2. For each entry, take its `Slice:` line and judge it against the requirements in `openspec/specs/**/*.md`:
   - **Covered** — shipped requirements now deliver that demoable behavior. Propose deleting the entry.
   - **Partially covered** — report which part remains; do not propose deletion.
   - **Not covered** — leave it, say nothing.
   Semantic judgment, not a string match. A shared capability name is not proof.
3. Show every proposed deletion and partial-coverage note one entry at a time: name the entry, quote its `Slice:` line, name the covering requirement(s), ask the user to confirm. Follow the `plain-language-writing` skill's COMMS rules.
4. Apply only confirmed deletions. Remove the entry's full block (`## <slug>` heading through its last `- ` line). Keep the `# Deferred Slices` header even if the file empties. MUST NOT delete the file.
5. Report what was removed and what was kept.

## Entry format (kept in sync with hrt-change-size-gate)

```
## <slug-kebab>
- Raised by: <change-id> (<YYYY-MM-DD>)
- Slice: <1–2 sentences: what a user can demo when this slice is done>
- Deferred because: <blocking dependency / scope / capacity>
```

File header, when the file exists:

```
# Deferred Slices

> Slices raised while planning another change, deliberately deferred. Not proposals - just enough to start a `discovery` session. Delete an entry when it becomes a change.
```

`hrt-change-size-gate` owns writes to this file during `proposal` (adding on a split, deleting entries its own change covers); this skill owns hand-run reconciliation. Both follow the format above.

## Limits

- Specs-based only. An entry whose `Raised by` change was abandoned, with no trace in `openspec/specs/`, is not detected here — prune those by hand.
- Needs an interactive user for step 3. In a non-interactive run, report the proposed deletions and stop without editing.
