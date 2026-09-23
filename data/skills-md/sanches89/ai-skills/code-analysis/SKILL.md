---
name: code-analysis
description: Measures a repository's duplication, complexity, tests, coverage, and mutation score, and compares a branch with its base. Use when the user wants code measured or analyzed.
license: MIT
compatibility: Requires Node.js 22.13 or newer with npx and git, run inside a git repository, with network access on the first run. Complexity needs lizard on PATH, or uv, pipx, or a Python that has lizard. Tests and coverage need the project's own test command. Mutation needs the project's own mutation command. A missing tool skips its measurement and never blocks the report.
argument-hint: "[base]"
disable-model-invocation: true
---

# Code Analysis

Take one repository and measure its duplication, complexity, hotspots, unit
tests, coverage, and mutation score. With a base name, measure the base
commit too and compare. Return a measurement report.

## Hard rules

1. **The project stays as it is.** Change no project file. Add no
   dependency, tool, configuration file, JUnit report, coverage report, or
   mutation report to the repository. Write every report, summary, diff, and
   note of the run in the scratch directory.
2. **Never ask what research can answer.** Consult the code, the docs, the
   git history, and the summaries first.
3. **Never assume.** When a decision changes the work and research cannot
   settle it, ask the user.
4. **No outward actions.** Never commit, push, open a pull request, or post
   a comment.

## Script

`scripts/diff-summaries.mjs` compares two summaries of the measure tool. Run
it as `node <skill-dir>/scripts/diff-summaries.mjs`, where `<skill-dir>` is
the folder holding this `SKILL.md` (in Claude Code, `${CLAUDE_SKILL_DIR}`
expands to it). Run it with `--help` for the options and the exit codes.
Step 5 runs it once.

## Workflow

### Step 1: Load the request

Resolve the invocation text, or the request in the conversation, as one
kind:
- **Nothing**: no base name. The run analyzes the working tree alone.
- **One name**: the base name, a branch, a tag, or a commit. Confirm it with
  `git rev-parse --verify --quiet "<base name>^{commit}"`. When the command
  fails, ask one question: which base name to use.
- **Anything else**: ask one question: which one name is the base name, or
  none.

With a base name, record the base commit: the output of
`git merge-base <base name> HEAD`. When that command fails, the base name
and `HEAD` share no history. Ask one question: take the commit the base name
resolves to as the base commit, or give another base name.

The current code is the working tree, uncommitted and untracked files
included. Record the output of `git status --porcelain` and of
`git rev-parse --short HEAD`.

Write private notes in a scratch directory outside the repository, written
`<scratch-dir>` in commands (in Claude Code, the scratchpad directory). Keep
in the notes every list a later step reads.

### Step 2: Inventory

Run every command from the repository root, the output of
`git rev-parse --show-toplevel`, unless a step says otherwise. Measure the
repository root in every run, with `.` as the path.

**2a. Ignore globs.** List the tracked files that are generated, vendored,
or built:

```bash
git ls-files | grep -iE \
  -e '(^|/)(generated|__generated__|vendor|vendored|third_party)/' \
  -e '\.(min\.js|min\.css|pb\.go|pb\.ts|g\.dart|generated\.[a-z]+)$'
```

Record one glob per folder or extension found, such as `**/generated/**` or
`**/*.pb.go`. Add one glob per folder that the project's lint or coverage
configuration lists as generated. Record the globs as `<globs>`, joined by
commas.

**2b. Limits.** Read `references/measure-tool.md` now. Record `<ccn>`,
`<length>`, and `<params>`: the project's own limits when it configures
them, else 10, 50, and 4.

**2c. Install and test commands.** Read `references/test-reports.md` now.
Record, as that file says:
- the install command, `none`, or `unknown`;
- the test command with the report options, with `<dir>` in place of the
  output folder;
- `<junit-report>` and `<coverage-report>`: the paths of the JUnit report
  and the coverage report relative to `<dir>`, or the reason a report is
  skipped.

Skip 3b and 4a when the runner writes neither report.

**2d. Changed files.** Skip this sub-step without a base name. Write the
changed files, one path per line:

```bash
{ git diff --name-status <base-commit> | grep -v '^D' \
    | awk -F'\t' '{ print $NF }'
  git ls-files --others --exclude-standard
} | sort -u > <scratch-dir>/changed.txt
```

Record the count of deleted files from
`git diff --name-status <base-commit> | grep -c '^D'`.

