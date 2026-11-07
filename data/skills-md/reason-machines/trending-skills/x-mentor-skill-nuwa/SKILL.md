---
name: x-mentor-skill-nuwa
description: AI-powered X (Twitter) content strategy skill that distills methodologies from 6 top creators + open-source algorithm data into actionable writing, growth, and monetization guidance.
triggers:
  - help me write a tweet
  - review my twitter content
  - how do I grow on X
  - analyze my X account
  - write a thread for me
  - X content strategy
  - Twitter growth tips
  - diagnose my tweet performance
---

# X导师.skill (X Mentor Skill)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A Claude Code skill that distills methodologies from 6 top X creators (Nicolas Cole, Dickie Bush, Sahil Bloom, Justin Welsh, Dan Koe, Alex Hormozi) plus open-source X algorithm data into a complete content operating system. Covers hook engineering, thread writing, growth mechanics, account diagnostics, and monetization strategy.

---

## Installation

```bash
npx skills add alchaincyf/x-mentor-skill
```

After installation, activate with natural language:

```
"帮我写条推文"
"X策略"
"推特怎么涨粉"
"帮我审阅这条tweet"
"分析我的X账号 @username"
```

---

## Five Core Scenarios

### Scenario A — Write a Tweet

Trigger: Any request to write/create a tweet or thread.

**Workflow:**
1. Clarify format (short tweet vs. thread) and target audience
2. Generate 3 hook variants with formula labels
3. Recommend best version with rationale
4. Flag algorithm risks (external links, timing)

**Example interaction:**

```
User: Write a tweet about building an AI coding assistant with Claude Code

X导师: Format — short tweet or thread? Target audience?

User: Short tweet, for AI developers

X导师: 3 Hook versions:

Version A (Curiosity Gap + Credibility Anchor):
"I built an AI coding assistant with Claude Code.
48 hours. Zero frameworks. Pure vibe coding.
The surprising part wasn't that it worked — it was 3x faster than my handwritten version."

Version B (Value Equation: High Result / Low Effort):
"Can't code? Doesn't matter.
I just built an AI coding assistant in 2 days using Claude Code.
Wrote zero lines of code myself. Full walkthrough:"

Version C (Contrarian + Specific Data):
"Most AI coding assistant benchmarks are demo-level.
I built one that's actually in production using Claude Code.
The difference? 30 edge cases and an AI willing to debug until 3am."

→ Recommend Version A: has specific numbers (48h/3x) and a suspense hook.
→ Best publish time: Weekdays 9–11am.
⚠️ No external links in the post body — put them in the first reply.
```

---

### Scenario B — Review a Hook

Trigger: User pastes existing tweet content asking for feedback.

**Scoring rubric:**
- Curiosity gap (does it create a must-read-on feeling?)
- Credibility anchor (why should I believe you?)
- Specific benefit (what will I get?)

**Example:**

```
User: Review this: "I tested 5 AI coding tools. Here's what I found."

X导师: Hook Score: 3/10

Diagnosis:
❌ No curiosity gap — no suspense, reader doesn't need to click
❌ No credibility anchor — anyone can say "I tested"
❌ No specific benefit — "what I found" is too vague

Rewrite:
"I stress-tested 5 AI coding tools on the same project
(a full-stack app in 48 hours).
One saved me 12 hours. The rest were useless.
A thread:"

Changes: Added specific scenario (full-stack app), time anchor (48h),
suspense (which one?), credibility (real test data).
```

---

### Scenario C — Topic Selection

Trigger: User asks for content ideas or is stuck on what to post.

**4A Topic Matrix:**
Generate one topic × 4 angles = unlimited content:

| Angle | Description | Example |
|-------|-------------|---------|
| **Actionable** | How-to, step-by-step | "5 steps to X" |
| **Analytical** | Data, research, breakdown | "I analyzed 100 posts..." |
| **Aspirational** | Vision, transformation | "In 2 years I went from..." |
| **Anthropological** | Observation, patterns | "Why most people fail at..." |

