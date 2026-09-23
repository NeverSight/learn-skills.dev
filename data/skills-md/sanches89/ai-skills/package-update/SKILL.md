---
name: package-update
description: Updates the npm dependencies of a package or monorepo to current versions. Use when the user wants packages updated, upgraded, or bumped, or says they are outdated.
license: MIT
compatibility: Requires Node.js 22 or newer with npx, git, network access to the package registry, and the project's package manager (npm, pnpm, yarn, or bun) on PATH. npx fetches npm-check-updates and semver into its own cache on the first run.
argument-hint: "[path...] [package name...] [latest | minor | patch] [cooldown <days>]"
disable-model-invocation: true
---

# Package Update

Move every dependency in every `package.json` of one repository to the
highest version that the project's own check commands accept. Return the
change in the working tree plus an update report.

## Terms

These words have exactly one meaning in this skill.

- **Install root**: a folder that owns a lockfile and the `node_modules` that
  one install of that lockfile fills. A workspace root and its members share
  one install root.
- **Root manifest**: the `package.json` in the folder of an install root.
- **Apply**: set every range of a batch of packages, then run the plain
  install. Then run the check commands in the baseline order up to the first
  failure.
- **Pass**: the outcome of an apply that meets three conditions. The plain
  install succeeds. Every failing check command fails in the baseline results
  too. The peer report shows no problem beyond the baseline peer report.
  Every other outcome is a fail.
- **Accepted**: the state of a plan entry, a group, or a rung whose apply
  passed.
- **Hold**: leave the range that a package has at that moment, recording a
  hold reason for the package.

## Hard rules

1. **Only manifests and lockfiles change**, from Step 6 on, through the
   script and the package manager. Never edit source code, a configuration
   file, a CI file, or a lockfile by hand.
2. **No tool enters the project.** Run npm-check-updates and semver from the
   npx cache. Never add either to a manifest or write an `.ncurc` file.
3. **Never ask what research can answer.** Consult the manifests, the
   lockfiles, the docs, and the registry first.
4. **Never assume.** When a decision changes the work and research cannot
   settle it, ask the user.
5. **No outward actions.** Commit, push, or open a pull request only when
   the request says so. Then make one commit per accepted plan entry, in
   the project's branch and commit conventions.

## Script

`scripts/set-range.mjs` rewrites the range of one dependency in one
`package.json` and keeps every other byte. Run it as
`node <skill-dir>/scripts/set-range.mjs`, where `<skill-dir>` is the folder
holding this `SKILL.md` (in Claude Code, `${CLAUDE_SKILL_DIR}`). Run it with
`--help` for the options and the exit codes. Step 6 writes every range with
it.

## Workflow

### Step 1: Load the request

Resolve the invocation text, or the request in the conversation, into four
values:
- **Paths**: files or folders that limit the manifests. Default: the whole
  repository.
- **Package names**: names that limit the dependencies. Default: every
  dependency.
- **Level**: `latest`, `minor`, or `patch`. Default: `latest`. `minor` never
  bumps a major. `patch` never bumps a minor.
- **Cooldown**: the number of days since a version's publish date below
  which the run never takes it. Default: 7.

Record whether the request asks for commits, for hard rule 5.

Write private notes in a scratch directory outside the repository from this
step on, written `<scratch-dir>` in commands (in Claude Code, the scratchpad
directory). Keep in them every list that a later step reads.

### Step 2: Inventory

**2a. Manifests.** List every `package.json` under the paths. Run from the
repository root:

```bash
git ls-files -co --exclude-standard -- '*package.json' \
  | grep -E '(^|/)package\.json$' \
  | grep -vE '(^|/)(node_modules|fixtures|__fixtures__|templates?)/' \
  | grep -vE '(^|/)(dist|build|out|coverage)/'
```

**2b. Install roots.** Read `references/package-managers.md` now. Assign
each manifest one kind:
- a manifest with a `workspaces` field, or with a `pnpm-workspace.yaml`
  beside it, is a workspace root. Its members are the manifests its
  workspace globs match. Its folder is the install root of itself and of
  its members;
- a manifest beside a lockfile, and not a member, is the root manifest of a
  standalone install root: its own folder;
- every other manifest is an orphan manifest. Step 6 sets its ranges without
  an install. The update report lists it under *Unverified*.

Record the package manager and version of each install root by the
*Detection* section of `package-managers.md`. When the package manager on
PATH has a different major, follow its *Version* section. Every later
install of that install root runs with that package manager, never another.

**2c. Node version.** Read `references/update-rules.md` now. Take the first
Node version source that exists, in this order:
1. `.nvmrc`;
2. `.node-version`;
3. the `volta.node` field of the root manifest;
4. the `node-version` of a workflow file under `.github/workflows/`;
5. the `engines.node` field of the root manifest;
6. `node -v`.

