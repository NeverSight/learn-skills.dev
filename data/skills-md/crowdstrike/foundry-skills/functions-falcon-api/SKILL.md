---
name: functions-falcon-api
description: Call CrowdStrike Falcon platform APIs (detections, alerts, hosts, RTR) from within Foundry function handlers. TRIGGER when user asks to "call Falcon APIs from a function", "use FalconPy in a function", "use gofalcon in a function", or needs to integrate Falcon platform APIs within serverless function code. DO NOT TRIGGER when user wants to expose external third-party APIs to Foundry — use api-integrations instead.
version: 1.6.0
updated: 2026-10-01
tags: [foundry, functions, falcon-api, falconpy, gofalcon]
author: CrowdStrike
license: MIT
compatibility: Claude Code >=1.0
metadata:
  category: backend
---

# Falcon API Integration in Functions

> Call Falcon APIs through the CrowdStrike SDKs inside Foundry function handlers. Authentication is automatic with the FDK handler pattern.
>
> The FalconPy `Detects` class is **removed**. Do not import it. Use `Alerts` for detection queries.

> **Part of a suite.** If `development-workflow` has not already run, and this is a new app or its first capability, load the `development-workflow` skill first — it owns the CLI prerequisite check, scaffolding order, and manifest coordination.

This skill covers calling CrowdStrike Falcon APIs from within Foundry functions (serverless Go or Python code). Authentication is completely automatic when code runs inside Foundry function handlers — the platform handles all OAuth flows, token management, and credential injection.

For exposing external APIs to Foundry via OpenAPI specs, see **api-integrations** instead.

> **🚫 DEPRECATED API — NEVER USE:**
>
> **Do NOT import or use the `Detects` class from FalconPy.** The Detects API (`/detects/entities/detects/v2`) is deprecated and returns **405 Method Not Allowed**. Any code using `Detects()`, `query_detects()`, or `get_detect_summaries()` will fail at runtime.
>
> **Use instead:** `from falconpy import Alerts` with `query_alerts_v2()` / `get_alerts_v2()`. Filter by `product:'detections'` to scope to detections only.

## Reference Files

| Topic | Reference |
|-------|-----------|
| Retry decorator with exponential backoff, multi-API enrichment, counter-rationalizations table | [references/advanced-patterns.md](references/advanced-patterns.md) |

## Python: Zero-Argument Authentication

FalconPy Service Classes require zero arguments when called inside Foundry Function handlers. The `crowdstrike.foundry.function` FDK provides the handler decorator that enables automatic authentication:

```python
from logging import Logger
from typing import Any, Dict, Union
from crowdstrike.foundry.function import Function, Request, Response
from falconpy import Alerts, Hosts

func = Function.instance()

@func.handler(method='GET', path='/api/alerts')
def get_alerts(request: Request, config: Union[Dict[str, Any], None], logger: Logger) -> Response:
    falcon = Alerts()  # Zero-arg constructor — auth is automatic

    limit = min(int(request.params.query.get("limit", ["50"])[0]), 100)
    # FQL filter: high-severity alerts from the last 24 hours.
    # Combine conditions with '+' (AND); relative times like 'now-24h' are supported.
    response = falcon.query_alerts_v2(
        filter="severity_name:'High'+created_timestamp:>'now-24h'",
        limit=limit,
        sort="created_timestamp|desc",
    )

    if response["status_code"] != 200:
        logger.error(f"Failed to query alerts: {response.get('errors')}")
        return Response(body={"error": "Failed to fetch alerts"}, code=500)

    alert_ids = response.get("body", {}).get("resources", [])
    if not alert_ids:
        return Response(body={"alerts": []}, code=200)

    details_response = falcon.get_alerts_v2(composite_ids=alert_ids)
    if details_response["status_code"] != 200:
        return Response(body={"error": "Failed to fetch alert details"}, code=500)

    alerts = details_response.get("body", {}).get("resources", [])
    return Response(body={"alerts": alerts}, code=200)

if __name__ == '__main__':
    func.run()
```

**How it works:**
- **In Foundry cloud**: Uses context-based authentication injected by the platform
- **Locally**: Reads `FALCON_CLIENT_ID` and `FALCON_CLIENT_SECRET` from environment variables

FalconPy already reads env vars internally, so writing a `get_falcon_client()` wrapper adds no value and breaks context auth in the cloud.


