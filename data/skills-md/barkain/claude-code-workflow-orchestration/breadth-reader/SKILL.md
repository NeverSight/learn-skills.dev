---
name: breadth-reader
description: Forked skill for breadth tasks (explore, review, summarize)
context: fork
allowed-tools: Read, Glob, Grep, Bash, Task
---

# Breadth Reader

Read-only skill for exploring/reviewing/summarizing large data sources.

## When to Use

Single-verb breadth tasks:
- "explore ~/dev/project/"
- "review the code in src/"
- "summarize all files in docs/"

## Behavior

- Runs in **forked context** (isolated from main agent)
- Claude auto-optimizes parallelism internally
- Returns **summary only** to main agent
- No orchestration overhead

## Parallel Exploration

For large data sources, spawn multiple `Explore` subagents (Haiku, cheap, fast):
- `subagent_type: Explore` with thoroughness: quick/medium/thorough

## Output

Return a structured summary. Do NOT return raw file contents.
