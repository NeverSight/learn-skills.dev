---
name: convert
description: Convert .cast to .txt for Claude Code analysis. Supports batch mode. TRIGGERS - convert cast, cast to txt, batch convert, bulk convert, iTerm2 logs, prepare analysis.
allowed-tools: Bash, AskUserQuestion, Glob, Write
argument-hint: "[file] [-o output] [--batch] [--source dir] [--output-dir dir] [--skip-existing] [--index] [--analyze]"
---

# /asciinema-tools:convert

Convert asciinema .cast recordings to clean .txt files. Supports single file and batch directory modes.

## Arguments

### Single File Mode

| Argument       | Description                        |
| -------------- | ---------------------------------- |
| `file`         | Path to .cast file                 |
| `-o, --output` | Output path (default: same dir)    |
| `--index`      | Create timestamp indexed version   |
| `--chunks`     | Split at 30s+ idle pauses          |
| `--dims`       | Preserve terminal dimensions       |
| `--analyze`    | Auto-run /analyze after conversion |

### Batch Mode

| Argument          | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `--batch`         | Enable batch mode for directory conversion               |
| `--source`        | Source directory (default: ~/asciinemalogs)              |
| `--output-dir`    | Output directory (default: ~/Downloads/cast-txt/)        |
| `--skip-existing` | Skip files that already have .txt output (default: true) |

**Note**: `--batch` and positional `file` are mutually exclusive.

## Execution

Invoke the `asciinema-converter` skill with user-selected options.

### Single File Skip Logic

- If `file` provided → skip Phase 1 (file selection)
- If options provided → skip Phase 2 (options)
- If `-o` provided → skip Phase 3 (output location)
- If `--analyze` provided → skip Phase 6 and auto-run analyze

### Batch Mode Skip Logic

- If `--batch` provided → skip Phases 1-3, enter batch phases (7-10)
- If `--source` provided → skip Phase 7 (source selection)
- If `--output-dir` provided → skip Phase 8 (output organization)

### Single File Workflow

1. **Preflight**: Check asciinema convert command
2. **Discovery**: Find .cast files
3. **Selection**: AskUserQuestion for file
4. **Options**: AskUserQuestion for conversion options
5. **Location**: AskUserQuestion for output location
6. **Execute**: Run asciinema convert
7. **Report**: Display compression ratio
8. **Next**: AskUserQuestion for follow-up action

### Batch Workflow

1. **Preflight**: Check asciinema convert command
2. **Source**: AskUserQuestion for source directory
3. **Output**: AskUserQuestion for output directory
4. **Execute**: Batch convert with progress reporting
5. **Report**: Display aggregate compression stats
6. **Next**: AskUserQuestion for follow-up action

## Examples

```bash
# Single file conversion
/asciinema-tools:convert ~/Downloads/session.cast

# Batch mode with defaults
/asciinema-tools:convert --batch

# Batch mode with custom paths
/asciinema-tools:convert --batch --source ~/Downloads --output-dir ~/cast-txt/

# Batch mode, force re-convert existing
/asciinema-tools:convert --batch --skip-existing=false
```

## Troubleshooting

| Issue                  | Cause                   | Solution                            |
| ---------------------- | ----------------------- | ----------------------------------- |
| asciinema not found    | asciinema not installed | `brew install asciinema`            |
| Convert command failed | Corrupted .cast file    | Try `asciinema cat file.cast` first |
| No .cast files found   | Wrong directory         | Check --source path                 |
| Output not created     | Permission denied       | Check write permissions on output   |
| File too large         | Long recording session  | Use --chunks to split at pauses     |
