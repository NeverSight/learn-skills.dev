---
name: zig-best-practices
description: "Comprehensive Zig expertise covering allocators, comptime, error handling, build system, C interop, SIMD, volatile, atomic, align, and performance. Use when writing, reviewing, debugging, or refactoring Zig code. Triggers: Zig, .zig files, build.zig, build.zig.zon, zig test, zig build, allocators, comptime, SIMD, volatile, atomic, align, or any Zig-specific concept."
---

# Zig Best Practices

Helps you write, review, and improve idiomatic, safe, and performant Zig code. Adapt depth to the user's level — skip basics for advanced comptime questions, explain fundamentals for allocator newcomers.

## How to use this skill

Read **SKILL.md** for quick guidance, then consult 1-2 relevant reference files as needed.
**Do NOT load all references at once.**

### Reference files — when to read each one

| Reference | Read when... |
|-----------|-------------|
| `references/memory-management.md` | Allocators, alloc/free, defer/errdefer, arena patterns, init/deinit, FixedBufferAllocator, allocation failure testing, custom allocator wrappers. |
| `references/error-handling.md` | Error unions, try/catch, errdefer chains, specific error sets, error return traces, optional handling patterns. |
| `references/comptime-and-generics.md` | Comptime parameters, `@typeInfo`, generic structs, compile-time validation, lookup tables, state machines, `anytype`, fat pointer interfaces, type-level metaprogramming, event emitter pattern, typed `EventEmitter(comptime EventEnum, comptime PayloadMap)` with per-event payloads, callback storage with comptime dispatch. |
| `references/types-and-pointers.md` | Pointer types (`*T`, `[*]T`, `[]T`, sentinels), type casting (`@ptrCast`, `@alignCast`, `@bitCast`, `@intCast`), packed structs, zero-sized types, integer overflow, saturating arithmetic (`\|+`, `\|-`), type coercion, anonymous structs/tuples, custom formatting with comptime fmt, HashMap key types (`eql`/`hash`/`HashContext`), volatile/hardware MMIO, `std.atomic.Value`, alignment rules, **complete Color module example** (format + hash + lerp + saturating blend + tests). |
| `references/testing-and-build.md` | Inline tests, table-driven tests, `std.testing.allocator`, coverage, `build.zig`, `build.zig.zon`, dependencies, cross-compilation, WASM target (`.cpu_arch = .wasm32, .os_tag = .freestanding`), custom build steps, `b.addSystemCommand` with `addOutputFileArg` for code generation, `getEmitDocs` for documentation, **complete multi-target build.zig example** (CLI + WASM + cross-compile + codegen + docs + named steps), project structure, library setup. |
| `references/stdlib-recipes.md` | Data structures (ArrayList, HashMap, LinkedList), file I/O, string handling, networking (HTTP, TCP), concurrency (threads, mutex, thread pool). |
| `references/performance.md` | SIMD/`@Vector`, cache-friendly layout, benchmarking, buffered I/O, arena in hot paths, build modes, comptime lookup tables, stack vs heap. |
| `references/c-interop.md` | `@cImport`, `extern struct`, C pointers, string conversion, exporting Zig to C, sentinel termination for C APIs. |
| `references/code-review-checklist.md` | Reviewing Zig code, code review, PR review, common mistakes to check for, formatting/style rules, structured review methodology. |

## Mandatory workflows

### When writing code: completeness checklist

Before finalizing any code response, verify it includes **all** of the following that apply:

1. **Error set definition** — define specific error sets, never use `anyerror` in public APIs.
2. **Build boilerplate** — if a project is requested, include both `build.zig` AND `build.zig.zon`.
3. **init/deinit pair** — every struct that owns resources must have both.
4. **Trait implementations** — if a type will be used as a HashMap key, implement `eql()` and `hash()`. If it should be printable, implement `format()`.
5. **Doc comments** — all `pub` functions and types must have `///` doc comments.
6. **Inline tests** — include at minimum one test per public function using `std.testing.allocator`.
7. **Integer overflow safety** — any arithmetic on bounded integers (`u8`, `u16`, etc.) must use widening, saturating operators, or explicit overflow checks. State which approach and why.

### When reviewing code: structured analysis

Review code in three mandatory passes. Do NOT skip any pass.

**Pass 1 — Memory Safety:**
- Every `alloc` has a matching `free` via `defer`
- Every fallible path after allocation has `errdefer`
- No global mutable allocators — allocators passed as parameters
- No dangling pointers from slices into freed memory
- No reading from `undefined` memory without initialization first

