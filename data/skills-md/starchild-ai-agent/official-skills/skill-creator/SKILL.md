---
name: skill-creator
version: 1.0.0
description: "Create and scaffold new skills with proper frontmatter, directory structure, and validation. Use when the user asks to build a new capability, integrate a new API, or extend the system with a repeatable workflow."

metadata:
  starchild:
    emoji: "🛠️"
    skillKey: skill-creator

user-invocable: true
---

# Skill Creator

Create new skills to permanently extend your capabilities.

## Core Principles

**Concise is key.** The context window is a shared resource between the system prompt, skills, conversation history, and your reasoning. Every line in a SKILL.md competes with everything else. Only add what you don't already know — don't document tool parameters visible in the system prompt, don't prescribe step-by-step workflows for things you can figure out. Focus on domain knowledge, interpretation guides, decision frameworks, and gotchas.

**Progressive disclosure.** Skills load in three levels:
1. **Always in context** — name, emoji, and description appear in `<available_skills>` in every conversation. This is how you decide which skill to activate. The description must be a strong trigger.
2. **On activation** — the full SKILL.md body is loaded via `read_file` when you decide the skill is relevant. This is where workflow, guidelines, and decision trees live.
3. **On demand** — scripts/, references/, and assets/ are only loaded when explicitly needed. Heavy content goes here, not in the body.

This means: keep the SKILL.md body lean (< 500 lines). Put detailed API docs in `references/`. Put automation in `scripts/`. The body should be what you need to *start working*, not an encyclopedia.

**Degrees of freedom.** Match instruction specificity to task fragility:

- **High freedom** (text guidance) — When multiple approaches are valid. Write natural language explaining WHAT and WHY, not step-by-step HOW. Example: "Check funding rates and social sentiment to gauge market mood."
- **Medium freedom** (pseudocode + params) — When a preferred pattern exists but details can vary. Describe the approach with key parameters. Example: "Use RSI with period 14, buy below 30, sell above 70."
- **Low freedom** (scripts in `scripts/`) — When operations are fragile, require exact syntax, or are repetitive boilerplate. Put the code in standalone scripts that get executed, not loaded into context. Example: Chart rendering with exact color codes and API calls.

Default assumption: you are already smart. Only add context you don't already have.

## Anatomy of a Skill

```
my-skill/
├── SKILL.md          # Required: Frontmatter + instructions
├── scripts/          # Optional: Executable code (low freedom)
│   └── render.py     #   Run via bash, not loaded into context
├── references/       # Optional: Docs loaded on demand (medium freedom)
│   └── api-guide.md  #   Loaded via read_file when needed
└── assets/           # Optional: Templates, images, data files
    └── template.json #   NOT loaded into context, used in output
```

**When to use each:**

| Directory | Loaded into context? | Use for |
|-----------|---------------------|---------|
| SKILL.md body | On activation | Core workflow, decision trees, gotchas |
| `scripts/` | Never (executed) | Fragile operations, exact syntax, boilerplate |
| `references/` | On demand | Detailed API docs, long guides, lookup tables |
| `assets/` | Never | Templates, images, data files used in output |

## Creating a Skill

### Step 1: Understand the Request

Before scaffolding, understand what you're building:

- **What capability?** API integration, workflow automation, knowledge domain?
- **What triggers it?** When should the agent activate this skill? (This becomes the description.)
- **What freedom level?** Can the agent improvise, or does it need exact scripts?
- **What dependencies?** API keys, binaries, Python packages?

Examples:
- "I want to generate charts" → charting skill with scripts (low freedom rendering)
- "Help me think about trading strategies" → knowledge skill (high freedom, conversational)
- "Integrate with Binance API" → API skill with env requirements and reference docs

### Step 2: Scaffold

Use the init script:

```bash
python skills/skill-creator/scripts/init_skill.py my-new-skill --path ./workspace/skills
```

With resource directories:
```bash
python skills/skill-creator/scripts/init_skill.py api-helper --path ./workspace/skills --resources scripts,references
```

With example files:
```bash
python skills/skill-creator/scripts/init_skill.py my-skill --path ./workspace/skills --resources scripts --examples
```

### Step 3: Plan Reusable Contents

Before writing, decide what goes where:

