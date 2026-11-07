---
name: codesight-ai-context
description: Universal AI context generator that compiles codebase maps, wiki knowledge bases, and MCP tools to save thousands of tokens per AI conversation.
triggers:
  - "generate ai context for my project"
  - "save tokens in claude code cursor copilot"
  - "create codebase map for llm"
  - "set up codesight in my project"
  - "generate CLAUDE.md and cursorrules"
  - "create wiki knowledge base from codebase"
  - "reduce token usage in ai coding assistant"
  - "analyze my codebase for ai context"
---

# CodeSight — AI Context Generator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CodeSight compiles your codebase into a compact, structured context map (routes, models, components, dependencies) that AI coding assistants can read in one shot — eliminating thousands of tokens spent on manual file exploration. Supports 14 languages, 30+ frameworks, 13 ORM parsers, and an MCP server with 13 tools.

## Installation

No installation required. Run directly with `npx`:

```bash
npx codesight
```

Or install globally:

```bash
npm install -g codesight
codesight
```

**Requirements:** Node.js >= 18, no API keys, no config files needed.

## Core Commands

```bash
# Generate context map (default — outputs .codesight/CODESIGHT.md)
npx codesight

# Generate persistent wiki knowledge base (.codesight/wiki/)
npx codesight --wiki

# Generate AI tool config files (CLAUDE.md, .cursorrules, codex.md, AGENTS.md)
npx codesight --init

# Open interactive HTML report in browser
npx codesight --open

# Start as MCP server (13 tools) for Claude Code / Cursor
npx codesight --mcp

# Show blast radius for a specific file
npx codesight --blast src/lib/db.ts

# Generate optimized config for a specific AI tool
npx codesight --profile claude-code
npx codesight --profile cursor
npx codesight --profile copilot
npx codesight --profile codex

# Show token savings breakdown
npx codesight --benchmark

# Map markdown knowledge base (ADRs, meeting notes, Obsidian vault)
npx codesight --mode knowledge
npx codesight --mode knowledge ~/vault
npx codesight --mode knowledge ./docs

# Watch mode — regenerate on file changes
npx codesight --watch

# Git hook — regenerate on every commit
npx codesight --hook
```

## What Gets Generated

### Default Scan (`npx codesight`)

Outputs `.codesight/CODESIGHT.md` — a structured map including:
- Project metadata (stack, language, framework, package manager)
- All routes with HTTP methods and handler locations
- Database models with fields and relations
- UI components with props
- High-impact files ranked by dependency count
- Framework and ORM detection results

### Wiki Knowledge Base (`--wiki`)

Outputs `.codesight/wiki/` directory:

```
.codesight/wiki/
  index.md      — catalog of all articles (~200 tokens)
  overview.md   — architecture, subsystems, high-impact files
  auth.md       — auth routes, middleware, session flow
  payments.md   — payment routes, webhook handling, billing flow
  database.md   — all models, fields, relations
  users.md      — user management routes and models
  ui.md         — UI components with props
  log.md        — append-only operation log
```

### AI Tool Config Files (`--init`)

Generates project-root files for each AI tool:
- `CLAUDE.md` — Claude Code project instructions
- `.cursorrules` — Cursor rules file
- `codex.md` — OpenAI Codex context
- `AGENTS.md` — general agent instructions

## MCP Server Mode

Start CodeSight as an MCP server to give Claude Code or Cursor direct tool access:

```bash
npx codesight --mcp
```

### MCP Tool Reference

| Tool | Description |
|---|---|
| `codesight_get_context` | Full codebase context map |
| `codesight_get_routes` | All API routes with methods and handlers |
| `codesight_get_models` | All database models and schema |
| `codesight_get_components` | UI components with props |
| `codesight_get_blast_radius` | Impact analysis for a specific file |
| `codesight_get_high_impact_files` | Files ranked by dependency count |
| `codesight_get_framework_info` | Detected frameworks and ORMs |
| `codesight_get_wiki_index` | Wiki catalog (~200 tokens) for session start |
| `codesight_get_wiki_article` | Read one wiki article by name |
| `codesight_lint_wiki` | Wiki health check (orphans, stale, missing links) |
| `codesight_get_knowledge` | Knowledge map from markdown notes |
| `codesight_benchmark` | Token savings analysis |
| `codesight_get_overview` | Project overview summary |

### Configuring MCP in Claude Code

