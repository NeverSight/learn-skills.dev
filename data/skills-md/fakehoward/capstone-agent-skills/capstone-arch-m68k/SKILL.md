---
name: capstone-arch-m68k
description: >-
  Guides Capstone M68K CPU/ColdFire modes, big-endian open, runtime CS_OPT_MODE
  no-op (reopen to change), cs_m68k detail/operands, and cs_regs_access support.
  Use when working with CS_ARCH_M68K, m68k.h, M68KModule, 68000/ColdFire code, or
  tests/details/m68k.yaml.
---

# Capstone M68K

## Scope

`CS_ARCH_M68K` only. Sources: `include/capstone/m68k.h`, `arch/M68K/`,
`cs.c` `CS_ARCH_CONFIG_M68K`, `tests/details/m68k.yaml`.

## Open / valid modes

Allowed: `CS_MODE_BIG_ENDIAN` | `CS_MODE_M68K_FEATURE_MASK`
(000/010/020/030/040/060, CPU32, ColdFire ISA/feature bits and composites
`CS_MODE_M68K_COLDFIRE`, `CFV1`…`CFV5`).

```c
cs_open(CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_040, &h);
cs_open(CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_COLDFIRE, &h);
```

If no CPU/feature bits are set, decode defaults to **68000**
(`CS_MODE_M68K_000`) inside `M68K_getInstruction`.

## Runtime mode

`M68K_option` always returns `CS_ERR_OK` and **does not** write `handle->mode`.
`cs_option(h, CS_OPT_MODE, …)` can pass the mask check then silently leave the
engine on the open-time mode. **Reopen** (`cs_close` + `cs_open`) to change CPU
or ColdFire features.

## Options

No arch-specific syntax options. Use core `CS_OPT_DETAIL` (and skipdata as
needed). Skipdata size for M68K is **2**.

## Detail / operands

`cs_detail.m68k` (`cs_m68k`):

| Field | Notes |
|-------|--------|
| `op_count` | up to `M68K_OPERAND_COUNT` (6) |
| `operands[]` | REG, IMM, MEM, FP_SINGLE/DOUBLE, REG_BITS, REG_PAIR, BR_DISP, SHIFT |
| `op_size` | CPU vs FPU size (`.b`/`.w`/`.l`, FP sizes) |

Each operand has `address_mode` (`m68k_address_mode`) and optional `flags`
(`m68k_op_flags` for ColdFire MAC, etc.).

Not auto-sync: ignore `is_alias` / `alias_id`.

## regs_access

**Supported** (non-DIET): `ud->reg_access = M68K_reg_access`.
Detail tests often assert `regs_read` / implicit regs. In DIET builds,
`cs_regs_access` → `CS_ERR_DIET`.

## Workflow

1. Open with BE + desired CPU/ColdFire feature bits
2. Enable detail for addressing modes / `op_size`
3. Use `cs_regs_access` when you need aggregated read/write regs
4. To switch 020↔040 or ColdFire profile: reopen, do not `CS_OPT_MODE`

## Traps

- Runtime `CS_OPT_MODE` is a no-op; success does not mean the ISA changed
- Feature bits are OR masks; wrong CPU rejects opcodes (empty decode in tests)
- ColdFire composites (`CFV*`) expand via `m68k_has_feature` helpers

## More

- Feature mask, operand types: [reference.md](reference.md)
- Open / reopen examples: [examples.md](examples.md)
