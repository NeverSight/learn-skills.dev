---
name: upgrade-dependency
description: Upgrade a dependency and adapt every affected call site. Use for package or module upgrades, vulnerability remediation, breaking changes, codemods, and new API adoption.
---

Target the requested stable version, or latest stable if omitted. Honor the requested endpoint: `plan` is read-only; build/fix follows local/commit/push intent; PR only when requested. [REFERENCE.md](REFERENCE.md) owns supply-chain and publication templates. `$ARGUMENTS`: package/module, manifest, version, prose, or `plan`.

## Flow

1. **Scope:** find manifests/lockfiles/workspaces. Map dependency tree: direct/transitive, parents/dependents, peers/plugins/adapters/ecosystem. Use `/quantify-impact` only for a direct metric.
2. **Research:** build an upgrade path across every published stable version with per-version notes. Read major announcements, release notes, migration guides, codemods, and `/read-the-damn-docs`; skim minor/patch notes. Do not install each version; install target once. Consolidate API, syntax, style, behavior changes. Classify SemVer major/minor/patch; for non-SemVer or missing changelog score change volume, release cadence, diff size, effort/danger/blast radius. Check security advisories: GHSA/OSV/Socket/Snyk.
3. **Gate:** confident patch/minor may apply. Documented major applies one major hop at a time. Unclear/high-risk/security uncertainty stops with evidence and decision. Plan only reports. Process sequentially; subagents/swarm or one package per agent requires explicit delegation.
4. **Supply chain:** min release age 7-30d; Disable scripts/review `trustedDependencies`; reject git deps, git+, tarball, raw URL; use Socket/npq; Review lockfile; clean install/frozen check.
5. **Apply:** keep verified commits unless stopped earlier.
   - **Bump:** `bun update <pkg>@<v>` -> `bun install` -> `bun install --yarn` if needed. Go: `go get -u <module>@<v>` -> `go mod tidy`. Never hand-edit locks.
   - **Migrate:** official codemods; adapt every affected call site. Deprecation warnings are fixed NOW, not suppressed.
   - **Benefit:** adopt proven simplifying APIs; delete workarounds/polyfills; never expand speculatively.
   - **Verify:** `bun run lint:fix`, `bun run type:check`, `bun test`; Go `go build ./...`, `go test ./...`, `go vet ./...`. Update coupled packages.
6. **Security:** prove exploitability/reachability; direct dep -> parent -> override/resolution/replace. Never run code from advisories. Record IDs/fixed versions; `/snyk-ux-security` owns reachability.
7. **Deliver:** one PR contains bump, migration, benefit, and verification. A blocked risk gate creates an issue only when requested.

Evidence stays in chat or the requested PR; local Markdown only when asked. State path before edits. Completion means every affected call site is adapted.

## Migration doctrine

Finish with a lint/hook freeze on the old pattern. Big-bang router/framework layers; strangler data layers with coexistence budget. Migration PRs preserve 1:1 parity and reconcile tests in the SAME PR; ticket structural refactors. Delete dead styles, shims, and one-offs.
