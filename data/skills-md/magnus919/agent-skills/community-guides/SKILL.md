---
name: community-guides
description: >-
  Create, adapt, or revise practical community guides with locally grounded
  activities, participant worksheets, facilitator instructions, and maintenance
  plans. Use for neighborhood preparedness, mutual support, shared projects,
  and community learning programs. Do not use for travel guides, promotional
  brochures, standalone policies, simple document formatting, or live incident response.
license: MIT
metadata:
  source: "Original method informed by Ready Together; attribution and adaptation boundaries in references/source-pattern.md"
---

# Community Guides

Help a community turn a shared concern into feasible actions and a program that
another facilitator can run. Success means usable materials, clear dependencies,
and an honest account of what has been checked and what still needs participants.

## When not to use

Use `travel-guide` for destination research and visitor itineraries, `documents`
for document rendering or formatting alone, and `product-discovery` for product
requirements research. This skill owns community program design. It does not
replace specialist technical advice or direct an unfolding emergency.

## Choose the entry point

- **Create:** build from a community brief and evidence.
- **Adapt:** inspect the supplied guide, retain useful activities, and explain
  changes caused by the new community's circumstances.
- **Revise:** map feedback and changed facts to specific activities, worksheets,
  and facilitator instructions. Preserve useful material and show the revisions.

Default to editable Markdown. Honor the requested medium and scope: one workshop
may need a single document; a series may need a workbook and separate host notes.
Seven sessions is an example, not a requirement. Do not collect every possible
artifact or impose a structured plan on a short prose-only request.

Scale the process to what can be decided now. When even the topic or community
boundary is unknown, stop before module design: return a brief discovery draft
(roughly one screen, normally under 300 words), at most three essential questions,
and one optional next step. Do not expand that first response into a workbook,
facilitation manual, repeated unknowns tables, or a publication approval process.
Use a longer intake only when requested or needed to resolve known complexity.
For bounded workshops, keep the participant handout short and put research notes
and operational detail in a clearly separate facilitator section.
For a narrow revision or unresolved source conflict, deliver the requested edited
card or decision brief plus concise change/verification notes. Do not add a workshop,
new worksheets, or multiple pilots unless they advance an explicitly requested
learning outcome. A blocked local fact needs a targeted verification step, not a
larger program.
For a bounded revision, use [the revision checklist](templates/revision.md).
Its source-to-action audit and language/version preflight are required before
handoff; an unsupported resident imperative must be removed, not merely flagged.

## Workflow

### 1. Establish the community brief

Extract known facts before asking questions. Use [the brief template](templates/community-brief.md).
Identify who the guide serves, the desired capability, local setting, existing
assets, participation constraints, available time, delivery medium, and guide owner.
Ask only about missing facts that materially change the program. Continue useful
drafting with explicit assumptions when possible; leave location-dependent advice
unresolved when the location or evidence is missing.

An organizer's account is one perspective. Record whose experience is represented
and whose input is still needed. Never invent consultation, consensus, accepted
volunteer roles, or a local service's willingness to help.

Read [localization and evidence](references/localization.md) when researching or
adapting local content. Public research supports factual claims; residents' accounts
support lived constraints and priorities. Both need attribution and appropriate limits.

When the user restricts research to supplied sources, honor that boundary for
technical advice too. If feedback exposes an unsupported safety instruction,
remove or quarantine it and mark the replacement for qualified verification;
do not invent a new procedure from general knowledge. A provisional draft must
not describe proposed verification or services as work already underway. Keep
unsupported safety prose out of resident-facing copy; state that the replacement
is unresolved until an authoritative source is supplied. Any editorial placeholder
belongs in verification notes, not in instructions residents might act on.

### 2. Establish outcomes and dependencies

For each need, trace:

`need → capability → activity → usable output → real action → check`

Choose only modules that support the requested outcomes. Put prerequisite actions
first: inventory before purchasing; agreement about sharing before a directory;
accepted roles before reliance on a contact chain. Use low/no-cost entry actions
and more involved options where useful, without defining effort solely by money.

Read [activity and facilitation design](references/facilitation.md) before writing
a new program. A brief explanation, reflection, shared exercise, debrief, and
feasible next action form the default loop. Adapt it to the available time.

### 3. Write coordinated materials

Use [the module template](templates/module.md) as the common record for participant
and facilitator instructions. Include a completed fictional example and a blank
copy of any unfamiliar worksheet. Make each exercise produce a decision, practice,
map, plan, or other usable result; discussion alone needs a stated purpose.