Add to your Claude Code MCP config (`~/.claude/mcp_settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "codesight": {
      "command": "npx",
      "args": ["codesight", "--mcp"],
      "cwd": "/path/to/your/project"
    }
  }
}
```

### Configuring MCP in Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "codesight": {
      "command": "npx",
      "args": ["codesight", "--mcp"]
    }
  }
}
```

## Language & Framework Support

| Language | AST Precision | Frameworks Detected |
|---|---|---|
| TypeScript | ✅ Full AST | Next.js, NestJS, Hono, Remix, SvelteKit, Nuxt, Express, Fastify |
| JavaScript | Regex | Express, Fastify, Koa, Hapi |
| Python | Regex | Django, FastAPI, Flask, SQLAlchemy |
| Go | Regex | Gin, Echo, Fiber, Chi |
| Ruby | Regex | Rails, Sinatra |
| PHP | Regex | Laravel, Symfony |
| Elixir | Regex | Phoenix |
| Java | Regex | Spring Boot |
| Kotlin | Regex | Ktor, Spring Boot |
| Rust | Regex | Axum, Actix |
| Dart | Regex | Flutter |
| Swift | Regex | Vapor |
| C# | Regex | ASP.NET Core |

## ORM / Database Support

Drizzle, Prisma, TypeORM, Sequelize, Mongoose, MikroORM, SQLAlchemy, Django ORM, ActiveRecord, Eloquent, Ecto, GORM, and more (13 total).

## Real Usage Patterns

### Pattern 1: Session Start with Wiki

At the beginning of every AI session, load the wiki index instead of the full context map:

```
# In Claude Code or Cursor, at session start:
Use codesight_get_wiki_index to get project overview, 
then codesight_get_wiki_article for "auth" to understand authentication.
```

### Pattern 2: Blast Radius Before Refactoring

Before modifying a shared file, check what breaks:

```bash
npx codesight --blast src/lib/database.ts
```

Output shows every file that imports the target, ranked by impact — critical before refactoring database connections, shared utilities, or types.

### Pattern 3: CI/CD Integration

Keep context fresh on every push:

```yaml
# .github/workflows/codesight.yml
name: Update AI Context
on:
  push:
    branches: [main]

jobs:
  update-context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Generate context map
        run: npx codesight
      - name: Generate wiki
        run: npx codesight --wiki
      - name: Generate knowledge map
        run: npx codesight --mode knowledge ./docs
      - name: Commit updated context
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .codesight/
          git diff --staged --quiet || git commit -m "chore: update AI context [skip ci]"
          git push
```

### Pattern 4: Git Hook for Local Freshness

```bash
npx codesight --hook
```

This installs a post-commit hook that regenerates `.codesight/CODESIGHT.md` automatically after every commit.

### Pattern 5: Knowledge Mapping for Decision Records

```bash
# Map ADRs and architecture docs
npx codesight --mode knowledge ./docs/decisions

# Map full Obsidian vault
npx codesight --mode knowledge ~/vault

# Outputs .codesight/KNOWLEDGE.md with:
# - Key decisions extracted from ADR files
# - Open questions surfaced from notes
# - Meeting notes indexed by date
# - Specs and PRDs cataloged
```

## Consuming the Output in AI Sessions

### Loading Context in Claude Code (manual)

```
Read .codesight/CODESIGHT.md for project context before answering questions.
```

### Loading Wiki at Session Start

```
Read .codesight/wiki/index.md first. 
Then read the relevant article (e.g. .codesight/wiki/auth.md) 
only when questions about that domain arise.
```

### Loading Combined Context

```
Read .codesight/CODESIGHT.md for code structure and 
.codesight/KNOWLEDGE.md for architectural decisions.
```

## Token Savings Reference

| Approach | Tokens per session | Savings vs baseline |
|---|---|---|
| Manual file exploration | 26K–47K | baseline |
| `npx codesight` (context map) | 3K–5K | **7x–12x** |
| `--wiki` targeted article | ~200 + ~300/question | **60x–130x** |

Real benchmark results from production codebases:

| Project | Stack | Files | Output Tokens | Exploration Tokens | Savings |
|---|---|---|---|---|---|
| SaaS A | Hono + Drizzle | 138 | 3,936 | 46,020 | **11.7x** |
| SaaS B | Hono + Drizzle (monorepo) | 53 | 3,629 | 26,130 | **7.2x** |
| SaaS C | FastAPI + MongoDB | 40 | 4,162 | 47,450 | **11.4x** |
| Rails app | Rails + ActiveRecord | 4,172 | 21,711 | 386,100 | **17.8x** |
| Laravel app | Laravel + Eloquent | 3,896 | 30,739 | 493,285 | **16x** |

## .codesight Directory Structure

```
.codesight/
  CODESIGHT.md       — main context map (commit this)
  KNOWLEDGE.md       — knowledge/decision map (commit this)
  wiki/
    index.md         — wiki catalog (commit this)
    overview.md
    auth.md
    database.md
    payments.md
    users.md
    ui.md
    log.md
```

Add `.codesight/` to git to persist context across sessions and team members. The wiki survives session restarts — every new conversation starts with full codebase knowledge from the first message.

## Troubleshooting

**Routes not detected:**
- Ensure you're running from the project root (where `package.json` or equivalent lives)
- TypeScript projects get full AST parsing; other languages use regex — check that route files follow standard framework conventions
- For Python FastAPI, ensure router files use standard `@app.get()` / `@router.post()` decorators

**Models showing 0 for MongoDB:**
- This is correct behavior — codesight parses SQL ORM declarations. MongoDB collections without Mongoose schemas won't appear. Define Mongoose schemas explicitly to get model detection.

**Wiki articles missing:**
- Run `npx codesight --wiki` first to generate the wiki directory
- Use `codesight_lint_wiki` MCP tool or check `.codesight/wiki/log.md` for generation errors

**Large monorepos (10K+ files) are slow:**
- Add a `.codesightignore` file (same syntax as `.gitignore`) to exclude build artifacts, generated files, and `node_modules` subdirectories
- Typical scan time: 186ms–890ms for projects under 5K files

**MCP server not connecting:**
- Verify Node.js >= 18: `node --version`
- Check `cwd` in MCP config points to the actual project root
- Run `npx codesight --mcp` manually first to confirm it starts without errors

**`--init` overwrites existing CLAUDE.md:**
- Back up existing files before running `--init` on a project with custom AI instructions
- Generated files are additive starting points — merge with your existing content manually
