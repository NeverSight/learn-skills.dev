---
name: asset-passport
description: Create film-asset passports before generation. Use for characters, locations, props, and state variants that need repeatable visual identity.
---

# Asset Passport

Create one authoritative visual passport for one film asset at a time.
Treat the passport as the asset's memory: its descriptor and approved references will be copied unchanged into later prompts.

## Start

1. Read the `## AI film studio` section in the project's `CLAUDE.md` or `AGENTS.md`.
2. Use the configured image model only as the destination for reference-sheet prompts; do not assume a particular model.
3. If the section is missing, tell the user to run setup first.
4. Continue if the user wants to proceed by asking which image model they use and how they submit prompts.
5. Check for `/assets/characters/`, `/assets/locations/`, `/assets/props/`, `/docs/registry.md`, and `/docs/breakdown.md` in the studio root.
6. If a required folder is missing, offer to create only the needed folder in the studio tree.
7. Ask which single character, location, prop, or state variant to passport.

Ask one question at a time throughout.

## Establish identity

Confirm the asset's:

- tag, beginning with `@`;
- type: character, location, or prop;
- version;
- scenes in which it appears;
- seed or reference files already chosen.

Read `/docs/breakdown.md` when available and reconcile its scene IDs and asset tags with the user's answers.
Do not silently merge two tags or change an existing tag.

Treat every state variant as a separate asset with its own passport and registry row.
For example, keep `@cal`, `@cal_wet`, and `@cal_blood` separate.
Ask what visibly changes in the variant and what must remain identical to the base asset.

## Write the descriptor

Interview the user until the visual identity is exhaustive and unambiguous.
Ask about one missing dimension at a time.
Cover stable visual facts that another prompt writer must reproduce without guessing.
Separate permanent identity from scene-specific action, framing, or camera choices.

For a character, resolve face, hair, age cues, build, skin, wardrobe, footwear, carried items, wear, and distinctive details.
For a prop, resolve form, scale, material, colour, finish, wear, markings, moving parts, and distinctive details.
For a location, resolve layout, surfaces, architecture, fixed objects, scale, weathering, and spatial landmarks.

For a location, also include the scene's:

- dominant, secondary, and accent colours;
- light character;
- built-in grade.

Pull those colour decisions from `/docs/bible.md` when present.
If they are undecided, ask the user rather than inventing them.

Write one canonical descriptor in complete prose.
Never provide a short form or omit details for brevity.
Mark the descriptor as `draft` until the asset passes stress-test.

## Write the reference-sheet prompt

Write a prompt for the user's configured image model.
Ask it to show the same asset on a neutral grey background in these views:

1. front;
2. three-quarter;
3. profile;
4. back;
5. close portrait or close detail.

Paste the canonical descriptor verbatim into the prompt.
Keep unrelated locations, set dressing, narrative action, and dramatic staging out of the sheet.
For a state variant, include the full invariant identity and the variant's exact visible changes.
Save each generated reference sheet beside its passport under the matching `/assets/<type>/` folder.
Give every sheet a versioned filename and record that exact path in the passport.

## Create the passport file

Choose the matching folder:

- characters: `/assets/characters/`;
- locations: `/assets/locations/`;
- props: `/assets/props/`.

Create a versioned Markdown file using the project's existing naming pattern.
If no pattern exists, use `<tag-without-@>-v<version>.md`.
Never rename a reference file; a new version gets a new file.

Use this structure:

```markdown
# <tag> — version <version>
Status: draft
Type: <type>
Scenes: <scene IDs>
Seed files: <paths or pending>

## Canonical descriptor
<exhaustive descriptor>

## Reference-sheet prompt
<prompt containing the descriptor verbatim>

## Reference files
<versioned paths or pending>
```

## Update the registry

Open `/docs/registry.md` and find the row by exact tag and version.
Preserve the columns `tag · type · version · seed file · scenes · status`.
Append a row when none exists; otherwise update that exact draft row.
Set `status` to `draft`.
Use the passport or reference-sheet path in `seed file` according to the project's existing convention.
Do not mark the asset `locked`; only stress-test can do that.

## Finish

Report the passport path, registry row, unresolved fields, and the next action.
Tell the user to generate or attach the reference sheet in the asset folder, approve the references, and run stress-test before using the asset in film generation.
