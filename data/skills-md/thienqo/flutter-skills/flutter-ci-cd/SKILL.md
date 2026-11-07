---
name: flutter-ci-cd
description: Create, repair, or harden provider-neutral Flutter CI/CD pipelines, quality gates, caches, artifacts, secrets, and staged delivery. Use for GitHub Actions, GitLab CI, Codemagic, Bitrise, Xcode Cloud, or similar orchestration; route local artifact configuration to flutter-build-release and never publish without explicit authorization.
---

# Flutter CI/CD

Build a reproducible pipeline around the repository's existing delivery model. Preserve the current provider, Flutter version source, package manager, flavors, signing flow, and deployment tooling unless migration is explicitly requested.

## Preflight

Read `pubspec.yaml`, lockfiles, SDK/version-manager files, workspace layout, generated-code policy, flavors, tests, native targets, existing pipeline files, repository scripts, release tooling, protected environments, and secret names before writing pipeline changes. Inspect the actual job dependency graph and recent timing/failure output when diagnosing reliability or speed. When repository evidence is unavailable, request or list the exact files and logs required and keep advice at the invariant level; do not present a placeholder workflow as a completed repair. Never print, move, synthesize, or commit signing material or service credentials.

Separate pull-request confidence from release authority. A passing CI job may prove checks and artifact creation; it does not authorize tagging, store upload, production deployment, or credential changes.

## Route the work

- For deterministic format, analysis, generation, test, coverage, golden, matrix, and cache gates, read [quality gates](references/quality-gates.md).
- For signing, secrets, artifacts, symbols, protected environments, staged rollout, and publication boundaries, read [delivery and secrets](references/delivery-and-secrets.md).
- For GitHub Actions, GitLab CI, Codemagic, Bitrise, Xcode Cloud, monorepos, and provider-preserving decisions, read [provider and monorepo](references/provider-and-monorepo.md).

Load only the references needed by the current pipeline.

## Boundaries

- `flutter-build-release` owns flavors, signing configuration, versioning, symbol production, and local store-ready artifacts; inspect and orchestrate those established commands instead of reimplementing them inside provider YAML.
- `flutter-testing` owns test strategy and test implementation; this skill runs the repository's chosen suites as gates.
- `flutter-security` owns a broader security audit; this skill still applies least privilege, secret isolation, trusted dependency pinning, and untrusted-fork boundaries.
- Do not change application architecture, state management, or packages to make pipeline authoring more convenient.

## Verification

Validate provider syntax with the provider's current linter/dry-run facility and run every underlying repository command locally where the environment permits. Check cold and cached paths, pull-request and protected-branch conditions, expected artifacts, cancellation/concurrency behavior, and failure propagation. A cache hit and miss must produce the same correctness result. Formatting and golden gates must not rewrite source or expectations. A freshness gate may run the established generator in the disposable checkout, but it must fail on a resulting diff and must never commit or conceal that diff. For delivery, prefer a dry run or non-production target before any authorized external mutation.

Report commands and pipeline paths changed, environments exercised, artifact evidence, and any macOS runner, signing, secret, quota, or store-side gap. Never weaken a gate merely to turn the pipeline green.

## Sources

- [Continuous delivery with Flutter](https://docs.flutter.dev/deployment/cd)
- [Testing Flutter apps](https://docs.flutter.dev/testing/overview)
- [GitHub Actions security guidance](https://docs.github.com/en/code-security/tutorials/secure-your-organization/protect-against-threats)
