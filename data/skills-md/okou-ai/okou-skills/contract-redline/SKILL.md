---
name: contract-redline
description: Review commercial contracts against a playbook, flag risk, and draft redlines or fallback language.
---

## Pre-Review Setup

### Organizational Playbook

Before any analysis begins, look for a negotiation playbook configured in the user's local settings. A playbook codifies the organization's preferred positions, tolerable bands, and hard limits for every major provision category.

When no playbook exists:
- Propose building one collaboratively with the user
- If the user wants to proceed immediately, anchor the analysis to mainstream commercial norms as your reference point

### Contextual Framing

Every review must start by establishing three things:

1. **Agreement category** -- Determine whether this is a SaaS subscription, professional services engagement, software license, channel partnership, procurement arrangement, or another structure. The category dictates which provisions carry the most weight.
2. **Client posture** -- Establish whether the organization sits on the buying side, selling side, licensing side, or partnership side. Protective language that benefits one party harms the other.
3. **Holistic reading** -- Read the entire document end-to-end before marking up any single provision. Provisions operate as an interconnected system. An aggressive indemnity clause may be counterbalanced by a strong liability cap elsewhere.

## Provision-by-Provision Analysis

### Liability Caps and Damage Exclusions

**What to examine:**
- Total cap structure: fixed dollar figure, fee multiple, or absence of any ceiling
- Symmetry of the cap between the parties
- Exceptions carved out from the cap and which party they favor
- Whether indirect, consequential, special, and punitive damages are waived
- Mutuality of the damages waiver
- Exceptions to the damages waiver
- Cap measurement window: per-incident, annual, or lifetime aggregate

**Typical problems:**
- Cap pegged to a small fraction of fees (for example, three months of spend on a modest-value deal)
- One-sided exceptions that hollow out the cap for the drafter's benefit
- Sweeping exception language like "any breach of this Agreement" that renders the cap meaningless
- Asymmetric damages waiver leaving one party exposed to consequential loss claims

### Indemnification Provisions

**What to examine:**
- Reciprocity: does each side indemnify the other, or is it one-directional
- Triggering events: IP infringement, data incidents, personal injury, warranty breaches
- Relationship to the liability cap: subject to cap, partially capped, or unlimited
- Procedural mechanics: timely notice, who controls the defense, settlement authority
- Duty of the protected party to minimize harm
- Survival period after the agreement ends

**Typical problems:**
- One-directional IP indemnification when both parties contribute intellectual property
- Catch-all "any breach" triggers that effectively eliminate the liability ceiling
- No right for the indemnifying party to direct the legal defense
- Open-ended survival with no time boundary

### Intellectual Property Rights

**What to examine:**
- Background IP ownership: each party must retain what they brought in
- Foreground IP: who owns work product created during the engagement
- Work-for-hire designations and whether their reach is proportionate
- License grants: breadth, exclusivity, geographic scope, sublicense rights
- Open source exposure
- Feedback provisions that grant rights over suggestions or improvements

**Typical problems:**
- Overbroad assignment language that could sweep in the customer's pre-existing assets
- Work-for-hire clauses extending well beyond the specific deliverables
- Perpetual, irrevocable feedback licenses with no practical limit
- License scope that exceeds what the business relationship actually requires

### Data Protection Provisions

**What to examine:**
- Whether a Data Processing Agreement or Addendum is needed and present
- Controller/processor role allocation
- Sub-processor engagement rights and change-notification obligations
- Breach reporting window (must enable the controller to satisfy the 72-hour GDPR deadline)
- International transfer safeguards: Standard Contractual Clauses, adequacy findings, binding corporate rules
- Data return or destruction duties upon contract end
- Security standards and the controller's audit entitlements
- Processing purpose restrictions

**Typical problems:**
- Personal data in scope but no DPA attached
- Unrestricted sub-processor authorization with no advance notice
- Breach notification window that exceeds regulatory deadlines
- No transfer protections for data crossing international borders
- Vague or missing data deletion commitments

### Duration, Renewal, and Exit

**What to examine:**
- Length of the initial commitment and any renewal periods
- Auto-renewal mechanics and the window for opting out
- Convenience termination: availability, required notice, early exit penalties
- Cause-based termination: what qualifies as cause, whether a cure window exists
- Post-termination obligations: data handback, transition support, surviving provisions
- Wind-down logistics and timeline

**Typical problems:**
- Extended initial lock-in with no convenience exit
- Auto-renewal paired with a narrow opt-out window (such as 30 days before an annual renewal)
- Termination for cause with no opportunity to remedy the breach
- Weak or nonexistent transition assistance language
- Survival provisions that effectively perpetuate core obligations

