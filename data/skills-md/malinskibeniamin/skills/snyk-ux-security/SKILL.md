---
name: snyk-ux-security
description: Audit frontend, Go, and Bazel dependencies with Snyk, exploitability triage, and release gates.
disable-model-invocation: true
---

[REFERENCE.md](REFERENCE.md). Scan -> reachability -> act -> verify. `$ARGUMENTS`: paths, globs or findings.

Report-only runs stop after scan and reachability: no monitor, ignore removal, or edits. Detect `package.json`, `go.mod`, `MODULE.bazel`, or `bazel/repositories.bzl`. Process sequentially in the primary context; worktree lanes require that the user explicitly delegates or invokes `/swarm`. Bazel checks backports; draft PRs.

1. **Prepare:** verify `snyk`/`gh` auth; reuse an existing Snyk project. Never create one from an audit/sweep branch or YYYY-MM-DD identity. Infer reviewers from CODEOWNERS, then `git log`; flags win.
2. **Revisit:** re-triage `.snyk`; remove stale ignores with `snyk ignore --remove --id=<id>` and mark `cleaned-up`.
3. **Scan:** `snyk test`; JS adds `bun audit`, Go `govulncheck ./...`. Run `snyk monitor` only when the requested endpoint includes a Snyk cloud update for one existing project.
4. **Reachability:** use `bun why`, `go mod why`, imports, callers, and the vulnerable symbol. Use `/steelman` for transitives and `/diagnosing-bugs` before a `package.json` fix. Its admission gate permits a direct dep, reachable parent, or proven last-resort override. Direct dep absence means do not add it; without vulnerable-symbol reachability, a bump makes no sense: dismiss the unproven finding.
5. **Act:** default unreachable findings to `snyk ignore --id=<id> --reason='<why>' --expiry=<date>`. Always include `.snyk` in any requested delivery; confirm `Ignored`. PR text alone is not enough. Reachable: use `/upgrade-dependency` and its supply-chain gate; direct dep, parent, Remove dependency surface third, then last-resort `resolutions`/`overrides`/`replace`. Override list growth is a smell: lockfile bloat scales poorly.
6. **Ecosystem gates:**
   - JS: minimum release age gate audit, Socket.dev web check, React 18 `bun info <pkg>@<v> peerDependencies.react`; record `react19-blocked`. Run `bun update`, `bun install`, `bun install --yarn`. Commit both lockfiles (`bun.lock`, `yarn.lock`); Snyk IO needs `yarn.lock`. Do not create, update, or commit `package-lock.json`; `lockfile-sync-check` enforces dual-lockfile sync.
   - Go: `go get -u`, `go mod tidy`; commit `go.mod`/`go.sum`.
   - Bazel: update applicable manifests; run `bazel mod deps --lockfile_mode=update`; preserve mirror/FIPS/CMVP.
7. **Verify:** read changelogs/`BREAKING`; migrate 7 -> 8 -> 9 incrementally. Commit `refactor(deps)` groups unless stopped earlier. Never defer real vulnerabilities; escalate. JS: `bun run lint:fix`, `bun run type:check`, `bun test`, build. Go: `go build ./...`, `go test ./...`, `go vet ./...`, `govulncheck ./...`.
8. **Deliver:** run `/resilience-review` and `/review`; `/to-tickets` only when ticket publication is requested. If the requested endpoint includes a commit or PR, commit `fix(deps)` and open a PR only when requested. Use `gh pr create --assignee <triggerer> --reviewer <team-group> --label security,...`; resolve via `gh api user --jq .login`, require a CODEOWNERS team group, auto-add security for dismissals/overrides. Apply `team/`, `dismissals`, `overrides-added`, `react19-blocked`, `cleaned-up`. Run `gh workflow run` only when cloud review was requested.

Report path, ecosystem, branch/PR, and outcome counts. Never run advisory code or expose tokens.
