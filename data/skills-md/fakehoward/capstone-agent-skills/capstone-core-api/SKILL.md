---
name: capstone-core-api
description: >-
  Guides Capstone handle lifecycle and core C API: cs_version, cs_support,
  cs_open, cs_close, cs_errno, cs_strerror, and CS_OPT_MEM setup. Use when
  opening or closing a csh, checking architecture support, reporting Capstone
  errors, or bootstrapping Capstone API 6 alpha.
---

# Capstone core API

Verified against Capstone `next` (API 6 alpha): `capstone.h`, `cs.c`.

## Decision rules

1. Call `cs_version` / `cs_support` before assuming an arch or diet build.
2. If the platform has no system allocator (or you replace it), set
   `CS_OPT_MEM` **before** `cs_open`. Handle may be anything for that call.
3. `cs_open(arch, mode, &handle)` → check return/`cs_errno`; never use handle
   on failure.
4. Configure options after open (except `CS_OPT_MEM`).
5. `cs_close(&handle)` zeros the handle; do not reuse afterward.
6. Prefer `cs_strerror(cs_errno(handle))` for diagnostics.

## Minimal lifecycle

```c
csh handle;
cs_err err = cs_open(CS_ARCH_X86, CS_MODE_64, &handle);
if (err != CS_ERR_OK) {
    /* use cs_strerror(err) — handle is not valid */
    return;
}
/* cs_option / disasm ... */
cs_close(&handle);
```

## Error codes to treat specially

| Code | Meaning for callers |
| --- | --- |
| `CS_ERR_ARCH` | Arch not compiled in / unsupported |
| `CS_ERR_MODE` | Mode bits invalid for arch |
| `CS_ERR_MEM` / `CS_ERR_MEMSETUP` | Allocator missing or OOM |
| `CS_ERR_CSH` | Bad handle argument |
| `CS_ERR_DETAIL` | Detail-dependent API used without detail |
| `CS_ERR_SKIPDATA` | Detail/regs API used on skipdata "insn" (`id == 0`) |
| `CS_ERR_DIET` | Name/detail APIs unavailable in diet engine |

## Related skills

- Disasm APIs: [../capstone-disasm-iteration/SKILL.md](../capstone-disasm-iteration/SKILL.md)
- Options: [../capstone-options-syntax/SKILL.md](../capstone-options-syntax/SKILL.md)
- Failures: [../capstone-troubleshooting/SKILL.md](../capstone-troubleshooting/SKILL.md)

## More

- API notes: [reference.md](reference.md)
- Snippets: [examples.md](examples.md)
