---
name: ad-creative-brief
description: "Turn a campaign goal and an audience insight into a structured creative brief a designer, video editor, or UGC creator can execute - messaging angle, hook directions, art direction, specs, testing intent, and the handoff and revision loop. Covers B2B and B2C, with variants for static image, short-form video/UGC, and search/responsive text ads. Use whenever the user needs to brief a designer or creator, asks what an ad should say, or mentions messaging pillars, creative direction, or a design handoff - even if they never say 'brief'. Writes direction, never the finished asset: the ad copy itself is mbfinotti/advertising-skills@ad-copy-variants and shot-by-shot creator scripts are mbfinotti/advertising-skills@ugc-ad-scripts."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.1"
---

# Creative Brief

Write a performance-marketing creative brief: a per-concept test specification, not a brand brief with metrics bolted on. The classic agency brief centers on a single-minded proposition, is written once per campaign, and stays deliberately loose so it can inspire. The performance brief replaces that proposition with a **falsifiable creative hypothesis**, is written per concept per sprint, and is prescriptive about hooks, specs and decision thresholds because dozens of variants ship each cycle.

The stakes are documented. The BetterBriefs Project (IPA, 1,700+ marketers and agency staff, 70+ countries) found respondents estimate ~33% of marketing budget is wasted through poor briefing, and that 80% of marketers think they write good briefs while only 10% of agencies agree. Agencies name the gaps as focus (83%), clarity (79%) and inspiration (65%).

One honesty check frames everything else. Motion's 2026 analysis of $1.29B in Meta spend across 578,750 creatives found roughly 5% of creatives become winners - a hit rate no brief can repeal. So the brief's job is not to promise a winner; it is to maximise the quality, cleanliness and diversity of every at-bat.

This skill ends at the approved brief document, and never produces final creative. Writing the finished ad copy belongs to `mbfinotti/advertising-skills@ad-copy-variants`; the shot-by-shot creator script - spoken lines, shot list - belongs to `mbfinotti/advertising-skills@ugc-ad-scripts`. This brief writes hook _direction_, never hook scripts; that line is the boundary.

Hand off elsewhere too: scoring an existing video opening to `mbfinotti/advertising-skills@ad-hook-analyzer`, deciding a running ad is worn out to `mbfinotti/advertising-skills@ad-creative-fatigue`, sample-sizing and structuring the test itself to `mbfinotti/advertising-skills@ad-creative-test-plan`, and the targeting plan to `mbfinotti/advertising-skills@ad-audience-targeting`.

## Interview

Ask before drafting anything. One question per message; offer multiple-choice answers where possible; skip anything already answered or visible in supplied material.

- Campaign goal, and the single primary KPI the creative will be judged on?
- Platform(s) and placements?
- B2B or B2C/DTC?
- Awareness level of the target audience: unaware / problem-aware / solution-aware / product-aware / most-aware? ("All audiences" is not an answer - it is the most common brief defect; press for one level per brief.)
- Who executes the brief: in-house designer, video editor, freelance UGC creator, or agency? (Changes how prescriptive to be, and whether rights and disclosure fields apply.)
- Production capacity, deadline, and revision cap? Is the deadline hard? (The format and testing-intent orderings below span hours to a week in time-to-effect, so they cannot be ranked without it.)
- Do you want the fastest at-bat available now, or learning that compounds across future briefs - a validated persona, a cleared proof asset, an owned footage library? (The first favours static and hook tests, the second favours video/UGC and persona tests.)
- Effort ceiling: who can be pulled in without asking permission, and can you get creator rights and claim approval at all? (A "no" deletes rungs rather than delaying them.)
- Brand mandatories and compliance constraints? (Regulated category? Which claims need substantiation before they may appear in a paid ad?)
- What evidence already exists: customer reviews, sales-call notes, ad comments, past winners with their metrics, competitor ads?
- Budget and expected deliverable count?
- Are platform auto-enhancements on or off - and does anyone actually know?

## Brainstorm Before You Brief

Never jump from interview to a finished brief; the brief hardens assumptions, so surface them first.

