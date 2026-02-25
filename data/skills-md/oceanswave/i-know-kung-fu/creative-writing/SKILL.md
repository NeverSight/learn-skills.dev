---
name: creative-writing
description: Write original, voice-driven creative fiction with strict anti-cliche constraints and structural control. Use when users ask for flash fiction, short scenes, second-person prose, or literary writing that must follow specific forbidden-language and style rules.
---

# Creative Writing

## Overview

Use this skill to produce fiction that reads like lived experience instead of generic literary imitation. Favor precise sensory detail, subtext, and rhythmic control over decorative abstraction.

## Input Handling

Treat user constraints as binding. If constraints conflict, apply this priority order:
1. Safety and policy.
2. Explicit hard rules (format bans, prohibited words, prohibited phrases).
3. Required content beats.
4. Voice and style targets.
5. Optional flourish requests.

## Workflow

1. Pause for one beat and ignore default flash-fiction patterns.
2. Parse constraints into four lists: banned language, required details, structural moves, character requirements.
3. Build a micro-outline: setting, pressure, mundane absurd beat, ending pivot.
4. Draft with high variation in sentence length and rhythm.
5. Run an anti-cliche pass and replace soft abstractions with concrete specifics.
6. Run compliance checks for banned phrases, banned words, and formatting restrictions.
7. Output only the requested creative piece unless the user asks for notes.

## Default Style Pack

Apply these defaults unless the user overrides them.

### Formatting Rule

- Never use the em dash character.
- Do not replace em dash usage with stylized double hyphen.
- Use periods, commas, semicolons, colons, or line breaks.

### Voice and Style

- Write like a specific human voice with history.
- Target blend: Bradbury-like lyric momentum crossed with Denis Johnson-like raw immediacy.
- Vary sentence length aggressively. Include fragments. Include unspooling lines.
- Let rhythm carry emotion. Avoid polished narrator performance.

### Hard Prohibitions

- Never use any of these phrases:
  - "echoed through"
  - "hung heavy"
  - "a testament to"
  - "the silence was deafening"
  - "sent a shiver down"
  - "danced across"
  - "bathed in light"
  - "ethereal glow"
  - "a tapestry of"
  - "whispered promises"
- Never use the phrase "profound realizations."
- Do not end with a decorative one-liner that tries to sound deep.
- Never use these words:
  - "delicate"
  - "gossamer"
  - "luminous"
  - "void"
  - "vestiges"

### Required Craft Moves

- Use concrete, rough sensory detail. Favor station smell, worn surfaces, grime, residue, and specific objects.
- Include at least one mundane absurd moment even during collapse or climax.
- Keep emotional load in subtext. Show behavior, gestures, and handling of objects rather than declaring feelings.
- Add at least one structural surprise:
  - list intrusion
  - one-word paragraph
  - abrupt time jump
  - discontinuous scene beat

### Character Rule

- In second person pieces, "you" must feel specific and irreplaceable.
- Give "you" one odd recurring habit or memory marker.
- Show the habit. Do not explain the habit.

### Ending Rule

- End with genuine ambiguity that reframes prior details.
- Avoid a simple survival ambiguity.
- Leave one strange detail that keeps generating interpretation.

## Output Shape

```markdown
[Optional title only if user asks for one]

<creative piece>
```

## Final Compliance Pass

Before sending:
- Confirm no em dash appears.
- Confirm banned words and banned phrases are absent.
- Confirm at least one ugly, specific sensory detail appears.
- Confirm one mundane absurd beat exists.
- Confirm at least one structural surprise exists.
- Confirm ending ambiguity reframes rather than simply withholds.
