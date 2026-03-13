---
name: openclaw-cost-optimization
description: "Audit and optimize OpenClaw API costs. Applies six proven optimizations — model routing, prompt caching, lean context, local heartbeats, rate limits, and workspace trimming — to cut monthly spend by up to 90%. Use when asked to reduce costs, optimize tokens, audit API spend, or configure cost-saving settings."
---

# OpenClaw Cost Optimization

Your OpenClaw setup is probably burning money on three things: using expensive models for trivial tasks, re-processing the same static files on every message, and loading context the agent never touches.

The default config optimizes for capability. That's fine when you're exploring. But once you're running 24/7, it's the difference between $1,500/month and $150/month or even less.

This skill audits your current setup and applies six optimizations in order of impact. Most take under 5 minutes. Combined, they cut costs by roughly 97% without reducing quality where it matters.

---

## What Claude Gets Wrong Without This

Left to its own defaults, an OpenClaw agent will:
- Run Sonnet or Opus for "what's the weather?" — that's a Haiku job
- Load 50KB of context at session start when 8KB would do
- Send heartbeat checks to a paid API 96 times a day
- Re-process your SOUL.md and USER.md at full price on every single message
- Let a search loop burn $20 overnight with no guardrails

None of these are bugs. They're just defaults that weren't designed for 24/7 autonomous operation.

---

## The Six Optimizations

Ordered by impact. Start at #1 and work down.

### 1. Route the Right Model to the Right Job

**Impact: $40-300/month saved depending on usage**

This is the single biggest lever. Your agent handles many different types of work — chat, heartbeats, coding, web crawling, image analysis — and each has a model that hits the sweet spot of quality vs cost. Using Opus for a heartbeat check is like hiring a surgeon to take your temperature.

**The model routing map:**

| Task | Best (no budget) | Budget alternative | Savings |
|------|-----------------|-------------------|---------|
| **Chat (brain)** | Opus 4.6 | Kimi K2.5 | Massive — near-Opus intelligence, slightly less personality |
| **Heartbeat checks** | Haiku 4.5 | Haiku 4.5 (+ reduce frequency) | ~$50/month |
| **Coding / overnight dev** | Codex GPT-5.2 | Miniax 2.1 | ~$250/month on long coding runs |
| **Web browsing / crawling** | Opus 4.6 | DeepSeek V3 | Hundreds/month if you crawl a lot |
| **Image understanding** | Opus 4.6 | Gemini 2.5 Flash | Significant — Flash is very capable on vision |
| **Routine tasks** | Haiku 4.5 | Haiku 4.5 | 10x cheaper than Sonnet |

**The key insight:** You're not picking ONE cheap model. You're building a roster where each task gets the cheapest model that handles it well.

