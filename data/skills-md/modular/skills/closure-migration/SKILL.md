---
name: closure-migration
description: >-
  Migrates Mojo code off legacy parametric closures (`capturing[_]`,
  `@__parameter` / `@parameter`, `api[fn](args)`) onto value-taking unified
  closures (`api(args, fn)` with `{imm}` / `{mut}` / `{var}` / named capture
  lists). Use when removing parametric overloads, fixing "capturing thin"
  conversion errors, rewriting nested launch/callback closures, or migrating
  any API that took a comptime function parameter. Also use when CI SIGSEGVs
  while compiling a Mojo object with `compile_offload_closure func must be
  fully bound` — that is host elaboration; verify with `kgen -elaborate`,
  not remote GPU execution.
---

# Closure migration

Migrate callers **before** deleting parametric overloads. Prefer value-taking
APIs with unified closures. Pair with `mojo-syntax` (and
`mojo-gpu-fundamentals` for GPU launch code).

## Forbidden

**Hard ban — do not under any circumstance** add `@__parameter` / `@parameter`
to a nested closure to persist, introduce, or paper over a legacy closure.
Not as a migration bridge, not to satisfy a still-capturing API, not to
“borrow imm”, not behind a thin `*_value` wrapper. That is forbidden.

**Hard ban — do not under any circumstance** add a new caller of a
**capturing** parametric endpoint (`func: def(...) capturing [_] -> None`
or `capturing` without `thin`), or restore a deleted capturing overload,
to paper over a typecheck or bind failure. Look at the callee parameter
type: `thin` is a function pointer and is fine (`add_function[vec_add]`,
`compile_function[kernel]()`). `capturing` and not `thin` is the legacy
closure. Do not route a unified-closure site back through `capturing[_]`.

**Hard ban — do not write an empty capture list `{}`.** If the nested def
has no free runtime captures, omit the list: `def foo() -> Int:` not
`def foo() {} -> Int:` and not `raises {}`. `{}` is not a spelling of
“no captures”; it is noise that reviewers will flag. `{imm}` is
capture-all of outer state, not a stand-in for an empty list.

| Do not | Do instead |
|--------|------------|
| `@__parameter` / `@parameter` on nested defs | Unified `def … {imm}:` / `{mut x, imm}:` / named captures |
| `@__parameter` body + `*_value` forwarder | Make the body unified; pass it as a value |
| `@__parameter` “imm borrow” helper | File-scope / normal function with an imm parameter |
| `@__copy_capture(x, y)` dropped for `{imm}` | `{var x, var y, imm}` (copy each listed name). `{var}` capture-all only if every capture was copy-captured. `{var^}` / `{var^ x}` is a **move**, not a copy |
| Keep `@__parameter` because an API is still `capturing[_]` / comptime `fn` | Migrate or widen that API to value-taking; do not paper over it |
| Wrap a `MutUntrackedOrigin` / `MutAnyOrigin` ptr in a new `DeviceBuffer` so memset or a launch “doesn’t alias” | Pass the original `DeviceBuffer` as an imm argument (`enqueue_memset` takes imm) |
| Hoist `comptime if` arm buffers / `TileTensor`s to function scope (size-1 placeholders on other arms) | Keep them in the arm; define the unified closure next to those locals |
| Rebuild `a_shape` / layouts inside the timed `call_fn` | Build once in the helper body; `{imm}`-capture |
| New `api[fn](args)` where the callee param is `capturing` and not `thin` | Keep value-taking unified closures. `thin` function-pointer `api[fn]` is OK |
| Empty `{}` (`def f() {} -> T` / `raises {}`) | Omit the capture list. `{imm}` only when you mean to capture outer state |

If a callee still only accepts a comptime `capturing[_]` function parameter
**and that overload is not being deleted in this change**, use a nested
`def … capturing -> T` **without** `@__parameter` when that is what the type
requires, or migrate that API. Leave an *existing* capturing `api[fn]` site
you have not rewritten; do not add new capturing ones. `thin` function-pointer
parameters are not that case. Never put `@__parameter` on the caller.

`@__copy_capture` copies into closure storage. Transfer it; do not drop it
for `{imm}`:

```mojo
# WRONG — copy-capture became an imm borrow
@__copy_capture(gamma, epsilon, input_fn)
def bench_fn(mut b: Bencher) raises:
    ...
# became
def bench_fn(mut b: Bencher) raises {imm}:

# CORRECT — each listed name is a named copy; trailing imm for the rest
def bench_fn(mut b: Bencher) raises {var gamma, var epsilon, var input_fn, imm}:
```

