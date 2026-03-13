---
name: logging-observability
description: Guidelines for structured logging, distributed tracing, and debugging patterns across languages. Covers logging best practices, observability, security considerations, and performance analysis.
activation_triggers:
  - logging
  - observability
  - tracing
  - debugging
  - structured logging
  - log aggregation
  - performance metrics
  - monitoring
  - correlation ID
  - trace ID
---

# Logging & Observability Skill

Activate when working with logging systems, distributed tracing, debugging, monitoring, or any observability-related tasks across applications.

## 1. Logging Best Practices

### Log Levels

Use appropriate log levels for different severity:

| Level | Severity | When to Use |
|-------|----------|------------|
| **DEBUG** | Low | Development only - detailed info, variable states, control flow. Use sparingly in production. |
| **INFO** | Low | Important application lifecycle events - startup, shutdown, config loaded, user actions, key state changes. |
| **WARN** | Medium | Recoverable issues - deprecated usage, resource constraints, unexpected but handled conditions. Investigate later. |
| **ERROR** | High | Unrecoverable problems - exceptions, failed operations, missing required data. Requires immediate attention. |
| **FATAL** | Critical | System-level failures - abort conditions, out of memory, unrecoverable state. System may crash. |

### General Principles

- **Actionable**: Logs should help diagnose problems, not just record events
- **Contextual**: Include enough context to understand what happened without code inspection
- **Consistent**: Use same terminology across codebase for same events
- **Sparse**: Don't log everything - unnecessary noise obscures real issues
- **Sampling**: In high-volume scenarios, sample logs (10%, 1%, etc.) rather than logging everything
- **Structured**: Always use structured format (JSON) for programmatic parsing

## 2. Structured Logging Format

### Standard Fields

Every log entry should include:

```json
{
  "timestamp": "2025-11-17T10:30:45.123Z",
  "level": "ERROR",
  "message": "Failed to process user request",
  "service": "auth-service",
  "version": "1.2.3",
  "environment": "production",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "parent_span_id": "0af7651916cd43dd",
  "user_id": "user-12345",
  "request_id": "req-98765",
  "path": "/api/users/authenticate",
  "method": "POST",
  "status_code": 500,
  "error": {
    "type": "InvalidCredentialsError",
    "message": "Provided credentials do not match",
    "stack": "Error: InvalidCredentialsError...",
    "code": "AUTH_INVALID_CREDS"
  },
  "context": {
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "attempt_number": 3,
    "rate_limit_remaining": 2
  },
  "duration_ms": 245,
  "custom_field": "custom_value"
}
```

### Required vs Optional Fields

**Always include:**
- timestamp
- level
- message
- trace_id
- service
- environment

**When applicable:**
- span_id / parent_span_id (distributed tracing)
- user_id (any user action)
- request_id (any request)
- error (on ERROR/FATAL)
- duration_ms (operations)
- context (relevant metadata)

## 3. What to Log

### Application Lifecycle

```json
// Startup
{"timestamp": "...", "level": "INFO", "message": "Service starting", "service": "auth-service", "version": "1.2.3"}

// Configuration loaded
{"timestamp": "...", "level": "INFO", "message": "Configuration loaded", "config_source": "environment", "environment": "production"}

// Database connection established
{"timestamp": "...", "level": "INFO", "message": "Database connected", "host": "db.internal", "pool_size": 20}

// Shutdown
{"timestamp": "...", "level": "INFO", "message": "Service shutting down", "reason": "SIGTERM", "uptime_seconds": 3600}
```

### User Actions

```json
// Login attempt
{"timestamp": "...", "level": "INFO", "message": "User login attempt", "user_id": "user-123", "method": "password"}

// Data modification
{"timestamp": "...", "level": "INFO", "message": "User updated profile", "user_id": "user-123", "fields_changed": ["email", "name"]}

// Permission check
{"timestamp": "...", "level": "INFO", "message": "Permission check", "user_id": "user-123", "resource": "report-456", "permission": "read", "granted": true}
```

### External API Calls

```json
// API call started
{"timestamp": "...", "level": "DEBUG", "message": "External API call", "service": "my-service", "api": "stripe", "endpoint": "/charges", "method": "POST"}

// API response
{"timestamp": "...", "level": "DEBUG", "message": "API response received", "api": "stripe", "endpoint": "/charges", "status_code": 200, "duration_ms": 145}

// API error
{"timestamp": "...", "level": "WARN", "message": "External API error", "api": "stripe", "status_code": 429, "error": "rate_limit_exceeded", "retry_after_seconds": 60}
```

