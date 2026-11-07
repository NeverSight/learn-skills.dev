---
name: port-dashboards
description: >-
  Build and update Port dashboard pages: widgets (table, number chart, pie
  chart, bar chart, multi-line chart, markdown, iframe, links, action card,
  action-runs table, entity details, AI agent), the 12-column row layout,
  sidebar placement, and private-page rules. Covers dataset filter syntax so
  a widget shows the entities you expect instead of an empty or wrong
  result. Use when asked to "build a Port dashboard", "add a widget to a
  dashboard page", "create a number chart / pie chart / table widget in
  Port", "why is my Port widget empty", "make this dashboard page private",
  or "where should this dashboard go in the sidebar". For building a custom
  plugin widget (your own React iframe), use the nested
  `port-dashboard-plugins` skill instead.
license: MIT
compatibility: "Claude Code, Cursor, Codex CLI, GitHub Copilot"
metadata:
  version: "1.0.0"
  author: port-labs
  repository: https://github.com/port-labs/port-skills
  tags: port,dashboards,widgets,reference
  summary: Build Port dashboard pages with widgets, layout, and permissions
---

# Port dashboard pages

A Port dashboard page is a sidebar entry made of one or more widgets (tables,
charts, markdown, links, and more) arranged in a 12-column grid. This skill
is reference-only: static knowledge about widget schemas, the layout grid,
sidebar placement, and dataset filter syntax, drawn from Port's dashboard
page schema and public docs. It doesn't need a live Port account or MCP
server to produce a correct dashboard payload, only a real account to
actually create the page.

