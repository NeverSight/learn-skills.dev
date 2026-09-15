---
name: dev-event-hiring
description: Employer-side hiring for tech-event-organizing roles - producer/manager/coordinator, and the community-manager-shaped end of the field. Calibrates the scorecard to operating context (in-house, agency, non-profit/community, or a standing conference business), builds the loop from the general event-planner sequence plus CMX's five-competency set and paid mini-audit work sample, flags the "one hire owns sponsorship, content and production" consolidation pattern seen in postings, sources candidates from general event-industry boards since no tech-specific one exists, and gates compensation on named sources (PCMA, BLS, Glassdoor) rather than a blended figure. Use when the user asks how to hire an event producer or manager, write a posting, design a loop, or hire an event community manager. Do NOT use for candidate prep (samber/dev-event-organizer-skills@dev-event-career) or team org design (samber/dev-event-organizer-skills@event-team-structure).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Dev Event Hiring

Build the artefacts a hiring manager needs to recruit a tech-event-organizing role: a scorecard calibrated to operating context, an interview loop assembled from the field's real (if partial) evidence, a sourcing plan, and a compensation stance that names its source instead of blending numbers.

Out of scope, hand off instead:

- **Coaching the candidate** - samber/dev-event-organizer-skills@dev-event-career is the mirror image of this skill.
- **The standing organizing team's own structure** - legal entity, decision rights, succession, the volunteer-to-paid threshold - samber/dev-event-organizer-skills@event-team-structure. Route "should we hire our first paid role at all" there; this skill answers "how do we hire well, once we've decided to."

If the user is job-hunting rather than hiring, say so in one line and route them to dev-event-career.

## Interview

Ask one question at a time, multiple-choice where possible. Skip anything already answered. Questions 7-9 re-rank the artefacts below.

1. Operating context: (a) in-house at a company running its own conference or meetup series (b) an event-production agency hiring for client work (c) a non-profit/foundation or volunteer-community-run event making its first paid hire (d) a standing for-profit conference business.
2. Target role shape: (a) producer/logistics-and-production-focused (b) manager, blending production and stakeholder management (c) community-manager-shaped (meetup organizer, developer-community-events hybrid) (d) undecided - recommend one from the scope.
3. For a non-profit/community-run event: has the event crossed roughly low-thousands of attendees or a six-figure budget - the threshold where a first paid role typically appears? (If not, route to event-team-structure first - this may be premature.)
4. What does this role need to be measured on - attendee satisfaction, on-budget delivery, sponsor renewal, community growth, repeat-attendee rate?
5. How many people and what budget will this role actually have - solo ownership, a small team, or shared with existing staff?
6. Compensation stance: do you have a range in mind, and do you know which source (PCMA, BLS, Glassdoor tech-industry data) you're anchoring it to?
7. Deadline: this month, this quarter, or no hard date?
8. One-off hire or the first of several where the scorecard and loop get reused?
9. Effort ceiling: how many interviewer-hours per candidate, and is there a recruiter?

## Reading the answers

- **Q1 decides the scorecard template and realistic scope** - load [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md). An in-house hire needs cross-functional fluency (sales, marketing, product); an agency hire is screened against a specialized function inside a client-services structure; a non-profit/community hire is almost always an event coordinator/manager, never a community-manager role, at the first-paid-hire stage.
- **Q2 decides which interview design applies** - a community-manager-shaped role should use CMX's five-competency loop (see Workflow); a producer/manager-shaped role uses the general event-planner sequence.
- **Q3 is a gate, not just a data point.** If the threshold hasn't been crossed, the real question may be whether to hire at all, which is samber/dev-event-organizer-skills@event-team-structure's decision, not this skill's - say so before building a scorecard for a premature hire.
- **Q4 sets the scorecard's outcome metrics** - never write a generic "run great events" outcome; name the actual thing this role is measured on.
- **Q5 is the check against this field's real red-flag pattern** (see Reading a posting for red flags below): a solo hire expected to own sponsorship sales, content, and production simultaneously with no team or budget is the consolidation pattern job postings already show.
- **Q6 triggers the compensation gate** in the Quality gate - never quote one blended number; name PCMA, BLS, or Glassdoor explicitly, and state the tech-industry premium if hiring in-house.
- **Q7 promotes reusing an existing loop over designing one from scratch.**
- **Q8 decides whether the loop stays thin (one-off) or gets built properly (compounding).**
- **Q9 deletes loop stages rather than reordering them**, the same way sales-hiring and devrel-hiring treat a tight interviewer-hour budget.

## Workflow

1. Run the Interview. State the operating context and role-shape calibration in one short paragraph the user can veto.
2. **Artefact 1 - role scorecard.** Build from [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md):
   - a one-sentence mission naming the operating context and the metric from Q4
   - 3-8 measurable outcomes, never vague responsibilities like "run great events"
   - competencies weighted per role shape - a community-manager-shaped scorecard should use CMX's five competencies (growth mindset, data-driven approach, empathy, leadership, communication); a producer/manager scorecard should weight portfolio quality, budget management, and vendor/client relations
