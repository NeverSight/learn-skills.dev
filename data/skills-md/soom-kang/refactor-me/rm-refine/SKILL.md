---
name: rm-refine
license: MIT
description: Refine existing code or development documentation within an authorized scope. Use for behavior-preserving refactors or explicit updates to technical artifacts; exclude feature changes, unrelated cleanup, and general prose rewriting.
---

# Bounded refinement

Improve the specified artifact while preserving its required behavior or meaning. A justified no-op is a successful outcome.

## Inputs and mode

- Required: target artifact and requested improvement.
- Optional: allowed paths, forbidden changes, behavior contracts, canonical sources, and validation commands.
- Default: use the requested artifact as the boundary, preserve existing contracts, and follow local repository instructions.

For code, use behavior-preserving mode. For development documentation, use documentation mode only when that artifact is explicitly in scope. If the request does not establish which behavior or meaning may change, resolve that question before dependent edits. Neither mode authorizes a feature change.

## Procedure

1. Read the target, relevant project instructions, and current changes. Identify the user's existing edits and the smallest authorized scope. Inspect adjacent material when necessary; reading it does not authorize changing it.
2. Establish what must remain true. In code, include observable returns, errors, side effects, ordering, public interfaces, and persisted shapes relevant to this change. In documentation, identify requirements, decisions, uncertainty, provenance, and audience that must be preserved.
3. Choose the smallest revision that achieves the requested improvement. Prefer existing structure and conventions. Do not add unrelated renames, formatting, abstractions, or synchronization of neighboring files. Within the authorized scope only, these are removable when the request covers them:
   - scaffolding left behind by an earlier iteration
   - a superseded delta or an old-versus-new comparison
   - process narration already stated elsewhere in the same artifact
   - content the artifact itself marks as retired
   - history specific enough that it will not apply again
4. Apply authorized edits without replacing unrelated user changes. For code, use language-aware edits when structural complexity requires them; do not invent unavailable tooling. For documentation, verify changed claims against the applicable source, preserve unresolved decisions rather than rewriting them as facts, and where the format supports it: fold a parenthetical that interrupts its own sentence into a clause or cut it, rejoin a hard break that splits one sentence, and turn a bare textual reference to another section or file into something the reader can actually follow. Formatted blocks — code, tabular data, quotations — stay exactly as authored.
5. Run the smallest meaningful existing checks for the change. Inspect the resulting diff, changed references, and relevant behavior. Record failed or unavailable checks and their impact; do not edit tests merely to hide changed behavior.

## Rules

- **Assert the target, then edit it.** Confirm each replacement target exists before writing and report a MISS rather than finishing on a silent no-op; act on one occurrence at a time instead of sweeping the file; leave every byte outside the edit exactly as found, non-ASCII characters and line endings included; drive a large structural move with a language-aware tool or a script rather than a text substitution.
- **Repair from the source, not from the damaged surface.** Check a changed claim against the canonical or governing artifact; do not reconstruct it from the text you are fixing.
- **State what is true now.** Unless the artifact is a changelog, the result carries no old-and-new trace of the edit and no note that an edit occurred.
- **Fix machine-clear residue; leave judgment to the caller.** Never auto-resolve an ambiguity, and never correct a deliberate look-alike: a value, comment, or section the user authored or marked stays exactly as written even when it matches a removal category above.
- **Prefer an existing section to a new one, and add no files** unless the request asks for them.
- **Authorization covers this artifact and this improvement.** It does not extend to committing, pushing, deploying, changing secrets, or modifying production settings. In a read-only or planning context, return the proposed revision without editing.

## Output and stopping

Follow the caller's schema. Otherwise report the actual change, why it meets the request, validation performed, and remaining limitations. If no useful improvement exists, report the no-op without creating changes.

Stop when the revision is verified within scope, or when it requires unauthorized files, a behavior change, unavailable evidence, or a separate approval. Describe any partial edits accurately and preserve user work; do not use blanket resets or silently expand the scope. Existing authorization is sufficient for work it already covers.

## Examples

- Normal: extract a helper inside an allowed module while preserving error behavior and call order; run the module's existing checks and inspect the focused diff.
- Edge: a cleanup would also require changing a public response field or an excluded guide. Stop that part and explain the required scope decision instead of treating it as incidental cleanup.

## Completion check

The diff serves the stated purpose, user edits remain intact, behavior or documentation meaning is preserved as required, and validation claims match executed checks.
