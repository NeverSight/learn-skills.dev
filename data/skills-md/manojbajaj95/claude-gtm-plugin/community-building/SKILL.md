---
name: community-building
description: |
  Build and grow online communities across all platforms and contexts — from developer/B2B communities (Discord, Slack, Circle, Discourse) to social communities (Twitter/X, Reddit, Farcaster) to crypto/holder communities (Telegram). Covers strategy, platform selection, channel architecture, member journey mapping, onboarding, engagement rituals, ambassador/champions programs, moderation, governance, growth, retention, crisis management, and metrics.
  Use for: community-led growth, community strategy, developer community, user community, Discord/Slack/forum/Telegram setup, ambassador programs, community health, holder psychology, engagement systems, social community building, cross-platform coordination.
metadata:
  version: 2.0.0
  category: Marketing
---

# Community Building

Build communities that turn members into believers and believers into advocates.

## Scope

**Covers**
- Community strategy (goal, members, value exchange, movement thesis)
- Platform selection: home base + outposts (Discord, Slack, Circle, Discourse, Telegram, Twitter/X, Reddit, Farcaster)
- Channel architecture, onboarding, and activation
- Programming/rituals and ambassador/champions programs
- Governance, moderation, and crisis management
- Holder psychology and retention engineering (crypto/token communities)
- Social community building across Twitter/X, Reddit, Farcaster, forums
- Measurement and community health

**When NOT to use**
- You haven't defined ICP/positioning (use `positioning-messaging` first)
- You want paid acquisition (ads/creative) rather than community
- You want to spam/scrape DMs or manipulate members
- You need customer support ops overhaul (ticketing/SLAs) more than community

---

## Community Philosophy

Great communities are built on three pillars:
1. **Shared purpose** — Members need a reason bigger than the product
2. **Genuine connection** — People stay for people, not features
3. **Member empowerment** — The best communities run themselves

### Community vs Audience

| Dimension | Audience | Community |
|-----------|----------|-----------|
| **Direction** | One to many | Many to many |
| **Value** | From creator | From each other |
| **Ownership** | Creator owns | Members co-own |
| **Content** | Creator produces | Members produce |
| **Retention** | Content-dependent | Relationship-dependent |
| **Scalability** | Linear | Network effects |

---

## Core Frameworks

### The Community Flywheel

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │  ATTRACT │───▶│ ACTIVATE │───▶│  ENGAGE  │             │
│   │ (Reach)  │    │ (Value)  │    │ (Habit)  │             │
│   └──────────┘    └──────────┘    └──────────┘             │
│        ▲                                │                   │
│        │          ┌──────────┐          │                   │
│        │          │ ADVOCATE │          │                   │
│        └──────────│ (Amplify)│◀─────────┘                   │
│                   └──────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

### Community Maturity Model

| Stage | Size | Characteristics | Focus |
|-------|------|-----------------|-------|
| **Nascent** | <100 | Founder-led | 1:1 conversations, manual everything |
| **Growing** | 100–1,000 | Early champions emerge | Systems, rituals, first programs |
| **Scaling** | 1,000–10,000 | Self-sustaining activity | Governance, moderation, delegation |
| **Mature** | 10,000+ | Community-led initiatives | Sub-communities, ecosystem |

### The 1-9-90 Rule

- **1%** create content (Creators)
- **9%** engage with content (Contributors)
- **90%** consume content (Lurkers)

Goal: Move people up the engagement ladder, not force everyone to create.

### Member Journey

```
Aware → Join → Lurk → First Post → Regular Contributor → Champion → Ambassador
```

| Stage | Goal | Key Metric |
|-------|------|------------|
| **Lurker** | First interaction | Post/reply count |
| **Newcomer** | Find value, connect | Retention D7 |
| **Regular** | Form habits, contribute | Weekly active |
| **Champion** | Lead initiatives | Content created |
| **Ambassador** | Represent externally | Referrals, reach |

---

## Inputs

