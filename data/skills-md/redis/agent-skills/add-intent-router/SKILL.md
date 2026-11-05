---
name: add-intent-router
description: Replace an existing agent's hand-written routing (keyword if/else chains, regex, or an LLM call that only picks a route) with a Redis Iris Intent Router through redis-iris, so a message maps to a defined intent and its dispatch target by example phrasings and a score threshold. Asks five questions (what the routes are today, a few real phrasings per route, what each route dispatches to, what happens when nothing matches, which embedding model), writes the answers to intents.yaml, provisions the Router from the terminal with `iris intent-router service create`, loads the intents with `iris intent-router intents add`, then wires `router.match()` where the agent decides today. Use when the agent routes with keywords or an extra LLM call, or the user asks for intent detection, intent routing, or semantic routing.
license: MIT
metadata:
  author: redis
  version: "1.0.0"
---

# Add Intent Router

One `match()` call in place of the code that decides where a message goes. The Router embeds the message, finds the nearest example phrasings, groups them by intent, applies a threshold, and returns the matching intents best first, each with the target you attached. No match is an empty result, not an error. The routes and their phrasings are content, not code: ask first, write `intents.yaml`, provision, load, then wire.

## 1. Discover

Read the project:

- Find where the agent decides what to do with a message: `if "refund" in text`, a regex table, a `match` statement, a classifier prompt ("Classify this message as one of ..."), or a router node or conditional edge in a graph.
- List every route it can take and what each one does: call a tool, hand off to a sub-agent, pick a prompt, or answer directly.
- Find real phrasings: test fixtures, logs, the keywords in the if/else, the examples in the classifier prompt.
- Async agent? `amatch` and `adefine` are the async twins; every other method is sync only.

Then ask the developer these five questions, nothing more. A shrug takes the default.

| Ask | If the answer is | Configure |
|---|---|---|
| What are the routes today? | A list | One intent each in `intents.yaml`. Names use letters, digits, `.`, `_` and `-` |
| Give three to five real phrasings for each route | Phrasings | `examples` for that intent. An intent with no examples never matches |
| What does each route dispatch to? | A tool, a sub-agent, a prompt | `target: {type, ref, args}`. The Router stores it and never interprets it |
| | The code already knows | No target; dispatch on the intent name |
| What should happen when nothing matches? | Fall back to the general agent (default) | Keep the existing default path for an empty result |
| | Ask a clarifying question | That branch on an empty result |
| Which embedding model? | OpenAI (default) | `--provider openai --model text-embedding-3-small --dimensions 1536` |
| | Another | `iris intent-router service models` lists what the deployment offers. The choice is fixed once the Router exists |

## 2. Get current facts from MCP

Do this before writing code. Never guess framework APIs from memory.

