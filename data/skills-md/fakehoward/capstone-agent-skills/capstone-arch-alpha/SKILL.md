---
name: capstone-arch-alpha
description: >-
  Guides Capstone Alpha (CS_ARCH_ALPHA) disassembly: little/big endian modes,
  runtime MODE/SYNTAX, detail REG/IMM operands with access, regs_access, and
  no Capstone alias IDs. Use when working with DEC Alpha, alphabe, alpha.h,
  or CS_ARCH_ALPHA.
---

# Capstone arch: Alpha

Source of truth: sibling Capstone tree — `include/capstone/alpha.h`,
`arch/Alpha/AlphaModule.c`, `AlphaMapping.c`, `cs.c` (`CS_ARCH_CONFIG_ALPHA`),
`tests/details/alpha.yaml`, `tests/MC/Alpha/`.

## Hard rules

- Modes: `CS_MODE_LITTLE_ENDIAN` (`0`, default) or `CS_MODE_BIG_ENDIAN` only.
- No CPU/version mode flags.
- Runtime `CS_OPT_MODE` / `CS_OPT_SYNTAX` **replace** (`handle->mode` /
  `handle->syntax = value` in `ALPHA_option`).
- Detail: `insn->detail->alpha` — up to 3 operands, types REG/IMM, with `access`.
- `cs_regs_access` supported (`Alpha_reg_access`).
- Printer alias stub returns false; Capstone `is_alias` / `alias_id` unused.

## Quick open

```c
csh handle;
cs_open(CS_ARCH_ALPHA, CS_MODE_LITTLE_ENDIAN, &handle);
cs_option(handle, CS_OPT_DETAIL, CS_OPT_ON);
```

## More

- Modes, options, operands, pitfalls: [reference.md](reference.md)
- API / cstool snippets: [examples.md](examples.md)
