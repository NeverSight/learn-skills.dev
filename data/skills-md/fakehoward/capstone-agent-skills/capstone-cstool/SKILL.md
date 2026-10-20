---
name: capstone-cstool
description: >-
  Uses Capstone cstool to disassemble hex strings with arch+mode selectors and
  detail flags. Use when running cstool, decoding hex dumps, enabling -d/-r/-a
  detail output, checking build-time arch support via -v, or building the
  cstool target with CAPSTONE_BUILD_CSTOOL.
---

# Capstone cstool

## Build

Root CMake builds `cstool` when `CAPSTONE_BUILD_CSTOOL` is ON (default for
top-level configures). Binary lands in the build tree and installs to bindir
when install is enabled.

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target cstool
```

## Invocation

```text
cstool [-d|-a|-r|-s|-u|-v] <arch+opts> <assembly-hexstring> [start-address-hex]
```

Hex input is flexible: spaces, `0x`, `\x`, commas, semicolons, `+`, `:` all work
(see `cstool/README.md`).

## Useful flags

| Flag | Meaning |
|------|---------|
| `-d` | Detail mode |
| `-r` | Real (non-alias) detail |
| `-a` | Capstone register aliases instead of LLVM names |
| `-s` | SKIPDATA |
| `-u` | Unsigned immediates |
| `-v` | Version and which arches the linked core includes |

Run `cstool` with no args (or `-h`) for the arch+mode table supported by that
binary.

## Agent rules

1. Pick `<arch+opts>` from the tool’s own help for that build; names differ
   from raw `cs_mode` enums.
2. For fuzz crash repro hex, pad single-digit bytes (`0x03` not `0x3`) — see
   the fuzzing skill.
3. Do not assume every arch string exists if the core was built with arches off.

## More detail

- Output columns and detail behavior: [reference.md](reference.md)
- Example commands: [examples.md](examples.md)
- Package fixture smoke (may SKIP without toolchain): package script
  `scripts/runtime_smoke.py`
