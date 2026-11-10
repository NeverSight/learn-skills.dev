---
name: lookahead-bias-detection-methodology
description: 'Use this skill on any backtest before trusting its results, applying concrete, mechanical tests to actually catch lookahead bias rather than just warning it might exist. Also use it when a backtest''s performance seems too good relative to overfitting-and-robustness-checks''s red-flag thresholds, since lookahead bias is one of the most common root causes of a suspiciously good result. This skill exists because "check for lookahead bias" is easy advice to give and hard to actually act on without a concrete method; this skill is that method, not just the warning.'
---

# Lookahead Bias Detection Methodology

## Why this matters

[overfitting-and-robustness-checks](../overfitting-and-robustness-checks/SKILL.md) and [feature-and-signal-engineering-discipline](../feature-and-signal-engineering-discipline/SKILL.md) both warn that lookahead bias exists and describe common ways it creeps in, but knowing lookahead bias is a risk category doesn't tell you how to actually go find it in a specific piece of code and a specific data pipeline. Lookahead bias is also uniquely dangerous among backtest bugs because it doesn't produce an error, a crash, or even an obviously wrong-looking number; it produces a backtest that runs cleanly and reports a better result than reality would have allowed, which is exactly the failure mode that gets shipped to live trading before anyone notices.

## Do this

### Run a truncation ("time-travel") test: rerun the backtest with data cut off at an earlier date and verify prior decisions don't change

Pick a date partway through the backtest period, rerun the strategy using only data up to that date, and compare every decision (signal, position, trade) made before that date against the decisions from the full-history run. If any decision made before the cutoff date differs between the truncated run and the full run, the strategy is using data from after that decision was made, which is lookahead bias by definition; a correct backtest's decisions at any point in time cannot depend on data from after that point, so this test should produce identical results for every date up to the truncation point, every time it's run. This is the single most direct, mechanical way to actually catch lookahead bias rather than reasoning about whether it could theoretically exist.

### Run a future-data corruption test: deliberately corrupt future bars and verify past decisions are unaffected

As a complementary check to truncation, deliberately replace or randomize the data for a specific future date range (bars well after the period being checked) with garbage values, then rerun the backtest and verify decisions before that corrupted range are completely unchanged. If corrupting data far in the future changes a decision made in the past, that's direct, unambiguous proof of a lookahead path in the code, and this test can be automated to run on every code change as a regression test, not just as a one-time audit.

### Audit the code path for every feature and signal, tracing exactly which timestamps of data it reads

For each feature or signal computation, trace through the actual code to identify every data point it reads, and verify each one has a timestamp strictly at or before the decision timestamp; pay particular attention to any function that computes a statistic over a window (rolling means, normalization, any "full history" or "whole dataset" statistic per [feature-and-signal-engineering-discipline](../feature-and-signal-engineering-discipline/SKILL.md)), any join or merge between data sources that might not be aligned the way it's assumed to be, and any place where a bar's own "close" is used to generate a signal that then trades within that same bar as if the close were already known before it was.

### Check every point where separate data feeds or datasets are merged, since misaligned joins are a common and easy-to-miss lookahead source

A join between a price series and a fundamentals series, an alternative dataset, or an economic release calendar can silently introduce lookahead if the join key or timestamp alignment doesn't correctly reflect when each piece of data was actually available (see [alternative-data-evaluation](../alternative-data-evaluation/SKILL.md) and [data-cleaning-and-preprocessing-pitfalls](../data-cleaning-and-preprocessing-pitfalls/SKILL.md) for related concerns); explicitly verify the actual availability timestamp used in every merge, not just the nominal "as of" date attached to the data.

### Automate these tests to run on every strategy code change, not just once at the end

Lookahead bias can be introduced by a single careless code change to an otherwise-clean strategy, so the truncation test and the future-corruption test should be automated regression tests that run whenever the strategy's code changes, consistent with [reproducibility-and-experiment-tracking](../reproducibility-and-experiment-tracking/SKILL.md)'s emphasis on a reliable, repeatable research process, rather than a one-time manual audit performed only when a result looks suspicious.

## Never do this

- Never trust a backtest's absence of an obvious error as evidence it's free of lookahead bias; lookahead bias produces clean-running code with an inflated result, not a crash.
- Never skip running an actual truncation test before trusting a backtest's results; reasoning about whether lookahead bias could theoretically exist is not a substitute for mechanically testing for it.
- Never assume a rolling-window or normalization calculation is safe without explicitly verifying it only uses data up to and including the current point in time.
- Never merge or join separate data sources without explicitly verifying the actual availability timestamp used, not just the nominal date field.
- Never treat a lookahead-bias check as a one-time audit; automate the truncation and corruption tests to run on every strategy code change.

## Verification checklist

- [ ] A truncation ("time-travel") test has been run, confirming decisions made before a cutoff date are identical whether or not later data exists in the dataset
- [ ] A future-data corruption test has been run, confirming that corrupting data in a future date range does not change any decision made before that range
- [ ] Every feature and signal's code path has been traced to confirm it only reads data with a timestamp at or before the decision timestamp
- [ ] Every merge or join between separate data sources has been checked for correct availability-timestamp alignment, not just nominal date matching
- [ ] The truncation and corruption tests are automated to run on every strategy code change, not performed only as a one-time manual audit