**Pass 2 — Concurrency, Hardware, and Low-Level Safety:**
- Hardware register pointers use `volatile` (not regular pointers)
- Thread-shared state uses `std.atomic.Value` or `std.Thread.Mutex` (NOT volatile)
- `@ptrCast` is always paired with `@alignCast` — or use `std.mem.readInt` for unaligned access
- Structs for hardware/binary protocols use `extern struct` or `packed struct` for guaranteed layout
- Integer overflow operators (`+%`, `|+`) are used intentionally
- `undefined` buffers are not read before being written

**Pass 3 — API Design and Completeness:**
- `anyerror` replaced with specific error sets
- `var` replaced with `const` wherever mutation isn't needed
- File/network I/O uses buffered readers/writers
- Public API has doc comments
- Null/optional handling is safe (no unguarded `.?` unwrap)

### When doing arithmetic on bounded integers: overflow verification

Before finalizing code that does arithmetic on `u8`, `u16`, or any bounded integer type:

1. **Write the range** — what is the maximum value of each intermediate expression? (e.g., `u8 * u8` max = 65025, which overflows `u8` and `u16` alike — needs `u32`.)
2. **Widen before operating** — promote operands to a larger type (`u16`, `u32`) before multiplication or addition that could overflow, then truncate back with `@intCast`.
3. **Choose the right operator** — default `+`/`*` for bug-catching, `|+`/`|-` for clamping (audio, color), `+%`/`*%` for intentional wrapping (hashes).
4. **Never rely on implicit safety** — in `ReleaseFast` builds overflow is undefined behavior, not a panic.

### When writing comptime/pointer-heavy code: verification step

Before outputting complex comptime or low-level pointer code, mentally trace through:

1. Does every comptime block actually run at comptime? (No runtime variables in comptime context)
2. Are `@setEvalBranchQuota` calls needed for large iterations?
3. Do all pointer casts maintain alignment? (`@ptrCast` + `@alignCast` together)
4. Are packed struct fields accessed correctly? (Cannot take address of non-byte-aligned fields)
5. For `@typeInfo(.@"struct")` iteration: mentally substitute a concrete type and trace field access — does it handle all field types (`u8`, `u16`, `u32`, `u64`, `i8`–`i64`, `bool`, `[N]u8`)?
6. For serialization/deserialization: use `std.mem.readInt`/`std.mem.writeInt` with explicit endianness — never raw pointer casts for wire formats.

### Compile-check step for comptime type-safety

When writing generic comptime code (event emitters, serializers, type-safe builders):

1. **Draft the type signature first** — write `fn MyType(comptime Param: type, comptime mapFn: fn (Param) type) type` before the body.
2. **Verify callback/function pointer signatures** — ensure `*const fn (*const PayloadType) void` matches what callers pass. Never use `anytype` for stored callbacks.
3. **Check that `@ptrCast`/`@alignCast` round-trips are correct** — type-erased pointers (`*const anyopaque`) must be cast back to the original type with matching alignment.
4. **Simulate a call mentally** — pick a concrete enum variant, trace the comptime function resolution, verify the callback type matches.

### Constraint checklist against `anytype` misuse

Before using `anytype` in a function signature, verify:

- [ ] The function genuinely works with multiple unrelated types (not just one)
- [ ] You cannot express the constraint with a concrete type or comptime parameter
- [ ] Stored function pointers use concrete types, not `anytype` (you cannot store `anytype`)
- [ ] The doc comment documents what interface the `anytype` parameter must satisfy

### When responding to multi-requirement prompts: requirement verification

When the prompt lists multiple requirements (numbered or bulleted), verify completeness before finalizing:

1. **Label each requirement** — mentally map each prompt requirement to a specific section of your code.
2. **Check for missing requirements** — scan the prompt again after writing code. Each requirement must have corresponding code.
3. **Verify test coverage** — each requirement should have at least one test exercising it.
4. **For complete module requests** — output a single, self-contained module (not scattered fragments). Include all imports, the type definition, all methods, and all tests in one code block.

## Quick principles

1. **Default to `const`.** Only use `var` when you genuinely need mutation.
2. **Pair every allocation with deallocation via `defer`.** Use `errdefer` for cleanup that should only run on error paths.
3. **Pass allocators as explicit parameters.** Functions that allocate accept an `Allocator` — no globals, no hidden heap.
4. **Errors are values.** Use specific error sets, propagate with `try`, handle with `catch`. Never silently discard errors without good reason.
5. **Use optionals (`?T`) for absence, not `undefined`.** Reserve `undefined` for buffers you'll fill immediately.
6. **Prefer slices (`[]T`) over many-item pointers (`[*]T`).** Convert raw pointers to slices as early as possible.
7. **Push work to `comptime` when it makes sense.** But don't overuse `anytype` — if a concrete type works, use it.
8. **Write inline tests with `std.testing.allocator`.** It catches memory leaks automatically.
9. **Run `zig fmt` unconditionally.** No exceptions, no debates.
10. **Profile before optimizing.** Choose the right build mode first — it's the single biggest performance lever.
