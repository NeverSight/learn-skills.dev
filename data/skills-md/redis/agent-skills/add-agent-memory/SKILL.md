---
name: add-agent-memory
description: Wire Redis Agent Memory into an existing agent with redis-iris so it remembers users across sessions. Asks five questions (what to remember, what to share, what never to keep, how long to keep it, whether users can be forgotten), writes the answers to service.yaml, provisions the service from the terminal with `iris agent-memory service create`, then wires recall and write-back into the agent's turn in any framework. Use when the agent forgets users, uses InMemoryStore or a checkpointer only, keeps memory in a dict or local DB, or the user asks for long-term memory, recall, or right-to-erasure.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Add Agent Memory

Before the model: recall what is known about the user. After the turn: write the exchange back. The service extracts long-term memories from sessions. What it remembers, shares, excludes and retains is a service setting, not an SDK argument: ask first, provision, then wire.

## 1. Discover

Read the project:

- Find the turn (where the model is called) and the user id and session or thread id in scope there.
- Identify the framework from imports.
- Find existing memory code (`BaseStore`, `InMemoryStore`, custom dict or DB). You will replace its reads and writes, not the graph.
- Already on Redis Agent Memory through its own client? Inventory before changing anything: adapters over the generated `redis_agent_memory` client, an MCP client exposing memory tools to the model, a `namespace` string written on every record, and any second runtime or framework plugin writing the same store. See "Already on Redis Agent Memory" in step 4.
- Async agent? Use the `a`-prefixed methods.

Then ask the developer these five questions, nothing more. A shrug takes the default.

| Ask | If the answer is | Configure |
|---|---|---|
| What should the agent remember about a user across sessions? | Free facts and preferences (default) | Nothing: built-in `semantic` and `episodic` types cover it |
| | Structured business data: trip requirements, order constraints, account preferences | One `memory_types` entry with named `fields` and an extraction `prompt` |
| Is there knowledge every conversation should see? | Incidents, temporary policies, team notes | `memory.shared_namespace("<name>")`; an ops owner writes with `remember(..., namespace_id=...)`; the agent reads with `recall(shared=[...])` |
| | No (default) | Skip the namespace |
| What must never be kept? | Passwords, tokens, card numbers, confirmation codes, health data | `exclusions.prompt` naming each one. Guidance, not a guarantee: session content still reaches the model provider, and direct `remember()` writes skip it |
| How long should memory live? | Session TTL, long-term TTL (defaults 30d / 365d) | `short_term_ttl`, `long_term_ttl` |
| Do users need to be forgotten on request? | Yes | `memory.forget(owner)` on the erasure path |

Long sessions (support threads, multi-hour chats): keep `summarization` enabled with `after_messages: 20`, `keep_recent: 10`.

## 2. Get current facts from MCP

Do this before writing code. Never guess framework APIs from memory.

- Framework docs: query an available docs MCP (Context7, or the framework's own docs MCP such as LangChain's) for the installed version's dynamic system prompt or instructions, before/after model callbacks, and run context (how a tool or callback reads the user id).
- Redis docs: if the Redis docs MCP is connected, use `search` / `fetch` / `ask` for Agent Memory concepts (sessions, long-term memory, namespaces, custom memory types, exclusions).
- No MCP available: read the installed package source in the virtualenv. Say so in the report.

## 3. Configure

Write `service.yaml` from the answers. Commit it: it is the reviewable record of the service.

```yaml
name: support-memory
# database: "1"                # the default on-prem; the registered database id the store lives in
short_term_ttl: 30d
long_term_ttl: 365d
# extraction_cadence: 60s      # the default (60s to 600s); raise it to spend less on extraction
summarization: {enabled: true, after_messages: 20, keep_recent: 10}
exclusions: {prompt: "Do not keep passwords, access tokens, recovery codes, payment card information, or booking confirmation codes in long-term memory."}
memory_types:                  # only when question 1 named structured data
  - name: trip_preference
    description: Structured requirements for a planned trip
    prompt: Extract trip requirements only when the user states a destination or travel plan.
    enabled: true
    fields: {destinations: "list[str]", travel_period: str, dietary_requirements: "list[str]"}
```

