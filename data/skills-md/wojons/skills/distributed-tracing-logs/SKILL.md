---
name: distributed-tracing-logs
description: Implement distributed tracing using logs, including trace context propagation, span logging, correlation IDs, and OpenTelemetry integration for observability
license: MIT
compatibility: opencode
metadata:
  audience: developers, SREs, platform engineers
  category: observability
---

# Distributed Tracing with Logs

Implement distributed tracing using logs by propagating trace context, creating span logs, using correlation IDs, and integrating with OpenTelemetry standards to enable end-to-end request tracing across distributed systems.

## When to use me

Use this skill when:
- Building or maintaining distributed systems (microservices, serverless functions)
- Need to trace requests across multiple service boundaries
- Debugging issues that span multiple components or services
- Implementing observability for complex workflows
- Correlating logs from different services for a single user request
- Setting up OpenTelemetry or other tracing standards
- Analyzing latency and performance across service boundaries
- Implementing request context propagation
- Building audit trails for business transactions

## What I do

### 1. Trace Context Propagation
- **Generate trace and span IDs** for request initiation
- **Propagate context through HTTP headers** across services
- **Maintain context through async operations** (queues, background jobs, callbacks)
- **Handle context in batch processing** and streaming systems
- **Implement context extraction and injection** middleware
- **Manage sampling decisions** for trace collection

### 2. Span Logging
- **Create span start/end logs** with timing information
- **Log span attributes and events** during execution
- **Capture parent-child relationships** between spans
- **Record span status and errors** for failed operations
- **Include business context** in span logs
- **Implement span baggage** for custom key-value propagation

### 3. Correlation & Context Management
- **Generate correlation IDs** for business transactions
- **Link logs to traces** through trace_id fields
- **Maintain user/session context** across service boundaries
- **Propagate business identifiers** (order_id, transaction_id, etc.)
- **Handle context in distributed transactions**
- **Implement context storage and retrieval** for long-running operations

### 4. OpenTelemetry Integration
- **Implement OpenTelemetry SDKs** for various languages
- **Configure trace exporters** (Jaeger, Zipkin, OTEL Collector, etc.)
- **Set up automatic instrumentation** for common frameworks
- **Define custom spans and attributes** for business logic
- **Configure sampling strategies** for production environments
- **Integrate with existing logging infrastructure**

### 5. Trace Analysis & Visualization
- **Extract trace information from logs** for analysis
- **Calculate trace duration and latency** across services
- **Identify critical paths and bottlenecks**
- **Correlate traces with business metrics**
- **Create trace visualizations** and dependency graphs
- **Set up trace-based alerting** for performance degradation

## Trace Context Propagation

### W3C Trace Context Standard
The W3C Trace Context specification defines standard HTTP headers for trace propagation:

```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
tracestate: congo=t61rcWkgMzE
```

**Header format:**
- `traceparent`: `00-{trace-id}-{span-id}-{trace-flags}`
- `tracestate`: Vendor-specific trace state information

### Propagation Methods

#### HTTP Headers (Synchronous calls)
```http
GET /api/users HTTP/1.1
Host: api.example.com
Traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
X-Correlation-Id: tx-123456
X-Request-Id: req-789012
```

#### Message Queues (Asynchronous)
```json
{
  "headers": {
    "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
    "correlation_id": "tx-123456"
  },
  "body": {
    "order_id": "ord-789",
    "amount": 99.99
  }
}
```

#### Database Operations
```sql
-- Include trace context in audit fields
INSERT INTO orders (id, amount, trace_id, span_id, created_at)
VALUES ('ord-789', 99.99, '0af7651916cd43dd8448eb211c80319c', 'b7ad6b7169203331', NOW());
```

## Span Logging Patterns

### Basic Span Logging
```json
{
  "timestamp": "2026-02-26T18:00:00Z",
  "level": "INFO",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "span_name": "process_payment",
  "span_kind": "SERVER",
  "event": "span_start",
  "duration_ms": 0,
  "attributes": {
    "order_id": "ord-789",
    "payment_method": "credit_card",
    "amount": 99.99
  }
}
```

```json
{
  "timestamp": "2026-02-26T18:00:00.123Z",
  "level": "INFO",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "span_name": "process_payment",
  "span_kind": "SERVER",
  "event": "span_end",
  "duration_ms": 123,
  "status": "OK",
  "attributes": {
    "order_id": "ord-789",
    "payment_id": "pay-456",
    "gateway_response": "success"
  }
}
```

### Error Span Logging
```json
{
  "timestamp": "2026-02-26T18:00:00Z",
  "level": "ERROR",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "span_name": "process_payment",
  "span_kind": "SERVER",
  "event": "span_end",
  "duration_ms": 5123,
  "status": "ERROR",
  "error_code": "PAYMENT_GATEWAY_TIMEOUT",
  "error_message": "Payment gateway timeout after 5000ms",
  "stack_trace": "...",
  "attributes": {
    "order_id": "ord-789",
    "retry_count": 3,
    "gateway": "stripe"
  }
}
```

