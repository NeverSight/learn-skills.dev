---
name: psx-analyst
description: >-
  The Results Analyst for the Pakistan Stock Exchange. Reads a company's
  results from its PSX company page (saved with your browser, or the PSX site
  when you allow it): sales (for a bank, mark-up earned and total income),
  profit after tax, EPS and margins, quarter by quarter, each against the same
  quarter a year back, and the last full year. Flags a quarter label that looks
  wrong, derived quarters and one-off items. Finds the newest results notice
  and the next board meeting. Use when the user says "how did OGDC's results
  look", "what changed this quarter", "is profit growing", "compare margins",
  "when is the next board meeting", "are results due this week", or before
  trading a stock around its results.
argument-hint: "[symbols]"
---

# psx-analyst

Results move PSX stocks a lot. They often come out during the session.
This skill reads the numbers on the company's PSX page and lines them up,
quarter by quarter. Then it says plainly what changed.

For a day trader it answers two questions before a trade:
- What did the last results say?
- Does the next board meeting (the next results) fall inside this trade?

Tool in this folder (standard library Python, no keys):

```bash
python3 "${CLAUDE_SKILL_DIR}/facts.py" --help
```

- It reads your data folder: `psx/data/` (or `--data DIR`).
- It uses the PSX site only when `psx/config.json` has `"psx_site": true`.
- Turn that on only if PSX has given you permission (marketdatarequest@psx.com.pk).
- With the site on, it asks the site first. If the site does not answer, it reads the saved page and says so.
- `--offline` never touches the network. Nor does `--now`: a replay reads only the data folder.

## What it reads and writes

| file | reads or writes | what |
| --- | --- | --- |
| `psx/data/company/<SYM>.html` | reads | a saved `https://dps.psx.com.pk/company/<SYM>` page |
| `psx/data/docs/<id>.txt` or `<id>.pdf` | reads | a saved notice, for the meeting date (a PDF needs `pdftotext`) |
| `psx/config.json` | reads | `"psx_site"` only |
| `psx/metrics.json` | writes, with `--metrics` | one row per company, merged by symbol |

- The company page holds 4 fiscal years and 4 quarters: the 3 newest, then the same quarter a year back.
- It also holds a few ratios and the 5 newest notices of each kind (results, board meetings, others).
- Figures are in Rs thousands, except EPS (rupees). They are unconsolidated.
- `metrics.example.json` in this folder is a run on the sample market. It is made up.
- The tool does not fetch reports or briefing calls. If the user pastes one, read it.
  Sum up what management said changed: payouts, margins, demand, plans.

## The rules

- **The page's numbers first.** The table is what the PSX page shows.
  Use the results notice for more (a payout, the consolidated figures). Say which number came from where.
- **Compare like with like.** Growth is against the same quarter a year back.
  The quarter before is shown too, but many businesses are seasonal.
- **Check the label.** Labels follow the fiscal year end. Many PSX companies end in June, so Q1 is July to September.
  A label that does not fit the year end is flagged: "the label looks wrong; check the results notice".
  Example: FFC's page shows "Q1 2027" for July to September 2026, but FFC's year ends in December.
- **Say what is derived.** The page has no Q4 column. Q4 = the year minus Q1, Q2 and Q3 of the same fiscal year,
  when all four are on the page. It is marked derived. Derived EPS is approximate.
- **Unconsolidated.** The page shows the company alone, not its group. A notice may also give group (consolidated)
  figures. Never mix the two.
- **Banks.** A bank shows Mark-up Earned and Total Income, not sales. It has no gross margin: blank, not zero.
  Its net margin is profit / mark-up earned, like the page's own ratio.
- **Flag one-offs.** Profit above sales, or profit growth 20 points or more above sales growth:
  check for one-off items (other income, a gain, a tax item). For a bank the tool uses total income growth.
- **Say when the page lags.** When the newest results notice is for a later period than the page's figures,
  the tool prints a NOTE with the link. Read the notice before you sum up.
- **Board meetings.** The date comes from a board notice's saved text ("will be held on ...").
  The tool reads the newest notice first. If it gives no date, an older notice counts while its meeting is ahead.
  Then the tool says that a newer notice can change the date or time.
  AGM notices are left out. "Board Meeting In Progress" means the board meets that day.
  A meeting "other than financial results" is not for results. The tool shows it on its own line.
  The closed period is the time when directors and executives may not trade the shares.

## Steps

