---
name: api-spec
description: 'Produce the api-specs/ document set (numbered NN-topic.md files plus _index.md) from the technical specs. Derives every operation, its inputs/outputs, errors, and access rules from the module definitions and data model already decided in docs/technical-specs/, and writes them in whatever protocol the project chose: REST, GraphQL, gRPC, or SOAP. Use when the user wants an API specification, endpoint contracts, an OpenAPI/schema/proto/WSDL companion, or asks to "write the api specs". Runs after technical-spec and before task-breakdown.'
---

# API Specification

The interface contract for the system. It runs **after** `technical-spec` (the architecture, modules, and data model must already exist in `docs/technical-specs/`) and **before** `task-breakdown`, `tech-lead-setups`, and `lead-review`, all of which cite endpoint contracts. The technical specs decide *what modules exist and what data they own*; this set pins down *the exact wire contract a client calls and a server must honor*.

Output is a **numbered file set** under `docs/api-specs/`, not one monolith (`_index.md` plus `NN-topic.md` files), so a single resource or operation is linkable from task cards, stubs, and reviews (e.g. `api-specs/03-work-orders.md` -> `POST /work-orders`).

The protocol is **already decided** in `technical-specs/04-tech-stack.md` (API style: REST / GraphQL / gRPC / SOAP). Do not re-litigate it; read it, confirm it, and write the contract in that protocol's idiom. The document set's job is identical across protocols ([references/contract-format.md](references/contract-format.md#protocol-agnostic-core)); only the surface notation changes ([references/contract-format.md](references/contract-format.md#protocol-idioms)).

Two phases: **derive the surface from the technical specs, then write the set.**

**Running project (adopt mode).** If the API already runs, document the live surface. Import an existing OpenAPI, schema, proto, or WSDL file if there is one; otherwise read the route, resolver, or service definitions in the code. Derive each operation from what the code does, not from the module definitions. Mark each place where the code and the technical spec disagree as a finding in that operation's file, and list the findings in your report. Do not change the contract here.

## Phase 1: Derive the surface

Read the source of truth before writing anything. The api-specs are a *projection* of the technical specs, not new invention:

- `technical-specs/04-tech-stack.md`: the **API style/protocol** and the validation/schema layer. This selects the idiom for the whole set.
- `technical-specs/05-module-definitions.md`: the public surface of each module. Each module becomes one `NN-<resource>.md` file; its listed operations become the documented operations.
- `technical-specs/06-data-model.md`: every entity, field, type, nullability, default, and state machine. Request/response shapes, enums, and valid transitions come straight from here. Do not invent fields the data model does not have.
- `technical-specs/07-security.md` and `09-authentication-and-authorization.md`: the authn mechanism and the role matrix. These become the per-operation **Access** line and the auth conventions file.
- `technical-specs/11-environment-configuration.md` and the operational endpoints (health monitor, reset-db-state); these become the `system` resource file, with the production gating noted.
- `docs/business/`: the AC/US each operation serves. Every operation cites the AC/US that justifies it; an operation tracing to no AC/US is a flag to raise, not a row to write. In adopt mode, when `docs/business/` does not exist, skip this traceability and say so in `_index.md`.

Confirm the protocol and the planned file list (one per module plus conventions, authentication, system, and the index) with the user before writing. Surface contradictions against the technical specs as you go ("module-definitions section 5.8 says only Super Admin sets this field, but the data model has no role column on it; where is that enforced?"). Only grill where the technical specs are genuinely silent on a contract detail (e.g. pagination defaults, idempotency keys, an envelope shape the specs never pinned); recommend a default for each and confirm.

### Design the operation surface for depth

An API operation is an **interface** in the strict sense: the full contract a client must know (inputs, outputs, errors, ordering, idempotency), which is exactly the eight-part core below. Apply the depth lens in [../technical-spec/references/module-design.md](../technical-spec/references/module-design.md#vocabulary) when shaping the surface:

- Prefer **few deep operations** that do a meaningful unit of work over many shallow CRUD passthroughs that push orchestration onto every client. If three clients all call `POST` then `PATCH` then `POST` to complete one workflow step, that workflow step is the operation the surface is missing.
- Apply the **deletion test** to each proposed operation: if removing it just makes callers compose two others, it was a passthrough; if removing it forces every caller to reimplement a rule, it earns its place.
- The contract is the client's test surface: a client tests against the operation's interface, so an operation that hides the right behaviour spares every client the same logic.
- When the core resource's surface has real alternatives (RPC-style verbs vs resource transitions, coarse vs granular operations), offer the **Design it twice** exploration in [../technical-spec/references/module-design.md](../technical-spec/references/module-design.md#design-it-twice): draft a couple of radically different operation surfaces, compare by depth and by how much orchestration each leaves to clients, and let the user pick before writing the file. Stay within the boundaries and entities the technical specs already fixed; this designs the *contract shape*, not new architecture.

## Phase 2: Write the set

Write to `docs/api-specs/`. The file set, in order:

1. **`01-conventions.md`**: the transport contract shared by every operation, in the project's protocol idiom ([references/contract-format.md](references/contract-format.md#protocol-idioms)): base address, message/content type, the success and error envelope, pagination, the full status/fault-code table, standard error codes mapped to their condition, and a **role reference** table mirroring the auth doc. This is the single source for cross-cutting rules; every resource file cites it rather than restating.
2. **`02-authentication.md`**: the login / refresh / logout (or token-issue) operations, fully documented including the token/cookie strategy from the technical specs.
3. **`NN-<resource>.md`**: one file per module/bounded resource from `05-module-definitions.md`. Each operation documented per [references/contract-format.md](references/contract-format.md#protocol-agnostic-core). Order resources by dependency (foundational/master data and the entities others reference first).
4. **`NN-system.md`** (the last numbered file): the operational endpoints, meaning the health monitor (aggregate and per-dependency) and, where mounted, reset-db-state, with the rule that it is registered only in non-production environments.
5. **`_index.md`**: the version/base-address header, an **Operation Status Tracker** grouped by resource (legend: `OK` implemented and tested, `WIP` in progress, `TODO` not started, `SCAFFOLD` Tech Lead stub returning a mock), a **Files in This Directory** table, and a **Companion Documents** link back to `../technical-specs/` and `../business/`. The tracker is the at-a-glance build state the task board and stubs sync against.

The tracker has owners: `tech-lead-setups` marks each stubbed operation `SCAFFOLD`, the pull request that implements an operation sets its row to `OK`, and `lead-review` checks that row in its API-contract step.

If an api-specs set already exists, read it and update affected files in place rather than clobbering; report what changed. Then check that `_index.md` matches the files on disk: `python3 <technical-spec dir>/scripts/check_index.py --specs-dir docs/api-specs`.

## Writing rules

- The api-specs are a projection of the technical specs. Trace every operation to a module and every field to the data model; where the specs are silent, raise it in Phase 1 rather than inventing the contract.
- Cite, do not restate: cross-link `../technical-specs/` sections (`[../technical-specs/06-data-model.md section 6.5](...)`) for authoritative field rules, role matrices, and state machines instead of duplicating them.
- Preserve domain terms and non-English UI labels and messages verbatim; mirror the glossary. If error messages are user-facing in a non-English UI language, keep `code` in English and the `message` in the UI language, as the example sets do.
- Keep `_index.md`, the operation status tracker, and the file numbering consistent; if you add or reorder files, update the index and tracker.
- Number sections within each file so operations are citable as stable anchors.

## Writing conventions

- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative tone.
- Metadata header lines (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`) each end with two trailing spaces so Markdown renders them on separate lines.
