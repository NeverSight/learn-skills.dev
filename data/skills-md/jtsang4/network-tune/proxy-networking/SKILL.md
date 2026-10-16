---
name: proxy-networking
description: Build and maintain relay-to-exit proxy networks across VPS nodes. Use when Codex needs to deploy or update VLESS Reality relay entrypoints through v2ray-agent/vasma, WireGuard relay-to-exit links, sing-box multi-inbound routing, legacy Realm-to-Xray bridges, per-link tuning, or VLESS share links for existing or newly added relay and exit machines.
---

# Proxy Networking

## Goal

Build a relay-to-exit proxy network from user-supplied relay machines, exit machines, bandwidth, and relationship mappings.

Default target:

```text
client -> relay sing-box VLESS Reality inbound -> WireGuard tunnel -> exit Linux egress
```

Flexible migration target:

```text
client -> existing relay entrypoint -> existing Realm bridge -> WireGuard tunnel -> existing exit Xray/VLESS Reality
```

Use `v2ray-agent`/`vasma` as the preferred installer and manager for Xray or sing-box VLESS Reality when a host needs a new VLESS stack or already uses that project. Directly edit generated configs when preserving existing links, adding WireGuard behind an existing service, or making a small targeted repair.

Keep TCP/kernel tuning delegated to the `network-tune` skill in this repository. Use this skill for topology, proxy services, WireGuard links, maintenance, link generation, and per-link measurement.

## Inputs To Normalize

Collect or infer a topology table before changing hosts:

```text
relays:
  - ip / ssh target / bandwidth / region / current services / desired public ports
exits:
  - ip / ssh target / bandwidth / region / current services / desired egress role
relationships:
  - relay -> one or more exits
  - per relationship: public inbound port, protocol preference, preserve existing link yes/no, label
```

If the user gives only IPs, use `root@IP`. Treat bandwidth values as operator intent; use Speedtest or iperf only to validate link behavior.

## Workflow

1. Run preflight before changing any host:
   - Read `references/preflight.md`.
   - Mark a host or relationship as `blocked` when kernel, package, disk, SSH, port, or UDP direction checks fail.
   - Keep blocked relationships on their current working path and report the exact blocker.
2. Inventory every relay and exit over SSH:
   - OS, kernel, public/private IPs, interfaces, routes, bandwidth notes.
   - Services: `sing-box`, `xray`, `realm`, `wg-quick@*`, `nginx`, `hysteria`, `tuic`.
   - Config paths: `/root/realm.toml`, `/etc/v2ray-agent/xray/conf`, `/etc/sing-box`, `/usr/local/etc/sing-box`, `/etc/wireguard`.
3. Classify each relationship:
   - Fresh build: relay terminates VLESS Reality with sing-box and exits through WireGuard.
   - Existing Realm bridge: keep the client-facing port and change Realm's remote target to the exit WireGuard IP.
   - Existing sing-box/Xray entry: add only missing inbounds, outbounds, routes, peers, or systemd persistence.
4. Create a per-link plan:
   - WireGuard tunnel address, port, MTU, preshared key, allowed IPs.
   - WireGuard interface name, compressed to Linux's 15-byte interface limit.
   - Relay inbound tag and public port.
   - Exit egress behavior: NAT gateway for fresh builds, or private Xray target for bridge preservation.
   - Connection direction: relay dials exit, or exit dials relay when exit-side public UDP ingress is unavailable.
   - Verification commands and rollback paths.
5. Apply one relationship at a time using the state model in `references/link-state.md`:
   - Back up all touched files with timestamps.
   - Follow `references/ssh-execution.md` for SSH invocation shape.
   - Follow `references/package-policy.md` before installing packages.
   - Use `v2ray-agent`/`vasma` for fresh VLESS Reality stacks when appropriate.
   - Create or update WireGuard peers.
   - Create or update sing-box, Realm, Xray, NAT, and systemd units according to the selected pattern.
   - For Realm bridge updates, follow `references/realm-safety.md` and prefer `scripts/patch-realm-endpoint.py`.
6. Verify:
   - Read `references/verification.md`.
   - `wg show`, ping over WireGuard, TCP reachability to private exit target.
   - `iperf3` public UDP, WireGuard TCP, and reverse direction tests.
   - Client-facing port reachability from the relay.
   - Service persistence after reboot when the user permits reboot verification.
7. Report:
   - Topology, active services, per-link private IPs, throughput, pacing, rollback paths.
   - Completed relationships, preserved relationships, blocked relationships, and required host repairs.
   - Mention VLESS share links can be generated on request. Provide links only when requested.

## References

Read the matching reference before implementation:

- `references/topology-workflow.md` for inventory, build/update decision rules, and verification.
- `references/v2ray-agent.md` for using `v2ray-agent`/`vasma` as the VLESS Reality implementation layer.
- `references/config-patterns.md` for WireGuard, sing-box, Realm, Xray, NAT, tuning, and rollback patterns.
- `references/preflight.md` for host checks before any change.
- `references/link-state.md` for per-relationship state tracking and resume behavior.
- `references/wireguard-rules.md` for interface naming, address planning, and connection direction.
- `references/realm-safety.md` for safe Realm endpoint updates.
- `references/ssh-execution.md` for SSH execution patterns in batch changes.
- `references/package-policy.md` for conservative package installation rules.
- `references/verification.md` for acceptance checks.
- `references/vless-links.md` for extracting and generating VLESS Reality share links.

Use `scripts/gen-vless-link.py` to generate share links from known fields.
Use `scripts/patch-realm-endpoint.py` to update one Realm endpoint safely.

Example:

```bash
scripts/gen-vless-link.py \
  --host 8.209.199.131 \
  --port 15659 \
  --uuid 00000000-0000-0000-0000-000000000000 \
  --sni www.example.com \
  --public-key REALITY_PUBLIC_KEY \
  --short-id abcd1234 \
  --flow xtls-rprx-vision \
  --name "relay-8-to-exit-45"
```

## Safety Rules

- Prefer preserving working client-facing links during migration.
- Back up every edited remote file with a timestamp.
- Keep existing unrelated inbounds and exits active.
- Use `systemctl reload` when supported; use restart only after validating config syntax.
- Limit live traffic disruption to the specific relationship being changed.
- Treat generated VLESS links as sensitive credentials.
- Treat a relationship as blocked when preflight fails; leave its current working route in place.
- Never run a multi-link batch as one opaque operation; each relationship needs its own state and verification result.
