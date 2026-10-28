---
name: ship
description: Ship the current branch — evaluate its SemVer release impact, refresh the docs, write the changelog entry for the version this merge will mint, file its human follow-ups, run the fast checks, push, and open or update the PR. Use when a feature branch is ready for review, or when the user says "ship it", "open a PR", or "push this".
metadata:
  settings: workspace issue-tracker human-follow-up releases ship
---

# Ship

Take the current branch from "code is done" to "PR is open and green-able", with a changelog that
names the version this merge will actually create.

**Announce at start:** "I'm using the ship skill to open a PR for this branch."

Run shell snippets in bash (Git Bash on Windows). Where `gh` is unavailable, use the equivalent
GitHub MCP operation: a missing CLI changes the interface, not the step or its completion
criterion.

`ship` stops at "PR open". It never merges, never pushes to `main`, never force-pushes, and never
runs the full test suites: CI owns them, and running them here makes the skill slow.

## 0. Settings

This skill reads `docs/agents/workspace.md`, `docs/agents/issue-tracker.md`,
`docs/agents/human-follow-up.md`, `docs/agents/releases.md` and `docs/agents/ship.md`. Follow
`.agents/skills/ship/settings/README.md` to read them and complete any that are missing; the
definitions sit beside it. Resolve each `discover:` value once, here, and
reuse it below.

With `Scheme: none`, skip every step marked **(release)**.

## 1. Preconditions — stop if any fail

- **Not on `main`.** Work happens on a branch. On `main`, stop and offer to create one named by the
  `Issue link` branch pattern (`<type>/<slug>` when it is `none`).
- **Clean tree.** `git status --porcelain` prints nothing but the settings files step 0 just wrote,
  which go into this run's commit. Otherwise stop and ask whether to commit what is there; never
  commit it silently. Once answered, restart from this step. Every change staged later was then
  made by this run.
- **GitHub reachable.** `gh auth status` succeeds, or GitHub MCP can reach this repository.
- **Companion in step.** When the `Private companion` is set and its checkout exists, run the
  `Workspace status command`: the companion must be clean and neither ahead of nor behind its
  upstream. An absent checkout is a valid state; report it.
- **Up to date with `main`.**

  ```bash
  git fetch -q --tags origin
  git merge-base --is-ancestor origin/main HEAD && echo current || echo behind
  ```

  When behind, offer to `git merge origin/main` now, and resolve conflicts with the user. Never
  rebase a pushed branch.

Use `origin/main` throughout, never local `main`: a stale local `main` silently widens the diff to
work already merged, and a clone that fetched only this branch has none.

## 2. Evaluate the release impact (release)

Read the whole branch, not its latest commit:

```bash
base="$(git merge-base origin/main HEAD)"
git diff --stat "$base"..HEAD
git log --format='%s%n%b' "$base"..HEAD
git diff "$base"..HEAD
```

The stat and the log are an index. Read the diff, and the tests and docs it touches, before
deciding. Classify the impact to **this project**, highest level present:

- **Major** — an existing public behavior, API, URL, persisted-data shape, configuration,
  deployment contract or established user workflow becomes incompatible, and its users must
  migrate. On a `0.y` line, an incompatible change is minor unless the branch deliberately cuts
  `1.0.0`.
- **Minor** — a backwards-compatible capability or a material expansion of behavior, or a
  deliberate platform or toolchain generation change that raises the supported baseline.
- **Build** — fixes (security fixes included), dependency maintenance, refactors, tests, docs,
  tooling: nothing that adds capability or raises a baseline.

Judge this project's contracts, not a dependency's version number. Release metadata and generated
mirrors are not evidence. With `Scheme: per-merge`, the cumulative content of `Unreleased` counts
too. A level the user asked for is still evaluated; when the evaluation differs, show both and ask.

Record `Release level: <major|minor|build> — <one-sentence rationale>`. Steps 9 and 10 use that
exact line.

**Apply it.** The baseline is the higher of the newest `v*` tag (ignoring the `Skipped tags`
**Ignore** patterns) and the `Version file` on `origin/main` (`git show "origin/main:<file>"`).

- **Build** — the `Version file` stays at its `origin/main` value. Restore it if the branch moved it
  without release intent.
- **Minor** — the target line is `<major>.<minor + 1>.0` of the baseline.
- **Major** — the target line is `<major + 1>.0.0`.

For major or minor, follow `Ask before bumping` first, then run `Bump command` with the exact
target, so a re-run lands on the same value instead of advancing twice. Check that the version file
and any lockfile beside it agree. A branch that already carries the target keeps it; a branch that
carries a different line was bumped on purpose: ask before replacing it.

