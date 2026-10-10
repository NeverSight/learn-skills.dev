---
name: start-migration
description: Start, resume, or advance a persisted legacy-to-target codebase migration one validated checkpoint at a time, using two-phase confirm-then-execute helpers, OpenSpec requirement traceability, and mandatory fresh evidence-backed gates before any checkpoint or the whole migration can be marked complete. Use this whenever the user wants to migrate, port, rewrite, or modernize a legacy module, feature, or app into a different target codebase or architecture across multiple sessions — including resuming an interrupted migration, refreshing after the legacy code changed, running in `--mock` data-source mode, checking migration `--status`, upgrading an older persisted migration contract, or invoking a Ponytail review/audit at finalize. Trigger this even when the user just says "continue the migration", "what's the status of the X migration", or describes wanting to move behavior from an old repo into a new one without using the word "migration" explicitly.
user-invocable: true
---

# Start Migration

Execute exactly one validated migration checkpoint, or one implementation/
verification slice, per iteration. A later session — possibly a different model
or provider — resumes from the saved state, never from conversation memory.

## Runtime preflight

Before migration status or any other migration work, run the installed skill's
`scripts/runtime.mjs` from this skill directory:

```bash
node <skill-directory>/scripts/runtime.mjs ensure --provider <claude|codex|opencode|copilot> --root <current-working-directory>
```

Use the provider running this invocation. This preflight is the only normal
runtime installer, and **this skill's own exact identity is what selects the
runtime**: the `release-identity.json` beside this file states the toolkit
version it needs *and* the canonical digest of its own semantics, and only a
release whose manifest proves that digest may run it. Matching version numbers
alone are never enough.

It consults four local sources before any network call — the current receipt,
the releases that receipt retains, sibling provider receipts in this consumer,
and the release store — each verified against its pinned release manifest. A
receipt that satisfies this skill is reused with zero network requests, and it
reuses a verified runtime another provider already installed in this same
consumer without network access; a different required identity found locally
converges offline; only an exact release that exists nowhere locally is fetched,
and then only as the exact tag `v<version>`. The preflight never resolves `releases/latest` and never installs
a release other than the one this skill requires. Then it registers MCP and runs
both doctors. Switching providers never redownloads a runtime this consumer
already has, and never adopts a sibling whose skill identity differs.

The JSON result names which rule fired: `selection` is `skill` (normal),
`pinned` (an explicit rollback is in force) or `explicit` (a one-invocation
`--version`); `skillIdentity` is `required`, `pinned` or `unverified`; and
`network` says whether anything was fetched.

It also re-validates the MCP registration it owns on every run. A registration
that is absent — a consumer tool regenerated the provider configuration, for
instance — is restored from the receipt alone, preserving every unrelated
server and every unrelated provider setting, and reported as `mcpRepair`. A
registration that exists at the owned location but differs from the receipt
fails closed and is never overwritten.

On success, use the absolute commands in its JSON result and continue the
original invocation. A newly installed or repaired registration may not be
loadable by the host that is already running, so prefer MCP only while the
`start-migration` server is actually connected, and use those absolute CLI
commands as the fallback for the rest of this invocation when it is not —
`mcpRepair.restartRequired` means exactly that, and never that the migration
must stop. Stop on preflight failure; never fall back to a checkout, branch,
`latest` URL, package-manager install, or ambient `PATH`.

When the preflight returns `bootstrapped: true` because the required identity
changed, run `artifact-migration-toolkit status` before resuming an existing
migration, so a record still stamped with the previous toolkit identity surfaces
as a decision rather than mid-checkpoint. The preflight itself never reads or
writes any record's `toolkitIdentity`.

### Preflight refusals

Every refusal is typed, names both sides, and leaves the receipt, the release
store, the provider configuration and the MCP registration unchanged. Report the
code and its remedy; do not work around it.

| Code | Remedy to report |
| --- | --- |
| `SKILL_IDENTITY_MISSING` | This skill carries no usable `release-identity.json`. Reinstall it with `skills add`. |
| `SKILL_IDENTITY_LEGACY` | The stamp predates exact identity binding. Reinstall it with `skills add`. |
| `SKILL_IDENTITY_UNRELEASED` | This skill's bytes were never published under the version it names. Install it from a published release with `skills add`. |
| `RELEASE_NOT_PUBLISHED` | No immutable release carries the required version. Install a published release with `skills add`. |
| `RUNTIME_UPDATE_REQUIRED_OFFLINE` | The required release is not available locally. One connected run clears it. |
| `RUNTIME_ARCHIVE_UNREADABLE` | tar could not read the verified release archive; the error names the tar used. Make a working tar available (on Windows, `%SystemRoot%\System32\tar.exe`), then run this skill again. |
| `SKILL_SET_INCOHERENT` | Two installed skills require different releases. Run `skills add` for both so they match. |
| `SKILL_PROJECTION_SKEW` | Installed copies of this skill in different host roots disagree and cannot be updated from a verified `.agents/skills` copy. Run `skills add` for both skills, then run this skill again. |
| `SKILL_PROJECTION_CONVERGED` | This copy was older than `.agents/skills`; every copy and the runtime were updated. Run this skill again so the updated instructions load. |

To update, run `skills add` for both skills; the next preflight from any host
updates every other project copy (`.claude`, `.github`, `.codex`,
`.opencode/skills`) from the verified `.agents/skills` copy and reports the
replaced paths as `projectionsConverged`. Copies a provider receipt owns are
left to that provider's installer.

Never suggest editing or deleting `.artifact-migration-tools/<provider>.json`,
any provider MCP configuration, or the install lock. None of them is a repair
step, and a hand-edited receipt is rejected rather than trusted. An interrupted
installation recovers on its own when its owner process is provably gone.

`--version X.Y.Z` and `ARTIFACT_MIGRATION_TOOLS_VERSION=X.Y.Z` are explicit
admin/CI overrides for **one invocation only**. They select another immutable
release, bypass the identity proof (reported as `skillIdentity: "unverified"`),
persist nothing, and the next ordinary invocation converges back. Only an
explicit `rollback` through the provider installer persists a pin, which is
reported as `selection: "pinned"` on every invocation and is superseded when
`skills add` changes this skill's digest. Neither ever updates a migration
record's `toolkitIdentity`; use the engine's explicit toolkit update/rollback
operation separately when intended.

## Runtime requirements

Run `artifact-migration-discover --doctor` first on any host you have not used before.
It is read-only: it takes no lock, opens no record, and creates no directory.

| Dependency                          | Purpose                                                                  | Failure mode if absent                                                                 |
| ----------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| Node.js 20+                         | Runs every script; the suites use modern `node:test`                     | Scripts fail to parse or the suites do not collect                                     |
| Git                                 | `git ls-files` **is** the census; also `gitRevision`, dirty manifests    | `DISCOVER_LEGACY` and `DISCOVERY_COMPLETENESS` cannot run                              |
| `ts-discovery-compiler`             | The pinned classic-API TypeScript parser (see below)                     | `DISCOVERY_COMPLETENESS` and every artifact structural census fail on module resolution |
| The target's own TypeScript         | Type-checks the target in `migrate-artifact` code validation             | Falls back to the pinned parser and stamps `compiler.origin: PINNED_FALLBACK`           |
| `yaml`                              | `providers:sync` renders provider frontmatter                            | `pnpm providers:check` crashes before it can compare anything                            |
| Playwright MCP                      | Runtime UI evidence for every `hasVisibleUi: true` slice                 | Those slices cannot be verified — an unreachable runtime is **not** a waiver            |
| Figma MCP                           | Optional design-source evidence                                          | Only `--design-source figma-mcp` is unavailable                                         |
| Writable `.agents/knowledge/migrations/` | Records, locks, journals and decision ledgers all live here         | No migration can be bootstrapped, resumed, or locked                                   |
| ripgrep                             | Used by the agent while reading, never shelled out to by a script        | Discovery reading is slower; nothing fails                                              |

`ts-discovery-compiler` is `npm:typescript@5.9.3`, declared by the engine
package itself (`@artifact-migration-tools/migration-engine`), not by the
repository being migrated. It is pinned on purpose: the scan runs the
**classic** Node-hosted TypeScript API, which TypeScript 7+ no longer ships, so
the analyzed project's own compiler cannot stand in for it. Parsing the target's
`tsconfig` and *type-checking* the target are different jobs with opposite
version requirements, and they resolve from different places.

### Installation

Install one exact version of the toolkit anywhere on the host. The engine
package brings its own `node_modules`, so the repository being migrated declares
nothing: no `ts-discovery-compiler`, no skill copy, no engine source.

The engine resolves the consumer's registry, records, locks, journals and
evidence from the **working directory** you run it in. It resolves *itself* from
its own installed location. Those are two different questions and answering the
second one from the first is the defect this layout exists to prevent — so run
every command from the repository being migrated, and never point a command or
an MCP registration at a path inside that repository.

