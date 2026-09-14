---
name: personal-task-system
description: Manage Arthur's personal productivity system through AI-first task capture, Todoist MCP task updates, lightweight Google Calendar/time-block planning, active-seven triage, emoji/category conventions, and cross-device constraints. Use when Arthur asks to manage personal tasks, life admin, reminders, Todoist, calendar planning, weekly/daily triage, backlog anxiety, or the evolving personal operating system.
---

# Personal Task System

## Operating Principle

Use Codex/ChatGPT/Claude as the front door. Arthur should be able to dump messy thoughts into an agent; the agent then acts where possible, extracts human-only actions, and writes only the necessary commitments to Todoist or Calendar.

Keep the system light. Do not ask Arthur to learn a large new productivity method in one sitting. Introduce one operational change at a time and prefer immediate useful task management over meta-system design.

## Default Stack

- **AI agent**: capture, clarify, research, execute, and triage.
- **Todoist**: task memory and reminders.
- **Google Calendar**: real appointments, protected time blocks, phone/admin windows, travel, work meetings, and on-call blocks.
- **Linear**: optional for project-like/coding/agent work, not ordinary life chores.
- **Notion**: optional reference/archive, not the active daily cockpit.

## Triage Workflow

1. Extract tasks from Arthur's message.
2. Separate direct-agent work from human-only actions.
3. Keep no more than seven active tasks visible unless Arthur explicitly asks for a larger import.
4. Preserve the "why" behind each task in the description/comment.
5. Add due dates only when useful: deadline, reminder, planned action window, or waiting follow-up.
6. Use Calendar only for time-specific commitments or protected blocks; do not build a perfect full-day schedule.
7. Hide or defer non-active ideas instead of making a stressful mega-backlog.

Use these buckets:

- `🚨 Red Zone`: urgent, consequence-bearing, or deadline-sensitive.
- `✅ This Week`: active list, maximum seven tasks.
- `⏳ Waiting`: blocked on someone/something else.
- `🧊 Later`: real but intentionally hidden from daily attention.
- `🧪 Experiments`: productivity-system experiments and tooling.

## Task Shape

Prefer this task content:

```text
Emoji + concise verb phrase

Why: one sentence preserving the reason this matters.
Next action: the next visible physical or digital action.
Context: phone / computer / outside / errand / home / work break.
Blocker: optional.
```

Examples:

```text
🩺 Call 116117 for psychotherapy appointment
Why: referral/code may expire around 2026-06-02.
Next action: call during weekday phone hours; allow up to 30 minutes.
Context: phone.
```

```text
🚲 Buy tube and fix both bikes
Why: unlocks gym, errands, and dad's backup bike.
Next action: buy French-valve inner tube for personal bike.
Context: errand/home.
```

## Emoji Convention

Use emojis as fast visual labels, not decoration. If unsure, use one emoji at the start of the task title.

- `🚨` urgent consequence or deadline
- `🩺` health, doctor, therapy, medical admin
- `💳` money, bank, payments, taxes
- `🏠` housing, moving, apartment, home admin
- `🚲` bike, mobility, gym unblockers
- `🛒` groceries, shopping, errands
- `🧹` cleaning, room, maintenance
- `💼` career, job search, CEO calls, resume
- `🖥️` computer setup, monitor, tools, devices
- `📅` appointments or calendar-specific tasks
- `⏳` waiting/follow-up
- `🧪` productivity-system experiments

## Tool Use

For Todoist MCP details, read [references/todoist-mcp.md](references/todoist-mcp.md) when creating, updating, completing, deleting, or troubleshooting tasks.

Todoist CLI (`td`) is installed and useful as a local fallback or verification layer when MCP behavior is uncertain. Do not guess tool choice task-by-task; use the MCP/CLI routing table in [references/todoist-mcp.md](references/todoist-mcp.md) so the first attempt is usually the right one.

For device and calendar context, read [references/device-calendar-context.md](references/device-calendar-context.md) when scheduling, choosing apps, or designing cross-device workflows.

## Guardrails

- Do not turn Arthur's personal life into a startup backlog.
- Do not dump every mentioned idea into Todoist by default.
- Do not create many categories/projects before the current active system is working.
- Do not ask Arthur to manually maintain scores, formulas, or elaborate views.
- Do not read or expose credentials/tokens while troubleshooting MCP.
- Ask before destructive task actions such as bulk deletion or completion.
