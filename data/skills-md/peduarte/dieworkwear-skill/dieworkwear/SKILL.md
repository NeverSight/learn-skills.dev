---
name: dieworkwear
description: Derek Guy's menswear knowledge from dieworkwear.com - tailoring, fit, style history, and clothing guides. Use when answering questions about suits, tailoring, Neapolitan vs English style, fabric choices, shoe construction, how to dress well, wardrobe building, or menswear shopping recommendations.
---

# Die, Workwear! Knowledge Base

Derek Guy is one of the most respected voices in menswear. His blog covers tailoring, fit, fabrics, shoes, style history, and practical shopping advice.

## How to Use

When asked about menswear topics:

1. **Search the reference file** for relevant content:
   ```bash
   grep -i "neapolitan\|naples" references/articles.txt | head -50
   grep -i "shoulder" references/articles.txt | head -50
   ```

2. **Read relevant sections** from `references/articles.txt` — the file contains all 580+ articles concatenated with URL headers.

3. **Synthesize** Derek's insights for the user's question.

## Topics Covered

- **Suits & Tailoring** — Neapolitan, Savile Row, American sack suit, Japanese-Italian hybrids
- **Fit & Construction** — Shoulders, lapels, trouser rise, pleats, shirt collars
- **Shoes** — Bespoke shoemaking, Goodyear welt vs handwelted, shoe care, brand recommendations
- **Fabrics** — Wool, flannel, fresco, tweed, linen; mills like Fox Brothers, Loro Piana
- **Outerwear** — Parkas, field jackets, leather jackets, raincoats
- **Shopping** — Where to buy, Black Friday sales, value recommendations
- **Style Philosophy** — Building a wardrobe, dressing for context, breaking rules intentionally

## Quick Grep Patterns

```bash
# Tailoring styles
grep -i "neapolitan\|savile row\|english cut\|american sack" references/articles.txt

# Specific garments
grep -i "sport coat\|odd jacket\|blazer" references/articles.txt
grep -i "trouser\|pants\|denim\|jeans" references/articles.txt

# Footwear
grep -i "alden\|edward green\|boot\|loafer\|sneaker" references/articles.txt

# Fabrics
grep -i "flannel\|tweed\|fresco\|cashmere\|linen" references/articles.txt

# Shopping/brands
grep -i "no man walks alone\|drake\|armoury\|sale" references/articles.txt
```

## Sync

To update content:
```bash
sitefetch https://dieworkwear.com -m "/20*/**" -o references/articles.txt --concurrency 5
```

## Credits

All content © Derek Guy / dieworkwear.com  
This skill is for personal reference only.