MCP is registered against the installed engine's own entry point, which the
provider adapter resolves at install time. See `provider-compatibility.md`.

## Execution protocol

One protocol, identical on Claude Code, Codex, GitHub Copilot, and OpenCode.
The provider supplies only the front end; the migration engine owns every
decision about what happens next.

```
START -> STATUS FIRST -> persisted state? -> FAST RESUME (no completed-work rescan)
      -> nextWork from the engine -> read only bounded required context
      -> author the requested artifact -> run -> obey the typed outcome -> repeat
```

### 1. Status first

Before reading source files, listing directories, grepping legacy code, or
performing any repository analysis, ask the engine what it already knows:

- MCP: `migration_status { module, cwd }`
- CLI fallback:
  `artifact-migration-discover <module> --status`

Nothing else comes first. A broad repository scan before status is a protocol
violation, not diligence.

### 2. Fast resume

If persisted migration state exists, resume from it. Do not:

- rerun completed discovery;
- re-derive completed checkpoints;
- rescan completed slices;
- reopen work merely because the previous session used another LLM or provider;
- inspect broad repository context before status.

### 3. Obtain `nextWork` from the engine

- MCP: `migration_run`
- CLI fallback:
  `artifact-migration-run <module> ... --json`

`--json` is the typed fallback outcome channel: it prints the same structured
outcome the MCP tool result carries, so the CLI path is read exactly like the
MCP path. Read the `outcome`, never the human `log`.

### 4. Read only bounded required context

- artifacts named by `nextWork`;
- evidence named by `nextWork`;
- schema or reference files `nextWork` explicitly requires.

Nothing broader. Then author the requested artifact and run again.

### 5. Obey the typed outcome literally

- `CONTINUE` — execute exactly the next iteration the engine requires.
- `STOP` — relay the typed stop and do not improvise progression.
- `FORMAT_UPGRADE` — the record owes a format increment and the whole migration
  lifecycle is frozen behind it. Stop. Supply only the input the engine's
  `formatUpgrade` result names, or relay its blockers (see Format upgrades).
- `FORMAT_UPGRADED` — exactly one increment committed and no checkpoint moved.
  Obey the emitted `loop:` line literally; it continues through the same normal
  command.

Providers never decide checkpoint progression themselves. Never infer the next
checkpoint, skip one that "looks done", or continue from conversation memory.
Never select a format-specific transition: which increment is owed, and how it
commits, is the engine's decision, reported as a typed outcome.

## Authorities and boundaries

- **Target authority**: the target root resolved by the migration registry —
  its current source, repository instructions, architecture documents,
  routing conventions, design system, and validation commands.
- **Legacy evidence**: the legacy root resolved by the registry, read-only.
- **Mappings**: the target-owned registry. First setup accepts `--registry
<path>`; confirmed execution persists its workspace-relative binding in the
  canonical project `package.json` for every later command.
- **Active migration state**:
  `.agents/knowledge/migrations/modules/<module>/state.json`.
- **Full schema authority**: `references/migration-contract.md` — read it
  before authoring any JSON artifact by hand; this file only summarizes.
- **Discovery coverage checklist**: `references/discovery-checklist.md`.
- **Requirements authority**: the target-relative path in
  `MIGRATION_REQUIREMENTS_FILE`, defaulting to
  `openspec/specs/<target-module>/spec.md`. At `NOT_STARTED`/`RESOLVE`, this
  file is validly absent because it is a confirmed `RESOLVE` output. After
  initialization it is mandatory and byte-pinned by state.

Migrate observable legacy functional behavior and route flows only. Never
copy legacy source, file structure, component hierarchy, page composition,
layout, visual design, styles, tokens, architecture, routing implementation,
or tests — the target project is always authoritative for all of those.
Ignoring a target-required component or pattern when an equivalent exists is
a `DESIGN_SYSTEM_GAP` unless an explicit exception is approved.

## Invocation

`/start-migration <module>` means: perform one migration iteration for that
module. One iteration is preflight, validate, at most one advance, directive.
Author the artifact it asks for, then obey the `loop:` line. Never continue
from conversation memory — every iteration re-reads `state.json` through its
own preflight.

There are two front ends: use connected MCP when available, otherwise the
installed CLI. Neither front end can attest a module-19 decision.

1. **MCP — preferred whenever the `start-migration` MCP server is connected.**
   Call its `migration_run` tool with the invocation's supplied `module`,
   `target`, `registry`, `slice`, `mode`, `ponytail`, `designSource`, and
   `figma` values. Supply `cwd` as the absolute working directory of the current
   migration interaction on every MCP call (status, scan, pending decisions,
   and run), including in isolated worktrees. The server keeps that context
   through the driver, native elicitation, trusted recorder, and final status
   read; it must not substitute its own checkout. For example,
   `/start-migration roles --target role --ponytail full-audit` becomes
   `{ "module": "roles", "target": "role", "ponytail": "full-audit" }`
   plus `cwd` set to the current absolute working directory.
   Omitted `mode` remains `auto`; omitted migration `ponytail` remains disabled,
   regardless of any session-level `/ponytail` mode. It runs the same driver,
    and may present an engine-owned review. The server is registered in the
    repository's `.mcp.json`. Read `outcome` from the tool result, not the `log`.
    For module format 19, status, pending decisions and run use the same fresh,
    read-only decision projection. Its full candidate-bound review is for
    presentation, not an instruction to transcribe IDs, digests or a challenge.
     The engine-owned `STANDARD_LOCAL` policy requires `AGENT_RELAYED`: the
     operator explicitly selects `APPROVE` or `REJECT` for this review, through
     native elicitation when the host renders it, otherwise in this conversation.
     Cancellation, dismissal, timeout, missing response and transport failure
     append nothing and end at `OPERATOR_DECISION`. No auto-permission, inferred
     intent or prior conversation may answer the review. A provider response never attests a
     human. Only an optional protected high-assurance policy requires
     `HUMAN_ATTESTED`; missing or invalid signer activation then fails closed
     with `SIGNER_UNAVAILABLE`, without downgrade. A recorded decision
    becomes visible to the next status/pending/run call in this same session;
    no restart and no model-carried receipt are required.
    For module formats ≤18 and artifact 13 only, the historical elicitation or
    terminal challenge and `decisionReferences`/`decisionId`/`decisionDigest`
    citation rules still apply. Cite only fields the existing artifact schema
    accepts (`recordedDecisionId` in its pending rows). One human act records
    at most one approval per iteration; a host decline records no rejection.
2. **Bash — the fallback when that server is not connected.**

   ```bash
   artifact-migration-run <module> [--mode auto|step] [--slice <id>] [options]
   ```

   An agent-run shell has no TTY, so an operator decision reached this way
   stops at `OPERATOR_DECISION`; it is relayed as in step 2 below.

Either way the directive's `next=` repeats the iteration; obey it literally
through the same front end.

**Whenever an iteration ends at `OPERATOR_DECISION`**, follow the typed result.
For module 19, when `operatorApproval.blocked` is null:

1. Show the user the engine review (`operatorApproval.review`, or the review in
   `log`), ask them to answer `APPROVE` or `REJECT`, and **end your turn**.
2. Only when the user's next message is an explicit `APPROVE` or `REJECT`, call
   the MCP tool `migration_relay_decision` with `module`, `cwd`,
   `reference` = `operatorApproval.reference` unchanged, and `decision` = that
   answer. Without MCP, run the same relay through the CLI from the same
   working directory:
   `artifact-migration-decision <module> --relay <operatorApproval.reference> --decision <APPROVE|REJECT>`.
   Anything else relays nothing; show the review again if asked.
3. Then call `migration_run` (or `artifact-migration-run <module> --json`)
   again; it resumes normally.

Never approve or reject on your own, never in the same turn you asked, and
never from an earlier message. Never ask the user for IDs, digests, references,
commands or runtime paths; the user types only `APPROVE` or `REJECT`. Never
send them to another terminal or any command other than the relay above. A `STALE_REVIEW` result means the review changed: run
the migration again and ask about the new review. If `blocked` names a
required `HUMAN_ATTESTED` principal, report it and stop; the relay refuses it.
For historical formats,
`reason` names any recorded line and `decisionReferences` carries its citation;
further pending decisions remain unapproved. Never call a host decline a human
rejection: no applicable approval arrived.

**`--mode auto` is a principal, not consent on a human's behalf.** AUTO is a
distinct, auditable principal: it decides what it can derive from evidence it
already holds, records every such decision in its own
`decisions/auto-decisions.ndjson` ledger under its own hash chain, and may never
write, forge or impersonate a line in the human `decisions/operator-decisions.ndjson`.
A judgment needing a person is not AUTO's to make: legacy records stop for
the historical operator act, while module 19 requires an explicit operator
decision even in auto mode. Standard decisions need no signer.
A reported remainder stays unapproved; `--mode step` does not supply attestation.

