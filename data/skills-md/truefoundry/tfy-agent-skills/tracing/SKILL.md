---
name: tracing
description: Adds OpenTelemetry-based tracing to applications via TrueFoundry's tracing platform (Traceloop SDK). Creates tracing projects, instruments Python/TypeScript code, and captures LLM calls and custom spans.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *) Bash(pip*) Bash(npm*)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Tracing

Add OpenTelemetry-based tracing and observability to applications using TrueFoundry's tracing platform (powered by Traceloop SDK). Creates tracing projects, installs dependencies, and instruments code to capture LLM calls, workflows, and custom spans.

## When to Use

Set up tracing projects, install Traceloop SDK, and instrument Python or TypeScript applications for LLM call tracing and observability on TrueFoundry.

</objective>

<instructions>

## Step 1: Preflight

Run the `status` skill first to verify `TFY_BASE_URL` and `TFY_API_KEY` are set and valid.

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

## Step 2: Tracing Project Setup

Ask the user: **"Do you already have a tracing project FQN, or should I create one?"**

### List Existing Projects

#### Via Tool Call
```
tfy_tracing_list_projects()
```

#### Via Direct API
```bash
TFY_API_SH=~/.claude/skills/truefoundry-tracing/scripts/tfy-api.sh

# List tracing projects
$TFY_API_SH GET /api/ml/v1/tracing-projects
```

### Create a New Project

Ask for a project name, then create:

#### Via Tool Call
```
tfy_tracing_create_project(name="my-tracing-project")
```

#### Via Direct API
```bash
# Create tracing project
$TFY_API_SH POST /api/ml/v1/tracing-projects '{"name": "my-tracing-project"}'
```

Save the returned project `id` for the next step.

### Create an Application Under the Project

Each tracing project can have multiple applications (e.g., "chatbot", "rag-pipeline").

#### Via Tool Call
```
tfy_tracing_create_application(project_id="PROJECT_ID", name="my-app")
```

#### Via Direct API
```bash
# Create application under project
$TFY_API_SH POST /api/ml/v1/tracing-projects/PROJECT_ID/applications '{"name": "my-app"}'
```

> **Fallback**: If any of these API endpoints return 404, the tracing API may have changed. Direct the user to create the tracing project via the TrueFoundry UI at `$TFY_BASE_URL` → Tracing section, then return here with the project FQN.

## Step 3: Detect Application Type

Scan the project to determine the language and LLM libraries in use:

1. **Python** — look for `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`
   - Check for LLM libraries: `openai`, `anthropic`, `langchain`, `llama-index`, `litellm`, `cohere`, `bedrock`, `vertexai`, `transformers`
2. **TypeScript/JavaScript** — look for `package.json`
   - Check for LLM libraries: `openai`, `@anthropic-ai/sdk`, `langchain`, `@langchain/core`

Report what was detected to the user before proceeding.

## Step 4: Install Dependencies

### Python
```bash
pip install traceloop-sdk
```

Also add `traceloop-sdk` to `requirements.txt` or the appropriate dependency file.

### TypeScript/JavaScript
```bash
npm install @traceloop/node-server-sdk
```

Also add to `package.json` dependencies.

## Step 5: Instrument the Application

**CRITICAL**: `Traceloop.init()` MUST be called at the TOP of the entry point, BEFORE any LLM library imports. This is required for auto-instrumentation to work.

### Python Instrumentation

Add this to the very top of the entry point file (e.g., `main.py`, `app.py`):

```python
# --- Traceloop init MUST be before any LLM imports ---
from traceloop.sdk import Traceloop

Traceloop.init(
    app_name="<APP_NAME>",
    api_endpoint=f"<TFY_BASE_URL>/api/otel",
    headers={
        "Authorization": f"Bearer <TFY_API_KEY>",
        "X-TFY-TRACING-PROJECT-FQN": "<TRACING_PROJECT_FQN>",
    },
    disable_batch=False,
)

# --- Now import LLM libraries ---
# from openai import OpenAI
# from anthropic import Anthropic
# etc.
```

Replace placeholders:
- `<APP_NAME>` — the application name (e.g., "my-chatbot")
- `<TFY_BASE_URL>` — from environment or `.env`
- `<TFY_API_KEY>` — from environment or `.env`
- `<TRACING_PROJECT_FQN>` — the tracing project FQN from Step 2

**Best practice**: Read `TFY_BASE_URL` and `TFY_API_KEY` from environment variables:

```python
import os
from traceloop.sdk import Traceloop

Traceloop.init(
    app_name="<APP_NAME>",
    api_endpoint=f"{os.environ['TFY_BASE_URL']}/api/otel",
    headers={
        "Authorization": f"Bearer {os.environ['TFY_API_KEY']}",
        "X-TFY-TRACING-PROJECT-FQN": "<TRACING_PROJECT_FQN>",
    },
    disable_batch=False,
)
```

### TypeScript/JavaScript Instrumentation

Add this to the very top of the entry point file (e.g., `index.ts`, `app.ts`):