## Go: FDK Helper Authentication

Go requires the FDK helper to get cloud and user-agent configuration:

```go
package main

import (
    "context"
    "log/slog"
    "github.com/crowdstrike/gofalcon/falcon"
    "github.com/crowdstrike/gofalcon/falcon/client"
    fdk "github.com/crowdstrike/foundry-fn-go"
)

func newHandler(_ context.Context, _ *slog.Logger, _ fdk.SkipCfg) fdk.Handler {
    m := fdk.NewMux()

    m.Get("/api/alerts", fdk.HandleFnOf(func(ctx context.Context, r fdk.RequestOf[struct{}]) fdk.Response {
        accessToken := r.Header.Get("X-CS-ACCESSTOKEN")

        opts := fdk.FalconClientOpts()
        falconClient, err := falcon.NewClient(&falcon.ApiConfig{
            AccessToken:       accessToken,
            Cloud:             falcon.Cloud(opts.Cloud),
            Context:           ctx,
            UserAgentOverride: opts.UserAgent,
        })
        if err != nil {
            return fdk.Response{Code: 500, Body: fdk.JSON(map[string]string{"error": "Failed to authenticate"})}
        }

        // ... API calls with falconClient ...
        return fdk.Response{Code: 200, Body: fdk.JSON(map[string]interface{}{"alerts": []interface{}{}})}
    }))

    return m
}

func main() {
    fdk.Run(context.Background(), newHandler)
}
```

## Common API Patterns

### Detection Queries (via Alerts API)

> **⚠️ The legacy Detects API (`/detects/entities/detects/v2`) is deprecated and returns 405 Method Not Allowed.** Use the Alerts API (`/alerts/entities/alerts/v3`) for all detection queries — it covers both detections and cases.

```python
@func.handler(method='GET', path='/api/detections')
def get_detections(request: Request, config, logger) -> Response:
    falcon = Alerts()  # Zero-arg — auth is automatic

    severity_min = int(request.params.query.get("severity_min", ["3"])[0])
    limit = min(int(request.params.query.get("limit", ["50"])[0]), 100)

    # Use Alerts v2 methods — these hit /alerts/entities/alerts/v3 under the hood.
    # FQL filter: severity threshold + product "detections" (excludes cases/incidents).
    query_response = falcon.query_alerts_v2(
        filter=f"severity:>='{severity_min}'+product:'detections'",
        limit=limit,
        sort="created_timestamp|desc",
    )
    if query_response["status_code"] != 200:
        return Response(body={"error": "Failed to query detections"}, code=500)

    alert_ids = query_response.get("body", {}).get("resources", [])
    if not alert_ids:
        return Response(body={"detections": []}, code=200)

    details = falcon.get_alerts_v2(composite_ids=alert_ids)
    if details["status_code"] != 200:
        return Response(body={"error": "Failed to get details"}, code=500)

    return Response(body={"detections": details["body"]["resources"]}, code=200)
```

### Host Lookups

```python
@func.handler(method='GET', path='/api/hosts')
def get_host_details(request: Request, config, logger) -> Response:
    falcon = Hosts()

    hostname = request.params.query.get("hostname", [""])[0]  # ?hostname=...
    if not hostname:
        return Response(body={"error": "Hostname required"}, code=400)

    query = falcon.query_devices_by_filter(filter=f"hostname:'{hostname}'")
    if query["status_code"] != 200:
        return Response(body={"error": "Failed to query devices"}, code=500)

    host_ids = query.get("body", {}).get("resources", [])
    if not host_ids:
        return Response(body={"error": f"Host not found: {hostname}"}, code=404)

    details = falcon.get_device_details(ids=host_ids)
    host = details.get("body", {}).get("resources", [{}])[0]
    return Response(body={"host": host}, code=200)
```

### Multi-API Enrichment

Combining `Hosts` and `Alerts` in one handler follows the same query-then-get-details shape as above. See [references/advanced-patterns.md](references/advanced-patterns.md) for the full example.

## LogScale / NG-SIEM Queries from Functions

When you need to **query** LogScale data (e.g., workflow execution stats from the "fusion" repo, detection telemetry, custom ingested events), use the `NGSIEM` class. This is distinct from **ingestion** (covered in functions-development).

