---
name: metaclaw-evolving-agent
description: Deploy and configure MetaClaw — an agent that meta-learns and evolves from live conversations using skills injection, RL training, and smart scheduling.
triggers:
  - set up metaclaw agent
  - configure evolving agent
  - metaclaw skills mode
  - metaclaw rl training
  - metaclaw madmax scheduler
  - agent meta-learning setup
  - tinker rl backend configuration
  - metaclaw proxy deployment
---

# MetaClaw Evolving Agent

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

MetaClaw is an OpenAI-compatible proxy agent that intercepts conversations, injects learned skills, and continuously improves itself through real-world interactions. It supports three modes: lightweight skills injection, immediate RL training, and a smart "madmax" scheduler that defers weight updates to idle/sleep windows.

---

## Installation

```bash
# Minimal — skills injection only, no GPU required
pip install -e .

# Full RL training support (torch, transformers, tinker)
pip install -e ".[rl]"

# Skill evolution via LLM summarization
pip install -e ".[evolve]"

# Google Calendar scheduler for madmax mode
pip install -e ".[scheduler]"

# Recommended: everything
pip install -e ".[rl,evolve,scheduler]"
```

---

## Quick Start

```bash
# One-time interactive config wizard
metaclaw setup

# Start in default madmax mode (skills + RL + smart scheduler)
metaclaw start

# Skills only — no GPU, no Tinker needed
metaclaw start --mode skills_only

# RL mode — trains immediately when batch is full
metaclaw start --mode rl

# RL without scheduler (same as above, explicit)
metaclaw start --mode rl
```

After `metaclaw start`, a local OpenAI-compatible proxy is running. Point your client (OpenClaw or any OpenAI SDK consumer) at `http://localhost:<port>` instead of the upstream LLM endpoint.

---

## Configuration

`metaclaw setup` writes a config file (default: `~/.metaclaw/config.yaml`). You can also edit it directly:

```yaml
# ~/.metaclaw/config.yaml

proxy:
  host: 0.0.0.0
  port: 8080

llm:
  provider: kimi          # kimi | qwen | claude | minimax | openai | gemini
  base_url: https://api.moonshot.cn/v1
  model: moonshot-v1-8k
  # api_key loaded from env: METACLAW_LLM_API_KEY

skills:
  enabled: true
  max_injected: 5         # max skills injected per turn
  summarize_after_session: true

rl:
  enabled: true
  backend: auto           # auto | tinker | mint
  batch_size: 32
  algorithm: grpo
  opd_teacher: false      # optional teacher distillation

scheduler:                # madmax mode only
  enabled: true
  sleep_hours: [22, 7]    # local 22:00–07:00
  idle_timeout_minutes: 15
  google_calendar: false  # set true + configure OAuth for meeting detection

logging:
  level: info
  log_dir: ~/.metaclaw/logs
```

### Environment Variables

```bash
export METACLAW_LLM_API_KEY="your-llm-api-key"
export METACLAW_TINKER_API_KEY="your-tinker-api-key"   # rl mode
export METACLAW_MINT_API_KEY="your-mint-api-key"        # if backend=mint
export GOOGLE_CALENDAR_CREDENTIALS_PATH="path/to/creds.json"  # scheduler
```

---

## Operating Modes

| Mode | Command | GPU Required | Description |
|------|---------|--------------|-------------|
| `skills_only` | `metaclaw start --mode skills_only` | No | Proxy + skills injection + auto-summarization |
| `rl` | `metaclaw start --mode rl` | Via API | Skills + GRPO training when batch fills |
| `madmax` | `metaclaw start` | Via API | Skills + RL + scheduler (trains only during idle/sleep/meetings) |

---

## Python API

### Programmatic startup

```python
import asyncio
from metaclaw import MetaClawAgent, AgentConfig, Mode

async def main():
    config = AgentConfig.from_yaml("~/.metaclaw/config.yaml")
    agent = MetaClawAgent(config, mode=Mode.MADMAX)
    await agent.start()

asyncio.run(main())
```

### Manual skill injection

```python
from metaclaw.skills import SkillStore, SkillInjector

store = SkillStore(path="~/.metaclaw/skills")

# Add a skill manually
store.add(
    name="code-review-checklist",
    content="Always check for: 1) error handling, 2) type hints, 3) docstrings.",
    tags=["code", "review"]
)

# Retrieve top-k relevant skills for a query
injector = SkillInjector(store)
relevant = injector.retrieve(query="review my Python function", top_k=3)
for skill in relevant:
    print(skill.name, skill.score)
```

### Intercepting and recording conversations

```python
from metaclaw.proxy import ConversationInterceptor
from metaclaw.memory import ExperienceBuffer

buffer = ExperienceBuffer(max_size=1000)

interceptor = ConversationInterceptor(
    upstream_url="https://api.moonshot.cn/v1",
    on_complete=buffer.record   # called after each turn with (messages, response)
)

# buffer.record signature:
async def on_complete(messages: list[dict], response: dict) -> None:
    ...
```

### Triggering RL training manually

```python
from metaclaw.training import RLTrainer, TrainingConfig

trainer = RLTrainer(
    config=TrainingConfig(
        backend="tinker",       # or "mint"
        algorithm="grpo",
        batch_size=32,
        lora_rank=16,
    )
)

# Collect a batch from the experience buffer and train
async def run_training(buffer):
    batch = buffer.sample(n=32, split="support")   # support/query separation
    result = await trainer.train(batch)
    print(f"Training complete. Loss: {result.loss:.4f}, Steps: {result.steps}")
```

