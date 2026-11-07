---
name: figcraft-live
description: >
  Designs, inspects, renders, and exports in FigCraft (github.com/storytold/figcraft)
  and .figcraft files via the lazy figcraft-live MCP server (mounts globally, opens
  one shared app window on ensure) or headless figcraft-cli. Use for FigCraft work.
license: MIT
compatibility: >
  Live editing requires the FigCraft desktop app and the figcraft-live-mcp server
  (bash and jq; launching requires macOS open, or FIGCRAFT_APP pointing to the
  binary or AppImage on Linux). Headless file work (inspect, render, export, run)
  runs anywhere figcraft-cli is installed.
metadata:
  author: fang2hou
  version: "4.2"
---

# FigCraft Live

Drive live design in the FigCraft desktop app through the lazy `figcraft-live` MCP server (`scripts/figcraft-live-mcp`), or run headless file operations through `figcraft-cli`. The MCP server mounts in every session without starting anything; the app opens only when a task calls `ensure`, sharing at most one window per repository across worktrees and agents.

## When to Use

- Designing, editing, inspecting, or rendering `.figcraft` documents live in the FigCraft desktop app
- Converting, rendering, exporting (`.png`, `.svg`, `.pdf`, `.fig`), or running atomic command scripts on `.figcraft`, `.fig`, `.svg`, or Figma REST `.json` files via `figcraft-cli`
- Setting up or debugging the `figcraft-live` MCP server or the FigCraft loopback control channel

## When NOT to Use

- Implementing web, HTML, or React UI code directly without FigCraft (use `frontend-design` or `shadcn`)
- Building HTML reports or review dashboards (use `agent-report`)

## The Demand Gate (Hard Rules)

- **Global silent mount**: Register `figcraft-live` at user scope. It answers `initialize` and `tools/list` from static data without opening a window or touching a socket, so multiple agents can mount it simultaneously.
- **Only `ensure` may start the app**: `ensure` first checks for a running controllable FigCraft instance and adopts the user's window if found; it launches a new instance only when none responds. Always announce to the user before calling `ensure` when a launch is needed.
- **All other tools never launch**: `status`, `commands`, `inspect`, `render`, `exec`, `batch`, and `stop` reuse the running instance or fail with a message pointing to `ensure`.
- **No gate bypass or silent fallback**: Never launch the app manually via shell or a second MCP registration, because that bypasses the repository port lock and opens duplicate windows. If `ensure` fails, stop and report the error rather than silently switching to headless CLI editing.

## Setup

One-time install (per machine, not per project):

1. **MCP server**: Run `install -m 755 <skill-dir>/scripts/figcraft-live-mcp ~/.local/bin/` (requires `bash` and `jq`). Register it at user scope with a `>= 60000` ms timeout (`ensure` waits up to 30s for cold launch):
   - omp: add to `~/.omp/agent/mcp.json`
   - Claude Code: `claude mcp add --scope user figcraft-live ~/.local/bin/figcraft-live-mcp`
   - Full config snippets: [references/mcp.md](references/mcp.md)
2. **Headless CLI**: Install `figcraft-cli` from the GitHub release and verify its SHA-256 checksum: [references/setup.md](references/setup.md).

**Per-task readiness check** (report in your first progress note): confirm that the session lists the `figcraft-live` tools and that `figcraft-cli --version` succeeds. Neither check starts the app.

## Inputs & Environment

| Input / Variable      | Required | Default / Format                              | Purpose                                                       |
| --------------------- | -------- | --------------------------------------------- | ------------------------------------------------------------- |
| Document `path`       | No       | Repo-relative or absolute `.figcraft` path    | Passed to `ensure {path}` and `file.save`                     |
| Document `name`       | No       | String (for example `"Mobile App"`)           | Passed to `ensure {name}` when creating a new unsaved tab     |
| `FIGCRAFT_APP`        | No       | `/Applications/FigCraft.app` or binary path   | Overrides app bundle (macOS) or binary/AppImage path (Linux)  |
| `FIGCRAFT_PORT`       | No       | Auto (`7979` or repo-derived `7979..7979+60`) | Pins the loopback control port; busy non-FigCraft port errors |
| `FIGCRAFT_PROJECT`    | No       | Server working directory (`.` / `--project`)  | Pins the repository root used for worktree port sharing       |
| `FIGCRAFT_START_WAIT` | No       | `30` (seconds)                                | Max wait for the control port to open on launch               |