> **⚠️ Class Disambiguation:**
> - `NGSIEM` — Use for **querying** (async search jobs) and file uploads (lookup files, CSV imports). This is the query interface.
> - `FoundryLogScale` — Use only for **ingestion** (`ingest_data`). Despite the name suggesting broad LogScale functionality, it does NOT have the search methods.

### Query Pattern (Python)

```python
import time
from logging import Logger
from typing import Any, Dict, Union
from crowdstrike.foundry.function import Function, Request, Response
from falconpy import NGSIEM

func = Function.instance()

# Always "search-all" — see the gotcha below. Scope to a repo in the query, not here.
REPO = "search-all"


def run_logscale_query(ngsiem, query_string, start, end, logger, max_wait=40):
    """Execute a CQL query as an async search job and return result rows.

    ``start`` / ``end`` accept Humio relative strings ("24h", "7d", "30d",
    "now") or epoch-millisecond integers.
    """
    payload = {"queryString": query_string, "start": start, "end": end, "isLive": False}
    started = ngsiem.start_search(repository=REPO, search=payload)

    if not isinstance(started, dict) or started.get("status_code", 500) >= 300:
        logger.error(f"start_search failed: {started}")
        return None

    # start_search returns "resources"; get_search_status returns "body".
    job_id = (started.get("resources") or {}).get("id")
    if not job_id:
        logger.error(f"start_search returned no job id: {started}")
        return None

    # Poll until done
    waited = 0.0
    poll_interval = 1.5
    while waited < max_wait:
        time.sleep(poll_interval)
        waited += poll_interval
        status = ngsiem.get_search_status(repository=REPO, id=job_id)
        if not isinstance(status, dict) or status.get("status_code", 500) >= 300:
            logger.error(f"get_search_status failed: {status}")
            return None
        sbody = status.get("body") or {}
        if sbody.get("done"):
            return sbody.get("events", []) or []

    logger.warning(f"query timed out after {max_wait}s: {query_string}")
    return None


@func.handler(method='POST', path='/api/query')
def handle_query(request: Request, config: Union[Dict[str, Any], None], logger: Logger) -> Response:
    ngsiem = NGSIEM()  # Zero-arg auth — automatic in Foundry

    query = request.body.get("query", "")
    start = request.body.get("start", "24h")
    end = request.body.get("end", "now")

    events = run_logscale_query(ngsiem, query, start, end, logger)
    if events is None:
        return Response(body={"error": "LogScale query failed"}, code=500)

    return Response(body={"results": events, "count": len(events)}, code=200)

if __name__ == '__main__':
    func.run()
```

### `start_search` Arguments and Responses

Pass the query to `start_search` as `search=`, as in the example above. Response keys are asymmetric: `start_search` renames its payload to `resources` (read `started["resources"]["id"]`), while `get_search_status` does not (read `status["body"]`).

### The "search-all" Repository Gotcha

**CRITICAL:** Always pass `repository="search-all"` when querying from Foundry functions. Passing a specific repository name (e.g., `"fusion"`, `"main"`) causes **403 Forbidden** errors at runtime (`"scope not permitted"`), even if the repository exists and the app has `humio-auth-proxy` scopes granted.

The NG-SIEM queryjobs API is addressed by **searchable view**, not by raw repo name. Use `search-all` as the repository and add `#repo=fusion` (or whichever repo you need) as a filter prefix in your query string:

```python
# Filter to a specific repo within the query itself
query = "#repo=fusion | execution_log_type=summary | execution_log_subtype=end | groupby([status], function=count(execution_id, distinct=true))"
events = run_logscale_query(ngsiem, query, "24h", "now", logger)
```

### Required OAuth Scopes

```yaml
# manifest.yml
auth:
    scopes:
        - humio-auth-proxy:read     # Required for queries
        - humio-auth-proxy:write    # Required only if also uploading lookup files
```

### Reference

