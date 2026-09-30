---
name: esp-idf-v6-migration
description: Migrate ESP-IDF applications from 5.x to 6.0 with baseline comparison, version-matched cumulative guides, isolated builds, configuration and dependency review, failure triage, and subsystem validation. Use when planning, implementing, debugging, or reviewing an ESP-IDF 6.0 migration.
---

# ESP-IDF v6 Migration

This workflow targets application repositories. Treat migration as cumulative:
review every intermediate guide between the source release and 6.0.

## When to Use

- Migrating an application from ESP-IDF 4.4 or 5.x to 6.0.
- Triaging failures after switching to ESP-IDF 6.0.
- Auditing removed APIs, moved components, toolchain changes, configuration, or
  runtime regressions.
- For versions older than 4.4, first define a staged migration plan and agree on
  scope and validation with the user; do not attempt one unreviewed jump.

## Source Priority

- Use the official online ESP-IDF migration guides as the primary source of truth.
- Resolve the exact target patch release first and use documentation under
  `/en/<TARGET_IDF_VERSION>/`; do not use `/latest/` for migration decisions.
- Use a matching local checkout only as supporting context.
- Use [references/migration-paths.md](references/migration-paths.md) for the
  cumulative guide chain and
  [references/version-summary.md](references/version-summary.md) for routing.

## Workflow

### 1. Establish the original baseline

- Inspect repository status and preserve unrelated user changes.
- Resolve the exact source version from `idf.py --version`, CI, project
  documentation, `IDF_PATH`, and EIM. If it remains unclear, stop and ask.
- In the original environment, build every affected supported target that is
  practical and run relevant host, unit, and integration tests.
- Record target, warnings, binary and partition sizes, dependency versions,
  configuration defaults, and expected runtime behavior.
- Flash baseline firmware only when explicitly authorized and after confirming
  the port, target, and device.

### 2. Pick the cumulative migration path

- Use [references/migration-paths.md](references/migration-paths.md) to select the exact guide chain.
- A 5.5 project starts with the 5.5-to-6.0 guide.
- A 5.4 or older project reviews every intermediate guide through 5.5 before the
  6.0 guide.
- Use [references/version-summary.md](references/version-summary.md) to decide which subsystem chapters to inspect first.

### 3. Switch the environment to the target IDF

- Prefer EIM when the repository does not prescribe another setup:
  - Discover versions and absolute paths: `eim list`
  - Verify the target: `eim run "idf.py --version" <TARGET_IDF_VERSION>`
  - Build with the target:
    `eim run "idf.py -B build-v6 build" <TARGET_IDF_VERSION>`
  - Install a missing version only with authorization:
    `eim install -i <TARGET_IDF_VERSION>`
- If EIM is unavailable but a valid matching environment is active, continue
  without blocking on EIM installation.
- Use a separate target build directory such as `build-v6`; do not reuse v5
  build artifacts or run `fullclean` by default.
- Ask before `idf.py set-target` because it clears build state and replaces
  `sdkconfig`.
- Confirm Python, CMake, and toolchain requirements before the first build.
- Run the first target build before broad source edits. If ESP-IDF reports the
  old CMake baseline, update the first line to
  `cmake_minimum_required(VERSION 3.22)`.

### 4. Run an initial build and categorize failures

- Review warnings as well as hard failures.
- Group failures before editing:
  - build system or linker
  - GCC or header/toolchain
  - removed or moved components
  - components not supported
  - driver dependency splits
  - subsystem API changes
  - config and Kconfig syntax issues
- Use [references/common-breakpoints.md](references/common-breakpoints.md) to map symptoms to likely migration areas.
- Use [references/build-errors.md](references/build-errors.md) when the build log already points to a concrete missing header, removed API, linker failure, or tool behavior change.

### 5. Fix migration issues by subsystem

- Build system:
  - check CMake version warnings and align the top-level `cmake_minimum_required(...)` with `3.22` when the project still pins an older baseline
  - check orphan section errors
  - check constructor-order assumptions
  - check Kconfig v3 syntax compatibility
  - check warnings-as-errors defaults
- Toolchain:
  - check GCC 15 warnings and promoted errors
  - replace outdated headers such as `sys/dirent.h` where needed
  - account for Picolibc header differences if enabled
- Components and dependencies:
  - replace removed in-tree drivers with Component Registry dependencies where required
  - update `REQUIRES` and `PRIV_REQUIRES` explicitly when legacy transitive dependencies disappear
  - review `driver` usage and split dependencies to `esp_driver_*` components when needed
- Configuration and generated dependencies:
  - keep intentional values in `sdkconfig.defaults*`; treat `sdkconfig` as generated
  - ask whether to run `idf.py reconfigure` after Kconfig changes
  - inspect removed or renamed symbols and review generated configuration diffs
  - never edit `dependencies.lock` or `managed_components/` manually; update manifests or constraints and let Component Manager regenerate them
  - review partition size, bootloader size, and OTA/rollback implications
- Subsystems:
  - review the relevant migration chapters for networking, peripherals, protocols, Wi-Fi, storage, system, security, provisioning, and Bluetooth
  - do not apply mechanical edits outside the subsystem actually implicated by build or runtime evidence
  - do not patch external or managed components without explicit user approval;
    prefer updating the dependency or reporting an upstream incompatibility

### 6. Rebuild and validate behavior

- Rebuild after each coherent migration batch, not after every small edit.
- Repeat the relevant original-version test matrix under the exact target version.
- Build every affected supported target that is practical and compare warnings,
  sizes, tests, and behavior with the baseline.
- Flash only when explicitly authorized; confirm the port, target, and device,
  then capture monitor logs.
- Review all generated configuration, manifest, lockfile, and partition changes
  before handoff.
- Report source and target versions, targets, tests, runtime evidence, notable
  size/configuration changes, and anything not validated.

## References

- Migration path matrix: [references/migration-paths.md](references/migration-paths.md)
- Common migration breakpoints: [references/common-breakpoints.md](references/common-breakpoints.md)
- Build error symptom map: [references/build-errors.md](references/build-errors.md)
- Version coverage summary: [references/version-summary.md](references/version-summary.md)

## Avoid

- Jumping straight from 5.4 or earlier to 6.0 without reviewing intermediate migration guides
- Treating a local ESP-IDF 6.0 checkout as more authoritative than the current official migration docs
- Suppressing warnings or linker errors before understanding the underlying breakage
- Assuming legacy `driver` dependencies or moved components still arrive transitively
- Making broad unrelated cleanups while the migration error set is still being established
