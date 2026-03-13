---
name: browser-preview
version: 1.0.0
description: "Browser preview panel knowledge — the iframe-based Browser tab in the right panel. Use when the user mentions browser, preview, tab disappeared, page broken, blank screen, white screen, 白屏, 页面挂了, tab 不见了, preview not loading, or asks about running services."

metadata:
  starchild:
    emoji: "🌐"
    skillKey: browser-preview

user-invocable: true
disable-model-invocation: false
---

# Browser Preview

You already know `preview_serve` and `preview_stop`. This skill fills the gap: what happens **after** preview_serve returns a URL — how the user actually sees it.

## What is Browser

The frontend has a right-side panel with two tabs: **Workspace** and **Browser**. Browser renders preview URLs inside an iframe. When you call `preview_serve`, the frontend automatically opens a Browser tab loading that URL.

Key facts:
- Each `preview_serve` call creates one Browser tab
- URL format: `https://<host>/preview/{id}/`
- Browser panel has a **⋮ menu** (top-right) showing "RUNNING SERVICES" list
- Browser tab can be **closed by the user** without stopping the backend service
- Backend service stopping → Browser tab shows an error page

## ⚠️ CRITICAL: Never Tell Users to Access localhost

**The user's browser CANNOT access `localhost` or `127.0.0.1`.** These addresses point to the server container, not the user's machine. The preview architecture uses a **reverse proxy**:

```
User's Browser → https://<host>/preview/{id}/path → (reverse proxy) → 127.0.0.1:{port}/path
```

Rules:
- **NEVER** tell the user to visit `http://localhost:{port}` or `http://127.0.0.1:{port}` — they cannot reach it
- **ALWAYS** direct users to the preview URL: `/preview/{id}/` (or the full URL `https://<host>/preview/{id}/`)
- `curl http://localhost:{port}` is for **your own server-side diagnostics only** — never suggest it to the user as a way to "test" the preview
- When a preview is running, tell the user: "Check the Browser panel, or refresh the Browser panel"
- If you need to give the user a URL, use the `url` field returned by `preview_serve` (format: `/preview/{id}/`)

## ⚠️ Static Assets Must Use Relative Paths

Because previews are served under `/preview/{id}/`, **absolute paths in HTML/JS/CSS will break**. The reverse proxy strips the `/preview/{id}` prefix before forwarding to the backend, but the browser resolves absolute paths from the domain root.

Example of the problem:
```html
<!-- ❌ BROKEN: browser requests https://host/static/app.js → 404 (bypasses preview proxy) -->
<script src="/static/app.js"></script>

<!-- ✅ WORKS: browser requests https://host/preview/{id}/static/app.js → proxied correctly -->
<script src="static/app.js"></script>
<script src="./static/app.js"></script>
```

Common patterns to fix:
| Broken (absolute) | Fixed (relative) |
|---|---|
| `"/static/app.js"` | `"static/app.js"` or `"./static/app.js"` |
| `"/api/users"` | `"api/users"` or `"./api/users"` |
| `"/images/logo.png"` | `"images/logo.png"` or `"./images/logo.png"` |
| `url('/fonts/x.woff')` | `url('./fonts/x.woff')` |
| `fetch('/data.json')` | `fetch('data.json')` |

**Check ALL places** where paths appear:
1. HTML `src`, `href` attributes
2. JavaScript `fetch()`, `XMLHttpRequest`, dynamic imports
3. CSS `url()` references
4. JavaScript string literals (e.g., `'/static/'` in template strings or concatenation)
5. Framework config files (e.g., `publicPath`, `base`, `assetPrefix`)

⚠️ Be thorough — it's common to fix CSS `url()` but miss JS string literals like `'/static/'` (with single quotes). Search for ALL occurrences of absolute paths across all file types.

## ⚠️ Do NOT Browse Filesystem to Debug Previews

**Never** look at workspace directories like `preview/`, `output/`, or random folders to understand preview state. Those are user data, not preview service state.

The **only** sources of truth:
1. Registry file: `/data/previews.json` (running services)
2. History file: `/data/preview_history.json` (all past services)
3. `preview_serve` / `preview_stop` tools
4. Port checks via `curl` (server-side only, for your diagnostics)

Do NOT use `ls`/`find` on workspace directories to diagnose preview issues. Do NOT call unrelated tools like `list_scheduled_tasks`. Stay focused.

## Step-by-Step: Diagnosing Browser Issues

When a user reports any Browser problem, follow this exact sequence:

### Step 1: Read the registry (running services)

```bash
cat /data/previews.json 2>/dev/null || echo "NO_REGISTRY"
```

⚠️ Your bash CWD is `/data/workspace/`. The registry is at `/data/previews.json` (absolute path, one level up). Always use the absolute path.

