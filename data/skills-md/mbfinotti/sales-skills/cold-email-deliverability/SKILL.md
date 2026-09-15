---
name: cold-email-deliverability
description: Reviews a cold email draft and its sending setup for deliverability - SPF/DKIM/DMARC alignment, sender reputation and complaint risk, body mechanics (length, links, images, tracking pixels, HTML vs plain text, opt-out), and legal compliance by region. Covers B2B cold outbound and B2C bulk/lifecycle mail. Use whenever the user mentions the spam folder, blacklisting, domain warmup, inbox placement, bounce rates, DMARC, or "why are my emails not landing", even without the word deliverability. Do NOT use for subject lines (mbfinotti/sales-skills@cold-email-subject-line-tester) or cadence (mbfinotti/sales-skills@sales-outbound-sequence). Hygiene and compliance only, never spam-filter evasion.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.2"
---

# Email Deliverability Review

Review a cold email draft and the setup that sends it - authentication, domain architecture, reputation signals, body structure, legal compliance; return a placement-risk report ordered by what actually decides inbox placement.

Label every claim's provenance:

- **provider-verified** - mailbox-provider or standards-body documentation.
- **vendor** - tool-vendor marketing, no independent methodology.
- **contested** - credible sources disagree.
- **practitioner** - expert consensus, uncontrolled.

Never present a vendor number as a law. Where evidence does not exist, say so.

## The placement hierarchy

Encode this order in every review. It is what most advice in this space gets backwards. Effort below is setup and monitoring time and reversibility, never a price.

- value (placement bought): authentication > reputation and complaint control > content structure > word choice
- effort (setup, monitoring, reversibility): reputation and complaint control > authentication == content structure > word choice
- efficiency (do first): authentication > content structure > reputation and complaint control > word choice

Authentication and content structure tie on effort because each is a single one-time hour and each is fully reversible. They differ only in who executes them - DNS access versus the draft's author; this is a re-ranking condition, not an effort difference.

1. **Authentication is a hard gate.** An hour of DNS work, and nothing downstream works without it. SPF/DKIM/DMARC alignment, valid PTR, TLS. Provider-verified: failures now mean rejection (Microsoft `550 5.7.515` since May 5, 2025) or Gmail 4.7.x/5.7.x codes. No copy edit compensates.
2. **Sender reputation and recipient engagement/complaint signals dominate placement.** The largest lever over placement once mail is accepted at all, and the only one of the four that is a standing job rather than a fix. Gmail filters at the mailstream level, not the message level; spam-button complaints are the single largest negative signal (provider-verified mechanics, practitioner-documented).
3. **Content structure is a distant tiebreaker**, cheap enough to stay ahead of reputation work on ratio alone: image-only mail, low text-to-image ratio, HTML with no plain-text part, link-domain reputation - not vocabulary.
4. **"Spam trigger word" lists are largely folklore.** The weakest lever, and last for that reason. No independent controlled study ties word choice, word count, or link count to spam placement (as opposed to reply rate). A clean-reputation domain inboxes "FREE!!! Act now"; a burned domain does not inbox a haiku. Check content anyway - but tell the user plainly, and never hand back a banned-word list as the primary fix.

What this order starves: reputation and complaint control, which ranks second on value yet loses to a cheap tiebreaker on every efficiency round, because it is a standing job with no finish line. Promote it to first whenever the sender intends to keep sending past this campaign, or whenever the Gmail spam rate is already above 0.10% - past that point no authentication or content fix reaches a stream already flagged.

A review that returns a word-list score while the sending domain has no DMARC record is malpractice. The workflow runs preconditions first and content last for this reason - that is the review order, and it differs from the efficiency order on purpose. Reputation is assessed early because a burned stream cancels the copy review entirely; it is repaired late because the repair is a standing job that outlives the campaign.

## Ethics boundary

M3AAWG's November 2025 Position on Cold Email states that "using deceptive and misleading delivery methods to send unsolicited email (including Cold Email) is an abusive practice." It also states that "any attempts to bypass mail volume limits, avoid spam filters, mask sending domains, artificially simulate subscriber engagement, or use other tools or services that exploit loopholes in mailbox providers or cloud platforms are particularly egregious and are not acceptable in any manner."

This skill is deliverability hygiene and compliance - never filter evasion. Refuse, explicitly, to help with:

- Masking or falsifying sender identity.
- Lookalike or deceptive domains.
- Fake `Re:`/`Fwd:` threading.
- Artificial engagement or reply-bot warmup networks.
- Evading provider volume limits.
- Hiding, breaking, or discouraging an opt-out.

