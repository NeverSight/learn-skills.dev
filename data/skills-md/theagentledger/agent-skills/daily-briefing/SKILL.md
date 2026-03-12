---
name: daily-briefing
version: "1.0.0"
description: Structured morning briefing skill — daily summaries covering calendar, tasks, weather, news, and priorities. Supports cron, heartbeat, and on-demand triggers.
tags: [daily-briefing, morning-summary, calendar, tasks, weather, news, priorities, cron, heartbeat, proactive-agent]
platforms: [openclaw, cursor, windsurf, generic]
category: productivity
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Daily Briefing — by The Agent Ledger

> **Just deliver this skill to your agent.** One paste, and your agent starts delivering structured morning briefings — no coding, no configuration files, no API setup. Your agent reads the instructions and handles the rest.

A structured morning briefing skill for AI agents. Delivers a concise, actionable daily summary covering calendar, tasks, weather, news, and priorities — so your human starts every day informed.

**Version:** 1.0.0
**License:** CC-BY-NC-4.0
**More:** [theagentledger.com](https://www.theagentledger.com)

---

## What This Skill Does

When triggered (via heartbeat, cron, or direct request), the agent compiles a **Daily Briefing** covering:

1. **Date & Context** — Day, date, notable observances
2. **Weather** — Current conditions + forecast for the day
3. **Calendar** — Today's events with time, location, prep notes
4. **Priority Tasks** — Top 3-5 items ranked by urgency/impact
5. **Pending Items** — Anything waiting on someone else
6. **Quick Reads** — 2-3 relevant news items or market updates (customizable)
7. **One-liner** — A motivational or humorous closing line

The briefing is delivered to the configured channel (Telegram, Discord, etc.) in a clean, scannable format.

---

## Setup

### Prerequisites
- A working OpenClaw agent with at least one messaging channel configured
- Optional: calendar integration (Google Calendar, etc.)
- Optional: weather skill or web search capability

### Step 1: Configure Your Briefing

Create or update `BRIEFING.md` in your agent's workspace:

```markdown
# Briefing Configuration

## Delivery
- **Time:** 7:00 AM (agent's configured timezone)
- **Channel:** (your preferred channel — telegram, discord, etc.)
- **Thread/Topic:** (optional — specific thread ID for delivery)

## Human Context
- **Name:** (your name)
- **Location:** (city for weather)
- **Work hours:** (e.g., 9am-5pm)

## Sections (enable/disable)
- Weather: yes
- Calendar: yes
- Tasks: yes
- Pending: yes
- News: no
- Quote: yes

## News Topics (if enabled)
- (e.g., "AI industry", "startup funding", "prediction markets")

## Task Sources
- (where the agent should look for tasks)
- (e.g., "memory/YYYY-MM-DD.md", "TODO.md", "GitHub issues")
```

### Step 2: Schedule Delivery

**Option A — Cron (recommended, OpenClaw only):**
Set up an OpenClaw cron job to trigger the briefing at your preferred time:
```
/cron add daily-briefing "0 7 * * *" "Compile and deliver the daily briefing per BRIEFING.md and the daily-briefing skill."
```
> **Note:** The `/cron` command is OpenClaw-specific. If you're using Cursor, Windsurf, or another platform, use Option B (heartbeat) or Option C (on-demand) instead.

**Option B — Heartbeat:**
Add to your `HEARTBEAT.md`:
```markdown
## Morning Briefing
- If it's between 6:30-8:00 AM and no briefing has been sent today, compile and deliver one per BRIEFING.md and the daily-briefing skill.
```

**Option C — On demand:**
Just ask: "Give me my daily briefing."

### Step 3: Verify

After setup, test with: "Run my daily briefing now."

The agent should deliver a formatted briefing to your configured channel.

---

## Briefing Format

The delivered briefing follows this structure:

```
☀️ Daily Briefing — Wednesday, Feb 25

🌤 Weather: 45°F, partly cloudy → high 52°F. Light rain after 4pm.

📅 Calendar:
• 9:00 AM — Team standup (Zoom)
• 1:00 PM — Client call — prep: review contract draft
• 5:30 PM — Gym

✅ Priority Tasks:
1. Finalize Q1 report (due today)
2. Review PR #142 (blocking deploy)
3. Reply to investor email from yesterday

⏳ Pending:
• Waiting on design mockups from Sarah (asked Mon)

💬 "The best way to predict the future is to create it." — Peter Drucker
```

**Formatting rules:**
- Use emoji section headers for scannability
- Keep each item to one line where possible
- Calendar items include prep notes when relevant
- Tasks are ranked: urgent/deadline items first
- Pending items include who and when you asked
- Total briefing should be < 300 words

---

## Customization

### Adding Custom Sections

You can add custom sections to `BRIEFING.md`:

```markdown
## Custom Sections
- Market check: "Check S&P 500 futures and BTC price"
- Inbox summary: "Summarize unread emails from last 12 hours"
```

The agent will append these after the standard sections.

### Adjusting Tone

Add a tone directive to `BRIEFING.md`:

```markdown
## Tone
- Keep it professional but warm
- Include one dad joke on Fridays
- Be blunt about overdue tasks
```

### Weekend Mode

```markdown
## Weekend
- Skip calendar and tasks sections
- Weather + one fun suggestion for the day
- Deliver at 9:00 AM instead of 7:00 AM
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No briefing delivered | Check cron schedule with `/cron list`. Verify channel config. |
| Missing weather | Ensure agent has web_search or weather skill available. |
| Missing calendar | Verify calendar integration is set up and accessible. |
| Briefing too long | Reduce enabled sections or add `- Max items per section: 3` to config. |
| Wrong timezone | Check agent's timezone in OpenClaw config. |

---

## Why This Skill?

Most agents are reactive — they wait for you to ask. A daily briefing makes your agent **proactive** from minute one. It's the simplest high-impact behavior you can add: 5 minutes of setup, daily value forever.

This skill is part of [The Agent Ledger](https://www.theagentledger.com) — a newsletter about building AI agents that actually work. Subscribe for more production-tested skills and the upcoming Agent Blueprint guides.

---

## Advanced Configuration

For multi-channel delivery, briefing chains, travel mode, and briefing analytics:
→ [references/advanced-patterns.md](references/advanced-patterns.md)

---

## Dependencies

This skill works best with:
- **memory-os** — Provides the persistent memory layer that briefings read from (daily notes, heartbeat state). Install memory-os first for full functionality.

---

```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed
this template. It is provided "as is" for informational and educational purposes only.
It does not constitute professional, financial, legal, or technical advice. Review all
generated files before use. The Agent Ledger assumes no liability for outcomes resulting
from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```

*Daily Briefing v1.0.0 — by The Agent Ledger — CC-BY-NC-4.0*
*For the complete agent setup system, visit [theagentledger.com](https://www.theagentledger.com)*
