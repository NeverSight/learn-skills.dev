---
name: affiliate-disclosure-compliance
description: Check a specific piece of affiliate or influencer content (caption, video script, transcript, screenshot, or live URL) against disclosure regulations and return a pass/fail compliance review with placement, wording, and per-format fixes. Covers FTC affiliate disclosure (16 CFR 255 and 465), UK CAP/CMA rules, EU UCPD and DSA, and German, French and Italian overlays, pre-publication or already live. Use whenever the user mentions affiliate disclosure, FTC disclosure, paid partnership labeling, sponsored content, ad tags, or a partner post that may be missing or burying its disclosure, even if they never say compliance. Reviews content only - for disclosure clauses inside program terms use mbfinotti/partnerships-skills@affiliate-program-terms.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.8"
---

# Affiliate Disclosure Compliance

Check one piece of affiliate or influencer content against disclosure regulations and return a compliance review: pass/fail per requirement, with placement, wording, and per-format fixes. Built for program managers reviewing partner and creator content before publication, and remediating what is already live. The legal basis is the FTC's clear-and-conspicuous standard (16 CFR 255.0(f)), CAP Code rule 2.1, the UCPD, and national overlays; the checklist itself is this skill's own working tool, not an official named framework.

## A Compliance Review, Not Legal Advice

1. State before reviewing anything: "This is a compliance review against published regulator rules, not legal advice. Counsel owns the legal call; this review finds what counsel and regulators would find."
2. Mark every counsel-grade ambiguity inline with `[COUNSEL: <question>]`, attached to the affected finding, never pooled at the end of the report.
3. Always escalate: whether the poster is a "trader" under EU law, regulated verticals (health, finance, alcohol, gambling), children's audiences, active regulator contact, and any market not covered by the references.
4. Repeat the disclaimer with the delivered report; instruct the user to keep every marker until counsel resolves it.

Ambiguity flagged inline stays attached to the evidence that raised it; a footer disclaimer gets skimmed past and the nuance is lost.

## Interview

Ask one question per message; offer multiple-choice answers; skip anything already answered or evident from the artefact.

- Which jurisdictions is the audience in? US / UK / EU, and which member states (Germany, France, Italy, other)?
- Content format? Short-form video / livestream / story or ephemeral / static image post / long-form video / podcast or audio / blog or review article / newsletter or email / affiliate roundup or comparison page.
- Which platform(s) will it run on?
- Relationship type? Paid post / affiliate-commission-only / gifted product / unpaid ambassador / employee or insider / agency-intermediated.
- B2B or B2C audience, or both?
- Pre-publication, or already live? Live shifts the output toward remediation.
- What artefact do you actually have? Caption text / script / transcript / URL / screenshot / the rendered post.
- By when must the result land? A scheduled publish date / a live violation already earning impressions / no fixed date.
- One-off or compounding? Clear this asset only, or also stand up monitoring and a wording bank that keep clearing assets.
- Effort ceiling? Hours available per review cycle, whether anyone can gate publication, and whether the program terms already back withholding commission or terminating a partner.

Re-rank the menus in Ranked Choices against the last three answers, and name the move out loud:

- A live violation still earning impressions promotes the fastest remediation rung.
- A compounding mandate promotes the wording bank and the pre-publication gate.
- A ceiling of a few hours per cycle deletes the full-roster review and every rung the program terms do not already back.

## Review Workflow

1. Deliver the not-legal-advice statement, then run the Interview.
2. Confirm scope: this skill reviews content. Drafting program terms, briefs, or contract clauses belongs to sibling skills (see Reference).
3. Inspect the artefact. If you can view images or fetch the URL, review the rendered asset exactly as a viewer meets it. Otherwise review the provided text and mark visual/audio checks "not assessable from the artefact provided": never guess what the frame shows.
4. Load the jurisdiction references for every market the interview surfaced: [references/us-ftc-standard.md](references/us-ftc-standard.md), [references/uk-and-eu-rules.md](references/uk-and-eu-rules.md).
5. If you can browse the web, re-verify penalty figures and regulator guidance before citing them: caps are inflation-adjusted and guidance gets revised. Otherwise label each figure "as of drafting, re-verify".
6. Run the six-layer check below for every applicable jurisdiction.
7. Write the per-asset report: verdict, findings with cited rules, one concrete rewritten fix per failure. Shape below; worked examples in [references/review-report-example.md](references/review-report-example.md).
8. For already-live content, add a remediation plan built from the Remediation Ladder below: the rung chosen per asset, the order across assets, and a note that 16 CFR 255.1(d) states advertisers _should_ remediate non-compliance they know of. Write it as the FTC's stated expectation, never as a standalone statutory duty, since Part 255 is interpretive guidance and not a safe harbour: the enforceable exposure runs through FTC Act Section 5. Attach `[COUNSEL]` if the user intends to assert the obligation to a partner.
9. Flag genuinely unsettled points with `[COUNSEL]` instead of asserting an answer.
10. Recommend one monitoring approach and one guidance route from Ranked Choices when the interview shows the program has neither: name the rung above the recommendation and the condition that promotes it.
11. Iterate until the completeness threshold in Measurement passes.
12. If your harness has persistent memory, memorize the program's jurisdiction set, approved wording bank, and each partner's recurring failures: later reviews start faster and repeat offenders surface. Otherwise ask the user to keep the report for the next review.

