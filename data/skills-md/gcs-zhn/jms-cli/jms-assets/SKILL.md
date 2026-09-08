---
name: jms-assets
description: >-
  JumpServer v4 asset discovery and resolution: `jms ls` (list / keyword
  search of authorized assets, -n count), the search_assets/list_assets/
  resolve_asset library API, AssetInfo connection parameters, account alias
  and protocol selection rules (select_account: @USER first, then the first
  non-@ alias/username, then the first account, finally @INPUT;
  select_protocol: ssh first), exact-name match preferred over the first
  search hit, and limit/offset pagination semantics. Use whenever the user
  lists or searches assets, hits a not-found error (No asset found / Asset
  'x' not found), resolves connection parameters, writes code that calls the
  assets library, or wants to confirm an asset is reachable — even if they
  just ask "what assets are there" or "is x on prod". CLI first (jms ls);
  programmatic use via search_assets / resolve_asset.
compatibility: Python >= 3.10; uv environment (requests is a project dependency)
metadata:
  author: codex
  version: "1.0"
  project: jms-cli
---

# jms-assets — Asset discovery & resolution

## When to use

Trigger on mentions of ls, assets, search, listing, resolve, connection
parameters, account alias, protocol selection, `AssetInfo`, `No asset found`,
or asset-not-found — even without naming the assets module. Use cases:
seeing which assets exist on a server, filtering by keyword, resolving a
name into connectable (address/account/protocol) parameters, and debugging
"asset not found".

## Prerequisites

- This skill consumes an authenticated `JMSSession` (`jms-auth` skill) and
  server-alias resolution (`jms-config` skill): load the config and log in
  before querying assets.
- Downstream consumption (exec/login/SFTP) belongs to the `jms-terminal` /
  `jms-transfer` skills. This skill only finds and resolves the asset.

## Core facts (read first)

1. **CLI**: `jms ls [server] [-q keyword] [-n limit]`. `server` is the config
   alias (e.g. `prod`); omit it for the default server; `-q` searches;
   `-n` caps results (default 50). **Do not prefix the server with `@`**
   (`jms ls @prod` looks up the alias `@prod` and fails with
   `Server '@prod' not found`); the `asset@server` syntax is only for
   exec/login/sftp target arguments.
2. **Library API**: `search_assets(session, keyword) -> list[dict]` (all
   pages), `list_assets(session, limit=50) -> list[dict]` (lazy pagination,
   never beyond limit), `resolve_asset(session, name, account=None,
   protocol=None) -> AssetInfo`. `AssetInfo` has
   `id/name/address/account/protocol/platform/org_id`.
3. **Resolution rules**: `resolve_asset` prefers an exact name match, falling
   back to the first search hit; then it fetches detail for
   `permed_accounts`/`permed_protocols`. The account must be an **alias**
   (`select_account` priority: `@USER` > first non-`@` alias or username >
   first account > `@INPUT`); protocol defaults to `ssh` first
   (`select_protocol`).
4. **Pagination**: list endpoints page by `limit`/`offset` (`api_get_all`
   fetches lazily until count); `jms ls -n` is the limit passed to
   `list_assets`.

## Workflow

### A. CLI first (user operations)

```bash
uv run jms ls                      # default server, max 50
uv run jms ls prod                 # specific server alias (no @)
uv run jms ls -q mysql             # keyword search
uv run jms ls -n 100               # more results
uv run jms ls --config /tmp/cfg.yaml   # explicit config path (hidden option)
```

When troubleshooting, run `jms ls` first to confirm the name spelling and
alias before `jms exec/login/sftp`.

### B. Library API (programmatic)

```python
from jms import JMSSession, resolve_asset, search_assets, list_assets
from jms.config import load_config

sess = JMSSession(load_config().get_server("prod"), otp_prompt=lambda: input("MFA: "))
sess.login()

all_assets = list_assets(sess)                 # default limit=50
matched = search_assets(sess, "mysql")         # all pages
info = resolve_asset(sess, "web")              # exact name first; else first hit
print(info.address, info.account, info.protocol)

# Explicit account/protocol override (e.g. SFTP)
info2 = resolve_asset(sess, "web", account="@USER", protocol="sftp")
```

### C. Common failure troubleshooting

| Symptom | Root cause | Fix |
|---|---|---|
| `Asset 'x' not found` (CLI) | misspelled name, or not in this server's grants | `jms ls [server]` to confirm |
| `No asset found matching 'x'` (library) | search returned nothing | try another keyword/server |
| `Server '@prod' not found` | `@` prefix on the ls server arg | drop the `@`, pass the alias |
| account not what was expected (e.g. display name) | `select_account` uses alias rules | pass an explicit `account=` |
| protocol is not SSH | no ssh in the asset's granted protocols | pass an explicit `protocol=`, or accept the first protocol |

### D. Verification

After touching assets code, run the deterministic regression:

```bash
uv run pytest tests/test_assets.py -q
```

Real-server cases are gated by `JMS_TEST_*` env vars and skip automatically
without them.

## Scope & Boundaries

> - Capabilities, commands, subcommands, flags, parameters, environment
>   variables, endpoints, and file paths **not mentioned in this skill are not
>   part of this skill**. Do not guess or extrapolate them from related tools,
>   documentation memory, or pattern-matching across similar CLIs.
> - If the user asks for functionality outside this skill, stop and ask — do
>   not invent it.
> - The consuming agent is not responsible for completing or improving the
>   skill. Discovering missing functionality is a signal to **ask the user**,
>   not to fill the gap silently.
> - If the skill's instructions appear wrong, contradictory, outdated, or
>   produce errors when executed, stop and consult the user before proceeding.
>   Do not "fix" the skill on the fly, substitute an alternative command, or
>   retry with guessed parameters.
> - Modifying or extending the skill itself requires explicit user permission
>   and should be routed back through `skill-creator`.

This skill covers asset discovery and resolution only; auth belongs to
`jms-auth`, connection and transfer to `jms-terminal` / `jms-transfer`. Admin
asset CRUD (create/modify/delete assets, grant management) is out of the
current project scope and not extended here.
