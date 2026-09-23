---
name: dsh-plugin-upgrade
description: "Help migrate a DeepSeek Harness (DSH) plugin from DSH 0.1.1 to 0.1.5 with the dsh-doctor CLI, deciding explicitly up front whether the upgraded release must stay compatible with DSH 0.1.1. Use when a plugin developer plans a migration or compatibility assessment: checking what changed between DSH versions, replacing imports of packages 0.1.5 removed (such as dsh-client-runtime or dsh-host-apiproxy), migrating settingsNamespace to the settings Service, updating DSH dependency ranges, or verifying and preparing a plugin release for 0.1.5. Applies only catalog-confirmed exact rewrites automatically and guides the semantic changes that need developer judgment. Not for debugging a plugin that already targets 0.1.5, general DSH usage or configuration questions, or developing the Harness itself."
---

# Upgrade a DSH 0.1.1 plugin to 0.1.5

Help the developer diagnose and modify one plugin at a time. Treat source migration, artifact verification, runtime activation, and business behavior as separate gates.

The migration knowledge covers the DSH 0.1.1 to 0.1.5 transition, derived and verified from one exact catalog version pair (declared below). Keep the skill's product scope at the release-line level (`0.1.1` to `0.1.5`), while keeping the catalog target exact. First record the plugin's actual DSH ranges and requested target. When a newer patch or prerelease appears, use the catalog for known changes only, inspect the additional interval, and report that it is not catalog-confirmed until the catalog and this skill are deliberately updated — a pass for the catalog pair never proves an unlisted version combination.

## Current catalog version pair

This block is the single source of truth for the exact refs. Every command below and every reference file defers to it; the references avoid repeating the literals on purpose. When the catalog advances, update this block, the `migrate analyze` example, and the shipped catalog together.

- source ref: `dsh-v0.1.1-rc.2`
- target ref: `dsh-v0.1.5-rc.2`

Standard commands target this pair and need no `--target-version`. If the developer explicitly targets a newer 0.1.5 build before the catalog is updated, inspect that additional interval first (see [source-investigation.md](references/source-investigation.md)), then pass its exact version to every migration phase as `--target-version <actual-0.1.5-version>`. That changes dependency pins and runtime expectations only; the catalog's API claims still end at the declared pair.

## Inputs

Determine:

- the plugin repository root;
- the DSH Harness checkout when available;
- the plugin's actual DSH dependency and peer ranges, and the requested 0.1.5 target;
- whether the upgraded plugin must keep supporting DSH 0.1.1, target only DSH 0.1.5, or still needs that decision from the developer;
- whether the developer authorizes writes and project command execution;
- whether the developer authorizes a global CLI install or update;
- the plugin's package manager and build scripts.

Read [cli-bootstrap.md](references/cli-bootstrap.md) before running any migration command, [compatibility-strategy.md](references/compatibility-strategy.md) before proposing or writing changes, [source-investigation.md](references/source-investigation.md) before investigating an unlisted version or semantic task, [migration-map.md](references/migration-map.md) before making semantic changes, and [verification.md](references/verification.md) before dependency, build, or runtime verification.

Before touching the plugin, inspect the local CLI and perform the read-only registry update check described in `cli-bootstrap.md`. Select one exact DSH Doctor version, verify it exposes this migration catalog, and keep the same invocation for analyze, apply, and verify. Prefer the exact-version `npm exec` fallback over changing the developer's global installation; a global install or update always needs explicit authorization.

The examples below use `dsh-doctor` for readability. When bootstrap selected a package-runner invocation, substitute the complete pinned prefix, `npm exec --yes --package=@bruc3van/dsh-doctor@<selected-version> -- dsh-doctor`, in every phase. Command examples use POSIX shell syntax (bash, zsh, Git Bash); in PowerShell or cmd, join lines continued with `\` into a single line before running them.

## Compatibility decision gate

An upgrade request does not say whether the developer accepts dropping DSH 0.1.1, and write authorization does not answer that product decision. The current peer range, the word "upgrade," and the fact that a 0.1.5-only rewrite is simpler are all weak evidence — only the developer's explicit choice settles it.

You may inspect files, bootstrap the CLI, and run read-only analysis first. Before any `migrate apply` preview, source or manifest edit, dependency install, build, or runtime command, the compatibility intent must come from one of:

1. an explicit choice already present in the developer's request; or
2. the developer's own reply to: **"Should the same upgraded plugin release continue to support DSH 0.1.1, or may it target DSH 0.1.5 only?"**

No other resolution counts. Do not simulate, assume, or fabricate a reply the developer did not give — a question the developer has not genuinely answered means the gate is still pending. The plugin may be migrated only after the developer has actually made the choice.

If the answer is unavailable or ambiguous, stop at `analyzed`, report the compatibility decision as pending, and leave the plugin unmodified. Follow the selected path in [compatibility-strategy.md](references/compatibility-strategy.md): it defines the three intents (`0.1.5-only`, `dual-version`, `pending developer decision`) and the write policy for each. In particular, `dual-version` treats every 0.1.5 catalog rewrite as a candidate needing cross-version design and review before any write, never an automatically compatible change.

## Phase 1: analyze

Run from any directory:

```sh
dsh-doctor migrate analyze <plugin-root> \
  --from dsh-v0.1.1-rc.2 \
  --to dsh-v0.1.5-rc.2 \
  --json
