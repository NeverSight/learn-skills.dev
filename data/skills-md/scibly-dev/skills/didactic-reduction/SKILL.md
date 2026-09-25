---
name: didactic-reduction
description: Didactic Reduction with AI — strip any topic down to its learning-essential core using the three filters from German educational science (Didaktische Reduktion). Use this skill when an L&D professional, instructional designer, or trainer is overwhelmed by too much content and needs to figure out what's truly essential to teach. Trigger when someone says things like "there's too much to cover", "the SME gave me 200 slides", "how do I cut this down", "what should I actually include", "I need to simplify this", "help me prioritize the content", "scope this training", or "what is didactic reduction". Also trigger for any task involving content reduction, curriculum trimming, or deciding what to leave out of a course or program.
---

# Didactic Reduction with AI

**The problem**: SMEs give you everything they know. Learners can absorb a fraction of it. Your job is to find the essential core — and cut everything else without losing meaning.

**Didactic reduction** (from the German educational science concept *Didaktische Reduktion*) means reducing content to the minimum a learner must understand to think and act correctly in this domain. Not the minimum you can get away with — the minimum that preserves integrity.

## Step 1 — Understand the situation

Ask the user:

1. **What's the raw material?** (Ask them to paste or describe it — a document, slide deck overview, SME notes, existing course outline)
2. **Who is the learner?** (role, experience level, what they already know)
3. **What do learners need to be able to DO after this?** One concrete action, decision, or behavior — not a list.
4. **How much time do learners have?** (5 minutes? 30 minutes? A half-day?)
5. **Is this reference content or memory content?** (Do learners need it in their heads, or will it be available while working?)

## Step 2 — Apply the three filters

Walk the user through the three filters before touching a single piece of content:

| Filter | The question | What to keep |
|--------|-------------|--------------|
| **Exemplary** | Does this represent a whole class of situations? | One example that teaches the principle — not five examples of the same thing |
| **Representative** | Does this reflect how learners actually encounter it on the job? | Real-world relevant content; cut textbook definitions that don't transfer |
| **Transferable** | Can the learner use this to handle novel situations they haven't seen before? | Principles and mental models; cut procedures that only work in one specific context |

## Step 3 — Run the scoping

Apply the three filters to the user's content and produce:

```
CONTENT SCOPING OUTPUT

Topic: [what this covers]
Learner: [who, doing what, with what background]
Available time: [X minutes/hours]
Performance goal: [what the learner must be able to DO]

THE ESSENTIAL CORE
(Maximum 3 things the learner must internalize)

1. [Concept/principle — framed as why it matters, not just what it is]
2. [Concept/principle]
3. [Concept/principle]

THE ONE REPRESENTATIVE EXAMPLE
[The single example that best illustrates the essential core for this audience and context]

WHAT TO CUT
- [Content item] — reason: [already known / textbook only / nice-to-know / too specialized]
- [Content item] — reason: [...]

WHAT BECOMES A REFERENCE (not training)
[Things learners don't need memorized but should be able to look up]

DRAFT LEARNING OBJECTIVE
After this, learners will be able to: [action verb + what they do + in what context]
```

## Step 4 — Hold the line on cuts

After producing the scope, ask: "Does this feel right? Often the hardest part is letting go of content that's interesting but not essential. Is there anything in the cut list you're worried about removing?"

Help the user distinguish:
- "This might be useful" ≠ essential
- "The SME will be upset" ≠ essential
- "It's in the current course" ≠ essential

The test: if a learner skips this, will they fail at the performance goal? If no, it's a cut.

## Step 5 — The didactic reduction prompt to take away

```
DIDACTIC REDUCTION PROMPT

Role: You are an expert instructional designer.
Learner: [role, experience level, what they already know]
Available learning time: [X minutes/hours]
Performance goal: The learner must be able to [action] in [context].

Review the following content and apply three filters:
1. EXEMPLARY: Keep content that represents a whole class of situations. Collapse multiple similar examples into one.
2. REPRESENTATIVE: Keep only content the learner will encounter in their actual job. Remove textbook definitions they won't use.
3. TRANSFERABLE: Keep principles and mental models. Remove procedures that only work in one specific situation.

Output:
- The 3 essential concepts/principles (maximum) the learner must internalize
- The single most representative example
- A list of what to cut and why
- What belongs in a reference document, not in training
- One learning objective using an action verb

[PASTE YOUR RAW CONTENT HERE]
```
