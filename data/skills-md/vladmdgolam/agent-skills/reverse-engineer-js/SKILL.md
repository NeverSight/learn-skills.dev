---
name: reverse-engineer-js
description: "Reverse-engineer minified or obfuscated JavaScript bundles. Primary tool: humanify (humanifyjs) — uses an LLM to rename mangled identifiers back to meaningful names. Default model: gemini-3.8-flash. Use when the user says 'deobfuscate this bundle', 'humanify this', 'rename minified vars', 'reverse engineer this JS', 'what does bundle.js do', or is working in a project with a deobfuscated `og/` or `modules/` folder fed by humanify. Covers humanify CLI invocation, the pseudo-TTY workaround for cursorTo crashes, single-module extraction from a bundle, and chaining with beautifiers."
---

# Reverse Engineer JS

LLM-assisted deobfuscation of minified / mangled JavaScript using [humanifyjs](https://github.com/jehna/humanify) plus surrounding tooling for extracting and reintegrating modules.

# Tools at a glance

| Tool | Purpose | When |
|------|---------|------|
| `humanifyjs` (npx) | Rename mangled vars/functions via LLM | Mangled but already valid JS |
| `prettier` / `js-beautify` | Reformat single-line minified code | Before humanify, if needed |
| `webcrack` | Unpack webpack / browserify bundles into per-module files | When bundle is one big file |
| Source-map sleuthing | `// # sourceMappingURL=...` may exist next to the bundle | Always check first — beats LLM rename |

Always check for a sourcemap (`bundle.js.map` or `sourceMappingURL` comment in the file) **before** spending tokens on humanify. If found, original sources are recoverable for free.

# Default humanify invocation

Use Gemini unless the user says otherwise:

```bash
npx humanifyjs gemini -m "gemini-3.8-flash" -o <outputDir> <inputFile>
```

Requires `GEMINI_API_KEY` in env (the project's root `.env` is the usual place).

Other backends:

```bash
# OpenAI
npx humanifyjs openai --apiKey="$OPENAI_API_KEY" --model gpt-4.1-mini bundle.js

# Local (slower, free)
npx humanifyjs local bundle.js
```

# Critical gotchas

## 1. Pseudo-TTY required in non-interactive shells

humanify calls `process.stdout.cursorTo(...)` for its progress bar. In Claude Code / CI / piped contexts, stdout is not a TTY and the call **crashes with `TypeError: process.stdout.cursorTo is not a function`**.

Wrap the call in `script -q /dev/null`:

```bash
script -q /dev/null npx humanifyjs gemini -m "gemini-3.8-flash" -o "$OUT" "$IN"
```

(macOS/BSD `script` syntax. On Linux: `script -qc "<cmd>" /dev/null`.)

## 2. Output filename is fixed

humanify always writes its result as `<outputDir>/deobfuscated.js` regardless of input filename. Don't expect `module_1234.js` in → `module_1234.js` out.

## 3. Long files = long runs

humanify processes top-level declarations sequentially with one LLM call each. A 5 MB bundle can take 30+ minutes. Strategies:
- Run on **single modules** extracted from the bundle, not the whole thing
- Pre-split with `webcrack` first if the bundle is webpacked
- Pick the cheapest model that still reads the code well. `gemini-3.8-flash` is the default here; on a very large bundle a lite variant (`gemini-3.5-flash-lite`) cuts the per-declaration cost, at some accuracy cost on dense code

## 4. Keep an archive of the original

Before any rewrite, copy the pristine bundle to `archive/bundle.original.js`. humanify is non-deterministic and you may want to re-run with a different model.

# Workflow A: Whole-bundle deobfuscation

When the bundle is small (<500 KB) or you have time:

```bash
mkdir -p archive out
cp bundle.js archive/bundle.original.js
script -q /dev/null npx humanifyjs gemini \
  -m "gemini-3.8-flash" \
  -o out bundle.js
# result: out/deobfuscated.js
```

Then optionally run `prettier --write out/deobfuscated.js` for nicer formatting.

# Workflow B: Single-module extraction (large bundles)

Common in fxhash / generative-art bundles: a single bundle contains many `id: (params) => { ... }` modules and you only want to humanify a few interesting ones.

1. **Identify the module ID** — search the bundle for distinctive strings, then trace back to the enclosing `<id>: (e, t, n) => {` opener.
2. **Extract the module body** — match the opener, count braces (respecting strings) until the matching `}`.
3. **Wrap as a standalone arrow** — write `(e, t, n) => { <body> }` to a temp file. humanify needs valid top-level code.
4. **Run humanify** — `script -q /dev/null npx humanifyjs gemini -m "gemini-3.8-flash" -o "$OUT" "$IN"`.
5. **Unwrap** — strip the `(e, t, n) => { ... }` shell back off the result.
6. **Save and stub** — write the deobf'd body to `modules/module_<id>_<name>.js`, replace the body in the bundle with a stub like `<id>: (e, t, n) => { window.DEOBF[<id>](e, t, n); }`.

If the project already has a `scripts/deobfuscate.js` (or similar), reuse it — the brace-counting / string-escape logic is finicky enough that re-deriving it for each new bundle is a waste. A typical script: takes a numeric module ID, extracts the body from `bundle.js`, runs humanify on the wrapped function, unwraps, and writes `modules/module_<id>_<name>.js`.

# Workflow C: Webpack bundle → per-module files

When dealing with a webpack bundle, [webcrack](https://github.com/j4k0xb/webcrack) splits modules cleanly before humanify even runs:

```bash
npx webcrack bundle.js -o webcracked/
# Then humanify each module of interest:
script -q /dev/null npx humanifyjs gemini \
  -m "gemini-3.8-flash" \
  -o humanified webcracked/modules/123.js
```

# Examples

## Example 1: deobfuscate a small fxhash bundle

**User says:** "humanify the bundle.js in this fxhash project"

**Actions:**
1. Check for sourcemap: `head -c 4096 bundle.js | tail -c 200` — look for `sourceMappingURL`. None? Continue.
2. Confirm `GEMINI_API_KEY` in `.env`. Source it: `set -a; source .env; set +a`.
3. Archive: `mkdir -p archive && cp bundle.js archive/bundle.original.js`.
4. Run: `mkdir -p out && script -q /dev/null npx humanifyjs gemini -m "gemini-3.8-flash" -o out bundle.js`.
5. Beautify: `npx prettier --write out/deobfuscated.js`.

**Result:** `out/deobfuscated.js` with renamed vars, ready to read.

## Example 2: deobfuscate one module out of a giant bundle

**User says:** "Deobfuscate module 3658 from `og/bundle.js`, name it `treeGenerator`"

**Actions:**
1. If the project already has a deobfuscation helper (e.g. `scripts/deobfuscate.js`), run it: `node scripts/deobfuscate.js 3658 treeGenerator`.
2. Otherwise: extract the module body by brace-counting, wrap as `(e, t, n) => { ... }`, run humanify with `script -q /dev/null`, unwrap, save to `modules/module_3658_treeGenerator.js`, stub the bundle.

**Result:** New file in `modules/` with a readable version of the function; `bundle.js` shrunk by stubbing.

## Example 3: humanify crashed with `cursorTo is not a function`

**User says:** "humanify just dies immediately"

**Diagnosis:** Non-TTY stdout (this is the default in Claude Code's bash tool).

**Fix:** Re-run wrapped in `script -q /dev/null <cmd>` (macOS) or `script -qc "<cmd>" /dev/null` (Linux).

# Troubleshooting

## `cursorTo is not a function`
**Cause:** stdout is not a TTY. **Fix:** wrap in `script -q /dev/null`.

## `GEMINI_API_KEY` not set
**Cause:** humanify reads from process env, not from the project `.env` automatically. **Fix:** `set -a; source .env; set +a` in the same shell, or pass inline: `GEMINI_API_KEY=... npx humanifyjs gemini ...`.

## Output is identical to input (no renames)
**Cause:** humanify only renames identifiers it considers mangled (short, single-letter). Already-readable code is left alone. **Fix:** confirm the input is actually obfuscated; if names like `useState` survive that's expected, not a bug.

## Rate limits / quota errors from Gemini
**Cause:** large file, many top-level functions → many sequential LLM calls. **Fix:** switch to `local` backend for free local rename, or extract a single module (Workflow B) instead of the whole bundle.

## humanify takes hours
**Cause:** big bundle, sequential per-function calls. **Fix:** pre-split with `webcrack`, or only humanify the modules you actually need.

## Output directory contains stale `deobfuscated.js`
**Cause:** humanify writes to a fixed filename. A failed second run will pick up the previous good output. **Fix:** `rm -f $OUT/deobfuscated.js` before each run.
