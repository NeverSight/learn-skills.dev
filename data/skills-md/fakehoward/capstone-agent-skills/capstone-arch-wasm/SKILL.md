---
name: capstone-arch-wasm
description: >-
  Guides Capstone WebAssembly (CS_ARCH_WASM) disassembly: mode 0 only,
  CS_OPT_DETAIL operand types, rejected arch options, and missing
  cs_regs_access. Use when working with WASM, WebAssembly opcodes,
  get_local/i32.const/br_table, wasm.h, or CS_ARCH_WASM.
---

# Capstone arch: WASM

Source of truth: sibling Capstone tree — `include/capstone/wasm.h`,
`arch/WASM/WASMModule.c`, `cs.c` (`CS_ARCH_CONFIG_WASM`),
`tests/details/wasm.yaml`, `cstool/cstool_wasm.c`.

## Hard rules

- Open with mode `0` (`CS_MODE_LITTLE_ENDIAN`). Any non-zero mode → `CS_ERR_MODE`.
- Arch option hook always returns `CS_ERR_OPTION`. Core options (`CS_OPT_DETAIL`,
  `CS_OPT_SKIPDATA`, `CS_OPT_UNSIGNED`, `CS_OPT_MNEMONIC`) still work in `cs_option`.
- No `reg_access` callback → `cs_regs_access` returns `CS_ERR_ARCH`.
- No Capstone alias support (`is_alias` / `alias_id` unused).
- Detail lives in `insn->detail->wasm` (`cs_wasm`, up to 2 operands).

## Quick open

```c
csh handle;
cs_open(CS_ARCH_WASM, 0, &handle);
cs_option(handle, CS_OPT_DETAIL, CS_OPT_ON);
```

## More

- Modes, options, operands, pitfalls: [reference.md](reference.md)
- Concrete API / cstool snippets: [examples.md](examples.md)
