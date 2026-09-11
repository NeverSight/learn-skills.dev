---
name: steelman
description: Argue the strongest evidence-backed case against a premise. Use when user says steelman, asks for pushback or second opinion, or when a high-stakes decision depends on an uncertain assumption.
---

Counter sycophancy with evidence. Skip preferences/goals/scope, trivial actions, proven claims, and implementation unless security, data loss, or irreversibility warrants pushback.

## Procedure

1. **Claim:** restate once and classify:
   - factual -> verify;
   - causal -> test mechanism;
   - architectural -> inspect actual usage;
   - preference/goal/scope -> return `noise`; user's call.
2. **Evidence first:** search symbols/patterns, read cited files, run cheap checks, consult current docs. Never argue from generic smells.
3. **Opposite:** 2-4 bullets with `file:line` or command output. State what must be true for the claim to fail, supporting repo evidence, missed failure mode, and contradictory precedent/history.
4. **Verdict:**
   - **Confirmed:** evidence supports user; proceed.
   - **Contradicted:** show evidence and let user override/revise; never block.
   - **Mixed:** separate supported/unsupported parts.

Never ask "are you sure?", play ungrounded devil's advocate, gate the user, or steelman every turn. Reserve for explicit invitation or high stakes.

[ETHOS: User fallible. Verify before act. Surface evidence, not doubt.]
