---
name: ot-handoff
description: Capture portable working context directly under on-track/handoffs. Use when switching harness or model, ending a session, or the user says "handoff", "compact this", or "pick this up later".
---

1. Read `on-track/INDEX.md` and the current conversation. Identify the active objective, verified state, unresolved decisions, and relevant durable artifacts.
2. Preserve every active user instruction exactly under `Active user instructions, verbatim`. Omit only secrets or unnecessary personal data and disclose the omission. Do not paraphrase instructions whose wording constrains the next agent.
3. Separate verified completed work from next actions. List next actions in one ordered `## Next actions` list whose first item is the first concrete step. Record blockers, risks, relevant paths, and observed command results without presenting inference as observation.
4. Reference specs, research, refs, decisions, assessments, diffs, and other durable documents by path instead of duplicating their contents.
5. Compute the final path `on-track/handoffs/YYYY-MM-DD-HHmmssZ-<slug>.md` from the current UTC instant. Before writing, check that this path exists in neither the active directory nor `on-track/handoffs/archive/`; stop and report a collision instead of overwriting.
6. Write the final document directly to that path from `./assets/handoff.md`. Set `captured: YYYY-MM-DDTHH:MM:SSZ` to the same UTC instant as the filename. Do not use a lifecycle `status`.
7. Validate the new handoff before touching any other handoff: every heading in `./assets/handoff.md` is present, `captured` has the `YYYY-MM-DDTHH:MM:SSZ` form and names the filename instant, and the frontmatter fits the canonical subset (line 1 is `---`, a later `---` line closes it, each non-blank line between them is one `key: value` field, no key repeats). On failure, fix the new handoff or stop and report the failure; archive nothing.
8. Only after step 7 passes, order active handoffs by their `captured` instant, not filename text. Keep the three newest in `on-track/handoffs/`. Move each older handoff to `on-track/handoffs/archive/` only when its destination does not already exist; stop and report any collision without overwriting.
9. Only after archiving, run `../ot-init/scripts/on-track-index.sh <target>` using the owner copy and report any validation error.

Path resolution: `./` paths and `../ot-*` sibling paths resolve from this skill's installed directory, and `on-track/` paths resolve from the target repository root.

The owner index script is local Bash with no network calls: it reads frontmatter under `on-track/` and writes only `on-track/INDEX.md`, or exits with validation errors and leaves it unchanged. When it prints a `WARN:` line, relay it to the user in one sentence at the end of your report; a warning never blocks the stage.
