---
name: story-bible
description: Write and maintain a story bible - logline, cast sheets with locked visual descriptors, locations, props, style/LUT, voice - that every prompt, shot and check reads from. Use at the start of any film, series or ad, and whenever a character, look or location changes.
---

# story-bible

Produce `bible.md` (or JSON with the same sections). Every later skill copies its descriptors word for word.

## Sections
1. **Logline and tone:** one sentence each. Add the target length, aspect and fps.
2. **Cast:** for each character, an id, a role, and a *locked descriptor* of 25-40 words (age, build, face, hair, wardrobe, colors) that is pasted unchanged into every prompt. Add the reference still path and seed, plus the voice (reference clip and seed for `voiceover`).
3. **Locations:** an id, a descriptor, and the time of day and light.
4. **Props:** anything that has to stay consistent between shots.
5. **Style:** medium, palette, lens language, film stock or LUT (`camera-lens-lut`), and a short list of negatives.
6. **Rules:** screen direction, wardrobe changes by scene, and what must never change.

## Workflow
- Draft the bible from the user's sentence. Show it to the user and get approval before you generate anything. In Super Easy mode, auto-approve but still show it.
- Make character sheets with `flux3-klein-stills` (front, 3/4 and profile on a neutral background), then add angles with `image-edit`. Store the paths in the bible.
- When the user changes something mid-project, update the bible first. Then list the shots it affects and hand them to `continuity-check`.

## References
- `references/fuobe-character-sheet.md` (MIT): the character-sheet method.
- `references/seriesmith-episode-script.md` (MIT): a complete series config (subjects, locations, voices, profiles). The section "Starting a series: what to settle first" is a good model for the bible. Its file formats belong to seriesmith, so borrow the structure, not the syntax.
