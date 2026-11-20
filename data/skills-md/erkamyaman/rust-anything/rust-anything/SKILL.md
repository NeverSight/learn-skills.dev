---
name: rust-anything
description: Port TypeScript/JavaScript, Python, C, Go, Ruby or Java to Rust with the rust-anything CLI or MCP tools, from one hot function up to a whole app rewritten as a pure Rust app - profile, plan, bridge one unit at a time, record the original's behavior, port, diff, bench, shadow and gate; batch hot loops so they run in Rust on all cores. Use when asked to rewrite, port or migrate code or an app to Rust, to plan such a migration, or to make slow code faster with Rust.
---

# Migration to Rust with rust-anything

rust-anything gives you ground truth; you write the Rust. Port one unit at a time, even when the
goal is the whole app, and call a port done only when `gate` passes.

**Whole app to a pure Rust app** (the user wants the app rewritten in Rust, with the original kept
only as reference): read [whole-app.md](whole-app.md) first and follow it. It grills the user on
the decisions, researches the dependencies, records the whole app, puts a Rust front door in front
of the original, runs the steps below for every unit, then lifts the app to a standalone Rust
binary (or, for a library, one pure Rust crate). CLIs, HTTP servers and libraries.

Languages: TypeScript/JavaScript, Python, C, Go, Ruby, Java. The language is detected; `--lang`
overrides it. The steps are the same everywhere; only the bridge differs (napi-rs or wasm for
TS, PyO3, a C ABI, cgo, a magnus extension, JNI), and the original's callers keep their API.
For PHP: `analyze`, and for a whole app `app record`, `app replay` and
`app front-door` (CLIs, and servers run with `php -S 127.0.0.1:{port} router.php`); `bridge` does not
take PHP units yet, so tell the user before planning a PHP port past the front door. C# works
the same way: record a built app (`dotnet out/app.dll`, servers with
`--urls http://127.0.0.1:{port}`); `bridge` does not take C# units yet.

Tools: the `rust-anything` CLI, or the same steps as MCP tools (`rust-anything mcp`): `profile`,
`analyze`, `bridge`, `refresh`, `record`, `build`, `diff`, `bench`, `shadow`, `gate`, and for a
whole app `app_record`, `app_replay`, `app_front_door`, `app_wire`, `app_lift`.
If the MCP tools are not available, use the CLI; if `rust-anything` is not installed, ask the user
to install it (`cargo install rust-anything`) and run
`rust-anything setup`, then restart the agent. When a step fails because a runtime, the agent
setup or the MCP server is missing or out of date, run `rust-anything doctor`: it checks each one
and prints the command that fixes it.

## 0. Profile: find what is worth moving

When the goal is speed, measure before choosing anything:

```sh
rust-anything profile <repo> -- node bench.mjs      # or: python3 bench.py, ruby bench.rb,
                                                #     java -cp out Main, go test -run X -bench . ./pkg
```

It runs a real workload under the runtime's own profiler and lists hot functions with their
callers and advice. Go profiles only through `go test`; C is not supported (use `perf`).

- A small function called once per item is **not** worth porting alone: one call into Rust costs
  more than its work, and JITs (V8, the JVM, Go) run it in nanoseconds. Port it together with its
  callers, or batch it (step 2b). The advice line says which, with the exact command.
- Code that is already compiled (numba `@njit`, Cython, `@jax.jit`) runs as machine code: a Rust
  port gains little speed. `profile` lists it under "Already compiled" and says so in the advice of
  every hot function that calls it; tell the user before porting it for speed.
- If the user only wants a migration, skip to step 1.

## 1. Plan, then stop

```sh
rust-anything analyze <repo> -o plan.md        # people
rust-anything analyze <repo> --json            # you: schema rust-anything/analyze@1
```

- Present the `start_here` units (best first ports) and the order by package and wave.
- Call out `keep` units (UI, editor code: they stay in the source language), `blocked` units and
  their reason, and dependencies with fit `none` or `unknown`. Do not hand-roll a missing crate
  silently: flag it.
