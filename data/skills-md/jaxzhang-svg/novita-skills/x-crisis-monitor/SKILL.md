---
name: x-crisis-monitor
description: Comprehensive X (Twitter) crisis monitoring and management for tech/SaaS brands. Covers full lifecycle from pre-crisis surveillance to post-crisis analysis. Use when monitoring brand sentiment, handling negative publicity, managing PR crises on X, analyzing public opinion trends, or developing social media crisis response strategies. Includes keyword libraries, triage frameworks, response protocols, and post-mortem workflows tailored for tech companies.
---

# X Crisis Monitor

## Overview

Complete lifecycle management for X (Twitter) crisis monitoring and response, specifically designed for tech/SaaS brands. Covers four phases: intelligence gathering, crisis assessment, active response, and post-crisis analysis.

## Crisis Level Decision Tree

```
User Posts Negative Content
         ↓
Check Engagement Metrics
    ├─ Low (<100 likes/RTs) → Level 1: Customer Support
    ├─ Medium (100-1k) + KOL involved → Level 2: Operational Response
    └─ High (>1k) + Trending + Big Media → Level 3: PR Crisis Mode
```

## Phase 1: Intelligence Network (Pre-Crisis Surveillance)

### Keyword Library Construction

**Core Keywords:**
- Brand names (Chinese + English)
- Product names
- Slogan/tagline
- CEO/founders names
- Executive social media accounts

**Negative Sentiment Keywords:**
- "避雷", "垃圾", "维权", "骗子", "倒闭"
- "Diss", "scam", "fail", "broken"
- Tech/SaaS specific: "downtime", "data loss", "security breach"

**Misspellings & Variations:**
- Common typos (e.g., "Telsa" for Tesla)
- Homophones used by netizens
- Abbreviations and slang variations

**Tech/SaaS Industry-Specific:**
- "server down", "API error", "database crash"
- "data leak", "privacy violation", "GDPR"
- "subscription issue", "billing error", "overcharge"
- "feature missing", "bug report", "slow performance"

### Surveillance Tools

**X Pro (formerly TweetDeck):**
- Create keyword monitoring columns
- Set up real-time streams for core keywords
- Monitor mentions of key personnel

**Professional Sentiment Tools:**
- Brandwatch or Meltwater for AI sentiment analysis
- Automated alerts for negative sentiment spikes
- Competitor monitoring

**Supplementary:**
- Google Alerts for long-tail information
- Industry forums and communities (Product Hunt, Hacker News)

### Pre-Crisis Checklist

- [ ] Compile complete brand keyword list (core + variations)
- [ ] Set up X Pro monitoring columns for all keywords
- [ ] Configure automated alerts in sentiment tools
- [ ] Document escalation contacts (PR team, legal, executives)
- [ ] Prepare approved response templates for common scenarios
- [ ] Establish crisis communication channels (internal + external)

## Phase 2: Crisis Assessment & Triage

### Level Classification

**Level 1 (Microwave)**
- **Characteristics:** Individual user complaints, usability issues
- **Engagement:** Extremely low (<100 likes/RTs), no major influencer engagement
- **Strategy:** Customer support intervention
- **Action Items:**
  - Quick response within 1 hour
  - Direct message to understand issue
  - Provide solution or escalation path
  - Monitor for escalation

**Level 2 (Wave)**
- **Characteristics:** Vertical influencer complaints, generating retweets and quote tweets
- **Engagement:** Medium (100-1k), community discussion emerging
- **Strategy:** Operational response
- **Action Items:**
  - Prepare official statement
  - Contact influencer directly for conversation
  - Address concerns transparently
  - Engage community with empathy
  - Prepare for potential escalation to Level 3

**Level 3 (Tsunami)**
- **Characteristics:** Explosive growth, trending on X, major media/influencer amplification
- **Engagement:** High (>1k), cross-platform spread
- **Strategy:** PR crisis mode
- **Action Items:**
  - Alert executive leadership immediately
  - Coordinate PR, legal, and executive teams
  - Issue official statement
  - Activate crisis communication plan
  - Monitor cross-platform spread

### Triage Checklist

- [ ] Assess engagement metrics (likes, RTs, comments, quotes)
- [ ] Identify if key influencers or media accounts involved
- [ ] Check if post is trending or gaining momentum
- [ ] Determine sentiment (complaint vs. malicious attack)
- [ ] Verify factual accuracy of claims
- [ ] Classify crisis level (1/2/3)
- [ ] Notify appropriate stakeholders based on level

## Phase 3: Response & Crisis Management

