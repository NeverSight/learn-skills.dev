---
name: release-stable
description: Publish the next stable release by the project's own stable process — check that the main branch is green, choose the version and write its notes (through write-release-notes), publish whatever platforms still go out by hand, then push the version tag once the user has the notes, watch the build and check what it published and which release is marked latest. Use when the user asks to release, cut, ship or publish a stable version, push a version tag, or invokes /release-stable. Stops at a red main branch or a missing instruction instead of guessing; never moves, deletes or force-pushes a version tag.
---

# Release a stable version

A stable release is the one most people install, and it is permanent. A
version tag is never moved or deleted once pushed, the release's notes are
public at once, and installed builds update to it on their own. A mistake
is fixed with the next version, not by changing this one. So most of the
work is checks, done before anything leaves the machine.

## Find the project's stable instructions

Before anything else, find where the project describes a stable release:

- the workflow a version tag triggers (for example
  `.github/workflows/stable.yml`). Its header comment usually names the
  steps, the tag pattern, and which platforms it builds.
- the release descriptors' README (for example `releases/README.md`), and
  the design page it points to.
- the release-writing instructions (`releases/WRITING.md`), which choose the
  version.
- the release runbook, for any platform that is **still published by
  hand**. A project moving its releases to CI often publishes some
  platforms with a local command first, and that command may write the
  notes and create the tag itself.

They settle the tag pattern, where the notes live and how they are named,
which platforms CI builds, and the order of the hand-published and
CI-built halves. **If there are none, stop and ask** how stable releases
are made. Do not invent a tag, a version or an order.

## Check before writing anything

1. **The tree is what will ship.** Fetch with tags, then confirm you are on
   the main branch, level with the remote and clean. Main moves while you
   work, so check again just before tagging. CI builds the tagged commit's
   own workflow file: a workflow added after that commit does not run for
   it.
2. **Main is green on the commit you will tag.** Read the CI run for that
   exact commit. If a job failed, **stop**: name each failing job and its
   first real error, and ask whether to fix main first. Recommend fixing it,
   because a stable release cannot be replaced afterwards. If jobs are still
   running, say which, and ask whether to wait.
3. **The version is free.** No tag of that name exists locally or on the
   remote (`git ls-remote --tags origin v<version>`), and no release of
   that name exists (`gh release view v<version>` fails). A local tag that
   was never pushed is worth a sentence: it may be left over from an
   earlier hand publish, and it must point at the commit you mean to ship.
4. **There is something to release.** `git log --no-merges <last stable
   tag or commit>..HEAD` is not empty. Take the last stable commit from
   where the instructions say it is published, not from a local tag.
5. **The publishing side is set up.** The workflow's environment and the
   secrets it names exist (`gh api repos/<owner>/<repo>/environments`, and
   the environment's secrets list). A tag pushed before they exist starts a
   run that fails, and the tag cannot be taken back.

## Write the notes

Run **write-release-notes** for the stable channel. It chooses the version
by the project's rules and writes the descriptor the instructions name
(usually `releases/<version>.toml`). Beyond those rules:

- **One descriptor for every platform of the version.** The hand-published
  platforms and the CI-built ones show the same notes, so write them once.
- **Only what this release has, on each platform.** Before you describe a
  feature, check that it exists on the platforms the release carries. A
  `cfg(windows)` or a missing platform module is the usual tell. A
  platform-only change belongs under that platform's heading.
- **Full commit messages, not one-liners**:
  `git log --no-merges --format='%h %s%n%b' <last stable>..HEAD`, then the
  diffs behind anything the messages leave unclear.
- **Validate it.** It parses, every required field is there and not blank,
  and it has nothing the publisher refuses, such as images or HTML.

## Show, then publish

Show the user the version, the notes and the commit that will be tagged.
Publish only when the user has asked for this release, and has either seen
these notes or said to publish without reviewing them.

1. **Commit only the descriptor** on the main branch, in the style of
   earlier release commits (`git log --oneline -- releases/`), and push the
   branch. That is an ordinary fast-forward push, never a force.
2. **The hand-published platforms first**, if any, with the project's own
   command, run by the user where it needs their credentials or their
   machine (for example a Mac for a signed macOS build). Give the exact
   command. If that command creates the version tag, let it, and then
   check that the tag points at the descriptor's commit.
3. **Check again** that main has not moved and is still green. Then tag
   that commit, if it is not tagged already, and push **only that tag**:
   `git push origin v<version>`. Never `--force` and never `--tags`, which
   would also push every stray local tag.

## Watch and verify

1. Find the run the tag push started (`gh run list --workflow <file>`) and
   watch it (`gh run watch <id>`).
2. When it succeeds, check the release (`gh release view v<version>`). It
   is not a pre-release. It carries every CI-built platform's package,
   signature and update manifest. Its text is the notes.
3. **Check what "latest" points at.** Installed builds often read their
   update feed through the latest-release alias, so check that it resolves
   to the newest stable (`gh release view --json tagName`, with no tag).
   A patch on an older line must not be latest. If the wrong release is
   marked, say so before changing it: moving it changes what every
   installed build is offered.
4. Fetch the update manifest through the alias the app reads, and check
   that it names this version and a package that downloads.
5. Report the run's and the release's links, the version and build number,
   what the hand-published half produced, and anything a check found.

## If the build fails

The tag cannot move, so a failure is fixed without one.

- **A transient failure** (a runner fault, a network timeout): re-run the
  failed jobs (`gh run rerun <id> --failed`). The same tag and notes are
  built again, and the publish step must replace only that run's own
  files.
- **A missing secret or environment**: the user creates it, then the
  failed jobs are re-run. No new tag is needed.
- **A failure that needs a code fix**: this version cannot be built from
  this tag. Recommend the next patch version, with its own descriptor, from
  the fixed commit. Ask the user about the hand-published half of the
  failed version: if it is already out, the platforms differ until the
  patch ships, and the notes of the patch should say what it fixes.
