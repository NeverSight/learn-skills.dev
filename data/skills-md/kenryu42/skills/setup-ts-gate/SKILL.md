---
name: setup-ts-gate
description: Put a TypeScript project behind a static gate that stops agents from landing bad code. Oxlint with type-aware rules, Oxfmt, jscpd, Knip, TypeScript 7, and a comment lint all run from one `check` script. Installs or migrates the tooling, clears every existing finding locally, and writes a ship-stack plan that lands the fixes first and the gate last, so trunk never goes red. Stops at the plan for approval; leaves incompatible projects unchanged.
disable-model-invocation: true
---

# Setup TS gate

The gate is the project's `check` command: every check an agent's change must pass. This skill installs the gate, brings the codebase to zero findings, and plans the delivery:

- **Fix layers first.** Each passes the project's current `check`, because fixed code is valid without the new tools.
- **The tooling layer on top.** It turns every gate on at once, and it is green because the layers below already cleared the findings.
- **Refactor layers after that.** The code changes that make the code say what deleted comments said run with the gate already on.

All work happens in a temporary worktree. The user's checkout, branches, and remote stay untouched until the user approves the plan. Creating this skill is not an instruction to run it against the current repository.

Sibling skills live next to this one. `../cleanup-comments/SKILL.md` means the `cleanup-comments` skill in the directory that holds this skill. Read a sibling's `SKILL.md` and follow it when a step names it. `ship-stack` is a Claude Code skill; follow its plan rules and template.

## Establish compatibility before edits

- Read applicable project instructions and inspect the package manifests, lockfiles, source languages, framework, TypeScript configs, and quality commands. Follow commands into their actual orchestrators, CI jobs, hooks, and editor settings. Record the project's current check command: every fix layer must pass it.
- A package manifest alone does not establish compatibility. Require an actual TypeScript project that can run the full stack. For a JavaScript-only, Rust, Python, or other incompatible project, report the reason and make no changes.
- In a mixed repository, scope changes to compatible TypeScript packages. Preserve other languages' tools. Use the existing workspace owner for shared dependencies and avoid duplicate per-package installs. If the target package or root scope is materially ambiguous, resolve that before edits.
- Check current official package documentation and registry metadata for Node engines, package-manager support, TypeScript 7 support, peer dependencies, framework requirements, and configuration syntax. Do not assume the latest package versions are mutually compatible. Respect the project's runtime and dependency policies; do not upgrade its runtime, framework, or unrelated packages to force compatibility.
- Use the latest compatible stable TypeScript **7.x** release, not an unbounded latest tag, a preview, or a different major. If that or another required tool cannot work with the project, report the concrete blocker and change nothing. Do not silently install a partial stack. Do not introduce TypeScript aliases or compatibility fallbacks without explicit approval. TypeScript 7 has no JavaScript compiler API, so confirm that framework builds that typecheck through it can run the `tsc` CLI instead; Next.js 16.3 and later do by default.
- The checkout must be clean on an up-to-date trunk. Record the trunk commit as the baseline. Create a detached worktree at the baseline in a temporary directory outside the checkout, install dependencies there with the frozen lockfile, and do all following work in it. A worktree shares the checkout's `.git/hooks`: if an install script such as `prepare` installs git hooks (lefthook, husky), rerun that installer from the checkout after removing the worktree. Knip's lefthook plugin reads that shared hooks path, which lies outside the worktree and makes Knip scan from `/`. In the worktree, run Knip with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=.git/hooks`, but not installs, whose hook installer then fails.
- Choose the plan file's location by `ship-stack`'s rule. Keep the findings inventory, layer patches, and plan together, untracked.
- Keep the laptop responsive: at most 3 agents at once, and run installs, checks, and scans under `nice -n 15`.

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

Enable Oxlint's type-aware mode (`options.typeAware`) and relevant rules; installing the companion package alone is insufficient. Set `options.denyWarnings` so warning-level rules fail `check`. For JavaScript files outside the typechecked projects, such as scripts without `checkJs`, turn the type-aware rules off in an override, as typescript-eslint's `disable-type-checked` config does: without types they only report `any`. Keep full typechecking in the dedicated TypeScript step instead of also enabling Oxlint's full typecheck mode. Verify the installed executable and supported flags from the selected versions.

Reuse valid project configuration. Cover authored source and applicable tests with the project's TypeScript projects or references; avoid blanket unchecked scopes. Preserve framework-specific checkers when they cover templates or contracts the native checker cannot.

Model Knip's real package entry points, framework conventions, scripts, and dynamic loading. Configure jscpd for authored code. Exclude generated output, build artifacts, vendored code, and generated fixtures where justified; do not exclude ordinary source or tests merely because they produce findings.

Default to **zero detected duplicate blocks** without asking the user for a threshold. Wire jscpd with `--threshold 0 --exit-code 1 --no-tips --reporters ai` by default, replacing a nonzero existing threshold unless the user explicitly requests otherwise. Retain meaningful minimum block-size settings; zero detected blocks does not require every repeated expression or line to count as duplication. Never raise those minimums, infer a threshold from existing duplication, add a baseline, or suppress failures to obtain green results. Verify that the selected jscpd version supports the requested flags and that a detected duplicate block causes exit code 1 through the actual check command.

## Replace overlapping tools without losing coverage

Compare actual enabled rules, file types, custom plugins, and consumers, not package names alone. Remove redundant tools such as Biome, ESLint, or Prettier and their now-unused configs, plugins, dependencies, and scripts. When an old tool supplies unique checks or formatting the new stack cannot cover, retain it only for that responsibility and explain the gap. Examples can include framework diagnostics, specialized CSS rules, and unsupported file formats.

Carry equivalent deliberate rules and settings into the new configuration where supported. To map Biome, read each enabled rule's ESLint sources from `https://biomejs.dev/metadata/rules.json`, match them against `oxlint --rules --format=json`, and list the rules with no equivalent. Start Oxfmt's config with `oxfmt --migrate=biome` or `--migrate=prettier`; Biome's `organizeImports` maps to `sortImports` with `newlinesBetween: false`. Compare `oxfmt --list-different` with the old formatter until authored code shows no differences you did not choose, since the rest becomes a formatting commit. Inspect existing suppression comments such as `eslint-disable`, `biome-ignore`, and `prettier-ignore`; translate justified exceptions, remove obsolete directives, and report exceptions with no equivalent. Do not broadly suppress new findings or silently discard custom rules.

