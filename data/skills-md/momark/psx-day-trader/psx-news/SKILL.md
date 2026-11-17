---
name: psx-news
description: >-
  PSX News. Pulls the latest corporate announcements from the PSX Data
  Portal's /announcements/companies page (dividends, book closures,
  financial-result disclosures, directors' interest, material information,
  general meetings) and flags items for the symbols on your psx-scanner
  watchlist. Keeps a rolling 30-day log at psx/state/news.json with dedupe
  by document id, so you only see new announcements since the last run.
  Use when the user says "scan PSX news", "what announcements came out",
  "any material info on OGDC", "news for my watchlist", "dividend
  announcements", "book closures", or right after /psx-scanner before
  /psx-entry.
argument-hint: "[--symbols SYM,...] [--since YYYY-MM-DD] [--kind material|dividend|meeting|all]"
---

# psx-news

Pulls the latest corporate announcements from the PSX Data Portal and flags
the ones that touch symbols on your watchlist. Announcements are what
companies are legally obliged to disclose: dividends, directors' changes,
material information, meetings, financial results, Shariah disclosures.
They move prices. They are not a prediction and most of them are routine.

`${CLAUDE_SKILL_DIR}` below is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/news.py"                          # all watchlist symbols, since last run
python3 "${CLAUDE_SKILL_DIR}/news.py" --symbols OGDC,HUBC      # specific symbols
python3 "${CLAUDE_SKILL_DIR}/news.py" --since 2026-11-10       # cutoff date
python3 "${CLAUDE_SKILL_DIR}/news.py" --kind material          # only Material Information
python3 "${CLAUDE_SKILL_DIR}/news.py" --kind dividend          # dividends + book closures
python3 "${CLAUDE_SKILL_DIR}/news.py" --kind meeting           # AGM / EGM / briefings
```

Flags: `--offline PATH` (points PSX_FIXTURES_DIR at a captured folder),
`--limit 100`, `--json` (print the full list to stdout).

## State

`psx/state/news.json`:
```json
{
  "fetched_at": "2026-11-17T09:12:03+05:00",
  "seen_ids": ["289296", "289294", "289293", ...],
  "items": [{
    "doc_id": "289296",
    "date": "2026-11-16", "time": "15:15",
    "symbol": "AKD-FUNDS", "name": "AKD Opportunity Fund",
    "title": "Quarterly Financial Statements ...",
    "kind": "financial_result", "revoked": true,
    "image_url": "/download/image/289296-1.gif",
    "pdf_url": "/download/document/289296.pdf"
  }, ...]
}
```

30-day rolling window; older items are pruned on each run.

## Kind classification

Rough keyword buckets applied to the title:

- `material` — contains "Material Information"
- `dividend` — contains "Dividend", "Payout", or "Book Closure"
- `meeting` — contains "General Meeting", "AGM", "EGM", "Briefing"
- `financial_result` — contains "Quarterly", "Annual", "Half-Year", "Interim Financial"
- `shariah` — contains "Shariah"
- `other` — anything else

## What it does NOT do

The announcement text and its PDF stay on the PSX Data Portal. This
skill records the title, date, symbol and the PDF URL. If you want the
body of an announcement you follow the `pdf_url` in your browser.
There is no official RSS or Atom feed; this is a courteous poll of the
public announcements page.