### Reward modeling

```python
from metaclaw.rewards import RewardModel

reward_model = RewardModel(provider="llm")  # uses configured LLM for scoring

async def score_turn(prompt: str, response: str) -> float:
    score = await reward_model.score(prompt=prompt, response=response)
    return score  # float in [-1.0, 1.0]
```

---

## Skills Lifecycle

```
Conversation turn
       │
       ▼
 SkillInjector.retrieve()   ← vector search over SkillStore
       │  injects top-k skills into system prompt
       ▼
 LLM responds
       │
       ▼
 ExperienceBuffer.record()  ← stores (context, response, metadata)
       │
       ▼ (end of session)
 SkillSummarizer.run()      ← LLM extracts reusable patterns
       │
       ▼
 SkillStore.upsert()        ← new/updated skills persisted to disk
```

---

## Integration: OpenAI SDK as Client

Point any OpenAI SDK client at the MetaClaw proxy:

```python
from openai import OpenAI

# MetaClaw proxy is running on localhost:8080
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-used-but-required-by-sdk"
)

response = client.chat.completions.create(
    model="moonshot-v1-8k",   # passed through to upstream
    messages=[
        {"role": "user", "content": "Review my pull request strategy."}
    ]
)
print(response.choices[0].message.content)
```

Skills are injected transparently — the client code does not change.

---

## Scheduler (MadMax Mode)

The scheduler ensures RL weight updates never interrupt active use:

```python
from metaclaw.scheduler import MadMaxScheduler, SchedulerConfig

scheduler = MadMaxScheduler(
    config=SchedulerConfig(
        sleep_hours=(22, 7),          # train between 22:00–07:00 local time
        idle_timeout_minutes=15,      # train after 15 min of no conversations
        google_calendar=True,         # also train during calendar meetings
        credentials_path="creds.json"
    )
)

# Check if it's safe to train right now
if await scheduler.is_training_window():
    await trainer.train(batch)
```

### Google Calendar Setup

```bash
# 1. Enable Google Calendar API in Google Cloud Console
# 2. Download OAuth2 credentials as creds.json
# 3. Set path in config or env
export GOOGLE_CALENDAR_CREDENTIALS_PATH="/path/to/creds.json"

# 4. First run will open browser for OAuth consent
metaclaw start
```

---

## Support/Query Set Separation

MetaClaw separates experience into support and query sets to prevent stale rewards from polluting updates:

```python
from metaclaw.memory import ExperienceBuffer

buffer = ExperienceBuffer(
    max_size=2000,
    support_ratio=0.5   # 50% support, 50% query
)

# During training:
support_batch = buffer.sample(n=16, split="support")  # used to compute reward signal
query_batch   = buffer.sample(n=16, split="query")    # used for gradient update

await trainer.train_meta(support=support_batch, query=query_batch)
```

---

## RL Backends

### Tinker (default)

```yaml
rl:
  backend: tinker
  tinker_project: my-metaclaw-project
  lora_rank: 16
  learning_rate: 1e-4
```

### MinT

```bash
# Install MinT compatibility layer separately
pip install metaclaw-mint
```

```yaml
rl:
  backend: mint
  mint_endpoint: https://your-mint-endpoint
```

### Auto-detection

```yaml
rl:
  backend: auto   # tries tinker first, falls back to mint, errors if neither available
```

---

## Troubleshooting

**Proxy not reachable after `metaclaw start`**
- Check port conflicts: `lsof -i :8080`
- Change `proxy.port` in config and restart

**`rl` mode: "No training backend available"**
- Ensure `pip install -e ".[rl]"` completed successfully
- Verify `METACLAW_TINKER_API_KEY` or `METACLAW_MINT_API_KEY` is set
- Try `rl.backend: tinker` explicitly instead of `auto`

**Skills not persisting between sessions**
- Confirm `skills.summarize_after_session: true` in config
- Check write permissions on `~/.metaclaw/skills/`
- Run `metaclaw skills list` to inspect stored skills

**Madmax mode never trains**
- Verify `scheduler.sleep_hours` covers your timezone's night
- Lower `scheduler.idle_timeout_minutes` for testing (e.g., `1`)
- Check scheduler logs: `~/.metaclaw/logs/scheduler.log`

**Google Calendar integration fails**
- Re-run OAuth flow: delete `~/.metaclaw/token.json` and restart
- Ensure Calendar API is enabled in your Google Cloud project

**OPD teacher distillation errors**
- Only supported with `rl.backend: tinker`
- Requires a separate teacher model endpoint in config:
  ```yaml
  rl:
    opd_teacher: true
    teacher_base_url: https://api.openai.com/v1
    teacher_model: gpt-4o
  ```

---

## CLI Reference

```bash
metaclaw setup                   # interactive config wizard
metaclaw start                   # start in madmax mode
metaclaw start --mode skills_only
metaclaw start --mode rl
metaclaw start --config path/to/config.yaml

metaclaw skills list             # show all stored skills
metaclaw skills delete <name>    # remove a skill
metaclaw skills export skills.json

metaclaw status                  # show proxy, scheduler, training status
metaclaw logs                    # tail all logs
metaclaw logs --component scheduler
```