### Response Framework

**Golden 2-Hour Rule:**
- Acknowledge within 2 hours of detection
- Even without final solution, show brand is responsive
- Prevent information vacuum from being filled with speculation

**Human-to-Human Communication:**
- Avoid robotic language ("We apologize for any inconvenience")
- Use authentic, empathetic tone
- Acknowledge specific concerns raised
- Show genuine commitment to resolution

**Community Notes Strategy:**
- If malicious false information, leverage Community Notes
- Provide evidence and documentation
- Engage platform if necessary
- Encourage community fact-checking

**Don't Delete Posts:**
- Deleting often triggers Streisand Effect (drawing more attention)
- Unless content violates legal terms/platform policies
- **"Guide" always better than "Block"**

### Tech/SaaS Specific Response Templates

**Level 1 - Technical Issue:**
```
Hi @[user], thanks for flagging this. We're looking into [issue] right now. Can you DM us with more details? We'll get this sorted out.
```

**Level 2 - Service Outage:**
```
We're aware of an issue affecting [feature/service]. Our team is investigating and will provide updates here. We apologize for the disruption.
```

**Level 3 - Data Breach/Security:**
```
We are investigating reports of [security issue]. We take this seriously and are working with security experts. More information at [link].
```

### Response Checklist

- [ ] Verify facts and gather accurate information
- [ ] Draft response with appropriate tone for crisis level
- [ ] Get legal review for Level 2-3 crises
- [ ] Obtain executive approval for official statements
- [ ] Publish response within 2 hours (acknowledgment) or 4 hours (full response)
- [ ] Monitor post-response sentiment
- [ ] Prepare follow-up communications
- [ ] Track key metrics (sentiment shift, engagement, reach)

## Phase 4: Post-Crisis Review & Asset Building

### Data Archiving

**Record Essential Information:**
- Crisis origin point and timeline
- Propagation path (who amplified, when)
- Key opinion leaders (KOLs/KOIs) who engaged
- Peak engagement metrics
- Response effectiveness data
- Cross-platform spread tracking

### Product Improvement

**Transform Complaints to Action Items:**
- Compile genuine user grievances into "Product Optimization List"
- Categorize by severity and frequency
- Prioritize based on user impact
- Share with product/engineering teams
- Track implementation status

### Relationship Recovery

**Convert Critics to Advocates:**
- Most vocal critics become most loyal fans when handled well
- Send sincerity gift pack to affected users after resolution
- Follow up personally with key influencers
- Showcase improvements made based on their feedback
- Invite them to beta test future features

### Post-Mortem Documentation

**Create Crisis Report Including:**
- Executive summary
- Timeline and key events
- What worked well in response
- What could be improved
- Lessons learned
- Action items for prevention
- Updated playbooks for similar future scenarios

### Post-Crisis Checklist

- [ ] Complete full timeline documentation
- [ ] Compile all metrics and data
- [ ] Identify key amplifiers and influencers
- [ ] Generate product improvement requests
- [ ] Execute relationship recovery actions
- [ ] Conduct post-mortem meeting
- [ ] Update crisis playbooks based on learnings
- [ ] Archive all materials for future reference
- [ ] Share insights with relevant teams (product, engineering, executive)

## Quick Reference Triage Guide

| Symptom | Metrics | Level | Response |
|---------|---------|-------|----------|
| Individual complaint, low engagement | <100 likes/RTs | 1 | Support response, DM resolution |
| Influencer complaint, community forming | 100-1k, multiple quotes | 2 | Official statement, direct outreach |
| Trending, media coverage | >1k, cross-platform | 3 | Crisis team, official announcement |

## Tech/SaaS Industry Crisis Indicators

**High-Risk Scenarios:**
- Service downtime > 30 minutes
- Data breach or security vulnerability
- Billing/subscription errors affecting multiple users
- Major feature removal or pricing changes
- Third-party integration failures
- Regulatory compliance issues

## Resources

### references/

**keyword-library.md** - Comprehensive keyword lists for tech/SaaS brands including industry-specific terms, misspellings, and sentiment indicators.

**response-templates.md** - Pre-approved response templates for different crisis levels and scenarios specific to tech companies.

**case-studies.md** - Real-world examples of tech/SaaS crisis management with analysis of what worked and what didn't.

### assets/

**checklist.md** - Printable checklists for each phase (pre-crisis, triage, response, post-mortem).

**decision-tree.md** - Visual decision tree for rapid crisis level assessment.

**post-mortem-template.md** - Structured template for documenting crisis response and lessons learned.
