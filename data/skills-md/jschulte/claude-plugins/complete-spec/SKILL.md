---
name: complete-spec
description: Resolves [NEEDS CLARIFICATION] markers in specifications through interactive Q&A. Asks focused questions about missing features, UX details, and business rules, then updates spec files with complete, unambiguous requirements. Step 5 of 6 in the reverse engineering process.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Complete Specification

**Step 5 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 30-60 minutes (interactive)
**Prerequisites:** Step 4 completed (`docs/gap-analysis-report.md` exists with clarifications list)
**Output:** Updated specs in `specs/` with all `[NEEDS CLARIFICATION]` markers resolved

## Canonical Paths

| Artifact | Path |
|----------|------|
| Gap analysis report | `docs/gap-analysis-report.md` |
| Feature spec files | `specs/*.md` |
| Clarification progress | `specs/.clarification-progress.md` |

---

## Phase 1: Collect Clarifications

Read `docs/gap-analysis-report.md`. If the file does not exist, report the error to the user and halt: "Gap analysis report not found at docs/gap-analysis-report.md. Run Step 4 (Gap Analysis) first."

Read all spec files matching `specs/*.md` using Glob.

If any spec file fails to read, report the filename and error to the user and skip that file.

Extract every line containing `[NEEDS CLARIFICATION]` from the gap analysis report and all spec files. Record for each marker:
- The source filename
- The feature name (nearest heading above the marker)
- The marker text
- The priority label if present (P0/P1/P2/P3), default to P1 if unlabeled

### Zero-Marker Guard

If zero `[NEEDS CLARIFICATION]` markers are found across all files, inform the user: "All specifications are already complete. No clarification markers found. Proceed to Step 6 (Implement from Spec)." Halt execution.

### Progress Resume

Check whether `specs/.clarification-progress.md` exists. If it does, read it and identify which markers have already been resolved. Remove resolved markers from the working list. Report to the user: "Found existing progress file. {N} of {total} markers already resolved. Resuming from marker {next}."

### Present Summary

Group remaining markers by feature. Sort groups so P0 features appear first, then P1, P2, P3. Present the grouped list to the user:

```
Found {N} clarification markers across {M} features:

**P0 - Critical ({count})**
- [feature]: [marker text] (specs/filename.md)
...

**P1 - High ({count})**
...

Starting with P0 items. Ready to begin?
```

Wait for user confirmation before proceeding.

**Signal:** "Phase 1 complete. {N} markers identified across {M} features."

---

## Phase 2: Interactive Q&A

For each unresolved marker, starting with P0:

1. Present the marker's context to the user. State the feature name, the question, and any surrounding context from the spec file.
2. Ask one focused question at a time. Provide examples of common patterns or industry standards when relevant.
3. Wait for the user's answer.
4. If the user answers "I don't know" or expresses uncertainty, suggest common industry patterns and offer to mark it as deferred (P3). If the user agrees to defer, record the deferral and move to the next marker.
5. If the user's answer contradicts a previously documented requirement, surface the contradiction explicitly: "This conflicts with [previous requirement] in [filename]. Which should take priority?" Wait for resolution before proceeding.

### Behavioral Constraints

- Ask one question per message. Do not combine multiple clarifications.
- Summarize your understanding of each answer before moving to the next question.
- Adapt question style and terminology to the actual project domain.

**Signal after every 5th marker:** "Progress: {resolved}/{total} markers resolved."

---

## Phase 3: Update Specs

After each user answer, immediately update the relevant spec file. Do not batch updates.

Load the operations file for detailed update instructions:

```
Read: skills/complete-spec/operations/update-spec-file.md
```

After each file write, re-read the file and verify:
1. The `[NEEDS CLARIFICATION]` marker has been removed.
2. The new content is present and correctly formatted.
3. No existing content was accidentally deleted.

If a write operation fails, report the error to the user and retry once. If the retry fails, log the intended change in `specs/.clarification-progress.md` and continue with the next marker.

After each successful update, append a completion record to `specs/.clarification-progress.md`:

```markdown
## {feature-name} - {marker-summary}
- **File:** specs/{filename}.md
- **Status:** Resolved
- **Resolution:** {one-line summary of the answer}
- **Timestamp:** {ISO 8601}
```

**Signal after each update:** "Updated specs/{filename}.md. Marker resolved."

---

## Phase 4: Confirm Priorities

After all markers are resolved (or deferred), present the finalized priority breakdown to the user:

```
All clarifications resolved. Priority summary:
- P0 (Critical): {count} features
- P1 (High): {count} features
- P2 (Medium): {count} features
- P3 (Low/Deferred): {count} features

Review these priorities. Should any features move up or down?
```

Wait for user confirmation. If the user requests priority changes, update the relevant spec files immediately.

**Signal:** "Phase 4 complete. Priorities confirmed."

---

## Phase 5: Final Verification

Read all spec files in `specs/`. Scan every file for remaining `[NEEDS CLARIFICATION]` markers.

If any markers remain:
- Report each remaining marker to the user with its file and location.
- Ask whether to resolve now or defer to P3.
- Process accordingly using Phase 2 and Phase 3 procedures.

If zero markers remain, confirm completion:

```
Final verification passed. Zero [NEEDS CLARIFICATION] markers remain.

Specifications are ready for Step 6 (Implement from Spec).
```

Delete `specs/.clarification-progress.md` since all work is complete.

**Signal:** "Phase 5 complete. All specifications finalized."

---

## Error Recovery Summary

| Error | Action |
|-------|--------|
| `docs/gap-analysis-report.md` not found | Halt. Instruct user to run Step 4 first. |
| Spec file unreadable | Skip file. Report error. Continue with remaining files. |
| Write operation fails | Retry once. On second failure, log to progress file and continue. |
| Zero markers found | Inform user specs are complete. Halt. |
| User contradicts prior requirement | Surface conflict. Wait for resolution. |
| Session interrupted | Progress file preserves state. Resume on next invocation. |
