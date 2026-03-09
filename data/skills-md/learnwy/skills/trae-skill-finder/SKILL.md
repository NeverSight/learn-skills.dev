---
name: trae-skill-finder
description: "Discover and install skills for Trae IDE. Use when user asks 'find a skill', 'is there a skill for X', 'how do I do X'. Wraps find-skills with Trae-specific --agent flag."
priority: 100
requires:
  - find-skills
compatibility: "Trae IDE, Trae CN IDE"
---

# Trae Skill Finder

Wrapper for `find-skills`. Only adds `--agent` flag for Trae installation.

## What This Skill Does

1. Delegate ALL logic to `find-skills` (search, display, install prompts)
2. Only inject `--agent` flag when `find-skills` runs install command

## Agent Flag Injection

When `find-skills` would run:
```bash
npx skills add <package> -g -y
```

Change to:
```bash
# Trae CN (if ~/.trae-cn/ exists)
npx skills add <package> -a trae-cn -g -y

# Trae (if ~/.trae/ exists)  
npx skills add <package> -a trae -g -y
```

That's it. Everything else is handled by `find-skills`.

## Fallback

If NOT in Trae/Trae-CN environment → use `find-skills` directly without `-a` flag.
