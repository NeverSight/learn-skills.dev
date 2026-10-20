---
name: capstone-fuzzing-crash-repro
description: >-
  Reproduces Capstone OSS-Fuzz and suite/fuzz crashes by decoding the platform
  byte and replaying padded hex through cstool. Use when triaging fuzz reports,
  converting fuzzer inputs to cstool commands, building fuzz_disasm /
  fuzz_decode_platform, or handling suite/fuzz drivers.
---

# Capstone fuzzing crash reproduction

## Input layout

Fuzz payloads (OSS-Fuzz style) encode:

1. **Byte 0** — platform index → Capstone arch+mode (`suite/fuzz/platform.c`)
2. **Remaining bytes** — code fed to the disassembler

Decode byte 0 with `fuzz_decode_platform` (built from `suite/fuzz` via its
Makefile, or compile `fuzz_decode_platform.c` + `platform.c` against Capstone):

```bash
./fuzz_decode_platform 0x7
# → cstool arch+mode = aarch64
```

Alternatively read `platforms[]` in `suite/fuzz/platform.c` for the same mapping.

## Reproduce with cstool (padded hex)

From an OSS-Fuzz dump like `0x7,0xe8,0x3,0x4e,0xc0,0xf8,`:

```bash
# Skip the platform byte; pad every hex to two digits (0x3 → 0x03)
cstool -d aarch64 0xe8,0x03,0x4e,0xc0,0xf8,
```

Unpadded values break cstool parsing. This is the main gotcha in
`suite/fuzz/README.md`.

## What the repo actually builds

| Path | Reality |
|------|---------|
| Root CMake `fuzz_disasm` | Always added: `onefile.c` + `fuzz_disasm.c` + `platform.c` |
| `fuzz_decode_platform` | Not a root CMake target; produced by `suite/fuzz/Makefile` (or manual compile) |
| `suite/fuzz/Makefile` | Legacy Make helpers (`fuzz_bindisasm`, `fuzz_bindisasm2`, decode tool, …); needs static Capstone via Make |
| OSS-Fuzz | External project `google/oss-fuzz` `projects/capstone` |

Do not assume a libFuzzer CI job or `.travis.yml` in-tree (none present).

## Agent rules

1. Always pad hex digits for cstool repros.
2. Map platform byte before guessing arch.
3. Prefer CMake `fuzz_disasm` plus `platform.c` mapping (or Makefile decode tool) over inventing harnesses.
4. Sanitizer Make recipes in `suite/fuzz/README.md` are optional developer paths.

## More detail

- Drivers and platform table: [reference.md](reference.md)
- End-to-end repro steps: [examples.md](examples.md)
