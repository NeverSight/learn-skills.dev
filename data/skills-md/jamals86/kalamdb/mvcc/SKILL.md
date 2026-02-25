---
name: mvcc
description: 'MVCC in KalamDB: versioned records, visibility rules, snapshot reads, compaction, and transaction lifecycles. Keywords: mvcc, snapshot, visibility, commit, abort, tombstone, vacuum.'
---

Use this skill when implementing or modifying MVCC logic, including version metadata, visibility filtering, and cleanup.

Core principles:
- Reads see a consistent snapshot; writes create new versions.
- Version chains must be ordered and efficiently prunable.
- Visibility is determined by transaction timestamp/epoch and commit status.

Implementation guidance:
1) Locate the existing MVCC abstractions (e.g., version metadata types, visibility filters) before adding new logic.
2) Ensure reads filter out uncommitted or aborted versions and respect snapshot boundaries.
3) When inserting updates, create new version entries rather than in-place mutation.
4) For deletes, add tombstones and make them visible using the same MVCC rules.
5) Compaction/cleanup must only remove versions that are not visible to any active snapshot.
6) Keep metadata lightweight and store large payloads separately if needed.

Common pitfalls:
- Returning uncommitted data to readers.
- Deleting versions still visible to long-running snapshots.
- Mixing wall-clock time with logical timestamps; use the project’s canonical time/epoch source.

When adding new APIs:
- Prefer typed identifiers and enums.
- Keep MVCC filtering in the query path, not at the storage engine boundary unless it is explicitly part of the storage abstraction.
