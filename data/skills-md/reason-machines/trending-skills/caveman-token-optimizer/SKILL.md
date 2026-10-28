---
name: caveman-token-optimizer
description: Claude Code skill that makes AI agents respond in caveman-speak, cutting ~65-75% of output tokens while preserving full technical accuracy
triggers:
  - "install caveman mode"
  - "make claude talk like caveman"
  - "reduce token usage caveman"
  - "enable caveman skill"
  - "less tokens please"
  - "caveman mode for claude code"
  - "add caveman plugin"
  - "token optimization caveman"
---

# Caveman Token Optimizer

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code skill and Codex plugin that makes AI agents respond in compressed caveman-speak — cutting **~65% of output tokens on average** (up to 87%) while keeping full technical accuracy. No pleasantries. No filler. Just answer.

## What It Does

Caveman mode strips:
- Pleasantries: "Sure, I'd be happy to help!" → gone
- Hedging: "It might be worth considering" → gone
- Articles (a, an, the) → gone
- Verbose transitions → gone

Caveman keeps:
- All code blocks (written normally)
- Technical terms (exact: `useMemo`, `polymorphism`, `middleware`)
- Error messages (quoted exactly)
- Git commits and PR descriptions (normal)

**Same fix. 75% less word. Brain still big.**

## Install

### Claude Code (npx)
```bash
npx skills add JuliusBrussee/caveman
```

### Claude Code (plugin system)
```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

### Codex
1. Clone the repo
2. Open Codex inside the repo
3. Run `/plugins`
4. Search `Caveman`
5. Install plugin

Install once. Works in all sessions after that.

### Manual / Local
```bash
git clone https://github.com/JuliusBrussee/caveman.git
cd caveman
pip install -e .
```

## Usage — Trigger Commands

### Claude Code
```
/caveman          # enable default (full) caveman mode
/caveman lite     # professional brevity, grammar intact
/caveman full     # default — drop articles, use fragments
/caveman ultra    # maximum compression, telegraphic
```

### Codex
```
$caveman
$caveman lite
$caveman full
$caveman ultra
```

### Natural language triggers
Any of these phrases activate caveman mode:
- "talk like caveman"
- "caveman mode"
- "less tokens please"
- "be concise"

### Disable
```
/caveman off
# or say: "stop caveman" / "normal mode"
```

Level sticks until changed or session ends.

## Intensity Levels

| Level | Trigger | Style | Example |
|-------|---------|-------|---------|
| **Lite** | `/caveman lite` | Drop filler, keep grammar | "Component re-renders because inline object prop creates new reference each cycle. Wrap in `useMemo`." |
| **Full** | `/caveman full` | Drop articles, use fragments | "New object ref each render. Inline prop = new ref = re-render. Wrap in `useMemo`." |
| **Ultra** | `/caveman ultra` | Telegraphic, abbreviate everything | "Inline obj prop → new ref → re-render. `useMemo`." |

## Benchmark Results

Real token counts from Claude API (reproducible via `benchmarks/` directory):

| Task | Normal | Caveman | Saved |
|------|-------:|--------:|------:|
| React re-render bug | 1180 | 159 | 87% |
| Auth middleware fix | 704 | 121 | 83% |
| PostgreSQL pool setup | 2347 | 380 | 84% |
| Git rebase vs merge | 702 | 292 | 58% |
| Async/await refactor | 387 | 301 | 22% |
| Docker multi-stage build | 1042 | 290 | 72% |
| **Average** | **1214** | **294** | **65%** |

> **Important:** Caveman only affects output tokens. Thinking/reasoning tokens are untouched. Caveman make *mouth* smaller, not brain.

## Reproducing Benchmarks

```bash
git clone https://github.com/JuliusBrussee/caveman.git
cd caveman/benchmarks

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here

# Run benchmark suite
python run_benchmarks.py

# Compare normal vs caveman responses
python compare.py --task react-rerender
python compare.py --task auth-middleware
python compare.py --all
```

## Code Examples — What Caveman Mode Changes

### Before (normal, 69 tokens)
```
The reason your React component is re-rendering is likely because
you're creating a new object reference on each render cycle. When
you pass an inline object as a prop, React's shallow comparison
sees it as a different object every time, which triggers a
re-render. I'd recommend using useMemo to memoize the object.
```

### After (caveman full, 19 tokens)
```
New object ref each render. Inline object prop = new ref = re-render.
Wrap in `useMemo`.
```

### Code blocks stay normal — caveman not stupid
```python
# Caveman explains in grunt, but code stays clean:
# "Token expiry check broken. Fix:"

