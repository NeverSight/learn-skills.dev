---
name: meal-planner
description: "Plan weekly family meals based on fridge contents and a budget. Generates a 7-day dinner plan, identifies what to buy vs. what's already in the fridge, and saves the plan. Triggers on: /meals plan, /meals show, /meals pref, weekly meal planning requests, 'what should we eat this week', dinner ideas for the family."
license: Complete terms in LICENSE.txt
---

# Meal Planner

Weekly dinner planning for a family of 4 using fridge contents and a budget.

## Setup
```bash
bash skills/meal-planner/scripts/init-db.sh
```

## Commands

### `/meals plan [budget]`
Default budget: €100.

1. Load fridge contents:
   ```bash
   sqlite3 /data/workspace/pantry.db "SELECT item FROM fridge;" 2>/dev/null
   ```

2. Generate a 7-day plan — see `references/meal-templates.md` for default meals and output format.

3. Mark each ingredient as "have" (in fridge) or "buy" (missing).

4. Save plan:
   ```bash
   bash skills/meal-planner/scripts/save-plan.sh '[week]' '[plan_json]' [budget]
   ```

5. Display the plan and shopping list. End with: "Run `/shopping send` to send to Telegram."

### `/meals show`
```bash
sqlite3 /data/workspace/pantry.db "SELECT plan_json FROM meal_plans ORDER BY created_at DESC LIMIT 1;"
```
Display in readable format. If none: "No plan yet. Run `/meals plan` first."

### `/meals pref <key> <value>`
```bash
sqlite3 /data/workspace/pantry.db "CREATE TABLE IF NOT EXISTS family_prefs (key TEXT PRIMARY KEY, value TEXT); INSERT OR REPLACE INTO family_prefs VALUES ('<key>','<value>');"
```
Examples: `/meals pref people 4`, `/meals pref vegetarian yes`, `/meals pref budget 80`

## Notes
- Default family size: 4 people
- Berlin context: Aldi/Lidl for staples, Rewe for quality
- See `references/meal-templates.md` for the weekly template and display format
