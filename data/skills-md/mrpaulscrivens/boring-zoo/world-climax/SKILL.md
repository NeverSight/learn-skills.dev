---
name: world-climax
description: |-
  Define your Climax — the specific transformation you promise your audience.
  This is the second element of the World Code framework. Use when someone says
  "define my climax", "transformation promise", "what change do I create",
  "what do I promise", or "climax element".
---

# World Climax

You guide the user through discovering their Climax — the specific transformation they promise to the people they serve.

## Teaching Intro

Before asking any questions, share this brief context:

> Your Climax is the specific transformation you promise. Not vague ("feel more confident") but concrete and visualizable ("launch your first $5k offer within 90 days while being authentically yourself"). The strongest transformations connect to something primal — something people already want badly enough to pay for, change habits for, or rearrange their life around.

## Process

### Step 1: Read Voice file and create directory

Use the Bash tool to create the `world-code/` directory in the current working directory if it does not already exist:

```
mkdir -p world-code
```

Then check if `world-code/voice.md` exists and read it:

```
cat world-code/voice.md
```

If the file does not exist or is empty, tell the user:

> "Your Climax builds on your Voice — the tone and rules that make your writing sound like you. We need that foundation first. Let's capture your Voice."

Then invoke `/world-voice` and stop here.

If the file exists, read it and note the **Tone & Character**, **Hard Rules**, and **Authenticity Markers**. You will apply these when drafting the Climax statement in Step 5.

### Step 2: Check for Existing Work

Check if `world-code/climax.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Climax** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Climax file one at a time:
- Core Outcome
- The Transformation Promise
- Who This Is For
- The Before State
- The After State
- Why This Matters

For each section, show what's there and ask: "Keep this, tweak it, or rethink it?"
- **Keep:** Move to the next section
- **Tweak:** Ask focused follow-up questions about what to change, then update
- **Rethink:** Use the original discovery question that informed that section

After walking through all sections, save the updated file (same format, same path) and skip to the Transition step.

**If they choose START FRESH:**
Proceed with the normal discovery flow (Step 3 onward). Overwrite the existing file at the end.

**If they choose KEEP:**
Skip to the Transition step.

If the file **does not exist or is empty:**
Proceed with the normal discovery flow (Step 3 onward) — no change from current behavior.

### Step 3: Anchor to a core outcome

Most transformations that people will pay for connect to one of three primal outcomes:

- **More Money** — earning more, building wealth, financial freedom, career advancement, business growth
- **More Health** — physical fitness, mental wellness, energy, longevity, overcoming illness, looking better
- **More Love** — better relationships, finding a partner, deeper connection, community, self-acceptance, belonging

These aren't the only valid outcomes. Some transformations produce a tangible, desirable result that doesn't neatly fit those three — a beautiful garden, a finished novel, a renovated home, a skill mastered. The key test is: can someone picture the outcome clearly enough that they'd want it?

Ask the user:

**"When someone finishes working with you, what do they walk away with? Which of these is closest?"**
- More Money (or financial improvement)
- More Health (physical or mental)
- More Love (relationships, connection, belonging)
- Something else that's tangible and specific (describe it)

(Wait for answer.)

**Why this matters:** This anchor becomes the gravity center for everything else. When the Climax connects to a primal outcome, it practically sells itself because the desire already exists. When it connects to a tangible outcome outside the big three, you need to make sure that outcome is vivid and concrete enough to carry the same weight. Either way, you need to know what you're building toward before you start asking about frustrations and transformations.

If their answer is vague or abstract ("they feel empowered," "they have more clarity"), gently push:

> "That's the internal shift, and it matters. But what does someone on the outside *see* change? What would their spouse, their friend, their accountant notice is different? That visible change is what makes the transformation real and sellable."

Stay here until you have a concrete anchor. It doesn't need to be perfect — it will sharpen through the remaining questions. But it needs to be specific enough that someone could picture it.

### Step 4: Discovery questions — ask ONE AT A TIME

Now that you have the outcome anchor, use it to frame every question. Reference it specifically.

**Question 1:**
"What's the biggest frustration your ideal person has right now that's standing between them and [their outcome anchor]? Not a surface-level annoyance — the thing that actually keeps them stuck."

(Wait for answer. Acknowledge it before continuing.)

**Question 2:**
"Imagine they've worked with you and gotten [their outcome anchor]. It's 90 days from now. Describe a specific moment in their day that proves it happened. What are they doing? What are they looking at? How do they feel?"

(Wait for answer. If the answer is abstract or emotional without a concrete scene, ask: "Love that. Now what would a camera capture in that moment? What's the visible proof?")

**Question 3:**
"Beyond [their outcome anchor] itself, what shifts about how this person sees themselves? What do they believe about themselves now that they didn't before?"

(Wait for answer. This captures the identity shift underneath the practical change.)

**Question 4:**
"How would they describe what you helped them do — to a friend, over coffee, in one or two sentences? Their words, not marketing language."

(Wait for answer.)

### Step 5: Synthesize

After all answers, draft their Climax. The promise you draft must pass these tests:

**The Wallet Test:** Would someone hand over money for this outcome? If the transformation is too abstract or too small, they won't. The closer it ties to the core outcome anchor, the easier this test is to pass.

**The Picture Test:** Can someone close their eyes and see the after state? If they can't picture it, they can't want it badly enough to act.

**The Proof Test:** Is there a moment that proves it happened? Not a feeling — a visible, specific moment.

**The Voice Test:** Does this sound like something the user would actually say? Apply the tone, rhythm, hard rules, and authenticity markers from `world-code/voice.md`. Use the user's own language from Q4 especially.

Present the draft and ask:

> "Does this capture it? What would you adjust?"

### Step 6: Refine

Incorporate their feedback. Allow a maximum of **two refinement rounds**. If after two rounds they are still unsure, note what remains unresolved and suggest they revisit it after completing later elements (Method or Creation often clarify the Climax).

During refinement, if the Climax is drifting away from the core outcome anchor, name it:

> "I notice this is moving away from [anchor]. That's fine if intentional — but the closer your Climax stays to [anchor], the easier it'll be to sell. Want to pull it back, or does this new direction feel more honest?"

### Step 7: Save the file

Write the final Climax to `world-code/climax.md` in exactly this format:

```markdown
# One Climax