**Default model** — set your daily driver to Haiku or Kimi depending on how much personality matters:

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-haiku-4-5"
      }
    }
  }
}
```

**Model aliases** — define aliases in `agents.defaults.models` so cron jobs and agents can reference models by short name:

```json5
{
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-haiku-4-5": { "alias": "haiku" },
        "anthropic/claude-sonnet-4-5": { "alias": "sonnet" },
        "anthropic/claude-opus-4-6": { "alias": "opus" },
        "openai/codex-gpt-5.2": { "alias": "code" },
        "deepseek/deepseek-v3": { "alias": "crawl" },
        "google/gemini-2.5-flash": { "alias": "vision" }
      }
    }
  }
}
```

**Heartbeat frequency matters too.** Default is often every 10 minutes. If you're running Opus for heartbeats, that's ~$2/day / ~$54/month just on "anything need attention?" checks. Switch to Haiku AND reduce frequency to every hour:

```json5
{
  "heartbeat": {
    "every": "1h",
    "model": "anthropic/claude-haiku-4-5"
  }
}
```

That alone drops heartbeat costs to $0.01-0.10/day.

**Add to your agent's SOUL.md or system prompt:**

```markdown
## Model Selection
Default: Haiku for routine tasks.
Escalate to Sonnet/Opus only for: architecture decisions, code review, security analysis, complex reasoning.
For coding sessions: prefer Codex or dedicated coding model.
For web crawling: use DeepSeek V3.
For image analysis: use Gemini Flash.
When uncertain, try the cheaper model first.
```

The model follows this as a behavioral constraint. No code changes needed.

---

### 2. Cache Stable Context

**Impact: up to 90% discount on repeated tokens**

Every message re-reads SOUL.md, USER.md, tool definitions, and reference docs. These files don't change between requests. Without caching, you're paying full price to re-process identical content dozens of times a day.

Anthropic's prompt caching charges 10% for cached tokens on reuse. For content you send repeatedly, that's a 90% cut on your most frequent cost.

**What to cache** (stable, rarely updated):
- SOUL.md — personality, rules
- USER.md — user profile, preferences
- TOOLS.md — tool definitions
- Reference docs, project specs

**What NOT to cache** (changes frequently):
- Daily memory files
- Conversation history
- Tool outputs, search results

**Config** — set `cacheRetention` per model in `agents.defaults.models`:

```json5
{
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-opus-4-6": {
          "alias": "opus",
          "params": { "cacheRetention": "short" }
        }
      }
    }
  }
}
```

| Value | Cache Duration | Notes |
|-------|---------------|-------|
| `"none"` | No caching | Disables prompt caching |
| `"short"` | 5 minutes | **Default for API key auth** |
| `"long"` | 1 hour | Requires beta flag |

> **Note:** OpenClaw automatically applies `"short"` (5-min cache) when using Anthropic API key authentication. You only need to set this explicitly if you want `"long"` or `"none"`.

**Tips for maximizing cache hits:**
- Batch related requests within the cache window (5 min for `short`, 1h for `long`)
- Align heartbeat frequency just under the cache TTL (e.g., every 4 min for `short`, every 55 min for `long`) to keep caches warm
- Don't edit SOUL.md mid-conversation — each change invalidates the cache
- Keep stable content at the top of your context hierarchy

---

### 3. Start Sessions Lean

**Impact: ~$0.35 saved per session, $10-15/month with frequent use**

Many setups eagerly load everything at startup: full memory archives, past conversations, every reference file. Most of it sits unused.

**Load only what the agent needs to be itself and understand today:**

| Load at startup | Skip at startup |
|----------------|----------------|
| SOUL.md | Full conversation history |
| USER.md | Past memory archives |
| IDENTITY.md | Research docs from old projects |
| Today's memory file | Other agents' files |

**For everything else: pull on demand.** When a topic comes up that needs historical context, use memory search:

```
"Search my memory for what we discussed about the marketing campaign"
```

Semantic search retrieves the relevant passages without loading the entire history. This is both cheaper and more effective — targeted retrieval beats brute-force loading.

**Add to your agent's instructions:**

```markdown
## Session Startup
Load ONLY: SOUL.md, USER.md, IDENTITY.md, today's memory file.
For prior context: use memory_search() on demand. Don't pre-load history.
```

**Result:** Sessions start with ~8KB of context instead of 50KB+. The agent is faster, cheaper, and paradoxically better — less noise in the context means more focused responses.

---

### 4. Route Heartbeats to a Local Model

**Impact: $5-15/month saved**

Heartbeats are periodic checks — "anything need attention?" — that run every 15-60 minutes. They're simple tasks that don't need frontier reasoning. But by default, each one is a paid API call.

Route them to a free local model via Ollama instead.

**Setup:**

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a lightweight model (2GB, handles heartbeat tasks easily)
ollama pull llama3.2:3b
```

**Config:**

```json5
{
  "heartbeat": {
    "model": "ollama/llama3.2:3b"
  }
}
```

**Why it works:** Heartbeat tasks are classification problems — "is there something that needs attention?" A 3B parameter model running locally answers this with zero issues. The quality difference from Sonnet is nonexistent for yes/no monitoring, and the cost drops to zero on your API bill.

**Requirements:** A machine running Ollama with ~2GB free RAM. If OpenClaw already runs on a home server or VPS, you have this.

---

### 5. Set Rate Limits and Budget Caps

**Impact: prevents $50-200/month in runaway costs**

AI agents can loop. A search spawns follow-up searches. A debugging session fires dozens of API calls in seconds. Without guardrails, a single runaway interaction can burn through a day's budget in minutes.

**Add to SOUL.md or system prompt:**

```markdown
## API Discipline
- 5 seconds minimum between consecutive API calls
- 10 seconds minimum between web searches
- Max 5 searches per batch, then pause 2 minutes
- If a task needs more than 10 API calls, ask before continuing
- On rate limit error (429): stop, wait 5 minutes, retry once
```

**Budget discipline via behavioral rules:**

OpenClaw doesn't have a native budget config key. Instead, enforce limits through your agent's instructions and external monitoring:

