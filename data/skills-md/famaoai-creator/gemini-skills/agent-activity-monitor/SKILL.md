---
name: agent-activity-monitor
description: Collects and visualizes statistics regarding the agent's activities, including skill usage, execution success rates, and task duration. Provides a data-driven dashboard for ecosystem health.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - data-engineering
  - gemini-skill
  - observability
---

# Agent Activity Monitor

This skill provides transparency into the "Working Mind" of the agent by tracking and analyzing how it uses the 110+ available skills.

## Capabilities

### 1. Activity Data Collection

- Parses `work/` logs and Git commit history to extract:
  - **Skill Frequency**: Which skills are used most often.
  - **Outcome Tracking**: Success vs. failure rates per skill.
  - **Task Velocity**: Average time taken from "Request" to "Resolution."

### 2. Dashboard Generation

- Generates a periodic "Agent Activity Report" (Markdown/HTML).
- Visualizes trends in autonomy (e.g., how often `autonomous-skill-designer` is triggered).

### 3. Resource & Efficiency Insights

- Estimates token efficiency and identifies skills that might need `prompt-optimizer` intervention due to high failure rates.

## Knowledge Base

- **Historical Logs**: `knowledge/activity-logs/`
- Stores structured activity data (JSON) for long-term trend analysis.

## Usage

- "Generate a dashboard showing the skill usage statistics for the past 24 hours."
- "Show me which skills have the highest failure rate and need optimization."
- "Visualize our progress over the last week in terms of task completion and autonomy."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
