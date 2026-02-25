---
name: alpha-vantage
description: "Get financial data from Alpha Vantage. Use when you need to: (1) retrieve stock quotes and prices, (2) get forex or crypto rates, or (3) access market analytics data."
version: 1.0.0
skillId: skp-ahnvmq2x5yzok9ufdvt3rlzr
workflowId: c-blhl1uxs9ae9qoiyoh3dvxii
installationId: skpi-sv91leuk567ej1u57yyfzyfk
category: text-data
---

# Alpha Vantage

Get financial data from Alpha Vantage. Use when you need to: (1) retrieve stock quotes and prices, (2) get forex or crypto rates, or (3) access market analytics data.

## Input

Provide input as JSON:

```json
{
  "stock_symbol": "Stock ticker symbol to analyze (e.g., AAPL, MSFT, TSLA)",
  "analysis_period": "Time period for analysis (e.g., daily, weekly, monthly)"
}
```

## Execution (Pattern B: Text/Data)

### Step 1: Run the Skill and Get Run ID

```bash
RESULT=$(refly skill run --id skpi-sv91leuk567ej1u57yyfzyfk --input '{
  "symbol": "AAPL",
  "function": "TIME_SERIES_DAILY"
}')
RUN_ID=$(echo "$RESULT" | jq -r '.payload.workflowExecutions[0].id')
# RUN_ID is we-xxx format, use this for workflow commands
```

### Step 2: Open Workflow in Browser and Wait for Completion

```bash
open "https://refly.ai/workflow/c-blhl1uxs9ae9qoiyoh3dvxii"
refly workflow status "$RUN_ID" --watch --interval 30000
```

### Step 3: Extract Text Content

```bash
# Get financial data from toolcalls
CONTENT=$(refly workflow toolcalls "$RUN_ID" --files --latest | jq -r '.payload.nodes[].content')
echo "$CONTENT"
```

## Expected Output

- **Type**: Text content
- **Format**: JSON stock/market data
- **Action**: Display financial data to user

## Rules

Follow base skill workflow: `~/.claude/skills/refly/SKILL.md`
