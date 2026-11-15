---
name: verification-before-completion
description: "Verifies completion claims against inspected artifacts and relevant post-change command results. Use before reporting work done, fixed, passing, working, or ready, including subagent results; evidence must match the current state and claimed scope."
license: MIT
metadata:
  version: "1.1.0"
  author: "Cody-Sims"
  tier: "core"
---

# Verification Before Completion

Do not claim success from expectation, stale evidence, or a worker's summary.
Verify the final relevant state without rerunning unchanged checks ceremonially.

## Procedure

1. Name the claim and evidence that would prove it: reproduction, tests, build,
   lint, type checks, or artifact inspection. Match evidence to the claim.
2. Inspect the final diff or artifact. Choose the smallest check covering the
   changed behavior and its edges, plus every repository-required gate.
   Do not replace a required full suite with a focused test.
3. Run checks after the final relevant change. Read actual output and exit status;
   a nonzero exit is failure even when the log contains a success message.
   Keep a compact record of command, tested state, scope, result, and artifact.
4. Reuse recorded output from this session, including an earlier turn, only when
   it followed the final relevant change and the tested inputs, dependencies,
   configuration, environment, and artifacts remain unchanged. Otherwise rerun.
   A cached pass, previous-session result, or worker summary alone is insufficient.
5. For a bug fix, rerun the original failing case and confirm the symptom is gone.
   Check dependent service readiness for runtime reproductions; an unavailable
   prerequisite is not proof of a product defect or a successful fix.
6. For delegated work, inspect actual artifacts and recorded command output/exit
   status. Do not trust only a completion message. Verify shared integration
   separately; serialize gates that write the same generated or temporary state.
7. Widen or repeat checks for failures, integration risk, changed tested state,
   or required gates, not merely a new handoff. Preserve every required case and
   assertion; disclose pre-existing or unavailable checks rather than hiding them.

## Evidence boundaries

- Build success does not prove tests, lint, types, or runtime behavior.
- A focused test does not prove a full suite.
- Correct-looking code does not prove the original symptom is fixed.
- Shorter instructions or smaller outputs do not prove lower billed usage,
  faster completion, or better task quality; those require matched measurements.

## Output

Return a nonempty outcome with the supporting evidence appropriate to the request
and any unresolved limitation. Keep logs and repeated checklists out of the final
handoff; retain exact evidence for inspection. Never describe partial, blocked,
or unverified work as complete.
