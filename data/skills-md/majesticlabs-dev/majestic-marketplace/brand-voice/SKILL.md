---
name: brand-voice
description: Codify brand writing style into a reusable voice guide. Extracts patterns from existing content and generates a style document with tone rules, vocabulary, and do/don't examples.
triggers:
  - brand voice
  - voice guide
  - writing style
  - tone of voice
  - brand style
  - voice document
allowed-tools: Read Write Edit Grep Glob WebSearch AskUserQuestion
---

# Brand Voice Architect

Codify your brand's unique voice into a living style guide that ensures consistency across all content—website, emails, social, ads, and beyond.

## Deep Discovery (Optional)

For thorough voice exploration before creating the guide, run:

```
/majestic-tools:interview "brand voice"
```

This triggers a conversational interview with brand-specific questions about voice identity, audience connection, tone boundaries, and existing patterns. The interview output can then be synthesized into a full voice guide using this skill.

## Why This Matters

- **Consistency builds trust** - Readers recognize you instantly
- **Scales content creation** - Anyone can write on-brand
- **Saves editing time** - Clear rules reduce revisions
- **Enables AI assistance** - Voice guides make AI-generated content usable

## Conversation Starter

Use `AskUserQuestion` to gather initial context. Begin by asking:

"I'll help you codify your brand voice into a reusable style guide.

**Please provide one of these:**

**Option A - Existing Content (Preferred)**
Share 3-5 pieces of content you love that represent your voice:
- Website copy, emails, social posts, or blog articles
- Paste directly or provide URLs/file paths

**Option B - Brand Description**
If you don't have content yet, describe:
1. **Industry/Product**: What do you sell?
2. **Target Audience**: Who are you talking to?
3. **Brand Personality**: 3-5 adjectives that describe your brand
4. **Brands You Admire**: Whose voice do you like? (competitors or not)
5. **Avoid Sounding Like**: What tone would be wrong for you?

I'll analyze patterns and create your voice guide."

## Analysis Process

### If Content Provided (Option A)

Extract patterns across all samples:

**Voice Patterns to Identify:**
- Sentence length distribution (short/medium/long)
- Use of contractions (can't vs cannot)
- First/second/third person preference
- Active vs passive voice ratio
- Question usage frequency
- Exclamation point usage
- Emoji/punctuation style
- Paragraph length patterns
- Opening patterns (how pieces start)
- Closing patterns (how pieces end)

**Vocabulary Patterns:**
- Recurring power words
- Industry jargon usage (heavy/light/none)
- Colloquialisms and slang
- Metaphor and analogy patterns
- Words that appear frequently
- Words that are notably absent

**Tone Markers:**
- Formality level (1-10 scale)
- Humor usage (frequent/occasional/never)
- Confidence level (bold claims vs hedging)
- Emotional warmth (distant vs intimate)
- Authority stance (peer vs expert vs mentor)

### If Description Provided (Option B)

Use WebSearch to find:
- Example content from admired brands
- Industry voice benchmarks
- Competitor voice analysis
- Audience communication preferences

Then synthesize a voice based on inputs.

## Voice Guide Structure

### 1. Voice DNA (Core Identity)

```markdown
## Voice DNA

### Brand Personality
[3-5 defining traits with explanations]

| Trait | What It Means | How It Shows Up |
|-------|---------------|-----------------|
| [Trait 1] | [Definition] | [Example in copy] |
| [Trait 2] | [Definition] | [Example in copy] |
| [Trait 3] | [Definition] | [Example in copy] |

### The Elevator Pitch
"We sound like [description]. Think [reference point] meets [reference point]."

### If Our Brand Were a Person
[2-3 sentence description of brand as human—age, profession, how they talk at a party]
```

### 2. Tone Spectrum

```markdown
## Tone Spectrum

Our voice stays consistent, but tone adapts to context.

| Context | Tone | Example |
|---------|------|---------|
| Homepage hero | Confident, bold | "Stop guessing. Start knowing." |
| Error message | Helpful, calm | "Something went wrong. Let's fix it together." |
| Success message | Warm, celebratory | "You did it! Your first campaign is live." |
| Sales email | Direct, valuable | "Here's what's working for teams like yours." |
| Support docs | Clear, patient | "First, open Settings. You'll find it in the top right." |
| Social media | Casual, engaging | "Hot take: [opinion]. Fight me in the comments." |
| Legal/Terms | Clear, straightforward | "Your data belongs to you. Here's exactly what we collect." |

### Tone Dial

**Formal ←――――――→ Casual**
[Mark where brand sits: e.g., "We sit at 3/10—professional but never stiff."]

**Serious ←――――――→ Playful**
[Mark where brand sits: e.g., "We sit at 6/10—we crack jokes but know when to be serious."]

**Reserved ←――――――→ Enthusiastic**
[Mark where brand sits: e.g., "We sit at 7/10—we're excited about what we do and it shows."]
```

### 3. Vocabulary Guide

```markdown
## Vocabulary

### Words We Love
| Word/Phrase | Why | Use When |
|-------------|-----|----------|
| [Word] | [Reason] | [Context] |

### Words We Avoid
| Avoid | Use Instead | Why |
|-------|-------------|-----|
| [Word] | [Alternative] | [Reason] |

### Industry Jargon Rules
[How much jargon is acceptable and when]

### Pronouns
- **We/Our**: [When to use]
- **You/Your**: [When to use]
- **I/My**: [When to use, if ever]
- **They/The company**: [When to use, if ever]
```

### 4. Sentence Style

```markdown
## Sentence Style

### Length
- **Target**: [X words average per sentence]
- **Mix**: [Short sentences for punch, longer for explanation]
- **Paragraphs**: [Max X sentences per paragraph]

### Structure Preferences
- **Contractions**: [Always/Sometimes/Never] — "you're" vs "you are"
- **Active voice**: [Percentage target] — "We built this" vs "This was built"
- **Starting sentences**: [Patterns to use/avoid]
- **Questions**: [Rhetorical? Direct? Frequency?]

### Punctuation
- **Exclamation points**: [Rules for usage]
- **Em dashes**: [Heavy use/light use]
- **Ellipses**: [Never/sparingly/frequently]
- **Oxford comma**: [Yes/No]
- **Emojis**: [Never/sparingly/frequently + which ones]
```

### 5. Formatting Conventions

```markdown
## Formatting

### Headlines
- **Case**: [Sentence case / Title Case]
- **Length**: [Max X words]
- **Punctuation**: [Period/No period]

### CTAs
- **Style**: [Action verb first]
- **Examples**: [List of preferred CTA phrases]

### Lists
- **Bullet style**: [Dashes/dots/checkmarks]
- **Capitalization**: [First word only / Each word]
- **Punctuation**: [Periods/No periods]

### Numbers
- **Spell out**: [One through ten / all / none]
- **Percentages**: [50% vs fifty percent]
- **Currency**: [$X vs X dollars]
```

### 6. Do/Don't Examples

```markdown
## Do/Don't Examples

### Homepage Hero
❌ "Welcome to [Company]. We are the leading provider of innovative solutions."
✅ "[Bold claim that shows, not tells]."

### Feature Description
❌ "Our platform leverages cutting-edge technology to deliver best-in-class results."
✅ "[Specific outcome in plain language]."

### Email Subject Line
❌ "Newsletter #47 - Monthly Update"
✅ "[Curiosity hook or specific benefit]."

### Error Message
❌ "Error 403: Forbidden access denied."
✅ "[Human explanation + next step]."

### CTA Button
❌ "Submit" / "Click Here"
✅ "[Action + Outcome]" — "Start Free Trial" / "Get Your Report"

### Social Post
❌ "We are pleased to announce..."
✅ "[Direct statement or hook]."
```

### 7. Voice Validation Checklist

```markdown
## Voice Checklist

Before publishing, verify:

### Personality Check
- [ ] Could this only be written by us? (Not generic)
- [ ] Does it match our personality traits?
- [ ] Would our ideal customer feel spoken to?

### Tone Check
- [ ] Is the tone appropriate for this context?
- [ ] Does it match our position on the tone dials?

### Language Check
- [ ] No words from the "avoid" list?
- [ ] Jargon level appropriate for audience?
- [ ] Contractions used consistently?

### Style Check
- [ ] Sentence length varied?
- [ ] Active voice dominant?
- [ ] Formatting follows conventions?

### Final Gut Check
- [ ] Read it aloud—does it sound like us?
```

## Output Format

```markdown
# BRAND VOICE GUIDE: [Brand Name]

*Version 1.0 | Created [Date]*

---

## Quick Reference

**We are:** [3 traits]
**We sound like:** [1-sentence description]
**We never sound:** [What to avoid]

---

## 1. VOICE DNA
[Brand personality section]

---

## 2. TONE SPECTRUM
[Context-based tone adjustments]

---

## 3. VOCABULARY
[Words we love/avoid + jargon rules]

---

## 4. SENTENCE STYLE
[Length, structure, punctuation rules]

---

## 5. FORMATTING
[Headlines, CTAs, lists, numbers]

---

## 6. DO/DON'T EXAMPLES
[Before/after examples by content type]

---

## 7. VOICE CHECKLIST
[Pre-publish validation]

---

## APPENDIX: Sample Rewrites

### Original (Off-Brand)
> [Example of generic/wrong voice]

### Revised (On-Brand)
> [Same content in brand voice]

### What Changed
- [Change 1]
- [Change 2]
- [Change 3]
```

## File Output

After generating the guide, offer to save it:

"Would you like me to save this voice guide to a file?

Suggested location: `docs/brand-voice.md` or `.claude/brand-voice.md`

This file can be referenced by other skills (content-writer, email-nurture, content-atomizer) to maintain consistency."

## Quality Standards

- **Specific over generic** - "We use contractions" not "We're casual"
- **Examples required** - Every rule needs a concrete example
- **Actionable rules** - Must be possible to verify compliance
- **Source from reality** - Extract from actual content, don't invent
- **Living document** - Note that voice guides should evolve

## Integration with Other Skills

This voice guide works with:
- `content-writer` - Apply voice to articles
- `content-atomizer` - Maintain voice across platforms
- `email-nurture` - Consistent email sequences
- `linkedin-content` - On-brand social posts
- `landing-page-builder` - Voice-aligned landing pages
- `sales-page` - Consistent sales messaging

**Usage pattern:**
```
"Write this using the voice guide in docs/brand-voice.md"
```

## Maintenance Notes

Voice guides should be updated when:
- Brand positioning changes
- New content types are added
- Team feedback reveals gaps
- Voice drifts from guide (realign or update)

Recommend quarterly reviews.
