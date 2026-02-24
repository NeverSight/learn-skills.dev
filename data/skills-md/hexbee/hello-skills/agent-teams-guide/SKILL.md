---
name: agent-teams-guide
description: "Guide for orchestrating and controlling Claude Code agent teams. Use when working with or managing multi-agent team coordination in Claude Code, including: (1) Creating and starting agent teams, (2) Controlling teammates (display modes, task assignment, delegation), (3) Best practices for parallel work, (4) Troubleshooting team issues. Covers concepts like team lead, teammates, shared task lists, and inter-agent messaging."
---

# Agent Teams Guide

## Quick Reference

| Command | Description |
|---------|-------------|
| `Create an agent team...` | Spawn teammates for parallel work |
| `Clean up the team` | Shut down all teammates gracefully |
| `Delegate mode` | Press Shift+Tab after starting team |
| `Shift+Up/Down` | Select teammate in in-process mode |

## Enabling Agent Teams

Agent teams are experimental. Enable via environment variable:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or set the environment variable in your shell before running Claude Code.

## Creating a Team

Start a team by describing parallel work that would benefit from multiple perspectives:

```
Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

Claude creates:
- A **team lead** (your main session)
- **Teammates** (separate Claude Code instances)
- A **shared task list** for coordination

## Display Modes

### In-Process Mode (Default)
- All teammates run in your main terminal
- `Shift+Up/Down` to select a teammate
- Type to message them directly
- Works in any terminal

### Split-Pane Mode
- Each teammate gets its own pane
- Requires tmux or iTerm2
- Set `teammateMode` in settings.json:
```json
{ "teammateMode": "in-process" }
```
- Override per session: `claude --teammate-mode in-process`

## Controlling Teammates

### Task Assignment
- Lead assigns explicitly: tell the lead which task goes to which teammate
- Self-claim: teammates pick unassigned, unblocked tasks automatically

### Direct Communication
- **In-process**: Select teammate, type message, press Enter to view, Escape to interrupt
- **Split-pane**: Click into pane to interact directly

### Delegate Mode
Prevents the lead from implementing tasks itself, keeping it focused on coordination:
1. Start a team first
2. Press `Shift+Tab` to cycle into delegate mode

### Require Plan Approval
For complex tasks:
```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

## Best Practices

### Give Teammates Enough Context
Teammates don't inherit lead's conversation history. Include details in spawn prompt:
```
Spawn a security reviewer teammate with the prompt: "Review the authentication
module at src/auth/ for security vulnerabilities. Focus on token handling,
session management, and input validation..."
```

### Size Tasks Appropriately
- **Too small**: coordination overhead exceeds benefit
- **Too large**: teammates work too long without check-ins
- **Just right**: self-contained units (function, test file, review)

### Avoid File Conflicts
Break work so each teammate owns different files. Two teammates editing same file causes overwrites.

### Monitor and Steer
Check progress, redirect approaches, synthesize findings. Don't leave teams unattended too long.

## Cleanup

When finished:
```
Clean up the team
```

The lead removes shared team resources. Always use the lead for cleanup, not teammates.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Teammates not visible | Press Shift+Down to cycle; ensure task warrants a team |
| Too many permission prompts | Pre-approve operations in permission settings |
| Teammates stopping on errors | Check output, give additional instructions, or spawn replacement |
| Lead shuts down early | Tell lead to keep going and wait for teammates |
| Orphaned tmux sessions | `tmux ls` then `tmux kill-session -t <name>` |

## When to Use Agent Teams

**Best for:**
- Research and review (multiple perspectives simultaneously)
- New modules or features (independent pieces)
- Debugging with competing hypotheses (parallel investigation)
- Cross-layer coordination (frontend, backend, tests)

**Not ideal for:**
- Sequential tasks
- Same-file edits
- Work with many dependencies

## Common Patterns

### Parallel Code Review
```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Investigate with Competing Hypotheses
```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk
to each other to try to disprove each other's theories.
```

## Limitations

- No session resumption with in-process teammates
- Task status can lag behind actual completion
- Shutdown can be slow (teammates finish current request first)
- One team per session
- No nested teams (teammates can't spawn their own)
- Lead is fixed for team lifetime
- Split panes require tmux or iTerm2 (not VS Code terminal, Windows Terminal, Ghostty)
