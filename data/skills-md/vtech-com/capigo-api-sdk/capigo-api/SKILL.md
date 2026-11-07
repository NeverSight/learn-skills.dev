---
name: capigo-api
description: >
  Drive the Capigo platform through the installed `capigo` CLI — the entry point for any Capigo
  work an agent does for a tenant. Use this whenever a request maps to Capigo data or
  capabilities — tasks, boards, members, products, variants, brands, categories, product types,
  product properties and property definitions, units, warehouses, stock locations, inbound
  receipts, outbound shipments, stock transfers, availability, tenants, authentication,
  configuration — even when the user never names the CLI or Capigo itself, and in whatever
  language they ask: "create a task and assign it to someone", "what's on the board this week",
  "read or post comments on that task", "list products", "look up this SKU or barcode", "set
  this product's origin or voltage", "tag this product Hè", "products tagged Sale",
  "how many brands do we have", "tag this task urgent",
  "tasks labelled X", "plan an inbound receipt for this PO", "which warehouse can cover this
  order". Also the reference for how the CLI itself works: detecting the install, logging in,
  picking a tenant, exit codes, JSON output, and self-diagnosing a misbehaving command. If a
  request touches Capigo and you are unsure how to talk to it, reach for this skill first
  instead of guessing raw API calls.
---

# Capigo CLI operator

Use `capigo` as the normal interface to Capigo. The installed binary is self-documenting and
the Public API will continue to grow, so this skill teaches a discovery workflow rather than
duplicating the command tree or API reference.

## 1. Preflight the environment and authentication

Start each new environment or session by resolving the executable with the shell's native lookup
(`command -v capigo` in a POSIX shell or `Get-Command capigo` in PowerShell), then run:

```bash
capigo version
```

Use the resolved executable consistently for version, help, preflight, and execution; mixing help
from one build with commands sent through another produces false flag and capability errors.

If the shell cannot find `capigo`:

1. Inspect the OS, architecture, shell, and available package managers using read-only checks.
2. Tell the user that the Capigo CLI is not installed and recommend the official installation
   guide: <https://github.com/vtech-com/capigo-api-sdk#installation>.
3. Prefer the installation path that fits the detected machine. For example, when Homebrew is
   present, suggest `brew install --cask vtech-com/tap/capigo`; the guide also covers GitHub
   Releases and Go-based installation with their platform-specific caveats.
4. Do not install software or change the machine merely because the binary is missing. Wait
   for the user's authorization, then verify the result with `capigo version`.

After the version check succeeds, run the read-only authentication and connectivity probe:

```bash
capigo health
```

Interpret it by exit code and its stdout `error` object:

- Exit `0`: the API is reachable and the configured key was accepted. Continue.
- Exit `2`: the key is missing, malformed, or rejected. Run `capigo auth login --help`, tell the
  user to create or retrieve their key while signed in at <https://platform.capigo.app>, and ask
  them to run the supported login command locally. Then retry `capigo health`. Code
  `AUTH_MISSING_HEADER` is the first-run case — no key is configured at all, so the CLI never
  reached the API. Nothing about it is transient: do not retry until the user has logged in.
- Exit `6`: connectivity failed. Diagnose DNS, network access, or the configured API URL; do not
  mislabel it as an authentication problem or ask the user to log in again.
- Any other non-zero exit: read the error object and `capigo help exit-codes` before recommending
  a recovery step.

Do not use `capigo auth whoami` as a preflight. Its `/me` route is not implemented, so a 404 does
not say whether the configured key is valid.

Authentication secrets belong to the user. Never ask them to paste an API key into chat, inspect
credential files or environment variables to recover it, print it, place it in examples, or expose
it through shell tracing. Guide the user through `capigo auth login --help` and let them enter the
key locally through the supported flow.

### A key reaches one workspace

A key is bound to the single workspace it was created in; the platform's API keys page shows which.
That bound is enforced server-side on every request, so it holds regardless of what the CLI sends:

- Naming another workspace — `--tenant`, `CAPIGO_TENANT`, or a `default_tenant` that belongs to a
  different key — fails with exit `3`. The key is valid; the workspace is not its own.
- Naming none does **not** widen the call. The request still reads only the key's workspace, and
  `meta` names no tenant, because the CLI reports the tenant it resolved and it resolved none. If
  the user needs to know which workspace an answer belongs to, pass the key's own workspace as
  `--tenant`: same rows, and `meta.tenant` appears.
- `capigo tenants list` is **not** this key's reach. It lists the workspaces the account belongs to
  and is not narrowed to the key, so treat it as a directory of the account, never as the set of
  workspaces the current key can be pointed at.
- Older keys may carry no workspace and reach every workspace the account has. Do not infer a key's
  reach from its prefix or age; take it from the API keys page, or from the exit code of the call
  you were about to make.

Working in several workspaces therefore takes one key each — one profile per key, or
`CAPIGO_API_KEY` and `CAPIGO_TENANT` set per invocation. There is no `--profile` flag, and no
command creates a profile: a second one is a hand edit of `~/.capigo/config.json`.

