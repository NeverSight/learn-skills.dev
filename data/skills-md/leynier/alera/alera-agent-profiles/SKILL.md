---
name: alera-agent-profiles
description: Maintain Alera Agent Profiles or research and validate a launch catalog.
metadata:
  version: 2
---

# Alera Agent Profiles

Use `alera agent-profile` to inspect or administer launch recipes. `alera orchestration agent-profiles` is read-only coordinator discovery. Ordinary dispatch belongs to the `alera-orchestration` skill.

## Choose The Scope

- List, show, rename, edit a description, reorder, remove, or launch an existing profile: read [maintenance](references/maintenance.md). Apply the specified change and verify persistence; no model research or smoke test is required for a metadata edit.
- Select models, redesign roles, or compare quota pools: read [catalog research](references/catalog-research.md).
- Create or change Managed launch configuration: read [managed profiles](references/managed-profiles.md). Discover support for the affected model and flags rather than assuming remembered values.
- Requested launch smoke tests or launch/status diagnosis: read [launch validation](references/launch-validation.md).

## Authorization And Scope

Listing, research, and previews are read-only. Creating, updating, reordering, removing, or launching profiles changes runtime state and must be covered by the user's request. Honor prior explicit authorization for the same scope; do not add another approval round. A proposal-only request stops at the proposal.

Never infer permission to reduce protections from a general profile request. YOLO, bypass, trust, disabled sandbox, and auto-approval changes require explicit intent and the CLI's `--confirm-reduced-protections` when applicable.

Before removal, inspect `removal-impact` and report affected references. Use `--confirm` only for authorized removal; ask only if the discovered impact exceeds that authorization. Preserve unrelated profiles and ordering; reorder supplies every current profile id exactly once. Use the supported CLI instead of the runtime database or private socket requests.
