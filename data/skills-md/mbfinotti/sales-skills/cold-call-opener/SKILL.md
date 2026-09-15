---
name: cold-call-opener
description: Writes the opening 5-30 seconds of a live outbound cold call - a tailored opener for a named persona and pain point, with 2-3 testable variants, delivery notes, and a measurement plan. Covers B2B and B2C phone outreach, including do-not-call scrubbing. Use whenever the user mentions a cold call opener, cold call script, phone opener, dialer talk track, "what do I say when they pick up", or opening a call for a persona, even if they don't say "opener" explicitly. Do NOT use for rebuttals later in the call (use mbfinotti/sales-skills@sales-objection-handling), grading a recorded call (mbfinotti/sales-skills@sales-call-review), or cadence planning (mbfinotti/sales-skills@sales-outbound-sequence).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.3"
---

# Cold Call Opener

Draft what a rep says between "hello" and the prospect's first real response. The opener ends the moment the prospect engages or brushes off - everything after that belongs to a neighboring skill (see References). The published evidence on opener wording comes almost entirely from two Gong datasets that contradict each other, plus Cognism's funnel data. This skill reports each source honestly instead of blending them into a fake industry benchmark.

## Interview

Ask before drafting anything. One question per message; offer multiple-choice answers when possible. Skip any question the user already answered.

- B2B or B2C? (If both, draft separate openers - the pain framing and the legal scrubbing differ.)
- Who picks up: title and seniority? (IC / manager / director-VP / executive / business owner / consumer.)
- What does the product do, in one plain sentence a stranger would understand? Refuse feature lists; one sentence.
- What pain do you believe this person has, in their words?
- Where did that pain hypothesis come from: a verified signal (job posting, funding, tool change, something they said or submitted) or an educated guess? This decides the wording, not just the confidence.
- Desired outcome of the call: booked meeting / qualification / referral to the right person / (B2C) quote, appointment, or sign-up?
- List temperature: fully cold, warm-ish (prior touch, inbound form), or a re-attempt?
- If a re-attempt: what happened on the previous attempts?
- How does the rep naturally talk: direct, warm, understated, high-energy? (Or paste two sentences of how they actually speak.)
- Which market/jurisdiction is being called: US / UK / EU member state (which one) / France / other? For B2C this drives mandatory scrubbing - see [references/consumer-calling-constraints.md](references/consumer-calling-constraints.md).
- By what date must this opener be booking meetings? (Inside two weeks promotes the cheapest pattern and caps the test at one variable; a quarter or more makes the research-heavy pattern affordable.)
- One-off win or compounding asset: a script for one campaign push, or the team's default opener for the year? (One-off promotes direct reason-for-call; compounding promotes permission-based, whose rehearsal cost is paid once and collected on every call after.)
- Effort ceiling: rehearsal hours per rep, months of phone tenure behind them, and minutes of pre-call research affordable per account. (Near-zero research minutes removes context-first/peer-proof from the menu for this run; a first-week rep promotes direct reason-for-call to first.)

## Opener anatomy

Four components, one length budget. The whole opener runs 5-30 seconds of rep speech, then stops.

Stay short for two reasons:

- Chris Beall's framing: a cold caller has roughly seven seconds to establish trust, since curiosity, not value, is what avoids triggering reactance.
- Jason Bay's observation, quoted in Cognism's 2025 report: only 10% of cold calls make it past 2 minutes. An opener that eats 45 seconds has already spent a third of the median call before the prospect says a word.

1. **Identification** (~3-5s). Full name plus company. Honest, unhurried, no fake familiarity.
2. **Reason-for-call** (~5s). One sentence naming why this person, today. Gong credits John Barrows with the test: if the rep cannot finish "the reason for my call is...", do not make the call.
3. **Pain hypothesis** (~10s). One spoken sentence the prospect recognizes as their own problem. Rules in Pain-hypothesis line below.
4. **Ask / transition** (~5s). Exactly one ask, matched to the desired outcome from the interview. Then stop talking.

Working cap: about 75 words, a self-set bar rather than a published one. Verify with a read-aloud timer, not a word counter alone.

## Workflow

1. Run the Interview; collect every answer first.
2. If you can browse the web, verify the pain signal (job posting, funding news, public statement); otherwise ask the user for the evidence. Never invent a signal. For turning raw signals into angles, see `mbfinotti/sales-skills@sales-outreach-personalization`.
3. Enter brainstorming mode: propose 2-3 candidate angles (each = one opener pattern + one pain framing). Score every candidate on the three axes Choosing the pattern uses:
   - Measured value.
   - Rep effort (rehearsal, live composure, how it fails in unskilled hands).
   - Conversations needed before it can be judged.

   Recommend one and name the axis that decided it. Ask questions one at a time. Draft nothing until the user picks an angle.

