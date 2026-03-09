---
name: datadog-analyser
description: Analyse Datadog observability data including metrics, logs, monitors, incidents, SLOs, APM traces, RUM, security signals, and more. Use when asked to investigate infrastructure health, query metrics, search logs, check monitors, diagnose errors, or analyse any Datadog data.
argument-hint: "what to analyse (e.g. 'error rate last 1h', 'triggered monitors', 'incidents today')"
allowed-tools: Bash(pup test), Bash(pup auth status), Bash(pup agent *), Bash(pup monitors list *), Bash(pup monitors get *), Bash(pup monitors search *), Bash(pup metrics query *), Bash(pup metrics list *), Bash(pup metrics get *), Bash(pup metrics search *), Bash(pup logs search *), Bash(pup logs list *), Bash(pup logs aggregate *), Bash(pup events list *), Bash(pup events search *), Bash(pup events get *), Bash(pup incidents list *), Bash(pup incidents get *), Bash(pup incidents attachments *), Bash(pup dashboards list *), Bash(pup dashboards get *), Bash(pup dashboards url *), Bash(pup slos list *), Bash(pup slos get *), Bash(pup slos status *), Bash(pup apm *), Bash(pup rum apps *), Bash(pup rum sessions *), Bash(pup rum metrics *), Bash(pup synthetics tests *), Bash(pup synthetics locations *), Bash(pup infrastructure hosts *), Bash(pup error-tracking issues *), Bash(pup service-catalog list *), Bash(pup service-catalog get *), Bash(pup scorecards list *), Bash(pup scorecards get *), Bash(pup security rules list *), Bash(pup security signals list *), Bash(pup security findings *), Bash(pup cicd pipelines *), Bash(pup cicd events *), Bash(pup on-call teams *), Bash(pup cases search *), Bash(pup cases get *), Bash(pup notebooks list *), Bash(pup notebooks get *), Bash(pup misc status), Bash(pup misc ip-ranges), Read, Write, Edit
model: sonnet
context: fork
---

# Datadog Analyser

Investigate and analyse Datadog observability data using the `pup` CLI.

## Arguments
- `$ARGUMENTS[0]` — What to analyse (e.g. `"error rate last 1h"`, `"triggered monitors"`, `"incidents today"`, `"service:api logs"`). Use current agent's local timezone (detect via system clock) for any time-based queries (e.g. "last 1h" means the last hour in current agent's local timezone, not UTC).

## System Requirements
- `pup` CLI installed — see https://github.com/datadog-labs/pup/blob/main/README.md
- `DD_API_KEY` and `DD_APP_KEY` environment variables set. **Important:** When checking these variables, verify at least 2 times before concluding they are not set. Environment variables can appear unset due to shell context differences. **Never expose the values** — use existence checks only (e.g. `test -n "$DD_API_KEY"`).
- `DD_SITE` set if not using `datadoghq.com` (optional)

## Output Directory

```
.datadog-analyser-tmp/
└── report.md    # Final analysis report
```

## Execution

### 1. Verify Connection

Run `pup test` to confirm the CLI is configured and connected:

```bash
pup test
```

If this fails, use `AskUserQuestion` to inform the user that `pup` is not configured or `DD_API_KEY`/`DD_APP_KEY` are not set, and link to the setup guide: https://github.com/datadog-labs/pup/blob/main/README.md

Do NOT continue until `pup test` succeeds.

### 2. Discover Available Commands

Run `pup agent guide` to get the full list of available commands and usage patterns for this session:

```bash
pup agent guide
```

If `pup agent guide` is not available (command not found), use the known command reference below and continue.

### 3. Analyse

Based on `$ARGUMENTS[0]`, determine which `pup` commands are most relevant. Use `--output=json` (default) for all commands to get structured output. Run commands sequentially.

**Common analysis patterns:**

| Goal | Commands |
|------|----------|
| Triggered/alerting monitors | `pup monitors list`, `pup monitors search --query="status:alert"` |
| Error logs | `pup logs search --query="status:error" --from="1h"` |
| Metric trend | `pup metrics query --query="<metric>" --from="<window>"` |
| Active incidents | `pup incidents list` |
| SLO health | `pup slos list`, `pup slos status <id>` |
| APM service health | `pup apm services`, `pup apm dependencies` |
| Security signals | `pup security signals list`, `pup security findings search` |
| Error tracking | `pup error-tracking issues search --query="<service>"` |
| Synthetics failures | `pup synthetics tests list` |
| CI failures | `pup cicd pipelines list`, `pup cicd events list` |

All commands default to JSON output. Use flags like `--from`, `--to`, `--query`, `--tags` to narrow scope. Refer to `pup <command> --help` for available flags.

### 4. Report

All timestamps in the report must use current agent's local timezone (detect via system clock), not UTC.

Write a structured analysis to `.datadog-analyser-tmp/report.md` using the Write tool:

1. **Summary** — Overall health status and key findings
2. **Details** — Breakdown of findings per domain (monitors, logs, metrics, etc.)
3. **Anomalies** — Anything alerting, degraded, or unusual
4. **Recommendations** — Suggested follow-up actions

Inform the user of the report location: `.datadog-analyser-tmp/report.md`

<tags>
  <mode>think</mode>
  <custom>yes</custom>
</tags>
