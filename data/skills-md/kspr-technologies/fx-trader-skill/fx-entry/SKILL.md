---
name: fx-entry
description: >-
  Entry Timer for currency pairs and commodities at a MetaTrader broker, on
  both sides. Watches one setup and names the moment its rule is met: a
  finished daily bar that closes beyond the scanner's level (swing), or the
  first finished 5-minute bar that closes above or below the London opening
  range (day). Knows the FX day, the sessions, the CME break, holidays, early
  closes and the 9:00 PM PKT entry cut-off. Says waiting and how far,
  triggered with the time and the price, expired, late or closed, with the
  data age and news quiet times, and writes fx/entry.json for /fx-exit. It
  never places an order. Use when the user says "tell me when to get in",
  "watch gold", "has EURUSD broken out", "did it break the range", "entry
  signal", "time my entry", "check my watchlist", or after /fx-scanner and
  /fx-news, before /fx-exit.
argument-hint: "[check SYMBOL | watchlist | watch SYMBOL] [--side buy|sell] [--write]"
---

# fx-entry

The Entry Timer turns a setup into one moment: the bar that confirms it.
It waits for each bar to finish.

- A price that pokes past the level in the middle of a bar is not an entry.
- A bar that CLOSES beyond it is.
- Then it says the time and the price, writes them down for the Exit Planner, and stops.

