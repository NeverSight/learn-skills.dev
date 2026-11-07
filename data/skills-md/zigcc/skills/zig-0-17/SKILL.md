---
name: zig-0-17
description: Zig 0.17.0 API guidance and porting notes. Use this when writing or upgrading Zig code to the 0.17.0 stable release (@backingInt/@fromBackingInt, SafeAllocator, SoA type reflection, build system maker/configurer separation).
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  version: "0.17.0"
  language: "zig"
  category: "programming-language"
---

# Zig 0.17.0 Programming Guide

> **Version Scope**: Pinned to **Zig 0.17.0** (stable).
> **Release Notes**: https://ziglang.org/download/0.17.0/release-notes.html

Zig 0.17.0 advances language stability towards 1.0. Major highlights include replacing `@intFromEnum`/`@enumFromInt` with `@backingInt`/`@fromBackingInt`, moving type reflection (`std.lang.Type`) and container builtins to Struct-Of-Arrays (SoA) style, removing array multiplication syntax `**` in favor of `@splat`, replacing `DebugAllocator` with the thread-safe `SafeAllocator`, moving `fmt.allocPrint` into `mem.Allocator`, decoupling C translation to an external package, and separating the Build System into distinct Configurer and Maker processes with fine-grained cache poisoning tracking.

---

## Local Documentation First

Run `zig env` to discover local installation paths — never hardcode them:
- **Language Reference**: `<lib_dir>/../doc/langref.html`
- **Std Library Source**: Inspect source files under `.std_dir` for exact signatures.
- **Std Library Docs**: Run `zig std` to launch the local documentation HTTP server.

Always check local docs or source before searching online.

---

## Quick Reference: Top Breaking Changes

| Old (0.16.x) | New (0.17.0) | Notes |
|---|---|---|
| `@intFromEnum(val)` | `@backingInt(val)` | Also works on bitpacks and tagged unions |
| `@enumFromInt(val)` | `@fromBackingInt(val)` | Return type inferred; illegal values safety-checked |
| `[1]T{val} ** len` | `@splat(val)` | Array multiplication `**` removed; use `@splat` |
| `@bitCast(extern_struct_val)` | `@ptrCast(&val).*` or `extern union` | `@bitCast` forbidden on `extern struct`/`extern union` |
| `void{}` | `{}` | Syntax `void{}` removed |
| `errdefer \|err\| { ... }` | Refactor into helper fn + `catch \|err\|` | Error capture in `errdefer` removed |
| `i0` | `u0` | `i0` primitive integer type removed |
| `@hasDecl` (returns true for private in same file) | Returns `true` ONLY for `pub` declarations | Behavior now uniform across files |
| `@cImport({...})` | `b.dependency("translate_c", .{})` + `Translator` | `@cImport` removed; C translator moved to package |
| `std.heap.DebugAllocator` | `std.heap.SafeAllocator` | Thread-safe, non-reusing, leak & corruption detection |
| `std.heap.StackFallbackAllocator(N)` | `std.heap.BufferFirstAllocator.init(buf, fallback)` | Explicit buffer argument instead of comptime size |
| `std.fmt.allocPrint(arena, ...)` | `arena.print(...)` / `allocator.print(...)` | Moved into `std.mem.Allocator` |
| `list.getLastOrNull()` | `list.last()` | Returns `?T` |
| `list.getLast()` | `list.last().?` | Non-null assert via `.?`; new `list.lastPtr()` returns `?*T` |
| `std.zon.parse.fromSliceAlloc` | `std.zon.parse.fromSlice(T, .{ ... })` | Struct arguments; new `updateFromSlice` |
| `std.bit_set.IntegerBitSet` | `std.bit_set.Integer` | Similarly: `Array`, `Static`, `Dynamic`; `.empty`/`.full` |
| `@typeInfo(S).@"struct".fields` | `field_names`, `field_types`, `field_attrs` | Type reflection rewritten in Struct-Of-Arrays (SoA) |
| `@Struct` (7 params) | `@Struct(layout, BackingInt, names, types, attrs)` | 5 params; `@Union` (5 params), `@Enum` (4 params) |
| `std.lang.OptimizeMode` | `std.lang.Optimize` | Lowercase tags: `.debug`, `.safe`, `.fast`, `.small` |
| `@import("builtin").cpu / os / abi` | `@import("builtin").target.cpu / os / abi` | Access through `.target` |
| `b.build_root` (Directory) | `b.root` (Cache.Path) | Path representation changed |
| `if (b.args) \|args\| run.addArgs(args);` | `run.addPassthruArgs()` | Keeps configure cache pure across arg changes |
| `b.findProgram(...)` | `b.findProgramLazy(...)` | Lazy resolution avoids configure cache poisoning |