## 3. Compute the target version (release)

- **`per-merge`** — first confirm the newest merge on `origin/main` is tagged:

  ```bash
  git tag --points-at origin/main -l 'v*'
  ```

  Empty output means the tag workflow has not finished for a merge that just landed, and the next
  version would repeat a taken number. Wait for the workflow, fetch tags again, and re-check; if it
  stays untagged after the workflow finished, ask the user. Then run `Next-version command`. It
  prints a bare SemVer and is the single source of truth: never compute the build number yourself.

  Check whether another open PR already claims that version:

  ```bash
  gh pr list --state open --json number,headRefName --jq '.[] | "\(.number) \(.headRefName)"'
  gh pr diff <number> -- CHANGELOG.md | grep '^+## \['
  ```

  If one does, name it in the report: whichever merges second renumbers on its next `ship`.
- **`cut-on-line`** — a build has no exact target: the next tag assigns it, whether a workflow tags
  each merge or a maintainer tags a release, and another merge can land first. A confirmed major or
  minor's target is the new line from step 2.

## 4. Backfill skipped tags (release)

Only with `Scheme: per-merge` and `Skipped tags: backfill`. List released versions with no section.
Run it exactly; tags print as `v1.1.5` and sections as `1.1.5`, so comparing raw lists by eye
reports every tag as missing:

```bash
comm -23 \
  <(git tag -l 'v*' | sed -nE 's/^v([0-9]+\.[0-9]+\.[0-9]+)$/\1/p' | sort) \
  <(sed -nE 's/^## \[([0-9]+\.[0-9]+\.[0-9]+)\].*/\1/p' CHANGELOG.md | sort)
```

Drop versions matching the **Ignore** patterns. Each one left is a merge that wrote no section — a
dependency bot's PR, or one opened in the web UI. Add a dated section for it in place, newest
first. With `version` set to each, read the tag; it is the merge commit, so the merged branch is its
second parent:

```bash
git log -1 --format='%cs' "v$version"                  # the section's date
git log --format='%s%n%b' "v$version^1..v$version^2"   # what landed
git diff "v$version^1" "v$version" --stat              # manifests and lockfiles it changed
git log -1 --format=%an "v$version^2"                  # dependabot[bot] for a bot PR
```

Keep it factual: name the packages and versions, and call a lockfile-only change transitive.
Attribute to a bot only when the second parent's author is the bot: the merge commit's author is
whoever clicked Merge. When `^2` does not exist (a squash or fast-forward), read the tag's own
commit.

With `Skipped tags: roll up`, invent no section per skipped tag; their changes join the next section
written.

## 5. Refresh the docs

Run the `docs-updater` skill in `fix` mode, scoped to this branch's diff, not a full audit — in a
subagent where the harness has one, told to follow `.agents/skills/docs-updater/SKILL.md`;
otherwise follow it yourself. A subagent cannot ask the user, so complete its settings first, here,
by following its step 0.

```bash
range="$(git merge-base origin/main HEAD)..HEAD"
```

Tell it what changed and why, that it was invoked by `ship` on an unmerged branch, and that this
skill writes the changelog and the `Version file`. It leaves its edits uncommitted and returns the
human actions it found for step 6, and any wiki search it owes after the merge (the `Follow-up
wiki`, or a `Doc map` item in a wiki).
Companion edits are committed there as its own repository, never in this one: with `Companion
commit policy` `commit` or `ship`, commit and push them; with `ask`, show the diff and ask first.
Run its **Before committing** checks either way.

## 6. Human follow-ups

Run the `## Procedure` in `.agents/skills/ship/settings/human-follow-up.md` for every required human
action this branch leaves, before the PR opens, including those `docs-updater` returned. Reconcile
rather than duplicate; on a re-ship, reuse the records already made. A follow-up never lives only
in the changelog or the PR body. Its links go in the report and private records, never in the
public PR.

## 7. Write the changelog (release)

Write user-visible behavior and its consequences, derived from the diff — not a commit log. Use the
headings the file already uses (Keep a Changelog: `Added`, `Changed`, `Deprecated`, `Removed`,
`Fixed`, `Security`, plus any the file adds), one of each per section, and match its voice. Dates
are today's, `YYYY-MM-DD`.

**Idempotent.** List the sections this branch added:

```bash
git diff origin/main...HEAD -- CHANGELOG.md | grep '^+## \['
```

A section listed there is this branch's from an earlier `ship`: rewrite it in place, never stack a
second. Entries this branch added to `Unreleased` are rewritten the same way.