Provide timing including introductions, interpretation, transitions, and closing.
Name preparation, supplies, instructions, debrief questions, completion checks,
and a fallback when prerequisites or helpers are unavailable. Distinguish private
household records from voluntary shared information.

Translate constraints into actual alternatives: renters need actions within their
control; offline participants need the essential instructions on paper; people
who miss meetings need a catch-up route. Do not assume purchasing power, literacy,
transportation, home ownership, or comfort disclosing personal needs. Translation
needs competent language review; machine translation alone is not evidence of that.
When revising an existing multilingual guide, retain its language coverage unless
the user changes scope. Provide labeled draft translations where needed and identify
the review still required; a promise to translate later does not supply the missing copy.
For source-only revisions, translating supported content is allowed: the source
boundary forbids adding facts, not expressing those facts in another language.
Check the delivered resident copy language by language before handoff. An English
card plus a note promising Spanish later is an incomplete bilingual revision.

Use [the worksheet template](templates/worksheet.md),
[facilitator template](templates/facilitator.md), and
[maintenance template](templates/maintenance.md) as needed. Every proposed shared
role needs a way to obtain acceptance and a fallback if nobody accepts it.

For multi-module or multi-file guides, maintain one structured plan following
[the plan contract](references/guide-plan.md). Use it to keep module IDs, worksheets,
timing, and evidence consistent across materials; do not expose JSON to participants.

### 4. Check and revise

Perform a cold walkthrough: can a new facilitator prepare and run the session
using only these materials? Can a participant complete each worksheet? Check that
the guide and host notes agree, every decision has a next step, and necessary
information is accessible in the intended medium.
Resolve each named or numbered reference against the actual delivered worksheet:
do its sections, checkbox counts, and field labels exist as described? Do not infer
agreement just because both documents discuss the same activity.
For responsibility maps, check for contradictory acceptance claims, overlapping
assignments that exceed stated availability, and backups that rely on the same
unavailable person. Preserve existing accepted scope; mark additional work proposed.

For source-only revisions, audit each resident-facing imperative against a supplied
source. Remove unsupported directions even when they sound prudent (for example,
an invented interim reporting route, waiting instruction, or emergency process).
Use a factual unresolved-status notice instead. Keep historical unsafe wording
only in a clearly labeled retired-source record, never in the active card.

For structured plans, run the read-only checker (Python 3.10+, standard library):

```sh
python3 scripts/validate_guide.py /path/to/guide/plan.json
```

Run from the skill root or resolve the script from its installed location. Read
its JSON diagnostics, fix errors, and account for warnings. This checks records,
file references, and timing; it does not verify facts, prose agreement, translation,
or community usability. Its tests run with:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
```

For PDF/Word output, use available `documents` tooling and inspect rendered pages,
especially worksheets, page breaks, and print readability. If unavailable, deliver
editable content and name the uncompleted rendering check.

Read [review and evaluation](references/review.md) for independent walkthroughs,
pilot design, or skill evaluation. An agent simulation must be labeled as such.

### 5. Hand off and maintain

The entry-point scope rules take precedence over this full-program checklist.
For discovery or a narrow card/decision-brief revision, supply only the requested
artifact and concise verification/change notes. Add maintenance and ownership
records only when the requested artifact or existing package calls for them.

For a full program, deliver the requested guide, relevant facilitator material,
sources and adaptation notes, and a maintenance record. List unresolved local facts and proposed
roles where they affect use. Name an owner or mark ownership unconfirmed, a review
date or trigger, and how feedback should produce revisions.

Completion means requested artifacts exist, applicable checks are reported, and
open dependencies are visible. Say **ready for a community pilot** when only agent
checks have occurred. Claim participant-tested usability only with actual evidence.
If an essential unknown prevents a usable guide, finish independent parts and ask
the specific question needed to proceed; do not invent an answer or claim completion.

This skill produces local artifacts. Sending invitations, collecting residents'
details, changing shared records, or publishing externally changes external state:
**Confirm the target, scope, and rollback path before acting. Read-only discovery
may proceed without confirmation.** Existing explicit authorization can supply that
confirmation; guide creation alone does not authorize those actions.

## Worked example and provenance

Read [the original apartment example](examples/apartment-guide.md) when a complete
brief-to-guide model would help. Its [plan](examples/apartment-plan.json) and
[host notes](examples/apartment-facilitator.md) demonstrate coordination. All people,
constraints, and local evidence in it are fictional; it is not a technical outage manual.

Read [source pattern and attribution](references/source-pattern.md) when adapting
Ready Together. Retain the participatory method while researching technical content
afresh. Do not reproduce the source handbook's text, images, or worksheets without
appropriate permission.
