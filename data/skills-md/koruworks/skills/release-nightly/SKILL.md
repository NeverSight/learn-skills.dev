---
name: release-nightly
description: Publish the next nightly build by the project's own nightly process — check that the main branch is green and the nightly tag is current, write the one notes file the build needs (through write-release-notes), commit it, move and push the tag once the user has the notes, then watch the build and check what it published. Use when the user asks to release, cut, publish or update the nightly, to move or update the nightly tag, or invokes /release-nightly. Stops at a red main branch or a missing instruction instead of guessing; never force-pushes anything but the nightly tag.
---

# Release a nightly

A nightly is cheap to make and impossible to take back: its notes are public
the moment the tag moves, and installed builds update to it on their own. So
the work is mostly checks, done before anything leaves the machine.

## Find the project's nightly instructions

Before anything else, find where the project describes its nightly:

- the workflow the tag triggers (for example `.github/workflows/nightly.yml`;
  its header comment usually names the steps),
- the notes folder's README (for example `releases/nightly/README.md`),
- the release-writing instructions' nightly section (`releases/WRITING.md`).

They settle the tag's name, where the notes live and what they are named, how
the build picks the notes, and which platforms the build makes. **If there are
none, stop and ask** how nightlies are released; do not invent a tag or a
notes format.

## Check before writing anything

1. **The tag is current.** Fetch it from the remote with force
   (`git fetch origin --force tag nightly`). A local tag left from an older
   checkout gives the wrong baseline, and the notes then describe the wrong
   commits.
2. **The tree is what will ship.** Fetch, then confirm you are on the main
   branch, level with the remote and clean. Main moves while you work, since
   other people merge, so check again just before tagging. A submodule
   pointer that differs from its checkout does not change a build that does
   not check submodules out, but say so.
3. **Main is green on the commit you will tag.** Read the CI run for that
   exact commit. The nightly workflow usually runs no tests or lints, so CI
   is the only check the build gets. If a job failed, **stop**: name each
   failing job and its first real error, recommend fixing main first, and
   ask whether to fix it first or release anyway. If jobs are still running,
   say which, and ask whether to wait.
4. **There is something to release.** `git log --no-merges <tag>..HEAD` is
   not empty.
5. **The last nightly worked.** Check the nightly workflow's recent runs. A
   failed run that left the tag on an unpublished commit changes the next
   step (see "If the build fails").

## Write the notes

Run **write-release-notes** for the nightly channel, against the project's
nightly notes instructions. What it needs, beyond those instructions:

- **The exact file.** Name it as the notes README says, usually the UTC date,
  with a suffix for a second build that day. The build takes exactly one
  notes file added since the tag's last position, so check that this range
  adds no other.
- **Full commit messages, not one-liners.** `git log --no-merges
  --format='%h %s%n%b' <tag>..HEAD`, then the diffs behind anything the
  messages leave unclear.
- **Only what this build has.** Read which platforms the workflow builds.
  Before you describe a feature, check it exists on those platforms (a
  `cfg(windows)` or a missing platform module is the usual tell). A
  platform-only change belongs under that platform's heading, or nowhere.
- **The project's drafting command may call an agent.** If you are that
  agent, write the file yourself from the same commit range instead of
  starting another one.
- **Validate it.** It parses, every required field is there and not blank,
  and it has nothing the publisher refuses, such as images or HTML.

## Show, then publish

Show the user the notes and the commit that will be tagged. Publish only
when the user has asked for this release, and has either seen these notes
or said to publish without reviewing them. A published notes file is never
edited afterwards: it is the archive.

1. Commit only the notes file on the main branch, in the style of earlier
   notes commits (`git log --oneline -- <notes folder>`), and push the
   branch. That is an ordinary fast-forward push, never a force.
2. Check again that main has not moved and is still green, then move the
   tag to that commit and push it with force:
   `git tag -f nightly && git push -f origin nightly`. The force is right
   for a rolling tag, and only for that tag.

## Watch and verify

1. Find the run the tag push started (`gh run list --workflow <file>`) and
   watch it (`gh run watch <id>`). A run already in progress makes this one
   wait.
2. When it succeeds, check the release itself (`gh release view nightly`):
   it is still a pre-release, it carries this build's package, signature and
   update manifest and nothing older, and its text is the new notes.
3. Report the run's and the release's links, the version or build number,
   and anything a check found.

## If the build fails

The release page keeps the previous build when the workflow publishes in
the safe order (new package, then manifest, then deletions). Read the
failing step and report it.

- **A transient failure** (a runner fault, a network timeout): re-run the
  failed run (`gh run rerun <id> --failed`). The tag has not moved, so the
  run takes the same notes.
- **A failure that needs a code fix**: ask the user before moving the tag
  again. The build picks notes from the commits between the tag's previous
  position and its new one, so a tag moved from the failed commit to the fix
  finds no new notes and stops. Recommend a choice for the user to make:
  a second notes file for the fixed build, or moving the tag back to the
  last published commit first (that run fails before building, by design)
  and then to the fix.
