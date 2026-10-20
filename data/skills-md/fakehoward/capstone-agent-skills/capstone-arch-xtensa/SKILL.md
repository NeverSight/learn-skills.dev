---
name: capstone-arch-xtensa
description: >-
  Guides Capstone Xtensa disassembly: ESP chip modes, CS_OPT_LITBASE for L32R,
  CS_OPT_MODE OR semantics, cs_xtensa detail, and regs_access. Use when working
  with CS_ARCH_XTENSA, xtensa.h, XtensaModule, ESP32/S2/S3/ESP8266, or LITBASE.
---

# Capstone Xtensa

Load only this skill for Xtensa work. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/xtensa.h` — `cs_xtensa`, `XTENSA_OP_L32R`
- `arch/Xtensa/XtensaModule.c` — init, `CS_OPT_LITBASE`, mode OR
- `cs.c` — `CS_ARCH_CONFIG_XTENSA`, skipdata (see warning)
- `tests/details/xtensa.yaml`, `tests/MC/Xtensa/`,
  `tests/integration/test_litbase.c`

## Valid modes

Allowed chip bits: `CS_MODE_XTENSA_ESP32`, `ESP32S2`, `ESP8266`, `ESP32S3`
(plus LE = 0). **`CS_MODE_BIG_ENDIAN` is rejected.**

| Target | Mode |
|--------|------|
| ESP32 | `CS_MODE_XTENSA_ESP32` |
| ESP32-S2 | `CS_MODE_XTENSA_ESP32S2` |
| ESP32-S3 | `CS_MODE_XTENSA_ESP32S3` |
| ESP8266 | `CS_MODE_XTENSA_ESP8266` |

`CS_OPT_MODE` **ORs** into `handle->mode` (does not replace). Chip bits may
accumulate; reopen to clear.

## Options and detail

- `CS_OPT_LITBASE` — Extended L32R; LSB=1 enables; base = `value & 0xfffff000`
- Detail → `insn->detail->xtensa` (`format`, up to 8 ops)
- Ops: `REG`, `IMM`, `MEM`, `L32R` (resolved absolute in `.imm`)
- Print aliases (OR→`mov`, etc.): generated but **inactive** (no `PRINT_ALIAS_INSTR`)
- `cs_regs_access`: **supported** (non-DIET)

## Current-tree warning: skipdata default 255

`skipdata_size()` has **no** `CS_ARCH_XTENSA` case → falls through to
`(uint8_t)-1` = **255**. Document this only as a **current-tree warning**, not
as correct ISA alignment (Xtensa sizes are 2/3/4/(6)). Prefer explicit
`CS_OPT_SKIPDATA_SETUP` until fixed.

## Workflow

1. Open with the chip mode needed (S3 for `ee.*` / HiFi3).
2. For Extended L32R: `cs_option(handle, CS_OPT_LITBASE, base | 1)`.
3. Enable detail; call `cs_regs_access` when not DIET.
4. Do not pass big-endian.

## Traps

- Mode OR accumulates chip bits.
- Asm `a1` ↔ enum `XTENSA_REG_SP` (no `XTENSA_REG_A1`).
- Bare mode still decodes much of base+density (features default allow).
- Skipdata 255 is a tree gap, not intended behavior.
- No public `cs_arch_register_xtensa` under `CAPSTONE_USE_ARCH_REGISTRATION`
  (same gap as HPPA) — use compile-time `CAPSTONE_XTENSA_SUPPORT`.

## More

- Modes, LITBASE, registration gap: [reference.md](reference.md)
- Open/disasm snippets: [examples.md](examples.md)