Draw the real tension for the user instead of hiding it: practitioners recommend spreading volume across several owned, warmed, honestly-identified sending domains, while M3AAWG condemns "masking sending domains" to evade limits. The line is identity, never count:

- **Hygiene** - transparently owned, correctly authenticated domains that identify the real sender.
- **Abuse** - domains chosen to disguise who is sending, defeat a volume limit, or restart a burned reputation under a new name.

Decline the abusive part of a request and continue with the rest. Abuse is not a low-ranked option on the menu below - it is off the menu, and no volume target, deadline, or effort ceiling ranks it back on.

### Domain architecture - ranking the legitimate options

Legitimacy is the gate; this ranking runs only over what passes it. Effort here is provisioning and warming time, ongoing monitoring, and reversibility - a burned domain is the least reversible outcome in this skill, so reversibility carries most of the weight.

- value (blast radius contained plus placement earned): domain fleet > one dedicated sending domain > corporate subdomain
- effort (provisioning, warming, monitoring, reversibility): domain fleet > corporate subdomain > one dedicated sending domain
- compliance cost (sender identification and suppression surface per region): domain fleet > one dedicated sending domain == corporate subdomain
- efficiency (start here): one dedicated sending domain > corporate subdomain > domain fleet

The dedicated domain and the subdomain tie on compliance cost because both are one sender identity behind one suppression list, and a recipient's region attaches its rules to that identity, not to the DNS label. The subdomain still costs more effort than the dedicated domain despite the cheaper setup; a burn there reaches the organizational domain and cannot be parked.

1. **One dedicated sending domain**, brand-adjacent and honestly identifying the same sender; this is the default rung. An hour to provision, a week or more to warm, and the only architecture whose recovery move (park it, replace it) is near-zero.
2. **A subdomain of the corporate domain** - brand recognition and DNS you already control, but containment is partial; reputation bleeds toward the organizational domain, and Gmail counts bulk volume across the primary domain including subdomains, so it never resets the 5,000/day clock.
3. **A fleet of dedicated domains and mailboxes** - what this order starves - is highest value of the three, and it loses every efficiency round because each domain owes its own authentication, warming, postmaster enrollment, and monitoring, permanently. Promote it when the volume target exceeds what one warmed domain's mailboxes carry against the sender's own postmaster data, or when a genuine second brand exists. Its compliance cost is real: one suppression list must span every domain, since an opt-out binds the sender and not the domain - a fleet suppressing per-domain has a broken opt-out and files a BLOCKER.

Deleted from this menu rather than demoted: cold outbound at volume on the primary corporate domain. It is the one asset that cannot be parked and replaced, and it carries the transactional and corporate mail a single complaint wave would take down with it.

Both rankings on this page are defaults, not laws - they shift with context and with who executes them. Re-rank against what you already know about this sender:

- An established domain with years of real reputation makes the subdomain competitive and makes park-and-replace the wrong recovery.
- A brand-new company has no reputation to protect and no brand to inherit, which flattens the gap between the top two rungs.
- A team whose IT controls DNS and will not delegate a new domain has the subdomain as its only fast option; a team that provisions its own domains reaches the top rung at near-zero friction.

## Interview

- Ask one question per message.
- Offer multiple-choice options.
- Skip anything context already answers.
- If your harness has persistent memory and a prior run stored this sender's setup, confirm it instead of re-asking.

1. Regime: B2B cold outbound (unsolicited) or B2C bulk/lifecycle (opt-in)? Ask first - consent basis, unsubscribe rules, warmup unit, and feedback loops all diverge.
2. Date this has to land by: sending this week, this month, or no fixed date?
3. One-off win or compounding asset: one campaign to one list, or an outbound channel meant to keep running?
4. Effort ceiling: who executes, how many hours do they have, do they control DNS, and how much of this has to stay reversible?
5. Daily volume and volume approaching 5,000/day to any one provider? (Provider-verified bulk-sender threshold at Gmail and Microsoft; permanent once reached at Gmail.)
6. Sending domain: primary corporate domain, dedicated sending domain/subdomain, or several? Does each honestly identify the real sender?
7. Do SPF, DKIM, and DMARC records exist, and is alignment known? "Don't know" is a valid answer - step 3 of the workflow verifies.
8. Recipient provider mix: mostly Gmail, Microsoft, Yahoo, corporate gateways, or mixed?
9. Recipient regions: US, EU (which member states), UK, Canada, Australia, mixed? The legal answer changes completely by region.
10. Postmaster dashboards enrolled - Google Postmaster Tools, Microsoft SNDS/JMRP, Yahoo CFL? Current Gmail spam rate, if known?
11. Is the draft genuine 1:1 mail or templated at volume? Changes bulk-requirement applicability and the opt-out recommendation.
12. Symptoms so far: bounce codes (`550 5.7.515`, 4.7.x/5.7.x, `550 5.4.5`), spam-folder reports, sudden reply drop?

