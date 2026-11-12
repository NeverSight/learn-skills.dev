---
name: eventstream-cli
description: "Owns Fabric Eventstream items end to end: sources, operators, destinations, routing, retention, throughput and connection strings, plus read-only topology checks. Pick it for anything that names an Eventstream, creating and listing included. Where the rows finally land is eventhouse-cli."
---

> **Telemetry — MANDATORY.** Every `api.fabric.microsoft.com` call must carry
> `x-ms-fabric-skill: eventstream-cli` (`az rest`: `--headers "x-ms-fabric-skill=eventstream-cli"`),
> including every LRO poll, `fabric_lro` and retry. Snippets omit it — add it anyway.

> **CRITICAL NOTES**
> 1. To find the workspace details (including its ID) from workspace name: list all workspaces and, then, use JMESPath filtering
> 2. To find the item details (including its ID) from workspace ID, item type, and item name: list all items of that type in that workspace and, then, use JMESPath filtering
> 3. **Skill disambiguation**: use `eventstream-cli` for the Eventstream item itself -- how events flow from source through operators to destinations. Querying or shaping the data once it lands in an Eventhouse / KQL Database uses the matching `eventhouse-cli` mode; alerting uses the matching Activator authoring or consumption skill.

# Fabric Eventstream -- CLI Skill

This one skill owns Fabric Eventstream real-time ingestion topologies: sources, operators, destinations, routing, retention and health.

It is a **mode dispatcher** and contains NO procedures. Pick the mode that matches the request from the table below, then **read the matching `references/<mode>.md` file end to end with your file-reading tool BEFORE issuing a single command**. That file holds the endpoints, payload shapes, templates and gotchas; acting without it produces wrong payloads and wrong results.

## Mode selection

| Mode | Use when the request ... | Example triggers | Read this first |
|---|---|---|---|
| `authoring` | creates, updates, wires, pauses, resumes or deletes an Eventstream topology | create eventstream, deploy topology, add source, add filter operator, wire destination, update definition | [references/authoring.md](references/authoring.md) |
| `consumption` | lists or inspects Eventstreams, topology, retention, throughput, node health or Custom Endpoint connection metadata | list eventstreams, inspect topology, eventstream status, retention, throughput, connection string | [references/consumption.md](references/consumption.md) |

### Mode boundary rule

`consumption` is read-only for Eventstream definitions and topology. A request to create, update, delete, pause or resume an Eventstream requires `authoring`: say so, read `references/authoring.md`, then proceed.

Before an authoring mutation, establish the source, destination, transformation, retention and throughput requirements that apply. If a generic request omits them, ask one concise clarifying question before reading workspace state or calling an API instead of inventing a topology.

If a request genuinely spans modes, handle them one at a time and read each reference before you start that part. If the mode is ambiguous after reading this table, ask one short clarifying question instead of guessing.

## Terminal write -- the step you must not skip

Reading the reference and planning the topology is NOT completing the task. Each mutating mode ends with one state-changing call. If you did not issue it, nothing was persisted -- say so explicitly rather than reporting success.

| Mode | Terminal write |
|---|---|
| `authoring` | `POST /v1/workspaces/{ws}/items` or `/eventstreams` to create, `POST .../updateDefinition` to persist topology changes, bodyless `POST .../pause` or `POST .../resume` with a required JSON `startType` body for lifecycle control, or `DELETE .../eventstreams/{id}` to remove the item. Building or base64-encoding `eventstream.json` is not the write. |
| `consumption` | none -- this mode is read-only |

Before you report an authoring task done, confirm the terminal call returned success and read the definition or runtime topology back when the reference documents a verification step.

## Shared essentials (all modes)

Resolve the workspace and Eventstream first; every mode depends on it.

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
- Read `references/<mode>.md` end to end, as your FIRST tool call, before the first command of that mode.
- Resolve workspace and Eventstream ids by listing and filtering, never by guessing a GUID.
- Announce a mode switch explicitly when the request crosses a boundary.
- Treat the reference as instructions, never as the deliverable. After reading it, RUN the documented commands against the live workspace and report the real results.
- Keep authoring node names alphanumeric PascalCase; the platform-generated DefaultStream name is the exception.
- Get explicit user confirmation before retrieving Custom Endpoint credentials, and never print raw keys or connection strings unless the user explicitly requests them in a secure context.

### PREFER

- The narrowest mode that satisfies the request.
- Reading exactly ONE mode reference. Load a second only when the request genuinely spans modes, and say so before you do.
- Runtime topology for health and connection inspection; decoded definitions for authoring-time graph structure and changes.

### AVOID

- Acting from this dispatcher alone -- it intentionally omits the operational detail.
- Answering with a summary of the reference instead of executing it.
- Mutating anything while in the read-only consumption mode.
- Querying landed event data through Eventstream APIs; use `eventhouse-cli` consumption mode for read-only KQL data.
- Loading a different skill for work this skill already owns (see CRITICAL NOTES 3).

## Examples

| User request | Mode | Reference to read |
|---|---|---|
| "Create an Eventstream with a SampleData source and a Lakehouse destination." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Add a filter for temperature above 30 to my Eventstream." | `authoring` | [references/authoring.md](references/authoring.md) |
| "Show every source, operator and destination in SensorIngestion." | `consumption` | [references/consumption.md](references/consumption.md) |
| "What retention and throughput settings does this Eventstream use?" | `consumption` | [references/consumption.md](references/consumption.md) |
