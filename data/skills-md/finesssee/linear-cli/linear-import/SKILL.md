---
name: linear-import
description: Import issues from CSV or JSON files. Use when bulk-creating issues from external data.
allowed-tools: Bash
---

# Import

```bash
# Import from CSV
linear-cli im csv issues.csv -t ENG

# Preview without creating (dry run)
linear-cli im csv issues.csv -t ENG --dry-run

# Import from JSON
linear-cli im json issues.json -t ENG

# JSON round-trip (export then re-import)
linear-cli exp json -t ENG -f backup.json
linear-cli im json backup.json -t ENG
```

## CSV Format

CSV files need a header row. Supported columns: `title`, `description`, `priority`, `status`, `assignee`, `labels`, `estimate`, `dueDate`.

Status, assignee, and labels are resolved by name automatically.

## JSON Format

JSON files should be an array of issue objects matching the export format.

## Flags

| Flag | Purpose |
|------|---------|
| `-t TEAM` | Target team (required) |
| `--dry-run` | Preview without creating |
| `--output json` | JSON output |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
