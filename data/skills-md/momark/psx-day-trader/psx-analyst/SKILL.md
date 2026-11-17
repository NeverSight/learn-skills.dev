---
name: psx-analyst
description: >-
  PSX Analyst. For one symbol, lists every quarterly, half-year and
  annual financial report PSX Data Portal has links for (going back to
  2013-14 for mature issuers), scrapes recent dividend/payout history,
  and flags the latest report's recency so you know if the company's
  numbers are current or a year stale. Does not read PDFs - it hands
  you the direct financials.psx.com.pk URL so you can open them in
  your browser. Use when the user says "fundamentals for OGDC", "when
  was HUBC's last report", "OGDC dividend history", "latest annual
  for LUCK", "has ENGROH posted Q3", or wants a sanity check before
  swinging a position.
argument-hint: "SYMBOL [--latest-only] [--kind annual|quarterly|all] [--dividends]"
---

# psx-analyst

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/facts.py" OGDC                            # all reports listed
python3 "${CLAUDE_SKILL_DIR}/facts.py" HUBC --latest-only              # just the most recent
python3 "${CLAUDE_SKILL_DIR}/facts.py" LUCK --kind annual              # annuals only
python3 "${CLAUDE_SKILL_DIR}/facts.py" OGDC --dividends                # payout history too
python3 "${CLAUDE_SKILL_DIR}/facts.py" OGDC --json
```

Flags: `--offline PATH`, `--out psx/analyst/{SYM}.json`.

## Output

`psx/analyst/{SYMBOL}.json`:
```json
{
  "symbol": "OGDC",
  "latest_report": {
    "kind": "Quarterly", "period_ended": "2026-09-30",
    "posted": "2026-10-28",
    "pdf": "https://financials.psx.com.pk/lib/DownloadPDF.php?id=OGDC-Q1-2026"
  },
  "latest_report_lag_days": 20,
  "reports": [
    {"kind": "Annual", "period_ended": "2025",
     "posted": "2025-10-07",
     "pdf": "https://financials.psx.com.pk/lib/DownloadPDF.php?id=OGDC-ANNUAL-2024"}
  ],
  "dividends": [
    {"date_ex": "2026-09-30", "rate_pct": 35, "kind": "Cash"},
    ...
  ]
}
```

`latest_report_lag_days` is how old the most recently posted report
is. For a liquid KSE-100 issuer that is usually ≤ 60 days after
quarter-end. A value > 120 days means the company is late on filing
and the price may be moving on thin information.

## PDFs stay on PSX

This skill records URLs and dates, not the PDF bytes. The actual
income statement, balance sheet, cash flow and management discussion
live on `financials.psx.com.pk`. Open them there.