## MCP Tools

Every tool accepts a JSON object and returns one JSON text block containing the control channel reply (`ok` / `error`). Clients prefix tool names with the server name (for example `mcp__figcraft_live_status` in omp).

| Tool                                   | Starts App             | Purpose                                                                                                                                                                   |
| -------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `status {}`                            | Never                  | Reports `{running, port, origin, windows}` (`origin` is `started` or `adopted`).                                                                                          |
| `ensure {path?, name?, raise?}`        | **Yes — the only one** | Adopts or launches the shared instance. `path` opens the file or reuses its tab (reporting `already`/`new` and `stale`); `name` creates a new tab; `raise: true` focuses. |
| `exec {command, params?}`              | Never                  | Executes one registry command (`file.save`, `node.set`, `select.set`, `edit.undo`, `image.place`, `inspect.code`).                                                        |
| `batch {label?, commands[]}`           | Never                  | Runs an array of commands as a single undo step (`command.batch`). Name steps with `as` and reference them later with `{"$ref": "<name>"}`. Build one section per batch.  |
| `inspect {id?, depth?}`                | Never                  | Reads the model: calls `node.get` when `id` is an integer, or `document.inspect` otherwise (returns solved sizes, `absoluteBounds`, and undo history).                    |
| `render {ids, scale?, path?, window?}` | Never                  | Renders PNG via `ui.render` and returns the image inline. **Pass `ids` explicitly**: omitting `ids` renders the current selection, not the page. `window: true` captures. |
| `commands {filter?}`                   | Never                  | Lists the 400+ in-app commands filtered by a case-insensitive regex on `id` or `label`. Offline equivalent: `figcraft-cli commands --filter <text>`.                      |
| `stop {force?}`                        | Never                  | Calls `app.quit` on an instance this server started (`origin: started`). Discards unsaved changes; adopted instances require `force: true` after saving.                  |

### Standard Live Session

1. **Check state**: Call `status` to see whether an instance is running and which documents are open.
2. **Open or adopt (`ensure`)**: Call `ensure {path: "design/app.figcraft"}` (or `ensure {name: "..."}` for a new document), announcing the launch first if no instance is running. If `ensure` fails, stop and report the error rather than editing whatever tab happens to be active.
3. **Discover commands**: Call `commands {filter: "layout"}` (or run `figcraft-cli commands --filter layout`) whenever you are unsure of a command ID or its parameters.
4. **Build section by section**: Send one design section per `batch` call using `as` and `{"$ref": "<name>"}` bindings, and record the returned node IDs.
5. **Verify model then pixels**:
   - Call `inspect` to check solved `width`, `height`, and `absoluteBounds` (any unexpected `100×100` frame means `sizingH`/`sizingV` is missing).
   - Call `render {ids: [<frame_id>]}` to confirm nothing is clipped and fills and text appear where expected.
6. **Save**: Call `exec {command: "file.save", params: {path: "design/app.figcraft"}}` after each verified section. The saved `.figcraft` file on disk is the source of truth.
7. **Wind down**: Leave the app open while design work continues. When the task finishes, save first and call `stop` only if this server started the instance (`origin: started`).

Section batch example (using `as` and `$ref` instead of counting IDs):