## The Six-Layer Check

Judge each layer per jurisdiction; a single fail on any layer fails the asset.

These six layers are gates, not a menu: they carry no efficiency ranking and never will. A legal disclosure obligation is not a trade-off; never run the two highest-ratio layers, skip the rest, and call the asset reviewed.

No layer has a discounted version that partially passes, and no cheaper check anywhere in this skill substitutes for one. Rank the delivery choices around the review (see Ranked Choices); never the obligations themselves.

1. **Presence**: does any disclosure exist? Any material connection triggers the duty: payment, commission, free product, free trial, employment, family relationship. A gift is not an exemption.
2. **Wording**: is the label unambiguous? Check against [references/disclosure-wording.md](references/disclosure-wording.md). "#ad", "advertising", "paid partnership with [brand]" pass; "#sp", "#collab", "ambassador", "thanks to [brand]" fail.
3. **Placement and prominence**: apply the 16 CFR 255.0(f) factors, judged separately for visual, audible, and interactive media, and always uncontradicted by anything else in the content. See [references/us-ftc-standard.md](references/us-ftc-standard.md) for the factor breakdown per media type.
4. **Per-format requirements**: check the format's row in [references/format-placement-rules.md](references/format-placement-rules.md): in-video and spoken for video, periodic repeats for livestreams, overlays for stories, link-adjacent disclosure for roundups.
5. **Truncation and portability**: does the disclosure survive the caption "more" cut, embeds, screenshots, and cross-posts? A platform-native paid-partnership label alone is never sufficient: FTC and CMA both say so, and the label itself may not travel off-platform.
6. **Jurisdiction overlays**: Germany's rebuttable payment presumption, France's mandatory "publicité"/"collaboration commerciale" mention, Italy's Digital Chart format rules, the CMA's accepted-label list. See [references/uk-and-eu-rules.md](references/uk-and-eu-rules.md).

## Ranked Choices: Monitoring, Guidance, Remediation

Three genuine menus sit around the obligations above:

- How assets reach this review.
- How the rules reach partners.
- How a live violation gets cured.

Each is ranked by value per unit of effort: effort meaning monitoring hours, tooling setup, coordination, relationship capital, and reversibility. Read every axis line as descending on that axis: highest value, highest effort, highest compliance cost first. The efficiency line is the recommended order of attack.

Every ranking below is a default, not a law. It shifts with context and with who executes it, so re-rank before recommending a rung:

- Re-rank when the affiliate network enforces disclosure centrally: its own scan and terms already cover rungs the program would otherwise build.
- Re-rank when the roster is too large to monitor asset-by-asset: sampling and automation move up, per-asset review moves down.
- Re-rank when the vertical is regulated (health, finance, alcohol, gambling) or a regulator has made contact: the highest-value rung wins regardless of effort.
- Re-rank against the Interview's timing, compounding, and effort-ceiling answers, and say which answer moved which rung.

### Monitoring coverage: which assets reach this review

Monitoring is not optional; which approach delivers it is. 16 CFR 255.1(d) and the CMA's brand-side duty both require it, and no rung below discharges that duty on its own.

- efficiency: risk-weighted spot-check > pre-publication gate on ephemeral and video > automated label scan > partner self-attestation > full-roster review
- value (violations caught before an audience or a regulator sees them): pre-publication gate > full-roster review > risk-weighted spot-check == automated label scan > partner self-attestation
- effort: full-roster review > pre-publication gate > automated label scan > risk-weighted spot-check > partner self-attestation
- compliance cost: automated label scan > pre-publication gate > partner self-attestation > risk-weighted spot-check == full-roster review

Effort in magnitudes:

- Self-attestation and spot-checks: near-zero per asset once running.
- Automated label scan: about a week to set up and tune.
- Pre-publication gate and full-roster review: standing jobs.

