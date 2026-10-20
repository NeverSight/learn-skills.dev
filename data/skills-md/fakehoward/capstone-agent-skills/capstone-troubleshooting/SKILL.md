---
name: capstone-troubleshooting
description: >-
  Diagnoses Capstone API 6 alpha failures: CS_ERR_* codes, detail pointer
  issues, skipdata callback mismatches, missing regs_access, and the probable
  Xtensa skipdata size 255 defect. Use when Capstone disassembly misbehaves,
  detail is null, options appear stuck, or skip sizes look wrong.
---

# Capstone troubleshooting

Verified against `cs.c`, `capstone.h`, arch `*Module.c`, `skipdata_size()`.

## Triage order

1. `cs_errno` / `cs_strerror` after the failing call.
2. Confirm arch compiled in (`cs_support`).
3. Confirm detail / malloc ordering for the API used.
4. Check skipdata and `insn->id == 0`.
5. Check arch-specific support (regs_access, alias).

## Symptom → cause

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `CS_OPT_DETAIL` + `CS_OPT_OFF` still detailed | `detail_opt |= value`; OFF is 0 | New handle; see detail-aliases |
| Iter detail APIs → `CS_ERR_DETAIL` / NULL `detail` | `cs_malloc` before DETAIL | Option then `cs_malloc` |
| `cs_regs_access` → `CS_ERR_ARCH` | Arch has no `reg_access` | Use detail operands; see operands-registers |
| `CS_ERR_SKIPDATA` | Helper used on data insn | Guard `insn->id` |
| Skip callback wrong index in iter | Iter passes `offset=0` + remaining slice | Fix callback; see skipdata |
| Xtensa skips **255** bytes | `skipdata_size` default `(uint8_t)-1` | Probable defect; custom callback |
| Crash / race with threads | Shared handle or live `CS_OPT_MEM` swap | Handle-per-thread; hooks at init |
| Build break on `CS_ARCH_ARM64` / `SYSZ` | v6 rename | Compat macros or rename; v6-migration |
| Empty names / diet errors | Diet engine | `cs_support(CS_SUPPORT_DIET)` |

## Probable defect: Xtensa skipdata size 255

In `skipdata_size()` the `switch (handle->arch)` has **no** `CS_ARCH_XTENSA`
(and no final return after the switch). Unlisted arches hit:

```c
default:
    return (uint8_t)-1; /* 255 */
```

When SKIPDATA is on without a callback, Capstone may skip 255 bytes on Xtensa.
**Do not document 255 as intended ISA alignment.** Workarounds:

1. Provide `CS_OPT_SKIPDATA_SETUP.callback` returning a sane size (e.g. 1/2/3).
2. Or avoid SKIPDATA on Xtensa until fixed upstream.

Mention this only as a defect hypothesis tied to current `cs.c`.

## Detail latch reminder

```c
handle->detail_opt |= (cs_opt_value)value; /* cannot clear with CS_OPT_OFF */
```

## Quick validation snippets

```c
/* after failure */
fprintf(stderr, "%s\n", cs_strerror(cs_errno(h)));

/* before regs/detail helpers */
if (!insn->id || !insn->detail) { /* handle skipdata / missing detail */ }

/* arch support */
if (!cs_support(CS_ARCH_XTENSA)) { /* not built */ }
```

## Related skills

- [../capstone-detail-aliases/SKILL.md](../capstone-detail-aliases/SKILL.md)
- [../capstone-skipdata/SKILL.md](../capstone-skipdata/SKILL.md)
- [../capstone-operands-registers/SKILL.md](../capstone-operands-registers/SKILL.md)
- [../capstone-performance-concurrency/SKILL.md](../capstone-performance-concurrency/SKILL.md)
- [../capstone-v6-migration/SKILL.md](../capstone-v6-migration/SKILL.md)

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
