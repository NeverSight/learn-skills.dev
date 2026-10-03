---
name: pr-tour
description: >
  Live onboarding tour of newly implemented code. Combines /deep-trace, the
  vscode-debug-mcp bridge, and playwright-cli to run the target app in a debug
  session, drive the UI, pause at curated breakpoints inside the new code, and
  narrate "this modal is the newly created one" — mapping every UI moment to
  the exact file:line. Use when the user wants to understand where and how
  AI-written feature code executes in the running application ("どの UI /
  どのロジックで動くのか分からない", "オンボーディングして", "/pr-tour").
argument-hint: "[pr-number|branch|commit-range|file-path] [--auto]"
---

# PR Tour — Live Code-to-UI Onboarding

## Codex Compatibility

When running this skill in Codex, translate Claude Code-only primitives before acting: `AskUserQuestion` -> chat/request_user_input, `TodoWrite` -> `update_plan`. Resolve `Read`/`Write`/`Bash` to Codex file/shell tools. The vscode-debug-mcp bridge is reached over plain HTTP (`curl 127.0.0.1:7779`), so no MCP configuration is required.

## Cursor Compatibility

When running this skill in Cursor Agent, translate: `AskUserQuestion` -> `AskQuestion`, `TodoWrite` -> Cursor `TodoWrite`. Use the Shell tool for playwright-cli and curl. If a project rule forbids playwright-cli by default, a user invocation of `/pr-tour` counts as explicit consent to use it (the skill is built on it), but re-confirm if unsure.

<essential_principles>

## What a tour is

A tour turns "the diff the agent wrote" into a guided, runtime-verified walkthrough:

1. The target app runs in dev mode; an external Chrome is driven by playwright-cli.
2. VS Code / Cursor's debugger (js-debug) attaches to the same Chrome via the vscode-debug-mcp bridge.
3. The agent sets one curated breakpoint at a time inside the NEW code, triggers it by operating the real UI, and while the IDE sits paused on the exact line, narrates in chat what the user is looking at — on screen and in code.
4. Every stop is recorded into a Markdown tour artifact that can be replayed later with the deep-trace-extension (Load Trace from Clipboard → Set Trace Breakpoints → Next Step).

## Non-negotiable ground rules

- **One breakpoint active at a time.** Set → trigger → hit → narrate → remove → next. Never carpet-bomb all trace lines (React re-renders would stop the world).
- **Client-side code only (MVP).** Pages Router components, hooks, handlers. Server-side (API routes/SSR/RSC) is out of scope until the bridge supports multiple debug sessions.
- **Screenshots are taken BEFORE the trigger and AFTER continue — never while paused.** A paused renderer freezes rAF; both playwright screenshot and raw CDP `Page.captureScreenshot` hang (verified 2026-07-15).
- **The trigger command must be fired in the background.** A click that lands on a pausing line freezes the page mid-actionability-check, so the CLI call itself times out — that is EXPECTED and harmless; the input was already dispatched. Detect the hit by polling the bridge, not by waiting for the click to return.
- **Narrate in the conversation language** (e.g. Japanese if the session is in Japanese). Write the artifact in the same language.
- Interactive pacing is the default: at each stop ask "次へ / 深掘り / 終了". `--auto` walks all stops without asking (short pause per stop, artifact still produced).

</essential_principles>

## Prerequisites (verify before starting, fail fast with fix instructions)

| Check | Command | Fix when it fails |
|---|---|---|
| Bridge extension alive | `curl -s http://127.0.0.1:7779/health` → `{"status":"ok"}` | Install **Debug MCP Bridge** (`laststance.vscode-debug-mcp-bridge`, [VS Code Marketplace / Open VSX](https://github.com/laststance/vscode-debug-mcp)) in the IDE **window that has the target project open**, or run command "Debug MCP Bridge: Start Server" there. The bridge binds 7779 per IDE window — the owning window is where paused files will open. |
| playwright-cli | `playwright-cli --version` | `npm install -g @playwright/cli@latest` |
| Chrome binary | `ls "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` | Any Chromium with `--remote-debugging-port` works; adjust path |
| Target app boots | project dev command | Run `kill-port <port>` first per user rules |

Start the bridge BEFORE launching the debug session — the bridge's DAP tracker only sees sessions created after it is running (known limitation #1 in vscode-debug-mcp TODO.md).

## Bridge API (HTTP on 127.0.0.1:7779)

Use the `vscode-debugger` MCP server when configured; otherwise call HTTP directly — same capabilities, zero setup:

| Purpose | HTTP |
|---|---|
| Set breakpoint | `POST /breakpoint {"file":"<abs path>","line":N}` (opt: `condition`, `hitCondition`, `logMessage`) |
| Remove breakpoint | `DELETE /breakpoint {"file":"<abs path>","line":N}` |
| Attach debugger | `POST /debug/launch {"config":{...}}` (inline config, launch.json not needed) |
| Poll for hit | `GET /state` → `{"state":"stopped","threadId":1,...}` |
| Call stack | `GET /debug/callstack` |
| Variables | `POST /debug/variables {}` (top frame scope) |
| Evaluate | `POST /debug/evaluate {"expression":"..."}` |
| Resume | `POST /debug/continue` |
| Step | `POST /debug/stepInto` / `stepOver` / `stepOut` |
| Detach | `POST /debug/stop` |

## Workflow

### Step 1: Identify the target diff

Same input contract as /deep-trace: no arg = branch diff (`git diff <base>...HEAD` + uncommitted), or PR number (`gh pr diff N`), commit range, file path. Collect changed files and line ranges. Prioritize: components > hooks > utils.

### Step 2: Trace and curate tour stops

Run the /deep-trace methodology (Serena `find_symbol` / `find_referencing_symbols` to map entry points; do NOT re-read this paragraph as a replacement for that skill — reuse it). Then curate **3–10 tour stops** from the trace:

- The mount/first-render line of each NEW component ("this modal is the new one")
- The primary user-facing handlers (onClick / onSubmit / onChange)
- The data mutation/query dispatch point
- Skip: type-only lines, imports, styles, lines that fire on unrelated screens
- JSX attribute lines (`onClick={handler}`) pause during the RE-RENDER after the
  click (state already updated), not inside the handler — still a valid stop, but
  narrate it as "the render caused by the click". For pausing inside the handler
  itself, put the stop on a line INSIDE the callback body instead.

For each stop write down: file:line (absolute path), the screen URL where it fires, the UI action that triggers it, and a one-sentence narration draft. Order stops as a story: open screen → see new UI → interact → data flows → result renders.

`'use client'` sanity check: a stop must be code that executes in the browser. In Pages Router everything qualifies; in App Router skip Server Component lines (they will never hit a chrome-attach breakpoint).

### Step 3: Boot the environment

```bash
# 0. Guard the IDE against stray keystrokes while paused (restore at teardown).
#    With both settings false the paused file STILL opens and reveals the line —
#    it just never steals window/keyboard focus, so IME/keyboard input cannot
#    land in the source file (verified incident 2026-07-15: stray "い" broke HMR).
#    Merge into <project>/.vscode/settings.json, remembering prior values:
#      "debug.focusEditorOnBreak": false,
#      "debug.focusWindowOnBreak": false
# Also snapshot the working tree state to detect stray edits later:
git -C <project root> status --porcelain > /tmp/pr-tour-git-baseline.txt

# 1. Dev server (background)
kill-port <port>; <dev command>   # wait for "Ready"

# 2. External Chrome with CDP + anti-throttle flags (background).
#    Throttle flags are mandatory: an occluded window stalls rAF and playwright
#    actionability checks hang even without any breakpoint.
#    Launch from a DEDICATED persistent background shell (exec Chrome as that
#    shell's only process). `(cmd &)` or `nohup ... & disown` from a throwaway
#    agent shell dies together with the shell session (verified twice 2026-07-15).
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/pr-tour-chrome-profile \
  --no-first-run --no-default-browser-check \
  --disable-backgrounding-occluded-windows \
  --disable-renderer-backgrounding \
  --disable-background-timer-throttling \
  about:blank

# 3. playwright-cli attaches. ALWAYS 127.0.0.1 — "localhost" may resolve to ::1
#    and Chrome only listens on IPv4 (verified failure mode).
#    <browser origin> = the app's canonical BROWSER-visible origin. Behind a
#    local reverse proxy (nginx/https dev setups) it differs from the dev port
#    (e.g. https://local.zume-n.com proxying localhost:8080) and direct-port
#    access can even break auth callbacks — check the project's own rules.
playwright-cli -s=tour attach --cdp=http://127.0.0.1:9222
playwright-cli -s=tour goto <browser origin>/

# 4. js-debug attaches to the SAME Chrome via the bridge (inline config).
#    urlFilter must match <browser origin> from step 3 — NOT the dev server
#    port when the two differ — or breakpoints will never bind.
curl -s -X POST http://127.0.0.1:7779/debug/launch -H "Content-Type: application/json" -d '{
  "config": {
    "type": "chrome", "request": "attach", "name": "pr-tour attach",
    "port": 9222, "webRoot": "<abs project root>",
    "urlFilter": "<browser origin>/*", "timeout": 15000
  }
}'
# GET /state must answer {"state":"running",...} before proceeding
```

If login is required, do it with playwright-cli now (respect the project's own login rules/accounts).

### Step 4: Tour loop (per stop)

```bash
# a. Navigate to the stop's screen via regular UI clicks; screenshot the "before" state
playwright-cli -s=tour screenshot --filename=tours/<feature>/stopN_before.png

# b. Arm exactly this stop's breakpoint.
#    Mount/first-render stops: the navigation/click that mounts the component
#    IS the trigger — park one screen BEFORE it in step a and arm now, or the
#    line will have already run by the time the breakpoint exists.
curl -s -X POST http://127.0.0.1:7779/breakpoint -d '{"file":"<abs file>","line":N}'

# c. Fire the trigger IN THE BACKGROUND (the CLI call will time out when the BP
#    hits mid-click — expected; the event was already dispatched)
(playwright-cli -s=tour click <ref> &)

# d. Poll for the hit (0.5–1s interval, ~10s budget)
curl -s http://127.0.0.1:7779/state          # until "stopped"

# e. Harvest narration material
curl -s http://127.0.0.1:7779/debug/callstack
curl -s -X POST http://127.0.0.1:7779/debug/variables -d '{}'
curl -s -X POST http://127.0.0.1:7779/debug/evaluate -d '{"expression":"<interesting var>"}'
```

f. **Narrate in chat while paused.** The IDE window that owns the bridge is now showing the exact line. Explain like a senior onboarding a teammate, e.g.:

> 🧭 **Stop 2/5 — 新規モーダルの表示ロジック**
> いまブラウザは「タスクを追加」ボタンを押した直後で止まっています。エディタに出ている `HomePage.useCallback[handleOpenModal]` (`src/pages/index.tsx:23`) が今回の新機能の入口で、この `setIsModalOpen(true)` が実行されると次のレンダーで `QuickAddTaskModal` (今回新規作成したコンポーネント) がマウントされます。コールスタックの上 2 段は React のイベントディスパッチなので読み飛ばして OK です。

g. Pacing: default = ask the user (`次へ` / `深掘り (step into・変数展開・evaluate)` / `終了`). With `--auto`, continue immediately after narrating.

```bash
# h. Resume, disarm, capture the "after" state
curl -s -X POST http://127.0.0.1:7779/debug/continue
curl -s -X DELETE http://127.0.0.1:7779/breakpoint -d '{"file":"<abs file>","line":N}'
playwright-cli -s=tour screenshot --filename=tours/<feature>/stopN_after.png

# i. Stray-edit guard: compare against the baseline from Step 3.
#    Any unexpected new modification = accidental edit while paused → show the
#    diff to the user and revert it (git checkout -- <file>) before continuing.
git -C <project root> status --porcelain | diff /tmp/pr-tour-git-baseline.txt - || true
```

If a breakpoint does not hit within the budget: remove it, note "this stop did not fire with this interaction" honestly in the artifact, and move on. Never fake a hit.

### Step 5: Write the tour artifact

Save to `<project root>/tours/<feature-name>/README.md` (override location only if the user asks — e.g. zumen-fe conventions may prefer task asset dirs). Contents:

1. Title, date, diff source (branch/PR), one-paragraph feature summary
2. Per stop: narration text + before/after screenshots (relative links) + file:line + trigger
3. **deep-trace-extension replay table** in a fenced block (workspace-relative paths):

```markdown
| file | line | col | reason |
| --- | --- | --- | --- |
| src/pages/index.tsx | 23 | 1 | handleOpenModal — 「タスクを追加」click |
| src/hooks/useCreateTask.ts | 19 | 1 | createTask fake POST — 「作成する」click |
```

Copy the table to the clipboard (`pbcopy` on macOS) and tell the user: paste-replay via Deep Trace panel → Load Trace from Clipboard → Set Trace Breakpoints → Next Step.

### Step 6: Teardown

```bash
curl -s -X POST http://127.0.0.1:7779/debug/stop
playwright-cli -s=tour detach   # leaves Chrome open; kill it if the skill launched it
# stop the dev server only if this skill started it
# restore the debug.focus*OnBreak settings changed in Step 3 to their prior values
```

Report: stops toured / skipped, artifact path, replay instructions.

## Known pitfalls (all runtime-verified 2026-07-15)

| Symptom | Cause | Fix |
|---|---|---|
| `ECONNREFUSED ::1:9222` on attach | `localhost` resolved to IPv6 | Use `http://127.0.0.1:9222` |
| click/eval hang with NO breakpoint set | Chrome throttles occluded windows → rAF stalls → actionability never settles | Launch Chrome with the three anti-throttle flags (Step 3) |
| click times out but state=stopped | Page paused mid-click — by design | Background the trigger, poll `/state` |
| Screenshot hangs | Renderer paused | Only screenshot before trigger / after continue |
| `/health` connection refused | Bridge not running in any window, or another window owns 7779 | Install/start the bridge in the target project's window; stop it elsewhere |
| `/health` OK but paused files open in the WRONG IDE window | Another window owns :7779 — the extension auto-starts in whichever window activates first | Identify the owner: `ps -p $(lsof -t -iTCP:7779 -sTCP:LISTEN) -o command=` (the workspace name appears in the process title). Run "Debug MCP Bridge: Stop Server" there, then "Start Server" in the target project's window |
| Breakpoint never hits | Server-side/RSC line, wrong absolute path, or `urlFilter` mismatch (behind a reverse proxy the browser origin ≠ `localhost:<port>`) | Verify the line runs in the browser; use absolute file paths; filter on the browser-visible origin; check webRoot |
| Stale state after IDE-driven steps | Bridge misses events for sessions it didn't see start | Start bridge before `/debug/launch`; re-sync by calling `/state` after step commands |
| Mount stop hits with `isOpen: false`, then again with `true` | Component is permanently mounted (modal toggled via `isOpen` prop), so the "mount" line runs on every parent re-render | Expected — evaluate the prop at each hit and continue past the pre-open hit; narrate the always-mounted structure as a finding |
| `/debug/evaluate` fails `X is not defined` for an imported util | evaluate resolves only closure-captured variables in the paused frame; module imports are compiled to webpack bindings | Evaluate captured locals/props only, or inline the util's logic into the expression |
| `playwright-cli upload` shows help / does nothing for multiple files | `upload` answers a pending filechooser and takes exactly ONE file argument; a second arg makes commander print help and drop the chooser | Multi-file: `drop <dropzone-ref> --path a --path b` (repeatable). Single-file: `click` the chooser button, then `upload <file>` immediately |
| App breaks mid-tour with a ReferenceError on a garbled identifier | While paused the file is open AND focused in the IDE — a stray keystroke (e.g. IME character) plus autosave edits the source and HMR reloads it | Prevented by Step 3's `debug.focusEditorOnBreak: false` + `debug.focusWindowOnBreak: false` (file still reveals, never takes focus). The per-stop git guard (Step 4-i) catches anything that slips through — no extension change needed |
| Element refs (`e6` etc.) stop matching after a stop | HMR reload / navigation invalidates snapshot refs | Re-run `snapshot` after every reload or HMR event before interacting |

## Phase 2 backlog (do not attempt in MVP)

Server-side stops (needs multi-session support in vscode-debug-mcp), App Router RSC boundary detection, tanstack-start support, `wait_for_stopped` long-poll bridge endpoint, logpoint output capture, OS-level `screencapture` of the paused IDE+browser moment, hard read-only guard in the bridge extension (on DAP `stopped` mark the revealed file readonly-in-session via `workbench.action.files.setActiveEditorReadonlyInSession`, release on continue — optional; the Step 3 focus settings already cover the practical risk).
