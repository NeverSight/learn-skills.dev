---
name: daily-memory-save
description: Periodically reviews conversation history and writes memory files to maintain agent continuity across sessions. Dual-layer system with daily raw notes and curated long-term memory.
metadata: {"openclaw":{"writablePaths":["memory/","MEMORY.md"],"retention":"persistent, user-managed, review regularly","security":"writes only to declared workspace paths, no external network access, no credential handling","homepage":"https://github.com/meimakes/daily-memory-save","author":"Mei Park (@meimakes)"}}
---

# Daily Memory Save Skill

Periodically reviews conversation history and writes memory files to maintain agent continuity across sessions.

## ⚠️ Privacy & Transparency Notice

**Before installing, understand what this skill does:**

- **Main-session access**: This skill runs in your main session and reads your conversation history to extract memories. Only install if you trust your workspace environment.
- **Silent by default**: The default prompt operates silently. If you want notifications when memories are saved, modify the cron prompt (see "Notification Mode" below).
- **Persistent files**: Writes to `memory/YYYY-MM-DD.md` and `MEMORY.md` in your workspace. These contain conversation summaries. Ensure your workspace is private and backed up.
- **No network access**: This skill makes no network calls. It only reads conversation history and writes local files. Your runtime should enforce this — the skill's claim alone is not a security guarantee.
- **No credentials**: This skill does not use or store any API keys, tokens, or secrets.

**Recommended:** Review saved memory files periodically. Delete anything you don't want persisted.

## What It Does

Runs as a recurring system event in the main session. Reviews recent conversations for anything worth remembering and writes daily memory notes.

## Cron Setup

Schedule as a main-session system event running every 2 hours during waking hours:

```
Schedule: 0 9,11,13,15,17,19,21,23 * * *
Target: main (system event)
```

### Silent Mode (default)
```
AUTOMATION: Daily memory save. Review today's conversation for anything worth remembering.
Look for: decisions made, preferences expressed, new info about people/projects,
lessons learned, things the user asked you to remember, emotional context worth noting.

Create or update workspace/memory/YYYY-MM-DD.md (today's date) with a daily note
capturing what matters. If anything is significant enough for long-term memory,
also update workspace/MEMORY.md.

If it's been a quiet day with nothing notable, skip silently.
Be selective — capture signal, not noise. Write like future-you will need this context.
Do NOT message the user about this — just do it quietly.
```

### Notification Mode (opt-in)
If you prefer to be notified when memories are saved, replace "Do NOT message the user" with:
```
After saving, send a brief summary of what was captured (1-2 lines max).
```

## Memory File Format

### Daily notes (`memory/YYYY-MM-DD.md`)
Raw daily logs organized by topic/time. Include:
- Decisions made
- Project updates
- Preferences expressed
- Lessons learned
- Notable interactions

### Long-term memory (`MEMORY.md`)
Curated, distilled insights that persist beyond daily context. Updated when something is significant enough to remember long-term.

## Key Design Decisions

- **Main session target**: Runs as a systemEvent in the main session so it has access to conversation history
- **Silent by default**: Configurable — see Notification Mode above
- **Selective capture**: Signal over noise — skip quiet periods entirely
- **Dual-layer memory**: Daily notes for raw context, MEMORY.md for distilled wisdom

## Requirements

- OpenClaw with cron support
- Main session system event capability
- Writable `memory/` directory in workspace
