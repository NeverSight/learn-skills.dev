---
name: cookie
description: Chrome cookies to Playwright
---

# Copy Chrome cookies into playwright-cli

## Codex Compatibility
When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`, `Task`/`TaskCreate`/`TeamCreate`/`SendMessage` -> `spawn_agent`/`send_input`/`wait_agent` when available and allowed, and `EnterPlanMode`/`ExitPlanMode` -> a concise chat plan plus explicit approval.
Resolve `Read`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` to Codex file/shell/web tools, and map `~/.claude/...` paths to `~/.agents/...` or `~/.codex/...` unless the task explicitly targets Claude Code.

## Cursor Compatibility
When running this skill in Cursor Agent, translate Claude Code-only primitives before acting: `AskUserQuestion` -> `AskQuestion`; `TodoWrite` -> Cursor `TodoWrite` or an equivalent checklist; `Task`/`TaskCreate`/`TeamCreate`/`SendMessage`/multi-agent flows -> Cursor `Task` (subagents), parallel Tasks, or `run_in_background` when allowed (`TeamCreate`/`SendMessage` may have no exact match); `EnterPlanMode`/`ExitPlanMode` -> Plan mode (`SwitchMode` / `CreatePlan`) plus explicit user approval.
Resolve `Read`/`Write`/`Edit`/`StrReplace`/`Bash`/web/search/MCP via Cursor Composer or Agent equivalents. MCP names written as `mcp__server__tool` typically map to `call_mcp_tool` with configured server identifiers. Map `~/.claude/...` to `~/.cursor/skills/`, `.cursor/skills/`, and `.cursor/rules/` unless the task explicitly targets Claude Code.

Decrypt every cookie from the user's real Google Chrome and load them into a
playwright-cli session, so automation inherits all logged-in sessions (GitHub,
etc.) instead of starting logged out.

**macOS only.** Decryption uses the macOS Keychain + Chrome's AES-128-CBC
scheme. Linux/Windows use different key storage and are not handled here.

## Prerequisites

- macOS with Google Chrome installed (it can stay running — we snapshot the DB).
- `playwright-cli` on PATH (`playwright-cli --version`; else `npx playwright-cli`).
- Node.js (for the export script).

## Workflow

### 1. Export + decrypt all Chrome cookies

```bash
node ~/.claude/skills/cookie/scripts/export-chrome-cookies.mjs
# non-default profile: pass its dir name, e.g. "Profile 1"
node ~/.claude/skills/cookie/scripts/export-chrome-cookies.mjs "Profile 1"
```

Writes two files and prints a summary (`rows`, `exported`, `prefixStripped`…):

- `/tmp/chrome-load-cookies.js` — the run-code loader (the path that works).
- `/tmp/chrome-pw-cookies.json` — storageState, for inspection only.

**Keychain dialog (first run):** macOS shows "… wants to use the 'Chrome Safe
Storage' key". The script BLOCKS until the user clicks **Always Allow**. Tell
the user to click it; do not assume the script hung.

A healthy run has `prefixStripped` ≈ `exported` and `decryptErrors` near 0.

### 2. Open a PERSISTENT playwright-cli session

```bash
playwright-cli open --persistent
```

`--persistent` is required. The default profile is in-memory and loses every
cookie the moment the daemon restarts.

### 3. Load the cookies

```bash
playwright-cli run-code --filename=/tmp/chrome-load-cookies.js
```

Returns `{ ok, fail, total, sampleErrors }`. The loader adds cookies one at a
time inside try/catch, so a few malformed rows can't abort the batch — expect
`ok` to be nearly `total`.

> Do **not** use `playwright-cli state-load` for this. It runs a single batched
> `addCookies`, so one malformed row out of thousands fails the whole load
> atomically. The per-cookie loader above exists precisely to avoid that.

### 4. Verify BEFORE navigating anywhere

```bash
playwright-cli cookie-list --domain=github.com
```

Confirm the auth cookies are present FIRST. If you `goto` a site while its auth
cookie set is incomplete, the server can `Set-Cookie`-clear your session and
you'll have logged yourself back out. Only after cookies check out:

```bash
playwright-cli goto https://github.com   # then confirm the logged-in UI
```

### 5. Delete the plaintext token files 🔴

> **These two `/tmp` files hold every session token the user has. Delete them
> the moment the load succeeds — this is a hard requirement, not cleanup.**

```bash
rm -f /tmp/chrome-load-cookies.js /tmp/chrome-pw-cookies.json
```

Never commit these files or any `.playwright-cli/` / storageState artifacts.
Cookies are secrets.

## Notes & gotchas

- **Session cookies don't survive a restart.** Cookies with `expires: -1` (no
  expiry — browser-session only; ~45 of ~4000 last time) are correctly dropped
  when the daemon restarts. That's expected, not data loss. Persistent auth
  cookies (e.g. GitHub `user_session`) do survive.
- **Flush before closing.** Chromium writes added cookies to disk lazily. If you
  `close` and later reopen the persistent session, first stay on a real page
  (not `about:blank`) and wait ~4s before a graceful `close`, or the freshly
  added cookies are lost. Not needed if you keep the session open.
- **Re-run anytime.** The script regenerates plaintext on demand and holds no
  secrets itself, so it's safe to leave in the skill dir and re-run to refresh.