Out of scope: building your own custom-code widget (a React/TypeScript
iframe plugin uploaded via `port-plugins-cli`) is the nested
[`port-dashboard-plugins`](port-dashboard-plugins/SKILL.md) skill, not this
one. Blueprint and property modeling (what a `dataset` can filter on) is
owned by the `port-blueprints` skill; this skill only covers how those
properties map onto widget and dataset fields. The full search rule
grammar (all operators, `and`/`or`/`not` nesting) is Port's [Search and
query](https://docs.port.io/search-and-query/structure-and-syntax) syntax;
this skill covers the subset relevant to widget datasets. Who can **view or
edit** a page once it exists, including private pages shared with specific
users or teams, is the `port-permissions` skill's page-permissions
reference, not this one; this skill only covers a private page's own
creation and visibility mechanics (see [Step 5](#step-5---handle-private-pages-correctly)).

## Skill class

Reference skill: the widget schemas, grid rules, and dataset syntax below
are static and enough to hand-author a correct dashboard JSON payload. If
the [Port MCP server](https://docs.port.io/ai-interfaces/port-mcp-server/overview)
is connected, its dashboard tools (`upsert_dashboard_page`, `upsert_widget`,
`get_page`, `get_sidebar`, `load_widget_schema`, `list_entities`,
`list_blueprints`) are an optional enhancement: they create the page for
you and let you sample real entities to validate a dataset before saving.
Without them, use the fallback in every step below: the Port UI's dashboard
editor, or the [Pages API](https://docs.port.io/api-reference/pages) /
[Swagger](https://api.port.io/swagger/#Pages) directly.

## Prerequisites

- Go over the `port-getting-started` skill first if this is your first time
  working with Port.
- The blueprint(s) the dashboard's widgets will query already exist, with
  the properties you plan to filter, group, or chart on.
- Optional: the Port MCP server connected in your agent, for live dataset
  validation and one-shot page creation (see Skill class above). Without
  it, use the Port UI or the Pages API with a `client_id`/`client_secret`
  pair (**...** menu > **Credentials** in the Port app). Search
  `search_port_knowledge_sources` for anything this skill doesn't cover.

## Step 1 - Decide sidebar placement

Precondition: a new dashboard page needs a home in the sidebar.
Action: if MCP is available, call `get_sidebar` to inspect the existing
folder structure before creating the page. If a single folder clearly
matches the dashboard's topic, place the page there (`parent` on the page).
If several folders are plausible, ask the user which one they prefer
instead of guessing. If nothing matches, place the page at the sidebar
root, creating a new folder only when the dashboard starts a new category
of its own.
Fallback: without MCP, open the Port UI's sidebar and read the folder tree
directly, or `GET /v1/pages` (see [references/dashboards.md](references/dashboards.md#sidebar-placement-and-page-fields))
to list existing pages and their `parent`/`after` fields.

## Step 2 - Choose widgets and validate each dataset

Precondition: you know which entities and metrics the dashboard should
show.
Action: pick one widget type per metric or view from the twelve types in
[references/dashboards.md](references/dashboards.md#widget-types), matching the widget to the question
("how many" -> number chart, "trend over time" -> multi-line chart, "browse
rows" -> table). For every widget with a `dataset`, resolve the target
blueprint first, then validate the dataset **before** creating the widget:
if MCP is available, run `list_entities` with the dataset as `query`,
`countOnly: true`, and a small `limit` (3-5), to confirm the count and that
the returned entities look right. If the call errors or the results look
wrong, call `list_blueprints` to check property names, types, and enum
values, fix the dataset, and retry.
Fallback: without MCP, run the equivalent call yourself:
`POST /v1/blueprints/{blueprint}/entities/search` with the same `query`
body (see [references/dashboards.md](references/dashboards.md#dataset-filter-syntax) for the rule
grammar and examples), or build the widget in the Port UI and use its
built-in entity count/preview before saving.

## Step 3 - Lay out the page (12-column grid)

Precondition: the widget set for the page is known.
Action: arrange widgets into rows. Every row's column sizes must sum to
exactly 12, a row holds at most 4 columns, each column is 3-12 wide, and
every row is at least 400px tall. Every layout column's `id` must match a
widget's `id` exactly, one-to-one. See
[references/dashboards.md](references/dashboards.md#the-12-column-layout-grid) for the layout
schema and worked examples.
Fallback: the Port UI's drag-and-drop dashboard editor enforces these
constraints for you, use it when hand-writing a layout for 6+ widgets gets
error-prone.

## Step 4 - Create or update the page

Precondition: widgets and layout are ready.
Action: if MCP is available, call `upsert_dashboard_page` with the full
`identifier`, `title`, `widgets`, and `layout`. For 5+ widgets, try the full
payload first; if it fails on size or complexity, fall back to an
incremental flow: create an empty page (`widgets: []`), add widgets one at
a time with parallel `upsert_widget` calls, then call `get_page` and pass
its `widgets` straight through to a final `upsert_dashboard_page` call that
only adds the new `layout`.
Fallback: without MCP, create the page from the Port UI's dashboard editor,
or call the [Pages API](https://docs.port.io/api-reference/pages) directly:
`POST /v1/pages` (or `PATCH /v1/pages/{identifier}` if it already exists)
with `type: "dashboard"` and a single root `dashboard-widget` wrapping your
`widgets` and `layout` (see
[references/dashboards.md](references/dashboards.md#creating-a-page-with-the-raw-api) for the exact
envelope Port expects).

## Step 5 - Handle private pages correctly

Precondition: the dashboard is personal, not for the whole organization.
Action: set `visibility: "private"` and omit `parent` and `after`
entirely, whether via MCP or the raw API. Port keeps private pages in a
separate sidebar section and appends an owner-specific suffix to the
identifier in its response, use *that* returned identifier for any
follow-up edit, widget update, or delete, not the one you sent.
Fallback: from the UI, set **Visibility** to **Private** when creating the
page (the field is read-only after creation for non-admins); an org admin
must first grant the `create:private-pages` scope if the option isn't
visible. See [references/dashboards.md](references/dashboards.md#private-pages) for the full
rules and an example payload.

## Examples

Worked, complete JSON payloads for every widget type, a full layout, and
the raw API envelope are in
[references/dashboards.md](references/dashboards.md#widget-types).

## Common pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Widget renders empty or with the wrong entities | Dataset filters on the wrong property, wrong blueprint, or a typo'd enum value | Validate with `list_entities`/`entities/search` before creating the widget, see [Step 2](#step-2---choose-widgets-and-validate-each-dataset) |
| Page creation rejected: "column sizes must sum to 12" | A row's column `size` values don't add to 12 | Recompute the row, max 4 columns, each 3-12 wide, see [Step 3](#step-3---lay-out-the-page-12-column-grid) |
| Page creation rejected: row height too small | A row's `height` is under 400px | Set every row to at least 400 |
| Widget never renders / layout looks broken | A layout column's `id` doesn't match any widget's `id` | Keep widget `id`s and layout column `id`s in exact sync |
| Private page edits silently target the wrong page, or 404 | Used the `identifier` you sent instead of the one Port returned (owner-suffixed) | Store and reuse the identifier from the create/`get_page` response, see [Step 5](#step-5---handle-private-pages-correctly) |
| Private page creation rejected | `parent` or `after` was set alongside `visibility: "private"` | Omit both fields entirely for private pages |
| Number chart shows 0 or an error | `chartType`-specific required fields missing (e.g. `func`/`averageOf` for `aggregateByProperty`) | Check the per-`chartType` required fields in [references/dashboards.md](references/dashboards.md#number-chart-entities-number-chart) |
| Pie/bar chart property rejected | `property` isn't prefixed (`property#`, `relation#`, `scorecard#`, ...) or a meta field (`$identifier`, `$title`, `$team`) | Use the prefixed form, see [references/dashboards.md](references/dashboards.md#property-reference-syntax) |

## Quick reference

- Widget types: `table-entities-explorer`, `entity-details`,
  `action-card-widget`, `action-runs-table-widget`, `links-widget`,
  `ai-agent`, `markdown`, `iframe-widget`, `entities-number-chart`,
  `entities-pie-chart`, `bar-chart`, `multi-line-chart`. Full schema for
  each: [references/dashboards.md](references/dashboards.md#widget-types).
- Layout: rows of 1-4 columns, column `size` 3-12 summing to exactly 12 per
  row, row `height` >= 400px, column `id` matches a widget `id`.
- Visibility: `"org"` (default, sidebar-placeable via `parent`/`after`) or
  `"private"` (no `parent`/`after`, identifier gets an owner suffix).
- Dataset shape: `{ combinator: "and" | "or", rules: [...] }`, each rule a
  `property`/`relation`/`scorecard` clause. Full grammar:
  [references/dashboards.md](references/dashboards.md#dataset-filter-syntax).
- MCP tools (optional, live account): `get_sidebar`, `list_blueprints`,
  `list_entities`, `load_widget_schema`, `upsert_widget`,
  `upsert_dashboard_page`, `get_page`.
- Fallback without MCP: Port's UI dashboard editor, or the
  [Pages API](https://docs.port.io/api-reference/pages) (`POST`/`PATCH`/`GET`
  `/v1/pages`) and `POST /v1/blueprints/{blueprint}/entities/search` for
  dataset checks.
- For custom-code widgets instead of built-in widget types, see the nested
  [port-dashboard-plugins](port-dashboard-plugins/SKILL.md) skill.
