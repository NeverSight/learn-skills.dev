---
name: ira-prompting
description: Apply the seven Intent-Result Alignment prompting techniques and score prompts with the IRA rubric. Use when instructing AI agents/coding assistants to write code, produce reports, or generate content with fewer wasted iterations.
version: 0.1.0
license: MIT
---

# IRA Prompting

IRA (Intent-Result Alignment) measures the gap between the Pilot's Vibe (the Mission Script) and the Machine's Output. IRA 100% means agents delivered exactly what was intended. IRA 60% means drift or hallucination crept in.

> Source: "Vibe Leading The AI: The Corporate Race Against Machines" (Jean Machuca). Framework concept: Intent-Result Alignment and the seven IRA techniques.

## The seven IRA techniques

### 1. Phase Contract
One goal per prompt. If a prompt contains more than three concerns, split it into phases. You can't measure alignment on five goals at once.

### 2. Delta Prompt
After the first prompt, describe only the change, in two to three sentences max. Do not re-wrap the whole context; re-explanation is how drift sneaks in.

### 3. Symptom Report
Describe what you see and let the AI diagnose. Do not tell it which code to change.

- **Bad:** "Change the useEffect in App.jsx to add a flag so the tooltip doesn't unmount."
- **Good:** "When the AI plays, the hover preview marker disappears as soon as the AI takes its turn."

### 4. Constraint-First
State security and limits in the first sentence. The opening line is the frame; put the must-nots there.

### 5. Design by Reference
Use the target technology's vocabulary. "Make it pop" is not CSS; "neon text-shadow" is. Speak the machine's language and the machine obliges.

### 6. Pivot Prompt
When the AI is on the wrong track, do not explain why it is wrong. Prescribe the correct approach directly.

- **Low:** "No, that's not what I meant, I wanted it to use the modal, you keep showing me the full flow which is not what the design said, look at the navigation again."
- **High:** "Pivot: use the modal pattern only. Remove the full-page flow."

### 7. Checklist Close
End each phase with an explicit verification prompt. Not "does it work?" — name the artifact: "Is ai.js in the PRECACHE?", "Does config.js still contain the real secret?"

## AI working memory

Working memory is roughly four files / eight turns. Anything not mentioned recently is likely left behind. Re-reference files and constraints that were set earlier rather than assuming they are still in context.

## Using the Scoring Rubric

Score each phase against the five criteria (Scope, Constraints, Refinement, Bug report, Verification), 0-2 each. Target 8-10 per phase. Below 6 means you are iterating too much — sharpen the Vibe instead of re-rolling the prompt.

The full table is in `references/ira-rubric.md`.

## How to use this skill

1. Write one phase at a time (Phase Contract).
2. Put constraints first (Constraint-First).
3. Report symptoms, never prescribed code changes (Symptom Report).
4. When it drifts, Pivot — prescribe the fix, skip the lecture.
5. Close the phase with a Checklist Close verification prompt.
6. Score the phase with the rubric. 8-10, ship. Below 6, rewrite the Vibe.