---
name: together-chat-completions
description: Serverless chat and text completion inference via Together AI's OpenAI-compatible API. Access 100+ open-source models with pay-per-token pricing. Includes function calling (tool use) with 6 calling patterns, structured outputs (JSON mode, json_schema, regex), and reasoning/thinking models (DeepSeek R1, Qwen3 Thinking, Kimi K2). Use when building chat applications, text generation, multi-turn conversations, function calling, structured JSON outputs, reasoning/chain-of-thought, thinking mode toggle, or any LLM inference task using Together AI.
---

# Together Chat Completions

## Overview

Send inference requests to 100+ open-source models via Together AI's serverless API. OpenAI-compatible — swap the base URL and API key to migrate existing code.

- Base URL: `https://api.together.xyz/v1`
- Auth: `Authorization: Bearer $TOGETHER_API_KEY`
- Endpoints: `/v1/chat/completions` (chat), `/v1/completions` (text)
- SDKs: `pip install together` (Python), `npm install together-ai` (TypeScript)

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## Quick Start

### Basic Chat Completion

```python
from together import Together

client = Together()

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "What are some fun things to do in NYC?"}],
)
print(response.choices[0].message.content)
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.chat.completions.create({
  model: "openai/gpt-oss-20b",
  messages: [{ role: "user", content: "What are some fun things to do in NYC?" }],
});
console.log(response.choices[0].message.content);
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/gpt-oss-20b","messages":[{"role":"user","content":"What are some fun things to do in NYC?"}]}'
```

### Streaming

Set `stream=True` to receive tokens incrementally:

```python
stream = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

```typescript
import Together from "together-ai";
const together = new Together();

const stream = await together.chat.completions.create({
  model: "openai/gpt-oss-20b",
  messages: [
    { role: "user", content: "What are some fun things to do in New York?" },
  ],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || "");
}
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "messages": [
      {"role": "user", "content": "What are some fun things to do in New York?"}
    ],
    "stream": true
  }'
```

### Multi-Turn Conversation

Pass conversation history in the `messages` array with alternating `user`/`assistant` roles:

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a helpful travel guide."},
        {"role": "user", "content": "What should I do in Paris?"},
        {"role": "assistant", "content": "Visit the Eiffel Tower and the Louvre!"},
        {"role": "user", "content": "How about food recommendations?"},
    ],
)
```

### Async (Python)

Use `AsyncTogether` for parallel requests:

```python
import asyncio
from together import AsyncTogether

async def main():
    client = AsyncTogether()
    tasks = [
        client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": msg}],
        )
        for msg in ["Hello", "How are you?", "Tell me a joke"]
    ]
    responses = await asyncio.gather(*tasks)
    for r in responses:
        print(r.choices[0].message.content)

asyncio.run(main())
```

## Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (required) |
| `messages` | array | Conversation messages with `role` and `content` (required for chat) |
| `max_tokens` | int | Max tokens to generate |
| `temperature` | float | Sampling temperature (0-1, default ~0.7) |
| `top_p` | float | Nucleus sampling threshold (0-1) |
| `top_k` | int | Top-k sampling |
| `repetition_penalty` | float | Penalize repeated tokens (>1.0 = more penalty) |
| `stop` | string[] | Stop sequences |
| `stream` | bool | Enable streaming |
| `response_format` | object | Force JSON output or schema (see function-calling skill) |
| `logprobs` | int | Return log probabilities for top N tokens |
| `n` | int | Number of completions to generate |

## Message Roles

- **system**: Set model behavior and context (first message)
- **user**: End-user input
- **assistant**: Model responses (for conversation history)
- **tool**: Tool/function call results

## OpenAI Compatibility

Migrate from OpenAI by changing base URL and API key:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key="YOUR_TOGETHER_API_KEY",
)
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## Text Completions

For non-chat models, use `/v1/completions`:

```python
response = client.completions.create(
    model="openai/gpt-oss-20b",
    prompt="The quick brown fox",
    max_tokens=50,
)
print(response.choices[0].text)
```

## Rate Limits & Build Tiers

Rate limits depend on your Build Tier (based on lifetime spend):

| Tier | Lifetime Spend | RPM (most models) |
|------|---------------|-------------------|
| Tier 1 | $5+ | 60 |
| Tier 2 | $50+ | 600 |
| Tier 3 | $200+ | 600 |
| Tier 4 | $500+ | 600 |
| Tier 5 | $1000+ | 600 |

Larger models (>100B) have separate, lower limits. See references/models.md for the full model catalog.

## Function Calling (Tool Use)

Define tools the model can call, then execute them and pass results back:

```python
import json
from together import Together
client = Together()

tools = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
        },
    },
}]

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can access external functions."},
        {"role": "user", "content": "What is the current temperature of New York?"},
    ],
    tools=tools,
)

# Process tool calls
tool_calls = response.choices[0].message.tool_calls
for tc in tool_calls:
    args = json.loads(tc.function.arguments)
    result = get_current_weather(**args)  # your function

    # Pass result back
    messages.append(response.choices[0].message)
    messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})

final = client.chat.completions.create(model="Qwen/Qwen2.5-7B-Instruct-Turbo", messages=messages, tools=tools)
```

