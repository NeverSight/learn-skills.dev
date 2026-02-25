---
name: phoenix-observability
description: "Open-source AI observability platform for LLM tracing, evaluation, and monitoring. Use when debugging LLM applications with detailed traces, running evaluations on datasets, monitoring production AI systems, or setting up observability infrastructure for agentic systems. **PROACTIVE ACTIVATION**: Auto-invoke when implementing observability/tracing for LLM agents, setting up evaluation pipelines, or configuring OpenTelemetry instrumentation. **DETECTION**: Check for arize-phoenix imports, OpenTelemetry setup, or observability-related code. **USE CASES**: Debugging LLM apps, running evaluations, monitoring production systems, setting up tracing infrastructure, instrumenting agent frameworks, tracing custom agents with decorators (@tracer.agent, @tracer.chain, @tracer.tool)."
author: mguinada
version: 1.0.0
tags: [observability, phoenix, arize, tracing, evaluation, monitoring, llm-ops, opentelemetry, agents]
---

# Phoenix - AI Observability Platform

Open-source AI observability and evaluation platform for LLM applications with tracing, evaluation, datasets, experiments, and real-time monitoring.

## When to Use Phoenix

- **Debugging LLM applications** with detailed traces and span analysis
- **Running systematic evaluations** on datasets with LLM-as-judge
- **Monitoring production LLM systems** with real-time insights
- **Building experiment pipelines** for prompt/model comparison
- **Self-hosted observability** without vendor lock-in

## Key Features

- **Tracing**: OpenTelemetry-based trace collection for any LLM framework
- **Evaluation**: LLM-as-judge evaluators for quality assessment
- **Datasets**: Versioned test sets for regression testing
- **Experiments**: Compare prompts, models, and configurations
- **Open-source**: Self-hosted with PostgreSQL or SQLite

## Quick Start

### Installation

```bash
pip install arize-phoenix
# With specific features
pip install arize-phoenix[embeddings]  # Embedding analysis
pip install arize-phoenix-otel         # OpenTelemetry config
pip install arize-phoenix-evals        # Evaluation framework
```

### Launch Phoenix Server

```python
import phoenix as px
# Launch in notebook
session = px.launch_app()
# View UI
session.view()  # Embedded iframe
print(session.url)  # http://localhost:6006
```

### Command-line Server

```bash
# Start Phoenix server
phoenix serve

# With PostgreSQL backend
export PHOENIX_SQL_DATABASE_URL="postgresql://user:pass@host/db"
phoenix serve --port 6006
```

### Basic Tracing

```python
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# Configure OpenTelemetry with Phoenix
tracer_provider = register(
    project_name="my-llm-app",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument OpenAI SDK
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

# All OpenAI calls are now traced
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Custom Agents with Decorators

For framework-agnostic agentic systems, use `@tracer.agent`, `@tracer.chain`, and `@tracer.tool` decorators:

```python
from openinference.instrumentation import Instrumentor
from phoenix.otel import register

tracer_provider = register(project_name="custom-agent")
instrumentor = Instrumentor(tracer_provider=tracer_provider)

@instrumentor.agent
def my_agent(query: str) -> str:
    context = search_tool(query)
    return synthesize_tool(context, query)

@instrumentor.tool
def search_tool(query: str) -> list:
    return vector_store.search(query)

@instrumentor.tool
def synthesize_tool(context: list, query: str) -> str:
    return llm.generate(query, context)
```

For detailed tracing patterns, see [tracing-setup.md](references/tracing-setup.md).

## Storage Backends

Phoenix supports both SQLite and PostgreSQL for persistent storage:

- **SQLite**: Simple, file-based storage (default, ideal for development)
- **PostgreSQL**: Production-ready database for scalability and concurrent access

For detailed configuration examples, see [storage-backends.md](references/storage-backends.md).

## Docker Deployment

For containerized deployment, see [docker-deployment.md](references/docker-deployment.md) for:
- Docker compose files for both SQLite and PostgreSQL
- Production-ready configuration
- Multi-container setup

## Tracing Setup

For comprehensive tracing setup with OpenTelemetry, see [tracing-setup.md](references/tracing-setup.md):
- **Framework-agnostic decorators**: `@tracer.agent`, `@tracer.chain`, `@tracer.tool` for custom agents
- Manual instrumentation with OpenTelemetry API
- Automatic instrumentation for LLM frameworks
- Distributed tracing for multi-service applications
- Custom span attributes and context propagation

## Framework Integrations

Phoenix provides auto-instrumentation for many LLM frameworks. For detailed integration guides, see:

- **[framework-integrations.md](references/framework-integrations.md)**: Complete list of supported frameworks
  - DSPy, LangChain, LlamaIndex, Agno, AutoGen, CrewAI, and more
  - Provider-specific integrations (OpenAI, Anthropic, Bedrock, etc.)
  - Platform integrations (Dify, Flowise, LangFlow)

## Core Concepts

### Traces and Spans

A **trace** represents a complete execution flow, while **spans** are individual operations within that trace.

```python
from phoenix.otel import register
from opentelemetry import trace

