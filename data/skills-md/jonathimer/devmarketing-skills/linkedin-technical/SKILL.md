---
name: linkedin-technical
description: When the user wants to reach developers on LinkedIn, create technical content for B2B audiences, or understand when LinkedIn beats Twitter. Trigger phrases include "LinkedIn," "LinkedIn for developers," "B2B developer marketing," "engineering managers," "reaching CTOs," or "technical LinkedIn content."
metadata:
  version: 1.0.0
---

# LinkedIn for Technical Audiences

LinkedIn is where B2B developer tools win deals. This skill covers technical content that works on LinkedIn, reaching engineering managers and decision-makers, and knowing when LinkedIn beats Twitter.

---

## Before You Start

1. Read `.agents/developer-audience-context.md` if it exists
2. Assess your LinkedIn presence (profile, connections, content history)
3. Understand: LinkedIn rewards different content than developer Twitter

---

## When LinkedIn Beats Twitter

### LinkedIn's Unique Value

| Factor | LinkedIn advantage |
|--------|-------------------|
| **B2B decisions** | Decision-makers are here |
| **Enterprise reach** | CTOs, VPs, directors active |
| **Company context** | See role, company, team size |
| **Professional network** | Second-degree reach is valuable |
| **Long-form content** | Articles rank in Google |
| **Lead generation** | Built-in company/role targeting |

### Use LinkedIn When

| Scenario | Why |
|----------|-----|
| Selling to enterprises | Buyers are on LinkedIn |
| Reaching engineering managers | More managers here than Twitter |
| Recruiting developer users | Professional context |
| B2B partnerships | Companies > individuals |
| Industry/vertical targeting | Company data available |
| Longer professional content | Newsletters, articles |

### Use Twitter When

| Scenario | Why |
|----------|-----|
| Individual developers | More devs on Twitter |
| Real-time engagement | Faster conversation |
| Open source projects | Community is on Twitter |
| Casual/authentic voice | LinkedIn is more formal |
| Technical hot takes | Twitter thrives on debate |

---

## Understanding LinkedIn's Audience

### Who's Actually Active

| Segment | Engagement level | What they consume |
|---------|------------------|-------------------|
| Engineering managers | High | Leadership, team building |
| CTOs/VPs Engineering | Medium | Strategy, industry trends |
| Tech recruiters | Very high | Talent, employer branding |
| DevRel/Developer advocates | High | Community, content tactics |
| Solution architects | Medium | Technical evaluations |
| Individual developers | Lower | Career, learning |

### What LinkedIn Values

| Content type | Performance | Notes |
|--------------|-------------|-------|
| Personal stories | Very high | LinkedIn loves narrative |
| Career lessons | High | Professional growth content |
| Contrarian opinions | High | "Unpopular opinion:" works |
| Behind-the-scenes | High | Company/team stories |
| Technical deep dives | Medium | More accessible than Twitter |
| Plain announcements | Low | Need personal angle |
| Shared links | Very low | Algorithm deprioritizes |

---

## Content That Works

### The LinkedIn Technical Post Formula

```
[Hook: Personal statement or question]

[Short paragraph: The context or problem]

[Bullet points: 3-5 key insights]

[Personal take: What you learned]

[CTA: Question or action]

---

[Hashtags: 3-5 relevant ones]
```

### Example Formats

**The "Here's What Happened" Post**:
```
Last month we migrated 2TB of data from MongoDB to PostgreSQL.

Here's what we learned (and what we'd do differently):

→ Start with a test migration
   We didn't. Cost us 3 days.

→ Schema mapping is 80% of the work
   The actual migration is easy.

→ Watch for timezone handling
   MongoDB stores UTC, Postgres respects your settings.

→ Have a rollback plan
   Ours worked. Twice.

The migration took 4 days total, not the "weekend project" we planned.

What's your biggest database migration war story?

#engineering #databases #postgresql
```

