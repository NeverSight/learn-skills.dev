---
name: obsidian-master-skill
description: >-
  Comprehensive Obsidian vault management. USE WHEN obsidian, vault, note, daily note,
  PARA, inbox, knowledge capture, dataview, DQL, search vault, .base, bases, wikilink,
  frontmatter, second brain, markdown syntax, obsidian.nvim, OR obsidian API.
  Python-powered tools for search, creation, and vault health.
---

# obsidian-master-skill

Unified skill for all Obsidian vault operations — note creation, search, vault health, knowledge capture, bases, and daily notes. Uses progressive disclosure: essential rules below, deep reference in `reference/`.

## Directory Structure

```
obsidian-master-skill/
├── SKILL.md                          # This file (overview + quick reference)
├── reference/                        # Detailed documentation
│   ├── markdown.md                   # Obsidian Flavored Markdown syntax
│   ├── vault-organization.md         # PARA folders, frontmatter, Dataview
│   ├── rest-api.md                   # Local REST API, URI scheme, plugin API
│   ├── bases.md                      # .base YAML schema, filters, formulas
│   ├── integration-patterns.md       # Claude Code integration patterns
│   └── knowledge-capture.md          # ADR, concept, how-to, meeting templates
├── Workflows/                        # Step-by-step workflow definitions
│   ├── CreateNote.md                 # Create notes with templates + PARA placement
│   ├── SearchVault.md                # DQL, content search, tag filtering
│   ├── ManageVault.md                # Health checks, orphans, broken links
│   ├── CaptureKnowledge.md           # Extract insights from conversations
│   ├── CreateBase.md                 # Build .base database views
│   ├── DailyNote.md                  # Daily note creation/enhancement
│   ├── ProcessInbox.md               # Triage inbox into PARA folders
│   └── SyncDocs.md                   # Sync external project docs to vault
└── Tools/                            # Python CLI tools (click + httpx)
    ├── SearchVault.py                # status, auth, search (dataview|content|jsonlogic)
    ├── VaultManager.py               # health, orphans, broken-links, lifecycle, move, inbox
    ├── NoteCreator.py                # create, daily, capture
    └── BaseBuilder.py                # create, validate, preview
```

## Workflow Routing

| Intent | Workflow | Tool |
|--------|----------|------|
| Create a note (any type) | `Workflows/CreateNote.md` | `Tools/NoteCreator.py` |
| Search vault (DQL, content, tags) | `Workflows/SearchVault.md` | `Tools/SearchVault.py` |
| Vault health, orphans, broken links | `Workflows/ManageVault.md` | `Tools/VaultManager.py` |
| Extract knowledge from conversation | `Workflows/CaptureKnowledge.md` | `Tools/NoteCreator.py` |
| Create/edit .base database views | `Workflows/CreateBase.md` | `Tools/BaseBuilder.py` |
| Daily note create/enhance | `Workflows/DailyNote.md` | `Tools/NoteCreator.py` |
| Process inbox notes into PARA | `Workflows/ProcessInbox.md` | `Tools/VaultManager.py` |
| Sync project docs to vault | `Workflows/SyncDocs.md` | `Tools/VaultManager.py` |

## Quick Reference

### PARA Folder Map

| Folder | Purpose | Note Types |
|--------|---------|------------|
| `00 - Inbox/` | Quick capture, unsorted | Fleeting thoughts |
| `00 - Maps of Content/` | Index notes | MOCs, dashboards |
| `01 - Projects/` | Active projects | Project docs |
| `02 - Areas/` | Ongoing responsibilities | Area overviews |
| `03 - Resources/` | Reference materials | Evergreen notes |
| `04 - Archive/` | Completed/inactive | Archived projects |
| `04 - Permanent/` | Zettelkasten notes | Atomic ideas |
| `06 - Daily/` | Daily journal (YYYY/MM/YYYYMMDD.md) | Journal entries |
| `08 - books/` | Book notes | Reading notes |
| `10 - 1-1/` | Meeting notes | 1-on-1s |

> Deep dive: `reference/vault-organization.md`

### Frontmatter Schemas

**Standard Note:**
```yaml
---
created: YYYY-MM-DDTHH:mm
updated: YYYY-MM-DDTHH:mm
tags:
  - category/subcategory
---
```

**Daily Note (v2.0):**
```yaml
---
created: YYYY-MM-DDTHH:mm
updated: YYYY-MM-DDTHH:mm
title: YYYYMMDD
type: daily-note
status: true
tags:
  - daily
  - y/YYYY
  - y/YYYY-MM
aliases:
  - YYYY-MM-DD
date_formatted: YYYY-MM-DD
cssclasses:
  - daily
---
```

**Project Note:**
```yaml
---
created: YYYY-MM-DDTHH:mm
updated: YYYY-MM-DDTHH:mm
type: project
status: active | paused | complete
priority: high | medium | low
tags:
  - project/name
---
```