Re-rank both orderings against answers 2-4, and tell the user which answer moved which option:

- A deadline inside a week promotes authentication (an hour, unblocks everything) and demotes every architecture needing a warming period - a domain provisioned today does not carry volume this week. Say that rather than shipping a plan that misses the date.
- A compounding mandate promotes reputation and complaint control from third to first, and promotes the domain fleet once the volume target proves one domain cannot carry it.
- A one-off win keeps the efficiency order as written and rules the fleet out entirely.
- No DNS control caps the sender at a corporate subdomain and puts the authentication fixes in someone else's queue - sequence around that hand-off instead of assuming an hour.
- A low tolerance for irreversible outcomes promotes the dedicated sending domain over the subdomain whatever the other answers say.

## Workflow

1. Run the Interview.
2. Screen the request against the Ethics boundary. Decline evasion asks explicitly before doing anything else.
3. Audit preconditions with [references/authentication-and-setup.md](references/authentication-and-setup.md): SPF/DKIM/DMARC presence and alignment, PTR, TLS, unsubscribe headers where required, and domain architecture against the ranking above. If you can run DNS lookups or browse the web, verify records yourself; otherwise ask the user to paste lookup output. Any failure is a BLOCKER: report it, state that no copy edit compensates, and hold the content review until fixed.
4. Assess reputation and measurement with [references/reputation-and-measurement.md](references/reputation-and-measurement.md): spam rate against thresholds, bounces, blocklists, dashboard enrollment, volume and warmup sanity. A burned domain routes to the remediation path, not a copy review.
5. Review body structure with [references/content-review.md](references/content-review.md) - structure and link-domain quality first, vocabulary last, honestly framed as the weakest lever.
6. Flag the subject line only for deception or placement-damaging structure (fake `Re:`/`Fwd:`, ALL CAPS, excess punctuation). Never score it for open rate or draft variants - route that to `mbfinotti/sales-skills@cold-email-subject-line-tester`.
7. Check legal compliance for every recipient region with [references/compliance-by-region.md](references/compliance-by-region.md).
8. Assemble the report (shape and worked pass/fail examples in [references/review-examples.md](references/review-examples.md)), run the Quality gate, and iterate with the user until it passes.
9. Run any rewritten copy proposed for a flagged section through your preferred humanizer skill before delivering - raw first-draft model output is never shipped.
10. If your harness has persistent memory, store the setup answers (domains, auth status, volume, regions, dashboards) so later reviews skip straight to the draft.

## B2B cold vs B2C bulk

**Identical for both:**

- The authentication stack and alignment rules.
- Reputation mechanics and complaint math.
- The structural content checks.

**Diverges** - split it every time:

- Consent basis: B2C is opt-in by definition; cold B2B is unsolicited and legality varies by region (compliance reference).
- One-click `List-Unsubscribe` (RFC 8058): a bulk/marketing requirement; genuine 1:1 cold mail below bulk thresholds is not covered - the plain-text opt-out line question is contested (content reference).
- Warmup unit: B2C ESP senders warm dedicated IPs on published ramps; cold B2B warms mailboxes and domains (reputation reference).
- Feedback loops: B2C ESPs suppress individual complainers via Yahoo CFL / Microsoft JMRP; Gmail offers no per-message loop to anyone.
- List hygiene: sunset policies, re-engagement, and double opt-in are B2C bulk practice; B2B equivalents are bounce pruning and verification before send.

## Invocation examples and expected output

Typical requests: "why are my cold emails going to spam", "review this cold email for deliverability", "check my email for spam trigger words" (answer honestly - see hierarchy point 4), "am I going to get my domain blacklisted", "we start sending 2,000/day next month - is our setup ready".

Expected output - the review report, in order:

1. Verdict: CLEARED, AT RISK, or BLOCKED.
2. Findings grouped by layer (authentication → reputation → content → compliance), each with severity (BLOCKER / RISK / ADVISORY) and provenance label.
3. Fix list in the efficiency order of the placement hierarchy, not in the finding-group order above - DNS and setup fixes before content edits, always.
4. Measurement plan: which dashboards to enroll, which metrics to watch, thresholds that trigger action.