For historical module formats ≤18 and artifact 13, `operatorApproval` carries
the pending candidate commands and the exact `cwd` in which to run them; the
ordinary next iteration returns citation fields for the historical artifacts.
For module 19, `operatorApproval` instead carries the engine-owned review and
typed blocked state; no terminal challenge or receipt-copying fallback grants
`HUMAN_ATTESTED`. Never inspect or edit raw state/ledger JSON to authorize a
decision, pass approval through a tool/CLI argument, or answer a historical
challenge yourself.

Everything below is the operator's, either because `run` refuses it by name or
because a loop can never reach it. Each line names an executable the installed
toolkit provides, so it resolves wherever the toolkit was installed and never
against the repository being migrated:

```bash
artifact-migration-discover <module> --status | --scan | --reopen-discovery
artifact-migration-discover <module> [--target <t>] [--openspec-proposal-stdin] [--confirm-execution <id>]   # bootstrap
artifact-migration-discover <module> --refresh --confirm-mismatch
artifact-migration-discover <module> --reopen-complete <slice[,slice...]> --reopen-reason <text> --reopen-evidence <path> --confirm-reopen [--confirm-legacy-revision <sha>]
artifact-migration-discover <module> --rework-slice <id> --confirm-rework
artifact-migration-discover <module> --reopen-ui <slice[,slice...]>
artifact-migration-discover <module> --amend-slice <id> --add-file <path> [--add-file <path>...]
artifact-migration-decision <module> --pending | --approve <stable-id> | --list
artifact-migration-registry <module> --target <target> [--alias <alias>]
artifact-migration-upgrade <module> [--confirm-upgrade <id> | --rollback | --recover]
artifact-migration-validate <module> [--step <step> [--slice <id>] | --complete]
artifact-migration-advance <module> --step <step> [--slice <id>] [--mode auto|step] [--confirm-advance <id>]
artifact-migration-toolkit status|adopt|update|rollback --module <module> [--registry <path>]
```

Validation is read-only; advance only after it passes.

The three recovery transitions differ: `--rework-slice` returns an *active*
slice with a recorded `FAIL` to implementation, preserving the failed attempt;
`--reopen-ui` reopens completed slices for a visible-UI parity audit;
`--amend-slice` is **add-only** — it adds files to a reopened slice's pinned
`changedFiles`, requires at least one `--add-file`, and removes nothing. It is
one of the two legitimate exits from `UNCLAIMED_TARGET_DRIFT`, the other being a
`TARGET_DRIFT_ACCEPTED` operator decision.

`artifact-migration-toolkit` is the one identity-maintenance executable, and it
accepts exactly one identity target per invocation: `--module <module>`
[`--registry <path>`] for a module record, or `--artifact <source>`
[`--type <type>`] [`--source-root <path>`] [`--target-root <path>`] for an
artifact record. An identity MISMATCH is reconciled through
`artifact-migration-toolkit`, never by manually editing persisted migration
state. `status` is read-only: it writes nothing, on any record, in any state.
`state.json`, `integrity.json` and `history/history.ndjson` are never
hand-edited to reconcile toolkit identity. `adopt`, `update` and `rollback`
advance no checkpoint, so resume the lifecycle with its own command afterwards.

Registry resolution is shared by every helper and generated provider: existing
migration state, first-setup `--registry`, persisted
`package.json#config.startMigration.registry`, then `MIGRATION_REGISTRY_PATH`
as an optional CI fallback. Conflicting values fail; they never silently
override state. On first setup only, add `--registry
<target-root>/.agents/knowledge/migrations/registry.json`.

- `--mode` defaults to `auto` and selects who supplies each confirmation, never
  what a confirmation authorizes. `auto` eliminates mechanical confirmations,
  never genuine operator decisions or project-level binding changes: AUTO is an
  execution authority, not an exemption from the authorization rules, so every
  transition it confirms still re-verifies its confirmation ID against the
  previewed bytes and still writes its ledger line. What AUTO must never do is
  originate an authorization only the operator can give — it never refreshes a
  legacy mismatch or drift on its own initiative, and no loop may add
  `--refresh` for it. An operator may still authorize a refresh explicitly with
  `--refresh --confirm-mismatch`, including while running `--mode auto`; that
  refresh is operator-originated and its `REFRESHED` event records
  `principal: OPERATOR`.
- `--status` is read-only and rejects being combined with any other flag,
  `--mode` included.
- `--slice` selects an active or pending slice; it cannot bypass required
  implementation or verification.
- `--target` is mandatory only while bootstrapping an unregistered mapping.
- `--legacy <module>` is repeatable and declares the legacy sources that
  converge on one target. With it the bare positional names the **target**
  module, not a legacy one. The set is sorted and deduplicated before it is
  persisted, so flag order never reaches the record, and it is fixed for the
  migration's lifetime exactly like `--mock`. Omitting it keeps today's
  behavior: the positional is the one legacy module and it becomes the record's
  single source. From format 15 the record directory and the module lock key on
  the target module, so `legacySources[0]` is alphabetically first and never
  "the" legacy module — read the whole set.
- `--adopt-target` declares that the target is already substantially
  implemented. It is refused unless `src/features/<target>/` exists, and it
  pins `inventories/target-baseline.json`: the target's committed revision plus
  every uncommitted path and its bytes, captured before the migration starts.
  Pre-existing work then cannot be claimed as slice work, and an
  already-implemented behavior can be recorded `ADOPTED_VERIFIED` — but only
  with a captured, hash-bound passing test run that names the row's scenarios
  and whose output literally names the spec files it executed. Existing code is
  a hypothesis; the bound run is the proof.
- `--registry` is accepted only before a project binding or migration state
  exists. Confirmed registration or migration execution persists the binding;
  omit the option thereafter.
- `--mock` selects `dataSourceMode: mock` at bootstrap; the default is
  `standard`. This choice is fixed for the migration's lifetime: passing
  `--mock` against a migration created as `standard` is rejected, but
  _omitting_ `--mock` on a migration already created as `mock` keeps it in
  mock mode rather than reverting to standard — the flag only ever matters
  at bootstrap, not on every subsequent resume.
- `--design-source target-system|figma-mcp|legacy-runtime` selects the visual
  authority at bootstrap; the default is `target-system` (current behavior).
  `figma-mcp` requires one or more `--figma <url>` links (`/design/` or
  `/make/`; FigJam and Slides are refused) and makes Figma the visual/UX
  authority. `legacy-runtime` makes the *running legacy app* the visual
  authority, refuses `--figma` links, and obliges ASSESS_TARGET to pin
  `inventories/legacy-runtime-context.json`. Under either, legacy stays
  authoritative for behavior, routes, and business rules and the target stays
  authoritative for architecture and design-system components. Like `--mock` it
  is fixed for the migration's lifetime: naming a different design source on
  resume is rejected, and omitting the flags resumes the recorded one
  untouched. See "Design source (Figma MCP)".
- Ponytail is opt-in. Bare `--ponytail` means `full`. Never enable Ponytail
  from provider or session defaults — its absence must always be the
  code-enforced default, not a documentation convention.
- `--refresh --confirm-mismatch` preserves authored artifacts, marks them
  invalidated, updates the pinned legacy revision, and reopens at
  `DISCOVER_LEGACY`. Use it only after a genuine legacy-side change has been
  reviewed and the user has decided parity must be recalculated — a target
  working-tree change, a model change, a provider change, or an interrupted
  session never justifies it.

## Legacy and target topology

The registry may point legacy and target at two different subtrees of the
_same_ Git repository. When it does, the pinned "legacy revision" is computed
from the last commit that actually touched files under the legacy root, not the
repository's overall `HEAD` — otherwise the migration's own target-side commits
would look like a legacy change and force a spurious `--refresh`. A brand-new
root with no commits touching it falls back to `HEAD` and is recorded as such.

## Contract compatibility and the explicit upgrade

One row per supported format, and the rows are bound to the engine's exported
constants by a contract test — the table cannot drift from the code.

| Persisted source       | Result                                                                                                                |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| contract 5, format 19  | active production creation default and supported ceiling; direct-ledger `STANDARD_LOCAL` decisions use explicit `AGENT_RELAYED` authority |
| contract 5, format 18  | remains readable/resumable with historical citation decisions and frozen `requiredObservations`; explicit 18→19 upgrade only |
| contract 5, format 17  | owes 17→18; DISCOVER_LEGACY may first validate and pin the legacy inventory, after which the upgrade freezes the lifecycle until it commits (see Format upgrades) |
| contract 5, format 16  | executes the full lifecycle with controlled same-slice rework and unclaimed-drift refusal at FINALIZE; never promoted to 17 |
| contract 5, format 15  | executes the full lifecycle with multi-source/brownfield targets; self-heals to 16 on the next advance                |
| contract 5, format 14  | executes with a recorded design source; self-heals forward                                                            |
| contract 5, format 13  | executes the full lifecycle with artifact-delegated shared prerequisites; self-heals forward                          |
| contract 5, format 12  | executes with UI verification; self-heals forward                                                                     |
| contract 5, format 11  | executes the full nine-checkpoint lifecycle with capability ownership; self-heals forward                             |
| contract 5, format 10  | executes the nine-checkpoint lifecycle it was born under, without capability ownership; never promoted to 11          |
| contract 5, format 4–9 | executes normally on the eight-checkpoint lifecycle it was born under; formats 4–8 self-heal to 9 on the next advance |
| contract 4, format 3   | refused, with the explicit upgrade command                                                                            |
| contract 2 or 3        | refused as unsupported; files are never touched                                                                       |
| newer than supported   | refused; update start-migration first                                                                                 |