1. Restate the campaign goal and the audience insight in one sentence each; get confirmation before proceeding.
2. Mine the evidence (methods in [references/angle-frameworks.md](references/angle-frameworks.md)) and shortlist the candidate pains/desires and personas.
3. Present 2-3 candidate concept directions - each with its messaging angle, the evidence it rides on, its format family, its trade-offs - and one recommendation with rationale. Ask narrowing questions one at a time.
4. Once a direction is picked (or blended), draft the brief section by section and validate each before moving on: context + audience, then message + hypothesis, then hooks + art direction, then the testing block.
5. Hold an explicit approval gate: no brief is final without sign-off. Log rejected directions in the angle bank - they are future tests, not waste.

## Workflow

1. Run the Interview.
2. Gather evidence using the mining methods in [references/angle-frameworks.md](references/angle-frameworks.md): scored review mining, top recurring 1-2 star objections, voice-of-customer beyond reviews (B2B: call notes, CRM comments, search terms), competitor ads filtered by longevity, past winners with their metrics. Every claim in the brief cites a source; a brief without evidence is a wish list.
3. Run the brainstorming mode above.
4. Fix the translation chain (below): pain → persona → messaging angle → awareness level → hook direction → format.
5. Write **one brief per concept** using [references/brief-template.md](references/brief-template.md), choosing the format variant (static / search / video-UGC, ranked in Format Variants below). Variations of a winning concept ride the original brief; only a genuinely distinct concept gets a new one. Target length: 1-2 pages including references.
6. Fill the testing-intent block and assign asset names via the naming convention - never leave naming to whoever uploads.
7. If you can browse the web, pull the platform's _currently published_ aspect ratios and safe zones for each target placement; otherwise write "preview in-placement before export" into the specs field. Published safe-zone numbers disagree by tens of pixels, so a hardcoded number is a defect either way.
8. Check the draft against the failure-modes table, then pass the messaging angle and hook option lines through your preferred humanizer skill - they must read as conversational human statements, not marketing copy.
9. Hand off. Run the revision loop: collect feedback in one consolidated round per revision (scattered piecemeal notes burn the revision cap), and send creative back if it addresses neither of the brief's top objections.
10. When results land, write the outcome into the brief's learning field and the angle bank. If your harness has persistent memory, memorize the angle bank, hook performance by trigger type, and per-concept outcomes so the next brief starts from history.

## The Translation Chain

The intellectual core, and the part most briefs skip. Motion's Creative Strategy Engine is the named public methodology: **Pain (or Desire) → Persona → Messaging Angle → Awareness level → Hook → Format.**

- Pain is the default anchor; reserve desire for aspirational or luxury categories where no functional problem exists.
- Personas are secondary: different life contexts in which people feel the _same_ pain. Each pain × persona cell is a distinct messaging-angle opportunity.
- A messaging angle is a conversational human statement capturing the insight at that intersection - explicitly not a tagline or slogan.
- The angle stays constant across awareness levels; only its expression changes.

The named frameworks behind the chain - Eugene Schwartz's five levels of awareness (Breakthrough Advertising, 1966; Schwartz's own word was _levels_, not stages) and its neglected sibling, market sophistication - plus the pain × persona matrix and the awareness-to-hook mapping live in [references/angle-frameworks.md](references/angle-frameworks.md).

## Fixed Vocabulary

