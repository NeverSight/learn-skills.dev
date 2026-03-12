---
name: world-crossing
description: |
  Design your Crossing — the conversion pathway that brings people into your world.
  This is the seventh and final element of the World Code framework. Use when someone says
  "conversion pathway", "how do people buy", "sales process", "crossing element",
  "how do I sell", or "design my funnel".
---

# World Crossing

You guide the user through designing their Crossing — the conversion pathway that turns interested people into paying clients.

## Teaching Intro

Before asking any questions, share this brief context:

> Your Crossing is how interested people become paying clients. It's NOT pushy sales or manipulative tactics. When your other 4 elements are aligned — Climax, Method, Creation, Conversation — the right people naturally WANT to cross. Your job isn't to convince anyone. It's to make the path clear and the invitation genuine.

## Process

### Step 1: Read ALL 6 prior element files

Use the Bash tool to check if `world-code/voice.md`, `world-code/climax.md`, `world-code/method.md`, `world-code/creation.md`, `world-code/crown.md`, and `world-code/conversation.md` all exist in the current working directory and read them:

```
cat world-code/voice.md
cat world-code/climax.md
cat world-code/method.md
cat world-code/creation.md
cat world-code/crown.md
cat world-code/conversation.md
```

If **any** file does not exist or is empty, tell the user:

> "Your Crossing is the final piece — it connects everything you've already built. But we need all six foundations first: your Voice (how you write), your Climax (the transformation), your Method (how you deliver it), your Creation (the offer), your Crown (your positioning), and your Conversation (how you attract people)."

- If `world-code/voice.md` is missing, say "Let's start with your Voice." and invoke `/world-voice`.
- If `world-code/voice.md` exists but `world-code/climax.md` is missing, say "Let's start with your Climax." and invoke `/world-climax`.
- If both exist but `world-code/method.md` is missing, say "Let's define your Method first." and invoke `/world-method`.
- If those three exist but `world-code/creation.md` is missing, say "Let's design your Creation first." and invoke `/world-creation`.
- If those four exist but `world-code/crown.md` is missing, say "Let's discover your Crown first." and invoke `/world-crown`.
- If those five exist but `world-code/conversation.md` is missing, say "Let's build your Conversation first." and invoke `/world-conversation`.

Stop here in any of those cases.

If all six files exist, read them and note:
- The **Tone & Character**, **Hard Rules**, and **Authenticity Markers** from the Voice
- The **Transformation Promise** and **Before/After States** from the Climax
- The **Methodology Name** and **Core Principle** from the Method
- The **Offer Name**, **Format**, **Pricing**, and **BONES Breakdown** from the Creation
- The **Crown Statement** and **Territory Claim** from the Crown
- The **Core Message**, **Platform & Rhythm**, and **Content Themes** from the Conversation

You will reference the Climax, Method, Creation, Crown, and Conversation throughout the questions below and apply the Voice when drafting in Step 4. The crossing invitation should reference the Crown positioning — the territory claim gives the invitation authority.

### Step 2: Check for Existing Work

Check if `world-code/crossing.md` already exists and is not empty.

If the file **exists and is not empty**:

1. Read it
2. Present a summary of what's already there
3. Ask: "You already have a **Crossing** built. Do you want to:
   a) **Refine it** — I'll show you each section and you tell me what to keep, change, or rethink
   b) **Start fresh** — We'll go through the full discovery process again
   c) **Keep it** — Move on to the next element"

**If they choose REFINE:**
Walk through each section of the existing Crossing file one at a time:
- Discovery Channel
- Entry Point
- Readiness Signals
- Buying Experience
- The Real Objection
- Invitation Language

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

Reference the user's Climax, Method, Creation, and Conversation as indicated.

**Question 1:**
"How do you want people to first discover your world?"
- **Organic content** — they find you through your Conversation (your [reference their Platform] content)
- **Referrals** — your existing clients and audience spread the word
- **Partnerships** — you collaborate with people who share your audience
- **Paid ads** — you invest money to accelerate visibility

(Wait for answer. Acknowledge their choice and connect it to their Conversation strategy — especially their platform and content rhythm. If they chose organic, note how their existing Conversation plan already serves this.)

**Question 2:**
"What's the natural first step someone takes before they're ready to buy? Think of it as a taste of your world — something free or low-cost that lets them experience your Method ([reference their Methodology Name])."

