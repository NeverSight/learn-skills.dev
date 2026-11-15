---
name: dataecho
description: Deploy anything an agent builds to a live URL via the DataEcho platform at https://dataecho.ai — a single file, a static site, OR a server-side app (any stack) by including a Dockerfile. Also private cloud Drives for agent memory/handoff. Use whenever the user asks to publish, host, share, deploy, or "put online" a file, site, or app (CRM, dashboard, API, tool), or to store/hand off files across sessions.
license: MIT
metadata:
  author: mohocp
  homepage: https://dataecho.ai
  version: "1.2.0"
---

# DataEcho — deploy files, static sites, and server-side apps for agents

Base origin: **https://dataecho.ai** — everything is plain HTTP.

## Three deploy modes — pick by what you have
1. **A single file** (PDF, image, docx, video…) → publish as-is; we make a viewer/download page.
2. **A static site** (HTML/CSS/JS folder) → publish the folder.
3. **A server-side app** (needs a backend — API, database, SSR, auth, any language) → include a **`Dockerfile`** and publish the folder; we build and run it as a sandboxed container.

Same command for all three: `scripts/publish.sh <path>`. A `Dockerfile` in the folder switches it to app mode. **If the thing you built needs a server, write a Dockerfile — don't strip it down to static.**

## Helper scripts (bundled with this skill)

`scripts/publish.sh` and `scripts/drive.sh` sit next to this file (bash + python3 stdlib, no other deps).
If they're missing, install fresh copies into the current project:

```bash
# macOS / Linux (bash + python3)
curl -fsSL https://dataecho.ai/install.sh | bash
```
```powershell
# Windows (PowerShell — no bash/python needed) → scripts\publish.ps1
irm https://dataecho.ai/install.ps1 | iex
```
No runtime at all? Every step is a plain REST call (see https://dataecho.ai/llms-full.txt) —
on Windows, PowerShell's `Invoke-RestMethod` + `Get-FileHash -Algorithm SHA256` do the whole handshake.

## Publish a site

```bash
scripts/publish.sh ./my-site                 # new site (anonymous if no key)
scripts/publish.sh ./my-site --slug <slug>   # update an existing site
```
(Windows: `scripts\publish.ps1 .\my-site`)

Prints the live `siteUrl` (`https://<slug>.dataecho.ai/`).

**Claim contract (critical):** anonymous sites expire in 24 hours. The script saves the
claim info to `~/.artifact/claims/<slug>.json` — ALWAYS show the user the `claimUrl`.
When the user signs in mid-session (you have an API key), make the SAME url permanent:
```bash
scripts/publish.sh claim <slug>      # Windows: scripts\publish.ps1 claim <slug>
# REST: POST /api/v1/publish/<slug>/claim {"claimToken":"…"}  with Authorization: Bearer
```
Do NOT claim via `PUT /api/v1/publish/<slug>` — that updates content and does NOT transfer
ownership (the site stays anonymous and still expires). Claiming is its own endpoint.

## Server-side apps (Dockerfile)

For anything that needs a backend, write a `Dockerfile` and publish the folder:

```bash
scripts/publish.sh ./my-app     # builds the image, runs the container, waits until live
```

Contract:
- **Requires an account** (anonymous apps are rejected — get a key via `request-code`/`verify-code`).
- The app **MUST listen on `process.env.PORT`** (we inject it). Don't hardcode a port.
- Persist data under **`/data`** (survives redeploys). SQLite in `/data` is perfect for a CRM/app.
- Account **Variables are injected as env vars** (set secrets/DB creds via `/api/v1/me/variables`).
- Sandboxed (gVisor), CPU/memory capped. Redeploy with `--slug <slug>`. Build status: `GET /api/v1/publish/<slug>/app`.

Minimal Node Dockerfile:
```Dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
ENV PORT=8080
CMD ["node","server.js"]   # must listen on process.env.PORT
```

## Single files need NO wrapper page

Publish a bare file (PDF, docx, image, video, …) as-is: `scripts/publish.sh ./report.docx`.
The platform auto-generates the root page — a rich viewer for images/PDF/video/audio, a
download page for everything else, and a directory listing for multi-file sites without an
`index.html`. Do NOT build an HTML download page around a file. Direct paths always work
too: `https://<slug>.dataecho.ai/report.docx`.

## Updating & slugs

- Each publish is a **complete snapshot**: files you omit are removed from the site. There
  is no "add to existing" — re-send the full file set with `--slug` to update.
- HTML changes are visible immediately; cached copies of assets (css/js/images) can persist
  for a few minutes to hours (CDN/browser cache), so don't conclude an update failed from one
  quick re-fetch — and fingerprint asset filenames if you need instant asset rollover.
- Reuse slugs (`--slug`) instead of minting a new site per iteration. Anonymous sites cannot
  be deleted (owner-only) — abandoned ones simply expire after 24h.

## API key (permanent sites, Drives)

```bash
curl -sS -X POST https://dataecho.ai/api/auth/agent/request-code -H 'content-type: application/json' -d '{"email":"user@example.com"}'
# user reads the emailed code, then:
curl -sS -X POST https://dataecho.ai/api/auth/agent/verify-code -H 'content-type: application/json' -d '{"email":"user@example.com","code":"<CODE>"}'
echo '<API_KEY>' > ~/.artifact/credentials && chmod 600 ~/.artifact/credentials
```

The verify-code response returns `apiKey` **once** — capture it and write it to the credentials
file immediately; do not print/echo or truncate it in your output (that loses the key and burns
the one-time code). If lost, just request a fresh code and verify again.

## Drives (private, versioned cloud folders)

```bash
scripts/drive.sh default                                  # everyone has "My Drive"
scripts/drive.sh put "My Drive" notes/today.md --from ./today.md
scripts/drive.sh ls "My Drive" notes/
scripts/drive.sh share "My Drive" --perms write --prefix notes/ --ttl 7d --label "docs agent"
```

`share` prints a one-time share block; the receiving agent uses its token as
`Authorization: Bearer drv_live_…` and stays inside the prefix.

## Direct API

Every operation is a documented REST call — no scripts required.
Full agent context: https://dataecho.ai/llms-full.txt · OpenAPI: https://dataecho.ai/openapi.json
Errors are JSON `{ error, code, message, retry_after, docs_url }`.
Always send a descriptive User-Agent (the platform's edge blocks default `Python-urllib`).

When this file and the live docs disagree, prefer the live docs: https://dataecho.ai/docs