```typescript
import Together from "together-ai";
const together = new Together();

const response = await together.chat.completions.create({
  model: "Qwen/Qwen2.5-7B-Instruct-Turbo",
  messages: [
    {
      role: "system",
      content: "You are a helpful assistant that can access external functions.",
    },
    { role: "user", content: "What is the current temperature of New York?" },
  ],
  tools: [
    {
      type: "function",
      function: {
        name: "getCurrentWeather",
        description: "Get the current weather in a given location",
        parameters: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA",
            },
            unit: {
              type: "string",
              description: "The unit of temperature",
              enum: ["celsius", "fahrenheit"],
            },
          },
        },
      },
    },
  ],
});

console.log(JSON.stringify(response.choices[0].message?.tool_calls, null, 2));
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-7B-Instruct-Turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant that can access external functions."
      },
      {
        "role": "user",
        "content": "What is the current temperature of New York?"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_current_weather",
          "description": "Get the current weather in a given location",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
              },
              "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"]
              }
            }
          }
        }
      }
    ]
  }'
```

### tool_choice Parameter

- `"auto"` (default): Model decides whether to call functions
- `"required"`: Model must call at least one function
- `"none"`: Never call functions
- `{"type": "function", "function": {"name": "fn_name"}}`: Force specific function

### 6 Calling Patterns

1. **Simple**: Single function, single call
2. **Multiple functions**: Multiple tools available, model picks one
3. **Parallel**: Same function called multiple times in one turn
4. **Parallel multiple**: Different functions called in one turn
5. **Multi-step**: Chained calls (call -> result -> call -> result)
6. **Multi-turn**: Function calls across conversation turns

**Supported models**: Qwen2.5 family, Llama 3.x/4, DeepSeek V3, Mistral, GLM, Kimi K2, and most chat models.

## Structured Outputs (JSON Mode)

### json_schema (Recommended)

Constrain output to match your JSON schema exactly:

```python
from pydantic import BaseModel, Field

class VoiceNote(BaseModel):
    title: str = Field(description="A title")
    summary: str = Field(description="Short summary")
    actionItems: list[str] = Field(description="Action items")

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": f"Respond in JSON: {json.dumps(VoiceNote.model_json_schema())}"},
        {"role": "user", "content": "Summarize: Meeting about Q4 planning..."},
    ],
    response_format={"type": "json_schema", "schema": VoiceNote.model_json_schema()},
)
result = VoiceNote.model_validate_json(response.choices[0].message.content)
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "system",
        "content": "The following is a voice message transcript. Only answer in JSON."
      },
      {
        "role": "user",
        "content": "Good morning! Today is going to be a busy day. First, I need to make a quick breakfast. While cooking, I will also check my emails."
      }
    ],
    "model": "openai/gpt-oss-20b",
    "response_format": {
      "type": "json_schema",
      "schema": {
        "properties": {
          "title": { "type": "string", "description": "A title for the voice note" },
          "summary": { "type": "string", "description": "A short one sentence summary" },
          "actionItems": { "items": { "type": "string" }, "type": "array", "description": "Action items" }
        },
        "required": ["title", "summary", "actionItems"],
        "type": "object"
      }
    }
  }'
```

### json_object (Simple)

Model outputs valid JSON, structure guided by prompt only:

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "Respond in JSON with keys: name, age, city"},
        {"role": "user", "content": "Tell me about yourself"},
    ],
    response_format={"type": "json_object"},
)
```

### regex (Pattern Matching)

Constrain output to match a regex:

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Classify sentiment: I loved the movie!"}],
    response_format={"type": "regex", "pattern": "(positive|neutral|negative)"},
)
```

**JSON mode supported models**: DeepSeek R1/V3, GLM-5, Kimi K2, Llama 4, Qwen3/2.5, and many more.

## Reasoning Models

Reasoning models think step-by-step before answering. Best for complex math, code, planning, and logic tasks.

**How reasoning output is returned:**
- **Most reasoning models** (Kimi K2.5, GLM-5, GPT-OSS, Qwen3 Thinking, etc.) return reasoning in a separate `reasoning` field: `response.choices[0].message.reasoning`
- **DeepSeek R1** is a special case that outputs reasoning inside `<think>` tags within the `content` field

### Quick Start

```python
stream = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "Which is bigger: 9.9 or 9.11?"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

```typescript
import Together from "together-ai";
const together = new Together();

const stream = await together.chat.completions.create({
  model: "deepseek-ai/DeepSeek-R1",
  messages: [{ role: "user", content: "Which number is bigger 9.9 or 9.11?" }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || "");
}
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/DeepSeek-R1",
    "messages": [
      {"role": "user", "content": "Which number is bigger 9.9 or 9.11?"}
    ]
  }'
