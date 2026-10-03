---
name: oss-repo-setup
description: OSS-ready repo setup
disable-model-invocation: true
metadata:
  short-description: OSS-ready repo setup
---

# OSS Repo Setup

## Codex Compatibility
When running this skill in Codex, translate `AskUserQuestion` -> chat/`request_user_input`, and resolve `${CLAUDE_SKILL_DIR}` to the directory containing this `SKILL.md` (e.g. `~/.agents/skills/oss-repo-setup` or `~/.codex/skills/oss-repo-setup`).

## Cursor Compatibility
When running this skill in Cursor Agent, translate `AskUserQuestion` -> `AskQuestion`, and resolve `${CLAUDE_SKILL_DIR}` to the directory containing this `SKILL.md` (e.g. `~/.agents/skills/oss-repo-setup` or `~/.cursor/skills/oss-repo-setup`).

Bring a repository to the laststance open-source baseline in four reviewable commits, then push and configure GitHub only after the user confirms.

- **Model**: `laststance/happy-dom-extended` (`gh repo clone` it when you need to diff).
- **Applied example (VS Code extension)**: `laststance/deep-trace-extension`, commits `e19f27e` → `30da1c5`.
- Assets = generalized copies of those files. When unsure, diff against the example repo.

## Ground rules

- pnpm only, `packageManager` pinned with integrity, `.node-version` present.
- **No Dependabot.** Never add `.github/dependabot.yml`; remove an existing one.
- `CODECOV_TOKEN` and `SOCKET_SECURITY_API_TOKEN` are laststance **organization secrets**. Do not create repo secrets.
- Never silence Fallow/ESLint with ignores or thresholds to get green. Add tests or refactor.
- Code/docs in English. Tests: `test` not `it`, AAA comments, literal expectations.
- **Push and repo settings only after AskUserQuestion approval.**

## Scaffold script

```sh
node "${CLAUDE_SKILL_DIR}/scripts/scaffold.mjs" --group <tooling|ci|docs> [--dry-run] [--skip <path>]... [--force]
```

Copies `assets/<group>/` into the cwd repo (`dot-x` → `.x`), fills `{{OWNER}}`/`{{REPO}}` (from `origin`), `{{PROJECT_NAME}}` (package.json), `{{NODE_VERSION}}` (`.node-version`), `{{MAINTAINER}}` (the signed-in `gh` account). Existing files are **kept** (merge by hand). Prints placeholders left for you. Override with `--owner --repo --name --maintainer`.

## Workflow

### 1. Survey (read-only)

```sh
git status --short --branch && git log --oneline | head -20
cat package.json .node-version pnpm-workspace.yaml 2>/dev/null; ls -a; ls .github/workflows 2>/dev/null
gh repo view --json visibility,description,homepageUrl,repositoryTopics
gh api repos/{owner}/{repo}/actions/organization-secrets --jq '.secrets[].name'
```

Determine: project type (library / VS Code extension / CLI / app), test runner, build tool, existing lint/format/CI, LICENSE present, public or private (Scorecard needs public). Require a clean tree. Run a `--dry-run` of each group to see conflicts.

### 2. Tooling → commit `chore: add ESLint, Prettier, Fallow and coverage tooling`

`--group tooling`, install deps, scripts, TS 7/6 alias, `pnpm format` + `lint:fix` across the repo. Details: `references/tooling.md`.

### 3. Tests → commit `test: ...`

Loop `pnpm test:coverage && pnpm health` until green, then `pnpm dupes && pnpm dead-code`. Host APIs (e.g. `vscode`) via an in-memory fake. Details: `references/testing.md`.

### 4. CI → commit `ci: add lint, format, Fallow, security, Socket, Scorecard and Codecov workflows`

`--group ci`, adapt build/test matrix, fill `.coderabbit.yaml`, delete Dependabot. Details: `references/ci.md`.

### 5. Docs → commit `docs: add community health files, architecture and testing guides, README badges`