Update affected CI commands, Git hooks, editor settings, config references, and relevant tooling documentation together. Preserve unrelated settings and scripts. Remove old script implementations only after migrating their callers; a useful existing script name can invoke the new tool. Do not leave stale references or run two formatters over the same files.

## Wire the comment lint

The comment lint fails on every code comment except the directives the stack reads and exact per-file entries the maintainer approves, so agents get the feedback from `check` right after they write one.

- Copy `assets/lint-comments.mjs` to the package's `scripts/lint-comments.mjs`, and create `scripts/comment-lint.json` as `{ "exclude": [], "allow": {} }`. The script runs from the package directory and scans that package's tracked and untracked `.ts`, `.tsx`, `.mts`, `.cts`, `.js`, `.jsx`, `.mjs`, and `.cjs` files that git does not ignore. It also fails on files it cannot parse and on `allow` entries whose exact comment text is gone.
- Add a `lint:comments` script that runs it with the project's runtime (`node scripts/lint-comments.mjs`, or `bun` in a Bun project), as a step of `check`.
- Add committed generated output to `exclude`, matching what jscpd and Knip exclude, such as `dist/` or `src/routeTree.gen.ts`. An entry ending in `/` covers a directory; any other entry is one exact path. Never exclude authored source or tests.
- Fill `allow` only with the entries `cleanup-comments` classifies in "Clear every finding", never from the existing comments wholesale: that would be a baseline.
- Suppressions this setup writes, such as translated `eslint-disable` directives, must take an allowed form: `// oxlint-disable-next-line <rules> -- <reason>`, or `{/* … */}` inside JSX. A file-wide disable has no allowed form; translate it to a scoped config override or report it.
- Copy `assets/fix-comment-lint/` to `.agents/skills/fix-comment-lint/` at the repository root and add the symlink `.claude/skills/fix-comment-lint` pointing to `../../.agents/skills/fix-comment-lint`. If `.gitignore` ignores either directory, commit them with `git add -f` and leave `.gitignore` unchanged. Tracked files are unaffected by it, while a negation that re-includes anything under an ignored directory makes Knip stop honoring the whole ignore and report the user's untracked local files there. Later edits need `git add -f` too: naming a tracked path under an ignored directory still stages it, but `git add` exits 1, which breaks `&&` chains. In a workspace package, change `FIX_SKILL_PATH` in the copied script to the skill's path from the package directory.
- Add `assets/agents-comments-section.md` to the project's agent instructions: `AGENTS.md`, or `CLAUDE.md` if that is the project's file. Create `AGENTS.md` if neither exists. In the installed skill and section, replace `<run>` with the package manager's script runner, such as `bun run`, `pnpm`, or `npm run`. Report existing instructions that contradict the section, such as rules requiring doc comments, by file and line; do not rewrite them.
- Format the copied files with the project's formatter. They must pass the rest of the stack without suppressions. Model `scripts/lint-comments.mjs` as a Knip entry (a production entry if Knip runs in production mode) so `oxc-parser` counts as used.
- On reruns, never change `allow` or `exclude` entries. If the installed script differs from the template beyond formatting and `FIX_SKILL_PATH`, or the installed skill differs beyond `<run>`, report the difference instead of overwriting it.

## Wire the check command

