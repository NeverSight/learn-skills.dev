---
name: maccabi-pharm-search
version: 2.0.0
description: Search for medications and check real-time stock availability at Maccabi pharmacies in Israel. Use when searching for drugs like "nurofen", "acamol/אקמול", "advil", or finding nearby pharmacy branches with stock. Supports Hebrew and English drug names. מכבי פארם, תרופות, מלאי, בית מרקחת.
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-maccabi-pharm-search
metadata: {"openclaw": {"emoji": "💊", "os": ["darwin", "linux"], "requires": {"bins": ["node"]}}}
---

# Maccabi Pharmacy Stock Check

Search medications and check **real-time stock availability** at Maccabi Pharm locations across Israel.

> **Disclaimer**: This is an unofficial tool, not affiliated with or endorsed by Maccabi Healthcare Services. Stock information queries APIs that power the website and may not reflect actual availability. Always call the pharmacy to confirm stock before visiting. This tool is provided "as is" without warranty of any kind. Use at your own risk.

## Quick Start

```bash
# 1. Search for medication (get the Largo code)
node {baseDir}/scripts/pharmacy-search.js search "nurofen"
# Returns: Largo Code 58299 for NUROFEN LIQUID 20 CAP

# 2. Check which pharmacies have it in stock
node {baseDir}/scripts/pharmacy-search.js stock 58299
# Returns: Pharmacies with addresses, phones, stock status
```

## Commands

| Command | Description |
|---------|-------------|
| `search <query>` | Find medications, get Largo codes |
| `stock <largo_code> [city]` | Check real-time inventory at pharmacies |
| `branches maccabi [city]` | Get pharmacy locations |
| `cities` | Show all 51 available city codes |
| `test` | Quick functionality check |

## Search Examples

```bash
# Hebrew searches
node {baseDir}/scripts/pharmacy-search.js search "אקמול"
node {baseDir}/scripts/pharmacy-search.js search "נורופן"

# English searches
node {baseDir}/scripts/pharmacy-search.js search "acamol"
node {baseDir}/scripts/pharmacy-search.js search "nurofen"
```

## Stock Check by City

```bash
# Tel Aviv (default, city code 5000)
node {baseDir}/scripts/pharmacy-search.js stock 58299

# Jerusalem (city code 3000)
node {baseDir}/scripts/pharmacy-search.js stock 58299 3000

# Haifa (city code 4000)
node {baseDir}/scripts/pharmacy-search.js stock 58299 4000
```

## City Codes

Common examples (51 cities supported):

| City | Code |
|------|------|
| Tel Aviv | 5000 (default) |
| Jerusalem | 3000 |
| Haifa | 4000 |
| Beer Sheva | 9000 |
| Bat Yam | 6200 |
| Netanya | 7400 |

Run `cities` command to see all 51 available city codes.

## Output Examples

**Search results:**
```
NUROFEN LIQUID 20 CAP
  Largo Code: 58299 (use this for stock check)
  Prescription: No
```

**Stock results:**
```
=== Stock Summary ===
  In Stock: 6 pharmacies
  Low Stock: 0 pharmacies
  Out of Stock: 1 pharmacies

=== Pharmacies with Stock ===
מכבי פארם-ת"א-בלפור 10
   בלפור 10, תל אביב - יפו
   03-9193013
   Distance: 0.6 km
```

## Notes

- Stock information queries APIs that power the website
- Only shows Maccabi Pharm locations (not other pharmacy chains)
- Largo code from search is required for stock check
- Data provided "as is" without warranty