---

## Language Changes

### 1. `@backingInt` and `@fromBackingInt` Replace Enum Conversion Builtins

`@intFromEnum` and `@enumFromInt` are deprecated (#35966). Use `@backingInt` and `@fromBackingInt`:

- `@backingInt` works with:
  - All `enum` types.
  - Bitpacks (`packed struct` / `packed union`) with an **explicit** backing integer.
  - Tagged `union` types (returns the backing integer of the *active* tag).
- `@fromBackingInt` infers its destination type (any enum or explicit-backed bitpack). It accepts an integer matching that backing type and performs safety-checked validation of tag values for enums.
- Empty enums must declare `noreturn` as their backing integer (e.g. `enum(noreturn) {}`).
- `zig fmt` automatically upgrades old `@intFromEnum` and `@enumFromInt` calls.

```zig
const Status = enum(u8) {
    ok = 0,
    err = 1,
};

const status: Status = .ok;
// Convert enum to backing integer
const raw: u8 = @backingInt(status);

// Convert backing integer to enum (type is inferred from context)
const restored: Status = @fromBackingInt(raw);

// Helper function to query backing integer type:
const TagInt = std.meta.BackingInt(Status); // u8
```

### 2. `@bitCast` Semantics: Logical Bit Representation Only

Zig 0.17.0 redefined `@bitCast` to reinterpret the **logical bit representation** of values, making it strictly endian-agnostic:
- Allowed types: `void`, `bool`, integers (except `comptime_int`), floats (except `comptime_float`), integer-backed `enum(T)`, `packed struct(T)`, `packed union(T)`, and arrays/vectors thereof.
- **Forbidden**: `extern struct` and `extern union` can no longer be passed to `@bitCast`.
- To type-pun memory representations of `extern struct`, use `@ptrCast` or an `extern union`:

```zig
const TwoBytes = extern struct {
    b0: u8,
    b1: u8,
};

test "type pun extern struct in 0.17" {
    const bytes: TwoBytes = .{ .b0 = 0x12, .b1 = 0xAB };

    // OLD (0.16): const int: u16 = @bitCast(bytes); // COMPILE ERROR in 0.17

    // NEW (0.17): Use pointer cast
    const int_ptr: *align(1) const u16 = @ptrCast(&bytes);
    const int: u16 = int_ptr.*;
    _ = int;
}
```

### 3. Array Multiplication `**` Removed — Use `@splat`

The repetition syntax `[1]u8{0} ** N` has been removed. Use `@splat`:

```zig
// OLD (0.16)
var buf = [1]u8{0} ** 1024;
const arr = [1]f32{1.5} ** 4;

// NEW (0.17)
var buf: [1024]u8 = @splat(0);
const arr: [4]f32 = @splat(1.5);
```

### 4. Added `@divCeil`

Performs integer division rounding toward positive infinity ($+\infty$), complementing `@divTrunc`, `@divFloor`, and `@divExact`:

```zig
try std.testing.expectEqual(2, @divCeil(5, 3));
try std.testing.expectEqual(-1, @divCeil(-5, 3));
```

### 5. `@hasDecl` Only Inspects Public (`pub`) Declarations

Previously, `@hasDecl(T, name)` returned `true` for private declarations if invoked within the same source file. Now it **strictly checks `pub` declarations only**, regardless of caller context.

```zig
const Foo = struct {
    pub const public_val = 1;
    const private_val = 2;
};

// In 0.17:
@hasDecl(Foo, "public_val") == true;
@hasDecl(Foo, "private_val") == false; // Always false even within the same file
```

### 6. Comptime-Length Slice Dereferencing and Array Coercion

Slices with comptime-known lengths can now be dereferenced directly or coerced to array pointers:

```zig
const slice: []const u16 = &.{ 1, 2, 3 };
const array: [3]u16 = slice.*;               // Valid in 0.17
const array_ptr: *const [3]u16 = slice;      // Valid in 0.17
```

### 7. Syntax Removals: `void{}`, `errdefer |err|`, `i0`

- **`void{}` Removed**: Replace `void{}` with `{}`.
- **`errdefer |err|` Removed**: Capturing the error in `errdefer` is no longer valid. Refactor into an inner function or handle via `catch |err|`:
  ```zig
  // OLD:
  // errdefer |err| std.log.err("failed: {s}", .{@errorName(err)});

  // NEW:
  fn run() void {
      runInner() catch |err| {
          std.log.err("failed: {s}", .{@errorName(err)});
      };
  }
  fn runInner() !void { ... }
  ```
- **`i0` Removed**: Replace any `i0` usage with `u0`.
- **Global Linkage Cleanups**: `internal` and `link_once` in `std.lang.GlobalLinkage` removed. Use `weak` for `link_once`, and omit `@export` instead of `internal`.

### 8. `@cImport` Removed — External `translate_c` Package

`@cImport` is fully removed. Furthermore, `std.Build.Step.TranslateC` is deprecated in favor of the official external package:

```bash
zig fetch --save git+https://codeberg.org/ziglang/translate-c
```

In `build.zig`:

```zig
const std = @import("std");
const Translator = @import("translate_c").Translator;

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const translate_c_dep = b.dependency("translate_c", .{});
    const translator: Translator = .init(translate_c_dep, .{
        .c_source_file = b.path("src/c.h"),
        .target = target,
        .optimize = optimize,
    });
    translator.linkSystemLibrary("glfw3", .{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
            .imports = &.{
                .{ .name = "c", .module = translator.mod },
            },
        }),
    });
    b.installArtifact(exe);
}
```

---

## Standard Library Changes

### 1. `std.heap.SafeAllocator` (Replaces `DebugAllocator`)

`std.heap.DebugAllocator` is deprecated. Use `std.heap.SafeAllocator`:
- **Thread-safe**: Concurrency without external locks.
- **Safety guarantees**: Leaks reported on `deinit()`; invalid frees, operations races, and buffer overwrites panic or trigger segmentation faults via an `AllocFooter` checksum.
- **No memory reuse**: Backing memory is never recycled to catch use-after-free bugs.

```zig
const std = @import("std");

test "SafeAllocator usage" {
    var gpa: std.heap.SafeAllocator = .init(std.heap.page_allocator, .{});
    defer {
        const leaks = gpa.deinit();
        if (leaks != 0) @panic("Memory leak detected!");
    }
    const allocator = gpa.allocator();

    const slice = try allocator.alloc(u32, 16);
    defer allocator.free(slice);
}
```

### 2. `BufferFirstAllocator` (Reworked `StackFallbackAllocator`)

`StackFallbackAllocator(N)` is replaced by `std.heap.BufferFirstAllocator`. Pass an explicit buffer slice rather than declaring a comptime buffer size:

```zig
var stack_buf: [256]u8 = undefined;
var bfa: std.heap.BufferFirstAllocator = .init(&stack_buf, gpa);
const allocator = bfa.allocator();

// Allocations small enough will use stack_buf; spills fallback to gpa.
```

### 3. `mem.Allocator.print` Replaces `std.fmt.allocPrint`

`allocPrint` is now an instance method directly on `std.mem.Allocator`:

```zig
// OLD (0.16)
const str = try std.fmt.allocPrint(allocator, "{s}={d}", .{ key, val });

// NEW (0.17)
const str = try allocator.print("{s}={d}", .{ key, val });
// For null-terminated strings:
const zstr = try allocator.printSentinel("{s}={d}", .{ key, val }, 0);
```

### 4. `ArrayList` Updates: `last()`, `last().?`, `lastPtr()`

- `getLastOrNull()` is deprecated $\rightarrow$ use `last()` (returns `?T`).
- `getLast()` is deprecated $\rightarrow$ use `last().?`.
- Added `lastPtr()` $\rightarrow$ returns `?*T`.

```zig
var list = try std.ArrayList(u32).initCapacity(allocator, 8);
defer list.deinit(allocator);

try list.append(allocator, 42);

if (list.last()) |val| {
    // val == 42
}
const non_null = list.last().?;

if (list.lastPtr()) |ptr| {
    ptr.* += 1;
}
```

### 5. `std.zon.parse` Reworked

`std.zon` now takes a configuration struct and allocates from an arena:

```zig
const Config = struct {
    host: []const u8,
    port: u16,
};

var diag: std.zon.parse.Diagnostics = undefined;
const parsed = try std.zon.parse.fromSlice(Config, .{
    .gpa = gpa,
    .arena = arena,
    .source = zon_text,
    .diagnostics = &diag,
});

// For in-place field updates:
// std.zon.parse.updateFromSlice(&config, .{ ... });
```

### 6. `std.bit_set` Renamed

Standard bit set variants have been modernized:
- `IntegerBitSet` $\rightarrow$ `std.bit_set.Integer`
- `ArrayBitSet` $\rightarrow$ `std.bit_set.Array`
- `StaticBitSet` $\rightarrow$ `std.bit_set.Static`
- `DynamicBitSetUnmanaged` $\rightarrow$ `std.bit_set.Dynamic`
- `DynamicBitSet` (managed) $\rightarrow$ `std.bit_set.DynamicManaged` (deprecated)
- `initEmpty()` / `initFull()` $\rightarrow$ use `.empty` / `.full` decl literals.

### 7. Type Reflection: Struct-Of-Arrays (SoA) for `std.lang.Type`

Type inspection fields in `std.lang.Type` have migrated from an Array-of-Structs (`fields: []Field`) to Struct-of-Arrays (`field_names`, `field_types`, `field_attrs`):

```zig
fn printFieldNames(comptime T: type) void {
    const info = @typeInfo(T).@"struct";
    inline for (info.field_names, info.field_types, info.field_attrs) |name, field_type, attrs| {
        _ = field_type;
        _ = attrs;
        std.debug.print("Field: {s}\n", .{name});
    }
}
```

#### Updated Type-Creating Builtins:
- `@Struct(layout, BackingInt, field_names, field_types, field_attrs)` (5 parameters instead of 7)
- `@Union(layout, tag_type, field_names, field_types, field_attrs)` (5 parameters)
- `@Enum(tag_type, mode, field_names, field_values)` (4 parameters)

Tip: Use `&@splat(.{})` for default field attributes:
```zig
const MyStruct = @Struct(
    .auto,
    null,
    &.{"x", "y"},
    &.{i32, i32},
    &@splat(.{}),
);
```

### 8. `std.lang.Optimize` (Lowercase Tags)

`std.lang.OptimizeMode` is renamed to `std.lang.Optimize`:
- Tags: `.debug`, `.safe`, `.fast`, `.small`
- Use `std.lang.Optimize.runtimeSafety(mode)` instead of `std.debug.runtime_safety`.

### 9. Other Deprecations & Cleanups
- `@import("builtin")`: `.cpu`, `.os`, `.abi`, `.object_format` deprecated $\rightarrow$ use `.target.cpu`, `.target.os`, `.target.abi`, `.target.ofmt`.
- `std.builtin` deprecated in favor of `std.lang`.
- `std.DoublyLinkedList.pop` $\rightarrow$ `popLast`.
- `std.gpu` $\rightarrow$ `std.spirv`.
- `std.ascii.indexOfIgnoreCase*` $\rightarrow$ `std.ascii.findIgnoreCase*`.
- `Uri` decoupled from `net.HostName` $\rightarrow$ use `std.Io.net.HostName.fromUri(uri, &buf)`.
- `mem.eql` and `mem.findDiff` no longer short-circuit pointer equality on float slices (handles `NaN` correctly).

---

## Build System & Toolchain

### 1. Maker Process Separated from Configurer Process

`zig build` splits project configuration from build execution:
- **Configurer**: Evaluates `build.zig` into a binary format representing the build graph.
- **Maker**: Reusable pre-compiled binary that evaluates tasks, handles package fetching, and executes steps.
- Accelerates subsequent runs and powers the **Build Server Protocol (`--listen=-`)** for IDEs and tooling.

### 2. Configure Cache Poisoning

When logic in `build.zig` produces side effects that the cache system cannot track, it **poisons** the configuration cache, forcing full re-evaluation on next run.

- `b.findProgram(...)` searches PATH immediately at configure time $\rightarrow$ **poisons cache**.
- **Preferred**: `b.findProgramLazy(...)` returns a `LazyPath` $\rightarrow$ **pure, does not poison cache**.
- To declare file/directory dependencies explicitly and keep the cache pure:
  ```zig
  b.dependOnFileContents(path);
  b.dependOnFileMetadata(path);
  b.dependOnDirectoryContents(dir_path);
  b.dependOnDirectoryMetadata(dir_path);
  ```
- Override via CLI flag: `--cache-poison=pure` (default), `poisoned`, `disallowed`, or `ignored`.

### 3. Run Step: Passthru Args

Do not inspect `b.args` in `build.zig`. Use `addPassthruArgs()`:

```zig
// OLD (0.16)
if (b.args) |args| {
    run_cmd.addArgs(args);
}

// NEW (0.17)
run_cmd.addPassthruArgs();
```
Changing CLI arguments via `zig build run -- arg1 arg2` will no longer invalidate the configure cache!

### 4. System Libraries and pkg-config

`Module.linkSystemLibrary` uses pkg-config by default in Zig 0.17:

```zig
module.linkSystemLibrary("foo", .{});
```

For platform-provided libraries that do not ship `.pc` files, such as Windows
`bcrypt` and `ws2_32`, disable pkg-config explicitly:

```zig
module.linkSystemLibrary("bcrypt", .{
    .use_pkg_config = .no,
});
```

This still links the library by name; it only prevents Zig from invoking
`pkg-config`.

### 5. Build Root & Path Options

- `b.build_root` (Directory) $\rightarrow$ `b.root` (Cache.Path).
- `Step.Options`: Distinguish files from directories:
  - `addOptionPath(name, path)` (file only)
  - `addOptionPathDirectory(name, path)` (directory only)
  - `addOptionPathUntracked(name, path)` (opt out of dependency tracking)
- `b.pathList(&.{ "src", "test" })` produces `[]const LazyPath` for `fmt` steps:
  ```zig
  const fmt_step = b.addFmt(.{
      .paths = b.pathList(&.{ "src", "build.zig" }),
  });
  ```
- `b.dependencyLazy`: Can return `error.LazyDependencyNeeded`. In `pub fn build(b: *std.Build) !void`:
  ```zig
  const dep = try b.dependencyLazy("my_dep", .{});
  ```

---

## Common Idioms in Zig 0.17.0

### Standard Project Entrypoint (Juicy Main)

```zig
const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const gpa = init.gpa;
    const arena = init.arena.allocator();

    // Print to stdout
    try std.Io.File.stdout().writeStreamingAll(io, "Running on Zig 0.17.0!\n");

    // Dynamic formatted string
    const greeting = try gpa.print("Hello, {s}!", .{"World"});
    defer gpa.free(greeting);

    // Read CLI args
    const args = try init.minimal.args.toSlice(arena);
    for (args, 0..) |arg, i| {
        std.log.info("arg[{d}]: {s}", .{ i, arg });
    }
}
```

### Memory Management with SafeAllocator in Tests

```zig
const std = @import("std");

test "data processing test" {
    var gpa: std.heap.SafeAllocator = .init(std.heap.page_allocator, .{});
    defer {
        const leaks = gpa.deinit();
        std.debug.assert(leaks == 0);
    }
    const allocator = gpa.allocator();

    var list = try std.ArrayList(u32).initCapacity(allocator, 4);
    defer list.deinit(allocator);

    try list.append(allocator, 100);
    try std.testing.expectEqual(@as(u32, 100), list.last().?);
}
```

---

## Common Error Messages and Fixes (0.17)

| Error Message | Root Cause | Solution |
|---|---|---|
| `error: cannot @bitCast from 'extern struct'` | `@bitCast` disallows `extern struct`/`extern union` | Use `@ptrCast(&val).*` or use an `extern union` |
| `error: expected 5 arguments, found 7` on `@Struct` | `@Struct` parameter count reduced in SoA update | Group defaults/alignments/comptime into `field_attrs` slice |
| `error: no member named 'getLastOrNull' in 'ArrayList'` | Method renamed | Use `list.last()` |
| `error: no member named 'allocPrint' in 'std.fmt'` | Function moved to `mem.Allocator` | Call `allocator.print(...)` directly |
| `error: expected type 'std.lang.Optimize', found 'std.builtin.OptimizeMode'` | `OptimizeMode` renamed and tags lowercased | Use `std.lang.Optimize.debug` / `.safe` / `.fast` / `.small` |
| `error: no member named 'initEmpty' in 'std.bit_set'` | Initializer syntax updated | Use `std.bit_set.Integer.empty` or decl literal `.empty` |
| `error: 'errdefer' cannot capture error` | `\|err\|` capture syntax removed | Wrap logic into a helper function and use `catch \|err\|` |
| `error: cannot multiply array types with '**'` | Array multiplication removed | Replace `[1]T{val} ** N` with `@splat(val)` |

---

## Porting Strategy (0.16 → 0.17)

1. **Run `zig fmt` first**:
   `zig fmt` automatically migrates `@intFromEnum` $\rightarrow$ `@backingInt` and `@enumFromInt` $\rightarrow$ `@fromBackingInt`.
2. **Fix Array Repetitions**:
   Search and replace `**` array multiplications with `@splat(...)`.
3. **Audit `@bitCast`**:
   Ensure `@bitCast` is not used on `extern struct` or `extern union`. Convert them to `@ptrCast` on a pointer or refactor to `extern union`.
4. **Update `fmt.allocPrint`**:
   Change `std.fmt.allocPrint(alloc, ...)` to `alloc.print(...)`.
5. **Update `ArrayList` Calls**:
   Replace `getLastOrNull()` with `last()`, and `getLast()` with `last().?`.
6. **Migrate Build System**:
   - In `build.zig`, replace `run_cmd.addArgs(args)` conditionals with `run_cmd.addPassthruArgs()`.
   - Replace `b.findProgram` with `b.findProgramLazy` if the path is only needed at make time.
   - Replace `b.build_root` with `b.root`.
   - Update `paths` for formatting steps using `b.pathList(...)`.
   - If using C translation, add the `translate_c` dependency in `build.zig.zon` and use `Translator`.
7. **Verify Tests**:
   Run `zig build test` to ensure clean compilation and verify zero memory leaks with `SafeAllocator`.
