---
name: influencer-negotiation-playbook
description: Prepare a brand-side partnership manager to negotiate deal terms with an influencer or creator, from the creator's first positive reply to a signed contract - a written playbook of term-by-term opening positions, a concession ladder, red-flag responses, and walk-away thresholds covering rates, usage rights, exclusivity, revision limits, payment terms, and kill fees. Covers B2C brand collabs and B2B creator programs. Use whenever the user mentions creator rates, creator deal terms, usage rights, exclusivity, or negotiating with a creator's talent manager, even if they never say negotiation. Requires the user's own rate benchmarks. Do NOT use for the first-touch pitch - use mbfinotti/partnerships-skills@influencer-outreach instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.7"
---

# Influencer Negotiation Playbook

Build the playbook a brand-side partnership manager takes into deal-term negotiation with one creator. The window opens when the creator replies with interest and closes at contract signature.

No named negotiation framework (BATNA/ZOPA, tactical empathy, Ackerman, MESO) is documented as genuinely used in creator deal-making - targeted searches of two high-volume trade publications returned zero hits tying any of them to creator deals. This skill therefore uses plain working vocabulary (opening position, concession, walk-away threshold) and brands no method.

Nearly every quantified convention in its references traces to one vendor publication (Influencer Marketing Hub, mostly two staff writers, no survey backing, sometimes inconsistent between its own articles). Treat every such number as a negotiation range to pressure-test against the user's own rate intel, never as market price.

This skill prepares the human. It never:

- Negotiates on the user's behalf.
- Impersonates the user.
- Sends messages on the user's behalf.

It is not legal advice: final terms must land in a written contract reviewed by qualified counsel.

## Interview

Ask before drafting anything.

- One question per message, with multiple-choice answers when possible.
- Skip any question the user already answered.

- Is this a B2C brand collab or a B2B creator program (newsletter, podcast, industry expert)?
- Who is the creator, on which platform(s), and what tier/audience size?
- What do you want the creator to make - a rough deliverables sketch (formats, counts, timing)?
- What budget range is approved, and what rate intel or benchmark do you already hold? This skill does not benchmark rates - bring a range from past deals, the creator's rate card, or your own research.
- Which terms are must-haves and which are nice-to-haves?
- What usage rights do you actually need (organic repost, paid ads/whitelisting, duration, territory), and is competitor exclusivity required?
- By what date must the content be live - a fixed launch date, or a flexible window?
- Do you want a one-off campaign win, or a relationship that compounds into cheaper, faster deals later?
- What is your effort ceiling for running this deal - hours per week, whether anyone already owns tracking and payout reconciliation, and how much internal sign-off you can spend?
- Who negotiates - you directly with the creator, or via a talent manager/agency?
- What is your internal budget authority, and who signs off above it?

The live-by date, the one-off-versus-compounding answer, and the effort ceiling move the rankings in this skill. Re-rank every menu against them, and say which answer moved which option:

- A fixed date inside two weeks pins the flat one-off shape and deletes posting-date flexibility from the concession ladder.
- A compounding mandate promotes the retainer.
- A thin effort ceiling, or nobody owning attribution, deletes the hybrid flat+commission shape outright.

## Workflow

1. Run the Interview; collect every answer before drafting.
2. Gate on rate intel: if the user brings no rate range, stop and ask for one. Never build a rate benchmark - that is out of scope, and no sibling skill covers it either, so do not route the request onward as if someone else will answer it. Instead hand the user the three ways to get a band themselves, in this order, then wait:
   - efficiency: creator's own rate card > quotes from 3-5 comparable creators > the platform's published creator-earnings ranges
   - value (how well the number survives being challenged in the room): comparable quotes > rate card > published ranges
   - cost: comparable quotes (a week of outreach and waiting on replies) > published ranges (an hour of reading) > rate card (one message)
   - What each option buys, beyond the ranking above:
     - **Rate card**: leads on ratio, not on being free. One message puts a real number on the table, but it is the creator's ask, not a band.
     - **Comparable quotes**: the only option producing a band you can defend when the counterpart pushes. Recommend them whenever the campaign date is more than a couple of weeks out.
     - **Published ranges**: the fallback when neither is reachable. They stay a directional sanity check, never an opening position.
