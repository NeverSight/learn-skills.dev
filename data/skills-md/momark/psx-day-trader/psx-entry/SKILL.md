---
name: psx-entry
description: >-
  PSX Entry. Takes a symbol from the psx-scanner watchlist and watches
  intraday 5-minute bars (bucketed from PSX Data Portal ticks) for a
  precise entry: the first bar to close above the opening-range high (or
  below the opening-range low for a short), with a configurable confirm
  rule. Writes psx/entry.json with the entry price, time, and the exact
  bar that triggered it, so psx-exit, psx-budget and psx-risk have one
  clean price to size and plan against. Use when the user says "watch
  OGDC for an entry", "ORB entry on HUBC", "wait for a break on LUCK",
  "pullback entry on ENGROH", "when should I buy", "find me an entry
  point", or right after /psx-scanner orb.
argument-hint: "SYMBOL [--rule orb|pullback] [--long|--short] [--at HH:MM]"
---

# psx-entry

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/entry.py" OGDC                     # default: ORB long, now
python3 "${CLAUDE_SKILL_DIR}/entry.py" HUBC --rule orb --long   # explicit
python3 "${CLAUDE_SKILL_DIR}/entry.py" ENGROH --short           # ORB break-down
python3 "${CLAUDE_SKILL_DIR}/entry.py" LUCK --rule pullback     # pullback to OR high
python3 "${CLAUDE_SKILL_DIR}/entry.py" OGDC --at 10:15          # cut clock
python3 "${CLAUDE_SKILL_DIR}/entry.py" OGDC --or-minutes 15
```

Flags: `--or-minutes 15`, `--settle 60` (seconds after a bar's close
before trusting it), `--at HH:MM` and `--now "YYYY-MM-DD HH:MM"` (PKT)
for replay, `--offline PATH`, `--json`.

## Entry rules

**orb** (default). Builds the opening range from the first `--or-minutes`
after 09:32 PKT. For `--long`, triggers on the first 5-min bar that
*closes* above the range high (with volume > 0). For `--short`, first
bar to close below the range low. Pending bars (bars that have not
elapsed + the `--settle` grace) are ignored - a bar at 10:00 is only
considered final at 10:05:01 (bar close + 60s settle).

**pullback**. For `--long`, after a break above the OR high, waits for
a bar whose low re-tags the range high and then closes back above it.
Fires on the close of that confirming bar. For `--short`, mirror it.

## State

Writes `psx/entry.json`:
```json
{
  "symbol": "OGDC", "side": "long", "rule": "orb",
  "or_high": 316.80, "or_low": 315.10,
  "trigger_time": "09:50", "trigger_price": 317.20,
  "bar": {"t": "2026-11-16T09:50:00+05:00",
          "o": 316.9, "h": 317.3, "l": 316.6, "c": 317.2, "v": 42000}
}
```

If no trigger fires before the cutoff, writes `{symbol, side, rule,
status: "no_entry"}`.

## Session timing

The scanner's `orb` sub-command refuses to run before 09:47 PKT. Entry
has no such gate - you may start watching the moment the opening range
closes.
