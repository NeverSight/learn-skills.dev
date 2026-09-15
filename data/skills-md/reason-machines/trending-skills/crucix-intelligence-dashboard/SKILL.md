---
name: crucix-intelligence-dashboard
description: Personal intelligence agent that aggregates 27 OSINT data sources into a self-hosted Jarvis-style dashboard with Telegram/Discord bots, LLM analysis, and real-time alerts.
triggers:
  - set up Crucix intelligence dashboard
  - add OSINT monitoring with Crucix
  - configure Crucix alerts and bots
  - integrate LLM with Crucix intelligence
  - watch multiple data sources for changes
  - set up self-hosted intelligence terminal
  - configure Crucix Telegram or Discord bot
  - add real-time world monitoring dashboard
---

# Crucix Intelligence Dashboard

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Crucix is a self-hosted intelligence terminal that pulls from 27 open-source data feeds (satellite fire detection, flight tracking, radiation monitoring, conflict data, market prices, maritime AIS, economic indicators, and more) every 15 minutes, renders everything on a WebGL globe dashboard, and optionally pushes alerts to Telegram/Discord with LLM-enhanced analysis.

---

## Installation

```bash
git clone https://github.com/calesthio/Crucix.git
cd crucix
npm install          # installs Express (only hard dependency)
cp .env.example .env # then edit .env with your API keys
npm run dev          # dashboard at http://localhost:3117
```

**Docker:**
```bash
cp .env.example .env
docker compose up -d
# sweep data persists in ./runs/ via volume mount
```

**Requirements:** Node.js 22+ (uses native `fetch`, top-level `await`, ESM modules)

**If `npm run dev` exits silently:**
```bash
node --trace-warnings server.mjs   # bypasses npm script runner (useful on Windows PowerShell)
node diag.mjs                       # diagnoses Node version, module imports, port availability
```

---

## Environment Configuration (`.env`)

```dotenv
# ── Core Free APIs (highly recommended) ──────────────────────────────────────
FRED_API_KEY=           # Federal Reserve economic data — fred.stlouisfed.org
FIRMS_MAP_KEY=          # NASA satellite fire detection — firms.modaps.eosdis.nasa.gov
EIA_API_KEY=            # US Energy Info Admin — eia.gov/opendata/register.php

# ── Optional Data Sources ─────────────────────────────────────────────────────
ACLED_EMAIL=            # Armed conflict data — acleddata.com/register
ACLED_PASSWORD=
AISSTREAM_API_KEY=      # Maritime vessel tracking — aisstream.io (free)
ADSB_API_KEY=           # Unfiltered flight tracking — RapidAPI (~$10/mo)

# ── LLM Provider (pick one) ───────────────────────────────────────────────────
LLM_PROVIDER=           # anthropic | openai | gemini | codex
LLM_API_KEY=            # not needed for codex (uses ~/.codex/auth.json)

# ── Telegram Bot ─────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN=     # from @BotFather
TELEGRAM_CHAT_ID=       # from @userinfobot
TELEGRAM_CHANNELS=      # optional: extra channel IDs beyond 17 built-in
TELEGRAM_POLL_INTERVAL= # ms between command polls, default 5000

# ── Discord Bot ───────────────────────────────────────────────────────────────
DISCORD_BOT_TOKEN=      # Discord Developer Portal → Bot → Token
DISCORD_CHANNEL_ID=     # right-click channel → Copy Channel ID
DISCORD_GUILD_ID=       # optional: instant slash command registration
DISCORD_WEBHOOK_URL=    # optional: alert-only mode, no discord.js needed

# ── Trading (optional) ────────────────────────────────────────────────────────
ALPACA_API_KEY=
ALPACA_SECRET_KEY=
```

---

## Key Commands

| Command | Description |
|---|---|
| `npm run dev` | Start dashboard with auto-reload |
| `node server.mjs` | Start directly (bypasses npm script runner) |
| `node diag.mjs` | Diagnose setup issues |
| `docker compose up -d` | Run in background with Docker |
| `npx @openai/codex login` | Authenticate Codex LLM via ChatGPT subscription |

---

## Telegram Bot Commands

Once `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set, the bot responds to:

| Command | What It Does |
|---|---|
| `/status` | System health, last sweep time, source/LLM status |
| `/sweep` | Trigger a manual intelligence sweep immediately |
| `/brief` | Compact text summary: direction, key metrics, top OSINT |
| `/portfolio` | Portfolio status (requires Alpaca keys) |
| `/alerts` | Recent alert history with tier labels |
| `/mute` / `/mute 2h` | Silence alerts for 1h or custom duration |
| `/unmute` | Resume alerts |
| `/help` | List all commands |

---

## Discord Bot Commands

Install `discord.js` for full bot mode; otherwise Crucix auto-falls back to webhook-only:

```bash
npm install discord.js   # optional: enables slash commands + rich embeds
```

Slash commands available: `/status`, `/sweep`, `/brief`, `/portfolio`

Alert embeds are color-coded: 🔴 red = FLASH, 🟡 yellow = PRIORITY, 🔵 blue = ROUTINE.

**Webhook-only mode** (no `discord.js`, no slash commands):
```dotenv
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

---

## LLM Provider Setup

