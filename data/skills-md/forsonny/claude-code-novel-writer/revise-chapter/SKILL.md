---
name: revise-chapter
description: Substantively revise a specified chapter for structure, prose, character, pacing, or continuity while preserving its intended story function and established voice.
---

# Revise Chapter

Use the chapter number and revision goal supplied with the invocation.

1. Resolve the repository root and read the current chapter, its outline beat, adjacent chapters, and relevant canon.
2. Identify whether the requested change is structural, prose-level, character-level, continuity-related, or a combination.
3. For continuity-heavy work, read `.agents/roles/continuity-editor.md` and perform or delegate a focused audit first.
4. Read `.agents/roles/chapter-writer.md`.
5. If the harness exposes a named `chapter-writer` specialist, delegate the bounded prose revision to it. Otherwise perform that role directly.
6. Preserve good existing material. Do not rewrite the whole chapter merely to normalize style.
7. Run `automation/quality-check.sh <chapter-path>` for mechanical signals.
8. Run `./sync-state.sh`.
9. Recheck any continuity affected by substantive changes.
10. Report the revision's story effects and any downstream chapters or planning files that may need adjustment.