| Decorator / intent | Capture |
|--------------------|---------|
| `@__copy_capture(x, y)` | `{var x, var y, …}` (copy) |
| Every capture was copy-captured | `{var}` capture-all is OK |
| Move into storage (consume) | `{var^ x}` / `{var^}` — **not** the copy-capture mapping |
| Comptime parameter in the old list | Omit it (`value X is a parameter and does not need a capture convention`) |

Put the `{var …}` list on the **same def** that had `@__copy_capture`. Nested
children that already used `{imm}` then borrow those copies. If you hoist
`kernel_launch` out of `bench_fn`, the `{var …}` list moves with the names
onto the launch — do not hoist and leave `{imm}` on either def.

`{var x}` does **not** convert to a `capturing thin` callee such as
`elementwise_compute_lambda_type`, and a capture list is not parsed on a
`capturing` def. Until that API is migrated off `capturing`, form the
`LayoutTensor` on the host from an imm `residual_buf` parameter and keep
`@__copy_capture(residual_lt)` on `def … capturing` (no `@__parameter`).
Never call `DeviceBuffer` methods inside the GPU epilogue.

## Target shapes

| Legacy | Preferred |
|--------|-----------|
| `api[fn](a, b)` | `api(a, fn, b)` |
| Comptime param `fn: def(...) raises capturing[_] -> None` | `FuncType: def(...) raises -> None` + runtime `ref func: FuncType` (or `func: FuncType`) |
| Nested `@__parameter` / `@parameter` def | Unified `def ...(…) raises {imm}:` / `{mut buf, imm}:` / named captures |

`@__parameter` nested defs type as `capturing thin` and do **not** convert to
a unified `FuncType`. Call rewrite alone is not enough — change how the
closure is declared (and never re-add `@__parameter`).

## Checklist

1. Inventory: `rg 'api_name\[' --glob '*.mojo'` and `rg '@__parameter|@parameter' --glob '*.mojo'`
2. Rewrite calls: `api[fn](a, b)` → `api(a, fn, b)`
3. On every nested closure in scope: drop `@__parameter` / `@parameter` /
   `@__copy_capture`; add a capture list. Each `@__copy_capture(x)` name
   **must** become `{var x}` (or `{var}` capture-all if that was every
   capture). Do not replace the decorator with `{imm}`. Skip comptime
   params. Self-check the pre-image: every runtime name in
   `@__copy_capture(...)` appears as `var name` in the new list.
4. If a callee still needs a comptime **capturing** param **and that overload
   is not being deleted** → migrate that API first, or leave an existing
   capturing `api[fn]` site you have not rewritten. **Do not** add new
   capturing `api[fn]` callers or keep `@__parameter` on the caller. `thin`
   function-pointer parameters (`add_function[vec_add]`,
   `compile_function[kernel]()`) are not that case.
5. Delete parametric overloads only after callers typecheck
6. Update skills/docs that still teach the legacy path
7. Typecheck: `mojo build --emit llvm <file> -o /tmp/x.ll` (filters Metal noise)
8. Offload bind: if the change passes a kernel into `DeviceFunction` /
   `add_function` / `compile_info`, run `kgen -elaborate` (below). Do not
   `bt-b200` a compile-time bind assert.
9. Self-check: `rg '@__parameter|@parameter' --glob '<touched>.mojo'` → zero on
   nested closures you own
10. NFC self-check: allocation sites, comptime vs `Coord(IndexList)` layouts, and
    timed `call_fn` bodies match the pre-migration code except capture lists and
    `api[fn](…)` → `api(…, fn, …)`. No new `.as_unsafe_any_origin()` /
    `unsafe_origin_cast` / `DeviceBuffer(…, some.ptr, owning=False)` used to
    dodge aliasing

## Verify compile_offload bind without a GPU

`compile_offload_closure func must be fully bound` is an elaborator assert
in `Mojo/lib/Elaborator/IREvaluatorContext.cpp` (`evaluateCompileOffloadClosureAttr`).
It fires while folding `#kgen.compile_offload_closure` on
`CompiledFunctionInfo.populate` — the comptime field `DeviceFunction` and
`compile_info` instantiate. Offload codegen has not started. A CI SIGSEGV
during `compiling mojo object` with that message is a host bind failure, not
a GPU or PTX failure.

Do not `bt-b200` / `bt-mi355` it. Elaboration is host-only.

```bash
source ./utils/start-modular.sh
# Matching compiler: bazel-run kgen, not a stale PATH kgen vs std.mojoc
./bazelw run //Mojo/tools/kgen -- -elaborate path/to/file.mojo -o /dev/null
```

In-tree precedent: `kgen -elaborate` in
`KGEN/test/mojo-integration/compile_offload/internal/compile_different_emissionoptions_same_gpu.mojo`.

If PATH `kgen` errors with `Mojo precompiled file is incompatible with the
current version of the Mojo compiler`, the binary is stale relative to
`.derived` packages. Use bazel-run (or `./bazelw run //:install`), not a GPU
box.

