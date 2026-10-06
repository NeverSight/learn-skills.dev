---
name: native-decompile
description: "Decompile a native binary (ELF/PE/Mach-O) to C-like pseudocode with rizin's built-in Ghidra decompiler (pdg over all functions). Static: analyses and decompiles, never runs the target. Prereq-gated on rizin/r2; honest blind spot with an install hint when absent. Pair with elf/pe/macho-analyze."
---

# Native Decompiler

Decompile a native binary (ELF / PE / Mach-O) to C-like pseudocode with
[rizin](https://rizin.re)'s built-in Ghidra decompiler.

## When to use

A native executable/library you need to read past the disassembly. Triage with
`elf`/`pe`/`macho-analyze` first (arch, imports, packing), then decompile.

## What it does

Runs `rizin -q -c "aaa; pdg @@F" <input>` — analyse everything, then decompile every
function with rizin's built-in Ghidra decompiler (`pdg`) — and writes the pseudocode
to `outdir/decompiled.c`. Static: rizin analyses and decompiles; it never runs or
emulates the target.

## Prerequisites

- **python3** (runner) and **`rizin`** (or `r2`) on PATH. rizin is a large native
  toolchain, so it is **not bundled** — install from <https://rizin.re>. Its `pdg`
  gives you Ghidra-quality decompilation without a separate Ghidra/JVM install. Until
  it's present, `doctor` marks the skill not-ready and `run` reports the honest gap.

## Usage

```bash
rekit run native-decompile ./suspicious.elf ./out
```
