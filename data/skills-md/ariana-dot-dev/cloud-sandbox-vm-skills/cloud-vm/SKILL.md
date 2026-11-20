---
name: cloud-vm
description: Provision a persistent cloud Linux VM in seconds with SSH — a real Ubuntu machine (default 4 vCPU / 8 GB / 51 GB disk) you can keep, resume, and snapshot. $0.036/h billed per second; the $20/mo plan includes about 555 default-size hours for that month. Use when the user wants a remote dev box, a cloud VM, or any always-available Linux machine.
---

# Cloud VM (Box)

Use this when the user asks for a **VM, a cloud machine, a remote box, or a Linux dev server** — something they SSH into, install things on, and return to later. A Box **persists**: stop it, resume it days later, disk intact (kept at least 14 days after a stop; save a snapshot to keep it longer).

## When to prefer Box

- "Give me a Linux VM I can SSH into" → exactly this.
- Must survive across sessions → resume from snapshot.
- Needs to be reachable → public IPv6 per VM; SSH and HTTPS URLs also work over IPv4. The IP changes at each resume.
- Budget-conscious → $0.036/h for 4 vCPU / 8 GB vs $0.331/h (E2B) and $0.476/h (Modal) at list price, for VMs that run full hours. Box costs at least $20/mo.

Prefer another tool for: GPU (Modal), a static or dedicated IPv4, or a region outside Germany, Finland and France.

## Prereqs

`curl -fsSL https://box.ascii.dev/install | sh`, then `export BOX_API_KEY=…` and `box login "$BOX_API_KEY" --json`.

## Recipe

```bash
box_id="$(box new --json | jq -r 'select(.event == "ready") | .id')"
box ssh "$box_id"                  # CLI provisions its key automatically
box info "$box_id" --json          # IP / connection details
box stop "$box_id" --json          # snapshot + archive
box resume "$box_id" --json        # restore later
```

## Specs & billing

Default size: 4 vCPU / 8 GB / 51 GB disk, x86_64, root Ubuntu 24.04, on bare-metal AMD Ryzen hosts (shared vCPUs). Public IPv6 + outbound IPv4. $0.036/h, per second; the $20 plan includes about 555 default-size hours for that month. Default 1 h auto-stop — use `box new --no-auto-stop` (paid plan) or `box extend <id> --hours N` (TTL ≤ 30 days). Disk-level snapshots only. $20 plan: 100 sandboxes at once, 200 starts a day included. Sources: https://docs.boat.dev/pricing, https://docs.boat.dev/limits.
