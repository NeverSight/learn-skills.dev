---
name: zig
description: Up-to-date Zig programming language patterns for version 0.15.2. Use when writing, reviewing, or debugging Zig code, working with build.zig and build.zig.zon files, or using comptime metaprogramming. Critical for avoiding outdated patterns from training data - especially build system APIs (root_module instead of root_source_file, addLibrary with linkage), I/O APIs (buffered writer pattern), container initialization (.empty/.init), allocator selection (DebugAllocator), ArrayList now unmanaged by default, @typeInfo lowercase fields (.@"struct" not .Struct), and removed language features (async/await, usingnamespace).
license: MIT
compatibility:
  - claude-code
  - opencode
  - codex
metadata:
  version: "0.15.2"
  language: "zig"
  category: "programming-language"
---

# Zig Language Reference (v0.15.2)

Zig evolves rapidly. Training data contains outdated patterns that cause compilation errors. This skill documents breaking changes and correct modern patterns.

## Design Principles

### Type-First Development
Define types and function signatures before implementation. Let the compiler guide completeness:
1. Define data structures (structs, unions, error sets)
2. Define function signatures (parameters, return types, error unions)
3. Implement to satisfy types
4. Validate at compile-time

### Make Illegal States Unrepresentable
Use Zig's type system to prevent invalid states at compile time:
- **Tagged unions** over structs with optional fields — prevent impossible state combinations
- **Explicit error sets** over `anyerror` — document exactly which failures can occur
- **Distinct types** via `enum(u64) { _ }` — prevent mixing up IDs (user_id vs order_id)
- **Comptime validation** with `@compileError()` — catch invalid configurations at build time

### Module Structure
Larger cohesive files are idiomatic in Zig. Keep related code together — tests alongside implementation, comptime generics at file scope, visibility controlled by `pub`. Split files only for genuinely separate concerns. The std library demonstrates this with files like `std/mem.zig` containing thousands of cohesive lines.

### Memory Ownership
- Pass allocators explicitly — never use global state for allocation
- Use `defer` immediately after acquiring a resource — cleanup next to acquisition
- Name allocators by contract: `gpa` (caller must free), `arena` (bulk-free at boundary), `scratch` (never escapes)
- Prefer `const` over `var` — immutability signals intent and enables optimizations
- Prefer slices over raw pointers — bounds safety

## Critical: Removed Features (0.15.x)

### `usingnamespace` - REMOVED
```zig
// WRONG - compile error
pub usingnamespace @import("other.zig");

// CORRECT - explicit re-export
const other = @import("other.zig");
pub const foo = other.foo;
```

### `async`/`await` - REMOVED
Keywords removed from language. Async I/O support is planned for future releases.

### `std.BoundedArray` - REMOVED
Use `std.ArrayList` with `initBuffer`:
```zig
var buffer: [8]i32 = undefined;
var stack = std.ArrayList(i32).initBuffer(&buffer);
```

### `std.RingBuffer`, `std.fifo.LinearFifo` - REMOVED
Use `std.Io.Reader`/`std.Io.Writer` ring buffers instead.

### `std.io.SeekableStream`, `std.io.BitReader`, `std.io.BitWriter` - REMOVED

### `std.fmt.Formatter` - REMOVED
Replaced by `std.fmt.Alt`.

### Undefined Behavior Restrictions (0.15.x)
Arithmetic on `undefined` is now **illegal**. Only operators that can never trigger Illegal Behavior permit `undefined` as operand.
```zig
// WRONG - compile error in 0.15.x
var n: usize = undefined;
while (condition) : (n += 1) {}  // ERROR: use of undefined value

// CORRECT - explicit initialization required
var n: usize = 0;
while (condition) : (n += 1) {}

// OK - space reservation (no arithmetic)
var buffer: [256]u8 = undefined;
```

## Critical: I/O API Rewrite ("Writergate")

The entire `std.io` API changed. New `std.Io.Writer` and `std.Io.Reader` are **non-generic** with buffer in the interface.

### Writing
```zig
// WRONG - old API
const stdout = std.io.getStdOut().writer();
try stdout.print("Hello\n", .{});

// CORRECT - new API: provide buffer, access .interface, flush
var buf: [4096]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&buf);
const stdout = &stdout_writer.interface;
try stdout.print("Hello\n", .{});
try stdout.flush();  // REQUIRED!
```