NVIDIA offload on a Metal/CPU host: pin `target=` on `compile_info` /
`DeviceFunction` (`A100.target()`, `B200`, …), or `mojo build
--target-accelerator=nvidia:sm_100a` (see
`compile_offload_gpu_cross_compilation.mojo`). `kgen` has no
`--target-accelerator`; that flag is `mojo build`.

Elaborate the crashing file, or a reduced file that instantiates the same
`DeviceFunction[F.__call__, …]` / `CompiledFunctionInfo` type. A bound
non-generic kernel (`Kernels.vec_add`) is not a substitute for the
specialization that failed.

A file-scope `@no_inline` wrapper that binds leftover **kernel** comptime
parameters fixes `DeviceFunction[func, declared_arg_types]` when `func` is
that wrapper (`compile_function[kernel]()` / `add_function[kernel]`).
It does **not** bind `DeviceFunction[F.__call__, TypeList.of[T0,…]()]`.
`F.__call__` is `_PtrWrapper::__call__[AnyType, …]` even when the runtime
value is already a fully specialized thin kernel. For a thin kernel, use
the thin endpoint (`add_function[kernel](*args)` /
`compile_function[kernel]()`). `DeviceGraphBuilder.add_function` is
thin-only; capturing kernels use `enqueue_function` /
`recording_context()`. Do not paper a capturing site over with
`capturing[_]` / `@__parameter`.

## Capture choice

| Default / symptom | Choice |
|-------------------|--------|
| Read-only use of outer state | `{imm}` (capture-all) — **not** if the body calls `offset_ptr` or builds a mut `TileTensor` (see freeze note below) |
| Mutates some outer state; also reads `Int` / other register-passable values | `{mut buf, imm}` — **not** capture-all `{mut}` |
| Mutates several outer names | `{mut a, mut b, imm}` |
| Replacing `@__copy_capture(x, y)` | `{var x, var y, imm}` (copy). `{var}` only if every capture should be a copy. `{var^}` is a move — not this mapping. **Never** `{imm}` |
| Named precision only | `{mut count}`, `{imm buf, imm shape}` — `{imm}` captures names the body uses, not every local in scope |
| No free runtime captures | Omit the capture list. **Never** `{}` |
| `Could not infer capture convention` | Add `{imm}` / `{mut name, imm}` / named list |
| `expression must be mutable in assignment` on a capture | That name needs `mut` (or declare temporary view arrays locally inside the closure if rebuilt per iteration) |
| `register passible value … can not be captured by 'mut'` | Capture-all `{mut}` pulled in an `Int` (etc.) — use `{mut buf, imm}` |
| `.mut … is 'False' but … is 'True'` on `.unsafe_ptr()` / `TileTensor` | Buffer captured `{imm}` — `{mut out_buf, imm}`; do **not** paper over with `unsafe_mut_cast` |
| `'lit.call' op callee expected call argument #0` on `offset_ptr` / similar | `{imm}` froze the buffer used as `self` — `{mut cb_a, mut cb_b, …, imm}` |
| `cannot bind an RValue to a reference` on `bench_func` | `kernel_launch` nested inside `bench_func` with `@__copy_capture` — hoist `kernel_launch` to outer scope and put `{var x, var y, …}` on it for every copy-captured name. Do not hoist and write `{imm}` |
| `expected ':' in function definition` at `raises {…}` | Capture list on an `@__parameter` def — strip `@__parameter` and keep the list |
| `aliasing values passed immutably…mutably` / note names `origin_of(buf)` | Closure struct would hold fields that alias the same origin, one mut and one imm — see **Aliasing** below |
| `aliasing … origin_of(n)` on an `Int` (or other register-passable) local | `@__copy_capture(n)` became an imm ref to `var n`. Use `{var n}` (copy). Do not delete `n` and rewire to another `Int` unless that is smaller |
| `aliasing values passed mutably to 'x' … and passed mutably to 'y'` | Two mut captures of the same origin (view + backing buffer, or a value plus a nested helper that also captures it) — see **Aliasing** below |
| `cannot bind an RValue to a reference` on `bencher_iter_custom` value call | Value-taking `bencher_iter_custom` declared with `ref func: FuncType` rejecting temporary/lifted closure value — take `func: FuncType` by value |
| `'lit.call' op invalid symbol use` / `origin<false>` vs `origin<true>` on `bench_function[fn]` | `@__parameter` capturing-thin `bench_fn` captured unified `{imm}` children — drop `@__parameter`; `bench_function(fn, id, …)` value-taking |
| `two_launch` in `_dispatch_ag_norm` / `capturing` params | If an outer API still accepts a comptime `capturing` function parameter, write `def two_launch() raises capturing:` without `@__parameter` or capture lists |
| `cannot capture … not copyable` / not a parameter reference | `{imm}` if possible; else `{var}` / named `var x`; never `@__parameter` |
| Memset / launch aliases with a wrapper whose ptr is already `MutUntrackedOrigin` | Pass the original `DeviceBuffer` as an imm argument. Do **not** wrap the untracked ptr |

