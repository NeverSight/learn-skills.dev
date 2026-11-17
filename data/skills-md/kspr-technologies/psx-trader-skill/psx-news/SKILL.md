---
name: psx-news
description: >-
  News Monitor for the Pakistan Stock Exchange. Reads the PSX notices of every
  stock you watch (financial results, board meetings, material information,
  dividends, insider trades) and Pakistani business news (Business Recorder,
  Dawn, Express Tribune, ProPakistani), and shows how far each stock is from
  its last close, with a flag at the daily price limit. Shows only what is new
  since the last check, newest first, in Karachi time. Tags each item (results,
  dividend, board, material, insider, deal, halt, macro...) and never repeats
  one. Use when the user says "any news on OGDC", "why is this moving", "what's
  the news on my watchlist", "morning briefing", "check the PSX notices", "any
  results today", "KSE-100 today", "why is the KSE-100 down", "did anything
  break", or after /psx-scanner finds setups.
argument-hint: "[tickers]"
---

# psx-news

A chart can look good and still be about to jump on a results day, a halt or
a court case. Before a setup becomes a trade, this skill reads the PSX notices
and the news for every stock on the watchlist. It shows only what is new.
It also shows how far each stock has moved today, so a story and a move sit
side by side.

Tool in this folder (standard library Python, no keys):

```bash
python3 "${CLAUDE_SKILL_DIR}/news.py"                          # watchlist + plan + portfolio
python3 "${CLAUDE_SKILL_DIR}/news.py" --tickers OGDC HUBC --hours 12   # or --tickers OGDC,HUBC
python3 "${CLAUDE_SKILL_DIR}/news.py" --market                 # also Pakistani SBP, IMF, budget and KSE-100 news
python3 "${CLAUDE_SKILL_DIR}/news.py" --no-notices --json      # headlines only, as JSON
```

## What it reads and writes

| file / feed | what |
| --- | --- |
| `--tickers`, else `psx/watchlist.json` | the scanner's hits (psx-scanner) |
| `psx/plan.json` | the trade you are planning (psx-exit) |
| `psx/portfolio.json` | what you hold (psx-broker records fills there) |
| `psx/universe.txt` | company names, so "Lucky Cement" finds LUCK (psx-scanner writes it) |
| `psx/data/company/<SYM>.html` | a company page you saved: its 3 notice tabs, the price, the last close and today's price limits |
| `https://dps.psx.com.pk/company/<SYM>` | the same page from the PSX site, only with `"psx_site": true` in `psx/config.json`. Then the tool asks the site first. The saved page is used only when the site fails, with a note. |
| `psx/data/mkt_summary/YYYY-MM-DD.Z` | the daily closing file: the move when there is no company page |
| RSS feeds | Business Recorder (markets; business and finance), Dawn business, Express Tribune business, ProPakistani business. Change them with `"news_feeds"` in `psx/config.json` or `--feeds`. |
| `psx/data/news/<name>.xml` | saved feeds, read with `--offline` or `--now` |
| `psx/state/news.json` | what has been shown (kept 30 days) |

- The feeds are always on. They are made for readers, and this is your own use.
- The PSX site is off until you turn it on. PSX's terms do not allow tools
  without its written permission (ask marketdatarequest@psx.com.pk).
- With the site off, save the company page with your browser. When a page is
  missing, the tool says which file to save where.
- `--offline` never uses the network. It reads only `psx/data/` (or `--data`).
- `--now "2026-10-29 17:00"` is a replay at that Karachi time. Like
  `--offline`, it reads only `psx/data/`. The site only has today.
- `--tickers` takes `OGDC HUBC` or `OGDC,HUBC`. A symbol is capitals,
  digits and a dash. Any other sign stops the run before any request.

## The rules

- **Headlines are leads, not facts.** Before telling the user something
  happened, read the story or the notice. Quote the source and link it.
  Never sum up a story you could not read: say so.