```

Append `--harness-root <deepseek-harness-root>` when the checkout is available. Prefer an exact Harness checkout so the CLI verifies both tag commits. Both tags must exist and resolve to the commits recorded by the catalog; fetch the repository tags first when a shallow checkout lacks them. Without `--harness-root`, analysis is catalog-only — report it as such.

Follow `source-investigation.md` to record the actual PATH or explicit DSH command, installed package, profile, plugin manifest and resolved dependency versions. When the actual source or target differs from the catalog pair declared above, inspect that additional interval separately with read-only Git commands. For each semantic finding, use its target module and the catalog reference paths to inspect the exact exported API and the plugin's callers — naming a likely new owner is not enough to plan the rewrite.

The catalog reports the retained-package removal of `@deepseek-ai/dsh-settings.settingsNamespace` as semantic work. Remove only that named import, inject the `settings` Service, register through `ctx.settings.register(name, schema)`, and migrate any reads to the provider's current API. Symbols 0.1.5 still exports (such as `SettingsConflictError`) must survive the edit even though they share the same import declaration.

The static analyzer recognizes named imports and re-exports for retained-package symbol removals, but it does not resolve property access through namespace imports such as `import * as settings from '@deepseek-ai/dsh-settings'`. Search for and inspect those namespace bindings manually before declaring the semantic migration complete.

Group the result by:

1. errors blocking compatibility;
2. exact import moves eligible for safe codemods;
3. semantic tasks requiring developer judgment;
4. stale build artifacts;
5. required verification gates.

A clean bundled artifact alone does not establish compatibility, which is why the analyzer deliberately scans TypeScript type imports, source files, package metadata, client graph declarations, and built output.

## Phase 2: apply exact changes

Enter this phase only after the compatibility decision gate is resolved. The commands below are the 0.1.5-target migration path. For dual-version work, first apply the additional constraints in `compatibility-strategy.md`: a catalog-safe codemod proves nothing about 0.1.1.

Preview first:

```sh
dsh-doctor migrate apply <plugin-root> --safe \
  --plan-file <reviewed-plan-outside-plugin-root.json> \
  --harness-root <deepseek-harness-root> --json
```

Store the plan outside the plugin root so it is not treated as plugin input. Review the plan id, complete analysis, affected files, and before/after hashes. Apply that exact plan only with explicit authorization:

```sh
dsh-doctor migrate apply <plugin-root> --safe --yes \
  --plan-file <same-reviewed-plan.json> \
  --harness-root <deepseek-harness-root> --json
