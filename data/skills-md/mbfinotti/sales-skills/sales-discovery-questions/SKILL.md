---
name: sales-discovery-questions
description: Builds a sequenced sales discovery question set - pain, root cause, impact, urgency - for a specific deal or persona, sized to the call length, with follow-up ladders, branch triggers, and a do-not-ask list. Covers B2B (SDR qualification through multi-stakeholder AE discovery) and high-ticket B2C consultations. Use whenever the user mentions discovery call prep, qualification questions, SPIN or pain-funnel questions, a first-meeting agenda, or "what should I ask this prospect", even without the word discovery. Do NOT use for rebuttals (mbfinotti/sales-skills@sales-objection-handling), the cold-call opening (mbfinotti/sales-skills@cold-call-opener), or grading a finished call (mbfinotti/sales-skills@sales-call-review).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.7"
---

# Discovery Questions

Build the sequenced question set a rep carries into a sales discovery conversation, plus the follow-up ladders and branch logic to adapt it live.

Four questioning frameworks with a publicly documented structure converge on one spine:

- SPIN (Rackham, 1988)
- Sandler's Pain Funnel
- MEDDPICC's Three Whys
- GAP Selling's Problem / Root Cause / Impact chart

The spine: isolate a real problem, dig to its root cause, quantify the impact, then establish why now. This skill encodes that convergence, not any one acronym. Vendor question-count and talk-ratio benchmarks are directional at best - never set a number to hit.

## Interview

Ask before drafting. One question per message; offer multiple-choice answers when possible; skip anything the user already answered or that their notes make obvious.

- B2B, or B2C? (B2C here means considered, high-ticket consumer sales - coaching, remodeling, financial advice - not impulse retail.)
- Who is the persona, and how senior? (End user, manager, executive - seniority changes question count and depth.)
- What does the product do, and what problem does it solve, in one sentence each?
- What call is this: SDR qualification (15-30 min), AE deep discovery (30-45 min), persona-specific follow-up in a running deal, or a single B2C consultation? How long?
- Deal size and cycle complexity? (Transactional single-buyer / mid-market few stakeholders / enterprise buying committee.)
- Inbound or outbound origin? (Inbound buyers arrive with intent to confirm and deepen; outbound buyers need problem awareness built first.)
- What is already known from prior touches - outreach replies, notes, a prior call, a deal record?
- Does the team mandate a methodology (SPIN, MEDDPICC, Sandler, GAP, other)? If so, the set must map to its vocabulary.
- Is the buyer in a regulated context (healthcare, finance, government)? (Adds decision-process and procurement questions; constrains what can be asked about data and finances.)
- What pain does the rep already suspect? (Becomes the hypothesis to test - never a fact to confirm.)
- What next step would make this call a success? (The set must close toward it.)
- By what date must this call have produced a booked next step? (A hard date promotes the impact triad - a figure won on this call is what a dated ask is argued from - and demotes decision-context coverage, which pays back across the cycle, not today.)
- One-off win or compounding asset: a sheet for this one call, or a reusable persona template the team reruns? (Compounding promotes decision-context coverage and the full follow-up ladder, since both amortize across calls and personas; one-off keeps the bare spine.)
- Effort ceiling: how many of the call's minutes are yours to spend on questions, how much rehearsal will the rep actually do, and how much of the buyer's patience can you spend? (A low ceiling deletes the decision-context stage outright and caps every ladder at two rungs.)

## Workflow

