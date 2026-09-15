---
name: influencer-outreach
description: Draft the personalized first-touch pitch message and follow-up plan used to propose a partnership to one already-vetted influencer or creator - personalization angle, the compensation stated on offer, a message fitted to the channel the creator actually lists (email, DM, or their manager), and a bounded follow-up cadence. Covers B2C brand collabs and B2B creator programs (newsletter writers, podcasters, industry experts). Use whenever the user mentions pitching a creator, DMing an influencer, a collab proposal, or a creator outreach message, even if they never say outreach. Stops at the first positive reply. Do NOT use for list-scale affiliate recruitment - use mbfinotti/partnerships-skills@affiliate-recruitment-outreach instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.10"
---

# Influencer Outreach

Draft the first-touch pitch and follow-up plan a partnership manager uses to propose a collaboration to one individually vetted influencer or creator, then stop at the first positive reply.

No named industry-standard framework exists for creator pitching. Published guidance is a scatter of single-outlet formulations, none branded or adopted cross-vendor:

- one vendor's soft-CTA vs. specific-ask split
- one commerce guide's four-question first-message checklist
- one consultant's unnamed six-step process

Never present any of them as a standard.

## Interview

Ask before drafting anything. One question per message; offer multiple-choice answers when possible. Skip any question the user already answered.

