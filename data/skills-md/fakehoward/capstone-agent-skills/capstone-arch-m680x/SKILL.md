---
name: capstone-arch-m680x
description: >-
  Guides Capstone M680X chip modes (at least one required), multi-chip priority,
  runtime option behavior, cs_m680x operands, and cs_regs_access. Use when working
  with CS_ARCH_M680X, m680x.h, M680XModule, 6800/6809/CPU12/HCS families, or
  tests/details/m680x.yaml.
---

# Capstone M680X

## Scope

`CS_ARCH_M680X` only. Sources: `include/capstone/m680x.h`, `arch/M680X/`,
`cs.c` `CS_ARCH_CONFIG_M680X`, `tests/details/m680x.yaml`.

## Open / valid modes

Allowed chip bits (OR):

`6301`, `6309`, `6800`, `6801`, `6805`, `6808`, `6809`, `6811`, `CPU12`,
`HCS08`, `RS08`, `HCS12X`.

**At least one** chip mode is required. There is no default CPU; missing all
chip bits → `CS_ERR_MODE` in `M680X_global_init`.

Multiple chip bits are **allowed** by the mask and init. They are **not**
rejected as “exactly one”. Decode picks the first match in this priority order
(`else if` in `M680X_getInstruction`):

1. 6800 → 2. 6801 → 3. 6805 → 4. 6808 → 5. HCS08 → 6. 6809 → 7. 6301 →
8. 6309 → 9. 6811 → 10. CPU12 → 11. RS08 → 12. HCS12X

Prefer a single chip flag in production code.

```c
cs_open(CS_ARCH_M680X, CS_MODE_M680X_6809, &h);
```

## Runtime mode / options

`M680X_option` is a stub (`//TODO`, always `CS_ERR_OK`) and does not update mode.
Treat runtime `CS_OPT_MODE` as a no-op; reopen to change chip.

## Detail / operands

`cs_detail.m680x` (`cs_m680x`):

| Field | Notes |
|-------|--------|
| `flags` | `M680X_FIRST_OP_IN_MNEM` / `SECOND_OP_IN_MNEM` |
| `op_count` | up to `M680X_OPERAND_COUNT` (9) |
| `operands[]` | REGISTER, IMMEDIATE, INDEXED, EXTENDED, DIRECT, RELATIVE, CONSTANT |

Operands carry `size` and `access` (`cs_ac_type`) outside DIET.

Not auto-sync: no alias API.

## regs_access

**Supported** (non-DIET): `ud->reg_access = M680X_reg_access`. Detail YAML often
lists `regs_read` / `regs_write` and groups (`M680X_GRP_RET`, …).

## Workflow

1. Open with **at least one** chip mode (ideally exactly the target CPU)
2. Enable detail for indexed/direct/relative operands
3. Use `cs_regs_access` or detail regs arrays as needed
4. Skipdata size is **1**

## Traps

- Mode `0` fails open (no default chip)
- Multi-chip OR silently follows priority above; do not assume “exactly one”
- Runtime MODE option does not switch CPU

## More

- Chip list, operand structs, priority table: [reference.md](reference.md)
- Open / multi-mode note: [examples.md](examples.md)