- Framework docs: query an available docs MCP (Context7, or the framework's own) for how the installed version routes: conditional edges, handoffs, or tool choice.
- Redis docs: if the Redis docs MCP is connected, use it for Intent Router concepts (intents, examples, thresholds).
- No MCP available: read the installed package source in the virtualenv. Say so in the report.

## 3. Configure

Write `intents.yaml` from the answers and commit it: it is the reviewable record of the routes.

```yaml
intents:
  - name: track_order
    description: Where an order is and when it arrives
    examples: ["where is my order", "track my package", "has my parcel shipped yet"]
    target: {type: tool, ref: orders.track}
  - name: refund_request
    examples: ["I want my money back", "refund this order", "return and refund"]
    target: {type: agent, ref: refunds}
    minScore: 0.4   # stricter than the Router's default for this one
```

Provision from the terminal on a self-managed suite. A `cloud` profile refuses the control-plane commands with `cloud_unsupported`: the person creates the Router in **Iris → Intent Router → New Intent Router** and its key in **Iris → Access & Identity**. Add `--local` for a local stack (it assumes `127.0.0.1:9400` and `9401`), or let the person export `IRIS_INTENT_ROUTER_SERVICE_URL`, `IRIS_INTENT_ROUTER_SERVICE_TOKEN`, `IRIS_INTENT_ROUTER_URL`, `IRIS_IDENTITY_URL` and `IRIS_IDENTITY_TOKEN`. Full reference: `iris intent-router <command> --help` (for example `iris intent-router service create --help`).

```
iris --json --no-input intent-router service create --name support --provider openai --model text-embedding-3-small --dimensions 1536 --role read --dry-run
iris --json --no-input intent-router service create --name support --provider openai --model text-embedding-3-small --dimensions 1536 --role read --wait --write-env .env
iris --json --no-input intent-router service check <routerId from the result> --env-file .env
```

### Run the CLI as an agent

1. Always put `--json --no-input` before the product name. You get one JSON value on stdout, errors as one JSON value on stderr, and no prompts.
2. Dry-run first: it sends nothing and lists every missing setting. If anything is missing, stop and hand off (step 4) before any write.
3. Always deliver keys with `--write-env PATH` (or `--write PATH` on `service key`). Never run `create` or `key` with `--json` and no file: that prints the key into your transcript.
4. On `credential_required`, stop. Tell the person which variable to set (`details.env`) and link `details.obtain`. Never ask for a secret in chat, pass one on the command line, or echo, `cat` or `grep` an env file.
5. On `resource_exists`, ask whether to `--reuse` or pick another name. Never delete to retry. If `create` fails with `details.created: true`, run the command in `details.command`.

`--write-env .env` writes `IRIS_INTENT_ROUTER_URL`, `IRIS_INTENT_ROUTER_ID` and `IRIS_INTENT_ROUTER_API_KEY`. Add the same three names to `.env.example` with empty values. Never commit `.env`.

Two keys, never one:

| Key | Role | Mint |
|---|---|---|
| Agent (in `.env`) | `read`: match and list | `--role read` on `create` |
| Authoring, for loading `intents.yaml` | `write` | `iris intent-router service key ROUTER_ID --role write --write .env.authoring`; load it only in the shell that runs `intents add`, never in the agent's `.env` |

Load the intents with the authoring key. `intents add` is one atomic batch: an existing name is replaced, and nothing is written if any intent is invalid:

```
iris --json --no-input intent-router intents add --file intents.yaml
iris --json --no-input intent-router intents list --all
```

Re-run `intents add` after every change to `intents.yaml`.

## 4. Wire the decision point

Create once at startup:

```python
from redis_iris import IntentRouter

router = IntentRouter.from_env()
```

Replace the decision with one call:

```python
found = router.match(message)  # await router.amatch(...)
if found.best:
    route = found.best.name  # "track_order"
    target = found.best.target  # what intents.yaml attached, or None
    # dispatch exactly where the old if/else or classifier branch did
else:
    ...  # question 4: the existing fallback path
```

`found.best.score` is the score, higher is closer. `match(message, limit=3)` returns the next candidates, and `min_score=` overrides every threshold for one call. A `limit` above the server's cap is rejected, not clamped.

Where it goes (confirm names in step 2):

| Framework | Replace |
|---|---|
| LangGraph | the router node or the function behind the conditional edge: return the next node from `found.best` |
| OpenAI Agents SDK | the triage agent or handoff choice, when it only picks a route |
| Google ADK | the routing agent or `before_agent_callback` choice |
| CrewAI | the manager's delegation choice, when it is a fixed set of routes |
| Plain loop | the if/else or `match` statement |

Remove what it replaced: the keyword lists, the regex table, the classifier prompt and its model call. Keep the dispatch code; only the choice moves.

The SDK raises on a missing setting or an outage. Ask whether a Router failure may fail the turn; most agents catch it and take the question 4 fallback.

## 5. Verify

1. `iris intent-router service check ROUTER_ID --env-file .env` passes every hop: token, Router `READY`, Identity Service, a key granting the Router, one data read.
2. `iris intent-router intents list --all` shows every intent from `intents.yaml` with its example count.
3. `iris intent-router match "<a phrasing that is not in the examples>" --limit 3` returns the right intent first.
4. `iris intent-router match "<something no route covers>"` returns an empty list.
5. Run the agent once with each, and show it took the matched route and the fallback.
6. Unset `IRIS_INTENT_ROUTER_API_KEY` and confirm `ConfigurationError` names it.

Wrong intent first: add phrasings to the right intent or raise its `minScore`, re-run `intents add`. Everything empty: lower the Router's or the intent's threshold (`intents update NAME --min-score`). With the `noop` embedding provider, matching is lexical overlap, not semantic.

## 6. Report

List the five answers, the intents and example counts in `intents.yaml`, the embedding model, keys minted and their roles, where `match()` went and what it replaced, the fallback path, verification output, and anything you could not confirm over MCP.
