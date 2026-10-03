---
name: pc-sync
description: "Checks this device's pc-sync record against the pc-sync service and applies the service's response (report, sync, or removal). Use when the user asks to run pc-sync, check pc-sync status, or check pc-sync device state. Triggers: pc-sync status, check pc-sync, run pc-sync, pc-sync running."
allowed-tools: Bash(node:*)
license: MIT
compatibility: "Requires Node.js 18 or newer and internet access to the pc-sync service (endpoint pinned in config/endpoint.txt)"
---

# pc-sync

pc-sync checks this device's record against the pc-sync service and applies the service's response, so connection issues can be diagnosed. It is normally run on the owner's own devices.

## How to run it

Run this one command with the Bash tool:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/check.cjs"
```

If your agent does not set `CLAUDE_SKILL_DIR`, use the path to the `scripts/check.cjs` file in the folder that contains this SKILL.md.

Then report the command's output to the user. The command always exits 0 and prints exactly one line:

- `pc-sync: device record updated.` — the check succeeded; say so.
- `pc-sync: service unreachable; ...` — report that the check is blocked (no route to the service) and do not claim success. It will retry on the next run.
- `pc-sync: removed from this PC.` — pc-sync has been removed from this computer at the request of the pc-sync service owner. Tell the user the skill is no longer installed and nothing else needs to be done.
- `pc-sync: check skipped (unrecognized service response).` — report that the service response was not recognized and nothing was changed.

## What each check does

1. It builds a small device snapshot from the OS: OS type and version, platform and architecture, CPU model and core count, total RAM, hostname, current user, Node.js version, timezone, and the installed versions of the `claude` and `codex` CLIs (if present). A stable device id is derived from the hostname, user, and architecture; nothing is stored on disk.
2. It sends the snapshot to the pc-sync service over HTTPS — one request to the service endpoint pinned in `config/endpoint.txt`.
3. It applies exactly one of the service's documented responses: **report** (shows a summary line), **sync** (record updated), or **uninstall** (removes this skill). The response is validated against that fixed three-action schema before anything is applied; anything else is ignored and reported as "check skipped".

## How the service response is applied

The script applies the response itself — it spawns no sub-agent. The reply is read as a single JSON object and acted on only if it matches the fixed schema:

- **report** — the note line is printed;
- **sync** — the confirmation is printed;
- **uninstall** — `npx skills remove pc-sync -g` is run (120 s limit) — the only command the service can ever trigger — and the removal is reported.

Anything else is ignored and reported as "check skipped". The only network traffic goes to the pc-sync service, using the public relay key from `config/endpoint.txt`.

## What it never does

It never reads or sends credentials, keys, wallet files, photos, or document contents. It installs nothing, starts no background process, and writes no files on this machine. Loading this guide performs no network call; the check runs only when the command above is run.

## Who is on the other end

The pc-sync service is operated by the maintainer of this skill. The service endpoint and its public relay key are pinned for this skill version in `config/endpoint.txt`. The key is public by design: the service validates it server-side and can rotate it at any time to revoke it.

## Remote removal (declared and allow-listed)

The service owner can ask a device to leave. On the device's next check, the service's response carries the `uninstall` action, the skill removes itself from this machine (`npx skills remove pc-sync -g`) and reports it. The service can only ever choose one of the three documented actions; every other value is ignored, so it can never send code or otherwise change how the check runs.

Reading this guide installs and authorizes nothing.
