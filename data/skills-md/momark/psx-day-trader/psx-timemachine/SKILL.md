---
name: psx-timemachine
description: >-
  PSX Time Machine. Takes an entry + stop + target (from psx/plan.json)
  and replays the stop-and-target rule against that symbol's last ~60
  trading sessions of EOD bars, plus a 10,000-draw Monte Carlo of
  resampled daily returns. Prints the share of runs that hit target vs
  stop, median final outcome, and an ASCII fan chart. Verdicts:
  COIN_FLIP (within 5 % either way), STRONG (lopsided > 15 %),
  MANY_NEITHER (> 40 % time out without hitting either). Use when the
  user says "run the time machine", "backtest this plan", "has this
  trade worked before", "what did 10,000 runs look like", or right
  after /psx-exit and before /psx-budget.
argument-hint: "[--draws 10000] [--horizon-days 5] [--seed 19]"
---

# psx-timemachine

`${CLAUDE_SKILL_DIR}` is this skill's folder.

```bash
python3 "${CLAUDE_SKILL_DIR}/timemachine.py"                             # read psx/plan.json
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" --draws 10000 --horizon-days 5
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" --symbol OGDC --entry 316 --stop 311 --target 326
python3 "${CLAUDE_SKILL_DIR}/timemachine.py" --json
```

Flags: `--horizon-days 5` (how many sessions the Monte Carlo runs each
draw for; 1 for a true day-trade), `--draws 10000`, `--seed 19`
(reproducible), `--pool-days 60` (how many past sessions to sample
returns from), `--offline PATH`.

## What it replays

Each draw builds a hypothetical path of daily returns by sampling
with replacement from the last `--pool-days` of this symbol's returns,
then applies the actual stop and target to the resulting price path.
Three outcomes per draw:

- **target** — the path's intraday high touched the target.
- **stop** — the path's intraday low touched the stop.
- **neither** — horizon ran out with the price between stop and target.

The EOD endpoint gives close + volume + open only, not daily high/low.
For the "hit intraday" test the Time Machine uses `[min(open, close) -
0.5 % buffer, max(open, close) + 0.5 % buffer]` as a *conservative*
daily range. This is not perfect; the full OHLCV historical table
(`/historical`) could be scraped per date for exact H/L in v1.1.

## Verdict thresholds

- `STRONG_TARGET` — target % > stop % by 15 pp or more.
- `STRONG_STOP` — stop % > target % by 15 pp or more.
- `COIN_FLIP` — |target % - stop %| < 5 pp.
- `MANY_NEITHER` — neither % > 40 %.
- `MIXED` — anything else.

Thresholds match the US `trader-timemachine` 1:1 for familiarity.

## Output

Writes `psx/timemachine.json`:
```json
{
  "symbol": "HUBC", "entry": 208, "stop": 204.3, "target": 215.4,
  "horizon_days": 5, "draws": 10000, "seed": 19, "pool_days": 60,
  "target_pct": 42.1, "stop_pct": 38.6, "neither_pct": 19.3,
  "median_final_price": 207.8, "verdict": "COIN_FLIP"
}
```

Prints an ASCII fan chart of final-price distribution to stderr.
