---
name: codeburn-claude-cost-dashboard
description: Interactive TUI dashboard for visualizing Claude Code token usage, costs, and task breakdowns by project, model, and activity type.
triggers:
  - show me my Claude Code spending
  - track AI coding token costs
  - visualize claude code usage
  - see where my AI tokens are going
  - install codeburn dashboard
  - export claude code cost report
  - check my coding AI spend today
  - analyze claude code session costs
---

# CodeBurn

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

CodeBurn is an interactive TUI dashboard that reads Claude Code session transcripts directly from disk (`~/.claude/projects/`) and visualizes token usage, costs, and task breakdowns by project, model, activity type, MCP server, and tool. No API keys, no proxy — pure local file analysis.

## Install

```bash
npm install -g codeburn
# or run without installing
npx codeburn
```

**Requirements:** Node.js 20+, Claude Code installed (session data at `~/.claude/projects/`)

## Key Commands

```bash
# Interactive TUI dashboard (default: last 7 days)
codeburn

# Time period shortcuts
codeburn today
codeburn month
codeburn report -p month      # explicit period flag

# Compact one-liner summary
codeburn status
codeburn status --format json

# Export data
codeburn export               # CSV: today, 7d, 30d
codeburn export -f json       # JSON export

# macOS menu bar widget (requires SwiftBar)
codeburn install-menubar
codeburn uninstall-menubar
```

### TUI Keyboard Navigation

| Key | Action |
|-----|--------|
| `←` `→` arrow keys | Switch between Today / 7 Days / Month |
| `1` `2` `3` | Period shortcuts |
| `q` | Quit |

## What CodeBurn Tracks

### 13 Task Categories (deterministic, no LLM calls)

| Category | Trigger Pattern |
|---|---|
| Coding | Edit, Write tools |
| Debugging | Error/fix keywords + tool usage |
| Feature Dev | "add", "create", "implement" keywords |
| Refactoring | "refactor", "rename", "simplify" |
| Testing | pytest, vitest, jest in Bash |
| Exploration | Read, Grep, WebSearch without edits |
| Planning | EnterPlanMode, TaskCreate tools |
| Delegation | Agent tool spawns |
| Git Ops | git push/commit/merge in Bash |
| Build/Deploy | npm build, docker, pm2 |
| Brainstorming | "brainstorm", "what if", "design" |
| Conversation | No tools, pure text exchange |
| General | Skill tool, uncategorized |

### One-Shot Rate
For edit-heavy categories, CodeBurn detects Edit → Bash → Edit retry cycles. The **1-shot rate** shows what percentage of edit turns succeeded without retries. 90% means the AI got it right first try 9/10 times.

