---
name: reflex-browser
description: Use this skill for browser automation through Reflex Agent using the reflex-browser CLI, including session handling, command flow, selectors, and protocol-safe request patterns.
---

# Reflex Browser Skill (Agent-Only)

## Purpose

Use this skill when you need browser automation through Reflex Agent via stateless CLI commands.

The CLI is single-action per process:

- run one `reflex-browser <command>` invocation
- `--session` is optional; omitted commands use machine+repo auto-session
- read one JSON response from stdout

## Quick Start

1. Install globally from Gitea npm:
   - `npm config set @reflexautomation:registry "https://git.bqa-solutions.nl/api/packages/reflex/npm/" --location=user`
   - `npm config set "//git.bqa-solutions.nl/api/packages/reflex/npm/:_authToken" "YOUR_DEPLOY_TOKEN" --location=user`
   - `npm install -g @reflexautomation/browser-cli`
2. Start or reuse a session:
   - `reflex-browser start`
3. Default to auto-session mode for normal agent runs:
   - do **not** pass `--session` on follow-up commands
   - example: `reflex-browser open https://example.com`
4. Use explicit `--session` only for deterministic override:
   - example: `reflex-browser open https://example.com --session <sessionId>`
5. End with `session-kill` in auto-session mode.
   - if you used an explicit session id, use `session-kill --session <sessionId>` (or `session-kill <sessionId>`)

Agent defaults:

- do not pass `--session` by habit after `start`; normal flows should stay in scoped auto-session mode
- prefer `summary` with `-i`, `-C`, `-c`, `-d`, and `-s` for selector discovery and recovery before trying `eval` or `html`
- use `--help` only as a compact reference; follow this skill and the README examples for workflow shape

## Command Lifecycle (Required)

1. Send actions as separate CLI invocations.
2. Keep one logical session context for the task (auto-session by default).
3. Default rule: omit `--session` on commands unless explicit override is required.
4. Execute sequentially: run one command, inspect response, then run the next.
5. On transport failure, rerun the command as a new invocation.
6. Cleanup with `session-kill` when done unless the user explicitly asks to keep the session open.

## Response Handling (Required)

1. Always capture the full JSON response first, then parse fields from that captured payload.
2. Do not pipe command output directly into filtering (`jq | head`) as the only observable output; this hides critical context.
3. Prefer in-memory capture over temp files; if temp files are needed, use ephemeral files and clean them up.
4. Treat envelope fields (`ok`, `action`, `session`) as source-of-truth; mirrored duplicates may be compacted out of `response`.

## Parser-First Summary Contract (Required)

1. For selector discovery that feeds agent logic, use `summary` first.
2. Parse `response.data.summary.targets[]` as the primary selector feed:
   - `selector`
   - `selectorType`
   - `confidence`
   - `reason`
   - optional steering:
     - `status`
     - `hint`
     - `fallback`
     - `ref` — short-lived element ref (`@r1`, `@r2`, …); prefer over `selector` when present
3. Treat `summary.version` + `summary.targets[]` as the stable parser contract; avoid parsing deep fields from full summary output by default.
4. Do not parse `elements`/`actions`/`candidates`-style fields from summary output.
5. Keep extraction flow deterministic:
   - summary for candidate selection
   - targeted action (`click`/`text`/`attribute`/etc.)
   - re-run summary only after DOM-changing actions when needed

## Summary Refs (Required)

Each `summary` call assigns short-lived refs (`@r1`, `@r2`, …) to interactive elements:

- Refs appear in `targets[].ref` and inline in `snapshot` lines as `[ref=@rN]`.
- Pass a ref directly as the selector to any action: `click "@r10"`, `fill "@r5" "text"`, `attribute "@r3" href`.
- **Prefer refs over CSS/XPath selectors when available** — they resolve directly to the live DOM element, bypassing selector fragility entirely.
- Refs are **invalidated after any navigation or DOM-mutating action** (`click`, `fill`, `type`, `enter`, `tab`, `open`, `back`, `forward`, `refresh`, tab switches). Re-run `summary` after such actions to obtain fresh refs.
- A stale ref returns `errorCode: ELEMENT_STALE` with a `recoveryHint` — always re-run `summary` on that error.

```
# summary returns: - link "Fiction" [ref=@r10]
reflex-browser click "@r10"              # navigate using ref

# after navigation, refs are invalidated — re-run summary
reflex-browser summary 20 -i -c
# - link "Soumission" [ref=@r150]
reflex-browser attribute "@r150" title   # read without re-discovering selector
reflex-browser attribute "@r150" href
```

Helper script:

- `scripts/capture_json.sh` provides `rb_capture`, `rb_jq`, and `rb_pick_selector` for safe full-response handling.
- source via `source skills/reflex-browser/scripts/capture_json.sh` (from project root).

## Lua Output Handling

1. Treat `lua` action output as a raw trace by default.
2. If `response.data.generationGuidance` is present, apply it to produce a human-usable Lua 5.2 script.
3. Keep discovered selectors as-is when guidance says selectors are fixed.
4. Return both:
   - raw generated script (for traceability)
   - enhanced runnable script (for human use)

## Session Selection Rules

1. Default to scoped auto-session mode.
2. Use `start` to get-or-create the scoped auto-session.
3. After `start`, continue commands without `--session` in normal flows.
4. Use explicit `--session <id>` only when:
   - the user asks to pin/reuse a specific session id, or
   - the task requires switching between multiple concurrent sessions.
