---
name: 13f-firehose
description: Daily monitor for new 13F-HR filings from famous funds. Telegram alerts with NEW/ADDED/CLOSED diff vs. prior quarter.
---

# 13F Firehose

Scans SEC EDGAR twice daily for new 13F-HR filings from a curated registry of famous funds. Each new filing → Telegram alert with diff vs. prior quarter.

## Funds tracked (17)

**P1 (alert immediately)**: Leopold (Situational Awareness), NVIDIA Corp, Buffett (Berkshire), Ackman (Pershing), Loeb (Third Point), Tepper (Appaloosa), Soros, Burry (Scion), Englander (Millennium)

**P2**: RenTech, Bridgewater, Tiger Global, Coatue, Lone Pine, Marks (Oaktree)

**P3**: Wood (ARK), Einhorn (Greenlight)

Edit `scripts/fund_registry.py` to add/remove.

## Cron

Three times daily, weekdays only (US business hours):
- `13:00 UTC` (9 AM ET) — morning, catches overnight + pre-market filings
- `17:00 UTC` (1 PM ET) — midday filings
- `21:00 UTC` (5 PM ET) — post-close filings

13F deadlines: **Feb 14 / May 15 / Aug 14 / Nov 14** (45 days after quarter-end).

## Manual run

```bash
# Test (no Telegram)
TEST_MODE=1 PRIORITY_MAX=1 FORCE_RESCAN=1 python3 scripts/13f_firehose.py

# One CIK
python3 scripts/edgar_13f.py 2045724
```

## Alert format

NEW positions ($5M+ min) | ADDED (>+20% shares) | CLOSED | Top 10 holdings with % AUM | EDGAR link

## Adding a fund

1. Find CIK: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=NAME&type=13F-HR`
2. Add to `FUNDS` list in `fund_registry.py`
3. Seed state to avoid first-run flood: see `scripts/13f_firehose.py` header

## State

`scripts/state.json` tracks `seen[cik] = accession`. Committed back by GH Actions after each run.

To force re-alert one fund:
```bash
python3 -c "import json; s=json.load(open('scripts/state.json')); del s['seen']['2045724']; json.dump(s, open('scripts/state.json','w'), indent=2)"
```