3. Enumerate every negotiable term separately using [references/deal-terms-landscape.md](references/deal-terms-landscape.md). Never negotiate "the deal" as one number.
4. Enter brainstorming mode on deal shape, working the ranked menu in Deal shapes below. Apply its deletion conditions first, propose the top surviving shape plus the one behind it, and name which Interview answer moved the order. Ask questions one at a time; draft nothing until the user picks a shape.
5. Set an opening position, a fallback, and a walk-away threshold for every term, per [references/concession-ladder.md](references/concession-ladder.md). Apply its anchoring decision rule explicitly - who names a number first is a sourced, unresolved tension, not a solved question.
6. Order the concession ladder by what each give buys back per unit of cost to you, not by which give is cheapest, using the ranked table in [references/concession-ladder.md](references/concession-ladder.md). Delete the rows its conditions rule out instead of carrying them to the bottom, and state the resulting order in the playbook.
7. Attach red-flag responses and, when a talent manager is involved, the manager-specific etiquette from [references/red-flags.md](references/red-flags.md).
8. Insert the disclosure gate: disclosure/FTC compliance is a non-negotiable condition of the deal, never a tradeable term. Route obligations to `mbfinotti/partnerships-skills@affiliate-disclosure-compliance`; do not restate regulation.
9. List what must reach the written contract (deliverables, usage tier, exclusivity scope+duration, revision cap, payment terms, kill fee, disclosure obligation, tracking).
10. Self-check against the Quality gate; iterate until every item passes.
11. Validate the playbook with the user section by section - terms, ladder, red flags, contract list - before finalizing.
12. Deliver the playbook with the reminder: the user negotiates, and counsel reviews the contract before signature.
13. If your harness has persistent memory, log the deal's opening vs. final terms once known (see KPIs); otherwise hand the user the log table to keep.

## Deal shapes

Step 4's menu, ranked. Three shapes carry a creator deal; the orderings disagree, so state the one you are using out loud:

- efficiency (payoff per round of negotiation and per week of ops): flat one-off > retainer > hybrid flat+commission
- value (total payoff over a quarter): retainer > hybrid > flat one-off
- cost (effort to set up and run): hybrid > retainer > flat one-off
- compliance cost: hybrid > retainer > flat one-off

Lead with the flat one-off because it wins the ratio, not because it is the smallest deal. The shape with the biggest payoff is also the one that costs a standing job to run, and only the ratio answers which shape to propose on Monday.

| Shape                            | What it buys                                                                                                          | What it costs you                                                                                                                                     | Compliance exposure                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Flat fee, one-off                | One campaign, delivered and closed, with usage and exclusivity priced as add-ons rather than bundled                  | One negotiation, hours of prep, nothing owed after signature                                                                                          | One time-boxed usage grant and one disclosure obligation; fully reversible once the window ends                             |
| Retainer / multi-campaign volume | A lower per-deliverable rate, reserved creator capacity, and a relationship that makes the next deal cheaper to close | Several more rounds, budget authority spanning a quarter, and standing relationship management                                                        | Exclusivity and usage windows running the retainer's full length - the hardest terms to unwind mid-flight                   |
| Hybrid flat + commission         | Pay that tracks outcomes, with downside protection if the campaign underperforms                                      | Attribution, reconciliation, and payout operations - a standing job, not a setup task - plus a higher fixed ask from a creator trading certainty away | Ongoing material-connection disclosure past the campaign, payout and tax handling, and commission terms counsel has to read |

Default: flat fee, one-off. Move up one rung to the retainer once a first deal with this creator has closed and repeat intent is real on both sides.

Delete, do not demote:

- Drop the hybrid from the menu entirely when tracking is not live before content posts or nobody owns payout reconciliation. An untracked commission is a dispute with a creator, not a deal shape - do not hold it in reserve as an over-budget bridge either.
- Drop the retainer when repeat intent is not real or budget authority stops at this campaign. Volume pricing bought against a commitment you cannot honour costs more than paying full rate once.
- Never present a deleted shape demoted "for completeness"; a ruled-out option in a menu gets picked eventually.

This order is a default, not a law: it shifts with the deal and with who runs it. Re-rank against what you already know about the user before proposing:

- An existing signed relationship with this creator puts the retainer first, because its negotiation and trust costs are already sunk.
- In-house legal plus a live affiliate program collapses the hybrid's cost and compliance axes and promotes it.
- A fixed launch date inside two weeks pins the flat one-off whatever else is true.

## Invocation and expected output

Typical invocations:

- "@plantsbypriya replied and wants to talk terms - 2 reels + 3 stories, budget $4-6k from our past deals. Build my negotiation playbook."
- "The DevOps newsletter writer is interested but her manager quoted double our budget. Prep me for the call."

Deliver one structured artifact:

```
INFLUENCER NEGOTIATION PLAYBOOK - <creator>, <date>
Deal shape        : chosen shape + its rank, which rivals were deleted and by which condition
Term positions    : table - term / opening / fallback / walk-away
Concession ladder : ordered trades - give / order / what it buys back
Red flags         : counterpart signal -> scripted response
Walk-away line    : total-budget ceiling + automatic-exit conditions
Non-negotiable    : disclosure obligation (gate, not a term)
To contract       : every agreed term that must appear in writing
```

## B2B and B2C

