---
name: capstone-operands-registers
description: >-
  Documents Capstone operand and register helpers: cs_op_count, cs_op_index,
  cs_reg_read, cs_reg_write, cs_insn_group, and cs_regs_access, including
  architectures without reg_access. Use when querying operands, implicit
  registers, register access sets, or CS_ERR_ARCH from cs_regs_access.
---

# Capstone operands and registers

Verified: `capstone.h` helpers, `cs_regs_access` in `cs.c`, per-arch
`ud->reg_access` assignments in `*Module.c`.

## Preconditions

All of these need detail mode on (`detail_opt` non-zero) and a non-skipdata
insn (`insn->id != 0`, `insn->detail != NULL`):

- `cs_op_count` / `cs_op_index`
- `cs_reg_read` / `cs_reg_write`
- `cs_insn_group`
- `cs_regs_access`

Otherwise expect `CS_ERR_DETAIL`, `CS_ERR_SKIPDATA`, or false/`-1`.

## Two register views

| Source | Contents |
| --- | --- |
| `insn->detail->regs_read/write` | Implicit regs only; used by `cs_reg_read` / `cs_reg_write` |
| `cs_regs_access(...)` | Explicit + implicit regs via arch `reg_access` callback |

Do not treat the implicit arrays as a full def/use set.

## Architectures with `reg_access` (current tree)

ARM, AArch64, X86, Mips, M68K, M680X, BPF, RISCV, SH, TriCore, Alpha, HPPA,
LoongArch, ARC, Xtensa.

## Architectures without `reg_access`

These leave `handle->reg_access == NULL` → `cs_regs_access` returns
`CS_ERR_ARCH`:

PowerPC, Sparc, SystemZ, XCore, TMS320C64x, EVM, MOS65XX, WASM.

For those, use arch-specific `insn->detail-><arch>` operands and the implicit
reg arrays only.

## `cs_regs_access` checklist

1. Detail on before decode (and before `cs_malloc` if iterating).
2. Skip `id == 0` skipdata records.
3. Provide `cs_regs` arrays (`uint16_t[64]`) plus count out-params.
4. Handle `CS_ERR_ARCH` as “not implemented for this arch”, not a caller bug.
5. Diet builds: `CS_ERR_DIET`.

RISC-V notes from v6 guide: CSR and PC reads are intentionally not treated as
ordinary registers in `reg_access`.

## Operand indexing

```c
int n = cs_op_count(h, insn, X86_OP_IMM);
int idx = cs_op_index(h, insn, X86_OP_IMM, 1); /* 1-based position */
```

`position` is **1-based** in `[1, cs_op_count(...)]`.

## Related

- Detail flags: [../capstone-detail-aliases/SKILL.md](../capstone-detail-aliases/SKILL.md)
- Errors: [../capstone-troubleshooting/SKILL.md](../capstone-troubleshooting/SKILL.md)

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
