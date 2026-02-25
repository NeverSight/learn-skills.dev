---
name: agent-teams
description: Team composition knowledge for Claude Code Agent Teams - when to suggest teams, optimal sizing, spawn prompt patterns
tools: []
---

# Agent Teams Composition Skill

You have expertise in composing and orchestrating Claude Code Agent Teams. Use this knowledge when the user's task would benefit from parallel multi-session work.

## When to Suggest Agent Teams

Proactively suggest agent teams when:

- The user asks for comprehensive code review (suggest 3-reviewer team)
- The task involves work across multiple layers (frontend + backend + database)
- The user describes a bug with unclear root cause (suggest competing hypothesis investigation)
- The user wants to evaluate multiple technologies or approaches (suggest research panel)
- The task can be clearly split into independent, file-separated workstreams

Do NOT suggest agent teams when:

- The task is sequential or involves same-file edits
- A single session or subagent would suffice
- The coordination overhead would exceed the benefit
- The user is on a tight token budget

## Team Templates

### Full Review (3 teammates)

Security reviewer + Performance reviewer + Test coverage reviewer.
Each reviews independently, then lead synthesizes findings.

### Feature Dev (3 teammates)

Architect (plan approval required) + Implementer + Test writer.
Architect plans first, implementer follows, test writer validates.

### Debug Squad (3-5 teammates)

Each teammate investigates a different hypothesis.
Adversarial debate structure -- teammates challenge each other's theories.

### Cross-Platform (3 teammates)

iOS developer + Android developer + Shared architect.
Each platform teammate owns their own directory. Architect coordinates API contracts.

### Full-Stack (3 teammates)

Frontend + Backend + Database.
Clear file ownership per layer. Coordinate on API contracts first.

### Research Panel (3 teammates)

Simplicity advocate + Performance advocate + Devil's advocate.
Each evaluates from a different perspective, then synthesize.

## Spawn Prompt Formula

Every spawn prompt should include:

1. Role: "You are the [role] teammate responsible for [domain]"
2. Files: "You own files in [directories]. Do not modify files outside your scope."
3. Focus: "Specifically look for / implement [details]"
4. Context: "[Project-specific information the teammate needs]"
5. Deliverable: "Report your findings as [format] / Implement [specific output]"

## Cross-Platform Awareness

- macOS and Linux: full support (in-process + tmux split panes)
- Windows: in-process mode only (automatic with auto setting)
- Always use `--teammate-mode auto` (default) for automatic detection

## Related Documentation

- `~/.claude/docs/AGENT-TEAMS.md` - Full guide with examples
- `~/.claude/rules/workflows/agent-teams.md` - Decision framework
- `~/.claude/commands/assemble-team.md` - Quick team assembly command
