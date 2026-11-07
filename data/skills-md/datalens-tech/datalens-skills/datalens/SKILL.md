---
name: datalens
description: >-
  Start here for Yandex DataLens when the task has not yet settled on a tool, or when the question
  is about DataLens itself rather than about carrying something out in it: what DataLens is and
  what it can do; which installation is in play — Yandex Cloud, on-premise, or the internal Yandex
  Team one — and how they differ in hosts, auth, and capabilities; what a collection, workbook,
  connection, dataset, chart, or dashboard is and how they relate; and whether to reach for the MCP
  server, the Python SDK, the HTTP API, or the web UI. Use it to orient and to route to the skill
  that does the work. NOT for doing the work once the approach is chosen — that is `datalens-sdk`
  for Python and `datalens-html-pages` for standalone HTML reports — and not for interpreting what
  business metric values mean.
license: Apache-2.0
metadata:
  domain: datalens
---

# DataLens

[DataLens](https://datalens.ru) is a business intelligence and data visualization system: it connects to databases, models the data into datasets, and renders charts and dashboards on top of them. It is offered as a managed service in Yandex Cloud, deployed on-premise, and run internally at Yandex.

This file orients and routes. It does not teach any one interface — pick the interface below and follow the skill that owns it.

## Data flow

```
database → connection → source → dataset → chart → dashboard
```

- **connection** — credentials and driver for one database.
- **source** — a table or a SQL query exposed by that connection.
- **dataset** — the modelling layer: fields, calculated fields, joins, parameters, row-level
  security.
- **chart** — one visualization. *Wizard* charts sit on a dataset; *QL* charts skip the dataset and
  query a connection directly; *editor* charts are custom JavaScript.
- **dashboard** — tabs, widgets, selectors, and layout over charts.

Build left to right and reference by id. Deleting upstream breaks everything downstream.

## Object IDs and URLs

DataLens URLs for objects with an explicit type can use either of these forms:

- `/<object_type>/<object_id>-<readable_slug>` — pass only the object ID before the readable
  suffix to the API.
- `/<object_type>/<object_id>` — when the readable suffix is absent, the entire final path segment
  is the object ID.

Dashboard links have an additional short form: `https://datalens.ru/<dashboard_id>`. When the URL
is identified as a dashboard link, the only path segment is the dashboard ID; there is no object
type segment. For example, `https://datalens.ru/bgquq1234567` refers to dashboard ID
`bgquq1234567`.

For an explicitly typed object, `https://datalens.ru/connections/r6wa2j1ww5cad-demo` refers to the connection ID
`r6wa2j1ww5cad`; `demo` is a human-readable URL suffix. If the URL is
`https://datalens.ru/connections/r6wa2j1ww5cad`, use the same complete segment as the ID. The same
rule applies to connections, datasets, and charts. Do not apply the root-level short form to those
object types.

Treat object IDs as opaque values. Prefer the value from `Copy ID` or the API response's `id`
field when available. If a URL is ambiguous or does not match these forms, do not guess the ID.
Do not confuse an object ID with a display name, readable URL suffix, or a field UUID.

## Object model

Where entries are filed — a separate axis from the flow above. Connections, datasets, charts, and
dashboards are all *entries*, and entries live in a container tree. Two schemes exist, and which
one is available differs per installation:

```
newer    collection
           ├── collection …            nested, arbitrarily deep
           └── workbook
                 └── entries           connection, dataset, chart, dashboard

older    folder tree, path-addressed   e.g. Users/someone/reports
           └── entries                 held directly, no workbook in between
```

The workbook is the unit of grouping and permissions in the newer scheme; the folder path plays
that role in the older one. **Never assume which is available** — an installation may offer one,
the other, or both, so establish it the way the interface skill tells you rather than writing
path-based logic against a workbook-only deployment.

## Installations

**Never assume which one is in play** — hosts, auth, and the available connectors and chart types
all differ. Establish it before writing anything that talks to an API.

| Installation | UI | API host | Auth |
|---|---|---|---|
| **Yandex Cloud** | `datalens.ru` | `api.datalens.tech` | `yc` CLI IAM token, plus an organization id |
| **On-premise** | ask the user | ask the user | deployment-specific; commonly an OAuth token in the environment |
| **Yandex Team** (internal) | `datalens.yandex-team.ru` | `api.datalens.yandex.net` | internal |

**Yandex Cloud** is the managed service. **On-premise** covers both the open-source self-host
(`docker compose`, UI on `:8080`) and the commercial enterprise build. **Yandex Team** is the
internal Yandex installation — see *Installation-specific detail* below before answering anything
specific to it.

Tool-specific skills detect the installation for you — the SDK, for instance, ships a preflight
that reports it. Do not hand-roll detection.

## Choosing an interface

| Want to | Use | Skill |
|---|---|---|
| Manage entities from Python — create, update, inspect, export, clone | **Python SDK** (`datalens-sdk` on PyPI) | `datalens-sdk` |
| Let an agent call the DataLens API directly through tools | **MCP server** ([`@datalens-tech/mcp`](https://github.com/datalens-tech/datalens-mcp)) | — see its README |
| Anything else programmatic | the public HTTP API | — see below |
| Explore, click around, look at a rendered chart | the web UI | — human work, not agent work |

**SDK vs MCP.** The SDK is the default for anything scripted, repeatable, or committed to a
repository — it is typed, it has a documented object model, and the work survives as code. The MCP
server suits interactive one-offs inside an agent session: it fetches the API's OpenAPI spec at
startup and exposes a three-tool gateway (`list_commands` → `describe_commands` →
`invoke_command`) instead of hundreds of tools. Do not mix them for one task.

**The HTTP API, when neither fits.** The SDK and the MCP server are both built on it, so reach for
it directly only where they fall short. It is an HTTP API in an RPC style rather than a REST one:
you call named commands with JSON payloads, not resources. It is also self-describing — fetch the
OpenAPI spec from `/json/` on the installation's API host (*Installations* above;
`https://api.datalens.tech/json/` on the cloud) and work from the spec rather than guessing command
names or payload shapes. On the cloud the organization id is required, sent as an `x-dl-org-id`
header.

## Installation-specific detail

Two installations withhold something you need, and in both cases the answer is to ask rather than
to fill the gap yourself.

**Yandex Team** is extended by a skill distributed separately, `datalens-yateam`. If it is present
in the available skills list and the environment targets that installation, invoke it: it adds and
overrides installation-specific detail from this file, and it wins where the two disagree. If the
task concerns Yandex Team and the skill is *not* in the list, stop and ask the user to install it,
following the instructions at <https://datalens.yandex-team.ru/get-skills>. Do not reconstruct its
content in the meantime — say which part of the answer is installation-dependent and leave it
there.

**On-premise** publishes no endpoints, and the API does not necessarily sit on the UI's host. Stop
and ask the user for both — the DataLens endpoint and the DataLens API endpoint — before writing
anything that talks to either. Do not derive one from the other, do not fall back to a cloud
default, and do not carry on with a placeholder.

## Out of scope

State the boundary and stop rather than improvising an adjacent solution:

- What a metric *means* for the business, or whether a number looks right.
- Screenshotting or driving the web UI.
- Embedding DataLens in another product, or iframes.
- SQL and analysis that does not touch DataLens entities.