- Default to the risk-weighted spot-check: newest partners, highest earners, regulated claims, formats that failed before, with self-attestation underneath it as the paper trail.
- Promote the pre-publication gate for ephemeral and video content: the FTC's own fallback, because a story vanishes before any after-the-fact review reaches it.
- Justify the value tie: a scan reads many assets shallowly (label text only), a spot-check reads few assets fully (placement, prominence, truncation), different routes to a comparable share of real violations.
- Read the compliance-cost line as the review triggered and the reversibility spent: a scan needs a platform-terms review before it crawls, and a gate or attestation clause needs a program-terms amendment and partner notice. Reading published content, whether spot-check or full roster, needs neither - which is what ties those two.
- Never let self-attestation stand as the monitoring itself. A partner who misunderstood the rule attests in good faith and still fails; the FTC asks for a search of what partners are saying, not a collection of their promises.
- What this order starves: the full-roster review, high on value and high on effort, loses every round. Promote it when a regulator has made contact, when the vertical is regulated, or when the same partner fails twice.
- Delete the automated label scan when the campaign's disclosures are spoken or on-screen: a text scan cannot see them, rather than leaving it ranked at the bottom.

### Getting the rules to partners

- efficiency: approved wording bank > corrected line in the review reply > per-format one-pager in the partner portal > live training or office hours
- value (share of the roster that discloses correctly without being told): approved wording bank > per-format one-pager > live training > corrected line in the review reply
- effort: live training > per-format one-pager > approved wording bank > corrected line in the review reply

Effort in magnitudes:

- Corrected line in the review reply: near-zero.
- Approved wording bank: about an hour to adapt.
- Per-format one-pager: about a week of writing and portal work.
- Live training: a standing job.

- Default to the wording bank: adapt [references/disclosure-wording.md](references/disclosure-wording.md) into the program's own approved lines, one per format the campaign runs.
- Ship the corrected line with every failing finding regardless: the report shape already requires it, and it feeds the bank.
- What this order starves: live training, the only rung that catches a partner's misunderstanding before it reaches an asset. Promote it when the roster is small and concentrated, or when the same failure recurs across partners after the bank shipped.
- Delete the live-training rung for a self-serve roster that never meets the program team: a session nobody attends is not distribution.
- Hand the drafting of terms clauses and brief language to the sibling skills in Reference; this skill only picks the delivery route for rules it already checked.

### Remediation ladder for a live violation

Curing the violation is mandatory; which rung cures it is the choice. Ranked for one non-compliant live asset.

- efficiency: edit the disclosure into the live asset > re-publish a corrected version and remove the original > take the asset down > pause commission on that asset's links until fixed > terminate the partner
- value (undisclosed exposure removed, recurrence prevented): re-publish corrected == take down > edit in place > pause commission > terminate
- effort: terminate > pause commission > take down > re-publish corrected > edit in place
- compliance cost: terminate > pause commission > take down > re-publish corrected > edit in place

Effort in magnitudes:

- Edit in place: a message and a minute.
- Re-publish a corrected version: about an hour, plus the asset's earned reach.
- Takedown or payment hold: spends relationship capital and is hard to walk back.
- Terminate and replace the partner: about a quarter.

- Default to editing in place, and escalate one rung whenever the format's own rule puts the disclosure inside the content.
- Justify the value tie: both fully remove the non-compliant version from the audience; re-publishing also keeps the campaign's reach, which is why it wins on efficiency at equal value.
- Read the compliance-cost line as the review triggered and the reversibility spent: withholding commission or terminating needs a program-terms clause behind it and counsel's read, a takedown needs the partner's cooperation, and an edit reverses freely.
- Never offer a lower rung as a cure the format does not allow: a caption edit cannot fix a video whose spoken and on-screen disclosure is missing; only a re-publish reaches it.
- Never let termination stand in for remediation. Removing the partner leaves the undisclosed asset live; pair it with a takedown or the exposure outlives the relationship.
- What this order starves: re-recording long-form video, high on value and high on effort, always loses to a caption edit. Promote it whenever the failing layer is per-format placement rather than wording.
- Delete the payment-hold rung when the program terms carry no withholding clause: withholding without one is a contract dispute, not a remediation. Attach `[COUNSEL]` before recommending it.
- Order a multi-asset plan by exposure: assets still earning impressions first, then the highest-reach asset, then the rest.

## Output Shape