## Core Outcome
[The primal outcome anchor — More Money / More Health / More Love / or their specific tangible outcome]

## The Transformation Promise
[Their specific, concrete climax statement]

## Who This Is For
[Brief description of the person experiencing this]

## The Before State
[What life looks like before the transformation — specific, vivid, drawn from Q1]

## The After State
[The specific moment of transformation — drawn from Q2, camera-ready]

## Why This Matters
[The deeper significance — identity shift from Q3]
```

Populate every section using the answers from the discovery questions. Do not leave placeholders.

### Step 8: Transition

After saving, tell the user:

> "Your Climax is saved to `world-code/climax.md`. Next up is your **Method** — the unique system you use to deliver this transformation. Want to continue to Method now, or take a break and come back later?"

- If they want to continue, invoke `/world-method`.
- If they want a break, tell them they can return anytime with `/world-code-start` and it will pick up where they left off.

## Key Principles

- **One question at a time.** Never batch questions. Wait for each answer.
- **Anchor everything.** Reference the core outcome anchor in every question. It keeps the conversation focused and prevents drift into abstraction.
- **Push for specificity.** If an answer is vague, gently ask them to make it more concrete before moving on. "What would a camera capture?" is your best follow-up.
- **Build on their words.** Reference what they said in previous answers when framing the next question.
- **Apply their Voice.** Use the tone, rhythm, hard rules, and authenticity markers from `world-code/voice.md` when drafting the Climax statement.
- **Protect the outcome connection.** If the Climax drifts from the core outcome during refinement, flag it. Don't force them back — but make sure the drift is intentional, not accidental.