Create the package's `check` script if absent; otherwise extend its existing implementation or orchestrator. Preserve existing tests, builds, specialized validation, and ordering requirements. Ensure the command reaches linting, formatting checks, duplication detection, unused-code detection, dedicated typechecking, and the comment lint, plus retained unique checks. Avoid recursive workspace calls, cycles, and duplicate execution of the same checks.

Checks must propagate failure and must not apply fixes or rewrite authored files. Normal caches and required build outputs may follow existing project conventions. Use Oxfmt's check mode, and keep lint fixes, formatting writes, and Knip removals out of `check`. Reuse or add separate explicit fix/format commands where useful. Never add `|| true`, warnings-only gates, or automatic baseline updates to conceal findings.

## Verify the tooling

- Run each newly configured tool and the aggregate `check`. Verify that a comment added to authored source makes `check` exit 1 through the comment lint, then remove it. Run each gate individually as well, since the aggregate stops at its first failure. Verify that retained callers resolve and removed tools have no stale consumers. The worktree lacks the checkout's ignored local files, so plant an untracked source file in each ignored directory the setup touched and confirm that every gate still skips it.
- Distinguish broken setup from existing code findings using the reported files, rules, and before/after evidence. Fix setup problems now; existing findings are the next section's work. Do not claim a finding is pre-existing without evidence.
- Commit the tooling on the worktree's detached HEAD with a Conventional Commit message. This is the tooling commit.
- If the tooling cannot be completed, report the blocker, remove the worktree, and stop. The checkout was never touched.

## Clear every finding

Run every gate and save each gate's findings with counts next to the plan. Then clear them in the worktree, each theme as its own commit on top of the tooling commit. You commit; agents working in parallel edit disjoint files and never run git.

- **Comments:** run `cleanup-comments` (`../cleanup-comments/SKILL.md`) in its caller mode, with this worktree and the tooling commit as its baseline. It commits a strip proven to change no code, and returns keep and temporary `allow` entries and the `MUST KILL` items. Add the entries to `scripts/comment-lint.json` as one commit; it joins the tooling layer.
- **Formatting:** run Oxfmt in write mode as one commit. Prove it changes no code in source files with `node <skills directory>/cleanup-comments/scripts/verify-strip-js.mjs <previous commit>`, which should report no deleted comments; review its other files by diff.
- **Typecheck, Oxlint, Knip, and jscpd findings:** fix each at its root, grouped by gate and area into commits sized for review.
  - A finding that exposes a real bug gets a failing test first, then the fix.
  - Use Oxlint's and Knip's fix modes only where their rewrites are safe, and review their diffs.
  - Never loosen configuration, raise jscpd minimums, add Knip ignores, or suppress a finding without a proven reason in an allowed form.
  - Ask the user before a fix that needs a decision: a Knip "unused" export that may be public API, a duplicate whose merge needs a design choice, or any change to public behavior.

Repeat until `check` passes in the worktree. Behavior-preserving commits keep every existing test and assertion unchanged.

## Order the stack

Rebuild the commits on the baseline in this order, bottom to top:

1. the comment strip;
2. the formatting and fix commits;
3. the tooling layer: the tooling commit and the `allow` entries commit, squashed into one.

Record the cleaned worktree's HEAD, check out the baseline detached in the same worktree, and cherry-pick each commit in that order. After each one below the tooling layer, run the project's current check command. A commit that does not apply or does not pass without the tooling, such as formatting that the old formatter's check rejects, folds into the tooling layer. After the tooling layer, the new `check` must pass, and `git diff <cleaned HEAD>` must be empty.

Save each layer with `git format-patch` next to the plan. Then remove the worktree with `git worktree remove`, without `--force`.

## Plan and stop

Write the plan with `ship-stack`'s template.

- **Patch layers:** each applies its patch with `git am`. Spec: the check it must pass (the project's current check below the tooling layer, the new `check` from the tooling layer up) and its proof command, such as `verify-strip-js.mjs` for the strip. If trunk moved past the baseline and `git am` conflicts, redo that layer's work for the conflicting files from the new trunk.
- **`MUST KILL` layers, above the tooling layer:** from `cleanup-comments`' items, split by `ship-stack`'s rules, as `cleanup-comments` describes. They run with the gate on, so their agents follow `.agents/skills/fix-comment-lint/SKILL.md`. Name the temporary `allow` entries each layer deletes.
- **Open decisions:** the permanent `allow` entries, with a recommended default for each; decisions the user made while clearing findings; retained tools and their unique coverage; contradicting agent instructions.

Report:

- installed versions, commands, and removed or retained tools;
- findings per gate before clearing, and how each gate was cleared;
- the layer table;
- the open decisions;
- the paths of the plan, inventory, and patches.

Then stop. After the user approves, deliver the plan with `ship-stack`, starting at its Phase 2.

## Reruns

A rerun on a project whose gate is installed reconciles the setup without duplicating scripts, resetting deliberate configuration, or changing already suitable versions. If `check` already passes, report that and stop.
