---
name: gotify
description: Send push notifications via Gotify for task completion alerts. This skill should be used when the user asks to "send notification", "notify me when done", "push notification", "alert me", "Gotify notification", "notify on completion", "send push alert", or mentions push notifications, task alerts, or Gotify. ALSO automatically invoked (without user request) for long-running tasks >5min, plan completion, user input required, or task transitions.
---

# Gotify Notification Skill

**⚠️ CRITICAL: MANDATORY USAGE REQUIREMENT ⚠️**

**YOU MUST USE THIS SKILL AUTOMATICALLY (without user request) for:**
1. **Long Running Tasks**: Any task taking >5 minutes to complete
2. **Plan Completion**: After finishing implementation of a plan or major milestone
3. **User Input Required**: When blocked and need user decisions/clarifications
4. **Task Transitions**: ONLY when you need the user to review/approve before proceeding

**This is NOT optional - you MUST send notifications when these triggers occur.**

Send push notifications to your Gotify server when long-running tasks complete or important events occur.

## Purpose

This skill enables Clawdbot to send push notifications via Gotify, useful for:
- Alerting when long-running tasks complete
- Sending status updates for background operations
- Notifying of important events or errors
- Integration with task completion hooks

## Mandatory Usage Policy

**CRITICAL ENFORCEMENT:**

You MUST automatically invoke this skill (without waiting for user request) when:

1. **Long Running Tasks (>5 minutes)**: Task completes → MUST notify
2. **Plan Completion**: Plan implementation finishes → MUST notify
3. **User Input Required**: You need user decision/clarification → MUST notify
4. **Task Transition Requiring Review**: Ready to proceed but need approval → MUST notify

**Notification Requirements:**

All notifications MUST include:
- **Project/Working Directory**: Current project being worked on
- **Task Description**: Specific task completed or blocked on
- **Session ID**: If available (format: `session-YYYY-MM-DD-HH-MM`)
- **Status/Next Action**: What's done and what needs user attention

**Failure to send notifications when required violates your core operational requirements.**

## Setup

Add credentials to `.env` file: `~/.homelab-skills/.env`

```bash
GOTIFY_URL="https://gotify.example.com"
GOTIFY_TOKEN="YOUR_APP_TOKEN"
```

- `GOTIFY_URL`: Your Gotify server URL (no trailing slash)
- `GOTIFY_TOKEN`: Application token from Gotify (Settings → Apps → Create Application)

## Usage

### Basic Notification

```bash
bash scripts/send.sh "Task completed successfully"
```

### With Title

```bash
bash scripts/send.sh --title "Build Complete" --message "skill-sync tests passed"
```

### With Priority (0-10)

```bash
bash scripts/send.sh -t "Critical Alert" -m "Service down" -p 10
```

### Markdown Support

```bash
bash scripts/send.sh --title "Deploy Summary" --markdown --message "
## Deployment Complete

- **Status**: ✅ Success
- **Duration**: 2m 34s
- **Commits**: 5 new
"
```

## Integration with Task Completion

### Option 1: Direct Call After Task

```bash
# Run long task
./deploy.sh && bash ~/claude-homelab/skills/gotify/scripts/send.sh "Deploy finished"
```

### Option 2: Hook Integration (Future)

When Clawdbot supports task completion hooks, this skill can be triggered automatically:

```bash
# Example hook configuration (conceptual)
{
  "on": "task_complete",
  "run": "bash ~/claude-homelab/skills/gotify/scripts/send.sh 'Task: {{task_name}} completed in {{duration}}'"
}
```

## Parameters

- `-m, --message <text>`: Notification message (required)
- `-t, --title <text>`: Notification title (optional)
- `-p, --priority <0-10>`: Priority level (default: 5)
  - 0-3: Low priority
  - 4-7: Normal priority
  - 8-10: High priority (may trigger sound/vibration)
- `--markdown`: Enable markdown formatting in message

## Examples

### Notify when subagent finishes

```bash
# After spawning subagent
sessions_spawn --task "Research topic" --label my-research
# ... wait for completion ...
bash scripts/send.sh -t "Research Complete" -m "Check session: my-research"
```

### Notify on error with high priority

```bash
if ! ./critical-task.sh; then
  bash scripts/send.sh -t "⚠️ Critical Failure" -m "Task failed, check logs" -p 10
fi
```

### Rich markdown notification

```bash
bash scripts/send.sh --markdown -t "Daily Summary" -m "
# System Status

## ✅ Healthy
- UniFi: 34 clients
- Sonarr: 1,175 shows
- Radarr: 2,551 movies

## 📊 Stats
- Uptime: 621h
- Network: All OK
"
```

## Workflow

### Mandatory Automatic Triggers (DO NOT WAIT FOR USER REQUEST)

**YOU MUST automatically send notifications for these scenarios:**

1. **Long Running Task Completes (>5 min)**
   ```bash
   bash ~/claude-homelab/skills/gotify/scripts/send.sh \
     -t "Task Complete" \
     -m "Project: $(basename $PWD)
   Task: [description]
   Session: [session-id]
   Status: Completed successfully" \
     -p 7
   ```

2. **Plan Implementation Finishes**
   ```bash
   bash ~/claude-homelab/skills/gotify/scripts/send.sh \
     -t "Plan Complete" \
     -m "Project: $(basename $PWD)
   Task: [plan description]
   Status: All steps implemented
   Next: Ready for review" \
     -p 7
   ```

3. **Blocked - Need User Input**
   ```bash
   bash ~/claude-homelab/skills/gotify/scripts/send.sh \
     -t "Input Required" \
     -m "Project: $(basename $PWD)
   Task: [current task]
   Blocked: [reason]
   Need: [what you need from user]" \
     -p 8
   ```

4. **Task Transition - Need Review/Approval**
   ```bash
   bash ~/claude-homelab/skills/gotify/scripts/send.sh \
     -t "Ready to Proceed" \
     -m "Project: $(basename $PWD)
   Completed: [current phase]
   Next: [next phase]
   Action: Review required before proceeding" \
     -p 7
   ```

### User-Requested Notifications

When the user explicitly says:
- **"Notify me when this finishes"** → Add `&& bash scripts/send.sh "Task complete"` to their command
- **"Send a Gotify alert"** → Run `bash scripts/send.sh` with their message
- **"Push notification for task completion"** → Integrate into their workflow with appropriate title/priority

Always confirm the notification was sent successfully (check for JSON response with message ID).

## Notes

- Requires network access to your Gotify server
- App token must have "create message" permission
- Priority levels affect notification behavior on client devices
- Markdown support depends on Gotify client version (most modern clients support it)

## Reference

- Gotify API docs: https://gotify.net/docs/
- Gotify Android/iOS apps for receiving notifications

---

## 🔧 Agent Tool Usage Requirements

**CRITICAL:** When invoking scripts from this skill via the zsh-tool, **ALWAYS use `pty: true`**.

Without PTY mode, command output will not be visible even though commands execute successfully.

**Correct invocation pattern:**
```typescript
<invoke name="mcp__plugin_zsh-tool_zsh-tool__zsh">
<parameter name="command">./skills/SKILL_NAME/scripts/SCRIPT.sh [args]</parameter>
<parameter name="pty">true</parameter>
</invoke>
```