- **Wait for the user's approval of the plan and of the first unit.**

## 2. Port one unit

```sh
rust-anything bridge <repo> <unit-id>          # crate in <repo>/rust/<name>; never overwrites
rust-anything record <crate>                   # the original's behavior on edge-case inputs -> cases.jsonl
```

- If the original has tests, record their calls too: `record <crate> --from-tests -- npx jest`
  (TS/JS, any runner) or `-- pytest` (Python). Every call the suite makes to the unit's exported
  functions becomes a case; the source is restored afterwards. Exports that are not function
  declarations (`export const f = () => ...`) are listed as not captured.
- Add real-world inputs with `--inputs cases.jsonl` (`{"fn": name, "args": [...]}` per line) when
  the generated ones cannot reach the interesting paths (structured arguments, domain strings).
- TS that cannot run directly in Node (extensionless imports, path aliases): record from built
  output with `--module dist/x.mjs`, or pass `--node-arg=--import=tsx`.
- If the original has no tests, `record` is the characterization suite: keep `cases.jsonl`.

Write the port in `src/port.rs` only; `src/lib.rs` and the wrappers are generated. After changing
a signature in `port.rs`, run `rust-anything refresh <crate>`.

- Read each risk the plan lists for the unit, at its `file:line`, before writing code.
- String offsets: JS and Java index UTF-16 code units, Rust UTF-8 bytes: use `src/utf16.rs`.
- Errors: return `Err("TypeName: message")`; it becomes that exception in Python, Ruby and Java,
  and the `error` text in Go. Inside `port.rs`, a small error enum is clearer; turn it into that
  string only in the exported function.
- Letters and digits: Rust's `char::is_alphanumeric` takes more than Java's
  `Character.isLetterOrDigit` (letters and decimal digits, per UTF-16 unit, so nothing beyond
  U+FFFF) or Python's `str.isalpha` (letters only). Match the original's rule by general category.
- Numbers in Python and Ruby: ints that the original passes through must come back as ints;
  in Python ports use `crate::pynum::Num` for int-or-float, not `serde_json::Value`.
- C: inputs recorded as `crash:` are undefined behavior; any result passes.
- Ordered maps and object keys: `indexmap` where order reaches output.
- Regex lookaround or backreferences: `fancy-regex`, not `regex`. Either way, `\w`, `\b`, `\d`
  and case-insensitive matching treat non-ASCII text differently from the source language's
  engine: passing the recorded cases is not enough. `record` adds regex traps (Turkish i, Kelvin
  sign, joiners, non-ASCII digits and spaces) to functions in files that use regexes; ask the user
  for real text the patterns see, record it with `--inputs`, and set `unicode(false)` or spell out
  ASCII classes (`[A-Za-z0-9_]`) where the original's `\w` is ASCII-only (JS without `u`, Java).
- No `unsafe`. If truly needed: minimal, isolated, with a `// SAFETY:` comment.
- Add Rust unit tests in `port.rs` for the cases you reason about. `cargo test` passing with no
  tests proves nothing: the recorded cases are the proof.
- To silence a lint, use `#[expect(lint, reason = "...")]`, not `#[allow]`, so it is flagged once
  it no longer applies.

## 2b. Batch a hot loop

For a function called over many items (search, scoring, formatting a list):

```sh
rust-anything bridge <repo> <unit> --batch fn:param    # or: rust-anything refresh <crate> --batch fn:param
```

This generates a class that takes the `param` values once and keeps them in Rust:
`new FnBatch(items)` (TS, Python, Java), `Mod::FnBatch.new(items)` (Ruby), `NewFnBatch(items)`
(Go). Per query, `run(<other args>)` returns every result as one array, and `rank(<other args>,
min)` returns the item indexes, best first. It runs on all cores, and errors are the original's.
Close the batch when done in Go and Java (finalizers are only a fallback).

- Make the caller build the batch once, not per query. Map returned indexes back to items with a
  plain loop; in JS, `Array.from(order, fn)` costs 20x more.
