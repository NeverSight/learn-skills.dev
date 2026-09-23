---
name: go-style-guide
description: >
  Provides Go (Golang) engineering guidance for designing packages, services,
  and CLIs. Use whenever the task involves Go implementation, refactors, code
  reviews, API design, package layout, interfaces, constructors/config, error
  handling, logging, dependency or framework selection, HTTP/service wiring,
  concurrency/lifecycle, tests, benchmarks, godoc, or maintainability decisions.
license: Apache-2.0
metadata:
  author: "Benjamin Cane"
  version: "1.0.1"
---

# Go (Golang) Style Guide Skill

This skill defines practical Go engineering conventions for humans, coding
agents, and production-ready systems.

Use this skill whenever you are working with Go: new code, refactors, reviews,
architecture decisions, package design, or test strategy.

---

## TL;DR

- Design for testability first; inject dependencies and keep logic pure.
- Prefer `Config` in -> concrete struct out; validate, default, and document
  important runtime knobs.
- Errors are contracts: use sentinels for durable branching; wrap the rest with
  `%w` or `errors.Join`.
- Keep packages reusable: no hidden globals, no default logging, no surprise
  side effects.
- Prefer the standard library before adding dependencies; third-party packages
  must earn their weight through meaningful, maintained, adopted abstraction.
- Coverage is a signal, not proof; test edge cases and misuse paths, not just
  happy paths.
- Follow "accept interfaces, return structs"; consumers usually define
  interfaces, shared contract packages are a special case.
- Keep `main.go` thin; follow existing repo layout conventions rather than
  forcing one directory shape.
- Benchmark hot paths before claiming wins, and run concurrency code with
  `-race`.
- Maintain contracts such as function signatures, config shape, error behavior,
  and doc comments; they are as important as the code itself.

---

## House Style Disclaimer

This is intentionally opinionated. It favors consistency and long-term
maintainability over accommodating every Go style preference. If the target repo
has clear local conventions, those conventions usually win.

---

## Compatibility

Examples assume modern Go and use standard-library features such as
`errors.Join` and `log/slog`. Apply the guide within the constraints of the
target repository's supported Go version.

---

## Execution Protocol

Follow this workflow when using the skill for implementation work:

1. Inspect the repository first.
   Read existing package layout, constructors, tests, and error conventions
   before proposing new APIs or moving files.

2. Define the contract before coding.
   Decide the package boundary, config shape, concrete return type, sentinel
   errors, dependency seams, and context or shutdown expectations up front.

3. Write or update tests early when practical.
   Start with table-driven unit tests, add fuzz tests for parsing or other
   input-heavy code, and add benchmarks for performance-sensitive paths.

4. Implement the smallest maintainable change.
   Follow the repository's existing layout, keep `main.go` thin, and avoid
   introducing new abstractions without a clear boundary.

5. Run the finishing checks.
   Format with `gofmt` (and `goimports` if the repo uses it), run the relevant
   `go test` targets, run `go test -race` when concurrency is involved, and run
   benchmarks when claiming performance improvements.

6. Verify the human-facing contract.
   Make sure docs, comments, config defaults, and error behavior match the code
   you are shipping.

---

## Quick Rules Table

| Topic | Rule | Reference |
| --- | --- | --- |
| Testability | Design for confidence, not coverage percentages; test edge and misuse cases | `references/TESTING.md` |
| Constructors | `Config` in -> concrete struct out; validate + default in `New`; use `Config.Validate()` when config logic grows | `references/CONFIG.md` |
| Errors | Use sentinels for durable branching; wrap with `%w` or `errors.Join`; keep `recover` at app boundaries | `references/ERRORS.md` |
| Logging | Packages do not log by default; hot-path logging is a performance decision | `references/LOGGING.md` |
| Dependencies | Standard library first; add third-party packages only when they provide meaningful, maintained value | `references/LAYOUT.md` |
| Interfaces | "Accept interfaces, return structs"; consumers usually define interfaces | `references/INTERFACES.md` |
| Documentation | Write idiomatic godoc and durable comments; never add agent-context comments | `references/DOCUMENTATION.md` |
| Layout | Keep packages shallow, avoid junk drawers, and follow repo conventions | `references/LAYOUT.md` |
| Entry Points | `main.go` is wiring only | `references/LAYOUT.md` |
| Benchmarks | Benchmark hot paths; use `b.ReportAllocs()` and compare runs with `benchstat` | `references/BENCHMARKS.md` |
| Testing | Table-driven, stdlib-first, defensive against misuse, and fuzz-heavy where inputs are complex | `references/TESTING.md` |
| Concurrency | Every goroutine needs a shutdown path; use `context.Context`, `-race`, and jitter where needed | `references/CONCURRENCY.md` |
| Reviews | Use the checklist when reviewing Go changes | `references/REVIEW-CHECKLIST.md` |

