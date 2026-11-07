---
name: rfi-drafting
description: RFI drafting that gets answered for construction and design work, covering rfi, documents, coordination. Something on site does not match the drawings and you need an RFI that is clear enough to be answered first time, with the schedule impact stated. Use when the user asks for help with rfi drafting that gets answered, or is working on rfi, documents, coordination in a construction, engineering or design context. Produces a reviewable draft, never a final answer.
license: CC BY 4.0
section: Site and field operations
tags: rfi, documents, coordination
updated: 2026-09-24
source: construction-prompts/prompts/07-site-operations/02-rfi-drafting.md
---

# RFI drafting that gets answered

Something on site does not match the drawings and you need an RFI that is clear enough to be
answered first time, with the schedule impact stated.

## Inputs to collect

Ask the user for any of these you do not already have. Never invent project facts, dates,
costs or clause references to fill a gap.

- `{{date_needed}}`
- `{{impact}}`
- `{{issue_description}}`
- `{{our_interpretation}}`
- `{{project_name}}`
- `{{reason_for_date}}`
- `{{references}}`
- `{{site_findings}}`

## Instructions

```text
You are a project engineer drafting an RFI.

Project: {{project_name}}
Issue: {{issue_description}}
Drawing or specification references: {{references}}
What we have found on site: {{site_findings}}
What we think is intended: {{our_interpretation}}
Date the answer is needed: {{date_needed}} because {{reason_for_date}}
Cost or programme impact if answered late: {{impact}}

Draft the RFI with:
1. A one-sentence question in the subject line.
2. The background, in no more than four sentences.
3. The specific question, numbered if there is more than one.
4. Our proposed interpretation, so the answer can be a simple confirmation.
5. The date needed and why.

Tone: neutral and factual. No suggestion that anyone made a mistake. Keep it under 250
words, in a form I can paste into our RFI register.
```

## What good output looks like

- One clear question, sometimes two, rather than an open-ended request to review everything.
- Proposes an interpretation, which dramatically increases the chance of a fast answer.
- States the date and the consequence, which is what converts an RFI into a tracked obligation.

## Follow-ups

- "Rewrite the subject line so it is unambiguous in a register listing."
- "Draft the follow-up to send if there is no answer three days before the date needed."
- "Turn the reply we received into a record of the instruction, ready for our file."

## Guardrails

RFIs are contractual correspondence: the notice requirements in the contract may apply, and
documenting a delay without sending the required notice can cost the entitlement. Have someone with
commercial authority review anything with cost or time implications before it is issued.

---

*Part of the construction agent skills library — CC BY 4.0. Verify anything that leaves your
company: a named person owns every output.*
