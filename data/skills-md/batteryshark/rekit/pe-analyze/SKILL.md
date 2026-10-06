---
name: pe-analyze
description: "Static triage of Windows PE binaries (EXE/DLL) with pefile: machine/arch, subsystem, entry/imagebase, sections + per-section entropy (packing) and RWX flags, imports classified by capability (inject/exec/network/anti-debug/persist/crypto), exports, TLS callbacks, overlay, and Authenticode presence. Emits BINARY.* atoms. Reads structure only — never runs the binary."
---

# PE Binary Analyzer

Static triage of Windows PE binaries (EXE, DLL, SYS, `.node`) with
[pefile](https://github.com/erocarrera/pefile).

## When to use

You have a Windows binary and want a fast read on what it is and whether it looks
malicious — without running it. Pair it with `hex-view`; its `BINARY.*` atoms provide
structured evidence for downstream analysis.

## What it reports

- **Header** — machine/arch, EXE vs DLL, subsystem, entry point, image base, build
  timestamp, Authenticode signature presence (`BINARY.NO_SIGNATURE`).
- **Sections** — name, virtual/raw size, **Shannon entropy** (packing tell →
  `BINARY.HIGH_ENTROPY`), and writable+executable flags (`BINARY.RWX_SECTION`).
- **Imports** — DLLs and functions, classified by capability
  (inject / exec / network / anti-debug / persist / crypto) →
  `BINARY.SUSPICIOUS_IMPORT`.
- **Heuristics** — high entropy + almost no imports → `BINARY.PACKED`; TLS callbacks
  (code before entry) → `BINARY.TLS_CALLBACK`; appended `BINARY.OVERLAY`.

Strictly **static** — parses structure via pefile and never loads, maps, or executes
the binary. Safe on hostile files.

## Usage

```bash
rekit run pe-analyze ./sample.exe
rekit run pe-analyze ./driver.sys --format json
```

Non-PE input fails honestly (`{"ok": false, "error": "not a valid PE: …"}`).

## Prerequisites

- **python3 ≥ 3.8** — pefile is installed under `scripts/site` (pure-python), so no
  network/install at analysis time.

## Rebuilding

`scripts/site` is populated from the pinned `scripts/requirements.txt` by
`scripts/build.sh` (`uv pip install --target`, build time only).
