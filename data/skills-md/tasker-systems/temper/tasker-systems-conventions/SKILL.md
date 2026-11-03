---
name: tasker-systems-conventions
description: The tasker-systems engineering baseline as this repository is pinned to it — the rules,
  why each exists, and whether a gate enforces it here. Use before adding a lint suppression, an
  unsafe block, a dependency, a CI workflow, a test exception, or agent guidance; and whenever you
  are about to claim a rule is enforced.
---

# tasker-systems conventions

This skill is **projected** into this repository from the `tasker-systems/conventions` baseline at
the revision pinned in `.conventions/consumer.toml`. Do not edit it here: `conventions.py bump`
rewrites it, and CI fails if it differs from the projection (CONS-6).

The doctrine itself is in `.conventions/baseline/doctrine/`. Read the file for the area you are
touching; each rule states its *why* beside it, and its id is what you cite in a PR or an
`#[expect(reason)]`.

| Touching | Read |
|---|---|
| The rule register: every rule, and its status in each consumer | `.conventions/baseline/doctrine/rules.md` |
| The short list everything follows from | `.conventions/baseline/doctrine/tenets.md` |
| Rust: lints, formatting, API shape, unsafe, errors, panics, toolchain | `.conventions/baseline/doctrine/rust.md` |
| Python | `.conventions/baseline/doctrine/python.md` |
| TypeScript | `.conventions/baseline/doctrine/typescript.md` |
| Shell scripts and CI gate scripts | `.conventions/baseline/doctrine/shell.md` |
| Markdown | `.conventions/baseline/doctrine/docs.md` |
| HTTP API JSON and OpenAPI | `.conventions/baseline/doctrine/api.md` |
| Dependencies, advisories, licenses, Actions, tool pins | `.conventions/baseline/doctrine/supply-chain.md` |
| Credentials, redaction, SQL, auth | `.conventions/baseline/doctrine/security.md` |
| Channels, spawned work, locks, database coordination | `.conventions/baseline/doctrine/concurrency.md` |
| Tests and CI shape | `.conventions/baseline/doctrine/testing.md` |
| Writing a tripwire | `.conventions/baseline/doctrine/tripwires.md` |
| Agent guidance | `.conventions/baseline/doctrine/agent-guidance.md` |
| This repository's pin, exceptions and statuses | `.conventions/baseline/doctrine/consuming.md` |

## Before you claim a rule is enforced

Check the status below. `gated: <gate>` means a named check fails on a violation **here**. Anything
else — `partial`, `practiced`, `convention`, `uncovered`, `unexamined` — means nothing here would
catch a violation, and saying otherwise is the defect tenet 1 names. An unlisted rule is
unexamined in this repository, not covered.

Local departures from the baseline, each with its reason, are in `.conventions/exceptions.toml`.

<!-- consumer-status:begin -->

Statuses for **temper**:

