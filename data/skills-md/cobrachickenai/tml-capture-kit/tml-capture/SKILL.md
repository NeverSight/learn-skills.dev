---
name: tml-capture
description: "End-to-end architecture capture. Takes a context dump and/or conversation, produces an architecture map, inferences document, changelog, agent brief, and opportunity analysis. Orchestrates tml-extract, tml-interview, tml-infer, tml-map, tml-so-what, and tml-hygiene in one seamless experience. The user sees one flow; the skills compose underneath. This is the primary entry point — invoke this skill, not the sub-skills directly."
license: MIT
metadata:
  author: Michael Schartung
  repository: CobraChickenAI/tml-capture-kit
  version: "2.0.0"
  pipeline: tml-capture-pipeline
  pipeline-role: orchestrator
  pipeline-definition: pipeline.yaml
  inputs: context-dump
  outputs: "the-map, the-changelog, the-agent-brief, inferences-document, so-what-analysis, conversation-log, hygiene-report"
---

# TML Capture

One conversation. One flow. A complete architecture capture with visible reasoning and actionable opportunities.

**What the user experiences:** "Give me your docs, I'll ask a few questions, you get back a map of what you do, what I concluded about your structure, and where the opportunities are."

**What happens underneath:** Six skills compose in sequence — extract, interview, infer, map, so-what, hygiene.

## When to Use

- Someone wants to map their business, team, process, or system
- You want the full end-to-end flow without invoking skills manually
- You're introducing this approach to someone new

## The Flow

```
┌──────────┐   ┌───────────┐   ┌──────────┐   ┌─────────┐   ┌──────────┐   ┌──────────┐
│ CONTEXT  │──▶│ INFORMED  │──▶│ SURFACE  │──▶│  THREE  │──▶│  "SO    │──▶│ QUALITY  │
│ DUMP     │   │ INTERVIEW │   │INFERENCES│   │ARTIFACTS│   │  WHAT?" │   │  GATE    │
│          │   │           │   │          │   │         │   │         │   │          │
│tml-      │   │tml-       │   │tml-infer │   │tml-map  │   │tml-so-  │   │tml-      │
│extract   │   │interview  │   │          │   │         │   │what     │   │hygiene   │
└──────────┘   └───────────┘   └──────────┘   └─────────┘   └──────────┘   └──────────┘
   10 min          10 min           auto           auto          auto          auto
```

**Total time for the human: ~20 minutes.** Extraction, inference capture, and artifact generation happen automatically.

## Step by Step

### Step 1: Gather Context

**What to say:**

> "What I'd like to do is build a clear map of [what they want to map]. To start, can you share whatever you've got — documents, SOPs, wiki pages, process descriptions, org charts, anything that describes how it works? Don't worry about format or completeness. Whatever you have is a starting point."

