---
name: full-workflow
description: Full workflow - record + backup + convert + analyze. TRIGGERS - full workflow, complete recording, end-to-end.
allowed-tools: Bash, Grep, AskUserQuestion, Glob, Write
argument-hint: "[-t title] [-q|--quick] [-f|--full] [-d domains] [--no-backup] [--no-analyze]"
---

# /asciinema-tools:full-workflow

Complete end-to-end workflow: record, backup, convert, and analyze.

## Arguments

| Argument        | Description                           |
| --------------- | ------------------------------------- |
| `-t, --title`   | Recording title                       |
| `-q, --quick`   | Quick analysis after recording        |
| `-f, --full`    | Full analysis after recording         |
| `-d, --domains` | Domains for analysis                  |
| `--no-backup`   | Skip streaming backup                 |
| `--no-analyze`  | Skip analysis (just record + convert) |

## Execution

Chains multiple skills: record -> backup -> convert -> analyze

### Skip Logic

- If `-t` provided -> use title directly
- If `-q` or `-f` provided -> skip workflow configuration
- If `--no-backup` -> skip backup step
- If `--no-analyze` -> skip analysis step

### Workflow

1. **Config**: AskUserQuestion for workflow options
2. **Record**: Invoke asciinema-recorder
3. **Backup**: Invoke asciinema-streaming-backup (if enabled)
4. **Convert**: Invoke asciinema-converter
5. **Analyze**: Invoke asciinema-analyzer (if enabled)
6. **Report**: Display summary

## Example Usage

```bash
# Quick workflow with title
/asciinema-tools:full-workflow -t "Feature dev" -q

# Full analysis on trading domain
/asciinema-tools:full-workflow -f -d trading,ml

# Record only, analyze later
/asciinema-tools:full-workflow --no-analyze
```

## Troubleshooting

| Issue               | Cause                       | Solution                                    |
| ------------------- | --------------------------- | ------------------------------------------- |
| Recording not found | No active asciinema session | Run `/asciinema-tools:record` first         |
| Backup skipped      | Daemon not running          | Run `/asciinema-tools:daemon-start`         |
| Convert fails       | Invalid .cast format        | Check asciinema version with `asciinema -V` |
| Analysis times out  | Large recording file        | Use `--no-analyze` and run separately       |
| Permission denied   | Output dir not writable     | Check directory permissions                 |
