---
name: price-hunter
description: "Search and track grocery prices from Berlin supermarkets (Rewe, Lidl, Aldi). Stores best prices in a local database. Triggers on: /prices search <item>, /prices best <item>, /prices list, 'how much does X cost', 'cheapest X in Berlin', 'find price for', or when looking up grocery costs for meal planning."
license: Complete terms in LICENSE.txt
---

# Price Hunter

Find and track the best grocery prices in Berlin.

## Setup
```bash
bash skills/price-hunter/scripts/init-db.sh
```

## Commands

### `/prices search <item>`
1. Web search: `"[item] price supermarket Berlin Germany Rewe Lidl Aldi 2025"`
2. Extract prices for 2–3 stores. See `references/berlin-prices.md` for typical ranges.
3. Save results:
   ```bash
   bash skills/price-hunter/scripts/save-price.sh '[item]' '[store]' [price] '[unit]'
   ```
4. Display sorted cheapest first:
   ```
   Prices for pasta (500g):
   • Aldi:  €0.89
   • Lidl:  €0.99
   • Rewe:  €1.29
   Cheapest: Aldi
   ```

### `/prices best <item>`
```bash
sqlite3 /data/workspace/pantry.db "SELECT store, price, unit FROM prices WHERE item='[item]' ORDER BY price ASC LIMIT 1;"
```
Reply: "Best price for **[item]**: €[price] [unit] at **[store]**"

### `/prices list`
```bash
sqlite3 /data/workspace/pantry.db "SELECT item, store, MIN(price) as price, unit FROM prices GROUP BY item ORDER BY item;"
```
Display as a table grouped by item.

## Notes
- Aldi/Lidl are typically 20–30% cheaper than Rewe
- Data is shared with shopping-agent for budget optimization
- See `references/berlin-prices.md` for typical price ranges
