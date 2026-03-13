---
name: review-bug-fixer
description: Fix valid code review findings from one or more review markdown files. Use when the user has review files (e.g., review1.md, review2.md) containing code review findings, issues, or suggestions and wants to fix the valid ones in the current branch. Triggers on requests like "fix review findings", "fix issues from review", "apply code review fixes", or any mention of fixing bugs/issues from review markdown files.
---

# Review Bug Fixer

Fix valid code review findings from arbitrary review markdown files against the current branch.

## Workflow

1. **Collect review files** — Read all review files the user provides (e.g., `review1.md`, `review2.md`, `review3.md`). Accept any number of files in any format (structured or free-form).

2. **Build a unified issue list** — Extract every distinct finding across all files. Deduplicate: if multiple files flag the same issue (same file + same concern), merge them into one entry. Preserve the strongest/clearest description.

3. **Triage each finding** — Classify every finding into one of:
   - **Fix** — Valid bug, logic error, security issue, or correctness problem. Apply the fix.
   - **Skip** — Ignore if any of these apply:
     - Nit or style-only (naming preferences, formatting, comment wording)
     - Not actually valid (misunderstanding of the code, already handled, false positive)
     - Overly defensive (adds complexity for scenarios that realistically won't occur — e.g., redundant null checks on values guaranteed by the framework, error handling for impossible states, excessive input validation on internal-only code paths)

   When in doubt, lean toward skipping. The goal is to fix real bugs, not gold-plate the code.

4. **Fix valid issues** — For each "Fix" finding:
   - Read the relevant source file if not already read
   - Apply the minimal change that addresses the issue
   - Do not refactor surrounding code or add unrelated improvements

5. **Report summary** — After all fixes, output a brief summary:

   ```
   ## Review fixes applied

   ### Fixed
   - <file:line> — <one-line description>

   ### Skipped (not valid / nit / overly defensive)
   - <one-line description> — <reason skipped>
   ```

## Guidelines

- Never create new files unless a finding explicitly requires it.
- Keep fixes minimal and focused — one concern per edit.
- If a finding is ambiguous or could go either way, skip it and mention it in the summary so the user can decide.
- If two findings conflict, skip both and flag in the summary.
- Preserve existing code style (indentation, naming conventions, patterns).
