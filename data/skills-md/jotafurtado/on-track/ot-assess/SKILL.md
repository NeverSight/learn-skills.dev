---
name: ot-assess
description: Produce an evidence-backed internal assessment of a project, feature, or idea. Use when the user asks to assess, evaluate, audit, or review project completeness or fitness before creating an intent.
---

1. Read `on-track/INDEX.md` first. Freeze the requested target and scope. Assessment is read-only toward the assessed subject: inspect files, history, commands, and observed behavior, but do not modify the subject while gathering evidence.
2. State concrete criteria before reaching a conclusion. Do not require a generic numeric scorecard.
3. Gather evidence for and against the likely conclusion. Cite repository paths, durable artifacts, and observed command results precisely. Separate observed facts from inference.
4. Record material counterevidence under `Evidence against conclusion`. State unavailable evidence, uncertainty, evaluator limitations, and scope limits under `Limitations`.
5. Produce a defensible conclusion and concrete recommendations. Each finding states the problem, its evidence, its consequence, and the recommendation, and any priority follows from the stated consequence. Recommendations are inputs for later work, not implementation performed by this skill.
6. Record the evaluator as the provider and model when known, or the available stable agent identity otherwise. If assessment is delegated, record the delegated evaluator rather than the coordinating agent. Set `tracks` to the IDs of the tracks the assessment evaluates, or `[]` when it evaluates none.
7. Write exactly one file to `on-track/assessments/<YYYY-MM-DD>-<slug>.md` from `./assets/assessment.md`. Use the local calendar date, a descriptive kebab-case slug, and no lifecycle `status` field. When the target path already exists, rewrite it only when the user asked to redo that assessment; otherwise choose a distinct slug. Never overwrite an existing assessment file silently.
8. Run `../ot-init/scripts/on-track-index.sh <target>` using the owner copy and report any validation error.
9. When invoked by another skill as an auxiliary step, write the artifact, regenerate the index, and return conclusion, limitations, and artifact path to the caller, which reports the artifact to the user in its own summary. A direct call reports the result, path, and index outcome without a `.` line.

Path resolution: `./` paths and `../ot-*` sibling paths resolve from this skill's installed directory, and `on-track/` paths resolve from the target repository root.

The owner index script is local Bash with no network calls: it reads frontmatter under `on-track/` and writes only `on-track/INDEX.md`, or exits with validation errors and leaves it unchanged. When it prints a `WARN:` line, relay it to the user in one sentence at the end of your report; a warning never blocks the stage.
