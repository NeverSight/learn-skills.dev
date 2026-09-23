---
name: openobserve
description: "OpenObserve (O2) — open-source observability platform for logs, metrics, traces, dashboards, alerts, and Real User Monitoring. Use when setting up OpenObserve (Docker, binary, Kubernetes), ingesting logs/metrics/traces via HTTP API, OpenTelemetry, Fluent Bit, Vector, or Prometheus remote_write, configuring streams and organizations, building dashboards, setting up alerts, integrating with OTEL Collector, or migrating from Elasticsearch, Datadog, or the Grafana/Loki/Prometheus stack. Fetch live documentation for up-to-date details."
---

# OpenObserve

> **CRITICAL: Your training data for OpenObserve is unreliable.** APIs change between versions and memorized patterns may be wrong or deprecated. Before writing any code, you MUST use `WebFetch` to read the live docs:
>
> **`WebFetch("https://openobserve.ai/docs/quickstart/")`**
>
> For specific topics (ingestion, alerts, pipelines, OTEL integration), fetch the relevant page from `https://openobserve.ai/docs/`. Do not proceed without fetching first.

OpenObserve (O2) is a cloud-native observability platform built in Rust for logs, metrics, traces, dashboards, alerts, and Real User Monitoring — a self-hostable alternative to Datadog, Elasticsearch/Kibana, Splunk, and the Grafana/Loki/Prometheus stack. It achieves 140x lower storage costs than Elasticsearch through Parquet columnar storage and S3-native architecture.

## Key Capabilities

OpenObserve consolidates what typically requires multiple tools into a single binary:

- **Unified observability**: Logs, metrics, traces, RUM, dashboards, alerts, and pipelines — no separate Loki, Prometheus, Tempo, and Grafana to stitch together
- **140x lower storage cost**: Parquet columnar format + S3-native design vs Elasticsearch hot/warm/cold tiers
- **SQL + PromQL**: Query logs and traces with SQL, metrics with SQL or PromQL — no proprietary language
- **OpenTelemetry native**: Built-in OTLP support for traces, metrics, and logs — no vendor lock-in
- **Stream auto-creation**: Streams (equivalent to indices/tables) are created automatically on first ingest — no schema pre-definition required
- **Ingest pipelines**: Enrich, redact, reduce, or transform data at ingest time — no external stream processor needed
- **Multi-tenancy via organizations**: Organizations are first-class concepts with complete data isolation — every API endpoint is scoped to an org
- **Single binary deployment**: Runs in under 2 minutes with no cluster configuration — scales to terabytes in single-node mode, petabytes in HA mode
- **Immutable data**: Ingested records cannot be modified or deleted individually — only full retention periods can be dropped (by design, for audit integrity)

## Ingestion Quick Reference

### HTTP JSON (curl)
```bash
# Endpoint pattern: /api/{organization}/{stream_name}/_json
curl -u 'root@example.com:Complexpass#123' \
  -H 'Content-Type: application/json' \
  http://localhost:5080/api/default/my_stream/_json \
  -d '[{"level":"info","message":"hello","_timestamp":1697000000000000}]'
```

### Fluent Bit (HTTP output plugin)
```
[OUTPUT]
  Name             http
  Match            *
  URI              /api/{organization}/{stream}/_json
  Host             localhost
  Port             5080
  tls              Off
  Format           json
  Json_date_key    _timestamp
  Json_date_format iso8601
  HTTP_User        root@example.com
  HTTP_Passwd      password
```

### Fluent Bit (Elasticsearch-compatible output)
```
[OUTPUT]
  Name              es
  Match             *
  Path              /api/{organization}
  Host              localhost
  index             {stream}
  Port              5080
  tls               Off
  Suppress_Type_Name On
  HTTP_User         root@example.com
  HTTP_Passwd       password
```

### Prometheus remote_write
```yaml
remote_write:
  - url: http://localhost:5080/api/default/prometheus/api/v1/write
    queue_config:
      max_samples_per_send: 10000
    basic_auth:
      username: root@example.com
      password: password
```

