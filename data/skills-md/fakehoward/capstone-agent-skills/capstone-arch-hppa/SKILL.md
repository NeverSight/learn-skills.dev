---
name: capstone-arch-hppa
description: >-
  Guides Capstone HPPA/PA-RISC (CS_ARCH_HPPA) disassembly: HPPA 1.1/2.0/2.0W
  with little or big endian, runtime MODE, detail operands including MEM space
  and access, modifiers, and regs_access. Use when working with PA-RISC, HPPA,
  hppa20, hppa.h, or CS_ARCH_HPPA.
---

# Capstone arch: HPPA

Source of truth: sibling Capstone tree — `include/capstone/hppa.h`,
`arch/HPPA/HPPAModule.c`, `HPPADisassembler.c`, `cs.c` HPPA config,
`tests/details/hppa.yaml`, `tests/MC/HPPA/`.

## Hard rules

- Versions: `CS_MODE_HPPA_11`, `CS_MODE_HPPA_20`, `CS_MODE_HPPA_20W`
  (`HPPA_20 | (1<<3)`).
- Endian: `CS_MODE_LITTLE_ENDIAN` or `CS_MODE_BIG_ENDIAN` (both allowed).
- Runtime `CS_OPT_MODE` **replaces** `handle->mode` (`=` in `HPPA_option`);
  syntax is not handled specially.
- Detail: `insn->detail->hppa` — REG/IMM/MEM/IDX_REG/DISP/TARGET, with `access`.
- Completers/modifiers live in internal `hppa_ext` (print path), not `cs_hppa`.
- `cs_regs_access` supported (`HPPA_reg_access`).
- No Capstone `is_alias` support.

## Quick open

```c
csh handle;
cs_open(CS_ARCH_HPPA, CS_MODE_HPPA_20 | CS_MODE_BIG_ENDIAN, &handle);
cs_option(handle, CS_OPT_DETAIL, CS_OPT_ON);
```

## More

- Modes, options, operands, pitfalls: [reference.md](reference.md)
- API / cstool snippets: [examples.md](examples.md)
- Registration gap: troubleshooting section in [reference.md](reference.md)
