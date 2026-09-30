---
name: sync-agent-setups
description: Preview and sync Claude Code's user-authored behavioral setup outward to selected agents.
disable-model-invocation: true
---

# Sync Agent Setups

Claude Code is the only source of truth. This workflow lists every detected non-Claude agent, but it writes only to targets the user confirms during this invocation. It never starts automatically.

## 1. Inventory source and targets

Find Claude's active user-level setup on the current machine rather than assuming fixed paths. List only user-authored behavior:

- global rules;
- skills;
- custom slash workflows;
- hooks; and
- non-secret behavioral settings.

Exclude credentials, conversation history, caches, telemetry, generated runtime state, and platform-managed content. Detect every installed non-Claude agent and its supported setup surfaces read-only. Record unavailable or ambiguous surfaces instead of guessing.

Resolve each Claude-visible source through any symlink and calculate its checksum. Read the target's current path, file kind, link target, and checksum without following a downstream difference back into Claude.

**Gate.** every source and detected target has a stable path, ownership classification, and explicit in-scope or excluded reason.

## 2. Produce the dry-run manifest

Classify every in-scope pair per `${CLAUDE_SKILL_DIR}/references/manifest.md`. Load it now. It holds the classification table, the staged-adaptation rule, the backup-path resolution, and the manifest template. Exit only when every item carries exactly one status and every adaptation preview shows final bytes with their semantic delta.

## 3. Confirm the write set

Ask the user to select or confirm the target agents from the preview. Detection is not write authorization. A confirmation covers only the named targets, `ready` item IDs, backup path, exact-copy link targets, staged adaptation paths, checksums, and intended modes, semantic deltas, and proposed actions shown in the current manifest.

Re-inventory after confirmation, re-resolve the backup path, and rehash every staged adaptation. Any changed source checksum, target state, classification, path, selected target, resolved backup path, staged bytes, staged checksum, or intended mode invalidates that item and returns it to preview. Change confirmed `ready` items to `pending`; retain every `blocked`, `preserved-unsupported`, and `preserved-orphaned` row in the ledger.

**Gate.** every `pending` item belongs to an explicitly confirmed target and still matches its preview, while every non-ready item remains outside the mutation batch with its status and reason intact.

## 4. Preflight and back up

Immediately before the first backup or target write, invoke `preflight-mutations` for only the selected `pending` items. Include their target agents, source and target paths, current checksums and link targets, staged adaptation paths, checksums, and intended modes, semantic deltas, confirmation source, shared-symlink risk, resolved timestamped backup path, invalidators, per-item recovery, and post-write read-back. Reference the complete ledger for context, but do not put `blocked`, `preserved-unsupported`, or `preserved-orphaned` items into the mutation card's targets or batch items. Continue only when this independently ready mutation batch returns `ready` with unchanged guards.

Create the confirmed timestamped backup at the recorded resolved physical path before changing a target. Preserve for every affected path:

- its original path and whether it was absent, a file, directory, or symlink;
- symlink text without dereferencing it;
- resolved path and checksum when one exists; and
- enough content and permissions to restore the prior target state.

Write a backup manifest mapping each item ID to its recovery action. Verify the backup inventory and checksums before the first target mutation.

**Gate.** every pending target path has a verified recovery record, including preserved link metadata and resolved content evidence.

## 5. Apply confirmed items

Apply each item and verify each target per `${CLAUDE_SKILL_DIR}/references/apply-verify.md`. Load it now. It holds the write protection, the per-kind apply rules, the restore discipline, and the per-target verification. Exit only when every attempted item has a read-back state and everything untouched is byte- and link-identical to preflight.


**Done.** every detected target and source artifact is accounted for, only confirmed targets changed, every changed path is recoverable, and each target's parity claim is capped at its weakest acceptance surface.