**2e. Mutation command.** Read `references/mutation-reports.md` now.
Record, as that file says, the mutation command with the report options,
with `<dir>` in place of the output folder, and `<mutation-report>`. Record
the reason instead when the file says to skip the mutation run.

### Step 3: Base run

Skip this step without a base name.

**3a. Worktree.** Run
`git worktree add --detach <scratch-dir>/base <base-commit>`. Run 3b and 3c
from `<scratch-dir>/base`. Never check out, stash, reset, or switch the
working tree.

**3b. Tests.** With the install command `unknown`, record the base tests and
coverage as skipped with the reason `no install command`, and go to 3c.
Otherwise run the install command, unless it is `none`, then the test
command with `<dir>` set to `<scratch-dir>/base-reports`. Afterwards do the
step that `test-reports.md` gives for .NET, Maven, and Gradle. A failing
test is a result, not a failure of the run. When the install command fails,
or the test command writes neither report, record the base tests and
coverage as skipped. The reason is the first line of the error.

**3c. Measure.** Run the measure tool:

```bash
<measure> . --ignore "<globs>" --ccn <ccn> --length <length> \
  --params <params> --top 200 \
  --test-report <scratch-dir>/base-reports/<junit-report> \
  --coverage-report <scratch-dir>/base-reports/<coverage-report> \
  > <scratch-dir>/base.json
```

Leave out `--ignore` with no glob, and each report option without its
report.

**3d. Remove.** From the repository root, run
`git worktree remove --force <scratch-dir>/base`, then
`git worktree prune`. Run 3d also when 3a, 3b, or 3c fails.

### Step 4: Current run

**4a. Tests.** Run the test command from the repository root, with `<dir>`
set to `<scratch-dir>/current-reports`. When it fails to start on a missing
dependency, run the install command once and the test command again. Skip
both when the install command is `none` or `unknown`. Afterwards do the
step that `test-reports.md` gives for .NET, Maven, and Gradle. When the test
command writes neither report, record the current tests and coverage as
skipped. The reason is the first line of the error.

**4b. Mutation.** Skip this sub-step when Step 2e recorded a reason. Run
the mutation command from the folder that `mutation-reports.md` names, else
from the repository root, with `<dir>` set to
`<scratch-dir>/current-reports`. Only the current code gets a mutation run:
one run often takes longer than all other steps together. Let it finish,
however long it takes (in Claude Code, run it in the background). Afterwards
do the step that `mutation-reports.md` gives for the tool. A surviving
mutant is a result, not a failure of the run. When the mutation command
fails, or writes no report, record the first line of the error as the
reason.

**4c. Measure.** Without a base name, run the command of 3c with
`current-reports` in place of `base-reports` and `current.json` in place of
`base.json`. Add
`--mutation-report <scratch-dir>/current-reports/<mutation-report>`. With
a base name, run:

```bash
<measure> . --top 200 \
  --test-report <scratch-dir>/current-reports/<junit-report> \
  --coverage-report <scratch-dir>/current-reports/<coverage-report> \
  --mutation-report <scratch-dir>/current-reports/<mutation-report> \
  --compare <scratch-dir>/base.json > <scratch-dir>/current.json
```

Pass `--mutation-report` once per mutation report. Leave out each report
option without its report.

Record the exit code. On `2`, fix the arguments and run the command again.
On `1`, or when the measure command fails to start, go to Step 7. The
result is then `blocked`, with the first line of the error as the reason.

### Step 5: Compare

Skip this step without a base name. Run:

```bash
node <skill-dir>/scripts/diff-summaries.mjs \
  <scratch-dir>/base.json <scratch-dir>/current.json \
  --changed <scratch-dir>/changed.txt > <scratch-dir>/diff.json
```

`cut` in the output names every list that reached 200 entries: its diff is
partial. Name every cut list under *Skipped* in the measurement report.

### Step 6: Read the code

Read `references/analysis-rules.md` now. A number alone is never a finding:
read the code behind each entry that file names, both locations of a clone
included. Record per finding:
- the kind, and the location as `path:line` with the symbol;
- the evidence: the measured values, or what the code shows;
- the action, from the *Actions* section of `analysis-rules.md`;
- with a base name, whether the location is in a changed file, and whether
  `diff.json` lists the entry under `added`.

Rank the findings as the *Ranking* section of `analysis-rules.md` says.

### Step 7: Measurement report

Read `references/measurement-report-template.md` now and fill it in the
scratch directory. Run every check in `references/quality-checklist.md`,
grep helper included, over the measurement report. Fix every failure.

Send the measurement report as the final message, unchanged. Ask nothing and
offer nothing after it.
