---
name: zig
description: "Zig ecosystem skill with emerging patterns from zig-syrup"
version: 2.0.0
---


# zig

Zig ecosystem for systems programming without hidden control flow.

## Atomic Skills

| Skill | Commands | Domain |
|-------|----------|--------|
| zig build | build system | Compile, link, cross-compile |
| zig test | testing | Run test blocks |
| zig fmt | formatter | Canonical formatting |
| zls | LSP | Autocomplete, diagnostics |

## Quick Start

```bash
# New project
mkdir myproject && cd myproject
zig init

# Build and run
zig build run

# Test
zig build test

# Format
zig fmt src/

# Cross-compile to WASM
zig build -Dtarget=wasm32-freestanding
```

## build.zig (0.15.2)

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(exe);

    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());

    const run_step = b.step("run", "Run the application");
    run_step.dependOn(&run_cmd.step);

    const tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&b.addRunArtifact(tests).step);
}
```

### build.zig Module Registration (0.15.2)

When registering many modules in build.zig, Zig 0.15.2 enforces unused-const rules:

```zig
// If a module has downstream imports, keep the named const:
const message_frame_mod = b.addModule("message_frame", .{
    .root_source_file = b.path("src/message_frame.zig"),
});

// If a module has NO downstream imports, discard the return value directly:
_ = b.addModule("terminal", .{
    .root_source_file = b.path("src/terminal.zig"),
});

// WRONG — "pointless discard of local constant" error:
// const terminal_mod = b.addModule(...);
// _ = terminal_mod;

// Dependency chaining:
const qrtp_frame_mod = b.addModule("qrtp_frame", .{
    .root_source_file = b.path("src/qrtp_frame.zig"),
    .imports = &.{ .{ .name = "fountain", .module = fountain_mod } },
});
```

## Core Patterns

### Explicit Allocators

```zig
const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit();

    try list.appendSlice("hello");
}
```

### Error Handling

```zig
fn readFile(path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();
    return file.readToEndAlloc(allocator, 1024 * 1024);
}

// Usage with catch
const data = readFile("config.txt") catch |err| {
    std.log.err("Failed: {}", .{err});
    return err;
};
```

### Comptime Metaprogramming

```zig
fn Vec(comptime T: type, comptime N: usize) type {
    return struct {
        data: [N]T,

        const Self = @This();

        pub fn dot(self: Self, other: Self) T {
            var sum: T = 0;
            inline for (0..N) |i| {
                sum += self.data[i] * other.data[i];
            }
            return sum;
        }
    };
}

const Vec3 = Vec(f32, 3);
```

### Defer/Errdefer

```zig
fn process() !void {
    const resource = try acquire();
    defer release(resource);  // Always runs

    const temp = try allocate();
    errdefer free(temp);  // Only on error

    try doWork(resource, temp);
    // temp ownership transferred, no errdefer needed
}
```

### C Interop

```zig
const c = @cImport({
    @cInclude("stdio.h");
    @cInclude("mylib.h");
});

pub fn main() void {
    _ = c.printf("Hello from C\n");
}
```

## Emerging Patterns (zig-syrup)

### Pattern 1: SplitMix64 Bijection (Gay.jl Integration)

Comptime modular multiplicative inverse via Newton's method. Enables invertible hashing
with Strong Parallelism Invariance (SPI): same `(seed, index)` gives the same result
regardless of call order or parallelism.

```zig
pub const SplitMix64 = struct {
    pub const GOLDEN: u64 = 0x9e3779b97f4a7c15;
    pub const MIX1: u64 = 0xbf58476d1ce4e5b9;
    pub const MIX2: u64 = 0x94d049bb133111eb;
    pub const MIX1_INV: u64 = modInverse64(MIX1);
    pub const MIX2_INV: u64 = modInverse64(MIX2);
    state: u64,

    /// Forward bijection: deterministic, invertible.
    pub fn mix(x: u64) u64 {
        var z = x +% GOLDEN;
        z = (z ^ (z >> 30)) *% MIX1;
        z = (z ^ (z >> 27)) *% MIX2;
        return z ^ (z >> 31);
    }

    /// Inverse: unmix(mix(x)) == x for all x.
    pub fn unmix(z: u64) u64 {
        var x = z;
        x ^= x >> 31; x ^= x >> 62;
        x *%= MIX2_INV;
        x ^= x >> 27; x ^= x >> 54;
        x *%= MIX1_INV;
        x ^= x >> 30; x ^= x >> 60;
        x -%= GOLDEN;
        return x;
    }

    /// O(1) random access. SPI-compatible.
    pub fn colorAt(seed: u64, index: u64) u64 {
        return mix(seed ^ index);
    }

    /// Comptime modular inverse mod 2^64 via Newton's method.
    fn modInverse64(a: u64) u64 {
        @setEvalBranchQuota(10000);
        var x: u64 = a;
        x *%= 2 -% a *% x; // doubling correct bits each step
        x *%= 2 -% a *% x;
        x *%= 2 -% a *% x;
        x *%= 2 -% a *% x;
        x *%= 2 -% a *% x; // 64 bits converged
        return x;
    }
};
```

**Key insight**: `modInverse64` runs entirely at comptime — `MIX1_INV` and `MIX2_INV` are compile-time constants. The `@setEvalBranchQuota` is necessary for the comptime evaluator.

### Pattern 2: Three-Mode Tagged Union PRNG

Tagged union for GF(3)-aligned PRNG modes. Each mode has a distinct role:

```zig
pub const PrngMode = enum {
    splitmix,  // -1 (MINUS): bijective, invertible, SPI. Default.
    xoshiro,   //  0 (ERGODIC): fast, non-cryptographic.
    chacha,    // +1 (PLUS): CSPRNG for identity proofs.
};