| Rule | Status here |
|---|---|
| AG-1 | practiced |
| AG-2 | convention: whether each rule states its reason is judged in review |
| AG-3 | uncovered: most internal/agents rules do not say whether a gate enforces them |
| AG-4 | partial: README and docs CLI claims and counts are drift-checked (quality-gate.yml#guard-tests, code-quality.yml#rust-quality); internal/agents is not |
| AG-5 | gated: .github/workflows/quality-gate.yml#conventions |
| AG-6 | practiced |
| API-JSON-1 | uncovered: no casing check; 12 non-snake properties and one non-snake enum value in openapi.json |
| API-JSON-2 | uncovered: one error schema, but no per-variant validation against the spec |
| API-JSON-3 | uncovered: 2 of 26 *_at fields lack format date-time |
| API-JSON-4 | practiced |
| API-JSON-5 | uncovered: 26 list responses are bare arrays that cannot signal truncation |
| CI-1 | partial: quality-gate runs on every change, but its Rust half is scope-gated and only code-quality and test-rust wait on it |
| CI-2 | gated: .github/workflows/ci.yml#ci-success |
| CI-3 | gated: .github/workflows/code-quality.yml#rust-quality, .github/workflows/test-agents-ts.yml#temper-ts, .github/workflows/test-python.yml#test-python, .github/workflows/test-ruby.yml#test-ruby |
| CI-4 | practiced |
| CI-5 | practiced |
| CI-6 | practiced |
| CONC-BOUND-1 | gated: .github/workflows/code-quality.yml#rust-quality |
| CONC-BOUND-2 | uncovered: pool and channel capacities are literals in production code |
| CONC-BOUND-3 | convention: the at-bound strategy is a design decision judged in review |
| CONC-BOUND-4 | uncovered: no depth or saturation metrics for in-process bounds |
| CONC-DB-1 | convention: atomic transitions in the database are reviewed per change |
| CONC-DB-2 | convention: retry idempotency is designed and reviewed per operation |
| CONC-DB-3 | convention: transaction scope is judged in review |
| CONC-FAIL-1 | practiced |
| CONC-FAIL-2 | convention: span-per-act is a code-quality.md review rule; spawns are not named |
| CONC-FAIL-3 | uncovered: shape_loader.rs recovers poisoned locks at two production sites (the verdict cache) with no comment |
| CONS-1 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-2 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-3 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-4 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-5 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-6 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-7 | gated: .github/workflows/quality-gate.yml#conventions |
| CONS-8 | gated: .github/workflows/quality-gate.yml#conventions |
| DOC-1 | uncovered: no markdownlint in CI |
| DOC-2 | uncovered: no markdownlint in CI |
| DOC-3 | uncovered: no markdownlint in CI |
| DOC-4 | partial: relative links under docs/ are checked offline (quality-gate.yml#guard-tests); README, internal/ and agent guidance are not |
| PY-DEF-1 | gated: .github/workflows/quality-gate.yml#python-lint |
| PY-ERR-1 | gated: .github/workflows/quality-gate.yml#python-lint |
| PY-ERR-2 | gated: .github/workflows/quality-gate.yml#python-lint |
| PY-GEN-1 | gated: .github/workflows/test-python.yml#test-python |
| PY-LINT-1 | gated: .github/workflows/quality-gate.yml#python-lint |
| PY-LINT-2 | partial: the root ruff.toml is pinned to the projection (quality-gate.yml#conventions); an override in clients/temper-py's [tool.ruff] is caught only in review |
| PY-LINT-3 | partial: a suppression without a code, or an unused one, fails (quality-gate.yml#python-lint); its reason is review |
| PY-LOG-1 | gated: .github/workflows/quality-gate.yml#python-lint |
| PY-TYPE-1 | gated: .github/workflows/test-python.yml#test-python |
| PY-TYPE-2 | n/a: no native module |
| PY-VER-1 | partial: target-version is the projection's (quality-gate.yml#conventions); requires-python in clients/temper-py and packages/temper-design, and mypy's python_version, match it by hand |
| RUST-API-1 | convention: whether a crate is a library or an application is judged in review |
| RUST-API-2 | convention: open versus closed sets are judged in review |
| RUST-API-3 | gated: .github/workflows/code-quality.yml#rust-quality |
| RUST-API-4 | gated: .github/workflows/code-quality.yml#rust-quality |
| RUST-API-5 | partial: wrong_self_convention fails under default clippy -D warnings; constructor and getter naming is review |
| RUST-API-6 | convention: where ignoring a value is a bug is judged in review |
| RUST-DOC-1 | uncovered: the published library crates do not warn on missing docs |
| RUST-ERR-1 | practiced |
| RUST-ERR-2 | convention: whether a default stands in for a required value is judged in review |
| RUST-ERR-3 | convention: panic-or-Result and # Panics docs are judged in review |
| RUST-ERR-4 | uncovered: about 10 non-test unwrap() sites; unwrap_used is not enabled |
| RUST-FMT-1 | gated: .github/workflows/quality-gate.yml#rust-gate |
| RUST-INIT-1 | practiced |
| RUST-LINT-1 | uncovered: no workspace lint table yet; adopting the canonical one is the next step |
| RUST-LINT-2 | gated: .github/workflows/code-quality.yml#rust-quality |
| RUST-LINT-3 | uncovered: 43 #[allow] without a reason; the lints that refuse them arrive with the lint table |
| RUST-LINT-4 | convention: a review practice; the lint table's adoption is measured first (266 findings) and lands as its own change |
| RUST-LINT-5 | n/a: no lint table yet; clippy runs its default groups |
| RUST-MACRO-1 | convention: macro or function is judged in review |
| RUST-ORG-1 | uncovered: about 7 non-test glob imports; wildcard_imports is not enabled |
| RUST-ORG-2 | convention: file naming and module layout are judged in review |
| RUST-PANIC-1 | practiced |
| RUST-READ-1 | convention: readability is judged in review |
| RUST-SQL-1 | gated: .github/workflows/quality-gate.yml#rust-gate, .github/workflows/code-quality.yml#rust-quality |
| RUST-TC-1 | uncovered: floats on stable but declares no rust-version |
| RUST-TC-2 | practiced |
| RUST-TC-3 | gated: .github/workflows/code-quality.yml#rust-quality |
| RUST-TYPE-1 | uncovered: missing_debug_implementations is not enabled (70 types) |
| RUST-TYPE-2 | convention: newtype and enum-over-bool choices are judged in review |
| RUST-UNSAFE-1 | uncovered: no crate root declares #![forbid(unsafe_code)] |
| RUST-UNSAFE-2 | uncovered: unsafe in temper-ingest and temper-cli is not a registered exception |
| RUST-UNSAFE-3 | n/a: no FFI bindings; the SDKs are generated HTTP clients |
| SC-ADV-1 | gated: .github/workflows/quality-gate.yml#rust-gate |
| SC-ADV-2 | convention: each ignore is reviewed by hand; five FIX-PENDING entries state no reachability |
| SC-DENY-1 | gated: .github/workflows/quality-gate.yml#rust-gate |
| SC-DENY-2 | gated: .github/workflows/quality-gate.yml#rust-gate |
| SC-DENY-3 | gated: .github/workflows/quality-gate.yml#rust-gate |
| SC-GHA-1 | partial: SHA pins are required only in privileged jobs (quality-gate.yml#guard-tests); most other uses: are tag refs |
| SC-GHA-2 | uncovered: build-cli-binaries.yml has no top-level permissions; release.yml and release-tag.yml grant write at top level |
| SC-GHA-3 | gated: .github/workflows/quality-gate.yml#guard-tests |
| SC-IN-1 | uncovered: mise pins and cools, but CI installs several tools unversioned (taiki-e tool lists, setup-bun) |
| SC-IN-2 | uncovered: Dependabot misses temper-design (npm, uv), temper-py, temper-rb and the bench Dockerfile |
| SC-IN-3 | partial: Cargo.lock, bun.lock and the client npm locks are enforced; the agent workflows run npm install and temper-py commits no lock |
| SC-SEC-1 | gated: .github/workflows/secret-scan.yml#secret-scan, .github/workflows/codeql.yml#analyze |
| SEC-AUTH-1 | n/a: temper has no disabled-auth mode |
| SEC-AUTH-2 | partial: route auth tiers are pinned (audit-route-auth, audit-mcp-route-auth, quality-gate.yml#rust-gate); authorising before a write inside a handler is review |
| SEC-AUTH-3 | convention: refusal versus not-found parity is reviewed per handler |
| SEC-CRED-1 | uncovered: several credential fields outside temper-client are bare String |
| SEC-CRED-2 | gated: .github/workflows/quality-gate.yml#rust-gate |
| SEC-CRED-3 | practiced |
| SEC-CRED-4 | gated: .github/workflows/quality-gate.yml#rust-gate |
| SEC-RED-1 | practiced |
| SEC-RED-2 | convention: redaction by origin is a design judgement made in review |
| SEC-RPT-1 | practiced |
| SEC-SQL-1 | partial: values are bound by the query! macros and the runtime-query tripwire (quality-gate.yml#rust-gate); identifier validation is unchecked |
| SEC-SQL-2 | partial: the visibility-ungated fragments are pinned (audit-ungated-fragments, quality-gate.yml#rust-gate); other scoping is review |
| SEC-TEST-1 | gated: .github/workflows/code-quality.yml#rust-quality |
| SH-1 | uncovered: 4 zsh and 7 sh executables |
| SH-2 | uncovered: about 29 scripts lack strict mode |
| SH-3 | uncovered: ShellCheck runs only in the pre-commit hook |
| SH-4 | uncovered: backticks remain; SC2006 is not run |
| SH-5 | uncovered: the drift gates eval command strings |
| SH-6 | uncovered: non-portable constructs present, unchecked |
| SH-7 | convention: the shell-or-program split is judged in review |
| TEST-1 | gated: .github/workflows/quality-gate.yml#rust-gate |
| TEST-2 | convention: weakening a test is caught in review; the ignore set is pinned by TEST-1's tripwire |
| TEST-3 | partial: every tier but temper-client's integration-tests feature runs in test-rust.yml; nothing checks the mapping |
| TEST-4 | gated: .github/workflows/test-rust.yml#unit-tests, .github/workflows/test-rust.yml#integration-tests |
| TEST-5 | partial: coverage floors are enforced nightly (coverage.yml#coverage), not on pull requests |
| TS-CFG-1 | uncovered: packages set strict only, with no shared base (about 155 errors measured under the canonical one) |
| TS-CFG-2 | uncovered: erasableSyntaxOnly is unset; one namespace in hand-written TS |
| TS-DOC-1 | convention: Biome has no rule for exported doc comments |
| TS-ERR-1 | practiced |
| TS-GEN-1 | gated: .github/workflows/test-agents-ts.yml#temper-ts, .github/workflows/code-quality.yml#rust-quality |
| TS-MOD-1 | uncovered: noDefaultExport is not enabled; 29 default exports |
| TS-NAME-1 | convention: casing is reviewed |
| TS-SUP-1 | practiced |
| TS-TOOL-1 | partial: temper-cloud, temper-ui and temper-design are linted and typechecked; temper-ts, temper-telemetry-ts and the agent workflows are typechecked only |
| TS-TOOL-2 | uncovered: no shared Biome base, and warn-level rules never fail CI |
| TS-TOOL-3 | uncovered: four TypeScript version ranges, one a release candidate; Biome is a range |
| TS-TYPE-1 | uncovered: noExplicitAny is warn-only |
| TS-TYPE-2 | uncovered: noNonNullAssertion is warn-only |
| TW-1 | uncovered: about 7 of 19 tripwires state no NOT CHECKED section |
| TW-2 | uncovered: 5 of 19 tripwires lack --list or UPDATE_BASELINE |
| TW-3 | practiced |
| TW-4 | uncovered: audit-handler-authz-drift.sh cannot be pointed at a fixture |
| TW-5 | partial: 18 of 19 tripwires' bite tests run in quality-gate.yml#guard-tests; audit-handler-authz-drift has none, and nothing requires one |
| TW-6 | partial: the glob-and-coverage check is local (cargo make tripwires); CI runs a hand-kept list |
| TW-7 | convention: what a tripwire keys on is judged when it is written |

<!-- consumer-status:end -->