1. Run the Interview; collect every answer before writing a question.
2. Gather context. If you can browse the web, research the company and persona; otherwise work from the user's notes. Never fabricate account facts - research answers situation questions so the call doesn't have to.
3. Write 2-3 candidate pain hypotheses from the inputs, each stated as a hypothesis to test on the call. Confirm with the user which to prioritize.
4. Pick the coverage lens layered on the spine below. Call minutes are the budget every lens is priced in, and the buyer's patience is spent alongside them - a lens that costs more goodwill is expensive even though it is free to the rep.
   - efficiency: `GAP > Sandler > SPIN > MEDDPICC`
   - value: `GAP > MEDDPICC > Sandler > SPIN`
   - effort: `MEDDPICC > Sandler == GAP > SPIN`
   - Default GAP: about an hour of per-deal rehearsal and two impact questions - buys the figure in the prospect's own words that the close, the recap, and every downstream deal skill run on.
   - Sandler: costs the same hour and the same handful of minutes inside a stage already open, the genuine tie on effort with GAP - buys depth on one pain instead of a number, so it ranks second.
   - SPIN: near-zero on both axes - it only re-sequences questions already written, and the spine has absorbed its ordering. Take it free, never budget for it.
   - Starved: MEDDPICC's decision context. High value in a real buying group, highest effort - a whole extra stage, re-gathered per persona across the cycle - so efficiency buries it, and reps ship sheets that quantify a pain nobody can approve. Promote it to first whenever the buying group runs past a single economic buyer, or the buyer is regulated. Gather its elements as questions only; scoring belongs to the scorecard skill.
   - Delete, never demote:
     - A mandated methodology removes the other three from the sheet and maps every stage to its own vocabulary.
     - A transactional or B2C deal removes the decision-context stage outright.
     - A ruled-out lens parked at the bottom reappears as scope mid-call.
   - Re-rank before writing a question - this order is a default, not a law, and it moves with who runs the call and who answers:
     - Fifteen SDR minutes leave only the top of the line.
     - An hour with a practitioner promotes Sandler to par.
     - An executive promotes whichever lens reaches a figure fastest and deletes the rest.
5. Size the set to the call: roughly one substantive question plus its follow-ups per 3-4 minutes of questioning time; fewer and deeper for executives. Spend those minutes in step 4's order - the lens at the head of the efficiency line gets its questions first, and whatever the budget cannot fund is cut from the tail, never trimmed evenly across all four. Published "ideal question counts" are correlational and internally inconsistent, so size by call length, never a magic number.
6. Draft from [references/question-bank.md](references/question-bank.md), sequenced per the spine, one stage at a time. Attach a 2-3 rung follow-up ladder and a listen-for note to each primary question.
7. Add branch triggers (below) and the do-not-ask list from the question bank.
8. Assemble into the call sheet from [references/call-sheet-template.md](references/call-sheet-template.md).
9. Run the Quality gate; iterate - rewrite and re-check - until every item passes.
10. Deliver, and remind the user: the sheet is a map, not a script - follow the prospect's answers, use the branches.
11. If your harness has persistent memory, memorize the persona, the hypotheses that proved true, and which questions produced signal - the next set for the same persona starts warmer. Otherwise hand the user a short recap to keep.

## The pain → impact → urgency spine

Every question belongs to a stage. Every stage has an exit condition. Movement is one-way - never retreat to logistics before the spine is walked.

