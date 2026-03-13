---
name: you-skills
description: Helps users install, run, and integrate YouSkills (visual manager for local AI skills). Use when the user asks about you-skills, local skills visualization, viewing installed skills, npx you-skills, port 12434, or integrating with Codex/Cursor/OpenClaw skills.
---

# YouSkills

This skill provides guidance on **YouSkills** — a local-only visual manager for AI skills (Codex, Cursor, OpenClaw, custom paths). Use it when the user wants to install, run, troubleshoot, or integrate with YouSkills.

## What YouSkills Does

- **Local-only**: Scans standard skill roots and user paths; strictly read-only, no cloud.
- **Web UI**: Card/list views, filters, themes, i18n (zh/en).
- **Agent-friendly**: HTTP API for skills list and manifest.

## When to Use This Skill

- User asks how to install or run you-skills.
- User mentions "local skills", "visualize skills", "view my skills", "you-skills".
- User has issues with `npx you-skills` (e.g. 404, registry, or "opened a file" instead of browser).
- User wants to integrate an agent with local skills (API usage).

---

## Install & Run

**Requires Node.js 18+.**

### One-off (no global install)

```bash
npx you-skills --registry=https://registry.npmjs.org/
```

### Global install

```bash
npm install -g you-skills --registry=https://registry.npmjs.org/
you-skills
```

**Note**: If the user's default npm registry is a mirror (e.g. npmmirror), installs may 404. Always use `--registry=https://registry.npmjs.org/` for you-skills.

---

## Port & Environment

- **URL**: `http://localhost:12434`
- **Port**: `12434`
- **Env (optional)**: `CODEX_HOME`, `CURSOR_HOME` for default scan paths.

---

## Agent / Integration API

- `GET /api/skills?root=` — List skills (default roots or custom `root`).
- `GET /api/skills/manifest` or `GET /api/manifest` — Structured manifest for agents.
- `GET /api/config` — Current config (classification_scheme_id, theme_id).
- `PATCH /api/config` — Update config.
- `PATCH /api/skills/category` — Update one skill’s category (writes to `~/.you-skills/category-cache.json` only).
- `GET /api/browse?path=` — List directories (for picking root).

---

## Common Issues

1. **404 when installing**  
   User may be using a mirror. Use `--registry=https://registry.npmjs.org/` for both `npm install` and `npx`.

2. **“Only opened a file” after run**  
   Ensure they run the command in a terminal (e.g. `you-skills` or `npx you-skills`), not by double-clicking `cli.js`. The CLI starts the server and opens the browser.

3. **First-time / “real user” test**  
   Clear app data: remove `~/.you-skills` (config + category cache). Use browser incognito or clear localStorage for `localhost:12434` to see consent and initial config again.

---

## Links

- **npm**: https://www.npmjs.com/package/you-skills
- **GitHub**: https://github.com/goodpostidea-tech/you_skills