- Is this a B2C brand collab or a B2B creator program? (Product sold to consumers vs. to businesses - drives message framing and deliverable types.)
- What does the brand make, and what is the one-line reason this creator's audience would care?
- Who is the creator, on which platform(s), and what evidence says they fit? (Specific posts, audience data, a discovery brief - fit evidence is required input, not something to invent here.)
- What compensation model is on offer, with the actual number? (Flat fee $X / commission % + attribution window + payout schedule / gifted product only / hybrid.) This skill communicates the offer; it never designs or adjusts it.
- What campaign shape do you have in mind - rough deliverables and timing? (Stays a one-line sketch in message one.)
- What contact does the creator actually list: business email, DM only, or a manager/agent?
- What is the brand voice? (Formal, peer-casual, playful - or point to an example message.)
- Who signs, from which address or account?
- Which CTA can you actually honor: reply-for-details, product sample on reply, a short call, or an application link? (Anything you cannot honor this week is deleted from the menu, not ranked low.)
- By when does a reply have to land - is there a launch or campaign date this pitch must beat? (A hard date promotes the near-zero-effort angles, the reply-for-details CTA, and the single-follow-up cadence; no date lets an hour of grounding and the longer cadence pay off.)
- One-off win, or a relationship you intend to compound? (Compounding promotes the manager route and the long-tail cadence; one-off promotes the creator's own listed contact and a hard stop at three messages.)
- What is your effort ceiling per pitch - hours for grounding, product you can ship, calendar you can offer? (An hour of grounding buys the content-specific angle; no product deletes the sample CTA; no calendar deletes the call CTA.)

Every ordering this skill gives is a default, not a law: it shifts with context and with who executes it. Re-rank it against what you already know about this user before proposing anything, then say which answer moved which option:

- an existing relationship with this creator or their manager
- a brand the creator already recognizes
- audience data already in hand
- no product to gift at all

## Workflow

1. Run the Interview; collect every answer before writing a word.
2. Ground the personalization: if you can browse the web, load the creator's two or three most recent posts and confirm the fit evidence yourself; otherwise ask the user for the specific post, series, or audience trait the pitch will cite. Never fabricate familiarity.
3. Confirm the recipient against [references/channel-and-manager.md](references/channel-and-manager.md). The creator's published business contact decides it; where more than one is published, the default order is `listed manager > listed business email > DM`. Going around a listed manager is a failure mode, not a shortcut.
4. Enter brainstorming mode for the personalization angle: propose 2-3 candidate angles with trade-offs and a recommendation, phrased in the manager's own vocabulary (angle, hook, fit, deliverable, CTA). Draw them from the ranked angle menu in [references/pitch-anatomy.md](references/pitch-anatomy.md) - default order `already-recommending > recent launch > specific content > their-product-we-use > format fit > asserted overlap` - and delete any angle that is not true of this creator instead of offering it low.
5. Ask brainstorming questions one at a time. Write no message until the manager explicitly picks an angle.
6. Draft the first touch per [references/pitch-anatomy.md](references/pitch-anatomy.md), fitted to the confirmed recipient. Pick the one CTA from that file's ranked menu - default order `reply for details > sample on reply > short call > application link` - and drop any the brand cannot honor. Compensation transparency follows the model:
   - commission offers front-load exact mechanics
   - flat-fee offers name the model without dumping a rate card
7. Draft the follow-up plan per [references/follow-up-cadence.md](references/follow-up-cadence.md): default order `two follow-ups > one follow-up > long tail`, then close the file.
8. Run your preferred humanizer skill over the pitch and every follow-up. Never ship raw first-draft model output as final - AI-tell phrasing is exactly the mass-template smell that gets a pitch deleted on sight.
9. Self-check against the Quality gate below; redraft and re-run the humanizer until every item passes.
10. Present the package section by section - angle, first touch, follow-up plan, stop rule - and validate each with the user before finalizing.
11. Hand off the full artifact (next section). On a positive reply, this skill's job is done: carry the stated compensation facts into negotiation unchanged.
12. If your harness has persistent memory, memorize the approved angle, brand voice, compensation facts, and the outcome once known - later pitches for the same brand then skip straight past most of the interview.

## Invocation and expected output

Typical invocations:

- "Pitch @plantsbypriya for our ceramic planter launch - she's vetted, 48k on Instagram, offer is gifted product plus 15% commission."
- "Write the first-touch email to the DevOps newsletter writer from our shortlist - $2,000 sponsored deep-dive, she lists a partnerships email."

Deliver one structured artifact:

```
INFLUENCER PITCH PACKAGE - <creator>, <date>
Chosen angle   : approved personalization angle + why it beat the alternatives
First touch    : subject (email only) + message body, fitted to the confirmed channel
Follow-up plan : table - touch / day / channel / angle / one-line summary
Stop rule      : positive reply -> stop and hand off; silence after final touch -> close the file
Handoff notes  : compensation facts as stated, deliverables mentioned, CTA promised - for the negotiation stage
```

## B2B and B2C

- **B2B**
  - Speak to a business need the creator's audience has, not just a product benefit - the one consistently documented B2B-specific rule.
  - Deliverables skew to webinars, white papers, articles, and podcast reads.
  - Gifting is documented B2B practice, but shaped differently than in B2C: extended platform access, a conference pass, a beta invite, or event hosting, rather than a physical product. Zapier's creator-partner retreat is a real named example, and a 2025 industry report ranks in-person gifted events as the second most effective B2B creator content type after social posts. Where none of those forms fit, default to a fee or a commission.
  - Expect longer, multi-stakeholder buying cycles to shape what "conversion" means in the pitch.
- **B2C**
  - Deliverables skew to posts, videos, and stories.
  - Gifting and commission offers are common and well documented.
- Honest limit: the pitch-anatomy and cadence guidance here is published unsegmented by business model, which weakly suggests practitioners treat it as universal. Apply it to both, knowing that universality is an inference, not a documented rule.

## Quality gate

The gate splits by message type: a follow-up is capped at one or two sentences with nothing from the first touch restated (see the cadence reference), so it cannot carry the compensation terms or the full email structure.

Scoring a follow-up against the first-touch list would make the gate unpassable and the loop below never terminate. Iterate, redraft, and re-run the humanizer until nothing fails.

**First touch - all nine items, 9/9.**

1. Opens on one verifiable, creator-specific fact (a named post, series, or audience trait) framed as audience fit, not flattery.
2. The swap test: replacing the creator's name with another creator's would force a rewrite. If the message survives the swap, it is a template.
3. Compensation model and the real number are present and match the interview exactly.
   - Commission pitches state rate, attribution window, and payout schedule.
   - Flat-fee pitches name the model without a rate card.
   - Gifted-only pitches say so plainly and never imply payment.
4. Exactly one ask, low-friction, matching a CTA the manager confirmed they can honor.
5. Fitted to the confirmed channel: full structure for email, 2-4 sentences and no links for a DM, addressed to the manager when one is listed.
6. None of the documented negative signals: generic salutation, emoji-bait subject, fabricated familiarity, feature dump, rate-card dump, aggressive negotiation language, long campaign proposal.
7. B2B pitches state the business need; B2C pitches state the audience-purchase fit.
8. No disclosure language, contract terms, or exclusivity demands - documented practitioner workflows place all of these after agreement, never in the cold pitch.
9. Passes the humanizer and reads human when spoken aloud.

**Every follow-up - items 4, 6, 8 and 9 above, plus these three, 7/7.**

10. One or two sentences. Nothing from the first touch restated.
11. Carries one new small angle - a proof point held back from message one, an easier version of the ask, or a genuine timing hook. Never "just checking in", "bumping this", or "did you see my email?".
12. Low pressure: no guilt-tripping, no invented deadline, nothing that reads as chasing. Silence is busy, not rejection.

Items 1, 2, 3, 5 and 7 are first-touch content by construction and are not scored on follow-ups. Item 11 does the work item 2 does on the first touch: a follow-up that could be sent to any creator unchanged fails it.

## KPIs

- No trustworthy reply-rate benchmark exists for creator outreach. The only survey on the topic explicitly declines to publish one. Never quote any of the circulating figures as fact or as a target - each traces to broken citations or a single-source self-report:
  - an "8.5% reply rate"
  - a "99% ignored" claim for generic salutations
  - one practitioner's self-reported "90% response rate"
- Benchmark against your own log instead: track every pitch in a flat table (creator, channel, angle, sent date, follow-ups used, outcome, days-to-reply). After a dozen pitches, your own reply rate per angle and per channel is the benchmark that matters.
- Core KPIs:
  - reply rate (any response)
  - positive-reply rate (open to talking)
  - days to first reply
  - which angles produced pitches that survived negotiation, recorded after the downstream stage closes
- If your harness has persistent memory, keep the log there across sessions; otherwise hand the table to the user to maintain.

## Common failure modes

| Failure                                                   | Fix                                                                                                                    |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Template smell - personalization swappable to any creator | Rerun the angle brainstorm; cite one verifiable specific; apply the swap test                                          |
| Compensation question buried or omitted                   | State model + real number per the anatomy rules; vagueness reads as a lowball                                          |
| Copying a paid-collab template for a commission offer     | Commission flips the risk onto the creator - front-load rate, window, payout, per-sale estimate                        |
| Pitching the wrong channel                                | Re-run the recipient gate in step 3 before anything else - the published contact decides, the ranking only breaks ties |
| Ignoring or going around a listed manager                 | Pitch the manager with full personalization; go direct only when the creator has asked for it                          |
| Fabricated familiarity ("longtime fan of your work")      | One verifiable specific, or say honestly how you found them                                                            |
| Rate card or full campaign proposal in message one        | One-line deliverable sketch; details belong after the reply                                                            |
| Disclosure, contract, or exclusivity terms in the pitch   | Post-agreement topics; route disclosure to the compliance skill                                                        |
| Negotiating in the pitch thread after a positive reply    | Stop - the handoff notes carry the facts into the negotiation stage                                                    |

## Reference

- See [references/examples.md](references/examples.md) before writing copy - a positive B2C and B2B example with follow-up plan, and a line-by-line annotated negative example.
- See `mbfinotti/partnerships-skills@influencer-discovery-brief` for choosing and vetting which creator to pitch - this skill assumes that work is done.
- See `mbfinotti/partnerships-skills@influencer-negotiation-playbook` for everything after the creator replies with interest.
- See `mbfinotti/partnerships-skills@influencer-campaign-brief` for the creative brief once the deal is signed.
- See `mbfinotti/partnerships-skills@affiliate-recruitment-outreach` for recruiting affiliates across a prospect list rather than pitching one vetted creator.
- See `mbfinotti/partnerships-skills@affiliate-disclosure-compliance` for the disclosure obligations that attach once a material connection exists.
