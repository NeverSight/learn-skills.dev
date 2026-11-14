---
name: migrating-to-moc-2
description: "Move a Motoko project from moc 1 to moc 2 — toolchain bump, removed compiler flags, and the fix for every new error. Load when bumping the moc toolchain to a 2.x release, when code that built on moc 1 fails on moc 2, or when one codebase must compile with both."
license: Apache-2.0
compatibility: "moc >= 2.0.0, mops >= 3.0.0"
metadata:
  title: Migrating to moc 2
  category: Motoko
---

# Migrating to moc 2

moc 2 is a major release of the Motoko compiler. It changes four things:

- **Persistence.** Actors are persistent by default. Enhanced orthogonal persistence (EOP) is the only memory model and the incremental GC the only collector.
- **Strictness.** Warnings for code that traps or silently does not do what it says are now errors, and a pattern must fit the type it matches.
- **Syntax.** A few moc 1 forms no longer parse (`a ??b`, a branch glued to its condition, `flexible`). Several lighter forms are new and optional.
- **Flags.** Every flag of a removed feature is rejected as an unknown option.

Most projects need a handful of edits, and the compiler names each one. This skill maps every diagnostic to its fix. The upstream [moc 1 → 2 migration guide](https://github.com/caffeinelabs/motoko/blob/master/doc/md/moc-v2-migration.md) has longer explanations, and the [release notes](https://github.com/caffeinelabs/motoko/releases) list each change per release.

## First: is any canister still on classical persistence?

moc 2 cannot build a canister on classical (32-bit) persistence, but it can upgrade one to EOP. A deployed canister is classical if it was built with `--legacy-persistence`, with a non-incremental GC flag (`--copying-gc`, `--compacting-gc`, `--generational-gc`), or with a moc older than 0.15, where classical was the default.

- **Move it to EOP:** compile that **one** upgrade with `--enhanced-orthogonal-persistence` and **without** `--enhanced-migration`. The move is irreversible; later upgrades need neither flag. Without the flag the upgrade traps ("Detected implicit upgrade from classical orthogonal persistence to enhanced orthogonal persistence"); with `--enhanced-migration` it traps too ("Cannot upgrade from classical orthogonal persistence with --enhanced-migration").
- **Keep it classical:** stay on moc 1.

A canister that moved to EOP with a moc older than 1.5.0 can trap on a later upgrade with `cannot upgrade from an actor using enhanced migration to an actor not using enhanced migration`. Run that one upgrade with graph-copy stabilization; the upstream [EOP migration path](https://github.com/caffeinelabs/motoko/blob/master/doc/md/fundamentals/actors/orthogonal-persistence/enhanced.md#migration-path) has the steps.

Every other canister already runs on EOP and needs no persistence work.

## Checklist

1. **Build cleanly on the latest moc 1 first.** The `.vals()` (M0269) and `preupgrade`/`postupgrade` (M0270) deprecations are identical in moc 2, so fix them before switching; on moc 2, `mops check --fix` rewrites `.vals()` to `.values()`. Fix every warning in the [diagnostics table](#diagnostics) too — most become errors.
2. **Bump the toolchain** to the latest 2.x release: `mops toolchain use moc <version>` (it rewrites `[toolchain] moc` in `mops.toml`), or wherever your build pins moc.
3. **Delete the [removed flags](#removed-flags)** from `[moc].args`, `[build].args`, `[canisters.<name>].args`, `dfx.json` and build scripts.
4. **Run `mops check`** and fix what it reports in this order, because earlier errors hide later ones:
   1. syntax errors (`??`, glued branches, `flexible`, record literals in block position);
   2. errors that were warnings in moc 1;
   3. M0277, redundant `async` on a function body;
   4. M0142 and M0193 in libraries and actor classes;
   5. M0131, only if you built with `--legacy-actors`.
5. **Check upgrade compatibility** against the deployed version before upgrading a live canister: `mops check-stable`, or `moc --stable-compatible old.most new.most`. Removing `persistent` and `stable` keywords does not change the stable signature.
6. **Optionally adopt the moc 2 forms** — only once nothing builds this code with moc 1 anymore. See [After the switch](#after-the-switch).

## Removed flags

moc 2 exits with `unknown option '<flag>'` on each of these.

| Flag                                                                  | Replacement                                                                                                 |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `--default-persistent-actors`, `--require-persistent-actors`         | none needed: actors are persistent by default                                                               |
| `--legacy-actors`                                                     | mark every field that should reset on upgrade `transient`                                                  |
| `--legacy-persistence`, `--copying-gc`, `--compacting-gc`, `--generational-gc` | none: stay on moc 1 for classical canisters                                                        |
| `--incremental-gc`, `--rts-stack-pages`, `--skip-gc-deprecation-warning`, `--experimental-rtti` | none needed                                                                     |
| `--experimental-stable-memory`                                        | use `Region`                                                                                                |
| `--experimental-field-aliasing`                                       | none: [record update copies `var` fields](#record-update-copies-var-fields)                                 |
| `--generate-view-queries`                                             | write `public query func` getters. The generated `__<field>` queries leave the canister's Candid interface on upgrade, so update any client that called them |
| `--trap-on-call-error`                                                | none: a failed call throws; handle it with `try`/`catch`                                                    |
| `--experimental-multi-value`, `--no-experimental-multi-value`         | none needed                                                                                                 |
| `-no-system-api`                                                      | `-wasi-system-api` to run outside the Internet Computer                                                     |
| `-ref-system-api`                                                     | none needed: it selected the default                                                                        |
| `--print-source-on-error`, `-no-link`, `--profile`, `--profile-file`, `--profile-line-prefix`, `--profile-field` | none                                                                  |

`--enhanced-orthogonal-persistence` stays: it is a no-op on EOP canisters, and only the one-time classical upgrade needs it. `-A`, `-W` and `-E` no longer accept `M0135` and `M0142`.

## Diagnostics

Each moc 1 warning that became an error can be downgraded again with `-W <code>` (e.g. `-W=M0145,M0215` in `[moc].args`). That is a stopgap: the code it lets through traps or silently misbehaves. Pattern errors M0116, M0050 and M0115 cannot be downgraded.

| Code | In moc 1 | What it flags | Fix |
| --- | --- | --- | --- |
| M0001 at `??` | accepted | `a ??b` — `??` is whitespace-sensitive like `<` | `a ?? b` |
| M0001 at `flexible` | accepted | `flexible` is no longer a keyword | `transient` |
| M0273 | accepted | a block after `??` — `{` there now opens a record literal | `opt ?? do { ... }` |
| M0275 | accepted | a branch glued to its condition (`if (c)-1 else 1`, `if c[0] else [1]`), or a bare branch after a compound condition (`if f(x) a else b`) | space before the branch (`if (c) -1 else 1`), or braced branches |
| M0272 | M0001 | a record literal in block position — a `case` body, function body, or `if`/`switch`/`while` head | nest it as the block's result: `case null { { x = 0 } }`; parenthesize a head: `switch ({ x = 0 })` |
| M0274 | M0001 | a reserved keyword (`query`, `implicit`, …) as an identifier | rename it |
| M0277 | accepted | `= async { ... }` or `= ignore (async ...)` as a function body | drop the `async`; see [Async function bodies](#async-function-bodies) |
| M0145 | warning | a pattern that does not cover every value, in `switch`, `let`, `catch`, `for` and parameters | `let ... else { ... }`, or a `case _` arm |
| M0222 | warning | `ignore` of an `async*` value, which never runs | `await*` it |
| M0210 | warning | a parenthetical on an `await*` call, where it has no effect | attach `(with cycles = n)` to an `async` call |
| M0212 | warning | an unknown parenthetical attribute (`(with cycle = n)`) | fix the name: `cycles` |
| M0215 | warning | a field the expected type drops, e.g. the typo in `{ u with emial = e }` | fix the name, or drop the field |
| M0128 | warning | a function named like a system method (`heartbeat`, `inspect`, …) without `system` | `system func ...`, or rename it |
| M0242 | warning | a `public func` without a return type, implicitly oneway | `: ()` if oneway is intended, else `: async ()` |
| M0005 | warning | an import path whose letter case differs from the file name | match the file name |
| M0276 | warning M0062 | a comparison whose result is constant, at a type with one value (`Any`, `{}`, records sharing no field) | compare the fields you mean: `user.id == order.userId` |
| M0278 | warning M0251 | a file in the `--enhanced-migration` directory with no `public func migration`, so it never ran | rename the function to `migration`, or move the module out of the directory |
| M0074, M0081, M0101 | warning | an array, `if` or `switch` whose only common type is `Any` | make the elements or branches agree, or annotate `: Any` if intended |
| M0166, M0167 | warning | an intersection that is `None`, a union that is `Any` | write the intended type |
| M0116 | warning M0146 | a variant tag the scrutinee's type lacks — usually a typo | fix the tag; to match a wider type on purpose, annotate the scrutinee: `switch (x : T)` |
| M0050 | warning M0146 | a signed literal pattern (`case (-1)`) against `Nat` | annotate `switch (n : Int)`, or drop the case |
| M0115 | warning M0146 | an option pattern against `Null` | fix the scrutinee's type |
| M0142 | warning | an imported file that is a bare list of declarations | wrap it in `module { ... }` and mark exports `public` |
| M0193 | warning M0135 | an actor class whose return type is not `async` | `actor class C() : async actor { ... }` |
| M0131 | not reported: the field was transient | a function or object field that `--legacy-actors` left transient is now persistent | mark it `transient` |
| M0057 | accepted | under `moc --check a.mo b.mo`, a file using another file's declaration without importing it | move the shared code into a module and import it |
| M0072 | accepted | `mo:base/ExperimentalStableMemory` and the `Prim.stableMemory*` primitives are gone | use `Region` |

New **warnings**, which only break a `-Werror` build:

- M0217 / M0218 — the `persistent` keyword and `stable` modifier are redundant. `mops check --fix` deletes them, so hold off while moc 1 must still build the code: there, a bare `actor` needs `--default-persistent-actors`.
- M0196 — an explicit `<system>` on a primitive that no longer needs it (`Prim.getSelfPrincipal`, `Prim.envVar`, `Prim.envVarNames`, `Prim.callerInfoSigner`, `Prim.callerInfoData`, `Prim.getCandidLimits`, `Prim.getCandidTypeLimits`). Delete it; `query` methods can now call these.
- M0236 — a module call that could use dot notation (`Map.size(m)` → `m.size()`), now on by default. `mops check --fix` applies it; `-A M0236` silences it.
- M0146 — now also reported for an alternative that is never matched in `let ... else`.

## Persistence

### Actors are persistent by default

Every `actor` and `actor class` is persistent: its `let` and `var` fields keep their values across upgrades unless declared `transient`. Code written as `persistent actor` with `stable` fields compiles unchanged, with warnings M0217 and M0218.

If you built with `--legacy-actors`, unmarked fields used to be transient and are now persistent. Mark every field that should reset on upgrade `transient`; a field whose type cannot be persisted (a function, an object with methods) is error M0131 until you do. A field that turns from transient to persistent needs no migration: on the first upgrade it is new to the stable signature, so its initializer runs once.

### `preupgrade` and `postupgrade`

They still work, with deprecation warning M0270. The usual reason for them is a structure that could not be persisted, such as `mo:base/HashMap`, copied into a stable array before an upgrade and rebuilt after it:

```motoko
// moc 1, in the actor body
var entries : [(Text, Nat)] = [];
transient let users = HashMap.HashMap<Text, Nat>(16, Text.equal, Text.hash);

system func preupgrade() { entries := Iter.toArray(users.entries()) };
system func postupgrade() {
  for ((k, v) in entries.vals()) { users.put(k, v) };
  entries := [];
};
```

The `mo:core` collections are stable, so declare `users` as an ordinary field, `let users : Map.Map<Text, Nat> = Map.empty();`, delete both hooks and `entries`, and move the data once with a migration function on the actor:

```motoko
// moc 2
import Map "mo:core/Map";
import Text "mo:core/Text";

(with migration = func(old : { var entries : [(Text, Nat)] }) : { users : Map.Map<Text, Nat> } {
  { users = Map.fromIter(old.entries.values()) } // `compare` is implicit, from the imported Text
})
actor { /* ... */ };
```

The upgrade that installs this version still runs the old `preupgrade`, so `entries` holds the data when the migration reads it. Warning M0207 on the dropped field is expected. Delete the `(with migration = ...)` clause once this version is deployed. With an enhanced migration chain (`--enhanced-migration`), declare the field without an initializer, `let users : Map.Map<Text, Nat>;`, and put the same function in the next chain file as `public func migration` instead.

## Syntax that no longer parses

### `??` needs spaces, and its right-hand side is an expression

```motoko
let n = o ??0;                          // moc 2: syntax error
let n = o ?? 0;                         // both
let n = o ?? do { let k = f(); k + 1 }; // a block needs `do` (M0273 without it)
let r = o ?? ({ x = 1 });               // a record literal; parentheses work in both
```

### Branches glued to the condition

A `(`, `[` or prefix operator directly after a condition now continues the condition, so a bare branch needs a space before it. A condition that is more than a name or a parenthesized expression needs braced branches (M0275):

```motoko
if (c)-1 else 1;           // moc 2: `(c)-1` is the condition — M0275
if (c) -1 else 1;          // branch `-1`
if (f(x)) a else b;        // both
if (f(x)) { a } else { b } // both, and never ambiguous
```

## Async function bodies

A function whose return type is `async T` has an asynchronous body whether it is written `{ ... }` or `= e`. Spelling the `async` out is now M0277, and the fix-it removes it:

```motoko
func f() : async Nat = async { 1 }; // M0277
func f() : async Nat { 1 };         // both
```

The same applies to `= ignore (async ...)` in a oneway `shared` function. Two moc 1 forms have no direct replacement: a parenthetical on the body (`= (with cycles = n) async { ... }`) moves to each call site, `(with cycles = n) f()`; and a local function can no longer return a future created by its enclosing function — await it there instead.

## Record update copies `var` fields

`{ base with ... }` on a record with `var` fields was error M0179 in moc 1, or aliased the base's fields under `--experimental-field-aliasing`. moc 2 copies them into new cells, like the equivalent record literal:

```motoko
let base = { var count = 0; name = "a" };
let copy = { base with name = "b" };
copy.count += 1; // base.count is still 0
```

Code that relied on aliasing compiles silently with different behavior. Keep the shared mutable state in one object that both records reference.

## Libraries, modules and primitives

- **Imported files must be modules (M0142).** Wrap a bare list of declarations in `module { ... }` and mark the exports `public`.
- **Actor classes return `async` (M0193):** `actor class C() : async actor { ... }`.
- **`mo:base/ExperimentalStableMemory` no longer type-checks.** Use `Region` (`mo:core/Region` or `mo:base/Region`). The rest of `base` still compiles; new code should use `core`.
- **`Prim.createActor` is gone.** Use actor classes, or the management canister's `create_canister` and `install_code`.
- **Canisters no longer export `__motoko_stable_var_info`**, a query that always trapped under EOP.
- **Implicit arguments and dot notation also search nested modules**, so importing a facade that re-exports its package's modules is enough. Every call that resolved in moc 1 resolves the same way; a call moc 1 rejected may now resolve, or be ambiguous (M0224, M0231).

## Tooling

- **`moc --check a.mo b.mo` checks each file on its own**, seeing only its own imports. `-c`, `--idl` and `-r` take exactly one main file, and the REPL (`-i`) preloads at most one. Split programs with imports.
- **`-g`** emits only the DWARF line table.
- **`moc.js`:** `Motoko.run` takes `[]` as its first argument (use imports instead of preloads), and `gcFlags` accepts only `"force"` and `"scheduling"`.
- **No Intel-Mac binary.** On an x86_64 Mac, build moc from source, use `moc.js`, or stay on moc 1. The `motoko-base-library.tar.gz` artifact is gone too; get `base` from mops.
- **`mops bench`** cannot use `--legacy-persistence` or a non-incremental `--gc` under moc 2.

## Code that must compile with both moc 1 and moc 2

A library, or a codebase built by both majors during a transition, has to stay in the syntax both accept. Write moc 1 code with these rules and moc 2 compiles it with at most the warnings above:

- Fix every warning moc 2 turns into an error (the [diagnostics table](#diagnostics)) — moc 1 only warns, so a clean moc 1 build is the bar.
- Parenthesize `if`, `while`, `for` and `switch` heads: `if (c)`, `for (x in xs.values())`, `switch (e)`.
- Write case patterns in parentheses and end every case with `;`: `case (#tag(p)) { ... };`. Always parenthesize a variant payload.
- Put a space between a parenthesized condition and a bare branch, or brace the branches.
- Space both sides of `??`; write a block on its right as `do { ... }` and a record literal as `({ ... })`.
- Annotate a function passed where an `async` function is expected: `func(n : Nat) : async Nat { ... }`. moc 1 cannot infer it.
- Write a function body as a block, never `= async { ... }`.
- Never write `{ base with ... }` when `base` has `var` fields: moc 1 rejects it, moc 2 copies them.
- Never write `flexible` or `stable`.
- The read-only primitives listed above warn either way: moc 1 asks for `<system>` (M0195) and moc 2 calls it unneeded (M0196). The `mo:core` wrappers, such as `Runtime.envVar<system>(name)`, compile cleanly on both.
- For actor persistence, either build with `--default-persistent-actors` on moc 1 only and write a bare `actor`, or write `persistent actor` and allow M0217 on moc 2 (`-A M0217`).

## After the switch

Once no moc 1 build remains, these moc 2 forms are available. All are optional.

- Delete `persistent` and `stable` (M0217, M0218) — `mops check --fix` does it. The stable signature does not change.
- Heads without parentheses: `if f(x) { a } else { b }`, `while n > 0 { n -= 1 }`, `for x in xs.values() { ... }`, `switch p.x { ... }`. The branches or body must then be blocks.
- Lighter `switch` cases: the `;` between cases is optional, and a pattern with a fixed extent needs no parentheses — `case null`, `case -1`, `case ?v`, `case #tag(p)`, combined with `or`, `and` and `: T`. A variant payload keeps its own parentheses: `case #tag(p)`, never `case #tag p`.
- A function passed where an `async` function type is expected takes its parameter and return types from it: `run(func(n) { n + 1 })`.
- `do { ... }` works as an operator operand: `1 + do { ... }`, `debug_show do { ... }`.
