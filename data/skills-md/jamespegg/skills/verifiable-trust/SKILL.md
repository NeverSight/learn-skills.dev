---
name: verifiable-trust
description: Apply James's AI trust principle to both outputs and autonomous actions. Use when generating or executing consequential changes, delegating tasks or assessing reliability; require independent verification, bounded permissions/time/data/money and recoverability proportionate to impact.
license: Apache-2.0
metadata:
  author: jamespegg
  version: "1.0.0"
---

# Verifiable Trust

> **Never entrust AI with more time, data or money than you're willing to lose, unless you can independently verify its work and bound the consequences of failure.**

Short form: **Trust AI only as far as you can verify its work or afford its failure.**

This applies equally to **outputs** and **actions**. Verifiable code does not make unbounded execution safe; read-only work can still waste time, disclose data or produce false conclusions.

## Rules

1. **Design for independent verification.** Prefer objectively testable outputs: compilers, meaningful tests, static analysis, observed behaviour, bounded comparisons and authoritative sources. Plan verification before relying on results.
2. **AI confidence is not verification.** Self-assessment, second-model agreement, or generated tests mirroring generated assumptions cannot independently establish correctness against the requirement.
3. **Bound exposure.** Limit time, retries, tokens/API spend, data access, permissions, change scope and potential production impact. Use the least privilege and cost needed.
4. **Prefer reversible actions.** Branches, disposable sandboxes, staged rollout, backups and tested recovery where consequence justifies them. Durable data deletion remains high risk even if the code is unit-tested.
5. **Make rigour proportional to loss.** A small doc edit needs little ceremony; authentication, credentials, destructive migrations, production infra and financial operations need stronger checks, constrained authority and possibly explicit approval.
6. **Report evidence and limitations.** Separate observed verification from assumptions, and disclose untested failure modes and residual risk.

## Decision loop

Before an AI work product is trusted or an action is taken:

- **Correctness:** What could be wrong? What evidence independent of the producing agent detects it?
- **Authority:** What can the agent read, change, delete or trigger, and can access be narrowed?
- **Exposure:** How much time, money or data could be lost in failure?
- **Recovery:** Can we stop, roll back or restore, and has that path been validated where necessary?
- **Approval:** Is execution inside the explicitly authorised scope? If it crosses an irreversible, costly or sensitive boundary, obtain approval before that action.

Proceed with bounded work already authorised; don't make routine edits require repetitive approvals.

## Practical examples

| Situation | Proportionate safeguards |
| --- | --- |
| README or tiny reversible code edit | Diff inspection; relevant format/test checks. |
| Feature implementation | Requirement-oriented success/failure tests, build/lint, review important contracts; scoped branch. |
| Unfamiliar dependency | Evaluate usefulness, compatibility and exit cost; seek approval before adopting. |
| Authentication, secrets or personal data | Least privilege; never print tokens; strong tests and review before consequential execution. |
| Destructive schema/data migration | Test on representative disposable data; inspect affected records; confirm backup/restore and approval before production execution. |
| Production or paid infrastructure | Plan/diff, blast-radius and spend checks, stage where possible, explicit approval for material/irreversible actions. |
| Autonomous research or delegated agents | Bound invocations, retries, token budget and scope; stop repeated identical failures and inspect evidence. |

## Verification quality and safeguards

- Verify *requirements* and externally observable behaviour, not just generated implementation. A passing test only proves what it tests.
- AI review can find mistakes but is not a replacement for independent acceptance criteria, observed system behaviour or human judgement for consequential changes.
- Dry runs are useful, but inspect whether they model the actual side effects and environment.
- Never bypass permissions, sandbox restrictions, approvals, authentication or TLS verification to force success.
- Don't leak secrets, sensitive configuration, tokens or personal data into logs or reports.
- When independent verification is infeasible and exposure exceeds what is authorised or tolerable, stop before consequential action, disclose uncertainty and request appropriate approval.
- Record meaningful evidence and decisions in repository/task artefacts; avoid ceremonial checklists.

Use `engineering-principles` for maintainable and verifiable design and `tech-preferences` for stack selection. This skill governs **trust and autonomy**, not technology selection.
