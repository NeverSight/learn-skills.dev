---
name: outbound-sequencer
description: Design multi-touch outbound sequences with optimal timing, channel mix, and messaging progression for SDR campaigns
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Outbound Sequencer

> Create high-converting outbound sequences with strategic touchpoint timing, channel orchestration, and message progression.

## When to Use This Skill

- Designing new outbound campaigns
- Optimizing existing sequences
- Creating segment-specific cadences
- Testing sequence variations
- Training SDRs on best practices

## Methodology Foundation

Based on **Outreach.io Sequence Science** and **SalesLoft Cadence Research**, combining:
- Optimal touchpoint timing
- Multi-channel orchestration
- Message progression strategy
- Personalization at scale

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs sequence structure | Message copy |
| Suggests optimal timing | Brand voice |
| Recommends channel mix | Tool selection |
| Creates progression logic | A/B test priorities |
| Identifies optimization areas | Resource allocation |

## Instructions

### Step 1: Define Sequence Parameters

**Key Variables:**
| Parameter | Options |
|-----------|---------|
| Touches | 8-14 typical |
| Duration | 14-30 days |
| Channels | Email, Phone, LinkedIn, Video |
| Goal | Meeting, Response, Qualification |

### Step 2: Design Channel Mix

**Recommended Mix:**
| Channel | Percentage | Purpose |
|---------|------------|---------|
| Email | 50-60% | Scale, persistence |
| LinkedIn | 20-25% | Personal touch |
| Phone | 15-20% | Direct connection |
| Video | 5-10% | Differentiation |

### Step 3: Structure Touchpoints

**Framework: 4-Phase Sequence**

| Phase | Days | Purpose | Intensity |
|-------|------|---------|-----------|
| Opening | 1-3 | Hook, establish | High |
| Building | 4-10 | Value, credibility | Medium |
| Urgency | 11-18 | Social proof, FOMO | High |
| Breakup | 19-25 | Final push, close loop | Low |

### Step 4: Message Progression

**Progression Pattern:**
1. **Touch 1**: Hook with insight/trigger
2. **Touch 2-3**: Value proposition, social proof
3. **Touch 4-6**: Different angles, persistence
4. **Touch 7-9**: Urgency, scarcity
5. **Touch 10+**: Breakup, future timing

## Examples

### Example 1: Enterprise Outbound Sequence

**Output:**
```
## Enterprise Outbound Sequence (14 touches, 21 days)

### Sequence Overview
- **Target**: VP+ at enterprise companies
- **Goal**: Booked meeting
- **Duration**: 21 days
- **Touches**: 14 total

### Channel Mix
| Channel | Touches | % |
|---------|---------|---|
| Email | 7 | 50% |
| LinkedIn | 4 | 29% |
| Phone | 2 | 14% |
| Video | 1 | 7% |

---

### Full Sequence

#### Phase 1: Opening (Days 1-3)

**Day 1 - Email #1 (Trigger-based)**
```
Subject: [Trigger] + [Company]

Hi [FirstName],

[Trigger observation - funding, hire, news].

I work with [similar companies] who face [challenge]. Curious if that's on your radar?

[One line value prop]

Worth a quick call?

[Name]
```

**Day 1 - LinkedIn Connection**
- Send connection request
- Note: "Hi [Name], [brief reason for connecting]"

**Day 2 - Phone Call #1**
- Goal: Live conversation
- If VM: "Hi [Name], [Name] from [Company]. Quick call about [trigger]. Will follow up via email."

**Day 3 - LinkedIn Voice Note**
- 30-second personalized message
- Reference trigger + offer value

---

#### Phase 2: Building (Days 4-10)

**Day 4 - Email #2 (Value)**
```
Subject: Re: [Previous subject]

[FirstName],

Wanted to share what [Similar Customer] achieved:
- [Metric 1]
- [Metric 2]

They were in a similar situation when we first connected.

Worth comparing notes?

[Name]
```

**Day 6 - LinkedIn Engagement**
- Engage with their content (like, comment)
- OR share relevant content, tag them

**Day 8 - Email #3 (Different Angle)**
```
Subject: Quick question about [specific challenge]

[FirstName],

Most [Titles] I talk to say [specific challenge] is their #1 priority this quarter.

Quick question: Is that true for you too, or is something else taking priority?

Genuinely curious—helps me understand what matters most to leaders like you.

