---
name: x-algo-post
description: Expert guidance on X's (Twitter's) open-sourced recommendation algorithm from the official xai-org/x-algorithm repository. Use this skill to create content that maximizes algorithmic amplification, analyze post performance, and develop viral content strategies. Every recommendation traces directly to specific algorithm behavior from the open-sourced codebase.
license: MIT
metadata:
  author: felixondesk
  version: "1.0.0"
---

<div align="center">

# X Algorithm Mastery

### 🚀 Create Viral X Content Using the Official Open-Sourced Algorithm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-blue.svg)](https://claude.ai/claude-code)
[![Source: xai-org/x-algorithm](https://img.shields.io/badge/Source-xai--org/x--algorithm-green.svg)](https://github.com/xai-org/x-algorithm)

**Built from the official open-sourced algorithm at github.com/xai-org/x-algorithm**

Every recommendation traces directly to X's open-sourced recommendation algorithm codebase.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Examples](#-examples)

</div>

---

## ✨ Features

- **🎯 Multi-Action Prediction** - 15 algorithm signals with actual impact weights
- **🔄 Network Bridge Framework** - Convert out-of-network viewers to followers
- **🧬 Author Identity Building** - Strengthen your topical embedding via two-tower retrieval
- **🔗 Compound Patterns** - Signal cascades > single-signal optimization
- **⚠️ Anti-Pattern Detection** - Proactive root cause analysis, not reactive fixes
- **📊 Official Documentation** - Based directly on https://github.com/xai-org/x-algorithm

---

## 📊 Why This Is Different

| Feature | Generic Advice | This Skill |
|---------|---------------|------------|
| **Source** | Opinions & guesses | **Official xai-org codebase** |
| **Signals** | Vague "engagement" | **15 documented predictions** |
| **Retrieval** | Not mentioned | **Two-tower model explained** |
| **Network Strategy** | Missing | **OON → in-network framework** |
| **Author Embedding** | Not addressed | **Candidate tower strategy** |
| **Pipeline** | Unknown | **7 documented stages** |

---

## 📥 Installation

### Automatic Installation

```bash
npx skills add https://github.com/felixondesk/agent-skills --skill x-algo-post
```

### Manual Installation

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/x-algo-post

# Copy the skill files
# SKILL.md, .openskills.json, README.md, LICENSE.txt
```

### Verify Installation

```bash
ls ~/.claude/skills/x-algo-post/
# Should show: SKILL.md, .openskills.json, README.md, LICENSE.txt
```

---

## 🎯 Usage

### Basic Draft Review

```
Review this X post:

I built a SaaS that failed in 3 months. Here's what I learned:
1. I focused on features, not problems
2. I talked to users, but didn't listen
3. I optimized for metrics that didn't matter

The biggest lesson? Speed of learning > everything else.
```

### Viral Potential Analysis

```
Will this go viral?

The #1 product at Amazon isn't what you think.

Not AWS. Not Prime. Not Alexa.

It's the internal document culture.

Every major decision starts with a 6-page narrative memo.

That's why they move fast—everyone actually understands the decision.
```

### Content Optimization

```
Optimize this for maximum reach:

"Check out my new thread about productivity tips!"
```

### Strategy Session

```
I'm building an audience in AI/ML. What's my content strategy?
```

---

## 🧠 How It Works

### The Official Algorithm Architecture

Based on the open-sourced code at https://github.com/xai-org/x-algorithm

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         FOR YOU FEED REQUEST                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                         HOME MIXER                               │
│                                    (Orchestration Layer)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   1. QUERY HYDRATION                                                            │
│      ┌─────────────────────────────────────────────────────────────────┐        │
│      │ User Action Sequence (engagement history) + User Features        │        │
│      └─────────────────────────────────────────────────────────────────┘        │
│                                          │                                        │
│                                          ▼                                        │
│   2. CANDIDATE SOURCES                                                        │
│      ┌──────────────────────────┐    ┌────────────────────────────────┐          │
│      │      THUNDER              │    │     PHOENIX RETRIEVAL          │          │
│      │  (In-Network Posts)       │    │   (Out-of-Network Posts)       │          │
│      │                          │    │                                │          │
│      │  Posts from accounts      │    │  Two-tower similarity search   │          │
│      │  you follow               │    │  across global corpus         │          │
│      │  Sub-millisecond lookup   │    │  User Tower + Candidate Tower  │          │
│      └──────────────────────────┘    └────────────────────────────────┘          │
│                                          │                                        │
│                                          ▼                                        │
│   3. CANDIDATE HYDRATION                                                       │
│      Fetch: post text, author info, media metadata, video duration              │
│                                          │                                        │
│                                          ▼                                        │
│   4. PRE-SCORING FILTERS                                                      │
│      Remove: duplicates, too old, self-posts, blocked/muted authors            │
│                                          │                                        │
│                                          ▼                                        │
│   5. SCORING                                                                   │
│      ┌────────────────┐   ┌────────────────┐   ┌──────────────┐                │
│      │ Phoenix Scorer │ → │ Weighted Scorer│ → │   Author     │                │
│      │ (Grok-based    │   │ (Combine       │   │   Diversity  │                │
│      │  Transformer)  │   │  predictions)  │   │   Scorer     │                │
│      │                │   │                │   │              │                │
│      │ P(15 actions)  │   │ Σ(weight×P)    │   │ Decay penalty│                │
│      └────────────────┘   └────────────────┘   └──────────────┘                │
│                                          │                                        │
│                                          ▼                                        │
│   6. SELECTION                                                                 │
│      Sort by final score, select top K candidates                               │
│                                          │                                        │
│                                          ▼                                        │
│   7. POST-SELECTION PROCESSING                                                │
│      Final validation: deleted/spam/violence/gore filters                      │
│                                          │                                        │
│                                          ▼                                        │
│   2. RANKED FEED                                                                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### The 15 Engagement Signals

From the official Phoenix Grok-based transformer model:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         POSITIVE SIGNALS (Increase Score)                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   P(favorite)       ──────────────────┐   User likes the post                  │
│   P(reply)         ──────────────────┐   User replies to the post              │
│   P(repost)        ──────────────────┐   User reposts without comment          │
│   P(quote)         ──────────────────┐   User reposts with comment             │
│   P(click)         ──────────────────┐   User clicks on the post               │
│   P(profile_click) ──────────────────┐   User clicks author's profile          │
│   P(video_view)    ──────────────────┐   User views video content              │
│   P(photo_expand)  ──────────────────┐   User expands photo to view            │
│   P(share)         ──────────────────┐   User shares the post                  │
│   P(dwell)         ──────────────────┐   User dwells (pauses) on post          │
│   P(follow_author) ──────────────────┘   User follows the post's author         │
│                                                                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                          NEGATIVE SIGNALS (Decrease Score)                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   P(not_interested) ───────────────────┐  User marks as not interested          │
│   P(block_author)   ───────────────────┐  User blocks the author                │
│   P(mute_author)    ───────────────────┐  User mutes the author                 │
│   P(report)         ───────────────────┘  User reports the post                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Scoring Formula

```
Final Score = Σ (weight_i × P(action_i))

Positive actions → Positive weights → Higher score → More reach
Negative actions → Negative weights → Lower score → Less reach
```

### Two-Tower Retrieval (How Out-of-Network Works)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        TWO-TOWER MODEL FOR OUT-OF-NETWORK                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   USER TOWER                           CANDIDATE TOWER                           │
│   ┌─────────────────────┐             ┌─────────────────────────────────┐       │
│   │                     │             │                                 │       │
│   │ • User Features     │             │ • All Posts in Corpus           │       │
│   │ • Engagement        │             │ • Pre-computed Embeddings        │       │
│   │   History (128)     │             │ • Processed through MLP         │       │
│   │ • Actions Taken     │             │                                 │       │
│   │                     │             │                                 │       │
│   │         ▼           │             │            ▼                    │       │
│   │    [User Embedding] │             │    [Candidate Embeddings]       │       │
│   │         │           │             │            │                    │       │
│   └─────────┼───────────┘             └────────────┼───────────────────┘       │
│             │                                      │                           │
│             └──────────────┬───────────────────────┘                           │
│                            │                                                   │
│                            ▼                                                   │
│                   DOT PRODUCT SIMILARITY                                        │
│                   (Finds most similar posts)                                   │
│                            │                                                   │
│                            ▼                                                   │
│                     TOP-K RETRIEVAL                                           │
│                 (Returns thousands of candidates)                              │
│                                                                                 │
│   STRATEGY: Consistent topical posting → Stronger author embedding            │
│            → Easier for relevant users to find you                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Author Diversity Penalty

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      AUTHOR DIVERSITY: POST ATTENUATION                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   Position 1: ████████████████████ 100% (full score)                          │
│   Position 2: ████████████░░░░░░░░░  ~60% (× decay_factor)                    │
│   Position 3: ██████░░░░░░░░░░░░░░░░  ~36% (× decay_factor²)                  │
│   Position 4: ████░░░░░░░░░░░░░░░░░░  ~22% (× decay_factor³)                  │
│                                                                                 │
│   STRATEGY: Every post should be substantial. Avoid frequent low-value posts.  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### In-Network vs Out-of-Network

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                  NETWORK STRATEGY: THE COMPOUNDING ADVANTAGE                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   OUT-OF-NETWORK (OON)                      IN-NETWORK                          │
│   ┌─────────────────────────┐               ┌─────────────────────────┐         │
│   │ • Two-tower similarity   │               │ • Always in candidate   │         │
│   │   gate                  │    ──────────▶ │   pool                  │         │
│   │ • May have score         │    Convert!   │ • No retrieval penalty  │         │
│   │   adjustment             │               │ • Maximum reach         │         │
│   └─────────────────────────┘               └─────────────────────────┘         │
│                                                                                 │
│   Every follower you convert from OON → In-Network is a PERMANENT upgrade      │
│                                                                                 │
│   STRATEGY: Create content that makes OON viewers WANT to follow you           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Response Format

The skill provides structured, algorithm-backed feedback:

```
VERDICT: [WILL GO VIRAL / GOOD START / NEEDS WORK / WILL FLOP]

SIGNAL ANALYSIS:
- Reply: [High/Medium/Low] - [reasoning]
- Repost/Quote: [High/Medium/Low] - [reasoning]
- Dwell: [High/Medium/Low] - [reasoning]
- Follow: [High/Medium/Low] - [reasoning]
- Profile Click: [High/Medium/Low] - [reasoning]

WEAKNESSES:
1. [Specific issue with signal impact]
2. [Specific issue with signal impact]

OPTIMIZED VERSION:
[Your improved version]

WHY THIS WORKS BETTER:
[Algorithm explanation]
```

---

## 🎨 Compound Patterns

### The Multi-Signal Thread

```
Hook (curiosity) → Claim (debate-able) → Evidence (specific) →
Extension (open question) → CTA (follow for more)

Signals: dwell, reply, quote, profile_click, follow_author
```

**Example:**
```
I reviewed 200 failed startups for Y Combinator.

Here's what most people get wrong:

1. They pivoted too late, not too early
2. The cofounder conflicts started before the idea
3. "Running out of money" was the symptom, not the cause
4. The winners had customers before they had product

The real lesson: Speed of learning beats everything else.

What did I miss?
```

### The Network Bridge

```
Quote high-authority post → Your unique angle →
Specific insight → "Follow me for [niche] insights"

Signals: quote, profile_click, follow_author
```

### The Value Share

```
Clear promise → Scannable content →
Save-worthy insight → Reference value

Signals: dwell, share, profile_click
```

---

## ⚠️ Anti-Patterns to Avoid

### Immediately Reject If:

| Anti-Pattern | Why It Fails | Algorithm Impact |
|--------------|--------------|------------------|
| Explicit CTA ("like/repost if") | Learned inauthenticity | `not_interested` ↑ |
| Generic AI vocabulary | Structural tell | Reduces all signals |
| Perfect 3-item lists | AI structural pattern | Reduces `dwell` |
| Every thought as thread | Diversity penalty | Score × decay^position |
| Posting >3x/day | Embedding dilution | Weaker retrieval |
| Reposting same content | Deduplication filter | Filtered out entirely |

### Red Flag Warnings:

- Punching down → `block_author`, `mute_author` ↑
- Rage bait → Short-term `reply` gain, long-term damage
- "Not just X, but Y" → AI structural tell
- Em dash overuse → AI structural pattern

---

## 🧪 Example Usage

### Input

```
Review this post:

"3 tips for better productivity:

1. Wake up early
2. Make a to-do list
3. Take breaks

What would you add?"
```

### Output

```
VERDICT: WILL FLOP

SIGNAL ANALYSIS:
- Reply: Low - Generic question, no debate-worthy claim
- Quote: Low - No unique angle worth sharing
- Dwell: Low - Common knowledge, no new insights
- Follow: Low - Doesn't demonstrate unique expertise
- Profile Click: Low - No credibility signals

WEAKNESSES:
1. Generic AI vocabulary ("tips", "better", "productivity")
2. Perfectly structured 3-item list (structural tell)
3. Every point is common knowledge (no unique value)
4. Weak CTA that adds nothing

OPTIMIZED VERSION:

I tracked my time for 30 days to find my productivity killer.

It wasn't social media. It wasn't meetings.

It was "productive procrastination"—doing easy tasks to avoid hard ones.

The fix that actually worked:
• One "frog" (hard task) before anything else
• Time-boxed deep work (90min max)
• Zero notifications during focus blocks

My deep work hours increased 3x.

What's your weirdest productivity discovery?

WHY THIS WORKS BETTER:
• Specific personal story (dwell signal)
• Non-obvious insight (reply/quote signals)
• Clear numbers (credibility → follow signal)
• Open question about "weird" (encourages unique replies)
• Contractions and natural voice (avoids AI detection)
```

---

## 📚 Technical Reference

### Key Components

- **Home Mixer**: Orchestration layer with 7-stage pipeline
- **Thunder**: In-memory in-network post store (sub-millisecond lookups)
- **Phoenix**: Two-tower retrieval + Grok-based transformer ranking
- **Candidate Pipeline**: Composable framework for recommendation systems

### Design Principles

1. **No Hand-Engineered Features** - The transformer learns everything from engagement sequences
2. **Candidate Isolation** - Posts don't attend to each other during scoring (consistent, cacheable scores)
3. **Hash-Based Embeddings** - Multiple hash functions for efficient embedding lookup
4. **Multi-Action Prediction** - 15 engagement types, not a single "relevance" score

### Official Source

This skill is based entirely on the open-sourced algorithm at:
**https://github.com/xai-org/x-algorithm**

---

## 🤝 Contributing

Contributions welcome! Please ensure all changes trace back to the official documentation.

---

## 📄 License

MIT License - see [LICENSE.txt](LICENSE.txt) for details.

---

## 🙏 Acknowledgments

- **xAI** for open-sourcing the recommendation algorithm
- **home-mixer**, **thunder**, and **phoenix** teams
- **Claude Code** team for the skills framework

---

<div align="center">

**Built with ❤️ from the official source code**

**Source: https://github.com/xai-org/x-algorithm**

[⬆ Back to Top](#-x-algorithm-mastery)

</div>
