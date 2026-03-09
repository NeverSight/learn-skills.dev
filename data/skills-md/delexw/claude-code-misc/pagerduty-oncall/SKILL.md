---
name: pagerduty-oncall
description: Investigate PagerDuty incidents for Envato on-call escalation policies. Use when asked about incidents, on-call status, incident analysis, or PagerDuty investigation.
argument-hint: "what to investigate (e.g. 'incidents last 24h', 'on-call yesterday', 'incidents today')"
allowed-tools: Bash(pd auth *), Bash(pd ep list *), Bash(pd incident list *), Bash(pd incident log *), Bash(pd incident notes *), Bash(pd incident analytics *), Bash(node *), Bash(mkdir *), Bash(test *), Bash(chmod *), Read, Write, Edit
model: sonnet
context: fork
---

# PagerDuty On-Call Incident Investigator

Authenticate, list escalation policies, fetch all incidents and their details, then analyse relevance across Envato on-call teams.

## Arguments
- `$ARGUMENTS[0]` — What to investigate (e.g. `"incidents last 24h"`, `"on-call yesterday"`, `"incidents today"`, `"incidents 2026-03-01 to 2026-03-05"`). Defaults to `"incidents today"`. Interpret the time range to derive `--since` and `--until` dates (YYYY-MM-DD) in the agent's local timezone (detect via system clock), not UTC. See the date derivation table in Step 5.

## Target Escalation Policies

The list of escalation policies to investigate is resolved in order:
1. `config.json` — `escalation_policies` array in [config.json](config.json)
2. `PD_ESCALATION_POLICIES` — comma-separated env var (e.g. `"On Call, Platform Engineering On-Call"`)
3. If both are empty, all escalation policies are included