4. Pick the pattern with the ranking in Choosing the pattern; open [references/opener-patterns-and-evidence.md](references/opener-patterns-and-evidence.md) only for the full evidence trail behind a rate or an attribution.
5. Draft 2-3 variants. Each variant isolates exactly one variable (pattern, pain wording, or ask) against the others; a variant that changes two things teaches nothing.
6. Write delivery notes per variant (Delivery below).
7. Run your preferred humanizer skill over every variant, then read each aloud with a timer. A cold call opener is speech; raw first-draft model output is never the final deliverable.
8. Score every variant against the Self-check gate; iterate until all items pass.
9. Hand off the artifact in Expected output, including the test plan.
10. If your harness has persistent memory, memorize the approved persona, pain hypothesis, product sentence, and - once tested - the winning opener; later runs then skip the interview.

## Choosing the pattern

Rank patterns by what they return per unit of rep effort, and say the ranking out loud instead of letting row order imply it. Effort here is rehearsal time, live composure, and how badly the pattern fails in an unskilled rep's hands - a pattern that is strong for a veteran and damaging for a new rep is high-effort, not high-value. Full evidence, attributions, and the Gong 2018/2024 contradictions sit in [references/opener-patterns-and-evidence.md](references/opener-patterns-and-evidence.md).

The axes disagree, so each gets its own line:

- efficiency: permission-based > direct reason-for-call > context-first/peer-proof > pattern interrupt
- value: context-first/peer-proof == permission-based > direct reason-for-call
- effort: pattern interrupt > context-first/peer-proof > permission-based > direct reason-for-call

That `==` is a real tie, not a way of avoiding the call. Gong's 2024 study separates those two by 0.06 percentage points and publishes no per-opener sample size, so nothing in the data can order them. They split on effort instead.

No compliance-cost axis belongs on this menu. Consent and scrubbing duty attaches to the list and the jurisdiction, identically for every pattern (see [references/consumer-calling-constraints.md](references/consumer-calling-constraints.md)).

1. **Permission-based** - the default rung.
   - Value: ~11% of connected calls produced a held meeting in Gong's 2024 study, roughly 5x that study's worst-scoring opener.
   - Effort: about an hour of rehearsal, paid once and collected on every call after. The rep names the interruption without flinching, then actually stops talking.
   - Fails softly: rushed, it sounds like an apology, which costs that call and nothing else.
   - Guessed pain routes here, with the pain line hedged (see Pain-hypothesis line). A guess asserted as fact hands over the top-five brush-off "I don't have the problem you're describing" (Cognism 2025).
2. **Direct "reason for my call"** - the cheapest, and the only one that composes.
   - Value: about double baseline in Gong's 2018 study, the smallest measured lift on this menu. Gong describes it as pairable with any other opener, so it never fully loses a round.
   - Effort: minutes. One sentence, tested by John Barrows' rule: if the rep cannot finish "the reason for my call is...", do not make the call.
   - Promote it to first when any of these hold: a hard deadline, a rep in their first weeks, a re-attempt (name the prior attempt honestly, never pretend it is the first call), or an owner, SMB, or consumer line.
   - On a consented B2C list, the consent event _is_ the reason for the call ("you asked for a quote on our site Tuesday").
3. **Context-first / peer-proof** - tied for best measured value, an order of magnitude more effort.
   - Effort: pre-call research per account, plus the composure to defend a peer claim when the prospect challenges it live.
   - Fails hardest: an unsupportable name-drop or surveillance-flavored trivia loses the call outright, the personalization-backfire pattern documented in the reference.
   - State the verified signal before the ask.
   - Promote it above permission-based only when all three hold: director or above, a verified strategic signal already in hand, and a rep who has run the play before.
4. **Pattern interrupt** - last, and deliberately unranked on value. No dataset isolates it, so a number here would be false precision dressed as evidence.
   - Effort: high. Live improvisation, no script to fall back on.
   - Practitioners report the payoff decays as a novelty goes mainstream. Reported, not measured.
   - Use sparingly.

**Deleted, not demoted.** Small-talk openers ("How have you been?", "How's your day going?") are off this menu.

- The only forms either Gong dataset measured are addressed to a stranger, which fails this skill's own self-check gate on fabricated familiarity.
- An option the constraints rule out has to be removed: parked at the bottom, it comes back as a variant.
- Its evidence stays in the reference as a contradiction to report, never as an option to offer.

**What this order starves.** Context-first/peer-proof ties for the highest measured value and loses every efficiency round on research cost, the standard failure of ratio-ranking. Promote it deliberately on a short, durable list of high-value director+ accounts, where per-account research is affordable.

Gong's seniority conditionality applies here: company-specific personalization pays most at director+, measured on email reply rates. Carrying it to calls is therefore an inference rather than a finding.

