---
name: browser
description: >-
  Controls a live Chrome browser through a persistent puppeteer-core MCP
  connection — click, type, hover, drag, fill forms; navigate pages; take
  screenshots and export PDFs; read the DOM and accessibility tree; run
  Lighthouse audits and Core Web Vitals traces; intercept, record, stub, or
  block network requests; export HAR traffic; emulate devices and network
  conditions; manage browser storage; upload and download files. Use when
  interacting with or automating a running browser, clicking elements, taking
  screenshots, running Lighthouse, capturing network traffic as HAR, checking the
  accessibility tree, intercepting or stubbing requests, or emulating a device or
  viewport. Not for: web search or fetching public URLs without a browser session
  (use web-research), reading a static HTML file already on disk, fixing
  TypeScript or JavaScript build or compile errors, debugging source code
  without a running page, or tasks that don't require controlling a live browser.
when_to_use: >-
  take a screenshot of the page, click a button on the page, fill out the form
  in the browser, navigate to a URL in the browser, run a Lighthouse audit,
  Lighthouse performance audit, capture network requests as a HAR file, record
  network traffic HAR, check or inspect the accessibility tree, intercept network
  requests, stub an API response in the browser, mock network calls, emulate an
  iPhone or Android device, browser automation, automate the browser, end-to-end
  testing in Chrome. Not for build failures, compiler errors, or code edits.
---

# browser

Persistent Chrome/CDP control via puppeteer-core. The primary interaction model
is snapshot → stable ref → action. Selectors and coordinates are fallbacks only.
Output size decides where a read lands: at or above the server's inline
threshold (`PAYLOAD_THRESHOLD_BYTES` in `mcp-browser/src/lib/payload.ts`) the
payload is written to a temp file and the tool returns the path; below it the
payload comes back inline with `written: false` and no path. Handle both cases —
see `references/interaction.md` in this skill directory for the per-tool result
fields. Screenshots, PDFs, traces, HAR, Lighthouse reports, and saved storage
state are always files, however small.

## Prerequisites

Call `browser_connect` before any other tool. Mode `launch` spawns (or reuses)
a Chrome process; mode `attach` connects to a running Chrome via `browser_url`
or `ws_endpoint`.

## Primary loop: snapshot → ref → act

```
browser_snapshot          → returns compact AX tree; every interactive node carries a stable ref id
browser_click(ref=...)    → act on the ref (also: browser_type, browser_hover, browser_select, browser_fill_form, browser_press_key, browser_drag)
browser_snapshot          → verify the new state
```

Refs last until the next `browser_snapshot`, which invalidates every earlier ref.
Re-snapshot after navigation or DOM changes. `stale_ref` means the ref predates
the current snapshot or its element left the DOM; `interaction_failed` means the
element resolved but the action itself failed (hidden, no layout box, re-rendered
mid-action). Both recover the same way: take a new snapshot and retry.
Selector/coordinate targeting is the fallback when a ref is unavailable; a
selector must resolve to exactly one element (refinements and `ambiguous_match`
in `references/interaction.md` in this skill directory).

## Screenshot, DOM, and AX — route to a subagent when available

Screenshots, DOM trees, and accessibility trees usually run far past the inline
threshold, and a full-page capture can be very large. Loading them directly
bloats the main context. Use the host's subagent tool when available: dispatch
a small reviewer that reads the file path and returns a text summary, so the
artifact never enters this conversation. If the host has no subagent surface,
summarize inline only when the artifact is small enough; otherwise use local
deterministic tools or ask how to proceed.

One read may not cover a large artifact. Shrink it at capture time first —
`selector` on `browser_screenshot` and `browser_dom`, `max_depth`/`max_nodes` on
`browser_snapshot` — and check `bytes` (and a screenshot's `width`/`height`,
which drive image read cost) before dispatching. For a file that is still large,
tell the reviewer to search it or read it in chunks rather than assume a single
read saw the whole thing.

Claude Code dispatch shape (other hosts: see Compatibility below):

```
Dispatch Agent:
  model: haiku
  description: "browser: analyze [screenshot|dom|accessibility]"
  prompt: |
    The browser tool wrote an artifact to: <PATH>
    Read that file with the Read tool. If it is too large for one read,
    search it or read it in chunks until the question is answered.
    Return a concise text summary: what the page shows, key elements,
    errors or state, and the specific answer to: <USER_QUESTION>
    Return text only — no raw HTML, JSON, or image data.
```

Tools that produce large artifacts: `browser_screenshot`, `browser_dom`,
`browser_accessibility`, `browser_export_har`, `browser_performance_stop_trace`,
`browser_pdf`. Pass the returned path to a subagent for reading when available.

## Navigation and waiting

`browser_navigate` accepts http/https by default. `allow_internal=true` also
permits `file:` and `about:` URLs (a local HTML file, `about:blank`);
`javascript:` and every other scheme stay blocked (`blocked_url`) regardless.
After navigation, use `browser_wait`
(strategy `navigation` or `selector`) to confirm the page settled before
interacting. For text-triggered flows use `browser_wait_for_text`.

## Tool surface by group

Full parameter details in the references below. Load the relevant one when
planning work in that group.

| Group | Reference |
|---|---|
| Snapshot + refs interaction · Navigation · Read + extract | `references/interaction.md` in this skill directory |
| Performance · Lighthouse · HAR · Network routing · Throttling | `references/perf-network.md` in this skill directory |
| Storage · Device emulation · Geolocation · Capture (PDF / screencast / upload / download) | `references/storage-capture.md` in this skill directory |

## Payload discipline

| Artifact | Where it lives | In main context? |
|---|---|---|
| Screenshot PNG | file path from `browser_screenshot` | Prefer subagent; inline only if small enough |
| DOM HTML | file path from `browser_dom` | Prefer subagent; inline only if small enough |
| AX tree JSON | file path from `browser_accessibility` | Prefer subagent; inline only if small enough |
| HAR file | file path from `browser_export_har` | Prefer subagent; inline only if small enough |
| Performance trace | file path from `browser_performance_stop_trace` | No — analyze via `browser_analyze_insight` |
| PDF | file path from `browser_pdf` | Prefer subagent; inline only if small enough |
| Subagent text summary | returned text | Yes |
| Sub-threshold output (`written: false`, no path) | inlined in result | Yes |

## Compatibility

Tool names here are the server's short names (`browser_click`, `browser_snapshot`, …).
Claude Code exposes them under its plugin-prefixed MCP naming; on Codex or another
host, use that host's equivalent name for the same mcp-browser tool. The dispatch
block above is Claude Code's shape, including its `model` value: elsewhere,
substitute the host's subagent call with a small, cheap model, or read the artifact
inline when the host has no subagent surface and the artifact is small enough.
