---
name: fable-release
description: "Audit and certify repository merge and release readiness against required quality gates, clean git working trees, and verified distribution artifacts. Use when preparing a release tag, validating release checklist criteria, publishing npm/PyPI packages, or certifying a branch for merge — even if the user does not explicitly say \"fable-release\" (e.g. \"prepare the release\", \"is this ready to merge\", \"ship to production\", \"publish the package\"). Do NOT use when verification is stale, failing, or missing (use fable-verify first)."
version: 1.3.0
pack: delivery
inputs:
  - completion_evidence
requires:
  - clean_worktree
produces:
  - release_readiness
gates:
  - required_checks_pass
  - no_blocking_findings
fallback: fable-verify
mutatesWorkspace: false
parallelSafe: false
neural_links:
  precursors:
    - fable-verify
    - fable-review
    - fable-security
  continuations:
    - fable-handoff
  lateral_peers:
    - fable-handoff
  recovery: fable-recover
---

# Fable Release

Prove that the exact commit and artifact users will receive are ready to ship, then distinguish readiness from actual distribution.

## Mission
A release is an external state transition. Source tests can be perfect while the package omits files, the tag points at another commit, the registry still serves an old version, or a published artifact cannot start in a clean environment.

This Skill closes that gap by tying release claims to exact version, commit, artifact, workflow, tag, and registry evidence.

## Activate When
- preparing a branch for merge or a version for release;
- creating/pushing a version tag;
- publishing npm/package/plugin artifacts;
- finalizing a GitHub Release;
- verifying that a distribution channel actually serves the intended version;
- assessing whether release evidence is current after last-minute changes.

## Do Not Activate When
- implementation is still changing (`fable-execute`/`fable-tdd`);
- functional verification is incomplete (`fable-verify`);
- blocking review/security findings remain;
- the user has not authorized an irreversible publish action. Readiness checks may run; publishing itself requires the applicable authorization.

## Release Classification

| Release type | Extra concerns |
| --- | --- |
| Merge only | branch/base freshness, required CI, review |
| Package registry | package contents, clean install, registry verification |
| Git tag/GitHub Release | tag→SHA binding, notes/assets, draft/prerelease state |
| Plugin/marketplace | manifest/version parity, submission/approval state |
| Migration-bearing release | rollout order, backward compatibility, rollback |
| Security-sensitive release | advisory/secrets/dependency gates, disclosure constraints |

## Protocol

### Stage 1 — Freeze the candidate
Identify the exact candidate:
- version;
- commit SHA;
- target branch/tag;
- distribution channels;
- required CI/review/security evidence.

Any source/config/package mutation after this point invalidates relevant release evidence and creates a new candidate.

### Stage 2 — Validate version semantics
Check:
- version does not already exist in target registry/tag namespace;
- SemVer matches actual compatibility impact;
- all canonical version locations/manifests agree;
- changelog/release notes describe user-visible changes accurately;
- prerelease state is intentional.

Do not choose patch/minor/major purely for convenience.

### Stage 3 — Reconfirm fresh quality gates
Verify required functional/build/review/security evidence belongs to the candidate SHA/mutation generation. If evidence was produced before candidate changes, rerun it.
- When available, route branch pushes through the `no-mistakes` proxy (`git push no-mistakes` or `no-mistakes axi run`) to ensure rebase, automated review, tests, lint, and docs pass before remote merge.

### Stage 4 — Inspect the artifact boundary
Build/dry-run the exact artifact and inspect its manifest/content.

Check:
- required entrypoints/assets/manifests are present and non-empty;
- secrets, temp files, tests/fixtures/internal holdouts are excluded unless intentionally public;
- generated files are current;
- executable permissions/exports/bin paths are correct;
- dependency/runtime constraints are accurate.

### Stage 5 — Clean-environment smoke
Install/use the produced artifact outside the source checkout where feasible.

Prove at least:
- install succeeds;
- primary executable/import resolves;
- version/help/basic smoke works;
- documented quick-start path is not accidentally relying on repo-local files.

### Stage 6 — Verify repository release state
Before publishing:
- candidate commit is pushed;
- required CI on the candidate is green;
- tag does not exist or already points to exactly the intended SHA;
- release notes/assets target the same tag/SHA;
- branch is not known-broken relative to base.

