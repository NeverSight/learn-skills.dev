---
name: rust-test-tools
description: Use when choosing, adding, or reviewing a Rust test tool beyond plain cargo test, such as loom for hand-rolled atomics and lock-free code, proptest and cargo-fuzz for parsers of untrusted bytes, cargo-careful as an extra lane beside a sanitizer for FFI code that Miri cannot run, cargo-mutants with survived-mutant triage for weak tests, golden or snapshot files for deterministic output, and a differential fuzz target for a port with a reference implementation. Not for the test-first cycle (rust-tdd) or Miri and sanitizer setup (rust-sanitizers-miri).
license: BSD-3-Clause
---

# Rust Test Tools

A green `cargo test` does not find undefined behavior (UB), atomic-ordering bugs, parser edge
cases, weak assertions, or output drift. Pick the tool by the risk that the change adds. Run it
on the crate that the change touches while you iterate. Run the full lane once before merge.

## Pick the tool

| The change adds | Run | A green run does not prove |
|---|---|---|
| Pure-Rust `unsafe`: raw pointers, `transmute`, `MaybeUninit`, `from_raw_parts` | Miri. The `rust-sanitizers-miri` skill owns the flags and the aliasing-model policy | UB freedom on paths that the tests do not reach |
| `unsafe` next to foreign code: FFI, JNI, libc, syscalls | ASan on the host, or HWASan or MTE on a device; TSan when the code shares state across threads. Also Miri on the pure-Rust helpers, with the foreign calls stubbed under `#[cfg(miri)]` | UB freedom: a sanitizer does not know the Rust aliasing rules |
| Hand-rolled atomics, a spinlock, a lock-free structure, a publish flag | loom | freedom from bugs that need load buffering or more preemptions than the bound |
| A parser, a decoder, or any function that reads untrusted bytes | proptest, then cargo-fuzz | freedom from bugs that the strategy or the corpus never reaches |
| A port whose reference a test can call in-process | a differential fuzz target | equivalence outside the inputs that the fuzzer reached |
| A refactor of tested logic, or new tests for a critical change | cargo-mutants on the diff, or on the source files under test when the diff only adds tests | that the asserted values are the correct ones |
| Output that must be deterministic: serialized records, generated code, reports, images | golden files | that the first blessed baseline is correct |
| None of the above | the normal test run | behavior that no test asserts |

Code that uses only `std::sync::Mutex` or `RwLock`, or data-parallel code (for example rayon)
with no hand-rolled atomics, does not need loom.

## Lanes and cadence

If cargo-nextest is installed, use it as the runner, and run doctests separately. Keep
`--locked` so that a test run cannot rewrite `Cargo.lock`.

```bash
cargo nextest run --locked -p <crate> --no-fail-fast
cargo test --locked -p <crate> --doc

# Without nextest.
cargo test --locked -p <crate> --no-fail-fast
```

Run the tests for `unsafe` code in a debug build at least once: since Rust 1.78, std checks
unsafe preconditions only when debug assertions are on.

| Lane | Command | When |
|---|---|---|
| Tests, proptest, golden files | `cargo nextest run --locked --workspace` and `cargo test --locked --workspace --doc` | every pull request |
| cargo-careful | `cargo +nightly careful test --locked -p <ffi-crate> --no-fail-fast` | pull requests that touch `unsafe` or FFI crates |
| Miri, sanitizers | the `rust-sanitizers-miri` skill | pull requests that touch `unsafe`, and on a schedule |
| loom | `RUSTFLAGS="--cfg loom" cargo test --locked --release --test 'loom_*'`, with no tokio in the graph (`references/loom.md`) | pull requests that touch hand-rolled atomics |
| cargo-fuzz | `cargo +nightly fuzz run <target> -- -max_total_time=900` for each `cargo fuzz list` entry | nightly or weekly schedule, not every pull request |
| cargo-mutants | `--in-diff` run on demand, full run on a schedule | after a refactor, and weekly |

The `cargo-workflows` skill owns nextest profiles (`.config/nextest.toml`, run with
`cargo nextest run --locked --profile ci`) and pins each GitHub Action to a full commit SHA.

## Review gate

Before you approve a change, confirm each item that applies:

- [ ] New pure-Rust `unsafe`, FFI helpers included (foreign calls stubbed under `#[cfg(miri)]`),
      has a Miri run when nightly `miri` is installed; otherwise the report names it as not
      checked by Miri. A careful run alone is not UB evidence.
- [ ] New `unsafe` across FFI has an ASan run on the host, or a HWASan or MTE run on a device,
      and a TSan run when it shares state across threads.
- [ ] Every new hand-rolled atomic or lock-free primitive has a loom test that calls the crate's
      own type. The loom lane selects only the loom targets.
- [ ] Every new parser or decoder has a never-panics property, a roundtrip property where a
      roundtrip exists, and committed proptest regression files.
- [ ] Every fuzz crash is a committed, minimized regression test.
- [ ] A port with an in-process reference has a differential fuzz target.
- [ ] A refactor of tested logic has a cargo-mutants run on the diff. Each missed mutant has a
      test or a recorded exclusion.
- [ ] Deterministic output has committed golden files. Each fixture change is a reviewed,
      deliberate commit.

## cargo-careful

cargo-careful rebuilds std with debug assertions and runs code that Miri cannot run. It is a
cheap extra lane, not a UB proof: it does not check aliasing, uninitialized reads,
use-after-free, or data races.

Read [references/cargo-careful.md](references/cargo-careful.md) when you set up the lane (nightly
and `rust-src`), need the list of checks, or a flag from `target.<triple>.rustflags` is missing
in the careful run.

## loom

loom runs a test body under every interleaving that the preemption bound allows, and models
the C11 orderings. Know its limits:

- loom checks only the operations on its own types (`loom::sync::atomic`,
  `loom::cell::UnsafeCell`, `loom::thread::spawn` under `cfg(loom)`). A race on a `std` type is
  invisible to it.
- loom treats `SeqCst` loads and stores as `AcqRel`, and does not explore load buffering.
- Under `cfg(loom)`, every spin or retry loop must call `loom::thread::yield_now()`, or the
  model fails with "Model exceeded maximum number of branches".

Declare loom under `[target.'cfg(loom)'.dependencies]`, because the library itself imports it,
and add a `check-cfg` entry for `cfg(loom)`. Do not use a `loom` Cargo feature: `--all-features`
turns it on, and every ordinary test that touches the primitive then panics. Make the loom test
call the crate's own type. Select only the loom targets (`--test 'loom_*'`); other tests that
touch the primitive panic outside `loom::model`, so gate them with `#[cfg(not(loom))]`.

Read [references/loom.md](references/loom.md) before you trust a loom result (its limits), when
you set up loom in a crate, gate a `static` atomic or an `UnsafeCell`, or must bound a slow run.

## proptest

Write properties for any function that takes bytes, text, or a configuration value and
produces a parsed or validated result. Assert invariants, not single examples.

Read [references/proptest.md](references/proptest.md) for the four property shapes:
never-panics, roundtrip, structured roundtrip, and text.


- Random bytes seldom get past a magic number or a checksum. The structured strategy reaches
  the deeper code, so write one for every format with such a check.
- A line-based parser tested with `".*"` or `any::<String>()` never sees a newline (probe on
  proptest 1.12.0). Use `"(?s).*"`.
- proptest saves each failing case and runs it first on the next run. A test in `src/` saves to
  `proptest-regressions/` at the crate root. An integration test saves to
  `tests/<name>.proptest-regressions`. Commit these files.
- For a deeper local run, raise the case count:
  `PROPTEST_CASES=10000 cargo test --locked -p <crate> parse_`.

A new parser without a never-panics property is incomplete.

## cargo-fuzz

proptest finds the bugs that a strategy can reach. A coverage-guided fuzzer also finds the
bugs that only a mutated corpus reaches, above all in binary protocol and container decoders.

- Fuzz the outermost entry point that takes untrusted bytes.
- Cap an allocation length and a nesting depth in the parser, not in the fuzz target.
- Turn every crash into a committed regression test. Shrink it first with
  `cargo +nightly fuzz tmin <target> <artifact>`.

Read [references/fuzzing.md](references/fuzzing.md) when you set up cargo-fuzz, write a fuzz
target, reproduce a crash, or read a stack-overflow report.

## Differential testing

When a port's reference runs in-process (a C library, the previous Rust version, a spec
model), run a differential fuzz target; a Python or JavaScript original gets the `rust-port`
recorded comparison. Feed both the same bytes. Compare acceptance and the value, and the error
kind when callers depend on it. Seed the corpus with non-ASCII text and invalid UTF-8. Read
[references/fuzzing.md](references/fuzzing.md) when you write the target.

## cargo-mutants

cargo-mutants changes the code (a default body, a flipped comparison, a deleted call) and reruns
the tests for each change. A mutant that survives marks code that the tests run but do not check.

```bash
cargo install --locked cargo-mutants

# Fastest useful loop: only the lines that the branch changes.
git diff origin/main...HEAD > /tmp/pr.diff
cargo mutants --test-tool nextest --cargo-arg=--locked --in-diff /tmp/pr.diff --package <crate> -j2 --output target/

# One whole crate.
cargo mutants --test-tool nextest --cargo-arg=--locked --package <crate> -j2 --output target/
```

Without cargo-nextest, drop `--test-tool nextest`; cargo-mutants then runs `cargo test`.

A diff that only adds tests gives no mutants; run `--file <source-file>` instead. Exit code 2
means mutants survived; exit code 4 means the suite fails before any mutation. Triage
`mutants.out/missed.txt`: it is the gate, not a score. For each missed mutant, write a test that
asserts the exact value or side effect, or exclude untestable code (`Display`, logging, FFI glue)
with `exclude_re` or `#[mutants::skip]` and a recorded reason. Never write a meaningless test to
raise the count.

Do not block every pull request on a full run: it takes minutes to hours, and some mutants are
equivalent to the original code.

Read [references/mutation-testing.md](references/mutation-testing.md) when you write
`.cargo/mutants.toml`, pick `-j` or `--dir`, need the full flag or exit-code table, suspect a
false positive (for example a doctest-only behavior under nextest), or set up the scheduled CI
workflow.

## Golden files

A golden test compares output that another party reads with a committed file.

- Never set the bless variable in CI. A missing fixture must fail the run.
- Bless only an intended output change, and explain the contract change in the commit message.
  Never bless to turn a red run green.
- Replace timestamps, generated IDs, ports, temporary paths, and host names with placeholders,
  and iterate a hash map in sorted order.
- Do not build a golden file from `Debug` (`{:?}`) output: std does not keep that format stable.
- If the crate already uses `insta`, use `cargo insta review`. Do not add a second mechanism.

Read [references/golden-files.md](references/golden-files.md) when you write the helper, set up
`.gitattributes` for fixtures, or compare binary or image output.

## Related skills

When installed: `rust-sanitizers-miri` (Miri flags, `#[cfg(miri)]` stubs, sanitizers),
`memory-model` (atomic orderings; it pairs loom with
`MIRIFLAGS="-Zmiri-many-seeds=0..16" cargo +nightly miri test --locked`), `rust-unsafe` (SAFETY
contracts), and `rust-tdd` (the test-first cycle).
