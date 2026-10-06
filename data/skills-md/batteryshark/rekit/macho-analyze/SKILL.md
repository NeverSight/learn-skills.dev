---
name: macho-analyze
description: "Static triage of Mach-O binaries (macOS/iOS executables, dylibs, bundles, kexts) with macholib: arch/fat slices, file type, PIE, linked dylibs, RPATH, code-signature presence, and encryption (LC_ENCRYPTION_INFO). Emits BINARY.* atoms. Reads structure only — never runs the binary."
---

# Mach-O Binary Analyzer

Static triage of Mach-O binaries (macOS/iOS executables, `.dylib`, bundles, kexts)
with [macholib](https://github.com/ronaldoussoren/macholib).

## When to use

You have a macOS/iOS binary and want a fast read on what it is and whether it looks
suspicious — without running it. This completes the PE/ELF/Mach-O triage trio and
emits `BINARY.*` atoms for downstream analysis.

## What it reports

Per architecture slice (Mach-O can be fat/universal):

- **Header** — CPU/arch, file type (EXECUTE/DYLIB/BUNDLE/KEXT…), PIE (`BINARY.NO_PIE`).
- **Linked dylibs** — every `LC_LOAD_DYLIB`, classified for network/crypto frameworks
  (`BINARY.INTERESTING_LINK`).
- **RPATH** — `LC_RPATH` entries (`@rpath` dylib-hijack surface) → `BINARY.RPATH`.
- **Signature** — `LC_CODE_SIGNATURE` presence → `BINARY.NO_SIGNATURE` when absent.
- **Encryption** — `LC_ENCRYPTION_INFO` with `cryptid` set (protector/DRM, the Mach-O
  packing tell) → `BINARY.ENCRYPTED`.

Strictly **static** — parses load commands via macholib and never loads, maps, or
executes the binary. Safe on hostile files.

## Usage

```bash
rekit run macho-analyze ./suspicious.dylib
rekit run macho-analyze /path/to/app.app/Contents/MacOS/app --format json
```

Non-Mach-O input fails honestly (`{"ok": false, "error": "not a valid Mach-O: …"}`).

## Prerequisites

- **python3 ≥ 3.8** — macholib is installed under `scripts/site` (pure-python), so no
  network/install at analysis time.

## Rebuilding

`scripts/site` is populated from the pinned `scripts/requirements.txt` by
`scripts/build.sh` (`uv pip install --target`, build time only).