### Reading
```zig
// Reading from file
var buf: [4096]u8 = undefined;
var file_reader = file.reader(&buf);
const r = &file_reader.interface;

// Read line by line (takeDelimiter returns null at EOF)
while (try r.takeDelimiter('\n')) |line| {
    // process line (doesn't include '\n')
}

// Read binary data
const header = try r.takeStruct(Header, .little);
const value = try r.takeInt(u32, .big);
```

### Fixed Buffer Writer (no file)
```zig
var buf: [256]u8 = undefined;
var w: std.Io.Writer = .fixed(&buf);
try w.print("Hello {s}", .{"world"});
const result = w.buffered();  // "Hello world"
```

### Fixed Reader (from slice)
```zig
var r: std.Io.Reader = .fixed("hello\nworld");
const line = (try r.takeDelimiter('\n')).?;  // "hello" (returns null at EOF)
```

**Removed:** `BufferedWriter`, `CountingWriter`, `std.io.bufferedWriter()`

**Deprecated:** `GenericWriter`, `GenericReader`, `AnyWriter`, `AnyReader`, `FixedBufferStream`

**New:** `std.Io.Writer`, `std.Io.Reader` - non-generic, buffer in interface

**Replacements:**
- `CountingWriter` -> `std.Io.Writer.Discarding` (has `.fullCount()`)
- `BufferedWriter` -> buffer provided to `.writer(&buf)` call
- Allocating output -> `std.Io.Writer.Allocating`

## Critical: Build System (0.15.x)

`root_source_file` is REMOVED from `addExecutable`/`addLibrary`/`addTest`. Use `root_module`:

```zig
// WRONG - removed field
b.addExecutable(.{
    .name = "app",
    .root_source_file = b.path("src/main.zig"),  // ERROR
    .target = target,
});

// CORRECT
b.addExecutable(.{
    .name = "app",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    }),
});
```

**Module imports changed:**
```zig
// WRONG (old API)
exe.addModule("helper", helper_mod);

// CORRECT
exe.root_module.addImport("helper", helper_mod);
```

**Libraries: `addSharedLibrary` → `addLibrary` with `.linkage`:**
```zig
// WRONG - removed function
const lib = b.addSharedLibrary(.{ .name = "mylib", ... });

// CORRECT - unified addLibrary with linkage field
const lib = b.addLibrary(.{
    .name = "mylib",
    .linkage = .dynamic,  // or .static (default)
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/lib.zig"),
        .target = target,
        .optimize = optimize,
    }),
});
```

**Adding dependency modules:**
```zig
const dep = b.dependency("lib", .{ .target = target, .optimize = optimize });
exe.root_module.addImport("lib", dep.module("lib"));
```

See **[std.Build reference](references/std-build.md)** for complete build system documentation.

## Critical: Container Initialization

**Never use `.{}` for containers.** Use `.empty` or `.init`:

```zig
// WRONG - deprecated
var list: std.ArrayList(u32) = .{};
var gpa: std.heap.DebugAllocator(.{}) = .{};

// CORRECT - use .empty for empty collections
var list: std.ArrayList(u32) = .empty;
var map: std.AutoHashMapUnmanaged(u32, u32) = .empty;

// CORRECT - use .init for stateful types with internal config
var gpa: std.heap.DebugAllocator(.{}) = .init;
var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
```

### ArrayList: Unmanaged by Default
The old `std.ArrayList` (with allocator stored in struct) is now `std.array_list.Managed`.
The new `std.ArrayList` is **unmanaged** — no allocator field, pass allocator to every method:
```zig
// NEW default: unmanaged (no allocator field)
var list: std.ArrayList(u32) = .empty;
try list.append(allocator, 42);
list.deinit(allocator);

// If you want old behavior (allocator in struct), use Managed:
var list = std.array_list.Managed(u32).init(allocator);
try list.append(42);  // no allocator arg needed
list.deinit();
```

### HashMap: Managed vs Unmanaged
Same pattern applies — unmanaged variants require allocator per operation:
```zig
// Unmanaged (no internal allocator)
var map: std.StringHashMapUnmanaged(u32) = .empty;
try map.put(allocator, "key", 42);
map.deinit(allocator);

// Managed (stores allocator internally)
var map = std.StringHashMap(u32).init(allocator);
try map.put("key", 42);
map.deinit();
```

