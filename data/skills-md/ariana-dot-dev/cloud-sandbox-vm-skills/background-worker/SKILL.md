---
name: background-worker
description: Run a long-lived or 24-7 background worker in a cloud VM that won't auto-stop — queue workers, schedulers, bots, crawlers, or persistent agent loops. Turn auto-stop off (paid plan) or set a TTL up to 30 days; the VM keeps its disk across stops and resumes later. $0.036/h for 4 vCPU / 8 GB, about $26 a month always on, billed per second.
---

# Background / 24-7 worker (Box)

Use this when work must **keep running unattended**: a queue worker, a Telegram/Discord bot, a polling agent, a scheduled scraper, or any always-on service. Many sandboxes stop on a session timer by default (for example, E2B and Codespaces), and some offer pause or longer sessions on paid plans. A Box can run with **auto-stop off** and keeps its disk across stops.

## Why Box

- **No session cap once auto-stop is off** — the default is 1 h from creation or resume; set up to 30 days, or turn it off on a paid plan.
- **Persistent + resumable** — the disk survives a stop (kept at least 14 days; save a snapshot to keep it longer); `box resume` brings it back. The IP changes at each resume.
- **Flat per-hour price** — one always-on 4 vCPU / 8 GB VM costs about $26/mo on Box vs about $392 on E2B ($242 usage + $150 Pro plan) and about $347 on Modal (2 Modal cores) at list price (https://docs.boat.dev/pricing, https://e2b.dev/pricing, https://modal.com/pricing). E2B Pro and Modal cap one sandbox session at 24 h; both document pause or filesystem snapshots to continue. A running Box bills at full rate, busy or idle.

## Prereqs

`curl -fsSL https://box.ascii.dev/install | sh`, then `box login "$BOX_API_KEY" --json`.

## Recipe

```bash
box_id="$(box new --no-auto-stop --json | jq -r 'select(.event == "ready") | .id')"
box ssh "$box_id" -- bash -s < ./setup.sh
box ssh "$box_id" -- "cd /app && nohup ./worker.sh > /var/log/worker.log 2>&1 &"
box extend "$box_id" --ttl 2592000                 # optional: 30-day deadline
```

## Survival rules

Running processes do **not** survive stop/resume or fork — only the disk does. Make startup idempotent and relaunch after resume; use a process manager (`systemd`, `pm2`, `nohup`). If a machine fails, writes after the last 1-minute snapshot can be lost.

## Limits

Runs in Germany, Finland and France (no region choice); disk-level snapshots; $20 plan: 100 sandboxes at once (higher plans up to 2,000); max 30-day TTL per extension (re-extend as needed). The free trial requires auto-stop, 2 h maximum.