Provision from the terminal:

```
iris --json --no-input agent-memory service create --from service.yaml --dry-run
iris --json --no-input agent-memory service create --from service.yaml --write-env .env
iris --json --no-input agent-memory service check <storeId from the result> --env-file .env
```

| Stack | Before running |
|---|---|
| Local on-prem (Agent Memory service `http://127.0.0.1:9100`, Agent Memory URL `http://127.0.0.1:9000`) | Add `--local` |
| Self-managed suite | The person exports `IRIS_AGENT_MEMORY_SERVICE_TOKEN`, `IRIS_IDENTITY_TOKEN` and, on a multi-tenant Identity Service, `IRIS_IDENTITY_TENANT`; URLs come from `IRIS_AGENT_MEMORY_SERVICE_URL`, `IRIS_AGENT_MEMORY_URL` and `IRIS_IDENTITY_URL`, or a profile. See "Identity tokens" below |
| Redis Cloud | Service commands return `cloud_unsupported`; see the console note below |

**Identity tokens.** Each product chart can run its own Identity Service. Then set the product's own `IRIS_AGENT_MEMORY_IDENTITY_TOKEN` (and `IRIS_AGENT_MEMORY_IDENTITY_URL`, or the profile's `identity_url`), and leave `IRIS_IDENTITY_URL` unset: it overrides every product's `identity_url` in the profile. On a suite with one shared Identity Service, `IRIS_IDENTITY_TOKEN` and `IRIS_IDENTITY_URL` cover every product. The CLI takes the token from `--identity-token`, then `IRIS_AGENT_MEMORY_IDENTITY_TOKEN`, then `IRIS_IDENTITY_TOKEN`, then the product's service token, which only works when the two are the same secret. The dry run lists that fallback under `warnings`.

Start the project's `iris.toml`. Only the `iris` CLI reads `iris.toml`; the app reads env vars. It holds URLs only: a token in TOML makes the CLI exit 2. Select the profile with `IRIS_CONFIG=./iris.toml` and `IRIS_PROFILE=cloud` or `IRIS_PROFILE=suite`.

Redis Cloud. The person fills `.env` from the console: `IRIS_AGENT_MEMORY_URL`, `IRIS_AGENT_MEMORY_STORE_ID` and `IRIS_AGENT_MEMORY_API_KEY`.

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

A suite with one shared Identity Service sets `[profiles.suite.identity]` `url` once instead of each `identity_url`. `IRIS_<PRODUCT>_SERVICE_URL`, `IRIS_<PRODUCT>_URL` and `IRIS_<PRODUCT>_IDENTITY_URL` override the profile.

### Run the CLI as an agent

Every `iris` call you make follows the same loop:

1. Always put `--json --no-input` before the product name. You get one JSON value on stdout, errors as one JSON value on stderr, and no prompts.
2. Dry-run first: `service create ... --dry-run` sends nothing and lists in `missing` every credential or URL the real run needs. If `missing` is not empty, stop and hand off (step 4) before any write. Report anything in `warnings` (a grant with no tenant, or the service token standing in for the Identity Service token) to the person before the real run.
3. Always deliver keys with `--write-env PATH` (or `--write PATH` on `key`). Never run `create` or `key` with `--json` and no file: that prints the key on stdout and into your transcript.
4. On `credential_required`, stop. Tell the person which variable to set (`details.env`), for which product and profile, and link `details.obtain`. On `unauthenticated` or `forbidden`, say which value was refused (`details.source`). Never ask for the secret in chat, pass it on the command line, or echo, `cat` or `grep` an env file.
5. After provisioning, run `service check ID --env-file .env` (the file `create` wrote; the key stays out of your shell) and report each step. On failure, report the failing hop (`details.hop`, `details.step`, `details.cause`), not a guess.
6. On `resource_exists`, ask the person whether to `--reuse` `details.id` or pick another name. Never delete to retry. If `create` fails with `details.created: true`, the resource exists but has no key yet: re-run with `--reuse --write-env`.

