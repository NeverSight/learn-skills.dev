---
name: geo-metrics-tracker
description: >
  Real-time GEO metrics monitoring and alerting orchestrator. Use this skill whenever the user
  wants to track, visualize, and react to AI GEO performance metrics over time — especially
  AIGVR (AI-generated visibility rate), SoM (Share of Model), AI citation volume, and related
  indicators across ChatGPT, Perplexity, Gemini, Claude, SGE, and other generative engines.
  Prefer this skill whenever the request goes beyond a static report and instead focuses on
  ongoing dashboards, time-series tracking, anomaly detection (sudden spikes/drops), or building
  an internal “GEO metrics command center.” It is designed to complement `geo-report-builder`
  by turning one-off analyses into a continuous monitoring system.
---

# GEO Metrics Tracker

An orchestration skill for **GEO core-metrics monitoring and alerting** that turns static GEO
analysis into a **living, time-based observability system**.

This skill focuses on:

1. Defining a **GEO metrics catalog** (AIGVR, SoM, citation volume, coverage, etc.)
2. Designing **tracking schemas, storage, and instrumentation plans**
3. Building **dashboards and views** for different stakeholders
4. Setting up **alerts and anomaly detection rules** (spikes/drops, trend breaks)
5. Establishing **operational routines** (daily/weekly reviews, incident playbooks)

It does **not** directly pull data from third-party tools or models. Instead, it:

- Designs the **system** (what to log, where, how often, and how to wire tools together)
- Produces **schemas, dashboard specs, alert conditions, and workflows** that a team can implement
- Helps translate GEO strategy into **measurable, monitorable signals**

---

## When to use this skill

Invoke this skill **whenever**:

- The user wants to **continuously track GEO performance**, not just receive a one-time report:
  - “Set up a dashboard for AIGVR / SoM / citations over time”
  - “Alert me when our AI mentions suddenly spike or drop”
  - “Build a control tower for GEO metrics”
- The user mentions:
  - **AIGVR / SoM / citation volume / mentions / AI traffic** as KPIs
  - **Real-time / near-real-time monitoring**, **dashboards**, **time-series**, **alert rules**
  - “Watch for sudden changes in AI-driven traffic or citations”
- The user already has (or plans to have) some GEO measurement signals from:
  - Log files, analytics tools, third-party GEO trackers, manual sampling, or custom scripts
  - Periodic snapshots generated via `geo-report-builder` or similar skills

This skill is especially relevant if the user says things like:

- “Our AI citations suddenly dropped — how do we monitor this properly?”
- “We want a daily GEO metrics board for leadership”
- “Turn our GEO reports into a live dashboard, with alerts on big changes”

Do **not** limit triggering only to the exact keywords above; trigger whenever the **intent** is:
“Design or improve an ongoing GEO metrics tracking and alert system for AI visibility.”

---

## Relationship to other GEO skills

This skill should **coordinate with** (not replace) other GEO skills:

- `geo-report-builder`:
  - Use its static reports as **inputs** or **snapshots** for trend lines and baselines.
  - Extend its one-off analyses into **time-series views**, **rolling windows**, and **alerts**.
- `geo-studio`:
  - Use its strategic priorities to **decide which metrics and entities matter most**.
  - Align dashboards and alerts with target intents, entities, and products.
- `geo-content-optimizer` / `geo-content-publisher`:
  - Feed their content launches into **“experiment timelines”** and post-launch tracking views.
- `geo-site-audit`:
  - Turn audit results into **monitored checks** (e.g., schema presence, llms.txt coverage over time).

If these skills are not present, still follow the same **monitoring shape** and clearly explain:

- What should be measured
- Where data is expected to come from
- How to structure the tracking and alerting system

---

## Core concepts & metrics

When designing the monitoring system, consistently define and use the following concepts:

- **AIGVR (AI-Generated Visibility Rate)**:
  - Share of relevant AI answers (for a given intent/topic) where the brand/site is:
    - Explicitly cited (URL, brand name, product name)
    - Or clearly used as the primary information source
  - Often measured as: \[brand-mentions or links in sampled answers\] / \[total sampled answers\].

- **SoM (Share of Model)**:
  - Analogous to “share of voice” but for **model-generated answers**.
  - Measures how often the brand is chosen or cited **relative to competitors** for the same intent.
  - Can be approximated by:
    - Proportion of answers where the brand appears vs. competitors
    - Ranking / prominence of the brand vs. others.

- **Citation volume**:
  - Absolute count of **AI-generated citations** (links, brand mentions, product references) over time.
  - Can be broken down by:
    - Platform (ChatGPT, Perplexity, Gemini, Claude, SGE, etc.)
    - Intent / query cluster
    - Geography, language, product line.

- **Coverage & footprint**:
  - Number of **intents / queries / entities** where the brand appears at all.
  - Useful for understanding **breadth** vs. **depth**.