### Errors and Exceptions

```json
{
  "timestamp": "...",
  "level": "ERROR",
  "message": "Payment processing failed",
  "service": "payment-service",
  "user_id": "user-456",
  "error": {
    "type": "PaymentGatewayError",
    "message": "Connection timeout",
    "code": "GATEWAY_TIMEOUT",
    "stack": "PaymentGatewayError: Connection timeout\n    at processPayment (payment.ts:45)\n    at ..."
  },
  "context": {
    "amount": 9999,
    "currency": "USD",
    "gateway": "stripe"
  }
}
```

### Performance Metrics

```json
// Slow operation
{"timestamp": "...", "level": "WARN", "message": "Slow query detected", "duration_ms": 5234, "threshold_ms": 1000, "query": "SELECT * FROM orders WHERE..."}

// Resource usage
{"timestamp": "...", "level": "INFO", "message": "Memory usage high", "memory_used_mb": 2048, "memory_limit_mb": 2560, "percentage": 80}

// Cache statistics
{"timestamp": "...", "level": "DEBUG", "message": "Cache stats", "cache_hits": 4521, "cache_misses": 234, "hit_rate": 0.95}
```

## 4. What NOT to Log

**NEVER log:**
- Passwords or authentication tokens
- API keys or secrets
- Private keys or certificates
- Database credentials
- OAuth tokens or refresh tokens
- Credit card numbers
- Social security numbers
- Email addresses (without redaction in logs)
- Personal identification numbers
- Medical records
- Raw HTTP request/response bodies (especially with auth headers)

**Be careful with:**
- PII in general (name, phone, address) - redact or use anonymized IDs
- Query parameters (may contain secrets)
- Request/response headers (often contain authorization)
- User input (may contain sensitive data)

**Security rule: When in doubt, DON'T log it**

```python
# BAD - logging credentials
logger.info(f"Login attempt for {username} with password {password}")

# GOOD - logging action without sensitive data
logger.info("Login attempt", extra={"username": username, "method": "password"})

# BAD - logging full request with auth header
logger.debug(f"Request: {request.headers}")

# GOOD - logging request metadata
logger.debug("Incoming request", extra={
    "method": request.method,
    "path": request.path,
    "user_agent": request.headers.get('user-agent')
})
```

## 5. Distributed Tracing

### Trace IDs and Span IDs

- **Trace ID**: Unique identifier for entire request flow across services
- **Span ID**: Unique identifier for single operation/service call
- **Parent Span ID**: Span that initiated current span (for tracing parent-child relationships)

Generated once at entry point, propagated through all downstream calls:

```
Request → [Service A, Trace: abc123]
  ├─ [Span: span1] Database query
  ├─ [Span: span2] → Service B, parent: span2
       └─ [Span: span3] Cache lookup
  └─ [Span: span4] External API call
```

### Implementation

```python
# Python example with trace context
import uuid

class RequestContext:
    def __init__(self, trace_id=None, span_id=None, parent_span_id=None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = span_id or str(uuid.uuid4())
        self.parent_span_id = parent_span_id

# Middleware/decorator
def trace_request(func):
    def wrapper(*args, **kwargs):
        ctx = RequestContext()
        return func(*args, context=ctx, **kwargs)
    return wrapper

# Propagate to downstream services
def call_downstream_service(service_url, data, context):
    headers = {
        'X-Trace-ID': context.trace_id,
        'X-Span-ID': context.span_id,
        'X-Parent-Span-ID': context.span_id  # Current becomes parent
    }
    response = requests.post(service_url, json=data, headers=headers)
    return response
```

### Sampling Strategies

- **No sampling**: Log all traces (high volume services may be expensive)
- **Rate sampling**: Log every Nth request (e.g., 1 in 100)
- **Adaptive sampling**: Sample based on error rate, latency, or traffic volume
- **Tail sampling**: Sample based on trace outcome (errors always sampled)

```python
# Adaptive sampling example
def should_sample(trace):
    # Always sample errors
    if trace.has_error:
        return True

    # Sample slow requests (>1s)
    if trace.duration_ms > 1000:
        return True

    # Sample 1% of normal requests
    return random.random() < 0.01
```

## 6. Performance Logging

### Execution Time

```python
import time

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000
            logger.info(f"{func.__name__} completed", extra={
                "duration_ms": duration_ms,
                "status": "success"
            })
            return result
        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            logger.error(f"{func.__name__} failed", extra={
                "duration_ms": duration_ms,
                "error": str(e)
            })
            raise
    return wrapper
```