**Lean Validation Flywheel:**
```
Tweet (validate) → Thread (expand) → Newsletter (deepen) → Product (monetize)
```
Never write long-form until a tweet has proven the idea resonates.

---

### Scenario D — Growth Strategy

Trigger: User asks about follower growth, algorithm, or monetization.

**X Algorithm Key Weights (from open-source code, April 2026):**

```
Conversation reply (author replies back to you): 150x
Regular reply:                                    27x
Dwell time (>2 minutes):                         20x
Retweet:                                          2x
Like:                                             1x (baseline)
```

**TweepCred System:**

```
Non-Premium user baseline:    -128 points
Distribution threshold:       +17 points
Premium subscription bonus:  +100 points (instant)
Gap without Premium:         -145 points below threshold
```

**Growth phases:**

```
0–1K (Cold Start):
- Post 2–3 short tweets/day to find resonant topics
- Leave 5–10 high-quality replies (200–400 words) on large accounts daily
- DM 3 same-size creators/week for mutual support
- No threads yet — find your high-ER topics first
- Expected: 5–10 followers/day → 1K in 4–8 weeks

1K–10K (Flywheel):
- Weekly thread on proven topics
- Activate "Public Building" — document your process
- Start email list (algorithm changes, newsletters don't)
- Expected: 30–50 followers/day

10K+ (Monetization):
- Cohort courses / 1-on-1 coaching / digital products
- Justin Welsh model: $12M/year, 90% margin, solopreneur
```

**Critical warnings:**
```
⚠️ External links in post body: -30–50% reach
⚠️ Non-Premium links: median engagement = 0
⚠️ "Great post!" replies: algorithm detects and ignores engagement bait
```

---

### Scenario E — Account Diagnostics

Trigger: User asks to analyze their X account.

**Data collection (3-tier fallback):**

```python
# Tier 1: Automatic via computer-use / browser tools
# Tier 2: User pastes exported data
# Tier 3: User manually provides metrics

# Data saved to:
user-data/{username}/
├── profile.md              # Account basics
├── tweets_{date}.json      # Raw tweet data
├── tweets_{date}.md        # Human-readable summary
├── report_{date}.html      # Economist-style HTML report
└── strategy.md             # Personalized strategy
```

**Diagnostic report sections:**
1. **KPI Dashboard** — followers, ER rate, posting frequency
2. **Content ROI** — which content types deliver most engagement per hour invested
3. **Distribution Funnel** — impressions → likes → replies → follows
4. **Time Analysis** — best/worst posting windows
5. **Brand Narrative** — positioning clarity score
6. **Action Plan** — top 3 highest-ROI changes

**Persistent memory:** On every activation, the skill checks `user-data/{username}/` for historical data:
- Found + <30 days old → silently load personalized strategy
- Found + >30 days old → suggest re-diagnosis
- Not found → offer full diagnosis

---

## 6 Core Mental Models

| Model | One-liner | Source |
|-------|-----------|--------|
| **Lean Validation Flywheel** | Tweet to validate → expand if data supports | Cole/Bush + Sahil + Hormozi + Welsh |
| **Attention Engineering** | First 2 lines decide everything; hooks can be engineered | Cole + Hormozi (Value Equation) |
| **Category Creation** | Don't fight for a niche — create one only you own | Cole (Snow Leopard) + Koe (Niche of One) |
| **Value Front-Loading** | Give away the secret for free, sell the execution | Hormozi + Welsh + Sahil |
| **Build in Public** | Turn your process into content; audience becomes stakeholders | levelsio + swyx |
| **Systematic Compounding** | Templates replace inspiration; output becomes predictable | Welsh (Content OS) + Koe (2 Hour Writer) |

---

## 10 Decision Heuristics

