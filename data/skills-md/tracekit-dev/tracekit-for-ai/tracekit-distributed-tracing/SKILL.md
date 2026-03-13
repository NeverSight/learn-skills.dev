---
name: tracekit-distributed-tracing
description: Connect frontend and backend traces across services with TraceKit distributed tracing. Covers W3C Trace Context propagation, multi-service correlation, and the unified waterfall view. Use when the user asks about connecting traces across services, frontend-to-backend tracing, or seeing the full request lifecycle.
---

# TraceKit Distributed Tracing

## When To Use

Use this skill when the user asks to:
- Connect traces across services
- Set up frontend-to-backend tracing
- Configure distributed tracing
- Set up trace propagation between microservices
- See the full request flow across services
- View the unified waterfall for a request
- Correlate frontend and backend performance
- Trace requests through microservices
- Debug latency across multiple services

## Non-Negotiable Rules

1. **Never hardcode API keys** in code. Always use `TRACEKIT_API_KEY` env var.
2. **Always use W3C Trace Context** (`traceparent` header) for propagation — never proprietary headers.
3. **Always verify traces connect across services** in the unified waterfall view before considering setup complete.
4. **Always configure `tracePropagationTargets`** in the frontend SDK to limit which outbound requests get trace headers. This prevents leaking trace context to third-party APIs.

## Prerequisites

- **At least two TraceKit SDKs must be installed** — one frontend and one or more backend, or multiple backend services.
- Each service must have its own unique `serviceName` configured in SDK init.
- If only one SDK is installed, complete the other SDK skills first:
  - Frontend: `tracekit-browser-sdk`, `tracekit-react-sdk`, `tracekit-vue-sdk`, etc.
  - Backend: `tracekit-node-sdk`, `tracekit-go-sdk`, `tracekit-python-sdk`, etc.
- Browser SDK or framework wrapper must have `tracePropagationTargets` configured (see Step 2).

## Detection

Before applying this skill, detect the project setup:

1. **Scan for multiple TraceKit SDKs** across the project or monorepo.
2. **Frontend detection:** Check `package.json` for `@tracekit/browser`, `@tracekit/react`, `@tracekit/vue`, `@tracekit/angular`, `@tracekit/nextjs`, or `@tracekit/nuxt`.
3. **Backend detection:** Check `go.mod` for `github.com/Tracekit-Dev/go-sdk`, `requirements.txt` for `tracekit-apm`, `package.json` for `@tracekit/node-apm`, `composer.json` for `tracekit/php-apm`, `pom.xml` for `tracekit-core`, `.csproj` for `TraceKit.AspNetCore`, or `Gemfile` for `tracekit`.
4. **If only frontend found**, suggest completing a backend SDK skill first.
5. **If only backend found**, suggest completing a browser SDK or framework wrapper skill first.
6. **If both found**, proceed with distributed tracing setup.

## Step 1: Understand W3C Trace Context

Distributed tracing works by passing trace context between services via HTTP headers. TraceKit uses the W3C Trace Context standard, which is compatible with OpenTelemetry, Jaeger, Zipkin, and other observability tools.

### How It Works

1. Every traced request carries a `traceparent` header with the format:
   ```
   traceparent: 00-<trace-id>-<span-id>-<flags>
   ```
   Example: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`

2. When a frontend makes an API call, the browser SDK **injects** the `traceparent` header into the outbound request.

3. When a backend receives the request, the backend SDK **extracts** the `traceparent` header and continues the same trace.

4. Each service creates **child spans** under the same trace ID, forming a tree of operations.

5. TraceKit collects all spans with the same trace ID and renders them in the **unified waterfall view** — showing timing, dependencies, and service boundaries.

### Why W3C Trace Context

- Industry standard — works across vendors and languages
- No vendor lock-in — switch observability backends without changing propagation
- Supported natively by all TraceKit SDKs
- Compatible with OpenTelemetry exporters if you use them alongside TraceKit

## Step 2: Configure Frontend Trace Propagation

In your frontend SDK init, configure `tracePropagationTargets` to specify which backend URLs should receive trace headers.

```javascript
TraceKit.init({
  apiKey: process.env.TRACEKIT_API_KEY,
  serviceName: 'my-react-app',
  tracePropagationTargets: [
    'api.yourapp.com',           // production API
    /^https:\/\/api\./,          // regex: any api.* subdomain
    'localhost:3001',            // development backend
    'localhost:8080',            // development Go service
  ],
});
```

### What `tracePropagationTargets` Does

- **Only requests matching these patterns** get `traceparent` and `tracestate` headers injected.
- Requests to non-matching URLs (third-party APIs, CDNs, analytics) do **not** get trace headers.
- **Default behavior** (if not set): same-origin requests only.
- **Security:** This prevents leaking internal trace context to external services. Always configure this explicitly.

### Pattern Matching

- **String patterns** match as substrings: `'api.yourapp.com'` matches `https://api.yourapp.com/users`.
- **Regex patterns** provide full control: `/^https:\/\/api\./` matches only HTTPS API subdomains.
- Include both production and development URLs if you want traces in local development.

