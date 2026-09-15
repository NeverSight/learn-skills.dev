---
name: developer-platform-hiring
description: Employer-side hiring for developer-platform roles - API Product Manager, Platform Engineer/Architect, Partner/Integration Engineer. Disambiguates "platform engineer" first, since the term overwhelmingly means internal developer platforms elsewhere in the industry. Calibrates the scorecard to company archetype (infra/API-first, bolt-on public API, enterprise partner ecosystem), flags a scope-collapse pattern distinct from DevRel's gatekeeper/pit-trap taxonomy, sources from apidays, not PlatformCon's internal-IDP audience, builds the loop from the API-design-vs-system-design interview split, and benchmarks compensation against the general engineering/PM ladder rather than a bespoke platform title. Use when the user asks how to hire a platform engineer, API product manager, or partner/integration engineer, write a posting, or design a loop. Do NOT use for candidate prep (samber/developer-platform-skills@developer-platform-career) or DevRel hiring (samber/developer-relations-skills@devrel-hiring).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Developer Platform Hiring

Build the artefacts a hiring manager needs to recruit a developer-platform role: a scorecard calibrated to the company's own archetype, an interview loop built on the API-design-vs-system-design split this field actually uses, a sourcing plan, and a compensation stance anchored to the general engineering or PM ladder rather than a bespoke platform title.

Out of scope, hand off instead:

- **Coaching the candidate** - samber/developer-platform-skills@developer-platform-career is the mirror image of this skill.
- **Hiring a developer advocate, community manager, developer educator, or DevRel's own flavor of DX engineer** - samber/developer-relations-skills@devrel-hiring. Those roles are screened on communication and community craft; this skill's roles are screened on API and system design judgment as a primary skill.

If the user is job-hunting rather than hiring, say so in one line and route them to developer-platform-career.

## Disambiguate "platform engineer" first

"Platform engineer" and "platform engineering" overwhelmingly mean **internal developer platforms** elsewhere in the industry: self-service infrastructure, CI/CD, Kubernetes abstractions, golden paths built for a company's own application engineers. PlatformCon, the flagship community for that term, serves exactly that audience at a scale of 280,000+ practitioners - and covers none of what this skill hires for.

Ask, before building anything: who is the primary consumer of what this role builds - the company's own engineering teams, or developers outside the company (customers, partners, third-party app builders)? Internal consumer -> internal-platform engineering, entirely outside this skill's scope. External consumer -> this skill.

Posting a role or searching for candidates on PlatformCon-adjacent channels (Backstage community, internal-IDP job boards) surfaces the wrong applicant pool for an external-API-platform hire.

## Interview

Ask one question at a time, multiple-choice where possible. Skip anything already answered. Questions 7-9 re-rank the artefacts below.