### OpenTelemetry traces (OTLP HTTP)
```
POST /api/{organization}/traces
```
Configure your OTEL exporter to target `http://localhost:5080/api/{org}/` with basic auth headers.

## Docker Quick Start
```bash
docker run -d \
  --name openobserve \
  -v $PWD/data:/data \
  -p 5080:5080 \
  -e ZO_ROOT_USER_EMAIL="root@example.com" \
  -e ZO_ROOT_USER_PASSWORD="Complexpass#123" \
  public.ecr.aws/zinclabs/openobserve:latest
```
UI is available at `http://localhost:5080`. Default org is `default`.

## Key Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `ZO_ROOT_USER_EMAIL` | — | Root user email (required on first start) |
| `ZO_ROOT_USER_PASSWORD` | — | Root user password (required on first start) |
| `ZO_DATA_DIR` | `./data/openobserve/` | Local data directory |
| `ZO_S3_PROVIDER` | — | Object storage provider: `aws`, `gcs`, `minio`, `swift` |
| `ZO_S3_SERVER_URL` | — | S3-compatible endpoint (required for MinIO/GCS) |
| `ZO_S3_BUCKET_NAME` | — | Storage bucket name |
| `ZO_S3_ACCESS_KEY` | — | Object storage access key |
| `ZO_S3_SECRET_KEY` | — | Object storage secret key |
| `ZO_S3_REGION_NAME` | — | Cloud region |
| `ZO_MEMORY_CACHE_ENABLED` | `true` | In-memory file caching |
| `ZO_DISK_CACHE_ENABLED` | `true` | Disk-based query caching |

## Best Practices

- **The `_timestamp` field must be microseconds (not milliseconds or seconds).** OpenObserve expects the `_timestamp` field in microseconds since Unix epoch. Sending milliseconds produces incorrect time ordering (data appears 1000x too old) without any error or warning. If omitted, OpenObserve auto-generates `_timestamp` at ingest time — but if your log already has a time field, map it explicitly and convert to microseconds. In Fluent Bit, set `Json_date_format iso8601` and `Json_date_key _timestamp` and let OpenObserve parse ISO 8601, which avoids manual epoch conversion.

- **Streams are created automatically on first ingest — schema is inferred, not enforced.** Sending data to `/api/default/my_stream/_json` creates the `my_stream` stream automatically if it does not exist. There is no `PUT /stream` step. The downside: if your first batch has inconsistent field types (e.g., `level` as integer in one record, string in another), the inferred schema may cause later query failures. Send a consistent payload on first ingest or define the schema explicitly in the UI before ingesting.

- **Every API endpoint is scoped to an organization — omitting or misspelling the org name creates a second isolated org.** The URL pattern `/api/{organization}/{stream}/_json` requires the correct org slug. The default org created on first start is `default`. If you typo the org (e.g., `/api/Default/` vs `/api/default/`), OpenObserve silently creates a new org and the data is invisible in the intended org's UI. Verify the org slug in the UI under IAM before configuring collectors.

- **Do not use local disk storage in production.** The default `ZO_DATA_DIR` stores all stream data on local disk with no replication. A single disk failure loses all ingested data. For production, configure an S3-compatible backend (`ZO_S3_PROVIDER`, `ZO_S3_BUCKET_NAME`, etc.) before ingesting any data — there is no migration path from local disk to S3 after the fact. MinIO is a common self-hosted alternative if AWS S3 is not available.

- **Stream and organization names are case-sensitive and must use only lowercase alphanumeric characters and underscores.** Names like `MyApp-Logs` or `prod.errors` will either be rejected or silently normalized, causing mismatch between your collector config and the UI. Stick to `my_app_logs` and `prod_errors` patterns. Org names follow the same rule — the default org is `default` (all lowercase).

- **Basic auth credentials must be base64-encoded for the `Authorization` header but most integrations support plain username/password fields.** When using OpenTelemetry Collector or other integrations that require explicit HTTP headers, use `Authorization: Basic <base64(user:pass)>`. However, Fluent Bit's `HTTP_User`/`HTTP_Passwd` and Prometheus `basic_auth` block handle encoding automatically — do not double-encode. Mixing approaches is a common source of 401 errors.
