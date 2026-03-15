---
name: revolut-currency-converter
description: "Currency conversion using Revolut's API. Use for: converting currencies, finding optimal routes, getting exchange rates."
---

# Revolut Currency Converter

Currency conversion CLI using Revolut's real-time exchange rates.

## How to Use

When user asks to convert currencies or get exchange rates, run the converter.py script and parse the JSON output.

## Commands

**convert** - Direct conversion

```bash
python revolut-currency-converter/scripts/converter.py convert <amount> <from> <to>
```

- Returns: `{"success": true, "from": "EUR", "to": "HUF", "amount": 1000, "result": 377820, "rate": 377.82}`

**find-route** - Find optimal route via bridge currencies

```bash
python revolut-currency-converter/scripts/converter.py find-route <amount> <from> <to> [-n HOPS] [-b BRIDGES...]
```

- Returns all routes with `best` path and `best_amount`

**rate** - Get current rate

```bash
python revolut-currency-converter/scripts/converter.py rate <from> <to>
```

- Returns: `{"success": true, "from": "EUR", "to": "USD", "rate": 1.08}`

## Examples

User says: "Convert 1000 EUR to HUF"
→ Run: `python converter.py convert 1000 EUR HUF`
→ Parse JSON result for the converted amount

User says: "What's the best route to convert 50000 JPY to GBP?"
→ Run: `python converter.py find-route 50000 JPY GBP`
→ Parse JSON result for `best` and `best_amount`

User says: "What's the EUR to USD rate?"
→ Run: `python converter.py rate EUR USD`

## Notes

- Amount must be integer >= 1
- Default bridges for find-route: EUR USD
- Output is always JSON
