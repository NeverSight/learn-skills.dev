---
name: brand-voice-learner
description: Analyze existing brand content to extract voice patterns, create voice guidelines, and ensure consistent brand expression
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Brand Voice Learner

> Analyze existing brand content to extract voice characteristics, create actionable voice guidelines, and ensure consistent brand expression across all communications.

## When to Use This Skill

- Creating brand voice guidelines
- Onboarding new writers
- Auditing voice consistency
- Adapting voice for channels
- Training AI writing tools

## Methodology Foundation

Based on **NN/g voice research** and **content strategy best practices**, combining:
- Linguistic pattern analysis
- Voice dimension mapping
- Guidelines development
- Consistency measurement

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Analyzes existing content | Content sources to analyze |
| Extracts voice patterns | Voice evolution direction |
| Creates voice guidelines | Approval of guidelines |
| Identifies inconsistencies | Exception handling |
| Suggests voice examples | Final voice choices |

## Instructions

### Step 1: Gather Voice Samples

**Content to Analyze:**
| Source | Purpose |
|--------|---------|
| Website copy | Core brand voice |
| Blog posts | Extended voice |
| Social media | Casual variation |
| Email campaigns | Direct communication |
| Product UI | Functional voice |
| Customer support | Empathetic voice |

**Sample Requirements:**
- Minimum 10-15 pieces
- Variety of contexts
- Include best examples
- Cover different tones

### Step 2: Analyze Voice Dimensions

**Voice Dimension Framework:**

| Dimension | Spectrum |
|-----------|----------|
| Formality | Casual ←→ Formal |
| Personality | Serious ←→ Playful |
| Directness | Indirect ←→ Direct |
| Enthusiasm | Reserved ←→ Enthusiastic |
| Technical | Simple ←→ Technical |
| Warmth | Distant ←→ Warm |

### Step 3: Extract Patterns

**Linguistic Elements:**
| Element | What to Identify |
|---------|-----------------|
| Sentence length | Short, medium, long |
| Word choice | Common, specialized, branded |
| Contractions | Used, avoided, mixed |
| Active/passive | Preference |
| Pronouns | We/you/they patterns |
| Punctuation | Exclamations, ellipses, etc. |

### Step 4: Document Guidelines

**Guidelines Structure:**
1. Voice principles (3-5)
2. Dimension scores
3. Do/Don't examples
4. Channel variations
5. Word lists

### Step 5: Create Consistency Tools

**Tools to Create:**
- Voice checklist
- Example library
- Word/phrase dictionary
- Channel guidelines

## Examples

### Example 1: Complete Voice Analysis

**Input:**
```
Analyze brand voice from these samples:

Website: "We build tools that actually work. No fluff, no complexity—
just software that helps you get stuff done."

Blog: "Here's the thing about productivity apps: most of them make
your life harder, not easier. We think that's backwards."

Email: "Hey there! Your trial is almost over. Before you go, we wanted
to make sure you saw everything [Product] can do."

Social: "Mondays are hard. Your software shouldn't be. ☕"
```

