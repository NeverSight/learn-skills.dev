---
name: orca-morning-briefing
description: Daily security briefing summarizing new critical alerts, attack paths, compliance drift, exposure changes, and aging unactioned alerts from the last 24-72 hours. Use when user asks for a briefing, summary, or overview (e.g., "morning briefing", "what happened", "security summary", "daily report", "what needs attention").
trigger: When user asks for a morning briefing, daily summary, overnight changes, security status, what happened overnight, what's new, environment health, or "brief me" (e.g., "morning briefing", "what happened overnight?", "daily security summary", "brief me on the last 72 hours")
---

# Orca Morning Briefing Skill

Answers the question: **"What happened while I was away, and what needs my attention?"**

Provides a security briefing for the last 24-72 hours covering new critical alerts, escalated alerts, attack path changes, compliance drift, exposure changes, CDR activity anomalies, crown jewel risks, and aging unactioned alerts.

## Usage

```
/orca-morning-briefing
/orca-morning-briefing 72h
/orca-morning-briefing week
```

Or natural language:
- "morning briefing"
- "what happened overnight?"
- "brief me on the last 72 hours"
- "daily security summary"
- "what's new since yesterday?"

## Time Range

| Argument | Period | When to Use |
|----------|--------|-------------|
| *(none)* | Last 24 hours | Daily morning check |
| `72h` | Last 3 days | Monday morning / after weekend |
| `week` | Last 7 days | Weekly review / returning from PTO |

Map these to CDR `time_range` enum values:
- 24h → `"last_24_hours"`
- 72h → `"last_3_days"`
- week → `"last_7_days"`

## Processing Logic

### Data Gathering Phase

Run ALL of the following queries in parallel to minimize latency. Do not wait for one to finish before starting the next.

#### Group 1: Alert Queries (via discovery_search)

Run these `discovery_search` queries in parallel:

**Query 1a: New critical alerts**
```
discovery_search:
  search_phrase: "critical open alerts"
  limit: 10
```

**Query 1b: New high alerts**
```
discovery_search:
  search_phrase: "high severity open alerts"
  limit: 10
```

**Query 1c: Alerts on crown jewel assets**
```
discovery_search:
  search_phrase: "open alerts on crown jewel assets"
  limit: 10
```

**Query 1d: Internet-facing assets with critical vulnerabilities**
```
discovery_search:
  search_phrase: "internet facing assets with critical vulnerabilities"
  limit: 10
```

**Query 1e: New attack paths**
```
discovery_search:
  search_phrase: "critical attack paths"
  limit: 10
```

#### Group 2: Compliance Queries

Run these in parallel:

**Query 2a: Current compliance scores**
```
get_enabled_compliance_frameworks:
  (no filters — get all frameworks)
```

**Query 2b: Compliance trend**
```
get_compliance_trend_over_time:
  filters:
    datetime_filter: 7  (or 14/30 depending on time range)
```

**Query 2c: Compliance by account**
```
get_compliance_analysis_by_account_or_business_unit:
  group_by: "accounts"
```

#### Group 3: CDR Activity

Run these in parallel:

**Query 3a: CDR events grouped by action (last 24h)**
```
get_cdr_events_grouped_by_event_name:
  time_range: "last_24_hours"  (or "last_3_days" / "last_7_days")
  page_size: 50
```

**Query 3b: CDR events from unusual sources**
```
search_cdr_events:
  time_range: "last_24_hours"  (or "last_3_days" / "last_7_days")
  limit: 50
```

### Analysis Phase

After all queries return, analyze and synthesize:

#### 1. New Alerts Analysis

