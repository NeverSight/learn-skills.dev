---
name: verification-before-completion
description: Use before claiming work is fixed, complete, passing, or ready to integrate.
---

# Make Claims Match Evidence

Verify the behavior that changed and the boundaries it could affect. Choose checks
proportionate to the risk and follow required repository checks.

For each completion claim, know which command, inspection, or experiment supports
it and which revision was checked. Read the result, including failures and skipped
checks. A subagent's summary or a successful build alone does not prove every
behavior works.

Evidence remains usable while the relevant code and environment are unchanged.
Do not rerun the same suite just to repeat a status update. Rerun affected checks
after edits or integration changes that could invalidate the result.

Before delivery:

- Review the actual diff for accidental changes and unnecessary complexity.
- Confirm relevant checks passed, or clearly identify failures and untested areas.
- Distinguish local tests, mocked integration checks, and live end-to-end validation.
- Report limitations without claiming success beyond the evidence.

If verification is blocked, give the exact check that could not run and why.
Do not hide failures, weaken assertions, or label an unverified change complete.