Do **not** use capture-all `{mut}` when the closure also mentions register-passable
outer values (`Int`, indices, lengths). Mix an explicit `mut` name with a
trailing default `imm` (`{mut tt_in, imm}`). At most one bare convention
(`imm` / `mut` / `var`) may appear as the default for unlisted captures.

`{imm}` **freezes** captured buffers. That is wrong whenever the body:

- writes an output (`TileTensor` / `.unsafe_ptr()` where `mut=True` is required), or
- calls a method that internally does `self._buf.unsafe_ptr()` then
  `unsafe_mut_cast[True]()` — `CacheBustingBuffer.offset_ptr` is the usual
  case. The method may be declared `self` (imm); the captured field still
  fails to match (`lit.call` argument #0). Mut-capture every such buffer
  (`{mut cb_a, mut cb_b, mut cb_c, mut cb_a_scales, mut cb_b_scales, imm}`).

Do **not** “fix” this with extra `unsafe_mut_cast` (the method already has
that) or by restoring `@__parameter`. Only skip `mut` when that would create
an aliasing pair with another captured field of the same origin (see below).

### Aliasing

When several captured / nested values reference the **same origin** and one of
them is mutable, the closure struct would contain aliasing fields. Two captures
that alias the same memory are permitted only when **both are read-only**.

`@__copy_capture(n)` on a register-passable local (`Int` index, length, row
count) becomes `{var n}` — a copy into closure storage. `{imm}` of
`var n = …` is a reference to that mutable local and aliases once a unified
sibling embeds `origin_of(n)`. Use `{var n}`. Do not delete `n` or wrap the
function just for that integer.

Prefer, in order:

1. **Capture as read (`imm`)** whenever the body does not actually mutate that
   origin. Drop `{mut …}`; pass an imm parameter. `enqueue_memset` takes an
   imm `DeviceBuffer`. A helper that only reads `config.rank_units` must not
   mut-capture `config`. Prefer this also when an outer `var buf` stays
   mutable while a nested unified closure would capture a view of `buf`: call a
   **normal function** (file-scope or otherwise non-capturing) that takes
   `buf: DeviceBuffer[…]` as an imm parameter, and form the launch there.
2. **Disassemble the instance** so origin tags are finer-grained. If the
   compiler treats two uses as overlapping because they capture a whole object
   (a `config`, a struct, a `List` of buffers) but the mutation does not
   actually touch the other use's memory, pull out the fields you need (e.g.
   hoist `rank_units` / `rank_unit_start` into `Array[Int, ngpus]`) and capture
   or pass those instead of the parent.
3. **Pass the mutable origin as an argument** (`mut buf: …` in the parameter
   list) so it is not a captured field. Lift **only** the capture that must
   be mut and still aliases another use — read-only captures can stay
   captures. When the value-taking API's `FuncType` is fixed, use a thin
   `{mut buf, imm}` adapter that only forwards `buf` into the all-imm body.
   Prefer widening the API when practical.

Do **not** “fix” aliasing by erasing the origin. That includes
`.as_unsafe_any_origin()`, `unsafe_origin_cast[MutUntrackedOrigin]` /
`MutAnyOrigin` on the original buffer, and wrapping an already-untracked
pointer (`EPLocalSyncCounters.ptr`, `offset_ptr` result) in a new
`DeviceBuffer(ctx, ptr, …, owning=False)` just to memset or launch. Pass the
original buffer as an argument instead.
Do **not** “fix” anything with `@__parameter`.

## Safety rules

- Key bulk edits off the **value-argument name**, not every def with that name
- Do not bulk-replace capture lists (destroys `{mut count}` etc.)
- `name[i] =` inside `with … as name` is a local, not an outer `mut` capture
- Zero `@__parameter` / `@parameter` on nested closures in migrated code
- Lift a capture to an argument **only** for origin exclusivity (or a
  normal function with an imm `DeviceBuffer` parameter)
- Stay NFC: do not change allocation lifetime, comptime vs dynamic layouts, or
  host work on the timed path. `comptime if` arm locals (buffers, host copies,
  `TileTensor`s, `row_major[M, N]()` layouts) stay in that arm — a size-1 alloc
  at function scope is a semantic change. Layouts built once (`a_shape`) stay
  outside `call_fn`

## More detail

Full step-by-step process, error catalog, and verification:
[process.md](process.md).