**Minimum required**
- Product + category + ICP (who it's for)
- Primary community goal (pick 1): support, activation, retention, advocacy/UGC, product feedback, moving upmarket
- Target members (roles/seniority) and where they already gather
- Resources: owner, hours/week, budget, moderators/SMEs
- Existing assets: email list, social following, events, partners
- Constraints: compliance/privacy, brand voice, moderation risk tolerance

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time)
- Proceed with explicit assumptions if critical inputs missing; provide 2–3 options with tradeoffs

---

## Platform Selection

### Platform Comparison

| Platform | Best For | Key Strength | Key Weakness |
|----------|----------|--------------|--------------|
| **Discord** | Gaming, dev, real-time | Rich features, free | Overwhelming UX |
| **Slack** | Professional, B2B | Familiar, searchable | Expensive at scale |
| **Circle** | Courses, creators | Clean UX, courses | Less real-time |
| **Discourse** | Long-form, async | SEO, knowledge base | Old-school feel |
| **GitHub Discussions** | Open source, devs | Code integration | Limited features |
| **Reddit** | Public discovery | SEO, scale | Less control |
| **Telegram** | Crypto/token holders | Real-time, bots | Limited moderation |

### Platform Architecture

**Discord (larger projects)**
```
INFORMATION: #announcements #faq #roadmap #rules
COMMUNITY:   #general #price-talk #memes #introductions
ALPHA (role-gated): #whale-chat #og-lounge #team-updates
SUPPORT:     #help #report-scams #suggestions
VOICE:       General VC, AMA Stage
```

**Telegram (token/crypto communities)**
```
[Main Group]     — Public chat, price bot, welcome message, active mods
[Announcements]  — One-way official updates only
[Alpha/Holders]  — Token-gated, exclusive content, direct team access
[International]  — CN/KR/JP with local mods (if needed)
```

**Essential Bots**: Price bot, Buy bot (celebrate purchases), Holder verification, Anti-spam/scam, Welcome bot.

### Social Platform Strategies

**Twitter/X**: Reach and real-time discussion. Twitter Spaces for live audio, threads for depth, quote tweets for community amplification.

**Reddit**: Long-form depth and discovery. Build a subreddit or participate in existing ones. SEO benefit from indexed discussions.

**Farcaster**: Crypto-native audience, frames for interactive content, native to web3 culture.

**Forums (Discourse, etc.)**: Long-form async knowledge base, SEO-indexed, permanent resource for members.

---

## Workflow (8 Steps)

### 1) Intake + Pick Primary Job-to-be-Done
- **Inputs:** User prompt; [references/INTAKE.md](references/INTAKE.md)
- **Actions:** Confirm ICP, define primary goal, identify where community already gathers, list constraints
- **Outputs:** Context snapshot + assumptions/TBDs list
- **Check:** You can finish: "In 8–12 weeks, this community will _____ for _____, measured by _____."