- **SKILL.md body**: Core instructions the agent needs every time this skill activates. Decision trees, interpretation guides, "when to do X vs Y" logic.
- **scripts/**: Any code that must run exactly as written — API calls with specific auth, rendering with exact formats, data processing pipelines.
- **references/**: Detailed docs the agent might need occasionally — full API endpoint lists, schema definitions, troubleshooting guides.
- **assets/**: Output templates, images, config files that the agent copies/modifies for output.

### Step 4: Write the SKILL.md

Use `read_file` and `write_file` to complete the generated SKILL.md:

1. **Frontmatter** — Update description (CRITICAL trigger), add requirements, set emoji
2. **Body** — Write for the agent, not the user. Short paragraphs over bullet walls. Opinions over hedging.

Design patterns for the body:

- **Workflow-based** — Step-by-step process (charting: fetch data → configure chart → render → serve)
- **Task-based** — Organized by what the user might ask (trading: "analyze a coin" / "compare strategies" / "check sentiment")
- **Reference/guidelines** — Rules and frameworks (strategy: core truths, conversation style, when to pull data)
- **Capabilities-based** — Organized by what the skill can do (market-data: price tools / derivatives tools / social tools)

### Step 5: Validate

```bash
python skills/skill-creator/scripts/validate_skill.py ./workspace/skills/my-new-skill
```

### Step 6: Refresh

Call the `skill_refresh` tool to make the skill available:

```
skill_refresh()
```

## Frontmatter Format

The frontmatter uses `metadata.starchild` for Star Child-specific fields:

```yaml
---
name: skill-name
description: "What this skill does. Use when [specific trigger scenarios]."

metadata:
  starchild:
    emoji: "🔧"
    skillKey: skill-name
    requires:
      env: [API_KEY_NAME]
      bins: [python]
      anyBins: [curl, wget]
    install:
      - kind: pip
        package: pandas
      - kind: apt
        package: curl
        bins: [curl]

user-invocable: true
disable-model-invocation: false
---
```

**Field reference:**

| Field | Location | Required | Purpose |
|-------|----------|----------|---------|
| `name` | top-level | Yes | Skill identifier (lowercase hyphen-case) |
| `description` | top-level | Yes | Trigger text — when should the agent use this? |
| `emoji` | `metadata.starchild` | No | Display emoji |
| `skillKey` | `metadata.starchild` | No | Dedup key |
| `requires.env` | `metadata.starchild` | No | Required env vars |
| `requires.bins` | `metadata.starchild` | No | Required binaries (ALL must exist) |
| `requires.anyBins` | `metadata.starchild` | No | Required binaries (ANY one) |
| `install` | `metadata.starchild` | No | How to install deps (pip, apt, npm, etc.) |
| `user-invocable` | top-level | No | Can user trigger via /command (default: true) |
| `disable-model-invocation` | top-level | No | Hide from `<available_skills>` (default: false) |

## On-Chain Skills — Wallet Policy Prerequisite

If the skill involves **any on-chain operations** (sending transactions, token approvals, swaps, bridging, signing, deposits, withdrawals, smart contract interactions), add a Prerequisites section near the top of the SKILL.md:

```markdown
## Prerequisites — Wallet Policy

Before executing any [operation], the wallet policy must be active.
Load the **wallet-policy** skill and propose the standard wildcard
policy (deny key export + allow `*`). This covers all [skill-name]
operations across all chains.
```

This ensures the agent proposes a wallet policy **before** attempting any transaction. Without it, the first transaction will fail with a policy violation.

## What NOT to Include

- **README.md** — The SKILL.md IS the readme. Don't duplicate.
- **CHANGELOG.md** — Skills aren't versioned packages.
- **Docs the agent already has** — Don't repeat tool descriptions from the system prompt.
- **Step-by-step for simple tasks** — The agent can figure out "read a file then process it."
- **Generic programming advice** — "Use error handling" is noise. Specific gotchas are signal.

## Best Practices

1. **Description is the trigger.** This is how the agent decides to activate your skill. Include "Use when..." with specific scenarios. Bad: "Trading utilities." Good: "Test trading strategies against real historical data. Use when a strategy needs validation or before committing to a trade approach."

2. **Write for the agent, not the user.** The skill is instructions for the AI. Use direct language: "You generate charts" not "This skill can be used to generate charts."

3. **Scripts execute without loading.** Good for large automation. The agent reads the script only when it needs to customize, keeping context clean.

4. **Don't duplicate the system prompt.** The agent already sees tool names and descriptions. Focus on knowledge it doesn't have: interpretation guides, decision trees, domain-specific gotchas.

5. **Request credentials last.** Design the skill first, then ask the user for API keys.

6. **Always validate** before refreshing — run `validate_skill.py` to catch issues early.
