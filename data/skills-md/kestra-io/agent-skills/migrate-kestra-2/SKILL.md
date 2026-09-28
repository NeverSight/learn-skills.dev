---
name: migrate-kestra-2
description: "Migrate a Kestra 1.3 instance and its flows to Kestra 2.0: pre-flight audit with readiness report and complexity rating, server upgrade (database migrations, Docker/Helm), CLI-first flow migration with kestra-migrate, and guided rewrites of the patterns the CLI cannot automate (ForEach/ForEachItem → Loop, trigger conditions → when/dependsOn, pluginDefaults → Policies). Use when users want to upgrade or migrate to Kestra 2.0, ask if their instance is ready for 2.0, mention kestra-migrate or its warnings, or report flows failing to parse after a 2.0 upgrade. For migrations FROM other orchestrators (Airflow), use migrate-airflow-kestra instead."
---

# migrate-kestra-2

Guide a user through the full Kestra 1.3 → 2.0 migration: audit, flow migration, server upgrade, verification. The stance throughout is **advisory** — warn loudly, record every accepted risk, proceed only on the user's explicit go. The authoritative knowledge source is the official migration guide at `https://kestra.io/docs/migration-guide/v2.0.0/` (cite the matching page whenever you apply a pattern); the bundled `references/` files distill it for offline use.

Two hard facts frame every conversation:

- **The upgrade is a one-way door.** Kestra 2.0 drops the JDBC queue tables on first start — irreversibly — and rehashes BasicAuth passwords to bcrypt, which breaks 1.x login after rollback. A verified pre-upgrade backup is the only way back.
- **Migrated 2.0 syntax does not parse on 1.3, and unmigrated 1.3 patterns fail to parse on 2.0.** Sequencing is therefore not optional; the audit's Target answer decides it (Phase 2).

## Step 0 — Route

Before anything else, identify where this user is in the journey:

| Signal | Route |
|---|---|
| No readiness report, no ledger | Phase 1 (fresh start) |
| `kestra-2-migration-readiness-*.md` exists | Phase 2, reusing the report's facts |
| `migration-ledger.md` exists | Phase 2, resuming from its non-terminal rows |
| A single pattern question ("how do I migrate this ForEachItem?") | Jump straight to the matching reference file; no phases |

Routing is complete when you have named the route to the user and they've confirmed it.

## Phase 1 — Pre-flight audit

Full procedure, interview script, complexity tiers, and report template: [references/audit.md](references/audit.md).

The shape: **ask access, confirm the probe plan, then detect first, ask the rest**. Access (instance URL, auth method, tenant) is always asked — the user sees where the agent points before anything runs. Then probe what a machine can know (binaries, kestractl contexts, instance version/edition, flow counts, `kestra-migrate --check` triage), and interview the user only on what it can't (topology, flow source of truth, safety, target, integrations, timeline). One instance per run — for fleets, recommend starting with staging and re-running per instance.

The advisory guardrail lives here: if no verified backup exists, tell the user to take and verify one before any upgrade step, explain the one-way door, and — if they choose to proceed anyway — record it in the report's risk register as an explicitly accepted risk.

**Done when:** the access answers were confirmed by the user before the first probe, the readiness report is written to disk, every interview area is answered or detection-skipped, and a complexity tier (Low/Medium/High/Critical) is assigned with cited evidence.

## Phase 2 — Flow migration

CLI mechanics (flags, output parsing, kestractl fallback commands): [references/cli-reference.md](references/cli-reference.md).

1. **Export** the v1.3 flows to a local directory — from Git when it is the source of truth, otherwise from the instance (via the kestra-ops skill when installed; fallback commands in cli-reference).
2. **Triage**: `kestra-migrate --check <dir>` classifies every flow as clean (✔), auto-migratable (✎), or needing manual work (✗). Then run the **blind-spot greps** from cli-reference — `kestra-migrate` misses `json(` and `pluginDefaults:`, both hard breaks.
3. **Create the ledger** (`migration-ledger.md`, beside the flows) — one row per flow:

   | flow | state | notes |
   |---|---|---|
   | `<namespace>.<id>` | `clean` \| `auto-migrated` \| `rewritten-confirmed` \| `deferred(reason)` \| `validated` \| `deployed` \| `held(reason)` | pattern classes, decisions, accepted risks |

