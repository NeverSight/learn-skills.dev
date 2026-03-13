---
name: youtube-devrel
description: When the user wants to create developer YouTube content, technical screencasts, or video tutorials. Trigger phrases include "YouTube," "developer video," "screencast," "video tutorial," "live coding," "YouTube for developers," "tech YouTube," or "YouTube thumbnails."
metadata:
  version: 1.0.0
---

# YouTube for Developer Relations

YouTube is the second-largest search engine and where developers go to learn. This skill covers tutorial structure, screen recording setup, live coding, shorts vs long-form, thumbnails, and SEO for technical content.

---

## Before You Start

1. Read `.agents/developer-audience-context.md` if it exists
2. Audit existing technical YouTube channels in your space
3. Understand: Developer YouTube is a long game — consistency > perfection

---

## Understanding Developer YouTube

### Who Watches Dev Content

| Audience | What they want | Video length |
|----------|----------------|--------------|
| Learning developers | Complete tutorials | 15-45 min |
| Working developers | Quick solutions | 5-15 min |
| Senior developers | Deep dives, architecture | 30-60 min |
| Decision makers | Demos, overviews | 3-10 min |
| Conference attendees | Recorded talks | 20-45 min |

### Content Types That Work

| Content type | View potential | Effort | Notes |
|--------------|----------------|--------|-------|
| Tutorial (build X) | Very high | High | Evergreen traffic |
| Problem/solution | High | Medium | Search-driven |
| Tool comparisons | High | Medium | High search volume |
| Live coding | Medium-high | Low | Engagement-focused |
| Project updates | Medium | Low | Community building |
| Conference talks | Medium | Low | Repurpose content |
| Shorts | High reach | Low | Discovery-focused |

### Successful Dev YouTube Channels

| Channel | Style | Why it works |
|---------|-------|--------------|
| Fireship | Fast, dense, opinionated | Respects viewer time |
| ThePrimeagen | Personality, live reactions | Authentic, entertaining |
| Traversy Media | Clear, beginner-friendly | Comprehensive tutorials |
| Hussein Nasser | Deep dives, whiteboard | Engineering depth |
| Ben Awad | Casual, real coding | Relatable, genuine |

---

## Tutorial Structure

### The Tutorial Template

```
0:00 - Hook (what you'll build/learn)
0:30 - Prerequisites & setup
2:00 - Concept explanation (why)
4:00 - Step 1: [First major step]
8:00 - Step 2: [Second major step]
...
XX:00 - Final result demo
XX:30 - Recap & next steps
XX:45 - CTA (subscribe, comment)
```

### Opening Hook (First 30 Seconds)

| Element | Purpose |
|---------|---------|
| Show the end result | Prove it's worth watching |
| State what they'll learn | Set expectations |
| Mention prerequisites | Qualify viewers |
| Estimated time | Respect their time |

**Example hook**:
```
"By the end of this video, you'll have a working CLI tool
that can scrape any website and export to JSON. We'll use
Node.js and Cheerio — you just need basic JavaScript
knowledge. This should take about 20 minutes. Let's go."
```

### Pacing Guidelines

| Video length | Segment length | Notes |
|--------------|----------------|-------|
| 5-10 min | 1-2 min segments | Fast, focused |
| 15-30 min | 3-5 min segments | Standard tutorial |
| 30-60 min | 5-10 min segments | Deep dive |

### Common Tutorial Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Too much setup | Viewers drop off | Skip to interesting parts |
| Not showing end result | No motivation | Show finished product first |
| Going too fast | Confusion | Pause on key steps |
| Going too slow | Boredom | Edit out pauses, typos |
| No timestamps | Poor navigation | Add chapters |
| Walls of code | Overwhelming | Build incrementally |

---

## Screen Recording Setup

### Essential Equipment

| Equipment | Budget option | Better option |
|-----------|---------------|---------------|
| **Microphone** | Blue Snowball ($50) | Shure SM7B ($400) |
| **Screen recording** | OBS (free) | ScreenFlow ($170) |
| **Webcam** | Built-in | Logitech C920 ($80) |
| **Lighting** | Window light | Ring light ($30) |
| **Editor** | DaVinci Resolve (free) | Premiere Pro ($22/mo) |

