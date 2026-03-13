---
name: x-devs
description: When the user wants to build a developer following on Twitter/X, write technical threads, or understand what works for dev audiences on X. Trigger phrases include "Twitter," "X," "developer Twitter," "tech Twitter," "technical threads," "building dev following," or "Twitter for developers."
metadata:
  version: 1.0.0
---

# X/Twitter for Developers

Twitter/X remains the real-time pulse of the developer community. This skill covers thread structure, code screenshots, engagement tactics, and building an authentic developer following without being cringe.

---

## Before You Start

1. Read `.agents/developer-audience-context.md` if it exists
2. Audit your current X presence (bio, pinned, recent posts)
3. Understand: Developer Twitter rewards authenticity and technical depth

---

## Understanding Dev Twitter

### Who's on Dev Twitter

| Segment | What they share | What they consume |
|---------|-----------------|-------------------|
| Open source maintainers | Project updates, war stories | Industry news, peer projects |
| Tech leads | Team learnings, hiring | Architecture, management |
| Indie hackers | Building in public, MRR | Growth tactics, tools |
| DevRel | Content, events, community | Trends, developer sentiment |
| Framework authors | Updates, opinions | Feedback, community vibes |
| Learning devs | Questions, progress | Tutorials, inspiration |

### What Works on Dev Twitter

| Content type | Engagement level | Notes |
|--------------|------------------|-------|
| Technical threads | High | Deep dives get saved/shared |
| Code screenshots | High | Visual, scannable |
| Hot takes | High (risky) | Can backfire spectacularly |
| Building in public | High | Journey > destination |
| Memes | Medium-high | Know your audience |
| Announcements | Medium | Better with context |
| Tutorial links | Medium | Need compelling hook |
| Retweets with comment | Low-medium | Add real value |
| Plain links | Low | Algorithm deprioritizes |

### The Algorithm (As We Understand It)

| Factor | Impact |
|--------|--------|
| Replies in first hour | High — signals engagement |
| Time spent on post | High — threads > tweets |
| Profile visits from post | High — interesting content |
| Bookmarks | High — "save for later" |
| Retweets | Medium — distribution |
| Likes | Medium — engagement signal |
| Link clicks | Low — X wants you on platform |
| External links | Negative — deprioritized |

---

## Thread Structure

### Thread Anatomy

```
Tweet 1: HOOK
↓
Tweet 2: Context/Promise
↓
Tweets 3-8: The meat (examples, steps, insights)
↓
Tweet 9: Summary/Takeaway
↓
Tweet 10: CTA + Engagement ask
```

### Hook Patterns That Work

| Pattern | Example |
|---------|---------|
| **Contrarian** | "Hot take: You don't need Kubernetes for most apps" |
| **Promise** | "How we reduced our AWS bill by 60% (thread)" |
| **Story** | "Last week our API went down for 4 hours. Here's what happened:" |
| **List tease** | "7 TypeScript tricks that changed how I code:" |
| **Question** | "Why do most startups get database migrations wrong?" |
| **Result** | "We went from 0 to 10K users in 30 days. Here's the playbook:" |

### Thread Writing Best Practices

| Element | Guideline |
|---------|-----------|
| **Length** | 5-12 tweets optimal |
| **First tweet** | Hook — no hashtags, no links |
| **Each tweet** | One idea, complete thought |
| **Numbering** | Use X/10 format or emoji bullets |
| **Code** | Screenshots > text (more engaging) |
| **Pacing** | Mix short punchy + longer explanatory |
| **Last tweet** | CTA: follow, reply, bookmark |

### Thread Template

```
🧵 [Hook: Compelling statement or question]

Here's what I learned [context]:

1/ [First key point]

[Supporting detail or example]

2/ [Second key point]

[Code screenshot or visual]

3/ [Third key point]

The counterintuitive part:

[Insight that surprises]

4/ [Fourth key point]

Common mistake to avoid:

[What not to do and why]

5/ [Summary]

TL;DR:
• Point 1
• Point 2
• Point 3

If this was helpful, give me a follow @handle for more [topic].

What's your experience with [topic]? 👇
```

---

## Code Screenshots

### Why Screenshots Beat Code Blocks

| Screenshots | Code blocks |
|-------------|-------------|
| Syntax highlighting | Plain text |
| Control over appearance | Platform formatting |
| Can include context | Just code |
| More visual stops | Scroll past |
| Better engagement | Lower engagement |

### Code Screenshot Tools

| Tool | Best for |
|------|----------|
| **Carbon** (carbon.now.sh) | Beautiful, customizable |
| **Ray.so** | Clean, modern |
| **Snappify** | Annotations, animations |
| **CodeSnap** (VS Code) | Quick from editor |
| **Silicon** (CLI) | Automation |

### Screenshot Best Practices

| Do | Don't |
|----|-------|
| Use dark theme | Light theme (harder to read) |
| Include file name | Remove context |
| Highlight key lines | Show walls of code |
| Keep width reasonable | Make text tiny |
| Use consistent styling | Different themes per post |
| Add comments in code | Explain separately only |

---

## Engagement Timing

### Best Posting Times

| Time (PT) | Audience | Notes |
|-----------|----------|-------|
| 6-8 AM | US East Coast + Europe | Morning scroll |
| 10 AM - 12 PM | Peak US | Lunch break |
| 4-6 PM | US evening + Europe late | End of workday |

### Posting Frequency

| Frequency | Effect |
|-----------|--------|
| 1-3 tweets/day | Sustainable, quality |
| 3-5 tweets/day | Growth mode |
| 5+ tweets/day | Risk of overexposure |
| 1 thread/week | Good cadence |
| 2-3 threads/week | Aggressive growth |