### Anthropic Claude
```dotenv
LLM_PROVIDER=anthropic
LLM_API_KEY=$ANTHROPIC_API_KEY
```

### OpenAI
```dotenv
LLM_PROVIDER=openai
LLM_API_KEY=$OPENAI_API_KEY
```

### Google Gemini
```dotenv
LLM_PROVIDER=gemini
LLM_API_KEY=$GEMINI_API_KEY
```

### OpenAI Codex (ChatGPT subscription — no API key needed)
```bash
npx @openai/codex login   # authenticate once
```
```dotenv
LLM_PROVIDER=codex
# LLM_API_KEY not required
```

LLM failures are non-fatal — Crucix automatically falls back to rule-based alert evaluation without crashing the sweep cycle.

---

## Architecture & Data Flow

Each 15-minute sweep cycle:
1. **Parallel fetch** — all 27 sources queried simultaneously (~30–60s)
2. **Synthesis** — raw data normalized into dashboard format
3. **Delta computation** — what changed, escalated, or de-escalated vs. previous run
4. **LLM analysis** — 5–8 trade ideas generated (or rule-based fallback)
5. **Alert evaluation** — FLASH / PRIORITY / ROUTINE tiering with semantic dedup
6. **Push** — SSE update to all connected browsers + Telegram/Discord if configured
7. **Persistence** — sweep written to `./runs/` directory

---

## Dashboard Features

- **3D WebGL globe** (Globe.gl) with atmosphere, star field, rotation + flat map toggle
- **9 marker types**: fires, aircraft, radiation, maritime chokepoints, SDR receivers, OSINT events, health alerts, geolocated news, conflict events
- **Animated 3D flight arcs** between air traffic hotspots
- **Region filters**: World, Americas, Europe, Middle East, Asia Pacific, Africa
- **Live markets**: indexes, crypto, energy, commodities (Yahoo Finance, no key needed)
- **Risk gauges**: VIX, high-yield spread, supply chain pressure index
- **OSINT feed**: 17 built-in Telegram intelligence channels
- **Sweep Delta panel**: live diff of what changed this cycle
- **Nuclear watch**: Safecast + EPA RadNet radiation readings
- **Space watch**: CelesTrak satellite tracking — ISS, Starlink, military constellations

---

## Common Patterns

### Minimal Setup (no API keys)
```bash
# Works out of the box — sources without keys still populate:
# Yahoo Finance markets, CelesTrak satellites, GDELT news, RSS feeds,
# OpenSky flight tracking (public tier), Safecast radiation
npm run dev
```

### Maximum Free Coverage
```dotenv
# Register all three free keys (~3 minutes total):
FRED_API_KEY=       # fred.stlouisfed.org — 60 sec signup
FIRMS_MAP_KEY=      # firms.modaps.eosdis.nasa.gov — 60 sec signup
EIA_API_KEY=        # eia.gov/opendata/register.php — 60 sec signup
```

### Telegram Alerts Only (no LLM)
```dotenv
TELEGRAM_BOT_TOKEN=your_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id_from_userinfobot
# LLM_PROVIDER intentionally omitted — rule-based alerts still fire
```

### Full Stack with LLM + Both Bots
```dotenv
FRED_API_KEY=...
FIRMS_MAP_KEY=...
EIA_API_KEY=...
LLM_PROVIDER=anthropic
LLM_API_KEY=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
DISCORD_BOT_TOKEN=...
DISCORD_CHANNEL_ID=...
DISCORD_GUILD_ID=...   # for instant slash command registration
```

### Adding Extra Telegram OSINT Channels
```dotenv
# Comma-separated channel IDs beyond the 17 built-in channels
TELEGRAM_CHANNELS=-1001234567890,-1009876543210
```

---

## Troubleshooting

**Dashboard empty after startup:**
Normal — the first sweep takes 30–60 seconds to query all 27 sources. Wait for it to complete before expecting data.

**`npm run dev` exits silently (especially Windows PowerShell):**
```bash
node --trace-warnings server.mjs
# or run the diagnostic tool:
node diag.mjs
```

**Port already in use:**
```bash
# Default port is 3117 — check if something else is using it:
lsof -i :3117        # macOS/Linux
netstat -ano | findstr :3117   # Windows
```

**Telegram bot not receiving commands:**
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are both set
- Confirm the chat ID is your personal chat, not a group (use @userinfobot)
- Default poll interval is 5000ms — set `TELEGRAM_POLL_INTERVAL=2000` for faster response

**Discord slash commands not appearing:**
- Set `DISCORD_GUILD_ID` for instant registration (vs. up to 1 hour for global)
- Ensure the bot invite URL includes both `bot` and `applications.commands` scopes
- Check **Message Content Intent** is enabled in the Developer Portal

**LLM errors crashing sweeps:**
They won't — LLM failures are caught and the sweep continues with rule-based fallback. Check logs for the specific provider error (invalid key, rate limit, etc.).

**ACLED conflict data missing:**
ACLED uses OAuth2 with email/password — both `ACLED_EMAIL` and `ACLED_PASSWORD` must be set together.

**Sweep data persistence:**
All runs are saved to `./runs/`. In Docker, this is volume-mounted so data survives container restarts.
