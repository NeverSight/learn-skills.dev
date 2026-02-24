---
name: notify
description: >
  Send notifications via ntfy.sh to alert about completed tasks, errors, or
  important events. Use when a long-running task has finished, an error needs
  attention, or the user explicitly asks to be notified about any event.
---

# Notify Skill

Send notifications via ntfy.sh to alert the user about completed tasks, errors, or any important events.

## Usage

Use this skill when:

- A long-running task has completed
- An error or issue needs attention
- The user explicitly asks to be notified
- Any event that warrants alerting the user

## How to Send Notifications

Execute the following command with an appropriate message using fish shell:

```bash
fish -c 'curl -d "<MESSAGE>" "ntfy.sh/$NTFY_SUB_TOPIC"'
```

Replace `<MESSAGE>` with a concise, descriptive message about the event.

**Note**: `$NTFY_SUB_TOPIC` is a private fish shell variable, so the command must be run via `fish -c`.

## Message Guidelines

- Keep messages short and actionable (under 100 characters when possible)
- Include relevant context (e.g., task name, file, error type)
- Use clear language

## Example Messages

- "Build completed successfully"
- "Tests passed: 42/42"
- "Error: TypeScript compilation failed in src/index.ts"
- "PR #123 is ready for review"
- "Task complete: Database migration finished"
