---
name: interactive-diff-review
description: "Supports commands: [commit|commit_a commit_b] [--verify] [--apply] [--commit] Interactive git diff review skill. Parses git diff output into individual hunks, presents each hunk to the user with analysis for accept/reject decisions, verifies complete coverage, and generates a Markdown review report. "
---

# Git Diff Review Skill

Interactive hunk-by-hunk code review. Parse → Review → Verify → Report → Apply → Commit.

---

## Commands

Parse `$ARGUMENTS` to determine the command and diff target:

| Command | Usage | Description |
|---------|-------|-------------|
| `review` | `/interactive-diff-review [target]` | **Default**. Full interactive review: parse → review → report |
| `--verify` | `/interactive-diff-review --verify` | Check report exists, matches current diff, and all hunks passed |
| `--apply` | `/interactive-diff-review --apply` | Fix code based on rejected hunks' review suggestions |
| `--commit` | `/interactive-diff-review --commit` | Generate and execute git commit (requires `--verify` pass first) |

**Target** is optional: `<commit>`, `<commit_a> <commit_b>`, or omit for auto-detect (staged → workspace).

Commands can be combined: `/interactive-diff-review --apply --commit` will apply fixes then commit if verify passes.

### Command Routing

1. Parse `$ARGUMENTS` — extract command flags and remaining positional args (diff target).
2. If no command flag is present → default to `review`.
3. Route to the corresponding section below.

---

## Workflow Checklist

Copy this checklist and check off items as you complete them:

```
Diff Review Progress:
- [ ] Step 1: Resolve & Parse
  - [ ] 1.1 Run resolve_diff.py to get diff + language
  - [ ] 1.2 Verify no error, inform user of diff source + language
  - [ ] 1.3 Run parse_hunks.py to split into hunks
  - [ ] 1.4 Handle edge cases ⚠️ Load references/edge-cases.md
- [ ] Step 2: Interactive Review ⚠️ CORE LOOP
  - [ ] Load references/review-format.md
  - [ ] 2.1 Display hunk (index/total, file, type, diff body)
  - [ ] 2.2 Provide analysis (summary, impact, risks, suggestions)
  - [ ] 2.3 Collect decision via ask_user_input (Accept / Reject / Skip)
  - [ ] 2.4 If rejected, ask reason (open-ended text follow-up)
  - [ ] 2.5 Show running tally, advance to next hunk
  - [ ] 2.6 Repeat 2.1–2.5 until all hunks done
  - [ ] 2.7 Loop back for any skipped hunks
- [ ] Step 3: Coverage Verification ⚠️ REQUIRED
  - [ ] 3.1 Re-run resolve_diff.py + parse_hunks.py
  - [ ] 3.2 Compare new hunks against reviewed hunks (file + header + body)
  - [ ] 3.3 If new/changed hunks → review them (back to Step 2)
  - [ ] 3.4 Confirm full coverage before proceeding
- [ ] Step 4: Generate Report
  - [ ] Load references/report-template.md
  - [ ] 4.1 Build Markdown report (detected language, diff order)
  - [ ] 4.2 Save to /mnt/user-data/outputs/diff-review-report.md
  - [ ] 4.3 Present to user
```

---

## Step 1: Resolve & Parse

### 1.1 Run resolver

```bash
python scripts/resolve_diff.py                       # auto: staged → workspace
python scripts/resolve_diff.py <commit>              # single commit
python scripts/resolve_diff.py <commit_a> <commit_b> # commit range
```

Returns JSON: `{ source, ref, language, diff, error }`

### 1.2 Verify & inform

If `error` is non-null → report to user and **stop**.
Otherwise tell the user which diff source was resolved and what language was detected.

### 1.3 Save diff & run parser

Extract the `diff` field from Step 1.1's JSON output and write it to a temporary file, then parse:

```bash
# Write the diff field to a temp file (agent should use Write tool or shell redirect)
# e.g. write resolve output's .diff value to /tmp/diff.txt

python scripts/parse_hunks.py --file /tmp/diff.txt
```

Returns JSON: `{ total, hunks: [{ index, file, header, body, type, status, reason }] }`

### 1.4 Edge cases

Load `references/edge-cases.md` and handle accordingly.

---

## Step 2: Interactive Review

