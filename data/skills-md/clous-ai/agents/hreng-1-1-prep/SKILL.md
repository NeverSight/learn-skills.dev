---
name: hreng-1-1-prep
description: Use when the user is preparing for a 1:1 meeting and wants an agenda from recent feedback, incidents, goals, and prior notes, with talking points and follow-ups.
version: 1.0.0
license: MIT
---

# 1:1 Prep

Build a short, scannable 1:1 agenda and talking points from recent feedback, incidents, and goals.

## When to Use

Use this skill when:
- A manager is **preparing for a 1:1** and wants structure.
- You have **recent feedback, incidents, or goals** to surface in one place.
- You want **talking points and suggested follow-ups** so nothing drops.

Do **not** use this skill when:
- The focus is **performance diagnosis or PIP** → use `hreng-perf-diagnose`.
- The focus is **promotion or review packet** → use `hreng-ladder` / review-packet.

## Inputs Required

- Person (report name/identifier).
- Time window (e.g. last 2 weeks; default if not specified).
- Optional: prior 1:1 notes, recent feedback text, incident summaries, current goals.

## Outputs Produced

- **Short agenda** (5–10 min to scan): sections such as Wins, Feedback to address, Incidents, Goals/OKRs, Blockers, Action items, Follow-ups.
- **Talking-point bullets** per section so the manager can lead the conversation.
- **Suggested follow-ups** (e.g. “Send recap,” “Schedule deep-dive,” “Escalate X”).

## Core Pattern

1. **Gather** recent feedback, incidents, goals (AskUserQuestion or Read).
2. **Group** into agenda sections; prioritize by urgency and relationship impact.
3. **Draft** 2–3 bullets per section; keep tone direct and actionable.
4. **Suggest** 1–2 follow-ups so commitments don’t get lost.

## Using Supporting Resources

### Templates
- **`templates/agenda-template.md`** – Base structure for 1:1 agenda and talking points.

### References
- None in-repo; use MCP or user-provided context for calendar, tickets, feedback.

### Scripts
- No validation script; use MCP or manual review for completeness.

## Tips

- Prefer MCP for calendar, tickets, or feedback tools if available.
- Keep output to one page; manager can expand in the meeting.
