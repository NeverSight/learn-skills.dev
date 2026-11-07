---
name: llm-cost-reduction
description: Find and cut LLM/AI API spend in applications and agents without breaking quality. Measures cost per feature and per request first, then right-sizes models per task, routes simple requests to cheap models and hard ones to frontier models, trims bloated prompts and RAG context, turns on provider prompt caching with stable prefixes, adds exact and semantic response caching, moves offline work to Batch APIs, caps max_tokens and agent loops, reuses embeddings, and sets per-team and per-feature budgets and cost attribution. Use when someone says "our OpenAI/Anthropic bill spiked", "surprise LLM bill", "reduce token costs", "LLM cost optimization", "everything goes to GPT/Claude Opus", "which feature is burning tokens", "prompt caching isn't hitting", "cache LLM responses", "the agent looped and cost $X", "set a budget per team", "route cheap queries to a smaller model", "model routing by complexity", or "track AI spend by customer". Gives Python/TypeScript fixes, a grep audit, and gateway controls with Bifrost.
license: MIT
metadata:
  author: build-with-ai-hq
  version: "1.0.0"
---

# LLM Cost Reduction

Cut what an AI application spends on model calls while holding output quality steady. LLM cost is `requests x (input tokens x input price + output tokens x output price)`. Every fix below attacks one factor: fewer requests (caching, dedup, loop caps), fewer tokens (trimming, output limits), or a lower price per token (smaller models, prompt-cache discounts, batch discounts).

Work in this order: **measure, then fix the biggest line item, then verify quality did not drop.** Optimizing without per-feature numbers usually trims the wrong thing.

## When to use

- The provider invoice jumped and nobody can say which feature, team, or customer caused it.
- Every request, including classification, extraction and short chat turns, goes to a frontier model.
- The same or near-identical prompts are sent repeatedly (FAQ bots, retries, dashboards, evals).
- System prompts, tool schemas, few-shot examples or RAG chunks run to thousands of tokens per call.
- `max_tokens` is unset, agents run without an iteration or spend cap, or retries stack up.
- Provider prompt caching is available but `cached_tokens` / `cache_read_input_tokens` is zero.
- Nightly or backfill jobs call the synchronous API one item at a time.
- Embeddings are recomputed for unchanged documents on every ingest.

## Quick diagnosis (run first)

Run from the repo root. Each hit is a lead; read the surrounding code.

```bash
g() { grep -rnE "$@" --exclude-dir={node_modules,.git,dist,build,.venv,venv,__pycache__} . ; }
# 1. Every LLM call site and which models they use
g "chat\.completions\.create|responses\.create|messages\.create|generateContent|generate_content|ChatOpenAI|ChatAnthropic|streamText|generateText|embeddings\.create"
g -o "\"(gpt-[0-9a-z.-]+|o[1-9][a-z0-9-]*|claude-[a-z0-9.-]+|gemini-[0-9a-z.-]+)\"" | sort | uniq -c | sort -rn
# 2. Output limits: calls with no max_tokens / max_output_tokens / maxTokens nearby
g "max_tokens|max_completion_tokens|max_output_tokens|maxTokens|maxOutputTokens" | wc -l
# 3. Agent / tool loops without an obvious cap
g "while True|while \(true\)|for \(;;\)|max_iterations|maxSteps|max_turns|recursion_limit|stopWhen"
# 4. Retry wrappers (retry storms multiply spend)
g "max_retries|maxRetries|tenacity|backoff|p-retry|retry\("
# 5. Is usage being recorded at all?
g "usage\.(prompt_tokens|completion_tokens|input_tokens|output_tokens)|usageMetadata|cached_tokens|cache_read_input_tokens"
# 6. Prompt-cache killers: timestamps, UUIDs, or per-user data at the top of prompts
g "(system|instructions).{0,80}(datetime\.now|Date\.now|new Date\(|uuid|time\.time)"
# 7. Embeddings recomputed on every run
g "embed(_documents|Documents|dings\.create)"
```

Then get numbers. If the app already logs usage, group it; if not, add the instrumentation in step 1 below and collect a day of traffic. You need, per feature: requests/day, average input tokens, average output tokens, model, and cost. Rank features by cost. The top one or two usually account for most of the bill.

## Fixes, ordered by typical impact

### 1. Attribute every call to a feature (do this first)

Wrap the client once so every call records feature, model and usage. Without this you cannot prove any later fix worked.

```python
import time, json, logging
from openai import OpenAI

client = OpenAI()
log = logging.getLogger("llm_usage")

def llm_call(feature: str, **kwargs):
    t0 = time.monotonic()
    resp = client.chat.completions.create(**kwargs)
    u = resp.usage
    log.info(json.dumps({
        "feature": feature, "model": resp.model,
        "input_tokens": u.prompt_tokens, "output_tokens": u.completion_tokens,
        "cached_tokens": getattr(u.prompt_tokens_details, "cached_tokens", 0) if u.prompt_tokens_details else 0,
        "latency_ms": int((time.monotonic() - t0) * 1000),
    }))
    return resp
```