- **`per-merge`** — insert `## [<target>] - <date>` directly below `## [Unreleased]`, holding this
  branch's entries plus anything accumulated in `Unreleased`; reset `Unreleased` to the `Unreleased
  placeholder`. When the branch's section names an older version because another PR merged first,
  **renumber that section** to the target. Then merge `origin/main`: their section sits in the same
  place, so resolve `CHANGELOG.md` keeping both, newest version first, and go back to step 3 — their
  merge minted a tag, so the target moved again.
- **`cut-on-line`, build** — add the entries under `Unreleased`, replacing its placeholder. No dated
  section, no `Version file` edit.
- **`cut-on-line`, confirmed major or minor** — add the entries under `Unreleased`, move its whole
  content into `## [<target>] - <date>`, and restore the placeholder. When the cut is already there
  from an earlier `ship`, rewrite this branch's entries inside it; never leave them both above and
  below the cut.

**Reference links.** When the file ends in a link footer, keep it consistent in the pattern its
entries follow: `[Unreleased]` compares from the newest version to `HEAD`, and each new or
renumbered section — backfilled ones too — gets its own link, newest first.

Run `Changelog check`. A mismatch names the version the merge will really mint: redo this step with
it.

## 8. Fast checks — refuse to push if any fail

Run every `Fast checks` entry, in order, from its folder; skip a conditional entry only when none of
its paths changed (`git diff --name-only origin/main...HEAD`). They run after the doc and changelog
edits, because formatters and linters cover those files too.

If any is red, stop and report; do not push. Offer the entry's fix command. After a fix that writes
files, run the list again from the top: a generated mirror built from unformatted sources is stale
again once they are formatted. A check that cannot run here (a missing service, a missing secret) is
named in the report as left to CI.

Then run `Hook: before PR` from `docs/agents/ship.md`. Its findings go in the report and, where it
says, the PR body.

## 9. Commit, push, and open or update the PR

Commit only when `git status --porcelain` shows changes; a re-ship with nothing new makes no empty
commit. Staging everything is safe because step 1 proved the tree was clean, and the companion is
ignored, never staged:

```bash
git add -A
git commit -m "<Release commit message, with the real version>"
git push -u origin "$(git branch --show-current)"
```

A rejected push means the remote has commits this checkout lacks: stop and report. Never force-push.

```bash
gh pr list --head "$(git branch --show-current)" --state open --json number,url
```

- **No PR** → `gh pr create --base main`.
- **A PR exists** → `gh pr edit <number>` to refresh its body. Never open a second PR.

Write the body to a temporary file and pass `--body-file`. Fill the repository's PR template
(`.github/pull_request_template.md` or `PULL_REQUEST_TEMPLATE.md`) when there is one, from the
changelog entries and the diff. Include the `Release level:` line from step 2 and, with `per-merge`,
the version this merge will mint.

**Issue link**, when the setting is not `none`. The body opens with the link line, in the slot the
template leaves for it:

- Take `N` from the branch per its **Branch pattern**, and read the issue:
  `gh issue view <N> --json title,state,labels,body`.
- The finishing line (`Closes #N`) when this PR finishes the issue; the slice line (`Part of #N`)
  when it is one slice of a spec that stays open. Each finished issue gets its own keyword:
  GitHub links only the first issue in `Closes #1 and #2`.
- A branch with no number: the **Waiver line** when the user waived the flow; no link line for an
  **Exempt** kind.
- When the branch's number and the issue disagree, or finishing versus slice is unclear, ask before
  creating the PR. A refreshed body keeps its link line. A number in the title alone links nothing.

Warn, never block, when the PR opens with no link line and is not exempt, or when the `Board` is set
and the linked issue is not on it. An issue in the `Private issue repository` is never named in a
public PR body, commit message or public issue; it is closed by hand after the merge.

Nothing this step writes in public carries a private repository name, link, board number or
companion detail.

## 10. Report

- The PR URL and branch.
- The `Release level:` line and its evidence; the version this merge will mint (`per-merge`), the
  new line (a `cut-on-line` cut), or that the next tag assigns the build. Name a competing PR
  claiming the same version, and say the section is renumbered on a re-ship.
- What the docs refresh changed, the changelog entries written, and any sections backfilled. When
  docs-updater owes a wiki search after the merge, say so: the next `end-session` performs it.
- Human follow-ups: verified issue and wiki links, what is unpublished and why, or that none remain.
- Fast-check results, checks left to CI, `Hook: before PR` findings, and issue-link warnings.
- The companion: absent, or clean and in step, and any companion commit made. Never describe the
  unmerged PR as shipped there.
- Settings files written in step 0.

Say plainly that the full suites run in CI, not here: the branch is verified only as far as the fast
checks go.