### Thread Timing

- **Post threads** in morning (7-10 AM PT)
- **Engage replies** for first 2 hours
- **Quote tweet** your thread later in day
- **Post follow-up** content same day

---

## Hashtags (Use Sparingly)

### Developer Hashtags

| Hashtag | Use for |
|---------|---------|
| #buildinpublic | Indie hacker updates |
| #devrel | DevRel content |
| #100DaysOfCode | Learning journey |
| #opensource | OSS announcements |
| #webdev | Web development |
| #javascript #python etc. | Language-specific |

### Hashtag Rules

| Do | Don't |
|----|-------|
| Max 1-2 per tweet | Stuff with hashtags |
| Put at end | Lead with hashtags |
| Use for discoverability | Use on every post |
| Skip in threads | Add to every tweet |

---

## Building a Dev Following

### The Flywheel

1. **Create valuable content** → People engage
2. **Engage with replies** → Build relationships
3. **Reply to others' posts** → Get discovered
4. **Consistency** → Algorithm favors you
5. **Followers grow** → More reach
6. **Repeat**

### Profile Optimization

| Element | Best practice |
|---------|---------------|
| **Photo** | Clear face, professional |
| **Name** | Real name (or consistent handle) |
| **Bio** | What you do + what you tweet about |
| **Link** | Your most important URL |
| **Pinned tweet** | Your best/most representative content |
| **Header** | On-brand, not cluttered |

**Bio formula**:
```
[Role] at [Company/Project]. Building [what].
Tweeting about [topics]. [Credibility signal].
```

**Examples**:
```
Engineering @ Vercel. Building the web, one component at a time.
Tweeting about React, Next.js, and developer experience.

Indie hacker. Building saas.com ($10K MRR).
Writing about startups, coding, and building in public.
```

### Reply Strategy

| Reply to | Why |
|----------|-----|
| Big accounts in your niche | Visibility to their audience |
| People asking questions you can answer | Demonstrate expertise |
| Your followers | Build relationships |
| Controversial takes | Join the conversation (carefully) |

**Good reply patterns**:
- Add information they missed
- Share your experience
- Ask thoughtful follow-up
- Respectfully disagree with reasoning

---

## What to Avoid (The Cringe Zone)

### Content That Fails

| Type | Why it fails |
|------|--------------|
| Humble brags | "So humbled to be named Top 100..." |
| Engagement bait | "Like if you agree!" |
| Empty motivation | "Keep grinding!" |
| Obvious pitches | "Check out our product!" |
| Excessive hashtags | Looks spammy |
| Copied threads | People notice |
| AI-generated slop | Obvious and hollow |
| Thread guys formula | Overused patterns |

### Behaviors to Avoid

| Behavior | Why it hurts |
|----------|--------------|
| Buying followers | Fake engagement, obvious |
| Engagement pods | Manipulated, not real reach |
| Aggressive follow/unfollow | Looks desperate |
| DM pitching | Spam, burns bridges |
| Arguing publicly | Rarely looks good |
| Dunking on people | Short-term engagement, long-term reputation |
| Deleting unpopular takes | Own your opinions |

### The Authenticity Test

Before posting, ask:
1. Would I say this in person?
2. Is this genuinely useful or interesting?
3. Am I adding to the conversation?
4. Would I respect someone who posted this?

---

## Platform-Specific Do's and Don'ts

### Do's

1. **Do** share real experiences and learnings
2. **Do** use visuals (code screenshots, diagrams)
3. **Do** engage in first hour after posting
4. **Do** build in public authentically
5. **Do** reply thoughtfully to others
6. **Do** share credit and amplify others
7. **Do** be consistent in posting schedule
8. **Do** have opinions (respectfully)

### Don'ts

1. **Don't** be a reply guy with no original content
2. **Don't** use AI to generate generic content
3. **Don't** copy popular threads verbatim
4. **Don't** pitch in DMs uninvited
5. **Don't** use more than 2 hashtags
6. **Don't** post links without context
7. **Don't** be negative/dunking constantly
8. **Don't** automate engagement

---

## Content Calendar

### Weekly Template

| Day | Content type |
|-----|--------------|
| Monday | Thread (educational) |
| Tuesday | Quick tip or insight |
| Wednesday | Engage/reply heavy |
| Thursday | Share someone else's great content |
| Friday | Personal/behind the scenes |
| Weekend | Optional: light content |

### Content Mix

| Type | Percentage |
|------|------------|
| Educational/useful | 50% |
| Personal/journey | 25% |
| Opinions/takes | 15% |
| Promotional | 10% |

---

## Tools

| Tool | Use case |
|------|----------|
| **[Octolens](https://octolens.com)** | Monitor Twitter/X for mentions of your product, competitors, and relevant conversations. Get alerts when people discuss problems you solve. |
| **Carbon** | Beautiful code screenshots |
| **Typefully** | Thread drafting and scheduling |
| **Buffer/Hootsuite** | Scheduling |
| **TweetDeck** | Multi-column management |
| **Followerwonk** | Audience analysis |

---

## Thread Checklist

Before posting:

- [ ] Hook is compelling (no links, no hashtags)
- [ ] Each tweet is a complete thought
- [ ] Code is in screenshots, not text
- [ ] Thread is 5-12 tweets
- [ ] Summary/TL;DR included
- [ ] CTA at the end
- [ ] Scheduled for optimal time
- [ ] Ready to engage for first 2 hours

---

## Related Skills

- `developer-audience-context` — Know who you're talking to
- `dev-to-hashnode` — Turn threads into blog posts
- `linkedin-technical` — Cross-post for B2B reach
- `hacker-news-strategy` — Drive traffic from X to HN posts
