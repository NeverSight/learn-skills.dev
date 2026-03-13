---
name: objection-handler
description: Generate responses to sales objections. Use when the user encounters a specific objection from a prospect and needs help crafting a response, or when preparing objection handling for an upcoming meeting.
license: MIT
metadata:
  author: toughtongueai
  version: "1.0"
---

# Objection Handler

Generate thoughtful responses to sales objections. Provides multiple response options with different tones and explains the psychology behind each approach.

## When to Use

- User says "How do I respond to: [objection]?"
- User is preparing for a meeting and wants to rehearse objection handling
- User encountered an objection on a call and wants better responses for next time
- User wants to build an objection library for their team

## Required Inputs

```
Objection: [The exact words the prospect said, or a paraphrase]
Context: [Optional — who said it, what company, what stage of the conversation]
```

## Process

### 1. Load Context

Read `company-profile.md` for:
- The user's standard objection responses (if they've filled them in)
- Product differentiators (ammunition for responses)
- Pricing information (for budget objections)
- Competitor positioning (for competitive objections)

### 2. Classify the Objection

Every objection falls into one of these categories:

| Category | What They're Really Saying | Example |
|----------|---------------------------|---------|
| **Price / Budget** | "I can't justify the cost" | "It's too expensive" / "We don't have budget" |
| **Timing** | "Not a priority right now" | "Check back next quarter" / "We're too busy" |
| **Authority** | "I can't make this decision alone" | "I need to run this by my manager" |
| **Need** | "I don't see why we need this" | "We're fine with our current process" |
| **Trust** | "I don't trust this will work" | "We tried something like this before" / "AI isn't good enough" |
| **Competition** | "We already have something" | "We use [competitor]" / "We're building this ourselves" |
| **Stall** | "I want to avoid saying no" | "Send me more info" / "Let me think about it" |

### 3. Generate Responses

For each objection, provide three response options with different approaches:

## Output Format

```markdown
## Objection: "[The exact objection]"

**Category:** [Price / Timing / Authority / Need / Trust / Competition / Stall]
**What they're really saying:** [The underlying concern beneath the surface objection]

---

### Response 1: Acknowledge and Redirect
> "[Response that validates their concern, then reframes the conversation]"

**Why this works:** [1 sentence explaining the psychology]

### Response 2: Quantify the Cost of Inaction
> "[Response that helps them see the cost of NOT solving the problem]"

**Why this works:** [1 sentence explaining the psychology]

### Response 3: Reduce the Risk
> "[Response that lowers the barrier — pilot, trial, smaller commitment]"

**Why this works:** [1 sentence explaining the psychology]

---

**Follow-up question to regain control:**
> "[A question that moves the conversation forward regardless of which response you use]"
```

## Response Principles

### The ACR Framework

Every objection response should follow Acknowledge → Clarify → Respond:

1. **Acknowledge** — Show you heard them. Never dismiss or argue. ("That's a fair concern.")
2. **Clarify** — Make sure you understand the real objection. ("Help me understand — is it the total cost, or the timing of the investment?")
3. **Respond** — Address the real concern, not the surface objection.

### Universal Response Patterns

These patterns work across most objection categories:

**"That's exactly why..."**
Turn the objection into a reason to buy.
> "We don't have time for this." → "That's exactly why this exists — it saves your team [X hours/week] so they can focus on [what matters]."

**"What if we could..."**
Reframe as a hypothetical to lower resistance.
> "It's too expensive." → "What if we could start with a smaller pilot at [lower price point] and expand based on results?"

**"Other teams like yours..."**
Social proof without being pushy.
> "We tried something like this before and it didn't work." → "Totally fair. [Similar company] had the same experience with [previous solution]. The difference they found with us was [specific differentiator]."

**"Help me understand..."**
Clarify the real objection beneath the surface.
> "Send me more info." → "Happy to. Help me understand — what specifically would be most useful? That way I can send you the right thing, not a generic deck."

## Common Objections Library

If the user hasn't provided custom objections in `company-profile.md`, use these universal B2B SaaS objections as a starting point:

| Objection | Category | Key Response Angle |
|-----------|----------|-------------------|
| "It's too expensive" | Price | Reframe as cost-per-outcome, not cost-per-tool |
| "We don't have budget right now" | Price/Timing | Offer pilot, or help them build the business case |
| "We're happy with our current solution" | Competition | Ask what "happy" means — there's always a gap |
| "We're building this ourselves" | Competition | Acknowledge, then highlight hidden complexity and time cost |
| "I need to check with my team" | Authority | Offer to join the next conversation, or provide materials they can share |
| "Not the right time" | Timing | Respect it, set a specific follow-up date, leave value behind |
| "Send me more info" | Stall | Clarify what specifically they want to know — redirects to real conversation |
| "We tried something like this and it didn't work" | Trust | Acknowledge the experience, differentiate specifically, offer low-risk proof |
| "AI isn't good enough for this" | Trust | Agree with the general concern, then show specific evidence for your use case |
| "Our team won't use it" | Trust | Focus on adoption strategy — relevance drives usage, not mandates |

## Instructions

1. **Use the user's actual positioning.** Pull differentiators and competitor responses from `company-profile.md`. Generic responses are useless.
2. **Classify before responding.** The response to a Trust objection is completely different from a Price objection, even if the words sound similar.
3. **Always provide the "real concern."** The stated objection is rarely the actual objection. Surface the real concern.
4. **Three options, different tones.** Give the user choices — they know their prospect's personality better than you do.
5. **End with a follow-up question.** The goal is to continue the conversation, not "win" the objection.
6. **Never be dismissive.** "That's not really an issue" or "You're wrong about that" kills trust instantly.
