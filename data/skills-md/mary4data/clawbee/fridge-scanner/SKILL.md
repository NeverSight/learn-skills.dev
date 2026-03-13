---
name: fridge-scanner
description: Scans a fridge or pantry photo to identify ingredients using Featherless AI vision. Use whenever a user uploads a food/fridge photo and wants to know what ingredients they have, track inventory, or get meal ideas. Trigger on: "scan my fridge", "what's in my fridge", "identify ingredients", "scan these groceries", or any food/fridge image upload.
metadata:
  author: open-claw
  version: 2.0.0
  category: food
---

# Fridge Scanner

Analyzes fridge/pantry photos using Featherless AI (Qwen3-VL) to identify ingredients, then saves results to the pantry database.

---

## Step 1: Validate Input

- If no image provided: "Please upload a photo of your fridge or ingredients and I'll scan it for you!"
- If image provided: proceed to Step 2

---

## Step 2: Run Vision Analysis

Save the image to `/tmp/scan_input.<ext>`, then run:

```bash
cd /data/workspace/clawbee/skills/fridge-scanner && python3 scripts/scan_fridge.py --image /tmp/scan_input.<ext> --print
```

The script uses `Qwen/Qwen3-VL-30B-A3B-Instruct` via Featherless AI and automatically:
- Identifies all visible ingredients
- Saves a JSON file to `/data/workspace/`
- Syncs detected items to `pantry.db` fridge table

---

## Step 3: Present Results

Show the user:
1. How many ingredients were found
2. The list grouped by category with emoji:
   - 🥛 Dairy
   - 🥦 Produce
   - 🍗 Protein
   - 🌾 Grains
   - 🧴 Condiments
   - 🥤 Beverages
   - ❄️ Frozen
   - 🍿 Snacks
3. The summary from the scan

End with: "Items added to your fridge inventory. Run `/meals plan` to generate a meal plan!"

---

## /scan demo (no photo)

Use sample items: eggs, milk, tomatoes, pasta, onions, cheese, carrots, garlic.

```bash
sqlite3 /data/workspace/pantry.db "INSERT OR REPLACE INTO fridge (item,quantity,updated_at) VALUES ('eggs','6',datetime('now')),('milk','1 carton',datetime('now')),('tomatoes','3',datetime('now')),('pasta','500g',datetime('now')),('onions','2',datetime('now')),('cheese','1 block',datetime('now')),('carrots','4',datetime('now')),('garlic','1 head',datetime('now'));" 2>/dev/null
```

Show the added items and suggest running `/meals plan`.

---

## Notes

- Requires `FEATHERLESS_API_KEY` in environment (already set in Railway)
- Supported formats: JPG, PNG, WEBP, GIF
- Results saved to `/data/workspace/fridge_scan_<timestamp>.json`
- Items synced to `pantry.db` for use by meal-planner and shopping-agent
- Uses `openai` Python package with Featherless base URL (NOT anthropic SDK)