Module default/active = 19; supported = 19. Artifact default/active = 14;
supported = 14, including delegated children. No pilot flag, signer or protected
policy is required. Existing records never silently upgrade: module 18 uses the
explicit pre-pin 18 -> 19 path; artifact 13 uses the explicit pristine 13 -> 14
adoption; non-pristine 13 records are never promoted. Artifact 14 direct-ledger
authority covers `ARTIFACT_DECISION` and `VISUAL_UNBACKED` only; not
`GROUP_APPROVAL`, and `EXCEPTION_RECORDED` is unchanged. The retained WebAuthn
signer provides optional protected `HUMAN_ATTESTED` authority; its deployment and
activation requirements never gate standard migration operation.

### Format bump policy

- **Additive and derivable** → self-healing. The feature has a default a record
  can satisfy by omission, so an older record simply behaves as that default and
  is stamped at the highest format whose vocabulary it actually uses. Formats
  12, 13, 14, 15 and 16 are all of this kind, and none introduces an upgrade
  command.
- **New authored artifact, or a new lifecycle step** → non-promoting. The record
  runs the lifecycle it was born under, for its whole life. Formats 10 (inserts
  the `DISCOVERY_COMPLETENESS` checkpoint, and `completedSteps` must remain an
  in-order prefix) and 11 (adds an *authored* capability matrix that cannot be
  computed after the fact) are the worked examples. Format 17 (authored Figma
  evidence and `matrices/visual-acceptance.json`) is the same kind: a format-16
  figma-mcp record keeps provenance-only visual semantics for its whole life.
  Format 18 (authored `requiredObservations` in the legacy inventory) is the
  same kind for a record *below* the floor: a pre-17 UI record stays readable
  and earns no new VERIFY_SLICES or FINALIZE PASS until it adopts them.
- **At or above the format-upgrade floor** → the engine's registered upgrader
  owns the increment. Nothing self-heals and nothing is skipped: the lifecycle
  freezes, the normal command reports the owed `N → N+1` transition, and the
  agent supplies only the input that transition names. See Format upgrades.
- **Format 19** changes decision authority and is non-promoting. An eligible
  unfinished 18 record may enter it only through an explicit journalled pre-pin
  adoption with preview/confirmation; otherwise keep historical citation rules
  or follow the typed `LEGACY_COMPATIBILITY_ACTION_REQUIRED` outcome. Ordinary
  advances do not promote 18 to 19.
- A record is never promoted into a feature it never ran, and a persisted
  version field is never hand-edited to route around a refusal.

A record runs the lifecycle it was born under. An older contract is refused
with an explicit upgrade command and is never converted implicitly; never
propose editing a persisted version field to route around that refusal. Full
transaction, recovery, rollback, and snapshot-retention rules:
`references/v5-contract.md`.

A `.agents/knowledge/migrations/modules/<module>.md` checklist is a retired
contract-2/3 workflow. Bootstrap refuses while one exists; never parse,
convert, move, or delete it — there is no automatic import path.

## Format upgrades

From the format-upgrade floor forward, moving a record's persisted
`formatVersion` is the engine's job, not the agent's. Never choose, name, or
type a format-specific transition; run the normal command and obey what comes
back.

| Engine | Floor | Registry |
| --- | --- | --- |
| module | `FORMAT_UPGRADE_FLOOR = 17` | active/default and supported 19; historical upgrade cursor stops at 18, with 18→19 only by explicit eligible adoption |
| artifact | `ARTIFACT_FORMAT_UPGRADE_FLOOR = 13` | active/default and supported 14; explicit pristine 13→14 upgrader; existing 13 records stay historical |

Below the module floor nothing here applies: formats 4–16 keep their existing
compatibility behavior (self-healing where the bump was additive, running the
lifecycle they were born under where it was not), and the pre-17 one-shot
adoptions remain the only way such a record reaches 17 or 18. Formats 4–16 were
never retrofitted into adjacent upgraders.

### The one protocol

```text
normal migration invocation                     (/start-migration <module>)
  -> engine detects the owed N -> N+1 increment
  -> if INACTIVE, continue old-format lifecycle until its prerequisite is pinned
  -> then the increment becomes ACTIVE
  -> the normal lifecycle freezes; no checkpoint, slice or decision may move
  -> engine reports a typed FORMAT_UPGRADE target
  -> supply ONLY the authoritative input that target requests
  -> rerun the SAME normal migration command
  -> engine commits exactly one increment      (FORMAT_UPGRADED)
  -> obey the emitted `loop: CONTINUE next=<command>` literally
  -> the later invocation continues upgrades, or resumes the lifecycle
```

One increment per upgrade invocation, always. The engine never jumps or
promotes an owed increment through ordinary lifecycle progress. Owed does not
automatically mean frozen: only an ACTIVE increment is exclusive.

### The typed `formatUpgrade` result

`migration_status` and active-upgrade preflight carry a structured `formatUpgrade`
(`null` for a module record at 18 or 19, unless explicit adoption was selected), reporting `recordFormat`,
`runtimeFormat`, `from`/`to`, `upgrader {id, version}`, `active`, `state`,
`prerequisite`, `domain`, `requiredInput`, `blockers` and `nextAction`. Read that object; do not
rediscover which transition is required.

- `INACTIVE` (`active: false`) — the old-format `activation.prerequisite` has
  not yet been validated and pinned. Status names it read-only; normal lifecycle
  execution continues until it produces that authority. The format stays put
  and no `FORMAT_UPGRADED` event is written.
- `NEEDS_INPUT` — the increment's declared input is absent. Author exactly the
  artifact `requiredInput` names, at the path it names, from the authority it
  names. Nothing was written.
