---
name: write-release-notes
description: Write the release descriptor and notes for the next release on a channel (stable, beta, nightly or whatever the project names), following the project's own release-writing instructions. Use when the user asks for release notes, a changelog entry, a release descriptor, or "the next nightly / beta / stable". Gathers what is published now and what this tree holds, lets the project's instructions choose the version and the format, writes the file, and never publishes.
---

# Release notes

The project owns the rules: how versions advance, where the published
manifests live, what the descriptor looks like and how its copy reads. This
skill only gathers the context and makes sure those rules are followed rather
than guessed.

## Find the instructions

Look for the project's release-writing instructions before anything else —
`releases/WRITING.md` first, then whatever `AGENTS.md`, `CONTRIBUTING.md` or a
`releases/README.md` points at. **If there are none, stop and ask** where
releases are described; do not invent a version scheme or a file format.

If the user named no channel and the instructions define more than one, ask
which. One question, with the channels as options.

## Gather the context

Collect these yourself unless the request already supplied them:

1. **What is published on each channel**, from wherever the instructions say
   the manifests live. Bypass caches the way they describe (a fresh query
   parameter is the usual one). A missing manifest means the channel was never
   published; a network failure is not the same thing — report it, do not
   treat it as an empty history.
2. **This tree**: `git rev-parse --short HEAD`, today's date in UTC
   (`date -u +%Y%m%d`), and `git status --porcelain`. A dirty tree is worth a
   sentence to the user, since a build from it would not match HEAD.
3. **What changed** since the published commit on that channel —
   `git log <published>..HEAD`, read for what a user would notice. Commit
   messages written for changelog readers (see `commit-changes`) are the
   source; the diff settles anything they leave unclear.

## Write it

Follow the instructions for version selection, the file name and the format
exactly. If the publisher supplied an exact descriptor path or version, use it
unchanged, even if the date or the manifests have moved since.

Write for the person installing the release: what they can now do, what was
fixed that they may have hit, what changed under them. Leave out internal
refactors unless they change something observable.

## Finish

Show the file and the version you chose, with the one line of reasoning
behind the version. Do not commit unless asked, and **never publish, tag or
push** — releasing is the user's step.
