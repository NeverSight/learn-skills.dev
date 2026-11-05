---
name: microsoft-365
description: Use when the user asks to 'check my email/Teams/calendar', 'what meetings do I have', 'any messages about X', or whenever a task needs live Microsoft 365 data rather than memory. Microsoft 365 (Graph) access to email, Teams, calendar, and SharePoint — scriptable scans plus an interactive query.py.
license: Apache-2.0
compatibility: Requires Python 3.10+. Dependencies and Azure AD app are auto-configured on first run.
metadata:
  authors:
    - Artem Rozumenko <artem_rozumenko@epam.com>
  version: "0.2.0"
---

# Microsoft Graph Skill

Provides Microsoft 365 data access via the Microsoft Graph API. Two operating modes:

## Mode 1 — LLM-less Scan Scripts (Scheduled)

Four scripts run autonomously on a schedule without involving an LLM:

| Script | What it scans |
|---|---|
| `scripts/scan-email.py` | Inbox messages newer than `--since` |
| `scripts/scan-teams.py` | Teams channel messages newer than `--since` |
| `scripts/scan-calendar.py` | Calendar events starting within `--since` window |
| `scripts/scan-sharepoint.py` | SharePoint/OneDrive files modified within `--since` |

### Common CLI arguments

```
--since     Lookback window, e.g. 1h, 4h, 24h, 7d  (default: 1h)
--output    Path for JSON output                     (default: m365-inbox.json)
--relay     Path to a script or webhook to call when items are found
--role      Role name passed to the relay for routing
```

### Per-script additional arguments

| Script | Extra flag | Purpose |
|---|---|---|
| `scan-email.py` | `--sender boss@company.com` | Filter to a specific sender |
| `scan-teams.py` | `--team-id TEAM_ID` | Limit to a single team |
| `scan-calendar.py` | `--hours-ahead 24` | Look forward N hours instead of backward |
| `scan-sharepoint.py` | `--site-id SITE_ID` | Scan a SharePoint site instead of personal OneDrive |

### How results are delivered

1. If no items are found the script exits silently (exit code 0).
2. If items are found they are **appended** (not overwritten) to `--output` as a JSON array.
3. If `--relay` is provided the script calls:
   ```
   python3 <relay> --role <role> --data <output_path>
   ```
   The relay script is called with the found items and is responsible for
   any further routing or notification.

### Output record shape

Every item in the output JSON array has the following fields:

```json
{
  "source":  "email | teams | calendar | sharepoint",
  "ts":      "2026-04-04T11:00:00+00:00",
  "summary": "one-line description",
  "detail":  { /* raw API fields */ },
  "urgent":  false
}
```

### Example cron entry

```
0 * * * *  cd /path/to/project && python3 scripts/scan-email.py --since 1h --relay scripts/notify.py --role triage
```

## Mode 2 — Interactive Query via Claude (Bash Tool)

`scripts/query.py` is called by Claude during a session when the user asks about their Microsoft 365 data.

**Typed subcommands (recommended):**
```bash
python3 scripts/query.py email --filter "isRead eq false" --select "subject,from" --top 20
python3 scripts/query.py teams channels --team-id TEAM_ID
python3 scripts/query.py teams messages --team-id TEAM_ID --channel-id CHANNEL_ID --top 20
python3 scripts/query.py calendar --start 2026-04-04 --end 2026-04-11
python3 scripts/query.py sharepoint files --drive-id DRIVE_ID --path /Documents
```

**Sample file mode:**
```bash
python3 scripts/query.py --sample samples/email/unread-today.yaml
```

**Raw endpoint mode:**
```bash
python3 scripts/query.py --endpoint "/me/messages" --filter "isRead eq false" --select "subject,from" --top 20
python3 scripts/query.py --endpoint "/me/calendarView" --params "startDateTime=2024-01-01T00:00:00Z&endDateTime=2024-01-07T23:59:59Z"
```

Results are printed as pretty-printed JSON to stdout. Claude reads and summarises them for the user.
All pages are fetched automatically via `@odata.nextLink` pagination.

Sample YAML files in `samples/` describe pre-built queries that Claude can run by name.

## Authentication

Scripts auto-install Python dependencies (from `requirements.txt`) into
`~/.msgraph-skill/.venv/` on first run — no manual `pip install` or venv creation
needed. A built-in Azure AD app ID
is used by default, so no environment variables or Azure portal setup is required
for most users.