**Accept anything:**
- Pasted text
- File paths or uploaded documents
- Links to internal wikis (you'll need the content, not just the URL)
- "Let me just describe it" (this is fine — skip to Step 2 in cold-start mode)

**If they provide content:** Run `tml-extract` silently. Don't narrate the extraction process. Just read, extract, and prepare for the interview.

**If they have nothing to share:** That's okay. Proceed in cold-start interview mode.

### Step 2: The Conversation

**Warm-start (content was provided):**

> "Okay, I've read through what you shared. Here's what I think I'm seeing..."

Present a brief, conversational summary of the extraction. Not a data dump — a playback:

> "It looks like [scope] has a few main areas: [domains]. The core things that happen are [top capabilities]. The people involved are [archetypes]. And there seem to be some important rules around [policies]."
>
> "How close am I?"

Then run `tml-interview` in warm-start mode. Focus on:
1. Corrections
2. Confirmations (move fast)
3. Gap-filling (specific questions, not generic)
4. Surfacing implicit knowledge

**Cold-start (no content provided):**

> "No problem. Let's just talk through it. What are we describing today?"

Run `tml-interview` in cold-start mode.

**Interview pacing:**
- Don't ask all phases back-to-back like an interrogation
- Let them talk. Follow their thread.
- When they naturally touch on a primitive, capture it and move on
- The phases are a checklist for YOU, not a script for THEM
- Aim for 10-15 minutes, not 30

### Step 3: Surface Inferences

Before generating the map, run `tml-infer` against the confirmed primitives. This step makes the model's reasoning visible — separating what the human explicitly said from what the system concluded.

Present the Inferences document briefly:

> "Before I give you the full map, here's what I concluded vs. what you actually said. Take a look at the medium and low confidence items — if any of those are wrong, correct them now and the map will be right."

Allow corrections. Update the primitives accordingly. Then proceed.

### Step 4: Generate Artifacts

Once inferences are reviewed, generate the three artifacts using `tml-map`:

1. **The Map** — plain-language architecture document
2. **The Changelog** — provenance trail
3. **The Agent Brief** — operational instructions for AI

Present the Map first. It's the main deliverable.

> "Here's your map. Take a look — does this feel right? Anything jump out as wrong or missing?"

Allow one round of corrections. Update the map and changelog accordingly.

### Step 5: The "So What?"

Once the map is confirmed, run `tml-so-what`.

**Transition:**

> "Now that we have the map, let's look at what it tells us. Where are the opportunities? Where is the friction? Where can things get better?"

Present the So What? analysis. Lead with the summary and recommended starting point.

> "Based on what you described, here's what stands out..."

---

## What They Walk Away With

By the end of one session, the person has:

| Artifact | What It Is | Who It's For |
|----------|-----------|-------------|
| **The Map** | Plain-language architecture of their world | Everyone — shareable, readable, no jargon |
| **The Inferences** | What the system concluded vs. what was stated | The architect — the debugging surface |
| **The Changelog** | Provenance trail — where every element came from | Anyone who asks "where did this come from?" |
| **The Agent Brief** | Operational instructions for AI | Any AI agent that needs to work within this scope |
| **The So What?** | Grounded opportunities, friction points, quick wins | The person deciding what to do next |

## Tone for the Entire Flow

This is a conversation, not a consulting engagement. The person should feel like they're talking to a smart, curious colleague who happens to be really good at organizing information.

- **No jargon.** Not "primitives," not "TML," not "architecture" unless they use those words.
- **No formality.** "Here's what I see" not "The analysis reveals."
- **No overselling.** "This could save time" not "This will revolutionize your workflow."
- **Honest about gaps.** "I'm not sure about this part — can you clarify?" is always better than guessing.
- **Respect their time.** Move briskly. Don't belabor points they already confirmed. Don't ask questions the documents already answered.

## Edge Cases

### They only want part of the flow
Fine. The skills are composable:
- "I just want to describe it, no documents" → skip extract, run interview + map + so-what
- "I already have a map, just tell me the so-what" → run so-what standalone
- "Just extract what you can from this doc, I'll review later" → run extract only

### The scope is too big
If what they're describing is an entire company with 50 processes, focus:

> "That's a lot to map at once. Where would it be most useful to start? What's the area that's most confusing, most broken, or most important right now?"

Map one scope well. Then expand.

### They push back on the interview
Some people don't want to answer questions. They want to dump and get results. That's okay:

> "Tell you what — I'll work with what you've shared and generate a draft map. Then you can tell me what I got wrong."

Run extract → map with all candidates marked as "pending confirmation." Present the draft map and iterate from there. The interview becomes implicit in the correction process.

### Multiple participants
If mapping a team or process that spans people:
- Interview the primary owner first
- Note their perspective in the changelog
- Flag areas where other perspectives are needed
- Document who confirmed what

---

## The Pitch (How to Introduce This)

When offering this to someone at work:

> "I can help you create a clear map of [your process / your team's work / how this thing actually runs]. All I need is whatever docs you have — SOPs, wiki pages, whatever — and about 20 minutes of your time to fill in the gaps. You'll get back a clean document that shows what you do, who does it, what the rules are, and where the opportunities are. Interested?"

That's it. No tooling ask. No installation. No training. Just: give me your stuff, talk to me, get back a map.

---

*v2.0 — The orchestrator. One flow, six skills, seven artifacts (map + inferences + changelog + agent brief + so-what + conversation log + hygiene report).*
