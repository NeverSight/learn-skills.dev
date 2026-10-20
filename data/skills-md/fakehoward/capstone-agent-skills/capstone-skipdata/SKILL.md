---
name: capstone-skipdata
description: >-
  Configures Capstone SKIPDATA mode, default skip sizes, and
  CS_OPT_SKIPDATA_SETUP callbacks, including batch versus iter offset
  differences. Use when continuing past invalid bytes, customizing data
  mnemonics, or implementing cs_skipdata_cb_t on API 6 alpha.
---

# Capstone skipdata

Verified: `cs_disasm` / `cs_disasm_iter` skipdata paths in `cs.c`,
`skipdata_size()`, `tests/integration/test_skipdata.c`.

## Enable

```c
cs_option(handle, CS_OPT_SKIPDATA, CS_OPT_ON);
cs_opt_skipdata setup = {
    .mnemonic = "db",   /* NULL → ".byte" */
    .callback = my_cb,  /* NULL → default size */
    .user_data = ctx,
};
cs_option(handle, CS_OPT_SKIPDATA_SETUP, (uintptr_t)&setup);
```

`CS_OPT_SKIPDATA` stores a boolean (`value == CS_OPT_ON`); `CS_OPT_OFF` works.

## Synthetic data instruction

On skip:

- `insn->id == 0`
- mnemonic/op_str describe bytes (diet: empty strings)
- batch path sets `detail = NULL`
- detail/regs APIs → `CS_ERR_SKIPDATA`

## Default skip sizes (`skipdata_size`)

From `cs.c` (selected):

| Arch | Default skip |
| --- | --- |
| X86 / EVM / WASM / MOS65XX / M680X | 1 |
| SystemZ / XCore / M68K / SH / TriCore / ARC | 2 |
| ARM Thumb | 2 |
| ARM non-Thumb / AArch64 / Mips / PPC / Sparc / TMS320C64x / Alpha / HPPA / LoongArch | 4 |
| RISCV | 2 if `CS_MODE_RISCV_C`, else 4 |
| BPF | 8 |

**Xtensa / any arch missing from the switch:** hits `default: return (uint8_t)-1`
→ **255**. Treat as a probable defect, not a feature
([troubleshooting](../capstone-troubleshooting/SKILL.md)).

## Callback contract (documented)

```c
typedef size_t (*cs_skipdata_cb_t)(const uint8_t *code, size_t code_size,
                                   size_t offset, void *user_data);
```

Return `>0` bytes to skip; `0` to stop disassembly.

## Batch vs iter: different arguments (critical)

| API | `code` / `code_size` | `offset` |
| --- | --- | --- |
| `cs_disasm` | Original full buffer (`buffer_org`, `size_org`) | Bytes from buffer start: `(size_t)(offset - offset_org)` |
| `cs_disasm_iter` | **Remaining** slice (`*code`, `*size`) | **Always `0`** |

Callbacks written for batch will mis-index if reused naively with iter.
For iter, either:

- ignore `offset` and treat `code` as current faulting bytes, or
- track absolute position in `user_data`.

## Decision rules

1. Need continue-on-garbage → SKIPDATA ON.
2. Need alignment-aware skips → default size usually enough.
3. Need custom framing → callback; write separate logic or shared state for
   batch vs iter.
4. Never read `detail` on `id == 0`.

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