"Concept", "angle" and "hook" are used inconsistently across the industry - strategists, copywriters and media buyers each mean something different, and testing under one fuzzy label destroys learning. The practical fix is to tag on independent dimensions rather than argue over a word (Dara Denney's decomposition uses five: format, creator, messaging, imagery, persona). This skill fixes the vocabulary, and every brief restates these definitions in its own header:

- **Concept**: a distinct creative idea - one brief, one concept.
- **Angle**: the argument for why this person should care, stated as a human sentence.
- **Hook**: the opening 1-3 seconds (video) or the first-read elements (static) - an _expression_ of the angle.
- **Format**: the execution container (testimonial, demo, founder, us-vs-them, static, carousel...).
- **Iteration**: a variant that changes one element of an existing concept; not a new concept, not a new brief.

## The Brief Skeleton

Compact shape; per-field guidance and format variants in [references/brief-template.md](references/brief-template.md); worked examples plus an annotated bad brief in [references/examples.md](references/examples.md).

```
CREATIVE BRIEF - <concept name>, <date> - definitions header (concept/angle/hook/format/iteration)
1 CONTEXT      goal + primary KPI | platform(s) + placements | launch + production dates | budget
2 AUDIENCE     persona + life context | awareness level (one of five) | belief held before seeing
               the ad | core objection | B2B: committee role this brief targets
3 MESSAGE      messaging angle (one conversational sentence) | value prop | one proof point |
               evidence citations (review/call-note/winner each claim traces to)
4 HYPOTHESIS   "If we lead with [pain] and [proof], then [audience] will [action]"
               type (efficiency order): hook | proof | format | angle | persona
5 HOOKS        3-5 directions, each tagged by trigger type; video: SPOKEN / VISUAL / TEXT OVERLAY
               per option; recommended first test + rationale
6 ART          2-3 reference ads, one-line note each | do (max 2) / don't (max 2) | ratios + safe
               zones ("preview in-placement") | sound-off design + accessibility | enhancements
               on/off per type | AI-disclosure line
7 DELIVERABLES arithmetic (e.g. 2 hooks x 1 main edit = 3 files) | iteration vs net-new flag |
               naming convention | revision cap | UGC: usage rights (where / how long / geography)
               + creator-level disclosure
8 TEST         the one variable that changes + what stays constant | minimum spend or impressions
               before any call | deciding KPI + its benchmark | on win / on loss | where the
               learning gets written
```

## Hook Direction

A video hook has three layers; brief and label them separately (Motion's convention):

- **SPOKEN** - first words on camera.
- **VISUAL** - what happens in the first frame.
- **TEXT OVERLAY** - on-screen text.

For statics: primary-text hook, headline, caption hook. Offer 3-5 options, each tagged with exactly one trigger type, plus a recommended first test and why.

Value is not a property of the trigger - the awareness level sets it (mapping in [references/angle-frameworks.md](references/angle-frameworks.md)), so a trigger the level rules out is worth nothing however cheap it is. Gate on the level first, then rank the survivors by what they cost on a body already shot or a layout already designed. The eight trigger types, in that efficiency order:

1. **Pain agitation** - one spoken line, and the evidence is already mined. Near-zero.
2. **Identity call-out** - one spoken line plus one overlay. Near-zero.
3. **Contrarian / myth-busting** - near-zero to write; spends political capital when the claim contradicts brand or category orthodoxy.
4. **Urgency / stakes** - near-zero to write; gated on offer mechanics, and any scarcity or deadline claim has to be true before it runs.
5. **Curiosity gap** - near-zero to write, plus the resolution field: where the loop closes.
6. **Social proof / credibility** - near-zero when the review wall or badge already exists; a week when it must be gathered, plus testimonial substantiation and sign-off in a regulated category.
7. **Aspiration / desire** - an after-state to stage or shoot.
8. **Pattern interrupt** - its own frame or set-up: a shoot, not a rewrite.

- effort: pattern interrupt > aspiration > social proof > curiosity gap > pain agitation == identity call-out == contrarian == urgency
- compliance cost: social proof > urgency > contrarian > aspiration == pain agitation == identity call-out == curiosity gap == pattern interrupt

The four-way effort tie is real, not a shrug: pain agitation, identity call-out, contrarian and urgency are each one written line against footage that already exists, so there is nothing left to trade between them. Contrarian and urgency then separate on compliance instead, which is why they leave the tie on the line below. The five-way compliance tie holds for the same shape of reason: none of those five asserts a result, names a person, or promises a deadline, so none triggers a review the category did not already require.

**What this order starves: social proof, and pattern interrupt behind it.** Social proof is the only trigger carrying third-party evidence and it sits sixth, because gathering the wall or the badge costs a week and a sign-off. Pattern interrupt is last on effort because it needs its own frame shot.

A brief written purely by ratio therefore tests the four one-line triggers forever and never puts evidence in front of the reader. Promote them when the asset already exists and is cleared - social proof's cost then collapses to near-zero while its value is unchanged - or when the interview answer was a compounding mandate, which justifies paying for a pattern-interrupt shoot once and reusing the footage across the quarter.

Delete rather than demote: if no cleared customer result exists and none can be obtained, **social proof is deleted from this brief's trigger menu and named as deleted**; if the category bars the claim contrarian or urgency rests on, those are deleted too. A ruled-out trigger held at the bottom of the list gets briefed anyway by whoever reads it next.

Default first test: the highest-ranked surviving trigger the awareness level actually endorses. That is a default, not a law - it moves with the category and with who executes. Re-rank against the interview answers and say which answer moved which trigger: a hard deadline keeps you inside the one-line four. Then re-rank against what this account already owns - an in-house editor who turns a new opening frame in an afternoon, a cleared library of customer footage, a founder who is genuinely good on camera - each of which moves an expensive trigger up several places.

Direction, not script: "open with the problem, named directly" is direction; the exact words belong to the executor or to `mbfinotti/advertising-skills@ugc-ad-scripts`. Source hook options from evidence, not a blank page: pull competitor ads from public ad libraries and filter by **longevity, not recency** - an ad still running after months is the validated one (Foreplay's Jack Kavanagh) - and use Ben Heath's hook-factory approach (a few video bodies × many spoken and visual hook variants captured in one shoot) to make hook options cheap to produce.

## Art Direction Rules

- **Reference examples beat adjectives.** "Authentic" and "premium" mean different things to different people; a reference ad means the same thing to everyone. Include 2-3 in-category reference ads, each with a one-line note on what to take from it.
- Cap brand do's and don'ts at ~2 each; a longer list stops being read.
- Name aspect ratios per placement, but do not hardcode safe-zone pixels - published numbers disagree by tens of pixels. Require an in-placement preview before export instead.
- Design sound-off: every claim that matters must be legible as on-screen text; captions are non-optional. Exception to note in the brief: Reels skews sound-on (roughly 70-80% of viewers with audio, per Benly), so the best Reels creative works both ways.
- Accessibility fields: WCAG 4.5:1 minimum contrast for text, captions on video, alt text, and no more than three flashes per second.
- Meta's "20% text rule" was retired in 2020: there is no hard limit and no auction penalty. Treat text density as a performance preference. Claims of a persistent hidden delivery penalty circulate in vendor posts and are unverified - say so rather than encoding folklore as a rule.
- **Enhancements field**: platform auto-enhancements are default-on and expand the variable space without asking. A toggle nobody set is an uncontrolled variable, so the brief records enhancements on/off per type.
- **AI-disclosure line**: content generated outside the platform's own tools generally must be declared in the ads manager (platforms auto-label their own tools' output); undisclosed AI content is a commonly reported rejection reason. A brief field, not an afterthought.

## Testing Intent

Every brief carries a falsifiable hypothesis - Directive Consulting's B2B template generalizes well: _"If we lead with [pain] and [proof], then [audience] will [action]."_ Type it, change exactly one variable, and hold everything else constant.

The five types, in efficiency order:

- **Hook** - one extra cut from the same shoot.
- **Proof** - swap the evidence, reshoot nothing.
- **Format** - a new container, so a new production.
- **Angle** - a new concept and a new brief.
- **Persona** - new research, new audience, parallel briefs.

That order inverts on the other two axes, which is the whole point of naming a type:

- effort: persona > angle > format > proof > hook
- value (how much of the account the learning transfers to, and for how long): persona == angle > format > proof > hook

Persona and angle tie on value because a result at either level rewrites every brief downstream of it - a wrong persona and a wrong angle both invalidate the hooks, formats and proofs already tested underneath them. They separate on effort, which is the only thing that orders them.

**What this order starves: persona, and angle behind it.** They are the two highest-value types and the two most expensive, so a ratio picks hook every sprint. That is the documented failure of a testing programme that only ever iterates: months of hook cuts inside a premise nobody has ever tested.

Promote them when the concept family is flat - no hook rescues a wrong angle, and no angle rescues a wrong persona - when the flat family is the only family you have ever run (skip rungs outright), or when the interview answer was a compounding-learning mandate. A research team that can stand up a persona in days collapses the effort axis and promotes it on cost alone.

Default rung: **hook**, whenever the angle has already won somewhere - a hook test is one extra cut from the same shoot and resolves inside a sprint. A hard near-term deadline pins you there.

Re-rank against an unfair advantage you already hold, such as a proof asset (named customer outcome, third-party badge) already cleared and sitting unused, which makes a proof test the cheapest rung rather than the third. Where the account cannot run a type at all - no budget for persona research, no second audience to test against - delete that rung and say so, rather than leaving it at the top of a list nobody can act on.

- State deliverables as arithmetic (`2 hooks × 1 main edit = 3 files`) and flag iteration vs net-new explicitly: a resize is not a new design; three hook cuts of one video are not three concepts. This field is what prevents scope disputes.
- Pre-commit minimum evidence before any kill/scale call. Attributed starting points, not laws: at least 2,000 impressions before reading a hook rate (SparkUGC), and roughly 5-10 conversions or spend of 5-10× target CPA before a conversion-based call (Taylor Sicard). Adapt to the account's volume.
- Metric trap: hook rate is 3-second plays ÷ impressions on Meta but TikTok counts at 2 seconds - never benchmark across platforms. Published reference bands, attributed and never universal: 25-30%+ hook rate healthy on Meta cold traffic, 25%+ hold rate (SparkUGC; Motion).
- Decide up front what happens on win and on loss, and where the learning gets written - a system the whole team reads, never only a slide deck.
- **Naming**: the brief assigns asset names. Four levels - concept → iteration → format → test variable - ASCII only, underscores between variables (published convention via Apogee). Example: `PainFirst_V2_9x16_HookQuestion`.

## B2B vs B2C

The translation chain, hook layers, art rules and testing block work the same way for both. What differs:

**B2B**: one product needs _parallel_ persona briefs (economic buyer, technical evaluator, end user), because the buying committee averages ~8-13 people over cycles near 10 months (SalesHive) - not one persona at a time. The brief's KPI is SQL rate or cost per opportunity, never CTR alone: Directive's worked example had a variant win on clicks (+35%) while producing fewer conversions at a higher CPA - a CTR-optimised B2B brief buys expensive junk leads.

Proof is a quantifiable outcome plus a badge or product screenshot, not a before/after. Practitioner-led talking-head video tends to beat polished brand video (AJ Wilcox). Product marketing owns ICP and differentiator accuracy - consult them on every brief.

**B2C/DTC**: faster cycles, offer mechanics as an explicit brief field, review-mined verbatim language in angles and hooks, creator formats dominant.

## Format Variants

Full field lists in [references/brief-template.md](references/brief-template.md). Pick the container by learning bought per production hour, then let the placement veto the pick. The three, in efficiency order:

1. **Static** - one designer for an hour or two, and it reads the angle directly. The cheapest honest at-bat, and the default first concept.
2. **Search** - an afternoon of writing an asset pool, but the read is diluted because the system assembles the ad. Enters the ranking only where keyword demand already exists; where it does not, it drops out rather than ranking last.
3. **Video/UGC** - the strongest learning, since the three hook layers are isolated separately, and the largest bill: creator search, shoot, rights, revision rounds. A week of coordination, not hours.

- effort: video/UGC > search > static
- learning value per concept: video/UGC > static > search
- compliance cost: video/UGC (creator usage rights, paid-partnership and testimonial disclosure, AI-likeness disclosure where the face is synthetic) > static == search (whatever claim substantiation the category already demands)

Static and search tie on compliance because neither introduces a person, a performance or a rights-holder: the only review either triggers is the claim substantiation the category already demanded before either brief existed.

**What this order starves: video/UGC.** Top of the value axis, last on efficiency, so it loses every round to a static a designer turns in an hour. A team briefing by ratio alone ships statics indefinitely, never builds a footage library, and still cannot say which hook layer moves the number.

Promote it over the ratio on any of these, and name which one did it:

- A compounding mandate in the interview. The shoot buys footage, a validated creator and a rights agreement that make every later video brief an editing job.
- The placement vetoes the alternatives: on Reels- or TikTok-first placements a static barely earns delivery, so video/UGC leads because the others score zero there, not because it got cheaper.
- Statics have plateaued across the concept family. No new layout rescues an angle whose delivery format is wrong.
- The account already holds the expensive parts - in-house studio, standing creator roster, owned footage library - each of which collapses the effort axis outright.

Delete, do not demote. If the user answered that they cannot get creator rights or claim approval at all, **video/UGC is deleted from this brief's format menu and named as deleted**, not ranked last where the next sprint reads it as merely expensive and briefs it anyway. Same treatment for search where no keyword demand exists - it drops out rather than ranking last (above).

A hard deadline is different: it pins you to static for _this_ brief without removing video/UGC from the menu, so say "deferred to the next sprint", never "deleted".

The variant that breaks intuition is **search**: no hook, no visual - the system assembles the ad. Brief an asset pool (up to 15 headlines at 30 characters, 4 descriptions at 90 on responsive search ads) and map headlines to pain / product / proof themes - search's messaging-pillar equivalent (Directive).

Two warnings belong in every search brief:

- Ad Strength is a content-quality signal with no direct effect on Ad Rank; never chase it.
- Pinning restricts combination testing sharply (one published analysis puts a single pinned headline at >75% less testing).

For **UGC**: hook direction not hook script, talking points over word-for-word lines, revision cap and usage rights (where, how long, which geography) as brief fields, and creator-level FTC disclosure that platform ad labels do not satisfy.

## Measuring Whether This Worked

Instrument in this order - efficiency, not importance - rather than standing all three up at once:

1. **Rebrief rate** - share of briefs sent back for clarification before production starts. A counter kept by whoever sends briefs back, so near-zero to run, and the primary brief-quality KPI. This skill's practical target, not a researched constant: under 20%, tightened from your own history.
2. **Brief-to-launch cycle time** - two dates per brief. Directive's published B2B benchmark is 10 business days or less.
3. **Concepts-briefed-to-winner ratio** over a rolling 90-day window (an agency-published operational KPI) - a standing job, and noise until enough concepts have shipped. Read it against the denominator honestly: winners run near 5% of creatives at scale (Motion), so judge the trend against your own history, not an absolute bar.

Re-rank if that rolling log already exists in your reporting stack: the ratio becomes free rather than expensive, and moves to the top.

Iterate a brief until every template field carries real content with an evidence citation, and the executor confirms zero clarification questions on read-through.

Then track the three KPIs on a rolling log:

- A rising rebrief rate is a brief problem.
- A collapsing winner ratio with clean briefs is a concept-diversity problem.

## Common Failure Modes

Rows are in fix-first order, and that ordering is pure value: every fix costs the same brief-writing minutes before production starts (`goal == awareness == benchmark == everything below`), so nothing separates them but what each one buys. The top four make every fix beneath them unreadable - a brief with no KPI cannot be judged, one with no awareness level cannot pick a hook, and a test whose targeting moved cannot be read at all. Re-rank against the failure this team actually repeats: a shop that writes tight hypotheses but burns creators every quarter fixes the feedback rows first, whatever the general ordering says.

| Trap                                              | Why it burns                                                                                  | Fix                                                                         |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Briefing deliverables before the goal exists      | Volume without a hypothesis teaches nothing                                                   | Goal and KPI are interview question one; no goal, no brief                  |
| Awareness level blank or "all audiences"          | Every level needs a different opening; targeting all serves none                              | One level per brief; split briefs when levels genuinely differ              |
| No performance benchmark in the brief             | Kill/scale decisions get made by feel                                                         | Deciding KPI + threshold + minimum evidence, written before launch          |
| Changing targeting mid-test                       | The test variable is no longer the only variable                                              | Freeze targeting for the test window; targeting changes are their own test  |
| Multiple messages crammed into one ad             | The viewer picks none of them                                                                 | One angle, one proof point; extra messages become separate concepts         |
| Hook direction left to the executor's judgement   | The highest-leverage element goes untested and unrecorded                                     | 3-5 tagged options plus a recommended first test                            |
| Vague adjectives instead of reference ads         | "Premium" and "authentic" decode differently per reader                                       | 2-3 in-category references, one note each                                   |
| Generic specs reused across platforms             | Placements crop, truncate and overlay differently                                             | Per-placement ratios; in-placement preview before export                    |
| Over-scripting a creator                          | Delivery stops sounding natural - the reason UGC works                                        | Talking points and hook direction; words are the creator's                  |
| Too many stakeholders adding conflicting feedback | Revision rounds multiply; the message dilutes                                                 | One approver; one consolidated feedback round per revision                  |
| Results stored only in slide decks                | Losing variants teach nothing next sprint                                                     | Learning field in the brief + a persistent angle bank                       |
| Iteration paralysis (contested - Dara Denney)     | A brief format optimised purely for variable isolation produces creative that all looks alike | Reserve a share of briefs for genuinely fresh concepts, not only iterations |

## Reference

- Read [references/brief-template.md](references/brief-template.md) when writing the brief - field-by-field guidance plus the static / search / video-UGC variants.
- Read [references/examples.md](references/examples.md) before the first brief for a client - a worked B2C brief, a worked B2B brief, and a bad brief annotated with what is wrong.
- Read [references/angle-frameworks.md](references/angle-frameworks.md) during brainstorming and the translation chain - awareness levels, market sophistication, the pain × persona matrix, the hook trigger taxonomy, and the evidence-mining methods.
