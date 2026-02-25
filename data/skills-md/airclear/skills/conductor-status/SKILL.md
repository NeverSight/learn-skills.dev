---
name: conductor-status
description: Provides a comprehensive status overview of the Conductor project. Use when the user wants to know the current progress, active tasks, next steps, or overall health of the project tracks and plans.
---

# Conductor Status

## Overview

This skill acts as a project dashboard. It aggregates information from the project's Tracks Registry and individual Implementation Plans to provide a unified view of what's done, what's currently being worked on, and what's coming up next.

## When to Use

- When a user asks "What's the status?", "How are we doing?", or "Show me the project progress."
- To identify current blockers or the next actionable task.

## Workflow

1.  **Setup Check:** Ensure all core Conductor context files exist.
2.  **Registry Parsing:** Read the `tracks.md` file to find all active tracks.
3.  **Plan Analysis:** Traverse the `plan.md` for each track to calculate completion percentages and identify active tasks.
4.  **Summary Generation:** Synthesize the data into a readable report including metrics, active work, and next steps.

## Implementation Details

Refer to the following protocols for detailed procedural instructions:

- **Resolution Protocol:** [references/resolution-protocol.md](references/resolution-protocol.md) - How to find and verify Conductor artifacts.
- **Status Protocol:** [references/status-protocol.md](references/status-protocol.md) - The logic for parsing plans and generating the status report.

## Mandatory Constraints

- **Accurate Metrics:** Percentages MUST be based on actual task counts in the `plan.md` files.
- **Clear Identification:** Explicitly state which track, phase, and task is currently "In Progress".