## 2. Discover the live command surface

Once `capigo version` succeeds, use built-in help progressively:

```bash
capigo --help
capigo <group> --help
capigo <group> <command> --help
```

Read only the group and command relevant to the user's intent. A runnable command page includes
its purpose, usage, flags, constraints, examples, and output. Do not reconstruct a command from
memory, guess a flag, or treat this skill as a command inventory.

Pull cross-cutting contracts from the binary when they matter:

```bash
capigo help tenancy
capigo help output
capigo help exit-codes
capigo help soft-delete
capigo help versioning
```

The installed help wins for CLI spelling and behavior because it ships with that exact build.
If help and this skill disagree, follow help and report the mismatch for the skill maintainer.

## 3. Plan, execute, and verify

Before a call:

1. Translate the request into one mechanical Capigo intent.
2. Discover the group and command from help.
3. Read the leaf command's help before constructing flags or JSON.
4. Resolve the tenant. If a write's tenant is ambiguous, ask before writing. Do not add a
   redundant confirmation when the user already authorized the exact resource, change, and
   tenant. Task creation still follows the separate assignee-choice gate below. Remember that a
   key is bound to one workspace: on a write, name that workspace explicitly rather than letting
   the default carry it, so `meta.tenant` is on stdout to verify afterwards.
5. Use the conventions in [`references/cli-conventions.md`](./references/cli-conventions.md).

After a call:

1. Parse the single JSON document on stdout.
2. Check for an `error` key before trusting `data`; partial results can contain both.
3. On writes, verify `meta.tenant` and the returned object rather than assuming the intended
   tenant or mutation was used.
4. Report the result without exposing credentials, raw auth headers, or unrelated tenant data.

## 4. Handle missing commands and failures

If an expected command is absent, re-check the root and relevant group help. A name you guessed
is not evidence that the capability is unavailable. The operation may live under a neighboring
group, or the installed CLI may be older than the current API.

If a command fails:

1. Read the stdout `error` object, especially `message`, `next`, `request_id`, and any
   `capability_note`.
2. Read the leaf command help and `capigo help exit-codes`.
3. Use `--verbose` only when the redacted HTTP trace is actually needed.
4. Retry only when the error class supports it, such as a transient network or rate-limit
   response. Do not retry validation, auth, permission, conflict, or ambiguous write outcomes
   blindly.

A failed write does not prove the API lacks the capability. Do not invent destructive recovery
steps such as recreating resources, changing identifiers, or bypassing tenant handling.

## 5. Use the Public API specification sparingly

Public specification: <https://platform.capigo.app/api/openapi>

For ordinary user operations, stop at CLI help and execute through `capigo`. Open the spec only
when at least one of these is true:

- the user explicitly asks about the Public API contract or is building an integration;
- you are developing or reviewing this SDK;
- live help confirms a CLI gap and you need to distinguish "not exposed by this CLI" from
  "not present in the Public API";
- a version mismatch or inaccurate help/spec claim must be diagnosed.

When inside the SDK repository, prefer its versioned `api/openapi.json` for the release being
worked on; use the public URL to check the currently published contract. The spec defines API
paths and schemas, not the installed CLI's flag spelling. Finding an endpoint in the spec does
not authorize bypassing the CLI for a routine tenant operation. Report the gap or recommend an
upgrade. Call raw HTTP only when the user's task is explicitly to build or test a Public API
integration and that work is separately authorized.

## 6. Load special-case guidance only when needed

Most operations need no bundled domain guide: leaf help is sufficient.

For an operation that creates, traverses, or changes a relationship, load only the relevant
domain reference after reading leaf help:

- [`references/domains/products.md`](./references/domains/products.md) for products, variants,
  product references, product properties (`capigo property-definitions`), and catalog tags
  (`products tags`, `variants tags`, `capigo tags list`);
- [`references/domains/tasks.md`](./references/domains/tasks.md) for tasks, assignees, subtasks,
  comments and mentions, and labels (`--label`, `capigo labels list`);
- [`references/domains/boards.md`](./references/domains/boards.md) when placing a task on a board
  or list, or reading a board by code;
- [`references/domains/wms.md`](./references/domains/wms.md) for anything under `capigo wms`:
  warehouses, locations, availability, and the four stock documents.

For product creation, for any write to `properties` or a property definition, and for adding or
removing a catalog tag, read `products.md` after the leaf help. For task or subtask
creation, or for posting a comment, read `tasks.md` after the relevant leaf help; read `boards.md`
as well only for board placement. For any `capigo wms` write, and for reporting a WMS read to the user, read `wms.md`: its
verdicts, null costs, and statuses are easy to report wrongly. Do not load a domain reference for
unrelated listing or search work.

## Scope boundary

This skill covers Capigo CLI operation and Public API discovery. It does not define an
organization's product-code, barcode, naming, approval, or data-governance policies. Apply those
from the user's own policy or a separate organization-specific skill.