```json
{
  "label": "nav",
  "commands": [
    {
      "command": "frame.create",
      "as": "page",
      "params": {
        "width": 390,
        "height": 844,
        "name": "Home",
        "props": { "fill": "#FFFFFF", "layout": "vertical", "padding": 0 }
      }
    },
    {
      "command": "frame.create",
      "as": "nav",
      "params": {
        "parent": { "$ref": "page" },
        "name": "nav",
        "props": {
          "layout": "horizontal",
          "sizingH": "fill",
          "sizingV": "hug",
          "padding": [16, 20, 16, 20],
          "mainAlign": "spaceBetween",
          "crossAlign": "center"
        }
      }
    },
    {
      "command": "node.create",
      "params": {
        "type": "text",
        "parent": { "$ref": "nav" },
        "text": "App",
        "name": "nav-title",
        "props": { "fontSize": 17, "fill": "#111827" }
      }
    }
  ]
}
```

## Editing Rules

1. **Discover before calling**: Guessed command IDs and parameter names fail; check `commands` (or `figcraft-cli commands` offline) first.
2. **One section per `batch`**: Each `batch` is one undo step. A failing step rolls back the entire batch and identifies the failing command.
3. **Stay in your target tab**: Open your target document with `ensure` and run `file.save` after each section. Never edit a tab you did not open; check `status` if active tab state is unclear.
4. **Respect the shared canvas**: Because the user may be working in the same window, `inspect` a layer before modifying it, and never send raw input commands (`ui.pointer`, `ui.key`, `ui.type`) unless asked. Highlight completed work with `select.set` followed by `view.zoomSelection`.
5. **Inspect before retrying**: A timed-out or failed call may still have mutated the document; run `inspect` before sending a retry.
6. **Local or base64 images only**: `image.place` accepts a local `path` or base64 `data`, never a URL. Download remote images to disk first: [references/images.md](references/images.md).
7. **Explicit auto-layout sizing and contrast**: Declare `sizingH` and `sizingV` on every auto-layout frame, and keep body text contrast at `>= 4.5:1` (WCAG AA): [references/design.md](references/design.md).
8. **Verify every section**: A command returning `ok: true` only proves the engine accepted the call; run the Step 5 model and pixel checks before moving on.

## Worktrees and Multiple Agents

- **One window per repository**: The server keys instances by `git rev-parse --git-common-dir`, so every worktree of a repository resolves to the same control port. When multiple agents run across worktrees, the first `ensure` call launches the app under a directory lock and the others adopt that instance.
- **Stale-tab and overwrite guards**: Keep one canonical `.figcraft` path per design in the repository. `ensure {path}` reuses an already-open tab for that path and sets `stale: true` if the disk file changed since the tab loaded it. `file.save` refuses to overwrite a file modified on disk by another session; reload the tab before passing `overwrite: true`.
- **No concurrent writers on one file**: The shared instance serializes incoming commands on the UI thread, but it does not merge conflicting edits to the same document.
- **Protect user-owned windows**: Only call `stop` on instances with `origin: started`; `origin: adopted` windows belong to the user and lose unsaved work on `app.quit`.

## Headless File Route (`figcraft-cli`)

Use `figcraft-cli` when no live window is needed (file inspection, asset export, CI pipelines, Linux servers without a display, or when the demand gate must remain closed):

| Task                                    | Command                                                               |
| --------------------------------------- | --------------------------------------------------------------------- |
| Inspect or convert a file               | `figcraft-cli info <file> [--json]`, `convert <in> <out>`             |
| Render a page or export frame assets    | `render <file> -o out.png`, `export <file> -o dir/ --scale 2`         |
| Run atomic scripted edits (1 undo unit) | `figcraft-cli run script.jsonl --in base.figcraft --out out.figcraft` |
| Search the 400+ command registry        | `figcraft-cli commands --filter <text> [--json]`                      |

`figcraft-cli run` accepts the same `{command, params, as?}` objects as MCP `batch`. Full CLI reference: [references/cli.md](references/cli.md).

## Failure Handling