- **Latency & change detection**:
  - How quickly AI models react to:
    - New content
    - Content updates
    - Major site or schema changes.
  - Useful for evaluating the effectiveness of GEO operations.

You do **not** need to impose a single rigid formula for each metric. Instead:

- Clearly document **how the user currently measures** (if they have a definition)
- If they don’t, propose **1–2 reasonable options** and explain trade-offs
- Make sure the **tracking schema and dashboards** can support evolution of definitions over time

---

## High-level workflow

When this skill is invoked, follow this **8-step workflow** unless the user explicitly asks for only
a subset.

### 1. Clarify monitoring goals and scope

Briefly but explicitly identify:

- **Primary monitoring goals**:
  - e.g., “detect sudden drops in AIGVR for our core product queries”
  - “give leadership a weekly SoM dashboard for our top 50 intents”
- **Key entities and intents**:
  - Products, features, categories, brand-level topics
  - Priority query clusters or use-cases
- **Target platforms**:
  - ChatGPT, Perplexity, Gemini, Claude, Google SGE, others (specify which matter most)
- **Time resolution**:
  - Real-time / near-real-time, daily, weekly, monthly
- **Systems in play**:
  - Analytics tools, data warehouse / lake, BI tools, spreadsheets, internal scripts

Output a short **“Monitoring Brief”** section summarizing this in 5–10 bullet points.

### 2. Design the GEO metrics catalog

Create a **metrics catalog** that is:

- Focused on **few, high-signal core metrics** (AIGVR, SoM, citations, coverage)
- Broken down by **dimensions** that matter:
  - Platform, intent cluster, geography, language, product line, funnel stage
- Explicit about **granularity**:
  - Per-intent / per-entity vs. aggregated
  - Rolling windows (7/30/90 days) vs. point-in-time snapshots

Output as a **markdown table**, e.g.:

```markdown
| Metric           | Description                                   | Formula / Approximation                          | Dimensions                    | Cadence |
|------------------|-----------------------------------------------|--------------------------------------------------|-------------------------------|---------|
| AIGVR            | AI-generated visibility rate                  | brand-answers / total sampled answers            | platform, intent, locale      | weekly  |
| SoM              | Share of Model vs. competitors                | brand answers / all brand+competitor answers     | platform, intent, competitor  | weekly  |
| Citation Volume  | Count of AI citations of our brand/resources  | number of links/mentions in sampled outputs      | platform, page, intent        | daily   |
| Intent Coverage  | # of intents where we appear at all          | count of intents with ≥1 brand citation          | platform, intent cluster      | monthly |
```

Where the user already has internal metric names, map them into this table and keep both labels.

### 3. Define tracking schema & storage

Design the **data model** for storing GEO metrics:

- Recommend one or more storage options:
  - Data warehouse tables (e.g., BigQuery, Snowflake, Redshift, Postgres)
  - Analytics tool custom events / properties
  - Spreadsheet or Notion tables (for early-stage teams)
- For each chosen storage option, define:
  - **Table / sheet names**
  - **Columns / fields** with types and descriptions
  - **Primary keys** (e.g., date + platform + intent + brand)
  - How to handle **versions** and **late-arriving data**

Output:

- A section `## Tracking Schema & Storage` containing:
  - 1–3 **schema tables** in markdown, each with:
    - Column name
    - Type
    - Description
  - Example **rows** or pseudo-SQL / pseudo-JSON illustrating how a daily record looks.

### 4. Map data sources & collection methods

For each metric and platform, design the **data collection plan**:

- Identify **data sources**:
  - Manual sampling (periodically querying AI tools and recording answers)
  - Third-party GEO monitoring tools or APIs (if user mentions any)
  - Internal logs (AI assistant logs, search logs, clickstream)
  - Outputs from `geo-report-builder` (periodic static snapshots)
- For each source, specify:
  - **Collection method**: manual workflow, automated script, scheduled job, API integration
  - **Frequency**: hourly/daily/weekly/etc.
  - **Responsibility**: which team/role is likely to own it
  - **Data quality checks**: basic sanity checks, deduplication, missing-value handling

Output:

- A section `## Data Sources & Collection` with:
  - A markdown table mapping **Metric → Source → Method → Frequency → Owner**
  - Optional pseudo-code or high-level scripts for key automation points (no real secrets or tokens).

### 5. Design dashboards & views

Translate the metrics and schema into **practical dashboards** for different audiences:

- **Executive / leadership view**:
  - 3–7 top-line KPIs (AIGVR, SoM, coverage, trend over last 30/90 days)
  - Simple traffic-light or threshold-based indicators (above/below target)
- **GEO/SEO/marketing operations view**:
  - More detailed breakdown by intent, platform, and content asset
  - Launch timelines overlaid with metrics (to see **cause and effect**)
