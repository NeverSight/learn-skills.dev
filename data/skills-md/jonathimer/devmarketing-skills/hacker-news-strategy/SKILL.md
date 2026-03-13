---
name: hacker-news-strategy
description: When the user wants to promote on Hacker News, launch on HN, or understand what works on HN. Trigger phrases include "Hacker News," "HN post," "Show HN," "HN strategy," "getting upvotes on HN," "HN launch," or "why did my HN post die."
metadata:
  version: 1.0.0
---

# Hacker News Strategy

Hacker News is the most influential developer community — and the easiest to get wrong. This skill covers what actually works, what gets you flagged, and how to build authentic presence.

---

## Before You Start

1. Read `.agents/developer-audience-context.md` if it exists
2. Check if the product/content is genuinely interesting to HN's audience (hackers, founders, deep tech enthusiasts)
3. Be honest: HN users can smell marketing from miles away

---

## Understanding HN's Culture

### Who's Actually on Hacker News

| Segment | What they care about |
|---------|---------------------|
| Founders | Fundraising, growth tactics, startup war stories |
| Senior engineers | Deep technical content, architecture, systems |
| Tech leads | Engineering management, team scaling, processes |
| Indie hackers | Solo projects, bootstrapping, revenue |
| Researchers | AI/ML, distributed systems, PLT, security |

### What HN Values

- **Technical depth** over marketing polish
- **Genuine novelty** over incremental updates
- **Transparency** over corporate speak
- **Building in public** over stealth launches
- **Contrarian insights** over conventional wisdom

### What HN Hates

- Self-promotion disguised as content
- Clickbait headlines
- Corporate PR speak
- Engagement bait ("What do you think?")
- Anything that feels like an ad

---

## Post Types and When to Use Them

### Show HN

**Use when**: You built something and want feedback from the community.

| Requirement | Details |
|-------------|---------|
| Must be something people can try | Live demo, downloadable, or detailed walkthrough |
| Must be new | Not a repost or minor update |
| Creator must be available | Answer questions in comments for 2-3 hours |
| Title format | "Show HN: [Name] – [One-line description]" |

**Good Show HN examples**:
- "Show HN: I built a SQLite extension for vector search"
- "Show HN: Open source Heroku alternative written in Rust"
- "Show HN: Real-time collaborative code editor in the browser"

**Bad Show HN examples**:
- "Show HN: My startup just raised $5M" (not something to try)
- "Show HN: We updated our pricing page" (not interesting)
- "Show HN: Check out our new feature" (too vague)

### Launch HN

**Use when**: Major company launch or significant funding announcement.

| Guideline | Details |
|-----------|---------|
| Include technical details | What's under the hood, architectural decisions |
| Share the journey | How you got here, lessons learned |
| Be available | Founders should answer questions personally |
| Avoid PR speak | Write like a human, not a press release |

### Regular Submissions

**Use when**: Sharing interesting content (yours or others).

| What works | What doesn't |
|------------|--------------|
| Technical blog posts with depth | Listicles and "10 tips" posts |
| War stories with lessons | Company announcements |
| Deep dives into problems | Product updates |
| Original research or data | Repackaged content |
| Contrarian technical takes | Obvious or consensus opinions |

---

## Title Optimization

### Title Principles

| Do | Don't |
|----|-------|
| Be specific and concrete | Use vague buzzwords |
| State what it is, not why it's great | Include superlatives ("amazing," "best") |
| Use technical terms appropriately | Dumb down for broader appeal |
| Keep it factual | Use clickbait patterns |

### Title Transformations

| Before (bad) | After (good) |
|--------------|--------------|
| "The Best Way to Handle Errors in Node.js" | "Error handling patterns in Node.js production systems" |
| "We Made Deployments 10x Faster" | "How we reduced deployment time from 20min to 2min" |
| "Announcing Our Amazing New Feature" | "Show HN: [Feature] – [What it does]" |
| "You Won't Believe What We Found" | "[Specific finding] in [specific context]" |
| "Why Everyone Should Use TypeScript" | "TypeScript's type system caught 15% of our production bugs" |

### HN Moderators Edit Titles

Be aware: HN moderators (especially dang) will edit sensationalized titles to be more neutral. They'll also merge duplicate submissions and sometimes give worthy posts a second chance.

---

## Timing and Mechanics

### Best Posting Times

| Time (PT) | Why it works |
|-----------|--------------|
| 6-9 AM | Catches US East Coast morning, Europe afternoon |
| 10 AM - 12 PM | Peak US activity |
| Avoid: Weekends | Lower traffic, but less competition |

### The Algorithm

- Initial upvotes in first 1-2 hours matter most
- Comments boost ranking (engagement signal)
- Fast upvotes can trigger the "flamewar detector" penalty
- Posts from new accounts get extra scrutiny
- Controversial posts get rank penalties

### What Kills Posts

| Killer | Why |
|--------|-----|
| Voting rings | Multiple accounts/friends upvoting = detected and penalized |
| No early engagement | Post dies without initial momentum |
| Flagged by users | Multiple flags = post hidden |
| Duplicate content | Already posted = merged or killed |
| Self-promotion pattern | Multiple posts about same company |

