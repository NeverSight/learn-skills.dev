---
name: setup-code-quality
description: Set up or migrate TypeScript projects to Oxlint, type-aware linting, Oxfmt, jscpd, Knip, TypeScript 7, and a comment lint that rejects code comments, through a shared check script. Use for requests to adopt this quality stack or replace overlapping lint and format tools; leave incompatible projects unchanged.
disable-model-invocation: true
---

# Setup code quality

Install and wire the requested quality stack, preserving checks with unique coverage. Scope is tooling setup and verification. Do not automatically repair pre-existing code findings, delete unused application code, remove existing comments, reformat the repository, or refactor duplication. Creating this skill is not an instruction to run it against the current repository.

## Establish compatibility before edits

- Read applicable project instructions and inspect the existing working changes, package manifests, lockfiles, source languages, framework, TypeScript configs, and quality commands. Follow commands into their actual orchestrators, CI jobs, hooks, and editor settings.
- A package manifest alone does not establish compatibility. Require an actual TypeScript project that can run the full requested stack. For a JavaScript-only, pure Rust, Python, or other incompatible project, report the reason and make no changes, including no new package manifest or lockfile.
- In a mixed repository, scope changes to compatible TypeScript packages. Preserve other languages' tools. Use the existing workspace owner for shared dependencies and avoid duplicate per-package installs. If the target package or root scope is materially ambiguous, resolve that before edits.
- Check current official package documentation and registry metadata for Node engines, package-manager support, TypeScript 7 support, peer dependencies, framework requirements, and configuration syntax. Do not assume the latest package versions are mutually compatible. Respect the project's runtime and dependency policies; do not upgrade its runtime, framework, or unrelated packages to force compatibility.
- Use the latest compatible stable TypeScript **7.x** release, not an unbounded latest tag, a preview, or a different major. If that or another required tool cannot work with the project, leave the target unchanged and report the concrete blocker. Do not silently install a partial stack. Do not introduce TypeScript aliases or compatibility fallbacks without explicit approval.

## Configure the stack

Use the project's existing package manager to add or reconcile these **devDependencies** and its authoritative lockfile. Run the installed local tools, not `dlx`, global executables, or commands that fetch packages on demand. Preserve an already suitable version rather than upgrading unnecessarily.

| Package | Responsibility |
| --- | --- |
| `oxlint` | General JS/TS lint rules and the lint CLI |
| `oxlint-tsgolint` | Type-aware lint rules through Oxlint |
| `oxfmt` | Formatting and formatting checks for supported files |
| `jscpd` | Duplicate-code detection with a failing threshold |
| `knip` | Unused files, exports, and dependencies |
| `typescript` at 7.x | Dedicated typechecking through its native checker |
| `oxc-parser` | Comment extraction for the comment lint script |

Enable Oxlint's type-aware mode and relevant rules; installing the companion package alone is insufficient. Keep full typechecking in the dedicated TypeScript step instead of also enabling Oxlint's full typecheck mode. Verify the installed executable and supported flags from the selected versions.

Reuse valid project configuration. Cover authored source and applicable tests with the project's TypeScript projects or references; avoid blanket unchecked scopes. Preserve framework-specific checkers when they cover templates or contracts the native checker cannot.

Model Knip's real package entry points, framework conventions, scripts, and dynamic loading. Configure jscpd for authored code. Exclude generated output, build artifacts, vendored code, and generated fixtures where justified; do not exclude ordinary source or tests merely because they produce findings.

Default to **zero detected duplicate blocks** without asking the user for a threshold. Wire jscpd with `--threshold 0 --exit-code 1 --no-tips --reporters ai` by default, replacing a nonzero existing threshold unless the user explicitly requests otherwise. Retain meaningful minimum block-size settings; zero detected blocks does not require every repeated expression or line to count as duplication. Never raise those minimums, infer a threshold from existing duplication, add a baseline, or suppress failures to obtain green results. Verify that the selected jscpd version supports the requested flags and that a detected duplicate block causes exit code 1 through the actual check command.

## Replace overlapping tools without losing coverage

Compare actual enabled rules, file types, custom plugins, and consumers, not package names alone. Remove redundant tools such as Biome, ESLint, or Prettier and their now-unused configs, plugins, dependencies, and scripts. When an old tool supplies unique checks or formatting the new stack cannot cover, retain it only for that responsibility and explain the gap. Examples can include framework diagnostics, specialized CSS rules, and unsupported file formats.

Carry equivalent deliberate rules and settings into the new configuration where supported. Inspect existing suppression comments such as `eslint-disable`, `biome-ignore`, and `prettier-ignore`; translate justified exceptions, remove obsolete directives, and report exceptions with no equivalent. Do not broadly suppress new findings or silently discard custom rules.