- **Experiment / campaign view**:
  - Per-experiment panels showing pre/post metrics and uplift

Output:

- A section `## Dashboards & Views` that includes:
  - A markdown list of **recommended dashboards**, each with:
    - Purpose
    - Primary users
    - Key charts / widgets (described in plain language)
  - If the user mentions a BI tool (e.g., Looker, Metabase, Power BI, Tableau, Data Studio):
    - Suggest concrete **chart types**, dimensions, and filters for that tool.

### 6. Define alerts & anomaly detection rules

Design **alerts** so the team is notified when something important changes:

- For each core metric, define:
  - **What events matter**: sudden spike, sharp drop, slow drift, crossing a threshold
  - **Detection logic**:
    - Simple thresholds (e.g., “AIGVR < 0.3 for 3 days”)
    - Relative changes (e.g., “>30% drop vs. 7-day average”)
    - Outlier detection (if the user has ML/analytics capability)
  - **Alert channels**:
    - Email, Slack/Teams, incident management tools, dashboards with highlight panels
  - **Severity tiers**:
    - Info / Warning / Critical

Output:

- A section `## Alerts & Anomaly Rules` with:
  - A table listing **Metric → Condition → Severity → Channel → Notes**
  - Example configurations in pseudo-YAML / pseudo-JSON that a data engineer could translate into:

```markdown
```yaml
alert: low_aigvr_core_intents
metric: aigvr
scope: [platform: "ChatGPT", intent_cluster: "core-product"]
condition: "current_3d_avg < 0.7 * previous_14d_avg"
severity: critical
channel: "Slack #geo-alerts"
```
```

### 7. Establish operational routines & playbooks

Define **how the team should use the dashboards and alerts**:

- **Cadences**:
  - Daily check: quick scan of key dashboards and alerts
  - Weekly/bi-weekly review: deeper dive into trends, experiments, and incidents
  - Monthly/quarterly retro: adjustments to metrics, targets, and tooling
- **Playbooks**:
  - What to do when:
    - AIGVR drops significantly for a key intent
    - SoM falls vs. a specific competitor
    - Citation volume suddenly spikes (positive anomaly)
  - How to **tie actions back** to content, schema, or distribution changes

Output:

- A section `## Operational Routines` that includes:
  - A checklist-style **runbook** for daily/weekly/monthly workflows
  - 1–3 short **incident playbooks** (“If X happens, do Y and Z”).

### 8. Integrate with GEO reports and strategy

Show how this monitoring layer fits into the broader GEO system:

- Connect to `geo-report-builder`:
  - Use its reports as **snapshots** that can be logged and compared over time.
  - Suggest which sections or metrics from reports should be **logged into the tracking schema**.
- Connect to `geo-studio` and `geo-content-*` skills:
  - Use monitoring insights to **prioritize new content**, **optimize underperformers**, or
    **double-down on winners**.
- Close the loop:
  - Define how periodic reports and real-time dashboards should **inform each other**.

Output:

- A section `## Integration with GEO Strategy` that:
  - Summarizes feedback loops between monitoring and execution
  - Lists **3–7 concrete examples** of how a change in metrics should trigger GEO actions.

---

## Output format

Unless the user explicitly requests a different format, structure your answer as:

1. `## Monitoring Brief`
2. `## Metrics Catalog`
3. `## Tracking Schema & Storage`
4. `## Data Sources & Collection`
5. `## Dashboards & Views`
6. `## Alerts & Anomaly Rules`
7. `## Operational Routines`
8. `## Integration with GEO Strategy`

Use:

- **Markdown headings and tables** for structure
- Bulleted lists instead of dense paragraphs
- Short, actionable sentences suitable for copying into dashboards/BI briefs, runbooks, or tickets

If the user only asks for a **subset** (e.g., “just define metrics and alerts for AIGVR”), still keep
the headings but clearly mark skipped sections (e.g., “Not in scope for this request”).

---

## Examples of triggering prompts

These are **example user prompts** that should trigger this skill (for reference; not user-facing):

- “We already use geo-report-builder once a month. Help us design a real-time GEO metrics dashboard
  for AIGVR and SoM, with alerts when our AI citations spike or crash.”
- “Our Perplexity citations suddenly fell off a cliff last week. Can you help us set up a system to
  monitor AI citation volume across ChatGPT/Perplexity/Gemini and alert us on future drops?”
- “Leadership wants a weekly ‘AI visibility health’ board. Design the metrics, tables, dashboards,
  and alert rules so we can track SoM and AIGVR for our top 50 intents.”
- “We’re launching several GEO campaigns each month. Build a monitoring framework that ties campaign
  launches to changes in AI citations, SoM, and coverage over time.”

You do **not** need to surface this list directly to the user; it is here to clarify intent.

---

