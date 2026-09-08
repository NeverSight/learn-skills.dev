---
name: reviewing-motoko
description: "Design review for existing Motoko backends — judging whether code is well designed, not how to write it. Covers invariants encoded in types (variants over Text, correlated fields, case _ smells), stable vs transient state discipline under enhanced migration, file structure (types.mo/lib/mixins/main.mo), and severity-ranked findings (Blocker/Warning/Note). Use when reviewing, auditing, critiquing, or refactoring existing .mo files, or when asked for code-review feedback on a Motoko canister. Do NOT use for writing new Motoko code or fixing compiler errors (writing-motoko), authoring migration files (migrating-motoko-actors), or deployment."
license: Apache-2.0
compatibility: "moc >= 1.11.2, core >= 2.6.0, mops >= 3.0.0"
metadata:
  title: Reviewing Motoko
  category: Motoko
---

# Reviewing Motoko

This skill judges whether Motoko code is **well designed**. It does not teach the language — load `writing-motoko` for syntax, `mo:core` APIs, and mechanical rules, and `migrating-motoko-actors` before changing anything that is stable state.

Four questions decide a review, in this order — the first three because each can invalidate the next, the fourth last because it is the least consequential:

1. **Is every invariant the code relies on encoded in a type?** Where the type system *can* rule out a bad state, leaving that to a runtime check or a comment is a defect, not a style preference.
2. **Is state declared with the right persistence?** Under enhanced migration, stable and transient are separate worlds. Blurring them produces state that silently stops updating.
3. **Does the code live in the right files?** `types.mo` / `lib/` / `mixins/` / `main.mo` is a contract about what may depend on what, not a folder convention.
4. **Does it read like Motoko?** Contextual dot notation, inferred implicits, no annotation the call already supplies, no classes. `mops check --fix` handles most of this; only what it cannot see is the reviewer's job.

## Procedure

**Run the mechanical pass first** — do not spend review attention on what the compiler already reports.

```bash
mops check --fix
```

Its style auto-fixes (M0236 dot notation, M0237 redundant implicits, M0223 redundant instantiation) only fire where `[moc] args` enables `-W` for them; `writing-motoko`'s `references/project-setup.md` has the setup. Where they are off, the **Conventions** findings below are all yours to make by hand.

Then read in this order — outside in, because a misplaced file makes every type inside it suspect:

1. `mops.toml` — is there a `[canisters.*.migrations]` chain? If not, finding **B1** below outranks everything else.
2. **Structure** — the file layout, then each file's imports.
3. `types.mo` — every type declaration. This is where most findings are.
4. **State** — the actor fields in `main.mo`, and what each `include` passes. See [references/state-and-persistence.md](references/state-and-persistence.md).
5. **The API boundary** — every `public shared` / `public query` function: its parameter types, its return type, its authorization.
6. **Bodies** — last, and only for the smells under **Maintainability** below.

## Severity

Report findings with one of three levels. Do not inflate: a reviewer who calls everything a blocker gets ignored.

| Level        | Meaning                                                                                 |
| ------------ | --------------------------------------------------------------------------------------- |
| **Blocker**  | Can corrupt or silently lose state, or lets a caller reach an unauthorized action.       |
| **Warning**  | An invariant the type system could enforce is left to runtime, a comment, or a convention. |
| **Note**     | Readability, duplication, or naming. Fix while you are in the file; do not gate on it.   |

State the concrete failure, not the rule. "`status : Text` accepts `"complete"`, and the three call sites spell it `"completed"`" beats "prefer variants over strings".

## Type encoding

The rule: **if a value has a fixed set of shapes, the type must have that set of shapes.** Full recipes, including how to carry each change through a migration, are in [references/type-encoding.md](references/type-encoding.md).

### T1. `Text` for a closed set of values — **Warning**, **Blocker** if it gates authorization

The most common defect in generated Motoko. Every producer and consumer agrees on spelling by convention and the compiler checks nothing — no exhaustiveness, no error on a typo, no error when a new state is added and half the call sites are not updated.

```motoko
public type Task = { id : Nat; var status : Text };           // WRONG
public type TaskStatus = { #open; #claimed : Principal; #done : { at : Time.Time } };
```

Variants are shared, so this reaches the frontend as a discriminated union too. **Flag `Text` (or `Nat`, or `Bool`) whenever the code, a comment, or a doc lists the permitted values** — `== "..."` comparisons, a `switch` on a `Text` with a `case _`, role names held as `Text`. Keep `Text` for genuinely open sets, and for strings an external system owns.

### T2. Correlated fields — **Warning**

Two fields that are only valid together belong in one variant. A `Bool` plus an optional payload has four representable combinations and two meaningful ones.

```motoko
// WRONG — { hasDeadline = true; deadline = null } compiles and means nothing
{ hasDeadline : Bool; deadline : ?Time.Time }

// RIGHT
{ deadline : { #none; #due : Time.Time } }   // or simply `deadline : ?Time.Time`
```

