---
name: brain
description: Search and manage your second brain knowledge base. Use when the user asks about their notes, wants to find information, or needs to add/organize knowledge. Also use proactively before research, brainstorming, or planning tasks to pull relevant prior work, and after completing research or making decisions to deposit findings.
---

# Brain — Knowledge Management

A CLI for managing a developer second brain with hybrid BM25 + vector search over markdown notes.

## When to Use

- User asks "what do I know about X" or "find my notes on Y"
- User wants to save something to their knowledge base
- Before starting work on a topic (context pull)
- After completing research or making a decision (deposit)
- User asks about stale or outdated notes

## Commands

All commands are run via `brain` (ensure it's on PATH or use the full path to the CLI).
Use `--json` flag on all commands when processing output programmatically.

### Search

```bash
brain search "<query>" [options]
  --json                    JSON output
  --limit <n>               Max results (default 10)
  --min-score <score>       Minimum relevance 0-1 (use 0.4 for broad queries)
  --category <cat>          Filter by project category
  --tier <tier>             slow|fast
  --tags <tags>             Comma-separated tag filter
  --confidence <level>      high|medium|low|speculative
  --since <date>            Notes modified after YYYY-MM-DD
  --expand                  Include graph-connected notes
```

### Add Notes

```bash
brain add <file> [options]
  --title <title>               Note title
  --type <type>                 note|decision|pattern|research|meeting|session-log|guide
  --tier <tier>                 slow|fast (default: slow)
  --tags <tags>                 Comma-separated tags
  --summary <text>              One-line summary for search excerpts
  --confidence <level>          high|medium|low|speculative
  --status <status>             current|outdated|deprecated|draft
  --category <cat>              Project category
  --related <ids>               Comma-separated related note IDs
  --review-interval <interval>  e.g. 30d, 60d, 90d, 180d
  --created <date>              YYYY-MM-DD (defaults to today)
```

### Other

| Command | Purpose |
|---------|---------|
| `brain status --json` | Database stats (note count, embeddings, types) |
| `brain stale --json` | Notes past their review interval |
| `brain graph <note-id> --json` | Show note's connections |
| `brain index` | Rebuild search index (slow — only when asked) |
| `brain template <type>` | Generate frontmatter template for a note type |

## Quality Rules

When **adding** notes:
- ALWAYS include `--category`, `--tags` (2-3 minimum), and `--summary`
- Include `--related` when the note references existing notes
- Set `--confidence` to signal how proven the content is
- Set `--review-interval` by type: decisions=180d, research=90d, patterns=60d, guides=90d

When **searching**:
- Use `--category` to scope queries to the relevant project
- Use `--min-score 0.4` to filter noise on broad queries
- Use `--expand` when you need the full context graph around a result

## Workflow Patterns

**Context pull** — before planning or brainstorming:
```bash
brain search "topic" --category mobile --min-score 0.4 --expand --json
```

**Research deposit** — after completing research:
```bash
brain add research.md --title "Finding title" --type research \
  --category voltra-sdk --tags "ble,protocol" --confidence medium \
  --summary "One-line finding" --review-interval 90d
```

**Decision record** — after an architectural decision:
```bash
brain add decision.md --title "Use X over Y" --type decision \
  --category mobile --tags "architecture,state" --confidence high \
  --summary "Chose X because..." --review-interval 180d --related existing-note-id
```

## Rules

- Always use `--json` when you need to parse output
- Search before claiming information isn't in the knowledge base
- Do NOT run `brain index` unless the user explicitly asks — it processes all files and is slow
- Present search results with score, file path, and excerpt