Per asset: a header (asset, format, platform, relationship, jurisdictions, B2B/B2C, pre-publication or live), a check table (requirement | pass/fail | evidence | rule | fix), and an overall verdict: PASS, FAIL, or PASS WITH `[COUNSEL]` ITEMS. Every failing row carries a rewritten, ready-to-paste fix, not just a critique.

Live content adds a prioritized remediation section. Full positive and negative examples: [references/review-report-example.md](references/review-report-example.md).

## Common Failure Modes

| Failure                                                                                | Why it fails                                                                                                                  | Fix                                                                   |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Disclosure below the fold or behind the "more" cut                                     | FTC: disclosures needing a click on MORE are likely missed; CMA: no scrolling required                                        | Move the label into the first visible line                            |
| Ambiguous tags: #sp, #spon, #collab, #ambassador, vague "partner", "thanks to [brand]" | Viewers can't decode the commercial relationship; regulators reject them                                                      | Replace with "#ad" or "paid partnership with [brand]"                 |
| Disclosure in bio or profile only                                                      | Viewers of one post never open the profile; FTC calls these likely missed                                                     | Disclose inside every commercial post itself                          |
| Gifted product treated as a loophole                                                   | Free product is a material connection, same as payment                                                                        | Disclose the gift: "[brand] sent me this for free"                    |
| Platform's native label relied on alone                                                | FTC: platform tools are "no guarantee"; CMA accepts them only if clearly visible; labels can vanish in embeds and screenshots | Keep the label and add the partner's own written or spoken disclosure |
| Video disclosure only in the description                                               | FTC: the disclosure belongs in the video, not just the description                                                            | On-screen overlay plus a spoken line at the start                     |
| Livestream disclosed once at the start                                                 | Mid-stream joiners never hear it; FTC requires periodic repetition                                                            | Repeat verbally at regular intervals and at segment changes           |
| Roundup disclosure separated from the links                                            | FTC: readers must see the disclosure and the link at the same time                                                            | Put "paid link" or a commission line adjacent to each link block      |

Every row is the mandatory correction of one specific failure, not a rung in a ladder: no cheaper variant of any fix passes, and the rows are never traded off against each other. The choices this skill does rank live in Ranked Choices.

## Measurement

Program KPIs:

- First-pass rate: share of assets passing on first review. Sustained below 80% signals an upstream defect: fix the brief and the onboarding, not just the assets.
- Time-to-remediation: for live violations, request the fix within 24 hours of the finding; track days until resolved.
- Roster coverage: share of active partners with at least one asset reviewed per period, measured against the monitoring approach chosen in Ranked Choices. An unreviewed partner is unmonitored risk under 16 CFR 255.1(d).

Review completeness threshold: iterate on the review until all four hold:

- Every applicable check carries an explicit pass or fail; unverifiable checks say "not assessable", never silence.
- Every fail cites a specific rule and carries a concrete rewritten fix.
- Every unsettled point carries a `[COUNSEL]` marker.
- Every jurisdiction the interview surfaced was checked, not just the home market.

## Invocation Examples

- "Check this caption for our affiliate's photo post: US and UK audience, commission-only relationship, goes live tomorrow."
- "Review this video script for FTC disclosure compliance: paid sponsorship, B2B SaaS audience."
- "This post is already live: <URL>. Gifted product, French audience: is the disclosure compliant, and what do we fix first?"

## Reference

- See [references/us-ftc-standard.md](references/us-ftc-standard.md) for the US layer: 255.0(f) factors, advertiser duties, incentivized and insider reviews, penalty mechanics.
- See [references/uk-and-eu-rules.md](references/uk-and-eu-rules.md) for UK, EU, German, French, and Italian rules.
- See [references/format-placement-rules.md](references/format-placement-rules.md) for the per-format placement table with the regulator behind each rule.
- See [references/disclosure-wording.md](references/disclosure-wording.md) for accepted vs rejected labels and ready-to-use compliant lines, including B2B variants.
- See [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md) for what is identical across B2B and B2C and what differs.
- See [references/review-report-example.md](references/review-report-example.md) for one full worked review and one review done badly.
- See `mbfinotti/partnerships-skills@affiliate-program-terms` to write the disclosure obligation into the program terms: this skill only checks content against the rules.
- See `mbfinotti/partnerships-skills@influencer-campaign-brief` to put disclosure requirements into the campaign brief: this skill checks the content that brief produced.
- See `mbfinotti/partnerships-skills@affiliate-onboarding-sequence` for where partners first learn the disclosure rules this skill later enforces.
- See `mbfinotti/partnerships-skills@affiliate-fraud-detection` for traffic and commission fraud: a different problem entirely; a perfectly disclosed post can still carry fraudulent traffic.
