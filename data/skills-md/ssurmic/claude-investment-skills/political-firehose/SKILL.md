---
name: political-firehose
description: Daily monitor for political stock trades — Congress STOCK Act PTRs and executive OGE Form 278-T filings. Telegram alerts with trade details.
---

# Political Trade Firehose

Monitors stock trades by politicians and government officials, covering two separate disclosure systems:

| System | Who | Form | Timing | Format |
|--------|-----|------|--------|--------|
| STOCK Act PTR | Congress (Senate + House) | Periodic Transaction Report | Within 45 days | JSON/XML (scrapeable) |
| OGE Form 278-T | Executive (President, Cabinet) | Periodic Transaction Report | Within 30-45 days | PDF only |

## Politicians tracked (12)

**Executive (OGE 278-T)**:
- Trump (President) — 3,642 Q1 2026 trades
- Bessent (Treasury Secretary) — macro lens on policy
- Lutnick (Commerce Secretary)

**Senate (STOCK Act)**:
- Tuberville (R-AL) — P1, most active Senate trader
- Mark Kelly (D-AZ), Dan Sullivan (R-AK), Whitehouse (D-RI)

**House (STOCK Act)**:
- Nancy Pelosi (D-CA) — P1, legendary track record
- Austin Scott (R-GA), Dan Crenshaw (R-TX) — P1
- McCaul (R-TX), Gottheimer (D-NJ), Marjorie Taylor Greene (R-GA)

Edit `scripts/politician_registry.py` to add/remove.

## Cron

Three times daily, weekdays only:
- `13:00 UTC` ( 9 AM ET) — catches overnight + pre-market OGE filings
- `17:00 UTC` ( 1 PM ET) — mid-day
- `21:00 UTC` ( 5 PM ET) — post-close

## Manual run

```bash
# Test mode (no Telegram)
TEST_MODE=1 PRIORITY_MAX=2 python3 scripts/political_firehose.py

# Congress backtest (last 30 days, all trades)
python3 scripts/backtest_congress.py

# OGE PDF backtest (known Trump filings)
python3 scripts/backtest_oge.py
```

## OGE limitations

OGE 278-T PDFs report amount ranges (not exact prices):
- J = $1K–$15K  |  K = $15K–$50K  |  L = $50K–$100K  |  M = $100K–$250K
- N = $250K–$500K  |  O = $500K–$1M  |  P1 = $1M–$5M  |  P2 = $5M–$25M  |  P3 = $25M+

No exact trade prices. No transaction cost basis.

## State

`scripts/state.json` tracks seen Congress trade keys and OGE PDF URLs.
Pre-seeded with 4 known Trump 278-T PDFs (Oct 2025, Oct 2025, Feb 2026, May 2026) to avoid flood on first run.

## Adding a politician

1. Find their name exactly as listed on disclosures (check efdsearch.senate.gov or disclosures.house.gov)
2. Add to `POLITICIANS` list in `politician_registry.py`
3. Set `system="CONGRESS"` or `system="OGE"` and correct `chamber`

---

## Example Telegram alerts

These are real alerts rendered from backtest data. Data is objective disclosure records — not investment recommendations.

### OGE 278-T — Trump Q1 2026 (filed 2026-05-08)

> Source: OGE Form 278-T, 2,707 parsed transactions (of 3,642 total in filing).  
> ORCL (Oracle Corp) bought 3/17/2026, amount range P1 = $1M–$5M, as disclosed.

```
🏛 *OGE 278-T*  ⚡ NEW FILING

👤 *Donald J. Trump*  🔴 `R`
🎯 President of the United States
🗓 Filed: `5/8/2026`  |  *2,707* total transactions  (*2,415* buys / *292* sells)

🟢 *TOP BUYS* (2,415 total):
  🟢 `MSFT`   Microsoft Corp                *$5M–$25M*  _3/17/2026_
  🟢 `NOW`    ServiceNow Inc                *$1M–$5M*   _2/10/2026_
  🟢 `NVDA`   Nvidia Corp                   *$1M–$5M*   _2/10/2026_
  🟢 `ORCL`   Oracle Corp                   *$1M–$5M*   _3/17/2026_
  🟢 `QCOM`   Qualcomm Inc                  *$1M–$5M*   _1/12/2026_
  🟢 `HOOD`   Robinhood Markets             *$1M–$5M*   _2/10/2026_
  _...+2,409 more buys_

🔴 *TOP SELLS* (292 total):
  🔴 `VIG`    Vanguard Div Appreciation ETF *$5M–$25M*  _?_
  🔴 `META`   Meta Platforms                *$5M–$25M*  _?_
  🔴 `AMZN`   Amazon.com Inc                *$1M–$5M*   _?_
  🔴 `MSFT`   Microsoft Corp                *$1M–$5M*   _?_
  🔴 `GOOGL`  Alphabet Inc                  *$1M–$5M*   _?_
  _...+287 more sells_

📎 [OGE 278-T PDF](https://extapps2.oge.gov/...)
_3,642 trades in Q1 2026. MSFT $5M-25M top buy; ORCL/NVDA/HOOD among $1M-5M buys; VIG/META top sells_
```

**Note on ORCL**: Oracle Corp (`ORCL`) appears as a $1M–$5M purchase on 3/17/2026 in Trump's Q1 2026 278-T. This is public mandatory disclosure data under the Ethics in Government Act — presented here as raw signal, same as every other trade in the filing.

---

### STOCK Act PTR — Congress (House example)

> Source: House disclosures XML + PDF, filed 2026-05-13.

```
🏛 *STOCK Act PTR*  ⚡ NEW FILING

👤 *Rep. Mary Peltola*  🔵 `D-AK`
🎯 U.S. House of Representatives
🗓 Filed: `2026-05-13`  |  *3* transactions

🟢 `AAPL`  Apple Inc - Common Stock        *$1K–$15K*  _2026-05-13_
🟢 `NVDA`  NVIDIA Corporation              *$1K–$15K*  _2026-05-13_
🔴 `MSFT`  Microsoft Corporation           *$15K–$50K* _2026-05-12_

📎 [PTR Filing](https://disclosures-clerk.house.gov/...)
```

---

### Alert field reference

| Field | Source | Notes |
|-------|--------|-------|
| `Filed` date | Filing metadata | Date OGE/House received the form |
| Transaction date | Per-row data | Date the trade actually executed; may be `?` if not in PDF |
| Amount | OGE letter code → range | Never exact; ranges only (J=$1K–$15K … P2=$5M–$25M) |
| Ticker | Extracted from asset name | Best-effort regex; may be blank for funds/options |
| Buys/sells | Transaction type field | Purchase=🟢, Sale=🔴 |