If a `?T` already says it, drop the `Bool` — do not introduce a variant that only restates `?T`.

### T3. Wrong cardinality — **Note**, **Warning** when callers loop defensively

Use the type that matches the real count. A `[T]` that is always empty-or-one makes every caller write a loop or an `if size == 1`; a `?T` tells them there is nothing to iterate.

### T4. Errors as `Text` — **Warning**

`Result<Ok, Text>` forces every caller to string-match to tell one failure from another. Make `Err` a variant with the data each case needs. See the `Result` section of `writing-motoko` for the full rule, including when to return `?T` and when to trap instead.

### T5. `var` fields leaking into the API — **Blocker** (it does not compile) or **Warning** (it compiles but over-shares)

A record with a `var` field is not shared, so it cannot be returned from a public function. Where a project already has the internal/view split (`Task` internal, `TaskView` shared), check that:

- no public signature mentions the internal type;
- the view is **narrower** than the internal record, not a mechanical field-for-field copy. A view that re-exports an internal `Principal` list, an audit trail, or another user's data is an information leak that compiles.

### T6. `case _` swallowing variants — **Warning**

A catch-all arm is what turns "adding a variant tag is a compile error everywhere it matters" into "adding a variant tag silently takes the default branch". Keep `case _` only where the arms are genuinely uniform and the set is expected to grow (e.g. mapping many tags to one label). Anywhere a new tag would need new behaviour, enumerate the tags.

### T7. Transparent aliases sold as safety — **Note**

`type UserId = Principal` is a documentation alias: any `Principal` still type-checks where a `UserId` is expected. That is fine, and usually the right trade. Just do not treat it as an enforced distinction — and if two different id types are genuinely being confused at call sites, a one-field record (`{ userId : Principal }`) or a variant tag (`#user(Principal)`) is what actually enforces it, at the cost of changing the Candid shape.

## State and persistence

Under enhanced migration (EM) the actor's stable fields are declared **type-only** and every initial value comes from the migration chain. That separation is the point: it is what makes stable state impossible to initialize from something transient. Details in [references/state-and-persistence.md](references/state-and-persistence.md).

### B1. No enhanced migration — **Blocker**

No `[canisters.<name>.migrations]` chain in `mops.toml` means pre-EM persistence, where stable fields carry inline initializers — so a stable field can be initialized from a transient one:

```motoko
transient let defaultQuota = 100;
let quota = defaultQuota;   // stable; the initializer runs ONCE, on first install
```

Change `defaultQuota` to `250`, deploy, and `quota` is still `100` — forever, no warning. Point at `migrating-motoko-actors` for the conversion; everything below assumes EM.

### S1. Inline initializer on a stable field — **Blocker**

Under EM this is M0250 / M0014, so it will not compile — but it appears constantly in code copied from pre-EM examples and in half-finished refactors. The fix is never to add `transient`: move the initial value into the pending migration's `NewActor`.

### S2. `transient` misused — **Warning** both ways

Ask of every actor and mixin field: *if this is lost on upgrade, is the app still correct?*

- **Missing `transient`**: caches, derived indexes, rate-limit counters, and anything rebuildable are being persisted. They then have to be migrated forever, and a stale cache survives the upgrade that was supposed to clear it.
- **Wrongly `transient`**: durable domain data silently resets to its initializer on every upgrade. Look for `transient` on anything a user would expect to still be there after a deploy.

### S3. `var` actor field shared with a mixin — **Blocker**

`var` parameters pass by value, so the mixin mutates a copy and the actor's field never changes. Wrap it in a record and pass the record. Also flag a fresh record literal at the `include` site (`include Api({ var n = state.n })`) — each mixin then gets its own copy. See `writing-motoko`.

### S4. Stable state inside a `mixin` block — **Blocker**

Every bare `let`/`var` at the top of a `mixin` is implicitly stable and traps at runtime with `IC0503`. State comes in as a parameter; constants go in a module; only `transient` is allowed inline.

### S5. Migration hygiene — **Blocker**

- A migration file importing anything other than `mo:core/...` — the chain replays forever, so a project import makes it wrong the moment that type changes. (`caffeineai-lints` catches this.)
- More than one pending migration in a build, or an edit to a migration that predates this build.
- A stable field in `main.mo` that no migration in the chain supplies (M0254 / M0267).

