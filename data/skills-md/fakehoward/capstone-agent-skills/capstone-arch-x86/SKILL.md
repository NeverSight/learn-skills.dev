---
name: capstone-arch-x86
description: >-
  Guides Capstone x86/x86-64 disassembly: 16/32/64 modes, Intel/ATT/MASM syntax,
  cs_x86 encoding detail, and regs_access. Use when the task involves CS_ARCH_X86,
  include/capstone/x86.h, X86Module, prefixes/ModRM/SIB, or x86-specific Capstone
  build options (ATT disable, X86_REDUCE).
---

# Capstone x86

Load only this skill for x86/x64. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/x86.h` — `cs_x86`, encoding, eflags
- `arch/X86/X86Module.c` — syntax printers, mode replace
- `cs.c` — `CS_ARCH_CONFIG_X86`
- `tests/details/x86.yaml`, `tests/MC/X86/`, and issue YAML under
  `tests/issues/` matching glob `x86-*.yaml` (not a single literal path)

## Valid modes

Allowed: `CS_MODE_LITTLE_ENDIAN` (0), `CS_MODE_16`, `CS_MODE_32`, `CS_MODE_64`.

Big-endian is **not** allowed. Pick one width:

| Target | Mode |
|--------|------|
| 16-bit | `CS_MODE_16` |
| 32-bit | `CS_MODE_32` |
| 64-bit | `CS_MODE_64` |

Runtime `CS_OPT_MODE` **replaces** `handle->mode` and switches `regsize_map` (64 vs 32/16 map).

## Options and syntax

Default at init: Intel printer + `CS_OPT_SYNTAX_INTEL`.

| Value | Effect |
|-------|--------|
| `CS_OPT_SYNTAX_INTEL` / `DEFAULT` | Intel printer |
| `CS_OPT_SYNTAX_MASM` | Intel printer + MASM syntax flag |
| `CS_OPT_SYNTAX_ATT` | ATT printer; `CS_ERR_X86_ATT` if `CAPSTONE_X86_ATT_DISABLE`; `CS_ERR_DIET` in diet |
| Other syntax values | `CS_ERR_OPTION` |

Skipdata stride: 1.

## Detail, alias, regs_access

- Detail: `insn->detail->x86` (`cs_x86`) — `prefix[4]`, `opcode[4]`, `rex`, `modrm`, `sib`, `disp`, encoding offsets, eflags/FPU flags, up to 8 ops (`REG`/`IMM`/`MEM`)
- Auto-Sync `is_alias` / `alias_id`: **not** used by the X86 backend (no alias mapping hooks under `arch/X86/`)
- `cs_regs_access`: supported (`X86_reg_access`, not in DIET)

## Workflow

1. `cs_open(CS_ARCH_X86, CS_MODE_32 or CS_MODE_64, &handle)`.
2. Optionally set ATT/MASM via `CS_OPT_SYNTAX`.
3. Enable detail for prefixes, ModRM/SIB, encoding offsets, eflags.
4. Use `X86_REL_ADDR(insn)` helper from `x86.h` when resolving relative targets from detail.
5. For reduced ISA builds, check `cs_support(CS_SUPPORT_X86_REDUCE)`.

## Traps

- Wrong width mode mis-decodes (especially 16 vs 32 addressing).
- ATT unavailable under diet or `CAPSTONE_X86_ATT_DISABLE`.
- `CAPSTONE_X86_REDUCE` shrinks tables/insn coverage; full-ISA expectations fail.
- Mode replace overwrites previous width; unlike ARM, no bit OR.

## More

- Encoding fields and build flags: [reference.md](reference.md)
- Snippets: [examples.md](examples.md)
