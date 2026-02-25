---
name: meta-hook-creator
description: 'Create event hooks for Claude Code that trigger on tool calls, prompts, and lifecycle events. Use when automating workflows, blocking dangerous commands, protecting files, or adding notifications. Use for hooks, PreToolUse, PostToolUse, event handling, automation.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://code.claude.com/docs/en/hooks'
disable-model-invocation: true
---

# Hook Creator

## Overview

Claude Code hooks are user-defined shell commands, LLM prompts, or agent evaluations that execute automatically at specific lifecycle points. Hooks receive JSON context via stdin, take action, and communicate results through exit codes, stdout, and stderr.

**When to use:** Blocking dangerous commands, auto-formatting after writes, protecting sensitive files, custom notifications, environment setup, enforcing project conventions, auto-approving safe tools, running tests after changes.

**When NOT to use:** Static context injection (use CLAUDE.md), simple permission rules (use allowlist settings), one-time setup (use shell scripts directly).

## Quick Reference

| Pattern                 | Event                | Matcher           | Key Points                                        |
| ----------------------- | -------------------- | ----------------- | ------------------------------------------------- |
| Block tool call         | `PreToolUse`         | Tool name         | Exit 2 or JSON `permissionDecision: "deny"`       |
| Auto-approve tool       | `PreToolUse`         | Tool name         | JSON `permissionDecision: "allow"`                |
| Modify tool input       | `PreToolUse`         | Tool name         | JSON `updatedInput` with modified parameters      |
| Format after write      | `PostToolUse`        | `Write\|Edit`     | Run formatter, exit 0                             |
| Log tool failures       | `PostToolUseFailure` | Tool name         | Fires when tool throws error or returns failure   |
| Handle permission       | `PermissionRequest`  | Tool name         | JSON `decision.behavior: "allow"` or `"deny"`     |
| Validate user prompt    | `UserPromptSubmit`   | No matcher        | Exit 2 blocks prompt, stdout adds context         |
| Desktop notification    | `Notification`       | Notification type | `permission_prompt`, `idle_prompt`, etc.          |
| Force continue          | `Stop`               | No matcher        | JSON `decision: "block"` with reason              |
| Subagent lifecycle      | `SubagentStop`       | Agent type        | Same decision control as Stop                     |
| Environment setup       | `SessionStart`       | Source type       | Write to `CLAUDE_ENV_FILE` to persist env vars    |
| Session cleanup         | `SessionEnd`         | Exit reason       | Cannot block termination                          |
| Pre-compact context     | `PreCompact`         | `manual\|auto`    | Fires before context compaction                   |
| Background tasks        | Any post-event       | Any               | Set `async: true` on command hooks                |
| LLM evaluation          | Supported events     | Any               | Use `type: "prompt"` for single-turn LLM check    |
| Multi-turn verification | Supported events     | Any               | Use `type: "agent"` for subagent with tool access |

## Common Mistakes

| Mistake                                               | Correct Pattern                                                            |
| ----------------------------------------------------- | -------------------------------------------------------------------------- |
| Exit 1 expecting to block a tool call                 | Use exit 2 to block in PreToolUse and PermissionRequest                    |
| Printing JSON on exit 2                               | JSON output is only processed on exit 0; stderr is used on exit 2          |
| Complex inline bash in settings.json                  | Extract to a script file, reference with `$CLAUDE_PROJECT_DIR`             |
| Missing timeout on slow hooks                         | Set `timeout` field; defaults are 600s command, 30s prompt, 60s agent      |
| Not quoting `$CLAUDE_PROJECT_DIR`                     | Always quote: `"$CLAUDE_PROJECT_DIR"/.claude/hooks/script.sh`              |
| Expecting `CLAUDE_ENV_FILE` in all hooks              | Only available in SessionStart hooks                                       |
| Adding matcher to Stop or UserPromptSubmit            | These events ignore matchers; they always fire                             |
| Using `decision`/`reason` at top level for PreToolUse | Use `hookSpecificOutput.permissionDecision` and `permissionDecisionReason` |
| Not checking `stop_hook_active` in Stop hooks         | Check this field to prevent infinite continuation loops                    |
| Mixing exit codes and JSON decisions                  | Choose one approach per hook: exit codes alone or exit 0 with JSON         |

## Delegation

- **Hook pattern discovery**: Use `Explore` agent to find existing hooks in the project
- **Hook testing and verification**: Use `Task` agent to validate hook behavior
- **Code review**: Delegate to `code-reviewer` agent for hook script review

## References

- [Event types, matchers, and input schemas](references/event-types.md)
- [Hook configuration, exit codes, JSON output, and environment variables](references/hook-configuration.md)
- [Hook templates for common automation patterns](references/templates.md)