Every error is one JSON value on stderr with `error.code`; credential errors also carry `details.env` and `details.obtain`, never the value. Stop on the first failure and relay it:

| `error.code` | Who acts | Action |
|---|---|---|
| `credential_required` | person | Set the variable in `details.env` in the agent's shell. See "Identity tokens" above. |
| `unauthenticated` | person | The token from `details.source` was refused: it expired or belongs to another deployment. Issue a new one. |
| `forbidden` | person | The token is valid but lacks the role or tenant. Use a token with the right role for that product. |
| `configuration_error` | person or agent | A URL is missing, such as `url`. Add it to the profile. |
| `invalid_request` | agent | HTTP 400. Fix the request the message names. |
| `resource_exists` | person | Decide: re-run with `--reuse` to adopt `details.id`, or choose another name. |
| `unavailable` | person | The hop is unreachable. Check the URL, the ingress and the service's pods. |
| `check_failed` | person | `details.hop` and `details.cause` name the broken hop. Fix it and re-run the check. |
| `cloud_unsupported` | person | The profile is `kind = "cloud"`. Follow `details.steps` in the console. |
| `input_error`, `usage_error` | agent | Fix the command. A destructive command under `--no-input` needs `--yes` from a person. |

`--write-env .env` writes `IRIS_AGENT_MEMORY_URL`, `IRIS_AGENT_MEMORY_STORE_ID`, `IRIS_AGENT_MEMORY_API_KEY`. Add the same three names to `.env.example` with empty values. Never commit `.env`. Later: `iris agent-memory service list | show STORE_ID | env STORE_ID [--write PATH]` (add `--local` for a local stack).

No access to the Agent Memory service, or on Redis Cloud? The person creates the service in the Redis Cloud console: **Iris → Agent Memory → New service**. They enter a Service name and pick a Database; **Customize settings** sets TTLs, extraction cadence, summarization, custom memory types and exclusions. Then they copy the **Store ID** and a URL from the **URL List** on the store's **Configuration** tab, and create an API key with access to the store in **Iris → Access & Identity**. The API key is shown once.

| Console | Env var | Required |
|---|---|---|
| URL List | `IRIS_AGENT_MEMORY_URL` | yes |
| Store ID | `IRIS_AGENT_MEMORY_STORE_ID` | yes |
| API key | `IRIS_AGENT_MEMORY_API_KEY` | yes |
| | `IRIS_AGENT_MEMORY_TIMEOUT` | no, seconds, default `30` |

Create once at startup:

```python
from redis_iris import AgentMemory

memory = AgentMemory.from_env(assistant_id="<agent-name>")
floor = memory.shared_namespace("<team-namespace>")  # question 2: memories every user may read
```

## 4. Wire the two seams

Before the model (context in):

```python
known = memory.recall(question, owner=user_id, shared=[floor])  # await memory.arecall(...)
system_prompt = f"{system_prompt}\n\n{known.as_prompt()}"
```

After the turn (write-back):

```python
convo = memory.conversation(owner=user_id, session_id=thread_id)  # session_id optional
convo.user(question)  # await convo.auser(...)
convo.assistant(answer)  # await convo.aassistant(...)
```

Explicit facts: `memory.remember(text, owner=user_id, topics=[...])`. Erasure (question 5): `memory.forget(user_id)` returns `Forgotten(owner, sessions, memories)`. Anything else: `memory.client`.

