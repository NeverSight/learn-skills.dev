---
name: nurture-sequences
description: "Transformez l'attention en conviction avec des séquences email evergreen qui font progresser les leads de curiosité → confiance → call booké, basé sur la méthodologie A5 du Marketing Swarm de Lasse Flagstad. Use when: **Créer une séquence evergreen** - Emails automatiques qui tournent indéfiniment; **Réactiver une liste froide** - Réveiller des leads dormants sans spam; **Structurer le nurturing post-lead-magnet** - Que se passe-t-il après l'opt-in?; **Définir les segments et triggers** - HOT..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Nurture Sequences

> Transformez l'attention en conviction avec des séquences email evergreen qui font progresser les leads de curiosité → confiance → call booké, basé sur la méthodologie A5 du Marketing Swarm de Lasse Flagstad.

## When to Use This Skill

- **Créer une séquence evergreen** - Emails automatiques qui tournent indéfiniment
- **Réactiver une liste froide** - Réveiller des leads dormants sans spam
- **Structurer le nurturing post-lead-magnet** - Que se passe-t-il après l'opt-in?
- **Définir les segments et triggers** - HOT/WARM/IDLE/COLD et leurs parcours
- **Créer du contenu retargeting** - Snippets pour ads et emails de relance

## Methodology Foundation

**Source**: Lasse Flagstad - A5 Nurture Orchestrator (Marketing Swarm, 2025)

**Core Principle**: "Le nurturing n'est pas du spam programmé. C'est une conversation asynchrone qui construit la confiance pendant que vous dormez. Chaque email doit apporter de la valeur OU faire avancer vers la décision."

**Why This Matters**: La plupart des leads ne sont pas prêts à acheter immédiatement. Sans nurturing, vous perdez 80% de votre pipeline. Avec un bon système, vous restez top-of-mind jusqu'au moment où ils sont prêts.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Structure la séquence 5-email** - Resource → Case → Insight → Invite → Check-in
2. **Définit les segments** - HOT/WARM/IDLE/COLD avec règles d'entrée/sortie
3. **Crée les templates email** - Sujets, preview text, corps, CTA
4. **Produit les snippets retargeting** - 3 one-liners pour ads
5. **Planifie la serialisation de preuves** - Proof → Post schedule

## How to Use

### Créer une séquence evergreen from scratch
```
J'ai des leads qui opt-in mais je ne sais pas quoi leur envoyer après. Crée ma séquence nurture avec le skill nurture-sequences.
```

### Réactiver une liste dormante
```
J'ai 2000 emails qui n'ont pas ouvert depuis 3 mois. Comment les réactiver sans tuer ma délivrabilité?
```

### Optimiser une séquence existante
```
Ma séquence a un taux d'ouverture de 15% et 1% de clics. Audite et propose des améliorations.
```

## Instructions

### Step 1: Audit de l'existant

```
## Nurture Audit

**ESP & Domain:**
- ESP utilisé: _____________
- Domaine d'envoi contrôlé: [ ] Oui [ ] Non
- SPF/DKIM/DMARC configuré: [ ] Oui [ ] Non [ ] Je ne sais pas

**Liste actuelle:**
- Taille: _____ contacts
- Actifs (ouvert/cliqué 30j): _____ (~___%)
- Idle (30-90j sans activité): _____
- Cold (>90j sans activité): _____
- Taux de bounce estimé: ___%

**Séquence actuelle:**
[ ] Aucune séquence automatique
[ ] Welcome email uniquement
[ ] Séquence ___ emails
[ ] Newsletter régulière

**Fréquence confort:**
[ ] 1x/semaine (safe)
[ ] 2x/semaine (standard)
[ ] 3x/semaine (aggressive)

**Tone:**
[ ] Formel (B2B corporate)
[ ] Neutre (professionnel friendly)
[ ] Conversationnel (comme un ami)
[ ] Edgy (polarisant, opinion forte)
```

---

### Step 2: La Séquence 5-Email Evergreen

```
## Email Loop Structure

**Objectif:** Faire progresser de "curieux" à "convaincu" en 5 touches

**Email 1: Resource (Valeur immédiate)**
- Timing: Immédiat après opt-in
- But: Délivrer la promesse + quick win
- Contenu: Lead magnet + 1 insight bonus + question ouverte
- CTA: Soft ("Reply if you want...")

**Email 2: Case (Preuve sociale)**
- Timing: +2-3 jours
- But: Montrer que ça marche pour des gens comme eux
- Contenu: 1 client story avec chiffres + before/after
- CTA: Soft ("Curious if this resonates?")

**Email 3: Insight (POV différenciant)**
- Timing: +2-3 jours
- But: Challenger leur façon de penser
- Contenu: "La plupart pensent X. En réalité Y."
- CTA: Medium ("If this clicked, here's the next step...")

**Email 4: Invite (Proposition claire)**
- Timing: +3-4 jours
- But: Présenter l'offre sans friction
- Contenu: Ce qu'on fait, pour qui, comment ça marche, next step
- CTA: Direct (booking link)

**Email 5: Check-in (Relance légère)**
- Timing: +4-5 jours
- But: Dernière chance sans pression
- Contenu: "Still interested?" + question binaire
- CTA: Reply-based ("Reply YES if you want the details")
```

