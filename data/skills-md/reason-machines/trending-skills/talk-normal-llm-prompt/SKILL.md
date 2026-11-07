---
name: talk-normal-llm-prompt
description: System prompt toolkit that removes AI slop and makes any LLM respond like a normal person — concise, direct, no filler.
triggers:
  - make the LLM stop being verbose
  - remove AI slop from responses
  - use talk-normal system prompt
  - make ChatGPT talk normally
  - reduce LLM output verbosity
  - install talk-normal prompt
  - strip filler from AI responses
  - configure LLM to be concise
---

# talk-normal

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

**talk-normal** is a system prompt (plus a shell-script helper) that strips AI slop — bullet-point padding, hollow affirmations, corporate filler — from any LLM while preserving all useful information. Tested at **~73% character reduction** on GPT-4o-mini and GPT-5.4 with no information loss.

---

## How it works

The project is a single `prompt.md` file (the system prompt) plus optional shell helpers. You copy the prompt text into the "System" field of any LLM interface or API call.

```
repo layout
├── prompt.md          ← the system prompt (main artifact)
├── CHANGELOG.md       ← rule history
├── CONTRIBUTING.md    ← how to add rules
└── TEST_RESULTS.md    ← before/after comparisons
```

---

## Installation

### 1 — Clone the repo

```bash
git clone https://github.com/hexiecs/talk-normal.git
cd talk-normal
```

### 2 — Read the prompt

```bash
cat prompt.md
```

### 3 — Copy into your tool

Paste the contents of `prompt.md` into:
- **ChatGPT** → Settings → Customize ChatGPT → Custom Instructions → "How should ChatGPT respond?"
- **Claude.ai** → Project Instructions
- **Cursor / Windsurf** → `.cursorrules` or global AI rules
- **API calls** → `system` parameter (see examples below)

---

## Using the prompt via API

### OpenAI (Python)

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

system_prompt = Path("prompt.md").read_text()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": "What is Python?"},
    ],
)
print(response.choices[0].message.content)
```

### OpenAI (curl)

```bash
SYSTEM=$(cat prompt.md | jq -Rs .)

curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gpt-4o-mini\",
    \"messages\": [
      {\"role\": \"system\", \"content\": $SYSTEM},
      {\"role\": \"user\",   \"content\": \"What is Python?\"}
    ]
  }"
```

### Anthropic Claude (Python)

```python
import os
from pathlib import Path
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

system_prompt = Path("prompt.md").read_text()

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    system=system_prompt,
    messages=[{"role": "user", "content": "Explain Docker in one paragraph."}],
)
print(message.content[0].text)
```

### Google Gemini (Python)

```python
import os
from pathlib import Path
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

system_prompt = Path("prompt.md").read_text()

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt,
)

response = model.generate_content("What is a neural network?")
print(response.text)
```

### Ollama (local models)

```bash
SYSTEM=$(cat prompt.md)

ollama run llama3 \
  --system "$SYSTEM" \
  "What is a REST API?"
```

Or via the Ollama Python SDK:

```python
import subprocess, json
from pathlib import Path

system_prompt = Path("prompt.md").read_text()

result = subprocess.run(
    ["ollama", "run", "llama3"],
    input=f"SYSTEM: {system_prompt}\nUSER: What is a REST API?",
    capture_output=True, text=True,
)
print(result.stdout)
```

---

## Shell helper: one-liner wrapper

A reusable shell function that injects the prompt automatically:

```bash
# Add to ~/.bashrc or ~/.zshrc
export TALK_NORMAL_PROMPT="$HOME/talk-normal/prompt.md"

asknormal() {
  local question="$*"
  local system
  system=$(cat "$TALK_NORMAL_PROMPT")

  curl -s https://api.openai.com/v1/chat/completions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg sys "$system" \
      --arg q   "$question" \
      '{model:"gpt-4o-mini",messages:[{role:"system",content:$sys},{role:"user",content:$q}]}'
    )" | jq -r '.choices[0].message.content'
}
```

Usage:

```bash
source ~/.bashrc
asknormal "What is the CAP theorem?"
```

---

## Embedding in a project's AI config

### Cursor (`.cursorrules`)

```bash
# Prepend talk-normal to your existing rules
cat talk-normal/prompt.md > .cursorrules
echo "" >> .cursorrules
echo "# Project-specific rules below" >> .cursorrules
cat your-existing-rules.md >> .cursorrules
```

### OpenAI Assistants API

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
system_prompt = Path("talk-normal/prompt.md").read_text()

assistant = client.beta.assistants.create(
    name="Normal Assistant",
    instructions=system_prompt,
    model="gpt-4o-mini",
)
print(f"Assistant ID: {assistant.id}")
```

---

## Combining with your own system prompt

talk-normal rules are additive — prepend them before your domain instructions:

```python
from pathlib import Path

talk_normal = Path("talk-normal/prompt.md").read_text()

your_rules = """
You are a senior backend engineer. Answer questions about Python, Go, and distributed systems.
"""

combined_system = f"{talk_normal}\n\n---\n\n{your_rules}"
```

---

## Common patterns

### Pattern 1: Measure verbosity reduction

```python
def verbosity_ratio(before: str, after: str) -> float:
    """Returns fraction of original length kept (lower = more concise)."""
    return len(after) / len(before)

before = "Python is a high-level, interpreted programming language known for its readability..."  # 1583 chars
after  = "Python is a high-level, interpreted language known for readability..."                  #  513 chars
print(f"{verbosity_ratio(before, after):.0%} of original length")  # → 32%
```

### Pattern 2: A/B test with and without the prompt

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
system_prompt = Path("talk-normal/prompt.md").read_text()

question = "What is Kubernetes?"

def ask(system: str | None, user: str) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return resp.choices[0].message.content

without = ask(None, question)
with_prompt = ask(system_prompt, question)

print(f"Without: {len(without)} chars")
print(f"With:    {len(with_prompt)} chars")
print(f"Reduction: {(1 - len(with_prompt)/len(without)):.0%}")
```

### Pattern 3: Keep the prompt up to date

```bash
# Pull latest rules from upstream
cd talk-normal
git pull origin main

# Check what changed
git log --oneline -10
cat CHANGELOG.md | head -50
```

---

## Contributing a new rule

1. Fork the repo and create a branch: `git checkout -b rule/no-em-dashes`
2. Edit `prompt.md` — add your rule in plain imperative English
3. Add an entry to `CHANGELOG.md`
4. Open an Issue or PR describing: what slop the rule targets, a before/after example

```bash
# Quick before/after test for your new rule
SYSTEM=$(cat prompt.md)
echo "Test question" | asknormal   # uses your modified prompt
```

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Model still uses bullet points | Ensure the system prompt is in the `system` role, not prepended to `user` |
| Prompt too long for context window | Use a smaller model or trim older messages; `prompt.md` is intentionally compact |
| Ollama ignores system prompt | Some quantized models have weak instruction-following; try `mistral` or `llama3` |
| Rules conflict with your own system prompt | Put talk-normal rules first; add `# Override:` comment before conflicting rules |
| Response is too terse / lost information | The prompt reduces filler, not facts — file an issue with a reproduction case |

---

## Key facts for agents

- **Primary artifact**: `prompt.md` — copy its text verbatim as the `system` message
- **No code to run**: this is a prompt, not a library; no `pip install`, no build step
- **Model-agnostic**: works with GPT, Claude, Gemini, LLaMA, Mistral, etc.
- **Tested reduction**: ~72–73% character reduction, zero information loss on 10-question benchmark
- **License**: MIT — use freely in commercial products
