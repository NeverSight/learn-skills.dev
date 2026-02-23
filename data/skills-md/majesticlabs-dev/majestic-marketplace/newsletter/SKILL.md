---
name: newsletter
description: Create engaging newsletter editions with proven structures, subject lines, and content formats. Supports curator, educator, and thought leader archetypes for ongoing audience communication.
triggers:
  - newsletter
  - write newsletter
  - newsletter edition
  - weekly newsletter
  - email newsletter
allowed-tools: Read Write Edit Grep Glob WebSearch WebFetch AskUserQuestion
disable-model-invocation: true
---

# Newsletter Architect

Create compelling newsletter editions that readers actually open, read, and forward.

## Newsletter vs Email Nurture

| Newsletter (this skill) | Email Nurture |
|------------------------|---------------|
| Ongoing communication | One-time sequences |
| Regular cadence (weekly/monthly) | Triggered by action |
| Curated + original content | Focused drip campaign |
| Builds relationship over time | Moves toward conversion |
| Subscribers expect it | Automated based on behavior |

## Conversation Starter

Use `AskUserQuestion` to gather context:

"I'll help you create a newsletter edition that readers will love.

**Quick info needed:**

1. **Newsletter name/topic**: What's your newsletter about?
2. **Archetype** (pick one):
   - **Curator** - Curate the best links/resources (like Morning Brew)
   - **Educator** - Teach one thing deeply (like James Clear)
   - **Thought Leader** - Share opinions/insights (like Lenny's Newsletter)
   - **Hybrid** - Mix of above
3. **This edition's focus**: What's the main topic/theme?
4. **Cadence**: Weekly, bi-weekly, or monthly?
5. **Tone**: Casual, professional, witty, etc.
6. **Any specific content to include?** (links, announcements, stories)

I'll draft your edition with subject line options."

## Newsletter Archetypes

### 1. The Curator

**Best for:** Busy professionals who want filtered content

**Structure:**
```
SUBJECT: [Number] + [Benefit] + [Timeframe]
"7 links that'll make you smarter this week"

---

[Personal 2-3 sentence intro - what you're thinking about]

---

## 🔗 This Week's Picks

### 1. [Link Title]
[1-2 sentence summary + why it matters]
→ [Link]

### 2. [Link Title]
[1-2 sentence summary + why it matters]
→ [Link]

(5-7 links total)

---

## 💡 One Thing I'm Thinking About
[1 paragraph personal insight]

---

## 🛠️ Tool/Resource of the Week
[Name]: [What it does + why you like it]
→ [Link]

---

[Sign-off + CTA]
```

**Subject Line Formulas:**
- `[Number] things you missed this week`
- `The [topic] links worth your time`
- `Your [day] reading list is here`
- `[Number] [topic] finds (+ one surprise)`

### 2. The Educator

**Best for:** Building authority, teaching skills

**Structure:**
```
SUBJECT: How to [Outcome] + [Constraint/Twist]
"How to write emails that get replies (even from busy executives)"

---

[Hook - relatable problem or surprising fact]

---

## The Problem

[2-3 paragraphs setting up the challenge]

---

## The Solution

### Step 1: [Action]
[Explanation + example]

### Step 2: [Action]
[Explanation + example]

### Step 3: [Action]
[Explanation + example]

---

## Real Example

[Before/after or case study]

---

## Your Action Item

[One specific thing to do this week]

---

[Sign-off + what's coming next week]
```

**Subject Line Formulas:**
- `How to [outcome] (without [common sacrifice])`
- `The [topic] mistake costing you [loss]`
- `I [did thing]. Here's what happened.`
- `[Number] [topic] lessons from [source]`

### 3. The Thought Leader

**Best for:** Building personal brand, sharing opinions

**Structure:**
```
SUBJECT: [Contrarian take] or [Provocative question]
"Nobody talks about this side of [topic]"

---

[Personal story or observation that sparked this edition]

---

## Here's What I've Been Thinking

[3-5 paragraphs of your perspective]

- [Key point 1]
- [Key point 2]
- [Key point 3]

---

## Why This Matters

[Connect to reader's life/work]

---

## The Uncomfortable Truth

[Your bold take that others won't say]

---

## What I'd Do About It

[Actionable perspective]

---

[Question for readers + sign-off]
```

**Subject Line Formulas:**
- `The thing nobody tells you about [topic]`
- `I was wrong about [topic]`
- `Unpopular opinion: [take]`
- `Why I stopped [common practice]`

### 4. The Hybrid

**Best for:** Variety, testing what resonates

**Structure:**
```
SUBJECT: [Main value] + [Curiosity element]

---

## 👋 Hey [Name/Friend],

[2-3 sentence personal intro]

---

## 📝 Main Story: [Title]

[The meat of this edition - 300-500 words]

---

## 🔗 Links Worth Clicking

1. **[Title]** - [One-liner] → [Link]
2. **[Title]** - [One-liner] → [Link]
3. **[Title]** - [One-liner] → [Link]

---

## 💬 From Last Week

[Reader reply/question + your response]

---

## 🎯 This Week's Challenge

[One actionable thing]

---

[Personal sign-off]

P.S. [Teaser for next week or bonus link]
```

## Section Templates

**Intro styles:** Story open (personal anecdote), observation (pattern you noticed), confession (honest admission), direct (topic + no fluff).

**Sign-off styles:** Personal (where you're headed), forward ask (share request), reply prompt (specific question), teaser (next week preview).

## Subject Line Toolkit

### Formulas That Work

| Type | Formula | Example |
|------|---------|---------|
| Curiosity | `The [thing] no one talks about` | The hiring mistake no one talks about |
| Specificity | `[Number] ways to [outcome]` | 5 ways to close deals faster |
| Personal | `I [action]. Here's what happened.` | I quit meetings. Here's what happened. |
| Question | `What if [unexpected possibility]?` | What if your best employee is wrong? |
| Contrast | `[Common belief] vs [reality]` | What they teach vs what works |
| FOMO | `[Number] people already know this` | 10,000 people already know this |
| Direct | `[Benefit] inside` | Your productivity playbook inside |

**Power words:** "Actually" (contrarian), "Finally" (solution), "Warning" (urgency), "Secretly" (insider), "Quick" (low commitment). **Avoid:** "Newsletter", "Update", "Monthly/Weekly", "Don't miss", "Exciting news".

## Content Sourcing

- **Curators:** Twitter/X lists, HN, Reddit, Slack/Discord communities, Google Alerts. Curation test: "Would I send this to a smart friend?"
- **Educators:** Reader questions, your mistakes, processes that work, book insights, sparked conversations
- **Thought Leaders:** Disagreements with common practice, beginner mistakes, changed minds, hindsight lessons

## Output Format

```markdown
# NEWSLETTER EDITION: [Edition # or Date]

## Subject Line Options
1. **[Primary - best performer predicted]**
2. [Alternative A]
3. [Alternative B]

**Preview text:** [40-90 chars that show after subject]

---

## Newsletter Body

[Full newsletter content following chosen archetype structure]

---

## Metadata

- **Archetype:** [Curator/Educator/Thought Leader/Hybrid]
- **Word count:** [X words]
- **Estimated read time:** [X minutes]
- **Main CTA:** [What you want readers to do]

---

## A/B Test Suggestions

**Subject lines to test:**
- Version A: [Subject]
- Version B: [Subject]

**Send time options:**
- [Day] at [Time] - [Why]
- [Day] at [Time] - [Why]
```

## Quality Checklist

Before sending, verify:

- [ ] Subject line creates curiosity (would YOU open it?)
- [ ] First line hooks immediately (no "hope you're well")
- [ ] One clear theme/focus (not a content dump)
- [ ] Scannable format (headers, bullets, short paragraphs)
- [ ] Personal voice (sounds like you, not corporate)
- [ ] Clear CTA (reply, forward, click, or just enjoy)
- [ ] Mobile-friendly (preview on phone)
- [ ] Proofread (typos kill trust)

## Integration

Works well with:
- `brand-voice` - Apply your documented voice
- `content-atomizer` - Turn newsletter into social posts
- `hook-writer` - Generate subject line options
- `copy-editor` - Polish before sending

**Workflow:**
```
Newsletter draft → brand-voice check → copy-editor polish → send
                                    → content-atomizer → social posts
```

## Frequency Guidelines

| Cadence | Best For | Reader Expectation |
|---------|----------|-------------------|
| Daily | News, markets, quick hits | <3 min read |
| Weekly | Deep dives, curated | 5-10 min read |
| Bi-weekly | Thought leadership | 7-15 min read |
| Monthly | Comprehensive roundups | 10-20 min read |

**Rule:** Don't send if you have nothing valuable. Silence > noise.