From discovery_search results for critical and high alerts:
- Count total new alerts by severity
- Filter to alerts whose `CreatedAt` falls within the requested time window
- For alerts that were already shown in previous briefings but were reopened or escalated, flag as "ESCALATED" or "REOPENED"
- Identify any alert types that appear for the first time (compare alert type names against the full list — if it's the first time this `AlertType` appears, flag as "NEW TYPE")
- Sort by Orca Score descending

#### 2. Attack Path Analysis

From discovery_search attack path results:
- Count attack paths by severity
- Identify any that involve crown jewel assets
- Look for attack paths with stories involving lateral movement, privilege escalation, or data exfiltration

#### 3. Compliance Drift Detection

From compliance framework results:
- Compare current scores against trend data
- Flag any framework that DROPPED in score (even 1%)
- Highlight frameworks below organizational thresholds (e.g., < 90%)
- Identify the account(s) dragging scores down (from account heatmap)

#### 4. CDR Activity Analysis

From CDR event aggregation:
- Identify high-volume event types (top 10 by count)
- Flag events from unusual actors or IP addresses
- Look for patterns suggesting:
  - Bulk resource changes (many Create*/Delete*/Modify* events)
  - Reconnaissance (many Describe*/List*/Get* calls from one actor)
  - Privilege escalation attempts (IAM policy changes, role assumptions)
  - Data access spikes (S3 GetObject, database queries)

Classify CDR activity into:
```
Category            Event Patterns                    Concern Level
────────────────────────────────────────────────────────────────────
Normal operations   Describe*, List*, Get* (read)     LOW
Resource changes    Create*, Put*, Modify*, Update*   MEDIUM
Deletions           Delete*, Remove*, Terminate*      HIGH
IAM changes         Attach*Policy, Create*Role,       HIGH
                    PutRolePolicy, AssumeRole
Security changes    AuthorizeSecurityGroup*,           HIGH
                    PutBucketPolicy, ModifyVpc*
Console logins      ConsoleLogin from new IPs         MEDIUM-HIGH
Root account usage  Any action by root account         CRITICAL
```

#### 5. Exposure Changes

From discovery_search internet-facing results:
- Identify assets that are public-facing with high/critical alerts
- Cross-reference with crown jewel status

#### 6. Crown Jewel Risk

From discovery_search crown jewel results:
- Count alerts on crown jewel assets by severity
- Flag any crown jewel with NEW critical alerts

#### 7. Aging Alert Detection

From all alert results, identify:
- Critical alerts open > 7 days
- Critical alerts open > 30 days (severe aging)
- Alerts that were dismissed and reopened (remediation friction)
- Alerts with Jira tickets stuck in "To Do" status

#### 8. Environment Pulse Calculation

Calculate the overall environment health:

```
IF new_critical_alerts > 0 AND (crown_jewel_affected OR compliance_dropped) THEN
  pulse = "🔴 DEGRADING — immediate attention needed"
ELSE IF new_critical_alerts > 0 OR compliance_dropped THEN
  pulse = "⚠️  NEEDS ATTENTION — new critical findings"
ELSE IF new_high_alerts > 3 THEN
  pulse = "⚠️  ELEVATED — review high-severity queue"
ELSE IF aging_criticals > 0 THEN
  pulse = "⏳ STALE — no new threats but unresolved criticals aging"
ELSE
  pulse = "✅ STABLE — no significant changes"
```

## Output Format

### Layer 1: Dashboard (always shown)

```
═══════════════════════════════════════════════════════════════════
MORNING BRIEFING — <date>
Last <time_range> | <account(s)>
═══════════════════════════════════════════════════════════════════

PULSE: <environment health assessment — 1 line>

┌─────────────────────────────────────────────────────────────────┐
│  NEW ALERTS         <N> total (<X> critical, <Y> high)         │
│  ESCALATED          <N> alerts changed severity or reopened     │
│  ATTACK PATHS       <N> new or worsened                         │
│  COMPLIANCE         <framework> dropped <X>%                    │
│  EXPOSURE           <N> assets newly internet-facing            │
│  CROWN JEWELS       <N> new alerts on critical assets           │
│  AGING CRITICALS    <N> critical alerts open > 7 days           │
│  CDR ACTIVITY       <volume assessment — normal/elevated/spike> │
└─────────────────────────────────────────────────────────────────┘

TOP PRIORITIES:
  [1] <alert-id> — <title> (<score>, <age>)
  [2] <alert-id> — <title> (<score>, <age>)
  [3] <alert-id> — <title> (<score>, <age>)
  [4] <alert-id> — <title> (<score>, <age>)
  [5] <alert-id> — <title> (<score>, <age>)

═══════════════════════════════════════════════════════════════════
Type a keyword to drill down: alerts | escalated | attack paths |
compliance | exposure | crown jewels | aging | activity |
new types | trends | full
═══════════════════════════════════════════════════════════════════
```

The TOP PRIORITIES list should be ordered by:
1. New critical alerts on crown jewel or public-facing assets
2. New critical alerts (by Orca Score descending)
3. Escalated alerts (severity increased)
4. Reopened alerts that were previously dismissed
5. Aging critical alerts (oldest first)

Show up to 5 items. If fewer than 5 priorities, show fewer.

### Layer 2: Drill-Down Sections

When user types a keyword, show the expanded section:

#### "alerts" — New Alerts Detail

```
───────────────────────────────────────────────────────────────────
NEW ALERTS — last <time_range>
───────────────────────────────────────────────────────────────────

CRITICAL (<N>):
  <alert-id>  <score>  <title>
              <asset> in <account> | <age> | <labels>

  <alert-id>  <score>  <title>
              <asset> in <account> | <age> | <labels>

HIGH (<N>):
  <alert-id>  <score>  <title>
              <asset> in <account> | <age> | <labels>

  ...

NEW ALERT TYPES (first time in environment):
  ⚡ <alert-type> — never seen before (orca-XXXX on <asset>)

───────────────────────────────────────────────────────────────────
Triage any alert: /orca-alert-triage <alert-id>
───────────────────────────────────────────────────────────────────
```

#### "escalated" — Escalated Alerts

```
───────────────────────────────────────────────────────────────────
ESCALATED ALERTS — last <time_range>
───────────────────────────────────────────────────────────────────

SEVERITY INCREASED:
  <alert-id>  <old-level> → <new-level>  <title>
              Reason: <score vector change>

REOPENED (was closed/dismissed):
  <alert-id>  dismissed → open  <title>
              <asset> | originally opened <date>

───────────────────────────────────────────────────────────────────
```

#### "attack paths" — Attack Path Changes

```
───────────────────────────────────────────────────────────────────
ATTACK PATHS — last <time_range>
───────────────────────────────────────────────────────────────────

NEW ATTACK PATHS:
  [!] <score>  <attack path story — 1 line>
      Assets: <list> | Kill chain: <step count>
      Crown jewel involved: YES/NO

WORSENED:
  [↑] <score>  <attack path story>
      Change: <what got worse>

───────────────────────────────────────────────────────────────────
```

#### "compliance" — Compliance Drift

```
───────────────────────────────────────────────────────────────────
COMPLIANCE POSTURE — last <time_range>
───────────────────────────────────────────────────────────────────

FRAMEWORK SCORES:
  Framework                Score    7-Day Trend    Status
  ─────────────────────────────────────────────────────────
  PCI DSS v4.0.1           87%      ↓ -2%         ⚠ DROPPED
  NIST 800-53              93%      → 0%          ✓ STABLE
  SOC 2                    95%      ↑ +1%         ✓ IMPROVING
  CIS AWS v3.0             81%      ↓ -1%         ⚠ DROPPED

WORST ACCOUNTS:
  <account>  —  <score>% avg across frameworks
  <account>  —  <score>% avg across frameworks

NEW FAILING CONTROLS:
  <framework>: <control> — <N> assets failing
  ...

───────────────────────────────────────────────────────────────────
```

#### "exposure" — Exposure Changes

```
───────────────────────────────────────────────────────────────────
EXPOSURE — Internet-Facing Assets with Critical Alerts
───────────────────────────────────────────────────────────────────

  <asset> (<type>) in <account>
    Public IP: <ip>
    Critical alerts: <N> | Orca Score: <score>
    Crown jewel: YES/NO

  <asset> (<type>) in <account>
    ...

───────────────────────────────────────────────────────────────────
```

#### "crown jewels" — Crown Jewel Risk

```
───────────────────────────────────────────────────────────────────
CROWN JEWEL ALERTS — last <time_range>
───────────────────────────────────────────────────────────────────

  <asset> (crown jewel score: <N>)
    Reason: <why it's a crown jewel>
    New alerts: <N> (<severity breakdown>)
    Top alert: <alert-id> — <title> (score: <X>)

  ...

───────────────────────────────────────────────────────────────────
```

#### "aging" — Unactioned Aging Alerts

```
───────────────────────────────────────────────────────────────────
AGING ALERTS — Critical Alerts Needing Attention
───────────────────────────────────────────────────────────────────

CRITICAL > 30 DAYS (urgent):
  <alert-id>  <age>d  <title>
              <asset> | Jira: <ticket> (<status>)

CRITICAL > 7 DAYS:
  <alert-id>  <age>d  <title>
              <asset> | Jira: <ticket> (<status>)

DISMISSED → REOPENED (remediation friction):
  <alert-id>  <title>
              dismissed <date>, reopened <date>

JIRA STUCK:
  <alert-id>  Jira <ticket> in "<status>" for <N> days
              <title>

───────────────────────────────────────────────────────────────────
```

#### "activity" — CDR Activity Overview

```
───────────────────────────────────────────────────────────────────
CDR ACTIVITY — last <time_range>
───────────────────────────────────────────────────────────────────

VOLUME: <total events> events (<assessment>)

TOP EVENTS BY VOLUME:
  <event_name>            <count>   <assessment>
  <event_name>            <count>   <assessment>
  ...

HIGH-INTEREST ACTIVITY:
  [!] <description of suspicious pattern>
      Actor: <identity> | Count: <N> | Service: <service>

  [!] <description>
      ...

UNUSUAL ACTORS (if any):
  <actor> — <N events>, services: <list>
  First seen in this period: YES/NO

───────────────────────────────────────────────────────────────────
```

#### "new types" — First-Time Alert Types

```
───────────────────────────────────────────────────────────────────
NEW ALERT TYPES — First Time in Environment
───────────────────────────────────────────────────────────────────

  ⚡ <alert-type>
    First occurrence: <alert-id> on <asset>
    Severity: <level> | Score: <X.X>
    What it means: <1-line explanation>

  ⚡ <alert-type>
    ...

(If none): No new alert types detected in this period.

───────────────────────────────────────────────────────────────────
```

#### "trends" — Week-Over-Week Trends

```
───────────────────────────────────────────────────────────────────
TRENDS — Environment Over Time
───────────────────────────────────────────────────────────────────

ALERT TREND (7-day):
  Day         Critical  High  Medium  Total
  ──────────────────────────────────────────
  Mon Apr 14     2       5      12     19
  Tue Apr 15     1       3       8     12
  ...
  Today          3       4       5     12

DIRECTION: <improving / degrading / stable>

TOP 5 MOST-AFFECTED ASSETS:
  <asset>  —  <N> open alerts (<X> critical)
  <asset>  —  <N> open alerts (<X> critical)
  ...

TOP 3 MOST-AFFECTED ACCOUNTS:
  <account>  —  <N> critical alerts, compliance: <score>%
  ...

───────────────────────────────────────────────────────────────────
```

#### "full" — Everything Expanded

Show all sections above in order:
1. Dashboard (repeated for context)
2. New Alerts
3. Escalated
4. Attack Paths
5. Compliance
6. Exposure
7. Crown Jewels
8. Aging
9. Activity
10. New Types
11. Trends

This is the "report mode" — useful for sharing with the team or pasting into a status update.

## Edge Cases

### No New Alerts

If no new critical/high alerts in the time window:

```
PULSE: ✅ STABLE — no new critical or high alerts

NEW ALERTS: 0 critical, 0 high
  (Last critical alert was <N> days ago: <alert-id>)
```

Still show aging alerts, compliance, and CDR activity — the absence of new alerts doesn't mean everything is fine.

### discovery_search Returns Partial Data

`discovery_search` is limited to 10 results per query. If results are capped:
- Note "showing top 10 of potentially more"
- Include the Orca UI URL for the full filtered view when available (from `app_url` in results)
- For alert counts, qualify with "at least N" rather than exact numbers

### No Compliance Frameworks Enabled

If `get_enabled_compliance_frameworks` returns empty:

```
COMPLIANCE: No frameworks enabled.
  Consider enabling PCI DSS, SOC 2, or CIS benchmarks.
```

### CDR Not Configured

If CDR queries return 0 events:

```
CDR ACTIVITY: No events found.
  Possible reasons:
  • CloudTrail / audit log ingestion not configured
  • CDR not enabled for this account
```

### First Briefing (No Baseline)

On the first run, there's no historical baseline to compare against. Note this:

```
Note: This is the first briefing for this environment.
Future briefings will show trends and comparisons.
```

## MCP Tools Used

### Primary Tools (always called)

| Tool | Purpose | Briefing Section |
|------|---------|-----------------|
| `discovery_search` | Find new critical alerts | New Alerts, Crown Jewels, Exposure |
| `discovery_search` | Find new high alerts | New Alerts |
| `discovery_search` | Find crown jewel alerts | Crown Jewels |
| `discovery_search` | Find exposed assets | Exposure |
| `discovery_search` | Find attack paths | Attack Paths |
| `get_enabled_compliance_frameworks` | Current compliance scores | Compliance |
| `get_compliance_trend_over_time` | Score trends (7/14/30 days) | Compliance, Trends |
| `get_cdr_events_grouped_by_event_name` | Event volume by action type | CDR Activity |

### Secondary Tools (called for drill-downs)

| Tool | Purpose | When Called |
|------|---------|------------|
| `get_compliance_analysis_by_account_or_business_unit` | Account-level compliance breakdown | "compliance" drill-down |
| `get_compliance_framework_control_tests` | Failing controls per framework | "compliance" drill-down |
| `search_cdr_events` | Detailed event inspection | "activity" drill-down |
| `get_alert` | Full alert details | When user triages from briefing |
| `get_asset_crown_jewel_info` | Crown jewel status for specific asset | "crown jewels" drill-down |
| `get_framework_assets_with_failed_controls_count` | Worst assets per framework | "compliance" drill-down |

### Tool Parameter Reference

#### discovery_search
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search_phrase` | string | Yes | Natural language query |
| `limit` | integer (1-10) | No | Max results (default: 5) |

#### get_enabled_compliance_frameworks
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filters` | object | No | Contains `datetime_filter` (7/14/30), `providers`, `accounts`, `framework_ids`, etc. |

#### get_compliance_trend_over_time
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filters` | object | No | Same shape as compliance frameworks filters |

#### get_compliance_analysis_by_account_or_business_unit
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `group_by` | enum | No | `"accounts"` or `"business_units"` (default: `"business_units"`) |
| `framework_ids` | array | No | Filter to specific frameworks |

#### get_cdr_events_grouped_by_event_name
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `time_range` | enum | Yes | `"last_1_hour"`, `"last_24_hours"`, `"last_3_days"`, `"last_7_days"`, `"last_30_days"` |
| `cloud_providers` | array | No | Filter by provider |
| `accounts` | array | No | Filter by account |
| `actors` | array | No | Filter by actor |
| `services` | array | No | Filter by service |
| `page_size` | integer (1-100) | No | Results per page (default: 15) |

#### search_cdr_events
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `time_range` | enum | Yes | Same as above |
| `actors` | array | No | Filter by actor ARNs |
| `targets` | array | No | Filter by target resources |
| `services` | array | No | Filter by service |
| `actions` | array | No | Filter by event name |
| `source_ip_addresses` | array | No | Filter by source IP |
| `limit` | integer (1-100) | No | Max events (default: 20) |

**All array parameters must be arrays**, even for single values: `["value"]` not `"value"`.

## Implementation Notes

1. **Parallelize everything** — run all Group 1, 2, and 3 queries simultaneously. The briefing should complete in a single round of parallel MCP calls.
2. **discovery_search is capped at 10 results** — qualify counts with "at least N" and include Orca UI URLs for full views.
3. **Time filtering** — `discovery_search` does not have an explicit time parameter. Use time-related language in the search phrase (e.g., "critical alerts created in the last 24 hours"). For CDR and compliance tools, use their native time filters.
4. **Alert deduplication** — the same alert may appear in multiple discovery_search results (e.g., a critical alert on a crown jewel). Deduplicate by alert_id before counting.
5. **Compliance trend interpretation** — `get_compliance_trend_over_time` returns data points over time. Compare the latest score against the score from N days ago to calculate drift.
6. **CDR volume assessment** — without historical baselines, use absolute thresholds:
   - < 100 events/day → LOW
   - 100-1000 events/day → NORMAL
   - 1000-10000 events/day → ELEVATED
   - \> 10000 events/day → HIGH VOLUME
   These are rough guidelines — adjust based on environment size.
7. **Keep the dashboard under 25 lines** — the whole point is quick scanning. Details go in drill-downs.
8. **Top priorities list** — always show the single most important thing to do first. This is the briefing's core value.
9. **Link to other skills** — when showing alerts in drill-downs, suggest `/orca-alert-triage <alert-id>` for investigation, `/orca-impact-analysis <alert-id>` for remediation planning, and `/orca-config-origin <alert-id>` for ownership.