### Nested Span Logging
```json
{
  "timestamp": "2026-02-26T18:00:00Z",
  "level": "INFO",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "parent_span_id": "c8be7c825a934b7d",
  "span_name": "charge_card",
  "span_kind": "INTERNAL",
  "event": "span_start",
  "duration_ms": 0,
  "attributes": {
    "order_id": "ord-789",
    "card_last4": "4242"
  }
}
```

## OpenTelemetry Integration

### Manual Instrumentation
```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

def process_payment(order_id, amount):
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("order_id", order_id)
        span.set_attribute("amount", amount)
        
        try:
            # Business logic
            result = charge_credit_card(order_id, amount)
            span.set_status(Status(StatusCode.OK))
            span.set_attribute("payment_id", result.payment_id)
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise
```

### Automatic Instrumentation
Configuration for automatic instrumentation of common frameworks:

```yaml
opentelemetry:
  instrumentations:
    - name: "opentelemetry-instrumentation-flask"
      enabled: true
    - name: "opentelemetry-instrumentation-sqlalchemy"
      enabled: true
    - name: "opentelemetry-instrumentation-requests"
      enabled: true
  
  sampling:
    type: "parentbased_traceidratio"
    ratio: 0.1  # Sample 10% of traces in production
  
  exporters:
    - type: "otlp"
      endpoint: "http://otel-collector:4317"
    - type: "logging"  # Also log spans for local debugging
  
  resource:
    attributes:
      service.name: "payment-service"
      service.version: "1.2.3"
      deployment.environment: "production"
```

## Examples

```bash
# Generate trace context for new request
npm run tracing:generate-context -- --service payment-service --output context.json

# Propagate trace context through HTTP call
npm run tracing:propagate -- --trace-id abc123 --span-id def456 --target http://api.example.com

# Analyze trace from logs
npm run tracing:analyze -- --trace-id abc123 --sources "app.log,api.log,db.log" --output trace.json

# Set up OpenTelemetry instrumentation
npm run tracing:setup-otel -- --language nodejs --exporter jaeger --sampling-ratio 0.1

# Extract trace timeline from logs
npm run tracing:timeline -- --trace-id abc123 --output timeline.html
```

## Output format

### Trace Context Configuration:
```yaml
tracing:
  standard: "W3C TraceContext"
  headers:
    traceparent: "traceparent"
    tracestate: "tracestate"
    correlation_id: "X-Correlation-Id"
    request_id: "X-Request-Id"
  
  propagation:
    http: true
    messaging: true
    database: true
    rpc: true
    
  sampling:
    strategy: "probability"
    rate: 0.1  # 10% sampling in production
    decision_deferred: false
    
  span_logging:
    enabled: true
    format: "json"
    include_fields:
      - trace_id
      - span_id
      - parent_span_id
      - span_name
      - span_kind
      - event
      - duration_ms
      - status
    events:
      - span_start
      - span_end
      - span_event
      - span_error
      
  correlation:
    business_ids:
      - order_id
      - user_id
      - transaction_id
      - session_id
```

### Trace Analysis Report:
```
Distributed Trace Analysis
─────────────────────────
Trace ID: 0af7651916cd43dd8448eb211c80319c
Start Time: 2026-02-26T18:00:00Z
Duration: 1.234s
Status: ERROR (partial failure)

Services Involved:
1. api-gateway (entry point)
2. auth-service (authentication)
3. payment-service (payment processing)
4. notification-service (notifications)
5. database (persistence)

Span Timeline:
00.000ms - api-gateway: request_received (span_start)
00.123ms - api-gateway: auth_check (span_start)
00.234ms - auth-service: validate_token (span_start)
00.345ms - auth-service: validate_token (span_end) [OK]
00.456ms - api-gateway: auth_check (span_end) [OK]
00.567ms - payment-service: process_payment (span_start)
01.234ms - payment-service: charge_card (span_start)
05.678ms - payment-service: charge_card (span_end) [ERROR: timeout]
05.789ms - payment-service: process_payment (span_end) [ERROR]
05.890ms - api-gateway: request_completed (span_end) [ERROR]

Critical Path Analysis:
- Total duration: 1.234s
- Payment processing: 1.111s (90% of total time)
- Card charging: 4.444s (within payment processing)
- Card charging timeout at 5.000ms

Error Analysis:
- Root cause: Payment gateway timeout
- Impact: Payment failed, user notified
- Recovery: Automatic retry scheduled
- Alternative flows: None configured

Performance Insights:
- Slowest service: payment-service (1.111s)
- Fastest service: auth-service (0.111ms)
- Bottleneck: External payment gateway call
- Recommendation: Implement circuit breaker for payment gateway

Business Context:
- User ID: user-123
- Order ID: ord-789
- Amount: $99.99
- Payment method: credit_card
- Outcome: Failed (gateway timeout)
```

## Notes

- **Trace context should be propagated consistently** across all service boundaries
- **Sampling is essential in production** to manage volume and cost
- **Span logs should include business context** for meaningful analysis
- **Trace visualization requires complete context** from all services
- **Consider trace storage and retention** policies for compliance
- **Monitor trace collection and processing** for reliability
- **Implement trace-based alerting** for performance degradation detection
- **Test trace propagation** in all communication patterns (sync, async, batch)
- **Document trace standards** for development teams
- **Regularly review trace sampling rates** based on volume and importance