---
name: otel-logging-patterns
description: |
  Implements OpenTelemetry (OTEL) logging with trace context correlation and structured logging. Use when setting up production logging with OTEL exporters, structlog/loguru integration, trace context propagation, and comprehensive test patterns. Covers Python implementations for FastAPI, Kafka consumers, and background jobs. Includes OTLP, Jaeger, and console exporters.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# OpenTelemetry Logging Patterns

## Table of Contents

- [Purpose](#purpose)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Configure OTEL Logging Provider](#step-1-configure-otel-logging-provider)
  - [Step 2: Integrate Structured Logging Library](#step-2-integrate-structured-logging-library)
  - [Step 3: Add Trace Context Propagation](#step-3-add-trace-context-propagation)
  - [Step 4: Set Up Log Exporters](#step-4-set-up-log-exporters)
  - [Step 5: Implement Instrumentation](#step-5-implement-instrumentation)
  - [Step 6: Add Error and Exception Logging](#step-6-add-error-and-exception-logging)
- [Requirements](#requirements)
- [Common Patterns](#common-patterns)
- [Testing OTEL Logging](#testing-otel-logging)
- [Troubleshooting](#troubleshooting)
- [Supporting Resources](#supporting-resources)

## Purpose

This skill provides production-grade OpenTelemetry logging patterns for Python applications. It covers:

- **OTEL Logging Architecture**: Provider and processor configuration
- **Trace Correlation**: Automatic trace context injection into logs
- **Structured Logging**: Integration with structlog for context preservation
- **Log Exporters**: OTLP, Jaeger, console, and file exporters
- **Error Handling**: Comprehensive exception and error logging
- **Testing Patterns**: Unit and integration tests for logging infrastructure
- **Performance**: Optimization tips to minimize logging overhead

This enables production observability where logs, traces, and metrics are correlated through trace IDs for efficient debugging and monitoring.

## Quick Start

**For this project**, use the authoritative OTEL logging module. Get started in 3 simple steps:

1. **Initialize OTEL at application startup** (once):

```python
from app.core.monitoring.otel_logger import initialize_otel_logger

# Call once at app startup
initialize_otel_logger(
    log_level="INFO",
    enable_console=True,
    enable_otlp=True,
    otlp_endpoint="localhost:4317"
)
```

2. **Get logger and tracer in each module**:

```python
from app.core.monitoring.otel_logger import logger, get_tracer

# Module-level initialization
logger = logger(__name__)
tracer = get_tracer(__name__)
```

3. **Use trace_span for operations**:

```python
from app.core.monitoring.otel_logger import trace_span, logger

logger = logger(__name__)

# Logs automatically include trace_id and span_id
with trace_span("process_order", order_id="12345") as span:
    logger.info("processing_order", order_id="12345")
    # Do work...
    logger.info("order_processed", result_count=5)
```

That's it! All logs automatically include trace context, and spans are created with attributes.

**Key Benefits**:
- ✅ Single entry point: `app/core/monitoring/otel_logger.py`
- ✅ No direct imports of structlog or opentelemetry needed
- ✅ Automatic trace context propagation
- ✅ Automatic exception handling in spans
- ✅ Works with async and sync functions

## Instructions

### Step 1: Configure OTEL Logging Provider

Set up the core OpenTelemetry logging infrastructure with provider and exporter configuration.

**Basic setup** (console exporter for development):

```python
# app/shared/otel_config.py
from opentelemetry import logs
from opentelemetry.sdk.logs import LoggerProvider
from opentelemetry.sdk.logs.export import ConsoleLogExporter, SimpleLogRecordExporter
from opentelemetry.sdk.resources import Resource

def setup_console_logging(service_name: str) -> LoggerProvider:
    """Set up OTEL logging with console exporter."""
    resource = Resource.create({"service.name": service_name})
    logger_provider = LoggerProvider(resource=resource)

    exporter = ConsoleLogExporter()
    processor = SimpleLogRecordExporter(exporter)
    logger_provider.add_log_record_processor(processor)
    logs.set_logger_provider(logger_provider)

    return logger_provider
```

**For production OTLP/Jaeger setup**, see [references/advanced-patterns.md](references/advanced-patterns.md#otelconfig-class)

### Step 2: Integrate Structured Logging Library

Set up structlog with OTEL trace context integration:

```python
# app/shared/logging_setup.py
import structlog
from opentelemetry.instrumentation.logging import LoggingInstrumentor

def setup_structlog() -> None:
    """Configure structlog with OTEL trace context integration."""
    # Enable OTEL logging instrumentation
    LoggingInstrumentor().instrument()

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.ExceptionRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.logging.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name: str):
    """Get a logger instance with trace context support."""
    return structlog.logger(name)
```

**For advanced structlog configuration**, see [references/advanced-patterns.md](references/advanced-patterns.md#structlog-configuration)

### Step 3: Add Trace Context Propagation

Ensure trace context flows through logs automatically:

```python
# app/shared/observability.py
from contextvars import ContextVar
from opentelemetry import trace

# Context variables for request tracking
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)
user_id_var: ContextVar[str | None] = ContextVar("user_id", default=None)

class ObservabilityContext:
    """Manage observability context (trace IDs, request IDs, user IDs)."""

    @staticmethod
    def set_request_id(request_id: str) -> None:
        """Set request ID in context."""
        request_id_var.set(request_id)

    @staticmethod
    def get_tracer(name: str):
        """Get tracer instance."""
        return trace.get_tracer(name)

    @staticmethod
    def set_span_attribute(key: str, value: any) -> None:
        """Set attribute on current span."""
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute(key, value)
```

**For complete ObservabilityContext class**, see [references/advanced-patterns.md](references/advanced-patterns.md#observability-context)

### Step 4: Set Up Log Exporters

Configure different exporters for different environments:

```python
# app/config.py
from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    """Configuration for OTEL logging."""

    otel_enabled: bool = Field(default=True)
    otel_exporter_type: str = Field(default="console")  # 'otlp', 'jaeger', or 'console'
    otel_otlp_endpoint: str = Field(default="localhost:4317")
    otel_jaeger_host: str = Field(default="localhost")
    otel_jaeger_port: int = Field(default=6831)
```

Then use config in main:

```python
# main.py
from app.config import Config
from app.shared.logging_setup import setup_structlog, get_logger
from app.shared.otel_config import OTELConfig

async def main() -> None:
    """Main entry point."""
    config = Config()
    setup_structlog()

    if config.otel_enabled:
        otel_config = OTELConfig(
            service_name="my-service",
            exporter_type=config.otel_exporter_type,
            otlp_endpoint=config.otel_otlp_endpoint,
        )
        otel_config.setup_logging()
        otel_config.setup_tracing()

    logger = get_logger(__name__)
    logger.info("service_started")
```

**For complete exporter configuration**, see [references/advanced-patterns.md](references/advanced-patterns.md#exporter-configuration)

### Step 5: Implement Instrumentation

Add tracing and logging to key application flows:

```python
# app/use_cases/extract_orders.py
from opentelemetry import trace
from app.shared.logging_setup import get_logger

class ExtractOrdersUseCase:
    """Use case with observability."""

    def __init__(self, gateway, publisher) -> None:
        self.gateway = gateway
        self.publisher = publisher
        self.logger = get_logger(__name__)
        self.tracer = trace.get_tracer(__name__)

    async def execute(self) -> int:
        """Execute with tracing."""
        with self.tracer.start_as_current_span("extract_orders") as span:
            self.logger.info("starting_extraction")

            try:
                orders = await self.gateway.fetch_all_orders()
                self.logger.info("orders_fetched", count=len(orders))

                for order in orders:
                    await self.publisher.publish(order)

                span.set_attribute("orders_processed", len(orders))
                self.logger.info("extraction_completed", total=len(orders))
                return len(orders)

            except Exception as e:
                self.logger.error("extraction_failed", error=str(e))
                span.record_exception(e)
                raise
```

**For advanced instrumentation patterns**, see [examples/examples.md](examples/examples.md#fastapi-instrumentation)

### Step 6: Add Error and Exception Logging

Implement comprehensive error logging with context:

```python
# app/error_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.shared.logging_setup import get_logger
from app.shared.observability import ObservabilityContext

logger = get_logger(__name__)

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler with OTEL logging."""
    request_id = ObservabilityContext.get_request_id()

    logger.error(
        "unhandled_exception",
        error=str(exc),
        error_type=type(exc).__name__,
        request_id=request_id,
        path=request.url.path,
        method=request.method,
        exc_info=True,  # Include full stack trace
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request_id},
    )

def setup_error_handlers(app: FastAPI) -> None:
    """Register error handlers."""
    app.add_exception_handler(Exception, global_exception_handler)
```

**For complete error handling patterns**, see [examples/examples.md](examples/examples.md#error-handling)

## Requirements

Production OTEL logging requires:

- `opentelemetry-api>=1.22.0` - OTEL API
- `opentelemetry-sdk>=1.22.0` - OTEL SDK with logging support
- `opentelemetry-exporter-otlp>=0.43b0` - OTLP exporter for gRPC
- `opentelemetry-instrumentation-logging>=0.43b0` - Logging instrumentation
- `structlog>=23.2.0` - Structured logging library
- `pydantic>=2.5.0` - Configuration management
- Python 3.11+ with type checking

## Common Patterns

### Trace Context Propagation

Logs automatically include trace_id and span_id when logged within a span:

```python
from opentelemetry import trace
from app.shared.logging_setup import get_logger

logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("process_payment"):
    logger.info("payment_started", customer_id="cust-123")
    logger.info("payment_completed", amount=99.99)
    # All logs have same trace_id and span_id
```

### Context Variables

Use context variables for request-scoped data:

```python
from app.shared.observability import ObservabilityContext

ObservabilityContext.set_request_id("req-12345")
ObservabilityContext.set_user_id("user-456")

logger.info("user_action", action="login")
# Log includes request_id and user_id automatically
```

**For complete pattern examples**, see [examples/examples.md](examples/examples.md)

## Testing OTEL Logging

### Unit Testing

Test logging configuration without external dependencies:

```python
import pytest
from opentelemetry import logs
from opentelemetry.sdk.logs import LoggerProvider

def test_logging_configuration():
    """Test OTEL logging provider setup."""
    logger_provider = LoggerProvider()
    assert logger_provider is not None
    logs.set_logger_provider(logger_provider)
    assert logs.get_logger_provider() == logger_provider
```

### Integration Testing

Test log export with real exporters:

```python
@pytest.fixture
def in_memory_log_exporter():
    """In-memory exporter for testing."""
    class InMemoryExporter:
        def __init__(self):
            self.records = []

        def emit(self, log_records):
            self.records.extend(log_records)

    return InMemoryExporter()

def test_trace_context_in_logs(in_memory_log_exporter):
    """Verify trace context is included in logs."""
    # Setup logger and tracer
    # Log within span
    # Verify trace context in exported logs
    pass
```

**For comprehensive testing patterns**, see [examples/examples.md](examples/examples.md#testing-patterns)

## Troubleshooting

### Common Issues and Solutions

**Issue: Trace IDs not appearing in logs**
- Ensure `LoggingInstrumentor().instrument()` is called before logging
- Verify logs are being created within a span context
- Check that OTEL trace provider is set before creating loggers

**Issue: OTLP exporter connection refused**
- Verify OTEL Collector is running on specified endpoint
- Check endpoint configuration (default: localhost:4317)
- Use console exporter in development
- Check firewall rules for gRPC port 4317

**Issue: High logging overhead**
- Use `BatchLogRecordExporter` instead of `SimpleLogRecordExporter`
- Increase batch size for fewer exports (e.g., 512 records)
- Filter verbose DEBUG logs in production

**Issue: Logs not appearing in output**
- Verify logger is initialized with `setup_structlog()`
- Check Python logging level (INFO, WARNING, ERROR)
- Verify structlog configuration has JSONRenderer processor

**For detailed troubleshooting**, see [references/advanced-patterns.md](references/advanced-patterns.md#troubleshooting-guide)

## Supporting Resources

| Resource | Purpose |
|----------|---------|
| [`examples/examples.md`](./examples/examples.md) | 10+ complete examples covering FastAPI, Kafka, background jobs, testing |
| [`references/advanced-patterns.md`](./references/advanced-patterns.md) | Performance tuning, custom exporters, trace propagation details |
