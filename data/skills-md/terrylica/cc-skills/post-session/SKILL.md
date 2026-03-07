---
name: post-session
description: Complete post-session workflow - finalize orphaned recordings, convert, and AI summarize. TRIGGERS - post session, analyze recording, session review, complete workflow.
allowed-tools: Bash, Grep, AskUserQuestion, Glob, Write, Read, Task
argument-hint: "[file] [--finalize] [-q|--quick] [-f|--full] [--summarize] [--output file]"
---

# /asciinema-tools:post-session

Complete post-session workflow: finalize orphaned recordings → convert to text → AI-powered summarize.

## Arguments

| Argument      | Description                                      |
| ------------- | ------------------------------------------------ |
| `file`        | Path to .cast file (or auto-detect)              |
| `--finalize`  | Include finalize step (stop processes, compress) |
| `-q, --quick` | Quick analysis (keyword grep + brief summary)    |
| `-f, --full`  | Full analysis (convert + AI deep-dive summarize) |
| `--summarize` | Include AI summarize step (iterative deep-dive)  |
| `--output`    | Save findings to markdown file                   |

## Workflow Modes

### Quick Mode (`-q`)

```
[file] → convert → keyword grep → brief summary
```

### Full Mode (`-f`)

```
[file] → convert → AI summarize (iterative deep-dive)
```

### Complete Mode (`--finalize --full`)

```
stop processes → compress → push → convert → AI summarize
```

## Execution

### Phase 1: Discovery

```yaml
AskUserQuestion:
  question: "What would you like to do?"
  header: "Workflow"
  options:
    - label: "Quick analysis (Recommended)"
      description: "Convert + keyword search + brief summary"
    - label: "Full AI analysis"
      description: "Convert + iterative AI deep-dive with guidance"
    - label: "Complete workflow"
      description: "Finalize orphans + convert + AI summarize"
    - label: "Finalize only"
      description: "Stop processes and push to orphan branch"
```

### Phase 2: File Selection

If no file specified, discover available recordings:

```bash
/usr/bin/env bash << 'DISCOVER_EOF'
echo "=== Running asciinema processes ==="
ps aux | grep -E "asciinema rec" | grep -v grep | while read -r line; do
  PID=$(echo "$line" | awk '{print $2}')
  CAST=$(echo "$line" | grep -oE '[^ ]+\.cast' | head -1)
  if [[ -n "$CAST" ]]; then
    SIZE=$(ls -lh "$CAST" 2>/dev/null | awk '{print $5}' || echo "?")
    echo "  [RUNNING] PID $PID: $CAST ($SIZE)"
  fi
done

echo ""
echo "=== Recent .cast files ==="
find ~/eon -name "*.cast" -size +1M -mtime -7 2>/dev/null | while read -r f; do
  SIZE=$(ls -lh "$f" | awk '{print $5}')
  MTIME=$(stat -f "%Sm" -t "%m-%d %H:%M" "$f" 2>/dev/null)
  echo "  $f ($SIZE, $MTIME)"
done | head -10

echo ""
echo "=== Recent .txt files (already converted) ==="
find ~/eon -name "*.txt" -size +100M -mtime -7 2>/dev/null | while read -r f; do
  SIZE=$(ls -lh "$f" | awk '{print $5}')
  echo "  $f ($SIZE)"
done | head -5
DISCOVER_EOF
```

```yaml
AskUserQuestion:
  question: "Which recording to analyze?"
  header: "Select"
  options:
    # Dynamically populated from discovery
    - label: "{filename} ({size})"
      description: "{path}"
```

### Phase 3: Finalize (if selected)

Chain to `/asciinema-tools:finalize`:

1. Stop running asciinema processes
2. Verify file integrity
3. Compress with zstd
4. Push to orphan branch

### Phase 4: Convert

```bash
/usr/bin/env bash << 'CONVERT_EOF'
CAST_FILE="$1"
TXT_FILE="${CAST_FILE%.cast}.txt"

echo "Converting: $CAST_FILE"
echo "Output: $TXT_FILE"

if asciinema convert -f txt "$CAST_FILE" "$TXT_FILE"; then
  ORIG=$(ls -lh "$CAST_FILE" | awk '{print $5}')
  CONV=$(ls -lh "$TXT_FILE" | awk '{print $5}')
  echo "✓ Converted: $ORIG → $CONV"
else
  echo "✗ Conversion failed"
  exit 1
fi
CONVERT_EOF
```

### Phase 5: Analysis

**Quick mode**: Keyword grep + brief summary

```bash
# Run curated keyword searches
grep -c -i "error\|fail\|exception" "$TXT_FILE"
grep -c -i "success\|complete\|done" "$TXT_FILE"
grep -c -i "sharpe\|drawdown\|backtest" "$TXT_FILE"
# ... summarize counts
```

**Full mode**: Chain to `/asciinema-tools:summarize`

- Initial guidance via AskUserQuestion
- Strategic sampling (head/middle/tail)
- Iterative deep-dive with user guidance
- Synthesis into findings report

### Phase 6: Output

```yaml
AskUserQuestion:
  question: "Analysis complete. What next?"
  header: "Output"
  options:
    - label: "Display summary"
      description: "Show findings in terminal"
    - label: "Save to markdown"
      description: "Write findings to {filename}_findings.md"
    - label: "Continue exploring"
      description: "Deep-dive into specific sections"
    - label: "Done"
      description: "Exit workflow"
```

## Example Usage

```bash
# Interactive mode - auto-detect and guide
/asciinema-tools:post-session

# Quick analysis on specific file
/asciinema-tools:post-session session.cast -q

# Full AI analysis with output
/asciinema-tools:post-session session.cast -f --output findings.md

# Complete workflow including finalize
/asciinema-tools:post-session --finalize -f
```

## Related Commands

- `/asciinema-tools:daemon-status` - View status and find unhandled files
- `/asciinema-tools:finalize` - Finalize orphaned recordings
- `/asciinema-tools:convert` - Convert .cast to .txt
- `/asciinema-tools:summarize` - AI-powered deep analysis
- `/asciinema-tools:analyze` - Keyword-based analysis

## Troubleshooting

| Issue                    | Cause                    | Solution                                    |
| ------------------------ | ------------------------ | ------------------------------------------- |
| No recordings found      | No .cast files in ~/eon  | Check recording directory with `find ~/eon` |
| File discovery empty     | Wrong search path        | Manually specify file path as argument      |
| Convert fails            | Corrupted .cast file     | Run `/asciinema-tools:finalize` first       |
| AI summarize timeout     | Recording too large      | Use `-q` for quick analysis first           |
| Orphan branch push fails | Git authentication issue | Check GitHub token with `echo $GH_TOKEN`    |