`--group docs`, fill every placeholder from the code, README badges + "Contribute and release" section, `git add` then `pnpm check:docs`. Details: `references/docs.md`.

### 6. Gate

`pnpm check` green on the final tree; each commit should pass on its own.

### 7. Confirm → 8. Push, settings, CI

AskUserQuestion: push target, description/homepage/topics, private vulnerability reporting, delete-branch-on-merge, ruleset. Then push, apply, watch runs, handle Codecov first-upload failure. Details: `references/publish.md`.

## Commit order matters

Tooling first: the reformat and new scripts land alone, so the test/ci/docs diffs stay reviewable and every later commit already passes format/lint. Tests before CI: the first CI run (Fallow health with coverage) is green. Docs last: badges and links point at workflows that exist.

## Pitfalls (verified on deep-trace-extension)

| Symptom                                                        | Cause → Fix                                                                                                                                                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Test job fails at Codecov upload: `Repository not found`       | New repo not synced in Codecov yet → `gh run rerun <id> --failed` (only the failed job). No workflow change                                                                                 |
| VS Code ext: badge missing on Marketplace / `vsce package` err | Marketplace allows only approved badge hosts → GitHub workflow badges, `codecov.io`, `img.shields.io`; Scorecard via `img.shields.io/ossf-scorecard` (not `api.scorecard.dev`)              |
| Marketplace version/installs badge broken                      | Marketplace dynamic badges discontinued → static `img.shields.io/badge/...` link; Open VSX dynamic badge still OK                                                                           |
| Want TS 7, but ESLint breaks when `typescript` is 7            | `eslint-config-ts-prefixer` (typescript-eslint) does not support TS 7 → `typescript@~6.0.3` + `typescript-compiler@npm:typescript@7`; run `node ./node_modules/typescript-compiler/bin/tsc` |
| TS 7 errors on `moduleResolution: node`                        | node10 removed → `node16`/`nodenext`/`bundler`                                                                                                                                              |
| Fallow dead-code flags `dispose`, provider methods             | `usedClassMembers[].implements` must be the full name as written: `vscode.Disposable`, not `Disposable`                                                                                     |
| Fallow flags `typescript-compiler` unused                      | Run by path → `ignoreDependencies` + `framework[].toolingDependencies`                                                                                                                      |
| Fallow flags the `vscode` fake's exports                       | `// fallow-ignore-file unused-export unused-type unused-class-member` at top of the fake                                                                                                    |
| `pnpm health` differs locally / in CI                          | Needs `pnpm test:coverage` first; CI checkout needs `fetch-depth: 0`                                                                                                                        |
| `pnpm check:docs` ignores a new doc / passes a broken link     | It reads `git ls-files '*.md'` only → `git add` new docs before running                                                                                                                     |
| `pnpm install --frozen-lockfile` fails in CI                   | pnpm 12 records `packageManagerDependencies` in the lockfile → commit the updated lockfile                                                                                                  |
| Fresh dependency version refuses to install                    | `minimumReleaseAge: 1440` → use the previous release; keep the setting                                                                                                                      |
| VSIX suddenly contains configs/docs                            | Add new files to `.vscodeignore`                                                                                                                                                            |

## References

Load each file when its step starts:

- [references/tooling.md](references/tooling.md) - deps, scripts, tsconfig, Fallow config, VS Code extension extras (step 2)
- [references/testing.md](references/testing.md) - health loop, test style, host API fakes (step 3)
- [references/ci.md](references/ci.md) - workflow table, conventions, re-pinning actions, secrets (step 4)
- [references/docs.md](references/docs.md) - placeholders, README badges (incl. Marketplace rules), link check (step 5)
- [references/publish.md](references/publish.md) - AskUserQuestion checklist, push, `gh` settings, CI triage (steps 7-8)
- [scripts/scaffold.mjs](scripts/scaffold.mjs) - template copier; its tests run with `node --test scripts/scaffold.test.mjs`