Record the version as `<node-version>`, with its Node version source.

**2d. Check commands.** Record the check commands of each install root, in
this order:
1. the frozen install and the plain install from `package-managers.md`;
2. each `scripts` entry of the root manifest named `typecheck`,
   `type-check`, `check-types`, `lint`, `build`, or `test`;
3. every other `scripts` entry of the root manifest that a workflow file
   under `.github/workflows/` runs.

When a workspace root has no `scripts` entry of item 2, record instead the
recursive run command of `package-managers.md` for each of the six names.
An install root with no check command beyond the install commands is an
install-only root.

**2e. Pins.** Read these files: `renovate.json`, `.renovaterc`,
`.renovaterc.json`, `.github/renovate.json`, and `.github/dependabot.yml`.
Read the `overrides`, `resolutions`, and `pnpm.overrides` fields of every
root manifest. Record two lists, as `update-rules.md` says under *Pins* and
*Overrides*:
- the held packages, each with its hold reason;
- the capped packages, each with its cap: a version range or a level.

### Step 3: Baseline

Record in the scratch directory, before changing anything:
- the output of `git status --porcelain`. When the request asks for commits
  and a manifest or a lockfile has uncommitted changes, ask one question:
  commit or stash them first;
- the baseline results, per install root: the result of the frozen install,
  then of each check command, with pass or fail and the duration. When the
  frozen install fails, run the plain install instead and record
  `install (frozen)` as a baseline failure;
- the baseline order: the check commands sorted by duration, shortest
  first. Keep that order for every later run of the check commands;
- the baseline peer report, per install root, from `package-managers.md`;
- the baseline copy and the checkpoint, as `update-rules.md` defines under
  *Checkpoint*.

### Step 4: Candidate versions

`<root>` in a file name below is the path of the install root, with `/`
replaced by `-`. For an orphan manifest, it is the path of the manifest's
folder, written the same way. The current range of a dependency is its range
in the baseline copy.

Run in each install root, and in the folder of each orphan manifest:

```bash
npx --yes npm-check-updates@23 --workspaces --root \
  --packageManager <package-manager> --target <level> --cooldown <days> \
  --no-deprecated --peer --dep prod,dev,optional \
  --reject '<member names>,@types/node,<held package names>' \
  --filter '<package names>' --jsonUpgraded \
  > <scratch-dir>/<root>-latest.json
```

Drop `--workspaces --root` for a standalone install root and for an orphan
manifest. Drop `--peer` for an orphan manifest. Drop `--filter` when the
request names no package. `<held package names>` are the held packages of
Step 2e. The output maps each manifest path to the dependencies with a
higher version, each with its new range in the manifest's own style. Remove
from it every range that *Left alone* of `update-rules.md` names. Record
each range and field under *Left alone*, with its kind, for the update
report.

With level `latest`, run the command a second time with `--target minor`
into `<scratch-dir>/<root>-minor.json`: the highest minor of every current
major. With level `minor` or `patch`, copy `<root>-latest.json` to
`<root>-minor.json`.

Write one `<name>@<version>` line per dependency of `<root>-latest.json`
into `<scratch-dir>/<root>-specs.txt`, with the version written without its
range prefix. For an alias `npm:<name>@<range>`, write the aliased name and
version. Then gather the registry facts in one loop:

```bash
while IFS= read -r spec; do
  printf '%s\t' "$spec"
  npm view "$spec" engines.node peerDependencies deprecated --json \
    2>/dev/null | tr -d '\n'
  printf '\n'
done < <scratch-dir>/<root>-specs.txt > <scratch-dir>/<root>-facts.tsv
```

Check each candidate version against the constraints of `update-rules.md`,
in its order. Lower or hold a refused candidate version as its *Constraints*
section says. Then add
`@types/node` as a candidate package in every manifest that has it, with the
version that constraint 3 of `update-rules.md` gives. Record per candidate
package:
- the manifest and the section;
- the name;
- the current range and the candidate range;
- the bump kind: `major`, `minor`, or `patch`, from the first number that
  differs between the current range and the candidate range;
- the constraint that lowered the candidate version, or `none`;
- the peer ties, as `update-rules.md` defines under *Groups*.

### Step 5: Write the update plan

Build the plan entries of each install root:
1. one plan entry *minor and patch*, with every candidate package of
   `<root>-minor.json` that Step 4 did not hold;
2. one plan entry per group, from the candidate packages of
   `<root>-latest.json` with bump kind `major`. `update-rules.md` defines a
   group under *Groups*.

Then build one plan entry *orphan* per orphan manifest, with every candidate
package of its `<root>-latest.json` that Step 4 did not hold.

