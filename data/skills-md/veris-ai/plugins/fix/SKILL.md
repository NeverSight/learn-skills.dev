---
name: fix
description: Fix a defect using Veris to answer relevant service questions and test the changed application. Reuse normal development tests and report their results. Takes an issue link or a prompt. Run when the engineer names this command.
argument-hint: "<issue link | prompt>"
disable-model-invocation: true
---

Fix the requested defect. Use the twin to answer questions that affect the change
and exercise the application. Reuse evidence from normal development: once the required
behavior is covered and passes, finish. Investigate further when a failure or a
specific unanswered requirement warrants it.

For a change with no meaningful vendor interaction, skip Veris setup and twin work;
use the repository's validation and state that scope in the result.
A local queue or cache defect that changes vendor-facing behavior still needs the
affected application flow tested against the twin.

## Use the working setup

Read relevant findings in `.veris/NOTES.md` and reuse those whose conditions still
apply. Follow **How to run** for preparation, the application command, evidence
collection and cleanup. Setup owns connection selection and configuration.
Run `setup` only when a needed handoff step is missing, the connection is broken,
or the change invalidates its wiring, such as adding a vendor service or hostname.
An application assertion failure alone is not a reason to redo setup.

In a plugin-managed session, follow [session.md](../veris-reference/session.md)
for the live repository/twin binding and provider tools. Reuse a binding already
verified in this session; revalidate after reconnect or a relevant identity change.
Saved metadata alone is not a live binding. Leave plugin-owned resources alive.

Use the saved start/reconnect steps only when needed, reuse this task's active
sandbox, and check its expiry before long work. Refresh expiring URLs or credentials
through the saved preparation steps.

An unavailable twin blocks verification that needs it. Report the concrete error;
independent code work and local checks can continue. Retry only when the error suggests
a recoverable condition or something changed. Do not report unrun checks as passed.

## Diagnose and implement

Keep reads and tool output focused. Save large logs or responses to a file and
inspect relevant excerpts instead of loading them repeatedly into the conversation.

Read the issue (`gh issue view <ref> --json title,body,comments` for GitHub) or the
supplied prompt, then inspect the affected code. Identify the reported outcome and
the behavior the fix should produce. The issue's proposed cause may be wrong; the
twin's list of injectable faults does not select the repository's diagnosis.

Reuse an existing relevant failure or reproduce it through the application when
practical. Use [fault injection](../veris-reference/faults.md) when the defect depends
on a vendor failure; reproduce local state, cache or queue defects in the application.
If the observation contradicts the diagnosis, revise the diagnosis. Do not manufacture
a historical red run by stashing a fix or restart work solely to record chronology.
If the original failure was not reproduced, say so and verify the implemented behavior.

Use the cheapest twin interface that answers an unresolved service question:

- [Manual/schema](../veris-reference/twin.md) for credentials, supported faults and
  field rules. Fetch the manual with `veris sandbox services manual <twin> --raw`
  when those details are needed; read the relevant sections.
- [Data and seeding](../veris-reference/state.md) for the state the application needs.
  Reuse appropriate seed rows; ids belong to this sandbox. Missing fixtures are a
  setup problem, not a reproduction of the reported defect.
- Direct twin calls for discovery; they establish twin behavior, not application
  correctness. A useful application test can answer the same question without a
  separate probe.

Implement using the repository's conventions and strengthen the affected test where
useful. For changes to retries, idempotency or identity, cover the applicable duplicate,
distinct-operation and recovery behavior in that test; the focused recipes are in
[proof.md](../veris-reference/proof.md#retry-and-identity-changes). Exercise the caller
the task promises to fix, including relevant dispatch branches. A test-only option
that bypasses the real caller does not establish that caller's behavior.
Inspect relevant sibling branches that implement the same behavior inline;
a search for callers of the changed symbol can miss them.

## Test the changed application

Run the affected application test or flow using **How to run**'s saved execution
and evidence steps. Prefer the repository's existing integration test. Select the
affected test or flow as documented while preserving the configured environment
and connection settings.

Use the edited source or a build produced from it, following the saved source/build
recipe. A wrong mount can execute the image's old baked code. Preserve the configured
routing and TLS trust; do not change a production vendor call to make a test pass.

The test must assert the expected response or persisted outcome, and its receipt or
attributed trace must show the relevant application traffic reached the twin. Existing
assertions that read the outcome are sufficient; do not repeat them with manual data
reads. If the result is unclear, inspect the relevant rows by returned ids or the
trace for this run using the saved evidence procedure. Interpret receipt/exit results
with the reference for that configured path; use
[webhooks.md](../veris-reference/webhooks.md) when a callback is part of the task.

An existing execution counts if it tested the final relevant code/build and conditions.
One suite can cover several requirements; a retry case can make multiple calls in one
test. There is no required second successful run or separate proof phase. Honor the
repository's required checks, reuse their evidence, and rerun affected checks after
changes or failures.

If the assertions fail, change the implementation or correct the diagnosed setup
problem. If required behavior remains untested, report that gap. A successful process
exit or unrelated twin traffic alone is not verification of the change.

## Finish

Summarize what changed, the test/command and outcome with an existing evidence
reference, and material limitations. [evidence.md](../veris-reference/evidence.md)
shows the short form. Note any task premise disproved by the investigation when it
affected the solution. A known contradiction is a defect to resolve, not an assumption.

Follow the repository's PR convention; open a draft when that is the requested
handoff. Without a PR-capable remote, save the description locally and say no PR was
opened. Git history, task ids and the optional [audit helpers](../veris-reference/proof.md#optional-audit-helpers)
are not prerequisites for working on code. Do not initialize Git or add a remote
implicitly. Use available package/version metadata if useful for debugging; it is
not a separate completion requirement.

Save cited redacted evidence before cleanup, honoring `.veris/setup.json`'s existing
`artifact_policy`. Add new reusable service or SDK findings to `.veris/NOTES.md`,
with their relevant conditions and existing redacted evidence reference. Correct
stale entries without duplicating the task report. Update **How to run** if you
repaired it. Follow the saved cleanup or change-handoff steps for the recorded
lifecycle owner; leave plugin-owned resources alive. Do not promote from this command.
Ask before sending repository code anywhere new.
