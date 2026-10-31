---
name: japanese-learning
description: Plan Japanese study, create printable learning materials, explain familiar expressions, and review exercises while maintaining a private learning history across sessions. Use for ongoing Japanese learning and study records, not unrelated document work.
---

# Japanese learning

Use the learner's actual evidence to choose the next step. Connect familiar spoken Japanese to kana, real expressions and short sentences. Keep personal history outside the public skill repository.

## Start with the saved record

Resolve the data directory using [records.md](references/records.md). Run the bundled `node scripts/learning-store.mjs context` for the selected learner; initialize only if no record exists. Read the profile and relevant recent summaries before proposing new work; fetch a full event only when its evidence matters. Follow [memory.md](references/memory.md) for selective retrieval and meaningful updates. Paths to bundled resources are relative to this skill, not the current working directory.

If no learner was specified, use `default`. Keep a classmate's submitted work in a separate learner profile when identifiable; do not assign shared progress or guesses to both people. Missing data is unknown, not zero ability. Do not claim disk access succeeded unless it did.

## Choose the task

- **Planning or explanations:** use [teaching.md](references/teaching.md). If the user asks only for ideas, answer inline without creating a workbook.
- **Printable materials:** additionally read [workbooks.md](references/workbooks.md). Use an available PDF/document skill for the requested format; otherwise use a suitable local renderer and inspect the output. Do not assume a fixed runtime path or a macOS font exists.
- **Submitted exercises:** preserve the actual answers before assessing them. Give the correction, a brief reason and one useful retry. Record the attempt and feedback as separate events. Do not turn casual questions into scored exams.

The current request and saved preferences take precedence over the teaching defaults. English-led material with Chinese glosses is a supported preference, not an assumption about every learner.

## Close the loop on disk

Record meaningful new materials, self-reports, submitted attempts and feedback in the private store using the helper. Repeated preferences, routine tool activity and conversation filler do not need new learning events. Respect a preference for no answer submission or accuracy-only reports; do not require either to continue. Save the source and final artifact for generated materials. Save the question/exercise identifiers together with answers so future feedback remains interpretable.

A generated workbook is **assigned material**, not completed practice. A self-report is not an assessed result. Report mastery only when supported by actual work; keep recognition, handwriting, listening and sentence production distinct. Unknown completion dates and scores remain null.

Before the next lesson, revisit actual errors and unresolved questions, then introduce a small amount of new material. Avoid repeating material merely because the conversation context was lost. If persistence fails, explain the failure; never say progress was saved when it was not.

Do not upload personal profiles, answers, screenshots or private artifacts with a public skill update. Private remote backup requires the user's chosen repository and authorization for that destination; local persistence needs no new permission when it is part of the learning request. This skill does not create background monitoring or automatic study sessions.
