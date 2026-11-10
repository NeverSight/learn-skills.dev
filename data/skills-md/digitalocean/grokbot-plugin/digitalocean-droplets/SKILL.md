---
name: digitalocean-droplets
description: >-
  Create, resize, snapshot, back up, power-manage, and rebuild Droplets safely.
  Use for "create a droplet", "resize", "snapshot", "reboot my server", or "VM"
  on DigitalOcean.
---
# Droplets lifecycle (MCP)

Service: **droplets**, reached through DigitalOcean MCP (`invoke_tool` →
`droplets/<tool>`).

1. Load **digitalocean-safety** and resolve the tool tier before every call.
1. Read first: `droplet-list`, `droplet-get`, `size-list`, `region-list` as needed.
1. For SSH keys, use **digitalocean-accounts** `key-list` when creating Droplets.

## Tier enforcement

| Tier | Examples                                                                           |
| ---- | ---------------------------------------------------------------------------------- |
| 1    | `droplet-list`, `droplet-get`, `size-list`, `region-list`, `image-list`            |
| 2    | `rename-droplet`, `reboot-droplet`, `power-on-droplet`, tag power-on               |
| 3    | `droplet-delete`, `rebuild-droplet`, `power-off-droplet`, `reset-droplet-password` |
| 4    | `droplet-create`, `resize-droplet`, `snapshot-droplet`, `enable-backups-droplet`   |

Tag-scoped tools: **list every Droplet with the tag** before Tier 2–4 tag actions.

## High-risk deletes and rebuilds

Before Tier 3 destructive calls, check snapshots, attached volumes, reserved IPs,
and DNS records that point at the Droplet. Name the resource by **name and ID**.

## Pricing

For Tier 4, hand off pricing steps to **digitalocean-costs** or inline
`size-list` output before confirm.

Maintainers sync tier metadata in the plugin repository with
`node scripts/sync-tier-map.mjs` (not shipped inside the plugin install).