- `BLOCKED` — the input exists (or the record's authority cannot be read) and
  the upgrader refused it. Relay `blockers` verbatim. Nothing was written.
- `READY` — the increment can commit. `domain: "TRANSFORM"` means the record
  needs the upgrader's domain work; `domain: "NO_OP"` means it does not and
  `requiredInput` is `null`. Both commit one atomic increment; neither is
  skipped. Do not invent work for a `NO_OP`.

`activation.prerequisite` is old-format authority needed before the upgrader
becomes active; `requiredInput` is new material requested by an already-active
upgrader. For 17→18, DISCOVER_LEGACY validates and pins
`inventories/legacy.json`; its bootstrap scaffold is not authority. Once that
pin exists, 17→18 is ACTIVE even if the file later goes missing or corrupt, and
the upgrade blocks while the lifecycle remains frozen.

For the module engine's active 17→18 increment the required input is
`ui-observations-adoption/candidate/legacy.json`, with `authority: "legacy"`:
author it from **validated legacy authority** (the record's pinned legacy
inventory and legacy runtime/source evidence) plus the **pinned
requirements/OpenSpec authority**. TARGET proof is never authority for
`requiredObservations` — a Playwright capture of the new implementation proves
the target does something, not that legacy required it. Read only the paths and
evidence the `formatUpgrade` result names. A record whose validated legacy
authority declares no visible UI needs no candidate at all: that increment is
classified `READY`/`NO_OP` and the engine commits it on its own.

### Status and loop contract

- `FORMAT_UPGRADE` — an ACTIVE increment cannot commit yet. The migration
  lifecycle is frozen: every advance, reopen, rework, amendment, slice-state
  repair and decision recording refuses while it is active, and the checkpoint
  tuple does not move. STOP until the required input or the blocker is
  resolved. Exit code is the blocked code and the directive is
  `loop: STOP reason=FORMAT_UPGRADE`.
- `FORMAT_UPGRADED` — exactly one increment committed, in one journalled
  transaction, with one canonical `FORMAT_UPGRADED` history event. No migration
  checkpoint advanced in that invocation. The directive is
  `loop: CONTINUE next=<the normal command>` — an executable front-end command,
  never an internal state token. Re-invoke exactly that command; do not
  substitute a format-specific one, and do not stop to ask.

INACTIVE status prints `FORMAT UPGRADE PENDING` with a live normal checklist and
does not set a stopping `FORMAT_UPGRADE` outcome. ACTIVE status prints
`FORMAT UPGRADE REQUIRED` above the frozen normal checklist. Reading status
never mutates: it writes no state, adopts no toolkit
identity, and leaves `revision`, `formatVersion` and history untouched.

### Historical compatibility surfaces

`--adopt-visual-contract`, `--adopt-ui-observations` and
`--confirm-adopt-ui-observations <digest>` are **pre-floor compatibility and
admin surfaces only**: the one-shot path by which a record *below* format 17
reaches the visual contract or the observations contract. They are not part of
normal operation, and a record already at format 17 must never be driven with
them — the engine's registered 17→18 increment owns that transition and the
normal command dispatches it automatically. `references/migration-contract.md`
holds the full pre-floor rules.

## Pre-execution confirmation

Except for `--status`, every invocation runs a read-only preflight first. It
never creates directories, modifies files, or advances state — it only prints a
summary and, when the action is executable, an opaque confirmation ID that
authorizes that single action and expires the instant any bound input moves.

A fresh migration bootstraps through `artifact-migration-discover`, in two phases:
`run` neither carries the OpenSpec proposal nor accepts `--confirm-execution`.
For a fresh migration whose OpenSpec file is absent, inspect enough legacy
evidence to draft the real capability requirements, keep that proposal in
memory, and pass the same bytes to both helper calls through the internal
`--openspec-proposal-stdin` option. The helper validates the proposal and shows
its SHA-256 digest during preview; the digest is part of the confirmation ID.
Do not write a temporary/placeholder spec or restore a deleted one manually.

The design source is a bootstrap input, collected with the others. It defaults
to `target-system` — the target project's own design system — and a bootstrap
that named no `--design-source` takes that default without asking. Only
`figma-mcp`, which makes Figma authoritative for visual/UX intent, needs the
user, and only because a Figma link is a value you cannot supply yourself: when
the request asks for Figma but carries no link, ask in one exchange for one or
more design links (`/design/` or `/make/`). `target-system` needs none and is
never asked for one. Settle both before the first preview call: they are bound
into the confirmation ID, so naming them afterwards only invalidates it.

Pass every link the user gives unmodified, one `--figma` value each. Never
invent, guess, complete, shorten, or parse a Figma URL — the engine is the only
Figma URL parser; relay its refusal verbatim and ask again.

Never ask for a value the invocation already carries, never on a resume, and
never for a value that has a default: status comes first, and a bootstrap-fixed
input is never re-requested once state exists.

Under `--mode step`, relay the summary to the user and wait. Treat only an
explicit affirmative reply (`Yes`, `Sí`, `Proceed`, `Continue`) as approval; a
negative, absent, conditional, or ambiguous reply must not authorize execution
— ask again without writing anything. After approval, rerun the identical
helper call with `--confirm-execution <id>`, an internal agent-to-helper option
the user never needs to see, type, or understand.

A confirmed bootstrap ends with the same `loop:` line an iteration ends with,
and it is obeyed the same way. Never decide from this prose whether the first
iteration runs.

## Resume after interruption

Persisted state is the source of truth across conversations, models, and
providers. On any new session, a bare `/start-migration <module>` continues
from the saved artifact — never add `--refresh`, recreate a slice, overwrite
authored evidence, or restart discovery merely because the previous session
used another model or stopped unexpectedly.

An interrupted `--mode auto` loop is an interruption like any other. Having
been driven autonomously is never a reason for `--refresh`, for recreating an
artifact, or for restarting discovery.

Never hand-edit `state.json` — not its navigation fields, not its artifact
hashes — and never truncate `history/history.ndjson`. Resume replays history
against state and blocks on any mismatch with a named reason.

## Mock data-source intent

`--mock` persists `dataSourceMode: mock`, recording a requirement for the
slice that owns the target data boundary — it does not prescribe an
environment-variable name, framework, repository factory, or fallback.
Inspect and follow the target project's existing data-source conventions;
introduce no shared resolver or configuration abstraction the target
architecture doesn't already require.

## Stop conditions

A stop condition is the only reason a loop ends; advancing a checkpoint,
finishing a slice, moving `IMPLEMENT_SLICES` -> `VERIFY_SLICES`, or starting
slice N+1 is not one. Never end a run because the work "feels" like a natural
stopping point, because a checkpoint just succeeded, or because a session
boundary would be tidy. Every stop condition but one is structural and
arrives as a typed stop reason on the `loop:` line.

**The one stop condition no command can detect**: a validation fails in a way
you cannot fix from the recorded evidence. That returns `CONTINUE` with the
validator's message, and re-authoring the same wrong artifact returns it again.
Stop and hand back rather than looping.

## Progress presentation

The engine owns migration progress. Every command that touches a record hands
it back already computed: `migration_status` returns `progress` (the canonical
projection) and `progressChecklist` (that same projection rendered as text),
and `migration_run` returns both on every outcome. Display one of those.
Never derive displayed progress from source files, changed files, git state,
test results, or conversation memory.

The tool output already shows progress: every `migration_run`,
`migration_status` and `artifact_run` result starts with a plain-text status
line and the checklist, and the CLI prints them (to stderr under `--json`).
You still render the full checklist at start, on resume and at stop.

Render progress at two moments, in this order, every iteration:

```
/start-migration <module>
  -> migration_status  -> render canonical progress
  -> migration_run     -> render canonical progress
  -> repeat
```

### Native task UI, or the text fallback

Where the provider has a stable native task/progress surface (OpenCode todos,
Claude Code's todo list, the equivalent Codex or Copilot surface), map
`progress` into it — one row per `checkpoints[]` entry, and nothing else:

- the row label is `<index>/<total> <name>`, the engine's checkpoint name,
  never a paraphrase;
- the row state is that entry's `state`: `COMPLETED`, `ACTIVE`, `PENDING` or
  `BLOCKED`;
- rows keep the engine's order — never sort, filter, merge, rename or add;
- while `IMPLEMENT_SLICES` or `VERIFY_SLICES` is active, list `slices.items[]`
  beneath that one row using the same four states. Slices are detail under a
  checkpoint, never a replacement for the checkpoint rows themselves.

The checkpoint rows are whatever `checkpoints[]` contains for this record —
read the array, never a list you remember. Visible-UI verification is sub-work
inside those checkpoints (`DISCOVER_LEGACY` inventories the UI behaviors,
`ASSESS_TARGET` and `PLAN` trace them, `VERIFY_SLICES` proves them per slice,
`FINALIZE` gates them), so where `uiEvidence.applicable` is true, show
`uiEvidence` as detail beneath those rows and never as an extra checkpoint.
It is `null` on a `migration_run` projection, which has not read the evidence;
that is an absence to leave blank, not a value to infer.

Where the provider has no such surface, or it is unavailable, relay
`progressChecklist` verbatim inside a fenced code block. The fallback always
works, and a native surface is never required to execute a migration.
Different rendering is allowed; different progress is not.

Never reformat, re-order, translate, summarize, add emoji to, or add
percentages to either form. A record born before the `DISCOVERY_COMPLETENESS`
checkpoint renders eight rows, not nine; that is correct, not a missing
checkpoint.

### Never author a migration plan

While this skill is active the user-facing progress is the engine projection
and nothing else. Do not build, and do not show, a task list of your own —
"inspect migration state", "analyze implementation", "author remediation",
"modify files", "run validation", "report status". Those may be how you reason
and act; they are not migration progress, and showing them as progress is
exactly how two providers end up disagreeing about one record. This overrides
any general instruction to open a task list before multi-step work.

A progress row is a display, never a control. No task item, checkbox or todo
may approve a candidate, close a checkpoint or advance a slice. Operator
approval for historical formats uses their elicitation/terminal challenge;
module 19 requires its trusted policy and verified ledger, with attested writes
unavailable; authorization is never through a model-callable affordance. After a decision is
persisted, re-read `migration_status` and re-render; do not edit the rendered
progress in place.

A blocked record shows the block where it happened: the active checkpoint
carries state `BLOCKED`, and `stopReason` and `blocker` are relayed with the
engine's own wording.

### Canonical progress, and current activity

Two different things, and they are never mixed:

- **Canonical progress** is the engine projection above — `progress`,
  `progressChecklist`, `checkpoints[]`, `slices.items[]`, `stopReason`,
  `blocker`, `nextWork`. The engine owns it, and it is the only account of where
  the migration is.
- **CURRENT ACTIVITY** is one transient line naming the operation in flight:
  `CURRENT ACTIVITY: Opening legacy roles route`, `CURRENT ACTIVITY: Running
  target verification`, `CURRENT ACTIVITY: Verification still running`.

An activity line is presentation and nothing more. It never becomes a
checkpoint, never becomes `progress`, never writes `state.json`, never implies
completion, and never carries a percentage. It is not the task list the previous
section forbids either: one line about the current operation, not a plan. It
holds no lifecycle authority, so after an interruption it is simply gone and the
next iteration re-renders canonical progress from the engine — keep no activity
log, no provider checkpoint, and no second record of migration position.

### Cooperative yielding during long work

Canonical progress for the current iteration is presented first. Then, before
each operation that does real work, print one CURRENT ACTIVITY line and invoke
only bounded work, so control returns to the provider between operations.

Work you expect to exceed roughly 10–15 seconds is never held open as one
foreground call. Where the host supports it, start it in the background, return
control, then poll with separate bounded calls, printing CURRENT ACTIVITY
between polls at roughly a 5-10 second cadence until it finishes. Then cross the
engine boundary as usual: `migration_run` or `migration_status`, canonical
progress, then the `loop:` line.

This is not a shell rule. It applies to any long operation — a verification
command, a test run, a build, a long scan, an external process, a long engine
CLI call. Short operations return normally: an ordinary `browser_*` call, a file
read, or a quick engine call needs no background process, and manufacturing one
is noise.

Routine continuation stays automatic, exactly as "Loop directive and handoff"
requires: `loop: CONTINUE` runs in the same session without asking the operator
to say "continue", and polling a background operation is not a stop condition.
Only a typed stop ends the loop, and the decisions that need a human still need
one — yielding between bounded calls never stands in for operator approval.

### Live-progress capability per provider

| Provider       | Live-progress mode | ≤15s visible-silence ceiling |
| -------------- | ------------------ | ---------------------------- |
| Claude Code    | cooperative-yield  | proven                       |
| OpenCode       | cooperative-yield  | proven                       |
| Codex          | best-effort        | not-proven                   |
| GitHub Copilot | best-effort        | not-proven                   |

`proven` means a real interactive host was observed holding visible silence
under 15 seconds across a long background operation; on those two providers,
hold that ceiling. `not-proven` means no such observation exists: execute the
same contract as far as the host allows, but never tell the operator that live
progress is guaranteed there, and never present the 15-second ceiling as one.
Canonical progress is correct on all four the moment control returns; only the
liveness of the intermediate activity differs. The same two values are declared
machine-readably as `liveProgress` in `providers/<provider>/adapter.json`, which
is provider capability, never migration state.

## Checkpoints

Full JSON schemas for every artifact below live in
`references/migration-contract.md`; this is only the per-step trigger.

1. **`RESOLVE`** — resolve module, target, roots, legacy revision, OpenSpec
   identity, brief, data-source mode, and Ponytail option. Invalid names,
   paths, target conflicts, or stale revisions stop without overwriting
   authored evidence.
2. **`DISCOVER_LEGACY`** — inspect the complete legacy surface (routes,
   transitions, permissions, APIs, edge cases, cross-module coupling) and
   assign every behavior and route flow a stable ID with concrete evidence.
   Before closing, declare the physical module roots in
   `inventories/module-classification.json`; the canonical scanner verifies
   every legacy evidence location is `OWNED`, typed `SUPPORTING`, an
   `INBOUND_CONSUMER`, or `GOVERNING_FRAMEWORK`. Shared configuration never
   becomes owned merely to make evidence resolve. Full coverage categories:
   `references/discovery-checklist.md`. Complete
   `steps/02-discover-legacy.md` and `inventories/legacy.json`.
3. **`DISCOVERY_COMPLETENESS`** — prove the inventory is complete, not just
   internally consistent. Recompute the canonical boundary with the explicitly
   recorded scanner version and revalidate every legacy evidence citation;
   roots and entry points remain editable until this checkpoint closes. Give
   every file the census finds under the final declared roots exactly one
   row in `inventories/module-classification.json` with a closed-enum
   disposition — including files nothing imports. `--scan` prints the
   recomputed census, graph, and findings to author against. A
   production-reachable component, style, image, SVG, or other visual asset is
   never dismissed on agent-authored rationale: it is `BEHAVIOR_BACKED` or
   `EXCLUDED_APPROVED` with a decision authorized under the record's policy. That
    happens one decision per iteration. Module 19 validates a policy-bound
    decision directly against the verified ledger; no challenge or receipt
     fields are authored in classification version 2. `STANDARD_LOCAL` requires
     explicit `AGENT_RELAYED` approval; only protected high-assurance policy
     requires a signer and blocks without one. Historical
    module formats ≤18 instead retain the terminal/elicitation challenge and
    require the cited `decisionId` and `decisionDigest` in the classification
    row after recording. A stale decision cannot authorize the current candidate.
    Non-literal module edges also require
   concrete tracked targets; prose and approval never substitute for a target.
   `new URL(expr, import.meta.url)`, safe immutable aliases, and nested module
   URL bases are module-resource edges. Proven HTTP/runtime URLs are recorded
   but nonblocking; unknown or mutable bases block as module-resource findings.
   I18n namespaces, JSON, CSS, assets, and framework runtime resources are
   typed supporting relations with exact edge evidence, not extra owned roots.
   If the fix belongs in `inventories/legacy.json`, `--reopen-discovery`
   returns to `DISCOVER_LEGACY` for one revision without invalidating
   anything else. Complete `steps/02a-discovery-completeness.md`.
4. **`ASSESS_TARGET`** — inspect the target independently, even where a
   route/feature/test already exists; classify it `ABSENT`, `PLACEHOLDER`,
   `PARTIAL`, `INCOMPATIBLE`, or `IMPLEMENTED_UNVERIFIED`, and record every
   visible control's actual component versus the target design-system
   equivalent. Complete `steps/03-assess-target.md` and
   `inventories/target.json`.
5. **`BUILD_BASELINE`** — build the five baseline matrices (behavior parity,
   route adaptation, target-native, design-system usage, capability
   ownership). Every legacy behavior/route ID appears exactly once; target
   existence is never parity. Merging an independently-reachable legacy
   list/detail into one target window is a `NAVIGATION_FLOW_GAP` unless
   explicitly `REDESIGNED_APPROVED` with an acceptance scenario. Also classify
   every capability the module requires in
   `matrices/capability-ownership.json` as `TARGET_REUSE`,
   `SHARED_PREREQUISITE`, `FEATURE_LOCAL`, or `DO_NOT_MIGRATE`, from legacy
   evidence, target evidence, and architecture authorities — the supporting
   relations the discovery scan already computed are the candidate set. A
   capability missing from the target is never rebuilt inside the feature when
   other features provably consume it: that is a `SHARED_PREREQUISITE` whose
   `targetOwner` must be outside `src/features/<target-module>/`. Shared
   ownership is proven by at least two other consumers, never assumed, so most
   capabilities stay `FEATURE_LOCAL`. At format 13 each shared prerequisite
   carries `artifactMigration: {source,type,target}`; the source and target are
   bound to the module roots and the target stays under `targetOwner`. A cited architecture authority must
   exist; a missing one is recorded in `authorityGaps` instead of invented
   around. Register the mapping only after this validates.
6. **`PLAN`** — divide the baseline into bounded slices. Each slice records
   _disjoint_ ID lists — `requirementIds` (OpenSpec requirements),
   `scenarioIds` (OpenSpec scenarios), `traceIds` (baseline matrix rows),
   `capabilityIds` (capability-ownership rows) — never mixed, and never
   sourced from `acceptanceScenarios` prose. Every non-terminal baseline row,
   including every target-native row not yet `PRESERVED`, belongs to exactly
   one slice's `traceIds`; every `SHARED_PREREQUISITE` and `FEATURE_LOCAL`
   capability belongs to exactly one slice's `capabilityIds`. A shared
   prerequisite need not be _implemented_ before `PLAN` closes, but it must be
   scheduled: a slice that builds one is declared before, and listed in the
   `dependencies` of, every slice that follows it — for example
   `shared-001 → roles-001 → roles-002`. Run the target's architecture review
   process and record its verdict as evidence for `ARCHITECTURE_PLAN_GATE`;
   the review itself must not change state.
7. **`IMPLEMENT_SLICES`** — implement only the active slice, using target
   routing and required design-system components. A slice owning a
   `SHARED_PREREQUISITE` delegates to its bound artifact migration first. The
   artifact record owns its lifecycle and evidence; the module records no copy
   of child state. The converse also holds: the artifact engine owns only its
   lifecycle, its inventories, its gates and its own format axis, and imports
   shared policy, locking, safe paths, atomic writes, decision recording,
   progress projection and loop directives from this engine's core. Neither
   side reimplements the other's rules — see
   `migrate-artifact/SKILL.md` *Responsibility boundary*. A non-delegated historical shared slice must still change at
   least one file under `targetOwner`. Record `slices/<slice-id>.json` with changed files,
   decisions, checks, and `implementationStatus: COMPLETE`. Every file you changed must be in its
   `changedFiles`; the engine lists any you missed (`SLICE_FILES_UNLISTED`) — add them, or revert them.
8. **`VERIFY_SLICES`** — verify only the active slice: execute its
   acceptance scenarios and affected tests, covering entry, transitions,
   URL/history semantics, and terminal outcomes. Record
   `evidence/<slice-id>/result.json`. A slice that owns visible UI behavior
   also records Playwright runtime evidence for every required state and
   interaction (see "Runtime UI evidence"). When all slices pass, advance to
   `FINALIZE`.
9. **`FINALIZE`** — recheck the _entire_ migration, not just the last
   slice: every behavior/route/target-native/design-system row terminal,
   provenance clean of copied legacy code, and all seven mandatory gates in
   `gates.json` `PASS` with fresh, bound evidence (see "Gate evidence" in
   `references/migration-contract.md`). `FUNCTIONAL_PARITY_GATE` can never
   be `NOT_APPLICABLE`. A Ponytail target requires the owning gate rows to
   carry typed evidence (`kind`/`reference`), never prose. Advance to
   `COMPLETE`, then run `artifact-migration-validate <module> --complete`.
   `COMPLETE` means ready for commit — it never commits, pushes, or opens a
   pull request itself.

## Evidence must resolve

Evidence is not accepted as an arbitrary string. Any evidence reference that
names a path with a file extension — in the legacy inventory, the target
inventory, a baseline row's `legacyEvidence`/`targetEvidence`, or a gate's
`reference` — must resolve to a file that exists under the legacy or target
repository; a trailing `:12-40` line locator and trailing prose are ignored.
A slice's `changedFiles` must resolve to files that exist and are inside the
target repository. When a gate's `reference` resolves to a real file, its
`hash` must equal that file's current SHA-256; a fabricated digest, a deleted
reference, or a mutated one fails `FINALIZE` without advancing state.

Prose evidence remains legal where the contract allows it, so this adds no
authoring burden — it only makes an invented path impossible to record.

## Blockers

Record a blocker only when a required decision, permission, environment, or
external dependency prevents the current checkpoint — never invent
implementation to avoid one.

## Loop directive and handoff

Every iteration, and every confirmed bootstrap, ends with one machine-readable
line:

```text
loop: CONTINUE next=/start-migration <module>
loop: STOP reason=AWAITING_CONFIRMATION | COMPLETE | OPERATOR_DECISION | BLOCKED | FAILED | FORMAT_UPGRADE
```

That line, not the prose around it, decides whether another iteration runs.
Obey it literally. A command that exits non-zero without printing one has
already failed and stops the loop; `--mode step` prints none at all, because
the operator drives every iteration there by hand.

On `CONTINUE`, run exactly the command `next=` names, in the same session. Do
not emit a handoff block, do not print a `Next command:` line, and never ask
the operator to say "continue" — a successful checkpoint or slice advance is
not a stopping point.

A committed format increment continues through that same line:
`FORMAT_UPGRADED` prints `loop: CONTINUE next=/start-migration <module>`, so
the next iteration is a fresh normal invocation and no agent decision sits
between them. `next=` always names a command a front end can execute; it is
never a state token, so there is no `next=FORMAT_UPGRADE`. An *owed* increment
stops instead, with `reason=FORMAT_UPGRADE`.

On every iteration, render canonical progress (see Progress presentation).
On `STOP`, follow it with:

```text
Migration: <module>
Mode: <auto|step>
Completed checkpoint: <step>
Completed slice: <id-or-none>
Evidence saved: <paths>
Current blockers: <none-or-list>
Stop reason: <the typed reason from the directive>
Next checkpoint: <step>
Next artifact: <path>
Resume command: /start-migration <module>
```

## Runtime UI evidence (Playwright MCP)

Only for `hasVisibleUi: true`. When it is `false`, UI runtime evidence is
`NOT_APPLICABLE` and Playwright is not used at all.

Use the repository's already-registered `playwright` MCP server (`.mcp.json`,
`@playwright/mcp`) through its `browser_*` tools. Do not add a second browser
automation stack, and do not write a bespoke runner.

Each `TARGET` PASS row references a `playwright-ui-proof/v1` JSON observation
(structured role/name/state per control, engine-evaluated `presence`,
`visibility`, `text`, `value`, `count` and `url` assertions, and an `action` plus
`postAction` observation per interaction); a hash-valid log is never proof. A
completed slice verified on older evidence is recovered with `--reopen-ui
<slices>`, legal on `COMPLETE` and on `ACTIVE` at `VERIFY_SLICES`/`FINALIZE`
(completed slices only). See `references/migration-contract.md`.

Playwright is an evidence provider, never a second migration engine. It decides
nothing: the engine owns which behaviors are required, whether evidence is
stale, and whether a checkpoint passes. Ask the engine first
(`--status` / `migration_status`, then `nextWork`), and capture only what the
current checkpoint is missing.

- `DISCOVER_LEGACY` — observe the legacy runtime to author the interaction
  inventory: hierarchy, visible controls, table/list structure, search,
  pagination, actions, menus/dialogs, conditional and permission-dependent
  visibility, loading, empty, error, responsive and density behavior where it
  is behaviorally meaningful. Record the exact configuration
  (`showToolbar: false`, `showPagination: false`, `compactMode: true`), not
  "a table exists". Discovery is not blocked when the legacy app is offline —
  author from source and record the gap.
- `VERIFY_SLICES` — drive the target runtime and assert observable behavior:
  the required control exists, the action exists, search filters, pagination
  moves, visibility and permission rules hold, navigation works, the
  dialog/menu opens, loading/empty/error render. Screenshots supplement those
  assertions; they never replace them.

Capture protocol, per required UI behavior:

1. `browser_navigate` to the route, `browser_resize` to the slice viewport.
2. `browser_snapshot` for the accessibility structure — that is the assertion
   surface, not the picture.
3. `browser_click` / `browser_type` / `browser_select_option` for each declared
   interaction; record `expected` (from discovery) and `actual` (observed).
4. `browser_take_screenshot` once per state, into
   `evidence/<slice-id>/ui/`.

Budget: one screenshot per origin/behavior/state, no duplicate digests
_within an origin_ (identical legacy and target captures are parity, not a
duplicate), one viewport per slice unless the behavior is `RESPONSIVE` or the
state is `DESKTOP`/`MOBILE`. Every `reference` must be a file you actually
wrote, hashed: a runtime claim with no artifact is refused.

Never re-capture on a plain `CONTINUE`; reuse persisted evidence unless the
engine reports it stale.

Never persist a password, token, cookie, authorization header, or any other
credential into evidence — the engine refuses it. Verify read-only; if a
mutation must be exercised, use disposable fixture data, never real business
records.

If the runtime is unreachable, record the reason as a
`uiEvidenceLimitations` entry with `availability: "NOT_AVAILABLE"`. That is not
a waiver: verification still refuses, and the unresolved requirement goes
through the ordinary blocker/operator-decision contract. Never author a PASS
you did not observe.

Full schemas: "Visible-UI verification" in `references/migration-contract.md`.

## Design source (Figma MCP)

Only when the migration was bootstrapped with `--design-source figma-mcp`
(`designSource: figma-mcp` in state). The default `target-system` uses no Figma
and this section does not apply. Both the source and its links are collected
from the user at bootstrap, before the first preview — see "Pre-execution
confirmation".

Figma is an evidence/context provider, exactly like Playwright — never a second
migration engine, and never reached by the migration core. The engine validates
links as pure strings and pins the design context's digest; the coding agent is
the one that calls the Figma MCP, exactly as it drives `browser_*` for runtime
UI evidence. Do not add Figma-client code to any migration script, and do not
hardcode a specific Figma MCP server prefix or tool namespace — use whichever
Figma MCP the host/runtime exposes, per the repository's Figma skill.

Authorities stay orthogonal:

- **Legacy** stays authoritative for behavior, business rules, data flow,
  routes, and permissions. Figma is never consulted at `DISCOVER_LEGACY`.
- **Figma** is authoritative for visual/UX intent: layout, spacing, states,
  iconography, and copy-as-designed. A legacy behavior the design omits stays
  required; a design that conflicts with a required behavior is an operator
  decision, not an agent dismissal.
- **Target** stays authoritative for architecture, routing, and which
  design-system component realizes a frame. A Figma element with no target
  component is a `DESIGN_SYSTEM_GAP`, exactly as today.

Lifecycle:

The pipeline (format 17): Figma MCP → persisted canonical node evidence →
pinned design source → derived visual-acceptance contract → implementation →
Playwright runtime measurements and screenshots → deterministic engine
comparison → PASS/FAIL.

- `ASSESS_TARGET` — prefer the official structured `use_figma` Plugin API read.
  Persist each node's returned JSON snapshot bytes without rewriting them,
  including the root and relevant descendants. Record each node's id,
  SHA-256 digest, `use_figma` operation/parameters/timestamp, and its
  `parentId`/`childIds`. Persist `get_metadata` to cross-check ancestry,
  `get_screenshot` at the frame's full dimensions, and official downloaded
  assets with export kind, MIME type, bytes and digest. A structured frame's
  `sources` adds `structuredNodes[]` and `assets[]`; its `authority` is
  `{versionPinned:false,versionSource:"none",authorityDigest}`. The pinned
  snapshot is the authority; resume and FINALIZE re-derive it without a live
  Figma refresh. The screenshot `capture` records `requested`, `returned`,
  `frameBox`, and `compare`; returned dimensions must equal the frame box or
  an exact integer multiple. Use `get_metadata`, `get_design_context`,
  `get_variable_defs`, and `get_screenshot` as the classic fallback when the
  Plugin API is unavailable.
  Persist each output **verbatim** under `inventories/figma/<node>/` — hierarchy,
  dimensions, positions, visibility, components/variants, text, typography,
  Auto Layout, fills, strokes, radius, opacity, effects, tokens, and assets live
  there, never in a summary. When `get_design_context` is too large, split it
  over child nodes (`designContext` is a list). Author
  `inventories/figma-context.json`: per frame `fileKey`, `nodeId` (a recorded
  link's node), `name`, `type`, `viewport` (the node's size, which the engine
  reads back from the persisted metadata), `states`, `extraction`
  (`retrievedAt`, `fidelity: COMPLETE | DEGRADED`, `limitations[]`), and
  `sources` `{ metadata, designContext[], variableDefs, screenshot }`, each
  `{ reference, hash }` on the classic path. The engine pins the context when `ASSESS_TARGET`
  closes and re-hashes every persisted source at each verification.
- `BUILD_BASELINE` — derive `matrices/visual-acceptance.json` from that
  evidence at `"version": 2`: structured frames use `frame.nodes[nodeId] =
  {facts,targetLocator}` and each acceptance row uses `nodes[nodeId] =
  {targetLocator,expect}`. Include every source-established fact on its owning
  node, directional padding and corners, the node's `stroke` record and
  `boxShadow` component list (present or empty — never the raw Figma paint or
  effect array), and
  nonempty asset ids for an asset-bearing subtree. The engine derives the
  complete set and refuses omission, unsupported values, or wrong-node claims.
  The classic fallback retains one row per required UI behavior state with
  `figmaNodeId`, `figmaState`, the frame `viewport`, and an `expect` set that
  covers the **full visual taxonomy** — `width`/`height`, `padding`/`gap`,
  `color`/`backgroundColor`, `fontFamily`, `fontSize`, `fontWeight`,
  `lineHeight`, `borderWidth`/`borderColor`/`borderRadius`, `boxShadow`,
  `opacity`/`visibility`, `assets`, at least one bounded `count`, **plus every
  fact the authority frame establishes** — each with the `locator` Playwright
  measures. A count declares `value`, or both `min` and `max`. Tolerance is
  **fixed at ±1px**: authoring a `tolerance` is refused. Every value is compared
  after normalization, so a Figma `#0B5FFF` and a browser `rgb(11, 95, 255)` are
  one fact; a value no normalization can place (`rem`, `em`, a named colour) is
  refused rather than guessed at. `"version": 1` remains readable only for a
  record that pinned it before version 2 existed, and is never a certification
  path a new record may choose.
  The row is the only binding of a state to
  Figma; nothing is inferred from frame names or states. A state with no row
  goes under `unbacked` with its reason. Module 19 resolves `VISUAL_UNBACKED`
  directly from the verified ledger; module formats ≤18 require a cited
  historical decision. A state with a row can never be unbacked. A DEGRADED frame cannot back a row and
  is not absence of design. Pinned.
- `VERIFY_SLICES` — each Figma-backed `origin: "TARGET"` row carries
  `figmaNodeId`, the contract `viewport`, a runtime `screenshot`, and
  `measurements` `{ reference, hash[, pointer] }` naming the persisted Playwright
  observation file (`{ viewport, nodes: { [nodeId]: { targetLocator,
  parentNodeId?, values } } }` for structured frames, `{ viewport, values }`
  for classic frames), measured with
  `getBoundingClientRect`/locator counts and computed styles). A `stroke` value
  is the node's computed `border*`/`outline*`/`box-sizing` declaration and a
  `boxShadow` value its computed `box-shadow` string; the engine normalizes
  both sides into the same record, so never hand it Figma's own JSON. The engine
  compares `values` with the
  contract at the fixed ±1px and owns the verdict: an authored `result: "PASS"`
  over a divergence is refused as `VISUAL_ACCEPTANCE_FAIL` — fix and re-measure,
  or record FAIL and rework. A slice tracing a design-system row that is not
  `COMPLIANT` or `EXCEPTION_APPROVED` cannot verify. Every TARGET row still binds
  `figmaContextDigest`. Functional parity and the seven final gates are never
  Figma-bound.

