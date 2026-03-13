---
name: tools-mdbase
description: This skill should be used when the user asks to "validate my collection", "query markdown files", "create mdbase type", "mdbase schema", "init mdbase", "mdbase validate", "mdbase query", or mentions mdbase, typed markdown collections, or frontmatter schemas.
---

# mdbase

Work with mdbase collections: typed, queryable markdown file databases with YAML frontmatter schemas.

## Monorepo vault setup

This vault is configured as an mdbase collection:

- Config: `./mdbase.yaml`
- Types: `./90-system/_types/`
- Schema docs: `./90-system/docs/mdbase-schema.md`

### Available types

| Namespace | Types |
|-----------|-------|
| journals-* | `journals-daily`, `journals-weekly`, `journals-quarterly`, `journals-yearly` |
| zettel-* | `zettel-source`, `zettel-publication`, `zettel-idea`, `zettel-fleeting` |
| entity-* | `entity-person`, `entity-organization` |
| para-* | `para-project`, `para-area`, `para-resource`, `para-task` |
| misc-* | `misc-software`, `misc-workflow`, and any ad-hoc types |

### Type matching

All types use `global-type` field for matching:

```yaml
global-type: zettel-source
```

Duck-typing fallback available for migration (e.g., files with `source-url` + `source-title` match `zettel-source`).

## CLI usage

Run from monorepo root:

```bash
# Run from repo root
npx mdbase <command> [options]
```

### Create notes

```bash
# Create a source note
npx mdbase create --type zettel-source

# Create with fields
npx mdbase create --type zettel-source \
  --source-title "Article Title" \
  --source-url "https://example.com" \
  --zettel-status drafted

# Create a task
npx mdbase create --type para-task \
  --para-status todo \
  --para-priority p2

# Create a project
npx mdbase create --type para-project \
  --para-status active \
  --para-area "[[Career]]"

# Create a person entity
npx mdbase create --type entity-person \
  --entity-name "Jane Doe"

# Create a publication
npx mdbase create --type zettel-publication \
  --pub-title "Episode Title" \
  --pub-type podcast \
  --zettel-status drafted
```

### Query notes

```bash
# All active projects
npx mdbase query "global-type = para-project AND para-status = active"

# Unreviewed sources
npx mdbase query "global-type = zettel-source AND zettel-status = drafted"

# Tasks by priority
npx mdbase query "global-type = para-task AND para-priority = p1"

# Overdue tasks
npx mdbase query "global-type = para-task AND para-due-date < 2026-02-06"

# YouTube sources
npx mdbase query "source-platform = youtube" --types zettel-source

# Projects sorted by deadline
npx mdbase query "para-status = active" --types para-project --sort para-deadline

# Limit results
npx mdbase query "global-type = zettel-source" --limit 10 --sort "-source-fetched-date"
```

### Validate

```bash
# Validate entire vault
npx mdbase validate .

# Validate specific folder
npx mdbase validate 20-zettel/
npx mdbase validate 30-para/

# Validate single file
npx mdbase validate 30-para/31-projects/example-project.md
```

### Update notes

```bash
# Mark source as reviewed
npx mdbase update 20-zettel/sources/article.md --set "zettel-status=reviewed"

# Complete a task
npx mdbase update 30-para/tasks/my-task.md --set "para-status=completed"

# Update project deadline
npx mdbase update 30-para/31-projects/project.md --set "para-deadline=2026-03-01"
```

### Read and inspect

```bash
# Read a file
npx mdbase read 30-para/31-projects/example-project.md

# Get vault statistics
npx mdbase stats .

# Visualize links
npx mdbase links . --format dot > graph.dot
```

### Export and import

```bash
# Export projects to CSV
npx mdbase export . --type para-project --format csv -o projects.csv

# Export sources to JSON
npx mdbase export . --type zettel-source --format json -o sources.json

# Import tasks from CSV
npx mdbase import tasks.csv --type para-task
```

### Rename with link updates

```bash
# Rename file and update all [[wikilinks]]
npx mdbase rename old-name.md new-name.md
```

### Run Obsidian bases

```bash
# Execute a .base query file
npx mdbase base run 90-system/bases/zettel-sources.base
npx mdbase base run 90-system/bases/para-tasks.base
```

## Adding new types

### Quick ad-hoc type

1. Use `misc-*` prefix in frontmatter:
```yaml
global-type: misc-recipe
```

2. No schema needed initially - mdbase allows unknown types

### Formal type definition

Create `90-system/_types/misc-example.md`:

```yaml
---
name: misc-example
matchFields: [global-type]
fields:
  global-type:
    type: enum
    values: [misc-example]
    required: true
  custom-field:
    type: string
    required: false
---

# misc-example

Description of when to use this type.
```

## Common workflows

### Process inbox item

```bash
# Query inbox items (untyped files in 00-inbox)
ls 00-inbox/

# Create typed note from inbox content
npx mdbase create --type zettel-source --source-title "..." --source-url "..."

# Or create task
npx mdbase create --type para-task --para-status todo
```

### Weekly review queries

```bash
# Unreviewed sources
npx mdbase query "zettel-status = drafted" --types zettel-source

# Active projects
npx mdbase query "para-status = active" --types para-project

# Todo tasks
npx mdbase query "para-status = todo" --types para-task --sort para-priority

# Orphan ideas (no sources linked)
npx mdbase query "zettel-sources = []" --types zettel-idea
```

### Bulk operations

```bash
# Archive old drafted sources
npx mdbase query "zettel-status = drafted AND source-fetched-date < 2025-01-01" \
  --types zettel-source --format paths | \
  xargs -I {} npx mdbase update {} --set "zettel-status=archived"
```

## Troubleshooting

### Node.js version

mdbase-cli requires Node.js 22+:

```bash
node --version
```

### Validation errors

Check:
1. Valid YAML frontmatter (between `---` markers)
2. Required fields present for the type
3. Enum values match allowed values
4. Date format is YYYY-MM-DD

### Type not matching

1. Verify `global-type` field value matches type name exactly
2. Check `90-system/_types/` for valid type names
3. For duck-typing, ensure characteristic fields are present

## References

- Schema docs: `90-system/docs/mdbase-schema.md`
- Type definitions: `90-system/_types/`
- Obsidian bases: `90-system/bases/`
- mdbase spec: https://github.com/callumalpass/mdbase-spec
- mdbase CLI: https://github.com/callumalpass/mdbase-cli