| Stage            | Job                                                                                | Move on when                                              |
| ---------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Frame            | One-line agenda agreement (Sandler's upfront contract, Sandler's own concept)      | Purpose, time, and possible outcomes agreed               |
| Situation        | Minimal context you could not research - 1-2 questions max                         | You can describe their current process in their words     |
| Pain             | Surface a real problem behind the hypothesis                                       | A named, specific problem with a recent example           |
| Root cause       | Why it happens and what they already tried                                         | Cause distinguished from symptom; prior attempts known    |
| Impact           | Quantify across technical, business, and personal dimensions (GAP Selling's triad) | At least one figure, plus who else it touches             |
| Urgency          | Why now - the compelling event                                                     | A dated or triggered reason to act, or its honest absence |
| Decision context | (Complex B2B) how a decision would actually get made                               | Process, other voices, evaluation path sketched           |
| Close            | Prospect's-words summary, then a dated next step                                   | Specific next step proposed against the impact uncovered  |

Sequencing rules - the logic the whole set obeys:

- Open before closed. Open the stage with an open-ended question; use closed questions only to confirm or quantify what was said. Approach discovery "with a learning mindset, not a selling one" (Chris Riley, via a vendor roundup).
- Layer before advancing: every meaningful answer earns 2-3 follow-ups before a new topic. Sandler's Pain Funnel (published by a vendor; Sandler's own pages don't show it) orders the ladder: vague → specific example → duration → prior attempts → cost → emotional weight. That ordering, not the exact wordings, is the transferable part.
- Root cause before impact. "You can't solve a problem you don't understand" (Keenan). Quantifying a symptom's cost quantifies the wrong thing - and "pain can be misleading" (Keenan).
- Impact before urgency. Urgency asked before impact is quantified is just pressure - and published buyer-indecision research (Dixon & McKenna's JOLT work, their book's own claim) found pressure deepens indecision rather than resolving it.
- One idea per question. Never compound, never stack. A stacked question gets the answer to its easiest half.
- Past-specific over hypothetical. "When did that last happen, and what did it cost?" beats "what would it cost if...". Answers about real events are data; answers about imagined ones are politeness.
- Their words, not the product's. Questions stay product-agnostic until the close; the product enters only after the gap is established. "Never sell to need" (Keenan).
- Quantify with their number. "Value is a figure, not an adjective" (Command of the Message, Force Management). Let the prospect say the number; a number the rep supplies is an objection waiting to happen.

Branch triggers - the live-adaptation half of the deliverable, written into every call sheet. These carry no ranking and never get one: each fires on its own condition rather than competing with the others for the same minute, so ordering them would invent a precision the call does not have.

- No pain surfaces after two hypotheses → switch hypothesis, or ask the honest fallback: "What would have to be true for this to be worth your time?". Do not manufacture pain.
- Prospect volunteers impact early → skip forward, bank it, return for root cause. The spine orders exit conditions, not scripts.
- Executive in the room → halve the question count, lead with the sharpest hypothesis, trade situation questions for a point-of-view statement. "Top-performing reps ask fewer questions during discovery calls" (Gong), and its published rules-of-thumb explicitly break down for C-suite buyers.
- Answers stay surface-level → drop down the Sandler ladder one rung at a time rather than moving on; a stage exited without its condition met is a gap the recap email will expose.
- Prospect asks for price or a demo mid-spine → answer briefly, then trade: one more stage before going deeper. Premature pitch is the top failure mode below.

## Invocation and expected output

Typical invocations:

- "Build my discovery question set for tomorrow's 30-minute call with a VP Ops at a 200-person logistics company - outbound, she replied to a cold email about shipping errors."
- "I sell kitchen remodels; couples book a 60-minute in-home consult. Give me the question set."
- "SDR qual call, inbound demo request, IT manager at a mid-market accounting firm - 15 minutes."

Deliver one call sheet (full template in [references/call-sheet-template.md](references/call-sheet-template.md)):

```
DISCOVERY CALL SHEET - <persona> at <company>, <call type>, <length>
Hypotheses     : 2-3 suspected pains, ranked - to test, not confirm
Frame          : one-line upfront agenda
Question path  : per spine stage - primary question, 2-3 follow-up rungs,
                 listen-for note, exit condition
Branches       : if no pain / if exec / if impact early / if price asked
Do-not-ask     : leading, logistics-first, and hypothetical questions to avoid
Close          : summary prompt + the dated next-step ask
After the call : which stages went unanswered → gaps for the next touch
```

## B2B and B2C

- Same for both (the frameworks converge here, and none of them splits the spine by business model):
  - The spine itself
  - The sequencing rules
  - The follow-up ladders
  - The quality gate

  What changes is who answers and which impact dimension leads.

- B2B: buying groups run large - a Gartner survey (2017, n=750, Gartner's own figure) puts the median at 6-10 decision makers - so discovery recurs per persona. Generate persona-specific variants (workflow pain for end users, business outcomes for the economic buyer, architecture and security for technical evaluators); route stakeholder strategy itself to the deal-champion-mapping skill.
- B2B: decision-context questions are load-bearing in complex deals; in regulated buyers, procurement and compliance path questions expand and personal-finance-adjacent questions disappear.
- B2C high-ticket: one conversation, one or two decision makers - usually the only shot at the full spine, so the close matters more than coverage breadth. Business impact becomes household time, money, and stress, which is why the question bank re-ranks the impact dimensions here. With a couple, ask each person the pain and impact questions separately - two decision makers means two spines.
- B2C: prior-attempts questions ("what's kept you from doing this until now?") carry the root-cause stage; regulated categories (financial advice, health) constrain phrasing - flag for the user, don't guess the rules.

## Quality gate

Score the drafted set against all ten items. Pass threshold: 10/10. Iterate until nothing fails.

1. Every question maps to exactly one spine stage; no orphans, no stage empty except a justified skip (e.g. decision context on a first SDR call).
2. Each stage opens open-ended; closed questions only confirm or quantify.
3. Root cause is probed before impact; impact carries at least one quantifying question before any urgency question appears.
4. Impact questions cover at least two of technical / business / personal.
5. No leading questions (the desired answer embedded in the wording) and no compound questions anywhere on the sheet.
6. Every question that can be past-specific is: it references a real, recent instance, not a hypothetical.
7. Budget, timeline, and process logistics appear only after pain and impact - never as openers. The two canonical offenders ("What's the timeline for this project?", "Is there budget allocated?") are on the do-not-ask list, negative examples published by GAP Selling practitioners.
8. The set fits the stated call length at roughly one primary question plus ladder per 3-4 minutes, reduced for executives; no target question-count is cited as a rule.
9. Every question could change what the rep does next. A question whose answer alters nothing is discovery theatre - cut it.
10. The sheet ends with a prospect's-words summary prompt and a dated next-step ask, and carries branch triggers and the do-not-ask list.

## KPIs and measurement

- Per call, the sheet worked if:
  - 3-4 distinct problems surfaced, with at least one quantified in the prospect's own number.
  - Every exited stage met its exit condition.
  - A dated next step was accepted.

  A recap email writable from the answers alone (route writing it to the sales-meeting-recap skill) is the honest test - unanswerable sections are the discovery gaps.

- Across calls, track first-call → next-meeting (or → opportunity) conversion per persona and per question set version. Movement there, not any talk-ratio target, is the signal - published talk-listen and question-count benchmarks are vendor claims, correlational, and internally inconsistent across the vendor's own refreshes (details in [references/frameworks-and-evidence.md](references/frameworks-and-evidence.md)).
- If a conversation-recording tool is available, review which questions produced long, specific answers and which produced one-liners; feed that back into the next version of the set. Without one, the rep's after-call gap notes on the sheet serve the same loop.

## Common failure modes

| Failure                                                           | Fix                                                                                                                                                                 |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Interrogation feel - rapid-fire list, no layering                 | Fewer primaries, deeper ladders; react to answers ("you said X - tell me more") instead of jumping topics                                                           |
| Happy ears - hearing confirmation of the hypothesis in everything | Hypotheses are written to be tested; require a recent, specific example before a pain counts as found                                                               |
| Surface-level pain - a complaint mistaken for a problem           | Walk the ladder: specific example → duration → prior attempts → cost; a pain without a story is a symptom                                                           |
| Unquantified impact                                               | No urgency questions until at least one figure exists, in the prospect's number, on ≥2 impact dimensions                                                            |
| No compelling event                                               | Ask why-now directly (MEDDPICC's Three Whys: "Why anything? Why you? Why now?"); record its honest absence rather than inventing one - absence is deal intelligence |
| Leading questions                                                 | Strip the embedded answer; "how do you feel about that cost?" not "that must be expensive, right?"                                                                  |
| Premature pitch - demo or product talk mid-spine                  | Product enters after the gap is established; brief answer, then trade back into the spine                                                                           |
| Logistics-first questions - budget and timeline as openers        | They harvest logistics before a problem exists; move them behind impact, per the gate                                                                               |
| Discovery theatre - questions whose answers change nothing        | Cut any question with no downstream consequence; coverage is measured in exit conditions, not questions asked                                                       |

## Reference

- See [references/question-bank.md](references/question-bank.md) for the stage-by-stage question bank with methodology attributions, follow-up ladders, B2C variants, and the do-not-ask list.
- See [references/call-sheet-template.md](references/call-sheet-template.md) for the fill-in-ready call sheet.
- See [references/worked-examples.md](references/worked-examples.md) for a complete B2B call sheet, an abbreviated B2C consult sheet, and an annotated logistics-first negative example.
- See [references/frameworks-and-evidence.md](references/frameworks-and-evidence.md) for the four verified frameworks in efficiency order, what each costs and buys as a coverage lens, and the evidence caveats behind the vendor benchmarks.
- See `mbfinotti/sales-skills@sales-objection-handling` for rebuttals when a question surfaces resistance.
- See `mbfinotti/sales-skills@cold-call-opener` for the opening script before discovery starts.
- See `mbfinotti/sales-skills@sales-call-review` for grading the call transcript afterwards.
- See `mbfinotti/sales-skills@meddpicc-scorecard` for scoring the deal against the elements these questions gather.
- See `mbfinotti/sales-skills@sales-meeting-recap` for turning the answers into the recap email.
- See `mbfinotti/sales-skills@sales-outreach-personalization` for the pre-call research that precedes this skill.