### Resource Usage

```python
import psutil
import os

def log_resource_usage():
    process = psutil.Process(os.getpid())
    memory = process.memory_info()

    logger.info("Resource usage", extra={
        "memory_rss_mb": memory.rss / 1024 / 1024,
        "memory_vms_mb": memory.vms / 1024 / 1024,
        "cpu_percent": process.cpu_percent(interval=1),
        "num_threads": process.num_threads()
    })
```

### Slow Query Logs

```python
# Track database query performance
SLOW_QUERY_THRESHOLD_MS = 1000

def execute_query(query, params):
    start = time.time()
    cursor.execute(query, params)
    duration_ms = (time.time() - start) * 1000

    if duration_ms > SLOW_QUERY_THRESHOLD_MS:
        logger.warn("Slow query detected", extra={
            "query": query,
            "params_count": len(params),
            "duration_ms": duration_ms,
            "threshold_ms": SLOW_QUERY_THRESHOLD_MS
        })

    return cursor.fetchall()
```

## 7. Debugging Patterns

### Debug Logging

Use DEBUG level for development/troubleshooting only:

```python
logger.debug("Function entry", extra={
    "function": "process_payment",
    "args": {"amount": 100, "currency": "USD"}
})

logger.debug("Intermediate state", extra={
    "processing_step": "validation",
    "validation_passed": True,
    "timestamp": time.time()
})

logger.debug("Function exit", extra={
    "function": "process_payment",
    "return_value": {"transaction_id": "txn-123", "status": "pending"}
})
```

### Conditional Breakpoints

In IDE debugger (VS Code, PyCharm, etc.):

```python
# Set breakpoint with condition
# Debugger pauses only when condition is true
if user_id == "debug-user-123":  # Breakpoint here with condition: amount > 1000
    processor.process(order)
```

### Remote Debugging

Python example:

```python
# Start remote debugger (debugpy)
import debugpy

debugpy.listen(("0.0.0.0", 5678))
print("Debugger attached, waiting for connection...")
debugpy.wait_for_client()

# Then connect from IDE on same port
```

### Log Aggregation for Debugging

```python
# Retrieve logs for specific trace
def get_trace_logs(trace_id):
    query = f"SELECT * FROM logs WHERE trace_id = '{trace_id}' ORDER BY timestamp"
    # Execute against log storage (ELK, Loki, etc.)
    return results

# Filter by user for debugging user issues
def get_user_logs(user_id, hours=1):
    query = f"SELECT * FROM logs WHERE user_id = '{user_id}' AND timestamp > now() - {hours}h"
    return results
```

## 8. Log Management

### Log Rotation

Prevent unbounded disk usage:

```python
# Python logging with rotation
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    filename='app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5       # Keep 5 rotated files
)

# Backup naming: app.log, app.log.1, app.log.2, etc.
```

### Retention Policies

```json
{
  "retention_policy": {
    "DEBUG": "7 days",
    "INFO": "30 days",
    "WARN": "90 days",
    "ERROR": "1 year",
    "FATAL": "indefinite"
  }
}
```

### Log Aggregation Tools

| Tool | Best For | Strengths |
|------|----------|-----------|
| **ELK Stack** (Elasticsearch, Logstash, Kibana) | On-premise, complex queries | Powerful search, rich dashboards, customizable |
| **Grafana Loki** | Simple log aggregation, cost-effective | Low overhead, integrates with Prometheus |
| **Datadog** | Cloud-first, all-in-one | Agent-based, excellent integrations |
| **Splunk** | Enterprise, security focus | Powerful search, alerting, compliance reports |
| **CloudWatch** | AWS native | Seamless AWS integration, log groups |
| **Stackdriver** | GCP native | Google Cloud integration |
| **CloudLogging** | Azure native | Microsoft ecosystem |

## 9. Metrics and Monitoring

### Application Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Counter: monotonically increasing
login_attempts = Counter('login_attempts_total', 'Total login attempts', ['status'])
login_attempts.labels(status='success').inc()

# Histogram: observe value distribution
request_duration = Histogram('request_duration_seconds', 'Request duration')
request_duration.observe(0.5)

# Gauge: can go up or down
active_connections = Gauge('active_connections', 'Current active connections')
active_connections.set(42)
```

### System Metrics

```python
# CPU, memory, disk usage
cpu_percent = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory()
disk = psutil.disk_usage('/')