### Audio is More Important Than Video

| Priority | Why |
|----------|-----|
| 1. Clear audio | Bad audio = immediate click away |
| 2. Readable code | Text must be crisp |
| 3. Good lighting | For facecam sections |
| 4. High resolution | 1080p minimum |

### Screen Recording Best Practices

| Setting | Recommendation |
|---------|----------------|
| Resolution | 1920x1080 or 2560x1440 |
| Font size | 18-24pt in editor |
| Theme | Dark theme (easier on eyes) |
| Zoom | Use IDE zoom for key sections |
| Notifications | Disable all |
| Browser | Use clean profile, no bookmarks bar |

### Recording Workflow

1. **Script key points** (don't read verbatim)
2. **Test audio levels** before recording
3. **Record in segments** (easier editing)
4. **Leave pauses** for edits (clap or say "edit")
5. **Show face** at transitions (builds connection)
6. **Record extra b-roll** (diagrams, browser, terminal)

---

## Live Coding Content

### Live Coding Formats

| Format | Length | Platform |
|--------|--------|----------|
| Twitch stream → YouTube | 1-4 hours | Both |
| YouTube Live | 30-90 min | YouTube |
| Pre-recorded "live" | 20-45 min | YouTube |

### Live Coding Best Practices

| Do | Don't |
|----|-------|
| Explain your thinking | Code silently |
| Embrace mistakes | Pretend you know everything |
| Read chat | Ignore audience |
| Have a goal | Meander aimlessly |
| Take breaks | Marathon without pause |
| Use timestamps post-stream | Leave as giant blob |

### Common Live Coding Content

| Content | Example |
|---------|---------|
| Project from scratch | "Building a REST API live" |
| Code review | "Reviewing subscriber PRs" |
| Problem solving | "LeetCode medium problems" |
| Exploring new tech | "Learning Rust in public" |
| Bug hunting | "Fixing production issues live" |

---

## Shorts vs Long-Form

### YouTube Shorts (< 60 seconds)

| Aspect | Best practice |
|--------|---------------|
| **Hook** | Immediate (first 1-2 seconds) |
| **Length** | 30-45 seconds optimal |
| **Aspect ratio** | 9:16 (vertical) |
| **Content** | One tip, one concept |
| **Text** | Big, on-screen captions |
| **Audio** | Clear voiceover |

### Shorts Content Ideas

| Type | Example |
|------|---------|
| Quick tips | "One command to speed up Git" |
| Syntax shortcuts | "JavaScript spread operator in 30s" |
| Tool demos | "VS Code extension you need" |
| Code transformations | "Before/after refactoring" |
| Hot takes | "Stop using X, here's why" |

### Shorts Strategy

| Goal | Approach |
|------|----------|
| Grow subscribers | Post 3-5 shorts/week |
| Drive to long-form | Tease tutorials in shorts |
| Algorithm favor | Consistent posting schedule |
| Repurpose content | Cut from long videos |

### Long-Form vs Shorts

| Long-form | Shorts |
|-----------|--------|
| Search traffic | Discovery traffic |
| Watch time revenue | Low revenue |
| Depth | Breadth |
| Subscribers who stay | Subscribers who scroll |
| Comments, community | Less engagement |

---

## Thumbnails for Developers

### Thumbnail Principles

| Element | Guideline |
|---------|-----------|
| **Text** | 3-5 words max |
| **Face** | Expression adds emotion |
| **Logo/icon** | Tech being discussed |
| **Colors** | High contrast, brand consistent |
| **Composition** | Rule of thirds |

### Thumbnail Patterns That Work

| Pattern | Example |
|---------|---------|
| Face + tech logo + emotion | [Surprised face] + [React logo] + "It changed everything" |
| Before/after | [Broken code] → [Working code] |
| Big text + icon | "STOP" + [X mark] |
| Comparison | [Tech A] vs [Tech B] |
| Result preview | [Screenshot of finished app] |

### Thumbnail Creation

| Tool | Best for |
|------|----------|
| Canva | Quick, easy templates |
| Figma | Design control |
| Photoshop | Advanced editing |
| Thumbnail templates | Consistency |

### A/B Test Thumbnails

YouTube allows thumbnail testing:
1. Upload video with thumbnail A
2. After 48 hours, change to B
3. Compare CTR in analytics
4. Keep winner

---

## YouTube SEO

### Where Keywords Matter

| Location | Impact | Best practice |
|----------|--------|---------------|
| **Title** | Highest | Primary keyword early |
| **Description** | High | First 2 sentences keyword-rich |
| **Tags** | Low | Include, but don't overthink |
| **Captions/transcript** | Medium | Auto-generated + edit |
| **Filename** | Low | Include keyword anyway |

### Title Formulas

| Formula | Example |
|---------|---------|
| [Tech] Tutorial: [What you'll build] | "React Tutorial: Build a Todo App from Scratch" |
| How to [Task] with [Tech] | "How to Deploy to AWS with Docker" |
| [Tech A] vs [Tech B]: Which is Better? | "Next.js vs Remix: Which Should You Learn?" |
| [Number] [Topic] Tips in [Time] | "10 VS Code Tips in 10 Minutes" |
| Why I [Action] [Tech] | "Why I Switched from React to Svelte" |

### Description Template

```
[First 150 chars: Compelling summary with main keyword]

In this video, I'll show you [what they'll learn].

Timestamps:
0:00 - Introduction
2:00 - [Section 1]
[...]

Resources mentioned:
- [Link 1]
- [Link 2]

Links:
🔗 My website: [URL]
🔗 GitHub repo: [URL]
🔗 Discord: [URL]

#[keyword1] #[keyword2] #[keyword3]
```

### Research Keywords

| Tool | Use for |
|------|---------|
| YouTube search autocomplete | Real search queries |
| TubeBuddy/VidIQ | Search volume, competition |
| Google Trends | Trending topics |
| Competitor titles | What's working |

---

## Platform-Specific Do's and Don'ts

### Do's

1. **Do** show the end result first
2. **Do** add chapters/timestamps
3. **Do** use clear, readable code fonts
4. **Do** invest in audio quality
5. **Do** maintain consistent posting schedule
6. **Do** engage with comments
7. **Do** repurpose to shorts
8. **Do** create custom thumbnails

### Don'ts

1. **Don't** skip the hook
2. **Don't** use tiny fonts
3. **Don't** record with room echo
4. **Don't** forget CTAs
5. **Don't** post inconsistently
6. **Don't** ignore SEO basics
7. **Don't** make clickbait thumbnails (trust erosion)
8. **Don't** perfectionism (ship it)

---

## Content Calendar

### Weekly Schedule Example

| Day | Content |
|-----|---------|
| Monday | Shorts (tip/trick) |
| Wednesday | Long-form tutorial |
| Friday | Shorts (from Wednesday video) |
| Weekend | Edit next week's content |

### Monthly Planning

| Week | Focus |
|------|-------|
| Week 1 | Tutorial (main content) |
| Week 2 | Live stream or Q&A |
| Week 3 | Tutorial (main content) |
| Week 4 | Comparison or review |

---

## Tools

| Tool | Use case |
|------|----------|
| **[Octolens](https://octolens.com)** | Monitor YouTube and social for mentions of your tech topics, competitors, and find what developers are asking about. |
| **OBS Studio** | Free screen recording and streaming |
| **ScreenFlow** | Mac recording and editing |
| **DaVinci Resolve** | Free professional editing |
| **Descript** | Edit video by editing transcript |
| **Canva** | Thumbnail creation |
| **TubeBuddy** | YouTube SEO tools |
| **Riverside.fm** | Remote recording |

---

## Getting Started Checklist

First video:

- [ ] Script/outline key points
- [ ] Test audio and screen recording
- [ ] Record in 1080p minimum
- [ ] Font size 18pt+ in editor
- [ ] Show end result in first 30 seconds
- [ ] Add timestamps/chapters
- [ ] Create custom thumbnail
- [ ] Write SEO-optimized title/description
- [ ] Include CTA at end
- [ ] Respond to comments within 24 hours

---

## Related Skills

- `developer-audience-context` — Know who's watching
- `dev-to-hashnode` — Turn videos into blog posts
- `linkedin-technical` — Share videos on LinkedIn
- `x-devs` — Promote videos on Twitter
- `github-presence` — Link repos in descriptions