---

### Step 3: Templates Email (Copy-Paste Ready)

```
## Email 1: Resource

**Subject lines (test 2-3):**
- "Here's [asset] as promised"
- "[Asset] + something extra"
- "Your [topic] shortcut"

**Preview:** The thing you asked for + a bonus question

**Body:**
---
Hey [first_name],

Here's [asset/lead magnet]: [LINK]

Most people who grab this are trying to [outcome].

Quick tip that's not in the guide: [1 bonus insight in 2 sentences].

Curious — what's your biggest challenge with [topic] right now?

[Signature]
---

**CTA:** Reply-based (no link)
**Length:** ~80 words
```

```
## Email 2: Case

**Subject lines:**
- "How [client type] went from [before] to [after]"
- "[Result] in [timeframe] — here's how"
- "This might be you"

**Preview:** A quick story that might sound familiar

**Body:**
---
[First_name],

Quick story:

[Client name/type] came to us [situation — 1 sentence].

Their biggest problem? [Pain point in their words].

[2-3 sentences on what changed and the result with numbers]

What made the difference: [1 key insight/mechanism].

Does this sound like your situation?

[Signature]
---

**CTA:** Question (reply-based)
**Length:** ~100 words
```

```
## Email 3: Insight

**Subject lines:**
- "The [topic] mistake everyone makes"
- "Why [common approach] doesn't work anymore"
- "Unpopular opinion about [topic]"

**Preview:** Something most people get wrong

**Body:**
---
[First_name],

Most [ICP type] think [common belief].

I used to think the same thing.

But here's what I've seen after [experience/data]:

[Contrarian insight in 2-3 sentences]

The fix isn't [obvious solution].
It's [your mechanism/approach in 1 sentence].

If this clicked for you, [soft CTA — usually a link or reply].

[Signature]
---

**CTA:** Medium (link to content or reply)
**Length:** ~90 words
```

```
## Email 4: Invite

**Subject lines:**
- "Is this a fit?"
- "Here's exactly what we do"
- "Quick overview of [offer name]"

**Preview:** A clear look at how this works

**Body:**
---
[First_name],

You've seen [what they've consumed so far].

Here's what working together actually looks like:

**Who it's for:**
- [Criteria 1]
- [Criteria 2]
- [Criteria 3]

**What happens:**
[2-3 sentences on mechanism/process]

**What you get:**
[Key deliverables/outcomes — bullet points]

**Next step:**
[Clear CTA — usually booking link]

If now's not the right time, no pressure.
But if you're ready — [link].

[Signature]
---

**CTA:** Direct (booking link)
**Length:** ~120 words
```

```
## Email 5: Check-in

**Subject lines:**
- "Still thinking about it?"
- "Quick check-in"
- "Yes or no?"

**Preview:** No pressure, just checking

**Body:**
---
[First_name],

Just checking in — are you still interested in [outcome]?

If yes, reply "YES" and I'll send over [next step / more details].

If the timing isn't right, totally get it. Just reply "LATER" and I'll follow up in a few months.

Either way, appreciate you.

[Signature]
---

**CTA:** Reply-based (binary choice)
**Length:** ~50 words
```

---

### Step 4: Segmentation Rules

```
## Segment Definitions

**HOT (High Intent)**
- Definition: Clicked/visited VSL or booking page in last 7 days
- Behavior: Actively evaluating
- Treatment: Invite + reminder email, skip to Email 4-5
- Exit: Books call or goes cold

**WARM (Engaged)**
- Definition: Opened or clicked in last 30 days
- Behavior: Interested but not ready
- Treatment: Full 5-email loop + weekly value
- Exit: Becomes HOT (visits VSL) or IDLE (no activity 30 days)

**IDLE (Cooling)**
- Definition: No open/click for 30-90 days
- Behavior: Lost interest or inbox issues
- Treatment: Reactivation micro-asset (1 high-value email)
- Exit: Re-engages → WARM, or stays idle → COLD

**COLD (Dormant)**
- Definition: >90 days no activity
- Behavior: Probably forgot you exist
- Treatment: Rescue sequence (3 emails) or sunset
- Exit: Re-engages → WARM, or unsubscribe/remove

**Trigger Map:**
- New subscriber → WARM → Start Email 1
- Clicks VSL link → HOT → Jump to Email 4
- No activity 30 days → IDLE → Reactivation email
- No activity 90 days → COLD → Rescue or sunset
```

