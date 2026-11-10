---
name: ci-pub
description: "Audit code health, propose semantic version bumps, and verify package publication readiness."
disable-model-invocation: true
---

# ci-pub — Automated Release Preflight & Publication Engine

## Operating Invariants

- **Pre-Mutation Gate**: Present version candidates and halt turn immediately; forbid modifying manifests, changelogs, or git history without affirmative human authorization.
- **Autonomous Upload Boundary**: Confine execution strictly to local preflight audit, manifest updates, and dry-run verification; forbid uploading packages, pushing tags, or publishing autonomously.
- **Atomic History Integrity**: Stage manifest, changelog, and workflow updates strictly within a single release commit (or amend HEAD); forbid detached chore commits or unanchored release tags.

## Execution Protocol

### Phase 1: Environment & Publishing Setup Discovery

1. **Publishing Strategy & CI Audit**:
   - Inspect `.github/workflows/` for existing release/publish workflows (e.g. `publish.yml`, `release.yml`). Identify configured trigger mechanisms: tag-driven OIDC (`refs/tags/*`), manual dispatch (`workflow_dispatch`), or absent (terminal/cmd driven).
   - **CI Seeding Gate (If No CI Configured)**: If `.github/workflows/` lacks a publish workflow, highlight that no automated CI was detected and offer to seed one from `references/workflow-single.yml` or `references/workflow-workspace.yml` (to be committed atomically with the release).
   - Read repository publishing documentation and runbooks (`doc/runbooks/*publish*.md`, `docs/*release*.md`, `CONTRIBUTING.md`) to extract project-specific release invariants and packaging constraints.
2. **Topology & Member Mapping**:
   - *Single Package*: Root `pubspec.yaml` without `workspace:` directive.
   - *Pub Workspace*: Root `pubspec.yaml` contains `workspace:` (requires Dart SDK `^3.6.0`, root `publish_to: none`). Run `dart pub workspace list` (or `fvm dart pub workspace list`) to identify candidate member packages and map topological dependency order.
3. **Remote & Local Version Baseline**:
   - Query pub.dev API (`curl -s https://pub.dev/api/packages/<pkg>`) to resolve **Remote Live Version** (or mark `UNPUBLISHED` if 404).
   - Read **Local Manifest Version** (`grep '^version:' <pubspec.yaml>`).
   - Compare Remote vs Local to baseline the proposal: unbumped (`Local == Remote`), pre-bumped in working tree (`Local > Remote`), or initial release (`UNPUBLISHED`).

### Phase 2: Preflight Quality Gate

Run formatting (`dart format --output=none --set-exit-if-changed .`), analyzer checks (`dart analyze --fatal-infos`), changelog readiness, and test suites across the target release scope. If any verification fails, report diagnostics and halt immediately.

### Phase 3: Version Proposal & Turn-Halt Gate

1. Assess changeset scope across the target package(s) (breaking, feat, fix).
2. Present release proposal:
   - *Single Package*: Propose recommended SemVer candidate grounded against remote baseline (and optional pre-release preview if applicable).
   - *Pub Workspace*: Present Release Matrix listing affected packages in topological order, Remote Live vs Local version, proposed version, and downstream constraint cascades.
   - *CI Workflow Addition*: If user elected in Phase 1 to seed a publish workflow, include `.github/workflows/publish.yml` in the proposed changeset.
3. Halt turn immediately for version selection and human authorization.

### Phase 4: Manifest Mutation, Dry-Run Verification & Handoff

1. **Manifest & Changelog Synchronization**: Upon user approval, synchronize versions across target `pubspec.yaml` manifests, per-package `CHANGELOG.md` files, and seed `.github/workflows/publish.yml` (if requested).
2. **Atomic Release Commit**: Stage updated files and amend HEAD (`git commit --amend --no-edit`) or create an atomic release commit (`git commit -m "chore(release): publish packages [...]"`).
3. **Last Verification (Dry-Run)**: Execute package manager publication dry-run sequentially in topological order:
   - *Single Package*: `dart pub publish --dry-run`
   - *Pub Workspace*: `dart pub -C <package_dir> publish --dry-run` for each approved package.
   - If errors, warnings, or archive leaks occur, supply exact failure diagnostics and halt immediately.
4. **Publication Readiness Report & Tailored Handoff**:
   - Present dry-run confirmation and topological release sequence.
   - Tailor handoff instructions to the publishing setup aligned in Phase 1:
     - *CI-Driven (Tag Push)*: Deliver exact Git tag commands matching the repo's tag pattern (e.g. `v<version>` for single, `<package>-v<version>` for workspace) pointing to the release commit SHA, and tag push commands.
     - *Terminal/CMD*: Deliver direct publish commands (`dart pub publish` / `dart pub -C <package_dir> publish` in topological order, noting the 120s pub.dev CDN propagation window; see `references/pub-workspace-workflow.md`).
