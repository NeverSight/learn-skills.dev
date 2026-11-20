---
name: agentic-design-systems
description: |
  Scaffold or audit a component library whose main consumer is an AI agent:
  machine-readable metadata for props, variants, relationships, component-scoped
  tokens, and anti-patterns.
triggers:
  - "agentic design system"
  - "AI-readable design system"
  - "component metadata schema"
  - "agent-readable components"
  - "design system for AI agents"
das:
  type: skill
  category: design-systems
  upstream: "https://github.com/thedesignproject/agent-skills"
  version: latest
---

# agentic-design-systems

> Catalogue stub — full skill: [thedesignproject/agent-skills](https://github.com/thedesignproject/agent-skills)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/agentic-design-systems/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/agentic-design-systems/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `agentic-design-systems`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/agentic-design-systems ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add thedesignproject/agent-skills --skill agentic-design-systems -g -y
   ```

   **Project:**
   ```bash
   npx skills add thedesignproject/agent-skills --skill agentic-design-systems -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `agentic-design-systems`
- Trigger phrases: "agentic design system", "AI-readable design system", "component metadata schema"

## What it does

Defines a schema for describing each component to an agent (props, variants, relationships to other components, component-scoped tokens, usage hints and anti-patterns) and a step-by-step workflow to scaffold that metadata for a new library or audit an existing one, with a worked example. Instructions only: no scripts, no network calls, no account.

## When NOT to use

- Extracting token values from a live site → use `extract-design-system`
- Writing a DESIGN.md of visual rules from existing code → use `extract-design-md`
- Token file format and architecture (W3C DTCG) → use `design-tokens-skill`
- Ownership, versioning and deprecation policy → use `design-system-governance`
- Building or auditing a design system inside Figma → use `work-with-design-systems`
