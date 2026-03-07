---
name: analyze
description: Semantic analysis of converted recordings. TRIGGERS - analyze cast, keyword extraction, find patterns.
allowed-tools: Bash, Grep, AskUserQuestion, Read
argument-hint: "[file] [-d domains] [-t type] [--json] [--md] [--density] [--jump]"
---

# /asciinema-tools:analyze

Run semantic analysis on converted .txt recordings.

## Arguments

| Argument        | Description                                |
| --------------- | ------------------------------------------ |
| `file`          | Path to .txt file                          |
| `-d, --domains` | Domains: `trading,ml,dev,claude`           |
| `-t, --type`    | Type: `curated`, `auto`, `full`, `density` |
| `--json`        | Output in JSON format                      |
| `--md`          | Save as markdown report                    |
| `--density`     | Include density analysis                   |
| `--jump`        | Jump to peak section after analysis        |

## Execution

Invoke the `asciinema-analyzer` skill with user-selected options.

### Skip Logic

- If `file` provided -> skip Phase 1 (file selection)
- If `-t` provided -> skip Phase 2 (analysis type)
- If `-d` provided -> skip Phase 3 (domain selection)
- If `--json/--md` provided -> skip Phase 6 (report format)
- If `--jump` provided -> auto-execute jump after analysis

### Workflow

1. **Preflight**: Check for .txt file
2. **Discovery**: Find .txt files
3. **Selection**: AskUserQuestion for file
4. **Type**: AskUserQuestion for analysis type
5. **Domain**: AskUserQuestion for domains (multi-select)
6. **Curated**: Run ripgrep searches
7. **Auto**: Run YAKE if selected
8. **Density**: Calculate density windows if selected
9. **Format**: AskUserQuestion for report format
10. **Next**: AskUserQuestion for follow-up action

## Examples

```bash
# Quick curated analysis for trading domain
/asciinema-tools:analyze session.txt -d trading -t curated

# Full analysis with density and JSON output
/asciinema-tools:analyze session.txt -t full --density --json

# Auto keyword discovery with markdown report
/asciinema-tools:analyze session.txt -t auto --md
```

## Troubleshooting

| Issue              | Cause                          | Solution                    |
| ------------------ | ------------------------------ | --------------------------- |
| ripgrep not found  | Not installed                  | `brew install ripgrep`      |
| YAKE not available | Python package missing         | `uv pip install yake`       |
| No keywords found  | Wrong domain or sparse content | Try `-t auto` for discovery |
