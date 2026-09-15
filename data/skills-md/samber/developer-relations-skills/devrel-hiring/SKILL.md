---
name: devrel-hiring
description: Employer-side DevRel hiring - writes the job posting and outcome-based scorecard, designs the interview loop and question bank across the field's formats (presentation round, take-homes, DevRel-opinion round), scores a portfolio against the six-signal rubric, designs a paid work sample instead of unpaid spec work, and builds a 30-60-90 ramp anchored on a friction log. Splits by company type and funding driver. Use when the user asks how to hire a developer advocate, write a DevRel job posting, design a loop for a community manager or educator, evaluate a candidate's portfolio, or plan a ramp. Do NOT use for candidate-side prep (samber/developer-relations-skills@devrel-career) or org design (samber/developer-relations-skills@devrel-team-structure).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Hiring

Build the four artefacts a hiring manager needs to recruit into a DevRel role with the same rigour the field's own hiring research recommends: a role scorecard and posting, a structured interview loop with question bank, a portfolio-and-work-sample evaluation, and a 30-60-90 ramp plan.

DevRel has no standard job description or career ladder (Chris Aniszczyk, CNCF CTO), and its own hiring literature documents two named failure patterns in postings written without this discipline - see Reading the answers. That absence is the reason to build these four artefacts deliberately rather than adapt a generic engineering or marketing hiring template.

Out of scope, hand off instead:

- **Where DevRel reports and how the team is shaped** - samber/developer-relations-skills@devrel-team-structure decides the org before this skill recruits into it.
- **Coaching the candidate** - samber/developer-relations-skills@devrel-career is the mirror image of this skill, built for the person being evaluated.

If the user is job-hunting rather than hiring ("how do I prep for a DevRel interview", "is this posting worth applying to"), say so in one line and point them at devrel-career.

## Interview

Ask one question at a time, multiple-choice where possible. Skip anything already answered. Questions 8-10 re-rank the artefacts below before any is built - ask them before producing anything.

1. Company type: (a) early startup, pre-seed-A, this will be a team of one (b) growth/scale-up, B-D (c) big-tech enterprise (d) OSS-first company or foundation.
2. Role target: (a) developer advocate, outreach-focused (b) developer advocate, product-focused (c) community manager (d) developer educator (e) DX engineer (f) not sure - recommend one from the funding driver.
3. What funds this role - the driver behind the budget: developer adoption, sales enablement, developer enablement, product input, ecosystem/partnerships, contributor community, or employer branding?
4. Go-to-market motion: sales-led B2B, product-led (PLG) B2B, B2C/individual-facing, or OSS/foundation with no purchase gate.
5. Coding-depth requirement: does this role need to ship SDK samples and review API design, or is the bar public communication with only light code?
6. Team stage: first DevRel hire with no incumbent to calibrate against, or a repeatable hire with existing top performers to profile from?
7. Compensation stance: will you publish a range in the posting, and do you know your hiring jurisdiction's pay-transparency requirement?
8. Deadline: this month, this quarter, or no hard date?
9. One-off hire or the first of several where the scorecard and question bank get reused?
10. Effort ceiling: how many interviewer-hours per candidate, and is there a recruiter or a trained panel?

## Reading the answers

- **Q1 sets the bar and the portfolio weighting** - load [references/company-type-and-driver-lookup.md](./references/company-type-and-driver-lookup.md). A startup hires a generalist who justifies the function's own existence; big tech anchors the role to its engineering levelling scale; an OSS/foundation role screens on contribution history, not communication polish.
- **Q2 + Q3 decide what the posting is screened on** - see [references/company-type-and-driver-lookup.md](./references/company-type-and-driver-lookup.md) for the per-role requirement table. A candidate who cannot say which sub-role they target is applying to all and matching none; the same is true of a posting that cannot say which sub-role it needs.
- **Q3 + Q4 decide the pillar mix and therefore the metric the role is measured on**: sales-led promotes advocacy plus sales enablement; PLG promotes enablement plus product input; B2C promotes community plus reach; OSS/foundation promotes community plus advocacy.
- **Before drafting the posting, self-audit it against the field's two named failure patterns** (Joe Nash, DevRelCon 2021 - the same taxonomy devrel-career teaches candidates to detect from the outside):
  - **Gatekeeper** - describing an impossible person: a full engineering career across several stacks plus OSS contribution, technical writing, community building and event organising, advertised at entry pay.
  - **Pit trap** - "founding DevRel, no background required" that actually expects one person to cover docs, SDKs, community, support, sales engineering, and training with no resources, no ladder and no stated goal.
  - Both share three symptoms: off-core skills emphasis, a tactics list with no stated outcome, and levelling that is inconsistent with the pay. A posting failing any symptom needs a rewrite before it goes out, not after it fails to convert.