### Pricing
Fetched from [LiteLLM](https://github.com/BerriAI/litellm) model prices, auto-cached 24h at `~/.cache/codeburn/`. Covers input, output, cache write, cache read, and web search costs. Falls back to hardcoded prices if fetch fails.

## Data Source

Claude Code stores session transcripts as JSONL:
```
~/.claude/projects/<sanitized-path>/<session-id>.jsonl
```

Each assistant entry contains: model name, token usage (input/output/cache_read/cache_write), tool_use blocks, timestamps. CodeBurn deduplicates by API message ID to prevent double-counting across sessions.

## macOS Menu Bar Setup

```bash
# 1. Install SwiftBar
brew install --cask swiftbar

# 2. Install the CodeBurn plugin
codeburn install-menubar

# 3. Launch SwiftBar — CodeBurn flame icon appears in menu bar
# Refreshes every 5 minutes, shows today's cost + breakdown dropdown
```

To remove:
```bash
codeburn uninstall-menubar
```

## Export Examples

```bash
# Export CSV (three sheets: today, 7d, 30d)
codeburn export
# Output: codeburn-export-2026-04-14.csv

# Export JSON
codeburn export -f json
# Output: codeburn-export-2026-04-14.json
```

### JSON Export Structure

```json
{
  "exported_at": "2026-04-14T10:00:00Z",
  "periods": {
    "today": {
      "total_cost": 1.42,
      "total_tokens": 284000,
      "by_project": { "my-app": 0.89, "other-project": 0.53 },
      "by_model": { "claude-sonnet-4-5": 1.10, "claude-opus-4-5": 0.32 },
      "by_activity": {
        "Coding": { "cost": 0.65, "turns": 34, "one_shot_rate": 0.88 },
        "Debugging": { "cost": 0.41, "turns": 18, "one_shot_rate": 0.72 }
      }
    },
    "7d": { ... },
    "30d": { ... }
  }
}
```

## Project Structure

```
src/
  cli.ts          # Commander.js entry point
  dashboard.tsx   # Ink TUI (React for terminals)
  parser.ts       # JSONL reader, dedup, date filter
  models.ts       # LiteLLM pricing, cost calculation
  classifier.ts   # 13-category task classifier
  types.ts        # Type definitions
  format.ts       # Text rendering (status bar)
  menubar.ts      # SwiftBar plugin generator
  export.ts       # CSV/JSON multi-period export
```

## Programmatic Usage (TypeScript)

If you want to integrate CodeBurn's parsing logic into your own scripts:

```typescript
import { parseSessions } from 'codeburn/parser';
import { calculateCost } from 'codeburn/models';
import { classifyTurn } from 'codeburn/classifier';

// Parse all sessions for a date range
const sessions = await parseSessions({
  startDate: new Date('2026-04-01'),
  endDate: new Date('2026-04-14'),
});

// Sessions are deduplicated by API message ID
for (const turn of sessions.turns) {
  const category = classifyTurn(turn);
  const cost = await calculateCost(turn.model, turn.usage);
  console.log(`${category}: $${cost.toFixed(4)}`);
}
```

```typescript
// Get a status summary programmatically
import { getStatus } from 'codeburn/format';

const status = await getStatus();
console.log(status);
// → "🔥 Today: $1.42 (284k tokens) | Month: $18.30 (3.6M tokens)"

// JSON format for scripting
const statusJson = await getStatus({ format: 'json' });
const data = JSON.parse(statusJson);
// { today: { cost: 1.42, tokens: 284000 }, month: { cost: 18.30, tokens: 3600000 } }
```

## Common Patterns

### Daily Cost Check in CI/Shell Scripts

```bash
#!/bin/bash
# Add to .zshrc or run in CI to log daily AI spend
SPEND=$(codeburn status --format json | jq '.today.cost')
echo "Today's Claude spend: \$$SPEND"

# Alert if over threshold
if (( $(echo "$SPEND > 5.00" | bc -l) )); then
  echo "⚠️  High AI spend today: \$$SPEND"
fi
```

### Export and Analyze with jq

```bash
# Export JSON and analyze by model
codeburn export -f json | jq '.periods["7d"].by_model'

# Find most expensive project this month
codeburn export -f json | jq '
  .periods["30d"].by_project
  | to_entries
  | sort_by(-.value)
  | .[0]
'
```

### Automate Weekly Reports

```bash
#!/bin/bash
# weekly-ai-report.sh — run via cron on Mondays
OUTPUT_DIR="$HOME/ai-cost-reports"
mkdir -p "$OUTPUT_DIR"

DATE=$(date +%Y-%m-%d)
codeburn export -f json > "$OUTPUT_DIR/week-$DATE.json"
codeburn status >> "$OUTPUT_DIR/history.log"
echo "[$DATE] Report saved to $OUTPUT_DIR/week-$DATE.json"
```

## Troubleshooting

### No data shown / "No sessions found"

```bash
# Verify Claude Code session files exist
ls ~/.claude/projects/

# Check a specific project's sessions
ls ~/.claude/projects/<project-name>/
# Should see *.jsonl files

# Confirm Node version is 20+
node --version
```

### Pricing fetch fails / shows $0.00

```bash
# Clear the price cache and retry
rm -rf ~/.cache/codeburn/

# CodeBurn falls back to hardcoded prices automatically
# Run again — it will re-fetch from LiteLLM
codeburn today
```

### Menu bar widget not updating

```bash
# Reinstall the plugin
codeburn uninstall-menubar
codeburn install-menubar

# Ensure SwiftBar is running and plugin directory is set
# SwiftBar → Preferences → Plugin folder should point to ~/Library/Application Support/SwiftBar/Plugins/
```

### Double-counted costs

CodeBurn deduplicates by API message ID automatically. If you see unexpectedly high numbers, check for duplicate JSONL files:

```bash
# List all session files sorted by size
find ~/.claude/projects/ -name "*.jsonl" | xargs wc -l | sort -rn | head -20
```

### TUI rendering issues

```bash
# Ensure terminal supports 256 colors
echo $TERM
# Should be xterm-256color or similar

# Force color mode
COLORTERM=truecolor codeburn
```

## Related

- [ccusage](https://github.com/ryoppippi/ccusage) — inspiration for this project
- [LiteLLM](https://github.com/BerriAI/litellm) — model pricing data source
- [SwiftBar](https://github.com/swiftbar/SwiftBar) — macOS menu bar plugin host
