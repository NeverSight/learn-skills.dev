---
name: cron-audit
description: Parses a crontab, expands every schedule into concrete values, explains each job in plain words, and flags invalid lines, impossible schedules, and over-frequent jobs. Crontab syntax is write-only for most humans; this makes it readable. Stdlib-only, deterministic.
when_to_use: Reviewing a server's crontab before touching it, CI validation of committed crontabs, or "when does this job actually run?" NOT a scheduler (it doesn't run anything) and not launchd/systemd (crontab format only).
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [cron, scheduling, sysops, automation, ci-gate]
---

# Cron Audit

Crontab lines are write-only for most humans. This reads them back.

## Commands

```bash
python3 scripts/cron_audit.py /etc/crontab
crontab -l | python3 scripts/cron_audit.py -
python3 scripts/cron_audit.py deploy/crontab.txt --max-freq-min 5 --json
```

## Reports

Per line: parsed schedule values (`hour [2], minute [0], weekday [1,2,3,4,5]`),
a plain-words explanation ("every weekday, hour 9-17, every 15 minutes"),
and the command. Invalid lines get the exact parse error
(`range 25-30 outside hour 0-23`).

Exit 1 on any invalid line — a CI gate for committed crontabs.

## Catches

- Wrong field count (5 fields + command required)
- Values/ranges outside field bounds (minute>59, month>12)
- Bad steps (`*/0`), unparseable tokens
- Jobs more frequent than `--max-freq-min` minutes (runaway polling)

## Pairs with

`apple-suite` (the GUI-app automation layer; cron is the headless layer),
`sys-health` (is the box those jobs run on healthy).
