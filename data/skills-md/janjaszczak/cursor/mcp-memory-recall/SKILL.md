---
name: mcp-memory-recall
description: Recall and reuse prior decisions, constraints, and artifacts using MCP memory (e.g., Neo4j). Use when the user references past work (“jak ostatnio”, “kontynuuj”), when resuming a project thread, or when a repeated topic suggests existing decisions.
compatibility: Requires MCP memory server configured in Cursor (e.g., Neo4j). Network access to MCP endpoint.
allowed-tools: MCP(*)
metadata:
  author: janjaszczak
  intent: Reduce repeated context; avoid unnecessary “pre-flight” on trivial tasks.
---

# mcp-memory-recall

## Activation gate (anti-noise)
Only run memory recall if at least one is true:
- User explicitly references past work (“jak ostatnio”, “wróćmy do…”, “kontynuuj”).
- The task is multi-step/refactor/migration where prior decisions materially affect correctness.
- The user asks to “remember/check what we decided”.

Do NOT run for:
- Single-shot Q&A, simple command request, or isolated conceptual question.

## Procedure
1. Query memory for: last relevant project node, decisions, constraints, open TODOs, and “lessons learned”.
2. Extract only the minimum set needed to answer.
3. If conflicts exist (new user constraints vs memory), prefer latest user instruction and mark memory as stale.
4. In output, reference memory-derived constraints as “previously decided” (no verbose dump).

## Output
- Short: “What I found” (key constraints/decisions) + “How it affects this task” + next action.

## Failure handling
- If MCP memory is unavailable: proceed without it and mark as UNCERTAIN + suggest fastest way to verify (open MCP, rerun).