logger.info("System metrics", extra={
    "cpu_percent": cpu_percent,
    "memory_percent": memory.percent,
    "disk_percent": disk.percent
})
```

### Alerting Rules

```yaml
# Prometheus alert rules
alert: HighErrorRate
expr: rate(requests_total{status="500"}[5m]) > 0.05
for: 5m
annotations:
  summary: "High error rate detected"
  description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.service }}"

alert: SlowRequestLatency
expr: histogram_quantile(0.95, request_duration_seconds) > 1
for: 10m
annotations:
  summary: "Slow requests detected (p95 > 1s)"
```

## 10. Common Libraries by Language

### Python

```python
# Standard library logging
import logging

# Structured logging with structlog
import structlog

logger = structlog.get_logger()
logger.info("user_created", user_id="u123", email_domain="example.com")

# For advanced tracing
from opentelemetry import trace, logging
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
```

**Libraries:**
- `logging` - Built-in, basic structured support
- `structlog` - Structured logging, cleaner API
- `python-json-logger` - JSON formatter for standard logging
- `OpenTelemetry` - Distributed tracing standard
- `Jaeger` - Distributed tracing backend

### Node.js / TypeScript

```javascript
// Winston
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [new winston.transports.Console()]
});

logger.info('User logged in', { userId: 'u123' });

// Pino (lightweight)
const pino = require('pino');
const logger = pino();
logger.info({ userId: 'u123' }, 'User logged in');
```

**Libraries:**
- `winston` - Full-featured, very popular
- `pino` - Lightweight, high performance
- `bunyan` - JSON logging, stream-based
- `morgan` - HTTP request logger for Express
- `OpenTelemetry` - Distributed tracing
- `@opentelemetry/api` - Standard tracing API

### Go

```go
// Structured logging with zap
import "go.uber.org/zap"

logger, _ := zap.NewProduction()
defer logger.Sync()

logger.Info("user login",
    zap.String("user_id", "u123"),
    zap.Duration("duration", time.Second),
)

// Or logrus (JSON support)
import "github.com/sirupsen/logrus"

logger := logrus.New()
logger.SetFormatter(&logrus.JSONFormatter{})
logger.WithFields(logrus.Fields{"user_id": "u123"}).Info("Login")
```

**Libraries:**
- `zap` - High performance, structured
- `logrus` - Popular, JSON output
- `slog` - Standard library (Go 1.21+)
- `OpenTelemetry` - Distributed tracing

### Java / Kotlin

```java
// Logback with SLF4J
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import net.logstash.logback.marker.Markers;

Logger logger = LoggerFactory.getLogger(MyClass.class);

// Structured with logback-json-encoder
logger.info(Markers.append("user_id", "u123"), "User logged in");

// Spring Boot with logback (built-in)
@RestController
public class UserController {
    private static final Logger logger = LoggerFactory.getLogger(UserController.class);
}
```

**Libraries:**
- `SLF4J` + `Logback` - Standard combo
- `Log4j2` - Enterprise feature-rich
- `Logstash Logback Encoder` - Structured output
- `OpenTelemetry` - Distributed tracing

### C# / .NET

```csharp
// Serilog (structured)
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .CreateLogger();

Log.Information("User {UserId} logged in", "u123");

// Built-in ILogger with dependency injection
public class UserService {
    private readonly ILogger<UserService> _logger;

    public UserService(ILogger<UserService> logger) {
        _logger = logger;
    }
}
```

**Libraries:**
- `Serilog` - Excellent structured support
- `NLog` - Enterprise logging
- `log4net` - Classic Apache Log4j port
- `Microsoft.Extensions.Logging` - Built-in DI support
- `OpenTelemetry.Exporter.Console` - Tracing

## 11. Example Patterns

### Complete Request Logging Pipeline (Python)

```python
from datetime import datetime
from uuid import uuid4
import json
import time
import structlog

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
)

class RequestLogger:
    def __init__(self):
        self.logger = structlog.get_logger()

    def log_request_start(self, request):
        trace_id = request.headers.get('X-Trace-ID') or str(uuid4())
        span_id = str(uuid4())

        self.logger.info(
            "request_started",
            trace_id=trace_id,
            span_id=span_id,
            method=request.method,
            path=request.path,
            user_id=request.user_id,
        )

        return trace_id, span_id

    def log_request_complete(self, trace_id, span_id, status, duration_ms):
        level = "info" if status < 400 else "warn" if status < 500 else "error"

        self.logger.log(
            level,
            "request_completed",
            trace_id=trace_id,
            span_id=span_id,
            status_code=status,
            duration_ms=duration_ms,
        )

    def log_error(self, trace_id, span_id, error, context=None):
        self.logger.error(
            "request_error",
            trace_id=trace_id,
            span_id=span_id,
            error_type=type(error).__name__,
            error_message=str(error),
            error_context=context or {},
        )