**Re-rank before drafting.** This order is a default, not a law: it shifts with context and with who executes it. Re-rank against what you already know about the user, then name which interview answer moved which pattern when presenting the choice.

- A veteran rep moves context-first up.
- A first-week rep moves it off the menu.
- A warm list or a re-attempt promotes direct reason-for-call.
- A persona who rarely picks up (B2C especially, see B2B vs B2C) raises the effort cost of every connect, which promotes the cheap patterns further.

## Pain-hypothesis line

- Write one sentence a prospect would recognize as their own words. Test: would they say this out loud themselves? If not, rewrite from their vocabulary, not the product's.
- Zero jargon, zero feature language. The line names the problem, never the solution.
- Concrete beats abstract: "your SDRs are booking off a list that's a year stale" beats "data quality challenges".
- Verified signal: lead with the observation and let it carry the relevance - it needs no hedging.
- Guessed pain: hedge it as something heard from peers ("Most ops leads I talk to at firms your size tell me X - I'm guessing that's on your plate too, but you'd know better"). Hedging makes disagreement cheap for the prospect instead of confrontational, and turns the assertion into a question.
- Never state a guess as a fact about their company, and never imply research the rep did not do.

## B2B vs B2C

Identical in both - say so, do not re-derive:

- The four-part anatomy.
- The 5-30 second budget.
- The one-ask rule.
- The pause discipline.
- The humanizer pass.
- The variant-testing method.

What differs:

- **Who answers.** B2B: the titled persona from the interview, behind a switchboard or direct dial. B2C: whoever owns a personal line - Hiya's State of the Call 2026 (a survey of 12,000+ consumers across six countries) found only 14% immediately answer calls from unrecognized numbers, so expect a lower answer floor and more re-attempts.
- **Pain framing.** B2B: a business outcome the persona is measured on. B2C: money, time, or hassle in plain household words - no business vocabulary at all.
- **The ask.** B2B: usually a calendared meeting or a referral. B2C: usually the conversation itself - a quote, an appointment, a sign-up - so the transition often continues the same call rather than booking a future one.
- **Regulatory scrubbing.** Consumer calling sits under consent-based regimes. B2B is mostly carved out, with exceptions. Before any B2C list is dialed: check the jurisdiction's do-not-call register and consent basis, and keep an internal do-not-call list. Jurisdiction specifics (US, EU, UK, France - including France's consumer opt-in regime effective 11 August 2026) are in [references/consumer-calling-constraints.md](references/consumer-calling-constraints.md). Factual note, not legal advice: have counsel confirm before a campaign.

## Delivery

- Pace: unhurried. Rushing signals fear; the identification especially gets said slowly.
- Tone: match the rep's natural register from the interview - a script in someone else's voice reads as a script.
- Stand up, or sit upright: breath support carries energy down a phone line. Practice advice, not a measured effect.
- After the ask: pause, and do not fill the silence. The ask ends the opener; whoever speaks next is the prospect.
- **Rhythm.** Gong's call data shows successful cold calls are not interrogations.
  - No statistical difference in the number of questions asked.
  - Successful calls contain _longer_ rep monologues (37s vs 25s longest burst).
  - Prospects' longest turns are _shorter_ on successful calls (3.5s vs 8s).
  - Successful calls show 77% more speaker switches per minute.

  Read together, this means: deliver the opener as one confident monologue, then stop cleanly. Keep the exchange brisk after that, with short turns and fast back-and-forth.

  Do not read this as "talk over the prospect." Do not teach "listen more, talk less" as if the data supported it. On these measures, it points the other way.

## Variants and testing

- Produce 2-3 variants per run, never one. One variable isolated per variant.
- Sequence the test: run variants in alternating blocks on comparable list segments, same daypart, same rep.
- Judging threshold: do not compare variants before roughly 100 conversations each - a working convention, since no vendor publishes a cold-call sample-size benchmark. At Cognism's 2025 connect-to-conversation rate (65.6%), that is roughly 150 connects per variant. That is the unit price of every option on the pattern menu: each variant kept costs another ~150 connects before it says anything.
- Treat small gaps as noise: the 0.06-point gap that ties the top two patterns in Choosing the pattern is the scale of what a test this size cannot separate. A difference that small is a coin flip, not a winner.

## Measurement

Track per variant, in the dialer or call recording tool:

- **Connect-to-conversation rate** - connects that become a real dialogue. Benchmark: 65.6% (Cognism 2025, computed from 41,936 connects producing 27,513 conversations). This is the opener's own KPI: the opener is what turns a pickup into a conversation.
- **Meetings booked per conversation.** Benchmark: 2.7% industry average (Cognism 2026); Cognism's internal team reports 11.3%, so the average is a floor, not a ceiling.
- **Early hang-up rate** - share of connects ending inside ~30 seconds. No vendor publishes this as a benchmarked KPI; compute it from call-duration distributions (see the source ranking below).
- **Conversation length** - trend it against the team's own baseline only. Cross-vendor averages disagree (Cognism 82-93s; Chorus 132s; Gong 5:50 successful vs 3:14 unsuccessful) because each measures different populations with different definitions.

