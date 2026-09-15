---
name: mikrotik-routeros
description: Configures and automates MikroTik RouterOS routers through the terminal, command line interface, .rsc imports, /system script repository, Scheduler, Netwatch, firewall, NAT, DHCP, DNS, bridge, VLAN, routing, VPN, device-mode, backup/export, and RouterOS scripting. Use this skill whenever the user mentions MikroTik, Mikrotik, RouterOS, WinBox terminal, router CLI, router scripts, .rsc files, or configuring MikroTik services from the command line.
license: MIT
metadata:
  author: github.com/bastos
  version: "1.0"
---

# MikroTik RouterOS CLI and Scripting

Use this skill to generate, review, or troubleshoot RouterOS command-line configuration and scripts. Target RouterOS v7 unless the user gives a different version.

## Reference Loading

Read the smallest relevant reference before producing commands:

- `references/official-docs.md` - source map for official MikroTik documentation and version notes.
- `references/routeros-cli.md` - terminal syntax, paths, item targeting, quoting, and SSH execution.
- `references/routeros-scripting.md` - RouterOS script structure, variables, functions, error handling, and script repository behavior.
- `references/config-change-workflows.md` - backups, exports, safe mode, imports, resets, and rollback planning.
- `references/recipes.md` - reusable command patterns for common configuration tasks.

## Operating Model

1. Determine whether the user wants live execution, a command plan, a reusable `.rsc` file, or a `/system script` entry.
2. Gather only the facts needed to avoid an unsafe or wrong config: RouterOS version, model, management IP/interface, WAN/LAN interface names, bridge/VLAN design, and existing rule order.
3. Prefer commands that are safe to paste into a RouterOS terminal. Use absolute menu paths such as `/ip/firewall/filter` instead of relying on the current menu.
4. Use stable identifiers: item names, comments, default-name values, or `[find ...]` filters. Avoid numeric item IDs in generated scripts because CLI numbers are session-local.
5. Make commands idempotent where practical. Check for existing objects with `[find ...]` before adding duplicates.
6. Separate preflight, changes, verification, and rollback. Router configuration mistakes can cut off management access.

## Safety Defaults

- For remote network, firewall, route, bridge, VLAN, or address changes, recommend an export and either safe mode or a staged rollback path before making changes.
- Never guess credentials, public IPs, interface roles, or firewall rule order. Use placeholders or ask for the missing value if it is a blocker.
- Do not include real passwords, private keys, shared secrets, or `show-sensitive` output unless the user explicitly asks and understands the exposure.
- Prefer SSH or local terminal examples. Do not recommend Telnet except for an explicitly isolated recovery scenario.
- Flag commands that reboot, reset, disable management services, remove addresses/routes, or alter input firewall policy.
- If the user asks for a destructive reset, include the exact consequence and a backup/export step first.

## Answer Shape

For configuration changes, use this structure:

```markdown
## Preflight
<read-only commands to inspect state and save config>

## Commands
<RouterOS commands, grouped by subsystem>

## Verify
<commands to prove the intended state and connectivity>

## Rollback
<minimal commands or restore path>
```

For scripts, use this structure:

```markdown
## Script
<source code or /system script add/set command>

## Install
<commands to add the script and required policy>

## Test
<manual run, logs, dry-run behavior if applicable>

## Schedule or Trigger
<scheduler/netwatch/button hook only if requested>
```

## RouterOS Command Style

- Write commands in slash-separated form: `/ip/address/print`, `/system/script/add`, `/interface/bridge/vlan/add`.
- Keep `param=value` tight; RouterOS does not allow spaces around `=`.
- Quote strings with spaces or special characters: `comment="managed by routeros-script"`.
- Use comments as durable anchors for generated rules and scheduled jobs.
- Use `print terse` or `print detail` for state capture, and `print where ...` for targeted checks.
- Use `export terse` for portable command output; use binary `/system backup` only for same-device restore scenarios.

## Idempotent Pattern

Use this pattern when adding an object that should exist at most once:

```routeros
:if ([:len [/ip/firewall/address-list/find list="mgmt-allow" address="203.0.113.10"]] = 0) do={
    /ip/firewall/address-list/add list="mgmt-allow" address="203.0.113.10" comment="managed: admin workstation"
}
```

For existing objects, use `set [find ...] ...` only when the `find` expression is expected to match exactly one item. If multiple matches are possible, print and ask the user to choose or narrow the filter.

## Validation Checklist

Before handing off commands, check:

- Interface names match the user's device, or are clearly placeholders.
- Firewall rules are placed before broad drop/reject rules.
- Management allow rules are added before any restrictive input policy.
- Scripts declare variables before use and use local scope unless persistence is intentional.
- Import files use RouterOS syntax, not Bash.
- Version-sensitive features are labelled and linked to official docs when needed.