| Symptom                                             | Recovery Action                                                                                                                        |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Tool returns `"not running; call the ensure tool"`  | Expected before the first `ensure`; announce the launch and call `ensure`.                                                             |
| `ensure` fails with an app or port launch error     | Stop and report the error; switch to headless `figcraft-cli` only with the user's explicit approval.                                   |
| `ensure` returns `stale: true`                      | The file changed on disk since the tab opened: reload via `exec {command: "file.open", params: {path, reload: true}}` or ask the user. |
| `no open document`                                  | The active tab was closed; call `ensure` again with `path` or `name`.                                                                  |
| Frame solves to `100×100` or children disappear     | The parent auto-layout frame is missing `sizingH`/`sizingV` (and clips children by default); set `sizingH`/`sizingV` on the parent.    |
| Render is tiny, empty, or shows one widget          | `render` without `ids` exports only the current selection; pass the target frame IDs in `ids: [<id>]`.                                 |
| `unsupported image: format could not be determined` | The path is missing or not a supported raster format; convert the file to PNG, JPG, or WebP first.                                     |
| `automation path rejected`                          | Target path lies outside the app's `--automation-read-root` or `--automation-write-root` flags; move the file inside the allowed root. |
| `control request queue is full`                     | The 8-slot socket/UI queue is saturated; wait briefly and send smaller `batch` payloads.                                               |
| `stop` refuses an adopted instance                  | Expected safeguard against losing unsaved user work; save all open documents first, then call `stop {force: true}` only if asked.      |

## Gotchas

- **Auto-layout frames default to `100×100` and clip**: An auto-layout frame never sizes itself automatically. Without `sizingH`/`sizingV` (or explicit `width`/`height`), it stays `100×100` with `clip: true` and truncates overflowing children.
- **Frames default to a white fill**: Set `"fill": "none"` on structural wrapper frames (rows, icon containers, tab items) so they do not paint opaque white boxes over tinted backgrounds.
- **Vector icons stretch if both dimensions are set**: Pass only `height` (or only `width`) on `vector` nodes so the SVG path preserves its aspect ratio.
- **Uncontrolled app windows cannot be adopted**: If the user opened FigCraft without `--control <port>`, `ensure` cannot attach to it and will launch a second controllable instance. Leave the user's window alone and never kill it.
- **Never hard-code node IDs**: Creation commands return `{"id": N}`; capture returned IDs or bind them with `as` and `{"$ref": "<name>"}`. Coordinates use page units (`y` downward), `x`/`y` are relative to the parent frame, and colors use `#RRGGBB` or `#RRGGBBAA`.
- **Font reproducibility**: Live sessions index system fonts; pass `--no-system-fonts` (or `FIGCRAFT_NO_SYSTEM_FONTS=1`) on `figcraft-cli` for deterministic CI renders.

## Output Contract

When finishing a FigCraft task, report:

1. **Interface used**: Live MCP (`origin: started` or `adopted`, plus `port`) or headless `figcraft-cli` (and why live mode was not used).
2. **Documents modified**: File paths and key created/updated node IDs and names.
3. **Images and exports**: Every placed image (`source`, target node, `mode`) and exported asset (`path`, format, `scale`).
4. **Verification results**: Model check (`inspect` solved bounds), pixel check (`render` findings), and any `note:` or tool warnings.

## References

| Topic                                                     | Reference                                      |
| --------------------------------------------------------- | ---------------------------------------------- |
| MCP server architecture, client registration, env, debug  | [references/mcp.md](references/mcp.md)         |
| Loopback JSON control protocol (`127.0.0.1`), limits, RPC | [references/control.md](references/control.md) |
| Placing, masking, adjusting, and verifying images         | [references/images.md](references/images.md)   |
| Auto-layout construction patterns, tokens, and QA loop    | [references/design.md](references/design.md)   |
| `figcraft-cli` probe, checksum install, and macOS quirks  | [references/setup.md](references/setup.md)     |
| `figcraft-cli` subcommands, flags, exit codes, gotchas    | [references/cli.md](references/cli.md)         |