- **With the site off, never fetch a PSX link yourself.** A notice link is on
  dps.psx.com.pk. Ask the user to open it in their browser and save it as
  `psx/data/docs/<id>.pdf` (an image as `<id>.gif`), or paste a screenshot.
  `<id>` is the number in the link. The tool prints this line under the
  notices. News sites (Dawn, Business Recorder) are fine to open.
- **Notices beat headlines.** A PSX notice is what the company told the
  exchange. If a notice and a headline disagree, the notice wins.
- **A notice has a date, not a time.** PSX shows only the day. A notice from
  today may be from before the open or after it. Say so.
- **Each tab shows only its 5 newest notices.** A busy company can push a
  notice off its page within days. So check every day.
- **Say what it touches.** Every item lists the tickers it touches and its
  tags: results, dividend, board, material, insider, rights, bonus, deal,
  capital, people, legal, regulatory, risk, halt, macro, analyst.
- **How a story finds a stock.** The symbol in capitals as a whole word,
  anywhere in the story (DEMO, not "Demo"). A short name in capitals counts
  the same way: OGDCL for OGDC, PTCL for PTC, SNGPL for SNGP, SSGCL for SSGC.
  Or the company name in the title or the first lines: without "Limited"
  ("Demo Industries"), or a common name from a short list (Hubco for HUBC,
  Lucky Cement for LUCK).
