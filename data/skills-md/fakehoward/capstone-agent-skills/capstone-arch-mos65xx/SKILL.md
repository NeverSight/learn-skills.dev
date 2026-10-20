---
name: capstone-arch-mos65xx
description: >-
  Guides Capstone MOS65XX CPU modes (6502/65C02/W65C02 and 65816 via LONG_M,
  LONG_X, LONG_MX), Motorola syntax, cs_mos65xx address modes/operands, and
  regs_access limits. Use when working with CS_ARCH_MOS65XX, mos65xx.h,
  MOS65XXModule, 6502/65816 code, or tests/details/mos65xx.yaml.
---

# Capstone MOS65XX

## Scope

`CS_ARCH_MOS65XX` only. Sources: `include/capstone/mos65xx.h`, `arch/MOS65XX/`,
`cs.c` `CS_ARCH_CONFIG_MOS65XX`, `tests/details/mos65xx.yaml`.

## Open / valid modes

Allowed by mask: LE (0), `CS_MODE_MOS65XX_6502`, `65C02`, `W65C02`, and
`CS_MODE_MOS65XX_65816_LONG_MX` (i.e. `LONG_M` | `LONG_X`).

| Goal | Mode to pass |
|------|----------------|
| MOS 6502 | `CS_MODE_MOS65XX_6502` (or `0` → default 6502 in init) |
| WDC 65C02 | `CS_MODE_MOS65XX_65C02` |
| WDC W65C02 | `CS_MODE_MOS65XX_W65C02` |
| 65816 | **`LONG_M` / `LONG_X` / `LONG_MX`** (sets CPU 65816 + m/x widths) |

For 65816 use the LONG_* flags (as cstool `"65816"` and detail tests do with
`LONG_MX`). Do not tell users to open with bare `CS_MODE_MOS65XX_65816`.

## Runtime mode / options

`MOS65XX_option` **replaces** `handle->mode` on `CS_OPT_MODE` and updates
`cpu_type` / `long_m` / `long_x`.

Syntax:

- `CS_OPT_SYNTAX_DEFAULT` — no hex prefix
- `CS_OPT_SYNTAX_MOTOROLA` — `$` hex prefix

Other syntax values → `CS_ERR_OPTION`.

## Detail / operands

`cs_detail.mos65xx` (`cs_mos65xx`):

| Field | Notes |
|-------|--------|
| `am` | `mos65xx_address_mode` (ZP/ABS/long/stack-relative/…) |
| `modifies_flags` | bool |
| `op_count` / `operands[3]` | REG / IMM (`uint16_t`) / MEM (`uint32_t` address) |

Not auto-sync: no alias API.

## regs_access

**Unsupported.** Module does not register `reg_access`. `cs_regs_access` →
`CS_ERR_ARCH`. Registers exist for operands / `cs_reg_name` only.

## Workflow

1. Open with the matching CPU mode; for 65816 prefer `LONG_MX` (or LONG_M/X)
2. Optionally `CS_OPT_SYNTAX_MOTOROLA`
3. Enable detail; read `am` + operands
4. Switch m/x width at runtime with `CS_OPT_MODE` + LONG_* bits (replace semantics)
5. Skipdata size **1**

## Traps

- Bare `CS_MODE_MOS65XX_65816` is rejected by the open/option mask — see
  troubleshooting note in [reference.md](reference.md)
- Last matching CPU bit wins when OR-ing 6502/65C02/W65C02/65816 selectors in
  `MOS65XX_option` (sequential `if`s)
- No `cs_regs_access`

## More

- Mode mask, 65816 note, address modes: [reference.md](reference.md)
- Open / syntax / LONG_MX: [examples.md](examples.md)
