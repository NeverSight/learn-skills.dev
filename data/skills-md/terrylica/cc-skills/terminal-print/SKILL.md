---
name: terminal-print
description: Print iTerm2 terminal output to network printer. TRIGGERS - print terminal, terminal PDF, print session output.
allowed-tools: Bash, Read
---

# Terminal Print

Print terminal output from iTerm2 to your HP network printer with a single command.

## When to Use This Skill

Use this skill when:

- Printing terminal output to a network printer
- Creating PDF copies of command-line session output
- Archiving terminal logs in print-friendly format
- Sharing terminal output in meetings or documentation

## Quick Start

1. **Copy** terminal output in iTerm2 (Cmd+C)
2. **Invoke** this skill
3. **Review** PDF preview, press Enter to print

## How It Works

```
Clipboard → Strip ANSI → Markdown code block → pandoc/xelatex → PDF → Preview → Print
```

- **ANSI codes stripped**: Colors and escape sequences removed for clean B&W output
- **Monospace font**: DejaVu Sans Mono for proper character alignment
- **Landscape orientation**: Fits ~120 characters per line
- **US Letter paper**: Auto-detected from printer settings

## Execution

```bash
/usr/bin/env bash << 'PRINT_EOF'
SKILL_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/doc-tools}/skills/terminal-print"
bash "$SKILL_DIR/assets/print-terminal.sh"
PRINT_EOF
```

## Options

Run with arguments by modifying the execution block:

```bash
/usr/bin/env bash << 'PRINT_EOF'
SKILL_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/marketplaces/cc-skills/plugins/doc-tools}/skills/terminal-print"
bash "$SKILL_DIR/assets/print-terminal.sh" --no-preview
PRINT_EOF
```

| Flag           | Description                              |
| -------------- | ---------------------------------------- |
| `--file FILE`  | Read from file instead of clipboard      |
| `--no-preview` | Skip PDF preview, print directly         |
| `--no-print`   | Generate PDF only, don't send to printer |
| `-h, --help`   | Show help message                        |

## Examples

### Print from clipboard (default)

```bash
# Copy terminal output in iTerm2, then:
/usr/bin/env bash << 'EOF'
bash "${CLAUDE_PLUGIN_ROOT}/skills/terminal-print/assets/print-terminal.sh"
EOF
```

### Print from file

```bash
/usr/bin/env bash << 'EOF'
bash "${CLAUDE_PLUGIN_ROOT}/skills/terminal-print/assets/print-terminal.sh" --file ~/session.log
EOF
```

### Generate PDF only (no print)

```bash
/usr/bin/env bash << 'EOF'
bash "${CLAUDE_PLUGIN_ROOT}/skills/terminal-print/assets/print-terminal.sh" --no-print
EOF
```

## Prerequisites

All dependencies are already available on macOS with MacTeX:

| Tool      | Purpose          | Status            |
| --------- | ---------------- | ----------------- |
| `pandoc`  | Markdown to PDF  | Required          |
| `xelatex` | PDF engine       | Required (MacTeX) |
| `pbpaste` | Clipboard access | Built-in          |
| `lpr`     | CUPS printing    | Built-in          |

## Output

- **PDF location**: `/tmp/terminal-output-YYYYMMDD_HHMMSS.pdf`
- **Markdown source**: `/tmp/terminal-YYYYMMDD_HHMMSS.md`
- **Cleanup**: macOS automatically cleans `/tmp` periodically

## Troubleshooting

### "No text in clipboard"

Copy terminal output first using Cmd+C in iTerm2.

### "Missing pandoc" or "Missing xelatex"

Install MacTeX: `brew install --cask mactex`

### Printer not found

Check printer status: `lpstat -p -d`

The default printer is `HP_LaserJet_Pro_MFP_3101_3108`. Edit the script to change.

## Related Skills

- [pandoc-pdf-generation](../pandoc-pdf-generation/SKILL.md) - General Markdown to PDF conversion
- [asciinema-converter](../../../asciinema-tools/skills/asciinema-converter/SKILL.md) - Convert terminal recordings
