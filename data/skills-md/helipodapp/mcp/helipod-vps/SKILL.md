---
name: helipod-vps
description: Create and manage Helipod VPS servers - pick a plan and OS, order, power on/off, reinstall, get SSH/RDP login, firewall rules, snapshots, renewals and upgrades. Use when the user wants a virtual server with root access on Helipod.
---

# Helipod VPS

Follow the `helipod` skill rules. A VPS is prepaid per period: creating one charges the wallet immediately.

## Create

1. `list_vps_plans` → present 2 or 3 fitting plans with CPU, RAM, disk and `effectiveMonthly` (IDR). Note `osTemplates`.
2. `list_projects` → the project it belongs to (required).
3. Confirm with the user: plan, OS, billing period (`monthly`, `3month`, `6month`, `yearly`) and the total price.
4. Generate a strong password (12 to 30 chars, upper, lower, digit, one of `!@#$%^*`) unless the user gives one; do not print it back unless asked.
5. `create_vps` → poll `get_vps` every 10 s until `running` (a few minutes) or `error` (`lastJobError` says why; a failed create is refunded).
6. Login: `get_vps_credentials` (Linux: `ssh root@<ip>`; Windows: RDP as Administrator, port 3389).

## Manage

- Power: `vps_power` (`start`, `stop`, `restart`). While a job runs the server is busy (`409 VPS_BUSY`): wait and retry.
- Firewall: `list_firewall_rules`, `add_firewall_rules` (e.g. `{ "Protocol": "TCP", "Port": "443", "CidrBlock": "0.0.0.0/0", "Action": "ACCEPT" }`), `remove_firewall_rules` by id. Never remove the SSH rule (port 22) without asking.
- Snapshots: `create_snapshot` before risky changes; `apply_snapshot` rolls the disk back (data after it is lost: confirm).
- Reinstall: `reinstall_vps` wipes the disk: confirm explicitly.
- Billing: `get_vps_renewal_options` → `renew_vps`; `upgrade_vps` to a larger plan (charges the difference, restarts); `toggle_vps_auto_renew`.
- Terminate: `terminate_vps` is permanent, no refund: confirm explicitly.

Backups (paid add-on) and anything else: `helipod_request` with paths from https://docs.helipod.io/docs/vps-api
