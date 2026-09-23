---
name: log-analyzer
description: Groups a log file's errors by pattern and ranks offenders — normalizes volatile tokens (timestamps, UUIDs, IPs, paths, numbers) so "connection refused to db-01" and "db-99" count as one problem seen N times. Handles both level-tagged logs (ERROR/WARN/INFO) and exception-style stack logs (DaemonError:, Traceback). Offline, stdlib-only, deterministic.
when_to_use: Triage on a big log file, CI gates on error budgets ("fail if any error" or "fail if >5 distinct patterns"), or turning a daemon log into an actionable report. NOT a log shipper or a live tail; it analyzes files you point it at.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [logs, debugging, backend, errors, ci-gate]
---

# Log Analyzer

A 50,000-line log is not a report. This is.

## Commands

```bash
python3 scripts/log_analyzer.py app.log
python3 scripts/log_analyzer.py app.log --level ERROR --top 10
python3 scripts/log_analyzer.py app.log --budget-errors 0     # CI: fail on any
python3 scripts/log_analyzer.py app.log --max-patterns 5      # CI: error diversity cap
python3 scripts/log_analyzer.py daemon.log --json
```

## What it reports

- Total lines, error count, warning count, distinct pattern count
- Ranked patterns with occurrence counts and one verbatim example each

Volatile tokens (timestamps, UUIDs, hex, IPs, host:port, paths, numbers) are
normalized to `<tokens>` so the same failure from different hosts/times
groups into one pattern. Exception-style lines (`FooError:`, `Traceback`,
`FAILED`) count as errors even without an ERROR level token.

## Exit codes

0 = no errors / within budget, 1 = errors found or over budget, 2 = input error.

## Pairs with

`systematic-debugging` (what to do with the top pattern once you have it),
`diff-review` (the diff-level gate upstream of the runtime log).