It never buys or sells anything.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/entry.py" check XAUUSD                 # the scanner hit for gold
python3 "${CLAUDE_SKILL_DIR}/entry.py" check XAUUSD --write         # also save fx/entry.json
python3 "${CLAUDE_SKILL_DIR}/entry.py" check EURUSD --style day --side sell
python3 "${CLAUDE_SKILL_DIR}/entry.py" check USOIL --level 71.25 --side buy
python3 "${CLAUDE_SKILL_DIR}/entry.py" watchlist                    # every hit in fx/watchlist.json
python3 "${CLAUDE_SKILL_DIR}/entry.py" watch EURUSD --write --until 21:00
```

Flags:

- `SYMBOL`: an instrument key from your config, like `XAUUSD` or `EURUSD`. Small letters are fine.
- `--side buy|sell|both`: which side to report. Default `both` (or `buy` when sells are off).
- `--setup NAME`: pick the watchlist hit with this setup, like `breakout_20d`.
- `--style swing|day`: the style when the watchlist has no hit for the symbol.
- `--level PRICE`: swing only. Your own level instead of a scanner hit. It needs `--side buy` or `--side sell`.
- `--watchlist FILE`: the scanner file (default `fx/watchlist.json`).
- `--write` (check, watch): save `fx/entry.json` for fx-exit.
- `--every SECONDS` (watch): seconds between two looks while waiting for a 5-minute bar. 60 to 3600. Default 60.
- `--until HH:MM` (watch): stop at this Karachi time (`...Z` for UTC). A day watch stops at the entry cut-off anyway.
- The common flags: `--config`, `--data`, `--offline`, `--now "2026-07-23 12:41"` (Karachi time; also means offline), `--json`, `--quiet`.

## What it reads and writes

| file | what |
| --- | --- |
| `fx/watchlist.json` | read: the scanner's hits (`symbol`, `side`, `setup`, `level`, `fx_day`, `opening_range`) |
| `fx/config.json` | read: `allow_short`, `style`, `day_end`, `day` (range session and minutes, `no_entries_after`, `flat_by`), `news` (quiet minutes, impacts), `yahoo`, `calendar_url`, `holidays`, `early_closes`, `instruments` |
| `fx/data/yahoo/` | read and refreshed: 1-hour bars (swing, and the daily ATR), 5-minute bars (day). Yahoo, at least 2 seconds between requests |
| `fx/data/rolls.json` | read; a new futures roll is added |
| `fx/data/calendar/` | read; this week's calendar, at most one download an hour |
| `fx/entry.json` | written with `--write`: `symbol`, `side`, `style`, `setup`, `fx_day`, `status`, `level`, `opening_range`, `bar`, `price`, `triggered_at`, `distance`, `atr`, `data_age_min`, `rolls_applied`, `note`. Read by fx-exit |

It reads no plan, order, price or portfolio file.

## The rule

Swing (the default style):

- The level comes from the scanner hit, or from `--level`.
- The rule needs a FINISHED daily bar that closes beyond the level.
- A buy needs a close above the level. A sell needs a close below it.
- A day ends at 5:00 PM New York (2:00 AM PKT in summer, 3:00 AM PKT in winter).
- A setup lasts 3 FX days. With no close beyond the level by then, it has expired.

Day:

- The opening range is the first 15 minutes of the London session.
- That is 1:00 PM to 1:15 PM PKT in winter, and 12:00 PM to 12:15 PM PKT in summer.
- The rule needs the first finished 5-minute bar after the range that closes beyond it.
- A buy needs a close above the range high. A sell needs a close below the range low.
- Both sides are watched. The first side to close beyond the range wins.
- One trigger a day. Later closes do not reset it.
- No new day trades after 9:00 PM PKT (or 30 minutes before an early close).

For both styles:

- A close exactly at the level is not beyond it.
- A wick beyond the level is not a trigger.
- An incomplete opening range never triggers.

## What it says

The first line is one of five words:

- `WAITING`: the rule is not met yet. It says how far the last close is from the level.
- `TRIGGERED`: a finished bar closed beyond the level. It says the time and the price.
- `EXPIRED`: the setup is over. The close came too long ago, 3 days passed, the other side triggered first, or the range failed a filter.
- `LATE`: it is past the entry cut-off. No new day trades now.
- `CLOSED`: the market is closed (weekend, holiday, CME break), or there is no usable data.

Exit codes: 0 when triggered (and for `watchlist` when at least one hit triggered), 1 for waiting, expired, late or closed, 2 for an error.

## Prices and their age

- Yahoo gives the bid price. Your broker's buy price (the ask) is a little higher.
- FX prices on Yahoo are close to live, and close to your broker's price.
- Gold, silver, oil, gas and copper come from Yahoo futures prices. They are about 10 minutes late, and they are not your broker's price.
- Every price line says where the price came from and how old it is.
- When a futures contract rolls, Yahoo prices jump. The tool moves the scanner's level by the same amount, so the level stays on the same scale as the bars.

## Steps

For Claude:

1. Run `entry.py check SYMBOL` (or `entry.py watchlist`) after `/fx-scanner`, `/fx-news` and `/fx-calendar`.
2. Tell the user the status in one line.
3. To wait for a trigger: run `entry.py watch SYMBOL --write` in the background, or `check --write` on a `/loop` every 5 minutes. Keep the computer awake while it watches.
4. On a trigger, say the time, the price, the data age, and that nothing was placed. If the trigger is more than one bar old, say a late entry is a different trade.
5. Hand off to `/fx-exit` to set the stop and the target BEFORE anything is bought or sold.
6. Never run `/fx-broker` or any order step from a watch. Nobody is there to say yes.

## Example

These come from the made-up sample market in `tests/fixtures/fx-market/`. The prices are not real.

Swing (`check XAUUSD --write --offline --now "2026-07-17 09:02"`):

```
TRIGGERED: the daily bar of Thu 2026-07-16 closed at 2,431.60, above 2,418.40.
This is the moment the rule names. Nothing was placed.
XAUUSD  buy side (waits for a close above)  20-day high breakout.
That day ended Fri 2:00 AM PKT (5:00 PM New York). Daily ATR 28.054.
Yahoo price (gold futures), not your broker's price. Newest 2,433.40, 2 min
old.
Note: Gold rolls about now, by 2026-08-03 at the latest (Aug to Dec): Yahoo
prices jump then.
Note: Yahoo futures prices are about 10 minutes late.
Wrote fx/entry.json (triggered).
Next: set the stop and the target before any order:
python3 fx-exit/exit.py plan --write
```

Day (`check EURUSD --write --offline --now "2026-07-23 12:41"`):

```
TRIGGERED 12:40 PM PKT at 1.08452: the 12:35 PM bar closed below the range low 1.08480.
This is the moment the rule names. Nothing was placed.
EURUSD  sell side (waits for a close below)  opening-range breakdown.
London range Thu 12:00 PM PKT (3:00 AM New York) to 12:15 PM PKT: high
1.08640, low 1.08480, middle 1.08560 (3 of 3 bars). 5-minute ATR 0.00067.
No new day trades after 9:00 PM PKT (12:00 PM New York).
Yahoo price, close to your broker's price. Newest 1.08452, 1 min old.
Note: Main Refinancing Rate (EUR) at Thu 5:15 PM PKT (8:15 AM New York), High
impact, before the flat-by time. Spreads widen and stops can slip.
Wrote fx/entry.json (triggered).
Next: set the stop and the target before any order:
python3 fx-exit/exit.py plan --write
```

## Rules

- A signal is information. It is not an order and not a promise.
- One trigger per setup per day. The first close beyond the level counts.
- Never call a bar early. A bar that looks like it will close beyond the level is not a trigger until it has closed.
- Never move the level after the scan. Only a futures roll rescales it.
- A news quiet window is said in a note. fx-risk blocks new trades in it.
- A late entry is a different trade. Scan again instead.

## What it never does

- It never places an order, never sizes a trade and never sets the stop (fx-exit does).
- It never counts a bar that has not finished.
- It never tells the user to buy or to sell. It says what the rule saw.
- It never moves the level after the scan.
- It never runs fx-broker or any order step from a watch.
- It never uses the network with `--offline` or `--now`, or for prices with `"yahoo": false`.

## Safety

- Education and tooling, not financial advice. A PASS is a rules check, not a recommendation.
- Paper trading by default (`"paper": true`). Going live is the user's own decision, in their own config.
- Nothing in this pack places an order. fx-broker shows the order and waits. It prints the line to
  type into MetaTrader only after fx-risk passed that exact order in the last 5 minutes and the user
  typed an explicit yes for that one order in the chat. The user then places it in their own
  MetaTrader. If the user ever adds a broker tool that can place orders, set it to "Needs approval"
  (Customize > Connectors > tool permissions), never "Always allow".
- Both sides. A buy opens at the ask, a sell opens at the bid. A sell's stop is above the price.
  Sells are on by default; `"allow_short": false` turns them off.
- Leverage makes losses bigger, as fast as gains. Every order carries a stop loss (SL) and a take
  profit (TP).
- A stop is not a promise. Over a weekend, at big news or at a futures roll the price can jump past
  the stop, and the fill is worse than the stop.
- Most retail CFD accounts lose money: 74% to 89% of them in EU regulators' studies (ESMA, 2018).
- MetaTrader logins, passwords and PINs never go in the chat.