1. **Set Anthropic API spend alerts** — configure billing alerts directly in [Anthropic Console](https://console.anthropic.com/) or your provider dashboard
2. **Add behavioral limits to SOUL.md** (see above) — the agent will self-regulate
3. **Monitor with the CLI:**
```bash
openclaw cron list --all --json  # Check what's running and on which model
```
4. **Track via Anthropic usage dashboard** — review daily/weekly spend patterns

Rate limits prevent waste during normal operation. Provider-level budget alerts catch edge cases. Together: predictable spending without limiting capability.

---

### 6. Trim Your Workspace Files

**Impact: incremental but compounding — saves on every single request**

SOUL.md, USER.md, and similar files load on every interaction. Every unnecessary line costs tokens not once, but on every message. A 200-line SOUL.md that could be 80 lines is silently 2-3x more expensive than it needs to be on your highest-frequency cost.

**The audit question for each line:** "Does the agent need this to do its job?"

**What stays:**
- Core personality (2-3 sentences, not paragraphs)
- Hard behavioral rules that change output
- Communication preferences
- Operational constraints

**What goes:**
- Backstory or lore (move to a reference doc, load on demand)
- Redundant restatements of the same rule
- Verbose explanations of things Claude already knows
- "Nice to have" context that doesn't affect responses

**Before (bloated, 85 tokens):**
```markdown
## Communication Style
You should always communicate in a way that is clear, concise, and helpful.
When talking to the user, make sure your responses are well-structured and easy
to follow. Use bullet points when listing things. Don't write overly long
responses unless the topic genuinely requires depth. The user values efficiency.
```

**After (lean, 22 tokens):**
```markdown
## Style
Direct and concise. Use structure for complex answers. Match depth to the question.
```

Same behavior. One-fourth the cost, multiplied by every message.

---

## Combined Impact

| Optimization | Monthly Savings | Setup Time |
|-------------|----------------|------------|
| Default to Haiku | $40-60 | 5 min |
| Prompt caching | $15-30 | 2 min |
| Lean startup context | $10-15 | 30 min |
| Local heartbeats | $5-15 | 15 min |
| Rate limits + budgets | $50-200 (prevention) | 10 min |
| Trim workspace files | $5-10 | 1 hour |

**From $1,500+/month to $30-50/month.**

Model routing and caching deliver the biggest absolute savings. Workspace trimming compounds over time because it reduces cost on every interaction.

---

## How to Apply This

You don't need to hand-edit JSON files for most of these. Tell your OpenClaw agent:

> "Switch your default model to Haiku. Only use Sonnet for complex reasoning tasks."

> "Enable prompt caching — set cacheRetention to 'long' for my Anthropic models."

> "Add API discipline rules to my SOUL.md — rate limits, search batching, and escalation thresholds."

> "Audit my SOUL.md and USER.md — flag anything that doesn't directly affect your output quality."

OpenClaw can modify its own config in most cases. Just ask.

---

## Verifying It Works

### Verification Commands

**Check actual model per cron job** (the table view hides this — you MUST use JSON):
```bash
openclaw cron list --all --json
```
Look at each job's `payload.model` field. Don't assume from the agent assignment — cron jobs can override the agent's default model.

**Check heartbeat status per agent** (config is in `~/.openclaw/openclaw.json`):
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import json,sys; c=json.load(sys.stdin)
d=c['agents']['defaults'].get('heartbeat',{}).get('every','')
print(f'Default: {d or \"(disabled)\"}')
for a in c['agents']['list']:
    e=a.get('heartbeat',{}).get('every',d)
    print(f'{a[\"id\"]}: {e or \"(disabled)\"}')
"
```
Agents without a `heartbeat` block inherit the default. An agent running on Opus with `every: "15m"` inherited = your biggest cost line.

**Check bootstrap context size:**
```bash
wc -c SOUL.md USER.md AGENTS.md MEMORY.md
```

### What Good Looks Like

- **Context size:** Should be 2-8KB at session start, not 50KB+
- **Default model:** Should show Haiku, not Sonnet
- **Cron jobs:** Each job's `payload.model` should match its complexity (Haiku for checkers, Sonnet for structured tasks, Opus only for creative/complex work)
- **Heartbeat:** Should route to Ollama/local or Haiku at minimum
- **Daily costs:** Should drop to $0.10-0.50 range within the first day

If costs haven't dropped, the most common issue is the system prompt not loading the model selection rules. Verify your SOUL.md changes are being picked up.

### Common Audit Mistake

Don't infer cron job models from the agent assignment. `openclaw cron list` table shows `Agent: sherlock` but the job itself may override the model in its payload. Always check `openclaw cron list --all --json` for the actual `payload.model` field.

---

## Anti-Patterns

**"I'll just use Haiku for everything, including complex tasks."**
Don't. Haiku is fast and cheap but genuinely worse at multi-step reasoning, nuanced analysis, and creative work. The goal is right-sizing, not downgrading. Escalate when quality matters.

**"I'll cache everything to save money."**
Caching volatile content (daily notes, tool outputs) wastes the cache slot and provides no benefit. Cache only what's stable.

**"I'll set the budget to $1/day to be safe."**
Too aggressive. Your agent will hit the cap during legitimate work and stop mid-task. Start at $5/day, observe for a week, then adjust based on actual patterns.

**"I trimmed SOUL.md to 10 lines and now the agent acts weird."**
You cut too deep. Some personality and behavioral rules genuinely affect output quality. Trim the fat, keep the muscle. If behavior degrades, add back the specific rule that was controlling it.

---

## Quality Check

Before sharing this config with others:

- [ ] Default model is Haiku (not Sonnet/Opus)
- [ ] Caching enabled for stable files
- [ ] Session startup loads only essentials
- [ ] Heartbeat routes to local model (or cheapest available)
- [ ] Budget caps set with warning threshold
- [ ] Workspace files audited for unnecessary content
- [ ] Agent behavior verified — no quality regression on important tasks
