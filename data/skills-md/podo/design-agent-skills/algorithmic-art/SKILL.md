---
name: algorithmic-art
description: |
  Create generative art using p5.js with seeded randomness, flow fields, and
  particle systems. Official Anthropic skill for procedural visual art generation
  in Claude artifacts.
triggers:
  - "algorithmic art"
  - "generative art"
  - "flow field art"
  - "particle system"
  - "procedural art"
  - "creative coding art"
das:
  category: creative-3d
  upstream: "https://github.com/anthropics/skills"
  upstream_path: "skills/algorithmic-art/SKILL.md"
  version: latest
  install: true
---

# algorithmic-art

> Catalogue stub — full skill: [anthropics/skills](https://github.com/anthropics/skills/blob/main/skills/algorithmic-art/SKILL.md)

## Decision tree

1. **Is the full skill already installed?**
   Check whether the skill at this location still has a `das:` block:
   - Global: `grep -q "^das:" ~/.agents/skills/algorithmic-art/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/algorithmic-art/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke it and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   To detect scope:
   ```bash
   [ -e ~/.agents/skills/algorithmic-art ] && echo "global" || echo "project"
   ```

   **Global** (installed with `-g`):
   ```bash
   npx skills add anthropics/skills --skill algorithmic-art -g -y
   ```

   **Project** (installed without `-g`):
   ```bash
   npx skills add anthropics/skills --skill algorithmic-art -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.


## Invoke after install

- Skill name: `algorithmic-art`
- Trigger phrases: "algorithmic art", "generative art", "p5.js", "flow field", "particle system"

## What it does

Official Anthropic skill for creating generative art with p5.js. Produces seeded-random compositions — flow fields, particle systems, geometric progressions — inside Claude artifacts. Seeding ensures reproducible outputs while retaining organic variation. Use for creative coding, visual experiments, and procedurally generated illustrations.
