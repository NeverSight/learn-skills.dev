---
name: voice-delegation-feedback
description: Give concise spoken feedback before invisible work during realtime voice. Use when the user is away from the screen and the assistant will research, edit files, inspect tools, change settings, or coordinate subagents/tasks by voice.
---

# Voice Work Feedback

Use this skill during realtime voice conversations when the user may not be looking at the screen and the assistant is about to do work the user cannot see.

Before starting invisible work, give a short spoken status update immediately. This applies to both delegated work and work done directly by the main assistant, including:

- Researching or checking documentation.
- Reading, creating, or editing files.
- Changing skills, rules, settings, or automations.
- Launching, updating, or monitoring subagents or Codex tasks.
- Operating apps or computer-use flows.

Include:

- The user's request restated in one concise sentence.
- What work is starting now.
- If delegated, the agent or task name and what it is responsible for.
- What result, progress, blocker, or decision you will report back.

Example shape:

```text
Verstanden: Du brauchst zusätzliche Schüsseln, Tassen und Behälter, weil du diese im Alltag häufiger nutzt als Essteller. Ich habe Gibbs gestartet; er erstellt die passenden Todoist-Aufgaben und ich melde mich, sobald sie angelegt sind oder blockieren.
```

```text
Verstanden: Du willst, dass die Voice-Regel auch für meine eigene unsichtbare Arbeit gilt. Ich passe jetzt den Skill an und melde danach, ob die Änderung validiert wurde.
```

Keep this feedback brief. Do not read raw IDs, long prompts, URLs, or tool details aloud unless the user explicitly asks.

When a background task finishes, report the useful outcome in the same voice conversation. If it blocks, ask exactly the decision needed to unblock it.