```

The CLI binds the apply to the persisted report and edit hashes, creates timestamped backups, and refuses writes when the plugin analysis changed after preview. It may split a mixed import: exact symbols move to their new owners while semantic symbols remain unresolved. Dependency additions follow catalog-owned Client/Host and peer/dev policies instead of copying the removed package's old dependency section. It may pin non-removed DSH development dependencies. It does not widen the ranges of existing published peers automatically. Never mechanically replace the removed Client Runtime with one aggregate package; no such replacement exists.

After apply, inspect every `MIG_SEMANTIC_API_CHANGE`. Rewrite behavior using the new domain owner and its current snapshot/lifecycle contract. Keep these edits separate enough to review and test.

### If apply fails partway or you want to undo it

Every file `migrate apply` overwrites is first copied to `<file>.dsh-doctor-<timestamp>.bak` next to the original; the apply output's `writes[]` records each file's `backup`, `beforeHash`, and `afterHash`. There is no `migrate rollback` subcommand — recover manually:

1. Restore each modified file from its `.bak` for the apply run being undone (`cp <file>.dsh-doctor-<timestamp>.bak <file>`, or `Copy-Item -Force` in PowerShell), taking the backups of that exact run when several exist.
2. Delete files apply created: they are the `writes[]` entries without a `backup` field.
3. Re-run `migrate analyze` and compare with the pre-apply report to confirm the plugin is back to its prior state before continuing.

Later analysis runs ignore leftover `.dsh-doctor-*` files, so backups can stay in place until the rollback is confirmed, then be deleted.

## Phase 3: verify

Run the gates in order:

```sh
dsh-doctor migrate verify <plugin-root> --level static --harness-root <deepseek-harness-root> --json
dsh-doctor migrate verify <plugin-root> --level build --yes --install --harness-root <deepseek-harness-root> --json
dsh-doctor migrate verify <plugin-root> --level runtime --yes --install --dsh-command <actual-dsh-command> --json
```

Build and runtime levels require `--yes --install`: the CLI first runs the detected package manager with lifecycle scripts disabled, updates the lockfile when needed, and verifies the installed DSH/Cordis versions against runtime, development, peer, and optional dependency declarations before executing project scripts. A required peer must resolve and satisfy every declared range; a missing optional peer is recorded but does not fail the gate. Review lockfile changes as migration changes. Runtime verification then packs the real plugin, creates a temporary `DSH_HOME`, installs into a new web profile, dumps effective config, and performs an activation smoke. It does not modify the developer's normal `~/.dsh`.

Resolve every semantic task and rebuild stale artifacts before expecting static verification to pass. An `apply` exit code of 1 after successful writes means migration blockers remain in the follow-up analysis; inspect `mode`, `writes`, and `report` instead of treating it as a write failure.

On failure, preserve and report the temporary directory. On success, the CLI removes it unless `--keep-temp` is used.

Runtime activation is not business-behavior proof. Finish with targeted manual or automated checks for visible UI, service lifecycle, event subscriptions, cleanup, configuration, and plugin-specific workflows.

For a dual-version result, verify the produced release against both the actual 0.1.1 and 0.1.5 environments. The catalog-driven `migrate verify` commands prove only the configured target side. Use the plugin's own build/test flow and an isolated 0.1.1 Harness profile for the legacy side, and name the evidence from each matrix row. A successful 0.1.5 runtime smoke must never be reported as dual-version compatibility.

## Prepare for release when requested

Verification prepares the plugin for release but does not publish it. Release only when the developer explicitly asks: first follow the repository's own release instructions and confirm that required semantic and behavior checks are complete. Then update the plugin version and changelog, inspect the packed artifact, and use the repository's existing commit, tag, publish, and registry-verification workflow — the migration skill being installed or run is not, by itself, release authorization.

For a `0.1.5-only` release, update the README or compatibility documentation to state the minimum actual 0.1.5 version, that the new release does not support 0.1.1, and which prior plugin release 0.1.1 users should retain when known. After changing the release version or any other packed metadata, rebuild, inspect the final-version tarball, and repeat the isolated runtime gate against that artifact before committing or tagging; evidence from a tarball carrying the previous plugin version is not final release evidence.

## Pass criteria before reporting

Call the migration complete only when every item holds:

- compatibility intent recorded as `0.1.5-only` or `dual-version` (not pending);
- every semantic finding resolved and reviewed, including namespace-import usages;
- static verification passes with no blocking finding;
- build and packed artifacts pass (`build` or `pack:check`, not `typecheck`/`test` alone);
- runtime smoke passed against the exact target version in the isolated profile;
- behavior checks executed with named evidence, or explicitly listed as remaining;
- for `dual-version`: every required matrix row passed on both the 0.1.1 and 0.1.5 sides.

## Report the outcome

State the highest achieved gate exactly:

- `analyzed`
- `source-migrated`
- `artifact-verified`
- `runtime-verified`
- behavior verified separately with named evidence

Do not call the plugin compatible while errors, semantic tasks, stale artifacts, or required behavior checks remain. Include backups and retained temporary directories in the handoff.
Also report the selected DSH Doctor version and source (`local`, exact-version `npx`, or explicitly authorized global install), the registry version observed at bootstrap, and whether update status was current, outdated, missing, or unknown.
Report the plugin's actual source/target version evidence separately from the catalog reference refs. State whether the plugin is ready for its normal release process; if a release was explicitly requested and completed, include the commit, tag, registry, and release verification evidence.
Report the migration plan file and plan id, dependency-install command, lockfile change, and resolved target dependency versions. For semantic or unlisted-version work, include the DSH executable/package evidence, checkout refs and commits, inspected source paths, and remaining unknowns described in `source-investigation.md`.
State the compatibility intent as one of `0.1.5-only`, `dual-version`, or `pending developer decision`. For `dual-version`, report build, artifact, runtime, and behavior evidence separately for 0.1.1 and 0.1.5; only call the release dual-compatible when every required row passes.
