---
name: series-bible
description: Creates and enforces a series bible, the single source of truth for a channel or series covering format, voice, characters, visual system, motion, sound and locked AI-generation settings, so every episode feels like the same show. Use when the user wants consistency across videos, a channel style guide, a recurring format, a character bible, brand guidelines for content, or asks to check a new script or design against their style, or says their videos all feel different.
license: MIT
metadata:
  version: "0.1.0"
  status: alpha
  category: consistency
  pack: creator-skills
---

# Series Bible

Consistency is what turns videos into a show. Viewers come back for a format they recognize, a voice they trust, and a look they can spot in the feed. The bible writes all of that down once, so every skill (and every collaborator) makes the same show.

The bible lives at `.creator/bible.md` in the user's project. Template: [assets/bible-template.md](assets/bible-template.md).

## The floor

1. **One bible per series.** A channel with two formats has two bibles (or one with two format sections).
2. **Concrete values only.** Hex codes, font names, millisecond durations, voice IDs, word counts. "Clean modern look" is not a bible entry.
3. **Every rule has an example.** A good episode, a frame, a line. Rules without examples get misread.
4. **The bible is versioned.** Changes are dated and logged at the bottom. No silent edits.
5. **Drift is flagged, not auto-fixed.** When new work breaks the bible, report it. The creator decides whether to fix the work or update the bible.
6. **Locked generation settings.** Style blocks, reference images, seeds, models and voice settings live here so outputs stay consistent.

## Procedures

### Create
1. **From existing work** (best): analyze 3–5 of the creator's videos or scripts that they consider on-brand. Extract the patterns: hook type, structure, length, voice, palette, fonts, motion, music.
2. **From scratch:** interview with the template sections as questions, ask for references they love, then propose values.
3. Fill the template. Mark anything assumed as `TBD (assumed)`.
4. Show a one-screen summary to confirm.

### Check
Compare a new script, storyboard or prompt pack against the bible. Output:

```markdown
## Bible check: <episode>   (bible v<version>)
✓ Format: 45 s, hook-setup-escalation-turn-button
✗ Voice: profanity at level 3 in the hook (bible: 2, never in the first 3 s)
✗ Visual: accent color #FF3B30 used (bible accent: #E8B04A)
? Motion: whip-pan used twice (bible: max one per video). Intentional?
Suggested fixes: <one line each>
Proposed bible changes (if the drift looks intentional): <...>
```

### Evolve
When the creator approves a change, update the bible, bump its version, and log: date, what changed, why, which episode triggered it.

## What goes in the bible

| Section | Holds |
|---|---|
| Identity | Premise, promise to the viewer, audience, why us |
| Format | Runtime, beat template with timings, recurring segments, openers and closers |
| Voice | Dials, signature phrases, banned words, person, example lines |
| Characters | Look, personality, voice, catchphrases, reference sheets |
| Visual | Palette with roles, typography, framing rules, thumbnail template, the style block for generation |
| Motion | Curves, durations, transitions, signature move |
| Audio | VO model + voice ID + settings + tag vocabulary + pronunciations; music style; stings; SFX palette; loudness |
| Generation | Models, style blocks, reference images, seeds, negative lists |
| Changelog | Dated changes |

## References

| File | Read when |
|---|---|
| [assets/bible-template.md](assets/bible-template.md) | Creating a bible; the canonical structure |