---

## Comment Strategy

### If It's Your Post

| Timing | Action |
|--------|--------|
| Immediately | Post a top-level comment with context, backstory, or technical details |
| First 2 hours | Respond to every comment, especially critical ones |
| Throughout day | Keep checking back, answer follow-ups |

**Your first comment template**:
```
Hey HN, [your name] here, [role] at [company/project].

Quick backstory: [1-2 sentences on why you built this]

Technical context: [What's interesting under the hood]

Happy to answer any questions about [specific technical areas].
```

### Responding to Criticism

| Criticism type | Response strategy |
|----------------|-------------------|
| Valid technical concern | Acknowledge, explain reasoning, ask for suggestions |
| Misunderstanding | Clarify without being defensive |
| Trolling | Don't engage, or one brief factual response |
| Feature request | "Good idea, I'll look into it" or explain constraints |
| Competitive comparison | Be gracious, focus on your approach |

**Never do**:
- Get defensive or sarcastic
- Argue with critics
- Dismiss valid concerns
- Use corporate speak in responses

### Commenting on Others' Posts

Building karma through genuine participation:

| Do | Don't |
|----|-------|
| Share relevant technical experience | Promote your stuff in others' threads |
| Ask thoughtful questions | Leave generic praise |
| Add context from your expertise | Be contrarian just for attention |
| Correct misinformation politely | Start arguments |

---

## What Gets Flagged/Killed

### Automatic Red Flags

| Behavior | Consequence |
|----------|-------------|
| Asking for upvotes (anywhere) | Post killed, possible ban |
| Voting from same IP/network | Votes nullified, accounts penalized |
| Multiple accounts upvoting | Accounts banned |
| Submitting competitors negatively | Flagged as abuse |
| Astroturfing in comments | Account banned |

### Content That Gets Flagged

| Content type | Why it's flagged |
|--------------|------------------|
| Obvious marketing | Community polices this aggressively |
| Political hot takes | Off-topic for HN |
| Crypto/Web3 (often) | Community fatigue |
| Paywalled content | Frustrates readers |
| Low-effort content | Doesn't meet quality bar |

### Recovering from a Failed Post

1. **Wait at least 24 hours** before reposting
2. **Change the title** to be more specific/interesting
3. **Add more context** if it was unclear
4. **Email the mods** (hn@ycombinator.com) if you think it was unfairly killed
5. **Consider**: Maybe HN isn't the right audience for this

---

## Building Karma Authentically

### The Long Game

| Timeframe | Strategy |
|-----------|----------|
| Week 1-4 | Comment only. No submissions. Build karma through genuine engagement. |
| Month 2-3 | Submit interesting content (not your own). Show you're a contributor. |
| Month 3+ | Occasional submissions of your own work, mixed with other contributions. |

### Karma-Building Comments

High-karma comment patterns:
- **Add context**: "I worked on a similar system at [company], and we found..."
- **Share data**: "Our benchmarks showed X when we tested this approach"
- **Provide alternatives**: "Another option is Y, which works well when..."
- **Historical context**: "This is similar to how Z solved this in the 90s"

### What Karma Gets You

| Karma level | Benefit |
|-------------|---------|
| 30+ | Can downvote comments |
| 500+ | Posts get more initial trust |
| 1000+ | Strong signal of genuine community member |

---

## Platform-Specific Do's and Don'ts

### Do's

1. **Do** write like a human, not a company
2. **Do** share technical details generously
3. **Do** acknowledge limitations and trade-offs
4. **Do** respond to criticism gracefully
5. **Do** share your Show HN link with your team (for awareness, not coordinated upvoting)
6. **Do** participate in discussions even when not promoting
7. **Do** read HN daily to understand the culture

### Don'ts

1. **Don't** ask anyone to upvote (bannable offense)
2. **Don't** post the same thing repeatedly
3. **Don't** use clickbait titles
4. **Don't** be defensive in comments
5. **Don't** ignore criticism
6. **Don't** astroturf with fake accounts
7. **Don't** treat HN as a free marketing channel

---

## Tools

| Tool | Use case |
|------|----------|
| **[Octolens](https://octolens.com)** | Monitor HN for mentions of your product, competitors, and relevant keywords. Get alerts when discussions happen so you can participate authentically. |
| **HN Search (hn.algolia.com)** | Research past posts on your topic, see what worked |
| **HN Front Page Check** | Monitor if your post is on front page and at what rank |
| **HN user pages** | Research commenters before responding |

---

## Show HN Launch Checklist

Before posting:

- [ ] Live demo or downloadable available
- [ ] Landing page clearly explains what it does
- [ ] Pricing (if any) is transparent
- [ ] Creator available for 2-3 hours after posting
- [ ] First comment drafted with backstory/technical details
- [ ] Title follows "Show HN: [Name] – [Description]" format
- [ ] Not posted on HN in last 24 hours
- [ ] Account has some karma from genuine participation

---

## Related Skills

- `developer-audience-context` — Understand who you're reaching
- `reddit-engagement` — Similar community dynamics, different norms
- `dev-to-hashnode` — For longer-form content that links from HN
- `github-presence` — What HN users check when evaluating your project
