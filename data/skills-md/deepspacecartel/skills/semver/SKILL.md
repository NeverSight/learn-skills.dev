---
name: semver
description: How to apply Semantic Versioning 2.0.0 (https://semver.org/) - project-agnostic. Covers the MAJOR.MINOR.PATCH rules, pre-release and build-metadata grammar, precedence rules for comparing versions, and the 0.y.z/1.0.0 FAQ. Use when deciding what the next version number should be, tagging a release, or reviewing whether a version bump matches what actually changed.
---

# Semantic Versioning (SemVer 2.0.0)

Given `MAJOR.MINOR.PATCH`, the spec-mandated rule
([semver.org](https://semver.org/)):

1. **MAJOR** — incompatible (breaking) API changes.
2. **MINOR** — new functionality, backward compatible.
3. **PATCH** — bug fixes, backward compatible.

This is a promise to your users, not a changelog summary — the
version number itself has to be trustworthy enough that someone can
upgrade a PATCH release blind, with zero risk of breakage.

## The rules that actually matter day to day

- **Declare a public API** first (in code, in docs, however) —
  SemVer only means something relative to what you've promised not to
  break. No declared API, no way to know if a change is breaking.
- **A released version is immutable.** Found a bug in `1.4.2` the day
  after tagging it? That's `1.4.3`, never an amended `1.4.2` — anyone
  who already pulled `1.4.2` needs to see a new version to know
  something changed.
- **PATCH** only for backward-compatible bug fixes — no new public API
  surface, even a small one.
- **MINOR** for backward-compatible new functionality, *and* whenever
  you deprecate part of the public API (the deprecation itself isn't
  breaking yet — removing it later is a MAJOR).
- **MAJOR** for any backward-incompatible change — a removed function,
  a changed required parameter, a changed default that alters
  behavior.
- **`0.y.z` means initial development** — "anything MAY change at any
  time," the public API is explicitly not yet considered stable. Don't
  read a `0.x` MINOR bump as carrying the same backward-compatibility
  promise a `1.x` MINOR bump does.
- **`1.0.0` is the commitment point** — ship it once there's a
  stable public API users depend on. Per the spec's own FAQ:
  "If your software is being used in production, it should probably
  already be 1.0.0."

## Pre-release and build metadata

```
1.0.0-alpha          # pre-release
1.0.0-alpha.1        # pre-release, dot-separated identifiers
1.0.0-0.3.7          # pre-release, numeric identifier
1.0.0-alpha+001      # pre-release + build metadata
1.0.0+20130313144700 # release + build metadata only
```
- A pre-release suffix (`-alpha`, `-rc.1`, ...) comes right after
  `PATCH`, and marks the version as **not yet stable** — tooling
  should not install it over a caller's explicit opt-in.
- Build metadata (`+001`, `+build.5`) can follow the version *or* the
  pre-release tag, and is **ignored for precedence** — `1.0.0+001` and
  `1.0.0+002` are the exact same version as far as comparison goes,
  the suffix is just an informational tag (a commit SHA, a CI build
  number).

## Precedence rules (how two versions actually compare)

1. Compare `MAJOR`, then `MINOR`, then `PATCH` numerically:
   `1.0.0 < 2.0.0 < 2.1.0 < 2.1.1`.
2. A pre-release version has **lower** precedence than its normal
   release: `1.0.0-alpha < 1.0.0`.
3. Pre-release identifiers compare left to right, dot-separated field by
   field: numeric fields compare numerically, alphanumeric fields
   compare lexically (ASCII sort), and a numeric field always has
   *lower* precedence than an alphanumeric one at the same position.

Worked example, low to high:
```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta
  < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
```

## Validation regex

```regex
^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
```
Use this (or your language's equivalent with named capture groups,
also published on semver.org) to validate a version string before
tagging, rather than hand-rolling a looser check.

## Starting a new project

Per the spec's own FAQ: start at `0.1.0`, increment `MINOR` for each
pre-1.0 release (`0.2.0`, `0.3.0`, ...) — don't invent your own
pre-1.0 numbering scheme, this is already the documented convention.

## What NOT to do

- Don't bump only `PATCH` for a change that removes or renames a public
  function, even if "it was barely used" — the version number is the
  one place that promise can't be judgment-called away.
- Don't leave leading zeros in any segment (`1.01.0` is invalid, not
  just unconventional) — the spec explicitly forbids it.
- Don't treat build metadata as meaningful for version *ordering* — if
  two consumers need to compare versions, strip `+...` first or use a
  semver-aware comparison library that already does.