- **Some names do not count.** A broker quoted as the source ("AHL said",
  "Arif Habib Limited said"). A name inside a longer name ("Pakistan Petroleum
  Dealers Association" is not PPL, "Habib Bank AG Zurich" is not HBL).
- **PSX is the exchange too.** Most market stories name PSX or "Pakistan
  Stock Exchange". So for the PSX stock, only its own notices and "PSX
  Limited" count.
- **`!` marks news that can move a price at once:** financial results,
  material information, a rights issue, a suspension or non-compliance, a
  merger or takeover, a market halt.
- **Some notices look like results but are not.** "Board Meeting Other Than
  Financial Results" is a board meeting: no `!`. "Other than Right Offer" is
  not a rights issue. A Board Meetings notice about results gets the tags
  results and board, but no `!`: the meeting is often still to come.
- **MOVING** marks a stock 3% or more from its last close (`--move-pct`).
  A move with no story is worth a word too.
- **AT UPPER LIMIT** or **AT LOWER LIMIT** means the price sits at today's
  limit: 10% from the last close (Rs 1 when the last close is under Rs 10).
  At a limit there may be no buyers, so a stop may not fill.
- **Free PSX prices are about 5 minutes late.** The price line shows the
  page's "As of" time. A daily file gives the official close of a past day.
- **"no trade since"** means the stock has not traded since that time. The
  move is against the newest last close. The page's own change is from that
  older day: do not report it as today's move.
- **No predictions.** Report what was published and how far the price is from
  the last close. Never say what the stock will do next.

## Steps

1. Run the check: `python3 "${CLAUDE_SKILL_DIR}/news.py"`. Exit code 1 means
   nothing new. `--all` shows items already seen. `--json` gives everything
   as JSON. `--dry-run` leaves the state alone.
2. Read the items that matter first: every `!`, anything tagged results,
   halt, legal, regulatory or risk, and every MOVING or AT ... LIMIT line.
3. To read a PSX notice with the site off, ask the user to open its link in
   their browser and save it as `psx/data/docs/<id>.pdf`, or paste a
   screenshot. Do not fetch it yourself. With `"psx_site": true` you may open it.
4. Write a short brief, per ticker: what happened, the source and the link,
   the move, and one line on why it matters to the setup (for example
   "results come out tomorrow: the price can jump at the open").
5. If a story changes the picture, say so before `/psx-entry` and `/psx-exit`:
   results inside the trade, a halt, a rights issue. Never act on a headline
   alone.

For "KSE-100 today" or "why is the KSE-100 down", run with `--market`. It
works with no tickers. It adds Pakistani market news only: foreign wire
stories (the Indian rupee, Wall Street, gold on US data) are left out. The
tool does not give the index level: quote it from the stories you read.

During the session: `/loop 15m /psx-news`. Or a task each morning before the
open, with `--market` for the SBP, IMF, budget and KSE-100 news.
Business Recorder keeps only about half a day of news, so check a few times a
day. On a Monday, `--hours 72` takes in Friday.

## Example

The sample market (made up: DEMO is not a real company). Thursday 2026-10-29,
checked at 5:00 PM, after the close:
`news.py --tickers DEMO --offline --now "2026-10-29 17:00"`

```
DEMO      101.60 +3.25% vs the last close 98.40 at 3:49 PM PKT  MOVING

PSX notices (PSX gives a date, not a time):
  2026-10-29  DEMO    Disclosure of Interest by a Director CEO, or Executive of a listed company and their Spouses and the Substantial Shareholders u/c 5.6.1.(d) of PSX Regulations
      tags: insider  https://dps.psx.com.pk/download/document/290210.pdf
! 2026-10-28  DEMO    Material Information
      tags: material  https://dps.psx.com.pk/download/document/290111.pdf
! 2026-10-27  DEMO    FINANCIAL RESULTS FOR THE QUARTER ENDED SEPTEMBER 30, 2026
      tags: results  https://dps.psx.com.pk/download/document/290000.pdf
  2026-10-27  DEMO    Board Meeting In Progress
      tags: board  https://dps.psx.com.pk/download/document/290005.pdf
To read a notice: ask the user to open its link in their browser and save it as psx/data/docs/<id>.pdf (an image as <id>.gif), or paste a screenshot. Do not fetch it yourself.

Headlines:
  2026-10-29 16:42 PKT  DEMO        Business Recorder  KSE-100 gains 1,265 points as banks and cement lead
      tags: results, macro  https://www.brecorder.com/news/40447120/kse100-gains-1265-points-as-banks-and-cement-lead
  2026-10-28 20:14 PKT  DEMO        Dawn               Demo Industries wins Rs1.2bn packaging order
      tags: deal  https://www.dawn.com/news/2040702/demo-industries-wins-rs12bn-packaging-order
Checked 2026-10-29 17:00 PKT. Page prices are about 5 minutes late. Headlines are leads, not facts: read the story or the notice before acting. Not financial advice.
```

- DEMO is 3.25% over its last close, so it is MOVING. The page is as of 3:49 PM.
- The site is off, so the line under the notices says how to read one: the
  user opens it. With `"psx_site": true` that line is not printed.
- Two `!` notices: the quarter results (10-27) and a "Material Information"
  notice (10-28). The notice is a contract worth about Rs 1.2 billion.
- The Dawn story says "Demo Industries": the name matches without "Limited".
- The Business Recorder story names DEMO in capitals. It also names OGDC and
  HUBC. They show too when you watch them.
- Business Recorder also ran "Banks may lead earnings growth, says brokerage".
  It quotes AHL, a broker, as the source. So it matches no stock.

The brief: "DEMO posted its quarter results on October 27. On October 28 it
told PSX about a contract worth about Rs 1.2 billion (Dawn has the story). It
closed 3.25% up, inside its limits. An insider notice came on October 29: open
it in your browser, or run /psx-insiders, to see who traded." When a ticker
has no news, say so. Keep the brief short.

## What it never does

- Never makes up a story, a quote or a number, and never adds to one.
- Never trades on news, and never tells the user to buy or sell because of a
  headline.
- Never floods a server: one request per feed, at least 1.5 seconds between
  requests, and the PSX site only when you turned it on.

## Safety

Education and tooling, not financial advice. This skill only reads and
reports. Nothing in this pack places an order. `/psx-broker` shows the
order first. It prints the line to type into the broker app only after
`/psx-risk` passes that exact order and the user types an explicit yes for it.