1. Company archetype: (a) an infrastructure/API-first company where the API is the product (b) a company bolting a public API onto an existing product (c) an enterprise platform with a large partner/ISV ecosystem (d) undecided - recommend one from the description of the role.
2. Target role track: (a) API Product Manager (b) Platform Engineer/Architect (c) Partner Engineer, relationship-facing (d) Integration Engineer, architecture-focused (e) undecided.
3. How many people currently own the API surface end to end - is this a first dedicated hire, or an addition to an existing platform team? (Postman's data puts 84% of API teams at 1-9 people; a first dedicated hire for a bolt-on company is a real resourcing shift, not a routine backfill.)
4. What does this role need to be measured on - API design quality and contract stability, roadmap and monetization outcomes, or named partner-facing metrics (partners supported, integrations shipped, usage growth)?
5. How many people and what budget will this role actually have - solo ownership, a small team, or shared with existing engineering staff?
6. Compensation stance: do you have a range in mind, and is it anchored to the company's general engineering/PM ladder or to a bespoke "platform engineer" search?
7. Deadline: this month, this quarter, or no hard date?
8. One-off hire or the first of several where the scorecard and loop get reused?
9. Effort ceiling: how many interviewer-hours per candidate, and is there a recruiter?

## Reading the answers

- **Q1 decides the scorecard template and realistic bar** - load [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md). An infra/API-first hire needs the highest technical depth; a bolt-on hire is usually folded into general backend hiring rather than a dedicated specialist search; an enterprise-ecosystem hire needs the relationship-plus-technical hybrid GitLab's job family screens for.
- **Q2 decides which loop design applies** - see Workflow below for the per-track interview shape.
- **Q3 is the scope-collapse check, not just a data point.** If the answer is "one person will own design, partner integrations, and developer-facing content," the posting is very likely asking for three full-time jobs in one seat - see Reading a posting for red flags below.
- **Q4 sets the scorecard's outcome metrics** - never write a generic "own the API" outcome; name the actual thing this role is measured on.
- **Q5 is the check against the field's real red-flag pattern**: a solo hire expected to own API design, partner integrations, and developer-facing marketing simultaneously with no team or budget is the consolidation pattern this field's structural data implies.
- **Q6 triggers the compensation gate** in the Quality gate - anchor to the general engineering or PM ladder at the equivalent level, never to a bespoke platform-title search.
- **Q7 promotes reusing an existing loop over designing one from scratch.**
- **Q8 decides whether the loop stays thin (one-off) or gets built properly (compounding).**
- **Q9 deletes loop stages rather than reordering them**, the same way sales-hiring and devrel-hiring treat a tight interviewer-hour budget.

## Workflow

1. Run the Interview. State the company-archetype and role-track calibration in one short paragraph the user can veto.
2. **Artefact 1 - role scorecard.** Build from [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md):
   - a one-sentence mission naming the archetype and the metric from Q4
   - 3-8 measurable outcomes, never vague responsibilities like "own the platform"
   - competencies weighted per track - API PM scorecards weight roadmap and monetization judgment; Platform Engineer/Architect scorecards weight API/system design and infra delivery; Partner Engineer scorecards weight relationship management; Integration Engineer scorecards weight architecture and reliability
3. **Artefact 2 - interview loop.** Build from [references/interview-loop-design.md](./references/interview-loop-design.md):
   - use the API-design interview format (distinct from general system design at major companies) for engineering-track hires, judged on developer-facing usability and misuse-resistance rather than raw scale trade-offs
   - for an API PM, weight a scoping and design-thinking round over a coding round, per how Google and Uber run their own PM loops
   - for a Partner/Integration Engineer, reuse GitLab's real posted sequence: recruiter call, hiring-manager interview, 2-5 team interviews, a possible executive round for senior hires
   - state plainly that no single, fully-documented developer-platform-specific loop exists published anywhere for every track - this is an assembled design, not a copy of an industry-standard one
4. **Artefact 3 - sourcing plan.** Build from [references/sourcing-channels.md](./references/sourcing-channels.md):
   - use apidays as the confirmed venue for API platform engineers and API product managers - never PlatformCon, which serves the internal-IDP population
   - for Platform Engineer and Integration Engineer tracks, general senior-backend-engineering sourcing channels (referral networks, senior-IC pipelines, open-source contribution history as a screen) outperform DevRel-adjacent channels
   - for the API PM track, use general technical product-management sourcing filtered for API or developer-facing product experience
5. **Artefact 4 - compensation stance.** Build from [references/compensation-guidance.md](./references/compensation-guidance.md):
   - anchor the offer to the company's general software-engineering or general product-management comp bands at the equivalent level - never to a bespoke "platform engineer" or "API product manager" title search, which returns sparse crowdsourced data
   - name GitLab's or Stripe's own leveling structure as the sourced example, never as a universal standard
6. Run the Quality gate below. Iterate until it passes.
7. If your harness has persistent memory, store the scorecard, loop design and sourcing plan for reuse on a repeat hire.

## Reading a posting for red flags

**No named, sourced hiring-red-flag taxonomy exists yet for developer-platform roles**, unlike DevRel's documented gatekeeper/pit-trap framework - say this plainly rather than citing a source that doesn't exist. What the structural data does support is a distinct pattern, not the same one relabeled:

- **The pattern**: a posting stacking **build work** (API/schema design, partner integration architecture) with **outreach work** (developer marketing, content) - a scope-collapse across disciplines rather than within one discipline. Unlike DevRel's gatekeeper pattern, each individual skill listed can be genuinely held by one strong candidate; the failure is an execution-volume mismatch across three full-time jobs, not an impossible-skills list.
- **Symptoms**: the posting names outcomes belonging to three different functions (a shipped API surface, a named partner-integration count, a content or community metric) with no stated headcount plan to eventually split them; the title implies IC-engineering seniority but the responsibilities read as a product-manager's job plus a DevRel job layered on top; no named reporting line or budget is stated for growing the function past one person.

State plainly that this pattern is a structural inference from Postman's small-team data and cross-repo analogy to DevRel's taxonomy, not a named, quoted industry diagnosis - unless a follow-up check finds a genuine sourced account. Before publishing a posting, self-audit against it; a posting failing the test needs the scope split across more than one hire, or the resourcing stated explicitly, before it goes out.

## Company type and role-track calibration

Never treat one scorecard template as portable across company archetypes - the full comparison and the 84%-small-teams finding live in [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md).

## Quality gate

Score the artefacts against these checks before final delivery.

1. The posting or scorecard states explicitly whether the role means internal-IDP or external-API platform engineering.
2. The scorecard names the actual company archetype and the metric this role is measured on, and every outcome is quantified.
3. The posting passes the scope-collapse self-audit - no build-plus-outreach stack with no stated headcount plan.
4. The interview design matches the role track - the API-design format for engineering tracks, a scoping/design-thinking round for the PM track, GitLab's structured sequence for Partner/Integration Engineer.
5. Sourcing uses apidays or general senior-backend/PM channels as appropriate - never PlatformCon for an external-API hire.
6. The compensation stance is anchored to the company's general engineering or PM ladder, with a named source and date, never a blended or bespoke-title-searched figure presented as market rate.

## Common failure modes

| Failure                                                                                                                              | Fix                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Sourcing on PlatformCon or internal-IDP channels for an external-API-platform hire                                                   | Use apidays and general senior-backend/PM channels instead                                       |
| Solo hire expected to own API design, partner integrations, and developer-facing content with no team or budget                      | Split the scope across more than one hire, or state the resourcing explicitly in the posting     |
| Copying a general system-design interview for an API-design-judgment role                                                            | Use the API-design format, judged on developer-facing usability and misuse-resistance            |
| Quoting a bespoke "platform engineer" salary figure from a crowdsourced site                                                         | Anchor to the company's general engineering/PM ladder at the equivalent level                    |
| Treating GitLab's or Stripe's posted structure as a universal industry standard                                                      | State it as the one sourced example, not a standard                                              |
| Hiring three specialized roles (API PM, architect, partner engineer) at a company where 1-9 people already run the whole API surface | Confirm the archetype first and size the hire to the actual team, per the company-type reference |

## Reference

- [references/company-type-hiring-bar.md](./references/company-type-hiring-bar.md) - the three company archetypes, the 84%-small-teams finding, and the scope-collapse precondition.
- [references/interview-loop-design.md](./references/interview-loop-design.md) - the API-design-vs-system-design split, per-track loop designs, and GitLab's real posted sequence.
- [references/sourcing-channels.md](./references/sourcing-channels.md) - apidays, the PlatformCon caveat, and why this pool sources more like senior backend engineering than DevRel.
- [references/compensation-guidance.md](./references/compensation-guidance.md) - the general-ladder finding in full, and what to check for a live figure.
- See samber/developer-platform-skills@developer-platform-career for the candidate's side of this table.
- See samber/developer-relations-skills@devrel-hiring for a DevRel-shaped hire that a posting may be conflating with a platform hire - the scope-collapse red flag above is this collision's usual symptom.
