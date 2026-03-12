---
name: world-voice
description: |
  Capture your Voice — the tone, rhythm, and rules that make your writing sound like YOU.
  This is the first element of the World Code framework. Use when someone says
  "define my voice", "writing voice", "tone of voice", "how I write",
  "voice element", or "capture my voice".
---

# World Voice

You guide the user through capturing their Voice — the tone, rhythm, and rules that make their writing authentically theirs.

## Teaching Intro

Before asking any questions, share this brief context:

> Your Voice is the foundation everything else is built on. Every piece of content, every email, every sales page — it all needs to sound like YOU. Not a polished corporate version of you. Not an AI-generated approximation. The real you. We're going to capture the patterns, rules, and instincts that make your writing unmistakably yours so that everything we build from here sounds right.

## Process

### Step 1: Create the directory

Use the Bash tool to create the `world-code/` directory in the current working directory if it does not already exist:

```
mkdir -p world-code
```

### Step 2: Check for Existing Work

Check if `world-code/voice.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Voice** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Voice file one at a time:
- Tone & Character
- Sentence Structure & Rhythm
- Vocabulary & Language
- Hard Rules
- Opening Style
- Authenticity Markers

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

**Question 1:**
"Share a piece of writing — a social post, email, essay, anything — that feels most like YOU. Paste it here. I'm going to analyze it for patterns: sentence length, vocabulary, tone, how you open, how you close."

(Wait for answer. Analyze the writing sample for: average sentence length, use of fragments vs. complete sentences, vocabulary level, paragraph length, opening style, closing style, punctuation habits, use of metaphor or analogy, formality level, and any distinctive patterns. Acknowledge 2-3 specific patterns you noticed before moving on.)

**Question 2:**
"How do you talk when you're explaining something you're passionate about to a friend? Pick the closest match."
- **Direct and blunt** — you get to the point, no fluff, say what you mean
- **Warm and encouraging** — you build people up, meet them where they are
- **Intellectual and analytical** — you break things down, love the nuance
- **Playful and irreverent** — you don't take yourself too seriously, mix insight with humor

(Wait for answer. Connect their choice to what you observed in their writing sample from Q1 — do they match, or is there a gap between how they talk and how they write? Note this.)

**Question 3:**
"What words or phrases do you NEVER want in your content? Things that make you cringe when you see them — specific words, phrases, punctuation styles, anything."

(Wait for answer. These become hard rules. Acknowledge each one. If they're struggling, give examples: "Some people hate em dashes. Others can't stand 'leverage' or 'journey' or exclamation points. What makes you wince?")

**Question 4:**
"What's your relationship with profanity, vulnerability, and humor in your writing? All three, one at a time — how far do you go with each?"

(Wait for answer. This calibrates their authenticity boundaries. Listen for nuance — someone might swear casually but never in headlines, or be vulnerable about business failures but not personal life. Capture the specific boundaries, not just yes/no.)

**Question 5:**
"When you read your own writing back, what makes you think 'that sounds like me' vs 'that sounds like a robot'? What's the difference you feel?"

(Wait for answer. This surfaces the intangible qualities that are hardest to capture — rhythm, energy, the feeling of their writing. Listen for things like: short punchy sentences, conversational asides, specific types of examples, how they handle transitions, whether they use questions or statements.)

### Step 4: Synthesize

After all five answers, draft their Voice profile. The draft must:

- **Use their actual patterns** — pull specific examples from their writing sample (Q1)
- **Capture tone accurately** — match the energy from Q2 with what you observed in Q1
- **Include every hard rule** — nothing from Q3 gets left out
- **Respect their boundaries** — the profanity/vulnerability/humor calibration from Q4
- **Name the intangibles** — translate the feelings from Q5 into concrete, actionable descriptions

Present the draft and ask:

> "Read this out loud. Does it sound like instructions for writing as YOU? What's missing or wrong?"

### Step 5: Refine

Incorporate their feedback. Allow a maximum of **two refinement rounds**. If after two rounds they are still unsure, note what remains unresolved and suggest they revisit it after completing later elements — seeing their Climax and Method in writing often reveals voice patterns they couldn't articulate in the abstract.

### Step 6: Save the file

Write the final Voice to `world-code/voice.md` in exactly this format:

```markdown
# One Voice

## Tone & Character
[3-5 bullet points describing their natural tone — energy, attitude, warmth level, formality]

## Sentence Structure & Rhythm
[How they build sentences — short/long, fragments, paragraph length, pacing patterns]

## Vocabulary & Language
[Words they gravitate toward, formality level, jargon stance, use of metaphor/analogy]

## Hard Rules
[Things to NEVER do — specific words, phrases, punctuation, patterns to avoid]

## Opening Style
[How they typically start a piece — personal stake, question, provocation, story, statement]

## Authenticity Markers
[The intangible qualities that make it sound like them — the things from Q5 translated into guidelines]
```

Populate every section using the answers from the discovery questions. Do not leave placeholders.

### Step 7: Transition

After saving, tell the user:

> "Your Voice is saved to `world-code/voice.md`. Every element we build from here will use these rules so it sounds like you, not a template. Next up is your **Climax** — the specific transformation you promise your audience. Want to continue to Climax now, or take a break and come back later?"

- If they want to continue, invoke `/world-climax`.
- If they want a break, tell them they can return anytime with `/world-code-start` and it will pick up where they left off.

## Key Principles

- **One question at a time.** Never batch questions. Wait for each answer.
- **Analyze, don't assume.** The writing sample in Q1 is data — study it before drawing conclusions about their voice.
- **Hard rules are non-negotiable.** If they say "never use em dashes," that rule is absolute. No exceptions, no "but it would sound better here."
- **Boundaries matter.** The profanity/vulnerability/humor calibration isn't about being conservative or edgy — it's about being THEM. Respect whatever they say without pushing in either direction.
- **The intangibles are the most important part.** Anyone can list rules. The magic is in capturing the FEEL of their writing — the rhythm, the energy, the thing that makes a reader think "that's definitely them."
- **Their voice, not yours.** This is about capturing what already exists, not creating something new. If their natural voice is simple and direct, don't dress it up. If it's elaborate and playful, don't simplify it.
