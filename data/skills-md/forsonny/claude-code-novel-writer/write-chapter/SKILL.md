---
name: write-chapter
description: Draft the next chapter or a specified chapter from the accepted outline while preserving manuscript continuity, character knowledge, and established voice.
---

# Write Chapter

Use any chapter number or constraints supplied with the invocation.

1. Resolve the repository root and run `./sync-state.sh --quiet`.
2. Determine the target chapter from the invocation, outline, and tracking state.
3. Refuse to overwrite substantial existing prose unless the request clearly asks for revision.
4. Read the relevant outline beat, previous chapter, directly relevant earlier chapters, character state, world state, and continuity notes.
5. Read `.agents/roles/chapter-writer.md`.
6. If the harness exposes a named `chapter-writer` specialist, delegate the complete bounded draft to it. Otherwise perform that role directly.
7. Write the chapter to `manuscript/chapters/chapter-N.md`, preserving repository formatting conventions.
8. Run `automation/quality-check.sh manuscript/chapters/chapter-N.md` for mechanical signals unless a lifecycle hook already did so.
9. Run `./sync-state.sh`.
10. Report the file, approximate word count, story-state changes, continuity facts, and any downstream concern.

Prefer one coherent chapter over many disconnected scene fragments unless there is a concrete reason to split the work.
