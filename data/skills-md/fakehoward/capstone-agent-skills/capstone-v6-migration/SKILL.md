---
name: capstone-v6-migration
description: >-
  Migrates clients to Capstone API 6 alpha from pre-v6: AArch64/SystemZ
  renames, compatibility headers for ARM64/SYSZ, alias/detail changes, and
  breaking enum updates. Use when porting Capstone 4/5 code, fixing
  CS_ARCH_ARM64 or CS_ARCH_SYSZ build breaks, or applying cs_v6_release_guide
  changes.
---

# Capstone v6 migration

Source: `docs/cs_v6_release_guide.md`, compat macros in `capstone.h`,
`tests/integration/compat_header/`.

## Naming: default vs compat

| Pre-v6 | v6 default | Compat (define before `#include <capstone/capstone.h>`) |
| --- | --- | --- |
| ARM64 | AArch64 (`CS_ARCH_AARCH64`, `cs_aarch64`, `AArch64_*`) | `#define CAPSTONE_AARCH64_COMPAT_HEADER` → `CS_ARCH_ARM64`, `cs_arm64`, … |
| SYSZ | SystemZ (`CS_ARCH_SYSTEMZ`, `cs_systemz`, …) | `#define CAPSTONE_SYSTEMZ_COMPAT_HEADER` → `CS_ARCH_SYSZ`, `cs_sysz`, … |
| `CS_MODE_RISCVC` | `CS_MODE_RISCV_C` | `#define CAPSTONE_RISCV_COMPAT_HEADER` |
| `ARM_CC` / `arm_cc` | `ARMCC` / `ARMCC_CondCodes` | `#define CAPSTONE_ARM_COMPAT_HEADER` (macros only) |

Prefer renaming to AArch64/SystemZ for new code. Use compat headers only when
maintaining dual v5/v6 trees.

```c
#define CAPSTONE_AARCH64_COMPAT_HEADER
#define CAPSTONE_SYSTEMZ_COMPAT_HEADER
#include <capstone/capstone.h>
```

## Alias model change

- Many former “real” alias ids removed from insn enums.
- Decode: `id` = real, `alias_id` / `is_alias` = alias identity.
- Operand sets: default alias details; `CS_OPT_DETAIL_REAL | CS_OPT_ON` for real
  details (see detail-aliases skill).
- Partial: SystemZ / LoongArch / TriCore limitations per release guide.

## Other high-impact breaks

- `writeback` moved into `cs_detail`.
- Operand `access` typed as `cs_ac_type`.
- Register pretty-aliases not printed unless LLVM does — restore old Capstone
  text with `CS_OPT_SYNTAX_CS_REG_ALIAS` (slow).
- Condition-code enums aligned to LLVM (values changed; e.g. `*_INVALID != 0`).
- ARM immediate fields widened (`int64_t`); `mem.lshift` removed.

## Migration workflow

1. Build against next headers; fix arch rename errors first (AArch64/SystemZ).
2. Decide: native names vs compat macros.
3. Update alias-sensitive logic to `is_alias` / `alias_id` / `DETAIL_REAL`.
4. Re-validate `cs_regs_access` availability per arch.
5. Re-run arch tests / `cstest` YAML expectations (`is_alias`, operand sets).

## Related

- Detail/alias: [../capstone-detail-aliases/SKILL.md](../capstone-detail-aliases/SKILL.md)
- Syntax flags: [../capstone-options-syntax/SKILL.md](../capstone-options-syntax/SKILL.md)

## More

- [reference.md](reference.md)
- [examples.md](examples.md)
