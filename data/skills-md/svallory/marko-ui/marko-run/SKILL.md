---
name: marko-run
description: Use when building or editing a Marko Run (@marko/run) app — anything under src/routes (+page, +layout, +handler, +middleware, +meta, +404, +500), route path syntax ($id, $$rest, _pathless, flat routes), Run.GET/POST verb helpers, ctx/$global request context, validation (params/search/json/form), data loading via next(), Run.href, vite.config adapters (node/static/netlify), or the marko-run CLI. Not for Marko template syntax itself (see marko6).
---

# Marko Run

Distilled from https://markojs.com/docs/marko-run. File-based routing on Vite, streaming SSR, zero config. `references/routing.md` (files, paths, flat routes, execution order), `references/handlers.md` (verb helpers, validation, data loading, context, typed URLs, embedding), `references/deploy.md` (vite plugin, adapters, CLI).

## Mental model

- `src/routes/**` — only `+`-prefixed files are routable; everything else is ignored (colocate components/tests freely).
- Request → **middlewares** (root→leaf) → **handler** → **layouts** (root→leaf) → **page**. Layouts+page compile into one component.
- `ctx` (handlers/middleware) === `$global` (templates). `ctx.params`, `ctx.url` are serialized to the browser by default; add others via `ctx.serializedGlobals`.
- Data flows down through `next({ ... })` → `ctx.data` / `$global.data` (shallow merge). **Pass promises, `<await>` them in the page** — awaiting before `next` kills streaming.
- `Run` is a global (no import): `Run.GET/HEAD/POST/PUT/DELETE/PATCH/OPTIONS/QUERY/ALL`, `Run.href`, types `Run.Context`, `Run.Platform`.

## Quick reference

### Files (any depth under routes)
| File | Role |
|---|---|
| `+page.marko` | GET → HTML. One per path. |
| `+layout.marko` | wraps nested layouts/pages; `input.content` = child. `$global` = ctx. |
| `+handler.ts` | `export const GET/POST/... = Run.X(...)`. One per path. Return `Response`, or `undefined` → `next()` auto. Missing HEAD → GET minus body. |
| `+middleware.ts` | `export default Run.ALL(...)` (all verbs) or `Run.POST(...)` (one verb); runs before handlers; options-only form `Run.ALL({ search })` attaches validation below. |
| `+meta.json` / `+meta.ts` | static `ctx.meta`; verb keys (`"POST": {...}`) shallow-override per method. |
| `+404.marko`, `+500.marko` | root-only; when `Accept` has `text/html`; wrapped by root layout. |

### Path segments
`users` static · `_admin` pathless (ignored in URL, scopes layouts/middleware) · `$id` param (`$` alone = match, no capture) · `$$rest` catch-all to end (`$$` no capture; nothing nests inside).
Flat routes: `projects.$projectId.members+page.marko`; dirs may use it too (`projects.$projectId/members+page.marko`); merged with nested dirs. Multi-path `members,people+page.marko`; groups `(members,people)`; optional `(home,)` or `(home,_x)`. Escape control chars with backticks: `` `sitemap.xml`/+handler.ts ``.

### Handlers & validation
```ts
export const POST = Run.POST({ json: NoteSchema }, async (ctx, next) => {
  const [note, issues] = await ctx.body;          // Standard Schema → [value, issues]; fn validator → its return
  if (issues) return Response.json({ issues }, { status: 422 });
  return ctx.redirect("/thanks");                 // PRG on success; next({ issues }) to re-render form with errors
});
```
- Options: `params`, `search` (fn or sync Standard Schema; lazy, cached on first access), `json` (`validator`, `maxBytes` 1MiB), `form` (`validator`, `maxBytes`, `maxParts` 1000, `maxFiles` 20, `maxFileBytes` 1MiB, `onFile(ctx, file)`; repeated fields → arrays). Forms: `Run.POST(options, [auth, handler])` arrays compose.
- `ctx.body` is a **promise** (`await ctx.body`), lazy, `undefined` when no `json`/`form` option. Don't call `ctx.request.json()` — bypasses validation/limits.
- Options merge across middleware+handler (last validator wins, objects shallow-merge).
- `ctx` methods: `fetch(url, init)` (internal re-request, sets `parent`), `render(template, input, init)`, `redirect(to, status=302)`, `back(fallback="/", status)`.
- `Run.href("/projects/$projectId/members", { params: { projectId: 42 }, search: {...}, hash })` — typed against real routes when `.marko-run/routes.d.ts` is in tsconfig `include`; rewritten at compile time on the client.

### Types
Generated `.marko-run/routes.d.ts` (needs tsconfig at root; add to `include`) narrows `Run.Context` per file (params, meta, search, body, upstream `data`). Extend globally: `declare module "@marko/run" { interface Context { db: DB } interface Platform { ... } }` — reserve for app-wide props; per-route data goes through `next()`.

### Config / deploy
- No `vite.config` needed. When needed: `import marko from "@marko/run/vite"; plugins: [marko({ adapter, routesDir, trailingSlashes })]` (+ all `@marko/vite` options). `trailingSlashes`: `RedirectWithout` (default) | `RedirectWith` | `RewriteWithout` | `RewriteWith` | `Ignore`.
- Adapter resolution: option → first dep named `@marko/run-adapter*`/`*marko-run-adapter*` → built-in Node. Packages: `@marko/run-adapter-node` (Express middleware: `routerMiddleware()`, `matchMiddleware()` → `req.route.invoke`), `@marko/run-adapter-static` (`urls: [...] | async fn`, crawls links), `@marko/run-adapter-netlify` (`{ edge: true }` + `netlify.toml` `functions`/`edge_functions = "dist"`, publish `dist/public`).
- Embed: `import * as router from "@marko/run/router"` → `router.fetch(request, platform)`, `router.match(method, path)` + `router.invoke(route, request, platform)`.
- CLI (`marko-run`, run via `bun run`/`bunx`): `dev` (default, `-p`), `build` (`-o`), `preview` (`-o -p -f`); all take `-c config`, `-e dotenv`.

## Common mistakes
- Awaiting data in `GET` before `next()` → whole response blocked. Pass the promise.
- Returning `next()` from a successful `POST` → refresh resubmits, URL unshareable. Redirect instead.
- Async Standard Schema validators throw at runtime — sync only.
- `ctx.body()` — it's a promise, not a function.
- Handler that always returns its own `Response` never renders the page (its verb is dropped from the page's typed context).
- Nesting route files inside a `$$catch-all` dir — never traversed.
- Expecting `$global.session` on the client — only `params`/`url` serialize by default; add to `ctx.serializedGlobals` (and never secrets).
