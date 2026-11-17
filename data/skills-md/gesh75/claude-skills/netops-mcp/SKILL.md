---
name: netops-mcp
description: Operate multi-vendor network devices (Junos, EOS, IOS/XR/NX-OS) via the netops MCP (NAPALM + Netmiko). Use for live troubleshooting or changes — BGP/OSPF/MPLS, interfaces, VLANs, routing. Read-first, dry-run, consent-gated. Not for CAB/RFC (network-change-cab).
origin: snm-pack
---

# netops-mcp — safe network operations

You have an MCP server (`netops`) that connects to real network devices. Treat every
device as production. **Default to read-only. Never change a device without a dry-run
and explicit human confirmation.**

Role-level work (CAB, RFC, healthcare, diagrams) belongs in the
**senior-network-manager** pack — see Pairs with.

## Golden rules

1. **Identify the device first** — call `list_devices` (optionally by group) to get the
   exact `device` id. Every tool takes that id.
2. **Diagnose with read tools** before proposing any change. Prefer structured getters
   (`get_bgp_neighbors`, `get_interfaces`, …) over `get_config`/`run_show_command`.
3. **Changes are ALWAYS two steps:**
   - `stage_config_diff(device, config, mode)` → returns a `diff`, any
     `self_lockout_warnings`, and a single-use `consent_token`.
   - **Show the diff to the user and get explicit approval.** Then
     `commit_config(device, config, consent_token, mode)`.
4. **Never invent a consent_token.** It must come from a fresh `stage_config_diff`.
   If the diff changed since staging, the commit will fail closed — re-stage.
5. **If `self_lockout_warnings` is non-empty**, the plain commit is refused. Use
   `commit_config_confirmed` (auto-revert, EOS/Junos/IOS only) and tell the user they
   must `confirm_pending_commit` within the window or the change auto-reverts.
6. **Raw CLI config** (screen-scrape platforms): `stage_raw_commands` → review →
   `run_config_commands`. Single read-only commands use `run_show_command`.
7. **Stop and report** if a write tool returns a freeze/circuit-breaker/blast-radius
   error — do not retry in a loop. Surface it to the user.

## Read-first diagnostic playbooks

**BGP peer down**
1. `get_bgp_neighbors(device)` — find the peer, check state/uptime.
2. `get_bgp_neighbors_detail(device, neighbor_address=...)` — flap counters, last error.
3. `get_interfaces(device)` / `get_interfaces_ip(device)` — verify the link & addressing.
4. `ping_from_device(device, destination=<peer_ip>)` — confirm reachability.
5. Only if a fix is needed: build the minimal config, `stage_config_diff`, confirm, commit.

**Interface / L1-L2 issue**
`get_interfaces` (up/enabled, last_flapped) → `get_interfaces_counters` (errors/discards)
→ `get_lldp_neighbors` (is the right neighbor seen?) → `get_environment` (optics/power).

**Reachability / path**
`get_arp_table` → `get_mac_address_table` → `traceroute_from_device` → `ping_from_device`.

More playbooks: [reference/playbooks.md](reference/playbooks.md).

## Change workflow (canonical)

```
list_devices                      # get device id
get_* (diagnose)                  # read-only
stage_config_diff(dev, cfg, mode) # dry-run -> diff + consent_token
# >>> show diff to user, get YES <<<
commit_config(dev, cfg, token, mode)
# verify
get_* (confirm the change took effect)
```

Production mutations also need a JSM Change (`network-change-cab` +
`atlassian-ops`) unless the user is in an active Sev1 and explicitly
chooses emergency.

## Vendor notes

- **Junos / EOS / IOS-XR**: NAPALM candidate model — use `stage_config_diff` + `commit_config`.
  Junos/EOS support `commit_config_confirmed`; IOS-XR does NOT.
- **Cisco IOS**: supports commit-confirmed only with on-device `archive`/`config replace`.
- **NX-OS**: no commit-confirm; merge-style changes.
- `config` you pass to `stage_config_diff` must be in the device's native syntax
  (Junos `set ...`/`delete ...`; IOS/EOS CLI config lines).
- Getter not supported on a platform → the tool returns `{"error": ...}`; pick another.

## Safety reminders for you, the agent

- Do not fan out writes across many devices in one turn — there is a deliberate
  blast-radius circuit breaker; respect it.
- Never echo raw `get_config` secrets back to the user; redaction is best-effort.
- If asked to do something destructive (erase, reload, zeroize), refuse and explain —
  the server blocks these, but you should not attempt them.
- Healthcare / ePHI paths: load `healthcare-network` and do **not** take packet
  captures on clinical VLANs.

## Pairs with

`senior-network-manager` (role) · `network-change-cab` (ticket/CAB) ·
`network-observability` (probes) · `healthcare-network` (clinical)

## Reference Files
- [reference/playbooks.md](reference/playbooks.md) — extra diagnostic sequences
