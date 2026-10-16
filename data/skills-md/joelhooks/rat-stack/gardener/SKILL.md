---
name: gardener
description: Keep rat-stack current and clean. Update exact dependency versions, learn from repos on the same versions, and add lint rules before cleanup.
plain: "Bump one pin line at a time, learn from peers, and write a failing lint rule before cleaning up a bad pattern."
diagram: |-
  check the pins
    │
  bump one line
    │ lockfile, mirrors, docs
    ▼
  refresh peers
    │
  garden
    rule fails first
    then fix every case
---

# Maintain rat-stack

Rat-stack runs on Effect 4 stable, Alchemy 2 betas, and XState 6 alphas. Effect describes work with typed failures and required dependencies. Alchemy declares and deploys cloud resources through Effect programs. Keep copied code compatible with the current dependency versions. Simplify it as these dependencies change.

Follow Lauren Tan's gardener loop from her Dune talk: remove technical debt, keep one supported implementation pattern, and reject prohibited patterns with lint. In her words: "whenever you see tech debt or bad patterns, your instinct should be, I need to write a lint rule against it." She ranks where to put corrections by enforcement strength: codebase, static analysis, rules, skills, style guide. Use the strongest applicable option for each finding.

Read `AGENTS.md` first. Work in a clean clone off `origin/main`, never in a checkout with other people's uncommitted files.

## 1. Check the pins

The core pins live in the `package.json` files and in `minimumReleaseAgeExclude` in `pnpm-workspace.yaml`. Compare each with the currently published versions on npm. Run registry queries outside the repo so its development-engine check does not block them:

```sh
cd /tmp
for p in effect @effect/platform-node @effect/vitest @effect/tsgo alchemy xstate @xstate/effect; do
  printf '%-24s ' "$p"; pnpm view "$p" dist-tags --json | tr -d '\n '; echo
done
```

Read the returned versions, not only the tag names. Effect 4 and its adapters now use `latest`; `rc` points to the older release candidate. Alchemy 2 and `@effect/tsgo` use `latest`. XState 6 uses `alpha`; its `latest` still points to XState 5. For `@xstate/effect`, compare both `alpha` and `latest` among the 0.1 alpha versions: `latest` can be newer. Check the bridge's peer ranges before choosing the matching XState pin.

## 2. Update one dependency family at a time

For each dependency family that is behind:

1. Replace the pin everywhere it appears. Effect runtime packages and adapters move together; `rg -l -F '"<old-pin>"' --glob '**/package.json'` finds both stable and prerelease pins. Keep each Effect-family update in its own commit, separate from other dependency updates and cleanup. XState and its Effect bridge move together.
2. Respect the release-age policy. Replace an existing `minimumReleaseAgeExclude` entry with the new exact package version; never widen it to a package name or range. Before adding a necessary exact-version exception, inspect the registry integrity, provenance, tarball file list, package scripts, and dependency changes. Record what you checked.
3. Check peer ranges before installing: `pnpm view alchemy@<pin> peerDependencies`. Alchemy pins exact Drizzle versions and a minimum Effect; follow them.
4. Let `pnpm install` generate the lockfile; never edit it by hand. Before gating, prove freshness with `pnpm --config.optimistic-repeat-install=false install --frozen-lockfile --force`, then `pnpm peers check`; compare warnings with `origin/main`. After any dependency change, run `pnpm install --frozen-lockfile` before each gate. Keep `verifyDepsBeforeRun: error`: pnpm otherwise auto-installs during scripts. Even `--force` can skip broken YAML through the optimistic cache; `lockfile:check` disables that cache and never repairs the lock.
5. Refresh the source mirrors with `./scripts/vendor-agent-sources.sh --refresh` and update the Ref column in `.agent_sources/README.md`. Agents read the mirrors as truth, so a stale mirror teaches old APIs.
6. Read what changed upstream: `git -C .agent_sources/github.com/<owner>/<repo> log --oneline <old-tag>..<new-tag>` when the old tag is fetchable, or the package's CHANGELOG. Grep our code for every API those commits touch.
7. Update the version text in `AGENTS.md` and `README.md`. `packages/core/test/docs-pins.test.ts` fails until they match the manifests.
8. Run `pnpm turbo run check test build --force` and check its exit code.

Commit each dependency family separately, so a regression can be traced to one library.

## 3. Peers refresh

Run the `find-peers` skill every week or two and after every shared dependency update, even when there are no new peers. Read each peer's default-branch manifests or lockfiles and refresh its exact versions, checked date, tier, and evidence-based reason in `.brain/data/peers.json`. The content build reads rat-stack's current pins from its manifests and filters/sorts this one dataset into `.brain/resources/peers.svx`; do not hand-edit table rows. Drift is expected. Keep every peer: S through B in the main table, C through F in the collapsed **Also seen** list. Study relevant new peers using the skill's source-first process.

Check the dataset's oldest peer checked date on every gardener pass. If it is fourteen days old, refresh it before continuing; a shared dependency update always triggers a refresh. This repo-native pass owns the cadence. Put the rubric, full ranking, tier changes, and unresolved versions at the top of the report for feedback after shipping; no separate approval round is required.

## 4. Remove prohibited patterns

Run `pnpm --filter @rat-stack/site generate`, read `.brain/data/unlinked-mentions.generated.json`, and turn useful unlinked mentions into explicit source links after checking their context; leave incidental matches alone.

Look for technical debt and patterns that should not spread:

- Duplicated logic.
- A second implementation where a supported pattern already exists.
- Unchecked `unknown` values passed to application code.
- Unused exports.
- Tests that assert nothing.

For each one:

1. Write the lint rule or test that fails on it first. Put a real-`oxlint` fixture test beside the other rule tests in `packages/core/test/`. Break the rule once to watch the test fail.
2. Then fix every existing instance, so the rule starts at zero findings.
3. If some findings have to stay for now, record them as a baseline that can only shrink. Never raise a baseline.
4. Delete code that nothing uses. Git keeps it.

When a pattern cannot be caught by lint, fix it in the codebase so the wrong version is hard to write. Only fall back to prose in `AGENTS.md` or a skill when neither works.

## Report

Report:

- each pin moved, from and to;
- upstream changes that affected us;
- peers studied, and what was adopted or rejected;
- lint rules added, and the findings each one removed;
- anything left undone.

Name the changes required in apps that copy rat-stack.
