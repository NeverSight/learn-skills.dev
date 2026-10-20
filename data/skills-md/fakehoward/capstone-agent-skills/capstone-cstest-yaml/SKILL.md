---
name: capstone-cstest-yaml
description: >-
  Runs and authors Capstone YAML disassembly tests with cstest or cstest_py,
  including boolean encoding quirks and enum mapping. Use when building
  CAPSTONE_BUILD_CSTEST, writing tests under tests/, fixing cstest mismatches,
  MC YAML updates, or encoding is_alias / skip fields.
---

# Capstone cstest and YAML tests

## Tools

| Tool | Location | Notes |
|------|----------|--------|
| `cstest` | `suite/cstest/` | C runner; enable with `-DCAPSTONE_BUILD_CSTEST=ON` |
| `cstest_py` | `bindings/python/cstest_py/` | Python runner; preferred on Windows/macOS |

YAML inputs live under repo `tests/` (details, MC, issues, features, negative,
…). Minimal shape: `suite/cstest/test/min_valid_test_file.yaml`.

## Build cstest (CMake)

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Debug -DCAPSTONE_BUILD_CSTEST=ON
cmake --build build --config Debug
```

Needs `libyaml` (or CMake builds it). C `cstest` is **only tested on Linux**
per `BUILDING.md` / `tests/README.md`. Elsewhere install `cstest_py`.

Also pulls unit/integration CMake tests under `tests/unit` and
`tests/integration` when CSTEST is ON.

## YAML boolean quirk (important)

C YAML parsing uses integers:

| Value | Meaning |
|-------|---------|
| `1` | true |
| `0` | unset / absent |
| `-1` | false |

Do not write YAML `true`/`false` if the field expects this `tbool` scheme
(e.g. `is_alias`, `post_indexed` style fields).

## Enum strings

C enum identifiers in YAML must exist in
`suite/cstest/include/test_mapping.h` or `cstest` cannot map them.

## Agent rules

1. Prefer copying an existing YAML file over inventing schema.
2. Use `skip` + `skip_reason` for known MC mismatches (feature-variant caveat).
3. Do not promise Auto-Sync/`MCUpdater` success without llvm-mc, FileCheck, and
   Auto-Sync install steps from `suite/auto-sync/`.

## More detail

- Layout, ctest, MC updater caveats: [reference.md](reference.md)
- Commands and minimal YAML: [examples.md](examples.md)
