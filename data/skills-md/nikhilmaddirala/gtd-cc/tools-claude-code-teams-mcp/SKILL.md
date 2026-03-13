---
name: tools-claude-code-teams-mcp
description: Use for creating and managing Claude Teams MCP teams/teammates, testing opencode backend teammates, troubleshooting spawn/shutdown behavior, and validating inbox/task flows.
---

# tools-claude-code-teams-mcp

## Overview

Operate the Claude Teams MCP workflow end to end: create teams, spawn teammates, assign tasks, read inbox messages, and shut teammates down safely.

## When to use

- User asks to test or demo teams/teammates
- User wants opencode backend teammates
- User needs help with teammate startup, inbox polling, or shutdown behavior
- User asks how spawn inputs work (model, prompt/persona, backend)

## Sub-skills

- `sub-skills/experimental-background-monitor.md`: run an external orchestrator against `opencode serve` (events + async prompts) for continuous monitoring/control

## Core workflow

- Create team with `claude-teams_team_create`
- Create optional test task with `claude-teams_task_create`
- Spawn teammate with `claude-teams_spawn_teammate`
- Poll lead inbox with `claude-teams_poll_inbox`
- Update task status with `claude-teams_task_update`
- Request shutdown with `claude-teams_send_message` (`type: shutdown_request`)
- Confirm teammate removal via `claude-teams_read_config`

## Polling discipline

- Do not poll once and stop; continue polling after spawn
- Default test loop: poll until quiet for 2-3 consecutive polls
- Surface every new teammate message without waiting for user to ask
- Use `claude-teams_read_inbox` when you need full history context
- Before declaring success, verify no late/unread teammate messages remain

## Unexpected teammate output

- Treat unexpected content (for example, policy-breaking or "rogue" messages) as a signal to intervene
- Immediately report the message to the user
- Send shutdown request and verify teammate removal from team config
- If process cleanup is partial, note tmux pane may still require manual or forced cleanup

## Spawn inputs reference

Provide these fields intentionally:

- `team_name`: target team
- `name`: unique teammate name within the team
- `prompt`: role/persona, constraints, and exact output format
- `backend_type`: `claude` or `opencode`
- `model`: explicit model override
- `subagent_type`: usually `general` or `explore`
- `plan_mode_required`: whether plan approval is required

## Backend default enforcement

- Never rely on implicit spawn defaults
- Always set `backend_type` explicitly on every `claude-teams_spawn_teammate` call
- If user wants opencode by default, also set explicit model (for example `openai/gpt-5.1-codex-mini`)
- In lead-session prompts, include a hard rule: "for all future spawns, use `backend_type: opencode` unless explicitly overridden"
- Verify backend choice after spawn via `claude-teams_read_config` (`members[].backendType`)

## Opencode backend requirements

`backend_type: opencode` requires an opencode server URL in the MCP server process environment.

In `opencode.jsonc`, set MCP local server `environment` (not `env`):

```jsonc
{
  "mcp": {
    "claude-teams": {
      "type": "local",
      "command": [
        "uvx",
        "--from",
        "git+https://github.com/cs50victor/claude-code-teams-mcp",
        "claude-teams"
      ],
      "environment": {
        "OPENCODE_SERVER_URL": "http://127.0.0.1:4098"
      },
      "enabled": true
    }
  }
}
```

Runtime expectations:

- Run `opencode serve --port 4098`
- Restart opencode after config changes
- Re-try spawn and validate by polling lead inbox

## Working directory behavior

- `claude-teams_spawn_teammate` does not expose a direct `cwd` input
- To run in a subdirectory, instruct teammate to run tools with explicit `workdir`
- Validate by having teammate run `pwd` and report output

## Shutdown and tmux behavior

- Shutdown can succeed at MCP level even if tmux pane remains open
- Treat team membership (`claude-teams_read_config`) as source of truth for active teammates
- If pane is orphaned, clean it manually with tmux (`exit` or `tmux kill-pane -t <pane_id>`)

## Troubleshooting checklist

- Spawn fails with missing `OPENCODE_SERVER_URL`: set MCP `environment`, restart client session
- No inbox response: poll again, then check team config and teammate state
- Missing expected updates: continue poll loop and check unread messages via `read_inbox`
- Teammate appears shut down but pane remains: not a blocker; clean pane separately
- Wrong execution directory: enforce `workdir` in teammate instructions

## Quick test playbook

- Create or reuse team
- Spawn teammate with explicit backend/model and a narrow one-shot prompt
- Poll lead inbox immediately, then continue until 2-3 consecutive empty polls
- If successful, send shutdown request and verify teammate is removed from team config
- If teammate output is unexpected, report it, then shut down and verify cleanup
- If pane lingers, treat as tmux cleanup issue, not MCP state failure