### 2) Define the Movement + Value Exchange
- **Inputs:** Product POV, category beliefs, member motivations
- **Actions:** Write community thesis: worldview/philosophy, what you stand for, what you're "against." Define give/get value exchange.
- **Outputs:** Community thesis + value exchange
- **Check:** Thesis is non-generic (can't fit any random company); value exchange includes concrete benefits and contributions

### 3) Choose Community Model + Map Member Journey
- **Inputs:** Primary goal, member needs, resources
- **Actions:** Choose model (support, learning, networking, advocacy, co-creation). Map journey with "first win" moments per stage.
- **Outputs:** Community model + journey map + metrics
- **Check:** Each stage has a designed "first win" and a measurable signal

### 4) Go Where They Already Are (Home Base + Outposts)
- **Inputs:** Where members already are; moderation/capacity constraints
- **Actions:** Select home base for 6–12 months. Define outposts (social, events, partner spaces). Create influencer/social-graph shortlist.
- **Outputs:** Platform plan + outpost playbook + influencer shortlist
- **Check:** Every outpost has a value-first contribution plan and an owner

### 5) Seed the Community (Cohort, Onboarding, Content)
- **Inputs:** Platform plan; existing assets; member criteria
- **Actions:** Design initial seed cohort (25–100 members). Create onboarding flow, welcome messages, starter threads, seeding schedule. Draft outreach scripts.
- **Outputs:** Seeding plan + onboarding checklist + outreach scripts
- **Check:** The "empty room problem" is solved — content, prompts, and people lined up for week 1

**Onboarding ritual (first 48 hours):**
1. Welcome DM with "Start Here" guide
2. Prompt to post in `#introductions`
3. React to their intro post (human touch)
4. Share one quick win they can get from the community

### 6) Program Rituals + Events (4–8 Week Calendar)
- **Inputs:** Member journey; thesis; capacity
- **Actions:** Build recurring rituals (AMAs, office hours, show-and-tell, challenges). Mix staff-led and member-led moments.
- **Outputs:** Programming & rituals calendar + event templates

**Weekly engagement calendar:**

| Day | Theme | Activities |
|-----|-------|-----------|
| Monday | Mission/Goals | Weekly goals, roadmap updates |
| Tuesday | Educational | Alpha sharing, tips, how-tos |
| Wednesday | Member Spotlight | Champion recognition, community wins |
| Thursday | Throwback/Story | Origin story, OG moments, milestones |
| Friday | Engagement | Partnership teasers, community events |
| Saturday | Growth | Community raids, meme contests, referrals |
| Sunday | Strategy | Market analysis, community AMAs |

**Daily loop**: Morning greeting + poll → Midday content + news → Evening recap + tomorrow's preview.

### 7) Launch Ambassador/Champions Program (Optional, Recommended)
- **Inputs:** Early active members; desired scaled behaviors
- **Actions:** Define qualification criteria, responsibilities, recognition/perks, feedback loop. Keep lightweight (v1), ethical (no pay-for-spam).
- **Outputs:** Ambassador/champions program spec (v1)
- **Check:** Incentives align to desired behaviors (helpfulness, creation, referrals), not vanity metrics

**Recognition system:**
- Public shoutouts for helpful members
- Badges or roles for milestones
- Leaderboard or "Member of the Month"
- Early access to features or beta programs

### 8) Governance + Measurement + Quality Gate
- **Inputs:** Draft pack; [references/CHECKLISTS.md](references/CHECKLISTS.md); [references/RUBRIC.md](references/RUBRIC.md)
- **Actions:** Define rules, moderation workflows, escalation paths. Create measurement plan + weekly ops cadence.
- **Outputs:** Final Community Building Pack

---

## Moderation & Governance

**Community rules (keep to 5–7):**
1. Be respectful — no harassment, hate speech, or personal attacks
2. Stay on topic — keep discussions relevant
3. No spam or self-promotion without permission
4. Share knowledge freely — help each other
5. Protect privacy — no sharing others' personal info
6. Report issues — use report function or DM mods

**Enforcement ladder**: Warning → Temporary mute → Permanent ban.

**Moderator responsibilities**: Daily check-in (15 min), respond to reports within 24h, escalate edge cases to community lead.

---

## Crisis Management (Especially for Token Communities)

### FUD Response Levels

| Level | Source | Response | Timeline |
|-------|--------|----------|----------|
| 1 — Minor | No-following account | Community handles; mods monitor | Hours |
| 2 — Moderate | Some-reach account | Mod statement + optional team clarification | 1–2 hours |
| 3 — Major | Major account or coordinated | Official team statement + pinned message | 30 min |
| 4 — Critical | Actual exploit or viral negative | All-hands, full transparency everywhere | Immediately |

### Crisis Response Template
```
TEAM STATEMENT: [Topic]
We're aware of [concern].

THE FACTS:
- [Fact 1]
- [Fact 2]

OUR RESPONSE: [What we're doing]
EVIDENCE: [Links to proof/data]

We remain committed to [mission]. Questions? We're here.
```

---

## Retention Tactics

**General retention:**
- Monthly digest email with top content
- Re-engagement campaign for inactive members (30-day lapse)
- Regular "bring a friend" referral moments

**Token/holder community retention:**
- Diamond hand cultivation: public commitments, holding anniversaries, "Day 1" badges
- Dip buying culture: celebrate dip buyers loudly; "sale" framing for price drops
- Multi-bag culture: "This AND that" — avoid forcing either/or decisions

---

## Key Metrics

| Category | Metrics | Healthy Target |
|----------|---------|---------------|
| **Growth** | New members, referral rate, churn rate | — |
| **Engagement** | DAU/MAU, posts per member, response time | DAU/MAU >20% |
| **Health** | Sentiment, helpful answers, retention | Monthly retention >80% |
| **Value** | NPS, support deflection, product influence | NPS >50 |

**Health signals:**
- DAU/MAU <10% → trigger re-engagement campaign
- Top 10 members account for >80% of posts → run "new voices" initiative

### Community Health Report Template
```
COMMUNITY HEALTH REPORT | Period: [Week/Month]

GROWTH:      Total Members [+/-X%] | New Joins | Departures
ENGAGEMENT:  Messages (7d) | Unique Chatters | Peak Activity | Score [X/10]
SENTIMENT:   Long-term Holders >30d [X%] | Toxicity Level [Low/Med/High]
MODERATION:  Bans | Warnings | Scam Attempts Blocked

RECOMMENDATIONS:
1. [Action]  2. [Action]  3. [Action]

HEALTH SCORE: [X]/100
```

---

## Community-Led Growth (CLG) Quick Reference

| Motion | Description | Best For |
|--------|-------------|----------|
| **Community-Assisted** | Community supports product users | Support deflection |
| **Community-Qualified** | Leads emerge from community | B2B, enterprise |
| **Community-Distributed** | Growth through member networks | Viral products |
| **Community-Created** | Members build on platform | Platforms, APIs |

---

## Anti-Patterns

- **Build it and they will come** — Communities require constant nurturing, especially early
- **Metrics over meaning** — Vanity metrics don't equal healthy community
- **Over-engineering early** — Start simple, add complexity as needed
- **Ignoring lurkers** — 90% of your community provides value by consuming
- **Founder absence** — Early communities need visible leadership
- **Feature obsession** — People join for people, not features
- **Forced engagement** — Authentic connection beats gamification
- **Scaling too fast** — Growth without engagement destroys community
- **Neglecting moderation** — One bad actor can poison the well
- **Spam/DM blasts** — Never auto-DM or manipulate members

---

## Outputs (Community Building Pack)

Produce in this order:

1. **Context snapshot** + assumptions/TBDs
2. **Community thesis** (movement/philosophy), target members, value exchange
3. **Community model + member journey** + success metrics
4. **Platform plan** (home base + outposts) + influencer/social-graph shortlist
5. **30/60/90 plan** (seeding, onboarding, activation) + outreach scripts
6. **Programming & rituals calendar** (first 4–8 weeks)
7. **Ambassador/champions program v1** (criteria, responsibilities, recognition)
8. **Governance & moderation** (rules, enforcement, escalation, safety)
9. **Measurement plan + weekly ops cadence**
10. **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

---

## Quality Gate (Required)

- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md)
- Always include: **Risks**, **Open questions**, **Next steps**

---

## Examples

**Developer tool:** "Use `community-building`. Product: observability SDK for TypeScript. ICP: senior full-stack engineers at startups. Goal: accelerate activation + word-of-mouth. Considering Discord. Resources: 1 community lead (8 hrs/week). Output: Community Building Pack with platform plan, 6-week programming calendar, ambassador program."

**B2B SaaS moving upmarket:** "We sell a team knowledge base to 200–2000 person companies. We want community-led growth to reduce enterprise perceived risk. Design home base + outpost plan, seed cohort strategy, and 30/60/90 plan with metrics."

**Token/crypto community:** "Building a Telegram community for our token launch. Need holder psychology framework, weekly engagement calendar, crisis management protocol, and launch checklist."

**Social community:** "We want to build a Twitter/X and Reddit presence for our developer tool community. Design a cross-platform social community strategy with engagement rituals and growth playbook."
