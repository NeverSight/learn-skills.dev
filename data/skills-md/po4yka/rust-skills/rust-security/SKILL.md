---
name: rust-security
description: Use when running cargo-audit or cargo-deny, editing deny.toml, triaging a RUSTSEC advisory or CVE in a dependency, vetting a new or updated crate for typosquat, malicious crate, or compromised-release risk, or hardening a Rust parser that reads untrusted files, archives, or binary formats. Not for authentication, secret storage, cryptographic design, or TLS policy (TLS belongs to rust-networking). Triggers on "RUSTSEC", "supply chain", "yanked", "path traversal", "decompression bomb".
license: BSD-3-Clause
---

# Rust Dependency and Parser Security

| Request | Route |
|---|---|
| Advisories, `deny.toml`, dependency vetting, registry and source policy | This skill. |
| Untrusted file, archive, backup, or binary-format parsing | This skill. |
| Publishing, Trusted Publishing, binary provenance, SBOMs | The `rust-crate-release` skill. |
| Unsafe-code soundness, Miri, sanitizers | The `rust-unsafe` or `rust-sanitizers-miri` skill; at minimum run `cargo +nightly miri test --locked`. |
| TLS transport policy | The `rust-networking` skill; never disable certificate checks with `danger_accept_invalid_certs`. |
| Authentication, secret storage, cryptographic protocol design, key lifecycle | Not this skill; follow the domain security review. |

Other skills named in this file apply when they are installed.

## Review gate

Block a change that does any of these:

- Adds a `Cargo.lock` package without the identity check and source triage of section 5.
- Adds an `=` requirement as a vetting device.
- Adds an `[advisories].ignore` entry for a `malicious` advisory, or one without an `id`,
  a `reason`, and a tracking issue.
- Adds a `[bans].skip` entry without an exact version and a causal `reason`.
- Widens the license allowlist to clear one dependency, with no recorded license review.
- Allocates from an untrusted length field without a cap.
- Extracts an archive entry without its own traversal check.
- Panics on malformed input across an FFI boundary.

Do not compile an unvetted package: build scripts and proc macros run at compile time. Until
section 5 step 3 passes for every new `Cargo.lock` package, run no `cargo build`, `check`,
`test`, `clippy`, `doc`, or `run`, and keep rust-analyzer off the workspace.

## Read the cargo-deny pin first

