---
name: scenario-admin-analytics
description: "Use when answering Scenario admin analytics questions about Creative Unit consumption, most-used models, usage by user or project, AI adoption observability, cached usage data, CSV exports, enterprise PDF reports with charts, or a local analytics dashboard. Keywords: usage API, CU, analytics, adoption, reporting, consumption, cache."
license: MIT
---

# Scenario Admin Analytics

## Overview

Turn Scenario MCP usage data into answers, CSV, Markdown, a PDF with charts, or an offline dashboard. All Scenario data collection stays on MCP. No direct API, SDK, browser scraping, or credentials in reporting scripts. Use the `scenario` skill for connection setup. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

Resolve the customer through `teams_list` and, when needed, `projects_list({team_id})`. Reuse the user's selected scope. If several names match, ask using the discovered choices; unattended, use the task's explicit team/project ID pair, otherwise stop and list the choices. Never choose the first silently. For an organization-wide request, use `scope:"team"` with an accessible context project. This covers projects accessible to the credential, not additional access rights. For a project use `scope:"project"` (default); `project_id` supplies authentication context and the default analytics filter. `project_ids` selects other projects within that team and cannot accompany `scope:"team"`. Deduplicate selected IDs. Do not add a team total to its project subtotals or sum project unique-user counts.

## Quick reference

| Question                      | MCP usage data                               | Calculation                                                                                               |
| ----------------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Top three models              | `modelUsages`                                | Sort by `totalCU` for CU or `totalJobs` for frequency; show both.                                         |
| All model CU for three months | Add `modelUsages.daily`                      | Export every model, grouping time buckets by UTC month.                                                   |
| Who consumed most CU?         | `consumption`, `entities`                    | Rank `value`; join `userId` to `entities.users[].id`.                                                     |
| Top models per user           | Repeat scoped `usage` with one `user_ids` ID | Rank each response's models; include CU and jobs.                                                         |
| Top five users for ten models | Same per-user queries                        | Select the top ten models overall, then rank five identities within each.                                 |
| Explain a difference          | `usages.daily`, `activity`                   | Inspect recorded evidence; follow `activityPagination.nextOffset` to null if complete activity is needed. |