```

Output:
```
<think>
Let me compare 9.9 and 9.11...
9.9 = 9.90, and 9.90 > 9.11
</think>

**Answer:** 9.9 is bigger.
```

### Available Reasoning Models

| Model | API String | Strengths |
|-------|-----------|-----------|
| DeepSeek R1 | `deepseek-ai/DeepSeek-R1` | Math, code, complex reasoning |
| DeepSeek V3.1 | `deepseek-ai/DeepSeek-V3.1` | General + reasoning |
| GPT-OSS 120B | `openai/gpt-oss-120b` | Reasoning only (adjustable effort) |
| GPT-OSS 20B | `openai/gpt-oss-20b` | Reasoning only (adjustable effort) |
| Kimi K2 Thinking | `moonshotai/Kimi-K2-Thinking` | Extended reasoning |
| Kimi K2.5 | `moonshotai/Kimi-K2.5` | Hybrid (reasoning + general) |
| GLM-5 | `zai-org/GLM-5` | Hybrid |
| MiniMax M2.5 | `MiniMaxAI/MiniMax-M2.5` | Reasoning only |
| Qwen3 235B Thinking | `Qwen/Qwen3-235B-A22B-Thinking-2507` | Thinking mode |
| Qwen3.5 397B | `Qwen/Qwen3.5-397B-A17B` | Hybrid |
| QwQ 32B | `Qwen/QwQ-32B` | Compact reasoning |
| R1 Distill Llama 70B | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | Distilled reasoning |
| R1 Distill Qwen 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | Compact distilled |

### Reasoning Effort

Control how much thinking the model does (`"low"`, `"medium"`, `"high"`):

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Prove the infinitude of primes"}],
    reasoning_effort="high",
)
```

```typescript
import Together from "together-ai";
const together = new Together();

const stream = await together.chat.completions.create({
  model: "openai/gpt-oss-120b",
  messages: [{ role: "user", content: "Prove the infinitude of primes" }],
  reasoning_effort: "high",
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || "");
}
```

```shell
curl -X POST "https://api.together.xyz/v1/chat/completions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "messages": [
      {"role": "user", "content": "Prove the infinitude of primes"}
    ],
    "reasoning_effort": "high"
  }'
```

### Qwen3 Thinking Toggle

Toggle thinking on/off by choosing the model variant:

- **Thinking enabled:** `Qwen/Qwen3-235B-A22B-Thinking-2507`
- **Thinking disabled (faster, cheaper):** `Qwen/Qwen3-235B-A22B-Instruct-2507-tput`

### Accessing Reasoning Output

**Most models (Kimi K2.5, GLM-5, GPT-OSS, Qwen3, etc.) -- use the `reasoning` field:**

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Which is bigger: 9.9 or 9.11?"}],
)
reasoning = response.choices[0].message.reasoning  # step-by-step thinking
answer = response.choices[0].message.content         # final answer
print(f"Reasoning: {reasoning}")
print(f"Answer: {answer}")
```

**DeepSeek R1 -- parse `<think>` tags from `content`:**

```python
import re
content = response.choices[0].message.content
think_match = re.search(r"<think>(.*?)</think>", content, re.DOTALL)
thinking = think_match.group(1).strip() if think_match else ""
answer = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
```

### Best Practices

- **DeepSeek R1**: Use temperature 0.5-0.7, omit system prompts, put instructions in user message
- Use streaming — reasoning outputs are long
- Use `reasoning_effort="low"` for simple questions, `"high"` for complex math/code/logic
- Reasoning models cost more (more tokens) — use standard models for simple tasks

## Resources

- **Model catalog and specs**: See [references/models.md](references/models.md)
- **Full parameter reference**: See [references/api-parameters.md](references/api-parameters.md)
- **Function calling patterns (detailed)**: See [references/function-calling-patterns.md](references/function-calling-patterns.md)
- **Structured output details**: See [references/structured-outputs.md](references/structured-outputs.md)
- **Reasoning model details**: See [references/reasoning-models.md](references/reasoning-models.md)
- **Runnable script**: See [scripts/tool_call_loop.py](scripts/tool_call_loop.py) — tool call loop with parallel call handling (v2 SDK)
- **Official docs**: [Chat Overview](https://docs.together.ai/docs/chat-overview)
- **Official docs**: [Inference Parameters](https://docs.together.ai/docs/inference-parameters)
- **Official docs**: [Serverless Models](https://docs.together.ai/docs/serverless-models)
- **Official docs**: [Function Calling](https://docs.together.ai/docs/function-calling)
- **Official docs**: [JSON Mode](https://docs.together.ai/docs/json-mode)
- **Official docs**: [Reasoning Overview](https://docs.together.ai/docs/reasoning-overview)
- **Official docs**: [DeepSeek R1](https://docs.together.ai/docs/deepseek-r1)
- **API reference**: [Chat Completions API](https://docs.together.ai/reference/chat-completions)
