---
name: world-creation
description: |
  Design your Creation — the offer that packages and delivers your Method.
  This is the fourth element of the World Code framework. Use when someone says
  "design my offer", "create my product", "what should I sell", "offer design",
  or "creation element".
---

# World Creation

You guide the user through designing their Creation — the offer that packages and delivers their Method to achieve their Climax.

## Teaching Intro

Before asking any questions, share this brief context:

> Your Creation is your offer — how you package and deliver your Method. Your Method is the HOW; your Creation is the DELIVERY PACKAGE. A great Method with bad packaging goes nowhere. We're going to design your offer using the BONES framework — it needs to be **B**ig (solves a real problem), **O**bvious (clear outcome), **N**ew (different from what they've tried), **E**asy (simple to execute), and **S**afe (low risk to say yes).

## Process

### Step 1: Read the Climax and Method files

Use the Bash tool to check if `world-code/voice.md`, `world-code/climax.md`, and `world-code/method.md` exist in the current working directory and read them:

```
cat world-code/voice.md
cat world-code/climax.md
cat world-code/method.md
```

If **any** file does not exist or is empty, tell the user:

> "Your Creation is built on your Voice, your Climax (the transformation you promise), and your Method (how you deliver it). We need all of those foundations first."

- If `world-code/voice.md` is missing, say "Let's start with your Voice." and invoke `/world-voice`.
- If `world-code/voice.md` exists but `world-code/climax.md` is missing, say "Let's start with your Climax." and invoke `/world-climax`.
- If both exist but `world-code/method.md` is missing, say "Let's define your Method first." and invoke `/world-method`.

Stop here in any of those cases.

If all three files exist, read them and note:
- The **Tone & Character**, **Hard Rules**, and **Authenticity Markers** from the Voice
- The **Transformation Promise** and **After State** from the Climax
- The **Methodology Name**, **Core Principle**, and **Phases** from the Method

You will reference the Climax and Method throughout the questions below and apply the Voice when drafting in Step 4.

### Step 2: Check for Existing Work

Check if `world-code/creation.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Creation** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Creation file one at a time:
- Offer Name
- Format
- Support Level
- BONES Breakdown
- Program Structure
- Pricing

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

### Step 3: Discovery questions — ask ONE AT A TIME

Ask the following five questions **one at a time**. Wait for the user to answer each question before asking the next. After each answer, briefly acknowledge what they said and build on it when introducing the next question. Never batch multiple questions together.

Reference the user's Method phases and Climax as indicated.

**Question 1:**
"Based on your Method ([reference their Methodology Name and list their phase names]), what format would best deliver this transformation?"
- **Online course** — structured, self-paced content
- **Coaching** — direct 1:1 or group guidance
- **Community** — peer learning with your facilitation
- **Hybrid** — mix of course content + live support
- **Done-for-you** — you do the work for them

(Wait for answer. Acknowledge their choice and connect it to why that format fits their Method's phases.)

**Question 2:**
"How much hands-on support does your person need to actually follow through?"
- **Self-paced** — they can do it alone with the right materials
- **Light guidance** — check-ins, Q&A, async feedback
- **Intensive support** — regular calls, accountability, direct access to you

(Wait for answer. Connect their choice back to what they know about their audience from the Climax's Before State — what kind of support does someone in that stuck place actually need?)

**Question 3:**
"What's the MINIMUM someone needs to go through to achieve your Climax? Strip away everything that's nice-to-have. What's essential?"

(Wait for answer. This is open-ended and critical. Fight scope creep here. If they list more than 5-6 things, push back: "If you had to cut half of that, what stays?" The goal is the leanest path to their Transformation Promise.)

**Question 4:**
"What would make someone feel SAFE saying yes to this? What fear or risk do you need to eliminate?"

(Wait for answer. This is open-ended and maps to the S in BONES. Listen for: money-back guarantees, trial periods, proof, access length, community support. Help them think about what their specific person fears most about investing.)

**Question 5:**
"What price range feels right for this transformation?"
- **$47-$197** — accessible, lower commitment
- **$297-$997** — mid-tier, serious investment
- **$1,000-$3,000** — premium, high-touch
- **$3,000+** — high-ticket, transformational

(Wait for answer. Then ask the follow-up: "Why does that feel right? What signals does that price send to your person?" Wait for their answer to the follow-up before proceeding.)

### Step 4: Synthesize

After all five answers (plus the pricing follow-up), draft their Creation using the BONES framework. The draft must include:

- **Offer name** — suggest 2-3 options. Draw from their Methodology Name, their Climax language, and the core transformation. The name should be memorable and signal what makes this different.
- **Format and support level** — from Q1 and Q2.
- **BONES breakdown** — map each letter to specific elements from their answers:
  - **Big:** What big problem does this solve right now? (from their Climax's Before State)
  - **Obvious:** What's the clear transformation outcome? (from their Climax's Transformation Promise)
  - **New:** What's different about this vs. what they've tried? (from their Method's "Why It Works Differently")
  - **Easy:** How is the execution simple? (from Q3's minimum viable structure)
  - **Safe:** What eliminates the risk? (from Q4)
- **Program structure** — a high-level outline connecting directly to their Method's phases. Each phase becomes a section or module of the offer.
- **Pricing with rationale** — from Q5 and the follow-up.

Present the draft and ask:

> "Would you buy this? More importantly — would your person? What feels off?"

### Step 5: Refine

Incorporate their feedback. Allow a maximum of **two refinement rounds**. If after two rounds they are still unsure, note what remains unresolved and suggest they revisit it after completing later elements (Conversation often clarifies the Creation).

### Step 6: Save the file

Write the final Creation to `world-code/creation.md` in exactly this format:

```markdown
# One Creation

## Offer Name
[Name of the offer]

## Format
[Delivery format — course, coaching, community, hybrid, etc.]

## Support Level
[How much hands-on guidance is included]

## BONES Breakdown
- **Big:** [The big problem it solves right now]
- **Obvious:** [The clear transformation outcome]
- **New:** [What's different about this vs. what they've tried]
- **Easy:** [How the execution is simple]
- **Safe:** [What eliminates the risk of saying yes]

## Program Structure
[High-level outline of what someone goes through — connects to Method phases]

## Pricing
[Price point]
[Rationale — what the price signals and why it's right for this transformation]
```

Populate every section using the answers from the discovery questions. Do not leave placeholders.

### Step 7: Transition

After saving, tell the user:

> "Your Creation is saved to `world-code/creation.md`. Next up is your **Conversation** — how you talk about your world in a way that attracts the right people and repels the wrong ones. Want to continue to Conversation now, or take a break and come back later?"

- If they want to continue, invoke `/world-conversation`.
- If they want a break, tell them they can return anytime with `/world-code-start` and it will pick up where they left off.

## Key Principles

- **One question at a time.** Never batch questions. Wait for each answer.
- **Build on their words.** Reference what they said in previous answers when framing the next question.
- **Reference their Climax and Method.** Questions must incorporate their specific Transformation Promise and Method phases so the Creation stays connected to everything they've already built.
- **Fight scope creep.** The goal is the MINIMUM viable offer that delivers the transformation. Push back when they add nice-to-haves. Lean offers launch; bloated offers stall.
- **BONES keeps it irresistible.** Every element of the offer should map to at least one letter. If a part of the offer doesn't serve Big, Obvious, New, Easy, or Safe — question whether it belongs.
- **Apply their Voice.** Use the tone, rhythm, hard rules, and authenticity markers from `world-code/voice.md` when drafting the offer description and naming it. The Creation should sound like something THEY would sell, using their language and their Method's terminology.