Token cache is stored at `~/.msgraph-skill/token_cache.json` (shared across all
projects — authenticate once, use everywhere).

### Login flow (important for Claude)

The default `login` opens an **interactive browser** (auth-code + PKCE on a
localhost redirect). This passes Conditional Access policies that block the
device-code flow. Because it needs a browser + a local redirect listener, **ask
the user to run it in their own terminal**:

```
python3 scripts/auth.py login            # Browser auth-code+PKCE (default)
python3 scripts/auth.py status           # Check token validity
python3 scripts/auth.py logout           # Clear cached credentials
```

If the browser flow can't be used (no GUI / SSH), fall back:

```
python3 scripts/auth.py login device     # Device-code — relay LOGIN_URL/LOGIN_CODE to user
python3 scripts/auth.py login authcode   # Browser via nativeclient redirect (manual URL paste)
```

For `login device`, the output contains `LOGIN_URL=...` and `LOGIN_CODE=...` —
relay both to the user. Note: many tenants block device-code via Conditional
Access ("...an authentication flow that is restricted by your admin"); prefer
the default browser flow.

### Environment variables (optional)

| Variable | Default | Description |
|---|---|---|
| `SDLC_SKILLS_CACHE_DIR` | `~/.msgraph-skill` | Shared cache root for all sdlc-skills (token cache, venv). When set, the skill stores its data under `$SDLC_SKILLS_CACHE_DIR/msgraph/`. |
| `MSGRAPH_CLIENT_ID` | `3d7688c6-f449-4d04-8b0d-57d94818e922` | Public client with localhost redirect; override with your own Azure AD app |
| `MSGRAPH_TENANT_ID` | `common` | Restrict to a specific tenant |

Variables can be set via environment or in a `.env` file at the skill root or cwd.
Most users do not need to set these.

### Custom Azure AD app (advanced)

If your organisation blocks third-party app IDs or you need additional permissions,
register your own Azure AD app:

1. [Azure portal → App registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps) → New registration.
2. Add delegated permissions: `Mail.Read`, `Calendars.Read`, `Team.ReadBasic.All`,
   `Channel.ReadBasic.All`, `Sites.Read.All`, `Files.Read.All`.
3. Under Authentication → Add platform → Mobile and desktop, enable the
   `http://localhost` redirect URI (required for the default browser flow).
4. Set `MSGRAPH_CLIENT_ID=<your-app-id>` in your `.env` and re-run login.

## Installation

### Claude Code plugin marketplace

```
/plugin marketplace add arozumenko/sdlc-skills
/plugin install microsoft-365@sdlc-skills
```

### Direct install via npx

```bash
npx github:arozumenko/sdlc-skills init --skills microsoft-365 --target claude
```

Python dependencies are installed automatically into `~/.msgraph-skill/.venv/`
on first script run — no manual setup needed.

### First-time authentication

```bash
python3 scripts/auth.py login
```

## Known issues / troubleshooting

- **Conditional Access blocks device-code** — Error: *"Your sign-in was
  successful but does not meet the criteria to access this resource ... an
  authentication flow that is restricted by your admin."* Many tenants block the
  device-code flow via Conditional Access. This is why the default `login` now
  uses the interactive browser (auth-code + PKCE) flow. If you still see this
  message *after* the browser sign-in, the CA policy is keying on device
  compliance / managed app / location rather than the auth flow — that needs
  your tenant admin (check Entra → Sign-in logs → your sign-in → Conditional
  Access tab for the exact policy).

- **`AADSTS50011` redirect URI mismatch** — The configured `MSGRAPH_CLIENT_ID`
  app has no `http://localhost` redirect registered. The default app does; if
  you override it with your own app, register the `http://localhost` redirect
  (Authentication → Mobile and desktop applications). The legacy device-code
  flow (`login device`) needs no redirect URI if you must avoid this.

- **Default app is a shared public client** — `3d7688c6-...` is a third-party
  public-client app reused because it has the `http://localhost` redirect. It is
  not controlled by this project. For a durable / auditable setup, register your
  own Azure AD app (see *Custom Azure AD app* above) and set `MSGRAPH_CLIENT_ID`.

- **Teams scopes may not consent on the default app** — The default app's
  registered scopes do **not** include `Team.ReadBasic.All` /
  `Channel.ReadBasic.All`. Mail, calendar, and SharePoint work; Teams scans may
  fail with a consent error. Use your own app registration with all six
  delegated permissions if you need Teams.