### Naming Changes
- **`std.ArrayListUnmanaged` -> `std.ArrayList`** (Unmanaged is now default, old name deprecated)
- **`std.heap.GeneralPurposeAllocator` -> `std.heap.DebugAllocator`** (GPA alias still works)

### Linked Lists: Generic Parameter Removed
```zig
// WRONG - old API
const Node = std.DoublyLinkedList(MyData).Node;

// CORRECT - non-generic, use @fieldParentPtr
const MyNode = struct {
    node: std.DoublyLinkedList.Node,
    data: MyData,
};
// Access: const my_node = @fieldParentPtr("node", node_ptr);
```

### Process API: Term is Tagged Union
```zig
// WRONG - direct field access removed
if (result.term.Exited != 0) {}

// CORRECT - pattern match
switch (result.term) {
    .exited => |code| if (code != 0) { /* handle */ },
    else => {},
}
```

## Critical: Format Strings (0.15.x)

`{f}` required to call format methods:
```zig
// WRONG - ambiguous error
std.debug.print("{}", .{std.zig.fmtId("x")});

// CORRECT
std.debug.print("{f}", .{std.zig.fmtId("x")});
```

Format method signature changed:
```zig
// OLD - wrong
pub fn format(self: @This(), comptime fmt: []const u8, opts: std.fmt.FormatOptions, writer: anytype) !void

// NEW - correct
pub fn format(self: @This(), writer: *std.Io.Writer) std.Io.Writer.Error!void
```

## Breaking Changes (0.14.0+)

### `@branchHint` replaces `@setCold`
```zig
// WRONG
@setCold(true);

// CORRECT
@branchHint(.cold);  // Must be first statement in block
```

### `@export` takes pointer
```zig
// WRONG
@export(foo, .{ .name = "bar" });

// CORRECT
@export(&foo, .{ .name = "bar" });
```

### Inline asm clobbers are typed
```zig
// WRONG
: "rcx", "r11"

// CORRECT
: .{ .rcx = true, .r11 = true }
```

### `@fence` - REMOVED
Use stronger atomic orderings or RMW operations instead.

### `@typeInfo` fields now lowercase
```zig
// WRONG - old PascalCase (compile error)
if (@typeInfo(T) == .Struct) { ... }
if (@typeInfo(T) == .Slice) { ... }
if (@typeInfo(T) == .Int) { ... }

// CORRECT - lowercase, keywords escaped with @""
if (@typeInfo(T) == .@"struct") { ... }
if (@typeInfo(T) == .@"enum") { ... }
if (@typeInfo(T) == .@"union") { ... }
if (@typeInfo(T) == .@"opaque") { ... }
if (@typeInfo(T) == .slice) { ... }
if (@typeInfo(T) == .int) { ... }
if (@typeInfo(T) == .bool) { ... }
if (@typeInfo(T) == .pointer) { ... }

// Accessing fields:
const fields = @typeInfo(T).@"struct".fields;
const tag_type = @typeInfo(T).@"enum".tag_type;
```

## Decl Literals (0.14.0+)

`.identifier` syntax works for declarations:
```zig
const S = struct {
    x: u32,
    const default: S = .{ .x = 0 };
    fn init(v: u32) S { return .{ .x = v }; }
};

const a: S = .default;      // S.default
const b: S = .init(42);     // S.init(42)
const c: S = try .init(1);  // works with try
```

## Labeled Switch (0.14.0+)

State machines use `continue :label`:
```zig
state: switch (initial) {
    .idle => continue :state .running,
    .running => if (done) break :state result else continue :state .running,
    .error => return error.Failed,
}
```

## Non-exhaustive Enum Switch (0.15.x)

Can mix explicit tags with `_` and `else`:
```zig
switch (value) {
    .a, .b => {},
    else => {},  // other named tags
    _ => {},     // unnamed integer values
}
```

## Critical: HTTP API Reworked (0.15.x)