pub const Prng = union(PrngMode) {
    splitmix: SplitMix64,
    xoshiro: std.Random.Xoshiro256,
    chacha: std.Random.ChaCha,

    pub fn init(prng_mode: PrngMode, seed: u64) Prng {
        return switch (prng_mode) {
            .splitmix => .{ .splitmix = SplitMix64.init(seed) },
            .xoshiro => .{ .xoshiro = std.Random.Xoshiro256.init(seed) },
            .chacha => initChaCha(seed),
        };
    }

    pub fn next(self: *Prng) u64 {
        return switch (self.*) {
            .splitmix => |*s| s.next(),
            .xoshiro => |*x| x.next(),
            .chacha => |*c| c.random().int(u64),
        };
    }

    // IMPORTANT: Don't name a method the same as the active tag field.
    // Use `activeMode` instead of `mode` to avoid shadowing.
    pub fn activeMode(self: *const Prng) PrngMode {
        return self.*;
    }
};
```

**Gotcha**: `pub fn mode(self)` would shadow the union's internal `mode` tag — renamed to `activeMode`.

### Pattern 3: C ABI Callback Abstraction

Platform-agnostic callbacks for hardware interaction (QRTP QR code rendering):

```zig
/// Platform renders QR code from raw bytes. Returns 0 on success.
pub const RenderQRFn = *const fn (
    data: [*]const u8,
    data_len: usize,
    context: ?*anyopaque,
) callconv(.c) c_int;

/// Platform scans QR code from camera. Returns decoded length, 0 if none.
pub const ScanQRFn = *const fn (
    buf: [*]u8,
    buf_len: usize,
    context: ?*anyopaque,
) callconv(.c) usize;

pub const TransportConfig = struct {
    render_qr: RenderQRFn,
    scan_qr: ScanQRFn,
    delay: DelayFn,
    context: ?*anyopaque = null,
    frame_delay_ms: u32 = 100,
};
```

**Gotcha (0.15.2)**: Use `callconv(.c)` (lowercase). `callconv(.C)` is a compile error.

### Pattern 4: SIMD XOR Block Combining

Fixed-size blocks enable SIMD vectorization without allocations:

```zig
pub fn xorBlocks(dst: []u8, src: []const u8) void {
    const len = @min(dst.len, src.len);
    const vec_len = 16;
    const full_vecs = len / vec_len;
    var i: usize = 0;

    while (i < full_vecs * vec_len) : (i += vec_len) {
        const d: @Vector(vec_len, u8) = dst[i..][0..vec_len].*;
        const s: @Vector(vec_len, u8) = src[i..][0..vec_len].*;
        dst[i..][0..vec_len].* = d ^ s;
    }

    // Scalar tail
    while (i < len) : (i += 1) {
        dst[i] ^= src[i];
    }
}
```

### Pattern 5: Sheaf-Theoretic Decoder (Bumpus StructuredDecompositions.jl)

Fountain decoder maps to adhesion_filter from Bumpus's tree decompositions:
- Source blocks = bags in the tree decomposition
- Encoded blocks = adhesion spans between bags
- XOR = pullback projection on the adhesion
- Belief propagation = sheaf consistency filtering

```zig
/// Fountain decoder with adhesion_filter alias.
pub const Decoder = struct {
    // ... source blocks, state, pending buffer ...

    /// Public alias: StructuredDecompositions.jl naming convention.
    pub fn adhesionFilter(self: *Decoder) bool {
        return self.propagate();
    }

    /// Sheaf consistency propagation:
    /// When a bag (source block) is solved, check all adhesion spans
    /// (pending encoded blocks) for newly degree-1 solvable entries.
    fn propagate(self: *Decoder) bool {
        var progress = true;
        while (progress) {
            progress = false;
            // XOR out known blocks from pending, solve degree-1 entries
            // ... (see fountain.zig for full implementation)
        }
        return progress;
    }
};
```

### Pattern 6: Compact Binary Framing (QRTP)

Fixed-layout binary serialization without allocators, fitting QR code capacity:

```zig
pub fn encodeFrame(block: *const fountain.EncodedBlock) QrtpFrame {
    var frame = QrtpFrame{};
    var pos: usize = 0;

    @memcpy(frame.data[pos..][0..4], "qrtp");  // 4-byte tag
    pos += 4;
    frame.data[pos] = PROTOCOL_VERSION;         // 1-byte version
    pos += 1;
    writeU64BE(frame.data[pos..], block.seed);  // 8-byte big-endian
    pos += 8;
    // ... indices, payload ...

    frame.len = pos;
    return frame;
}
```

## Zig 0.15.2 Gotchas

| Issue | Wrong | Right |
|-------|-------|-------|
| C calling convention | `callconv(.C)` | `callconv(.c)` |
| Unused module const | `const m = b.addModule(...); _ = m;` | `_ = b.addModule(...)` |
| Method name = tag field | `pub fn mode(self)` on `union(PrngMode)` | `pub fn activeMode(self)` |
| Hex literal | `0xGAY`, `0xPASS` | Only `[0-9a-fA-F]` valid |
| Wrapping arithmetic | `a + b` (overflow trap) | `a +% b` (wrapping) |

## Version Detection

```zig
// Feature detection over version checks
const has_new_api = @hasDecl(std, "Build");
const T = if (has_new_api) std.Build else std.build.Builder;
```

## Debug

```zig
std.debug.print("value: {any}\n", .{x});
std.log.info("structured: {}", .{data});
@breakpoint();  // Debugger trap
```

## Cross-Compile Targets

```bash
# List all targets
zig targets | jq '.native'