> Deep dive: `reference/vault-organization.md`

### Link Conventions

```markdown
[[Note Name]]                    # Wikilink
[[Note Name|Display Text]]       # Aliased link
[[Note Name#Heading]]            # Heading link
[[Note Name#^block-id]]          # Block reference
![[Note Name]]                   # Embed note
![[image.png]]                   # Embed image
![[image.png|300]]               # Embed with width
```

> Deep dive: `reference/markdown.md`

### Common Dataview Queries

```dataview
LIST FROM "06 - Daily" WHERE file.cday = date(today) SORT file.ctime DESC
```

```dataview
TABLE status, tags FROM "01 - Projects" WHERE status != "completed"
```

```dataview
TABLE WITHOUT ID file.link AS "Note", file.mtime AS "Modified"
FROM "03 - Resources" SORT file.mtime DESC LIMIT 20
```

```dataview
LIST FROM "" WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```

> Deep dive: `reference/vault-organization.md`

### Knowledge Capture Signals

| Signal in Conversation | Capture Type | Destination |
|----------------------|--------------|-------------|
| "We decided to..." | ADR | `03 - Resources/decisions/` |
| "What is X?" / "X works by..." | Concept | `04 - Permanent/` |
| "How do I..." / "Steps to..." | How-To | `03 - Resources/howtos/` |
| "In the meeting..." | Meeting Note | `10 - 1-1/` |
| "Track all notes about..." | MOC | `00 - Maps of Content/` |
| Quick insight or todo | Daily Append | `06 - Daily/YYYY/MM/YYYYMMDD.md` |

> Deep dive: `reference/knowledge-capture.md`

### Callout Types

```markdown
> [!note] Title
> Content

> [!tip]+ Expandable (default open)
> [!info]- Collapsed (default closed)
```

Types: `note`, `abstract/summary/tldr`, `info`, `todo`, `tip/hint/important`, `success/check/done`, `question/help/faq`, `warning/caution/attention`, `failure/fail/missing`, `danger/error`, `bug`, `example`, `quote/cite`

> Deep dive: `reference/markdown.md`

### REST API Quick Start

```bash
# Requires Local REST API plugin enabled in Obsidian
export OBSIDIAN_API_KEY="your-key"
export OBSIDIAN_BASE_URL="https://127.0.0.1:27124"

curl -H "Authorization: Bearer $OBSIDIAN_API_KEY" $OBSIDIAN_BASE_URL/vault/
```

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/vault/{path}` | GET/PUT/DELETE/PATCH | File CRUD |
| `/search/simple/` | POST | Text search |
| `/search/` | POST | Dataview query |
| `/search/jsonlogic/` | POST | Complex filtering |
| `/active/` | GET/PUT | Active file |
| `/commands/{id}` | POST | Execute command |

> Deep dive: `reference/rest-api.md`

### Base Files Quick Start

```yaml
# example.base — table of active projects
filters:
  and:
    - file.inFolder("01 - Projects")
    - 'status == "active"'
views:
  - type: table
    name: "Active Projects"
    order: [file.name, status, priority, due_date]
```

Embed: `![[example.base]]` or `![[example.base#View Name]]`

> Deep dive: `reference/bases.md`

## Tools (Python)

All tools use `click` CLI, `httpx` for REST API, `pyyaml` for frontmatter, `pathlib` for direct file access. Dual mode: REST API when Obsidian running, direct file fallback otherwise.

| Tool | Commands |
|------|----------|
| `Tools/SearchVault.py` | `status`, `auth`, `search --type dataview\|content\|jsonlogic` |
| `Tools/VaultManager.py` | `health`, `orphans`, `broken-links`, `lifecycle`, `move`, `inbox` |
| `Tools/NoteCreator.py` | `create`, `daily`, `capture` |
| `Tools/BaseBuilder.py` | `create`, `validate`, `preview` |

## Examples

```
"Create a new project note for API redesign"     -> Workflows/CreateNote.md
"Search my vault for notes about Kubernetes"      -> Workflows/SearchVault.md
"Find orphan notes and suggest connections"       -> Workflows/ManageVault.md
"Save what we just discussed as an ADR"           -> Workflows/CaptureKnowledge.md
"Create a base view of all active projects"       -> Workflows/CreateBase.md
"Create today's daily note"                       -> Workflows/DailyNote.md
"Process my inbox"                                -> Workflows/ProcessInbox.md
"What's the Obsidian markdown syntax for X?"      -> reference/markdown.md
"How do I use the REST API?"                      -> reference/rest-api.md
"How do bases formulas work?"                     -> reference/bases.md
```

## Neovim Reference

For obsidian.nvim configuration, see `reference/integration-patterns.md` section on Neovim integration.