def verify_token(token: str) -> bool:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    # Was: payload["exp"] < time.time()
    # Fix:
    return payload["exp"] >= time.time()
```

## What Caveman Preserves vs. Removes

```python
# Tokens caveman REMOVES (waste):
filler_phrases = [
    "I'd be happy to help you with that",   # 8 tokens gone
    "The reason this is happening is because", # 7 tokens gone
    "I would recommend that you consider",   # 7 tokens gone
    "Sure, let me take a look at that",      # 8 tokens gone
    "Great question!",                        # 2 tokens gone
    "Certainly!",                             # 1 token gone
]

# Things caveman KEEPS (substance):
preserved = [
    "code blocks",          # always normal
    "technical_terms",      # exact spelling preserved
    "error_messages",       # quoted verbatim
    "variable_names",       # exact
    "git_commits",          # normal prose
    "pr_descriptions",      # normal prose
]
```

## Integration Pattern — Using in a Project

If you want caveman-style compression in your own Claude API calls:

```python
import anthropic

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

# Load the caveman SKILL.md as a system prompt addition
with open("path/to/caveman/SKILL.md", "r") as f:
    caveman_skill = f.read()

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system=f"{caveman_skill}\n\nRespond in caveman mode: full intensity.",
    messages=[
        {"role": "user", "content": "Why is my React component re-rendering?"}
    ]
)

print(response.content[0].text)
# → "New object ref each render. Inline prop = new ref = re-render. useMemo fix."
print(f"Tokens used: {response.usage.output_tokens}")  # ~19 vs ~69
```

## Session Workflow

```
# Start session with caveman
/caveman full

# Ask technical questions normally — agent responds in caveman
> Why does my Docker build take so long?
→ "Layer cache miss. COPY before RUN npm install. Fix order:"
[code block shown normally]

# Switch intensity mid-session
/caveman lite

# Turn off for PR description writing
/caveman off
> Write a PR description for this auth fix
→ [normal, professional prose]

# Back to caveman
/caveman
```

## Troubleshooting

**Caveman mode not activating:**
```bash
# Verify plugin installed
claude plugin list | grep caveman

# Reinstall
claude plugin remove caveman
claude plugin install caveman@caveman
```

**Savings lower than expected:**
- Caveman only compresses *output* tokens — input tokens unchanged
- Tasks with heavy code output (like Docker setup) see less savings since code is preserved verbatim
- Reasoning/thinking tokens not affected — savings show in visible response only
- Ultra mode gets maximum compression; switch if full mode feels verbose

**Need normal mode for specific output:**
```
/caveman off   # for PR descriptions, user-facing docs, formal reports
/caveman       # re-enable after
```

**Benchmarking your own tasks:**
```bash
cd benchmarks/
export ANTHROPIC_API_KEY=your_key_here
python run_benchmarks.py --task "your custom task description"
```

## Why It Works

Backed by a March 2026 paper ["Brevity Constraints Reverse Performance Hierarchies in Language Models"](https://arxiv.org/abs/2604.00025): constraining large models to brief responses **improved accuracy by 26 percentage points** on certain benchmarks. Verbose not always better.

```
TOKENS SAVED          ████████ 65% avg (up to 87%)
TECHNICAL ACCURACY    ████████ 100%
RESPONSE SPEED        ████████ faster (less to generate)
READABILITY           ████████ better (no wall of text)
```

## Key Files

```
caveman/
├── SKILL.md          # the skill definition loaded by Claude Code
├── benchmarks/
│   ├── run_benchmarks.py   # reproduce token count results
│   └── compare.py          # side-by-side comparison tool
├── plugin.json             # Codex plugin manifest
└── README.md
```

## Links

- **Repo:** https://github.com/JuliusBrussee/caveman
- **Homepage:** https://juliusbrussee.github.io/caveman/
- **Also by Julius:** [Blueprint](https://github.com/JuliusBrussee/blueprint) — spec-driven dev for Claude Code

---

*One rock. That it.* 🪨
