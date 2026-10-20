---
name: capstone-arch-sparc
description: >-
  Guides Capstone SPARC disassembly: CS_MODE_V9, big/little endian, cs_sparc
  detail (ASI/MEMBAR), aliases, and missing cs_regs_access. Use when the task
  involves CS_ARCH_SPARC, SparcModule, sparc.h, sparcle, or SPARC Capstone
  modes and traps.
---

# Capstone SPARC

Load only this skill for SPARC work. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/sparc.h` — `cs_sparc`, operand types
- `arch/Sparc/SparcModule.c` — init, `CS_OPT_MODE` / `CS_OPT_SYNTAX`
- `cs.c` — `CS_ARCH_CONFIG_SPARC` allowed mask
- `tests/details/sparc.yaml`, `tests/MC/Sparc/`

## Valid modes

Allowed bits: `CS_MODE_LITTLE_ENDIAN` (0), `CS_MODE_BIG_ENDIAN`, `CS_MODE_V9`,
`CS_MODE_64`, `CS_MODE_32`.

| Target | Mode |
|--------|------|
| Typical SPARC | `CS_MODE_BIG_ENDIAN` |
| V9 | `CS_MODE_BIG_ENDIAN \| CS_MODE_V9` |
| sparcle | `CS_MODE_LITTLE_ENDIAN` (+ optional `CS_MODE_V9`) |

`CS_OPT_MODE` **ORs** bits. Setting `CS_MODE_V9` or `CS_MODE_64` forces both
`CS_MODE_V9 | CS_MODE_64`.

## Options and detail

- Detail: `CS_OPT_DETAIL` / `CS_OPT_DETAIL_REAL`
- Union member: `insn->detail->sparc` (`cs_sparc`, up to 6 ops)
- Operand types: `REG`, `IMM`, `MEM`, `MEMBAR_TAG`, `ASI`
- Fields: `cc`, `cc_field`, `hint`, `format`, `op_count`, `operands[]`
- Aliases: yes (`SPARC_INS_ALIAS_*`, `is_alias` / `alias_id`)
- `cs_regs_access`: **not supported** (`ud->reg_access` unset → `CS_ERR_ARCH`)

## Workflow

1. Open with `CS_MODE_BIG_ENDIAN` unless intentionally decoding LE streams.
2. Add `CS_MODE_V9` for V9 encodings (`casx`, named ASI, `membar`, `%xcc`).
3. Enable detail for ops/cc/hint; use `CS_OPT_DETAIL_REAL` for real-alias ops.
4. Read operand-level `access`; do **not** call `cs_regs_access`.

## Traps

- Default Capstone mode is LE (`0`); SPARC code is usually BE — forgetting
  `CS_MODE_BIG_ENDIAN` mis-decodes instruction words.
- Mode OR cannot clear BE; reopen to switch endian.
- Non-V9 LLVM feature bits are not mode-gated (VIS etc. always allowed).
- No `CS_OPT_ALIAS`; use Auto-Sync alias fields / `CS_OPT_DETAIL_REAL`.

## More

- Modes, structs, traps: [reference.md](reference.md)
- Open/disasm snippets: [examples.md](examples.md)
