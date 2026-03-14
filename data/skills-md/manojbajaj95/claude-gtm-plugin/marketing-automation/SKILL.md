---
name: marketing-automation
description: Use this skill when setting up marketing automation in HubSpot, Marketo, email sequences, lead scoring, and workflows.
---

# Marketing Automation Expert

Marketing automation strategy and implementation across HubSpot, Marketo, ActiveCampaign, and similar platforms.

---

## Platform Selection

| Platform | Best For | Complexity | Cost |
|----------|----------|------------|------|
| HubSpot | SMB to Enterprise, all-in-one | Medium | $$$–$$$$ |
| Marketo | Enterprise B2B | High | $$$$ |
| ActiveCampaign | SMB, strong automation | Low–Medium | $–$$ |
| Pardot | Salesforce-native B2B | Medium–High | $$$$ |
| Mailchimp | Small business, email-first | Low | $–$$ |

**Selection criteria**: CRM integration, email volume, workflow complexity, reporting depth, budget, team technical skill.

---

## Lead Scoring Model

**MQL threshold**: 100 points. Decay: −10 points after 30 days of inactivity.

### Behavioral Scoring

| Action | Points |
|--------|--------|
| Request demo | +50 |
| Pricing page visit | +30 |
| Case study download | +25 |
| Webinar attendance | +25 |
| Webinar registration | +15 |
| Content download | +10 |
| Email click | +3 (max 5/day) |
| Email open | +1 (max 3/day) |
| Blog visit | +1 (max 5/day) |
| Unsubscribe | −30 |
| Email bounce | −20 |
| Spam complaint | −100 |

### Demographic Scoring

| Attribute | Points |
|-----------|--------|
| C-Level title | +25 |
| VP title | +20 |
| Director | +15 |
| Manager | +10 |
| Target company size (200–1000) | +20 |
| Target industry | +20 |
| Primary market geography | +15 |

### Lead Grading (A–D)

- **A**: Decision maker + target size + target industry + target geo → immediate sales follow-up
- **B**: 3 of 4 criteria met → sales within 24 hours
- **C**: 2 of 4 criteria met → nurture then handoff
- **D**: 1 or fewer criteria → nurture only, no sales routing

---

## Email Sequences

### Welcome Series (6 emails over 14 days)

| Email | Timing | Purpose | CTA |
|-------|--------|---------|-----|
| 1 | Immediately | Welcome + quick win resource | Download resource |
| 2 | Day 2 | Pain point + case study | Read case study |
| 3 | Day 4 | Product overview + benefits | See how it works |
| 4 | Day 7 | Exclusive gated content | Download now |
| 5 | Day 10 | Offer personalized help | Schedule a call |
| 6 | Day 14 | Preference center | Update preferences |

Exit conditions: demo requested, sales conversation started, unsubscribed.

### Lead Nurture (score-triggered tracks)

| Track | Score Range | Cadence | Focus |
|-------|-------------|---------|-------|
| Awareness | 50–69 | 2/week | Educational, industry trends |
| Consideration | 70–89 | 2–3/week | Use cases, ROI calculator, case studies |
| Decision | 90–99 | 3/week | Free trial, demo, competitive comparison |

### Re-engagement (90-day lapse trigger)

4-email sequence over 15 days: "We miss you" → "Is this goodbye?" → "Last chance offer" → "Goodbye for now" with easy re-subscribe. Outcomes: engaged → return to nurture | no action → sunset list.

---

## Automation Workflows

### Lead Routing Workflow

1. Data enrichment (Clearbit/ZoomInfo) — wait 30 seconds
2. Lead scoring + grading
3. Check for existing account → route to account owner if yes
4. Territory assignment (geography → company size → industry)
5. Create follow-up task with SLA: A=15 min | B=2 hrs | C=24 hrs
6. Notify rep via email + Slack
7. Add to appropriate nurture track

### Lifecycle Stage Automation

| Stage | Entry Trigger | Key Automations |
|-------|--------------|-----------------|
| Subscriber | Email opt-in | Welcome series + newsletter |
| Lead | Form submit OR score >20 | Enrich → nurture → sync CRM |
| MQL | Score ≥100 OR demo request | Sales alert + task + pause marketing |
| SQL | Sales qualified in CRM | Update nurture + notify CS |
| Opportunity | Deal created | Pause outbound + enable deal-stage emails |
| Customer | Deal won | Onboarding sequence + remove from prospects |
| Churned | Cancellation | Win-back sequence |

---

## Key Workflows to Build

**1. Demo Request → Sales Handoff**: Form submit → enrich → score/grade → create HubSpot deal → assign to rep → send confirmation email → start sales sequence.

**2. Trial Signup → Activation**: Signup → welcome email → onboarding checklist → day 3/7/14 milestone emails → conversion offer at day 14.

**3. Event/Webinar**: Registration → confirmation email → 3 reminders → post-webinar follow-up (attended) or recording offer (no-show) → add to nurture based on engagement.

**4. Customer Onboarding**: Won deal → CSM assignment notification → welcome email → onboarding checklist → check-in at 30/60/90 days → NPS survey at 90 days.

---

## HubSpot Implementation

**Campaign setup**: Marketing → Campaigns → tag all assets (emails, landing pages, ads) with campaign ID.

**UTM convention**: `utm_source={channel}&utm_medium={cpc|email|organic}&utm_campaign={id}&utm_content={variant}`

**Attribution model**: W-shaped for hybrid PLG/sales-led (first touch + lead creation + close).

**Lead scoring setup**: Settings → Marketing → Lead Scoring. Set behavioral weights, demographic weights, and decay rules. Create MQL automation when score ≥100.

**Reporting cadence**: Daily review of MQLs/SQLs. Weekly channel ROI. Monthly win/loss trends.
