---
name: summarize
description: AI-powered iterative deep-dive analysis of converted recordings. TRIGGERS - summarize recording, analyze session, what happened, session summary, deep analysis, findings extraction.
allowed-tools: Bash, Grep, Read, AskUserQuestion, Task, Write
argument-hint: "[file] [--topic topic] [--depth quick|medium|deep] [--output file]"
---

# /asciinema-tools:summarize

AI-powered iterative deep-dive analysis for large .txt recordings. Uses guided sampling and AskUserQuestion to progressively explore the content.

## Philosophy

Large recordings (1GB+) cannot be read entirely. This command uses:

1. **Initial guidance** - What are you looking for?
2. **Strategic sampling** - Head, middle, tail + keyword-targeted sections
3. **Iterative refinement** - AskUserQuestion to drill deeper into findings
4. **Progressive synthesis** - Build understanding through multiple passes

## Arguments

| Argument   | Description                                        |
| ---------- | -------------------------------------------------- |
| `file`     | Path to .txt file (converted from .cast)           |
| `--topic`  | Initial focus area (e.g., "ML training", "errors") |
| `--depth`  | Analysis depth: `quick`, `medium`, `deep`          |
| `--output` | Save findings to markdown file                     |

## Workflow

### Phase 1: Initial Guidance

```yaml
AskUserQuestion:
  question: "What are you trying to understand from this recording?"
  header: "Focus"
  options:
    - label: "General overview"
      description: "What happened in this session? Key activities and outcomes"
    - label: "Key findings/decisions"
      description: "Important discoveries, conclusions, or decisions made"
    - label: "Errors and debugging"
      description: "What went wrong? How was it resolved?"
    - label: "Specific topic"
      description: "I'll specify what I'm looking for"
```

### Phase 2: File Statistics

```bash
/usr/bin/env bash << 'STATS_EOF'
FILE="$1"

echo "=== File Statistics ==="
SIZE=$(ls -lh "$FILE" | awk '{print $5}')
LINES=$(wc -l < "$FILE")
echo "Size: $SIZE"
echo "Lines: $LINES"

echo ""
echo "=== Content Sampling ==="
echo "First 20 lines:"
head -20 "$FILE"

echo ""
echo "Last 20 lines:"
tail -20 "$FILE"

echo ""
echo "=== Keyword Density ==="
echo "Errors/failures:"
grep -c -i "error\|fail\|exception" "$FILE" || echo "0"
echo "Success indicators:"
grep -c -i "success\|complete\|done\|pass" "$FILE" || echo "0"
echo "Key decisions:"
grep -c -i "decision\|chose\|selected\|using" "$FILE" || echo "0"
STATS_EOF
```

### Phase 3: Strategic Sampling

Based on file size, sample strategically:

**For files < 100MB:**

```bash
# Sample head, middle, tail (1000 lines each)
head -1000 "$FILE" > /tmp/sample_head.txt
tail -1000 "$FILE" > /tmp/sample_tail.txt
TOTAL=$(wc -l < "$FILE")
MIDDLE=$((TOTAL / 2))
sed -n "${MIDDLE},$((MIDDLE + 1000))p" "$FILE" > /tmp/sample_middle.txt
```

**For files > 100MB:**

```bash
# Keyword-targeted sampling
grep -B5 -A20 -i "$TOPIC_KEYWORDS" "$FILE" | head -5000 > /tmp/sample_targeted.txt
```

### Phase 4: Initial Analysis

Read the samples and provide initial findings. Then ask:

```yaml
AskUserQuestion:
  question: "Based on initial analysis, what would you like to explore deeper?"
  header: "Drill down"
  multiSelect: true
  options:
    - label: "Specific timeframe"
      description: "Jump to a particular section (e.g., 'around line 50000')"
    - label: "Follow keyword trail"
      description: "Search for specific patterns and expand context"
    - label: "Error investigation"
      description: "Deep dive into errors and their resolution"
    - label: "Success moments"
      description: "What worked? What were the wins?"
    - label: "Generate summary"
      description: "Synthesize findings into a report"
```

