---
name: pandascript
description: Write PandaScript agent scripts (.js) — Lightpanda's replayable browser-automation format, run token-free with `lightpanda agent script.js`.
---

# Writing Lightpanda agent scripts

Run with:

```console
./lightpanda agent script.js
```

## Mental model (get this right first)

The script runs in its **own V8 context** — neither the page nor Node.js:

- `Page` is the only global. `new Page()` makes a page and `await page.goto(url)` navigates it; every other primitive is a **method on that page**: `const page = new Page(); await page.goto(url); page.extract({...}); page.click(sel);`.
- No `window`, `document`, DOM, `localStorage` — read pages with `page.extract(...)`, run page-side JS only via `page.evaluate("...")`.
- No `require`, `process`, `fs`, npm. Standard ECMAScript built-ins only (`JSON`, `Map`, template literals, …).
- `page.goto(...)` is **async — always `await` it**. Page methods are **synchronous**: `const data = page.extract({...})`, never `await page.extract(...)`. The script body runs as an async function, so top-level `await` is allowed.
- **Re-navigating reuses the same page**: `await page.goto(url2)` keeps `page` valid and points it at the new URL, discarding the old page — read it before navigating away. Independent URLs don't share a page: make a `new Page()` for each and load them in parallel (fan-out, best practice 2).
- Page `evaluate("...")` cannot see script variables — interpolate values into the string. Script code cannot see page variables.
- Variables persist across navigations within one run, so cross-page aggregation is plain JS.
- **`return <value>` is the script's output**, printed automatically (objects/arrays as JSON). End with `return page.extract({...});` or `return results;`. A bare trailing expression is NOT printed; neither is `console.log(JSON.stringify(...))`.

## Primitives

`Page` is the only global; `new Page()` makes a page and everything else is a method on it.

| Call | Notes |
|------|-------|
| `new Page()` | Makes a page object. No navigation yet — call `page.goto(url)` before any other method. Make several to navigate in parallel (fan-out, best practice 2). |
| `page.close()` | Marks the page done; later method calls on it error. The page is otherwise reclaimed at script end. |
| `await page.goto(url[, { timeout }])` | **Async — must be `await`ed.** Navigates the page (re-navigating reuses the same object). Waits for `load`. Rejects on navigation failure; a **timeout does NOT reject** (the page may still be usable). Default timeout 10000 ms. |
| `page.evaluate(script[, { url, timeout, save }])` | Page-side JS escape hatch; returns text (JSON for objects/arrays). |
| `page.extract(schema)` | The only primitive returning a real JS value (object/array). The schema is its only argument. See schema below. |
| `page.click(selector)` |  |
| `page.fill(selector, value)` |  |
| `page.scroll([{ x, y }])` |  |
| `page.waitForSelector(selector[, { timeout }])` | `waitFor*` default timeout 5000 ms. |
| `page.waitForScript(script[, { timeout }])` | Re-evaluates page JS until truthy. |
| `page.waitForState(state[, { timeout }])` | `state`: one of `"load"`, `"domcontentloaded"`, `"networkalmostidle"`, `"networkidle"`, `"done"`. |
| `page.hover(selector)` |  |
| `page.press(selector, key)` | Selector first! `page.press("Enter")` binds "Enter" to `selector` and fails — use `page.press(null, "Enter")` or `page.press({ key: "Enter" })`. |
| `page.selectOption(selector, value)` |  |
| `page.setChecked(selector[, checked])` | `checked` defaults to `true`. |

Options (the trailing `{ … }` object; every option may be omitted):

- `goto`: `timeout` — Optional timeout in milliseconds. Defaults to 10000.
- `evaluate`: `url` — Optional URL to navigate to before evaluating. `timeout` — Optional timeout in milliseconds. Defaults to 10000. `save` — Optional bridge-store key. The evaluate's return value is stored under this name and re-exposed as `lp.<name>` to subsequent evaluates. Objects, arrays, and strings are serialized automatically — no JSON.stringify needed.
- `scroll`: `x` — Optional: The horizontal scroll offset. `y` — Optional: The vertical scroll offset.
- `waitForSelector`: `timeout` — Optional timeout in milliseconds. Defaults to 5000.
- `waitForScript`: `timeout` — Optional timeout in milliseconds. Defaults to 5000.
- `waitForState`: `timeout` — Optional timeout in milliseconds. Defaults to 5000.

Calling convention: leading positionals + optional trailing options object, or one object with everything (`page.waitForSelector("#row", { timeout: 2000 })` ≡ `page.waitForSelector({ selector: "#row", timeout: 2000 })`). A bare option positional (`page.waitForSelector("#row", 2000)`) and a field passed both ways are `invalid arguments`. `null` skips a positional. Arguments must be JSON-serializable.

CSS selectors only — `backendNodeId`s don't exist here. Standard CSS only: no jQuery `:contains()` or Playwright `:has-text()`.

## extract schema

Keys = output field names; values pick what to lift (not a JSON Schema):

