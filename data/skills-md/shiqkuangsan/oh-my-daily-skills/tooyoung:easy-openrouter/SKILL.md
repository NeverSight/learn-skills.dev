---
name: tooyoung:easy-openrouter
description: "Quickly test and compare LLM models via OpenRouter. Find the fastest/cheapest model, compare response quality. Trigger words: openrouter, test model, compare models, find fastest model, find cheapest model"
metadata:
  version: "1.0.0"
---

# Easy OpenRouter

Quickly test LLM models and find the best one for your task.

## Prerequisites

```bash
export OPENROUTER_API_KEY="sk-or-v1-xxxx"
```

## Quick Model Testing

Use `scripts/call_openrouter.sh`:

```bash
# Basic test
bash scripts/call_openrouter.sh \
  --model "anthropic/claude-sonnet-4" \
  --prompt "Explain quantum computing in one sentence" \
  --json

# With parameters
bash scripts/call_openrouter.sh \
  --model "openai/gpt-4o" \
  --prompt "Write a haiku about code" \
  --max-tokens 100 \
  --temperature 0.7 \
  --json
```

**Output includes**: response time (ms), cost ($), token usage, full response

**Parameters**:

- `--model`: Model ID (required)
- `--prompt`: Prompt text (required)
- `--system`: System prompt (optional)
- `--max-tokens`: Max tokens
- `--temperature`: Temperature 0.0-2.0
- `--json`: JSON output

## Model Naming Format

```
provider/model-name[:modifier]
```

**Common models**:

- `anthropic/claude-sonnet-4`
- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- `google/gemini-2.0-flash-001`
- `deepseek/deepseek-chat`

**Modifiers**:

- `:nitro` - Use fastest provider
- `:online` - Enable web search
- Combinable: `anthropic/claude-sonnet-4:nitro:online`

## Find Optimal Models

### Find Best Model by Category (Rankings)

```
https://openrouter.ai/rankings?category=<category>#categories
```

| Category    | URL                                                                |
| ----------- | ------------------------------------------------------------------ |
| Programming | `https://openrouter.ai/rankings?category=programming#categories`   |
| Translation | `https://openrouter.ai/rankings?category=translation#categories`   |
| Science     | `https://openrouter.ai/rankings?category=science#categories`       |
| Finance     | `https://openrouter.ai/rankings?category=finance#categories`       |
| Legal       | `https://openrouter.ai/rankings?category=legal#categories`         |
| Academia    | `https://openrouter.ai/rankings?category=academia#categories`      |
| Marketing   | `https://openrouter.ai/rankings?category=marketing#categories`     |
| SEO         | `https://openrouter.ai/rankings?category=marketing/seo#categories` |

### Find Provider by Performance/Price

```
https://openrouter.ai/<model-slug>/providers?sort=<sort>
```

**Sort options**:

- `throughput` - By throughput (tokens/sec)
- `latency` - By latency
- `price` - By price

**Example**: Find fastest provider for claude-sonnet-4

```
https://openrouter.ai/anthropic/claude-sonnet-4/providers?sort=throughput
```

### Get Full Model List

```bash
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | jq '.data | sort_by(.pricing.prompt) | .[:10] | .[].id'
# Output: top 10 cheapest models
```

## Typical Workflows

### 1. Quick Model Comparison

```bash
# Test Claude
bash scripts/call_openrouter.sh --model "anthropic/claude-sonnet-4" --prompt "Explain microservices architecture" --json > claude.json

# Test GPT-4o
bash scripts/call_openrouter.sh --model "openai/gpt-4o" --prompt "Explain microservices architecture" --json > gpt4o.json

# Compare results
jq -s '[.[0], .[1]] | map({model, response_time_ms, cost})' claude.json gpt4o.json
```

### 2. Find Best Model for Programming Tasks

1. Open `https://openrouter.ai/rankings?category=programming#categories`
2. Note the top-ranked models
3. Test actual performance with the script

### 3. Choose Model for Chainlit Demo

Considerations:

- **For demos**: Prioritize speed → use `:nitro` modifier
- **Cost-sensitive**: Use `gpt-4o-mini` or `deepseek-chat`
- **Quality-first**: Use `claude-sonnet-4` or `gpt-4o`

## Advanced

For API details, query OpenRouter documentation via Context7.
