---
name: sales-call-review
description: Scores one sales call transcript against an anchored rubric - opener, discovery, objection handling, close - quoting the transcript for every judgement and naming one focus behaviour. Handles messy ASR transcripts, missing speaker labels, and partial calls, covering B2B deal calls and B2C/inside-sales QA, rep self-review and manager tape review. Use whenever the user mentions a call recording, transcript, Gong or Chorus review, tape review, call scoring, or "how did this call go", even without the word review. Do NOT use for writing the follow-up email (mbfinotti/sales-skills@sales-meeting-recap) or scoring the deal itself (mbfinotti/sales-skills@meddpicc-scorecard).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.6"
---

# Call Review

Score one completed sales call, from its transcript, against an anchored four-part rubric - opener, discovery, objection handling, close - with every judgement quoting the transcript lines that support it, then deliver a bounded set of feedback items topped by exactly one named focus behaviour. This skill evaluates what the rep did on this call and stops there:

- Never writes the rep's next script.
- Never plans their quarter.
- Never scores the deal.
- Never drafts the follow-up email.

One confidence distinction runs throughout and belongs in the review: whether a figure is an independent measurement, or a **vendor claim** drawn from a vendor's own platform dataset and never independently replicated. No vendor correlation here is causal, ever.

## Interview

Ask before reviewing. One question per message; offer multiple-choice answers when possible; skip anything the transcript or the user's message already answers.

- Who is reviewing? (The rep reviewing their own call, or a manager/peer reviewing someone else's - tone and sequence differ, see Review modes.)
- What kind of call? (Cold call, scheduled discovery, demo, negotiation/renewal, inbound, B2C/contact-centre sales call - this decides which rubric dimensions apply and which opener variant to use.)
- B2B deal call, or B2C / inside-sales / high-volume consumer call? (B2C adds an optional compliance and script-adherence dimension.)
- Paste or attach the transcript. What shape is it - speaker-labeled? timestamped? complete, or partial?
- What was the call's outcome? (Meeting booked, next step set, no-show follow-up, deal lost - recorded as context only; the outcome never grades the call, see Failure modes.)
- Was a focus behaviour named in a previous review of this rep? (The first check of this review is whether it changed.)
- Does the team run a sales methodology or a house scorecard? (The review uses its vocabulary and any custom weights where they exist.)
- By when must the change show up on a live call? (Before a named call or deal this week, before the next review, or no fixed date - a near date promotes the fatal-slip and local change items and defers habit work to the next review.)
- Do you want this call fixed, or this rep's habit fixed? (One-off: the focus behaviour targets a local moment tied to the live deal. Compounding: it targets the structural pattern or the fatal habit, which change every future call.)
- How much coaching time exists before the next reviewed call? (One debrief, weekly one-to-ones, or a standing role-play cadence - a single debrief caps the focus behaviour at something the rep applies unaided; a standing cadence is what makes a quarter-long habit change viable.)

## Workflow

1. Run the Interview; obtain the transcript before forming any opinion.
2. Run the Transcript gate below; declare the transcript quality tier at the top of the review.
3. Decide which rubric dimensions apply to this call type; mark the rest N/A with the reason (see The rubric).
4. In manager/peer mode: elicit the rep's self-assessment before revealing any score - "play the tape and let the rep self-assess first before opening feedback" (Armand Farrokh's 3-Step Tape Review Method, 30MPC).
5. Walk the transcript once, segmenting it into opener / discovery / objection / close passages; collect candidate verbatim quotes per dimension along the way.
6. Score each applicable dimension against the anchored descriptors in [references/rubric-anchors.md](references/rubric-anchors.md). Apply the Evidence rule: no quote, no score.
7. Attach a confidence tier to each dimension score (rules below).
8. Identify any fatal moment - a single passage that would kill the deal or breach compliance regardless of how the rest scored. It is reported above the scores, never averaged away.
9. Select the bounded feedback set: at most 2 strengths (each quoted), at most 3 change items, exactly 1 named focus behaviour - ranked per Bounded feedback, then re-ranked against the Interview answers.
10. Assemble the review per [references/review-template.md](references/review-template.md); run the Quality gate; iterate until every check passes.
11. Deliver, ending on a strength - close the session with the rep "Positive. Better. Empowered." (Kevin Dorsey via 30MPC).
12. If your harness has persistent memory, memorize the rubric weights used, any agreed N/A conventions, and the single named focus behaviour - the next review starts by checking whether that behaviour changed. This is measurement continuity only; building a development plan from the trend belongs to a coaching skill, not here. Without memory, hand the user the review file to keep and re-supply.

