---
name: creative-seeds
description: Inject creative absurdity to break AI pattern-thinking before creative tasks. Randomly samples surreal micro-stories to spark unconventional thinking. Use before brainstorming, naming, writing, or any task needing fresh perspective.
allowed-tools: Bash
---

# Creative Seeds

Before any creative task, run the script below — it selects 3 random seeds and returns them directly.

## How to Use

Run this to pull 3 random seeds:

```bash
python3 -c "
import random, re, os
with open(os.path.expanduser('~/.claude/skills/creative-seeds/seeds.md')) as f:
    content = f.read()
seeds = [s.strip() for s in re.split(r'\n---\n', content) if re.search(r'##\s*\d+\.', s)]
random.shuffle(seeds)
print('\n\n---\n\n'.join(seeds[:3]))
"
```

## Instructions

1. Run the bash command above — it returns 3 randomly selected seed paragraphs
2. Read the output — let the absurdist logic seep in
3. Then proceed with the actual creative task with that mental residue active
4. Do NOT explain the seeds to the user unless asked — just use them internally to shift your thinking frame

The seeds are not prompts. They are cognitive disruptors. They work by contaminating your pattern-matching with nonsense, forcing novel connections.
