---
name: init-pipeline
description: Set up a Java backend project created by /new-java-backend for plan-feature and build-feature, before any /speckit command runs - installs the spec-kit constitution, the traceability gate and the project rules, then runs specify init with its git extension disabled when installed. Invoke by name (/init-pipeline).
disable-model-invocation: true
---
# Init pipeline — a new Java backend, ready for `plan-feature` and `build-feature`

A project created by `/new-java-backend` (from `dulguun0225/skills`) has the template vendored into `backend/` and a root `CLAUDE.md` with its base-branch line, and nothing for spec-kit or this repo's pipeline. This skill installs the files under its `project/` directory and ends at the commit that follows `specify init`; no spec-kit command is part of it. Nothing in it is a decision.

## Precondition: `/new-java-backend` first

**Run this skill only in a project `/new-java-backend` created, before spec-kit has run there.** The script refuses, before writing anything: a skill install missing any file under `project/`; a directory that is not a git repository's root; a dirty tree; a project without `backend/scripts/wall.mjs` (a standalone service is not supported); a root `CLAUDE.md` without exactly one base-branch line in the form `` Base branch: `dev` ``, or naming `main`, `master` or `HEAD`; a root `CLAUDE.md` without the rule that a session runs `git pull --ff-only` before changing a file; a current branch other than the one that line names, or a detached HEAD; an existing `.claude/settings.json` that is not a JSON object.

If spec-kit ran first, the constitution in place is spec-kit's generic one and the script refuses it. Run the script again with `--replace-constitution`: it replaces the file with this skill's, and the replaced one stays in git history. Write no constitution text yourself.

## A service created before the pipeline moved out of the template

Such a service's `backend/scripts/wall.mjs` does not run `scripts/wall-checks.txt`; `backend/` still holds the old traceability gate (`scripts/check-traceability.mjs`, its self-test, `scripts/fixtures/traceability/`), or its `wall.mjs`, `CLAUDE.md`, `docs/GATES.md`, `README.md` or `scripts/init.mjs` still holds text about that gate, spec-kit or the constitution that only the template before the split carried; its root `CLAUDE.md` holds the pipeline text the template used to carry, does not name `scripts/wall-checks.txt`, or lacks the `git pull --ff-only` rule the appended section refers to. The script refuses all of these in one report before writing anything: for the wall it prints the two ways to bring `backend/` up to the template; for the old gate it lists each file to delete and each file that still describes it, with the text found; for the old text it names each paragraph or sentence and whether to remove or replace it; for the wall's project checks it prints the sentence the template's `backend/` bullet holds; for a missing rule it prints the paragraph to add. The check of the files that describe the old gate is skipped under `--update`.

The two ways to bring `backend/` up to the template:

- A service that took the template by `git subtree`: `git subtree pull --prefix backend https://github.com/dulguun0225/java-backend-template.git main --squash`.
- A service that copies template changes by hand: copy the template's changes since the last commit it copied, at least the `projectChecks()` step in `backend/scripts/wall.mjs` that replaces its two traceability steps, and the deletion of the old gate files. A subtree pull in such a service merges against the snapshot it first added and conflicts wherever the copies went in.

**The template update, the `CLAUDE.md` edit and this skill's setup go in one commit, pushed only when all three are in it**, so no commit has a wall without the gate. Commit the template update together with the `CLAUDE.md` edit, removing or replacing exactly the paragraphs the script names; after a subtree pull, which commits by itself, fold the edit into its commit with `git commit --amend --no-edit --all`. Write that commit's message for the whole change, this skill's part included (the root traceability gate with its self-test and fixtures, `scripts/wall-checks.txt`, the `CLAUDE.md` section): the amend keeps it. Run the script again with `--amend`, which refuses a `HEAD` any remote branch or any other local branch holds and makes the printed step amend that commit. This is the one case where you edit a file yourself.

## Run the script; write nothing

**Run [`scripts/init-pipeline.mjs`](scripts/init-pipeline.mjs) from the project root and write no file yourself.**

```
node <this skill dir>/scripts/init-pipeline.mjs
```

It copies every file under this skill's `project/` directory into the project root where the target does not exist, printing each file it skips; appends the pipeline section of `project/CLAUDE.section.md` to the root `CLAUDE.md` once, found by its heading; and appends `.claude/worktrees/` to `.gitignore` when absent. Two existing files are merged instead of skipped: `.claude/settings.json` gets `worktree.baseRef: "head"` when the key is missing, and one set to another value is left with a warning; `scripts/wall-checks.txt` gets whichever of its two lines is missing, the self-test before the gate. The files are the spec-kit constitution, `.claude/settings.json`, the traceability gate `scripts/check-traceability.mjs` with its self-test and fixtures, and `scripts/wall-checks.txt`, which makes `node backend/scripts/wall.mjs` run the self-test and then the gate. The script makes no commit.

## Then spec-kit, and one commit

**Run the lines the script prints**, in a POSIX shell (Git Bash on Windows). In a project without spec-kit they run `specify init --here --force --non-interactive --integration claude`, disable spec-kit's `git` extension when it is installed and enabled, and commit when there is something to commit, with a message that names the disabled extension only when these lines disabled it. `--force` lets `init` run in a non-empty directory and leaves the installed constitution, `CLAUDE.md`, `.claude/settings.json` and `.gitignore` as they are; `--integration claude` installs the `.claude/skills/speckit-*` skills. A project that already has spec-kit, found by `.specify/templates/`, gets the same lines without `init`, and without the disable when the extension is not installed or already disabled. If `specify` is not on `PATH`, stop and say so.

The `git` extension is installed when `.specify/extensions/git` exists, which happens when an older spec-kit installed it by default or `init` ran with `--extension git`; it counts as enabled unless `.specify/extensions/.registry` parses and marks it `enabled: false`. Its mandatory `before_specify` hook, `speckit.git.feature`, makes and checks out a `<NNN>-<name>` branch for every `/speckit-specify`, which moves the domain expert off the base branch; `specify extension disable git` marks the extension disabled in `.specify/extensions/.registry` and sets `enabled: false` on each of its hooks in `.specify/extensions.yml`.

## Updating the gate

**Run the script with `--update` when this skill's gate, self-test or fixtures changed**, after installing the new skill version: projects do not receive gate changes any other way. It writes `scripts/check-traceability.mjs` and `scripts/check-traceability.selftest.mjs` and replaces `scripts/fixtures/traceability/` whole, restoring any of them that was deleted, leaves every other file alone, and prints the commit line when anything changed. It has the same preconditions, and refuses a project where the gate was never installed: no gate file and no `scripts/wall-checks.txt` line naming it.

## The constitution; run no spec-kit command

**The skill ends at the commit: run no `/speckit-*` command after it, and name none as a next step in the closing report.** Do not run `/speckit-constitution`, and do not close with "Next step: run `/speckit-constitution`" even though spec-kit's banner lists it first and Article VII is empty.

The constitution at `.specify/memory/constitution.md` carries Articles I–VI — the platform, the gates as the review, explicit over silent, the committed contract, the repo shape, features as packages — each restating what the backend wall enforces. They are not re-planned per feature; a plan's Technical Context inherits them. Article VI names no package: it points at the package bullet in `backend/CLAUDE.md`. Article VII is an optional slot for rules the project turns out to need; it starts empty, nothing reads whether it is filled, and an empty one blocks nothing. It is amended later, as a commit with its reason, from the candidates a feature's plan produces.

The closing report says what ran and what failed, and stops there.
