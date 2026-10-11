---
name: cloud-ship
description: >-
  Run one fire of a scheduled cloud routine: invoke `ship` unattended and relay
  its outcome. Composes `ship`. Use only from a cloud routine's prompt; a human
  runs `/ship`.
metadata:
  version: 0.2.1
---

# cloud-ship

One **fire**: one selected issue driven to one merge-ready PR, ending at the
merge gate with no human present. This skill adds the invocation and the relay,
nothing else.

## The fire

1. **Invoke `ship` unattended.** Call the Skill tool with skill `ship` and
   arguments `--unattended`, no issue number. Ship runs the whole unattended
   lane (`reference/unattended.md` in its own folder) and returns.
2. **Relay.** Report ship's step-5 result verbatim, prefixed with
   `cloud-ship <version>` (the `metadata.version` above): the PR link, where
   the merge summary is, and each reviewer's exit off its `Review` block
   (`reviewed`, `not reviewed: <reason>` or `not invoked: <primary>
   reviewed`), or the stop reason as ship named it.

## The one invariant

Hand the sandbox clone over untouched for `isolate --in-place` to branch, let
ship run every mechanic and write every claim, label, comment and hand-back,
and end the fire where ship returns.