Every row is the same two calls, with nothing framework-specific: `hooks = memory.hooks(shared=[...])`, then `hooks.before(message, owner=user_id)` into the system prompt and `hooks.after(message, answer, owner=user_id, session=thread_id)` after the reply (`abefore` / `aafter` in async code). Where they go (confirm names in step 2):

| Framework | Before model | After turn | Tool (optional `remember`) |
|---|---|---|---|
| LangGraph (StateGraph) | `attach(memory, graph)` from `redis_iris.integrations.langgraph` (extra `redis-iris[langgraph]`) does both seams before `compile()`; owner and thread from `configurable.user_id` / `thread_id`. Hand-wired alternative: a node before the model | included in `attach`; else a node after the model | `@tool` / `StructuredTool` |
| OpenAI Agents SDK | dynamic `instructions` callable | after `Runner.run` returns, or run hooks | `@function_tool` / `FunctionTool` |
| Google ADK (`LlmAgent`) | `attach(memory, agent)` from `redis_iris.integrations.adk` (no extra) adds both model callbacks ahead of the agent's own; owner and session from the invocation's `user_id` and `session.id` | included in `attach`: recorded once, on the final reply | `FunctionTool` |
| Pydantic AI | dynamic `@agent.system_prompt`, user id in deps | after `agent.run` returns | `Tool` / `@agent.tool` |
| CrewAI | inject into the task or agent inputs before `kickoff` | after `kickoff` returns, or `task_callback` | `@tool` / `BaseTool` |
| Plain loop | before the model call | after the model call | function definition in the request |

Remove the replaced memory code. Keep the checkpointer if the graph uses it for thread state.

### Already on Redis Agent Memory

The store stays; the client changes. Keep the owner id and the session id derivation the project already uses, so existing sessions continue.

- **Prior turns as messages.** If the agent seeds the model with the session so far, `memory.conversation(owner=user_id, session_id=thread_id).transcript()` returns `turns` as `(role, text)` and the `summary`; put the summary first as a system message. If it only needs the facts, `recall` is enough.
- **Two writers become one.** Model-facing memory tools (`create`, `search`, `edit`, `delete`) and the service's own extraction both write long-term memory. Default to dropping the tools: recall before, record after, the service extracts. Keep a `remember` tool only if an evaluation shows explicit writes matter.
- **A `namespace` string on records is the deprecated field.** Reads are scoped by owner; sharing uses namespaces created with `shared_namespace`. Check that `recall(owner=...)` returns the existing records before deleting the constant, and never run the old and new paths in one environment: a client that filters on the string will not see what the new path writes.
- **Values, not strings, when the agent needs them.** `hooks()` renders prompt blocks. An agent that validates a cached answer against memory, or counts what was recalled, calls `recall()` and `transcript()` directly.
- **Failure policy.** The SDK raises; if the agent must answer during a memory outage, catch per call and continue with an empty block.

## 5. Verify

1. `iris agent-memory service show $IRIS_AGENT_MEMORY_STORE_ID` echoes the TTLs, summarization, exclusions and memory types from `service.yaml`.
2. Seed one memory: `memory.remember("Prefers email.", owner="<test-user>")`.
3. Run the agent once as `<test-user>`.
4. Show `memory.recall("contact", owner="<test-user>").as_prompt()` lists the memory, and that it reached the model's prompt.
5. Show the session: `memory.conversation(owner="<test-user>", session_id=...).transcript().turns` is non-empty.
6. Question 5 was yes: `memory.forget("<test-user>")` reports the seeded counts, and a second `recall` returns nothing.
7. Unset a variable and confirm `ConfigurationError` names it (raised on first call).
8. Converted from an existing client: `memory.recall(<a known topic>, owner=<an existing user>)` returns memories written before the change.

Extracted memories appear after the extraction window; seeded memories are immediate.

## 6. Report

List the five answers and the `service.yaml` each produced, files changed, env vars added, where each seam went, verification output, and anything you could not confirm over MCP.
