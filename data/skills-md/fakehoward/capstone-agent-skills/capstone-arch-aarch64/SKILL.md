---
name: capstone-arch-aarch64
description: >-
  Guides Capstone AArch64 disassembly: modes including Apple proprietary,
  cs_aarch64 detail/sysops/SME, aliases, and regs_access. Use when the task
  involves CS_ARCH_AARCH64 or CS_ARCH_ARM64, aarch64.h / arm64.h, AArch64Module,
  SME/SVE/sysreg operands, or AArch64-specific Capstone options.
---

# Capstone AArch64

Load only this skill for AArch64. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/aarch64.h` — `cs_aarch64`, operand types
- `include/capstone/arm64.h` — compatibility typedefs/macros
- `arch/AArch64/AArch64Module.c`
- `cs.c` — `CS_ARCH_CONFIG_AARCH64`
- `tests/details/aarch64.yaml`, `tests/MC/AArch64/`

## Valid modes

Allowed (`CS_ARCH_CONFIG_AARCH64`): `CS_MODE_LITTLE_ENDIAN` (0), `CS_MODE_ARM` (0), `CS_MODE_BIG_ENDIAN`, `CS_MODE_APPLE_PROPRIETARY` (`1 << 30`).

| Target | Mode |
|--------|------|
| AArch64 LE (default) | `0` / `CS_MODE_LITTLE_ENDIAN` |
| BE | `CS_MODE_BIG_ENDIAN` |
| Apple proprietary (AMX, …) | OR `CS_MODE_APPLE_PROPRIETARY` |

`CS_MODE_AARCH64_ISA_BITS` exists in the header but ISA extensions are not selected via those bits in the current allowed mask.

Runtime `CS_OPT_MODE` **ORs** bits. Clear bits only by reopen.

Arch id: `CS_ARCH_AARCH64` equals `CS_ARCH_ARM64` (same value). Prefer `AARCH64` names; use `arm64.h` only with the compat define when migrating old code.

## Options and syntax

- Detail: `CS_OPT_DETAIL`, `CS_OPT_DETAIL_REAL`
- `CS_OPT_SYNTAX_CS_REG_ALIAS` — legacy fp/lr-style names in asm text
- `CS_OPT_SYNTAX_AARCH64_EXPLICIT_WIDE_IMM` — print shifted `MOVN`/`MOVZ` instead of `MOV` alias form
- `CS_OPT_ONLY_OFFSET_BRANCH`
- Skipdata stride: 4

## Detail, alias, regs_access

- Detail: `insn->detail->aarch64` (`cs_aarch64`, up to 16 ops)
- Operand surface includes MEM/MEM_REG/MEM_IMM, sysops (`SYSREG`, `SYSALIAS`, …), SME, PRED, IMM_RANGE
- Auto-Sync alias fields supported
- `cs_regs_access`: supported (`AArch64_reg_access`, not in DIET)

## Workflow

1. `cs_open(CS_ARCH_AARCH64, mode, &handle)`.
2. Enable detail for sysops/SME/vector layout (`vas`, `is_vreg`).
3. For Apple-only encodings, OR `CS_MODE_APPLE_PROPRIETARY` at open or via `CS_OPT_MODE`.
4. Inspect `cc`, `update_flags`, `post_index`, `operands[]`; check `detail->writeback`.
5. Use `CS_OPT_DETAIL_REAL` when alias operand sets must be ignored.

## Traps

- Mode OR cannot drop `APPLE_PROPRIETARY` or endian without reopen.
- Compat header rename: old `arm64_*` / `cs_arm64` only via `arm64.h` + `CAPSTONE_AARCH64_COMPAT_HEADER`.
- Post-index displacement is in the MEM operand; `mem.disp` is `int64_t`.
- Q/V registers share ids; `is_vreg` selects V interpretation.

## More

- Structs and mode notes: [reference.md](reference.md)
- Snippets: [examples.md](examples.md)