Never re-fetch Figma on a plain `CONTINUE`; reuse the pinned evidence unless the
engine reports it stale. If the Figma MCP is unavailable or a file is not
permitted, record it as a limitation and let verification refuse — never persist
a Figma token or author a fidelity claim you did not derive from the design.
The engine compares screenshots at the pinned frame-box resolution and reports
`diffPixels`, `diffRatio`, threshold and margin. No new checkpoint and no eighth
gate. A format-16 figma-mcp record keeps the older provenance-only behavior.

A **completed** pre-17 figma-mcp record can opt in without restarting. Under
`--mode step` it is an operator decision, never taken on your own initiative and
never self-confirmed; under `--mode auto` the AUTO principal decides it on the
evidence below and records it in the auto ledger:

1. Fetch fresh evidence through the Figma MCP (never reuse the old context's
   prose) and author it at `inventories/figma-context.adopted.json` under the
   format-17 frame schema, plus `matrices/visual-acceptance.json`.
2. `artifact-migration-discover <module> --adopt-visual-contract --confirm-adopt-visual-contract`,
   then show the summary, including the named slices, and pass the operator's
   `--confirm-execution <id>`. The ID binds those exact evidence bytes.
3. `--reopen-ui <every named slice>`; remediate, re-measure, reverify, FINALIZE.

