---
name: kubesense-skills
description: KubeSense observability skills for AI agents — query logs, traces, metrics and real user monitoring (RUM) data from Kubernetes clusters and the apps on them, inspect cluster inventory, manage service level objectives, and generate alert and dashboard configuration.
metadata:
  version: "2.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,observability,kubernetes,logs,traces,metrics,rum,alerts,dashboards,slo,mcp,cloud,aws,gcp,azure
---

# KubeSense Skills

Observability skills for KubeSense, grouped by telemetry surface.

## Skills

| Skill | Description |
|---|---|
| **kubesense-mcp** | The tool layer — connection, auth, the full tool inventory, the WHERE/field-name contract every query skill inherits. Start here. |
| **kubesense-logs** | Search and aggregate logs |
| **kubesense-traces** | Spans, latency percentiles, error rates, distributed-trace waterfalls |
| **kubesense-metrics** | PromQL/MetricsQL over Kubernetes, infrastructure and cloud-provider (AWS/GCP/Azure/Atlas/Confluent/Kong) metrics |
| **kubesense-rum** | Real user monitoring: sessions, page views, web vitals, frontend errors, slow requests from browser and mobile apps |
| **kubesense-spl** | SPL — the piped log query language, and its inverted field contract |
| **kubesense-sql** | Raw ClickHouse SQL over logs and traces — joins, CTEs, window functions |
| **kubesense-infra** | Cluster inventory: clusters, nodes, pods, workloads, infra failures, recent deploys |
| **kubesense-alerts** | List, investigate, and create alert rules; generate import JSON; migrate Datadog monitors |
| **kubesense-dashboards** | Create or edit dashboards, or generate preset JSON to import |
| **kubesense-slo** | Create and manage service level objectives; error budgets, burn-rate alerting, Datadog SLO migration |

## Routing

| The user is asking… | Skill |
|---|---|
| "show me errors / grep the logs" | kubesense-logs |
| "p99 latency / slow requests / which service is failing" | kubesense-traces |
| "CPU, memory, disk, saturation, capacity" | kubesense-metrics |
| "page load time / LCP / frontend errors / crashes / user sessions / slow requests in the browser or app" | kubesense-rum |
| "how is my RDS / EC2 / Azure VM / Atlas cluster doing" | kubesense-metrics |
| "which cloud accounts are connected / why is my AWS dashboard empty" | kubesense-metrics (`list-cloud-integrations`) |
| "what's running / why is this pod restarting / what changed" | kubesense-infra |
| "alert me when… / what's firing / convert this Datadog monitor" | kubesense-alerts |
| "build me a dashboard" | kubesense-dashboards |
| "track an SLO / error budget / port a Datadog SLO" | kubesense-slo |
| a query needing a join, CTE, or window function | kubesense-sql |
| "search the logs with a pipeline" / SPL tab | kubesense-spl |
| "this alert fired — what's wrong?" | kubesense-alerts, then kubesense-infra |
| a tool returned a field-name or WHERE error | kubesense-mcp |

## Prerequisites

Every skill except `kubesense-dashboards`, `kubesense-alerts` and `kubesense-slo`
(which can generate JSON offline) needs the **KubeSense MCP server** connected. Those
three need it for their validate and create tools, and for discovering real metric and
field names — offline they fall back to JSON built from names the user supplies.
`kubesense-slo` has no MCP tools at all: it drives the REST API directly, and uses the
MCP query tools only to discover names.

The MCP server is served by kubeapi at `/mcp` over Streamable HTTP and authenticates
with the same credentials as the REST API.

```bash
claude mcp add --scope user --transport http kubesense \
  https://<your-kubesense-host>/mcp \
  --header "x-api-key: <your-api-key>"
```

See [kubesense-mcp](./kubesense-mcp/SKILL.md) for auth alternatives and verification.

## Two Rules That Apply Everywhere

1. **Discover before querying.** Never invent a field name, metric name, cluster name,
   or label. Every surface has a discovery tool; a guessed name either errors or —
   worse — returns an empty result that reads like "zero".

2. **Field names are catalog labels, not storage columns.** Logs/traces queries take
   `type`, `instance`, `service`, `method`, `status_code` — *not* `level`, `pod_name`,
   `app_service`, `subtype`, `return_code`. The alert engine accepts a **different**
   set. See [kubesense-mcp](./kubesense-mcp/SKILL.md) for the contract and
   [kubesense-alerts](./kubesense-alerts/SKILL.md) for the divergence.

## Install

```bash
npx skills add kubesense-ai/kubesense-mcp-skills --full-depth -y
```

> [!IMPORTANT]
> **`--full-depth` is required.** Without it the installer stops at this root `SKILL.md`
> and installs only this index — 1 skill instead of 12 — with no warning.
>
> If you are reading this as the *only* installed KubeSense skill, that is what happened.
> Re-run the command above with `--full-depth`.

Verify with `npx skills add kubesense-ai/kubesense-mcp-skills --list --full-depth`, which
should report 12 skills. Or pick individual skills — see the [README](./README.md).
