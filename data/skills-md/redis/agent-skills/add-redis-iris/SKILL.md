---
name: add-redis-iris
description: Add Redis Iris to an existing AI agent in any framework (LangGraph, LangChain, OpenAI Agents SDK, Google ADK, Pydantic AI, CrewAI, or a plain loop). Use when the user asks to add Iris, Redis Agent Memory, Agent Playbooks, Context Gateway, Intent Router, or Lens to their agent, or asks which Iris product their agent needs. Detects the framework and routes to the product skill.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Add Redis Iris

Inspect, install, route. Do not rewrite the agent.

## 1. Find the agent

Locate:

- **The turn**: where the model is called (`invoke`, `Runner.run`, `generate_content`, `agent.run`, `kickoff`, `chat.completions.create`, `messages.create`).
- **Tool registration**: where tools are defined and handed to the model.
- **User and session ids**: where the request's user id and thread or session id live.
- **More than one loop** (a hand-written loop and a framework, or two frameworks)? Create the product objects once in a module with no framework imports, wire each loop at its own seam, and convert one loop at a time. Do not pick the loop for the user.

## 2. Detect the framework

Search imports:

| Import | Framework |
|---|---|
| `langgraph`, `langchain`, `langchain_core` | LangGraph / LangChain |
| `agents` (package `openai-agents`) | OpenAI Agents SDK |
| `google.adk` | Google ADK |
| `pydantic_ai` | Pydantic AI |
| `crewai` | CrewAI |
| only `openai`, `anthropic`, or another model client | Plain loop |

Note the version from the lockfile. Product skills look up that version's API over MCP.

## 3. Find what it lacks

| Symptom in the code | Product | Skill |
|---|---|---|
| No long-term memory, `InMemoryStore`, checkpointer only, memory in a dict or local DB | Agent Memory | `add-agent-memory` |
| Already on Redis Agent Memory through its own REST or MCP client, hand-written adapters, or model-facing memory tools | Agent Memory | `add-agent-memory`, "Already on Redis Agent Memory" |
| Policy or procedures hardcoded in the prompt, tool usage guidance in the prompt, or a vector store over policy docs | Agent Playbooks | `add-agent-playbooks` |
| A semantic response cache: model answers stored and re-served to later users, curated by hand | Agent Playbooks | `add-agent-playbooks`, "Replacing a response cache" |
| Several MCP servers configured one by one in the agent, each with its own secret, or too many tool schemas in the prompt | Context Gateway | `add-context-gateway` |
| A keyword if/else router, or an LLM call just to pick a route | Intent Router | `add-intent-router` |
| No per-turn tracing: no way to see which LLM calls, tools and retrievals one answer used, or what it cost | Lens | `add-lens` |

If the user named a product, use that. If unclear, ask once, listing what you found.

Lens goes next to any product, or on its own: it traces the turn, and every Iris product traces itself inside it. Offer it alongside whatever else you add.

## 4. Install

- `uv.lock` or `[tool.uv]` present: `uv add redis-iris`.
- Poetry: `poetry add redis-iris`.
- Otherwise add `redis-iris` to the project's requirements file.

If resolution fails on pre-releases, retry with `uv add --prerelease=allow redis-iris`. Confirm: `uv run python -c "import redis_iris; print(redis_iris.__version__)"`.

## 5. Route

Follow each chosen product skill. More than one product: each skill adds its own calls. Optionally build them from one config with `Iris.from_env()` (`iris.agent_memory()`, `iris.agent_playbooks()`, `iris.context_gateway()`, `iris.intent_router()`).

Ask once whether the services run on Redis Cloud or a self-managed suite, then write the project's `iris.toml` profile. Only the `iris` CLI reads `iris.toml`; the app reads env vars. It holds URLs only: a token in TOML makes the CLI exit 2. Select the profile with `IRIS_CONFIG=./iris.toml` and `IRIS_PROFILE=cloud` or `IRIS_PROFILE=suite`.

Redis Cloud. The person fills `.env` from the console: `IRIS_<PRODUCT>_URL`, its ID and `_API_KEY` per product.

```toml
[profiles.cloud]
kind = "cloud"
console_url = "https://cloud.redis.io"

[profiles.cloud.agent_memory]
url = "https://gcp-us-east4.memory.redis.io"  # the data-plane URL from the console
```

Self-managed suite. The operator's tokens go in `.env.admin`, never the app's `.env`; `service create --write-env .env` writes the app's `.env`.

```toml
[profiles.suite]
kind = "self-managed"

[profiles.suite.agent_memory]
service_url = "https://memory-admin.example.com"  # control plane: the CLI calls it for service create and check
url = "https://memory.example.com"  # data plane: what the agent calls
identity_url = "https://memory-identity.example.com"  # Identity Service that mints the agent's keys
```

Add one table per product the app uses: `agent_memory`, `agent_playbooks`, `context_gateway`, `intent_router`. `[profiles.suite.context_gateway]` has no `url`: `service create --write-env` writes the Gateway's endpoint. A suite with one shared Identity Service sets `[profiles.suite.identity]` `url` once instead of each `identity_url`. `IRIS_<PRODUCT>_SERVICE_URL`, `IRIS_<PRODUCT>_URL` and `IRIS_<PRODUCT>_IDENTITY_URL` override the profile.

## Rules

- Keep the user's framework, graph, and prompts. Smallest diff.
- Never guess framework APIs from memory. Look them up over MCP (see each product skill).
- Only use APIs in `redis_iris`. `redis_iris.integrations.langgraph.attach` (extra `redis-iris[langgraph]`) and `redis_iris.integrations.adk.attach` (no extra) exist; there is no `IrisTool`, `iris.tools()`, or `iris.turn()`.
- The SDK raises on a missing setting or an outage. Ask whether a product failure may fail the turn; most production agents catch it and continue with an empty block.
- Never commit secrets.
