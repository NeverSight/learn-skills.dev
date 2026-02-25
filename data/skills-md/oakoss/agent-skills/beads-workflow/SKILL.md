---
name: beads-workflow
description: 'Converts markdown plans into beads (tasks with dependencies) and polishes them until implementation-ready. The bridge between planning and agent swarm execution. Use when converting a plan to beads, polishing bead descriptions, adding test coverage beads, reviewing bead dependencies, or preparing tasks for agent swarm execution.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
---

# Beads Workflow

Beads are epics, tasks, and subtasks with dependency structure, optimized for AI coding agents. They function like Jira or Linear but designed for machines. This skill covers the full lifecycle: converting markdown plans into beads, iteratively polishing them across multiple rounds and models, and integrating with the bd CLI and Agent Mail for swarm execution. Use this when you have a markdown plan and need to produce self-contained, implementation-ready tasks. Do not use this for the planning phase itself; use a planning skill for that.

> **Core Principle:** "Check your beads N times, implement once" -- where N is as many as you can stomach.

## Quick Reference

| Workflow               | What It Does                                                   | Key Detail                                                              |
| ---------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Plan to beads          | Converts a markdown plan into granular beads with dependencies | Use the full or short conversion prompt with `bd` tool                  |
| Polish beads           | Iteratively reviews and improves bead quality                  | Run 6-9 rounds until steady-state; use full or standard prompt          |
| Fresh session          | Breaks out of polishing plateaus                               | Start new session, re-establish context, then resume polishing          |
| Cross-model review     | Gets alternative perspectives on bead quality                  | Run final pass with a different model (Codex, Gemini CLI)               |
| Add test coverage      | Creates unit test and e2e test beads                           | Use the test coverage prompt to audit and fill gaps                     |
| bd CLI basics          | Create, update, depend, close beads                            | Always use `bd` tool; never run bare `bv` (interactive TUI)             |
| Robot mode             | Machine-readable bv output for agents                          | `bv --robot-triage`, `--robot-next`, `--robot-plan`, `--robot-insights` |
| Agent Mail integration | Coordinate multi-agent bead execution                          | Use bead ID as `thread_id`; prefix subjects with `[bd-XXX]`             |

## Common Mistakes

| Mistake                                                  | Correct Pattern                                                                                                |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Oversimplifying bead descriptions to short bullet points | Beads must be verbose and self-documenting with background, reasoning, and considerations                      |
| Stopping after one polish round                          | Keep polishing until steady-state (typically 6-9 rounds); start a fresh session if progress flatlines          |
| Omitting test coverage beads                             | Every feature bead should have associated unit test and e2e test beads with detailed logging                   |
| Not making all blocking relationships explicit           | Use `bd depend` to declare every dependency; agents cannot infer implicit ordering                             |
| Losing features from the original plan                   | Cross-check every plan section against beads; everything must be embedded so the plan is never consulted again |
| Running bare `bv` without flags                          | Always use `bv --robot-*` flags; bare `bv` launches an interactive TUI that blocks agents                      |

## Delegation

- **Create initial beads from a markdown plan**: Use `Task` agent with the plan-to-beads prompt and `bd` tool access
- **Polish beads across multiple rounds**: Use `Task` agent with the standard polish prompt, repeating until steady-state
- **Review bead graph for cycles and missing dependencies**: Use `Explore` agent to run `bv --robot-insights` and validate the dependency structure
- **Add test coverage beads**: Use `Task` agent with the test coverage prompt

## References

- [Plan to Beads](references/plan-to-beads.md) -- Converting markdown plans into beads, exact prompts, what gets created
- [Polishing Workflow](references/polishing-workflow.md) -- Polishing protocol, fresh session technique, cross-model review, quality checklist
- [Agent Integration](references/agent-integration.md) -- bd CLI commands, robot mode, Agent Mail integration, test coverage beads
