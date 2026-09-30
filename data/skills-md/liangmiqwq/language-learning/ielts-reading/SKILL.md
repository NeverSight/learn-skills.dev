---
name: ielts-reading
description: Create or continue IELTS Academic Reading practice, produce printable passage sessions, and review answers using private persistent progress and passage deduplication. Use for IELTS reading study and continuation, not unrelated English conversation practice.
---

# IELTS reading

Continue from saved evidence, not from the current chat's memory. Keep personal preferences, passages, PDFs and answers outside the public skill checkout.

## Read before creating

Read [records.md](references/records.md), then run the bundled `scripts/learning-store.mjs show` for the selected learner. Paths to scripts are relative to this installed skill, not the working directory. Use learner `default` unless another learner is identified. Initialize only when the profile does not exist; a failed read is not permission to reset it. Respect `LANGUAGE_LEARNING_HOME` and preserve all existing history.

Read the profile, material events, self-reports and relevant attempts/feedback. Distinguish generated, delivered, self-reported completed and assessed work. Missing completion or accuracy is unknown. Do not require submissions or a progress report to continue making materials. Follow the learner's current request and saved preferences; do not infer English ability from programming experience or convert a single-passage score into a band.

## Create or continue

Use [practice.md](references/practice.md) for sourcing, question checks and printing. Determine the requested number of sessions from the current request or saved preference. Use `next_sequence` for new material; never restart numbering because this is a new chat.

Before drafting, inspect all prior titles, source identities, topics and passage text. Choose a different passage and vary recent topics. Before rendering, run `check --file` with the candidate material details. Exact normalized passages and identical source keys must not become new materials, even with different filenames, titles or questions. Inspect near-match warnings and record a substantive `novelty_review` only when the text is genuinely a different passage. Cosmetic rewriting does not qualify. The helper cannot detect all paraphrases; compare premise, examples, argument and question coverage yourself.

Archive the complete source, questions, checked key, explanations and final PDF privately in a new edition directory. Record each material with `record --file`; it rechecks duplicates under a write lock. Do not deliver new material as successfully saved until recording succeeds. For interrupted work, inspect saved material and artifacts and resume the existing edition rather than creating it again. For an explicit reprint or revision, reuse the material ID, retain earlier artifacts and append a `note` describing the new edition. A review reuses the existing passage with a new attempt, not a new material event.

## Record learning

Preserve actual answers as an `exercise_attempt` before giving assessed `feedback`. Separate first attempts, changes after hints and later reviews. Save question identifiers, supplied answers, evidence and concise error categories such as paraphrase, scope, location, word limit or False versus Not Given. Keep partial submissions partial; do not invent unanswered work.

If the learner only reports completion or accuracy, save a `self_report` with the exact claim, material ID when known, and null for unknown dates/counts. Do not require individual answers or infer specific mistakes from a percentage. Update the profile's next focus only with evidence and append a corresponding note; retain prior baseline evidence.

When importing history, recover existing passages and artifacts, attach conversation IDs and uncertainty, and make imports idempotent using stable event IDs. A source rejected for a different defect can still contain a previously seen passage: record that distinction instead of regenerating it. Do not log fetched-but-unused source candidates or generated answer keys as learned work.

Keep data local unless a private backup destination was explicitly authorized. Report persistence failures honestly. This skill does not schedule tasks or upload learning records.