3. **Artefact 2 - interview loop.** Build from [references/interview-loop-design.md](./references/interview-loop-design.md):
   - for a producer/manager-shaped hire, the general event-planner sequence applies: portfolio and past-events review first, a concrete-metrics request, scenario-based questions (a last-minute venue change, a vendor no-show), budget-management questions, and live reference calls rather than written recommendations
   - for a community-manager-shaped hire, use CMX's five-competency question set, including the pointed conflict question ("if the community wants one thing and your boss wants something else, what would you do?")
   - place a work-sample stage appropriately: a **paid mini-audit** of an existing community for a senior community-manager-shaped hire, or a **sample-thread-response exercise** for a junior/moderator-track one - never unpaid, open-ended client-style work for a producer/manager hire
   - state plainly that no single, fully-documented tech-conference-specific loop exists published anywhere - this is an assembled design, not a copy of an industry-standard one
4. **Artefact 3 - sourcing plan.** Build from [references/sourcing-channels.md](./references/sourcing-channels.md):
   - use general event-industry boards (PCMA Career Center, MPI Career Center, BizBash, MeetingJobs/Cadre, Event Careers) since no dev/tech-conference-specific board exists
   - for a community-manager-shaped role, the CMX Job Board and its Slack community are the closest tech-adjacent channel
5. **Artefact 4 - compensation stance.** Build from [references/compensation-guidance.md](./references/compensation-guidance.md):
   - name the source explicitly - PCMA Convene's level-based figures, BLS's broad occupational median, or Glassdoor's tech-industry-premium cut for an in-house tech-company hire
   - never blend sources into one number; state which one the offer is anchored to and why
6. Run the Quality gate below. Iterate until it passes.
7. If your harness has persistent memory, store the scorecard, loop design and sourcing plan for reuse on a repeat hire.

## Reading a posting for red flags

**No named "pit-trap"-style taxonomy exists yet for event-organizing hiring**, unlike DevRel's documented Joe Nash gatekeeper/pit-trap framework - say this plainly rather than citing a pre-existing source that doesn't exist. What real job-posting evidence does show is the same consolidation pattern DevRel names for its own field, applied here as a labeled transposition, not a second independently-discovered instance of it:

- **The gatekeeper equivalent**: a posting describing an impossible person - deep sponsorship-sales closing ability, hands-on AV/production expertise, CFP/content-curation judgment, and day-of crisis management - at entry-level pay and an individual-contributor title.
- **The pit-trap equivalent**: "founding event manager, no team, no budget, full ownership" language, asking one hire to run sponsorship sales, content, production, and volunteer/staff management simultaneously with no stated success metric, no reporting structure, and no stated path to headcount.

Before publishing a posting, self-audit against both patterns. A posting failing either needs the scope split across more than one hire, or the resourcing stated explicitly, before it goes out.

## Company type and role-shape calibration

Never treat one scorecard template as portable across operating contexts - the full comparison and the honest note on the unsourced fourth context (a standing for-profit conference business) live in [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md).

## Quality gate

Score the artefacts against these checks before final delivery.

1. The scorecard names the actual operating context and the metric this role is measured on, and every outcome is quantified.
2. The posting passes the gatekeeper/pit-trap self-audit - no impossible-person requirement list, no unresourced "full ownership" framing.
3. The interview design matches the role shape - CMX's five competencies for a community-manager-shaped hire, the general event-planner sequence for a producer/manager-shaped one.
4. Any work-sample stage is bounded and paid, never open-ended unpaid client work.
5. For a non-profit/community first paid hire, the threshold question (Q3) was actually asked, not assumed.
6. Sourcing uses named, real channels - general event-industry boards, or CMX specifically for a community-manager-shaped role - never an invented "tech-event job board."
7. The compensation stance names its source (PCMA, BLS, or Glassdoor) explicitly; no blended, unsourced figure is presented as market rate.

## Common failure modes

| Failure                                                                               | Fix                                                                                          |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Solo hire expected to own sponsorship, content, and production with no team or budget | Split the scope across more than one hire, or state the resourcing explicitly in the posting |
| Copying an agency-style specialized scorecard for a first non-profit/community hire   | Recalibrate against the actual operating context and the coordinator/manager-first pattern   |
| Using CMX's community-manager loop for a pure production/logistics hire               | Match the loop to the actual role shape, not the nearest documented one                      |
| Unpaid, open-ended "test project" as a work sample                                    | Use a bounded, paid mini-audit or sample-thread-response exercise instead                    |
| Quoting one blended salary figure with no named source                                | State PCMA, BLS, or Glassdoor explicitly, and the tech-industry premium if relevant          |
| Inventing a tech-specific job board that doesn't exist                                | Use the real general event-industry boards, or CMX for community-manager-shaped roles        |
| Hiring a first paid role at a community event before the threshold is reached         | Route to event-team-structure first to confirm the hire is warranted                         |

## Reference

- [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md) - the four operating contexts, what differs concretely, and the unsourced fourth context flagged honestly.
- [references/interview-loop-design.md](./references/interview-loop-design.md) - the general event-planner sequence, CMX's five-competency set, and the paid work-sample designs.
- [references/sourcing-channels.md](./references/sourcing-channels.md) - the named general event-industry boards and the CMX community-manager channel.
- [references/compensation-guidance.md](./references/compensation-guidance.md) - PCMA, BLS, and Glassdoor tables, named separately.
- See `samber/dev-event-organizer-skills@dev-event-career` for the candidate's side of this table.
- See `samber/dev-event-organizer-skills@event-team-structure` for whether to hire at all, and the standing team's decision rights once this role is filled.
- See `samber/developer-relations-skills@devrel-hiring` for a community-manager-shaped hire that leans more DevRel than event-production - the two skills' scorecards can cross-check each other.
