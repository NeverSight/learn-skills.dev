---
name: release-retrospective
description: "Produce a structured look-back after a major release or deprecation — capturing what the plan got right, what it missed, and what to do differently. Trigger when someone says: release retrospective, post-release review, what went wrong with the release, how did the deprecation go, release post-mortem, retro on the migration, or anything about reviewing how a release or deprecation actually went compared to the plan."
references:
  - ../../knowledge-notes/component-governance.md
---

## Context

Governance currently looks forward: plan the deprecation, estimate the blast radius, write the migration guide. There's no structured skill for reviewing how it actually went. Did the blast radius estimate hold? What did the communication miss? Where did teams get stuck despite the migration guide? A release retrospective completes the governance loop and builds institutional knowledge that keeps a system from repeating the same mistakes across team transitions.

The retrospective is not a blame exercise. It's a learning artifact. The goal is: what changes to our governance process will prevent this specific gap next time? Foreseeable gaps reveal process failures. Unforeseeable gaps become new guardrails.

## Key principles

**From component-governance:** Governance owns the release plan: who's affected, when they're affected, what they need to succeed. The plan is a hypothesis. The retrospective tests it. Blast radius, communication, migration path quality, timeline, and support burden are the five surfaces where plans often break. Each surface has a classification: was this predictable with better analysis, or genuinely novel?

**Key principle for retrospectives:** The plan was made with incomplete information. The retrospective reveals what information was missing. That gap is the insight — not a failure, a discovery.

## Configuration

Before writing the retrospective, gather these inputs:

1. **Release or deprecation:** Component name, token set change, system-level refactor, or major version bump. What changed?
2. **Original plan:** Link to the deprecation plan, migration guide, communication package, or governance decision record. Paste key dates, blast radius estimate, phased rollout plan if one existed.
3. **Actual execution:** When did it ship? What was the actual timeline? Which teams/codebases were affected (names or counts)?
4. **Quantitative data:** Instances affected (actual vs estimated). Migration completion rate. Support tickets or Slack threads related to the change.
5. **Qualitative data:** If quantitative isn't available: "three teams asked the same question about X", "one team skipped the codemod and manually updated", "unexpected platform dependency broke the migration".
6. **Communications received:** Which channels reached teams? Did they read the message? Evidence: Slack emoji reactions, email click-through rates, questions showing people didn't read.
7. **Support load:** How many questions in Slack? Escalations? Pattern categories (e.g., "5 questions about X", "2 teams didn't know about the codemod").
8. **Unplanned events:** Platform changes, team reorganizations, urgent hotfixes, or other novel circumstances that affected the release.

## Steps

**Step 1: Gather inputs**