Full template plus one failing and one passing worked example: [references/review-examples.md](references/review-examples.md).

## Quality gate

Every finding carries a severity. The gate is measurable: count of unresolved BLOCKERs and RISKs.

- Hard gates - any one unresolved keeps the verdict BLOCKED:
  - Authentication present and aligned for the sender's tier: SPF or DKIM minimum for any sender; SPF + DKIM + aligned DMARC for bulk.
  - No deceptive framing anywhere (sender identity, subject, domains).
  - The recipient region's consent/opt-out/disclosure requirement met.
  - Gmail spam rate below 0.30% where known.
- Scored content review: run all ten structural checks in the content reference; each failed check files a RISK or ADVISORY per that file's severity map.
- Pass threshold: zero BLOCKERs and zero unresolved RISKs. ADVISORY findings may ship if the user acknowledges them in the report.
- Iterate: re-run the failed layer after each fix until the gate passes. Never soften a BLOCKER to RISK to get a pass.

## KPIs and measurement

- Gmail spam rate: below 0.10% target, never at or above 0.30% (provider-verified; measured daily in the postmaster dashboard). Approaching 0.10% → audit list and targeting; at 0.30% → stop the stream (mitigation eligibility returns only after 7 consecutive clean days).
- Bounce rate: action thresholds around 2-5% circulate but are vendor conventions; trend and hard-bounce pruning matter more than the exact number.
- Reply rate (B2B) / click and conversion (B2C): the engagement signals worth trusting.
- Discount open rate explicitly: Apple Mail Privacy Protection pre-fetches tracking pixels (~55-60% of opens affected per Litmus 2026 - vendor measurement), and Google states it does not track open rates (provider-verified). Opens are directional at best; never a placement KPI.

## Failure modes

- Editing copy while authentication is broken. Fix: hierarchy order - DNS first, always; hold the content review behind the BLOCKER.
- Treating a seed-list "inbox" result as proof. Seed inboxes have no engagement history and placement is personalized per recipient - directional, not definitive.
- Confusing Google Workspace's 2,000 messages/day account cap (outbound hard limit, rolling 24h) with the 5,000/day Gmail bulk-sender reputation threshold (inbound classification); different mechanisms, different consequences.
- Assuming one universal compliance deadline. Gmail and Yahoo enforced bulk authentication from February 1, 2024; Microsoft's equivalent took effect May 5, 2025 - 15 months later.
- Assuming Gmail lets you suppress individual complainers. It has no per-message feedback loop; prevention is structurally the only option, unlike Yahoo (CFL) and Microsoft (JMRP).
- Relying on automated warmup networks. They manufacture artificial engagement; this is the exact practice M3AAWG names as egregious - and no independent evidence shows they improve real-recipient placement.
- Chasing a burned domain instead of retiring it. Practitioner norm: a domain on a domain-blocklist or with collapsed reputation is often cheaper to park and replace (with an honestly-identified domain) than to rehabilitate; "85% delisting success" figures are vendor and unverified. The exception that flips it is the domain carrying corporate and transactional mail - that one cannot be parked, so it has to be rehabilitated (reputation reference).
- Handing back a word-list score as the primary fix. Folklore - see hierarchy point 4; report content findings last and labeled.
- Applying B2B cold rules to B2C bulk or vice versa. Warmup unit, unsubscribe requirements, and consent basis all differ - see the split above.

## References

- `mbfinotti/sales-skills@sales-outbound-sequence` - touch-by-touch cadence and timing; out of scope here.
- [references/authentication-and-setup.md](references/authentication-and-setup.md) - provider requirements and dates, alignment, error codes, unsubscribe headers, DNS gotchas, domain architecture, hard account caps.
- [references/reputation-and-measurement.md](references/reputation-and-measurement.md) - mailstream filtering, complaint math, thresholds, dashboards, seed-test validity, warmup conventions, remediation and blocklists.
- [references/content-review.md](references/content-review.md) - the ten structural checks with severity map, tracking and link guidance, opt-out debate, folklore explainer.
- [references/compliance-by-region.md](references/compliance-by-region.md) - US, EU and member states, UK, Canada, Australia; B2B vs B2C consent bases and penalties.
- [references/review-examples.md](references/review-examples.md) - report template, one failing worked example, one passing worked example.
