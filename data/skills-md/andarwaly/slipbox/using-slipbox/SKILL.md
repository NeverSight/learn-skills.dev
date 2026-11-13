---
name: using-slipbox
description: Coordinate recoverable Slipbox work through named actions and the vault's installed CLI; use when a specialist needs to start, checkpoint, publish, link, cache, recover, or finish an artifact.
license: MIT
metadata:
  version: "1.0.0"
---

# Using Slipbox

`using-slipbox` is the shared runtime engine. A specialist decides what an artifact means; this engine owns recoverable work, validation hand-offs, and bookkeeping; `.slipbox/bin/slipbox` performs atomic filesystem operations. Read `.slipbox/AGENTS.md` before acting and treat it as the vault's runtime contract.

Caller skills state the natural imperative action and append `/using-slipbox`.
Write “Record the link `/using-slipbox`,” never “Run `/using-slipbox`” or
“record the link through `/using-slipbox`.”

## Start or resume work

- **Trigger:** An artifact operation may be interrupted or an existing work item must continue.
- **Inputs:** Artifact kind, activity, source/target identity, and any known affected paths.
- **Guarantee:** Work is isolated under `.slipbox/work/`, inspectable, and resumed only after identity/fingerprint checks.
- **Reference:** `references/work-lifecycle.md`.

## Checkpoint work

- **Trigger:** A recoverable operation reaches a meaningful boundary or needs to pause.
- **Inputs:** Work identity, current status, and updated source/target state.
- **Guarantee:** The manifest records progress without publishing partial artifacts.
- **Reference:** `references/work-lifecycle.md`.

## Publish an artifact

- **Trigger:** A specialist has an approved complete artifact ready for disk.
- **Inputs:** Work identity, artifact kind, exact path/content, and required validation context.
- **Guarantee:** `/write-checks` passes before the CLI atomically publishes; collisions and changed inputs stop the operation.
- **Reference:** `references/work-lifecycle.md`.

## Record an Evergreen candidate

- **Trigger:** The reader has approved a proposition for later Evergreen grounding.
- **Inputs:** Proposition verbatim, reason, origin kind, and origin paths.
- **Guarantee:** The proposition is recorded without reinterpretation and remains recoverable until discussed.
- **Reference:** `references/evergreen-candidates.md`.

## Record a link

- **Trigger:** A specialist has confirmed a mechanical relationship between two notes.
- **Inputs:** Exact source and target link identities, relation, and provenance where available.
- **Guarantee:** The link is appended to the ledger atomically and can be found later.
- **Reference:** `references/link-ledger.md`.

## Remove a link

- **Trigger:** A previously recorded link is confirmed invalid or should no longer resolve.
- **Inputs:** Exact link identity and removal reason/provenance.
- **Guarantee:** Removal is represented as a tombstone; history is not silently rewritten.
- **Reference:** `references/link-ledger.md`.

## Store source analysis

- **Trigger:** Analysis of a frozen Resource is complete and eligible for cache storage.
- **Inputs:** Resource identity/fingerprint, map payload, contract and producer versions, known paths, and persistence policy.
- **Guarantee:** The source map is keyed to the Resource fingerprint and never masquerades as note content.
- **Reference:** `references/source-map-cache.md`.

## Inspect source analysis

- **Trigger:** A specialist needs to read existing source-map state before deciding whether to reuse it.
- **Inputs:** Resource identity or fingerprint and requested output format.
- **Guarantee:** Returned metadata exposes compatibility and provenance; it does not mutate the cache.
- **Reference:** `references/source-map-cache.md`.

## Refresh source analysis

- **Trigger:** A map is missing, incompatible, stale by policy, or explicitly requested for refresh.
- **Inputs:** Resource identity, requested scope, and the user's cache persistence choice.
- **Guarantee:** Refresh is isolated from note-format migration and reports unresolved or orphaned entries.
- **Reference:** `references/source-map-cache.md`.

## Finish work with Git

- **Trigger:** The user authorizes finalization after artifact and bookkeeping checks pass.
- **Inputs:** Work identity, configured Git policy, commit style, and affected paths.
- **Guarantee:** Only the isolated artifact/index paths are staged; failed commits remain recoverable.
- **Reference:** `references/git-finalization.md`.

## Recover failed work

- **Trigger:** A command, validation gate, publication, or commit fails.
- **Inputs:** Work identity, failure JSON, and current on-disk fingerprints.
- **Guarantee:** The engine preserves evidence, distinguishes retryable from repair-required states, and never claims success.
- **Reference:** `references/work-lifecycle.md`.

## Discard work

- **Trigger:** The user explicitly abandons a work item.
- **Inputs:** Work identity and explicit discard confirmation.
- **Guarantee:** Only the selected local work directory is removed; published artifacts and ledgers remain untouched.
- **Reference:** `references/work-lifecycle.md`.

## Responsibility boundary

Specialist → `/using-slipbox` → `.slipbox/bin/slipbox`. The specialist owns semantic decisions and conversation. This engine routes the named action, invokes `/write-checks` where required, and supplies complete inputs. The CLI owns schemas, path safety, atomic writes, compare-and-swap, cache mechanics, tombstones, and Git isolation. Exact command syntax and flags belong in the progressive references and CLI help, not in each action above.
