---
name: jobs
description: Inspect visible research run state, scheduled research follow-ups when available, and durable watch artifacts. Use when the user asks what's running for a research workflow or wants research-run status.
---

# Jobs

Run the `/jobs` workflow. The slash command expands the full workflow instructions in the active session; do not try to read a relative prompt-template path from the installed skill directory.

Shows visible research-run process/scheduler state when those tools are installed, running subagent tasks, and durable watch/autoresearch/replication artifacts on disk. If process or scheduling tools are unavailable, the workflow reports that capability as blocked instead of claiming background state exists.
