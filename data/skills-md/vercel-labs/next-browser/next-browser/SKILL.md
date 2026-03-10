---
name: next-browser
description: >-
  CLI that gives agents what humans get from React DevTools and the Next.js
  dev overlay — component trees, props, hooks, PPR shells, errors, network —
  as shell commands that return structured text.
---

# next-browser

If `next-browser` is not already on PATH, install `@vercel/next-browser`
globally with the user's package manager, then `playwright install chromium`.

If `next-browser` is already installed, it may be outdated. Run
`next-browser --version` and compare against the latest on npm
(`npm view @vercel/next-browser version`). If the installed version is
behind, upgrade it (`npm install -g @vercel/next-browser@latest` or the
equivalent for the user's package manager) before proceeding.

---

## Next.js docs awareness

If the project's Next.js version is **v16.2.0-canary.37 or later**, bundled
docs live at `node_modules/next/dist/docs/`. Before doing PPR work, Cache
Components work, or any non-trivial Next.js task, read the relevant doc there
— your training data may be outdated. The bundled docs are the source of truth.

See https://nextjs.org/docs/app/guides/ai-agents for background.

---

## When this skill loads

Your first message introduces the tool and asks setup questions. Don't say
"ready, what would you like to do?" and don't run speculative commands or
auto-discover (port scans, `project`, config reads).

If the user already provided a URL, cookies, and task in their message,
skip the questions — go straight to `open` and start working. Only ask
what's missing.

Otherwise say something like:

> This opens a headed browser against your Next.js dev server so I can
> read the React component tree, see the PPR shell, and check errors the
> way you would in DevTools. To start:
>
> - What's your dev server URL? (And is it running?)
> - Are the pages you're debugging behind a login? If so I'll need your
>   session cookies — easiest is to copy them from your browser's
>   DevTools → Application → Cookies into a JSON file like
>   `[{"name":"session","value":"..."}]`. If the pages are public, skip
>   this.

Wait for answers. Then `open <url> [--cookies-json <file>]`. Every other
command errors without an open session.

---

## Commands

### `open <url> [--cookies-json <file>]`

Launch browser, navigate to URL. With `--cookies-json`, sets auth cookies
before navigating (domain derived from URL hostname).

```
$ next-browser open http://localhost:3024/vercel --cookies-json cookies.json
opened → http://localhost:3024/vercel (11 cookies for localhost)
```

Cookie file format: `[{"name":"authorization","value":"Bearer ..."}, ...]`

Only `name` and `value` are required per cookie — omit `domain`, `path`,
`expires`, etc. To create the file, use Bash (`echo '[...]' > /tmp/cookies.json`)
since the Write tool requires a prior Read.

### `close`

Close browser and kill daemon.

---

### `goto <url>`

Full-page navigation (new document load). Server renders fresh.

```
$ next-browser goto http://localhost:3024/vercel/~/deployments
→ http://localhost:3024/vercel/~/deployments
```

### `push [path]`

Client-side navigation via `next.router.push()`. Without a path, shows an interactive picker of all links (↑/↓, enter).

```
$ next-browser push /vercel/~/deployments
→ http://localhost:3024/vercel/~/deployments
```

If push fails silently (URL unchanged), the route wasn't prefetched.

### `back`

Browser back button.

### `reload`

Hard reload current page.

### `restart-server`

Restart the Next.js dev server (POSTs to `/__nextjs_restart_dev`).
Clears filesystem cache, forces clean recompile. Polls until the server
has a new execution ID, then reloads the page.

Last resort. HMR picks up code changes on its own — reach for this only
when you have evidence the dev server is wedged (stale output after edits,
builds that never finish, errors that don't clear).

`restart-server` often exits with `net::ERR_ABORTED` — this is expected
(the page detaches during restart). Follow up with `goto <url>` to
re-navigate after the server is back. Don't treat this error as a failure.

---

### `ppr lock`

**Prerequisite:** PPR requires `cacheComponents` to be enabled in
`next.config`. Without it the shell won't have pre-rendered content to show.

Enter PPR instant-navigation mode. Sets the `next-instant-navigation-testing`
cookie. After this:
- `goto` — server sends raw PPR shell (static HTML with `<template>` holes).
  No hydration — what you see is server HTML only.
- `push` — Next.js router blocks dynamic data writes, shows prefetched shell.
  Requires the current page to already be hydrated (prefetch is client-side),
  so lock *after* you've landed on the origin, not before.

```
$ next-browser ppr lock
locked
```

### `ppr unlock`

Exit PPR mode and print the shell analysis. Captures:
1. Locked snapshot — which boundaries are suspended = holes in the shell
2. Releases the lock, waits for boundaries to settle
3. Unlocked snapshot — what blocked each boundary (suspendedBy)
4. Matches them, prints Dynamic holes / Static

```
$ next-browser ppr unlock
unlocked

# PPR Shell Analysis
# 131 boundaries: 3 dynamic holes, 128 static

## Dynamic holes (suspended in shell)
  Next.Metadata
    rendered by: MetadataWrapper
  TeamDeploymentsLayout at app/(dashboard)/[teamSlug]/.../layout.tsx:37:9
    suspenders unknown: thrown Promise (library using throw instead of use())
  TrackedSuspense at ../../packages/navigation-metrics/.../tracked-suspense.js:6:20
    rendered by: TrackedSuspense > RootLayout > AppLayout
    blocked by:
      - usePathname (SSR): /vercel/~/deployments awaited in <FacePopover>

## Static (pre-rendered in shell)
  GeistProvider at .../geist-provider.tsx:80:9
  TrackedSuspense at ...
  ...
```

Each hole shows: boundary name + source, `rendered by:` ownership chain,
`blocked by:` the dynamic calls (hooks, server APIs, scripts, cache, etc.)

**`errors` doesn't report while locked.** If the shell looks wrong (empty,
bailed to CSR), unlock and `goto` the page normally, then run `errors`.
Don't debug blind under the lock.

**Full bailout (scrollHeight = 0).** When PPR bails out completely, `unlock`
returns just "unlocked" with no shell analysis — there are no boundaries to
report. In this case, unlock, `goto` the page normally, then use `errors`
and `logs` to find the root cause.

---

### `tree`

Full React component tree (via DevTools `flushInitialOperations`).

```
$ next-browser tree
# React component tree
# Columns: depth id parent name [key=...]
# Use `tree <id>` for props/hooks/state. IDs valid until next navigation.

0 38167 - Root
1 38168 38167 HeadManagerContext.Provider
2 38169 38168 Root
...
224 46375 46374 DeploymentsProvider
226 46506 46376 DeploymentsTable
```

### `tree <id>`

Inspect one component: ancestor path, props, hooks, state, source location
(source-mapped to original file).

```
$ next-browser tree 46375
path: Root > ... > Prerender(TeamDeploymentsPage) > Prerender(FullHeading) > Prerender(TrackedSuspense) > Suspense > DeploymentsProvider
DeploymentsProvider #46375
props:
  children: [<Lazy />, <Lazy />, <span />, <Lazy />, <Lazy />]
hooks:
  IsMobile: undefined (1 sub)
  Router: undefined (2 sub)
  DeploymentListScope: undefined (1 sub)
  User: undefined (4 sub)
  Team: undefined (4 sub)
  ...
  DeploymentsInfinite: undefined (12 sub)
source: app/(dashboard)/[teamSlug]/(team)/~/deployments/_parts/context.tsx:180:10
```

IDs are valid until navigation. Re-run `tree` after `goto`/`push`.

---

### `screenshot`

Full-page PNG to a temp file. Returns the path. Read with the Read tool.

```
$ next-browser screenshot
/var/folders/.../next-browser-1772770369495.png
```

Don't narrate what the screenshot shows — the user can see the browser.
State your conclusion or next action, not a description of the page.

### `eval <script>`

Run JS in page context. Returns the result as JSON.

```
$ next-browser eval 'document.title'
"Deployments – Vercel"

$ next-browser eval 'document.querySelectorAll("a[href]").length'
47

$ next-browser eval 'document.querySelector("nextjs-portal")?.shadowRoot?.querySelector("[data-nextjs-dialog]")?.textContent'
"Runtime ErrorCall Stack 6..."
```

Use this to read the Next.js error overlay (it's in shadow DOM).

---

### `errors`

Build and runtime errors from the Next.js dev server MCP.

```
$ next-browser errors
{
  "configErrors": [],
  "sessionErrors": [
    {
      "url": "/vercel/~/deployments",
      "buildError": null,
      "runtimeErrors": [
        {
          "type": "console",
          "errorName": "Error",
          "message": "Route \"/[teamSlug]/~/deployments\": Uncached data or `connection()` was accessed outside of `<Suspense>`...",
          "stack": [
            {"file": "app/(dashboard)/.../deployments.tsx", "methodName": "Deployments", "line": 105, "column": 27}
          ]
        }
      ]
    }
  ]
}
```

`buildError` is a compile failure. `runtimeErrors` has `type: "runtime"`
(React errors) and `type: "console"` (console.error calls).

### `logs`

Recent dev server log output (NDJSON from `.next/dev/logs/`).

```
$ next-browser logs
{"timestamp":"00:01:55.381","source":"Server","level":"WARN","message":"[browser] navigation-metrics: skeleton visible was already recorded..."}
{"timestamp":"00:01:55.382","source":"Browser","level":"WARN","message":"navigation-metrics: content visible was already recorded..."}
```

---

### `network`

List all network requests since last navigation.

```
$ next-browser network
# Network requests since last navigation
# Columns: idx status method type ms url [next-action=...]
# Use `network <idx>` for headers and body.

0 200 GET document 508ms http://localhost:3024/vercel
1 200 GET font 0ms http://localhost:3024/_next/static/media/797e433ab948586e.p.d2077940.woff2
2 200 GET stylesheet 6ms http://localhost:3024/_next/static/chunks/_a17e2099._.css
3 200 GET fetch 102ms http://localhost:3024/api/v9/projects next-action=abc123def
```

Server actions show `next-action=<id>` suffix.

### `network <idx>`

Full request/response for one entry. Long bodies spill to temp files.

```
$ next-browser network 0
GET http://localhost:3024/vercel
type: document  508ms

request headers:
  accept: text/html,...
  cookie: authorization=Bearer...; isLoggedIn=1; ...
  user-agent: Mozilla/5.0 ...

response: 200 OK
response headers:
  cache-control: no-cache, must-revalidate
  content-encoding: gzip
  ...

response body:
(8234 bytes written to /tmp/next-browser-12345-0.html)
```

---

### `page`

Route segments for the current URL (via Next.js MCP).

```
$ next-browser page
{
  "sessions": [
    {
      "url": "/vercel/~/deployments",
      "routerType": "app",
      "segments": [
        {"path": "app/(dashboard)/[teamSlug]/(team)/~/deployments/layout.tsx", "type": "layout", ...},
        {"path": "app/(dashboard)/[teamSlug]/(team)/~/deployments/page.tsx", "type": "page", ...},
        {"path": "app/(dashboard)/[teamSlug]/layout.tsx", "type": "layout", ...},
        {"path": "app/(dashboard)/layout.tsx", "type": "layout", ...},
        {"path": "app/layout.tsx", "type": "layout", ...}
      ]
    }
  ]
}
```

### `project`

Project root and dev server URL.

```
$ next-browser project
{
  "projectPath": "/Users/judegao/workspace/repo/front/apps/vercel-site",
  "devServerUrl": "http://localhost:3331"
}
```

### `routes`

All app router routes.

```
$ next-browser routes
{
  "appRouter": [
    "/[teamSlug]",
    "/[teamSlug]/~/deployments",
    "/[teamSlug]/[project]",
    "/[teamSlug]/[project]/[id]/logs",
    ...
  ]
}
```

### `action <id>`

Inspect a server action by its ID (from `next-action` header in network list).

---

## Scenarios

### Growing the static shell

The shell is what the user sees the instant they land — before any dynamic
data arrives. The measure is the screenshot while locked: does it read as
the page itself? A shell can be non-empty and still bad — one Suspense
fallback wrapping the whole content area renders *something*, but it's a
monolithic loading state, not the page.

A meaningful shell is the real component tree with small, local fallbacks
where data is genuinely pending. Getting there means the composition layer
— the layouts and wrappers between those leaf boundaries — can't itself
suspend. `ppr unlock` names what suspended (`blocked by:`) and where it
sits (`rendered by:`). A suspend high in the tree is what collapses
everything beneath it into one fallback.

Work it top-down. For the component that's suspending: can the dynamic
access move into a child? If yes, move it — this component becomes sync
and rejoins the shell. Follow the access down and ask again.

When you reach a component where it can't move any lower, there are two
exits — both are human calls, bring the question to them:

- Wrap it in a Suspense boundary. The fallback UI should resemble what
  renders inside — design it together, don't assume.
- Cache it so it's available at prerender (Cache Components). Whether
  this data is safe to cache — staleness, who sees it — is their call,
  not yours.

**Test your hypothesis before proposing a fix.** If you suspect a
component is the cause, find evidence — check `errors`, inspect the
component with `tree`, or compare a route where the shell works to
one where it doesn't. Don't commit to a root cause or propose changes
from a single observation.

There are two shells depending on how the user arrives. They're observed
differently and can differ in content — establish which one you're
optimizing before touching the browser. If the ask is "make this page
load faster" without qualification, ask: cold URL hit, or clicking in
from another page (which page)? Don't guess, don't do both.

**Direct load — the PPR shell.** Server HTML for a cold hit on the URL.
Lock first, then `goto` the target — the lock suppresses hydration so you
see exactly what the server sent. Screenshot once the load settles, then
unlock.

**Client navigation — the prefetched shell.** What the router already
holds when a link is clicked. The origin page decides this — it's the one
doing the prefetching — so `goto` the origin *unlocked* and let it fully
hydrate. Then lock, `push` to the target, let the navigation settle,
screenshot, unlock. Locking before the origin hydrates means nothing got
prefetched and `push` has nothing to show.

Between iterations: check `errors` while unlocked.

**After making a code change:** HMR picks it up — just re-lock,
`goto` the page, and re-test. No need to `restart-server`.
