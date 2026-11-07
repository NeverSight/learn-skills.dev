---
name: wkc-skills-release
description: Publish this collection's tags and GitHub Releases. Use when the maintainer asks to release merged work or resume an interrupted publication.
argument-hint: "[vX.Y.Z]"
disable-model-invocation: true
metadata:
  internal: true
---

# wkc-skills-release

- **What it does:** publishes lightweight tags and stable GitHub Releases for this collection by running `make release`, which runs `tools/release.mjs`.
- **When to use it:** explicit invocation by the maintainer, including recovery after a failed publication. Callers are people.
- **Dependencies:** a checkout of `wilsonkichoi/skills` on clean, synchronized `main`, with its `Makefile` and `tools/release.mjs`. Node.js, Git, an authenticated GitHub CLI (`gh`) with push access, and network access.
- **Input:** an optional exact `vX.Y.Z` tag. Without one, the target is `VERSION` on `main`; an existing tag resumes or confirms that release.
- **Output:** the script's verified result: a newly published or resumed release with its URL, an unchanged release, or a stop naming the failed check.

The script owns every release rule: the checkout and repository checks, the target, the notes from
`CHANGELOG.md`, the Latest decision, recovery, and verification. Do not reimplement, skip, or work
around any of them. Never change versions, create commits or pull requests, merge, or create, move,
delete, or edit a tag or release yourself.

## 1. Plan

From the repository root, run `make release`, adding `TAG=vX.Y.Z` when a tag was given. It writes
nothing. A stop is a result: report it with its reason, and change nothing to get past it unless the
maintainer asks.

## 2. Authorize

An unchanged release needs nothing more; report it. Otherwise show the whole plan: tag, commit,
state, preceding release, notes, Latest, and any warning.

Honor authorization the maintainer already gave for this tag and this commit. Otherwise end the turn
on a numbered question: publish this target (recommended), or stop. Creating a pull request,
approving a merge, or testing the skill does not authorize a release.

## 3. Publish

Run the publish command the plan printed, `make release TAG=<tag> PUBLISH=<full sha>`, unchanged.
The script reads everything again before each write and stops when the plan changed. A changed plan
needs a new authorization.

## 4. Report

Report the script's outcome: tag, commit, release URL, included versions, and Latest. On a stop or a
failure, report the failed check, the steps that completed, and the notes file the script kept.
Running the same publish command again resumes from matching state.