# Setup tracing
tracer_provider = register(project_name="my-app")
tracer = trace.get_tracer(__name__)

# Create custom spans
with tracer.start_as_current_span("process_query") as span:
    span.set_attribute("input.value", query)
    # Child spans are automatically nested
    with tracer.start_as_current_span("retrieve_context"):
        context = retriever.search(query)
    with tracer.start_as_current_span("generate_response"):
        response = llm.generate(query, context)
    span.set_attribute("output.value", response)
```

### Projects

Projects organize related traces:

```python
import os
os.environ["PHOENIX_PROJECT_NAME"] = "production-chatbot"

# Or per-trace
from phoenix.otel import register
tracer_provider = register(project_name="experiment-v2")
```

## Evaluation Framework

### Built-in Evaluators

```python
from phoenix.evals import (
    OpenAIModel,
    HallucinationEvaluator,
    RelevanceEvaluator,
    ToxicityEvaluator,
)

# Setup model for evaluation
eval_model = OpenAIModel(model="gpt-4o")

# Evaluate hallucination
hallucination_eval = HallucinationEvaluator(eval_model)
results = hallucination_eval.evaluate(
    input="What is the capital of France?",
    output="The capital of France is Paris.",
    reference="Paris is the capital of France."
)
```

### Run Evaluations on Dataset

```python
from phoenix import Client
from phoenix.evals import run_evals

client = Client()

# Get spans to evaluate
spans_df = client.get_spans_dataframe(
    project_name="my-app",
    filter_condition="span_kind == 'LLM'"
)

# Run evaluations
eval_results = run_evals(
    dataframe=spans_df,
    evaluators=[
        HallucinationEvaluator(eval_model),
        RelevanceEvaluator(eval_model)
    ],
    provide_explanation=True
)

# Log results back to Phoenix
client.log_evaluations(eval_results)
```

## Client API

### Query Traces and Spans

```python
from phoenix import Client

client = Client(endpoint="http://localhost:6006")

# Get spans as DataFrame
spans_df = client.get_spans_dataframe(
    project_name="my-app",
    filter_condition="span_kind == 'LLM'",
    limit=1000
)

# Get specific span
span = client.get_span(span_id="abc123")

# Get trace
trace = client.get_trace(trace_id="xyz789")
```

### Log Feedback

```python
from phoenix import Client

client = Client()

# Log user feedback
client.log_annotation(
    span_id="abc123",
    name="user_rating",
    annotator_kind="HUMAN",
    score=0.8,
    label="helpful",
    metadata={"comment": "Good response"}
)
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PHOENIX_PORT` | HTTP server port | `6006` |
| `PHOENIX_HOST` | Server bind address | `127.0.0.1` |
| `PHOENIX_GRPC_PORT` | gRPC/OTLP port | `4317` |
| `PHOENIX_SQL_DATABASE_URL` | Database connection | SQLite temp |
| `PHOENIX_WORKING_DIR` | Data storage directory | OS temp |
| `PHOENIX_ENABLE_AUTH` | Enable authentication | `false` |
| `PHOENIX_SECRET` | JWT signing secret | Required if auth enabled |

## Best Practices

1. **Use projects**: Separate traces by environment (dev/staging/prod)
2. **Add metadata**: Include user IDs, session IDs for debugging
3. **Evaluate regularly**: Run automated evaluations in CI/CD
4. **Version datasets**: Track test set changes over time
5. **Monitor costs**: Track token usage via Phoenix dashboards
6. **Self-host**: Use PostgreSQL for production deployments

## Common Issues

### Traces Not Appearing

```python
from phoenix.otel import register

# Verify endpoint
tracer_provider = register(
    project_name="my-app",
    endpoint="http://localhost:6006/v1/traces"  # Correct endpoint
)

# Force flush
from opentelemetry import trace
trace.get_tracer_provider().force_flush()
```

### Database Connection Issues

```bash
# Verify PostgreSQL connection
psql $PHOENIX_SQL_DATABASE_URL -c "SELECT 1"

# Check Phoenix logs
phoenix serve --log-level debug
```

## Resources

- **Documentation**: https://docs.arize.com/phoenix
- **Repository**: https://github.com/Arize-ai/phoenix
- **Docker Hub**: https://hub.docker.com/r/arizephoenix/phoenix
- **Version**: 12.0.0+
- **License**: Apache 2.0