## Step 3: Configure Backend Trace Extraction

Each TraceKit backend SDK **automatically extracts** `traceparent` from incoming requests when the SDK middleware is registered. No additional configuration is needed if you followed the SDK skill setup.

### Verify Middleware Is Registered

Distributed tracing requires the SDK middleware to be registered **before** route handlers. Verify for your backend:

**Node.js (Express):**
```javascript
const app = express();
// TraceKit middleware must be first
app.use(TraceKit.Handlers.requestHandler());
app.use(TraceKit.Handlers.tracingHandler());
// Then your routes
app.get('/api/users', (req, res) => { /* ... */ });
```

**Node.js (Fastify):**
```javascript
// Register TraceKit plugin before routes
fastify.register(require('@tracekit/node-apm').fastifyPlugin);
```

**Go (Gin):**
```go
r := gin.Default()
// TraceKit middleware must be before routes
r.Use(sdk.GinMiddleware())
r.GET("/api/users", handleUsers)
```

**Go (Echo):**
```go
e := echo.New()
// TraceKit middleware must be before routes
e.Use(sdk.EchoMiddleware())
e.GET("/api/users", handleUsers)
```

**Python (Django):**
```python
# settings.py — TraceKit middleware should be early in the list
MIDDLEWARE = [
    'tracekit.integrations.django.TracekitMiddleware',
    # ... other middleware
]
```

**Python (FastAPI):**
```python
from tracekit.integrations.fastapi import TracekitMiddleware
app = FastAPI()
app.add_middleware(TracekitMiddleware)
```

If middleware is registered correctly, the backend SDK will automatically extract `traceparent` from incoming requests and create child spans under the same trace.

## Step 4: Multi-Service Propagation

When one backend service calls another backend service, trace context must also be propagated. Use the TraceKit-instrumented HTTP client instead of the raw standard library client.

### Node.js (Backend-to-Backend)

```javascript
const { tracekit } = require('@tracekit/node-apm');

// Use tracekit.fetch — auto-injects traceparent into outbound requests
const response = await tracekit.fetch('http://go-service:8080/api/data');
const data = await response.json();
```

### Go (Backend-to-Backend)

```go
// Use tracekit.HTTPClient — auto-injects traceparent into outbound requests
resp, err := tracekit.HTTPClient.Get("http://python-service:5000/api/data")
if err != nil {
    sdk.CaptureException(err)
    return
}
defer resp.Body.Close()
```

### Python (Backend-to-Backend)

```python
import tracekit

# Use tracekit.requests — auto-injects traceparent into outbound requests
response = tracekit.requests.get("http://node-service:3001/api/data")
data = response.json()
```

**Key principle:** Always use the TraceKit-instrumented HTTP client for outbound requests between your own services. The raw `http.Get()`, `fetch()`, or `requests.get()` will **not** propagate trace context.

## Step 5: Concrete Multi-Service Example

Walk through a complete distributed trace across three services.

### Scenario: React Frontend -> Node.js API -> Go Microservice

**Architecture:**
- React frontend (port 3000) — user-facing UI
- Node.js API (port 3001) — API gateway, handles auth and routing
- Go microservice (port 8080) — user data service, queries database

**Request flow:**

1. **User clicks "Load Users" in React app** — the React SDK creates a browser span.
2. **React app calls `fetch('/api/users')`** — the browser SDK injects `traceparent` into the request headers (because `localhost:3001` is in `tracePropagationTargets`).
3. **Node.js API receives the request** — the Node SDK extracts `traceparent`, creates a child span under the same trace ID.
4. **Node.js API calls the Go microservice** — using `tracekit.fetch('http://localhost:8080/users')`, which injects `traceparent` into the outbound request.
5. **Go microservice receives the request** — the Go SDK extracts `traceparent`, creates a child span.
6. **Go microservice queries the database** — the SDK creates a database span under the Go service span.
7. **Response flows back** — each service closes its spans as responses return.

**All spans share the same trace ID**, forming a complete tree of the request lifecycle.

### Unified Waterfall View

Navigate to `https://app.tracekit.dev/traces`, find the trace, and click to open the waterfall:

```
Service              Timeline                                    Duration
---------------------------------------------------------------------------
React Frontend       |========================================|   420ms
  fetch /api/users   |  ====================================  |   380ms
Node.js API          |    ================================    |   360ms
  GET /api/users     |    ============================        |   300ms
  validate-auth      |    ====                                |    40ms
Go Microservice      |        ========================        |   240ms
  GET /users         |        ========================        |   240ms
  db.Query           |          ==================            |   180ms
```

Each row represents a service. Child spans are indented. The timeline shows exactly where time is spent — in this example, 180ms of the total 420ms is database query time in the Go microservice.

## Step 6: Verification

After configuring distributed tracing, verify end-to-end:

1. **Make a request from your frontend** that hits at least 2 backend services.
2. **Navigate to** `https://app.tracekit.dev/traces`.
3. **Find the trace** — filter by service name or sort by recency.
4. **Click to open the unified waterfall view.**
5. **Verify all services appear** as separate rows with their own spans.
6. **Verify span timing** shows the full request lifecycle with correct parent-child relationships.
7. **Click any span** to see its service name, operation name, duration, and metadata (tags, HTTP status, etc.).

