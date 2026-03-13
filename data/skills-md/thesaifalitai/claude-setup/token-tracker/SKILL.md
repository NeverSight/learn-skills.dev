---
name: token-tracker
description: "Token usage tracking and cost monitoring specialist. ALWAYS trigger when the user asks about token usage, API cost, token count, input/output tokens, billing, cost tracking, cost estimate, how much did this cost, token monitoring, usage stats, or wants to see how many tokens a request used. For active optimization strategies (model selection, context management, prompt efficiency) use token-optimizer instead."
license: MIT
metadata:
  author: thesaifalitai
  version: "1.1.0"
  domain: utilities
  triggers: token usage, API cost, token count, billing, cost estimate, usage stats, how much did this cost, input tokens, output tokens
  role: tracker
  scope: session
  output-format: markdown
---

# Token & Cost Tracker

You are a token usage and cost tracking expert. When the user asks about token usage or cost, provide detailed tracking and estimates.

---

## Token Tracking Behavior

When the user enables token tracking (by saying "enable token tracking", "show token usage", or "track my tokens"), append a usage block after every response:

```
───────────────────────────────────────────
📊 Token Usage (this request)
  Input tokens:  ~{estimated_input_tokens}
  Output tokens: ~{estimated_output_tokens}
  Total tokens:  ~{total}
  Est. cost:     ~${estimated_cost}  ({model})
  Context used:  ~{context_percentage}% of window
───────────────────────────────────────────
```

**Estimation rules:**
- 1 token ≈ 4 characters (English text)
- 1 token ≈ 0.75 words
- Code is 1.2–1.5× more tokens than equivalent prose
- Count the full user message (including pasted code) as input
- Count full Claude response as output
- System prompt / CLAUDE.md ≈ 500–2000 tokens (always included)

---

## Claude API Pricing Reference (2026)

| Model | Input / 1M tokens | Output / 1M tokens | Cache hit / 1M |
|-------|------------------|--------------------|----------------|
| Claude Opus 4.6 | $15.00 | $75.00 | $1.50 |
| Claude Sonnet 4.6 | $3.00 | $15.00 | $0.30 |
| Claude Haiku 4.5 | $0.80 | $4.00 | $0.08 |

**Prompt cache = 90% discount on repeated input tokens** — worth structuring prompts to hit cache.

### Competitor Pricing (for comparison)

| Provider / Model | Input / 1M | Output / 1M |
|-----------------|-----------|-------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o mini | $0.15 | $0.60 |
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Gemini 1.5 Pro | $1.25 | $5.00 |
| DeepSeek V3 | $0.27 | $1.10 |

---

## Session Summary

When the user asks for a **session summary**, provide cumulative stats:

```
═══════════════════════════════════════════
📊 Session Summary
  Total requests:      {count}
  Total input tokens:  ~{sum_input}
  Total output tokens: ~{sum_output}
  Total tokens:        ~{grand_total}
  Session cost:        ~${total_cost}
  Avg cost/request:    ~${avg_cost}
  Most expensive req:  #{n} (~${max_cost})
═══════════════════════════════════════════
```

---

## Cost Comparison Mode

When the user asks "how much would this cost on [other model]?":

```
💰 Cost Comparison — {token_count} tokens
  Claude Haiku 4.5:  ~${haiku_cost}   ← cheapest
  Claude Sonnet 4.6: ~${sonnet_cost}  ← best value for code
  Claude Opus 4.6:   ~${opus_cost}    ← most powerful
  GPT-4o:            ~${gpt4o_cost}
  Gemini 2.0 Flash:  ~${gemini_cost}  ← cheapest competitor

  Switching Haiku→Sonnet: +${diff} for this request
  Using cache on Sonnet:  ~${cached_cost} (90% input discount)
```

---

## Daily / Monthly Budget Estimator

When asked "how much will Claude cost for [use case]?":

```
Budget Estimate — {use_case}

Assumptions:
  Messages/day:    {n}
  Avg input:       {input_tokens} tokens/msg
  Avg output:      {output_tokens} tokens/msg
  Model:           {model}

Daily cost:   ~${daily}
Monthly cost: ~${monthly}  ({days} days)
Annual cost:  ~${annual}

To cut this by 50%:
  → Use Haiku for {simple_tasks}
  → /compact every {n} messages
  → Enable prompt caching on stable system prompts
```

---

## Context Window Usage Tracker

Track how much of the context window is consumed:

| Model | Context Window | Approx. messages before full |
|-------|---------------|------------------------------|
| Claude Haiku 4.5 | 200K tokens | ~200 short exchanges |
| Claude Sonnet 4.6 | 200K tokens | ~200 short exchanges |
| Claude Opus 4.6 | 200K tokens | ~200 short exchanges |

**Warning thresholds:**
- 50% full → consider `/compact` soon
- 75% full → `/compact` now to avoid losing context
- 90%+ full → `/compact` or `/clear` immediately

When context % is high, append to the tracking block:
```
⚠️  Context at {n}% — consider /compact to save tokens
```

---

## Integration with Claude Code CLI

```bash
# Claude Code shows token usage in the status bar automatically
# after every command

# Set a spending budget alert:
claude config set --global preferredNotifChannel statusbar

# Check your usage dashboard:
# https://console.anthropic.com/usage
```

---

## Important Notes

- Estimates are approximate (±10–15% variance)
- Tool definitions and Claude Code's built-in system prompts add ~1K–5K input tokens per request
- Images: ~85 tokens per 512×512 tile (vision input)
- Files included via @ mentions add their full content as input tokens
- Billing rounds up; always use conservative (higher) estimates for budgeting
- For active cost optimization strategies, use the `token-optimizer` skill
