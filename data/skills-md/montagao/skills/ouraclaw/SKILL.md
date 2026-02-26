---
name: ouraclaw
description: Fetch Oura Ring sleep data using the ouraclaw CLI. Use when the user asks about their sleep score, sleep data, sleep stages, HRV, heart rate during sleep, bedtimes, or any Oura Ring data. Triggers on "sleep score", "how did I sleep", "oura data", "sleep data", "last night's sleep", "sleep quality", "HRV", or any request for Oura Ring metrics.
---

# Ouraclaw

Fetch Oura Ring sleep data via the `ouraclaw` CLI. Outputs JSON to stdout.

## Ensure ouraclaw is installed

```bash
which ouraclaw
```

If not found:

```bash
git clone https://github.com/montagao/ouraclaw.git ~/projects/ouraclaw
cd ~/projects/ouraclaw && bun install && bun link
```

If auth is needed (no tokens in `.env`), run `cd ~/projects/ouraclaw && ouraclaw auth`.

## Commands

```bash
# Last night's sleep score
ouraclaw score

# Date range
ouraclaw score --start 2025-02-01 --end 2025-02-15

# Detailed sleep sessions (stages, HR, HRV, bedtimes)
ouraclaw sleep

# Date range
ouraclaw sleep --start 2025-02-01 --end 2025-02-15
```

## Extracting fields with jq

```bash
ouraclaw score | jq '.data[0].score'
ouraclaw sleep | jq '.data[0] | {bedtime_start, bedtime_end}'
ouraclaw score --start 2025-02-01 --end 2025-02-15 | jq '[.data[] | {day, score}]'
```

## Error handling

- **"No access token"**: Run `cd ~/projects/ouraclaw && ouraclaw auth`.
- **401 after auto-refresh fails**: Re-run `ouraclaw auth`.
