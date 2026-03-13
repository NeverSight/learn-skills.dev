---
name: lg-desktop
description: "Docker virtual desktop with GUI automation. Use when asked to interact with desktop applications, automate GUI workflows, test UI, or operate software that requires a display. OCR-powered text inspection instead of screenshots (97% fewer tokens). Subcommands: up, down, status, update, inspect, click, type, key, screenshot, find-and-click, wait-for, assert, run, copy-from, copy-to."
---

# lg-desktop

Docker virtual desktop with OCR-powered GUI automation. 97% fewer tokens than screenshot-based approaches.

## When to Use

Use this skill when the user asks to:
- Open, interact with, or automate a desktop application (e.g., "open Firefox", "click the Settings button")
- Test a GUI application or verify visual state
- Automate a workflow that requires a graphical environment
- Run software that needs a display (Java apps, IDEs, browsers)
- Take screenshots or inspect what's on a virtual desktop

## Multi-Agent Note

The desktop is a **shared singleton resource** -- one container per host. Multiple agents (parent + subagents) can safely share it:
- **DO**: Run `up` before use (it's idempotent -- skips if already running)
- **DO**: Use inspect/click/type/key/screenshot freely from any agent
- **DO NOT**: Run `down` from a subagent -- only the orchestrating agent should stop the desktop
- **DO NOT**: Run multiple `up --build` concurrently -- one agent starts, others wait and use

## Arguments: "$ARGUMENTS"

Parse the first word as the subcommand (action). The rest are arguments to that action.

Example: `lg-desktop click E5` -> action=`click`, args=`E5`

---

## Setup (MUST RUN FIRST)

Before ANY action, resolve the skill directory where Docker files are bundled.

**IMPORTANT**: Shell variables do NOT persist between separate command executions. You MUST combine the LG_DIR resolution with subsequent commands in a single shell invocation, or re-resolve LG_DIR each time.

```bash
LG_DIR=""
for d in .agents/skills/lg-desktop .claude/skills/lg-desktop; do
    if [ -f "$d/docker/docker-compose.yml" ]; then
        LG_DIR=$(cd "$d" && pwd)
        break
    fi
    if [ -L "$d" ]; then
        REAL=$(realpath "$d" 2>/dev/null)
        if [ -f "$REAL/docker/docker-compose.yml" ]; then
            LG_DIR="$REAL"
            break
        fi
    fi
done
echo "LG_DIR=$LG_DIR"
```

If `LG_DIR` is empty, the skill is not installed. Tell the user to run `npx skills add gyumaruya/lg-desktop`.

Use `$LG_DIR` for all Docker Compose commands below. Always combine with LG_DIR resolution in the same shell call.

---

## Subcommands

### up

Start the virtual desktop. Run this first before any interaction. **Idempotent**: safe to call even if already running.

**Note**: First-time build takes ~5 minutes (Rust compilation + Ubuntu packages). Subsequent starts are fast.

1. Check if already running (skip build if so):
```bash
STATUS=$(docker inspect --format '{{.State.Status}}' lg-desktop 2>/dev/null)
if [ "$STATUS" = "running" ]; then
    echo "Desktop already running: http://localhost:3000"
    exit 0
fi
```
If already running, **stop here** -- no need to rebuild. Report "Desktop already running" and proceed with your task.

2. Check Docker:
```bash
docker info > /dev/null 2>&1 && echo "Docker: OK" || echo "Docker: NOT FOUND"
```
If Docker is not found, tell the user to install Docker and stop.

3. Remove stale container if exists (handles "created" or "exited" state):
```bash
docker rm -f lg-desktop 2>/dev/null
```

4. Build and start (combine with LG_DIR resolution):
```bash
LG_DIR=""
for d in .agents/skills/lg-desktop .claude/skills/lg-desktop; do
    if [ -f "$d/docker/docker-compose.yml" ]; then LG_DIR=$(cd "$d" && pwd); break; fi
    if [ -L "$d" ]; then REAL=$(realpath "$d" 2>/dev/null); [ -f "$REAL/docker/docker-compose.yml" ] && LG_DIR="$REAL" && break; fi
done
docker compose -f "$LG_DIR/docker/docker-compose.yml" up -d --build 2>&1
```

5. Verify:
```bash
sleep 3 && docker inspect --format '{{.State.Status}}' lg-desktop 2>/dev/null || echo "not running"
```

If status is "created" but not "running", wait a few more seconds and check again -- the container may still be starting.

Report: "Desktop started: http://localhost:3000"

**Port conflict**: If port 3000 is already in use, stop the conflicting container first (`docker ps` to find it).

### down

**Caution**: Only run this when you are done with the desktop. If other agents or subagents are using it, stopping the container will interrupt their work.

```bash
docker compose -f "$LG_DIR/docker/docker-compose.yml" down 2>&1
```

### status

```bash
docker inspect --format '{{.State.Status}}' lg-desktop 2>/dev/null || echo "not running"
```

### update

Update skill and rebuild:
```bash
npx skills add gyumaruya/lg-desktop --yes 2>&1
docker compose -f "$LG_DIR/docker/docker-compose.yml" up -d --build 2>&1
```

---

## Container Check (before interaction commands)

Before running inspect/click/type/key/screenshot/run, verify the container is running:
```bash
docker inspect --format '{{.State.Status}}' lg-desktop 2>/dev/null || echo "not running"
```

If not running, run the **up** subcommand first to auto-bootstrap, then continue.

---

### inspect [--changes-only]

OCR-based desktop state inspection. Returns structured JSON.

```bash
docker exec -e DISPLAY=:1 lg-desktop lg-inspect 2>/dev/null
```

With --changes-only (only changed windows, fewer tokens):
```bash
docker exec -e DISPLAY=:1 lg-desktop lg-inspect --changes-only 2>/dev/null
```

**Output format:**
- `windows[]` - Array of windows with `id`, `title`, `geometry`, `ocr_text`, `elements[]`, `changed`
- `elements[]` - Clickable text with absolute coordinates `{text, x, y, w, h, confidence}`
- To click an element: center = (x + w/2, y + h/2)

**OCR limitation**: Terminal/console windows (xterm, etc.) may return empty `ocr_text` due to font rendering. If OCR returns empty text for a window you expect to have content, escalate to `screenshot --crop` to verify visually.

### click <target>

Target can be:
- Grid reference (A1-J10): Letter (A-J) = column, Number (1-10) = row
- Pixel coords (500,300): Direct x,y

**Grid conversion:**
```bash
docker exec -e DISPLAY=:1 lg-desktop xdotool getdisplaygeometry
```
Returns WIDTH HEIGHT. Then:
- col_idx = letter - 'A', row_idx = number - 1
- x = col_idx * (WIDTH/10) + (WIDTH/20)
- y = row_idx * (HEIGHT/10) + (HEIGHT/20)

**Execute:**
```bash
docker exec -e DISPLAY=:1 lg-desktop xdotool mousemove --sync <x> <y> click 1
```

**Verify** with quick wmctrl check:
```bash
docker exec -e DISPLAY=:1 lg-desktop wmctrl -l 2>/dev/null
```

### type <text>

```bash
docker exec -e DISPLAY=:1 lg-desktop xdotool type --clearmodifiers "<text>"
```

### key <keys>

```bash
docker exec -e DISPLAY=:1 lg-desktop xdotool key --clearmodifiers "<keys>"
```

Examples: `key Return`, `key ctrl+s`, `key alt+F4`, `key Tab`

### screenshot [--grid] [--crop x,y,w,h]

**Basic:**
```bash
docker exec -e DISPLAY=:1 lg-desktop scrot -z -o /tmp/lg-screenshot.png && \
docker cp lg-desktop:/tmp/lg-screenshot.png /tmp/lg-desktop-screenshot.png
```

**With grid overlay:**
```bash
docker exec -e DISPLAY=:1 lg-desktop scrot -z -o /tmp/lg-screenshot.png && \
docker exec -e DISPLAY=:1 lg-desktop lg-grid /tmp/lg-screenshot.png /tmp/lg-screenshot-grid.png && \
docker cp lg-desktop:/tmp/lg-screenshot-grid.png /tmp/lg-desktop-screenshot.png
```

**With crop (x,y,w,h):**
```bash
docker exec -e DISPLAY=:1 lg-desktop scrot -z -o /tmp/lg-screenshot.png && \
docker exec -e DISPLAY=:1 lg-desktop convert /tmp/lg-screenshot.png -crop <w>x<h>+<x>+<y> +repage /tmp/lg-screenshot.png && \
docker cp lg-desktop:/tmp/lg-screenshot.png /tmp/lg-desktop-screenshot.png
```

Then use Read tool on `/tmp/lg-desktop-screenshot.png`

### find-and-click <text>

1. Run inspect:
   ```bash
   docker exec -e DISPLAY=:1 lg-desktop lg-inspect 2>/dev/null
   ```
2. Search `elements[]` for matching text (case-insensitive)
3. Calculate center: cx = x + w/2, cy = y + h/2
4. Click:
   ```bash
   docker exec -e DISPLAY=:1 lg-desktop xdotool mousemove --sync <cx> <cy> click 1
   ```

### wait-for [--window/--text/--gone <value>] [--timeout N]

Poll every 500ms until condition met or timeout (default: 30s).

- `--window <title>`: `wmctrl -l | grep -i "<title>"`
- `--text <text>`: `lg-inspect | jq -r '.windows[].ocr_text' | grep -i "<text>"`
- `--gone <text>`: same as --text but wait until grep fails

### assert [--window/--no-window/--text <value>]

Check condition, report pass/fail as JSON.

### run <command...>

Execute any command inside the container.

```bash
docker exec -e DISPLAY=:1 lg-desktop <command...>
```

Examples:
- `run xterm` -- Open a terminal: `docker exec -d -e DISPLAY=:1 lg-desktop xterm`
- `run firefox` -- Open Firefox: `docker exec -d -e DISPLAY=:1 lg-desktop firefox`
- `run ls /tmp` -- List files: `docker exec -e DISPLAY=:1 lg-desktop ls /tmp`

**Note**: Use `-d` (detach) flag for GUI applications that run in the foreground, so the command returns immediately.

### copy-from <container-path> <host-path>

```bash
docker cp lg-desktop:<container-path> <host-path>
```

### copy-to <host-path> <container-path>

```bash
docker cp <host-path> lg-desktop:<container-path>
```

---

## Token Efficiency (IMPORTANT)

Always follow this 3-tier escalation. Start cheap, escalate only when needed:

| Tier | Method | Tokens | When |
|------|--------|--------|------|
| 1 | `inspect` (text/JSON) | 50-200 | DEFAULT -- always try first |
| 2 | `screenshot --crop` | ~200 | OCR is ambiguous or missing elements |
| 3 | `screenshot` (full) | 765+ | Last resort only |

**Typical workflow:** `inspect` -> act -> `inspect --changes-only` -> act -> repeat

## Quick Reference

| Key | Value |
|-----|-------|
| Container | `lg-desktop` |
| Display | `DISPLAY=:1` |
| Shared dir | `/tmp/lg-desktop-share` (host) = `/shared` (container) |
| Desktop URL | http://localhost:3000 |
| Resolution | 1280x1024 |
| Window manager | i3 (tiling) |
| Post-action delay | 200ms (GUI settle time) |
| Java SWT apps | use `--window $WID` flag with xdotool |