### Stage 7 — Publish only through an authorized secure path
Prefer configured trusted publishing/OIDC/host automation over introducing long-lived tokens.

Do not print/store credentials or weaken security to make a release pass.

If authorization or authentication is absent, stop at **READY_NOT_PUBLISHED** with exact remaining action.

### Stage 8 — Verify distribution independently
After publish, query the external destination rather than trusting the publish command.

Examples of proof:
- registry reports expected version/dist metadata;
- clean install from registry succeeds;
- Git tag resolves to candidate SHA;
- GitHub Release is actually public, not draft;
- marketplace status reflects submitted/published state.

### Stage 9 — Post-release smoke and handoff
Run the user-facing install/invocation path from public distribution. Record rollback/deprecation/follow-up issues if observed.

## Release Verdicts
- **NOT_READY**: required deterministic/review/security/artifact gate fails.
- **READY_NOT_PUBLISHED**: candidate is sound but publish is unauthorized/unavailable/not requested.
- **PUBLISHED_UNVERIFIED**: publish command/workflow claims success but external distribution has not been independently confirmed.
- **RELEASED**: exact candidate is public through intended channels and independently verified.

Do not collapse these states into "done."

## Decision Rules
- A dirty worktree does not automatically fail if dirt is explicitly unrelated and release artifact is from a clean candidate SHA; however uncommitted release changes do fail readiness.
- Tag exists at different SHA → hard stop; never move/force a release tag casually.
- Package version already exists in immutable registry → choose a new valid version, do not overwrite.
- Dry-run contents differ from intended public surface → fix package configuration before tagging/publishing.
- Local global install works from repo link but clean tarball/registry install fails → NOT_READY.
- CI green on older commit → stale release evidence.
- GitHub Release draft exists → not public release evidence.
- Publish workflow green but registry not updated yet → PUBLISHED_UNVERIFIED until independently confirmed or known propagation policy is resolved.
- Marketplace requiring manual approval → report submission state accurately; never claim publication.

## Invariants
- Release version, commit, tag, artifact, and public metadata refer to one candidate.
- No credential is committed or logged as release evidence.
- Irreversible external writes require applicable authorization.
- Public release claims are externally verified.
- Last-minute mutation invalidates stale candidate evidence.
- Release notes do not claim maturity/features unsupported by fresh proof.

## Failure Taxonomy
### Artifact omission/pollution
Package misses runtime file or includes secrets/internal material. Fix boundary, rebuild, resmoke.

### Version drift
Manifests/changelog/CLI/tag disagree. Reconcile before release.

### Candidate drift
CI/evidence points to older SHA after release commit changed. Rerun gates.

### Tag mismatch
Existing tag points elsewhere. Stop; investigate rather than force-move.

### Publish/auth failure
Candidate may remain READY_NOT_PUBLISHED. Diagnose secure auth/workflow without embedding credentials.

### Registry/release mismatch
Publish reports success but public channel serves wrong/old artifact. Keep PUBLISHED_UNVERIFIED and investigate.

### Clean-install failure
Artifact depends on repo-local files/dev state. NOT_READY regardless of source tests.

## Anti-Patterns
- "tests pass, publish";
- tagging before inspecting artifact contents;
- using source checkout as the only install test;
- force-moving tags;
- adding tokens to config/docs to bypass trusted publishing;
- equating draft release with public release;
- trusting workflow success without registry/release lookup;
- updating docs to claim availability before public verification;
- claiming 100% maturity while changed behavioral evidence is stale.

## Release Attestation

```text
Version:
Candidate SHA:
Target channels:
Fresh quality gates:
Artifact manifest check:
Clean-install smoke:
Tag → SHA:
GitHub Release state:
Registry/marketplace state:
External verification:
Verdict: NOT_READY | READY_NOT_PUBLISHED | PUBLISHED_UNVERIFIED | RELEASED
Rollback/follow-up:
```

## Completion Criteria
The Skill's work completes when the requested release stage is accurately attested:
- readiness claims are tied to exact candidate evidence;
- artifact boundary and clean install are proven where applicable;
- tag/release/registry states are consistent;
- public distribution is independently verified before `RELEASED`;
- missing authorization/external gates are represented as explicit state, never guessed away.

## Progressive Resources
- Deep guide: `references/artifact-and-distribution-verification.md`
- Existing release gates: `references/release-gates.md`
- Example: `examples/release-readiness-audit.md`