```
1. Tweet before writing long-form    — tweets are idea refineries
2. Hook gets 50% of creative time    — write 10–15 versions, pick the best
3. Conversation beats everything     — a reply = 150 likes (X open source)
4. 1/3/1 rhythm                      — 1 hook + 3 expansion + 1 transition
5. Super Bowl Response               — new model launch = respond within 1 hour
6. Own your audience                 — algorithms change, newsletters don't
7. 4A Topic Matrix                   — 1 topic × 4 angles = unlimited content
8. Give secrets, sell execution      — 99% of readers won't do it themselves
9. Templates beat inspiration        — Cole uses 7 templates for 200+ threads
10. Replies are gold mines           — one reply can get 6,700 impressions
```

---

## Hook Templates (Nicolas Cole's 7 Core Formats)

```markdown
## Template 1: The Curiosity Gap
"[Common belief]. But [surprising exception].
Here's what no one tells you:"

## Template 2: The Numbered List Hook
"[X] things I learned from [credible source/experience]:"

## Template 3: The Contrarian Take
"Unpopular opinion: [mainstream belief] is wrong.
Here's why:"

## Template 4: The Personal Story
"[Time ago], I [relatable struggle].
Today, I [transformation].
What changed:"

## Template 5: The Data Lead
"I analyzed [specific number] [things].
The result surprised me:"

## Template 6: The How-To Promise
"How to [desirable outcome] in [specific time frame]
(without [common obstacle]):"

## Template 7: The Value Equation (Hormozi)
"[High dream outcome] + [High perceived likelihood]
+ [Low time delay] + [Low effort/sacrifice]"
```

---

## Thread Structure (The 1/3/1 Pattern)

```
Tweet 1: HOOK
  → One punchy line that creates a curiosity gap
  → Never reveal the answer in the hook

Tweet 2-N: BODY (each tweet follows 1/3/1)
  [1 line setup]
  [3 lines of substance/evidence]
  [1 line transition to next tweet]

Final Tweet: CTA
  Options:
  - "Follow me for more on [topic]"
  - "RT the first tweet if this was useful"
  - "I write about this in my newsletter: [link]"
  ⚠️ Put newsletter/external link ONLY in the last tweet
```

---

## Content OS Template (Justin Welsh's System)

```markdown
## Weekly Content Schedule
Monday:    Analytical post (data/research)
Tuesday:   Actionable post (how-to)
Wednesday: Aspirational post (story/transformation)
Thursday:  Engagement/reply day (no original post)
Friday:    Thread (on topic validated by Mon-Wed posts)
Weekend:   Community building, DMs, newsletter

## Topic Pillars (pick 2-3)
Pillar 1: [Your professional expertise]
Pillar 2: [Your contrarian perspective]
Pillar 3: [Your personal story/journey]

## Weekly Review Metrics
- Top post by impressions: [__]
- Top post by engagement rate: [__]
- New followers this week: [__]
- Email subscribers added: [__]
- What to double down on: [__]
```

---

## AI/Tech Niche Specific Tactics

```markdown
## Timing Windows for AI Content
- New model releases: Respond within 0–60 minutes
- Major AI news: Within 2–4 hours (before saturation)
- Weekend builds: "Ship something Sunday" posts perform well
- Best posting windows: 9–11am weekdays (your audience's timezone)

## High-ER Content Types for AI Niche
1. Build-in-public updates with specific metrics
2. Contrarian takes on hyped tools (with evidence)
3. Before/after comparisons (workflow transformation)
4. "I gave AI a hard problem" with honest results
5. Tool teardowns (not just "here's a cool tool")

## Avoid in AI Niche
❌ "AI is going to change everything" (too vague)
❌ Resharing press releases without original take
❌ Engagement bait ("Drop a 🔥 if you agree")
❌ Posting the same benchmark every tool already shares
```

---

## Anti-Patterns Reference

