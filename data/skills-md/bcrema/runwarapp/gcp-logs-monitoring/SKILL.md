---
name: gcp-logs-monitoring
description: Use when the user needs to inspect Google Cloud (GCP) logs, metrics, and monitoring signals via gcloud for incident triage, debugging, or operational analysis. Supports Cloud Logging queries, Cloud Monitoring time-series reads, and environment checks for a target project.
---

## Goal
Inspect Cloud Logging and Cloud Monitoring data quickly and repeatably from the terminal.

## Inputs to collect (ask only if missing)
- `project_id`
- `time_window` for investigation (for example: last `30m`, `2h`, or explicit UTC `start/end`)
- `service/resource context` (`cloud_run_revision`, `k8s_container`, `gce_instance`, load balancer, etc.)
- `signals of interest` (errors, latency, CPU, memory, request count, restarts)
- `output_format` (`table` for quick scans, `json` for deeper analysis)

## Execution workflow
1. Validate prerequisites:
   `bash .agents/skills/gcp-logs-monitoring/scripts/check_prereqs.sh --project <project_id>`
2. Query Cloud Logging:
   `bash .agents/skills/gcp-logs-monitoring/scripts/read_logs.sh --project <project_id> --filter '<LOG_FILTER>' --freshness 1h --limit 100 --format json`
3. Query Cloud Monitoring time series:
   `bash .agents/skills/gcp-logs-monitoring/scripts/read_metrics.sh --project <project_id> --filter '<METRIC_FILTER>' --start <UTC_ISO8601> --end <UTC_ISO8601> --format json`
4. Correlate timestamps between logs and metrics, then summarize likely root cause and next checks.

## Common filter templates
### Cloud Logging
- Cloud Run errors:
  `resource.type="cloud_run_revision" severity>=ERROR`
- GKE container errors:
  `resource.type="k8s_container" severity>=ERROR`
- HTTP 5xx in load balancer logs:
  `resource.type="http_load_balancer" jsonPayload.statusDetails=~"5.."`
- Timeout text search:
  `textPayload:"timeout" OR jsonPayload.message:"timeout"`

### Cloud Monitoring
- Cloud Run request count:
  `metric.type="run.googleapis.com/request_count" AND resource.type="cloud_run_revision"`
- Cloud Run request latencies:
  `metric.type="run.googleapis.com/request_latencies" AND resource.type="cloud_run_revision"`
- VM CPU utilization:
  `metric.type="compute.googleapis.com/instance/cpu/utilization" AND resource.type="gce_instance"`

## Guardrails
- Prefer passing `--project` on every command instead of changing global gcloud config.
- Start with short windows (`15m` to `2h`) and widen only when needed.
- Use `--format json` when output will be parsed or compared across sources.
- If auth or project checks fail, fix environment first and then re-run queries.