### Phase 5: Iterative Deep-Dive

For each selected focus area:

1. **Extract relevant sections** using grep with context
2. **Read and analyze** the extracted content
3. **Report findings** to user
4. **Ask for next action** via AskUserQuestion

```yaml
AskUserQuestion:
  question: "Found {N} relevant sections. What next?"
  header: "Continue"
  options:
    - label: "Show me the most significant"
      description: "Display top 3 most relevant excerpts"
    - label: "Search for related patterns"
      description: "Expand search to related keywords"
    - label: "Move on"
      description: "I have enough on this topic"
```

### Phase 6: Synthesis

```yaml
AskUserQuestion:
  question: "Ready to generate summary. What format?"
  header: "Output"
  options:
    - label: "Concise bullet points"
      description: "Key findings in 10-15 bullets"
    - label: "Detailed markdown report"
      description: "Full report with sections and evidence"
    - label: "Executive summary"
      description: "1-paragraph high-level summary"
    - label: "Save to file"
      description: "Write findings to markdown file"
```

## Keyword Libraries

### Trading/ML Domain

```
sharpe|drawdown|backtest|overfitting|regime|validation
model|training|loss|epoch|gradient|convergence
feature|indicator|signal|position|portfolio
```

### Development Domain

```
error|exception|fail|bug|fix|debug
commit|push|merge|branch|deploy
test|assert|verify|validate|check
```

### Claude Code Domain

```
tool|bash|read|write|edit|grep
task|agent|subagent|spawn
permission|approve|reject|block
```

## Example Usage

```bash
# Interactive exploration
/asciinema-tools:summarize session.txt

# Focused on ML findings
/asciinema-tools:summarize session.txt --topic "ML training results"

# Quick overview
/asciinema-tools:summarize session.txt --depth quick

# Full analysis with report
/asciinema-tools:summarize session.txt --depth deep --output findings.md
```

## Example Output

```markdown
# Session Summary: alpha-forge-research_20251226

## Overview

- **Duration**: 4 days (Dec 26-30, 2025)
- **Size**: 12GB recording → 3.2GB text
- **Primary Focus**: ML robustness research

## Key Findings

### 1. Training-Evaluation Mismatch (CRITICAL)

- MSE loss optimizes magnitude, but Sharpe evaluates direction
- Result: 80% Sharpe collapse from 2024 to 2025

### 2. Fishr λ=0.1 Solution (BREAKTHROUGH)

- Gradient variance penalty solves V-REx binary threshold
- Feb'24 Sharpe: -6.14 → +6.14

### 3. Model Rankings

| Model  | Window | Sharpe |
| ------ | ------ | ------ |
| TFT    | 15mo   | 1.02   |
| BiLSTM | 12mo   | 0.50   |

## Evidence Locations

- Line 15234: "Fishr λ=0.1 SOLVES the V-REx binary threshold problem"
- Line 48102: Phase 4 results summary table

## Next Steps Identified

1. TFT 15mo + Fishr training
2. DSR/PBO statistical validation
3. Agent research synthesis
```

## Troubleshooting

| Issue                 | Cause                          | Solution                              |
| --------------------- | ------------------------------ | ------------------------------------- |
| File too large        | Recording exceeds memory limit | Use `--depth quick` for sampling only |
| No keywords found     | Wrong domain or sparse content | Try different `--topic` focus area    |
| Sampling timeout      | Very large file                | Increase terminal timeout or use grep |
| grep context error    | Missing GNU grep               | `brew install grep` (BSD grep limits) |
| Output file not saved | Permission denied              | Check write permissions on `--output` |

## Related Commands

- `/asciinema-tools:convert` - Convert .cast to .txt first
- `/asciinema-tools:analyze` - Keyword-based analysis (faster, less deep)
- `/asciinema-tools:finalize` - Process orphaned recordings
