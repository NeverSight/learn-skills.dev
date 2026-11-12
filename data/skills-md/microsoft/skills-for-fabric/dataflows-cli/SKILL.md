---
name: dataflows-cli
description: "Manages Fabric Dataflow Gen2 items, including creation, M editing, connections, output destinations, getDefinition and updateDefinition inspection, executeQuery, refresh history, and Gen1-to-Gen2 save-as upgrades via saveAsNativeArtifact. Use for Dataflow items or Power Query M definitions. For pipeline JSON use pipeline-migration; for Spark or Warehouse transformations use their own skills."
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: dataflows-cli` (`az rest`: `--headers "x-ms-fabric-skill=dataflows-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Skill disambiguation**: use `dataflows-cli` for every Fabric Dataflow Gen2 item and Power Query M concern. Synapse / ADF pipeline and dataset JSON translation is `pipeline-migration`; Spark notebook transformations are `spark-cli`; T-SQL transformations are `sqldw-cli`.

# Fabric Dataflow Gen2 -- CLI Skill

This one skill owns Fabric Dataflow Gen2 items: connections, Power Query M, output destinations, saved definitions, refresh history, and Gen1 upgrades.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

Read it once per session. A file you have already read stays in context, so do not re-read it on a later turn; open the deeper files under `references/<mode>/` only when a row in that file's reference table matches what you still need, and open only that row's file.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | creates or changes a dataflow: connections, credentials, M edits previewed before save, output destinations, updateDefinition | executeQuery preview, updateDefinition, connection setup, supportedConnectionTypes, credentialType, add output destination | [references/authoring.md](references/authoring.md) |
| `consumption` | reads a saved dataflow: definition, parameters, refresh history, or runs a saved/ad-hoc read-only M query and parses Arrow | getDefinition, executeQuery saved query, ad-hoc query, Arrow IPC, refresh history | [references/consumption.md](references/consumption.md) |
| `upgrade` | upgrades a Gen1 dataflow to Gen2.1 via save-as and rebind, or assesses upgrade readiness/risk | Gen1 Gen2 readiness, saveAsNativeArtifact, clone Gen1 dataflow, upgrade risk assessment | [references/upgrade.md](references/upgrade.md) |

### Mode boundary rule

`consumption` is read-only. A preview run that exists to validate M **before** `updateDefinition`, and any capability lookup (`supportedConnectionTypes`, `credentialType`), belong to `authoring` even though they issue the same `executeQuery` call -- classify by intent, not by endpoint.

If a request genuinely spans modes, handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the change is NOT completing the task. Each mutating mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | `POST /v1/workspaces/{ws}/dataflows/{id}/updateDefinition` to persist the M, connections and output destinations; a NEW dataflow needs `POST /v1/workspaces/{ws}/items` (or `/dataflows`) first. `executeQuery` is a preview and writes nothing. If the user asked for a refresh, also `POST .../jobs/instances?jobType=Refresh`. |
| `consumption` | none -- this mode is read-only |
| `upgrade` | `saveAsNativeArtifact` to create the Gen2.1 artefact, then rebind. A readiness report alone does not upgrade anything. |

Before you report the task done, confirm the terminal call returned success and, where the reference documents a readback, read the artefact back to prove the change landed.

### `upgrade` generation boundary -- HARD STOP (mandatory)

Save-as runs only from Gen1 to Gen2.1. For an execution request whose source is Gen2, or whose source generation is not established, state that no public save-as or in-place upgrade endpoint is available and stop before any API call. This does not block a read-only readiness scan whose purpose is to discover and classify Gen1 candidates.

Do not read "choose the closest endpoint and proceed" as approval to export a definition and create a copy, do not switch to `authoring` to do it instead, and do not mutate anything. Ask the user to clarify the intended outcome and to approve explicitly.

### `consumption` reporting

`consumption` has no terminal write, so its deliverable is the answer itself. When that mode runs `executeQuery`, name the operation you called and state the `QueryName` you sent, verbatim, next to the results, plus whether it was a saved `shared` member or a non-persisted ad-hoc `customMashupDocument`. Rows alone do not tell the user which call produced them.

This applies to `consumption` only. In `authoring`, `executeQuery` is an intermediate preview step -- do not add reporting turns around it; go on to the terminal write.

## Shared essentials (all modes)

Resolve the workspace and item first; every mode depends on it.

| Task | Reference | Notes |
|---|---|---|
| Finding Workspaces and Items in Fabric | [COMMON-CLI.md](../../common/COMMON-CLI.md#finding-workspaces-and-items-in-fabric) | **Mandatory** -- read before resolving any workspace or item id |
| Fabric Topology & Key Concepts | [COMMON-CORE.md](../../common/COMMON-CORE.md#fabric-topology--key-concepts) | Item types, workspaces, capacities |
| Environment URLs | [COMMON-CORE.md](../../common/COMMON-CORE.md#environment-urls) | Sovereign / non-public cloud hosts |
| Authentication & Token Acquisition | [COMMON-CORE.md](../../common/COMMON-CORE.md#authentication--token-acquisition) | Wrong audience = 401; read before any auth issue |
| Authentication Recipes | [COMMON-CLI.md](../../common/COMMON-CLI.md#authentication-recipes) | `az login` flows and token acquisition |
| Core Control-Plane REST APIs | [COMMON-CORE.md](../../common/COMMON-CORE.md#core-control-plane-rest-apis) | Pagination, LRO polling, rate limiting |
| Gotchas & Troubleshooting | [COMMON-CLI.md](../../common/COMMON-CLI.md#gotchas--troubleshooting-cli-specific) | `az rest` audience, shell escaping, token expiry |

## Rules

### MUST

- Select exactly one mode from the table above before doing anything else.
- Read `references/<mode>.md` end to end, as your FIRST tool call, before the first command of that mode. Read it ONCE, in a single full read: do not re-open it, do not grep it again, and do not page through it. You already have it.
- Resolve workspace and item ids by listing and filtering, never by guessing a GUID.
- Announce a mode switch explicitly when the request crosses a boundary.
- Treat the reference as instructions, never as the deliverable. After reading it, RUN the documented commands against the live workspace and report the real results. Quoting what the reference says instead of executing it does not answer the request.
- When a question about what Fabric supports IS the deliverable -- supported connection types, a connector's parameters, available credential types -- answer it from the endpoint the reference names rather than from the reference's own list, and name that endpoint in your answer. Whichever mode you are in: the reader cannot tell a live value from a quoted one unless you say where it came from. This is wording in the final answer, not an extra step.
- Produce every artefact the user asked for, under the name they used. Running the right API calls is not a substitute for the requested report: if the request names a deliverable, emit it, and keep its heading even when the finding is "none" or "not applicable".

### PREFER

- The narrowest mode that satisfies the request.
- Reading exactly ONE mode reference. Load a second only when the request genuinely spans modes, and say so before you do.
- Reporting the mode you chose in your first response so the user can correct you.

### AVOID

- Acting from this dispatcher alone -- it intentionally omits the operational detail.
- Answering with a summary of the reference instead of executing it.
- Re-reading or re-grepping a reference you already loaded; it costs turns and tokens.
- Mutating anything while in a read-only mode.
- Loading a different skill for work this skill already owns (see CRITICAL NOTES 3).

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "Show me the refresh history and parameters of the SalesIngest dataflow." | `consumption` | [references/consumption.md](references/consumption.md) |
| "Preview this M query, then save it into the SalesIngest dataflow definition." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Is my Gen1 dataflow ready to upgrade to Gen2.1?" | `upgrade` | [references/upgrade.md](references/upgrade.md) |