- [Exporting Falcon Next-Gen SIEM Query Results to CSV with Falcon Foundry](https://www.crowdstrike.com/tech-hub/ng-siem/exporting-falcon-next-gen-siem-query-results-to-csv-with-falcon-foundry/) — background on async LogScale querying from Foundry, plus CSV export. Note that this post reaches for `FoundryLogScale` with `mode="async"`; the `NGSIEM` pattern above is what has been verified end-to-end against the queryjobs API in a deployed app. Use the pattern above, and treat the post as context for the surrounding workflow (time ranges, result handling, export).

## Charlotte AI AgentWorks (`/agentic-studio/*`)

Use the `Agents`, `Spans`, `AgentInvocation`, `AgentVersions`, and `Models` classes with the `charlotte-ai-agent-definition` scopes (`read`; `write` to invoke and poll). Filter spans on `attributes.aw_agent.id` (not `aw_agent.agent_id`, which silently matches nothing). Route-to-method map: [advanced-patterns](references/advanced-patterns.md).

## The 207 Multi-Status Gotcha

CrowdStrike APIs may return `207 Multi-Status` responses that look successful but contain embedded errors. Check the errors array:

```python
response = falcon.perform_action(action_name="contain", ids=host_ids)

if response["status_code"] == 207:
    errors = response.get("body", {}).get("errors", [])
    rate_limited = [e for e in errors if e.get("code") == 429]
    if rate_limited:
        return Response(body={"error": "Rate limited", "failed_ids": [e.get("id") for e in rate_limited]}, code=429)
```

## Testing

Mock Falcon APIs in tests instead of making real API calls (they are slow, flaky, and quota-consuming):

```python
def test_get_alerts_success():
    mock_falcon = Mock()
    mock_falcon.query_alerts_v2.return_value = {
        "status_code": 200,
        "body": {"resources": ["alert-001", "alert-002"]}
    }
    mock_falcon.get_alerts_v2.return_value = {
        "status_code": 200,
        "body": {"resources": [{"id": "alert-001", "severity": 80}]}
    }

    with patch('falconpy.Alerts', return_value=mock_falcon):
        from crowdstrike.foundry.function import RequestParams
        from main import get_alerts
        request = Mock(spec=Request)
        request.params = RequestParams(query={"limit": ["10"]})
        response = get_alerts(request, None, Mock())
        assert response.code == 200
        assert len(response.body["alerts"]) == 1
        # get_alerts_v2 reads only composite_ids; ids= fails with a 400 before any request is sent
        mock_falcon.get_alerts_v2.assert_called_once_with(composite_ids=["alert-001", "alert-002"])
```

## Local Testing

```bash
export FALCON_CLIENT_ID="your-client-id"
export FALCON_CLIENT_SECRET="your-client-secret"
cd functions/my-function && python3 main.py
curl -X GET http://localhost:8081/api/alerts?limit=10
```

## OAuth Scopes for manifest.yml

Every FalconPy service class call requires the correct OAuth scope(s) declared in your manifest's `auth.scopes` array. Without the right scopes, the function gets a 403 at runtime. `foundry apps validate` does NOT catch missing scopes — it only fails at runtime.

> **⚠️ Scope names don't always match class names.** The `Hosts` class requires `devices:read`, not `hosts:read`. Always use this table rather than guessing from class names.

> **Built-in capabilities don't need scopes.** API integrations, collections, workflows, and LogScale ingestion work without declaring their scopes when used through Foundry's built-in SDK patterns (`falcon.apiIntegration()`, `CustomStorage()` for app collections, etc.). Only declare scopes when calling Falcon platform APIs directly via FalconPy service classes.

### Scope Reference (verified from production sample apps)

Each row maps a FalconPy method actually called in a sample function to the scope declared in that app's manifest.

| FalconPy Class | Methods | Required Scope(s) | Verified In |
|---|---|---|---|
| `Hosts` | `get_device_details` | `devices:read` | foundry-sample-functions-python |
| `Intel` | `query_indicator_ids` | `falconx-indicators:read` | foundry-sample-zscaler-internet-access |
| `IdentityProtection` | `graphql`, `query_sensors`, `get_sensor_details` | `identity-graphql:write`, `identity-entities:read` | foundry-sample-idp-notifications |
| `IdentityProtection` | `query_policy_rules`, `get_policy_rules`, `delete_policy_rules` | `identity-policy-rules:read`, `identity-policy-rules:write` | foundry-sample-servicenow-idp |
| `NGSIEM` | `upload_file` | `humio-auth-proxy:write` | foundry-sample-ngsiem-importer |
| `NGSIEM` | `start_search`, `get_search_status` | `humio-auth-proxy:read` | Verified against a live CID (200 + results); see LogScale Queries section |
| `FoundryLogScale` | `ingest_data` | `app-logs:read`, `app-logs:write` | foundry-sample-logscale |
| `FirewallManagement` | `create_rule_group`, `query_events`, `get_events` | `firewall-management:read`, `firewall-management:write` | foundry-sample-category-blocking |
| `HostGroup` | `query_host_groups`, `get_host_groups` | `host-group:read`, `host-group:write` | foundry-sample-category-blocking |
| `Agents`, `Spans`, `AgentInvocation`, `AgentVersions`, `Models` | AgentWorks | `charlotte-ai-agent-definition:read`, `:write` | Endpoints verified on EU-1 |

**Go functions (gofalcon) require the same scopes.** The table above uses FalconPy class/method names, but the underlying Falcon API scopes are identical regardless of SDK. If your Go function calls the RTR admin API, declare `real-time-response-admin:write`. If it manages incidents, declare `incidents:read`, `incidents:write`.

### How to declare scopes

```yaml
# manifest.yml
auth:
    scopes:
        - devices:read
        - falconx-indicators:read
    permissions: {}
    roles: []
```

### When unsure about the correct scope

If you're using a FalconPy method not in this table:
1. Check the method's HTTP verb and API path in FalconPy source — GET typically needs `:read`, POST/PUT/PATCH/DELETE typically needs `:write`
2. The scope prefix is usually the **API path prefix** (e.g., `/iocs/...` → `iocs`, `/devices/...` → `devices`), but exceptions exist (`Hosts` → `devices`, `NGSIEM` → `humio-auth-proxy`)
3. When ambiguous, **ask the user** which scopes to include rather than guessing

## Falcon Severity Values

CrowdStrike APIs return severity as **integers** (1-5) or display names. When integrating with external systems (Jira, ServiceNow, email), map them explicitly:

| Falcon Severity | Display Name | Typical External Mapping |
|----------------|--------------|--------------------------|
| 1 | Informational | Low / Lowest |
| 2 | Low | Low |
| 3 | Medium | Medium |
| 4 | High | High |
| 5 | Critical | Highest / Critical |

Use `max_severity_displayname` for FQL filters (string comparison) or `max_severity` for numeric comparison. When passing severity to external ticketing systems, always map to their expected format rather than passing the raw value through.

## Common Pitfalls

- **Writing OAuth code or credential management.** Auth is automatic inside FDK handlers. The zero-arg pattern (`Hosts()`, `Alerts()`) handles all auth. (Go requires `fdk.FalconClientOpts()` -- see above.)
- **Using `requests` library instead of CrowdStrike SDKs.** SDKs handle auth, retries, pagination, and region discovery.
- **Passing credentials explicitly to constructors.** Use zero-arg constructors (`Alerts()`, `Hosts()`). Do NOT write `IOC(client_id=os.environ["FALCON_CLIENT_ID"], client_secret=...)` -- this breaks context-based auth in the Foundry cloud.
- **Writing Falcon API calls outside of FDK handler functions.** The handler pattern is required for automatic auth injection.
- **Module-scope client, or `request.params.get()` / `request.query`.** `401` on every call, or an attribute error.
- **Not handling 207 Multi-Status.** These responses look successful but may contain embedded errors.

## Use Cases

For real-world implementation patterns, see:
- `use-cases/python-functions.md` — Python handler patterns, SDK usage, testing

## Reference Implementations

- **[foundry-sample-functions-python](https://github.com/CrowdStrike/foundry-sample-functions-python)**: Reference Python patterns. See also [Dive into Falcon Foundry Functions with Python](https://www.crowdstrike.com/tech-hub/ng-siem/dive-into-falcon-foundry-functions-with-python/).
- **[foundry-sample-anomali-threatstream](https://github.com/CrowdStrike/foundry-sample-anomali-threatstream)**: Side-by-side Go and Python auth patterns.
- **[foundry-sample-detection-translation](https://github.com/CrowdStrike/foundry-sample-detection-translation)**: CrowdStrike alerts API from functions.
- **[foundry-sample-threat-intel](https://github.com/CrowdStrike/foundry-sample-threat-intel)**: CrowdStrike Intelligence APIs from functions.
- **[foundry-sample-idp-notifications](https://github.com/CrowdStrike/foundry-sample-idp-notifications)**: Falcon IdP domain and connector monitoring.
