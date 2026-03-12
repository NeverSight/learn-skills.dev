---
name: world-conversation
description: |
  Build your Conversation — the content strategy that sustains your world.
  This is the sixth element of the World Code framework. Use when someone says
  "content strategy", "what should I post", "conversation element",
  "build my content plan", "content plan", or "build my bridge".
---

# World Conversation

You guide the user through building their Conversation — the Bridge that connects their audience to their Creation and generates infinite content.

## Teaching Intro

Before asking any questions, share this brief context:

> Your content strategy is a bridge. Your audience starts at Point A — stuck, frustrated, not where they want to be — and you're helping them get to Point B, the hard outcome your world delivers. On that bridge are walls they need to scale. Your content helps them scale those walls. Every piece of content you create comes FROM the bridge. You'll never have to ask "what should I post today?" — you look at your walls, pick a struggle, and make content about it. That's the whole game.

## Process

### Step 1: Read the Voice, Climax, Method, Creation, and Crown files

Use the Bash tool to check if `world-code/voice.md`, `world-code/climax.md`, `world-code/method.md`, `world-code/creation.md`, and `world-code/crown.md` exist in the current working directory and read them:

```
cat world-code/voice.md
cat world-code/climax.md
cat world-code/method.md
cat world-code/creation.md
cat world-code/crown.md
```

If **any** file does not exist or is empty, tell the user:

> "Your Conversation is built on your Voice, your Climax (the transformation), your Method (how you deliver it), your Creation (the offer that packages it), and your Crown (the territory you claim). We need all five foundations first."

- If `world-code/voice.md` is missing, say "Let's start with your Voice." and invoke `/world-voice`.
- If `world-code/voice.md` exists but `world-code/climax.md` is missing, say "Let's start with your Climax." and invoke `/world-climax`.
- If both exist but `world-code/method.md` is missing, say "Let's define your Method first." and invoke `/world-method`.
- If those three exist but `world-code/creation.md` is missing, say "Let's design your Creation first." and invoke `/world-creation`.
- If those four exist but `world-code/crown.md` is missing, say "Let's discover your Crown first." and invoke `/world-crown`.

Stop here in any of those cases.

If all five files exist, read them and note:
- The **Tone & Character**, **Hard Rules**, and **Authenticity Markers** from the Voice
- The **Transformation Promise** and **Before/After States** from the Climax
- The **Methodology Name** and **Core Principle** from the Method
- The **Offer Name**, **Format**, and **BONES Breakdown** from the Creation
- The **Crown Statement** and **Territory Claim** from the Crown

You will reference the Climax, Method, Creation, and Crown throughout the questions below and apply the Voice when drafting in Step 6. The Bridge outcome should align with the Crown's territory — your content defends and expands the territory your Crown claims.

### Step 2: Check for Existing Work

