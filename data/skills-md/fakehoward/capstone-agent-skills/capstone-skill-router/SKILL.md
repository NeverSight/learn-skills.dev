---
name: capstone-skill-router
description: >-
  Routes Capstone Engine API 6 (next/alpha) questions to the correct
  capstone-* skill. Use when the user mentions Capstone, cs_open, cs_disasm,
  cs_disasm_iter, cs_option, detail, alias, skipdata, regs_access, syntax,
  ARM64/AArch64, SYSZ/SystemZ, v6 migration, or Capstone errors.
---

# Capstone skill router

Source of truth: local Capstone tree on branch `next` (API 6 alpha):
`include/capstone/capstone.h`, `cs.c`, `cs_priv.h`, `tests/integration`,
`tests/unit`, `docs/cs_v6_release_guide.md`.

## Workflow

1. Classify the request (API use, option semantics, migration, bug).
2. Open the matching skill below. Prefer one primary skill; add a second only
   when the task spans domains.
3. Do not invent thread-safety guarantees, detail-OFF behavior, or skipdata
   callback offsets — those are covered by specialized skills and must match
   current `cs.c`.

## Route table

| Topic | Skill |
| --- | --- |
| Open/close, version, errno, support, basic lifecycle | [capstone-core-api](../capstone-core-api/SKILL.md) |
| `cs_disasm` vs `cs_disasm_iter`, `cs_malloc`/`cs_free` | [capstone-disasm-iteration](../capstone-disasm-iteration/SKILL.md) |
| `CS_OPT_DETAIL`, `CS_OPT_DETAIL_REAL`, `is_alias`, `usesAliasDetails` | [capstone-detail-aliases](../capstone-detail-aliases/SKILL.md) |
| Operands, `cs_op_*`, `cs_reg_*`, `cs_regs_access` | [capstone-operands-registers](../capstone-operands-registers/SKILL.md) |
| `CS_OPT_SYNTAX*`, mode, mnemonic, unsigned, litbase | [capstone-options-syntax](../capstone-options-syntax/SKILL.md) |
| Skipdata mode and callbacks | [capstone-skipdata](../capstone-skipdata/SKILL.md) |
| Throughput, memory, concurrency limits | [capstone-performance-concurrency](../capstone-performance-concurrency/SKILL.md) |
| v5→v6 rename, compat headers | [capstone-v6-migration](../capstone-v6-migration/SKILL.md) |
| Failure diagnosis, known defects | [capstone-troubleshooting](../capstone-troubleshooting/SKILL.md) |

### Architecture / build / tooling

| Topic | Skill |
| --- | --- |
| One ISA (`CS_ARCH_*`, modes, detail union) | `capstone-arch-<name>` (e.g. [aarch64](../capstone-arch-aarch64/SKILL.md), [x86](../capstone-arch-x86/SKILL.md), [riscv](../capstone-arch-riscv/SKILL.md)) |
| CMake configure / presets / install | [capstone-cmake-build](../capstone-cmake-build/SKILL.md) |
| Cross / Android / Windows / macOS | [capstone-cross-platform](../capstone-cross-platform/SKILL.md) |
| Diet, X86 reduce, arch trim, registration | [capstone-size-optimized-builds](../capstone-size-optimized-builds/SKILL.md) |
| Custom alloc / kernel embed | [capstone-custom-memory-embedding](../capstone-custom-memory-embedding/SKILL.md) |
| `cstool`, YAML `cstest`, bindings, fuzz repro | [cstool](../capstone-cstool/SKILL.md), [cstest-yaml](../capstone-cstest-yaml/SKILL.md), [language-bindings](../capstone-language-bindings/SKILL.md), [fuzzing-crash-repro](../capstone-fuzzing-crash-repro/SKILL.md) |

## Hard facts (always enforce)

- Detail cannot be cleared with `CS_OPT_OFF` in current `cs_option`
  (`detail_opt |= value`).
- Call `cs_option(..., CS_OPT_DETAIL, ...)` before `cs_malloc` when using iter.
- Skipdata callback `offset` differs: batch uses buffer-relative offset; iter
  always passes `0` and a remaining slice.
- Do not promise Capstone is thread-safe. Use one handle per thread; memory
  hooks (`CS_OPT_MEM`) are process-global.
- Default public names are `CS_ARCH_AARCH64` / `CS_ARCH_SYSTEMZ`. Legacy
  `ARM64` / `SYSZ` require compat macros.
- Xtensa default skip size `255` is a probable defect (`skipdata_size` default),
  not documented behavior — see troubleshooting.

## More

- Expanded decision notes: [reference.md](reference.md)