Collect the original plan (pull it directly, don't reconstruct from memory). Ask system owners and team leads: what actually happened? If you find disparities between the plan and what people remember, note them — that's a communication gap.

Output: A folder or Slack thread with the original plan, timeline notes, and team feedback.

**Step 2: Extract the blast radius dimension**

Compare estimate vs actual.

```
**Blast radius accuracy**

Planned: [X affected consumers, Y estimated instances]
Actual: [A affected consumers, B actual instances]
Gap: [Describe variance — larger, smaller, different teams]

Gap classification: 
  - [ ] Foreseeable — more thorough analysis would have caught this
  - [ ] Unforeseeable — novel circumstance (team reorganization, platform change)
  - [ ] Process — analysis was right, execution diverged (e.g., team didn't update)

Specific gaps:
- [List 1-3 unexpected impacts]

Insight: [One sentence — what should we have known or asked?]
```

**Step 3: Extract the communication dimension**

Assess message clarity and reach.

```
**Communication effectiveness**

Planned channels: [Slack #channel, email, async standup, office hours, etc.]
Actual reach: [% of teams knew before migration deadline, evidence: emoji reactions, replies, etc.]

Gap: [Did teams miss the message? Was it unclear? Did timing matter?]

Gap classification:
  - [ ] Foreseeable — communication plan was incomplete
  - [ ] Unforeseeable — novel (email landed in spam, team lead OOO at critical moment)
  - [ ] Process — communication was sent but not read or acted on

Specific gaps:
- [List examples: "Team X didn't see the Slack message", "Question about X appeared 10 times"]

Insight: [What communication lever do we need next time?]
```

**Step 4: Extract the migration path dimension**

Where did teams get stuck despite the guide?

```
**Migration path quality**

Planned: [Codemod available? Manual steps? Estimated time to update per team?]
Actual: [Did teams run the codemod? Manual updates? Time to complete?]

Gap: [Missing edge cases? Codemod incomplete? Guide unclear?]

Gap classification:
  - [ ] Foreseeable — guide could have covered this
  - [ ] Unforeseeable — novel usage pattern not in our control
  - [ ] Process — guide was clear but not followed

Specific gaps:
- [List 1-3 edge cases or friction points]
  Example: "Teams with custom webpack configs couldn't run the codemod"
  Example: "Migration guide didn't explain how to handle the breaking prop change in unit tests"

Insight: [What process or documentation change prevents this next time?]
```

**Step 5: Extract the timeline dimension**

Did the release stay on schedule?

```
**Timeline adherence**

Planned: [Deprecation announcement date, migration deadline, breaking change date]
Actual: [When did each milestone happen? What caused delays?]

Gap: [Slipped? Accelerated? Why?]

Gap classification:
  - [ ] Foreseeable — dependencies or risks we should have planned for
  - [ ] Unforeseeable — external event (platform outage, urgent security issue)
  - [ ] Process — team capacity or prioritization shifted

Specific gaps:
- [List delays or accelerations with cause]

Insight: [What buffer or dependency should we build into next timelines?]
```

**Step 6: Extract the support burden dimension**

What patterns emerged in questions or escalations?

```
**Support burden**

Planned support: [Proactive FAQ, office hours, Slack monitoring, etc.]
Actual support: [Support tickets count, Slack threads count, time invested by system team]

Question patterns:
- [Category A: X instances — e.g., "How do I update imports?"]
- [Category B: Y instances — e.g., "Does this break our custom theme?"]

Gap: [Were FAQs prepared for these? Escalations that shouldn't have happened?]

Gap classification:
  - [ ] Foreseeable — expected questions not in the FAQ
  - [ ] Unforeseeable — novel question type
  - [ ] Process — FAQ existed but wasn't linked in communication

Specific gaps:
- [List 1-2 unaddressed question categories]

Insight: [What specific FAQ entry or escalation path do we add?]
```

**Step 7: Classify each gap**

For every gap found, mark it foreseeable/unforeseeable/process:

- **Foreseeable:** The analysis was incomplete. Better consumer interviews, more thorough codemod testing, broader platform validation, or edge case exploration would have caught this.
- **Unforeseeable:** A genuinely novel circumstance. Team reorganization, platform release, urgent security incident, or unexpected architectural pattern in a consumer.
- **Process:** The analysis was sound but execution faltered. Communication sent but not read. Migration guide clear but not followed. Timeline understood but capacity wasn't available.

**Step 8: Write the retrospective report**

Use this structure:

```markdown
# Release Retrospective: [Release name]

**Release:** [What shipped — component deprecation, token refactor, major version, etc.]
**Date:** [Announcement → Migration deadline → Completion]
**Status:** [On schedule / Delayed / Completed early]

## Summary

[1 paragraph: What was released, when, what actually happened. 
Overall assessment: did it go as planned?]

Example: "We deprecated the legacy Button component on Jan 15. 
The migration deadline was Feb 28. All discovered consumers completed migration by Feb 25 — 
three days early. Communication reached 85% of likely consumers before the deadline. 
We found two unplanned edge cases in webpack configurations and one incomplete codemod scenario."

## Plan vs Reality

| Dimension | Planned | Actual | Gap | Class |
|---|---|---|---|---|
| **Blast radius** | X teams, Y instances | A teams, B instances | [Describe] | Foreseeable / Unforeseeable / Process |
| **Communication** | [Channels, timing] | [Actual reach %] | [Describe] | Foreseeable / Unforeseeable / Process |
| **Migration path** | [Codemod + manual steps, est. time] | [Actual approach, time] | [Describe] | Foreseeable / Unforeseeable / Process |
| **Timeline** | [Key dates] | [Actual dates] | [Describe] | Foreseeable / Unforeseeable / Process |
| **Support burden** | [Planned support approach] | [Actual load, patterns] | [Describe] | Foreseeable / Unforeseeable / Process |

## What worked well

[2-5 items. Keep doing these next time.]

Example:
- The codemod was complete and handled 95% of cases automatically
- Phased rollout meant we could respond to early feedback before the hard deadline
- Daily office hours during week 1 of migration prevented escalations
- Pre-migration dry-run period (2 weeks) let teams test in their own repos first

## What didn't work

[2-5 items. Stop or change these next time.]

Example:
- FAQ didn't mention webpack configuration workarounds — caused three escalations
- Slack announcement only reached 60% of consumers; email distribution list was outdated
- Migration guide showed code examples for React/Vue but not Svelte consumers
- Support burden on one person created a bottleneck in week 2

## Recommendations for next release

[Specific, actionable changes to governance or process. Each one solves a gap from above.]

Example recommendations:

1. **Add platform-specific migration testing before release announcement.**
   Currently, we test the codemod in our CI. Next time, test in representative consumer 
   repos with webpack, custom Rollup, and other non-standard configs. 
   (Solves: foreseeable gap in webpack compatibility)

2. **Maintain an up-to-date consumer distribution list.**
   Create a process to update email list quarterly (tie to quarterly business review). 
   Test distribution in a dry run before major announcements. 
   (Solves: process gap in communication reach)

3. **Expand FAQ during migration window.**
   Compile new FAQ entries from first-week support questions. 
   Publish mid-migration (day 3-5) for fast-moving teams. 
   (Solves: foreseeable gap in anticipating questions)

4. **Assign dedicated support person + backup.**
   No single point of failure in support. Rotating backup prevents burnout and ensures coverage. 
   (Solves: process gap in support load management)

## Decision record update

[Only if the retrospective reveals a standing decision should change.]

Example: "Decision record D-004 (Release timing strategy) should be updated 
to require platform-specific validation testing. Current guidance assumes 
standard tooling; update to add complexity estimate for non-standard consumer setups."

Link to updated decision record or create one.

---

**Retrospective completed:** [Date]  
**Prepared by:** [Your name/team]  
**Reviewed by:** [System team lead, key consumer representative]
```

## Quality Checks

1. **Every gap is classified:** No gaps listed without foreseeable/unforeseeable/process mark. Classification is clear.
2. **Recommendations are implementation-ready:** Each recommendation can be turned into a task without additional context. Not "communicate better" but "add platform-specific migration testing to CI before release announcement."
3. **Plan vs reality references original plan:** Not reconstructed from memory. Links to or quotes from the actual plan document.
4. **At least one "what worked" finding:** Retros that are entirely negative are incomplete and demoralizing. Even a problematic release had something worth repeating.
5. **Support burden identifies patterns, not just totals:** "5 questions about X" is better than "20 total support questions." Patterns drive recommendations.
6. **Shareable with stakeholders:** Report is complete enough to send to leadership and consumer leads without additional editing or context.

## Small-system note

For very small system releases (single component deprecation, single token rename):

- Compress the report to a single page: one-line summary per dimension, one "what worked", one "what didn't", one recommendation.
- Skip the table format if there's only one or two gaps total; use prose instead.
- Tie the recommendation directly to the next release (e.g., "next time we deprecate a component, use this checklist").
- Focus on process: small releases have small blast radii, so insights are mostly about governance efficiency, not breadth.