Update affected CI commands, Git hooks, editor settings, config references, and relevant tooling documentation together. Preserve unrelated settings and scripts. Remove old script implementations only after migrating their callers; a useful existing script name can invoke the new tool. Do not leave stale references or run two formatters over the same files.

## Wire the comment lint

The comment lint is on by default. It fails on every code comment except the directives the stack reads and exact per-file entries the maintainer approves, so agents get the feedback from `check` right after they write one.

- Copy `assets/lint-comments.mjs` to the package's `scripts/lint-comments.mjs`, and create `scripts/comment-lint.json` as `{ "exclude": [], "allow": {} }`. The script runs from the package directory and scans that package's tracked and untracked `.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs`, and `.cjs` files that git does not ignore. It also fails on files it cannot parse and on `allow` entries whose exact comment text is gone.
- Add a `lint:comments` script that runs it with the project's runtime (`node scripts/lint-comments.mjs`, or `bun` in a Bun project). Make it the last step of `check`, so a newly adopted repository's comment findings do not stop the other checks from running.
- Add committed generated output to `exclude`, matching what jscpd and Knip exclude, such as `dist/` or `src/routeTree.gen.ts`. An entry ending in `/` covers a directory; any other entry is one exact path. Never exclude authored source or tests.
- Leave `allow` empty. Filling it from the existing comments would be a baseline. Existing comments are pre-existing findings: report their count and suggest the `cleanup-comments` skill, if installed, for the cleanup.
- Suppressions this setup writes, such as translated `eslint-disable` directives, must take an allowed form: `// oxlint-disable-next-line <rules> -- <reason>`, or `{/* … */}` inside JSX. A file-wide disable has no allowed form; translate it to a scoped config override or report it.
- Copy `assets/fix-comment-lint/` to `.agents/skills/fix-comment-lint/` at the repository root and add the symlink `.claude/skills/fix-comment-lint` pointing to `../../.agents/skills/fix-comment-lint`. If `.gitignore` ignores either directory, add negations so both are committed. In a workspace package, change `FIX_SKILL_PATH` in the copied script to the skill's path from the package directory.
- Add `assets/agents-comments-section.md` to the project's agent instructions: `AGENTS.md`, or `CLAUDE.md` if that is the project's file. Create `AGENTS.md` if neither exists. In the installed skill and section, replace `<run>` with the package manager's script runner, such as `bun run`, `pnpm`, or `npm run`. Report existing instructions that contradict the section, such as rules requiring doc comments, by file and line; do not rewrite them.
- Format the copied files with the project's formatter. They must pass the rest of the stack without suppressions. Model `scripts/lint-comments.mjs` as a Knip entry (a production entry if Knip runs in production mode) so `oxc-parser` counts as used.
- On reruns, never change `allow` or `exclude` entries. If the installed script differs from the template beyond formatting and `FIX_SKILL_PATH`, or the installed skill differs beyond `<run>`, report the difference instead of overwriting it.

## Wire the check command

Create the package's `check` script if absent; otherwise extend its existing implementation or orchestrator. Preserve existing tests, builds, specialized validation, and ordering requirements. Ensure the command reaches linting, formatting checks, duplication detection, unused-code detection, dedicated typechecking, and the comment lint, plus retained unique checks. Avoid recursive workspace calls, cycles, and duplicate execution of the same checks.

Checks must propagate failure and must not apply fixes or rewrite authored files. Normal caches and required build outputs may follow existing project conventions. Use Oxfmt's check mode, and keep lint fixes, formatting writes, and Knip removals out of `check`. Reuse or add separate explicit fix/format commands where useful. Never add `|| true`, warnings-only gates, or automatic baseline updates to conceal findings.

## Verify and report

- Run each newly configured tool and the actual aggregate `check` entry point. Verify that a comment added to authored source makes the actual check command exit 1 through the comment lint, then remove it. If the aggregate stops at its first failure, run remaining new checks individually to learn whether they work. Inspect the diff and verify that retained callers resolve and removed tools have no stale consumers.
- Distinguish broken setup from pre-existing code findings using the reported files, rules, and before/after evidence where feasible. Fix migration-caused problems within this scope. Do not claim a finding is pre-existing without evidence. Preserve valid failure exits and report code findings separately rather than launching a cleanup campaign.
- If installation or configuration cannot be completed, restore only this run's changes, preserving previous dirty files and any concurrent work. Record enough initial state before edits to support that recovery; never use a blanket reset, clean, or checkout. Report any unresolved partial state honestly. Successful setup with existing code findings stays installed.
- Reruns reconcile the setup without duplicating scripts, resetting deliberate configuration, or changing already suitable versions. Do not commit or publish unless requested.
- Finish with the installed versions, commands, removed tools, retained tools and their unique coverage, the comment lint's finding count and any contradicting instructions, and observed check results. Separate setup completion from repository check success; identify any unrun checks.