An identity migration body is a **Warning** — the change was stable-compatible, so delete the file. [Full table](references/state-and-persistence.md#migration-hygiene).

## Structure

Layers, with dependencies pointing one way only: `main.mo` → `mixins/` → `lib/` → `types.mo`.

| File            | Holds                                                 | Must not hold                          |
| --------------- | ----------------------------------------------------- | -------------------------------------- |
| `types.mo`      | Type declarations; small pure helpers on those types  | State, endpoints, business rules       |
| `lib/*.mo`      | Domain logic as stateless modules, state as parameters | Public endpoints, actor fields         |
| `mixins/*.mo`   | Public endpoints: authorize, delegate, map to a view  | Domain logic, stable state             |
| `main.mo`       | State declarations and `include`s                     | **Any public method**, any logic       |
| `migrations/`   | The frozen chain, one module per file                 | Project imports                        |

- **A1 — Blocker/Warning:** a public method in `main.mo`. Move it to a mixin.
- **A2 — Warning:** a monolithic file. One `.mo` holding types, state, logic, and endpoints together.
- **A3 — Warning:** domain logic in a mixin body. If an endpoint's body is more than authorize → delegate → map, the middle belongs in `lib/`.
- **A4 — Warning:** wrong dependency direction — `lib/` importing a mixin, or `types.mo` importing either.
- **A5 — Note:** a mixin that is not a feature. Mixins split by *feature* (`mixins/Bookings.mo`), not by verb (`mixins/Getters.mo`).
- **A6 — Warning:** over-broad state injection. A mixin receiving state it never touches widens what a change can break; pass only the slices it uses.

## Maintainability

Most of this is caught in the last, bodies pass. The exception is **M1**, the authorization blocker — it is found during the API-boundary pass (step 5), not with the body smells below.

- **M1 — Blocker:** a `public shared` function that does not check `caller`. Every state change and every read of another user's data needs authorization on the backend.
- **M2 — Warning:** `Nat` subtraction that is not provably non-negative at the operation. It traps.
- **M3 — Warning:** a trap where the caller could have recovered. Traps roll back the message and reach the client as an opaque reject; caller-fixable failures belong in a `Result` error variant.
- **M4 — Note:** duplicated internal→view mapping. One `toView` per type, in `lib/` or `types.mo`.
- **M5 — Note:** magic values — bare literals for limits, quotas, or durations. Name them in a module.
- **M6 — Note:** a comment asserting an invariant the type could carry. Every "must be non-empty" / "only set when …" comment is a type-encoding finding in disguise. Where Motoko cannot express the invariant, keep the comment but validate the value once at the boundary rather than re-checking it at every use.

## Conventions

Least consequential of the four axes, and `mops check --fix` fixes most of it where the `-W` flags are on — so raise these only after the passes above, and only where the tooling cannot. `writing-motoko` has the rules; this is what to look for.

- **C1 — Note:** a module-function call where the function takes `self` — `List.add(list, x)`, `Principal.toText(p)`. M0236, auto-fixed.
- **C2 — Note:** an implicit passed explicitly (`map.add(Text.compare, k, v)`), or a type instantiation inference already resolved. M0237 / M0223, auto-fixed.
- **C3 — Warning:** type annotations on an inline `func` passed as a **call argument** — `xs.filter(func(x : Nat) : Bool { x > 1 })`. No diagnostic catches this, so it is the reviewer's job: the call already fixes both types, and the annotation duplicates them so they can drift. Write `xs.filter(func x = x > 1)`. Instantiate the *call* (`map<In, Out>`) when M0098 demands it — never the lambda. One exception: `: async ()` on an async callback is load-bearing.
- **C4 — Blocker:** a `class`, or any object holding functions, used as actor state. Functions are not stable, so it fails with M0131 (`declared stable but has non-stable type`). Outside state a class still is not the idiom here — a module taking `self` plus dot notation gets the same call sites and stays stable.

## Refactoring

Design fixes in Motoko are not free: **changing a type that is reachable from a stable actor field requires a migration**, and the chain is one-way. Before proposing a type change, establish whether that type is stable state.

1. `mops check --fix` first, so the mechanical noise is gone.
2. **Batch the stable-state type changes** — one pending migration per build, so they land together.
3. **Write the migration** (`migrating-motoko-actors`). For `Text` → variant, decide explicitly what an unrecognized string becomes rather than inventing an `#unknown` tag.
4. **Move code before changing it** — relocating, then editing, keeps each diff reviewable.
5. `mops check --fix` until clean, then `mops build` once.

## Reporting

Group findings by severity, blockers first. Per finding: `file:line`, the level, the concrete failure it permits, and the change. Suppress findings the compiler already reports.

```text
Blocker  src/backend/mixins/Tasks.mo:34  (M1)
  `claimTask` never reads `caller` — any principal can claim any task.

Warning  src/backend/types.mo:12  (T1)
  `Task.status : Text` is a closed set, so the comparison at Tasks.mo:51
  spells it "complete" and is never true. Stable state — needs a migration.
```

If nothing is wrong, say so plainly. Do not manufacture findings to fill a report.

## Additional References

- [references/type-encoding.md](references/type-encoding.md) — recipes per invariant, and the migration each one needs
- [references/state-and-persistence.md](references/state-and-persistence.md) — why EM matters, the stable/transient question, migration hygiene
- `writing-motoko` — language mechanics, `mo:core` APIs, `Result`, dot notation
- **mops tooling**: Load `mops-cli` for `mops.toml` configuration and `mops check`/`mops build` details
- `migrating-motoko-actors` — writing the migration a type change requires
- `troubleshooting-motoko-migrations` — compatibility diagnostics that do not match the source