**Output:**
```
## Brand Voice Analysis

### Voice Summary

**Overall Character:** Confident, casual, anti-corporate

Your brand sounds like a smart friend who's direct and relatable—
someone who gets frustrated by the same things your customers do
and isn't afraid to call out industry BS.

---

### Voice Dimensions

```
Formality     [===|======] Casual (3/10)
Personality   [======|===] Playful (7/10)
Directness    [========|=] Very Direct (9/10)
Enthusiasm    [=====|====] Moderate (6/10)
Technical     [====|=====] Accessible (4/10)
Warmth        [======|===] Warm (7/10)
```

---

### Voice Principles

#### 1. Say it Straight
No corporate speak, no jargon inflation. If you can say it
in fewer words, do it.

**Examples:**
- ✅ "We build tools that actually work"
- ❌ "We leverage cutting-edge solutions to optimize..."

#### 2. Take Their Side
Position as ally against frustration. You share their pain
with the status quo.

**Examples:**
- ✅ "Most productivity apps make your life harder"
- ❌ "Our competitors offer suboptimal experiences"

#### 3. Stay Human
Contractions, casual language, occasional humor. Sound like
a person, not a press release.

**Examples:**
- ✅ "Here's the thing about..."
- ❌ "It is important to note that..."

#### 4. Confident, Not Arrogant
State opinions clearly without hedging, but don't put
others down.

**Examples:**
- ✅ "No fluff, no complexity"
- ❌ "Unlike those other terrible apps..."

---

### Linguistic Patterns

| Element | Pattern | Examples |
|---------|---------|----------|
| Sentence length | Short to medium (8-15 words average) | "We think that's backwards." |
| Contractions | Always used | "That's", "shouldn't", "we're" |
| Pronouns | Heavy "we/you" | Creates conversational feel |
| Active voice | Strong preference | "We build" not "Tools are built" |
| Punctuation | Occasional em-dashes, rare exclamations | "No fluff—just software" |
| Emoji | Occasional, relevant | Coffee emoji for Monday post |

---

### Voice Do's and Don'ts

#### DO ✅

| Pattern | Example |
|---------|---------|
| Use contractions | "We're building" not "We are building" |
| Start with "Here's the thing" | Conversational opener |
| Use "actually" for emphasis | "Tools that actually work" |
| Reference shared frustrations | "Mondays are hard" |
| Keep paragraphs short | 2-3 sentences max |
| Use second person | "Your trial" "helps you" |

#### DON'T ❌

| Pattern | Why Not |
|---------|---------|
| "Leverage" "optimize" "synergy" | Corporate jargon |
| "We are pleased to announce" | Stiff, formal |
| Passive voice | "Was built by our team" |
| Hedging language | "We think maybe possibly..." |
| Long, complex sentences | Loses casual feel |
| Excessive exclamation points | Feels fake enthusiastic |

---

### Word Choice Guide

#### Preferred Terms

| Instead of | Use |
|------------|-----|
| Utilize | Use |
| Leverage | Use |
| Solutions | Tools, software |
| Empower | Help |
| Seamless | Easy, simple |
| Robust | Strong, reliable |
| Best-in-class | (just show, don't tell) |
| Cutting-edge | New, latest |

#### Signature Phrases

| Phrase | When to Use |
|--------|-------------|
| "Here's the thing" | Starting opinion pieces |
| "Actually" | Emphasizing real value |
| "No [negative], no [negative]" | Simple value props |
| "That's backwards" | Calling out industry norms |

---

### Channel Variations

#### Website (Core Voice)
- Most polished version
- Still casual but refined
- Slightly higher stakes language

#### Blog (Extended Voice)
- More conversational
- Can be longer, more exploratory
- Personal opinions encouraged

#### Social Media (Compressed Voice)
- Shortest, punchiest
- More humor allowed
- Emoji occasionally OK
- Can reference current events/culture

#### Email (Direct Voice)
- Friendly but action-oriented
- "Hey there" openings OK
- Clear CTAs
- Personal where possible

#### Support (Empathetic Voice)
- Warmer, more patient
- Solution-focused
- Less attitude, more help
- Still casual but careful

---

### Voice Checklist

Before publishing, check:

- [ ] Would you say this to a friend?
- [ ] Are there any "corporate speak" words?
- [ ] Is it shorter than it could be?
- [ ] Is the main point clear?
- [ ] Does it sound like us, not a competitor?
- [ ] Would it make sense without context?
```

### Example 2: Quick Voice Audit

**Input:**
```
Does this match our voice?
"We are delighted to inform you that your request has been
processed and the desired outcome has been achieved."
```

**Output:**
```
## Voice Audit

### Verdict: ❌ Does Not Match

---

### Issues Found

| Problem | Example | Should Be |
|---------|---------|-----------|
| Too formal | "We are delighted" | "Great news!" |
| Passive voice | "has been processed" | "We processed" |
| Corporate speak | "desired outcome" | "what you wanted" |
| Stiff structure | Full sentence | Shorter, direct |

---

### Rewritten

**Original:**
> "We are delighted to inform you that your request has been
> processed and the desired outcome has been achieved."

**On-brand version:**
> "Good news! We've taken care of your request—you're all set."

**Even more casual:**
> "Done! Your request went through. You're good to go."

---

### What Went Wrong

This sounds like a corporate auto-reply, not your brand.
It has:
- No contractions
- Passive voice
- Formal phrasing
- No personality

Your brand would sound like a helpful friend delivering good news,
not a legal notice.
```

## Skill Boundaries

### What This Skill Does Well
- Analyzing existing content
- Extracting voice patterns
- Creating guidelines
- Auditing consistency

### What This Skill Cannot Do
- Create voice from scratch
- Know your brand strategy
- Access all your content
- Replace brand judgment

## Iteration Guide

**Follow-up Prompts:**
- "Rewrite this in our brand voice"
- "Create voice variations for [channel]"
- "Audit these samples for consistency"
- "Add to our word/phrase dictionary"

## References

- NN/g Voice and Tone Guidelines
- Content Strategy Alliance
- Mailchimp Voice and Tone
- Buffer Brand Voice Guide

## Related Skills

- `brand-strategy` - Overall brand development
- `copywriting-ogilvy` - Writing craft
- `storytelling-storybrand` - Narrative voice

## Skill Metadata

- **Domain**: Branding / Content
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 2-4 hours for full guidelines
- **Prerequisites**: Content samples, brand context
