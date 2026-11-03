---
name: ai-change-evidence
description: Turn changes authored by AI coding agents into evidence an auditor accepts — provenance, authorization, and mapping to change-management controls. Use when agents contribute to code that falls under SOC 2, ISO 27001, PCI DSS or similar.
phase: attest
---

# AI Change Evidence

Change-management controls were written assuming a person made the change. When an agent writes the code and a person approves the pull request, the control still holds — but only if the record shows who decided what, and the record usually does not.

The goal is not to prove an agent was careful. It is to show the same things any change requires: it was authorized, it was reviewed by someone competent and separate, and it can be reconstructed.

## 1. Establish Where Agents Actually Contribute

Auditors ask about scope before controls. Determine, for the audit period:

- Which repositories and services accept agent-authored changes
- Which of those are in scope for the assessment
- Whether agent commits are distinguishable from human ones at all

If commits are attributed to a human's identity with no marker, say so plainly rather than reconstructing it later. An unmarked population is a scoping problem, not a paperwork one.

## 2. Establish Provenance

For each in-scope change, the record should support:

| Question | Evidence |
|---|---|
| Who initiated it? | the person, ticket, or schedule that triggered the run |
| What was asked? | the prompt, spec or plan, version-controlled with the diff |
| What produced it? | agent, model, and configuration in effect at the time |
| What did it touch? | the diff, and the tests and checks that ran |
| Who approved it? | a named human, distinct from the requester |

Configuration matters more than it looks. "Reviewed by the agent's policy" means nothing unless you can show which policy was loaded that day.

## 3. Preserve Separation of Duties

This is the control most likely to be quietly broken:

- The person who asked for a change should not be its sole approver — an agent in between does not create separation
- An agent approving its own output is not review, whatever the label on the check says
- Automated checks are evidence of verification, not of independent approval
- Where an agent both writes and merges, the control has moved to whoever authorized that autonomy — document it there rather than pretending review occurred

## 4. Map to the Controls You Are Assessed Against

Do not invent an "AI control". Map to what the framework already requires:

- **Change management** — authorization, testing, and approval before production (SOC 2 CC8.1, ISO 27001 A.8.32, PCI DSS 6.5)
- **Access control** — the agent's identity, its permissions, and periodic review of them (SOC 2 CC6.1-6.3, ISO 27001 A.5.15)
- **Logging and monitoring** — agent actions attributable and retained for the audit period (SOC 2 CC7.2)
- **Vendor management** — the model provider as a subprocessor, where source code or customer data leaves your boundary (SOC 2 CC9.2, ISO 27001 A.5.19)

Check framework versions against the assessment date; control identifiers move between revisions.

## 5. Answer the Data Questions

Expect these, and get the answer from the contract rather than from a marketing page:

- Does source code leave the environment, and to whom?
- Is it retained, and for how long? Is it used for training?
- Which regions process it, and does that match your commitments to customers?
- If customer data can reach an agent's context, which agreement covers it?

## 6. Sample the Way an Auditor Will

Pick changes at random from the period and try to assemble the full record end to end. Note where you had to ask a person, guess, or reconstruct from memory. Those are the findings — not the changes themselves, but the places the trail broke.

Where evidence is genuinely absent, record it as a gap with an owner and a date. A documented gap is defensible; a reconstructed record that quietly implies more rigour than existed is not, and is the thing that damages an assessment when it unravels.

## Scope and Rules of Engagement

Assess only environments you are authorized to review, and handle whatever the trail contains — prompts, diffs, ticket contents — under the confidentiality terms that apply to them. Do not present this output as an audit opinion or a certification: it is preparation for one, and the assessor's judgement is theirs.

## Output

Produce a control-by-control table: the control, the evidence that supports it, where that evidence lives, and whether it covers the whole period or part of it. List gaps separately with an owner and a remediation date. State plainly which claims rest on tooling you verified and which rest on someone's description of the process.
