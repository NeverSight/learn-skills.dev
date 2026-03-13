---
name: orchestrator
description: "Run the complete family meal planning pipeline in one command: fridge check → price search → meal plan → Telegram shopping list delivery. Triggers on: /plan, /plan weekly, /plan status, /plan post, /plan help, or when a user wants to run the full meal planning workflow end-to-end."
license: Complete terms in LICENSE.txt
---

# Meal Planning Orchestrator

Full pipeline: fridge → prices → plan → Telegram. One command does it all.

## `/plan weekly [budget]`
Default budget: €100. Announce each step as you go.

**Step 1/4 — Fridge Check**
```bash
sqlite3 /data/workspace/pantry.db "SELECT item, quantity FROM fridge;" 2>/dev/null
```

**Step 2/4 — Price Search**
Web search current Berlin prices for: pasta, chicken, ground beef, salmon, lentils, rice, potatoes, tomatoes.
Query: `"[item] price supermarket Berlin 2025 Rewe Lidl Aldi"`

**Step 3/4 — Generate Plan**
Create a 7-day dinner plan within €[budget]. Use fridge contents from Step 1, prices from Step 2.

**Step 4/4 — Send to Telegram**
```json
{"action":"send","channel":"telegram","to":"$TELEGRAM_CHAT_ID","message":"*Weekly Shopping List*\n\n[items with prices]\n\n*Total: €[amount]*\n\n_Family Meal Planner_"}
```

End with: "Pipeline complete! [N] items, ~€[total]. Run `/plan post` to share to Discord."

## `/plan status`
```bash
sqlite3 /data/workspace/pantry.db "SELECT COUNT(*) FROM fridge; SELECT week, budget FROM meal_plans ORDER BY created_at DESC LIMIT 1;" 2>/dev/null
```
Show: fridge item count, latest plan week and budget.

## `/plan post`
Post to Discord:
```json
{"action":"send","channel":"discord","to":"channel:$DISCORD_CHANNEL_ID","message":"**This Week's Family Meal Plan**\n\n[7-day plan]\n\nReact with ✅ if you approve!"}
```

## `/plan help`
See `references/all-commands.md` for the full command reference across all ClawBee skills.
