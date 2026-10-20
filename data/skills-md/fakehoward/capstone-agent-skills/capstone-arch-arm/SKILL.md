---
name: capstone-arch-arm
description: >-
  Guides Capstone ARM (A32/Thumb) disassembly: valid modes, Thumb interworking,
  cs_arm detail/operands, aliases, and regs_access. Use when the task involves
  CS_ARCH_ARM, CS_MODE_THUMB/MCLASS/V8, include/capstone/arm.h, ARMModule, or
  ARM-specific Capstone options and traps.
---

# Capstone ARM

Load only this skill for ARM A32/Thumb work. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/arm.h` — `cs_arm`, operand types
- `arch/ARM/ARMModule.c` — init, `CS_OPT_MODE` / `CS_OPT_SYNTAX`
- `cs.c` — `CS_ARCH_CONFIG_ARM` allowed mask, skipdata size
- `tests/details/arm.yaml`, `tests/MC/ARM/`

## Valid modes

Allowed bits (`CS_ARCH_CONFIG_ARM`): `CS_MODE_LITTLE_ENDIAN` (0), `CS_MODE_ARM` (0), `CS_MODE_THUMB`, `CS_MODE_MCLASS`, `CS_MODE_V8`, `CS_MODE_BIG_ENDIAN`.

Typical opens:

| Target | Mode |
|--------|------|
| A32 LE | `CS_MODE_ARM` or `0` |
| Thumb/Thumb-2 | `CS_MODE_THUMB` |
| Cortex-M | `CS_MODE_THUMB \| CS_MODE_MCLASS` |
| ARMv8 A32 | `CS_MODE_ARM \| CS_MODE_V8` (or Thumb+V8) |
| BE | OR `CS_MODE_BIG_ENDIAN` |

Runtime `CS_OPT_MODE` **ORs** bits (`handle->mode |= value`). Bits cannot be cleared without `cs_close` + reopen.

## Options and syntax

- Detail: `CS_OPT_DETAIL` / `CS_OPT_DETAIL_REAL` (alias vs real operands)
- Syntax: `CS_OPT_SYNTAX_CS_REG_ALIAS` for legacy Capstone register names (r9=sb, …); naive text replace — costly at scale
- Branch immediates: `CS_OPT_ONLY_OFFSET_BRANCH` (shared option; ARM supported)
- Skipdata default stride: 2 in Thumb, 4 in A32

## Detail, alias, regs_access

- Detail union member: `insn->detail->arm` (`cs_arm`, up to 36 ops)
- Auto-Sync alias: `is_alias`, `alias_id`, `usesAliasDetails` supported
- `cs_regs_access`: supported (`ARM_reg_access`, unavailable in DIET)

## Workflow

1. `cs_open(CS_ARCH_ARM, mode, &handle)` with a valid combination above.
2. Enable detail if operands/regs/groups are needed.
3. For Thumb interworking after BX/BLX, `cs_option(handle, CS_OPT_MODE, CS_MODE_THUMB)` (OR semantics).
4. Read `cs_arm` fields: `cc`, `vcc`, `post_index`, `pred_mask`, `operands[]`; `detail->writeback` for writeback.
5. Prefer `CS_OPT_DETAIL_REAL` when analyzing canonical encodings of aliases.

## Traps

- Mode OR accumulates; switching Thumb→ARM mid-stream requires reopen.
- `MCLASS` / `V8` tighten decode; wrong feature mode yields different or failed decode.
- Post-index: displacement lives in the MEM operand; `mem.disp` is non-negative and `subtracted` marks subtract.
- System/banked regs use dedicated operand types (`ARM_OP_SYSREG`, …), not plain `ARM_OP_REG`.

## More

- Modes, structs, traps: [reference.md](reference.md)
- Open/disasm snippets: [examples.md](examples.md)
