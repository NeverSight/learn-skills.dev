---
name: capstone-options-syntax
description: >-
  Configures Capstone cs_option values for syntax, mode, mnemonic, unsigned
  immediates, branch offset printing, and LITBASE. Use when setting
  CS_OPT_SYNTAX_*, Intel/ATT/MASM, NO_ALIAS_TEXT, CS_REG_ALIAS, CS_OPT_MODE,
  CS_OPT_MNEMONIC, CS_OPT_UNSIGNED, CS_OPT_ONLY_OFFSET_BRANCH, or CS_OPT_LITBASE.
---

# Capstone options and syntax

Verified: `cs_opt_type` / `cs_opt_value` in `capstone.h`, `cs_option` in `cs.c`,
syntax notes in `docs/cs_v6_release_guide.md`.

## Option dispatch rules

| Type | Storage behavior in current `cs.c` |
| --- | --- |
| `CS_OPT_DETAIL` | `detail_opt |= value` (bits latch; OFF ineffective) |
| `CS_OPT_SKIPDATA` | Boolean `value == CS_OPT_ON` (OFF works) |
| `CS_OPT_UNSIGNED` | Assigned (`OFF`/`ON` work) |
| `CS_OPT_ONLY_OFFSET_BRANCH` | `ON` → print branch imm as offset, not address |
| `CS_OPT_MEM` | Global hooks; handle ignored |
| `CS_OPT_MODE` / `CS_OPT_SYNTAX` / arch-specific | Forwarded to `arch_option` after validation |

Detail semantics → [../capstone-detail-aliases/SKILL.md](../capstone-detail-aliases/SKILL.md).
Skipdata → [../capstone-skipdata/SKILL.md](../capstone-skipdata/SKILL.md).

## Syntax flags (`CS_OPT_SYNTAX`)

Pass one primary dialect unless the arch documents combinations:

| Value | Typical use |
| --- | --- |
| `CS_OPT_SYNTAX_DEFAULT` | Arch default |
| `CS_OPT_SYNTAX_INTEL` | X86 Intel (default on X86) |
| `CS_OPT_SYNTAX_ATT` | X86 AT&T |
| `CS_OPT_SYNTAX_MASM` | X86 MASM |
| `CS_OPT_SYNTAX_NOREGNAME` | Numeric register names where supported |
| `CS_OPT_SYNTAX_MOTOROLA` | MOS65XX `$` hex prefix |
| `CS_OPT_SYNTAX_PERCENT` | PPC `%` register prefix |
| `CS_OPT_SYNTAX_NO_DOLLAR` | Strip `$` on Mips/LoongArch regs |
| `CS_OPT_SYNTAX_CS_REG_ALIAS` | Legacy Capstone reg aliases via text replace (slow at scale) |
| `CS_OPT_SYNTAX_NO_ALIAS_TEXT` | Print non-alias mnemonic text for aliases |
| `CS_OPT_SYNTAX_NO_ALIAS_TEXT_COMPRESSED` | Suppress aliases only for compressed forms (RISC-V) |
| `CS_OPT_SYNTAX_AARCH64_EXPLICIT_WIDE_IMM` | Explicit wide `MOVN`/`MOVZ` instead of `MOV` alias |

RISC-V alias-text interaction: `NO_ALIAS_TEXT` overrides
`NO_ALIAS_TEXT_COMPRESSED` (all aliases suppressed).

`CS_REG_ALIAS` uses naive search/replace on asm text; avoid on hot paths.

## Other runtime options

```c
cs_option(h, CS_OPT_MODE, new_mode);           /* reject disallowed bits → CS_ERR_OPTION */
cs_option(h, CS_OPT_UNSIGNED, CS_OPT_ON);
cs_option(h, CS_OPT_ONLY_OFFSET_BRANCH, CS_OPT_ON); /* ARM/PPC/AArch64 */
cs_option(h, CS_OPT_LITBASE, base | 1);        /* Xtensa; LSB enables; base & 0xfffff000 */
cs_option(h, CS_OPT_MNEMONIC, (uintptr_t)&mnem); /* reset: mnemonic = NULL */
```

## Decision workflow

1. Identify arch — many syntax bits are arch-specific no-ops or errors.
2. Set dialect first, then additive print tweaks.
3. Keep alias **text** options (`NO_ALIAS_TEXT*`) separate from detail
   **operand** mode (`CS_OPT_DETAIL_REAL`).
4. Do not use `CS_OPT_OFF` expecting to clear detail bits.

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
