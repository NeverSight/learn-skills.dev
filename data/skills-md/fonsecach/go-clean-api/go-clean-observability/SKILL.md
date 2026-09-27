---
name: go-clean-observability
description: >
  Structured logging, distributed tracing, metrics, and the Grafana LGTM stack
  for Go HTTP APIs laid out by go-clean-api. Covers slog, OpenTelemetry, and
  the observability standard: one OTel Collector fans out to Prometheus, Loki,
  and Tempo, with provisioned Grafana and log/trace correlation.
  Use when: "add logging", "structured logs", "add tracing", "OpenTelemetry",
  "add metrics", "Prometheus", "Grafana", "Loki", "Tempo", "dashboard",
  "observability", "observability stack", "otel collector", "instrument this code",
  or when standing up production telemetry for a Go API.
  Do NOT use for: where code lives in the layers (use go-clean-api),
  performance profiling with pprof (use go-performance-review),
  error handling patterns (use go-error-handling), or health check endpoints (use go-api-design).
license: MIT
metadata:
  author: github.com/fonsecach
  version: "1.0.0"
---

# Go Clean Observability

Observability is not optional for production services. Every service must produce
structured logs, expose metrics, and propagate trace context. Use the stdlib
`log/slog` for logging and OpenTelemetry for tracing and metrics.

## 1. Structured Logging with slog

### Use `log/slog` (Go 1.21+) as the standard logging package:

```go
// ✅ Good — structured, leveled logging
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))

logger.Info("user created",
    slog.String("user_id", user.ID),
    slog.String("email", user.Email),
    slog.Duration("latency", elapsed),
)
```

```go
// ❌ Bad — unstructured printf-style logging
log.Printf("user %s created with email %s in %v", user.ID, user.Email, elapsed)
```

### Pass logger via context or dependency injection:

```go
// ✅ Good — logger as dependency
type UserService struct {
    logger *slog.Logger
    store  UserStore
}

func NewUserService(logger *slog.Logger, store UserStore) *UserService {
    return &UserService{
        logger: logger.With(slog.String("component", "user_service")),
        store:  store,
    }
}
```

```go
// ❌ Bad — global logger
var logger = slog.Default()
```

### Create child loggers with scoped attributes:

```go
func (s *UserService) CreateUser(ctx context.Context, req CreateUserReq) error {
    log := s.logger.With(
        slog.String("method", "CreateUser"),
        slog.String("request_id", middleware.RequestID(ctx)),
    )

    log.Info("creating user", slog.String("email", req.Email))

    if err := s.store.Insert(ctx, req); err != nil {
        log.Error("failed to create user", slog.Any("error", err))
        return fmt.Errorf("create user: %w", err)
    }

    log.Info("user created successfully")
    return nil
}
```

### Log levels — use them consistently:

| Level | Use for |
|---|---|
| `Debug` | Verbose diagnostic info, disabled in production |
| `Info` | Normal operations: request received, job completed |
| `Warn` | Recoverable issues: retry succeeded, deprecated usage |
| `Error` | Failures requiring attention: DB down, external call failed |

NEVER log at Error level for expected conditions (e.g., user not found → Info or Warn).

### Sensitive data — NEVER log:

- Passwords, tokens, API keys
- Full credit card numbers, SSNs
- Raw request bodies containing PII

```go
// ✅ Good — redacted
logger.Info("auth attempt", slog.String("user", email), slog.Bool("success", ok))

// ❌ Bad — leaks credentials
logger.Info("auth attempt", slog.String("password", password))
```

## 2. Distributed Tracing with OpenTelemetry

### Initialize the tracer provider:

```go
func initTracer(ctx context.Context, serviceName string) (*trace.TracerProvider, error) {
    exporter, err := otlptrace.New(ctx, otlptracehttp.NewClient())
    if err != nil {
        return nil, fmt.Errorf("create exporter: %w", err)
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String(serviceName),
        )),
    )
    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.TraceContext{})

    return tp, nil
}
```

### Create spans for significant operations:

```go
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    ctx, span := otel.Tracer("user-service").Start(ctx, "GetUser")
    defer span.End()

    span.SetAttributes(attribute.String("user.id", id))

    user, err := s.store.FindByID(ctx, id)
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }

    return user, nil
}
```

### Span naming conventions:

```go
// ✅ Good — operation name, not function name
ctx, span := tracer.Start(ctx, "GetUser")
ctx, span := tracer.Start(ctx, "db.query")
ctx, span := tracer.Start(ctx, "http.request")

// ❌ Bad — too verbose or too generic
ctx, span := tracer.Start(ctx, "github.com/myorg/myapp/internal/user.(*Service).GetUser")
ctx, span := tracer.Start(ctx, "doStuff")
```

### Always propagate context through the call chain:

```go
// ✅ Good — context flows through
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context() // carries trace context from middleware
    user, err := h.service.GetUser(ctx, id)
    // ...
}

// ❌ Bad — trace context lost
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.service.GetUser(context.Background(), id) // breaks trace chain
    // ...
}
```

## 3. Metrics with OpenTelemetry / Prometheus

### Define metrics at package level:

```go
var (
    requestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "Duration of HTTP requests in seconds.",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "path", "status"},
    )

    requestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests.",
        },
        []string{"method", "path", "status"},
    )
)
```

### Metric naming conventions:

```text
<namespace>_<subsystem>_<name>_<unit>

http_request_duration_seconds     ✅ (unit in name)
http_requests_total               ✅ (counter with _total suffix)
db_connections_active             ✅ (gauge, no suffix needed)
user_signups                      ❌ (missing _total for counter)
requestLatency                    ❌ (camelCase, no unit)
```

### Instrument HTTP middleware:

```go
func MetricsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        ww := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

        next.ServeHTTP(ww, r)

        duration := time.Since(start).Seconds()
        status := strconv.Itoa(ww.statusCode)

        requestDuration.WithLabelValues(r.Method, r.URL.Path, status).Observe(duration)
        requestsTotal.WithLabelValues(r.Method, r.URL.Path, status).Inc()
    })
}
```

### Use histograms for latencies, counters for totals, gauges for current state:

| Type | Use for | Example |
|---|---|---|
| Counter | Monotonically increasing values | Requests total, errors total |
| Gauge | Values that go up and down | Active connections, queue depth |
| Histogram | Distribution of values | Request latency, response size |

### Keep cardinality low — avoid high-cardinality labels:

```go
// ✅ Good — bounded label values
requestsTotal.WithLabelValues(r.Method, routePattern, status)

// ❌ Bad — unbounded cardinality (user IDs, request IDs)
requestsTotal.WithLabelValues(r.Method, r.URL.Path, userID)
```

## 4. Connecting Logs, Traces, and Metrics

### Inject trace ID into log entries:

```go
func LogWithTrace(ctx context.Context, logger *slog.Logger) *slog.Logger {
    spanCtx := trace.SpanContextFromContext(ctx)
    if !spanCtx.IsValid() {
        return logger
    }
    return logger.With(
        slog.String("trace_id", spanCtx.TraceID().String()),
        slog.String("span_id", spanCtx.SpanID().String()),
    )
}

// Usage in handlers/services:
func (s *Service) Process(ctx context.Context) error {
    log := LogWithTrace(ctx, s.logger)
    log.Info("processing started") // log includes trace_id and span_id
    // ...
}
```

## 5. Grafana LGTM — project standard

slog, spans, and metrics are only operable once they land in this stack.
Do not pick another backend (Jaeger-only, ELK, Promtail, Alloy as the
pipeline, or scraping `/metrics` on the API as the primary path) when the
user wants production observability.

The API exports OTLP to one collector, which fans out to Prometheus (metrics),
Loki (logs), and Tempo (traces). Grafana is provisioned with stable datasource
UIDs and a derived field so a Loki line opens the Tempo trace. That shape is
defined in this skill. There is no external repository to copy from.

Read [references/grafana-lgtm.md](references/grafana-lgtm.md) before scaffolding
a stack, a dashboard, or collector config. Generate files for the service
name, dashboard uid, and database names in front of you. Recalculate memory
and CPU limits for the host. Where the code lives (`internal/infrastructure/observability`,
wiring only in `cmd`) is `go-clean-api`.

Generate Grafana provisioning from the template. Do not hand-write a new
dashboard JSON. From the skill root:

```bash
python scripts/render_grafana.py \
  --service-name <otel-service-name> \
  --title "<Dashboard title>" \
  --db-datname-regex "<datname regex>" \
  --out <dest>/grafana/provisioning
```

The template lives in `references/grafana-template/` (datasources, dashboard
provider, and the Fly.io-style dashboard). Datasource UIDs stay
`prometheus`, `loki`, and `tempo`.

Dashboards depend on these invariants:

- Telemetry is optional at startup. A dead collector must not stop the API.
- JSON logs include `trace_id` and `span_id` (the Loki derived field matches `"trace_id":"(\w+)"`).
- HTTP metrics use the route template, not the raw path.
- Grafana and the API bind to `127.0.0.1`. Do not publish Prometheus, Loki, Tempo, or exporters.

## 6. Graceful Shutdown of Telemetry

```go
func main() {
    ctx := context.Background()

    tp, err := initTracer(ctx, "my-service")
    if err != nil {
        log.Fatalf("init tracer: %v", err)
    }

    // Ensure all spans are flushed on shutdown
    defer func() {
        shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
        defer cancel()
        if err := tp.Shutdown(shutdownCtx); err != nil {
            log.Printf("tracer shutdown: %v", err)
        }
    }()

    // ... start server
}
```

## Verification Checklist

1. All logging uses `log/slog` with structured key-value pairs, not `fmt.Printf` or `log.Printf`
2. Logger is injected as a dependency, not used as a global
3. No sensitive data (passwords, tokens, PII) in log output
4. Trace context is propagated through all function calls via `context.Context`
5. Spans are created for significant operations (DB calls, HTTP requests, business logic)
6. Spans record errors with `span.RecordError(err)` and set error status
7. Metrics follow naming conventions: `_seconds`, `_total`, `_bytes`
8. No high-cardinality labels (user IDs, request IDs) in metrics
9. Telemetry providers are shut down gracefully on service exit
10. Trace IDs are included in log entries for correlation
11. New production telemetry follows the Grafana LGTM reference (collector → Prometheus, Loki, Tempo → provisioned Grafana), not a one-off backend
12. A missing collector or `OTEL_ENABLED=false` still lets the process serve traffic
13. Grafana datasource UIDs stay `prometheus`, `loki`, and `tempo`, with Loki → Tempo and Tempo → Loki correlation
14. API and Grafana listen on localhost only; metrics and log backends are not published on `0.0.0.0`
