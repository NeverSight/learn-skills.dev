---
name: call-coaching-scorecard
description: "Use this skill when a manager or rep wants feedback on sales calls: \"score this call\", \"review my discovery call transcript\", \"coaching feedback for my SDR\", \"build a call scorecard\". Scores a call transcript or notes on opening, discovery, listening, value, objection handling and next step, quotes the moments that mattered, picks the one skill to work on next, and gives a concrete drill. Also builds a team scorecard so coaching is consistent across managers."
license: MIT
metadata:
  title: Call coaching scorecard
  category: enablement
  tags: "Sales Leaders, SDR, Sales"
  author: prosyo
  version: "1.0.0"
  keywords: "sales call scorecard, call coaching template, discovery call review, claude call coaching skill, sales coaching feedback"
  inputs: "Call transcript or notes, Call type and goal, Rep level"
  outputs: "Scorecard, Quoted moments, One focus skill, Practice drill"
---

Use this after calls worth learning from: a first call, a lost deal, a new rep's first week. Coaching works when it is specific, quoted and focused on one thing at a time.

## Inputs

- The transcript (or detailed notes).
- Call type (cold call, discovery, demo, negotiation) and its goal.
- The rep's experience level.

## The play

### 1. Measure the basics
Talk ratio (rep vs buyer), number of questions asked, longest rep monologue, whether a next step was booked. Talk ratio over 60% on a discovery call is a red flag on its own.

### 2. Score the dimensions (1-4)
| Dimension | What 4 looks like |
| --- | --- |
| Opening | Clear agenda, buyer adds to it, permission to ask questions |
| Discovery | Layered questions to impact and priority; follow-ups on answers |
| Listening | Paraphrases, uses the buyer's words, does not interrupt |
| Value | Connects the product to the buyer's stated problem, with proof |
| Objections | Clarifies before answering; calm; checks the answer landed |
| Next step | Specific, dated, agreed on the call, with the right people |

Read [references/scorecard-rubric.md](references/scorecard-rubric.md) for the full rubric per call type and example quotes for each score.

### 3. Quote the moments
Two strengths and two misses, each with the exact quote and timestamp, and what a better line would have been.

### 4. Pick one focus
The single skill that would most change results on the next five calls. Usually the earliest weak stage: weak discovery causes weak value and weak next steps.

### 5. Give a drill
A 10-15 minute exercise for the focus skill: rewrite three questions, a role-play of the missed moment, or listen to a great call and note how the top rep handled the same moment.

## Output format

```
Call: <type> | <rep> | <date>   Goal: <...>   Outcome: <next step or not>
Talk ratio: x% | Questions: N | Longest monologue: N min
Scores: Opening x | Discovery x | Listening x | Value x | Objections x | Next step x
Strengths: <quote - why it worked> x2
Misses: <quote - better line> x2
Focus for next calls: <one skill>
Drill: <exercise>
```

## What good looks like

- Feedback quotes the call; no "be more consultative" without an example.
- One focus, not ten notes.
- Praise is as specific as criticism.
- The common mistake is scoring everything and changing nothing: a manager who gives seven pieces of feedback gets none of them applied.

## Rules

- MUST quote the call for every strength and miss.
- MUST pick one focus skill.
- MUST respect call-recording consent and keep transcripts private to the rep and their manager.
- NEVER share a rep's scores publicly or compare reps by name in team settings.

## Example prompts

- "Score this discovery call transcript and give me one thing to work on."
- "Build a call scorecard our 4 managers can use consistently."
- "Review my cold calls from today; I keep losing them at 'send me an email'."