```typescript
import OpenAI from "openai";
const client = new OpenAI();

export async function llmCall(feature: string, params: OpenAI.Chat.ChatCompletionCreateParamsNonStreaming) {
  const t0 = Date.now();
  const resp = await client.chat.completions.create(params);
  const u = resp.usage;
  console.log(JSON.stringify({
    feature, model: resp.model,
    input_tokens: u?.prompt_tokens, output_tokens: u?.completion_tokens,
    cached_tokens: u?.prompt_tokens_details?.cached_tokens ?? 0,
    latency_ms: Date.now() - t0,
  }));
  return resp;
}
```

Multiply tokens by the provider's current price sheet to get dollars, or let a gateway compute cost for you (see "Do it at the gateway" below). For per-team/per-customer attribution and budgets, read [references/budgets-and-attribution.md](references/budgets-and-attribution.md).

### 2. Right-size the model per task

Most production traffic does not need the most capable model. Classify call sites:

| Task shape | Typical right size |
|---|---|
| Classification, routing, extraction, short rewrites, yes/no checks | Small/fast model |
| Summaries, standard RAG answers, routine code edits | Mid-tier model |
| Multi-step reasoning, hard debugging, design, long synthesis | Frontier model |

How to do it safely:
1. Build a small eval set (50-200 real inputs per feature with expected outputs or a rubric).
2. Run the current model and the cheaper candidate on it. Compare quality, not vibes.
3. Switch call sites that pass. Keep the frontier model only where the eval shows it matters.

Use whatever models the project already uses or has access to; the model IDs in this skill are examples only.

When one endpoint receives both easy and hard requests (a chat box, a coding assistant), a static per-call-site choice is not enough. Route **per request** by complexity. Bifrost's Complexity Router does this at the gateway with no app changes; see section "Do it at the gateway" and [references/complexity-routing.md](references/complexity-routing.md).

### 3. Cap output and loops

Output tokens usually cost several times more than input tokens.

- Always set an output limit sized to the task (`max_tokens` / `max_completion_tokens` / `max_output_tokens` / `maxTokens`). A classifier needs single digits; a summary needs a few hundred.
- Ask for the format you need: "Answer in at most 3 bullets", JSON schema / structured outputs instead of prose plus parsing.
- For reasoning models, set the reasoning effort or thinking budget explicitly; the default can dominate the bill.
- Cap agent loops on three axes: iterations, total tokens, and wall time. Stop and return a partial result when any cap is hit.

```python
MAX_STEPS, MAX_TOKENS_PER_RUN = 12, 200_000
used = 0
for step in range(MAX_STEPS):
    resp = llm_call("agent", model=MODEL, messages=msgs, tools=tools, max_tokens=1024)
    used += resp.usage.total_tokens
    if used > MAX_TOKENS_PER_RUN:
        break  # return partial result + flag for review
    if not resp.choices[0].message.tool_calls:
        break
    msgs += run_tools(resp)  # append tool results
```

```typescript
const MAX_STEPS = 12, MAX_TOKENS_PER_RUN = 200_000;
let used = 0;
for (let step = 0; step < MAX_STEPS; step++) {
  const resp = await llmCall("agent", { model: MODEL, messages: msgs, tools, max_tokens: 1024 });
  used += resp.usage?.total_tokens ?? 0;
  if (used > MAX_TOKENS_PER_RUN || !resp.choices[0].message.tool_calls) break;
  msgs.push(...(await runTools(resp)));
}
```

- Cap retries (2-3 with exponential backoff and jitter). Never retry 400-class errors; they fail identically and still cost time and sometimes tokens.
- Detect repeated identical tool calls in agent loops (same tool + same arguments twice in a row) and stop.

### 4. Trim prompts and context

Input tokens are paid on every call, including every turn of a conversation.