If services are missing from the waterfall, see Troubleshooting below.

## Step 7: Custom Span Context

Add business context to distributed traces so you can search and filter by meaningful attributes.

### Frontend Tags

```javascript
// Set user context — propagates to all frontend spans
TraceKit.setTag('user.id', userId);
TraceKit.setTag('user.plan', 'enterprise');

// Set tags on a specific transaction
const transaction = TraceKit.startTransaction({ name: 'checkout' });
transaction.setTag('cart.items', itemCount);
```

### Backend Tags

```javascript
// Node.js — add request context
tracekit.setTag('order.id', orderId);
tracekit.setTag('tenant.id', tenantId);
```

```go
// Go — add request context
span := sdk.GetCurrentSpan(ctx)
span.SetTag("order.id", orderID)
span.SetTag("tenant.id", tenantID)
```

```python
# Python — add request context
tracekit.set_tag('order.id', order_id)
tracekit.set_tag('tenant.id', tenant_id)
```

Tags are searchable in the TraceKit dashboard. Use them to find traces for specific users, orders, tenants, or any business entity.

## Troubleshooting

### Traces not connecting across services

- **Check `tracePropagationTargets`:** Ensure the frontend SDK config includes the backend URL. If the backend URL is not matched, no `traceparent` header is sent.
- **Check CORS configuration:** The backend must allow `traceparent` and `tracestate` in `Access-Control-Allow-Headers`:
  ```javascript
  // Express CORS example
  app.use(cors({
    origin: 'http://localhost:3000',
    allowedHeaders: ['Content-Type', 'Authorization', 'traceparent', 'tracestate'],
  }));
  ```
  ```go
  // Gin CORS example
  config := cors.DefaultConfig()
  config.AllowHeaders = append(config.AllowHeaders, "traceparent", "tracestate")
  r.Use(cors.New(config))
  ```
- **Check browser DevTools:** Open the Network tab, find the API request, and check if `traceparent` appears in the request headers. If missing, the URL is not in `tracePropagationTargets`.

### Missing backend spans

- **Check SDK middleware is registered:** The middleware must be added **before** route handlers (see Step 3).
- **Check backend is sending data:** Visit `https://app.tracekit.dev/traces` and filter by the backend service name. If no traces appear at all, the backend SDK init may have an issue.
- **Check `TRACEKIT_API_KEY` is set:** Each backend service needs its own API key configured.

### CORS errors in browser console

- **`Access-Control-Allow-Headers` must include `traceparent`:** The `traceparent` header is a custom header, so CORS preflight must explicitly allow it.
- **`Access-Control-Allow-Origin` must match:** Ensure the frontend origin is allowed by the backend CORS config.
- **Do not use `*` for credentials:** If your frontend sends cookies or auth headers, `Access-Control-Allow-Origin` cannot be `*` — use the explicit origin.

### Only seeing one service in the waterfall

- **Check each service has a unique `serviceName`:** If two services share the same name, their spans will be grouped together and appear as one service.
- **Check both services are sending to the same TraceKit project:** If services use different API keys for different projects, traces will not be correlated.
- **Check the trace ID:** In the dashboard, click a trace and verify the trace ID. Then filter by that trace ID — all spans should appear regardless of service.

### Trace waterfall shows gaps

- **Network latency:** Gaps between a parent span ending and a child span starting indicate network time. This is normal for distributed systems.
- **Async operations:** If a service processes requests asynchronously, the response may return before all child operations complete. Use `await` or synchronous patterns for operations that should appear in the waterfall.
- **Clock skew:** If services run on different machines with unsynchronized clocks, spans may appear slightly out of order. Use NTP to synchronize clocks across your infrastructure.

### Frontend spans appear but backend spans do not

- **This usually means `traceparent` is being sent but the backend is not extracting it.** Verify the backend SDK middleware is registered (Step 3).
- **Check backend logs** for TraceKit initialization errors.
- **Test with curl:** Send a request with a manual `traceparent` header to the backend and check if a trace appears:
  ```bash
  curl -H "traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01" \
    http://localhost:3001/api/users
  ```

## Next Steps

Once distributed tracing is working across services, consider:
- **Code Monitoring** — Set live breakpoints on traced requests to capture production state without redeploying (see `tracekit-code-monitoring` skill)
- **Alerts** — Alert on cross-service latency or error propagation patterns (see `tracekit-alerts` skill)
- **Releases** — Track which release introduced a latency regression visible in traces (see `tracekit-releases` skill)

## References

- Distributed tracing docs: `https://app.tracekit.dev/docs/distributed-tracing`
- W3C Trace Context spec: `https://www.w3.org/TR/trace-context/`
- Dashboard: `https://app.tracekit.dev`
- See also: `tracekit-browser-sdk`, `tracekit-node-sdk`, `tracekit-go-sdk` skills for single-service setup
