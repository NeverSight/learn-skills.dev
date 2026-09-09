---
name: modern-go
description: "Modern Go release awareness for any Go source, test, module, tooling, build, upgrade, or API work from Go 1.21 onward."
---

# Modern Go

Anchor Go work in the repository's declared version, not the model's training
cutoff.

## Orient

1. Inspect the `go` and optional `toolchain` directives in `go.mod`, plus
   `go.work`, CI, container, and local toolchain pins when relevant.
2. Separate the module's minimum language/toolchain requirement from the
   toolchain selected to run the build. Use newer features only when the
   declared compatibility target permits them or the task raises that target.
3. Read every release crossed by an upgrade and any release whose feature or
   behavior affects the task.

## Release Radar

- [Go 1.21](references/go1.21.md) — strict toolchain requirements, PGO,
  structured logging, and generic collection helpers.
- [Go 1.22](references/go1.22.md) — per-iteration loop variables, integer
  ranges, enhanced HTTP routing, and `math/rand/v2`.
- [Go 1.23](references/go1.23.md) — range-over-function iterators, timer
  semantics, and iterator-aware library APIs.
- [Go 1.24](references/go1.24.md) — generic type aliases, tool dependencies,
  Swiss maps, weak pointers, and new testing APIs.
- [Go 1.25](references/go1.25.md) — container-aware `GOMAXPROCS`,
  `WaitGroup.Go`, stable `synctest`, and experimental JSON v2.
- [Go 1.26](references/go1.26.md) — `new(expr)`, modernized `go fix`, Green Tea
  GC by default, and test artifacts.

Coverage ends at Go 1.26. For a newer or uncertain toolchain, consult the
current official release history and release notes before making
version-sensitive decisions. Use the bundled files as orientation, then verify
exact APIs and behavior in current official documentation.
