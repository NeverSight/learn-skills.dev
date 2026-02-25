---
name: skill-authoring
description: Use when authoring, creating, refining, or troubleshooting agent skills — covers SKILL.md structure, frontmatter syntax, description optimization, and activation testing. Also when building a new skill from scratch, when a skill won't trigger, loads incorrectly, or the agent ignores it entirely. Use when a skill misbehaved in the current session and needs adjustment based on learnings.
---

# Writing Skills

## What Is a Skill?

A skill is a way to teach an agent something it doesn't already know.

LLM agents are already smart. They can write code, analyze documents, reason through problems. But they don't know *your* codebase, *your* workflows, *your* domain's quirks. Skills bridge that gap — they're onboarding documents that transform a general-purpose agent into a specialized one equipped with knowledge no model ships with.

Think of skills as institutional memory made accessible to AI. The same way a senior engineer onboards a new hire by explaining "here's how we do X, here's why we avoid Y, here's the tool for Z" — a skill does that for an agent.

## How Agents Find Skills

Understanding discovery is essential to writing skills that work.

When a conversation starts, the agent sees only **metadata** — the `name` and `description` from every available skill's frontmatter. That's it. Not the body. Not the instructions. Just names and descriptions, loaded into context alongside everything else.

When you ask the agent something, it pattern-matches your request against those descriptions. If your request seems to match a skill's description, the agent loads that skill. Only then does it read the full SKILL.md body.

This has profound implications:

1. **A skill with a perfect body but a vague description will never trigger.** The agent can't use what it can't find.

2. **The description must contain the words users actually say.** If users say "help me with PDFs" but your description says "document processing," the skill won't activate.

3. **Descriptions that summarize workflow are dangerous.** Testing revealed that when a description says "does X then Y then Z," agents sometimes follow that summary instead of reading the full skill. Keep descriptions to *when to use*, not *what it does step-by-step*.

## The Anatomy of a Skill

```
skill-name/
├── SKILL.md              # Required. The entry point.
├── references/           # Optional. Detailed docs loaded on demand.
├── scripts/              # Optional. Code executed, not read into context.
└── assets/               # Optional. Templates, images for output.
```

Every skill has a SKILL.md with two parts:

**Frontmatter** (YAML) — The metadata the agent uses for discovery:
```yaml
---
name: my-skill
description: Use when [triggering conditions]. Covers [capabilities].
---
```

**Body** (Markdown) — The instructions the agent follows after the skill triggers. Only loaded when needed.

This split is intentional. Frontmatter is always in context (~100 tokens per skill). Bodies are loaded on demand. This is why you keep SKILL.md lean and push detailed reference material to separate files.

## Writing Descriptions That Work

The description is the most important thing you'll write. It determines whether your skill ever gets used.

**Formula:** Describe *when* to use it, not *how* it works.

```yaml
# ✅ Good — triggering conditions only
description: Use when working with PDF files — extracts text, fills forms, merges documents.

# ❌ Bad — summarizes workflow (agent may follow this instead of reading body)
description: Processes PDFs by first extracting text, then analyzing structure, then outputting results.

# ❌ Bad — too vague
description: Helps with documents.
```

**Include:**
- Trigger words users actually say ("extract", "merge", "analyze")
- File types and extensions (.pdf, .xlsx, .docx)
- Error messages or symptoms ("skill won't trigger", "agent ignores")
- Synonyms for common terms

**Exclude:**
- Step-by-step workflow
- Implementation details
- First-person language ("I can help you...")

## Writing Bodies That Teach

Once your skill triggers, the agent reads the body. This is where you teach.

The best skills follow a pattern:

1. **Orient** — What is this? What problem does it solve? (1-2 sentences)
2. **Instruct** — What should the agent do? (Imperative mood, clear steps)
3. **Show** — Concrete examples with real input/output
4. **Warn** — Common mistakes and how to avoid them

Don't over-explain. The agent is smart. Only add context it doesn't already have. Every paragraph should justify its token cost.

## Progressive Disclosure

Skills share the context window with everything else — system prompt, conversation history, other skills' metadata, the user's actual request. Context is a public good. Don't waste it.

Structure your skill in layers:

| Layer | What | When Loaded | Size Target |
|-------|------|-------------|-------------|
| 1 | name + description | Always | ~50 tokens |
| 2 | SKILL.md body | When skill triggers | <500 lines |
| 3 | references/, scripts/ | When agent needs them | Unlimited |

**Split when:**
- SKILL.md approaches 500 lines
- Content is domain-specific (load only for that domain)
- Reference material exceeds 100 lines

**Keep references one level deep.** Don't link from references to other references — the agent may not follow the chain.

## The Cardinal Rules

| Rule | Why It Matters |
|------|----------------|
| Description has trigger keywords | Without them, skill never activates |
| Description in third person | It's injected into system prompt |
| Name matches directory | Required for skill loading |
| Critical instructions in first 100 lines | Content can be truncated |
| SKILL.md under 500 lines | Context is precious |
| One excellent example > many mediocre | Quality over quantity |
| Test activation before deployment | A skill that works but never triggers = zero value |
| Use agent-agnostic language | Skills work with any LLM, not just one |

## When You're Ready to Build

This document taught you how skills work. Now you need the practical tools.

**Scripts** — Automate the boring parts:

```bash
python scripts/init.py my-skill          # Scaffold a new skill
./scripts/validate.sh path/to/skill # Check for common errors
```

Or use the official [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) library:

```bash
pip install skills-ref
skills-ref validate path/to/skill
```

**Workflows** — Things you do:

| Task | Resource |
|------|----------|
| Create a new skill from scratch | [workflows/create.md](workflows/create.md) |
| Test activation and behavior | [workflows/test.md](workflows/test.md) |
| Debug a skill that isn't working | [workflows/debug.md](workflows/debug.md) |
| Refine a skill from session learnings | [workflows/refine.md](workflows/refine.md) |

**References** — Things you look up:

| Topic | Resource |
|-------|----------|
| Official Agent Skills specification | [spec/specification.md](spec/specification.md) |
| Patterns: templates, routers, conditionals | [references/patterns.md](references/patterns.md) |
| Good and bad examples with analysis | [references/examples.md](references/examples.md) |
| Granular rules organized by impact | [references/rules.md](references/rules.md) |

**Spec** — Authoritative documentation from [agentskills.io](https://agentskills.io):

| Document | Description |
|----------|-------------|
| [spec/what-are-skills.md](spec/what-are-skills.md) | Conceptual overview |
| [spec/specification.md](spec/specification.md) | Format specification |
| [spec/skills-ref/](spec/skills-ref/) | Official validation library (vendored) |

## Source Material

The `sources/` directory contains complete skill-authoring approaches from different authors, preserved for deeper study:

| Source | Approach |
|--------|----------|
| `sources/anthropic/` | Official Anthropic skill-creator with init/package scripts |
| `sources/obra/` | TDD-based methodology with pressure testing |
| `sources/everyinc/` | Router patterns and workflow templates |
| `sources/pproenca/` | 46 granular rules organized by impact level |
| `sources/pytorch/` | Simple single-file approach |

## The Bottom Line

A skill is a teaching document. Its job is to make an agent smarter about something specific.

Write the description for discovery — use the words users say.
Write the body for understanding — orient, instruct, show, warn.
Structure for efficiency — keep the main file lean, push details to references.
Test for activation — a skill that never triggers provides zero value.

The best skills don't just tell the agent what to do. They give it enough understanding to adapt when the situation doesn't match the template exactly.