---

## Common Pitfalls

- Returning interfaces by default instead of concrete types.
- Treating coverage percentages as proof of correctness.
- Logging in reusable packages instead of returning errors.
- Adding frameworks or helper libraries when the standard library is already
  clear enough.
- Passing global app config through packages rather than local `Config`.
- Leaving critical runtime knobs on dangerous defaults.
- Forcing a house directory layout onto repos that already have clear
  conventions.
- Loading every reference document before you know which topic the task touches.
- Shipping changes that claim performance wins without benchmarks or
  concurrency safety without `-race`.

---

## Core Guidance

Load reference files only when the task needs that topic's detail.

- App packages own dependency wiring, lifecycle, error policy, logging, and
  metrics policy.
- Reusable packages return errors, define local `Config` or `Opts`, accept
  initialized dependencies, and avoid hidden logging or global state.
- Dependency choices should start with the standard library. Reach for a
  third-party package only when it solves a real problem, is actively
  maintained, and earns its transitive cost.
- Services usually keep `cmd/<appname>/main.go` thin. Follow established repo
  layout over forcing `pkg/`, `internal/`, or any house shape.
- Libraries usually keep packages shallow and domain-focused.
- Constructors prefer `New(cfg Config) (*T, error)`, explicit defaults,
  validation, concrete returns, and immutable normalized config.
- Interfaces should be small, boundary-driven, and usually consumer-defined.
- Tests should be table-driven, stdlib-first, defensive, and run with `-race`
  for concurrency-sensitive code.
- Performance claims need benchmarks.
- Docs, comments, config defaults, error behavior, and signatures are part of
  the contract.

---

## Reference Loading

Load only the references needed for the active task:

- Read [references/CONFIG.md](references/CONFIG.md) for constructors,
  `Config` structs, defaults, validation, degraded modes, or logging injection.
- Read [references/INTERFACES.md](references/INTERFACES.md) for interface
  boundaries, driver patterns, mocks/fakes, or concrete return decisions.
- Read [references/ERRORS.md](references/ERRORS.md) for sentinel errors,
  wrapping, typed errors, recover placement, or constructor failures.
- Read [references/LOGGING.md](references/LOGGING.md) for package logging,
  `slog`, log levels, async error surfaces, or payload safety.
- Read [references/TESTING.md](references/TESTING.md) for table-driven tests,
  fuzzing, `testdata`, integration gates, test helpers, or assertion choices.
- Read [references/CONCURRENCY.md](references/CONCURRENCY.md) for goroutines,
  context propagation, graceful shutdown, mutex/atomic/channel choices, jitter,
  or race testing.
- Read [references/LAYOUT.md](references/LAYOUT.md) for package layout, file
  naming, `main.go`, dependency hygiene, struct field layout, or export rules.
- Read [references/DOCUMENTATION.md](references/DOCUMENTATION.md) for package
  docs, godoc, examples, deprecations, internal comments, or field docs.
- Read [references/BENCHMARKS.md](references/BENCHMARKS.md) for benchmark
  shape, allocation reporting, concurrent benchmarks, IO benchmarks, or
  `benchstat`.
- Read [references/REVIEW-CHECKLIST.md](references/REVIEW-CHECKLIST.md) when
  reviewing a Go PR or doing a final self-check.
