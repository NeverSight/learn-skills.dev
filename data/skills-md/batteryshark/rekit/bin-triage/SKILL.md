---
name: bin-triage
description: "Fast format-agnostic first look at any file, pure-stdlib: identify format from magic bytes (and route to the right analyzer), chunked Shannon entropy (packed/encrypted regions), string extraction with interesting-string surfacing (URLs/IPs/onion/shell/paths/exec-APIs), and an embedded-signature scan (mini-binwalk: ZIP/gzip/ELF/PDF at non-zero offsets). When given an output dir, also CARVES large embedded readable-source regions (the JS/text a single-file executable — Bun/Deno/pkg/nexe/SEA — appends after its native runtime) for rescanning. Emits BINARY.* atoms. Read-only — never executes the input."
---

# Binary Triage (format-agnostic)

A fast first look at *any* file, with no external tools. Pure-Python stdlib,
read-only. Use it when you don't yet know what you're holding.

## When to use

An unknown blob shows up — a dropped file, an attachment, a chunk carved out of
something bigger. Run this to learn what it is and where to look next; it routes you
to the format-specific analyzer (`pe-analyze`, `elf-analyze`, `macho-analyze`,
`dotnet-analyze`) or to `unpack` for archives.

## What it does

1. **Identify** — format from magic bytes (ELF/PE/Mach-O/DEX/WASM, ZIP/gzip/xz/7z/
   RAR/CAB/zstd/tar, PDF/PNG/JPEG, scripts) and a **route** to the right skill.
2. **Entropy** — Shannon entropy in 4 KiB chunks → flags packed/encrypted/compressed
   regions (`BINARY.HIGH_ENTROPY`, with the % of the file and first offset).
3. **Strings** — ASCII + UTF-16LE, surfacing interesting ones: URLs, IPs, `.onion`
   addresses, shell/exec cues (`/bin/sh`, `cmd.exe`, `powershell`), Windows paths,
   and exec/inject API names (`BINARY.INTERESTING_STRING`).
4. **Embedded scan** — a lightweight **mini-binwalk**: known signatures (ZIP, gzip,
   xz, 7z, ELF, PDF, PNG, zstd) found at **non-zero offsets** → `BINARY.EMBEDDED`.
   For actual carving/extraction of embedded filesystems use `binwalk-carve`.

Strictly **read-only** — reads bytes only, never parses as code or executes.

## Usage

```bash
rekit run bin-triage ./unknown.bin
rekit run bin-triage ./firmware.img --format json
```

## Prerequisites

- **python3 ≥ 3.8** — pure stdlib, nothing to vendor.