Before you write a `cargo deny` command or a `deny.toml` key, read the `cargo-deny`
version that CI pins. The commands in this skill need 0.20 or later, where `--config` is a
root option; across the 0.19/0.20 boundary the wrong position fails with
`unexpected argument '--config' found`. Read the version table in
[references/deny-policy.md](references/deny-policy.md#version-boundaries) when the pin is
older than 0.20, or when you add a key or a flag.

Use `--locked` in every command that resolves dependencies, or a check can pass against a
lockfile that CI never builds. Run cargo-deny from the workspace root: a relative `--config` path resolves against the
current directory. When no file is there, cargo-deny warns `falling back to default config`,
runs the default policy, and can exit 0. Treat that warning as a failure.

## 1. cargo-audit

`cargo-audit` compares `Cargo.lock` with the RustSec database, which it fetches on every run
unless you pass `--no-fetch`. `cargo audit` exits 1 on a vulnerability only; an informational
advisory (`unmaintained`, `unsound`, `notice`) and a yanked version are warnings, so pass
`cargo audit --deny warnings` to fail on them. It does not check licenses or sources.

Read [references/incidents.md](references/incidents.md) when you parse a `cargo audit` report,
need the `--json` filter for the category and `unaffected` ranges, or audit a shipped binary
with `cargo audit bin` (complete only for a `cargo auditable build`).

## 2. cargo-deny

`cargo-deny` is the blocking gate.

```bash
cargo deny --config deny.toml --locked check               # all four checks, cargo-deny >= 0.20
cargo deny --config deny.toml --locked check advisories    # or licenses, bans, sources
cargo deny --config deny.toml --locked --offline check advisories    # no database fetch
```

A green check does not catch a malicious crate that has no advisory yet; the gate in section 5
covers that.

Read [references/deny-policy.md](references/deny-policy.md) when you write or change
`deny.toml` or the CI job. It holds the annotated policy, the license allowlist, the
`ignore` and `skip` entry formats, and the CI job steps.

In CI, run the full check as its own job, on pull requests, on pushes to the default branch,
and on a schedule: new advisories land against unchanged lockfiles.

| Failing check or message | First action |
|---|---|
| `advisories` | Read the RUSTSEC ID and follow section 4. |
| `licenses` | Find the crate with `cargo tree --locked -i <crate>`. Do not widen the allowlist without a license review. |
| `bans` | Run `cargo tree --locked -d`. Unify the versions. Add a `skip` entry only with a causal `reason`. |
| `sources` | A registry or git remote that policy does not allow: check for a `[patch]` missing from `allow-git`, a leaked `path` override, or a new transitive git dependency. |
| `unexpected argument '--config' found` | The command and the pinned cargo-deny version disagree. See "Read the cargo-deny pin first". |

Reproduce a CI failure locally with the same command and pinned version. Do not extend an
`ignore` or `skip` list only to make the job green.

## 3. Advisory kinds

| Kind | How the advisory marks it | Response |
|---|---|---|
| Vulnerability | No `informational` field | Upgrade. If no fix exists, see section 4. |
| `unsound` | `informational = "unsound"` | Find out whether your code reaches the unsound API. |
| `unmaintained` | `informational = "unmaintained"` | Plan a replacement; a time-boxed ignore is fine. |
| `notice` | `informational = "notice"` | Read and decide. |
| Malicious crate | `categories = ["malicious"]`, `patched = []` | Act now. Follow "Malicious advisory" below. |

`yanked` is a registry state, not an advisory kind. Move off a yanked version, and set
`yanked = "deny"`.

## 4. Respond to an advisory

```bash
cargo tree --locked -i <crate>@<version>   # which dependency pulls it in
cargo update -p <crate> --dry-run          # is a semver-compatible fix available?
cargo update -p <crate>
cargo deny --config deny.toml --locked check advisories
```

Prefer an upgrade, of the parent crate when its range excludes the fix. Then prefer a
`[patch.crates-io]` entry at a fixed `rev`, with the fork URL in `[sources].allow-git` (and a
reason and tracking link) in the same change. Add an ignore entry only when no fix exists. Never ignore a `malicious` advisory: its code already ran, and the
ignore hides the crate from every later check.

Every `[advisories].ignore` entry must carry the RUSTSEC `id`, a `reason` that says why the
advisory is safe in this workspace ("not exploitable" alone is not one), and a tracking issue
link and re-evaluation date in a trailing comment.

Set `unused-ignored-advisory = "deny"`, remove the entry in the change that upgrades the
dependency, and review the whole ignore list on every dependency bump. Time-box every entry:
by default 90 days for low or informational, 30 for medium, and no ignore for high or critical
(fix within 7 days). The deny-policy reference has the time-box table and the valid cases.

### Malicious advisory

Assume that the code ran on every machine that built or tested the workspace with the crate, or
opened it in an IDE that runs rust-analyzer. Act now, in this order: take the code out of the
graph in one change, delete every local and CI copy, then report the exposed machines so the owner
rotates their credentials. Read
[references/malicious-advisory.md](references/malicious-advisory.md) before the first step: it
has the commands, and the `cargo audit` report hides the category.

## 5. Vet a new or changed dependency

Until step 3 passes, the no-compile rule under the review gate holds. Close the IDE, or set
`rust-analyzer.cargo.buildScripts.enable` and `rust-analyzer.procMacro.enable` to `false`.
`cargo metadata`, `cargo fetch`, `cargo tree`, and `cargo deny` do not run crate code. The one
exception is the scheduled latest-dependencies job of the `cargo-workflows` skill, on a
disposable runner with no secrets; vet its lock diff with this gate before you adopt it.

Apply this gate to every package name that is new in the `Cargo.lock` diff, transitive
packages included. A `cargo update` is a vetting event too. A payload can hide in runtime code,
in a new transitive dependency, or in a build script; read
[references/incidents.md](references/incidents.md) when a finding resembles a known attack.

Read [references/vetting.md](references/vetting.md) when you run the gate. It has the
commands for each step:

1. **Create the candidate lockfile** without a build (`cargo metadata --format-version 1`).
2. **Check the identity**: a name close to a popular crate and under 7 days old (a default
   threshold) is a red flag.
3. **Read the published source**, not the repository: every build script in full, and every
   file of a proc macro or a fresh release.
4. **Write a caret requirement at the reviewed version**, not `=1.2.3`.
5. **Run the policy**: `cargo deny --config deny.toml --locked check`.
6. **Justify the dependency** against std and the crates already in the graph.

For a version bump, read the diff of a release under 7 days old or one that adds a build
script or a proc-macro dependency.

## 6. Supply chain hardening

`cargo machete` finds unused dependencies heuristically: a renamed or macro-only dependency
is a false positive, so confirm each finding.

Run `cargo vet` only when a `supply-chain/` directory already exists: `cargo vet init`
exempts every current dependency, so a run right after it proves nothing.

- Commit `Cargo.lock` (the `cargo-workflows` skill owns the lockfile policy).
- Allow only crates.io, unless a git dependency has a written reason and a `rev` pin (a
  branch pin is unpinned code execution). Enforce it with `unknown-registry = "deny"` and
  `required-git-spec = "rev"`.
- Use Cargo 1.96.1 or later in every job that fetches from a third-party registry or over
  SSH git: older Cargo leaks registry tokens (CVE-2026-5222) and follows symlinks in crate
  tarballs (CVE-2026-5223). An MSRV job on an old toolchain is the usual exposure.

## 7. Untrusted-input parser hardening

Treat a file, byte buffer, or network frame from outside the process as adversarial.

- **Cap a length field** against a documented maximum and the remaining input before
  `Vec::with_capacity` or `vec![0u8; n]`.
- **Use checked arithmetic** (`checked_add`, `checked_mul`, `try_into`) for offsets and
  lengths: a release build wraps silently.
- **Limit recursion depth** with a counter, and **reject non-finite floats**.
- **Reject path traversal.** Accept only `Component::Normal` UTF-8 components, and create
  entries relative to an open staging-root handle with no-follow semantics. A library
  `extract` or `unpack_in` helper is not a traversal gate.
- **Disable XML entity expansion**, and **reject unknown schema versions**.
- **Authenticate before you mutate**: verify the digest or MAC of a container first.
- **Return typed errors across an FFI boundary**; never panic on malformed input.
- **Keep std `RandomState` for hash-map keys an outside caller controls.** `FxHasher`,
  `FnvHasher`, and `nohash` have no random secret.

Read [references/untrusted-input.md](references/untrusted-input.md) when you write or
review a parser, an archive extractor, a streamed backup format, an FFI parser, or a map
hasher. It has the format threat table, the checklists, the `catch_unwind` guard, and the
fuzz targets that must exist.
