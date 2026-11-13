---
name: deliver-setup
description: Check delivery prerequisites and offer fixes, configure delivery profiles and project defaults, validate a delivery host, migrate legacy Orca orchestration settings to `deliver` (or `flyingnobita-deliver`), or move Herdr top-level role tables under [hosts.herdr.roles.<role>].
---

# Set up delivery

Configure the requested repo for `deliver` (or `flyingnobita-deliver`). This is an idempotent
setup operation, not a delivery run. Existing valid defaults need no repeated
interview. Inside Deliver, join unresolved choices to its grilling stop.

1. Read the repo's rules and the shared
   [configuration](../deliver/references/configuration.md).
   Detect the host using [host detection](../deliver/references/host-detection.md).
   Read only its adapter: [Orca](../deliver/adapters/orca.md),
   [Herdr](../deliver/adapters/herdr.md), or
   [Paseo](../deliver/adapters/paseo.md).
2. Run every check in [prerequisites](references/prerequisites.md) for the
   selected host and report its table. For each failed required row, give the
   fix and its link, and apply it only on the user's approval. A blocking row
   (missing commit capability, helper or host component) stops setup
   before smoke tests. Then present the optional section separately.
3. If legacy configuration or an old run exists, read
   [migration](../deliver/references/migration.md). Preview changes
   and inventory existing runs before proposing removal. Do not commandeer them.
4. Resolve planner, implementer, reviewer and QA settings. Recommend a distinct
   reviewer model/harness when available. Ask only for missing/unsupported
   choices and changes in authority. Keep the initiating orchestrator unchanged.
   Review concurrency, human schedule and landing separately from permissions.
   When changing a Herdr harness, choose compatible `model`, `effort` and `mode`
   together; see [Changing a Herdr harness](../deliver/references/configuration.md#changing-a-herdr-harness).
5. Validate selected profiles through no-edit smoke tasks in a disposable
   workspace under the confirmed host. Ask each to report only its identity and
   completion; compare requested/effective settings. Native settlement, release
   and cleanup must be verified. Do not mark a failed or unavailable launch
   validated or silently broaden its permissions. Use an isolated setup record;
   a smoke test grants no delivery brief/plan approval. Use `purpose:"setup"`
   and `approved.setup` with the concrete request/selected profiles as defined
   in [run records](../deliver/references/run-record.md). Orca and
   Herdr smoke jobs use role `smoke` with each selected profile in turn.
6. Back up any existing project config. Write only approved project values,
   preserving unknown keys and unrelated host tables. On Herdr, write role
   profiles only as `[hosts.herdr.roles.<role>]` tables, and migrate old
   top-level role tables as described in [Herdr role table
   migration](#herdr-role-table-migration). Paseo profiles remain in
   Paseo; report required changes there rather than overwriting them. Keep
   legacy files and migration evidence while old runs may need them.
7. Add a concise pointer to `docs/agents/delivery.toml` in the repo's `AGENTS.md`
   only when requested or approved. The autonomous merge rule still requires
   the separate explicit consent in Deliver's project rules. Optional tracker
   setup is not a prerequisite to this skill.

Done when every required prerequisite is `ok` or named as a blocker, every
optional item was offered, settings are recorded, every selected profile has a
verified result or explicit blocker, and every setup resource is removed or
named as retained. Report the prerequisite table, changes, effective settings,
permissions, smoke evidence and migration decisions. Commit through
repository commit rules (or a configured custom commit skill); publication is separate.

## Herdr role table migration

A Herdr project layer lives under `[hosts.herdr.roles.<role>]`. When
`docs/agents/delivery.toml` has old top-level `[planner]`, `[implementer]`,
`[reviewer]` or `[qa]` tables and no `[hosts.herdr.roles.*]`, offer to move
them:

1. Back up the file and read the effective profiles first with `deliver-runtime
   herdr-project-roles` and `profiles`, passing
   [herdr-profiles.toml](../deliver/references/herdr-profiles.toml)
   as `defaults`.
2. Move each of the four role tables under `[hosts.herdr.roles.<role>]`, keeping
   every key and value, including unknown keys.
3. Leave `[delivery]`, `[hosts]`, other host tables, comments and all unrelated
   content in place.
4. Show the proposed file or its diff and get approval before writing it.
5. Repeat the profile reads and confirm the effective Herdr profiles are
   unchanged and no layout warning is reported.
6. Confirm no top-level role table remains; keep the backup as migration
   evidence while old runs may need it.