**The "Unpopular Opinion" Post**:
```
Unpopular opinion: Most engineering teams don't need Kubernetes.

I've seen 3-person startups running K8s because "Netflix uses it."

The reality:
• Single container on Railway/Render: $20/month
• Managed K8s: $300/month minimum
• Self-hosted K8s: 1 FTE just for maintenance

Kubernetes is amazing for:
→ Multi-region deployments
→ Complex orchestration needs
→ 99.99% SLA requirements

But most apps? Docker Compose on a VM is fine.

What's the smallest team you've seen running Kubernetes?

#devops #kubernetes #startups
```

**The "Behind the Scenes" Post**:
```
We just hit 10,000 API calls per second.

Here's the unsexy truth about scaling:

6 months ago we could barely handle 1,000 req/s.

What changed:
→ Moved hot paths to Redis
→ Implemented connection pooling (finally)
→ Added CDN for static assets
→ Profiled and found 3 N+1 queries

No fancy architecture. No rewrite.
Just fixing obvious stuff we'd ignored.

The lesson: Optimize boring things first.

What's the simplest optimization that made your biggest impact?
```

### Content Mix for LinkedIn

| Type | Percentage | Purpose |
|------|------------|---------|
| Personal insights | 40% | Build authority |
| Technical content | 30% | Demonstrate expertise |
| Company/team stories | 20% | Employer branding |
| Promotional | 10% | Actual asks |

---

## Formatting Best Practices

### Post Structure

| Element | Guideline |
|---------|-----------|
| **First line** | Hook — make them click "see more" |
| **Length** | 1,200-1,500 characters optimal |
| **Line breaks** | Every 1-2 sentences |
| **White space** | Use blank lines liberally |
| **Emojis** | Sparingly, for bullets (→, •) |
| **Hashtags** | 3-5 at the end |

### What Gets Hidden

LinkedIn truncates after ~210 characters. Your first 2-3 lines are critical.

**Bad hook** (no curiosity gap):
```
I wanted to share some thoughts about microservices.
```

**Good hook** (creates curiosity):
```
We ripped out our microservices architecture.

Here's why going back to a monolith was the right call:
```

### Visual Content

| Format | Performance | Use for |
|--------|-------------|---------|
| Carousels (PDF) | Very high | Step-by-step, lists |
| Native video | High | Demos, explanations |
| Images | Medium | Diagrams, screenshots |
| Text only | Medium | Stories, opinions |
| Links | Low | External content |

**Carousel tips**:
- 5-10 slides optimal
- First slide = thumbnail (make it count)
- Large text, minimal per slide
- Upload as PDF for carousel effect

---

## Company Page vs Personal

### When to Use Each

| Use Case | Company Page | Personal Profile |
|----------|--------------|------------------|
| Product announcements | ✓ | Cross-post |
| Company news | ✓ | Leadership shares |
| Industry thought leadership | | ✓ |
| Technical insights | | ✓ |
| Hiring posts | ✓ | Hiring manager shares |
| Customer stories | ✓ | Personal angle helps |

### The Reality

| Metric | Company Pages | Personal Profiles |
|--------|---------------|-------------------|
| Organic reach | Low (2-5%) | Higher (10-20%) |
| Engagement | Lower | Higher |
| Following growth | Slow | Faster |
| Lead gen tools | Available | Limited |
| Analytics | Better | Basic |

**Strategy**: Post from company page, have team members share with personal commentary.

---

## Reaching Engineering Managers

### What Engineering Managers Care About

| Topic | Why it resonates |
|-------|------------------|
| Team productivity | Their main metric |
| Hiring/retention | Constant challenge |
| Technical decisions | Balancing team + business |
| Developer experience | Team satisfaction |
| Technical debt | Constant negotiation |
| Process improvements | Making teams effective |

### Content Angles for EM Audience

| Angle | Example hook |
|-------|--------------|
| Metrics | "The 3 metrics our team tracks (and 5 we stopped tracking)" |
| Process | "How we cut our sprint planning from 4 hours to 45 minutes" |
| Hiring | "The technical interview question that tells us the most" |
| Tech decisions | "Why we chose boring technology for our startup" |
| Team building | "What I learned managing my first remote team" |

---

