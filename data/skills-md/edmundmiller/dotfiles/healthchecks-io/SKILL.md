---
name: healthchecks-io
description: Create, manage, and verify healthchecks.io monitors via the REST API. Use when adding monitoring to a new cron job or service, auditing existing checks, wiring ping URLs into configs, or verifying a check fired correctly.
---

# healthchecks.io API

Credentials available as env vars:

- `$HC_API_KEY` — read-write API key (create/update/delete checks)
- `$HC_API_KEY_READONLY` — read-only API key (list/view only)
- `$HC_PING_KEY` — ping key (for `https://hc-ping.com/$HC_PING_KEY/<slug>` URLs)

```bash
HC_API="https://healthchecks.io/api/v3"
```

## Create a check

```bash
curl -s -X POST "$HC_API/checks/" \
  -H "X-Api-Key: $HC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "service: job-name",
    "tags": "nuc cron",
    "desc": "What this monitors",
    "grace": 3600,
    "schedule": "0 * * * *",
    "tz": "America/Chicago"
  }' | jq '{name, ping_url, uuid}'
```

Key fields:

- `grace` — seconds after expected ping before alerting (3600 = 1h buffer)
- `schedule` — cron expression for expected cadence (sets the deadline clock)
- `timeout` — alternative to schedule for simple heartbeats (seconds between pings)
- `tz` — timezone for cron interpretation

Returns `ping_url` (`https://hc-ping.com/<uuid>`) — save this to your config.

## List / find existing checks

```bash
# All checks with status summary
curl -s "$HC_API/checks/" -H "X-Api-Key: $HC_API_KEY" \
  | jq '.checks[] | {name, status, last_ping, ping_url}'

# Find by name substring
curl -s "$HC_API/checks/" -H "X-Api-Key: $HC_API_KEY" \
  | jq '.checks[] | select(.name | contains("bugster")) | {name, uuid, status, ping_url}'

# Find by tag
curl -s "$HC_API/checks/" -H "X-Api-Key: $HC_API_KEY" \
  | jq '.checks[] | select(.tags | contains("nuc")) | {name, status}'
```

Statuses: `new` `up` `grace` `down` `paused`

## Delete a check

```bash
curl -s -X DELETE "$HC_API/checks/<uuid>" -H "X-Api-Key: $HC_API_KEY" \
  | jq '{name, n_pings, last_ping}'   # returns the deleted check
```

## Ping from a script

```bash
PING_URL="https://hc-ping.com/<uuid>"

# Signal start (measures duration, alerts if no success follows)
curl -sS -m 10 --retry 3 "$PING_URL/start"

# Signal success
curl -sS -m 10 --retry 3 "$PING_URL"

# Signal failure
curl -sS -m 10 --retry 3 "$PING_URL/fail"

# Signal success/failure by exit code (0 = success, non-zero = fail)
curl -sS -m 10 --retry 3 "$PING_URL/$EXIT_CODE"

# Attach logs to a ping (POST body, up to 10KB)
curl -sS -m 10 --retry 3 "$PING_URL" --data-raw "$(journalctl -u myservice -n 50 --no-pager)"
```

Wrap a script with start+exit-code:

```bash
curl -sS -m 10 "$PING_URL/start"
/path/to/my-script.sh
curl -sS -m 10 "$PING_URL/$?"
```

## Verify a check received pings

```bash
# Single check detail (includes last_ping, n_pings, status)
curl -s "$HC_API/checks/<uuid>" -H "X-Api-Key: $HC_API_KEY" \
  | jq '{name, status, n_pings, last_ping, next_ping}'

# Recent ping log for a check
curl -s "$HC_API/checks/<uuid>/pings/" -H "X-Api-Key: $HC_API_KEY" \
  | jq '.pings[:5] | .[] | {type, date, body}'
```

Ping types in log: `start` `success` `fail`

## Update an existing check

```bash
curl -s -X POST "$HC_API/checks/<uuid>" \
  -H "X-Api-Key: $HC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"grace": 7200, "tags": "nuc cron updated"}'
```

## Pause / resume

```bash
curl -s -X POST "$HC_API/checks/<uuid>/pause" -H "X-Api-Key: $HC_API_KEY"
curl -s -X POST "$HC_API/checks/<uuid>/resume" -H "X-Api-Key: $HC_API_KEY"
```

Useful when intentionally stopping a service (prevents false alarms).

## Naming convention

```
<service>: <job-name>         # bugster: github_personal_tasknotes
<host>/<service>              # nuc/znapzend
```

Tags: host + category (e.g. `nuc backup`, `bugster cron`).
