---
name: make-evergreen-note
description: Ground a hunch into a Take — the user's own synthesized
  position, checked against existing notes it connects, then written as an
  evergreen note.
license: MIT
metadata:
  version: "1.10.0"
---

# Make-evergreen-note

Bold terms in this file are defined in `GLOSSARY.md`.

## Prerequisite

- MUST: `.slipbox/AGENTS.md` exists — confirms `setup-slipbox` ran to completion.
- NEVER: proceed without it. Stop and tell the user to run `setup-slipbox` first.
- NEVER: call bare `slipbox` — always `.slipbox/bin/slipbox`, which isn't guaranteed to be on `PATH`.

## Workflow

### Recoverable work

Start or resume work for the Evergreen Take `/using-slipbox` before gathering material. Use
activity `create` for a new Take and `revise` when an existing Evergreen note is
being revisited. Record the target path, target fingerprint (or `null` for a new
note), and all contributing note identities in `manifest.json`. Keep the complete
transient evidence in `synthesis-map.json`; never write the vault note while the
conversation is in progress. If interrupted, inspect the same `work_id`, verify
all fingerprints, and resume it rather than starting a second operation.

### 01 - Take the material

- **Named directly** → the user names specific existing notes to connect.
- **Bare, just a hunch** → search for anything related before starting; a
  hunch with nothing to check against is still a valid, complete session —
  see `/grounding`'s own handling of "neither present."
- **From the backlog** → query the pending queue. The installed
  `.slipbox/AGENTS.md` is the canonical reference for backlog semantics and
  lifecycle; inspect the pending Evergreen candidates `/using-slipbox`.

  Offer these; let the user choose one. This is how a flagged tension from
  `make-literature-note` — or a spawned Compass sub-idea from a prior
  `make-evergreen-note` session — eventually gets picked up and turned
  into a real Take.

### 02 - Ground it

Run a `/grounding` session, holding yourself to whatever notes are in
play — the user's own answers are free here: personal experience, memory,
anything not written down anywhere. That freedom is the entire point of a
Take. What must stay grounded is *your* side of the conversation — your
questions and reflections trace to what the retrieved notes actually
establish, never to your own training or memory (same rule as always, just
aimed at yourself instead of the user this time). This is the
Fidelity-direction parameter you supply to `/grounding` when the session
starts.

Orient the take with the Compass technique — reach for whichever direction
the conversation calls for, no fixed order. Compass's own
directions may recurse into fresh sub-ideas; an unpursued spawned sub-idea
gets recorded as an Evergreen candidate `/using-slipbox` (see Compass's own Guardrail).

`/grounding` hands back the confirmed Take, and — only if the user opted
in — a flagged tension. If a tension came back, preserve it in the map's
`tensions` array as `{ proposition, reason, origin_kind, origin_paths, status: "pending" }`,
then record the Evergreen candidate `/using-slipbox` before moving on to writing.
The candidate remains a staged side effect; do not publish it separately.

When notes participated, use `origin_kind: note-connection` with every exact retrieved
vault-relative path. For a bare hunch with no related notes, use
`origin_kind: standalone` and an empty `origin_paths` list. Never reconstruct paths from
configured folders, and never rewrite provenance when reading an existing candidate.

Before writing, run a purity check on the draft: test each sentence — is it
attributable to a single cited note's claim, unchanged? If yes for any
sentence, the conversation isn't done — keep sharpening until the Take
states something none of the individual notes said on their own.

### 03 - Write and stage publication

- Run `/write-checks` with `artifact-kind: note`, `note-type: evergreen`, and
  fields `type`, `created`, `derived-from`, and `updated-at`. `updated-at` uses
  `created` on a first write and the current time on a revision.
- Resolve the configured Evergreen path, filename casing, exact prefixed basename and
  link target, and clean/unprefixed H1. A display alias after `|` is clean when used.
  Re-read and fingerprint the target immediately before assembling
  the complete draft. Write that draft only to the work directory as `draft.md`,
  including a full replacement on `revise`.
- Validate the complete `draft.md` with `/write-checks`, then run the configured
  Evergreen note validator against the staged draft. A collision on `create`, a
  malformed H1/basename, or a failed check blocks staging.
- Put every cited note and its one-line reason in `synthesis-map.json`. Stage one
  `mutations.json` containing the note replacement and exactly one `ledger-events`
  mutation for `links.jsonl`; that mutation contains all `cites` events for this
  publication. If the material came from a backlog candidate, include its
  status, slug, note-path, and iteration update in the same staged mutations.
- For a first-write backlog slug change, stage a create-new-row operation and a
  tombstone/removal for the old slug in the same atomic backlog mutation. For a
  revision, stage the iteration and note-path update without creating a second
  candidate. The operation must preserve the candidate's verbatim proposition.
- Checkpoint work with the map and draft `/using-slipbox`, set the manifest to
  `ready-to-finalize`, and publish an artifact `/using-slipbox` once. This is the only
  publication call: note, citations, and backlog bookkeeping are one compensated
compare-and-swap transaction. Do not write the target or update the backlog separately.
- Whether a citation is also rendered as an inline `[[wikilink]]` in the
  note's prose depends on a two-part test: (a) it has this links row (the
  mechanical baseline — only cited notes are ever eligible), and (b) the
  specific sentence containing the mention is actually asserting something
  about that note's subject, not just incidentally naming it while the
  sentence is really about something else.
- If preflight or finalization fails, preserve the work directory and diagnostics.
  Recompute every mutation fingerprint before resuming; a concurrent target
  change blocks publication and never overwrites newer user content.

### 04 - Sign-off, shown to the user before finishing

- The title is a complete claim.
- Standalone-comprehensible by a future version of the user with no memory
  of this session.
- About one thing, entirely.
- Every link has a stated reason.
- The note answers, or spawns, a "so what / what's next."

These five criteria draw on Matuschak's and Ahrens' evergreen/permanent-note
theory, including a real tension between the two the skill deliberately
sides on — see `references/sign-off-theory.md` for the rationale.

## Done

The finalized work item has published the Take (or revision), every cited note
and reason, any flagged tension, and the related backlog bookkeeping together;
then tell the user the file path. A failed or repair-required work item is not
success.

If this session's material came from the evergreen backlog rather than
being freshly named or a bare hunch, close out the row it drew from:

Apply the installed `.slipbox/AGENTS.md` Backlog contract for lifecycle details,
including first-write slug renames, revisit iteration bumps, and the candidate's
note-path/updated-at bookkeeping. The note's own `updated-at` frontmatter field
was already set in the Write section above.

## References

| File | Purpose | Triggering condition |
|---|---|---|
| `references/sign-off-theory.md` | Matuschak's/Ahrens' evergreen/permanent-note theory the Sign-off criteria draw on, including the audience-tension the skill deliberately sides on | Rationale lookup when a Sign-off criterion needs justifying, not routine sign-off itself |