4. **Auto-migrate**: `kestra-migrate -o v2-flows/ <dir>`, capturing stderr warnings (ANSI-stripped) into the ledger.
5. **Guided migration**, hybrid granularity:
   - **Batch pass** for mechanical classes — apply across all affected flows at once: `json()` → `fromJson()`, Pebble `version=` → `revision=`, `fromIon()` wrapping, `checks[].condition` → `when`. Table in [references/removed-constructs.md](references/removed-constructs.md). These only apply to flow code, be careful to not edit Python/JS code embedded that might use `json()` syntax.
   - **Flow-by-flow** for structural classes — each rewrite is presented as a diff with reasoning and its migration-guide link, applied on the user's confirmation. Ground rewrites in the 2.0 target's flow schema (see Composition):
     - `ForEach`/`ForEachItem`/`EachSequential`/`EachParallel` → [references/foreach-to-loop.md](references/foreach-to-loop.md)
     - trigger `conditions`/`preconditions` → [references/trigger-conditions.md](references/trigger-conditions.md)
     - `pluginDefaults` → [references/plugin-defaults.md](references/plugin-defaults.md)
     - removed types with no direct replacement → [references/removed-constructs.md](references/removed-constructs.md); implement the documented alternative on confirmation, or mark the flow `deferred(reason)` in the ledger.
6. **Validate** against a real 2.0 instance: `kestractl flows validate v2-flows/ --output json`. Triage failures per cli-reference. Validation needs a 2.0 endpoint — if none exists yet, the server upgrade (Phase 3, side-by-side provisioning) comes first.
7. **Deploy on confirmation**: `kestractl flows deploy v2-flows/ --override` to the 2.0 target — staging namespace/instance first when one exists. Update ledger rows to `deployed`.

   With two instances live, every validate/deploy carries explicit target flags — kestractl has no `--context` flag (cli-reference §Targeting an instance).

**Sequencing by the audit's Target answer:**

- **Side-by-side** (new 2.0 instance): provision the 2.0 instance (Phase 3) → validate → deploy there → cut triggers/traffic over.
- **In-place**: prepare fully-migrated flows in `v2-flows/`/Git; optionally deploy the `--stay-v1-compatible` output back to 1.3 during the transition window; at cutover run Phase 3, then deploy the fully-migrated flows immediately after the 2.0 server starts.

**Done when:** every flow in the ledger sits in a terminal state — `validated`/`deployed`, or `deferred` with a recorded reason. A flow unaccounted for means the phase is still open.

## Phase 3 — Server upgrade

Full sequence, Docker Compose and Kubernetes recipes, EE/OSS branches, rollback constraints: [references/server-upgrade.md](references/server-upgrade.md).

Two paths by the audit's Target answer:

- **In-place** (the one-way door): verify ≥ 1.3.0 → **verified backup** → stop all instances → `kestra migrate plan` then `kestra migrate run` with the 2.0 binary (EE must run it manually; OSS auto-migrates on startup) → image/chart bump → start.
- **Side-by-side**: provision a fresh 2.0 instance on a fresh, empty database while v1 keeps running — the one-way door stays shut, and rollback is "keep using v1" (server-upgrade §Side-by-side path).

**Done when:** the 2.0 server is running, migrations are verified complete — `kestra migrate plan` reports nothing pending, or (no exec access / OSS auto-migrate) startup logs show every `MigrationRunner` migration applied and none pending or failed — workers show a successful controller handshake (gRPC port 50051), and — in-place path — the migrated flows are deployed.

## Phase 4 — Verify

1. Every ledger row `deployed` executes (commands: cli-reference §executions) or lands in an explicit `held(reason)`: disabled flows (the server refuses manual runs — hold as-is), input-requiring flows (run with user-supplied test inputs, or hold), trigger-only flows (verify on the next natural fire, or hold as accepted risk). Every hold is the user's call, recorded in the ledger.
2. Run the **smoke-test checklist** for silent behavior changes (generated into the ledger during Phase 2): `fs.local.Delete` recursive default flip, ION binary `read()`, Flow-trigger default states losing `PAUSED`, `trigger.outputs` flowId scoping, `dependsOn` gating probe.
3. EE: verify migrated RBAC roles (action model) and re-grant dropped `IMPERSONATE`/`TEMPLATE` permissions; review auto-migrated Policies.

**Done when:** smoke checklist items are each confirmed or logged as accepted risk in the ledger, and the user has declared cutover complete.

## Composition

Prefer these skills when installed — search the available agent skills by name; install location varies (project or user scope): **kestra-ops** for every kestractl operation (contexts, export, validate, deploy), **kestra-flow** for schema-grounded YAML rewriting — with one override: kestra-flow predates 2.0 (it still suggests `ForEach` and the public schema), so this skill's pattern references win wherever they disagree. Ground 2.0 rewrites in the live target's own schema: `GET <2.0-host>/api/v1/plugins/schemas/flow` (tenant-less path) — the public `api.kestra.io` schema tracks 1.x and validates removed constructs. Standalone fallback: the exact commands inlined in [references/cli-reference.md](references/cli-reference.md).