- To prepare items once (lowercase, masks, position tables), define `pub struct FnIndex` in
  `port.rs` with `new(items)` and `run(<other args>) -> Result<Vec<R>, String>`. It must give the
  same result as the function, item by item: test it against the function over every item.
- When ranking can skip work, give the index its own `rank(<other args>, min) -> Result<Vec<u32>,
  String>` (narrowing to the last query's matches as the user types, table lookups). It must
  match ranking the function's results: score high to low, ties in item order.
- A batch multiplies the port's per-item speed by the cores. Against compiled originals (Go,
  Java) the port itself must be fast: handle ASCII without Unicode tables, build each result in one
  pre-sized `String`, avoid intermediate copies. Keep `diff` passing.
- Items and other arguments: numbers, booleans and strings (Ruby: any value); results: numbers,
  booleans or strings. Not for C.
- Batch crates allocate with mimalloc, which is built from C. Pass `--allocator rusty_alloc` to
  `bridge` if the target has no C compiler.

## 3. Prove it

```sh
rust-anything build <crate>
rust-anything diff <crate>                     # must be N/N
rust-anything bench <crate>                    # original vs Rust, bridge included, with a verdict
```

A mismatch is a behavior difference: fix the port, never the recording. If the difference is
intended (the user wants the port to fix a bug of the original), ask the user first, then add one
line per case to `<crate>/known-diffs.jsonl`: `{"fn", "args", "actual", "reason"}`, with `fn`,
`args` and `actual` copied from `diff --json`. That case then passes only with exactly that result,
and `gate` fails once it no longer differs, so remove the line then. If `gate` says the recording
is stale, the original changed: record again before porting further. After pulling upstream
changes, run `rust-anything map` (the `map` tool): every port marked changed needs `record`, then
`diff`, and the new mismatches are what changed upstream.

When `diff` says the port is stalled (its `trend.stalled`: three changes to `port.rs` in a row
gained no matching case), stop editing. Show the user the remaining mismatches and ask: they may
know the rule you are missing, or decide to keep those functions in the original for now. Each
failed `gate` check carries a `fix`: run that first.

Numeric code (physics, statistics, graphics) rarely gives bit-identical floats once ported:
operation order, fused multiply-add and the math library differ. When the user accepts that,
record with `--float-tolerance 1e-9` (their number): floats then match within that share of the
larger value (absolute below 1), and `diff` and `gate` use it. Integers, strings and the same
value written differently (`3` and `3.0`) still must match exactly. Never widen a tolerance to make
a mismatch go away: a difference beyond it is a bug in the port.

Follow `bench`'s verdict: ship, keep the slower functions in the source language, or port a
bigger unit (batch or include the callers). Do not ship a port that makes callers slower without
saying so.

## 4. Ship it safely

```sh
rust-anything shadow <crate>                   # drop-in with the original's API
```

Load the shadow where the app loaded the original. `RUST_ANYTHING_MODE=shadow` (default) returns the
original's results and reports Rust mismatches; `new` switches to Rust; `old` turns Rust off.
The public API does not change.

## 5. Done means gate passes

```sh
rust-anything gate <crate>
```

fmt, clippy with warnings as errors, cargo tests, `unsafe` only with SAFETY comments, nothing
`unimplemented!`, every place the original fails on purpose (`throw`, `raise`, an `error` result)
reached by a recorded failing case (add one with `record --inputs` when gate names it), no
`unwrap`, `expect` or `panic!` in a function whose original returns an error (return `Err`; for a
state the original also treats as impossible, a `// INFALLIBLE: <why>` comment), the port at most
3x the original's lines plus 50 for imports and signatures (over that, use the crates `analyze` lists and fold repeated code), the
module builds, every export present, every recorded case matches. A Rust panic never matches a
recorded error: return `Err` where the original throws.

Then report to the user, and **wait for their go-ahead before the next unit**:

- what changed (files, functions, bridge, batches),
- gate output, diff counts and bench numbers,
- behavior differences or risks left (e.g. error messages differ, a napi `String` refuses lone
  surrogates), and what is left in the plan.
