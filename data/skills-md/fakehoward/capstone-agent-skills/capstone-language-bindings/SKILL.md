---
name: capstone-language-bindings
description: >-
  Explains Capstone in-tree language bindings under bindings/ (Python, Java,
  OCaml, PowerShell, VB6) and their boundary versus the CMake C core. Use when
  installing or building bindings, using LIBCAPSTONE_PATH, running cstest_py,
  or asking which languages ship in-tree versus community repos.
---

# Capstone language bindings

## Boundary

| Layer | Where | Built by |
|-------|--------|----------|
| C core + cstool | repo root | CMake (`BUILDING.md`) |
| In-tree bindings | `bindings/<lang>/` (pattern: `python`, `java`, …) | Per-language README / make / pip — **not** root CMake targets |

Root CMake does not install Python/Java/OCaml bindings for you. Bindings wrap
a built or packaged `libcapstone`.

## In-tree directories

- `bindings/python/` — primary; `pip install` / editable install; optional
  `cstest_py`
- `bindings/java/` — JNA-based; `make` + `run.sh`
- `bindings/ocaml/` — `make` with OCaml toolchain
- `bindings/powershell/` — module + prebuilt/local `capstone.dll`
- `bindings/vb6/` — VB6 sample / shim (older Capstone note in its README)

`bindings/README.md` also lists **community** bindings (Go, Ruby, Rust, .NET,
etc.) hosted elsewhere. Do not treat those URLs as maintained in this tree.

## Python notes

- `pip install capstone` / `pip install bindings/python/` may compile the native
  core unless `LIBCAPSTONE_PATH` is set (any value inhibits the bundled build;
  at runtime it can point at a directory with the desired library).
- `cstest_py` is the YAML test runner for Windows/macOS (and Linux); C `cstest`
  is documented as Linux-tested only.

## Agent rules

1. Keep CMake advice for the core; send binding work to the matching README.
2. Distinguish in-tree vs community clearly.
3. Do not claim root `cmake --install` ships all language bindings.

## More detail

- Per-language install pointers: [reference.md](reference.md)
- Common command sequences: [examples.md](examples.md)