```typescript
// --- Traceloop init MUST be before any LLM imports ---
import * as traceloop from "@traceloop/node-server-sdk";

traceloop.initialize({
  appName: "<APP_NAME>",
  apiEndpoint: `${process.env.TFY_BASE_URL}/api/otel`,
  headers: {
    Authorization: `Bearer ${process.env.TFY_API_KEY}`,
    "X-TFY-TRACING-PROJECT-FQN": "<TRACING_PROJECT_FQN>",
  },
  disableBatch: false,
});

// --- Now import LLM libraries ---
// import OpenAI from "openai";
// etc.
```

## Step 6: Optional — Add Decorators for Multi-Step Apps

For applications with multiple logical steps (agents, RAG pipelines, etc.), offer to add decorators for better trace structure:

### Python Decorators

```python
from traceloop.sdk.decorators import workflow, task, agent, tool

@workflow(name="rag_pipeline")
def run_pipeline(query: str):
    context = retrieve(query)
    return generate(query, context)

@task(name="retrieve_context")
def retrieve(query: str):
    # retrieval logic
    ...

@task(name="generate_response")
def generate(query: str, context: str):
    # LLM call
    ...

@agent(name="research_agent")
def research_agent(topic: str):
    # agent logic
    ...

@tool(name="web_search")
def web_search(query: str):
    # tool logic
    ...
```

### TypeScript Decorators

```typescript
import { withWorkflow, withTask, withAgent, withTool } from "@traceloop/node-server-sdk";

const runPipeline = withWorkflow({ name: "rag_pipeline" }, async (query: string) => {
  const context = await retrieve(query);
  return generate(query, context);
});

const retrieve = withTask({ name: "retrieve_context" }, async (query: string) => {
  // retrieval logic
});

const generate = withTask({ name: "generate_response" }, async (query: string, context: string) => {
  // LLM call
});
```

## Step 7: Optional — Configure Sampling for Production

For high-traffic production apps, configure sampling to reduce trace volume:

### Python
```python
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased

Traceloop.init(
    app_name="<APP_NAME>",
    api_endpoint=f"{os.environ['TFY_BASE_URL']}/api/otel",
    headers={
        "Authorization": f"Bearer {os.environ['TFY_API_KEY']}",
        "X-TFY-TRACING-PROJECT-FQN": "<TRACING_PROJECT_FQN>",
    },
    disable_batch=False,
    sampler=ParentBased(root=TraceIdRatioBased(0.1)),  # 10% sampling
)
```

### TypeScript
```typescript
import { ParentBasedSampler, TraceIdRatioBasedSampler } from "@opentelemetry/sdk-trace-base";

traceloop.initialize({
  appName: "<APP_NAME>",
  apiEndpoint: `${process.env.TFY_BASE_URL}/api/otel`,
  headers: {
    Authorization: `Bearer ${process.env.TFY_API_KEY}`,
    "X-TFY-TRACING-PROJECT-FQN": "<TRACING_PROJECT_FQN>",
  },
  disableBatch: false,
  sampler: new ParentBasedSampler({ root: new TraceIdRatioBasedSampler(0.1) }), // 10%
});
```

</instructions>

<success_criteria>

## Success Criteria

- Tracing project exists (created or pre-existing) on TrueFoundry
- `traceloop-sdk` (Python) or `@traceloop/node-server-sdk` (TypeScript) is installed
- `Traceloop.init()` is placed at the top of the entry point, BEFORE LLM imports
- Auth headers include `Authorization` and `X-TFY-TRACING-PROJECT-FQN`
- The app runs without import errors
- Traces appear in the TrueFoundry tracing dashboard after a test request

</success_criteria>

<references>

## Composability

- **Preflight**: Use `status` skill to verify TFY_BASE_URL and TFY_API_KEY
- **Secrets**: Use `secrets` skill to store TFY_API_KEY as a secret instead of hardcoding
- **Deploy**: After instrumenting, use `deploy` skill to deploy the traced application
- **Logs**: Use `logs` skill to debug if traces aren't appearing

## API Endpoints

See `references/api-endpoints.md` for the full Tracing API reference.

</references>

<troubleshooting>

## Error Handling

### 401 Unauthorized on Trace Export
```
Check that TFY_API_KEY is valid and not expired.
Regenerate at $TFY_BASE_URL → Settings → API Keys.
```

### No Traces Appearing in Dashboard
```
1. Verify Traceloop.init() is called BEFORE LLM library imports — this is the #1 cause.
2. Check that api_endpoint ends with /api/otel (not /api/otel/).
3. Verify X-TFY-TRACING-PROJECT-FQN header matches the project FQN exactly.
4. Set disable_batch=True temporarily to force immediate export and check for errors.
5. Check application logs for OTLP export errors.
```

### ImportError: No module named 'traceloop'
```
Run: pip install traceloop-sdk
Ensure you're installing in the correct virtual environment.
```

### Traces Missing LLM Call Details
```
Traceloop.init() must be called BEFORE importing the LLM library.
Move the init call to the very top of your entry point file.
```

### High Trace Volume in Production
```
Add sampling — see Step 7 for ParentBased(TraceIdRatioBased) configuration.
Start with 10% sampling (0.1) and adjust based on needs.
```

### Tracing Project API Returns 404
```
The tracing API endpoints may differ on your TrueFoundry version.
Create the tracing project via the TrueFoundry UI instead:
$TFY_BASE_URL → Tracing → New Project
Then use the project FQN in your Traceloop.init() configuration.
```

</troubleshooting>
