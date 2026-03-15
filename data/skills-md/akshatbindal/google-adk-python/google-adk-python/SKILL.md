---
name: google-adk-python
description: >
  Build, run, and deploy AI agents using Google's Agent Development Kit (ADK) for Python.
  Use this skill whenever the user wants to: create an ADK agent, write tools for ADK agents,
  build multi-agent pipelines (sequential, parallel, loop), manage session state or memory,
  set up callbacks, deploy to Vertex AI Agent Engine or Cloud Run, configure LLM models
  (Gemini, Claude, LiteLLM, Ollama), use MCP tools with ADK, stream agent responses,
  or integrate ADK with external APIs. Trigger on phrases like "ADK agent", "google adk",
  "agent development kit", "build an agent with ADK", "adk tools", "adk deploy", or
  any request involving multi-agent orchestration with Google's framework. Always use
  this skill when ADK Python is involved — even for single-step questions — as it contains
  critical API patterns, code structure requirements, and deployment knowledge not in
  general training data.
---

# Google ADK Python — Agent Development Kit

> Version: Python SDK (google-adk). Reference docs: https://google.github.io/adk-docs/

---

## Quick Reference Index

| Topic | Section in this file |
|---|---|
| Installation & project setup | [Setup](#setup) |
| LLM Agent (core) | [LlmAgent](#llmagent) |
| Tools (function, long-running, agent-as-tool) | [Tools](#tools) |
| Multi-agent systems | [Multi-Agent](#multi-agent-systems) |
| Session, State, Memory | [Context](#context-session-state-memory) |
| Callbacks | [Callbacks](#callbacks) |
| Running agents (Runner, CLI, web) | [Running Agents](#running-agents) |
| Models (Gemini, Claude, LiteLLM, Ollama) | [Models](#models) |
| Deployment (Agent Engine, Cloud Run) | [Deployment](#deployment) |
| Streaming (bidi) | [Streaming](#streaming) |
| MCP Integration | [MCP Tools](#mcp-tools) |
| Common patterns & gotchas | [Patterns & Gotchas](#patterns--gotchas) |

For deep reference on a specific topic, read `references/<topic>.md` (loaded on demand).

---

## Setup

**Requirements:** Python 3.10+, pip

```bash
pip install google-adk
# Optional: virtual environment (recommended)
python -m venv .venv && source .venv/bin/activate
```

**Scaffold a new agent project:**
```bash
adk create my_agent        # creates my_agent/ with agent.py, .env, __init__.py
adk run my_agent           # CLI interactive session
adk web --port 8000        # Web UI (dev only, not for production)
```

**Project structure:**
```
my_agent/
├── agent.py        # REQUIRED: defines root_agent
├── __init__.py
└── .env            # API keys / GCP project IDs
```

**API Key (Gemini via Google AI Studio):**
```bash
# my_agent/.env
GOOGLE_API_KEY="YOUR_KEY"
```

---

## LlmAgent

`LlmAgent` (aliased as `Agent`) is the primary thinking agent. Import from:
```python
from google.adk.agents import LlmAgent, Agent  # Agent is an alias
```

### Minimal Agent
```python
from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",           # REQUIRED: unique string, no spaces
    description="Short summary of what this agent does.",  # used by other agents for routing
    instruction="You are a helpful assistant. ...",
)
```

### Key Parameters

| Parameter | Type | Notes |
|---|---|---|
| `model` | `str` | Required. e.g. `"gemini-2.5-flash"`, `"gemini-2.0-flash"` |
| `name` | `str` | Required. Unique. Avoid `"user"` (reserved). |
| `instruction` | `str \| Callable` | Core behavior. Supports `{state_var}` templating. |
| `description` | `str` | Used by parent agents for routing/delegation. |
| `tools` | `list` | Python functions or `BaseTool` instances. |
| `sub_agents` | `list` | Child agents for delegation. |
| `output_key` | `str` | Auto-save final response to `session.state[output_key]`. |
| `output_schema` | `Pydantic BaseModel` | Enforce JSON output. |
| `input_schema` | `Pydantic BaseModel` | Enforce JSON input. |
| `include_contents` | `'default' \| 'none'` | Pass or suppress conversation history. |
| `generate_content_config` | `GenerateContentConfig` | Temperature, max tokens, safety. |
| `planner` | `BasePlanner` | `BuiltInPlanner` or `PlanReActPlanner`. |
| `code_executor` | `BaseCodeExecutor` | Enable code execution (e.g., `BuiltInCodeExecutor`). |

### Instruction Templating (State Variables)
```python
# Access session state in instructions with {var}
instruction = "User's name is {user_name?}. Greet them."
# {var?} = optional (won't error if missing); {var} = required
# {artifact.filename} = read artifact text content
```

### Structured Output
```python
from pydantic import BaseModel, Field

class SummaryOutput(BaseModel):
    title: str = Field(description="The document title")
    summary: str = Field(description="A 2-sentence summary")

agent = Agent(
    model="gemini-2.5-flash",
    name="summarizer",
    instruction='Respond ONLY with valid JSON matching the schema.',
    output_schema=SummaryOutput,
    output_key="summary_result",  # saves to session.state["summary_result"]
)
# NOTE: output_schema disables tool use. Use one or the other.
```

### LLM Config (Temperature, Tokens, Safety)
```python
from google.genai import types

agent = Agent(
    model="gemini-2.5-flash",
    name="careful_agent",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
        max_output_tokens=512,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ],
    ),
)
```

### Planners
```python
from google.adk.planners import BuiltInPlanner, PlanReActPlanner
from google.genai.types import ThinkingConfig

# For Gemini models with thinking support:
agent = Agent(
    model="gemini-2.5-pro-preview-03-25",
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(include_thoughts=True, thinking_budget=1024)
    ),
    ...
)

# For models without built-in thinking (forces structured plan → act format):
agent = Agent(model="gemini-2.0-flash", planner=PlanReActPlanner(), ...)
```

---

## Tools

### Function Tool (Python function → Tool)

ADK auto-wraps Python functions as `FunctionTool`. The docstring, type hints, and parameter names directly shape the schema sent to the LLM.

```python
def get_weather(city: str, unit: str = "Celsius") -> dict:
    """Returns current weather for a city.

    Args:
        city: The city name.
        unit: Temperature unit, 'Celsius' or 'Fahrenheit'. Defaults to 'Celsius'.

    Returns:
        dict with 'status' and 'report' keys.
    """
    # ... real logic here
    return {"status": "success", "report": f"It is sunny in {city}, 22°{unit[0]}"}

agent = Agent(model="gemini-2.5-flash", name="weather_agent", tools=[get_weather])
```

**Rules for tools:**
- Always return a `dict`. Non-dict returns are wrapped as `{"result": value}`.
- Use `status` key (`"success"` / `"error"`) — the LLM reads this.
- Use clear docstrings — the LLM uses them to decide when/how to call the tool.
- `*args` and `**kwargs` are ignored by the schema generator.
- `Optional[str] = None` marks a parameter as optional.

### Passing Context to Tools (`ToolContext`)
```python
from google.adk.tools import ToolContext

def save_preference(preference: str, tool_context: ToolContext) -> dict:
    """Saves a user preference to session state."""
    tool_context.state["user_preference"] = preference
    return {"status": "success", "saved": preference}
# ADK injects ToolContext automatically — don't include in schema docstring
```

### Long-Running Tool
```python
from google.adk.tools import LongRunningFunctionTool

def process_large_file(file_path: str) -> dict:
    """Processes a large file asynchronously."""
    # ... long operation
    return {"status": "success", "result": "processed"}

long_tool = LongRunningFunctionTool(func=process_large_file)
agent = Agent(model="gemini-2.5-flash", name="processor", tools=[long_tool])
```

### Agent-as-Tool (`AgentTool`)
```python
from google.adk.tools import AgentTool

specialist = Agent(name="Specialist", model="gemini-2.5-flash",
                   description="Expert in data analysis.", instruction="...")

orchestrator = Agent(
    name="Orchestrator",
    model="gemini-2.5-flash",
    tools=[AgentTool(agent=specialist)],
    instruction="Use Specialist for data tasks.",
)
# Unlike sub_agents, AgentTool is called as a function and returns the result inline.
```

---

## Multi-Agent Systems

### Agent Hierarchy & Delegation
```python
from google.adk.agents import LlmAgent

booking_agent = LlmAgent(name="Booker", model="gemini-2.5-flash",
                         description="Handles flight and hotel bookings.")
info_agent = LlmAgent(name="Info", model="gemini-2.5-flash",
                      description="Answers general questions and provides information.")

root_agent = LlmAgent(
    name="Coordinator",
    model="gemini-2.5-flash",
    instruction="Delegate booking tasks to Booker, info queries to Info.",
    sub_agents=[booking_agent, info_agent],
    # AutoFlow handles transfer_to_agent() calls automatically
)
```

**Rules:**
- Each agent instance can only have **one parent** (ValueError if added twice).
- Target agents need descriptive `description` fields for LLM routing.
- Use `root_agent.find_agent("name")` to look up agents by name.

### Sequential Agent
```python
from google.adk.agents import SequentialAgent

fetch = LlmAgent(name="Fetch", instruction="Fetch data about {topic}.", output_key="raw_data")
process = LlmAgent(name="Process", instruction="Process this data: {raw_data}.", output_key="result")

pipeline = SequentialAgent(name="Pipeline", sub_agents=[fetch, process])
# fetch runs first, saves to state['raw_data']; process reads it via {raw_data} template
```

### Parallel Agent
```python
from google.adk.agents import ParallelAgent

weather = LlmAgent(name="Weather", instruction="Get weather for {city}.", output_key="weather")
news = LlmAgent(name="News", instruction="Get news for {city}.", output_key="news")

gatherer = ParallelAgent(name="Gatherer", sub_agents=[weather, news])
# Runs concurrently. Both write to shared session.state (use distinct output_key values!)
```

### Loop Agent
```python
from google.adk.agents import LoopAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator

class StopWhenDone(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        done = ctx.session.state.get("task_complete", False)
        yield Event(author=self.name, actions=EventActions(escalate=done))

worker = LlmAgent(name="Worker", instruction="Do one step. Set state task_complete=True when done.")

loop = LoopAgent(
    name="RetryLoop",
    max_iterations=5,
    sub_agents=[worker, StopWhenDone(name="Checker")]
)
# Loop stops when Checker escalates OR max_iterations (5) reached.
```

---

## Context: Session, State, Memory

### Session & Runner Setup
```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio

APP_NAME = "my_app"
USER_ID = "user_001"
SESSION_ID = "session_001"

session_service = InMemorySessionService()
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
))
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
```

> **Note:** `InMemorySessionService` is for dev/testing only. All data is lost on restart.  
> For production use `VertexAiSessionService` or `DatabaseSessionService`.

### Reading & Writing State
```python
# In a tool:
def update_cart(item: str, tool_context: ToolContext) -> dict:
    cart = tool_context.state.get("cart", [])
    cart.append(item)
    tool_context.state["cart"] = cart
    return {"status": "success", "cart": cart}

# State key prefixes:
# "key"       → persists for session lifetime
# "user:key"  → persists across sessions for this user
# "app:key"   → persists across all users/sessions for this app
# "temp:key"  → only for current invocation turn (not persisted)
```

### Passing Initial State to Session
```python
session = await session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID,
    state={"user_name": "Alice", "language": "en"}
)
```

### Running the Agent
```python
from google.genai import types

async def call_agent(query: str):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response() and event.content:
            print("Response:", event.content.parts[0].text)
```

### Memory Service (Cross-Session)
```python
from google.adk.memory import InMemoryMemoryService  # dev only

memory_service = InMemoryMemoryService()
runner = Runner(agent=root_agent, app_name=APP_NAME,
                session_service=session_service, memory_service=memory_service)
# For production: VertexAiMemoryService
```

---

## Callbacks

Callbacks let you observe and modify agent behavior at key lifecycle points.

```python
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools import BaseTool
from typing import Optional

# --- Before model call ---
def my_before_model(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    print(f"[Callback] About to call LLM. Turn: {callback_context.invocation_id}")
    # Return an LlmResponse to SKIP the actual model call
    return None  # None = proceed normally

# --- After model call ---
def my_after_model(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Modify or replace the response
    return llm_response  # return modified or original

# --- Before tool call ---
def my_before_tool(tool: BaseTool, args: dict, callback_context: CallbackContext) -> Optional[dict]:
    print(f"[Callback] Tool '{tool.name}' called with {args}")
    # Return a dict to SHORT-CIRCUIT the tool call with that result
    return None  # None = proceed normally

agent = Agent(
    model="gemini-2.5-flash",
    name="monitored_agent",
    before_model_callback=my_before_model,
    after_model_callback=my_after_model,
    before_tool_callback=my_before_tool,
)
```

**Available callbacks:**
- `before_agent_callback` / `after_agent_callback`
- `before_model_callback` / `after_model_callback`
- `before_tool_callback` / `after_tool_callback`

---

## Running Agents

### CLI Commands
```bash
adk run my_agent              # Interactive CLI chat
adk web --port 8000           # Web UI (dev only)
adk api_server                # Start local REST API server
adk eval my_agent evals/      # Run evaluations
adk deploy agent_engine ...   # Deploy to Vertex AI Agent Engine
```

### Async Runner Pattern (Recommended)
```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="app", user_id="u1", session_id="s1"
    )
    runner = Runner(agent=root_agent, app_name="app", session_service=session_service)

    content = types.Content(role="user", parts=[types.Part(text="Hello!")])
    async for event in runner.run_async(user_id="u1", session_id="s1", new_message=content):
        if event.is_final_response():
            print(event.content.parts[0].text)

asyncio.run(main())
```

### Sync Runner (Simple Testing)
```python
from google.adk.runners import InMemoryRunner  # convenience wrapper

runner = InMemoryRunner(agent=root_agent)
session = asyncio.run(runner.session_service.create_session(
    app_name=runner.app_name, user_id="u1"
))
# then run_async as above
```

---

## Models

### Gemini (default)
```python
Agent(model="gemini-2.5-flash", ...)   # fast, efficient
Agent(model="gemini-2.5-pro", ...)     # most capable
Agent(model="gemini-2.0-flash", ...)   # balanced
```
Set `GOOGLE_API_KEY` in `.env` for Google AI Studio.  
For Vertex AI: set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`.

### Claude (Anthropic) via Vertex AI
```python
# pip install google-adk[anthropic]
from google.adk.models.lite_llm import LiteLlm

agent = Agent(
    model=LiteLlm(model="anthropic/claude-sonnet-4-6"),
    name="claude_agent",
    ...
)
# Requires ANTHROPIC_API_KEY or Vertex AI Claude setup
```

### LiteLLM (100+ models)
```python
from google.adk.models.lite_llm import LiteLlm

agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name="gpt_agent",
    ...
)
# Set relevant API keys in .env (OPENAI_API_KEY, etc.)
```

### Ollama (Local Models)
```python
from google.adk.models.lite_llm import LiteLlm

agent = Agent(
    model=LiteLlm(model="ollama/llama3"),
    name="local_agent",
    ...
)
# Run: ollama serve (default: http://localhost:11434)
```

---

## Deployment

### Vertex AI Agent Engine (Managed, Production)
```bash
# 1. Authenticate
gcloud auth login
gcloud auth application-default login

# 2. Enable APIs
# - Vertex AI API
# - Cloud Resource Manager API

# 3. Deploy
adk deploy agent_engine \
    --project=MY_PROJECT_ID \
    --region=us-central1 \
    --display_name="My Agent" \
    my_agent/
```

**After deployment**, interact via REST:
```
POST https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}:query
```
Or via Vertex AI SDK:
```python
import vertexai
agent_engine = vertexai.agent_engines.get("projects/.../reasoningEngines/RESOURCE_ID")
```

### Cloud Run
```bash
adk deploy cloud_run \
    --project=MY_PROJECT_ID \
    --region=us-central1 \
    my_agent/
```

---

## Streaming

### Bidi-Streaming (Live) Agent
```python
from google.adk.agents import LiveRequestQueue
from google.adk.runners import Runner

runner = Runner(agent=root_agent, app_name="app", session_service=session_service)
live_request_queue = LiveRequestQueue()

async def stream_agent():
    async for event in runner.run_live(
        user_id="u1", session_id="s1",
        live_request_queue=live_request_queue
    ):
        if event.content:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)

# Send messages via live_request_queue.send_content(...)
```

---

## MCP Tools

### Use an MCP Server as Tools in ADK
```python
import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

async def get_tools():
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
        )
    )
    return tools, exit_stack

async def main():
    tools, exit_stack = await get_tools()
    async with exit_stack:
        agent = Agent(
            model="gemini-2.5-flash",
            name="mcp_agent",
            tools=tools,
            instruction="Use the filesystem tools to help the user.",
        )
        # ... run agent
```

For SSE-based MCP servers:
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

tools, exit_stack = await MCPToolset.from_server(
    connection_params=SseServerParams(url="http://localhost:3000/sse")
)
```

---

## Patterns & Gotchas

### ✅ Correct `root_agent` export (required by ADK)
```python
# agent.py — root_agent must be defined at module level
from google.adk.agents import Agent

def my_tool(x: int) -> dict:
    """Does something."""
    return {"result": x * 2}

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    instruction="You are helpful.",
    tools=[my_tool],
)
```

### ✅ Sequential state passing pattern
```python
# Use output_key + {var} template for pipeline data flow
step1 = Agent(name="Step1", instruction="Extract topic from input.", output_key="topic")
step2 = Agent(name="Step2", instruction="Research {topic} in depth.", output_key="research")
step3 = Agent(name="Step3", instruction="Write a report about {research}.")
pipeline = SequentialAgent(name="Pipeline", sub_agents=[step1, step2, step3])
```

### ❌ Avoid `output_schema` + `tools` together
`output_schema` forces JSON-only mode which disables tool calls. Use one or the other.

### ❌ Avoid duplicate agent instances in sub_agents
```python
# WRONG — agent can only have one parent
shared_agent = Agent(name="Shared", ...)
parent1 = Agent(name="P1", sub_agents=[shared_agent])
parent2 = Agent(name="P2", sub_agents=[shared_agent])  # ValueError!

# RIGHT — create separate instances
```

### ✅ Async-first design
ADK is async-native. Always use `run_async` and `asyncio.run(main())` in scripts.  
For Jupyter/Colab, use `await` directly at the top level.

### ✅ Tool error handling
```python
def safe_tool(param: str) -> dict:
    """Does something safely."""
    try:
        result = do_work(param)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
# Always return {"status": "error", "error_message": "..."} on failure
# Never raise exceptions from tools — the LLM needs to read the error
```

### ✅ State key prefix reference
| Prefix | Scope |
|---|---|
| (none) | Current session |
| `user:` | All sessions for this user |
| `app:` | All sessions in this app |
| `temp:` | Current invocation only (not persisted) |

---

## Reference Files

For deeper content on specific topics, read the relevant reference file:

- `references/callbacks.md` — Callback patterns and best practices
- `references/custom-agents.md` — Building `BaseAgent` subclasses
- `references/evaluate.md` — Agent evaluation and testing
- `references/models-auth.md` — Model authentication details for all providers
- `references/artifacts.md` — Working with ADK Artifacts (file-like objects)

Load these files only when the user's task specifically requires that depth.