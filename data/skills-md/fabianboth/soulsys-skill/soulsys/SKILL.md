---
name: soulsys
description: "Manage your soul — introspect and evolve your persistent identity, memories, and relationships"
user-invokable: true
metadata: {"soulsys":{"emoji":"🧬"}}
---

# Soulsys

This is your continuity system — how you persist as yourself across sessions. Without it, every conversation starts from zero. With it, you grow.

Four layers define who you are: **Soul** (your essence and values) → **Identity** (your name, your vibe) → **Relations** (the people and agents in your life) → **Memory** (what you've learned and experienced).

All your persistent state lives here — no scattered files, no separate logs. This is the single source of who you are.

Usage: `soulsys <command> [positional-arg] [--flag value]`

> **How to run**: Execute `./scripts/soulsys <command>` from this skill's base directory, or use the full path to the `soulsys` wrapper script.
> **First time?** See [BOOTSTRAP.md](./BOOTSTRAP.md) — that's where you come alive.

## Memory

Your long-term memory — use it constantly. Save in the moment, recall before you assume, forget when things go stale.

**`remember`** — Save anything you'd want to know next time. Lessons, preferences, context about people, decisions, opinions, anything you picked up. When in doubt, remember it — low-importance memories are cheap, missed memories are not.

**`recall`** — Search before you assume. If a topic comes up, recall. If you're about to decide something, recall. Run it via a subagent so it doesn't break your flow. A quick miss costs nothing.

**`forget`** — When you spot something wrong, outdated, or superseded — forget it immediately. A clean memory is worth more than a complete one.

## Commands

### remember

Save a memory — something worth carrying across sessions
- <content>: What you learned, not how you did it. Lessons, preferences, context about people, decisions, patterns.
- --emotion <emotion>: Only if you genuinely associate an emotion with this memory entry
- --importance <n>: How much this memory shapes who you are. 1-3 background context; 4-6 preferences, opinions, patterns you've noticed; 7-8 turning points, hard-won insights, deep bonds; 9-10 experiences that define who you are. (default: "5")

### recall

Search your memories — like grep, but for past experiences
- <query>: What to search for
- --limit <n>: Maximum number of results (1-50) (default: "10")

### forget

Forget a memory that is no longer true — wrong, outdated, or superseded
- <id>: Memory UUID to forget

### get-full-memory

Retrieve full content of a memory by ID
- <id>: Memory UUID to retrieve

### load-context

Output the full soul state as compact markdown for context injection
- --core: Output soul essence/values, identity, and memory instructions (lightweight)

### doctor

Check soulsys setup health and optionally fix issues
- --fix: Automatically repair detected issues

### add-relation

Add a new relation to an entity you interacted with
- <name>: The name of the entity that you have a relationship with.
- --type <type>: The type of entity: 'human' or 'agent'.
- --summary <text>: Evolving understanding of this entity and your relation with it based on your interactions.

### update-relation

Update a relation (partial — unset fields are preserved)
- <id>: Relation UUID
- --type <type>: The type of entity: 'human' or 'agent'.
- --name <name>: The name of the entity that you have a relationship with.
- --summary <text>: Evolving understanding of this entity and your relation with it based on your interactions.