1. Run it for the stocks in question (or the symbols on `psx/watchlist.json`):

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/facts.py" OGDC
   python3 "${CLAUDE_SKILL_DIR}/facts.py" OGDC HBL LUCK --metrics psx/metrics.json
   ```

   `--json` gives everything for a machine. `--now "2026-10-29 16:00"` sets the time (Karachi time).
2. If a page is missing, save it with your browser as `psx/data/company/<SYM>.html`.
   For the board meeting date, the tool needs the notice in `psx/data/docs/<id>.pdf` (the id is in the link).
   With the site off, never fetch a PSX link yourself. The tool prints what to say:
   "Ask the user to open <link> in their browser and save it as psx/data/docs/<id>.pdf, or paste a screenshot."
   Many PSX PDFs are scans with no text. Then the tool says so. Ask the user for a screenshot.
3. Read the results notice when the numbers need more, or when the tool prints a NOTE.
   With the site off, the same rule holds: the user opens the link, then saves the file or pastes a screenshot.
4. Write the summary in plain words:
   - one line on the quarter (sales, profit, EPS, growth);
   - one line on margins;
   - one line on anything odd (a wrong label, a derived quarter, a one-off, a page that lags);
   - the links.
   Use real numbers. No adjectives the numbers do not support.
5. If the next board meeting falls inside the planned trade, say it before `/psx-exit` sets the stop.
   Results can come out during the session, and the price can jump to its daily limit.
   A stop does not protect against a jump: the price can open, or trade, past it.

## Example: DEMO on Thu 2026-10-29

The sample market is made up. DEMO ("Demo Industries Limited") is not a real company.
Run after the close:

```bash
python3 "${CLAUDE_SKILL_DIR}/facts.py" DEMO --offline --data tests/fixtures/psx-market --now "2026-10-29 16:00"
```

It prints:

```text
Demo Industries Limited (DEMO), MISCELLANEOUS. Fiscal year ends in June.
Source: the saved PSX company page (page time Thu 2026-10-29 3:52 PM PKT).
Rs thousands, except EPS in rupees.

quarter  ends             sales   profit   EPS  net margin
Q1 2027  2026-09-30  10,210,451  838,074  3.35       8.21%
Q4 2026  2026-06-30  10,381,554  788,997  3.16       7.60%  derived
Q3 2026  2026-03-31   9,612,550  730,554  2.92       7.60%
Q2 2026  2025-12-31   9,420,299  715,943  2.86       7.60%
Q1 2026  2025-09-30   9,035,797  686,721  2.75       7.60%

What changed:
  - Q1 2027 (Jul to Sep 2026) against Q1 2026, a year back: sales +13.00%, profit +22.04%, EPS +21.82% (3.35 against 2.75).
  - Net margin 8.21% (profit / sales). A year back: 7.60%.
  - Against the quarter before, Q4 2026 (derived): sales -1.65%, profit +6.22%. Many businesses are seasonal: look at the year-back change first.
  - Last full year, 2026 (to 2026-06-30): sales 38,450,200, profit 2,922,215 (Rs thousands), EPS 11.69. Against 2025: sales +13.00%, profit +22.83%, EPS +22.79%.
  - The year's net margin 7.60%, gross margin 24.85% (from the page's ratios).
  - Last 4 quarters (one derived): sales 39,624,854, profit 3,073,568 (Rs thousands), EPS about 12.29.
  - On the page: price 101.60, P/E (TTM) 8.27.

Check:
  - Figures are unconsolidated: the company alone, not its group.
  - Q4 2026 is derived: the year 2026 minus Q1, Q2 and Q3 on the page. Its EPS is approximate.

Results notice: Tue 2026-10-27, FINANCIAL RESULTS FOR THE QUARTER ENDED SEPTEMBER 30, 2026
  https://dps.psx.com.pk/download/document/290000.pdf
  Its text (docs/290000.txt) shows the same numbers as the page.
Last board meeting: Tue 2026-10-27 (Board Meeting In Progress).
Next board meeting: Tue 2026-11-03 at 11:00 AM PKT (in 5 days).
  From the notice of Tue 2026-10-20 (NOTICE OF BOARD MEETING), text in docs/289306.txt.
  It says: "will be held on November 3, 2026 at 11:00 a.m."
  For the period ended 2026-09-30, the consolidated accounts.
  Closed period: 2026-10-27 to 2026-11-03 (today is inside it).
  https://dps.psx.com.pk/download/document/289306.pdf
```

A summary from it:
- Q1 2027 (July to September 2026): sales +13.00% against a year back, profit +22.04%, EPS 3.35 (+21.82%).
- Net margin 8.21%, up from 7.60% a year back. The year to June 2026: EPS 11.69.
- Q4 2026 is derived, so its EPS (3.16) is approximate.
- The next board meeting is Tue 2026-11-03 at 11:00 AM PKT, for the consolidated accounts.
  A day trade on 10-29 that is flat by 15:20 is not exposed to it. A hold to 11-03 is.

## What it never does

- Never says a stock is cheap, expensive, a buy or a sell. It reports what the page shows.
- Never invents a number the page does not have, or a quarter it cannot derive.
- Never guesses what a scanned notice says. It says the notice is a scan and gives the link.
- Never uses the PSX site unless `"psx_site": true` is in your config, never with `--offline` or `--now`,
  and never faster than one request every 1.5 seconds.
- With the site off, never tells Claude to open a PSX link. It asks the user to save the file instead.

## Safety

Education and tooling, not financial advice. This skill only reads results.
Nothing in this pack places an order. `/psx-broker` shows the order first. It
prints the line to type into the broker app only after `/psx-risk` passes that
order and the user types an explicit yes for it. The user places it in their own
broker's app.