## Transcript gate

Run before any scoring. A review built on a bad transcript is confidently wrong.

- **Quality check.** Read the transcript for ASR damage: garbled or nonsense words, non-speech tokens, heavy repeated filler, long unexplained gaps. If roughly a fifth or more of the content is damaged, refuse to score - report the damage and ask for a cleaner transcript or the recording's key passages instead (threshold adapted from published transcription-pipeline practice).
- **Speaker labels.** If labels are missing or generic, infer speakers from in-transcript cues: introductions, names used in address, who asks vs. answers. When a name resolves late in the transcript, relabel all earlier turns. If two speakers genuinely cannot be told apart on a passage, do not attribute it - flag it and ask the user; never guess silently (diarization-disambiguation practice from published transcript-handling workflows).
- **Citations.** Quote with a `[HH:MM:SS → HH:MM:SS]` range when timestamps exist; fall back to line numbers, then to the verbatim quote alone. Every citation must let the user find the passage.
- **Long transcripts.** Segment by call phase and review sequentially. Never deliver a review from a partially read transcript without saying exactly which part went unread.
- **Partial transcripts.** Score only the dimensions whose call phase is actually present; mark the rest "N/A - phase not in transcript". Absence of data is never a zero.
- **The one-line rule.** Never score a dimension confidently from a single garbled or ambiguous line. Cap that dimension at Low confidence and state what a cleaner transcript would resolve.