- Scope-before-rate sequencing, the written-contract requirement, the disclosure gate, and payment-term hygiene apply identically to both. Published guidance is unsegmented, which weakly suggests universality - treat that as an inference, not a documented rule.
- B2B documented specifics: funnel-stage tiered commissions (e.g. tiers at MQL/SQL/closed-deal), % of first-year ARR for high-ticket deals, newsletter pricing on CPM rather than flat fee, podcast mid-roll host-read CPM, and at least one major podcast marketplace publishing no rates at all (privately negotiated).
- LinkedIn now has documented relative rate shapes (consistent with this skill's base-rate-agnostic approach): a technical/SaaS creator commands roughly a 40-80% premium over a general professional-content creator of the same tier, format multipliers apply on top (carousel +20-35%, video +40-80%, newsletter placement 1.5-3x, a speaking slot ≈4x a sponsored post), and pricing varies by region (APAC roughly 30-60% below North America). YouTube has no published technical-versus-general rate split the way LinkedIn does - the closest figure found is one sponsorship-tracking platform's general Technology-niche CPM (SponsorRadar: $30-60, against $10-25 for gaming), directional only and not developer-specific. B2B exclusivity still has no published convention to inherit - set those terms explicitly instead of assuming B2C conventions transfer.
- B2C: the tier-based rate shapes, usage-rights ladders, and exclusivity conventions in the references skew B2C - apply them there with normal caution about how each number was produced.

## Quality gate

Score the playbook against all eleven items. Pass threshold: 11/11. Iterate until nothing fails.

1. Every negotiable term has an opening position AND a fallback AND a walk-away threshold - no term carries only one number.
2. Deliverables scope is fully defined before any rate appears; price tracks scope 1:1.
3. No number is presented as an industry standard; every vendor-sourced figure is labeled as one vendor's convention and framed as a range.
4. Rate positions trace to the user's stated rate intel, not to figures this skill supplied.
5. Disclosure appears only in the non-negotiable section - never on the concession ladder.
6. Usage rights and exclusivity are each time-boxed with priced extensions; no perpetual or open-ended language survives anywhere.
7. Revision rounds are counted and capped, with re-pricing defined beyond the cap.
8. Every ladder step names what the concession buys back; nothing is given for free.
9. Payment terms state a specific net window; the anchoring decision rule was applied explicitly, not defaulted.
10. The playbook ends with the written-contract checklist and the counsel-review reminder.
11. The chosen deal shape is the top-ranked shape surviving its deletion conditions, or the playbook names the Interview answer that overrode the default order.

## KPIs

- No trustworthy public benchmark exists for creator-deal negotiation outcomes. Never invent or quote one.
- Log every deal instead: terms asked, terms won, concessions given, final vs. opening on each term, days from positive reply to signature.
- After a handful of deals, the user's own history is the benchmark: concession patterns, terms that always slip, realistic days-to-signature.
- If your harness has persistent memory, keep the deal log there across sessions; otherwise hand the table to the user to maintain.

## Common failure modes

| Failure                                               | Fix                                                                                                                     |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Negotiating rate before scope is defined              | Lock the deliverables list first; every rate discussion references a fixed scope                                        |
| Treating usage rights as a throw-in                   | Price usage as its own term - duration, organic vs. paid, territory - it is a top-value clause                          |
| Open-ended exclusivity                                | Time-box it, restrict to named competitors, price extensions per period                                                 |
| Unlimited revision rounds                             | Cap included rounds in writing; define minor vs. major; price rounds beyond the cap                                     |
| Scope creep answered without re-pricing               | Acknowledge the added deliverable, name it specifically, attach a revised price immediately                             |
| Perpetual-usage language accepted                     | Replace with a time-boxed license plus pre-agreed renewal pricing                                                       |
| Exclusivity outlasting the usage window               | Reconcile both durations in the contract so old paid content can't silently extend the lockout                          |
| Imposing net-60/90 payment terms                      | Best-sourced failure in this domain - late payment demonstrably burns creator relationships; commit to net-30 or better |
| Different internal teams quoting different numbers    | Set one internal rate authority before outreach; inconsistency destroys negotiating credibility                         |
| Treating disclosure as tradeable                      | It is a gate - a counterpart or colleague proposing to trade it triggers the walk-away script                           |
| One-shot extraction from a repeat-intent relationship | Frame terms as the first move of a repeating deal; the second collaboration usually outperforms the first               |

## Reference

- `mbfinotti/partnerships-skills@influencer-outreach` for the cold pitch upstream - it stops at the positive reply where this skill starts.
- `mbfinotti/partnerships-skills@influencer-discovery-brief` for choosing and vetting the creator - assumed done here.
- `mbfinotti/partnerships-skills@influencer-campaign-brief` for the creative brief after signature - this skill stops at the signed contract.
- `mbfinotti/partnerships-skills@affiliate-disclosure-compliance` for disclosure obligations - the non-negotiable gate.
- `mbfinotti/partnerships-skills@affiliate-commission-structure` when the deal includes a commission component.
