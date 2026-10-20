---
name: capstone-arch-evm
description: >-
  Guides Capstone EVM disassembly with mode 0 only, cs_evm stack/gas detail
  (pop/push/fee), groups, and no register or regs_access API. Use when working
  with CS_ARCH_EVM, evm.h, EVMModule, Ethereum bytecode, or tests/details/evm.yaml.
---

# Capstone EVM

## Scope

`CS_ARCH_EVM` only. Sources: `include/capstone/evm.h`, `arch/EVM/`,
`cs.c` `CS_ARCH_CONFIG_EVM`, `tests/details/evm.yaml`.

## Open / valid modes

**Mode must be 0** (`CS_MODE_LITTLE_ENDIAN`). Non-zero mode → `CS_ERR_MODE` in
`EVM_global_init` (the `arch_disallowed_mode_mask` is 0, so rejection is in the
module, not the mask).

```c
cs_open(CS_ARCH_EVM, 0, &h);  /* cstool: "evm" */
```

## Runtime mode / options

`EVM_option` always returns `CS_ERR_OK` and does not change mode. Do not use
nonzero `CS_OPT_MODE` after open; reopen with 0 if needed. Core detail/skipdata
options still apply via the usual `cs_option` path before/around arch_option.

Skipdata size: **1**.

## Detail / operands

EVM has **no operand list**. `cs_detail.evm` (`cs_evm`):

| Field | Meaning |
|-------|---------|
| `pop` | stack items consumed |
| `push` | stack items produced |
| `fee` | gas fee |

`cs_op_count` / `cs_op_index` for EVM do nothing useful (empty `break`).

Groups: `EVM_GRP_JUMP`, `MATH`, `STACK_READ`/`WRITE`, `MEM_*`, `STORE_*`, `HALT`.

Not auto-sync: no alias API. **No registers** in the public model.

## regs_access

**Unsupported** (no regs, no `reg_access`). `cs_regs_access` → `CS_ERR_ARCH`.

## Workflow

1. `cs_open(CS_ARCH_EVM, 0, &h)`
2. Enable detail for pop/push/fee and groups
3. Walk bytecode; use `insn->bytes` / mnemonic for immediates (e.g. PUSH data in
   `op_str` / bytes), not a typed operand array
4. Never call `cs_regs_access`

## Traps

- Any nonzero open mode fails
- No `cs_*_op` union members for EVM — only pop/push/fee
- Instruction IDs match opcodes (`EVM_INS_ADD = 1`, …)

## More

- Groups and init checks: [reference.md](reference.md)
- Detail example: [examples.md](examples.md)
