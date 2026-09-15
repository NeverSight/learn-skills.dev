---
name: stress-test
description: Combat-test draft film assets before locking them. Use after a passport and references exist and before any scene generation.
---

# Stress Test

Test a draft asset under the conditions that can break it before locking it for film generation.
Use cheap static images for the entire test.

## Start

1. Read the `## AI film studio` section in the project's `CLAUDE.md` or `AGENTS.md`.
2. Use the configured image model as the destination for test prompts.
3. If the section is missing, tell the user to run setup first.
4. Continue if requested by asking which image model they use and how they submit prompts.
5. Check for `/docs/registry.md`, `/docs/breakdown.md`, and the asset passport under `/assets/characters/`, `/assets/locations/`, or `/assets/props/`.
6. If the studio tree is missing, offer to create the needed folder, but do not invent a passport or a lock result.
7. Ask which one draft asset to test.

Ask one question at a time throughout.

## Verify the draft

Find the exact registry row by tag and version.
Require a draft passport with a canonical descriptor and reference files.
If the descriptor or references are missing, stop the lock attempt and name what must be completed in asset-passport.
Never shorten or rewrite the descriptor while constructing test prompts.

Read the registry and `/docs/breakdown.md` to collect:

- every scene containing the asset;
- the lighting used in those actual scenes;
- every asset that shares the frame with it;
- the relevant state variant for each scene.

Ask the user about one unresolved scene condition at a time.
Do not substitute a base asset for a state variant.

## Build the combat-test matrix

Create a matrix inside the asset's passport under `## Stress test`.
Cover different angles, shot sizes, actual-scene lighting, and shared-frame pairings.
Include a two-shot beside every asset it shares frame with.
Use more than one matrix row when a pairing appears under materially different scene lighting.

Use these columns:

```markdown
| Test | Angle | Shot size | Scene lighting | Paired asset | Prompt | Result | Verdict |
|---|---|---|---|---|---|---|---|
```

Use `pending`, `pass`, or `miss` in the verdict column.
Keep each row traceable to a scene when it uses scene lighting or a pairing.

## Write the test prompts

For every row:

1. Paste the asset's canonical descriptor verbatim.
2. Point to its approved reference files without renaming them.
3. State the row's angle and shot size positively.
4. Reproduce the lighting of the actual scene.
5. For a two-shot, paste the paired asset's canonical descriptor verbatim and point to its references.
6. Describe a simple static composition that exposes identity consistency without adding unnecessary action.

Do not turn these tests into video generations.
Do not add cinematic complexity that the row is not testing.

## Run and record

Give the prompts to the user for their configured image workflow, or use the access method they provided.
Save each static result beside the passport under the matching `/assets/<type>/` folder with a versioned test filename.
Record each output path in the row's `Result` cell.
Review every output against the passport and references.
For characters, check face, hair, age cues, build, wardrobe, distinctive details, and variant state.
For locations, check layout, landmarks, materials, palette, light character, and grade.
For props, check form, scale, materials, markings, wear, and distinctive details.
For two-shots, check both identities rather than only the target asset.

Mark any identity drift or broken required detail as `miss`.
Do not average a miss away because another output looks good.

## Apply the gate

For a character, require ten passes out of ten attempts.
A result below 10/10 is a failed lock.
For a location or prop, present the completed matrix and require an explicit pass decision from the user.

On any miss, keep the registry status `draft` and choose one next action with the user:

- revise the descriptor or references in asset-passport, then rerun the full affected test;
- consciously move the affected scene to the next production block.

Never hide a failed row or mark a partial test as locked.

On a pass:

1. Change the exact registry row from `draft` to `locked`.
2. Change the passport status to `locked`.
3. Record the lock decision and completed result paths in its stress-test section.
4. Preserve the passport descriptor verbatim.

## Finish

Report the score or decision, every miss, the registry status, and the paths to the test record.
State the gate law: generation for a scene cannot start until every character, state variant, location, and prop in that scene is locked.
If any asset remains draft, name the blocked scenes and stop before expensive video generation.