[Name]
```

**Day 10 - Phone Call #2**
- Morning attempt
- Different VM: "Hi [Name], following up on my emails. Would love 15 minutes to discuss [value]. [Your number]."

---

#### Phase 3: Urgency (Days 11-18)

**Day 11 - Email #4 (Social Proof)**
```
Subject: How [Competitor's Customer] solved [problem]

[FirstName],

[Competitor's Customer] was dealing with [same problem].

After [implementing solution], they saw:
• [Result 1]
• [Result 2]

Happy to walk through their approach if useful.

[Name]
```

**Day 13 - LinkedIn Direct Message**
```
Hi [Name],

I've reached out a few times—wanted to try a different channel.

Not trying to sell you anything. Genuinely think [insight] could help [Company].

Open to a quick chat?
```

**Day 15 - Email #5 (Video)**
```
Subject: Recorded this for you, [FirstName]

[FirstName],

Put together a 60-second video on why I think [Company] would benefit from [approach].

[Video thumbnail/link]

If this resonates, let's talk. If not, no worries—I'll stop reaching out.

[Name]
```

**Day 18 - Email #6 (Urgency)**
```
Subject: [Event/timing trigger]

[FirstName],

With [event/quarter end/budget cycle] coming up, a lot of [Titles] are locking in [decisions].

Last chance to get this on your calendar before [deadline].

Quick call this week?

[Name]
```

---

#### Phase 4: Breakup (Days 19-21)

**Day 19 - LinkedIn Final**
- Send article or resource relevant to them
- No ask, just value

**Day 21 - Email #7 (Breakup)**
```
Subject: Should I close your file?

[FirstName],

I've reached out several times and haven't heard back. Totally understand—you're busy.

Just want to check: should I close out your file, or is this something worth revisiting in the future?

If timing isn't right, let me know and I'll circle back in [timeframe].

Either way, wishing you a great [quarter/year].

[Name]
```

---

### Sequence Metrics (Benchmarks)

| Metric | Target | Excellent |
|--------|--------|-----------|
| Open Rate | >40% | >55% |
| Reply Rate | >8% | >15% |
| Meeting Rate | >3% | >6% |
| Positive Reply | >60% of replies | >75% |
```

### Example 2: High-Velocity SMB Sequence

**Output:**
```
## SMB Quick-Hit Sequence (8 touches, 14 days)

### Sequence Overview
- **Target**: Manager/Director at SMB
- **Goal**: Demo or trial signup
- **Duration**: 14 days
- **Touches**: 8 total

### Channel Mix
| Channel | Touches | % |
|---------|---------|---|
| Email | 5 | 63% |
| LinkedIn | 2 | 25% |
| Phone | 1 | 12% |

---

### Rapid Sequence

**Day 1 - Email #1 (Direct)**
```
Subject: Quick question, [FirstName]

Hi [FirstName],

Do you handle [function] at [Company]?

If so, I have an idea that could help you [specific outcome] in [timeframe].

Interested?

[Name]
```

**Day 1 - LinkedIn Connect**
- Simple connection request

**Day 3 - Email #2 (Value)**
```
Subject: Re: Quick question

[FirstName],

[One stat or proof point from similar company]

That's what [Customer] did with us.

Worth 10 minutes to see if we can do the same for [Company]?

[Name]

P.S. Here's a 2-min video showing how: [link]
```

**Day 5 - Phone Call**
- Quick call attempt
- VM: Keep to 20 seconds

**Day 7 - LinkedIn Message**
```
Hey [Name] - saw you opened my email but haven't had a chance to connect. Totally get it. Is [problem] even a priority for you right now?
```

**Day 9 - Email #3 (Different Hook)**
```
Subject: [Competitor name] alternative?

[FirstName],

A lot of [Company size] companies tell us they're frustrated with [competitor/status quo].

We're simpler + faster. Most customers are up and running in [timeframe].

Worth a look?

[Name]
```

**Day 11 - Email #4 (Offer)**
```
Subject: Try us free?

[FirstName],

Want to just show you instead of tell you?

Here's a free [trial/assessment/audit]: [link]

No commitment, no call required.

[Name]
```

**Day 14 - Email #5 (Breakup)**
```
Subject: Last one from me

[FirstName],

Haven't heard back, so this will be my last email.

If [problem] becomes a priority, I'm here: [calendar link]

Good luck with everything!

[Name]
```
```

## Skill Boundaries

### What This Skill Does Well
- Structuring sequence flow
- Optimizing touchpoint timing
- Balancing channel mix
- Creating progression logic

### What This Skill Cannot Do
- Write final copy for you
- Know your specific personas
- Access sequence tools
- Test variations automatically

## References

- Outreach.io Sequence Science
- SalesLoft Cadence Research
- Gong Outbound Best Practices
- TOPO SDR Benchmark Report

## Related Skills

- `icp-matching` - Target the right accounts
- `signal-monitoring` - Trigger-based outreach
- `lead-qualification-bant` - Qualify responses

## Skill Metadata

- **Domain**: SDR Automation
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 1-2 hours per sequence
- **Prerequisites**: ICP, messaging framework
