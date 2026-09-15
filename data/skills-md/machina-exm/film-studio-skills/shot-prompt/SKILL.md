---
name: shot-prompt
description: Turn a shot card into a 15-block prompt before video. Use when every in-frame asset is locked and a shot is ready to generate.
---

# Shot Prompt

Turn one shot card and its locked asset passports into one versioned prompt.
Keep the fifteen blocks in the fixed order below.

## Start

1. Read the `## AI film studio` section in the project's `CLAUDE.md` or `AGENTS.md`.
2. Use the configured video model only as the destination for the finished prompt.
3. If the section is missing, tell the user to run setup first.
4. Continue if requested by asking which video model they use and how they submit prompts.
5. Locate the shot card in `/prompts/`, `/docs/registry.md`, `/docs/breakdown.md`, and the passports of every in-frame asset under `/assets/`.
6. If `/prompts/` or `/docs/` is missing, offer to create the needed folder in the studio tree.
7. Ask which one scene and shot to write.

Ask one question at a time throughout.

## Enforce the asset gate

List every character, state variant, location, and prop named in the shot card.
Match each exact tag and version to `/docs/registry.md`.
Require every row to be `locked` before producing a generation-ready prompt.
If any asset is missing or draft, name it, keep the shot blocked, and direct the user to asset-passport or stress-test.
Do not silently substitute another version or base asset.

Read each locked passport.
Copy every active canonical descriptor verbatim.
Do not shorten, paraphrase, or clean up a descriptor inside the prompt.

## Resolve the shot card

Carry forward its identity, direction, and camera/edit lanes.
Confirm that the clip contains one action and runs for 10–15 seconds.
Move any sign, screen, title, or other in-frame text to `/docs/text-tasks.md`; keep it out of generation.
Ask the user about one missing field at a time.

## Write the fifteen blocks

Use numbered headings and this exact order:

1. **Scene context** — Open with `EXACT N CHARACTERS — NO DUPLICATES`, using the exact count. State the scene, shot goal, and one action.
2. **Active references** — Paste every in-frame asset descriptor verbatim and identify its unchanged reference files.
3. **Location map** — Give positions and distances in metres. State the line the camera never crosses.
4. **First-frame blocking** — Place each character, prop, and the camera at the first frame. Begin with everyone already in place for the shot.
5. **Format mode** — State the required frame format and whether the configured workflow starts from text or an image.
6. **Optics** — Use one lens for the shot. Change field of view only on a hard cut.
7. **Camera body** — Describe the camera as a physical body: position, height, angle, support, movement, path, and stopping point.
8. **Action timing** — Break the single action into beats of 0.3–0.8 seconds across the clip.
9. **Physics** — State persistent physical consequences. Damage remains visible and debris stays where it lands.
10. **Lighting** — Use the location passport's light character and palette. Describe shaped light from its actual sources.
11. **Audio** — Include ambience, in-frame sound, and each verbatim dialogue line in exact quotation marks.
12. **Character acting** — Direct posture, gesture, breath, gaze, reaction, and living eye behaviour for each character.
13. **Style prefix** — Apply the locked visual style and give a `60:30:10` dominant, secondary, and accent colour line.
14. **Quality bar** — State the required reference match, anatomy, material, motion, continuity, lip-sync, and artifact standard.
15. **Positive constraints** — Rewrite every prohibition as what is visibly present, then add a concrete failure clause for the shot's known risk.

Do not add a negative-prompt section.
Keep the exact quoted dialogue from the shot card.
Keep block content specific enough to verify in the resulting take.

## Save a version

Create the prompt in `/prompts/` using the project's existing naming pattern.
If no pattern exists, use `<scene>-<shot>-prompt-v<version>.md`.
Preserve earlier versions instead of overwriting them.
Record which locked passport versions the prompt uses.

## Iterate surgically

After each generation, append one row to `/docs/generation-log.md` with:

```markdown
| shot id | prompt version | what changed | result | verdict |
```

Change exactly one line for the next prompt version and keep every other line verbatim.
Record the output path and verdict before trying again.
If the shot fails after 10–15 iterations, stop polishing words.
Choose one structural simplification with the user: split the shot in two, drop an action, or change the angle.

## Accept or reject the take

Accept only when all checks pass:

- characters and location match their references;
- hands, teeth, objects, and surfaces carry no artifacts or random text;
- camera movement follows the shot card;
- performance and lip-sync hold;
- eye-line, axis, size, and light cut with neighbouring shots;
- the world palette matches.

Give an accepted take its final name in `/selects/sc<NN>/`.
Keep raw outputs in `/generations/sc<NN>/`.
The editor works only from `/selects/`, never from raw generations.

## Finish

Report the prompt path and version, the locked passports used, any unresolved issue, and the next generation-log action.
