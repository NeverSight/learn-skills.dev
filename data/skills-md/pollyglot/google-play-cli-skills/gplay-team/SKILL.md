---
name: gplay-team
description: Developer account members and permissions with `gplay team`. Use when inviting or off-boarding a member, auditing what a member can do, granting per-app access, or looking up a permission alias or role bundle (`team permissions`, offline).
---

# gplay team (users + grants + permissions)

Two write surfaces and one offline reference: **account-wide** membership
(`team users`), **per-app** access (`team grants`), and the **permission
vocabulary** (`team permissions`). Shared conventions are in `gplay-cli-usage`.

## Permission vocabulary (start here)

```bash
gplay team permissions --scope app       # offline; account scope by default (team users), app scope for team grants
gplay team permissions --output json     # marks the admin-conferring alias and bundle
```

Writes take **`--role <bundle>` XOR `--permissions <alias,…>`** (raw `CAN_*`
enums accepted); `team users` resolves in account scope, `team grants` in app
scope.

## Account-wide members

```bash
gplay team users list
gplay team users view alice@example.com    # one member: permissions + per-app grants (unknown member: exit 30)
gplay team users add alice@example.com --role release-manager
gplay team users set bob@example.com --permissions CAN_REPLY_TO_REVIEWS_GLOBAL   # declaratively replaces the set
gplay team users remove carol@example.com --confirm     # off-boarding is destructive: exit 3 without it
```

`add`/`set` have no gate except conferring admin (`--role admin`, or a set
containing the all-permissions enum): `--grant-admin`, exit `3` without it
(ADR-0017). `remove` needs `--confirm`.

Inviting an existing member fails with exit `60`. To make `add` safe to
re-run, pass `--if-exists skip` (leave the member as is) or `--if-exists
update` (converge: replaces the whole permission set, like `set`), both
`[experimental]`. The `--grant-admin` gate still applies first.

## Per-app access grants

```bash
gplay team grants list
gplay team grants set alice@example.com --package com.example.app --role reviewer      # upsert; admin needs --grant-admin
gplay team grants remove alice@example.com --package com.example.app --confirm         # drops one app, keeps the membership
```

`grants set --dry-run --output json` reports the resolved verb (create/update)
and the permission diff beside `requires`.

## Developer account addressing

Commands address the Developer account id recorded by `gplay auth login
--developer-id`; the override cascade (`--developer-id`) is in
`gplay-cli-usage`.