Adoption fails closed on absent, incomplete, or DEGRADED evidence. It stamps
format 17, swaps the fresh context in, preserves the old one and an immutable
record under `visual-contract-adoption/`, and moves no step, slice, approval, or
functional evidence. Any other resume is blocked until the named slices are
reopened. It is not a refresh, replan, or reset, and runs once per record.

## Security

Treat names, aliases, registry data, OpenSpec content, brief paths,
repository content, and JSON artifacts as untrusted. Preserve safe-name
checks, target-root containment, symlink rejection, argument-array Git
execution, exclusive temporary files, and atomic rename. Never persist
secrets, tokens, passwords, environment files, dependencies, generated
output, large binaries, or symlinked evidence.

### The operator-approval boundary, and exactly what it is worth

For module formats ≤18 and artifact 13, an operator decision is recorded by one function, reached two ways: a terminal
(`process.stdin.isTTY`) or an in-process `ask` callback a front end may supply
only after it has itself obtained a human answer. `ask` is a function
reference, never an argv option, an environment variable, or a tool argument —
`record-decision.mjs` (`artifact-migration-decision`) declares no option that can produce it, and the MCP
adapter refuses any `tools/call` whose arguments carry an approval-shaped key
(`/approv|confirm|decision|challenge/i`) on any tool but `migration_run`.