# Common targets
zig build -Dtarget=x86_64-linux-gnu
zig build -Dtarget=aarch64-macos
zig build -Dtarget=wasm32-wasi
zig build -Dtarget=thumb-none-eabi  # Embedded
```

## Reference: zig-syrup Module Map

| Module | LOC | Trit | Role |
|--------|-----|------|------|
| `fountain.zig` | 907 | +1 | Luby Transform encoder/decoder, 3-mode PRNG |
| `qrtp_frame.zig` | 427 | 0 | Binary framing for QR/TCP transport |
| `qrtp_transport.zig` | 403 | -1 | Send/recv via C ABI QR callbacks |
| `message_frame.zig` | — | 0 | TCP length-prefixed framing |
| `tcp_transport.zig` | — | -1 | TCP OCapN transport |
| `propagator.zig` | — | 0 | Scoped propagators (lattice cells) |
| `color.zig` | — | +1 | Gay.jl Okhsl color space |

## Related Skills

| Skill | Trit | Role |
|-------|------|------|
| zig-programming | -1 | 223 recipes, full docs |
| rama-gay-zig | -1 | Rama + Gay.jl + Zig interleave |
| structured-decomp | 0 | Bumpus tree decompositions |
| **zig** | -1 | Ecosystem wrapper + emerging patterns |

## GF(3) Triads

```
zig(-1) ⊗ zls-integration(0) ⊗ c-interop(+1) = 0 ✓
zig(-1) ⊗ acsets(0) ⊗ gay-mcp(+1) = 0 ✓  [Schema coloring]
zig(-1) ⊗ babashka(0) ⊗ duckdb-ies(+1) = 0 ✓  [Build analytics]
zig(-1) ⊗ structured-decomp(0) ⊗ fountain(+1) = 0 ✓  [Sheaf decoder]
zig(-1) ⊗ qrtp-frame(0) ⊗ qrtp-transport(+1) = 0 ✓  [Air-gapped transport]
```

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 2. Domain-Specific Languages

**Concepts**: DSL, wrapper, pattern-directed, embedding

### GF(3) Balanced Triad

```
zig (−) + SDF.Ch2 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch6: Layering
- Ch7: Propagators (fountain decoder = belief propagation)

### Connection Pattern

DSLs embed domain knowledge. This skill defines domain-specific operations.

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule:

```
Trit: -1 (MINUS/Validator)
Home: Prof
Poly Op: ⊗
Kan Role: Ran (right Kan extension)
Color: #3B82F6 (blue)
```

### Why -1 (MINUS)?

Zig validates and constrains:
- No hidden allocations
- No hidden control flow
- No exceptions
- Explicit error handling
- Compile-time safety checks

The language itself is a **validator** — it refuses to compile unsafe patterns.

### zig-syrup Cat# Morphisms

```
fountain.Encoder (+1, Lan_K) →[qrtp_frame (0, Adj)]→ qrtp_transport (-1, Ran_K)
  Presheaves                     Prof                    Span

SplitMix64.mix (−1, Ran) ↔ SplitMix64.unmix (−1, Ran)
  Bijection = isomorphism in Cat#, self-dual in Span
```

## Philosophy

> "Zig is not designed to make fancy high-level things.
> It's designed to make it easy to write correct low-level code."

- Explicit over implicit
- Compile-time over runtime
- No hidden control flow
- Allocator-aware by design
- C interop without FFI overhead
- SPI: same seed → same output regardless of execution order