---
name: iblai-marketing-copywriting
description: When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages, or product pages. Also use when the user says "write copy for," "improve this copy," "rewrite this page," "marketing copy," "headline help," "CTA copy," "value proposition," "tagline," "subheadline," "hero section copy," "above the fold," "this copy is weak," "make this more compelling," or "help me describe my product." Use this whenever someone is working on website text that needs to persuade or convert. For email copy, see iblai-marketing-email-sequence. For popup copy, see iblai-marketing-popup-cro. For editing existing copy, see iblai-marketing-copy-editing.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-copywriting

Write marketing copy that's clear, compelling, and drives action.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pull this context:

### 1. Page Purpose
- Page type (homepage, landing, pricing, feature, about)
- The ONE primary action you want

### 2. Audience
- Ideal customer
- Problem they're trying to solve
- Objections or hesitations
- Language they use for the problem

### 3. Product/Offer
- What you're selling
- What makes it different
- Key transformation or outcome
- Proof points (numbers, testimonials, case studies)

### 4. Context
- Where traffic comes from (ads, organic, email)
- What visitors already know on arrival

---

## Principles

### Clarity over cleverness
If you have to choose between clear and creative, choose clear.

### Benefits over features
Features: what it does. Benefits: what that means for the customer.

### Specific over vague
- Vague: "Save time on your workflow"
- Specific: "Cut your weekly reporting from 4 hours to 15 minutes"

### Customer language over company language
Use the words your customers use. Mirror voice-of-customer from reviews, interviews, support tickets.

### One idea per section
Each section advances one argument. Build a logical flow down the page.

---

## Style Rules

1. **Simple over complex** — "Use" not "utilize," "help" not "facilitate"
2. **Specific over vague** — avoid "streamline," "optimize," "innovative"
3. **Active over passive** — "We generate reports" not "Reports are generated"
4. **Confident over qualified** — strip "almost," "very," "really"
5. **Show over tell** — describe the outcome, drop the adverbs
6. **Honest over sensational** — fabricated stats or testimonials erode trust and create legal liability

### Quick Quality Check

- Jargon that could confuse outsiders?
- Sentences trying to do too much?
- Passive voice?
- Exclamation points? (remove them)
- Buzzwords without substance?

For thorough line-by-line review, hand off to `/iblai-marketing-copy-editing` after the draft.

---

## Best Practices

### Be direct
Get to the point. Don't bury value in qualifications.

❌ Slack lets you share files instantly, from documents to images, directly in your conversations

✅ Need to share a screenshot? Send as many documents, images, and audio files as your heart desires.

### Use rhetorical questions
Questions engage readers and make them apply the copy to themselves.
- "Hate returning stuff to Amazon?"
- "Tired of chasing approvals?"

### Use analogies when helpful
Make abstract concepts concrete.

### Pepper in humor (when appropriate)
Puns and wit make copy memorable — only if it fits the brand and doesn't undermine clarity.

---

## Page Structure

### Above the Fold

**Headline**
- Your single most important message
- Communicate the core value prop
- Specific > generic

**Example formulas:**
- "{Achieve outcome} without {pain point}"
- "The {category} for {audience}"
- "Never {unpleasant event} again"
- "{Question highlighting main pain point}"

Comprehensive headline formulas: [references/copy-frameworks.md](references/copy-frameworks.md).

Natural transition phrases: [references/natural-transitions.md](references/natural-transitions.md).

**Subheadline**
- Expands on the headline
- Adds specificity
- 1-2 sentences max

**Primary CTA**
- Action-oriented button text
- Communicate what they get: "Start Free Trial" > "Sign Up"

### Core Sections

| Section | Purpose |
|---------|---------|
| Social Proof | Build credibility (logos, stats, testimonials) |
| Problem/Pain | Show you understand the situation |
| Solution/Benefits | Connect to outcomes (3-5 key benefits) |
| How It Works | Reduce perceived complexity (3-4 steps) |
| Objection Handling | FAQ, comparisons, guarantees |
| Final CTA | Recap value, repeat CTA, risk reversal |

Detailed section types and page templates: [references/copy-frameworks.md](references/copy-frameworks.md).

---

## CTA Copy

**Weak (avoid):**
- Submit, Sign Up, Learn More, Click Here, Get Started

**Strong (use):**
- Start Free Trial
- Get [Specific Thing]
- See [Product] in Action
- Create Your First [Thing]
- Download the Guide

**Formula:** [Action Verb] + [What They Get] + [Qualifier if needed]

Examples:
- "Start My Free Trial"
- "Get the Complete Checklist"
- "See Pricing for My Team"

---

## Page-Specific Guidance

### Homepage
- Serve multiple audiences without going generic
- Lead with the broadest value prop
- Clear paths for different visitor intents

### Landing Page
- Single message, single CTA
- Match the headline to the ad/traffic source
- Complete argument on one page

### Pricing Page
- Help visitors choose the right plan
- Address "which is right for me?" anxiety
- Make the recommended plan obvious

### Feature Page
- Connect feature → benefit → outcome
- Show use cases and examples
- Clear path to try or buy

### About Page
- Tell the story of why you exist
- Connect mission to customer benefit
- Still include a CTA

---

## Voice and Tone

Before writing, pin down:

**Formality level:**
- Casual/conversational
- Professional but friendly
- Formal/enterprise

**Brand personality:**
- Playful or serious?
- Bold or understated?
- Technical or accessible?

Keep it consistent, but vary intensity:
- Headlines can be bolder
- Body copy should be clearer
- CTAs should be action-oriented

---

## Output Format

Provide:

### Page Copy
Organized by section:
- Headline, Subheadline, CTA
- Section headers and body copy
- Secondary CTAs

### Annotations
For key elements, explain:
- Why you made the choice
- Which principle it applies

### Alternatives
For headlines and CTAs, 2-3 options:
- Option A: [copy] — [rationale]
- Option B: [copy] — [rationale]

### Meta Content (if relevant)
- Page title (for SEO)
- Meta description

---

## Related Skills

- **iblai-marketing-copy-editing**: Polishing existing copy (use after your draft)
- **iblai-marketing-page-cro**: When page structure/strategy needs work, not just copy
- **iblai-marketing-email-sequence**: Email copywriting
- **iblai-marketing-popup-cro**: Popup and modal copy
- **iblai-marketing-ab-test-setup**: Test copy variations
