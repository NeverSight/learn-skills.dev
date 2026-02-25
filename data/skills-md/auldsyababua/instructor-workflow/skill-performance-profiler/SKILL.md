---
name: skill-performance-profiler
description: Analyzes skill usage patterns across conversations to track token consumption, identify heavy vs. lightweight skills, measure invocation frequency, detect co-occurrence patterns, and suggest consolidation opportunities. Use when the user asks to analyze skill performance, optimize skill usage, identify token-heavy skills, find consolidation opportunities, or review skill metrics.
---

# Skill Performance Profiler

Comprehensive analysis tool for tracking and optimizing skill usage patterns, token consumption, and identifying opportunities for skill consolidation.

## When to Use This Skill

Use this skill when users request:
- Analysis of skill token usage or performance metrics
- Identification of "heavy" vs "lightweight" skills
- Skill consolidation opportunities or optimization suggestions
- Frequency analysis of skill invocations
- Co-occurrence patterns (skills used together)
- Time-based trends in skill usage
- Reports or visualizations of skill metrics

Trigger phrases include: "analyze my skills," "which skills use the most tokens," "skill performance," "consolidation opportunities," "optimize my skills," "skill usage report," etc.

## Analysis Process

The analysis involves three main steps:

1. **Data Collection**: Gather conversation history using recent_chats tool
2. **Analysis**: Process conversations to extract skill metrics
3. **Reporting**: Generate formatted output (markdown report, CSV, or visualization)

### Step 1: Collect Conversation Data

Use the `recent_chats` tool to gather conversations for analysis. The time range and number of conversations depends on the user's request:

```python
# For recent analysis (default - last 20 conversations)
recent_chats(n=20)

# For specific time periods
recent_chats(n=20, after="2025-10-01T00:00:00Z")

# For comprehensive analysis (iterate to get more)
recent_chats(n=20, before=earliest_timestamp_from_previous_call)
```

Extract the conversation content and metadata (especially `updated_at` timestamps) from the results.

### Step 2: Prepare Data for Analysis

Create a JSON file containing the conversation data in this format:

```json
{
  "conversations": [
    {
      "content": "full conversation text including tool calls and responses",
      "updated_at": "2025-10-22T10:30:00Z"
    }
  ]
}
```

Save this as `/home/claude/conversations.json`.

### Step 3: Run Analysis

Execute the analysis script:

```bash
cd /home/claude
python3 /mnt/skills/user/skill-performance-profiler/scripts/analyze_skills.py conversations.json
```

This produces `conversations_analysis.json` with comprehensive metrics including:
- Per-skill statistics (invocation count, token usage, averages)
- Skill categorization (Lightweight/Medium/Heavy/Very Heavy)
- Co-occurrence patterns
- Summary statistics
- Consolidation opportunities

### Step 4: Generate Reports

Create formatted output using the report generator:

```bash
# Generate markdown report
python3 /mnt/skills/user/skill-performance-profiler/scripts/generate_report.py conversations_analysis.json markdown

# Generate CSV export
python3 /mnt/skills/user/skill-performance-profiler/scripts/generate_report.py conversations_analysis.json csv

# Generate both formats
python3 /mnt/skills/user/skill-performance-profiler/scripts/generate_report.py conversations_analysis.json both
```

This creates:
- `conversations_report.md`: Comprehensive markdown report with all metrics
- `conversations_export.csv`: Tabular data for spreadsheet analysis

### Step 5: Present Results

Present the analysis to the user in the most appropriate format:

1. **For quick summaries**: Extract key findings from the JSON and present inline
2. **For detailed analysis**: Move the markdown report to `/mnt/user-data/outputs/` and provide a link
3. **For data exploration**: Create a spreadsheet (xlsx) or provide the CSV
4. **For visualization**: Consider creating a React artifact with charts (using recharts library)

## Key Metrics Explained

**Invocation Count**: Number of times a skill was used across analyzed conversations

**Token Consumption**:
- Total Tokens: Cumulative tokens consumed by the skill across all invocations
- Average Tokens: Mean token usage per invocation
- Min/Max Tokens: Range showing variability in skill usage

**Skill Categories** (by average tokens):
- Lightweight: < 500 tokens
- Medium: 500-2,000 tokens  
- Heavy: 2,000-5,000 tokens
- Very Heavy: > 5,000 tokens

**Co-occurrence Rate**: Percentage of time skills are used together, indicating potential consolidation opportunities

**Consolidation Opportunities**: Skill pairs used together ≥50% of the time, suggesting they might benefit from being merged into a single skill

## Example Usage Patterns

**Quick Performance Check**:
```
User: "Which of my skills are using the most tokens?"
→ Collect 20 recent chats, analyze, show top 5 heaviest skills
```

**Comprehensive Audit**:
```
User: "Give me a full analysis of my skill usage over the last month"
→ Collect conversations from last month (multiple calls to recent_chats)
→ Run full analysis
→ Generate markdown report and provide download link
```

**Consolidation Analysis**:
```
User: "Are there skills I should consolidate?"
→ Analyze conversation patterns
→ Focus on consolidation_opportunities in results
→ Present recommendations with supporting data
```

**Trend Analysis**:
```
User: "Show me skill usage trends over time"
→ Collect conversations across time periods
→ Analyze and group by time buckets
→ Create visualization artifact with trend charts
```

## Token Estimation Notes

Token counts are estimated using a 4:1 character-to-token ratio. This is an approximation since:
- Actual tokenization varies by content
- Skills are loaded into context but may not consume their full size
- Multiple skills may be loaded but only portions used

For more accurate analysis, actual token counts from the API would be ideal, but this estimation provides useful relative comparisons for optimization decisions.

## Output Recommendations

**Choose output format based on user needs**:

- **Inline summary**: For quick questions about specific metrics
- **Markdown report**: For comprehensive analysis requiring narrative explanation
- **CSV export**: When user wants to do their own analysis in Excel/Sheets
- **Visualization artifact**: For trend analysis or comparative visualizations
- **Spreadsheet (xlsx)**: For detailed data exploration with built-in charts

Move all generated files to `/mnt/user-data/outputs/` and provide computer:// links so users can download them.