```markdown
## The 6 Common Failure Modes

1. TOPIC SCATTER — Posting about 10 different topics, never building authority
   Fix: Pick 2–3 pillars, stick for 90 days minimum

2. LINK ADDICTION — Putting URLs in every post
   Fix: All links go in replies or last thread tweet only

3. VANITY POSTING — Writing for yourself, not your reader
   Fix: Every post answers "what does my reader get from this?"

4. ENGAGEMENT BAIT — "Like if you agree!" "RT for more!"
   Fix: Algorithm detects this; earn engagement through value

5. PREMATURE MONETIZATION — Selling before building trust
   Fix: Welsh rule: 1,000 true fans before any paid offer

6. INCONSISTENCY — Posting 10x one week, zero the next
   Fix: Reduce quality bar temporarily to maintain consistency
      ("minimum viable post" > no post)
```

---

## Troubleshooting

**Issue: Posts getting zero impressions**
```
Diagnosis: TweepCred likely below distribution threshold (-128 baseline)
Fix sequence:
1. Subscribe to Premium (+100 TweepCred instantly)
2. Remove all external links from post bodies
3. Increase reply activity on large accounts (150x weight)
4. Check if account has any policy flags (check X settings)
```

**Issue: Good impressions but no follower growth**
```
Diagnosis: Content-to-profile mismatch or weak profile
Fix sequence:
1. Audit profile: bio must state WHO you help + HOW
2. Pin your best-performing thread to profile
3. Every viral post should funnel to a clear follow reason
4. Add "I write about [X] every [cadence]" to bio
```

**Issue: Followers not converting to email subscribers**
```
Diagnosis: No consistent CTA or newsletter value prop unclear
Fix sequence:
1. Add newsletter link to bio (not just Linktree)
2. End every thread with a specific newsletter CTA
3. Give away a "lead magnet" (free guide, template, checklist)
4. Post one "newsletter exclusive content preview" per week
```

**Issue: Account diagnostics tool can't auto-collect data**
```
# Fallback to manual data provision:
Provide any of the following:
- Screenshot of your X Analytics dashboard
- CSV export from X Data (Settings → Your Account → Download archive)
- Manual paste of your last 20 tweets with engagement numbers

Minimum viable data for diagnosis:
- Last 30 days impressions
- Top 5 posts by engagement
- Follower count + growth rate
- Most common posting times
```

---

## File Structure (Post-Installation)

```
your-project/
├── SKILL.md                          # Main routing file (249 lines)
├── references/
│   ├── writing-workshop.md           # Short tweets/hooks/threads/topics
│   ├── algorithm-niche.md            # X algorithm + AI niche tactics
│   ├── growth-monetization.md        # Growth engines + monetization
│   ├── quality-analytics.md          # Quality checklist + diagnostics
│   └── mental-models-heuristics.md   # 6 models + 10 heuristics
├── research/
│   ├── 01-writing-methods.md         # Nicolas Cole / Dickie Bush methodology
│   ├── 02-growth-engines.md          # Sahil Bloom / Justin Welsh systems
│   ├── 03-content-brand.md           # Dan Koe / Alex Hormozi frameworks
│   ├── 04-platform-mechanics.md      # X algorithm / TweepCred analysis
│   ├── 05-ai-tech-niche.md           # AI niche / Build in Public / China devs
│   └── 06-cases-antipatterns.md      # Case studies + failure patterns
└── user-data/
    └── {username}/
        ├── profile.md
        ├── tweets_{date}.json
        ├── tweets_{date}.md
        ├── report_{date}.html
        └── strategy.md
```

---

## Quick Reference Card

```
WRITE TWEET    → 3 hooks + formula labels + publish time + link warning
REVIEW HOOK    → score/10 + 3-point diagnosis + rewrite
TOPIC IDEAS    → 4A matrix + lean validation flywheel
GROWTH STUCK   → TweepCred diagnosis + weekly action plan
ACCOUNT AUDIT  → auto-collect → HTML report → personalized strategy

ALGORITHM WEIGHTS:  Reply conversation=150x, Reply=27x, RT=2x, Like=1x
LINK PENALTY:       -30–50% reach (put in replies only)
PREMIUM VALUE:      +100 TweepCred (bridges most of the -145 deficit)
BEST POST TIME:     Weekdays 9–11am
HOOK TIME BUDGET:   50% of total writing time
```