## System Requirements
- `pd` CLI installed (https://github.com/martindstone/pagerduty-cli)
- Environment variable `PAGERDUTY_API_TOKEN` set with a valid PagerDuty REST API token. **Important:** When checking this variable, verify at least 2 times before concluding it is not set. Environment variables can appear unset due to shell context differences. **Never expose the value** — use existence checks only (e.g. `test -n "$PAGERDUTY_API_TOKEN"`).

## Scripts

All parsing and filtering is handled by scripts in `${CLAUDE_SKILL_DIR}/scripts/`:

| Script | Purpose |
|--------|---------|
| `extract-json.js` | Extracts JSON from pd CLI output that may contain non-JSON text |
| `filter-eps.js` | Filters EPs by target names, extracts relevant fields |
| `filter-incidents.js` | Filters incidents by service IDs from `ep-list.json`, extracts fields |
| `parse-log.js` | Extracts relevant fields from incident log entries |
| `parse-notes.js` | Extracts relevant fields from incident notes |
| `parse-analytics.js` | Extracts relevant fields from incident analytics |

All scripts read from stdin and write to stdout. Pipe pd CLI output through `extract-json.js` first, then through the appropriate filter/parse script.

## Output Directory

All intermediate JSON and the final report are saved to:

```
.pagerduty-oncall-tmp/
├── ep-list.json              # Filtered escalation policies
├── incidents.json            # Incidents filtered by target EPs
├── logs/<INCIDENT_ID>.json   # Log entries per incident
├── notes/<INCIDENT_ID>.json  # Notes per incident
├── analytics/<INCIDENT_ID>.json # Analytics per incident
└── report.md                 # Final analysis report
```

## Execution

### 1. Verify Connection

Check that `PAGERDUTY_API_TOKEN` is set (verify at least 2 times before concluding it is missing):
```bash
test -n "$PAGERDUTY_API_TOKEN" && echo "TOKEN_SET" || echo "TOKEN_MISSING"
```

If token is set, authenticate:
```bash
pd auth add --token "$PAGERDUTY_API_TOKEN"
```

If authentication fails, use `AskUserQuestion` to inform the user and link to the [PagerDuty CLI User Guide](https://github.com/martindstone/pagerduty-cli/wiki/PagerDuty-CLI-User-Guide) for setup instructions. Do NOT continue until authentication succeeds.

### 2. Prepare Output Directory

Create the output directory `.pagerduty-oncall-tmp/` and subdirectories `logs/`, `notes/`, `analytics/` before saving any files.

### 3. Load Escalation Policy Configuration

Read [config.json](config.json) using the Read tool. Extract the `escalation_policies` array.

If the array is empty, check for the `PD_ESCALATION_POLICIES` env var:
```bash
test -n "$PD_ESCALATION_POLICIES" && echo "$PD_ESCALATION_POLICIES" || echo "EMPTY"
```

Build the list of target EP names for the next step. If both sources are empty, no names will be passed (all EPs included).

### 4. List and Filter Escalation Policies

Fetch, extract JSON, filter by target names, and save in one pipeline:
```bash
pd ep list --json 2>&1 | node ${CLAUDE_SKILL_DIR}/scripts/extract-json.js | node ${CLAUDE_SKILL_DIR}/scripts/filter-eps.js "EP Name 1" "EP Name 2" > .pagerduty-oncall-tmp/ep-list.json
```

Pass each target EP name as a separate argument to `filter-eps.js`. If no target names, omit the arguments (all EPs pass through).

### 5. Fetch and Filter Incidents

Derive `SINCE_DATE` and `UNTIL_DATE` (YYYY-MM-DD) from `$ARGUMENTS[0]` in the agent's local timezone. **Important:** `--until` is **exclusive** in the `pd` CLI — it does NOT include that day. Use this table (assuming today is 2026-03-06):

| Input | SINCE_DATE | UNTIL_DATE | Why |
|-------|-----------|-----------|-----|
| "last 24h" | 2026-03-05 | 2026-03-07 | 24h back from now, until must be tomorrow to include today |
| "today" | 2026-03-06 | 2026-03-07 | until=tomorrow to include today |
| "yesterday" | 2026-03-05 | 2026-03-06 | until=today to include yesterday |
| "last 3 days" | 2026-03-03 | 2026-03-07 | 3 days back, until=tomorrow |
| "2026-03-01 to 2026-03-05" | 2026-03-01 | 2026-03-06 | until=day after end date |

Then fetch, extract JSON, filter by service IDs from `ep-list.json`, and save:
```bash
pd incident list --json --statuses=open --statuses=closed --statuses=triggered --statuses=acknowledged --statuses=resolved --since=SINCE_DATE --until=UNTIL_DATE 2>&1 | node ${CLAUDE_SKILL_DIR}/scripts/extract-json.js | node ${CLAUDE_SKILL_DIR}/scripts/filter-incidents.js .pagerduty-oncall-tmp/ep-list.json > .pagerduty-oncall-tmp/incidents.json
```

Read `.pagerduty-oncall-tmp/incidents.json` to check the result. If the array is empty, write a report noting zero incidents and stop.

### 6. Gather Incident Details

For each incident in `.pagerduty-oncall-tmp/incidents.json`, fetch details **sequentially** (to avoid PagerDuty API rate limits). Use the `id` field (e.g. `Q1V3O5Q3JX39LJ`), NOT `incident_number` — the `pd` CLI only accepts internal IDs.

**Log entries:**
```bash
pd incident log -i <INCIDENT_ID> --json 2>&1 | node ${CLAUDE_SKILL_DIR}/scripts/extract-json.js | node ${CLAUDE_SKILL_DIR}/scripts/parse-log.js > .pagerduty-oncall-tmp/logs/<INCIDENT_ID>.json
```

**Notes:**
```bash
pd incident notes -i <INCIDENT_ID> --output=json 2>&1 | node ${CLAUDE_SKILL_DIR}/scripts/extract-json.js | node ${CLAUDE_SKILL_DIR}/scripts/parse-notes.js > .pagerduty-oncall-tmp/notes/<INCIDENT_ID>.json
```

**Analytics:**
```bash
pd incident analytics -i <INCIDENT_ID> --json 2>&1 | node ${CLAUDE_SKILL_DIR}/scripts/extract-json.js | node ${CLAUDE_SKILL_DIR}/scripts/parse-analytics.js > .pagerduty-oncall-tmp/analytics/<INCIDENT_ID>.json
```

### 7. Analyse and Report

Read all saved JSON files from `.pagerduty-oncall-tmp/` using the Read tool. Produce a structured analysis and save it using Write to `.pagerduty-oncall-tmp/report.md`:

1. **Incident Summary Table** — For each incident: ID, title, service, escalation policy, status, urgency, created/resolved timestamps (current agent's local timezone via system clock, not UTC), duration
2. **Cross-Team Correlation** — Identify incidents that overlap in time across different escalation policies. Flag potential cascading failures or shared root causes
3. **Timeline** — Chronological view of all incidents across all teams in current agent's local timezone, highlighting clusters of activity
4. **Key Findings** — Patterns, recurring services, repeated triggers, or escalation policy gaps
5. **Recommendations** — Actionable suggestions based on the analysis

After writing the report, inform the user of the report location: `.pagerduty-oncall-tmp/report.md`

<tags>
   <mode>think</mode>
   <custom>yes</custom>
</tags>
