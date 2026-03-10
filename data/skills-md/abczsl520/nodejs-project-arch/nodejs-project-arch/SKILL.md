---
name: nodejs-project-arch
description: Node.js project architecture standards for AI-assisted development. Enforces file splitting (<400 lines), config externalization, route modularization, and admin dashboards. Use when creating new Node.js projects, refactoring large single-file codebases, or when AI context window is being consumed by oversized files. Covers H5 games (Canvas/Phaser/Matter.js), data tools (crawlers/scrapers), content platforms, monitoring dashboards, API services, and SDK libraries.
---

# Node.js Project Architecture for AI-Friendly Development

Architecture standards that keep files small enough for AI agents to read/edit without blowing the context window.

## Core Rules

- Single file max **400 lines**, `index.html` max **200 lines**, `server.js` entry max **100 lines**
- All tunable values in `config.json`, loaded at runtime, editable via admin dashboard
- Backend: `routes/` by domain, `services/` for shared logic, `db.js` for database
- Frontend: HTML skeleton only, JS/CSS in separate files
- Every project gets `admin.html` + `routes/admin.js` for config hot-reload

## Project Type Selection

Determine project type, then read the corresponding reference:

| Type | Signals | Reference |
|------|---------|-----------|
| **H5 Game** | Canvas, Phaser, Matter.js, game loop, sprites | [references/game.md](references/game.md) |
| **Data Tool** | Crawler, scraper, scheduler, data sync, analytics | [references/tool.md](references/tool.md) |
| **Content/Utility** | Generator, library, publisher, file processing | [references/tool.md](references/tool.md) |
| **Dashboard/Monitor** | Charts, real-time, alerts, metrics | [references/tool.md](references/tool.md) |
| **API Service** | REST endpoints, middleware, microservice | [references/tool.md](references/tool.md) |
| **SDK/Library** | Shared module, build step, multi-consumer | [references/sdk.md](references/sdk.md) |

## Quick Start (All Types)

1. Identify project type from table above
2. Read the corresponding reference file
3. Create directory structure per the reference
4. Extract hardcoded values → `config.json`
5. Split large files by function (each <400 lines)
6. Add `routes/admin.js` + `admin.html`
7. Frontend: `config.js` fetches `/api/config` at startup, code reads `GAME_CONFIG.xxx` or `APP_CONFIG.xxx`
8. Test locally → backup → deploy

## config.json Pattern (Universal)

```javascript
// Server: load and serve config
const config = JSON.parse(fs.readFileSync('./config.json', 'utf8'));
app.get('/api/config', (req, res) => {
  const safe = { ...config };
  delete safe.admin; // strip secrets
  res.json(safe);
});

// Admin: hot-reload
app.post('/admin/config', requireAdmin, (req, res) => {
  fs.writeFileSync('./config.json.bak', fs.readFileSync('./config.json'));
  fs.writeFileSync('./config.json', JSON.stringify(req.body, null, 2));
  Object.assign(config, req.body);
  res.json({ ok: true });
});
```

## Admin Dashboard Pattern (Universal)

`admin.html` auto-generates form from config structure:
- Password login (`x-admin-password` header)
- Visual config editor with save + hot-reload
- Stats overview (users/data/uptime)
- Config backup history + restore

## Why This Matters

Large single files consume massive context tokens when AI reads them:
- 3000-line file → ~40K tokens per read (20% of 200K window)
- 200-line module → ~2.7K tokens per read (1.3% of window)
- **Result: 10-15 productive rounds vs 3-5 before context compression**