**Before starting this step**, load `references/review-format.md` for display format, analysis fields, and decision collection details.

All UI text uses the **detected language** from Step 1. Technical terms remain in English.

Loop through each hunk: display → analyze → collect decision → show tally → next.
After the first pass, loop back for any skipped hunks.

---

## Step 3: Coverage Verification

1. Re-run `resolve_diff.py` + `parse_hunks.py` with same arguments as Step 1.
2. Compare new hunks against reviewed hunks by `file + header + body`.
3. New/changed hunks found → go back to Step 2 for those hunks only.
4. Confirm full coverage. Only proceed to Step 4 when all hunks are decided.

---

## Step 4: Generate Report

**Before starting this step**, load `references/report-template.md` for the full template.

Build the report in the **detected language** (technical terms in English), ordered by original diff sequence. Save to `diff-review-report.md` in the project root and present to user.

---

## Command: `--verify`

Validates that the review is complete and current.

1. Check `diff-review-report.md` exists in project root. If not → error: "No report found. Run `review` first."
2. Re-run `resolve_diff.py` + `parse_hunks.py` with same target args to get current hunks.
3. Parse the report's Overview table to extract reviewed hunks (file + type + status).
4. Compare:
   - Every current hunk has a matching entry in the report (by file path + hunk header + body hash).
   - No extra entries in report that don't exist in current diff (stale entries).
5. Check that all hunks have status ✅ Accepted (no ❌ Rejected, no missing).
6. Output result:
   - **PASS**: "Verification passed. All N hunks reviewed and accepted. Ready to commit."
   - **FAIL — unreviewed hunks**: List the unmatched hunks.
   - **FAIL — rejected hunks**: List the rejected hunks with their reasons.
   - **FAIL — stale report**: Report doesn't match current diff. Suggest re-running `review`.

---

## Command: `--apply`

Fixes code based on review suggestions for rejected hunks.

1. Check `diff-review-report.md` exists. If not → error.
2. Parse the report to find all ❌ Rejected hunks and their rejection reasons + analysis suggestions.
3. For each rejected hunk (in diff order):
   a. Read the relevant file and locate the code region from the hunk.
   b. Based on the rejection reason and the review analysis, generate a fix.
   c. Apply the fix using Edit tool.
   d. Show the user what was changed and why.
4. After all fixes applied, inform the user:
   - "Applied fixes for N rejected hunks. Run `--verify` or re-run `review` to confirm."

**Note**: `--apply` does NOT re-run the review. The user should run `review` again or `--verify` after applying.

---

## Command: `--commit`

Generates and executes a git commit. Requires verification to pass first.

1. Run the `--verify` flow internally (same as above).
2. If verify **FAILS** → stop and show the failure reason. Do not commit.
3. If verify **PASSES**:
   a. Parse the report to build a commit message:
      - Subject line: summarize the changes (max 72 chars), in detected language.
      - Body: list the key changes from the report overview (accepted hunks grouped by file).
   b. Show the proposed commit message to the user for confirmation.
   c. On user approval:
      - `git add -A` (or stage the specific files from the review).
      - `git commit` with the message.
   d. Show the commit result.

---

## Parameter Reference

| Parameter | Type | Description |
|-----------|------|-------------|
| (none) | — | Default `review` command, auto-detect diff source |
| `<commit>` | string | Commit hash, short hash, tag, or ref |
| `<commit_a> <commit_b>` | string | Commit range |
| `--verify` | flag | Run verification check on existing report |
| `--apply` | flag | Apply fixes for rejected hunks |
| `--commit` | flag | Verify + generate git commit |

---

## Language

- Detected from `git log --oneline -10` by `resolve_diff.py`.
- All UI, analysis, and report use detected language; technical terms stay English.
- Mixed-language commits → most frequent wins.
- No history → fall back to user's conversation language.

---

## File Structure

```
git-diff-review/
├── SKILL.md                          # This file — workflow orchestration
├── scripts/
│   ├── resolve_diff.py               # Diff source + language detection
│   └── parse_hunks.py                # Unified diff → structured hunks
└── references/
    ├── review-format.md              # Step 2: display, analysis, decisions
    ├── report-template.md            # Step 4: Markdown report template
    └── edge-cases.md                 # Step 1.4: edge case handling
```
