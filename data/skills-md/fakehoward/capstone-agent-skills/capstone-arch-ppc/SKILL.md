---
name: capstone-arch-ppc
description: >-
  Guides Capstone PowerPC disassembly: 32/64 and Book-E/QPX/SPE/PWR modes,
  little-endian mode exception, cs_ppc branch/format detail, and aliases. Use
  when the task involves CS_ARCH_PPC, include/capstone/ppc.h, PPCModule,
  CS_MODE_BOOKE/MSYNC/PWR*, or PPC syntax NOREGNAME/PERCENT. Note: no
  cs_regs_access.
---

# Capstone PowerPC

Load only this skill for PPC. Do not pull other architecture skills.

## Source of truth

Sibling Capstone tree (`capstone/`):

- `include/capstone/ppc.h` — `cs_ppc`, `ppc_bc`
- `arch/PowerPC/PPCModule.c` — mode OR + LE exception
- `cs.c` — `CS_ARCH_CONFIG_PPC`
- `tests/details/ppc.yaml`, `tests/MC/PowerPC/`

## Valid modes

Allowed: `LITTLE_ENDIAN`, `32`, `64`, `BIG_ENDIAN`, `QPX`, `SPE`, `BOOKE`, `PS`, `AIX_OS`, `PWR7`…`PWR10`, `PPC_ISA_FUTURE`, `MSYNC`, `MODERN_AIX_AS`.

| Target | Mode notes |
|--------|------------|
| Classic BE 32 | `CS_MODE_32 \| CS_MODE_BIG_ENDIAN` |
| 64-bit | OR `CS_MODE_64` |
| Book-E | `CS_MODE_BOOKE` (also implied by `MSYNC`) |
| Paired-singles / QPX / SPE | `PS` / `QPX` / `SPE` |
| Power9+ | `PWR9` / `PWR10` / … |

### Runtime mode rules (`PPC_option`)

- Normal: `handle->mode |= value` (OR).
- **Exception:** `value == CS_MODE_LITTLE_ENDIAN` clears `CS_MODE_BIG_ENDIAN` only (`mode &= ~BIG_ENDIAN`) and returns.
- `CS_MODE_MSYNC` also forces `CS_MODE_BOOKE`.

Bits other than BE cannot be cleared without reopen.

## Options and syntax

- Detail / `CS_OPT_DETAIL_REAL` — important for aliases (`lis`/`li`/rotates, …)
- `CS_OPT_SYNTAX_NOREGNAME` — numeric register names
- `CS_OPT_SYNTAX_PERCENT` — print `%` before registers
- Syntax assign: `handle->syntax = value` (replace, not OR)
- `CS_OPT_ONLY_OFFSET_BRANCH`
- Skipdata stride: 4

## Detail, alias, regs_access

- Detail: `insn->detail->ppc` — `bc`, `update_cr0`, `format`, up to 8 ops
- Auto-Sync alias supported (`is_alias` for `lis`/`li` in details tests)
- **`cs_regs_access`: not supported** — `PPC_global_init` does not set `reg_access`; API returns `CS_ERR_ARCH`
- Operand `access` and `detail->regs_read`/`regs_write` from mapping may still populate with detail on; do not call `cs_regs_access`

## Workflow

1. Open with explicit endian + 32/64 (+ Book-E/PWR as needed).
2. Enable detail for `bc` predicates and `format`.
3. To move BE→LE at runtime, `cs_option(MODE, CS_MODE_LITTLE_ENDIAN)` (special clear path).
4. Use `CS_OPT_DETAIL_REAL` when alias operand sets are insufficient.
5. Never rely on `cs_regs_access` for PPC.

## Traps

- Mode OR accumulates extension bits; only LE has a clear-BE shortcut.
- `MSYNC` silently enables `BOOKE`.
- `(RA|0)` cases surface as `PPC_REG_ZERO` (name `"0"`).
- No `regs_access` callback — treat as unsupported, not a caller bug.

## More

- Mode/option tables: [reference.md](reference.md)
- Snippets: [examples.md](examples.md)