- **Q6 decides the candidate profile.** First hire: a builder who can justify the function's existence without an incumbent team, similar to a company's first sales hire - weight self-direction and breadth over specialised depth. Repeatable hire: profile from the org's own top performers on the pillar this role actually owns.
- **Q7 triggers the compensation gate** in the Quality gate below - never invent a jurisdiction's legal requirement; confirm current pay-transparency rules for the hiring location before publishing.
- **Q8 promotes the fast-acting options**: a this-month deadline promotes reusing an existing question bank and a shorter loop over designing a new custom work sample from scratch.
- **Q9 decides whether the work sample stays thin.** One-off: design it once, cheaply. Compounding: the frozen rubric and question bank serve every future hire in this pillar, which promotes building both properly first.
- **Q10 deletes loop stages rather than reordering them.** Under a handful of interviewer-hours per candidate: cut to a scorecard, one structured conversational round, and the portfolio evaluation; skip a live work sample entirely rather than running it unscored.

## Workflow

Produce the four artefacts in order. Deliver each one, validate it with the user, then move to the next.

1. Run the Interview. State the role and pillar-mix recommendation in one short paragraph the user can veto.
2. **Artefact 1 - role scorecard and posting.** Build from [references/company-type-and-driver-lookup.md](./references/company-type-and-driver-lookup.md) and [references/scorecard-and-posting-template.md](./references/scorecard-and-posting-template.md):
   - a one-sentence mission naming the funding driver from Q3
   - 3-8 measurable outcomes ranked by importance and quantified (e.g. "cut top-three onboarding support threads 25% via a shipped friction-log fix", "40 accepted CFPs sourced from the community in year one"), never vague responsibilities
   - 5-7 competencies weighted per the role and company type from Q1-Q2
   - run the gatekeeper/pit-trap self-audit above before publishing
3. **Artefact 2 - interview loop and question bank.** Build from [references/interview-loop-and-question-bank.md](./references/interview-loop-and-question-bank.md):
   - pick 3-5 formats from the field's verified set (presentation round, content take-home, coding take-home, technical self-rating, conversational rounds, DevRel-opinion round, founder/exec round at startups) - there is no standard loop, so choose formats that actually test this role's pillar mix, never the whole set by default
   - place the portfolio evaluation (Artefact 3) early, before any new work is requested of the candidate
   - write 2-3 questions per scorecard competency from the category banks in the reference file, plus at least one DevRel-opinion question - candidates report it as the hardest round because it has no memorised answer, which is exactly why it separates a position from a rehearsed pitch
   - define scoring mechanics: every interviewer scores independently with an evidence note before any debrief, then combine mechanically against the scorecard's pre-set weights - a general employment-selection finding (structured, independently-scored, mechanically-combined interviews outperform unstructured ones and holistic debriefs), not one specific to DevRel, but it transfers directly since nothing about the finding is domain-specific
   - never request unpaid spec work when a public portfolio already exists; offer a paid live working session instead
4. **Artefact 3 - portfolio and work-sample evaluation.** Build from [references/portfolio-and-work-sample-scoring.md](./references/portfolio-and-work-sample-scoring.md):
   - score the candidate's shipped public work against the six-signal distribution rubric (public writing, public speaking, code in public, community evidence, teaching artefact, developer-voice artefact), weighted by the target sub-role from Q2 - the full rubric and its scoring bands live in devrel-career; this skill applies it from the evaluator's side
   - when the portfolio is thin or the candidate is new to the field, design a scored, paid work sample instead of judging by resume alone - a short lightning-talk round, a documentation-edit exercise, or an "explain this API change to a developer" exercise, matched to the target sub-role
   - name the negative signals explicitly when present (follower count with no substance, only self-promotion, no shipped code, inability to name a developer helped) rather than only listing what is missing
5. **Artefact 4 - 30-60-90 ramp plan.** Build from [references/ramp-plan-template.md](./references/ramp-plan-template.md):
   - Day 0-30: the new hire uses the product as a developer would and ships a friction log - the same artefact devrel-career recommends as a portfolio piece, now the first-30-days deliverable
   - Day 31-60: first public or internal artefact shipped in the target pillar, paired with an existing team member
   - Day 61-90: self-directed ownership of one recurring program slice, plus a documented plan for the metric the role's funding driver is measured on
6. Note candidate-sourcing channels from [references/sourcing-channels.md](./references/sourcing-channels.md) if the user has not yet identified where to find candidates.
7. Run the Quality gate below on all four artefacts. Iterate until it passes.
8. If your harness has persistent memory, store the scorecard, the frozen question bank, the loop design and the ramp milestones so later hires into the same role reuse them instead of restarting.

## Company type and funding driver

