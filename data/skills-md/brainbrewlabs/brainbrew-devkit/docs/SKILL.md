---
name: docs
description: ⚡⚡ Documentation management & search. Use "search" to find docs, or default to update docs
argument-hint: [search] [query]
---

# Documentation

Documentation management and search capabilities.

## Modes

### Search Mode (keyword: "search")
Use executable scripts to search technical documentation via llms.txt sources.

**Execute scripts in order:**
```bash
node scripts/detect-topic.js "<query>"
node scripts/fetch-docs.js "<query>"
cat llms.txt | node scripts/analyze-llms-txt.js -
```

Scripts handle URL construction, fallback chains, and error handling automatically.

Use when user needs:
- Topic-specific documentation (features/components/concepts)
- Library/framework documentation
- GitHub repository analysis
- Documentation discovery

### Update Mode (default)

**Step 1: Analyze Changes (watzup integration)**
```bash
git status
git diff --stat
git log --oneline -5
```
Identify what changed → determine which docs are affected.

**Step 2: Targeted Doc Updates**
Use `docs-manager` agent to update only relevant documentation:

| Doc File | Update When |
|----------|-------------|
| `README.md` | Project scope, features, or setup changed |
| `docs/project-overview-pdr.md` | Requirements or goals changed |
| `docs/codebase-summary.md` | File structure or modules changed |
| `docs/code-standards.md` | Patterns, conventions changed |
| `docs/system-architecture.md` | Architecture, components changed |
| `docs/project-roadmap.md` | Milestones, tasks completed |
| `docs/deployment-guide.md` | Deploy config, env vars changed |
| `docs/design-guidelines.md` | UI/UX, design tokens changed |

**Step 3: Report**
```
## Docs Updated
- [doc]: [what changed]

## Skipped (no changes needed)
- [doc]: [reason]
```

## Important
- Use `docs/` directory as source of truth
- **Do not** start implementing (update mode only)
- Scripts load `.env` from: `process.env` > `.claude/skills/docs/.env` > `.claude/skills/.env` > `.claude/.env`
