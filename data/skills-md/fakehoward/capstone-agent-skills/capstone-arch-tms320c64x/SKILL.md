---
name: capstone-arch-tms320c64x
description: >-
  Guides Capstone TMS320C64x endian modes, CS_OPT_MODE OR semantics, cs_tms320c64x
  detail (operands, funit, condition, parallel), and the lack of cs_regs_access.
  Use when working with CS_ARCH_TMS320C64X, tms320c64x.h, TMS320C64xModule, or
  tests/details/tms320c64x.yaml.
---

# Capstone TMS320C64x

## Scope

`CS_ARCH_TMS320C64X` only. Sources: `include/capstone/tms320c64x.h`,
`arch/TMS320C64x/`, `cs.c` `CS_ARCH_CONFIG_TMS320C64X`,
`tests/details/tms320c64x.yaml`.

## Open / valid modes

Allowed: `CS_MODE_LITTLE_ENDIAN` (0) and/or `CS_MODE_BIG_ENDIAN`.

```c
cs_open(CS_ARCH_TMS320C64X, CS_MODE_BIG_ENDIAN, &h);     /* cstool tms320c64x */
cs_open(CS_ARCH_TMS320C64X, CS_MODE_LITTLE_ENDIAN, &h);  /* tms320c64xle */
```

## Runtime mode / options

`TMS320C64x_option`:

- `CS_OPT_MODE` → `handle->mode |= value` (bits accumulate; cannot clear BE by
  OR-ing LE alone — reopen to reset)
- `CS_OPT_SYNTAX` → `handle->syntax |= value`

Fetch uses `readBytes32(MI, code)` (endian from the handle). Skipdata size **4**.

## Detail / operands

`cs_detail.tms320c64x` (`cs_tms320c64x`):

| Field | Notes |
|-------|--------|
| `op_count` / `operands[8]` | REG, IMM, MEM, **REGPAIR** (`TMS320C64X_OP_REGPAIR`) |
| `condition` | `reg`, `zero` (predicate) |
| `funit` | `unit`, `side`, `crosspath` |
| `parallel` | parallel-bar marker (`\|\|`) |

`tms320c64x_op_mem`: base, disp, unit, scaled, disptype, direction, modify.

Not auto-sync: no alias API.

## regs_access

**Unsupported.** Module does not set `reg_access`. `cs_regs_access` →
`CS_ERR_ARCH`.

## Workflow

1. Open with the correct endian for the image
2. Enable detail for funit / condition / parallel / mem modifiers
3. Do not call `cs_regs_access`
4. If you need to flip endian cleanly, reopen rather than OR-ing mode bits

## Traps

- `CS_OPT_MODE` ORs; sticky bits until reopen
- Fixed 4-byte instructions; short buffers fail decode
- No `cs_regs_access`

## More

- Structs and option quirks: [reference.md](reference.md)
- Detail walkthrough: [examples.md](examples.md)
