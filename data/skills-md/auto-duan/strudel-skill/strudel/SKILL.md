---
name: strudel
description: Write correct Strudel (strudel.cc) live-coding music code. Provides verified per-function references, mini-notation syntax, common gotchas, and runnable example patterns. Use when writing, editing, reviewing, or debugging Strudel / TidalCycles-style patterns, or when the user mentions Strudel, mini-notation, live coding music, or functions like note(), s(), n(), stack, jux, euclid.
---

# Strudel

## Overview

Strudel is a browser-based live-coding language for music — a JavaScript port of TidalCycles. Code is built from **patterns**: strings of "mini-notation" passed to functions like `s()`, `note()`, and `n()`, then transformed with chained `.method()` calls. This skill provides verified reference material so you write Strudel that actually runs, instead of inventing functions or misusing syntax.

All references are verified against the official docs (https://strudel.cc/). Treat them as the source of truth — do not rely on memory for function names, signatures, or aliases.

## Workflow

When asked to write or fix Strudel code:

1. **Refresh syntax** — read `references/cheatsheet.md` for the high-density overview of mini-notation, core functions, and effect params. This alone covers most needs.
2. **Check the trap list** — skim `references/gotchas.md` before committing code. Strudel has many counterintuitive behaviors (single vs double quotes, `stack` vs `cat`, continuous signals needing `.segment()`, `fast`/`slow` not changing pitch).
3. **Verify each function you use** — before using any function, confirm it exists and you have the right name/signature:
   - Query `references/index.json` (machine-readable manifest of all 111 functions + alias map). Resolve aliases here (`cutoff` → `lpf`, `s` → `sound`, `density` → `fast`).
   - For full docs on one function, read `references/functions/<category>/<name>.md`. Each file has signature, parameters, verified examples, gotchas, and related functions.
4. **Borrow from examples** — `references/patterns/` has complete runnable compositions (drums, chord voicings, euclidean rhythms, scale melodies, layered tracks). Adapt these rather than building from scratch.

## Core mental model

- **Mini-notation** lives inside double quotes `"..."` or backticks — single quotes are NOT parsed as patterns.
- Events in a sequence split the cycle's time evenly. `[ ]` subdivides one slot, `< >` alternates one value per cycle, `,` stacks (chord/polyphony), `*` speeds up, `~` is a rest.
- `stack` plays patterns simultaneously; `cat`/`seq` play them one after another. This distinction drives most composition.
- Transforms chain with `.method()`. `fast`/`slow`/`rev`/`ply`/`off`/`every` reshape time and structure but do NOT change pitch.
- Continuous signals (`sine`, `saw`, `rand`, `perlin`) output 0..1. To make events from them, use `.segment(n)`; to modulate a param, pass them to `.lpf()`, `.gain()`, etc.
- Pitch comes from `note` (absolute names like `c3 e3 g3`) or `n` + `scale` (scale degrees). Scales use `root:type` form, e.g. `"C:minor"`.
- Effects are params in the chain: `gain`, `pan`, `lpf`/`cutoff`, `hpf`, `room`, `delay`, `speed`, plus ADSR (`attack`/`decay`/`sustain`/`release`).

## Reference map

| File | What's in it | When to read |
|---|---|---|
| `references/cheatsheet.md` | High-density syntax + key functions | First, almost always |
| `references/gotchas.md` | Common mistakes & counterintuitive behavior | Before finalizing code |
| `references/mini-notation/README.md` | Complete mini-notation DSL reference | When using complex pattern strings |
| `references/index.json` | All 111 functions: names, signatures, aliases, categories | To check a function exists / resolve an alias |
| `references/functions/<category>/<name>.md` | Full per-function docs | When using a specific function |
| `references/patterns/*.md` | Complete runnable example compositions | When building a full track |

Function categories: `transform` (48), `sound` (32), `signal` (10), `tonal` (11), `sample` (5), `structure` (5).

## Rules

- Never invent a function or alias. If you can't find it in `index.json`, it probably doesn't exist — search for the capability instead (e.g. by tag in `index.json`).
- Prefer verified examples from the reference files over generated-from-memory code.
- When the user runs newer Strudel than these docs, defer to the live REPL / official docs at https://strudel.cc/ and note the version uncertainty.

## Source of truth

- Official docs: https://strudel.cc/
- Official repo: https://codeberg.org/uzu/strudel
- Reference docs in this skill are generated from https://github.com/auto-duan/strudel-docs-for-ai (one verified file per function).