Two places those numbers can come from, and the axes disagree:

- value: recorded-call duration data > dialer dispositions. Chorus found 40% of cold calls are mis-dispositioned or not dispositioned at all, so dispositions measure rep habits as much as prospect behavior.
- compliance cost: recorded-call duration data > dialer dispositions. Recording triggers a disclosure obligation and a retention decision, and consent rules vary by jurisdiction (all-party consent in several US states, notification duties in the EU and UK). Dispositions trigger neither. Cost it as the review it forces - legal sign-off once per jurisdiction dialed - and as reversibility: a recording cannot be un-made.
- Default: recorded duration data, with the disclosure cleared once per jurisdiction before the test starts. Fall back to dispositions only where recording is not cleared, and mark the early hang-up number directional.

Iteration target this skill chases: connect-to-conversation at or above the 65.6% Cognism benchmark, and meetings per conversation at or above the 2.7% average. If a variant sits below either after the judging threshold, change one variable and rerun. Keep iterating until a variant clears both.

## Self-check gate

Every variant passes all items before handoff. Iterate - redraft, re-run the humanizer - until none fail.

1. Read aloud at natural pace in 30 seconds or less (~75-word working cap).
2. Exactly one ask, matching the outcome the user chose in the interview.
3. Pain sentence passes the would-they-say-it-out-loud test; no jargon; no feature language.
4. Guessed pain is hedged; verified pain names its real signal.
5. No fabricated familiarity, no implied prior relationship, no research claims the rep cannot back.
6. Identification is honest: full name plus company.
7. Ends on the ask followed by a planned pause - no trailing filler.
8. Reads human aloud after the humanizer pass.
9. B2C only: list scrubbed for the jurisdiction and consent basis confirmed.

## Common failure modes

| Failure                                                         | Fix                                                                                                                         |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Sounds like a script                                            | Humanizer pass + read-aloud; contractions; the rep's own vocabulary from the interview                                      |
| Over-long opener                                                | Cut to one pain sentence; 30-second timer is the law                                                                        |
| Fake familiarity ("How have you been?" to a stranger)           | Cite a real signal or drop the claim; small-talk openers are off the pattern menu, not a judgment call                      |
| Stacked questions                                               | One ask; park the rest for discovery                                                                                        |
| Asking for time the rep does not need ("Can I get 30 minutes?") | Ask for the conversation already in progress                                                                                |
| Feature dumping                                                 | The opener names a pain, never describes the product beyond the one-liner                                                   |
| Apologizing for calling ("sorry to bother you")                 | Own the interruption instead - the permission-based pattern names it without apology                                        |
| Inviting the exit ("Did I catch you at a bad time?")            | Both Gong datasets rank better options (0.9% in 2018; 2.15% in 2024 - the two disagree on the baseline, not on the ranking) |
| Treating the opener as discovery                                | One hypothesis, one ask; question batteries belong after engagement                                                         |

## Expected output

```
COLD CALL OPENER - <persona>, <product>, <date>
Chosen pattern : <pattern> + the axis that decided it against the other candidate angles
Variant A/B/C  : verbatim opener + the one variable it isolates
Delivery notes : pace, pause points, tone - per variant
If brush-off   : hand to mbfinotti/sales-skills@sales-objection-handling
If engaged     : hand to mbfinotti/sales-skills@sales-discovery-questions
Test plan      : conversations per variant, KPIs, thresholds, judge date
Compliance     : (B2C) jurisdiction + scrub/consent confirmation
```

Full worked examples - two B2B, one B2C, one annotated negative - are in [references/example-openers.md](references/example-openers.md), never inline here.

## Reference

- See [references/opener-patterns-and-evidence.md](references/opener-patterns-and-evidence.md) after choosing a pattern - the evidence trail, attributions, and dataset contradictions behind the rates quoted in Choosing the pattern.
- See [references/example-openers.md](references/example-openers.md) before drafting - worked B2B and B2C openers plus a negative example with the reasons it fails.
- See [references/consumer-calling-constraints.md](references/consumer-calling-constraints.md) before dialing any B2C list - per-jurisdiction scrubbing notes.
- See `mbfinotti/sales-skills@sales-objection-handling` for what follows a brush-off.
- See `mbfinotti/sales-skills@sales-discovery-questions` for what follows engagement.
- See `mbfinotti/sales-skills@sales-call-review` for scoring recorded calls against a rubric afterward.
- See `mbfinotti/sales-skills@sales-hiring` for the hiring loop's mock-call work sample, which draws on this skill's opener craft when writing realistic scenario material for an SDR/high-velocity candidate exercise.
