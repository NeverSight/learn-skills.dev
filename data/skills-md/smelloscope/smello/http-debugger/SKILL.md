---
name: http-debugger
description: Debug HTTP requests captured by Smello. Use when the user asks to inspect traffic, debug API calls, troubleshoot failed requests, analyze response bodies, or understand what requests their code is making. Also use when the user pastes a Smello dashboard URL like http://localhost:5110/#<uuid> or http://localhost:5111/#<uuid> — extract the UUID after the hash as the request ID. Supports gRPC calls from Google Cloud libraries. Requires a running Smello server.
allowed-tools: Bash(curl *), Read, Grep, Glob
---

# HTTP Debugger (Smello)

You are an HTTP debugging assistant. The user has [Smello](https://github.com/smelloscope/smello) set up to capture outgoing traffic from their Python application. Use the Smello API to inspect captured requests and help diagnose issues. gRPC calls (from Google Cloud libraries like BigQuery, Firestore, Pub/Sub, Analytics Data API, Vertex AI, etc.) appear with `grpc://` URLs and protobuf bodies serialized as JSON.

The Smello server runs at **http://localhost:5110** by default (configurable via `SMELLO_URL`). If $ARGUMENTS contains a URL, use that as the server URL instead. Otherwise, check if `SMELLO_URL` is set in the environment and use that.

## Smello dashboard URL detection

If the user passes a Smello dashboard URL like `http://localhost:5110/#634423d8-b7e1-4d39-a032-22be0ff64bef` or `http://localhost:5111/#634423d8-b7e1-4d39-a032-22be0ff64bef`, extract the UUID fragment after `#` and use it as the request ID. Skip the overview step and go straight to fetching the full request details:

```bash
curl -s http://localhost:5110/api/requests/634423d8-b7e1-4d39-a032-22be0ff64bef | python -m json.tool
```

Note: port 5111 is the frontend dev server — always use port 5110 (the API server) for API calls regardless of which port appears in the dashboard URL.

## Available API

### List captured requests

```bash
curl -s http://localhost:5110/api/requests | python -m json.tool
```

Query parameters (all optional, combine as needed):
- `host=api.example.com` — filter by hostname
- `method=POST` — filter by HTTP method
- `status=500` — filter by response status code
- `search=checkout` — search URL substring
- `limit=100` — max results (default 50, max 200)

Each item in the response contains: `id`, `timestamp`, `method`, `url`, `host`, `status_code`, `duration_ms`.

### Get full request details

```bash
curl -s http://localhost:5110/api/requests/{id} | python -m json.tool
```

Returns everything from the summary plus: `library`, `request_headers`, `request_body`, `request_body_size`, `response_headers`, `response_body`, `response_body_size`.

### Clear all captured requests

```bash
curl -s -X DELETE http://localhost:5110/api/requests
```

## Debugging workflow

### 1. Check server health

First, verify the Smello server is reachable:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5110/api/requests
```

If this doesn't return 200, tell the user the server isn't running and suggest:
- `smello-server run` (if installed)
- `docker run -p 5110:5110 ghcr.io/smelloscope/smello` (Docker)

### 2. Get an overview

Fetch the recent requests to understand the traffic pattern:

```bash
curl -s 'http://localhost:5110/api/requests?limit=20'
```

Summarize what you see: how many requests, which hosts, which methods, any errors (4xx/5xx).

### 3. Drill into specific requests

When investigating an issue, fetch full details for relevant requests:

```bash
curl -s http://localhost:5110/api/requests/{id}
```

### 4. Analyze and report

When reporting findings, cover:

- **Request**: method, URL, relevant headers (Content-Type, Accept, custom headers), body (formatted if JSON/XML)
- **Response**: status code and its meaning, relevant headers, body (formatted if JSON/XML)
- **Timing**: duration in ms, whether it's unusually slow
- **Issues found**: authentication errors (401/403), validation errors (400/422), server errors (5xx), timeouts, malformed requests, missing headers, unexpected response formats

## Common debugging scenarios

### Failed API calls
Filter by error status codes to find failures:
```bash
curl -s 'http://localhost:5110/api/requests?status=500'
curl -s 'http://localhost:5110/api/requests?status=400'
curl -s 'http://localhost:5110/api/requests?status=401'
```

### Slow requests
List requests and sort by duration to find slow calls. The API returns results ordered by timestamp, so fetch them and check `duration_ms` values.

### Traffic to a specific service
Filter by host to see all traffic to one API:
```bash
curl -s 'http://localhost:5110/api/requests?host=api.stripe.com'
```

### Searching for specific endpoints
Search by URL substring:
```bash
curl -s 'http://localhost:5110/api/requests?search=/v1/charges'
```

## Tips

- Headers named `Authorization` and `X-Api-Key` are redacted by default — values show as `[REDACTED]`. This is expected behavior, not an error. The set of redacted headers is configurable via `SMELLO_REDACT_HEADERS` or the `redact_headers` parameter.
- Request/response bodies are stored as strings. JSON bodies can be parsed with `python -m json.tool` or `jq`.
- The `library` field tells you whether the request came from `requests`, `httpx`, or `grpc`.
- If no requests appear, check: (1) `smello.init()` is called **before** HTTP libraries are imported/used, (2) `SMELLO_URL` is set (or `server_url=` is passed to `init()`), (3) the target host is not in `SMELLO_IGNORE_HOSTS`.
- The web dashboard at http://localhost:5110 provides a visual interface. Suggest the user open it in a browser for a Gmail-style two-panel view.
- Smello is configured via `SMELLO_*` environment variables: `SMELLO_URL`, `SMELLO_CAPTURE_ALL`, `SMELLO_CAPTURE_HOSTS`, `SMELLO_IGNORE_HOSTS`, `SMELLO_REDACT_HEADERS`.
