---
name: logging-fundamentals
description: Implement proper logging practices including log levels, structured logging, context propagation, and logging best practices for applications and systems
license: MIT
compatibility: opencode
metadata:
  audience: developers, SREs, DevOps engineers
  category: observability
---

# Logging Fundamentals

Establish proper logging practices including log levels, structured logging, context propagation, and comprehensive logging strategies for applications, services, and infrastructure.

## When to use me

Use this skill when:
- Setting up logging for new applications or services
- Reviewing existing logging implementations
- Establishing logging standards for teams or projects
- Debugging issues with incomplete or poor logging
- Implementing structured logging for better observability
- Configuring log levels and verbosity for different environments
- Ensuring logs contain sufficient context for troubleshooting

## What I do

### 1. Log Level Management
- **Define appropriate log levels** (DEBUG, INFO, WARN, ERROR, FATAL)
- **Configure level filtering** per environment (development, staging, production)
- **Implement dynamic level adjustment** without application restarts
- **Establish level usage guidelines** for different types of information
- **Create level-based alerting thresholds** for operational monitoring

### 2. Structured Logging Implementation
- **Design log schema** with consistent field naming and types
- **Implement structured formats** (JSON, key-value pairs, structured text)
- **Include mandatory context fields** (timestamp, service, trace_id, user_id, etc.)
- **Handle nested structures and arrays** appropriately in logs
- **Ensure PII (Personally Identifiable Information) compliance** in log content

### 3. Context Propagation
- **Implement correlation IDs** for request tracing across services
- **Propagate context through async operations** (queues, background jobs)
- **Maintain user/session context** throughout request lifecycle
- **Include business context** (order_id, transaction_id, etc.) in logs
- **Handle context in distributed systems** with proper header propagation

### 4. Log Content Best Practices
- **Include sufficient context** for debugging without external systems
- **Balance detail with noise** - log enough but not too much
- **Use consistent message formats** across the codebase
- **Log before and after significant operations**
- **Include error details** (stack traces, error codes, recovery suggestions)
- **Avoid logging secrets, passwords, or sensitive data**

### 5. Environment-Specific Configuration
- **Development logging** - Verbose, human-readable, local file output
- **Staging logging** - Balanced detail, structured format, aggregation
- **Production logging** - Minimal noise, structured only, remote aggregation
- **Debug mode logging** - Temporary increased verbosity for troubleshooting

## Logging Principles

### The 5 Ws of Logging
1. **WHO** - Which user/service/process generated the log?
2. **WHAT** - What action/event is being logged?
3. **WHEN** - Precise timestamp with timezone information
4. **WHERE** - Which component/function/file generated the log?
5. **WHY** - What is the significance/severity of the logged event?

### Structured Logging Fields
```json
{
  "timestamp": "2026-02-26T18:00:00Z",
  "level": "ERROR",
  "service": "payment-service",
  "component": "process_payment",
  "trace_id": "abc123-def456",
  "span_id": "def456",
  "user_id": "user-789",
  "session_id": "session-xyz",
  "request_id": "req-123456",
  "message": "Payment processing failed",
  "error_code": "PAYMENT_GATEWAY_TIMEOUT",
  "error_details": "Gateway response timeout after 5000ms",
  "stack_trace": "...",
  "context": {
    "order_id": "ord-987654",
    "amount": 99.99,
    "currency": "USD"
  },
  "duration_ms": 5123,
  "environment": "production",
  "hostname": "payment-host-01",
  "version": "1.2.3"
}
```

### Log Level Guidelines
- **DEBUG**: Detailed information for debugging, typically disabled in production
- **INFO**: Routine information about normal operation
- **WARN**: Warning conditions that might require attention but don't indicate failure
- **ERROR**: Error conditions that indicate failure of a specific operation
- **FATAL**: Critical errors that cause application termination

## Examples

```bash
# Configure logging levels by environment
npm run logging:configure -- --environment production --level WARN

# Analyze current logging implementation
npm run logging:analyze -- --path src/ --output logging-report.json

# Generate structured logging configuration
npm run logging:generate-config -- --format json --output logging-config.json

# Test logging output
npm run logging:test -- --scenario "payment-failure" --levels "ERROR,WARN"

# Validate logging best practices
npm run logging:validate -- --strict --check-pii --check-context
```

## Output format

### Logging Configuration Template:
```yaml
logging:
  level: 
    root: INFO
    specific:
      "com.example.service": DEBUG
      "org.springframework": WARN
  
  format:
    type: json
    timestamp_format: "ISO8601"
    include_fields:
      - timestamp
      - level  
      - service
      - component
      - trace_id
      - message
    
  context:
    auto_included:
      - thread_id
      - hostname
      - service_version
    propagated:
      - trace_id
      - user_id
      - request_id
    
  appenders:
    - type: console
      level: INFO
    - type: file
      path: /var/log/app.log
      level: WARN
    - type: http
      endpoint: https://logs.example.com
      level: ERROR
```

### Logging Best Practices Report:
```
Logging Fundamentals Assessment
───────────────────────────────
Application: payment-service
Assessment Date: 2026-02-26
Score: 78/100

Strengths:
✅ Structured logging implemented (JSON format)
✅ Correlation IDs propagated across services
✅ Log levels appropriately configured
✅ PII filtering in place

Areas for Improvement:
⚠️  Insufficient context in error logs (missing user_id in 45% of error logs)
⚠️  Debug logs enabled in production for some components
⚠️  Inconsistent timestamp formats across services
⚠️  Missing business context in 30% of transaction logs

Critical Issues:
❌ No log sampling for high-volume debug logs
❌ Secret leakage detected in 2 log patterns
❌ Incomplete error context for 15% of database errors

Recommendations:
1. Implement consistent context inclusion middleware
2. Configure log sampling for debug-level logs
3. Add business context to all transaction logs
4. Update secret detection patterns
5. Standardize timestamp format across services

Implementation Priority:
- High: Fix secret leakage immediately
- Medium: Add missing context fields
- Low: Standardize timestamp format
```

## Notes

- **Structured logging is essential** for modern log analysis and observability
- **Context is more important than message content** - ensure logs can be correlated
- **Log levels should reflect operational importance**, not developer convenience
- **Consider log volume** - too many logs can overwhelm systems and teams
- **Test logging in production-like environments** - logging behavior can differ
- **Monitor your logging** - ensure logs are being captured, processed, and stored
- **Regularly review and update** logging practices as systems evolve
- **Balance human readability with machine parsability** in log formats
- **Document logging standards** and ensure team adherence
- **Consider the cost** of logging - storage, processing, and analysis have expenses