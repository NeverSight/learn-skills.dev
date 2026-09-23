---
name: dev-skill-creator
description: "Create a new technology documentation skill for the dev-skills library. Use when adding a skill for a specific technology (e.g., bun, hono, react, prisma, stripe, rustfs) that links to official documentation and includes curated best practices. Handles three doc source types: llms.txt URL, GitHub repository, or documentation website. Each skill is thin and agent-agnostic: a triggering description + a live docs pointer + a small curated layer of evergreen gotchas."
---

# Dev Skill Creator

Creates technology documentation skills for the dev-skills library. Each skill is a thin, agent-agnostic wrapper: it points to official live documentation and adds a small curated layer of best practices — only what an agent would get wrong by default.

## Skill Structure

Every tech skill follows the same two-layer pattern:

1. **Live docs pointer** — link to always-fresh official documentation
2. **Curated best practices** — small set of evergreen gotchas not obvious from the docs

See `references/skill-template.md` for the canonical SKILL.md template to follow.

## Step 1: Identify the doc source type

Determine which source type applies before starting:

| Type | When to use | Example |
|------|-------------|---------|
| **llms.txt** | Technology publishes an `llms.txt` file | `https://bun.sh/llms.txt` |
| **GitHub repo** | No dedicated docs site; repo README/docs are the primary source | `https://github.com/rustfs/rustfs` |
| **Website** | Official docs site exists but no `llms.txt` | `https://docs.rustfs.com` |

If a technology has both a GitHub repo and a docs website, prefer the docs website. If it has an `llms.txt`, always prefer that.

## Step 2: Initialize the skill

```bash
python scripts/init_skill.py <technology-name> --path <output-directory>
```

Use the bare technology name in kebab-case: `bun`, `hono`, `react`, `better-auth`, `rustfs`. No `-docs` suffix.

## Step 3: Run an Explorer agent on the docs

Launch an Explorer agent with the brief matching the source type:

**For llms.txt:**
> "Read the documentation at [llms.txt URL]. Do NOT summarize it. Find: (1) built-in capabilities that developers commonly replace with npm/external packages unnecessarily, (2) patterns or APIs non-obvious to someone coming from a similar technology, (3) common mistakes or gotchas easy to miss and not prominently documented. Be specific and concrete."

**For GitHub repo:**
> "Explore the repository at [repo URL]. Read the README, any docs/ or documentation/ folder, and key example files. Do NOT summarize. Find: (1) capabilities non-obvious from the project name or category, (2) configuration or setup mistakes that are easy to make, (3) patterns the project recommends that differ from common assumptions. Be specific and concrete."

**For website:**
> "Browse the documentation at [docs URL]. Read the getting started guide and any architecture or concepts pages. Do NOT summarize. Find: (1) capabilities developers commonly miss or replace unnecessarily, (2) configuration gotchas not obvious from the overview, (3) recommended patterns that differ from what someone might assume coming from a similar tool. Be specific and concrete."

## Step 4: Curate the findings

Include a finding in the skill ONLY if it meets ALL three criteria:
- An agent would get it **wrong by default** without being told
- It is **not** prominently covered in the docs themselves
- It is **unlikely to go stale** (stable APIs, architectural decisions, security patterns)

Skip: things the docs explain clearly, opinions that vary by project, anything tied to a minor version.

## Step 5: Write the final skill

Follow the template in `references/skill-template.md`. Use the appropriate documentation section for the source type. The docs pointer covers reference material — the skill only adds what the docs don't.

## Step 6: Package

```bash
cd scripts/
python package_skill.py <path/to/skill-folder>
```

## Placement

Skills are agent-agnostic. Install the same skill folder into:
- `.claude/skills/` for Claude Code
- `.agents/skills/` for other agent types (Gemini, OpenAI, etc.)
