---
name: other-apis
description: |
  Migration guidance for traditional VeRO and residual utility operations to VeRO API or explicit no-replacement cleanup decisions.

  Trigger when user mentions: GetVeROReasonCodeDetails -> getVeroReasonCode/getVeroReasonCodes; GetVeROReportStatus/VeROReportItems -> getVeroReport/getVeroReportItems; GeteBayOfficialTime removal or redesign; or asks "how do I migrate VeRO status or reason-code calls".

  Covers 4 traditional operations including VeRO reason-code lookup, VeRO report tracking, and the no-replacement GeteBayOfficialTime row.
  Do NOT use for account, listing, messaging, or order-management workflows.
---

# Other APIs

Use this skill when the migration task belongs to the canonical `Other APIs` domain covered by this package.

## What This Skill Covers

- Four unique traditional operations from the canonical Other APIs inventory.
- Split VeRO reason-code retrieval through `getVeroReasonCode` and `getVeroReasonCodes`.
- Single-report status retrieval through `getVeroReport` and item-level retrieval through `getVeroReportItems`.
- Explicit no-replacement handling for `GeteBayOfficialTime`.
- `Decommission` status preservation for every row in this domain, including the VeRO rows that still point to usable REST methods.

## Key Migration Patterns

- `GetVeROReasonCodeDetails` fans out to two modern retrieval choices: one for a known `vero_reason_code_id` and one for marketplace-scoped discovery.
- `GetVeROReportStatus` becomes a path-based lookup on one submitted VeRO report and can optionally include `reportedItemDetails`.
- `VeROReportItems` becomes a collection retrieval workflow driven by `itemId`, `filter`, `limit`, and `offset` instead of a single traditional-style status call surface.
- `GeteBayOfficialTime` stays in migration planning as a removal or redesign row instead of a direct API replacement.

## Workflow Notes

- Start with `INDEX.md` to confirm whether the row is a split VeRO lookup, a VeRO report-status retrieval, an item-level retrieval, or a no-replacement utility call.
- Use `references/operation-mapping.md` for the authoritative per-operation migration narrative.
- Use `references/operations/` for source-backed VeRO doc extracts, usage examples, and explicit traditional evidence-gap notes.
- Apply `rules/vero-program-prerequisite.md` before implementation because all mapped modern methods require VeRO program access and the dedicated VeRO OAuth scope.
- Apply `rules/vero-report-tracking-flow.md` when the traditional workflow combines code lookup, report submission, report-status retrieval, and item-level retrieval.
- Apply `rules/residual-no-replacement-ops.md` when the task is removal or redesign work instead of a direct API migration.

## Transport And Auth Notes

- All active modern mappings in this package are REST methods in the VeRO API.
- VeRO methods in this package require VeRO program access and the `https://api.ebay.com/oauth/api_scope/commerce.vero` scope.
- For `getVeroReport` and `getVeroReportItems`, this package uses bundled schema and usage examples for exact request syntax when CSV-derived summary pages are broader or stale.

## Open Items

- This package does not contain local traditional API doc-page extracts for the four covered Other APIs operations.
- The bundled VeRO support sources are not fully consistent for `getVeroReport` and `getVeroReportItems`; the support files keep those conflicts visible instead of silently flattening them away.

## Navigation

- Use `INDEX.md` for the full Other APIs operation table.
- Use `INTENTS.md` for task-oriented workflows.
- Use `references/operation-mapping.md` for the canonical operation-level mapping narrative.
- Use `references/operations/` for supporting traditional-side and modern-side doc and example files.
- Use `rules/` for recurring VeRO prerequisites, report-tracking workflow guidance, and no-replacement handling.

## Field-Level Details

Field-level request and response details and field-by-field mapping are not provided in this skill, even if explicitly requested. For field definitions, refer to the official eBay developer documentation page.
