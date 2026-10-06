---
name: kb-m365-fetch
description: >
  Pull Microsoft 365 project context into .raw/ — Outlook mail, Teams chats and
  channels, attachments, SharePoint — via deterministic Graph API scripts with an
  LLM fallback when a scope is blocked by tenant admin consent.
  Triggers on: "fetch emails", "pull teams chats", "sync m365",
  "graph fetch", "/kb-m365-fetch".
allowed-tools: Read Bash Grep Glob
---

# kb-m365-fetch: Pull M365 Context into `.raw/`

Two paths, and they are not interchangeable:

| Path | Script | Nature |
|---|---|---|
| **Primary** | `.agents/skills/kb-m365-fetch/scripts/graph-fetch.ps1` | Deterministic. Graph API. Reproducible. |
| **Fallback** | `.agents/skills/kb-m365-fetch/scripts/m365-copilot.py` | LLM-mediated. Use only when a scope is admin-blocked. |

Prefer Graph. Copilot output is a summary produced by a model — it is evidence
of what Copilot said, not a verbatim record. Never mix the two in one page
without labelling which is which.

---

## Primary: graph-fetch.ps1

```bash
pwsh -File .agents/skills/kb-m365-fetch/scripts/graph-fetch.ps1                                  # config defaults
pwsh -File .agents/skills/kb-m365-fetch/scripts/graph-fetch.ps1 -Modules chats,emails -Hours 72  # targeted
```

Parameters (all optional; `-1` means "use the config value"):

| Parameter | Meaning |
|---|---|
| `-Config <path>` | Alternate config file. Defaults to `kb-config.yaml`. |
| `-Hours <n>` | Look-back window. Config: `window.hours` (24). |
| `-Top <n>` | Max items per module. Config: `window.top` (100). |
| `-ChatLimit <n>` | Max chats scanned. Config: `window.chat_limit` (50). |
| `-Modules a,b,c` | Comma-separated override of the enabled set. |

### Configuration: `kb-config.yaml`, section `m365`

Modules are toggled here, and outputs are routed here. Project name and keywords
come from the `project` section.

A legacy flat `m365-config.json` (with `project_name`/`keywords` at the top
level) is still read when no `kb-config.yaml` exists, so vaults migrate without
breaking. `-Config` overrides both.

| Module | Default | Output |
|---|---|---|
| `emails` | on | `.raw/msoffice/` |
| `chats` | on | `.raw/msoffice/` |
| `teams_channels` | on | `.raw/msoffice/` |
| `attachments` | on | `.raw/msoffice/attachments/` |
| `chat_attachments` | on | `.raw/msoffice/chat-attachments/` |
| `transcripts` | **off** | `.raw/msoffice/transcripts/` |
| `sharepoint` | **off** | `.raw/sharepoint/` |

### Admin-consent trap — read before enabling a module

In some tenants, certain delegated scopes require Entra ID admin consent.
Requesting one at `Connect-MgGraph` time makes the **entire sign-in fail** — not
just that module. One greedy scope takes down the whole fetch.

- `transcripts` needs `OnlineMeetingTranscript.Read.All` → admin consent. Leave off.
- `sharepoint` uses `Sites.Read.All`, which **works** in most tenants.
- Chat file attachments download through `Sites.Read.All` via
  `GET /shares/{shareId}/driveItem/content`. `Files.Read.All` is **not** needed
  and is often admin-blocked — do not add it.

Enabling `sharepoint` also requires `sharepoint.site_host` and
`sharepoint.site_path`, which are empty by default.

---

## Fallback: m365-copilot.py

```bash
python3 .agents/skills/kb-m365-fetch/scripts/m365-copilot.py
COPILOT_DEBUG=1 python3 .agents/skills/kb-m365-fetch/scripts/m365-copilot.py   # dump WebSocket frames
```

- First run opens a browser for manual M365 login. The session persists in
  `.browser-session/` (gitignored) and is reused afterwards.
- `stderr` carries progress; `stdout` carries only the final response, so it
  pipes cleanly.
- Responses land in `.raw/msoffice/` with a timestamped filename.

---

## After fetching

`.raw/` is immutable source material — **never edit what these scripts wrote**.
Hand off to `wiki-ingest` to turn it into wiki pages.

Sanity-check the counts the script prints. A run that reports scanning far fewer
chats than it matched has silently lost data; that exact bug existed once
(a `Select-Object -Unique` collapsed 62 chats to 1) and printed a plausible
number while doing so.