Check if `world-code/conversation.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Conversation** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Conversation file one at a time:
- The Outcome
- Wall 1 (Struggles, Goblin voices, and Treasure)
- Wall 2 (Struggles, Goblin voices, and Treasure)
- Wall 3 (Struggles, Goblin voices, and Treasure)
- The Culprit
- Content Ecosystem

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

### Step 3: Build the Bridge — ask ONE AT A TIME

Ask the following questions **one at a time**. Wait for the user to answer each question before asking the next. After each answer, briefly acknowledge what they said and build on it when introducing the next question. Never batch multiple questions together.

Reference the user's Climax, Method, and Creation as indicated.

**Question 1: The Outcome (Point B)**
"What's the specific, hard outcome you help people achieve? Something they can visualize. Not 'more confidence' — something concrete like '$25k/month working 20 hours a week with no team.' What's the Point B of your bridge?"

(Wait for answer. Pull from the Climax transformation promise as a starting point. Push for hard promises — numbers, timeframes, constraints. If their answer is vague, push back: "Can you put a number on it? A timeframe? A constraint? The more specific, the more powerful your content becomes.")

**Question 2: The 3 Walls**
"What are the 3 biggest obstacles standing between your person and that outcome? These are the walls they have to scale on the bridge. Think about the major categories of problems, not specific tactics."

(Wait for answer. Each wall becomes a major content pillar. They should map to things the user actually helps with. If they list more than 3, help them consolidate. If they list fewer, help them identify what's missing.)

**Question 3: The Struggles (3 per wall)**
"Now let's break each wall down. For each wall, what are the 3 specific struggles your person faces?"

Present it as:
- Wall 1 [name]: What are the 3 struggles?
- Wall 2 [name]: What are the 3 struggles?
- Wall 3 [name]: What are the 3 struggles?

(Wait for answer. These 9 struggles become specific content topics. This can be asked as one question since the structure is clear.)

**Question 4: The Goblins**
"For each struggle, there's a voice in your person's head — a Goblin — whispering a false belief that keeps them stuck. What's the Goblin saying for each struggle?"

(Wait for answer. These become the false beliefs your content addresses. They map to the "Wrong Belief" concept but are more granular — one per struggle instead of one overall. Help the user think about what their person tells themselves to justify staying stuck.)

**Question 5: The Treasures**
"When someone scales each wall, what's the prize? What micro-outcome do they get? These are the Treasures — small wins that build belief toward the big outcome."

(Wait for answer. One treasure per wall. These become micro-promises in content — proof that the person is making progress.)

**Question 6: The Culprit**
"What's the big thing you and your people are all fighting against? The larger enemy — the system, the belief, the industry norm. The Culprit that makes all these walls exist in the first place."

(Wait for answer. This is the overarching narrative tension that ties all content together. It should feel like a shared enemy the creator and audience are united against.)

### Step 4: Add the 3 Content Layers

After the Bridge is built, introduce the content quality framework:

> "Now that your Bridge is built, let me show you how to make sure every piece of content actually hits. There are 3 layers to great content:
>
> **Layer 1: Outcomes, Problems, Mechanisms** — The practical layer. What's the result? What's the problem? How does the solution work? This is where most content lives and it's the minimum bar.
>
> **Layer 2: Experiences, Opinions, Worldviews** — The personal layer. Your stories, your takes, your way of seeing the world. This is what makes content YOURS instead of generic advice anyone could give.
>
> **Layer 3: Identity, Transformation, Becoming** — The deep layer. Who is your person becoming? What identity shift happens? This is the layer that creates real loyalty — people don't just learn from you, they see themselves in you.
>
> Long-form content should hit all 3 layers. Short-form can focus on 1-2. If your content isn't performing, it's probably missing a layer."

No questions needed here — this is teaching. Move to Step 5.

### Step 5: Content Ecosystem

Map out their content ecosystem by explaining how the Bridge feeds every format:

> "Here's how your Bridge feeds your entire content ecosystem:
>
> - **BVA (Big Value Asset)** — Your cornerstone content that covers the full bridge. This is the thing someone finds and goes 'holy shit, this person gets it.' Could be a YouTube video, a mega-post, a free guide. It shows the whole journey from Point A to Point B.
>
> - **Long form** (YouTube, blog, podcast) — Each piece covers an individual wall or struggle in depth. This is where you hit all 3 content layers.
>
> - **Short form** (Instagram, X, LinkedIn) — Each piece covers a specific struggle, a Goblin voice, or a micro-win (Treasure). Quick, punchy, one layer is enough.
>
> - **Email** — The relationship channel. Mix of all types, but with more personal Layer 2 and Layer 3 content.
>
> Think of it like a cattle pen, not a funnel. You're not forcing people through a straight chute. They circle, consume at their own pace, enter when they're ready. Short form catches attention. Long form builds understanding. BVA shows the full picture. Your offer is there when they're ready."

Ask: "What does your content ecosystem look like? What formats are you using or planning to use?"

(Wait for answer. Help them map their chosen formats to the Bridge structure.)

### Step 6: Synthesize & Save

After all answers, draft their Conversation strategy. The draft must be written using the Voice from `world-code/voice.md`. Present it and ask:

> "Does this capture your Bridge? Could you create content from this for 2 years without getting bored? If not, what would you change?"

Allow a maximum of **two refinement rounds**. If after two rounds they are still unsure, note what remains unresolved and suggest they revisit it after completing the final element (Crossing often clarifies the Conversation).

Write the final Conversation to `world-code/conversation.md` in exactly this format:

```markdown
# One Conversation

