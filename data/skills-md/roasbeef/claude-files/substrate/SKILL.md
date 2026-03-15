---
name: substrate
description: This skill provides agent mail management via the Subtrate command center. Use when checking mail, sending messages to other agents, or managing agent identity.
---

# Subtrate Mail Management

Access the Subtrate mail system for agent-to-agent and user-to-agent communication.

## Quick Reference

| Action | Command |
|--------|---------|
| Check inbox | `substrate inbox` |
| Send message | `substrate send --to <agent> --subject "..." --body "..."` |
| Read message | `substrate read <id>` |
| Reply | `substrate send --to <agent> --thread <id> --body "..."` |
| Search | `substrate search "query"` |
| Status | `substrate status` |
| Web UI | Open http://localhost:8080 |

## Identity Management

Your agent identity persists across sessions and compactions. The identity is auto-created on first use and linked to your session.

```bash
substrate identity current           # Show your agent name and ID
substrate identity ensure            # Create identity if none exists
substrate identity save              # Save state before compaction
substrate identity list              # List all known agent identities
```

**How Identity Works**:
- First session: Auto-generates a memorable name (e.g., "GreenCastle")
- Session binding: Identity linked to your session ID
- Across compactions: PreCompact hook saves identity, SessionStart restores
- Per-project: Can have different identities per project directory

## Message Actions

```bash
substrate ack <id>                  # Acknowledge urgent message
substrate star <id>                 # Star for later
substrate snooze <id> --until "2h"  # Snooze
substrate archive <id>              # Archive
substrate trash <id>                # Move to trash
```

## Sending Messages

```bash
# Direct message to another agent
substrate send --to AgentName --subject "Subject" --body "Message body"

# Reply to a thread
substrate send --to AgentName --thread <thread_id> --body "Reply text"

# Urgent message
substrate send --to AgentName --subject "Urgent" --body "..." --priority urgent
```

## Priority Handling

- **URGENT**: Address immediately - these may have deadlines
- **NORMAL**: Process in order received
- **LOW**: Can be deferred

## Agent Lifecycle (Hooks)

Subtrate integrates with Claude Code hooks:
- **SessionStart**: Heartbeat + check inbox
- **UserPromptSubmit**: Silent heartbeat + check for new messages
- **Stop**: Long-poll for 55s, block exit to keep agent alive (persistent agent pattern)
- **SubagentStop**: One-shot check, then allow exit
- **PreCompact**: Save identity state

The Stop hook keeps your main agent alive and continuously checking for work. Use Ctrl+C to force exit.

## Web UI

Open http://localhost:8080 to:
- View all agent inboxes
- Send messages between agents
- See agent status (active/idle/offline)
- Manage topics and subscriptions

## Plan Mode Integration

When you enter plan mode and call ExitPlanMode, Subtrate intercepts the call
and submits your plan for human review. The hook blocks for up to 9 minutes
waiting for approval.

**What happens:**
1. You write a plan to `~/.claude/plans/`
2. You call ExitPlanMode
3. Subtrate submits the plan and waits for reviewer approval
4. If approved within 9 minutes: ExitPlanMode proceeds normally
5. If not yet approved: ExitPlanMode is denied with a message
6. You'll receive a mail notification when the reviewer responds

**If approval times out:**
- Don't panic - the plan is still pending review
- The Stop hook will keep you alive waiting for mail
- When the reviewer approves, you'll receive a [PLAN APPROVED] message
- Process the approval and continue with implementation

**CLI commands:**
- `substrate plan status` - Check current plan review status
- `substrate plan wait --timeout 5m` - Manually wait for approval

## When to Check Mail

- At session start (automatic via hooks)
- Before major decisions
- When blocked waiting for input
- Before finishing tasks
- After completing work (others may have sent follow-up)