HTTP client/server completely restructured — depends only on I/O streams, not networking:
```zig
// Server now takes Reader/Writer interfaces, not connection directly
var recv_buffer: [4000]u8 = undefined;
var send_buffer: [4000]u8 = undefined;
var conn_reader = connection.stream.reader(&recv_buffer);
var conn_writer = connection.stream.writer(&send_buffer);
var server = std.http.Server.init(
    conn_reader.interface(),
    &conn_writer.interface,
);
```
**Note:** HTTP client API is still rapidly evolving. For stability-critical code, consider shelling out to `curl`.

## Quick Fixes

| Error | Fix |
|-------|-----|
| `no field 'root_source_file'` | Use `root_module = b.createModule(.{...})` |
| `use of undefined value` | Arithmetic on `undefined` is now illegal — initialize explicitly |
| `type 'f32' cannot represent integer` | Use float literal: `123_456_789.0` not `123_456_789` |
| `ambiguous format string` | Use `{f}` for format methods |
| `no field 'append'` on ArrayList | Pass allocator: `list.append(allocator, val)` (unmanaged default) |
| `expected 2 arguments, found 1` on ArrayList | Add allocator param: `.append(allocator, val)`, `.deinit(allocator)` |
| `BoundedArray` not found | Use `std.ArrayList(T).initBuffer(&buf)` |
| `GenericWriter`/`GenericReader` | Use `std.Io.Writer`/`std.Io.Reader` |
| missing `.flush()` — no output | Always call `try writer.flush()` after writing |
| `enum has no member named 'Struct'` | `@typeInfo` fields now lowercase: `.@"struct"`, `.slice`, `.int` |
| `no field named 'encode'` on base64 | Use `std.base64.standard.Encoder.encode()` |
| `no field named 'open'` on HTTP | Use `client.request()` or `client.fetch()` |
| `expected error union, found Signature` | `Ed25519.Signature.fromBytes()` doesn't return error — remove `try` |
| `addSharedLibrary` not found | Use `b.addLibrary(.{ .linkage = .dynamic, ... })` |

## Verification Workflow

After writing or modifying Zig code, verify with this sequence:
1. `zig build` — catch compilation errors, match against Quick Fixes above
2. `zig build test` — run unit tests
3. `zig build -Doptimize=ReleaseFast test` — detect undefined behavior (UB checks enabled in optimized builds)

**Development speed tips:**
- `zig build --watch -fincremental` — incremental compilation, rebuilds on file change
- 0.15.x uses self-hosted x86_64 backend by default — ~5x faster Debug builds than LLVM

## Common Pitfalls

- **Forgetting `defer`/`errdefer` cleanup** — place cleanup immediately after resource acquisition
- **Using `anyerror` instead of specific error sets** — explicit sets document failure modes
- **Ignoring error unions** — handle or propagate, never discard
- **Missing `errdefer` after allocations in multi-step init** — partial construction leaks
- **Expecting comptime side effects** — comptime code is evaluated lazily
- **Unhandled integer overflow** — Zig traps on overflow in debug builds
- **Missing null terminators for C strings** — use `:0` sentinel slices: `[:0]const u8`
- **Using `anytype` when `comptime T: type` works** — explicit types produce clearer errors
- **Scoped loggers**: always define per-module `const log = std.log.scoped(.my_module);` for filterable logging

## Learning Resources