```js
const { stories } = page.extract({
  stories: [{
    selector: "tr.athing",          // one record per match
    limit: 5,
    fields: {                        // resolved relative to each match
      title: ".titleline > a",      // first match's text (null if missing)
      url: { selector: ".titleline > a", attr: "href" },
      text: ""                       // "" = the matched element's own text
    }
  }]
});
```

- `"sel"` → first match's text; `["sel"]` → all matches' text; `{ selector, attr }` / `[{ selector, attr }]` → attribute(s); `limit: N` caps any array form.
- Every value is a string or null — parse numbers in script logic.
- Empty arrays are valid results; if **every** field misses, extract throws ("no schema selector matched any element") → your selectors are wrong, not the page empty.
- An object schema always returns an object (destructure it); a bare array schema returns the array directly.
- No `save:` option in scripts — keep results in variables.

## Best practices

1. **Navigate, settle, read.** After `await page.goto` on a dynamic page (feeds, search results, comment threads), call `page.waitForState("networkidle")` or `page.waitForSelector(...)` before extracting. Most static pages are complete at `load` — don't wait blindly.
2. **List-to-detail — fan out independent pages.** Extract the list, then open one page per item and start every navigation together so the detail pages load in parallel instead of one-after-another:
   ```js
   const list = new Page();
   await list.goto(listUrl);
   const { items } = list.extract({ items: [{ selector: "a.row", fields: { url: { attr: "href" } } }] });

   const pages = items.map(() => new Page());
   await Promise.all(pages.map((p, i) => p.goto(items[i].url)));   // all in flight at once
   return pages.map((p, i) => ({ ...items[i], ...p.extract({ /* schema */ }) }));
   ```
   - Concurrency is bounded by the HTTP connection pool: 40 total (`--http-max-concurrent`) and 6 per host (`--http-max-host-open`, the browser default — raising it much higher risks overwhelming the target server). Extra navigations queue rather than fail, so a same-site fan-out loads ~6 pages at a time. For long lists, fan out in batches and `page.close()` each page once read so its memory is reclaimed.
   - `Promise.all` rejects the whole batch if any `goto` *fails* (a timeout does not reject); use `Promise.allSettled` when partial results are fine.
   - Walk **serially** on one page (`for (const it of items) { await page.goto(it.url); … }`) only when the steps depend on each other — each page decides the next URL, or they share login/session state.
3. **`evaluate` is a last resort, not a reading tool.** A `querySelectorAll`-and-parse `page.evaluate` block is always wrong: lift the raw strings with `page.extract`, then trim/split/parse them in top-level JS. Reserve `page.evaluate` for behavior that must run inside the page and no builtin covers — and remember its state dies on every navigation/reload, while script variables persist.
4. **Credentials via `$LP_*` placeholders** in any string argument (`page.fill("#pw", "$LP_HN_PASSWORD")`). Never inline a real secret; placeholders resolve inside the Lightpanda process.
5. **Unique selectors.** Disambiguate with attributes/position: `input[type="submit"][value="login"]`, not `input[type="submit"]`.
6. **Let failures fail.** Primitives throw on error and stop the script — only `try/catch` where you have a real fallback (e.g. optional cookie banner: `try { page.click("#accept") } catch {}`).
7. **End with `return <result>`.** `console.log` is for debug output only and doesn't JSON-format objects.
8. Modern, readable JS: `const`/`let`, `for (const x of xs)`, template literals, destructuring, 2-space indent.
9. **Comment the intent of each block.** Put a one-line `//` comment above each logical step describing what it accomplishes toward the goal (not restating the call). One comment per block, not per line — skip self-evident lines:
   ```js
   // Load the Hacker News front page
   const page = new Page();
   await page.goto("https://news.ycombinator.com");

   // Pull the top 5 stories (title + link)
   const { stories } = page.extract({ stories: [{ selector: "tr.athing", limit: 5, fields: { title: ".titleline > a", url: { selector: ".titleline > a", attr: "href" } } }] });

   // Open each story page in parallel and read its text
   const pages = stories.map(() => new Page());
   await Promise.all(pages.map((p, i) => p.goto(stories[i].url)));
   ```

## Common errors

| Error | Cause / fix |
|-------|-------------|
| `extract is not defined` (or click/fill/…) | These are methods on the page object, not globals → `const page = new Page(); await page.goto(url); page.extract(...)` |
| `Page must be called with new` | `Page(...)` called without `new` → `const page = new Page();` |
| `page is not navigated or has been closed` | A method on a fresh `new Page()` (or a closed page) → `await page.goto(url)` first |
| `page handle is no longer valid` | Used a page after a later `goto` on the **same** page replaced it → read it before navigating away. Sibling pages from other `new Page()` calls stay valid. |
| `document is not defined` | DOM API in script context → use `page.extract` or `page.evaluate` |
| `require is not defined` | Not Node.js |
| `no page loaded - run page.goto(url) first` | Page method before navigation |
| `invalid arguments` | Wrong arity/shape, non-JSON value, or a field set both positionally and in options |
| `extract: no schema selector matched any element` | All schema fields missed → fix selectors |
| `press` fails with one string arg | Selector-first: use `page.press(null, "Enter")` or `page.press({ key: "Enter" })` |
