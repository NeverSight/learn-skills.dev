---
name: den
description: Control and drive Den Browser via the first-party den CLI. Use when browsing websites, inspecting page content, clicking or filling forms, capturing screenshots, managing Web and Terminal Boards, staging material in the Drawer, or observing and interacting with terminal processes.
---

# Den Browser (`den`)

Den Browser is a macOS companion browser organizing web and terminal work into Desks and horizontal Board layouts.
Its bundled CLI (`den`) allows agents in Terminal Boards to drive adjacent web content, manage workspace layout, and observe terminal sessions.

## 1. Domain Model

- Desk: Broad work context holding Boards in a horizontal work area. Multiple Desks can exist; one is active.
- Board: Work surface within a Desk.
  - Web Board: Displays a web browsing Sheet.
  - Terminal Board: Runs a native Ghostty terminal surface with shell/TUI processes.
- Sheet: Web screen held within a Web Board.
- Drawer: Den-wide staging area for web material whose Desk context is not yet settled.

## 2. Ambient Spatial Targeting (Zero-Config)

When running inside a Terminal Board in Den Browser:
- Environment variables `DEN_BOARD_ID` and `DEN_SOCKET` are set automatically.
- `den sheet ...` commands automatically target the nearest adjacent Web Board on the current Desk. Specify `--board <id>` only to target another board.
- `den terminal text` and `den terminal send` default to the calling Terminal Board when executed within one.
- `den board new <url>` opens a Web Board adjacent to you without stealing terminal focus.

## 3. Web Interaction Philosophy (Snapshot + Ref)

Follow this canonical interaction loop:
1. Open: `den board new <url>` (returns `board_id`).
2. Wait: `den sheet wait 1` (let DOM settle; can also wait for selectors: `den sheet wait "#submit"`).
3. Observe: `den sheet snapshot -i` (get compact `@e1`, `@e2` refs for interactive elements; avoids dumping raw HTML).
4. Act: `den sheet click @e1`, `den sheet fill @e2 "text"`, `den sheet press Enter`, `den sheet scroll down`.
5. Inspect: `den sheet url`, `den sheet text`, `den sheet eval "..."`, `den sheet screenshot [path]`.
6. Clean up: `den board close` when finished.

References belong to the latest snapshot. After navigation or DOM changes, wait if needed and take a new snapshot before reusing refs.

## 4. Drawer Workflow (Staging Material)

Use the Drawer to collect URLs during research without cluttering the active Desk:
- Keep: `den drawer keep <url> [--title <text>]` (stores item in Drawer).
- List: `den drawer list` (returns items with id, title, url).
- Place: `den drawer place <id>` (promotes item onto the active Desk as a Web Board).
- Discard: `den drawer discard <id>` (removes item from Drawer).

## 5. Terminal Board Observation & Control

Agents can spawn, observe, and interact with background jobs, dev servers, or TUIs:
- Spawn: `den terminal new [<path>] [--run "<cmd>"] [--focus]` (opens a Terminal Board; `--run` executes inside an interactive shell so session stays alive).
- List: `den terminal list` (returns `id`, `label`, `working_directory`, `foreground_pid`).
- Observe screen: `den terminal text [--board <id>]` (reads clean visible viewport text buffer; ideal for checking build output, logs, or TUI state).
- Send input: `den terminal send "<text>\n" [--board <id>]` (injects characters or escape sequences into terminal pty).

### Safety & Policy Boundary

- Never bypass harness constraints: Do not use `den terminal new --run` or `den terminal send` to execute commands that are denied, restricted, or blocked by your agent harness, sandbox, or security policies. Den must never serve as an escape hatch to evade environment restrictions.
- Intended use only: Terminal Boards are strictly for human-visible, long-running processes (e.g. dev servers, watcher tasks) and interactive TUIs, not for arbitrary unconstrained command proxying.

## 6. Command Discovery & Scripting

- Run `den --help` or `den <domain> --help` (`den sheet --help`, `den terminal --help`, `den drawer --help`) for all commands and options.
- When piped (e.g. `| jq`) or with `--json`, commands emit single-line JSON with `ok: true/false`:
  - Entities: `.board_id`, `.drawer_item_id`, `.url`, `.text`, `.value`
  - Collections: `.boards[]`, `.terminals[]`, `.drawer_items[]`, `.desks[]`
