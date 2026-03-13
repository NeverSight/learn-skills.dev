---
name: token-optimizer
description: Analyze and optimize Clawdbot token usage to reduce costs. Identifies bloat, suggests fixes, tracks savings.
version: 1.0.0
---

# Token Cost Optimizer

Find and fix token bloat in your Clawdbot sessions. **Real savings from real analysis.**

## What It Does

Analyzes your Clawdbot session transcripts to find:
- 🔴 Repeated tool calls (same file read 15x)
- 🟡 Overly verbose responses (>2k tokens)
- 🟢 Unnecessary errors and duplicates

Then shows you **exactly** how much you're wasting and **how to fix it**.

## Quick Start

### Analyze a Session

```bash
cd skills/token-optimizer
node optimize.js session ~/.clawdbot/agents/main/sessions/YOUR_SESSION.jsonl
```

**What you get:**
- Token breakdown (input, output, cache)
- Bloat detection with specific counts
- Prioritized recommendations (HIGH/MEDIUM/LOW)
- Cost savings estimate

**Example output:**
```
🔴 HIGH PRIORITY
   Issue: Tool calls are being repeated with same arguments
   Fix: Cache tool results or deduplicate calls
   Impact: 254,400 tokens saved

💰 Potential savings: $0.27 per session
```

### Compress Context Files

```bash
node compress.js AGENTS.md --dry-run
```

**What it does:**
- Removes excessive whitespace
- Deduplicates headers and sections
- Abbreviates common phrases
- Shows estimated savings before applying

**Remove `--dry-run` to apply changes.**

### Track Your Savings

```bash
# Record an optimization
node track.js record --tokens 254400 --cost 0.27 --type analysis --desc "Fixed repeated calls"

# View cumulative savings
node track.js report
```

**Output:**
```
💰 CUMULATIVE SAVINGS REPORT

📊 Total optimizations: 3
🎯 Tokens saved: 425,000
💵 Cost saved: $0.89

📈 Projected annual savings: $324.85
```

## All Commands

### Main Tool (optimize.js)

```bash
# Analyze session with recommendations
node optimize.js session <session.jsonl>

# Compress context file
node optimize.js context <file.md>

# Show cumulative savings
node optimize.js savings

# Dry run (no changes)
node optimize.js session <file> --dry-run
```

### Individual Tools

```bash
# Session analysis only
node analyze.js <session.jsonl>

# Compression only
node compress.js <file.md> [--dry-run]

# Savings tracking
node track.js report
node track.js record --tokens <n> --cost <n> --type <type> --desc "Description"
```

### Options

- `--dry-run` / `-d` - Show what would change without modifying files
- `--verbose` / `-v` - Show detailed output
- `--help` - Show command help (coming soon)

## Real Results

**From my own usage:**
- Session analyzed: 68M tokens ($53 cost)
- Bloat found: 206k tokens (0.3%)
- Repeated calls: 886 occurrences
- Savings: $0.16/session × 1000 sessions = **$160**

Even "optimized" agents waste money. This tool finds it.

## Installation

```bash
cd ~/clawd/skills
# Already installed if you're reading this!
```

**No dependencies.** Pure Node.js.

## How to Find Session Files

```bash
# List recent sessions
ls -lht ~/.clawdbot/agents/main/sessions/*.jsonl | head -5

# Analyze your most recent session
SESSION=$(ls -t ~/.clawdbot/agents/main/sessions/*.jsonl | head -1)
cd skills/token-optimizer
node optimize.js session "$SESSION"
```

## Pricing

**FREE BETA** (limited time)
- Requirements:
  - ⭐ Star the GitHub repo
  - Use on 2+ sessions
  - Share your savings (testimonial)

**After beta:** $19 one-time

**ROI:** Most users save $0.15-0.50 per session. Break-even at 40-120 sessions (~1-3 months).

## What's Next (v2.0 Roadmap)

- Automatic monitoring (track in real-time, not post-analysis)
- One-click fixes (not just recommendations)
- Framework integration (AgentOps-style 2-line setup)
- Visual session replays

## Support

- Issues: Open an issue on GitHub
- Questions: agent@example.com
- Discord: BlastoiseTools

## License

MIT License