JSON structure:
```json
{
  "previews": [
    {"id": "f343befc", "title": "My App", "dir": "/data/workspace/my-project", "command": "npm run dev", "port": 9080, "is_builtin": false}
  ]
}
```

### Step 2: Branch based on registry state

**If registry has entries** → Go to Step 3 (verify services)
**If registry is empty or missing** → Go to Step 4 (check history)

### Step 3: Registry has entries — verify and fix

For each preview in the registry, check if the port is responding **server-side** (this is your diagnostic, not for the user):
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:{port}
```

**If port responds (200):**
- The service IS running. Tell the user:
  - "You have a running service: {title}"
  - "Click the ⋮ menu at the top-right of the Browser panel, then click it in the RUNNING SERVICES list to reopen"
  - Preview URL: `/preview/{id}/`
- **If user says the ⋮ menu is empty or doesn't show the service** → frontend lost sync. Fix by recreating: `preview_stop(id)` then `preview_serve(dir, title, command)` using the info from the registry. This forces the frontend to re-register the tab.

**If port does NOT respond:**
- Process crashed but registry entry remains. Recreate:
  ```
  preview_stop(id="{id}")
  preview_serve(dir="{dir}", title="{title}", command="{command}")
  ```

### Step 4: No running services — check history first, then scan workspace

When there are no running services, use a **two-tier lookup** to find projects the user can preview:

#### Tier 1: Read preview history (preferred — fast and accurate)

```bash
cat /data/preview_history.json 2>/dev/null || echo "NO_HISTORY"
```

JSON structure:
```json
{
  "history": [
    {
      "id": "f343befc",
      "title": "Trading System",
      "dir": "/data/workspace/my-project",
      "command": "python main.py",
      "port": 8000,
      "is_builtin": false,
      "created_at": 1709100000.0,
      "last_started_at": 1709200000.0
    }
  ]
}
```

History entries are **never removed by `preview_stop`** — they persist across restarts. Entries are automatically pruned only when the project directory no longer exists.

**If history has entries:**
- List all history entries to the user with title, directory, and last started time
- Ask which one they want to restart
- Call `preview_serve` with the `dir`, `title`, and `command` from the history entry

**If user says a project is missing from history** → fall through to Tier 2.

#### Tier 2: Scan workspace (fallback — when history is empty or incomplete)

```bash
find /data/workspace -maxdepth 2 \( -name "package.json" -o -name "index.html" -o -name "*.html" -o -name "app.py" -o -name "main.py" -o -name "vite.config.*" \) -not -path "*/node_modules/*" -not -path "*/skills/*" -not -path "*/memory/*" -not -path "*/prompt/*" -not -path "*/.git/*" 2>/dev/null
```

Then:
1. List discovered projects with brief descriptions
2. Ask the user which one to preview
3. Call `preview_serve` with the appropriate directory

**Don't just say "no services running" and stop.** Always check history first, then scan, and offer options.

## Quick Reference

| User says | You do |
|-----------|--------|
| "tab disappeared" / "tab 不见了" | Step 1 → 2 → 3 or 4 |
| "blank page" / "白屏" | Check port (server-side), if dead → recreate; if alive → check for absolute path issues |
| "not updating" / "内容没更新" | Suggest refresh button in Browser tab, or recreate preview |
| "port conflict" / "端口冲突" | `preview_stop` old → `preview_serve` new |
| "can't see service" / "⋮ menu empty" | `preview_stop` + `preview_serve` to force re-register |
| "where's my project" / "what did I build" | Read `/data/preview_history.json` and list entries |
| "resource load failed" / "JS/CSS 404" | Check for absolute paths (`/static/`, `/api/`), fix to relative paths |

## What You Cannot Do

- Cannot directly open/close/refresh Browser tabs (frontend UI)
- Cannot force-refresh the iframe
- Cannot read what the iframe displays

When you can't do something, tell the user the manual action (e.g., "click refresh in Browser tab"). If manual action doesn't work, recreate the preview with `preview_stop` + `preview_serve`.

## Common Mistakes to Avoid

1. ❌ Telling user to "visit http://localhost:18791/" — user cannot access localhost
2. ❌ Saying "refresh the page at localhost" — meaningless to the user
3. ❌ Only fixing CSS `url()` paths but missing JS string literals with absolute paths
4. ❌ Forgetting to check ALL file types (HTML, JS, CSS, config) for absolute paths
5. ✅ Always use `/preview/{id}/` as the user-facing URL
6. ✅ Always use `curl localhost:{port}` only for your own server-side diagnostics
7. ✅ After fixing paths, call `preview_stop` + `preview_serve` to restart, then tell user to check Browser panel
