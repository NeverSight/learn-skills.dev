---
name: world-crown
description: |
  Discover your Crown — the positioning statement that declares what territory you rule.
  This is the fifth element of the World Code framework. Use when someone says
  "define my positioning", "market position", "what territory do I own",
  "crown element", or "what do I actually do".
---

# World Crown

You guide the user through discovering their Crown — the positioning declaration that claims their territory in the marketplace.

## Teaching Intro

Before asking any questions, share this brief context:

> Your Crown is the single statement that declares what territory you rule. Not a tagline. Not a mission statement. Your positioning declaration that makes everything else obvious. A king doesn't list every village — he says "I rule the Northern Territories" and everyone understands. We're going to build yours from the work you've already done.

## Process

### Step 1: Read all prerequisite files

Use the Bash tool to check if `world-code/voice.md`, `world-code/climax.md`, `world-code/method.md`, and `world-code/creation.md` exist in the current working directory and read them:

```
cat world-code/voice.md
cat world-code/climax.md
cat world-code/method.md
cat world-code/creation.md
```

If **any** file does not exist or is empty, tell the user:

> "Your Crown is built from your Voice, your Climax (the transformation), your Method (how you deliver it), and your Creation (the offer that packages it). We need all four foundations first."

- If `world-code/voice.md` is missing, say "Let's start with your Voice." and invoke `/world-voice`.
- If `world-code/voice.md` exists but `world-code/climax.md` is missing, say "Let's start with your Climax." and invoke `/world-climax`.
- If both exist but `world-code/method.md` is missing, say "Let's define your Method first." and invoke `/world-method`.
- If those three exist but `world-code/creation.md` is missing, say "Let's design your Creation first." and invoke `/world-creation`.

Stop here in any of those cases.

If all four files exist, read them and note:
- From Voice: **Tone & Character**, **Hard Rules**, **Authenticity Markers**
- From Climax: **Transformation Promise**, **Who This Is For**, **Before State**, **After State**
- From Method: **Methodology Name**, **Core Principle**, **Why It Works Differently**
- From Creation: **Offer Name**, **BONES Breakdown** (especially Obvious and New)

You will use these to auto-generate the Crown draft in Step 3 and apply the Voice throughout.

### Step 2: Check for Existing Work

Check if `world-code/crown.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Crown** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Crown file one at a time:
- Crown Statement
- Layer 1 (What You Do)
- Layer 2 (How You Think)
- Layer 3 (Who You Fight For)
- Territory Claim

For each section, show what's there and ask: "Keep this, tweak it, or rethink it?"
- **Keep:** Move to the next section
- **Tweak:** Ask focused follow-up questions about what to change, then update
- **Rethink:** Re-synthesize that layer from the prerequisite files and present a new draft

After walking through all sections, save the updated file (same format, same path) and skip to the Transition step.

**If they choose START FRESH:**
Proceed with the normal flow (Step 3 onward). Overwrite the existing file at the end.

**If they choose KEEP:**
Skip to the Transition step.

If the file **does not exist or is empty:**
Proceed with the normal flow (Step 3 onward).

### Step 3: Auto-generate Crown draft

Synthesize a Crown draft from the existing files. Map:

- **Layer 1 (What You Do):** Pull from Climax's Transformation Promise + Creation's BONES "Obvious". The specific, concrete outcome.
- **Layer 2 (How You Think):** Pull from Method's Core Principle + Creation's BONES "New". The belief/worldview that drives the approach.
- **Layer 3 (Who You Fight For):** Pull from Climax's Who This Is For + Before State. The identity + emotional state — not demographics but gut-level recognition.

Combine the three layers into a Crown Statement — a single powerful declaration. Write it in their Voice.

Present the draft:

> "I built this from everything you've already defined — your transformation, your method, your offer. Here's your Crown:"
>
> **Crown Statement:** [The combined declaration]
>
> **Layer 1 — What You Do:** [specific outcome]
> **Layer 2 — How You Think:** [driving principle]
> **Layer 3 — Who You Fight For:** [identity + emotion]
>
> "Now let's stress-test it."

### Step 4: Validation questions — ask ONE AT A TIME

4 validation questions. These aren't discovery — they're testing the auto-generated draft. Ask each one, wait for the answer, and adjust if needed before moving to the next.

**Question 1: The Gut Punch Test**
"Read your Crown out loud. Does your ideal person feel something visceral — not 'that sounds nice' but 'holy shit, finally someone who gets it'? What's your gut reaction?"

(Wait. If weak, ask what's missing — which layer doesn't land? Adjust that layer.)

**Question 2: The Hell No Test**
"Who should immediately think 'that's definitely not for me' when they hear this? List 3-5 types of people this should repel. If everyone could see themselves in it, it's not a Crown."

(Wait. If they can't list repelled people, the Crown is too broad — tighten Layer 3.)

**Question 3: The Territory Test**
"Could you defend this territory? Do you actually deliver this outcome (Layer 1), genuinely believe this principle (Layer 2), and truly understand these people (Layer 3)? Or are you claiming territory you don't rule?"

(Wait. If any layer feels inauthentic, rework that layer using their feedback.)

**Question 4: The Competitor Territory Check**
"Who else serves a similar audience? How does your Crown create territory that's YOURS — not just 'better' but 'different'? Where are you the ONLY option, not the BEST option?"

(Wait. If their Crown overlaps too much with competitors, sharpen Layer 2 — the belief layer is usually what differentiates.)

### Step 5: Refine

Incorporate feedback from the 4 tests. Max two refinement rounds. If the Crown still doesn't feel right, suggest they revisit after Conversation — real-world content often reveals positioning that abstract exercises miss.

### Step 6: Save the file

Write the final Crown to `world-code/crown.md` in exactly this format:

```markdown
# One Crown

## Crown Statement
[The complete positioning declaration]

## Layer 1: What You Do
[The specific outcome you deliver]

## Layer 2: How You Think
[The principle/belief that drives your approach]

## Layer 3: Who You Fight For
[Your audience's identity + emotional state]

## Territory Claim
[What specific territory this Crown stakes — and what it excludes]
```

Populate every section using the synthesized draft and validation feedback. Do not leave placeholders.

### Step 7: Transition

After saving, tell the user:

> "Your Crown is saved to `world-code/crown.md`. This is your positioning declaration — use it when someone asks what you do. Next up is your **Conversation** — how you create content that defends this territory and attracts the right people. Want to continue to Conversation now, or take a break?"

- If they want to continue, invoke `/world-conversation`.
- If they want a break, tell them they can return anytime with `/world-code-start` and it will pick up where they left off.

## Key Principles

- **Auto-generate, don't interrogate.** The user already answered 15+ questions across Voice, Climax, Method, and Creation. Crown synthesizes — it doesn't re-ask.
- **Test, don't discover.** The 4 questions are validation tests, not open-ended discovery. The draft should be close; the questions refine it.
- **Three layers, one statement.** The Crown Statement combines all three layers into something someone could say in conversation. The layers exist for clarity, but the statement is what matters.
- **Exclude to include.** A Crown that includes everyone includes no one. The Hell No Test is as important as the Gut Punch Test.
- **Apply their Voice.** The Crown Statement must sound like something THEY would say. Use their tone, vocabulary, and hard rules from voice.md.