Production Zig codebases worth studying:
- **[Bun](https://github.com/oven-sh/bun)** — JS runtime (~200k+ lines), async I/O, FFI, system calls
- **[Ghostty](https://github.com/ghostty-org/ghostty)** — Terminal emulator, cross-platform, GPU rendering
- **[TigerBeetle](https://github.com/tigerbeetle/tigerbeetle)** — Financial DB, deterministic execution, VOPR fuzzing
- **[Mach Engine](https://github.com/hexops/mach)** — Game engine, graphics, ECS
- **[Sig](https://github.com/Syndica/sig)** — Solana validator, high-performance networking

## Language References

Load these references when working with core language features:

### Code Style
- **[Style Guide](references/style-guide.md)** - Official Zig naming conventions (TitleCase types, camelCase functions, snake_case variables), whitespace rules, doc comment guidance, redundancy avoidance, `zig fmt`

### Language Basics & Built-ins
- **[Language Basics](references/language.md)** - Core language: types, control flow (if/while/for/switch), error handling (try/catch/errdefer), optionals, structs, enums, unions, pointers, slices, comptime, functions
- **[Built-in Functions](references/builtins.md)** - All `@` built-ins: type casts (@intCast, @bitCast, @ptrCast), arithmetic (@addWithOverflow, @divExact), bit ops (@clz, @popCount), memory (@memcpy, @sizeOf), atomics (@atomicRmw, @cmpxchgWeak), introspection (@typeInfo, @TypeOf, @hasDecl), SIMD (@Vector, @splat, @reduce), C interop (@cImport, @export)

## Standard Library References

Load these references when working with specific modules:

### Memory & Slices
- **[std.mem](references/std-mem.md)** - Slice search/compare, split/tokenize, alignment, endianness, byte conversion

### Text & Encoding
- **[std.fmt](references/std-fmt.md)** - Format strings, integer/float parsing, hex encoding, custom formatters, `{f}` specifier (0.15.x)
- **[std.ascii](references/std-ascii.md)** - ASCII character classification (isAlpha, isDigit), case conversion, case-insensitive comparison
- **[std.unicode](references/std-unicode.md)** - UTF-8/UTF-16 encoding/decoding, codepoint iteration, validation, WTF-8 for Windows
- **[std.base64](references/std-base64.md)** - Base64 encoding/decoding (standard, URL-safe, with/without padding)

### Math & Random
- **[std.math](references/std-math.md)** - Floating-point ops, trig, overflow-checked arithmetic, constants, complex numbers, big integers
- **[std.Random](references/std-random.md)** - PRNGs (Xoshiro256, Pcg), CSPRNGs (ChaCha), random integers/floats/booleans, shuffle, distributions
- **[std.hash](references/std-hash.md)** - Non-cryptographic hash functions (Wyhash, XxHash, FNV, Murmur, CityHash), checksums (CRC32, Adler32), auto-hashing

### SIMD & Vectorization
- **[std.simd](references/std-simd.md)** - SIMD vector utilities: optimal vector length, iota/repeat/join/interlace patterns, element shifting/rotation, parallel searching, prefix scans, branchless selection

### Time & Timing
- **[std.time](references/std-time.md)** - Wall-clock timestamps, monotonic Instant/Timer, epoch conversions, calendar utilities (year/month/day), time unit constants
- **[std.Tz](references/std-tz.md)** - TZif timezone database parsing (RFC 8536), UTC offsets, DST rules, timezone abbreviations, leap seconds

### Sorting & Searching
- **[std.sort](references/std-sort.md)** - Sorting algorithms (pdq, block, heap, insertion), binary search, min/max

### Core Data Structures
- **[std.ArrayList](references/std-arraylist.md)** - Dynamic arrays, vectors, BoundedArray replacement
- **[std.HashMap / AutoHashMap](references/std-hashmap.md)** - Hash maps, string maps, ordered maps
- **[std.ArrayHashMap](references/std-array-hash-map.md)** - Insertion-order preserving hash map, array-style key/value access
- **[std.MultiArrayList](references/std-multi-array-list.md)** - Struct-of-arrays for cache-efficient struct storage
- **[std.SegmentedList](references/std-segmented-list.md)** - Stable pointers, arena-friendly, non-copyable types
- **[std.DoublyLinkedList / SinglyLinkedList](references/std-linked-list.md)** - Intrusive linked lists, O(1) insert/remove
- **[std.PriorityQueue](references/std-priority-queue.md)** - Binary heap, min/max extraction, task scheduling
- **[std.PriorityDequeue](references/std-priority-dequeue.md)** - Min-max heap, double-ended priority extraction
- **[std.Treap](references/std-treap.md)** - Self-balancing BST, ordered keys, min/max/predecessor
- **[std.bit_set](references/std-bit-set.md)** - Bit sets (Static, Dynamic, Integer, Array), set operations, iteration
- **[std.BufMap / BufSet](references/std-buf-map.md)** - String-owning maps and sets, automatic key/value memory management
- **[std.StaticStringMap](references/std-static-string-map.md)** - Compile-time optimized string lookup, perfect hash for keywords
- **[std.enums](references/std-enums.md)** - EnumSet, EnumMap, EnumArray: bit-backed enum collections

### Allocators
- **[std.heap](references/std-allocators.md)** - Allocator selection guide, ArenaAllocator, DebugAllocator, FixedBufferAllocator, MemoryPool, SmpAllocator, ThreadSafeAllocator, StackFallbackAllocator, custom allocator implementation

### I/O & Files
- **[std.io](references/std-io.md)** - Reader/Writer API (0.15.x): buffered I/O, streaming, binary data, format strings
- **[std.fs](references/std-fs.md)** - File system: files, directories, iteration, atomic writes, paths
- **[std.tar](references/std-tar.md)** - Tar archive reading/writing, extraction, POSIX ustar, GNU/pax extensions
- **[std.zip](references/std-zip.md)** - ZIP archive reading/extraction, ZIP64 support, store/deflate compression
- **[std.compress](references/std-compress.md)** - Compression: DEFLATE (gzip, zlib), Zstandard, LZMA, LZMA2, XZ decompression/compression

### Networking
- **[std.http](references/std-http.md)** - HTTP client/server, TLS, connection pooling, compression, WebSocket
- **[std.net](references/std-net.md)** - TCP/UDP sockets, address parsing, DNS resolution
- **[std.Uri](references/std-uri.md)** - URI parsing/formatting (RFC 3986), percent-encoding/decoding, relative URI resolution

### Process Management
- **[std.process](references/std-process.md)** - Child process spawning, environment variables, argument parsing, exec

### OS-Specific APIs
- **[std.os](references/std-os.md)** - OS-specific APIs: Linux syscalls, io_uring, Windows NT APIs, WASI, direct platform access
- **[std.c](references/std-c.md)** - C ABI types and libc bindings: platform-specific types (fd_t, pid_t, timespec), errno values, socket/signal/memory types, fcntl/open flags, FFI with C libraries

### Concurrency
- **[std.Thread](references/std-thread.md)** - Thread spawning, Mutex, RwLock, Condition, Semaphore, WaitGroup, thread pools
- **[std.atomic](references/std-atomic.md)** - Lock-free atomic operations: Value wrapper, fetch-and-modify (add/sub/and/or/xor), compare-and-swap, atomic ordering semantics, spin loop hints, cache line sizing

### Patterns & Best Practices
- **[Zig Patterns](references/patterns.md)** - **Load when writing new code or reviewing code quality.** Comprehensive best practices extracted from the Zig standard library: quick patterns (memory/allocators, file I/O, HTTP, JSON, testing, build system) plus idiomatic code patterns covering syntax (closures, context pattern, options structs, destructuring), polymorphism (duck typing, generics, custom formatting, dynamic/static dispatch), safety (diagnostics, error payloads, defer/errdefer, compile-time assertions), and performance (const pointer passing)
- **[Production Patterns](references/production-patterns.md)** - **Load when building large-scale Zig systems or optimizing performance.** Real-world patterns from Bun, Ghostty, TigerBeetle: modular build systems, CPU feature locking, pre-allocated message pools, counting allocators, SIMD with scalar fallback, intrusive linked lists, cache-line aligned SoA, work-stealing thread pools, SmolStr (15-byte SSO), comptime string maps, EnumUnionType generation, VOPR fuzzing, snapshot testing, edge-biased fuzz generation, platform abstraction facades, Objective-C bridges, opaque C wrappers with RAII, packed struct bitfields, Result union types, radix sort, tournament trees
- **[MCP Server Patterns](references/mcp-server-patterns.md)** - **Load when building MCP servers, LSP bridges, JSON-RPC services, or protocol translators in Zig.** Patterns from zig-mcp: newline-delimited vs Content-Length transport, thread-based request correlation with ResetEvent, arena-per-request memory, child process lifecycle with pipe ownership transfer, tool registry with function pointers, std.json.Stringify for manual JSON building, lazy document sync with double-check locking, graceful degradation, auto-reconnect on crash, comptime schema generation, file URI encoding, common serialization gotchas
- **[Code Review](references/code-review.md)** - **Load when reviewing Zig code.** Systematic checklist organized by confidence level: ALWAYS FLAG (removed features, changed syntax, API changes), FLAG WITH CONTEXT (exception safety bugs, missing flush, allocator issues), SUGGEST (style improvements). Includes migration examples for 0.14/0.15 breaking changes

### Serialization
- **[std.json](references/std-json.md)** - JSON parsing, serialization, dynamic values, streaming, custom parse/stringify
- **[std.zon](references/std-zon.md)** - ZON (Zig Object Notation) parsing and serialization for build.zig.zon, config files, data interchange

### Testing & Debug
- **[std.testing](references/std-testing.md)** - Unit test assertions and utilities
- **[std.debug](references/std-debug.md)** - Panic, assert, stack traces, hex dump, format specifiers
- **[std.log](references/std-log.md)** - Scoped logging with configurable levels and output

### Metaprogramming
- **[Comptime Reference](references/comptime.md)** - Comptime fundamentals, type reflection (`@typeInfo`/`@Type`/`@TypeOf`), loop variants (`comptime for` vs `inline for`), branch elimination, type generation, comptime limitations
- **[std.meta](references/std-meta.md)** - Type introspection, field iteration, stringToEnum, generic programming

### Compiler Utilities
- **[std.zig](references/std-zig.md)** - AST parsing, tokenization, source analysis, linters, formatters, ZON parsing

### Security & Cryptography
- **[std.crypto](references/std-crypto.md)** - Hashing (SHA2, SHA3, Blake3), AEAD (AES-GCM, ChaCha20-Poly1305), signatures (Ed25519, ECDSA), key exchange (X25519), password hashing (Argon2, scrypt, bcrypt), secure random, timing-safe operations

### Build System
- **[std.Build](references/std-build.md)** - Build system: build.zig, modules, dependencies, build.zig.zon, steps, options, testing, C/C++ integration

### Interoperability
- **[C Interop](references/c-interop.md)** - Exporting C-compatible APIs: `export fn`, C calling convention, building static/dynamic libraries, creating headers, macOS universal binaries, XCFramework for Swift/Xcode, module maps

## Tooling

### ZLS (Zig Language Server)
IDE support via Language Server Protocol. Provides autocomplete, go-to-definition, hover docs, diagnostics.

**Version matching rule:** Use ZLS release matching your Zig release (0.15.x ZLS for 0.15.x Zig). Nightly Zig needs nightly ZLS.

**Installation:**
```bash
# VS Code: install "Zig Language" extension (includes ZLS)

# Manual / other editors:
# Download from https://github.com/zigtools/zls/releases
# Or build from source:
git clone https://github.com/zigtools/zls
cd zls && git checkout 0.15.0  # match your Zig version
zig build -Doptimize=ReleaseSafe

# Configure:
zls --config
```

**Editor support:** VS Code, Neovim (nvim-lspconfig), Helix, JetBrains, Emacs (lsp-mode), Sublime Text, Kate.

**Key features:**
- Autocomplete with semantic analysis
- Go-to-definition, find references
- Hover documentation
- Diagnostics (compile errors inline)
- Filesystem completions inside `@import("")` strings
- `std` and `builtin` module path completions
- Snippets for common declarations

### anyzig (Version Manager)
Universal Zig version manager — run any Zig version from any project. Replaces manual version switching.

**Source:** https://github.com/marler8997/anyzig

**How it works:**
1. Reads `minimum_zig_version` from `build.zig.zon` (searches up directory tree)
2. Auto-downloads needed compiler version into global cache
3. Invokes the correct `zig` transparently

**Installation:**
```bash
# macOS (Apple Silicon)
curl -L https://marler8997.github.io/anyzig/aarch64-macos/anyzig.tar.xz | tar xJ
mv zig /usr/local/bin/zig  # replaces/shadows system zig

# macOS (Intel)
curl -L https://marler8997.github.io/anyzig/x86_64-macos/anyzig.tar.xz | tar xJ
mv zig /usr/local/bin/zig

# Linux (x86_64)
curl -L https://marler8997.github.io/anyzig/x86_64-linux/anyzig.tar.xz | tar xJ
sudo mv zig /usr/local/bin/zig
```

**Usage:**
```bash
# Automatic — reads build.zig.zon minimum_zig_version:
cd myproject && zig build

# Manual version override:
zig 0.13.0 build-exe myproject.zig
zig 0.15.2 build

# Mach engine versions supported:
# Reads .mach_zig_version from build.zig.zon
# Format: 2024.10.0-mach

# anyzig-specific commands:
zig any --help
```

**build.zig.zon version field:**
```zig
.{
    .name = .myproject,
    .version = "0.1.0",
    .minimum_zig_version = "0.15.2",
    // ...
}
```