Confidence tiers per dimension (this skill's rubric): **High** - two or more clean, mutually consistent passages; **Medium** - one clean passage, or several partially damaged ones agreeing; **Low** - a single ambiguous or damaged passage; flag, do not conclude.

## The rubric

Four dimensions. Anchored behavioural descriptors for each - what a 0, 2, and 4 actually sound like on tape, plus per-dimension evidence cues - live in [references/rubric-anchors.md](references/rubric-anchors.md); load that file to score.

| Dimension          | What it measures                                                                                                                                 | Named sources                                                                                                                | N/A when                                                                                                                                                            | Default weight |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| Opener             | Cold call: earning explicit opt-in and an environment where real conversation can happen. Scheduled call: agenda set with Purpose, Plan, Outcome | Jason Bay's Cold Calling Framework (via 30MPC); PPO (Armand Farrokh)                                                         | Inbound call the prospect initiated with no opening move to judge                                                                                                   | 20%            |
| Discovery          | Problem-first questioning that ladders from symptom to consequence and tests whether the problem is worth solving - not an interrogation         | SPIN questioning heritage (Rackham's 35,000-call study); anti-interrogation warnings (Jen Allen-Knuth via 30MPC)             | Demo/negotiation call where discovery was explicitly completed on a prior call                                                                                      | 30%            |
| Objection handling | Objection restated, addressed, and resolution confirmed aloud - not argued over or capitulated to                                                | Mr. Miyagi Method: agree → disarm → redirect (Armand Farrokh); listen → restate → resolve → confirm (Salesman.com framework) | No objection surfaced - note whether prevention or disengagement explains it ("the best objection is the one you don't get", Chris Beall via Sales Gravy), then N/A | 20%            |
| Close              | Next-step commitment: continued-investment check, timeline pressure-tested, rep proposes concrete steps - on real deals only                     | The 5 Minute Drill (Armand Farrokh)                                                                                          | Call cut off before any close was possible                                                                                                                          | 30%            |

Scoring rules:

- Scale 0-4 per dimension; behavioural anchors written at 0, 2, and 4 only - interpolate 1 and 3. Anchoring a few points concretely beats vaguely labeling every integer (see Reliability).
- "Close" means the next-step close, not the contract signature - so it applies to nearly every call type, including discovery calls. Only a cut-off call makes it N/A.
- N/A dimensions leave the denominator entirely; renormalize any aggregate to the applicable maximum. Never score a structurally absent dimension 0 - a low number implies a coachable failure, and there was nothing to fail at.
- Weight ordering, stated: `discovery == close > opener == objection handling`. Discovery ties with close, and opener ties with objection handling: the sourced teardown material spends comparable attention on each pair member, and nothing measured separates them. Treat the ordering as this skill's weighting, not an outcome ranking - it follows where the teardown material puts its attention, not a measured effect on win rate.
- The weights stop at two tiers rather than four because splitting discovery from close would be false precision dressed as calibration. These weights carry no effort axis and no efficiency ranking - the reader chooses nothing here, since the call already happened. A house scorecard's weights win outright.
- The total score is the least interesting output. Report per-dimension scores plus a one-sentence shape reading ("strong open, discovery never tested whether the problem mattered, hollow close") and any fatal moment. A high total with one fatal moment is a worse call than a mediocre total without one - the fatal moment leads the review, never the number.

## Evidence rule

The single most important rule in this skill: **no quote, no score**. Every rubric judgement, every strength, and every change item cites the verbatim transcript passage(s) that earned it, with location.

If no passage supports a judgement, write "insufficient evidence" and leave the dimension unscored or Low-confidence. Never:

- Paraphrase from memory.
- Fabricate a quote.
- Score on vibes.

Conversational benchmarks (talk ratios, question counts) may appear as context only, always labeled. For example, Gong's ~43% talk / 57% listen figure is a vendor claim - correlational, drawn from the vendor's own platform corpus, never independently replicated - and it is never a scoring criterion here.

## Bounded feedback

"Managers, please stop giving 10-20 pieces of feedback on calls and role plays. One." (Kevin Dorsey via 30MPC). A rep's capacity for behaviour change is also capped - stacking too many simultaneous changes prevents any of them (Mark Kosoglow's Rep Assessment Matrix argument, 30MPC).

Reconcile that with a full rubric like this: **score everything, surface little**. The complete score sheet exists for the record - calibration, trend, and the next review's starting point.

The feedback conversation delivers at most 2 strengths (each with its quote), at most 3 change items, and exactly 1 named focus behaviour - the single highest-leverage change, phrased as an observable, re-executable action ("restate the objection before answering it"). That one is what the next review checks first.

"Great energy" is banned: a strength without a quoted moment is flattery, not a strength. Trait-level items ("careless", "low energy", "be more consultative", "not a closer") are deleted from the menu outright rather than ranked last - character language earns no rung here in either direction, and a ruled-out item parked at the bottom silently reappears as scope.

Shape every change item as observation before judgement - situation (quote + location), observable behaviour, impact on the call - the SBI structure (attributed to the Center for Creative Leadership).

### Ranking the change items

Four classes compete for the three slots and the one focus behaviour. Effort here is manager coaching time, rep practice reps before the change sticks, and how fast it shows up on a live call - never a currency amount.

- efficiency (pick in this order): `fatal slip > structural > local > fatal habit`
- value (what the change buys): `fatal habit == fatal slip > structural > local`
- effort (coaching time, practice reps, time-to-land): `fatal habit > structural > local == fatal slip`
- compliance cost: `fatal rule breach > fatal deal-killer == structural == local`

| Class       | What it is                                                              | Value bought                            | Effort to land                                                   |
| ----------- | ----------------------------------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------- |
| Fatal slip  | One deal-killing or rule-breaching moment the rep can simply stop doing | This deal, or the breach, avoided       | Near-zero - one quote, one instruction, visible on the next call |
| Structural  | A pattern repeated across this call                                     | Every future call of this type improves | A week - repeated reps to overwrite the pattern                  |
| Local       | One weak moment with no pattern behind it                               | One moment on one call                  | Near-zero - the rep applies it unaided on the next call          |
| Fatal habit | A deal-killing or rule-breaching behaviour the rep repeats by default   | This deal and every deal after it       | A quarter - standing coaching plus deliberate practice           |

Ties, justified:

- `fatal habit == fatal slip` on value: the damage when either fires is identical - the deal or the rule - and recurrence is an effort property, not a value one.
- `local == fatal slip` on effort: both are a single quoted moment carrying a single instruction the rep applies without practice.
- `fatal deal-killer == structural == local` on compliance cost: all three genuinely sit at zero, none of them leaves the coaching conversation. Only a rule breach carries real compliance cost - it triggers a review outside the sales org, and it is irreversible, because a recorded misstatement cannot be unsaid.

**What this order starves: the fatal habit.** It is the most valuable item on the page and it loses every efficiency round, because the quarter it costs buys one change while the same quarter of local fixes buys ten - exactly backwards when the habit is what loses the deals.

Promote it to the focus behaviour anyway when any of these holds:

- It is a rule breach.
- It was the previous review's focus behaviour and this transcript shows it unchanged.
- The rep is still in ramp, where a habit is cheaper to unlearn than it will ever be again.
- The same pattern appears on other reps' calls, which makes it an enablement fix rather than this rep's.

Re-rank before choosing, against what you already know about this rep and this team:

- A new rep in ramp promotes the fatal habit.
- A veteran whose manager runs one debrief a quarter demotes it, because the coaching time to land it does not exist - give them the structural item that fits the time that does.
- A manager with weekly one-to-ones can carry a habit change.
- A manager with no cadence cannot carry a habit change.
- A pattern showing on the whole team's calls is not this rep's focus behaviour at all.

Then re-rank once more against the three Interview answers, and state in the review which answer moved which item:

- A hard date promotes the fatal slip and the local fix.
- A compounding mandate promotes the structural item and the fatal habit.
- A low effort ceiling drops the fatal habit from this review and defers it to one with the coaching time behind it.

This ordering is a default, not a law - it shifts with the call, the rep, and whoever runs the coaching.

## Review modes

- **Rep self-review.** The skill acts as calibration partner: ask the rep to score each dimension first, then compare against the evidence-based score and explain every divergence with quotes. Hold self-criticism to the same evidence rule - "I was terrible" without a quote is as invalid as unearned praise.
- **Manager or peer review.** Self-assessment before reviewer scores, always (Farrokh's tape-review sequence). Deliver change items as SBI plus a question ("what was happening there?") rather than a verdict. Keep the whole review consumable in under 30 minutes - past that, "there is a 99% chance they are retaining 0% of the feedback" (quote, Armand Farrokh).

Both modes use the same rubric, evidence rule, and quality gate; only sequence and framing differ.

## B2B and B2C

Works identically for both: the transcript gate, the evidence rule, anchored scoring, bounded feedback, and the quality gate do not change.

- **B2B deal calls.** One call is one data point in a multi-call, multi-stakeholder deal. The close dimension grades next-step quality, and the 5 Minute Drill's anti-gaming criterion applies in full - setting next steps on every call regardless of deal reality is the mediocre pattern, not the good one (Farrokh).
- **B2C / inside-sales / contact-centre.** The call is often the entire deal, volume is higher, calls are shorter, and QA practice adds compliance and script-adherence checking - required disclosures made, claims accurate, script checkpoints hit - typically as binary items rather than 0-4 anchors. A real standardized framework exists at the contact-centre-operations level (COPC's CX Standard: critical-error categories, calibration, reviewer repeatability tracking), but nothing in it is sales-call-specific, so everything this skill transfers there beyond the shared core is still an adaptation, not established rubric practice - flag it as such in the review itself. The optional dimension's anchors are in [references/rubric-anchors.md](references/rubric-anchors.md); adapt them to the house script and its compliance list.

## Recording consent note

Short and factual, not legal advice: recording and reviewing calls is consent-regulated.

- **US.** Some states require all parties' consent (California, Florida, Illinois, Pennsylvania, Washington among them); most accept one-party consent (state statute summaries).
- **EU.** GDPR and the ePrivacy Directive require affirmative, purpose-specific consent - a passive "this call may be recorded" disclaimer alone is not sufficient, and consent for one purpose does not cover others (GDPR Recital 32 and ePrivacy summaries).

This skill reviews a transcript the user already holds and takes no position on the recording's lawfulness. If the transcript shows no consent disclosure where one was clearly expected, note it once. Check local rules before recording anything.

## Reliability

Anchored behavioural scales exist because unanchored ones are unreliable: inter-rater agreement (measured by Cohen's kappa or ICC) is poor for ambiguous judgements, and raters drift toward what they expect to see - "clearly stated guidelines for rendering ratings" are the documented fix (inter-rater reliability literature). That is the whole design argument for scoring against written 0/2/4 behaviours instead of gut-feel numbers, and for periodically re-reading the worked example in [references/worked-examples.md](references/worked-examples.md) to recalibrate.

## Common failure modes

| Failure                                    | Fix                                                                                                                                                                                                                   |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Grading the outcome instead of the process | A booked meeting doesn't prove a good call and a loss doesn't prove a bad one; every score must trace to quoted behaviour, and the outcome appears only as context                                                    |
| Next-steps theatre                         | The 5 Minute Drill's own criterion: never setting steps is bad, setting them on every call regardless of deal quality is mediocre, setting them on real deals only is good - a hollow calendared step scores 2, not 4 |
| Scoring personality or likeability         | "Confident", "likeable", "low energy" are not behaviours; replace with the observable action and its quote or drop the judgement                                                                                      |
| Rewarding question count                   | "Death by 1000 questions" interrogation is a failure mode, not a discovery win (Jen Allen-Knuth); score laddering and problem-testing, never volume                                                                   |
| A high total hiding one fatal moment       | The fatal moment is reported above the scores and leads the feedback, whatever the average says                                                                                                                       |
| Dumping every rubric miss on the rep       | The score sheet is the record; the rep gets at most 3 change items and 1 focus behaviour                                                                                                                              |
| Reviewing only lost calls                  | Sampling losses teaches only failure patterns and makes review feel like punishment; ask for a won or neutral call at the next opportunity                                                                            |
| Recency bias / rater drift                 | One call is one data point; anchor every score to this transcript's quotes, and recalibrate against the worked example between reviews                                                                                |
| Scoring a garbled line                     | The one-line rule: cap at Low confidence and say what a cleaner transcript would resolve                                                                                                                              |
| Vague praise                               | Every strength carries a quote; "good rapport" without one is deleted at the quality gate                                                                                                                             |

## Invocation and expected output

Typical invocations:

- "Here's the transcript of my cold call with the ops director at Brightline - tear it down."
- "Review this discovery call transcript. My AE thinks it went great; we lost the deal a week later."
- "I run an inside-sales team selling insurance by phone - QA this call against our script and give the rep one thing to fix."

Deliver one review (full fill-in template in [references/review-template.md](references/review-template.md)):

```
CALL REVIEW - <call/company>, <call type>, <B2B|B2C>, <mode: self|manager|peer>, <date>
Transcript     : quality tier, speaker-label status, complete/partial
Fatal moment   : quoted + located, or "none found"
Self-assessment: the rep's own read, captured before scores (manager/peer mode)
Per dimension  : score /4 (or N/A + reason), confidence, quote(s) + location, one-line why
Shape          : one sentence on where strength and weakness cluster (not the total)
Strengths      : <=2, each quoted
Change items   : <=3, ranked per Bounded feedback, class tagged, each SBI-shaped with quote
The one thing  : single named focus behaviour, observable and re-executable
Next-review check : what observable change on the next call counts as success
```

## Quality gate

Score the drafted review against all ten before delivering. Pass threshold: 10/10. Iterate until nothing fails.

1. Every scored dimension cites at least one verbatim quote with a findable location; every unscored dimension says N/A-with-reason or "insufficient evidence".
2. The transcript quality tier is declared before any score, and no dimension rests on a single garbled or ambiguous line above Low confidence.
3. N/A dimensions are out of every aggregate; nothing structurally absent is scored zero.
4. Feedback is bounded: at most 2 strengths (each quoted), at most 3 change items, exactly one focus behaviour phrased as an observable action. Each change item carries its class, the items follow the Bounded feedback ranking, and any deviation names the Interview answer or rep context that moved them.
5. Every change item is SBI-shaped; no personality or character language anywhere in the review.
6. Any fatal moment is named above the scores, however good the numbers look.
7. The call's outcome appears as context only and justifies no score.
8. In manager/peer mode, the rep's self-assessment was captured before scores were revealed, or its absence is explicitly noted.
9. Every statistic names where it comes from, and every vendor number is also marked correlational.
10. The review states the next-review check: the observable change that would count as the focus behaviour landing.

## KPIs and measurement

- The review worked if the named focus behaviour observably changed on the next reviewed call - compared at quote level, not by impression. That is the primary KPI; a review that produced no behaviour change was a document, not a review.
- Process KPIs per review:
  - 100% of judgements quoted.
  - Review consumable in under 30 minutes.
  - The rep can restate the one thing unprompted at the end.
- Across reviews: the same behaviour remaining the focus for three consecutive reviews signals the feedback isn't landing - surface that signal to the human; deciding what to do about it (coaching plan, role-play cadence) is out of this skill's scope. Rep self-scores converging toward reviewer scores over time is the calibration-health signal.

Optional integration note: call recording tools, transcription/ASR services, and conversation-intelligence platforms are categories - any tool of the class supplies the transcript, and the skill works from a pasted transcript with none of them.

## Reference

- See [references/rubric-anchors.md](references/rubric-anchors.md) for the anchored 0/2/4 behavioural descriptors, per-dimension evidence cues, and the optional B2C compliance dimension.
- See [references/review-template.md](references/review-template.md) for the fill-in review template with B2C/contact-centre adaptations.
- See [references/worked-examples.md](references/worked-examples.md) for a worked review built on a published, sourced cold-call teardown, plus an annotated counter-example of a bad review.
- `mbfinotti/sales-skills@cold-call-opener` - build or rewrite an opener script; this skill grades the one on tape.
- `mbfinotti/sales-skills@sales-discovery-questions` - build a discovery question set; this skill judges the questions asked.
- `mbfinotti/sales-skills@sales-objection-handling` - write objection rebuttals; this skill scores how the live objection was handled.
- `mbfinotti/sales-skills@deal-red-flags` - review free-text deal notes for red flags, a different artifact than call transcripts.
- `mbfinotti/sales-skills@sales-hiring` - reuse this rubric to score new hires' live calls during ramp with evidence-quoted discipline.