## The Bridge

### The Outcome
[Hard outcome with specifics — the Point B]

### Wall 1: [Name]
**Struggles:**
1. [Struggle] — Goblin voice: "[false belief]"
2. [Struggle] — Goblin voice: "[false belief]"
3. [Struggle] — Goblin voice: "[false belief]"
**Treasure:** [Micro-outcome after scaling this wall]

### Wall 2: [Name]
**Struggles:**
1. [Struggle] — Goblin voice: "[false belief]"
2. [Struggle] — Goblin voice: "[false belief]"
3. [Struggle] — Goblin voice: "[false belief]"
**Treasure:** [Micro-outcome after scaling this wall]

### Wall 3: [Name]
**Struggles:**
1. [Struggle] — Goblin voice: "[false belief]"
2. [Struggle] — Goblin voice: "[false belief]"
3. [Struggle] — Goblin voice: "[false belief]"
**Treasure:** [Micro-outcome after scaling this wall]

### The Culprit
[The big enemy — the overarching force that creates these walls]

## Content Layers Checklist
- Layer 1: Outcomes, Problems, Mechanisms
- Layer 2: Experiences, Opinions, Worldviews
- Layer 3: Identity, Transformation, Becoming

## Content Ecosystem
- **BVA:** [Description of cornerstone content covering the full bridge]
- **Long form:** [Platform] — covers walls and struggles in depth (all 3 layers)
- **Short form:** [Platform] — covers specific struggles, goblin voices, micro-wins (1-2 layers)
- **Email:** [How email fits into the ecosystem]
- **Flow:** Short form catches attention → Long form builds understanding → BVA shows full picture → Offer is there when ready

## Platform & Rhythm
[Note: Platform, rhythm, and communication style are set during content strategy planning, not here. See boring-content-strategy.]

## How Content Connects to Your Offer
[How the Bridge naturally leads people toward the Creation — the cattle pen, not the funnel]
```

Populate every section using the answers from the discovery questions. Do not leave placeholders.

### Step 7: Transition

After saving, tell the user:

> "Your Conversation is saved to `world-code/conversation.md`. Next up is your **Crossing** — the last piece. This is how someone goes from discovering your world to becoming part of it. The bridge from content to customer. Want to continue to Crossing now, or take a break and come back later?"

- If they want to continue, invoke `/world-crossing`.
- If they want a break, tell them they can return anytime with `/world-code-start` and it will pick up where they left off.

## Key Principles

- **One question at a time.** Never batch questions. Wait for each answer.
- **Build on their words.** Reference what they said in previous answers when framing the next question.
- **Push for specificity.** Vague walls and struggles make vague content. Hard outcomes, concrete struggles, and specific Goblin voices make content that resonates.
- **The Bridge is the content strategy.** Every piece of content comes from the Bridge. If they can't see how a wall generates content, the wall is wrong.
- **Content should naturally lead to the Creation.** The Conversation is not a sales funnel — it's a cattle pen. People circle, consume, and enter when ready. Great content makes the offer feel inevitable, not forced.
- **Reference their Climax, Method, and Creation.** The Outcome should connect to their Climax. The Walls should map to their Method. The offer at the end of the Bridge should be their Creation.
- **Apply their Voice.** Use the tone, rhythm, hard rules, and authenticity markers from `world-code/voice.md` when creating the Bridge and all content descriptions.
