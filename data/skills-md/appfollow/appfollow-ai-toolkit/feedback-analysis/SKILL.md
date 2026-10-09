---
name: feedback-analysis
description: >
  Analyze app or collection feedback over a window — KPIs with prev-window deltas, rating/volume/
  sentiment trends, anomaly callouts, and ranked top bugs + feature requests — then emit a structured
  findings.json plus a self-contained HTML report. Read-only (never writes). Trigger on "feedback
  report", "how are our reviews", "what are users complaining about", "review trends for <app>".
---

# feedback-analysis

Read `using-appfollow` first. This skill is **read-only** — it never calls a write pair.

## Inputs

- **scope:** an app (`ext_id`+`store`), a whole collection, or a **user-chosen subset of apps from one
  collection** (e.g. "just these 3 apps from my <collection>"). Spanning **multiple** collections in one
  report is not supported yet (deferred).
- **window:** default last 30 days; comparison = the preceding equal period.
- **country / lang** (optional).
- **depth:** `quick` | `standard` | `deep` = `get_reviews` page caps 2 / 5 / 10. **Default `deep`.**
  `quick`/`standard` only on an explicit user request.

## Two tiers, runtime-probed

Read the advertised tool list; pick the plan (toolkit and MCP release trains are decoupled):

- **Tier A (always):** `whoami`, `list_collections`, `list_apps`, `get_reviews`,
  `get_ratings_history`.
- **Tier B (degrade if the probe shows it absent):** `reviews_semantic`, `get_reviews_summary`,
  `get_reviews_ai_summary`.
- **Degradable, app-level (not a probe-gated tier):** `get_gp_console_ratings` — see Gather step B for
  the degrade rule.

## Gather (per app)

0. **Session** (`using-appfollow`).
A. **Scope resolve.** Collection lookup is **mandatory even for a bare ext_id** — `get_ratings_history`
   and `get_reviews_ai_summary` require `collection_name` + `store`. For a subset scope: resolve the
   collection via `list_collections`, list its apps via `list_apps`, then gather data for only the chosen
   subset — emit `scope.type: "collection_subset"` with `collection_name` set and `apps` = the chosen
   subset (not the full collection).
B. **Cheap aggregates first.** One `get_ratings_history` spanning both windows (`period=daily`,
   `type=total`, **explicit `limit`**); split client-side. `get_reviews_summary` × 2 windows (Tier B).
   `get_gp_console_ratings` is degradable — the app may have no Google Play Console connection, or the
   feature may be unavailable server-side. On any error (`VALIDATION_ERROR`, `UNKNOWN_TOOL`, or other),
   or an empty response, omit the GP-console rating signal, note the gap in the report, and continue; the
   App Store rating-history path is unaffected. Never fail the whole analysis on this call.
C. **Narrative.** `get_reviews_ai_summary` (skip on `AUTH_REQUIRED`/`UPSTREAM_ERROR`/`NOT_FOUND`).
   `reviews_semantic` — client-side classification is the first-class fallback. Then `get_reviews` raw
   pages **per app** (`ext_id` — the tool does not accept a collection; loop the scope's apps) up to the
   depth cap; stop early when `reviews.page.next` is null; replan after page-1 `total`; record coverage %.

## Analyze

Follow `references/method.md`: KPIs + deltas; daily-avg + 7-day-rolling trends; the anomaly heuristics
with their explicit thresholds; bug/feature mining (semantic-first, client-side classification the
default fallback). Apply **coverage gating** — demote text-derived findings below the 60% floor to
"indicative only". Ratings-derived findings are never coverage-gated. Group rollup weights by
`rating_cnt` and merges cross-app clusters into `affected_apps`.

## Error rails (`using-appfollow`)

`INSUFFICIENT_CREDITS` → stop, emit a **partial** report + coverage note. `RATE_LIMITED` → one backoff
then continue. `NETWORK_ERROR`/`UPSTREAM_ERROR` on a non-critical call → skip that section, keep going.
Missing Tier-B tool → documented fallback. Never fail the whole report on one tool error.

## Emit

Write `./appfollow-reports/<report_id>/`:

1. **`findings.json`** — `appfollow.toolkit.findings/v1`, `report_type:"feedback"`. Validate it against
   `schemas/findings.schema.json` before writing. Each finding: stable `id`, `type`, `title`,
   `description`, `severity`, `priority_hint`, `affected_apps`, `metrics`, `evidence` (3–5 quotes
   ≤200 chars via review ids — no permalink scheme exists), `suggested_labels`, stable `dedup_key`
   (so re-runs update rather than duplicate), `status:"proposed"`.
2. **`report.html`** — fill `references/report-template.html`; inline SVG charts; no external requests.
3. **`report.md`** — the same content in Markdown.

On Claude Code, also publish the HTML artifact; on Codex, write the files and state their path.

## Findings hand-off

Tell the user their own connected tracker agent can file `findings.json` into their tracker — the
toolkit never talks to a tracker.
