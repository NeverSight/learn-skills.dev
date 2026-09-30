---
name: manage-report-lifecycle
description: Consolidate, replace, or supersede hosted analytical reports without losing evidence.
disable-model-invocation: true
---

# Manage report lifecycle

Establish one authoritative hosted report while preserving every source item and predecessor. This skill coordinates lifecycle semantics here, shared-state authorization through `preflight-mutations`, and final acceptance through `done`.

## 1. Inventory the report set

Run one authoritative host or workspace discovery query broad enough to find every hosted analytical artifact matching the report's title, stable ID, source URLs, or subject. Record the exact query, every match's stable host ID and current guard, and classify each as `source`, `canonical-candidate`, or `unrelated`, with a rationale.

Fetch the rendered content and stable URL of every source and canonical candidate. For each, record its URL, title, write authority, current authority or supersession marker, and source-owned finding or item IDs with their direct evidence URLs. Preserve source-workflow IDs. When a report has none, assign artifact-scoped IDs without changing the source.

Keep this working record inline during read-only inventory and staging. Before the multi-write publication begins, persist it in an existing durable ledger that the user authorized this workflow to write. Record its stable URL or path and require it to remain outside every canonical and predecessor publication target for the full run. When no such ledger exists, stop and name authorization of a suitable existing artifact as the next action. Create no lifecycle registry.

The gate is that the exact discovery query and every classified match are recorded, every source, canonical candidate, and source item appears once, write authority is known, and competing authority claims are explicit.

## 2. Stage the canonical record

Choose one existing hosted, writable canonical candidate with a known stable URL and current write guard. When none exists, stop and name creation or selection of that hosted candidate as the next action. This skill does not create the first canonical object.

After election, reclassify every discovery match as `canonical`, `writable-predecessor`, `unwritable-predecessor`, or `unrelated`, with a rationale for every unrelated match. Every noncanonical match presenting itself as current authority must be one predecessor class and appear in the lifecycle record and publication plan.

Keep the lifecycle Artifact ID independent of any hosted version. Reuse an existing lifecycle ID or assign it once, retain it across replacements, and separately record the elected version's host object ID and URL.

Stage this section in the canonical report:

```markdown
## Report lifecycle

- **Artifact ID:** <stable ID>
- **Current host object ID:** <host ID>
- **Canonical URL:** <exact URL>
- **Source reports:** <complete URL list>
- **Supersedes:** <complete predecessor ID and URL list>
- **Unwritable predecessors:** <URL and reason, or none>
```

For every writable predecessor, stage its complete fetched report plus `Superseded by [<artifact ID>](<canonical URL>).` Preserve the original body and attributed evidence byte-for-byte. A marker-only replacement is not a valid payload. Record an unwritable predecessor and the reason in the canonical report instead of treating its missing marker as success.

Select one disposition for every source item:

| Source item ID | Source evidence URL | Disposition | Canonical destination or rationale |
|---|---|---|---|
| <ID> | <URL> | carried \| merged \| dismissed \| retained-by-reference | <canonical item/anchor ID or dismissal rationale> |

`carried` and `merged` name an existing canonical destination ID. `dismissed` records a reason. `retained-by-reference` names the canonical anchor that keeps the original evidence reachable. Merge only genuinely equivalent items. Preserve unique findings as distinct destinations or references rather than copying entire source reports.

Finalize and validate the disposition map before rendering any publication payload. Require its source-item IDs to equal the inventory exactly, with no duplicate rows, and require every named canonical destination or anchor to exist in the staged canonical record.

Render the complete canonical payload and every writable predecessor payload to separate immutable local staging paths, treating each path as write-once. Record each path and SHA-256 digest in the lifecycle ledger. Never overwrite or regenerate a frozen file. Changed bytes require a new path, digest, preview, and preflight.

The gate is that an existing hosted writable canonical candidate and guard are known, every discovery match has its final classification, every noncanonical authority is bound as a predecessor, and the canonical payload, predecessor report-plus-marker payloads, and item map are fully staged with every source item assigned exactly one valid disposition.

## 3. Preflight the publication plan

Build one complete logical publication plan containing:

- the complete canonical payload and its current write guard;
- every canonical and writable-predecessor payload's frozen local path, SHA-256 digest, and current write guard;
- the artifact ID, canonical URL, source URLs, superseded list, and unwritable-predecessor record;
- every source-item disposition and destination or rationale;
- the authoritative rendered-link and duplicate-status read-back plan;
- the dependency order across all writes.

Partition that plan into one or more mutation cards exactly where `preflight-mutations` requires different ownership, environment, reversibility, or confirmation domains. Preview all cards together. Invoke `preflight-mutations` for each card immediately before its first write, passing its exact targets, authorization, guards, recovery, invalidators, ordered items, dependencies, and read-back plan.

Apply each card's `preflight-mutations` result contract in the previewed dependency order. Preserve blocked or confirmation-required cards and their dependent writes as pending. A new target, marker, or content change returns the complete plan to preview. Re-preflight only invalidated cards.

The gate is that the complete preview accounts for every lifecycle write, each write belongs to exactly one domain-correct card, and no unpreviewed or dependency-violating write can execute.

## 4. Publish and reconcile

Apply the staged canonical payload and predecessor report-plus-marker payloads without regenerating them. Immediately before each write, rehash its frozen file and require the digest to match the ledger and current mutation card. A mismatch invalidates that card before the write. Atomically transition that item from `pending` to `attempting` in the durable ledger and continue only when the transition succeeds from the expected state. Follow `preflight-mutations`' execution and partial-state contract for each card while preserving the publication plan's dependency order and combined item ledger. After each attempted write, authoritatively read back the body and guard, then atomically persist that item's result, read-back guard, and observed body digest in the durable ledger before the next write. An unavailable or ambiguous ledger transition stops the dependent remainder. Mark an item `landed` only when its complete read-back body matches the frozen bytes. Require every predecessor's fetched content and attributed evidence to remain intact before recording its marker write as `landed`, and record the read-back guard as that target's expected post-write guard.

The gate is that every publication-plan item has an authoritative result, every landed payload matches its staged content, and the canonical report plus each writable predecessor has an expected post-write guard from authoritative read-back.

## 5. Verify authority and evidence

Re-fetch and reread the rendered canonical report and every predecessor. Exercise every canonical, source, predecessor, and evidence link. Repeat the exact Phase 1 discovery query and compare its stable host IDs and guards with the expected set. Use Phase 4's authoritative post-write guards for landed targets and Phase 1 guards for untouched matches. An expected landed guard is not drift. A missing stable ID, a new match, or any guard outside that expected set returns to inventory, staging, and preflight. Fetch every unexpected match before continuing.

Completion requires:

- the canonical report exposes the exact lifecycle artifact ID, current host object ID, canonical URL, complete source URLs, and superseded list;
- every writable predecessor renders the canonical replacement marker and link;
- every unwritable predecessor and reason appears in the canonical report;
- every source item appears exactly once in the item map, with a reachable destination or recorded dismissal rationale;
- every required rendered link resolves; and
- no writable predecessor or duplicate match still presents itself as current authority.

Repair and re-read missing evidence or links before completion. A writable competing authority, broken required link, or unaccounted source item blocks completion.

Run `done` for the final documentation, external-metadata, and publication lanes that apply. Include the final item ledger, rendered link results, duplicate-status query, unwritable predecessors, and exact next action.

The run is done when one hosted report is verifiably canonical, all predecessors are marked or documented, every source item is accounted for, and the completion claim matches `done`'s evidence ceiling.
