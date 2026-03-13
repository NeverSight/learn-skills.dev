---
name: "crossfit-programmer"
description: "Program personalized CrossFit sessions and microcycles from a comprehensive movement library with scalable variations. Use when users ask to create a WOD, adapt training for equipment/skill/injury constraints, or generate training that accounts for recent session history and movement-pattern fatigue."
---

# CrossFit Programmer

Create structured WODs that match user goals, available time, equipment, skill level, and recent training context.

## Quick Start

1. Gather or infer the athlete profile:
- Goal (`engine`, `strength`, `skill`, `mixed`)
- Session length in minutes
- Fitness level (`beginner`, `intermediate`, `advanced`)
- Available equipment
- Limitations (`avoid_patterns`, `avoid_movements`)
- Preferred modalities (optional)
- Desired WOD type (optional: `amrap`, `for_time`, `emom`, `chipper`, `interval`)

2. Prepare a profile JSON using `references/sample-profile.json` as the template.

3. If available, provide recent workout history using `references/sample-history.json` as the template.

4. Generate a WOD with the deterministic script:

```bash
node scripts/generate_wod.js \
  --profile-file references/sample-profile.json \
  --history-file references/sample-history.json
```

5. If needed, request JSON output for programmatic reuse:

```bash
node scripts/generate_wod.js \
  --profile-file references/sample-profile.json \
  --history-file references/sample-history.json \
  --output json
```

## Programming Rules

- Include warm-up, main work, and cooldown.
- Reduce repeated stress from very recent sessions by down-weighting repeated patterns and exact repeated movements.
- Prioritize equipment-available movements.
- Scale movement complexity to the user level while still offering progression options.
- Preserve modality balance unless the user explicitly asks for a biased day.
- Enforce movement coherence inside each piece (EMOM/AMRAP/chipper stations should share setup and context).
- Only program context-dependent variations when the context exists:
  - Bar-facing burpee is only valid if a barbell movement is in that same piece.
  - If no barbell lift is present, use standard burpee or lateral burpee instead.
  - Burpee box jump over is only valid if a box is already in that lane/piece.
  - Toes-to-bar, chest-to-bar pull-up, and pull-up variants require pull-up bar access in that piece.
  - Wall-ball shots are only valid when a wall-ball target and wall-ball are available for that piece.
  - Rope climb is only valid when a rope and safe descent setup are available; otherwise use rope pull or pull-up progressions.
  - Ring dip and ring muscle-up are only valid when rings are already set at working height in that piece.
  - Handstand walk is only valid when there is clear lane space; otherwise use handstand hold or wall-supported handstand work.
- Minimize pointless station transitions; prefer combinations that can be performed in one lane with shared equipment.

## Resources

- `references/movements.json`: movement library with modality, patterns, effects, equipment, and variations.
- `references/sample-profile.json`: canonical input profile template.
- `references/sample-history.json`: recent training context template.
- `scripts/generate_wod.js`: deterministic generator that turns profile + history into a full WOD.
