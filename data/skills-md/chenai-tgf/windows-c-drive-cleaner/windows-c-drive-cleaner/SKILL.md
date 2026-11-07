---
name: windows-c-drive-cleaner
description: >-
  Scans and cleans regenerable Windows C: drive caches using a configurable
  target list (uv, WPS, Notion, IDE caches, Temp, Package Cache, Windows Update
  download, etc.). Use when the user asks to free C: space, clean disk caches,
  reclaim disk space on Windows, or explicitly asks to use this skill /
  windows-c-drive-cleaner. Always scan and confirm before deleting. Dangerous
  targets require multi-step confirmation with risk explanation. Works with any
  agent that can load SKILL.md; also runnable as standalone PowerShell.
---

# Windows C Drive Cleaner

Help free space on Windows system drive (`C:`) by scanning and cleaning **configurable, mostly regenerable caches**.

This skill is for **any coding agent** that supports `SKILL.md`. Respond in the **same language the user is using**.

## When to use

- User mentions C: full / low disk / clean caches / reclaim Windows disk space
- User says to use this skill (`windows-c-drive-cleaner`)
- User asks to generate a reusable cleanup script from the current machine

## Do not use for

- Deleting random project source trees
- Manual `WinSxS` deletion
- Silent deletion of dangerous targets without multi-step confirmation

## Layout

```text
windows-c-drive-cleaner/
  SKILL.md
  README.md
  config/targets.json           # editable whitelist (per machine)
  config/targets.example.json   # template
  scripts/Invoke-CDriveCleanup.ps1
  scripts/Scan.bat
  scripts/Clean-Safe.bat
  reference.md                  # red lines and confirm protocol
```

## Workflow (mandatory)

Copy and track:

```text
Cleanup progress:
- [ ] 1) Detect OS + load config
- [ ] 2) Scan (no delete)
- [ ] 3) Present report + ask what to clean
- [ ] 4) Clean only confirmed targets
- [ ] 5) Summarize in user's language + optional desktop log
- [ ] 6) Offer reusable script (ask once)
```

### 1) Load config

- Prefer `config/targets.json` in this skill folder.
- If missing, copy from `config/targets.example.json`.
- Paths must use env vars (`%LOCALAPPDATA%`, `%APPDATA%`, `%USERPROFILE%`, `%TEMP%`) so the skill works across PCs/users.
- Users may edit `enabled`, `paths`, `tier`, `requiresAdmin` per machine.

### 2) Scan first (never delete in this step)

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill>/scripts/Invoke-CDriveCleanup.ps1" -Mode Scan -Tiers safe,caution,dangerous
```

Parse the `JSON_SUMMARY` block from stdout. Also note C: free GB.

### 3) Report + ask

Show a concise table:

- name / id
- size GB
- tier (`safe` / `caution` / `dangerous`)
- exists or missing

Then ask which set to clean, e.g.:

- all `safe`
- `safe` + selected `caution`
- specific ids

Do **not** clean until the user confirms the selection.

### 4) Clean confirmed targets only

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill>/scripts/Invoke-CDriveCleanup.ps1" -Mode Clean -Tiers safe -Elevate -LogPath "$env:USERPROFILE\Desktop\CleanCache_log_<timestamp>.txt"
```

For selected ids:

```powershell
... -Mode Clean -Ids "uv-cache,wps-addons,notion-caches" -Tiers safe,caution -Elevate
```

Elevation rules:

1. Prefer `-Elevate` (UAC prompt) when any selected target has `requiresAdmin: true`.
2. If elevation fails/cancelled, clean non-admin targets, report leftovers that need admin, and give the exact elevated command.

### 5) Brief the user

In the user's language, report:

- per-folder before/after/freed (or point to the details table)
- total freed (folder sum)
- C: free before -> after
- anything partial / need-admin
- path to log file if written

### 6) Offer a reusable script

After a successful cleanup (or when user asks), **ask** whether they want a standalone reusable script/bat for this machine.

If yes:

- Generate ASCII-named scripts (avoid encoding issues), UTF-8 BOM for `.ps1`
- Base them on `scripts/Invoke-CDriveCleanup.ps1` + current `config/targets.json`
- Put on Desktop unless user chooses another path
- Mention UAC behavior and that dangerous tiers stay disabled unless explicitly enabled

## Target tiers

| Tier | Meaning | Confirmation |
|------|---------|--------------|
| `safe` | Regenerable caches | Confirm selection once after scan |
| `caution` | Usually OK, may affect repair/install caches | Confirm explicitly (name the ids) |
| `dangerous` | Data/app risk | See [reference.md](reference.md) multi-step protocol |

Default clean suggestion: **enabled + safe** (and caution only if user asks).

## Red lines (defaults)

See [reference.md](reference.md). Summary:

- Never silently delete `dangerous` targets (`enabled: false` by default).
- Never manually wipe `C:\Windows\WinSxS`.
- Do not uninstall random programs unless user explicitly requests and confirms.
- Prefer migrate/junction for large installs (e.g. TeX Live) over blind delete.

## Auto-detect extras (optional)

If scan results are small but C: is still nearly full, optionally probe and **report only** (do not delete until confirmed):

- Large folders under `%LOCALAPPDATA%` / `%APPDATA%` (>= 1 GB)
- `C:\texlive`, Python `site-packages` heavy libs (`torch`, `paddle`, `tensorflow`)
- OEM leftovers under `C:\` (non-system folders >= 1 GB)

Propose adding them to `config/targets.json` with an appropriate tier.

## Examples

**User:** "My C: drive is full again. Can you check?"

1. Scan
2. Show top reclaimable safe/caution items
3. Ask what to clean

**User:** "Use windows-c-drive-cleaner to clean safe caches"

1. Scan (still required)
2. Confirm list briefly
3. Clean `-Tiers safe -Elevate`
4. Summarize + offer reusable script

**User:** "Also delete the IDE state.vscdb under AppData"

1. Treat as `dangerous` (e.g. `cursor-state-vscdb` if that target matches)
2. Follow multi-step confirmation in [reference.md](reference.md)
3. Only then clean that id

## Additional resources

- Red lines and confirmations: [reference.md](reference.md)
- Install / GitHub usage: [README.md](README.md)