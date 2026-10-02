---
name: apply-correction
description: Use this skill when revising persistent artifacts after factual corrections, review feedback, rejected alternatives, or changed requirements, especially when the final code comments, documentation, prose, or generated text should describe only the resulting current state. Preserve historical contrast when the artifact itself is a changelog, migration guide, comparison, rationale, or other history-sensitive document.
---

# Apply Correction

Treat correction history as reasoning input and the materialized current state as the semantic authority for the artifact. Resolve what is true now, then render from that state rather than asking the renderer to suppress obsolete content from the correction dialogue.

## Workflow

1. **Resolve the current state.** Determine the facts, behavior, interfaces, invariants, requirements, relationships, or intended wording that are authoritative now. When rendering will remain in the same model context, avoid restating discarded values more than necessary to resolve the correction. If an already-available isolated context will be used for rendering, scratch resolution may be more explicit because that scratch history will not cross the boundary.
2. **Materialize an authoritative state.** Convert the resolution into the smallest representation that preserves the semantics needed by the artifact. Represent the resulting state, not the conversation that produced it. Use a fact set, interface contract, behavior table, compact object, or other structured form when that reduces accidental carry-over.
3. **Switch generation authority.** Treat the materialized state as the semantic source of truth for the affected artifact. The correction dialogue may remain available as reasoning history, but it is no longer authoritative for generation. If the harness already provides a fresh model call, child agent, or equivalent isolated context, pass the materialized state plus only the source context needed to place the edit; isolation strengthens the boundary but is not required for the Skill to work.
4. **Render the artifact from the current state.** Write for a reader encountering the present system or fact directly. For comments, describe current behavior, intent, invariants, or useful rationale. For documentation and prose, state the resulting facts and relationships. Preserve unrelated surrounding material when editing an existing artifact.
5. **Review for correction residue.** Read the result as a reader who never saw the correction. Any remaining contrast, rejected alternative, previous interpretation, or conversational aside must contribute information that the artifact itself needs. When it exists only because of the editing history, reconstruct that passage from the authoritative current state and review again.

## Materializing current state

Treat the correction history like an event log and the authoritative state like a materialized view. The event log explains how the current state was reached; the artifact should normally be generated from the materialized view.

A useful test is: **would this representation make complete sense to someone who never saw the correction?** If so, it is suitable renderer input.

Do not over-compress the state. Preserve rationale, uncertainty, constraints, and other nuance when they are required to render the artifact faithfully. The goal is to remove obsolete authority, not useful semantics.

## Same-context and isolated rendering

Same-context rendering is a normal supported path. In that path, keep discarded content minimally stated during resolution, make the authoritative state explicit, then render from it and perform the residue review.

When an isolated renderer is already available, use it to strengthen the separation: resolve the correction, materialize the current state, cross the boundary, then render from only that state and the minimum source context. Do not require new runtime machinery solely for this Skill.

## History-sensitive artifacts

Some artifacts are specifically about change or contrast. Changelogs, migration guides, compatibility notes, comparisons, deprecation notices, and design rationales may need previous states or rejected alternatives because those facts are part of the subject.

In those cases, retain the history required by the reader and still apply the workflow to incidental correction residue. The criterion is whether the contrast describes the domain or merely records how the agent was corrected.

## Completion criteria

Finish when all of the following hold:

- The artifact agrees with the authoritative current state.
- A reader can understand the affected passage without access to the correction conversation.
- Remaining historical or contrastive language serves the artifact's subject.
- The renderer relies on the materialized current state rather than obsolete conversational state.
- Meaningful rationale, uncertainty, constraints, and terminology needed by the artifact are preserved.
