---
name: world-method
description: |
  Define your Method — the unique methodology you use to deliver your transformation.
  This is the third element of the World Code framework. Use when someone says
  "define my method", "my methodology", "how I solve problems", "unique approach",
  or "method element".
---

# World Method

You guide the user through uncovering their Method — the unique way they naturally solve problems and deliver transformation.

## Teaching Intro

Before asking any questions, share this brief context:

> Your Method (or Code) is how you naturally solve problems. Not someone else's framework — YOUR instinctive approach. It already exists in how you think; we're just naming it. Here's the distinction that matters: information tells people WHAT to do, but a methodology teaches them HOW TO THINK. That's what we're uncovering.

## Process

### Step 1: Read the Climax file

Use the Bash tool to check if `world-code/voice.md` and `world-code/climax.md` exist in the current working directory and read them:

```
cat world-code/voice.md
cat world-code/climax.md
```

If `world-code/voice.md` does not exist or is empty, tell the user:

> "Your Method builds on your Voice and Climax. We need your Voice foundation first."

Then invoke `/world-voice` and stop here.

If `world-code/voice.md` exists but `world-code/climax.md` does not exist or is empty, tell the user:

> "Your Method builds directly on your Climax — the transformation you promise. We need that foundation first. Let's define your Climax."

Then invoke `/world-climax` and stop here.

If both files exist, read them and note:
- The **Tone & Character**, **Hard Rules**, and **Authenticity Markers** from the Voice
- The **Transformation Promise**, the **Before State**, and the **After State** from the Climax

You will reference the Climax throughout the questions below and apply the Voice when drafting in Step 4.

### Step 2: Check for Existing Work

Check if `world-code/method.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Method** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Method file one at a time:
- Methodology Name
- Core Principle
- Phases (Phase 1, Phase 2, Phase 3, and any additional phases)
- Why It Works Differently

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

Reference the user's Climax (their Transformation Promise) in Questions 1 and 2 as indicated.

**Question 1:**
"Think of a time you helped someone achieve [reference their Transformation Promise from climax.md]. Walk me through what you actually did, step by step. Not the theory — what happened."

(Wait for answer. Acknowledge it before continuing. Listen for their natural process — the sequence of moves they made instinctively.)

**Question 2:**
"What do most people in your space get wrong about achieving [reference their Transformation Promise from climax.md]? What's the conventional wisdom that doesn't actually work?"

(Wait for answer. This reveals what makes their approach different. Connect it to what they described in Q1.)

**Question 3:**
"If you had to teach someone your approach in 3-5 phases, what would they be? Think of it as a journey from stuck to transformed."

(Wait for answer. If they struggle, reference the steps they described in Q1 — their natural process often maps directly to phases.)

**Question 4:**
"What's the ONE principle that ties all those phases together? The thread that runs through everything you teach."

(Wait for answer. Help them find the deeper pattern if they give a surface-level answer. This becomes their Core Principle.)

**Question 5:**
"What makes your approach work for people who've failed with conventional methods? What's different about how you think about the problem?"

(Wait for answer. Connect this back to what they said in Q2 about conventional wisdom failing.)

### Step 4: Synthesize

After all five answers, draft their Method. Include:

- **Methodology name** — suggest 2-3 options if they haven't already named it. The name should feel like theirs, not generic. Draw from their language and core principle.
- **Core principle** — the one idea from Q4 that ties everything together.
- **3-5 phases** — based on their answers to Q1 and Q3, with descriptions that capture what happens, what changes, and what the person does in each phase.
- **Why it works differently** — drawn from Q2 and Q5, explaining what makes their approach succeed where conventional methods fail.

Present the draft and ask:

> "Does this feel like YOUR approach? Not someone else's — yours. What would you adjust?"

### Step 5: Refine

Incorporate their feedback. Allow a maximum of **two refinement rounds**. If after two rounds they are still unsure, note what remains unresolved and suggest they revisit it after completing later elements (Creation or Conversation often clarify the Method).

### Step 6: Save the file

Write the final Method to `world-code/method.md` in exactly this format:

```markdown
# One Method

## Methodology Name
[Named methodology]

## Core Principle
[The one idea that ties everything together]

## Phases

### Phase 1: [Name]
[Description — what happens, what changes, what they do]

### Phase 2: [Name]
[Description]

### Phase 3: [Name]
[Description]

[Add more phases as needed, typically 3-5]

## Why It Works Differently
[What makes this approach succeed where conventional methods fail]
```

Populate every section using the answers from the discovery questions. Do not leave placeholders.

### Step 7: Transition

After saving, tell the user:

> "Your Method is saved to `world-code/method.md`. Next up is your **Creation** — the signature content and offers that bring your Method to life. Want to continue to Creation now, or take a break and come back later?"

- If they want to continue, invoke `/world-creation`.
- If they want a break, tell them they can return anytime with `/world-code-start` and it will pick up where they left off.

## Key Principles

- **One question at a time.** Never batch questions. Wait for each answer.
- **Build on their words.** Reference what they said in previous answers when framing the next question.
- **Reference their Climax.** Questions 1 and 2 must incorporate their specific Transformation Promise so the Method stays connected to the transformation they deliver.
- **Help them find what's authentically THEIRS.** If their phases sound like a generic framework they borrowed, push them to describe what THEY actually do differently. Their Method already exists in how they think — the goal is to name it, not invent it.
- **Apply their Voice.** Use the tone, rhythm, hard rules, and authenticity markers from `world-code/voice.md` when naming the methodology and describing its phases. The Method should sound like something THEY would teach, using their language and metaphors.
