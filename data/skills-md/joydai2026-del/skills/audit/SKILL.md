---
name: audit
description: Post-change independent audit. Run after major changes to verify everything was created correctly, check contents, validate frontmatter, and report discrepancies. Use when "audit", "verify changes", "check what was done", "review changes", or after any major implementation. Act as if someone else did the work, be critical.
write_scope: self-only
m1_compatible: true
version: 1.0.0
gotchas_count: 0
---

# Audit Skill

Post-change independent audit procedure.

## Procedure

### Step 1: Identify Scope

Determine what was changed:
- If in a git repo: `git diff --name-only HEAD~N` to see recently changed files
- If in vault: check recent session log for list of files created/modified
- If user specifies scope: use that

### Step 2: Enumerate Changes

List ALL files that were created, modified, or deleted. For each:
- Verify the file exists (or was intentionally deleted)
- Note file size and last modified date

### Step 3: Content Verification

For each file:
- Read the file
- Check: does the content match what was intended?
- Check: are there TODO/FIXME/HACK markers left behind?
- Check: are there placeholder values or mock data?
- Check: are there obvious errors (syntax, broken links, etc.)?

### Step 4: Frontmatter Validation (Vault files only)

For any .md files in the vault:
- Check required frontmatter fields per CONVENTIONS.md:
  - type (required)
  - created (required)
  - modified (required for notes)
  - tags (required)
- Check: are tags from the approved tag list?
- Check: is language field set for bilingual content?

### Step 5: Consistency Check

- Do new files follow naming conventions?
- Are cross-references/links valid?
- Do directory structures match conventions?
- Are there any orphaned files (created but not linked)?

### Step 6: Audit Report

```
AUDIT REPORT
============
Date: YYYY-MM-DD
Scope: [what was audited]
Auditor: [agent name]

Files Reviewed: N
Issues Found: N

## Files
| File | Status | Issues |
|------|--------|--------|
| [path] | ✅ OK / ⚠️ Warning / ❌ Error | [description] |

## Issues Detail
1. [severity] [file]: [description]
2. ...

## Summary
[overall assessment — PASS / PASS WITH WARNINGS / FAIL]
```

If writing to vault, save report to `agents/<agent-name>/health/YYYY-MM-DD-audit-report.md`

## Rules

- Be critical, act as if someone else did the work
- Never skip frontmatter validation for vault files
- Flag mock/placeholder data as errors
- Don't fix issues, just report them (unless user asks)
- M1 agents: can audit their own files only

## Gotchas

<!-- Updated whenever Claude fails at something while using this skill -->
<!-- Format: date | what failed | why | fix/workaround -->

_No gotchas recorded yet. Update this section when failures occur._