- **System prompt:** remove duplicated instructions, long examples the model no longer needs, and boilerplate. Measure with a tokenizer (`tiktoken`, the provider's count-tokens endpoint) before and after.
- **RAG:** retrieve fewer, better chunks. Lower `top_k`, add a reranker, deduplicate overlapping chunks, and strip markup/boilerplate before indexing.
- **Conversation history:** keep the last N turns verbatim and replace older turns with a running summary produced by a small model.
- **Tool definitions:** send only the tools relevant to the current step. Twenty tool schemas can cost thousands of tokens per call.
- **Tool results:** truncate or summarize large tool outputs (logs, HTML, JSON dumps) before appending them to the conversation.
- **Images and files:** downscale images to the resolution the task needs; send extracted text instead of whole PDFs where possible.

### 5. Use provider prompt caching

Major providers discount repeated prompt prefixes heavily (cached input is billed at a fraction of the normal input price; check current pricing). Some cache automatically above a minimum prefix length; others need explicit cache breakpoints. Either way the cache only hits when the **prefix is byte-identical**:

- Put static content first (system prompt, tool definitions, few-shot examples, long reference docs), variable content last (user message, retrieved chunks, timestamps).
- Do not inject the current time, request IDs, or user names into the system prompt. Move them into the final user message.
- Keep tool order and JSON serialization deterministic (sorted keys).
- Keep a conversation on the same provider, model and key; switching provider or key lands on a cold cache.
- Verify with usage fields: OpenAI `usage.prompt_tokens_details.cached_tokens`, Anthropic `usage.cache_read_input_tokens` / `cache_creation_input_tokens`.

Provider specifics, code, and response-level caching: [references/caching.md](references/caching.md).

### 6. Cache whole responses

When the same question arrives repeatedly, do not call the model at all.

- **Exact cache:** hash `(model, normalized messages, params)` and store the response with a TTL. Safe and cheap.
- **Semantic cache:** embed the request and serve a stored answer when similarity is above a threshold. Higher hit rate on paraphrases (FAQ, support, search), but tune the threshold and scope it carefully so users never receive another user's personalized answer.
- Do not cache responses that depend on private per-user data unless the cache key includes the user, and do not cache tool-call responses blindly.

### 7. Batch offline work

Evals, backfills, nightly enrichment, bulk classification and embeddings rarely need a synchronous answer. Provider Batch APIs (OpenAI, Anthropic, Google, Bedrock) process jobs asynchronously at a substantial discount, typically within 24 hours. Group items into batch files, submit, poll, and reconcile by `custom_id`. Bifrost exposes Files and Batch APIs across providers: https://docs.getbifrost.ai/integrations/openai-sdk/files-and-batch.md

### 8. Reuse embeddings

- Key stored embeddings by `sha256(model + normalized text)` and skip re-embedding unchanged content.
- Re-embed only changed chunks on ingest; do not rebuild the index on every deploy.
- Batch embedding requests (many inputs per call) instead of one call per chunk.
- Use the smallest embedding dimension that holds retrieval quality (some models support shortened dimensions).

### 9. Streaming

Streaming does not change the price per token. It helps cost in one way: when the user navigates away or presses stop, abort the request (`AbortController` in TS, close the stream in Python) so generation stops early. Propagate client disconnects to the upstream call on your server.

## Do it at the gateway (Bifrost)

Several of these controls work better in one place than in every service: per-request model routing, response caching, budgets, and cost attribution. Bifrost is an open-source (Apache 2.0) AI gateway that does all of them with OpenAI-compatible and provider-native drop-in endpoints. Repo: https://github.com/maximhq/bifrost, docs: https://docs.getbifrost.ai

### Run Bifrost locally

```bash
npx -y @maximhq/bifrost                       # or:
docker run -p 8080:8080 -v $(pwd)/data:/app/data maximhq/bifrost
# UI + API on http://localhost:8080 ; add provider keys in the UI (or config.json)
```

For production, pin a version (`maximhq/bifrost:<version>` or `npx -y @maximhq/bifrost --transport-version <version>`), enable auth, and issue virtual keys. Point existing SDKs at it by changing only the base URL:

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8080/openai", api_key="sk-bf-your-virtual-key")
```

```typescript
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic({ baseURL: "http://localhost:8080/anthropic", apiKey: "sk-bf-your-virtual-key" });
```

### Complexity Router: cheap model for simple requests, frontier for complex ones

The Complexity Router classifies each request as `SIMPLE`, `MEDIUM` or `COMPLEX` and exposes `complexity_tier` to CEL routing rules. The app keeps sending the model it sends today; a matching rule rewrites the target. Classification runs only when a rule references `complexity_tier`, and if no tier is produced the rule does not match and the request continues with normal routing.

1. Configure a classifier in the UI (**Models > Complexity Router**): **Decision model** (default Typesafe Jev; needs that provider configured with a key) or **Semantic** (embeds the request and matches reference phrases; needs an embedding provider such as `openai` / `text-embedding-3-small`).
2. Add routing rules (UI **Routing Rules**, `POST /api/routing/rules`, or `governance.routing_rules` in `config.json`):

```json
{
  "governance": {
    "routing_rules": [
      {
        "id": "complexity-simple",
        "name": "Simple -> small model",
        "enabled": true,
        "cel_expression": "complexity_tier == \"SIMPLE\"",
        "targets": [{ "provider": "openai", "model": "gpt-4o-mini", "weight": 1 }],
        "scope": "global",
        "priority": 0
      },
      {
        "id": "complexity-complex",
        "name": "Complex -> frontier model",
        "enabled": true,
        "cel_expression": "complexity_tier == \"COMPLEX\"",
        "targets": [{ "provider": "anthropic", "model": "claude-opus-4-5", "weight": 1 }],
        "scope": "global",
        "priority": 1
      }
    ]
  }
}
```

Unmatched (`MEDIUM`, or unclassified) requests keep the model the app asked for. Roll out with one rule or one team scope first, then filter logs by tier and compare quality and cost. Full setup, classifier choice, tuning, session-aware routing and verification: [references/complexity-routing.md](references/complexity-routing.md).

### Semantic and exact response caching

Enable the `semantic_cache` plugin with a vector store (Redis, Weaviate, Qdrant, Pinecone; or direct-hash-only mode with no embeddings). Caching engages only for requests that carry `x-bf-cache-key` (or when `default_cache_key` is set). Hits are reported in `x-bifrost-cache-hit` response headers and the `bifrost_cache_hits_total` metric. Config and safety rules: [references/caching.md](references/caching.md).

### Get provider prompt-cache hits

- **Session affinity:** send a stable `x-bf-session-id` per conversation or agent run. Bifrost keeps the session on the provider and key that served it, so each turn lands where its prompt cache lives. Claude Code, Codex CLI and OpenCode session headers are picked up automatically. Docs: https://docs.getbifrost.ai/providers/session-affinity.md
- **Auto prompt caching:** set `"prompt_cache": {"auto_inject": true}` on a provider (e.g. `anthropic`) and Bifrost adds a cache breakpoint to requests from clients that send none. Off by default; caller markers always win. Docs: https://docs.getbifrost.ai/features/prompt-caching.md

### Budgets, rate limits and cost attribution

- **Virtual keys** per team, feature or customer, each with `budgets` (e.g. `{"max_limit": 100.00, "reset_duration": "1M"}`), `rate_limit`, and `allowed_models`. Once a budget is used up, further requests are rejected with `402` until it resets; rate limits return `429`. Teams and customers can carry their own budgets above the key.
- **`x-bf-dim-<name>` headers** (e.g. `x-bf-dim-feature: summarize`) tag a request; the tag flows to logs, OpenTelemetry spans, and Prometheus custom labels.
- **`bifrost_cost_total`** (USD) on `/metrics`, labeled by `provider`, `model`, `virtual_key_name`, `team_name`, `customer_name`, `routing_rule_name`, `complexity_tier`.
- **Custom pricing** overrides catalog prices with your negotiated rates so reported cost matches the invoice: https://docs.getbifrost.ai/providers/custom-pricing.md

Setup and PromQL: [references/budgets-and-attribution.md](references/budgets-and-attribution.md). At org scale, Bifrost Enterprise adds budget and rate-limit alerting to Slack, PagerDuty and webhooks (14-day free trial: https://www.getmaxim.ai/bifrost/enterprise).

## Verify

1. **Cost moved:** compare cost per feature (or `bifrost_cost_total` per label) for equal traffic windows before and after. Report cost per 1,000 requests, not totals, so traffic changes do not hide the result.
2. **Quality held:** rerun the eval set for every feature whose model, prompt, or context changed. Spot-check production outputs for routed and cached traffic.
3. **Caches hit:** provider `cached_tokens` > 0 on repeat prefixes; response-cache hit rate is non-zero where expected and zero where it must be (personalized answers).
4. **Caps work:** force an agent into a loop in a test and confirm it stops at the cap; send a request to a key with a $0.01 budget and confirm it is refused.
5. **Latency:** cheaper models are usually faster, but a classifier, embedding lookup or LLM fallback adds latency per request. Check p95.

## Common mistakes

- Optimizing before measuring, then trimming a feature that was 2% of spend.
- Switching a call site to a smaller model with no eval set, and shipping a quality regression.
- Putting timestamps, request IDs or user data at the start of the prompt and wondering why prompt caching never hits.
- Load-balancing one conversation across providers or keys, breaking prompt-cache locality.
- Semantic cache with a low threshold or a shared key across users, serving wrong or private answers.
- No `max_tokens`, no loop cap, and unlimited retries on an agent.
- Counting only chat calls; embeddings, classifier calls, LLM-judge evals and retries also cost money.
- Using list prices in dashboards when the contract has discounts or committed-use pricing.
- Moving interactive traffic to batch APIs; batch is for work that can wait hours.

## References

- [references/complexity-routing.md](references/complexity-routing.md): read when routing per request by difficulty (Bifrost Complexity Router setup, rules, rollout, tuning, app-side alternative).
- [references/caching.md](references/caching.md): read when enabling provider prompt caching, response caching (exact/semantic), session affinity, or embedding reuse.
- [references/budgets-and-attribution.md](references/budgets-and-attribution.md): read when the question is "who is spending what", or when adding budgets, rate limits, per-feature tags, cost dashboards or custom pricing.