### Dispute Resolution and Governing Law

**What to examine:**
- Applicable law and jurisdiction selection
- Resolution pathway: courts, arbitration, mandatory mediation step
- Litigation venue and personal jurisdiction
- Arbitral institution, procedural rules, and seat (if arbitration applies)
- Jury trial waiver
- Class action waiver
- Fee-shifting for the prevailing party

**Typical problems:**
- Inconvenient or obscure venue selection
- Compulsory arbitration under rules that advantage the drafter
- Jury waiver without compensating procedural safeguards
- No graduated escalation mechanism before formal proceedings

## Deviation Rating System

### GREEN -- Within Bounds

The provision matches or improves upon the organization's baseline position. Any variation is commercially sensible and does not meaningfully shift risk.

**Illustrations:**
- Liability cap set at 18 months of fees when the baseline calls for 12 months (favorable to the buyer)
- Mutual confidentiality term of 2 years against a 3-year baseline (shorter but reasonable)
- Governing law in a reputable commercial jurisdiction near the preferred one

**Response**: Note for transparency. No negotiation warranted.

### YELLOW -- Push Back

The provision sits outside the baseline but within a zone where negotiation is realistic. The position is seen in the market but is not the organization's preference. Warrants attention and discussion, though not immediate escalation.

**Illustrations:**
- Liability cap at 6 months of fees against a 12-month baseline (below standard yet negotiable)
- One-directional IP indemnification when the baseline is mutual (common but not preferred)
- Auto-renewal opt-out of 60 days when the baseline is 90 days
- Acceptable but non-preferred governing law jurisdiction

**Response**: Draft specific replacement language. Supply a fallback if the primary ask is refused. Estimate the business consequence of accepting the term as-is versus negotiating.

### RED -- Escalate Immediately

The provision breaches the acceptable range, trips a defined escalation trigger, or introduces material exposure. Requires review by senior counsel, outside legal advisors, or a business decision-maker with sign-off authority.

**Illustrations:**
- No liability cap at all, or no limitation of liability provision
- Unilateral, uncapped, broadly-scoped indemnification
- Assignment of the organization's background intellectual property
- Personal data processing with no DPA offered
- Unreasonable restrictive covenants or exclusivity demands
- Hostile jurisdiction combined with mandatory arbitration

**Response**: Articulate the precise exposure. Offer market-standard replacement language. Quantify potential downside. Recommend the appropriate escalation path.

## Crafting Effective Redlines

Principles for producing markup that advances the negotiation:

1. **Supply exact text** -- Deliver language that can be inserted verbatim, not abstract guidance.
2. **Stay commercially reasonable** -- Aggressive overreach slows deals. Be firm on critical protections and pragmatic elsewhere.
3. **Include professional rationale** -- Attach a concise justification suitable for sharing with opposing counsel.
4. **Offer a Plan B** -- For every YELLOW item, provide a secondary position in case the first request is declined.
5. **Rank by importance** -- Signal which markups are essential and which are strategic asks.
6. **Match the relationship context** -- Calibrate tone depending on whether the counterparty is a new vendor, a long-standing partner, or a commodity supplier.

### Markup Format

Present each proposed change as follows:

```
**Provision**: [Section number and title]
**Existing text**: "[verbatim excerpt from the agreement]"
**Proposed replacement**: "[specific new language]"
**Justification**: [One to two sentences explaining the rationale, appropriate for external sharing]
**Importance**: [Essential / Strongly Preferred / Optional]
**Fallback**: [Alternative position if the primary request is declined]
```

## Negotiation Prioritization

Organize all proposed markups into three tiers to guide negotiation strategy:

### Tier 1 -- Non-Negotiable (Walk-Away Items)
Provisions where the organization cannot execute the agreement without resolution:
- Absent or grossly inadequate liability protections
- Missing data protection requirements for regulated information
- IP terms that jeopardize core business assets
- Clauses that conflict with the organization's regulatory obligations

### Tier 2 -- High Priority (Strong Preferences)
Provisions that materially affect the risk profile but allow room for negotiation:
- Liability cap adjustments within the acceptable band
- Indemnification scope and reciprocity improvements
- Flexibility around termination and exit rights
- Audit, inspection, and compliance verification rights

### Tier 3 -- Strategic Concessions (Trading Material)
Provisions that strengthen the position but can be yielded to secure more important wins:
- Preferred governing law when the alternative is still acceptable
- Notice period fine-tuning
- Minor definitional refinements
- Insurance documentation requirements

**Negotiation approach**: Open with Tier 1 demands. Offer Tier 3 concessions as currency to lock in Tier 2 outcomes. Never yield on Tier 1 without escalating to authorized decision-makers.