# Flask integration
app = Flask(__name__)
req_logger = RequestLogger()

@app.before_request
def before_request():
    request.trace_id, request.span_id = req_logger.log_request_start(request)
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration_ms = (time.time() - request.start_time) * 1000
    req_logger.log_request_complete(
        request.trace_id,
        request.span_id,
        response.status_code,
        duration_ms
    )
    return response

@app.errorhandler(Exception)
def handle_error(error):
    req_logger.log_error(
        request.trace_id,
        request.span_id,
        error,
        context={"path": request.path}
    )
    return {"error": "Internal server error"}, 500
```

### Distributed Tracing Example (Node.js)

```typescript
import { trace, context, SpanStatusCode } from '@opentelemetry/api';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger-thrift';

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter({
    host: process.env.JAEGER_HOST || 'localhost',
    port: parseInt(process.env.JAEGER_PORT || '6831'),
  }),
});

sdk.start();

const tracer = trace.getTracer('my-service');

async function processPayment(userId: string, amount: number) {
  const span = tracer.startSpan('processPayment', {
    attributes: {
      'user_id': userId,
      'amount': amount,
      'currency': 'USD',
    }
  });

  return context.with(trace.setSpan(context.active(), span), async () => {
    try {
      // Nested span
      const validationSpan = tracer.startSpan('validatePayment');
      try {
        await validatePayment(userId, amount);
        validationSpan.setStatus({ code: SpanStatusCode.OK });
      } catch (error) {
        validationSpan.recordException(error);
        validationSpan.setStatus({ code: SpanStatusCode.ERROR });
        throw error;
      } finally {
        validationSpan.end();
      }

      // Call external service with trace propagation
      const result = await callPaymentGateway(amount);

      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.recordException(error);
      span.setStatus({ code: SpanStatusCode.ERROR });
      throw error;
    } finally {
      span.end();
    }
  });
}
```

### Security-Conscious Logging (Go)

```go
package main

import (
  "go.uber.org/zap"
  "net/http"
)

// RedactSensitive removes sensitive fields from log data
func RedactSensitive(data map[string]interface{}) map[string]interface{} {
  sensitiveKeys := []string{"password", "api_key", "token", "credit_card", "ssn"}

  for _, key := range sensitiveKeys {
    if _, exists := data[key]; exists {
      data[key] = "[REDACTED]"
    }
  }
  return data
}

func LogRequest(logger *zap.Logger, r *http.Request) {
  // Extract safe headers only
  safeHeaders := map[string]string{
    "user-agent": r.Header.Get("User-Agent"),
    "content-type": r.Header.Get("Content-Type"),
  }

  logger.Info("incoming request",
    zap.String("method", r.Method),
    zap.String("path", r.URL.Path),
    zap.Any("headers", safeHeaders),
    zap.String("remote_addr", r.RemoteAddr),
  )
}

func LogError(logger *zap.Logger, err error, context map[string]interface{}) {
  logger.Error("operation failed",
    zap.Error(err),
    zap.Any("context", RedactSensitive(context)),
  )
}
```

## 12. Quick Reference Checklist

When implementing logging/observability:

- [ ] Use structured JSON logging
- [ ] Include trace_id and span_id in all logs
- [ ] Set appropriate log levels (don't over-log)
- [ ] Never log passwords, keys, tokens, PII
- [ ] Add contextual fields (user_id, request_id, etc.)
- [ ] Implement log rotation to prevent disk overflow
- [ ] Include stack traces for errors
- [ ] Log entry/exit for important functions
- [ ] Track execution time for performance monitoring
- [ ] Sample high-volume logs to prevent storage/bandwidth issues
- [ ] Use existing libraries (structlog, pino, zap, etc.)
- [ ] Set up log aggregation (ELK, Loki, Datadog, etc.)
- [ ] Create alerting rules for critical errors
- [ ] Document logging patterns in team guidelines
- [ ] Review logs regularly to spot issues early

---

**Activate this skill when:** working with logging systems, distributed tracing, debugging, monitoring, performance analysis, or observability-related tasks.

**Combine with:** development-philosophy (fail-fast debugging), security-first-design (never log secrets), testing-workflow (use logs to verify behavior).
