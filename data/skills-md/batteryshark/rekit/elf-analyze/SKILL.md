---
name: elf-analyze
description: "Static triage of ELF binaries (Linux/BSD) with pyelftools: class/arch/type, sections + per-section entropy (packing), needed libraries, RPATH/RUNPATH, imported symbols classified by capability (network/exec/inject/load/crypto), and hardening (PIE/NX/RELRO). Emits BINARY.* atoms. Reads structure only — never runs the binary."
---

# ELF Binary Analyzer

Static triage of ELF binaries (Linux/BSD executables, shared objects, relocatable
objects) with [pyelftools](https://github.com/eliben/pyelftools).

## When to use

You have a Linux binary or `.so` and want a fast read on what it is and whether it
looks suspicious — without running it. Pair it with `hex-view`; its `BINARY.*` atoms
provide structured evidence for downstream analysis.

## What it reports

- **Header** — ELF32/64, endianness, machine/arch, type (EXEC/DYN/REL), entry point.
- **Sections** — name, size, and **Shannon entropy** (a high-entropy section is a
  packing/encryption tell) → `BINARY.HIGH_ENTROPY`.
- **Dynamic** — needed libraries, and `RPATH`/`RUNPATH` (a `.so` search-path hijack
  surface) → `BINARY.RPATH`.
- **Imports** — undefined dynamic symbols, classified by capability
  (network / exec / inject / load / crypto) → `BINARY.INTERESTING_IMPORT`.
- **Hardening** — PIE, NX (executable stack → `BINARY.EXEC_STACK`), RELRO,
  text relocations (`BINARY.TEXTREL`).

It is strictly **static** — it parses structure via pyelftools and never loads,
maps, or executes the binary. Safe on hostile files.

## Usage

```bash
rekit run elf-analyze ./suspicious.so
rekit run elf-analyze ./payload --format json
```

Non-ELF input fails honestly (`{"ok": false, "error": "not a valid ELF: …"}`).

## Prerequisites

- **python3 ≥ 3.8** — pyelftools is installed under `scripts/site` (pure-python), so
  there's no network/install at analysis time.

## Rebuilding

`scripts/site` is populated from the pinned `scripts/requirements.txt` by
`scripts/build.sh` (`uv pip install --target`, build time only).
