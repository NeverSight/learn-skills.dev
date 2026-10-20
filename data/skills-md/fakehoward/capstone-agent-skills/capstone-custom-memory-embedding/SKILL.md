---
name: capstone-custom-memory-embedding
description: >-
  Configures Capstone for custom allocators and kernel/firmware embedding via
  CAPSTONE_USE_DEFAULT_ALLOC, CS_OPT_MEM, and in-tree Windows/OSX kernel helpers.
  Use when replacing malloc, embedding in drivers or kexts, fixing
  CS_ERR_MEMSETUP, or working under contrib/cs_driver, windows/winkernel_mm, or
  CAPSTONE_OSXKERNEL_SUPPORT.
---

# Capstone custom memory and embedding

## CMake switch

| CMake option | Default | Effect |
|--------------|---------|--------|
| `CAPSTONE_USE_DEFAULT_ALLOC` | `ON` | Defines `CAPSTONE_USE_SYS_DYN_MEM` and wires libc (or kernel) defaults |

Turn it off for fully user-supplied allocators:

```bash
-DCAPSTONE_USE_DEFAULT_ALLOC=OFF
```

Do not pass `-DCAPSTONE_USE_SYS_DYN_MEM=...` to CMake; that name is the compile
define / legacy Make variable, not the CMake option.

## Runtime API

Call once **before** `cs_open()` (handle may be `0`):

```c
cs_opt_mem mem = { my_malloc, my_calloc, my_realloc, my_free, my_vsnprintf };
cs_option(0, CS_OPT_MEM, (size_t)&mem);
```

If allocators stay NULL with default alloc disabled, APIs fail with
`CS_ERR_MEMSETUP`.

## In-tree embedding aids

- `windows/winkernel_mm.*` — Windows kernel malloc/vsnprintf shims.
- `contrib/cs_driver/` — sample VS driver using Capstone (see its README/comments).
- `contrib/windows_kernel/` — alternate C++ helpers for missing CRT pieces.
- `CAPSTONE_OSXKERNEL_SUPPORT=ON` — OS X kext-oriented build define
  (`CAPSTONE_HAS_OSXKERNEL`).

## Agent rules

1. Always name the CMake flag `CAPSTONE_USE_DEFAULT_ALLOC`.
2. Stress `CS_OPT_MEM` ordering relative to `cs_open`.
3. Do not promise a single turnkey kernel CMake product beyond the flags and
   sample trees that exist.

## More detail

- Kernel IRQL / floating-point notes: [reference.md](reference.md)
- Build + call sequences: [examples.md](examples.md)