Discover the current schema with `scenario_tools_search({query:"usage",limit:1})` when missing or stale. Normally call visible `usage` directly. If catalog-only, use `scenario_tool_execute_read({name:"usage",parameters:{...}})`, never `arguments`. A host may retain an older direct signature after deployment: if the fresh catalog exposes missing fields, use that same read executor with its schema or reconnect. An old host signature does not establish a missing capability. Ground calls in the [public usage reference](https://mcp.scenario.com/docs/tools/usage) and live catalog.

Always set both dates. Bounds are **inclusive**: a complete March ends at `2026-03-31T23:59:59.999Z`. State UTC buckets. For an undated question assume the last 30 complete days; for "last three months" assume the last three complete calendar months, stating the window. An undated API call defaults to 31 days, not lifetime. Current-day figures are provisional. The API enforces its range limit; do not invent a fixed cap. If it rejects a large range, split into non-overlapping inclusive windows, retain each source, and combine additive measures without summing unique-identity counts.

Begin with summary JSON; add `include:["modelUsages.daily","entities"]` for reports. Time buckets may be finer than daily for short ranges; aggregate by timestamp then UTC day, rejecting duplicate timestamps. `activity` is paginated in batches of at most 100 via `activity_offset`; follow the returned next offset, not guessed completeness. Summaries repeat on activity pages: count them once. Avoid activity for ordinary rankings.

### Accounting and confidence

`totals.totalCU` sums `consumption[].value`, already after discounts. Raw `consumption[].total` equals `value + discount`, before discounts. Model `totalCU` sums time-bucket `cost`, also already after discounts: **never subtract discount again**. API-key CU is a subset. Preserve decimals, zeros, fully discounted rows, and negatives. Jobs measure model executions, not successful assets.

Validate echoed `scope` and dates; check consumption against overall CU, time buckets against model summaries, and per-user model sums against the unfiltered models. The scope echo records applied filters; it does not prove access to every customer project. State established scope and results directly. Do not carry an old "unverified consumption" warning onto validated data.

Model series measure generation activity and exclude separately recorded refunds and non-model operations. Consequently model CU need not equal overall consumed CU. Show the measured difference without asserting its cause; inspect usage sections if an explanation is requested. Never allocate it to models, sum overlapping usage-type categories, or substitute job billing snapshots for consumption. If a check fails, withhold only the affected attribution, report the exact mismatch, and investigate through MCP.

For user/model matrices, collect one same-scope, same-period usage query per `consumption[].userId`, including zero or negative rows. Never join independent user and model summaries by proportion. Reconcile all model CU and jobs before claiming complete coverage; if identities are missing, investigate MCP identity/activity metadata rather than inventing attribution. Resolve names through returned entities; if names are missing and the recipient needs identifiable users, discover `team_members_list` and join its returned email by ID. Retain stable IDs internally, and distinguish API identities when metadata identifies them. Unknown identity type stays unknown. If "most used" has no stated metric, rank by jobs and show CU; an explicit CU request ranks by CU. Break ties deterministically by stable ID. Top-N rows include both metrics.

### Cache, output, and environment fallback

Inspect capabilities, not product names. With files and Python use the bundled [offline helper](scripts/analytics.py); the agent collects MCP data and the script only transforms local snapshots. Read [local reporting](references.md) for envelopes, commands, dependencies, supported filters, and cache validation. The [dashboard template](assets/dashboard.html) uses the warm paper, charcoal, and terracotta palette of [Scenario's public site](https://www.scenario.com), with local font fallbacks.

Cache by connection/account namespace, schema version, team, context project, scope, selected project/user IDs, exact dates, sections, and activity offset. Default TTL is one hour; "refresh" bypasses it. User/model questions also require fresh per-user snapshots. Preserve original retrieval timestamps; re-importing an export must not make it fresh. Summary-only data cannot answer a new trend question. Expired data may support a clearly labeled historical/offline answer. A connection change or accounting/scoping fix invalidates affected caches. Keep private snapshots outside repositories, omit credentials and unnecessary personal data, and delete on request. Retrieval time does not guarantee upstream freshness.

With ephemeral execution, use session files and explain their lifetime. With MCP but no files/execution, answer small questions directly and supply Markdown or fenced CSV; caching is session-only. If PDF generation is unavailable, offer local print-ready HTML when supported. Never claim an unsaved file or unrendered PDF exists. Without MCP, use a supplied prior MCP snapshot with its provenance and age, or report the connection gap; no alternate Scenario data surface.

Answer direct questions first with scope, dates, metric, and retrieval time. Reports include consumed CU, model jobs, model breadth, concentration, trends, identity rankings, and reconciliation. The helper supports CU/job sorting, configurable models per user, monthly CSV, and user/model/date dashboard filters when per-user time buckets exist. Full-period overall and identity consumption remain labeled separately from filtered generation activity. Refreshing a dashboard requires another MCP fetch; never publish customer data as part of this skill.

Park unsupported requests under "Not available through MCP", naming the missing evidence and any supported alternative. Usage alone cannot establish ROI, time saved, ticket attribution, delivered-output adoption, historical eligible-seat counts, or retention. Permission failures, empty results, incomplete coverage, and unsupported metrics are distinct outcomes.

## Worked example

Request on September 17, 2026: "Across all projects, give me the top five models per user by CU with job counts, a three-month CSV, and a PDF."

1. Resolve the team and an accessible context project. State June 1 through August 31, the last three complete calendar months. Discover the current usage schema if needed.
2. Check the exact cache, including user coverage. On a miss call `usage({team_id:"<selected team>",project_id:"<context project>",scope:"team",start_date:"2026-06-01T00:00:00Z",end_date:"2026-08-31T23:59:59.999Z",include:["modelUsages.daily","entities"],response_format:"json"})`. Placeholders come from discovery.
3. For each consumption identity repeat that query with `user_ids:["<returned identity ID>"]`. Save each complete `{query,response,fetched_at}` envelope. Verify dates, scope, and model-by-model reconciliation. Do not add these user totals to the parent total.
4. Ingest the parent and per-user envelopes, then render with `--rank-by cu --top-models-per-user 5 --pdf`. Return the answer plus full model/monthly CSV and per-user rankings. Subsequent top-three or job-ranked questions reuse these fresh snapshots offline.
5. Render every PDF page to images and inspect layout before delivery; disclose if visual verification is unavailable. Test dashboard filters against known totals. Keep customer artifacts local.

## Common mistakes

- Treating an authentication project as the only possible analytics filter, or assuming team scope grants wider permissions.
- Using an exclusive end date, lifetime assumptions, stale schemas, or pre-fix cached figures.
- Subtracting discounts twice, adding API subsets, or forcing model activity to equal overall consumption.
- Reporting a guessed refund explanation, proportional user/model joins, or partial history as complete usage.
- Calling CU "adoption rate" without a denominator, exposing customer snapshots, or using a non-MCP fallback.
