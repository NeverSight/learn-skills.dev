---
name: capstone-arch-xcore
description: >-
  Guides Capstone XCore open modes, runtime options, cs_xcore detail/operands,
  skipdata alignment, and the lack of cs_regs_access. Use when working with
  CS_ARCH_XCORE, xcore.h, XCoreModule, XCore firmware, or tests/details/xcore.yaml.
---

# Capstone XCore

## Scope

Load this skill for `CS_ARCH_XCORE` only. Source of truth: sibling `capstone/`
(`include/capstone/xcore.h`, `arch/XCore/`, `cs.c` `CS_ARCH_CONFIG_XCORE`,
`tests/details/xcore.yaml`).

## Open / valid modes

Allowed mask (`cs.c`): only `CS_MODE_BIG_ENDIAN` (plus `CS_MODE_LITTLE_ENDIAN`, which is 0).

```c
cs_open(CS_ARCH_XCORE, CS_MODE_BIG_ENDIAN, &handle);  /* cstool: "xcore" */
```

Mode `0` also passes the mask. Prefer `CS_MODE_BIG_ENDIAN` to match cstool/tests.

## Runtime mode / options

`XCore_option` always returns `CS_ERR_OK` and does **not** update `handle->mode`.
Comment in module: only big-endian is considered valid; little-endian cannot be
tested because it is 0. Do not rely on `cs_option(CS_OPT_MODE, …)` to change
endian; reopen if you must change open mode.

Common options still go through core: `CS_OPT_DETAIL`, skipdata, etc.

## Detail / operands

`cs_detail.xcore` (`cs_xcore`):

| Field | Notes |
|-------|--------|
| `op_count` | 0–8 |
| `operands[]` | `XCORE_OP_REG` / `IMM` / `MEM` |

`xcore_op_mem`: `base`, `index`, `disp`, `direct` (+1 forward / −1 backward).

Not an auto-sync arch: `is_alias` / `alias_id` are unused.

## regs_access

**Unsupported.** `XCore_global_init` does not set `ud->reg_access`.
`cs_regs_access` → `CS_ERR_ARCH`. Use explicit operands and (when detail is on)
`detail->regs_read` / `regs_write` only if the mapping filled them; do not call
`cs_regs_access`.

## Workflow

1. `cs_open(CS_ARCH_XCORE, CS_MODE_BIG_ENDIAN, &h)`
2. Enable detail if you need operands
3. Disassemble; consume `insn->detail->xcore`
4. Skipdata default size for XCore is **2** bytes

## Traps

- Calling `cs_regs_access` always fails for this arch
- Runtime `CS_OPT_MODE` is a no-op in the arch option handler
- Instruction stream decode uses little-endian 16/32-bit words in
  `XCoreDisassembler.c` regardless of the mode flag name

## More

- Modes, structs, traps: [reference.md](reference.md)
- Minimal C / cstool: [examples.md](examples.md)
