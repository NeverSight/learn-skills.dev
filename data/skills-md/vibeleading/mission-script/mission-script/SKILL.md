---
name: mission-script
description: Craft high-fidelity Vibe Leading Mission Scripts. Use when writing or calibrating strategic intent to hand to AI agents or a team, or when a deliverable/generation needs a clear Vibe.
version: 0.1.0
license: MIT
---

# Mission Script

A Mission Script is the written form of the Vibe: the high-frequency strategic intent of the leader. It is a Technical Specification, not a feeling. It couples poetic clarity (a human can feel it) with engineering precision (an AI can execute it).

> Source: "Vibe Leading The AI: The Corporate Race Against Machines" (Jean Machuca). Framework concept: the Vibe and the Mission Script.

## What makes a Vibe high or low

The AI is a massive amplifier. Blurry intent amplifies into hallucination; sharp intent amplifies into competitive advantage.

- **Low Vibe:** "Just get the report done by Friday." Low traction, high drift. Every ambiguous word is budget the machine spends guessing.
- **High Vibe:** "The report needs to identify the $2M gap in our Q3 prospecting with 99% accuracy." Specific scope, specific standard, specific number.

## How to set the Frequency

Before writing, fix the Frequency of the mission. It changes how the AI weighs speed against fidelity.

1. **Stealth / Precision mode:** correctness, validation, security. No surprises. Use for anything touching money, code, customers, or compliance. The AI should refuse rather than guess.
2. **High-Velocity / Market-Capture mode:** speed to insight and maximum breadth. Use for research, drafting, and creative exploration. Accept rougher edges for faster Laps.

State the Frequency in the first sentence of the script.

## Mission Script template

Fill in these six fields. A script with all six is high-fidelity; a script missing fields is drift waiting to happen.

1. **Mission Name** — one line, names the deliverable and its quality bar.
2. **Frequency** — Stealth/Precision or High-Velocity/Market-Capture.
3. **Outcome** — the concrete result, with the number or accuracy that defines done.
4. **Constraints** — security, limits, must-nots. State these first.
5. **Acceptance** — how we know it worked (the verification bar).
6. **Verification** — the explicit check or checks that close the phase.

Worked examples live in `references/mission-script-template.md`.

## The Prompt Ladder

The specificity ladder you climb to sharpen the Vibe. Higher rungs = higher IRA.

- **Aspirational** — "Make it look cool." Very low IRA. The AI guesses; you pay for the guess.
- **Functional** — "Add Google Sign-In." Medium. A feature exists but nothing constrains it.
- **Constrained** — "Add Google Sign-In using GIS, fallback to guest, persist in localStorage." High. Method, fallback, and storage are specified.
- **Behavioural** — "When the user clicks Sign In, show the Google picker. After callback, show avatar in nav. If GIS fails, show a Guest button that creates a local session." Very high. Sequences and reactions are specified.
- **Exemplar** — "Like the sign-in on this reference site: (URL). Only the modal part." Highest. Point at a working thing.

Start at the highest rung you can name. Climb when the machine drifts or when you sense the Vibe is too blurry to amplify correctly.

Full ladder table in `references/prompt-ladder.md`.

## How to use this skill

1. Pick the Frequency.
2. Draft the Mission Script using the six-field template.
3. Check the Vibe: can a human feel it? Can an AI execute it? If either is no, sharpen it.
4. Hand the script to the agent; do not translate it through a middle layer.
5. At the end of the task, run the Verification field and score the result against the Vibe.