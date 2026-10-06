---
name: emulate-code
description: "Emulate a raw code/shellcode blob on a virtual CPU (x86/x64/arm/arm64) with Unicorn and report the final register state, instruction count, and memory writes. Contained: the bytes run on an emulated CPU, not the host (memory-only; no host syscalls unless wired) — the safe way to 'run' shellcode or an isolated function."
---

# Code Emulator (Unicorn)

Emulate a raw code / shellcode blob on a virtual CPU and see what it computes — the
**contained** member of the dynamic tier (the bytes run on [Unicorn](https://www.unicorn-engine.org),
not the host).

## When to use

You have a chunk of machine code — shellcode carved out of a payload, an obfuscated
decoder stub, an isolated function — and you want to know what it *does* without
running it natively. Emulation gives you the register/memory effects safely.

## What it does

Maps memory + a stack, writes the blob at a base address, and emulates it (x86/x64/
arm/arm64) with an instruction-count and timeout cap. Reports:
- final **register** state,
- **instruction count** and stop reason (completed / fault / instruction-limit),
- **memory writes** (address ← value).
- emulator/backend provenance (version, host/process architecture, native/Rosetta,
  and library digest).

Contained: memory-only, no host syscalls unless explicitly wired. Because it can't
touch the host, it is **not** behind the `--allow-dynamic` gate (unlike `exec-observe`
and the tracer skills, which run the target natively).

## Usage

```bash
rekit run emulate-code ./shellcode.bin --arch x64
rekit run emulate-code ./stub.bin --arch arm64 --base 0x400000 --format json
```

## Prerequisites

- **python3 ≥ 3.8** — Unicorn is installed under `scripts/site` (native; the local
  tree is platform-specific — rebuild with `scripts/build.sh` on a new platform).
- On Apple Silicon, the build also vendors an x86_64 Unicorn runtime when Rosetta is
  available. Doctor probes x87 execution and register access in crash-isolated child
  processes and selects this lane explicitly if native Unicorn is unsafe.

See [`../../docs/UNICORN-X87.md`](../../docs/UNICORN-X87.md) for the macOS ARM64
root cause, reproducer, fallback contract, and qualified environment.