---

### Step 5: Retargeting Snippets

```
## 3 Retargeting Snippets (for A4/Ads)

**Snippet 1: Proof-led**
"[Client type] went from [before] to [after] in [timeframe].
Here's the system → [CTA]"

**Snippet 2: POV-led**
"Still doing [old way]?
There's a faster path → [CTA]"

**Snippet 3: Invite-led**
"Ready to [outcome]?
Book a quick call → [CTA]"

**Usage:**
- Meta/IG: Image + snippet as primary text
- Email subject: Use as inspiration
- LinkedIn: Adapt for carousel hooks
```

---

### Step 6: Proof Serialization Plan

```
## 2-Week Proof → Post Schedule

**Week 1:**
- Mon: Case study email (Email 2 variant)
- Wed: LinkedIn post (same case, hook format)
- Fri: Retargeting ad (Snippet 1)

**Week 2:**
- Mon: New proof email (different client)
- Wed: LinkedIn post (contrarian insight from case)
- Fri: Email 3 (Insight) referencing both proofs

**Rotation:**
- Swap in new proof every 2-4 weeks
- Archive top performers for retargeting
- Feed best-performing angles to A3/Hooksmith
```

## Benchmarks

```
## Target Metrics (Adjust by Industry)

| Metric | Floor | Target | Great |
|--------|-------|--------|-------|
| Open/Reach Rate | 20% | 30-40% | 50%+ |
| Click-through Rate | 2% | 4-6% | 8%+ |
| Reply Rate | 0.5% | 1-2% | 3%+ |
| Unsubscribe/send | <0.5% | <0.3% | <0.1% |
| Booking from loop | 0.5% | 1-2% | 3%+ |

**Red Flags:**
- Open rate <15% → Deliverability issue or bad subject lines
- CTR <1% → Content not resonating or CTA unclear
- Unsub >1% per send → Too aggressive or wrong audience
- Spam complaints >0.1% → Stop sending, clean list
```

## Examples

### Example 1: B2B SaaS Lead Magnet → Demo

**Sequence:**
1. Lead magnet delivery + "What's your biggest challenge?"
2. Customer story: "How [company] cut churn 40%"
3. Insight: "Why most retention strategies fail"
4. Demo invite with clear criteria
5. Check-in: "Still thinking about it?"

**Timing:** 0, +3, +6, +10, +14 days
**Result:** 2.5% lead → demo booking rate

---

### Example 2: Coach/Consultant Evergreen

**Sequence:**
1. Free guide + bonus tip + question
2. Client transformation story
3. "The myth of [common belief]"
4. "Here's exactly how I work with clients"
5. "Yes or no?"

**Timing:** 0, +2, +4, +7, +10 days
**Result:** 3% lead → discovery call rate

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Low open rates | Subject lines or deliverability | A/B test subjects, check spam score |
| Opens but no clicks | Content doesn't match expectation | Align preview text with body |
| Clicks but no bookings | Friction in booking flow | Simplify, add calendar in email |
| High unsubscribes | Wrong audience or too frequent | Segment tighter, reduce frequency |
| Replies but no conversions | Qualification issue | Add pre-qualification in sequence |
| Deliverability dropping | Domain/IP reputation | Warm up, clean list, reduce volume |

## Compliance & Deliverability

```
## Checklist Before Sending

**Technical:**
[ ] SPF record configured
[ ] DKIM signing enabled
[ ] DMARC policy set
[ ] Sending domain warmed (if new)

**List Hygiene:**
[ ] Double opt-in (or clear consent)
[ ] Bounces removed automatically
[ ] Unsubscribe link in every email
[ ] Complaints monitored

**Content:**
[ ] No spam trigger words
[ ] Text-to-image ratio reasonable
[ ] Links not flagged
[ ] Mobile preview checked
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

### Source
- Lasse Flagstad - A5 Nurture Orchestrator (Marketing Swarm)

### Related Reading
- `email-writing/` - Craft individual emails
- `distribution-engine/` - How leads enter the sequence
- `launch-formula/` - Jeff Walker's launch sequences

### Tools
- [ConvertKit](https://convertkit.com) - Creator-friendly ESP
- [Brevo](https://brevo.com) - Good free tier
- [Mailmeteor](https://mailmeteor.com) - Gmail sequences
- [Hunter.io Signals](https://hunter.io) - Email verification

## Related Skills

- `distribution-engine/` - Feed leads into this sequence
- `email-writing/` - Individual email craft
- `landing-page-copy/` - Optimize opt-in pages
- `dotcom-secrets/` - Advanced funnel sequences

---

*Skill version: 1.0*
*Last updated: 2026-01-28*
*Source: Lasse Flagstad Marketing Swarm*
