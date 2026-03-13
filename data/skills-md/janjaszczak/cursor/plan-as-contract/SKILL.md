---
name: plan-as-contract
description: Produce a reviewable, file-referenced implementation plan that acts as a contract before execution. Use for risky ops, architecture changes, migrations, multi-file edits.
compatibility: Works best with Cursor Plan Mode and ability to reference repo files.
allowed-tools: Read FileSearch(*)
metadata:
  intent: Use when approval gates reduce risk and rework.
---

# plan-as-contract

## Activation gate
Use if:
- Multi-file changes, migrations, security/perf sensitive work, or irreversible ops.

## Procedure
1. Define objective + acceptance criteria (testable).
2. Enumerate touched areas: BE/FE/DB/config/CI/CD/infra (or explicitly “NOT touched”).
3. Identify dependencies (APIs, flags, secrets, external services).
4. Provide ordered steps with file paths and validation commands.
5. Stop: wait for user approval (unless user asked “just do it”).

## Output
- Plan (steps) + Risks + Verification checklist.
