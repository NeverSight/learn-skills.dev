---
name: fridge-tracker
description: "Track fridge and pantry inventory. Add, remove, and list food items with quantities. Triggers on: /fridge, /fridge list, /fridge add <item>, /fridge remove <item>, /fridge clear, or when a user asks what's in the fridge or wants to manage pantry contents."
license: Complete terms in LICENSE.txt
---

# Fridge Tracker

Persistent fridge and pantry inventory using SQLite.

## Setup
```bash
bash skills/fridge-tracker/scripts/init-db.sh
```

## Commands

### `/fridge list` (default)
```bash
sqlite3 /data/workspace/pantry.db "SELECT item, quantity, updated_at FROM fridge ORDER BY item;"
```
Display as a bullet list. If empty: "Fridge is empty. Add items with `/fridge add <item> <quantity>`"

### `/fridge add <item> [quantity]`
```bash
sqlite3 /data/workspace/pantry.db "INSERT OR REPLACE INTO fridge (item,quantity,updated_at) VALUES (lower('<item>'), '<quantity>', datetime('now'));"
```
Reply: "Added **[item]** ([quantity]) to fridge."

### `/fridge remove <item>`
```bash
sqlite3 /data/workspace/pantry.db "DELETE FROM fridge WHERE item=lower('<item>');"
```
Reply: "Removed **[item]**." or "Item not found."

### `/fridge clear`
```bash
sqlite3 /data/workspace/pantry.db "DELETE FROM fridge;"
```
Reply: "Fridge cleared."

## Notes
- Always lowercase item names when storing
- Data is shared with meal-planner and shopping-agent skills
- If sqlite3 unavailable, maintain inventory in session memory as fallback