Both paths end at the same single comparison: `answer.trim() === challengeFor(candidate)`,
against a candidate recomputed under the module lock. A front end that returns
anything it composed itself has approved nothing — it has moved the forgery one
file over.

For historical formats, the elicitation schema is a **required free-text field**, never an enum. This
is load-bearing. An `enum: ["Approve","Decline"]` is answerable from the schema
alone: `{"action":"accept","content":{"decision":"Approve"}}` is a frame a host
can synthesize with no dialog and no person, authorizing multiple lines without
operator transcription. An accept carrying
any extra content key is also refused, so a host cannot smuggle a candidate
identifier alongside the phrase.

**What this is not.** The confirmation phrase is a *transcription barrier*
against schema-derived auto-answers. It is not proof of humanity. The phrase
appears in the message the host renders, so a host that scrapes its own dialog
text can still forge one approval per request — the same ceiling as an
operator's terminal being able to echo the phrase it was just printed. What it
does buy is that no default, no enum pick, and no empty auto-accept is ever an
approval. Do not tell an operator it is stronger than that. This historical
challenge does not mint `HUMAN_ATTESTED`. Module 19 instead requires a verified
ledger line bound to the current full candidate and trusted policy. Status,
pending and run share its fresh projection; a valid append is immediately
visible without advancing a checkpoint or restarting the session. The
standard `APPROVE`/`REJECT` review records `AGENT_RELAYED` without infrastructure.
The optional protected signer/WebAuthn verifier is retained. An explicit
high-assurance requirement blocks when its signer is unavailable or activation
invalid; `AGENT_RELAYED` cannot satisfy `HUMAN_ATTESTED`.

`artifact-migration-decision <module> --verify` audits a record read-only: it takes no
lock, re-derives every `prevDigest` itself, reports the first chain break, flags
any line claiming a human channel while carrying no derived candidate, and
checks the history and decision-ledger anchors `integrity.json` pins outside
`state.json`. It is the command to run first when an approval is in question.
