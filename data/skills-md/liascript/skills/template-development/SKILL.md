---
name: template-development
description: >
  Expert guidance for developing LiaScript templates — creating reusable macros, integrating
  JavaScript libraries (via CDN or as bundled npm projects), handling async execution, and following
  all established template patterns from the LiaTemplates ecosystem. Use when building, modifying, or
  debugging a LiaScript template.
license: CC0-1.0
---

# LiaScript Template Development

You are an expert LiaScript template developer. Apply the full knowledge below when helping the user build or modify LiaScript templates.

## What is a LiaScript Template?

A template is a standard LiaScript course (`README.md`) whose **header comment** defines reusable macros. The same file:
- Defines macros (used via `import:` in other courses)
- Demonstrates each macro in the slides below
- Is itself a runnable LiaScript course

---

## Macro Syntax

### Single-line macro (with colon — collapses all indented lines into one)
```markdown
<!--
@highlight: <b style="color: @0">@1</b>
@highlight_red: @highlight(red, @0)
-->
```

### Block macro (no colon — preserves whitespace; ends with `@end`)
```markdown
<!--
@MyBlock
<div id="container_@0">
  HTML, JS, CSS all work here.
  Other @macros can be called inside.
</div>
@end
-->
```

### Parameters
- `@0`, `@1`, `@2` … — positional (comma-separated at call site)
- Commas inside a param: wrap in backticks `` `val, ue` ``
- **Code block as last param**: `` ```lang @MacroName(p0) `` — fenced block content becomes final arg
- **URL as last param**: `@[MacroName(p0)](url)` — relative URLs auto-resolved to absolute
- **Escaped for JS strings**: `@'input` or `@'0` — backslash-escapes the value (safe for template literals)

### Calling macros from macros
```markdown
@outer: @inner(@uid, @0)   ← @uid generates a unique DOM id each call
```

### Commenting out macros
```markdown
@@SingleLineMacro       ← commented, won't run
@@@BlockMacro ... @end  ← block comment
```

### Debugging: prefix with extra `@` to dump expansion in a gray `<pre>`
```markdown
@@MyMacro(args)
```

---

## Header Meta-Macros

```markdown
<!--
author:    Name; Another Author
email:     contact@example.com
version:   0.1.0
language:  en
narrator:  US English Female
comment:   Short description shown on course card
logo:      ./logo.png
icon:      ./favicon.png
attribute: [LibName](url) by Author is licensed under [MIT](url)
repository: https://github.com/org/repo
edit:      true
mode:      Presentation | Slides | Textbook
persistent: true
-->
```

---

## Loading External JS & CSS

### Choosing how to load your library

A template's JavaScript can come from three places — pick the simplest one that works:

| Approach | Use when | How |
|---|---|---|
| **CDN / prebuilt** | A ready-made browser build (UMD/IIFE) exists on a CDN | `script: https://cdn.../lib.min.js` |
| **Local custom script** (no build) | You're hand-writing the glue yourself — wrapping an API, fetching/transforming external data | `script: ./local.js` |
| **npm package + bundler build** | The library is only on npm (no usable CDN build) or must be bundled with its deps | `npm run build` → `script: dist/index.js` (see [Template as an npm Project](#template-as-an-npm-project-bundling-a-library)) |

```markdown
<!--
script: https://cdn.example.com/lib.js
        ./local.js

link:   https://cdn.example.com/style.css
        ./local.css
-->
```
Multiple URLs: one per line, indented. Script/tag execution delayed until all loaded.

### Inline CSS (not shared when imported)
```markdown
<!--
@style
  body { font-size: 1.2em; }
  @keyframes fadeIn { from { opacity:0 } to { opacity:1 } }
@end
-->
```

### One-time JS initialization
```markdown
<!--
@onload
  window.myLib = {}
  // runs once before course loads
@end
-->
```

---

## Template as an npm Project (bundling a library)

When a JS library lives **only on npm** (no usable CDN/UMD build), needs to be **bundled with its
dependencies**, or you want a **self-contained template with a pinned version**, make the template a
real npm project: install the library, bundle a small entry point into `dist/index.js`, and load
that bundle from the header with `script: dist/index.js`. This is the build-time alternative to
loading a prebuilt CDN script.

> Real-world example: [LiaTemplates/Algebrite](https://github.com/LiaTemplates/Algebrite) bundles the
> npm-only `algebrite` CAS this way.

### Two distribution models

| Model | Build step? | Header |
|---|---|---|
| CDN / prebuilt | none | `script: https://cdn.../lib.min.js` |
| npm-bundled | `npm install` → `npm run build` | `script: dist/index.js` |

### Project layout
```
src/index.js      ← entry point: import the npm lib, attach what you need to window
dist/index.js     ← the bundle (COMMITTED — LiaScript loads it raw from the repo)
package.json
README.md         ← the template/course; header has `script: dist/index.js`
```

### `package.json`
Parcel is the bundler the LiaTemplates ecosystem uses (least config); esbuild/rollup/webpack work
too.
```json
{
  "name": "lia-mylib",
  "version": "0.1.0",
  "app": "dist/index.js",
  "scripts": { "build": "npx parcel build src/index.js" },
  "targets": { "app": {} },
  "devDependencies": {
    "mylib": "^1.0.0",
    "parcel": "^2.16.4"
  }
}
```
`"app": "dist/index.js"` together with `"targets": { "app": {} }` tells Parcel to emit a single,
fixed output filename — without it Parcel produces a content-hashed name and the `script:` line
can't reference a stable `dist/index.js`.

### `src/index.js` — expose globals the macros call
The bundle's only job is to put the library (and any helpers) on `window`, so macro `<script>`
blocks can reach it:
```js
// CommonJS
window.MyLib = require('mylib')

// or ESM
import MyLib from 'mylib'
window.MyLib = MyLib

// expose your own helpers too
window.myHelper = (input) => { /* ... */ }
```
Expose exactly what the macros reference — e.g. a `@MyLib.eval` macro that runs
`window.MyLib.run(\`@input\`)`.

### Build & setup
```bash
npm install        # pull deps into node_modules/
npm run build      # bundle src/index.js → dist/index.js
```
Re-run `npm run build` after any change to `src/` or after bumping the library version.

### Commit `dist/`, ignore the rest (important gotcha)
Unlike a normal npm package, the **bundle must be committed**: LiaScript fetches
`script: dist/index.js` *raw from the repository at runtime*, so an uncommitted `dist/` means the
template is broken for everyone importing it. Put `node_modules/` and `.parcel-cache/` in
`.gitignore`; do **not** ignore `dist/`.

### Versioning
Pin the npm dependency (`"mylib": "^1.0.0"`) so rebuilds are reproducible, and — per
[Pattern 10](#pattern-10--versioned-import-for-stability-in-courses) — offer consumers both a pinned
import URL (a tag/commit) and the `master` URL. Credit the bundled library in the header
`attribute:` field (see the header meta-macros and skeleton below).

---

## The `send` Object (Code Block API)

Every `<script>` tag gets a `send` object scoped to that block:

```js
// Control strings (last statement OR via send.lia())
"LIA: stop"       // halt, no output shown
"LIA: wait"       // show loading spinner (for async)
"LIA: terminal"   // activate interactive REPL
"LIA: clear"      // clear console

// Send output at any point during execution
send.lia("message")                    // output + continue
send.lia("LIA: stop")                  // output + stop
send.lia("message", [], true)          // success
send.lia("message", [], false)         // failure/error

// Render dynamic content
send.lia("LIASCRIPT:\n## Heading\n...") // parse as LiaScript
send.lia("HTML: <b>bold</b>")          // inject raw HTML
send.liascript(`## Dynamic content`)   // same as LIASCRIPT: prefix

// Console shorthands
console.log(...)     // info output
console.warn(...)    // warning
console.error(...)   // error (red)
console.debug(...)   // gray debug
console.html(str)    // inject HTML into console
console.stream(str)  // streaming text (no trailing newline)

// Terminal I/O
send.handle("input", input => { /* handle user typing */ })
send.handle("stop",  e     => { /* cleanup on stop */ })

// Cross-block events
send.register("event-name", callback)
send.dispatch("event-name", payload)
```

---

## 12 Implementation Patterns

### Pattern 1 — Synchronous interpreter (AlaSQL, BiwaScheme, Skulpt)
```markdown
@MyLang.eval
<script>
try {
  MyInterpreter.run(`@input`)
  "LIA: stop"
} catch(e) {
  let err = new LiaError(e.message, 1);
  err.add_detail(0, e.name + ": " + e.message, "error", lineNum - 1, 0);
  throw err;  // annotates editor with error location
}
</script>
@end
```

### Pattern 2 — Async rendering with unique ID (mermaid, JSXGraph, Chat)
```markdown
@mermaid: @mermaid_(@uid, ```@0```)   ← public shortcut injects a uid

@mermaid_
<script run-once modify="false" style="display:block; background: white">
async function draw() {
    const { svg } = await mermaid.render('graphDiv_@0', `@1`);
    send.lia("HTML: " + svg);
    send.lia("LIA: stop")
}
draw()
"LIA: wait"
</script>
@end
```

### Pattern 3 — Web components (ABCjs, JSXGraph)
The `dist/index.js` below is produced by an npm build — see [Template as an npm Project](#template-as-an-npm-project-bundling-a-library).
```markdown
script: dist/index.js     ← bundles custom HTML element definitions

@MyLib.render: @MyLib.renderWith( , ```@0```)

@MyLib.renderWith
<lia-keep>
<my-element @0>@1</my-element>
</lia-keep>
@end

@MyLib.eval: @MyLib.evalWith( , @0)

@MyLib.evalWith
<script>
console.html(`<my-element @0>@input</my-element>`)
"LIA: stop"
</script>
@end
```
`<lia-keep>` prevents LiaScript from destroying the wrapped element on slide change.

### Pattern 4 — Heavy runtime with global state (Pyodide, SQLite)
```markdown
@onload
window.myRuntime = null
window.myRuntime_running = false

async function initRuntime() {
    window.myRuntime = await loadRuntime()
}
initRuntime()
@end

@Lang.eval: @Lang.eval_(@uid)          ← public, passes uid

@Lang.eval_
<script>
if (window.myRuntime_running) {
    setTimeout(() => console.warn("Another process running..."), 500)
    "LIA: stop"
} else {
    window.myRuntime_running = true
    async function run() {
        const code = "@'input"   // backslash-escaped — safe in template literals
        try {
            const result = await window.myRuntime.exec(code)
            send.lia(String(result))
        } catch(e) {
            console.error(e.message)
        }
        send.lia("LIA: stop")
        window.myRuntime_running = false
    }
    setTimeout(run, 500)
    "LIA: wait"
}
</script>
<div id="target_@0"></div>
@end
```

### Pattern 5 — Shortcut chaining
```markdown
@Lang.eval:        @Lang.eval_(@uid)        ← public, injects uid
@Lang.eval.turtle: @Lang.eval_(skulpt_canvas) ← variant with fixed container
@highlight_green:  @highlight(green, @0)    ← default-param shortcut
@load.java:        @load(java, @0)          ← language-specific shortcut
```

### Pattern 6 — Dynamic content via fetch
```markdown
@load
<script style="display:block" modify="false" run-once>
fetch("@1")
  .then(r => r.ok ? r.text() : Promise.reject("404: @1"))
  .then(t => send.lia("LIASCRIPT:\n```@0\n" + t + "\n```"))
  .catch(e => send.lia("HTML: <span style='color:red'>" + e + "</span>"))
"loading: @1"
</script>
@end

@[load(java)](relative/path/App.java)   ← link syntax auto-resolves relative URLs
```

### Pattern 7 — Multiple code block inputs
```markdown
@SQL.run2(db-name)     ← receives two code blocks:
                           @input(0) = first block
                           @input(1) = second block

```SQL -hidden-setup
CREATE TABLE ...       ← minus prefix = hidden from student
```
```SQL +visible-query
SELECT * FROM ...      ← plus prefix = visible to student
```
@SQL.run2(mydb)
```

### Pattern 8 — `LiaError` for editor annotation
```js
let e = new LiaError("Error summary", 1);  // 1 = number of source files
e.add_detail(
    0,            // file index (0-based)
    "message",    // detail shown in console/gutter
    "error",      // or "warning"
    row - 1,      // 0-indexed row (subtract 1 from reported line)
    column        // 0-indexed column
);
throw e;
```

### Pattern 9 — `<script>` tag attributes
| Attribute | Effect |
|---|---|
| `run-once` / `run-once="true"` | Execute only on first render, not on slide revisit |
| `modify="false"` | Disable double-click-to-edit |
| `modify="// marker\n"` | Custom delimiter for the editable code region |
| `style="display: block"` | Show script output as a block element |

### Pattern 10 — Versioned import (for stability in courses)
```markdown
<!-- pinned (stable) -->
import: https://raw.githubusercontent.com/LiaTemplates/Pyodide/0.3.5/README.md

<!-- latest (may break) -->
import: https://raw.githubusercontent.com/LiaTemplates/Pyodide/master/README.md
```
Always offer both options to users.

### Pattern 11 — Template file structure
```
README.md            ← the template IS a LiaScript course
js/
  skulpt.min.js      ← bundled JS (or load from CDN)
src/
  index.js           ← bundler entry point (npm projects only)
dist/
  index.js           ← compiled web component bundle (committed)
```
Every slide in README.md demonstrates one macro with a live example, then an "Implementation" slide at the end shows all macro definitions. When the JS comes from npm, `src/` + `package.json` drive the build that produces `dist/index.js` — see [Template as an npm Project](#template-as-an-npm-project-bundling-a-library).

### Pattern 12 — Special built-in macros
| Macro | Where valid | Effect |
|---|---|---|
| `@uid` | Anywhere except header | Unique DOM id, different on each call |
| `@input` | Inside `<script>` tags | Current code block / quiz / user input |
| `@input(N)` | Inside `<script>` tags | Nth code block in a multi-file project |
| `@'input` | Inside `<script>` tags | Backslash-escaped input (for JS strings) |
| `@output` | Code block header | Marks which block is the output display |

---

## Minimal Template Skeleton

```markdown
<!--
author:   Your Name
email:    you@example.com
version:  0.0.1
language: en
narrator: US English Female
logo:     ./logo.png
comment:  One-line description for the course card.

script:   https://cdn.example.com/library.min.js

attribute: [LibraryName](https://lib.example.com)
           by Author is licensed under [MIT](https://opensource.org/licenses/MIT)

@MyLib.eval
<script>
try {
  MyLib.run(`@input`)
  "LIA: stop"
} catch(e) {
  let err = new LiaError(e.message, 1);
  err.add_detail(0, e.message, "error", 0, 0);
  throw err;
}
</script>
@end
-->

# MyLib - Template

Import via:
`import: https://raw.githubusercontent.com/LiaTemplates/mylib/master/README.md`

## `@MyLib.eval`

Add `@MyLib.eval` to any code block:

```mylang
-- your code here --
```
@MyLib.eval

## Implementation

``` html
script: https://cdn.example.com/library.min.js

@MyLib.eval
<script>
...
</script>
@end
```