## Hashtags

### Technical Hashtags That Work

| Hashtag | Audience |
|---------|----------|
| #engineering | Broad engineering |
| #softwaredevelopment | General dev |
| #webdevelopment | Web devs |
| #devops | DevOps/SRE |
| #cloudcomputing | Cloud/infra |
| #startup | Startup audience |
| #techleadership | EMs, VPs |
| #remotework | Remote teams |
| #hiring | Recruiting context |
| #opensource | OSS community |

### Hashtag Rules

- 3-5 hashtags maximum
- Put at the end of post
- Mix broad (#engineering) and specific (#kubernetes)
- Skip if post is personal/narrative

---

## Platform-Specific Do's and Don'ts

### Do's

1. **Do** write posts, not status updates
2. **Do** use line breaks liberally
3. **Do** start with a hook
4. **Do** share personal experiences
5. **Do** engage in comments (first hour matters)
6. **Do** cross-post from company page personally
7. **Do** use carousels for educational content
8. **Do** mention people and companies when relevant

### Don'ts

1. **Don't** post just links (algorithm kills them)
2. **Don't** use LinkedIn like Twitter
3. **Don't** over-hashtag (looks spammy)
4. **Don't** be too promotional
5. **Don't** ignore comments
6. **Don't** post walls of text without breaks
7. **Don't** share memes (different culture than Twitter)
8. **Don't** buy engagement pods

---

## Profile Optimization

### Technical Professional Profile

| Section | Best practice |
|---------|---------------|
| **Photo** | Professional, friendly |
| **Headline** | [Role] at [Company] | [What you do/help with] |
| **About** | Story format: background → now → what you share |
| **Featured** | Pin your best posts, articles |
| **Experience** | Focus on impact, not job duties |
| **Skills** | Technical skills get endorsements |

**Headline examples**:
```
Staff Engineer at Stripe | Building payments infrastructure

VP Engineering at Startup | Scaling teams from 5 to 50

DevRel at Supabase | Making databases accessible
```

---

## LinkedIn Articles vs Posts

### When to Use Articles

| Articles | Posts |
|----------|-------|
| 1,000+ words | Under 1,500 characters |
| SEO value (Google indexed) | No SEO |
| Evergreen content | Timely/current |
| Newsletter integration | One-time reach |
| Lower immediate reach | Higher immediate reach |

### Article Best Practices

- Front-load value (assume people don't finish)
- Use headers and formatting
- Include visuals
- End with CTA
- Share as post after publishing

---

## Tools

| Tool | Use case |
|------|----------|
| **[Octolens](https://octolens.com)** | Monitor LinkedIn for mentions of your product, competitors, and relevant conversations. Track when your space gets discussed. |
| **Shield Analytics** | Detailed LinkedIn analytics |
| **Taplio** | Post scheduling and analytics |
| **AuthoredUp** | Post formatting and preview |
| **Canva** | Carousel design |
| **PDF carousels** | Create in Canva, upload as PDF |

---

## Content Calendar

### Weekly Template

| Day | Content type |
|-----|--------------|
| Monday | Technical insight post |
| Tuesday | Engage with others' content |
| Wednesday | Personal/career story |
| Thursday | Company news (shared personally) |
| Friday | Industry opinion or hot take |

---

## Measuring Success

### Metrics That Matter

| Metric | What it tells you |
|--------|-------------------|
| Impressions | Reach of content |
| Engagement rate | Content resonance |
| Profile views | Interest generation |
| Connection requests | Network growth |
| Followers | Audience building |
| Click-throughs | Action conversion |
| Comments | Discussion value |

### Good Benchmarks

| Metric | Good | Great |
|--------|------|-------|
| Engagement rate | 2-3% | 5%+ |
| Profile views/week | 50+ | 200+ |
| Post reach | 500+ | 2000+ |

---

## Related Skills

- `developer-audience-context` — Know who you're reaching
- `x-devs` — Cross-post adapted content
- `github-presence` — Link from LinkedIn to GitHub
- `youtube-devrel` — Share video content on LinkedIn