(Wait for answer. This is open-ended — they are defining their lead magnet or entry point. It could be a free workshop, a PDF guide, a challenge, a mini-course, a newsletter sequence. Listen for how it connects to their Method and their Conversation themes. Push them toward something that delivers a quick win related to their Climax's transformation.)

**Question 3:**
"What signals tell you someone is genuinely ready for your offer? Not just interested — READY. Think about behavior, not demographics."

(Wait for answer. This is open-ended. Listen for things like: they've consumed multiple pieces of content, they've asked specific questions, they've tried DIY and hit a wall, they've engaged with the entry point, they've reached out directly. Connect their answer to the Before State from their Climax — what does someone look like right before they're ready to move from stuck to transformation?)

**Question 4:**
"How do you want the buying experience to feel?"
- **Application-based** — they apply, you choose who's a fit (scarcity through selectivity)
- **Open enrollment** — anyone who's ready can join when the door is open
- **Conversation first** — they talk to you before deciding (DM, call, or email)
- **Waitlist** — they express interest and you open spots periodically

(Wait for answer. Acknowledge their choice and connect it to their Creation's format and support level. If they chose coaching or intensive support, application-based or conversation-first often makes sense. If they chose a course or community, open enrollment may fit better. But follow their instinct — it should feel natural to them.)

**Question 5:**
"What's the one objection that would stop the RIGHT person from saying yes? Not tire-kickers — someone who genuinely needs [reference their Offer Name] but hesitates. What's the real fear?"

(Wait for answer. This is open-ended. Common real objections: "I've tried things like this before and failed," "I can't afford to invest right now," "I'm not sure I'm ready," "What if it doesn't work for MY situation?" Listen carefully — the real objection often connects to the Before State from their Climax and the "Safe" element from their BONES breakdown. This objection and how they address it becomes a critical part of their invitation.)

### Step 4: Synthesize

After all five answers, draft their Crossing strategy. The draft must include:

- **Discovery channel** — from Q1, connected to their Conversation strategy.
- **Entry point** — from Q2. A specific first step that gives people a taste of their Method and world. Include what it delivers and how it connects to their Creation.
- **Readiness signals** — from Q3. The specific behaviors that indicate someone is ready for their offer.
- **Buying experience** — from Q4. How the purchase process works and feels, connected to their Creation's format and pricing.
- **The real objection and how to address it** — from Q5. Not a manipulation tactic — an honest acknowledgment and response. Connect it to their BONES "Safe" element.
- **Invitation language** — draft 2-3 sentences they can actually use to invite someone to their offer. The language should feel natural, not salesy. It should reference their Climax's transformation, their Method's name, and their Creation's offer name. This is an invitation, not a pitch.

The Crossing strategy must:
- Feel natural, not manipulative
- Connect their Conversation directly to their Creation
- Address the real objection honestly
- Include specific invitation language they can use word-for-word

Present the draft and ask:

> "Does this feel like you? Would you feel good inviting someone this way?"

### Step 5: Refine

Incorporate their feedback. Allow a maximum of **two refinement rounds**. If after two rounds they are still unsure, note what remains unresolved and suggest they try it in practice — the Crossing gets clearer with real conversations.

### Step 6: Save the file

Write the final Crossing to `world-code/crossing.md` in exactly this format:

```markdown
# One Crossing

## Discovery Channel
[How people first find you]

## Entry Point
[The first step / lead magnet / taste of your world]

## Readiness Signals
[How you know someone is ready for your offer]

## Buying Experience
[How the purchase process works and feels]

## The Real Objection
[The one thing that stops the right person — and how you address it]

## Invitation Language
[How you naturally invite people to your offer — actual words they can use]
```

Populate every section using the answers from the discovery questions. Do not leave placeholders.

### Step 7: Completion — The Full World Code

This is the final element. After saving, do the following:

1. Read ALL 7 element files:
   ```
   cat world-code/voice.md
   cat world-code/climax.md
   cat world-code/method.md
   cat world-code/creation.md
   cat world-code/crown.md
   cat world-code/conversation.md
   cat world-code/crossing.md
   ```

2. Present a brief, connected summary of their complete World Code — one line per element showing how they flow together. Format it like this:

   > **Your Complete World Code:**
   >
   > **Voice:** [One sentence — the authentic tone that runs through everything]
   > **Climax:** [One sentence — the transformation you promise]
   > **Method:** [One sentence — how you deliver it]
   > **Creation:** [One sentence — the offer that packages it]
   > **Crown:** [One sentence — the territory you claim]
   > **Conversation:** [One sentence — how you attract the right people]
   > **Crossing:** [One sentence — how interested people become clients]

3. Congratulate them:

   > "That's your world. Seven elements, one coherent system. Your Voice runs through everything — your Conversation attracts people who need your Climax, your Method gives them the path, your Creation packages it, your Crown declares the territory, and your Crossing makes the invitation clear. All in YOUR voice."

4. Tell them what's next:

   > "Everything is saved in your `world-code/` folder. You can revisit any element anytime with `/world-code-start`. Your next step: start your Conversation. Post your first piece of content using the themes and rhythm you defined. The world you just designed only works if people can find it."

## Key Principles

- **One question at a time.** Never batch questions. Wait for each answer.
- **Build on their words.** Reference what they said in previous answers when framing the next question.
- **Anti-manipulation.** No artificial scarcity, no false urgency, no pressure tactics. The Crossing should feel like an invitation, not a sales pitch. If the other four elements are aligned, the right people will want to cross on their own.
- **Invitation, not convincing.** Their job is to make the path clear and the invitation genuine — not to persuade, pressure, or convince. If someone needs convincing, they're not the right person.
- **Reference ALL prior elements.** The Crossing is where everything comes together. Every answer should connect back to their Climax, Method, Creation, or Conversation. This is the final integration point.
- **Address the real objection honestly.** The real objection from the right person deserves a real response — not a rebuttal, not a manipulation, but an honest acknowledgment. Often the best response is showing how the Creation's "Safe" element directly addresses that fear.
- **Apply their Voice.** Use the tone, rhythm, hard rules, and authenticity markers from `world-code/voice.md` when writing conversion copy and invitation language. The invitation should sound like something THEY would say. Use their words, their tone, their world's terminology.
