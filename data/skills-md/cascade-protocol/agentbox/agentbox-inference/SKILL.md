---
name: agentbox-inference
description: "LLM inference via paid API: OpenAI-compatible chat completions proxied through x402 providers. Supports Kimi K2.5, MiniMax M2.5. Uses x_payment tool for automatic USDC micropayments ($0.001-$0.003/call). Use when: (1) generating text with a specific model, (2) running chat completions through a pay-per-request LLM endpoint, (3) comparing outputs across models."
metadata: {"openclaw": {"emoji": "🧠", "requires": {"bins": ["openclaw"]}}}
---

# LLM Inference

Paid OpenAI-compatible chat completions API at `https://inference.x402.agentbox.fyi`. Costs $0.001-$0.003 USDC per call via x402 on Solana. Use the `x_payment` tool for all requests.

## Endpoint

### Chat Completions

Generate a chat completion from a supported model.

```
x_payment({
  "url": "https://inference.x402.agentbox.fyi/v1/chat/completions",
  "method": "POST",
  "body": "{\"model\": \"moonshotai/kimi-k2.5\", \"messages\": [{\"role\": \"user\", \"content\": \"Explain x402 in one sentence\"}]}"
})
```

**Body Parameters:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| model | string | yes | Model ID (see table below) |
| messages | array | yes | Array of `{role, content}` objects |
| max_tokens | integer | no | Maximum tokens to generate |
| temperature | number | no | Sampling temperature (0-2) |
| top_p | number | no | Nucleus sampling (0-1) |

**Message roles:** `system`, `user`, `assistant`

## Models & Pricing

| Model | Cost/call | Best for |
|-------|-----------|----------|
| `moonshotai/kimi-k2.5` | $0.003 | High-quality output, large context (262K) |
| `minimax/minimax-m2.5` | $0.002 | Balanced quality/cost |

## Usage Patterns

### Simple question

```
x_payment({
  "url": "https://inference.x402.agentbox.fyi/v1/chat/completions",
  "method": "POST",
  "body": "{\"model\": \"moonshotai/kimi-k2.5\", \"messages\": [{\"role\": \"user\", \"content\": \"What is the x402 protocol?\"}]}"
})
```

### With system prompt and parameters

```
x_payment({
  "url": "https://inference.x402.agentbox.fyi/v1/chat/completions",
  "method": "POST",
  "body": "{\"model\": \"moonshotai/kimi-k2.5\", \"messages\": [{\"role\": \"system\", \"content\": \"You are a concise technical writer.\"}, {\"role\": \"user\", \"content\": \"Write a summary of Solana's transaction model\"}], \"max_tokens\": 500, \"temperature\": 0.7}"
})
```

## Response Format

Standard OpenAI chat completion response:

```json
{
  "id": "gen-...",
  "object": "chat.completion",
  "model": "moonshotai/kimi-k2.5",
  "choices": [{
    "index": 0,
    "message": { "role": "assistant", "content": "..." },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 42,
    "total_tokens": 54
  }
}
```

## Errors

| HTTP | Meaning |
|------|---------|
| 400 | Invalid request (check model name and messages format) |
| 402 | Payment required (handled automatically by x_payment) |
| 502 | Upstream provider error |

## Cost

Flat rate per model per call. Price is determined by the `model` field in the request body. Each call is independent - no sessions or state.