5. Use bare `--session` (no value) only on `start` or `open` when a fresh backend-assigned session id is explicitly required.
6. Do not pass `--session` by habit in single-flow tasks.
7. Pass `--profile` only when persistent browser state is intentionally needed.

## Hard Rules

1. Bridge is Chrome-only.
2. Do **not** send `options.browser`.
3. Recompute selectors after DOM changes with `summary`.
   - Use `-i` for interactive discovery.
   - Add `-C` for cursor-interactive components.
   - Add `-c` to reduce structural noise.
   - Add `-s <selector>` to scope discovery to a container.
4. Stop on first failed command (`ok: false`) to avoid cascading selector errors.
5. Pass relative links directly to `open`; CLI resolves them against current session URL.
6. For repeated-item extraction, anchor selectors at the collection parent (for example list/grid item), then index that parent; do not index unrelated descendants.
7. Treat repeated `no such element` or timeout on the same intent as a selector-state mismatch, not a transient flake.

## Wait Strategy (Required)

1. `click`, `fill`, `type`, and `open` include waiting behavior; avoid redundant waits.
2. Use explicit `wait` for real state transitions:
   - after navigation
   - after `back` / `forward` / `refresh`
   - after async UI updates
3. Prefer stable page-level wait targets over fragile positional selectors.
4. If an action fails once, retry once. If it fails again, run `summary` again with tighter flags and continue with updated selectors.
5. After 2 consecutive failures for the same intent, stop the loop and run recovery; never keep incrementing positional selectors blindly.
6. For `wait`/`visible`/`enabled`/`selected`, pass per-check timeout as the positional argument (`wait "<selector>" 8000`); reserve global `--cli-timeout` for transport/command envelope timeout.

## Anti-Patterns (Forbidden)

1. Running commands without checking each JSON response.
2. Using `eval` as default extraction when `text`, `summary`, `attribute`, or `property` can answer the task.
3. Running long blind command chains without validating page state.
4. Continuing extraction loops after a failed `open`.
5. Using positional selectors on the wrong structural level (for example `article:nth-of-type(n)` when siblings are actually `li` elements).
6. Repeating the same failing selector pattern across increasing indexes without re-discovery.
7. Jumping to full `html` dumps before trying `summary` for selector recovery.
8. Starting extra sessions during the same task without explicit need and cleanup.
9. Hiding browser flow in long shell scripts/loops instead of observable one-command-at-a-time CLI calls.
10. Passing explicit `--session` by habit in single-flow tasks that should use default auto-session behavior.
11. Using `--help` mid-task as a substitute for the documented selector/session workflow.

## Output Contract (Required)

1. Always evaluate envelope first:
   - `ok`
   - `action`
   - `session`
2. On failure (`ok: false`), parse structured error fields first:
   - `response.errorCode`
   - `response.recoveryHint`
   - then `message`/`response.message` for display text
3. Read actions (`text`, `value`, `attribute`, `property`, `tag`, `title`, `url`) return extracted values in:
   - `response.data.value`
4. Interaction actions (`click`, `fill`, `type`, `enter`, `tab`) return execution metadata in:
   - `response.selector`
   - `response.lua`
   - optional `response.data` fields
5. Summary contract:
   - `response.data.summary.version`
   - `response.data.summary.targets[]`
   - Prefer targets with `status: "ready"`.
   - Treat `status: "retry"` as a one-retry candidate, then refresh `summary`.
   - Treat `status: "avoid"` as a recovery hint, not a first-choice selector.
   - Use `fallback` only when the primary selector fails or the target is marked `avoid`.
   - Use `ref` as the selector when present — it resolves directly to the live element without re-parsing CSS/XPath.
6. Lua generation:
   - `response.data.script` as canonical script payload
   - `response.data.generationGuidance` as post-processing constraints
7. Screenshot contract:
   - `response.data.imageBase64`
   - `response.data.mimeType`

## Repeated Items Pattern (Required)

1. Identify the repeated container first (for example `css=ol.row > li`).
2. Validate the container count/visibility with `wait` or `visible`.
3. Extract child fields within indexed container selectors (for example `... > li:nth-of-type(2) h3 a`).
4. Prefer semantic field reads:
   - `attribute ... title` for titles when present
   - `text ... .price_color` for visible price text

## Bash URL Handling (Optional)

Use this only when writing shell wrappers around CLI JSON output.
For normal CLI usage, prefer `open <href>` directly (relative URLs are auto-resolved).

```bash
get_value() { jq -r '.response.data.value // empty'; }
get_url() { reflex-browser url | get_value; }
open_target() {
  local href="$1"
  reflex-browser open "$href" >/dev/null
  get_url
}
```

## PowerShell URL Handling (Optional)

Use the same pattern in PowerShell when running on Windows.

```powershell
function Get-Value {
  param([Parameter(ValueFromPipeline = $true)] $obj)
  process { $obj.response.data.value }
}

function Get-Url {
  reflex-browser url | ConvertFrom-Json | Get-Value
}

function Open-Target {
  param([string]$Href)
  reflex-browser open $Href | Out-Null
  Get-Url
}
```

## References

- Command catalog and flags:
  - `references/commands.md`
- CLI protocol contract:
  - `references/protocol.md`
- Selector workflow:
  - `references/selectors.md`
- Session lifecycle and recovery:
  - `references/session-management.md`
- Worked example:
  - `examples/books-to-scrape-summary.md`
