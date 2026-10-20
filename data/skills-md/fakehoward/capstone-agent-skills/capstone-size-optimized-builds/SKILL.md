---
name: capstone-size-optimized-builds
description: >-
  Shrinks Capstone binaries via architecture selection, diet mode, X86 reduce,
  and related CMake flags. Use when reducing library size, embedding a compact
  engine, enabling CAPSTONE_BUILD_DIET or CAPSTONE_X86_REDUCE, trimming unused
  architectures, or using CAPSTONE_USE_ARCH_REGISTRATION.
---

# Capstone size-optimized builds

## Size levers (CMake)

1. **Fewer architectures** — set `CAPSTONE_ARCHITECTURE_DEFAULT=OFF`, then enable
   only needed `CAPSTONE_<ARCH>_SUPPORT` options.
2. **Diet** — `CAPSTONE_BUILD_DIET=ON` (drops detail-oriented data; many detail
   APIs return `CS_ERR_DIET`).
3. **X86 reduce** — `CAPSTONE_X86_REDUCE=ON` for a smaller X86 instruction set.
4. **Drop AT&T** — `CAPSTONE_X86_ATT_DISABLE=ON` if unused.
5. **Skip tools** — `CAPSTONE_BUILD_CSTOOL=OFF` when the CLI is not needed
   (default is ON for top-level builds).
6. **Arch registration** — `CAPSTONE_USE_ARCH_REGISTRATION=ON` so each consumer
   calls `cs_arch_register_*()` before `cs_open` (one static build, selective
   use). **Gap:** there is no public `cs_arch_register_hppa` or
   `cs_arch_register_xtensa`; use compile-time `CAPSTONE_HPPA_SUPPORT` /
   `CAPSTONE_XTENSA_SUPPORT` instead of selective registration for those.

## Defaults to remember

- Static ON, shared OFF.
- Diet and X86 reduce OFF unless set.
- All arches ON unless you flip `CAPSTONE_ARCHITECTURE_DEFAULT` or individual
  supports.

## Agent rules

1. Warn that diet removes detail features callers may expect.
2. Do not invent size flags beyond `CMakeLists.txt`.
3. Do not invent `cs_arch_register_hppa` / `cs_arch_register_xtensa`.
4. For embedding with custom allocators, pair with
   `CAPSTONE_USE_DEFAULT_ALLOC=OFF` and the custom-memory skill.

## More detail

- Flag interactions and diet caveats: [reference.md](reference.md)
- Configure snippets: [examples.md](examples.md)