Order the plan entries:
1. the *minor and patch* plan entry of each install root;
2. every group that provides a peer dependency to another group;
3. the other groups, by their first package name;
4. the *orphan* plan entries.

Write each plan entry in this form:

```
<number>. <install root or manifest>: minor and patch | major group <name>
   packages: <name> <current range> to <candidate range>, ...
   lowered: <name> to <candidate range> by <constraint>, ... | none
```

Show in chat:
- the manifests of each install root, with its package manager and
  `<node-version>`;
- the check commands;
- the plan entries;
- the packages held by a constraint, each with its hold reason;
- the *Left alone* list.

Then ask one question with three options: approve every plan entry, approve
some plan entries by number, or change the plan. A change names a package to
exclude, a manifest to exclude, or a package to cap at a version. Repeat the
question until the user approves.

With no candidate package, go to Step 8 with the result `done` and zero plan
entries.

### Step 6: Apply the update plan

Work one install root at a time, in plan order. A batch is a list of
packages applied together: a plan entry, a half of one, or a group at one
rung. Set the ranges of a batch with one loop:

```bash
while IFS=$'\t' read -r manifest name range; do
  node <skill-dir>/scripts/set-range.mjs "$manifest" "$name" "$range" || break
done < <scratch-dir>/<root>-<batch>.tsv
```

A non-zero exit of the script stops the loop. Fix the TSV line that failed,
then run the loop again: the script leaves a range that already equals its
new value as it is. Never repair a fail with a code change. The bisection
and the ladder hold what breaks.

**6a. Minor and patch.** Apply the *minor and patch* plan entry. On a pass,
mark the plan entry accepted. On a fail, bisect the plan entry as
`update-rules.md` defines under *Bisection*. The bisection holds each
breaking package with the reason `check: <name>`. Then replace the
checkpoint. With commits requested, commit now.

**6b. Major groups.** Without commits requested, apply every approved group
as one batch. On a pass, mark every group accepted. On a fail, bisect the
batch with a group as the unit. Walk the ladder of `update-rules.md` for each
breaking group: apply the group at each rung, highest first. Mark the first
rung whose apply passes as accepted. Hold a group with no accepted rung, with
the reason `check: <name>`.

With commits requested, apply the groups one at a time in plan order:
1. apply the group;
2. on a fail, restore the checkpoint. Then apply the group at the next rung
   of its ladder. Hold the group when no rung remains;
3. on a pass, commit. Then replace the checkpoint.

**6c. Assemble.** Skip this step with commits requested. Otherwise:
1. restore the checkpoint;
2. apply every accepted group as one batch, each at its accepted rung, or
   at its candidate versions when the bisection accepted it without the
   ladder;
3. on a fail, apply the accepted groups one at a time in plan order. After
   a pass, replace the checkpoint. After a fail, restore the checkpoint.
   Then hold the group.

**6d. Orphans.** Set the ranges of each approved *orphan* plan entry with the
loop above. Run no install and no check command there. With commits
requested, commit after each *orphan* plan entry.

### Step 7: Verify

Run for each install root, in this order:
1. the frozen install from the new lockfile;
2. every check command, in the baseline order;
3. the peer report of `package-managers.md`;
4. the diff review: compare every manifest with the baseline copy.

Step 7 passes for an install root when all of these hold:
- the frozen install succeeds;
- every failing check command fails in the baseline results too;
- the peer report shows no problem beyond the baseline peer report;
- `git status --porcelain` names only manifests and lockfiles beyond the
  Step 3 record;
- every changed line of a manifest holds the range of an accepted package;
- every changed range keeps its style;
- the diff adds, removes, downgrades, or moves no dependency;
- every range under *Left alone* is unchanged;
- every `overrides`, `resolutions`, and `pnpm.overrides` field is unchanged;
- no file outside the install root changed.

On a fail, act on the first condition above that fails, then run this step
again:
- the frozen install: run the plain install;
- a check command or the peer report: find the accepted plan entry that
  causes the fail by bisection, with a plan entry as the unit. Hold every
  package of that plan entry with the reason `verify: <condition>`;
- a condition on a manifest: restore that manifest from the checkpoint. Set
  its accepted ranges again with the script. Run the plain install;
- a condition on a file that is not a manifest or a lockfile: revert a
  tracked file with `git checkout -- <file>`, and delete an untracked file.

After 3 fails on one install root, restore that install root from the
baseline copy. Then hold every package of that install root.

### Step 8: Update report

Read `references/update-report-template.md` now and fill it in the scratch
directory. Run every check in `references/quality-checklist.md` over the
report, grep helper included, and fix every failure.

Send the update report as the final message, unchanged. Ask nothing and
offer nothing after it.