Never treat a posting template as portable across company types: the same title means a different job at a startup, a growth-stage company, a big-tech vendor, and an OSS-first foundation, and each expects a different portfolio bar and coding depth. The full comparison table, the four pillars, and the seven funding drivers that predict what a role is measured on: [references/company-type-and-driver-lookup.md](./references/company-type-and-driver-lookup.md).

Foundation and OSS-adjacent ambassador-style roles are frequently unpaid and gated on measurable contribution rather than communication skill - confirm which kind of role this is before writing a salaried posting's requirements into an unpaid program, or the reverse.

## Quality gate

Score the four artefacts against these checks before final delivery. Iterate until every check passes.

1. The scorecard has 3-8 outcomes, every one quantified and ranked, and names the funding driver from Q3.
2. The posting passes the gatekeeper/pit-trap self-audit: no off-core skills emphasis, no tactics-without-outcomes list, levelling consistent with the stated pay.
3. Every interview question maps to a named scorecard competency; the same question set applies to every candidate for the role.
4. The loop includes at least one format that actually tests the target pillar (a presentation round for outreach-heavy roles, a coding take-home for DX/product-focused roles), never a generic set copied regardless of role.
5. No stage asks for unpaid spec work when public portfolio evidence already exists.
6. Interviewers submit independent, evidence-noted scores before any debrief; the final combination is mechanical against pre-set weights.
7. The portfolio evaluation is scored against the six-signal rubric, weighted by target sub-role, with negative signals named explicitly where present.
8. If a live work sample was designed, it is scored on a fixed rubric and paid, never treated as free trial work.
9. The posting states a real compensation stance (a published range, or an explicit note on why it is gated) consistent with the Q7 jurisdiction answer - never publish "competitive" with no figure and no stated reason.
10. The ramp plan contains a day-30 friction-log deliverable, a day-60 shipped-artefact milestone, and a day-90 self-directed-ownership milestone.
11. Every claim about "what good looks like" in this skill's own output is traceable to a named source or explicitly marked as this skill's own working assumption - this field has no single authoritative career-ladder body, so an unlabelled claim reads as more settled than it is.

## Common failure modes

Not ranked, deliberately: every row is a defect with one mandatory fix.

| Failure                                                | Fix                                                                                                                      |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Gatekeeper posting                                     | Cut the off-core requirement list to what the pillar mix actually needs; re-price the level against the real requirement |
| Pit-trap posting                                       | State the resources, the ladder and the twelve-month goal explicitly, or postpone the hire until they exist              |
| Copying a generic engineering or marketing JD template | Rebuild from the funding driver and pillar mix; DevRel's outcomes and competencies do not map onto either template       |
| Judging by resume instead of shipped work              | Run the six-signal portfolio evaluation before any conversational round                                                  |
| Unpaid spec-work audition                              | Offer a paid live working session or judge the existing public portfolio instead                                         |
| One blended gut score after a group debrief            | Independent, evidence-noted scores before any discussion, combined mechanically                                          |
| Applying the same loop to every DevRel sub-role        | Choose formats and questions per the target sub-role's actual screened requirements                                      |
| "Competitive compensation", no range, no reason        | Publish a range or state explicitly why it is gated, checked against the jurisdiction's own current requirement          |
| Ramp plan with no artefact milestone                   | Anchor day 30 on a shipped friction log, day 60 on a shipped pillar artefact, day 90 on self-directed ownership          |
| Treating a title as portable across company types      | Recalibrate the whole scorecard against Q1's company-type row before reusing any prior posting                           |

## Reference

- See [references/company-type-and-driver-lookup.md](./references/company-type-and-driver-lookup.md) for the company-type comparison table, the four pillars, and the seven funding drivers.
- See [references/scorecard-and-posting-template.md](./references/scorecard-and-posting-template.md) for the scorecard structure and a worked posting example.
- See [references/interview-loop-and-question-bank.md](./references/interview-loop-and-question-bank.md) for the format table, per-role loop design, and the category-organised question bank.
- See [references/portfolio-and-work-sample-scoring.md](./references/portfolio-and-work-sample-scoring.md) for the six-signal scoring application and paid work-sample designs.
- See [references/ramp-plan-template.md](./references/ramp-plan-template.md) for the full 30-60-90 template.
- See [references/sourcing-channels.md](./references/sourcing-channels.md) for where DevRel candidates are actually found.
- See `samber/developer-relations-skills@devrel-career` for the candidate's side of this table - portfolio building, interview prep, offer evaluation; this skill never coaches candidates.
- See `samber/developer-relations-skills@devrel-team-structure` for the org design and reporting line this role is recruited into - decided before, not by, this skill.
- See `samber/developer-relations-skills@devrel-metrics` for the measurement framework the scorecard's outcomes should stay consistent with once the hire is in seat.
- See `samber/developer-relations-skills@tech-employer-branding` for the employer-brand surfaces a candidate will check before accepting.
