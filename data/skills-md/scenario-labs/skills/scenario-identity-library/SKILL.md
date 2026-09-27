---
name: scenario-identity-library
description: "Use when a named character or prop must become a reusable identity in Scenario: creating a character or prop from a brief or interview, building its approved image collection (character: <name> or props: <name>), assembling a character sheet or turnaround, or generating new images of an established one. Triggers include create a new character, design a prop, character sheet, turnaround, more images of this character. Keywords: character design, identity, library, collection, grid."
license: MIT
---

# Scenario Identity Library

## Overview

A game or brand runs on named identities: characters and props that must stay recognizable in every image that ships. This skill runs that lifecycle end to end: interview a brief, generate and gate a hero image, file approved shots in a named collection, assemble a sheet, and pull the library back out for new images. The per-image mechanics live in siblings and are not repeated here: connection and the core loop in `scenario`, holding a look with references in `scenario-consistency`, pass/fail verdicts in `scenario-quality-gate`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

| Stage   | Mechanism                                                                                    | Rule                             |
| ------- | -------------------------------------------------------------------------------------------- | -------------------------------- |
| Brief   | interview, written as the must-not-change enumeration                                        | before anything generates        |
| Anchor  | hero generation, gated to pass                                                               | uploaded art skips generation    |
| Library | collection named `character: <name>` or `props: <name>`                                      | gated images only                |
| Sheet   | Grid Maker assembly of approved shots                                                        | rebuild after membership changes |
| Reuse   | `collections_list` prefix match, members via `search`, references per `scenario-consistency` | any later session                |

## From interview to anchor

Interview before generating: the answers become the baseline enumeration every later image restates (`scenario-consistency`), so a gap here becomes drift later. Ask what it is, silhouette and proportions, palette by name or hex, two or three signature details that make it recognizable (the cracked headlamp, the brass buckle), the rendering style, and which views the set needs: a full view alone gives a reference slot too little detail to hold close-ups, so an identity that will be shot close also needs a straight-on close view of the face or signature detail and an exact profile. Non-interactive runs take what the task supplies and flag the rest. A user who already has art skips generation: their drawing or photo is the uploaded anchor, per `scenario-consistency`.

Pick one reference-capable model for the whole identity before the first run (`recommend`, then the schema gate in `scenario-consistency`): every later view rides its reference field, so a model without one disqualifies itself here, not at view three. Generate the hero, a neutral full view on a plain background (a reference slot isolates identity best from an uncluttered anchor: nothing beyond the brief in frame, no text), then gate it per `scenario-quality-gate` with a round cap fixed up front (its default is three); absent that skill and the gate itself, review against the brief enumeration, same cap. The hero is the anchor everything else cites.

## The library is a named collection

`collection_create` with the exact name `character: <name>` or `props: <name>`, then `collection_add_assets` for the hero (catalog tools, write lane; the create call takes the name plus the scope pair, and no description field). The name is the registry key: collections are not a `search` target, so a later session finds the library by paging `collections_list` (read lane) and matching the prefix, then pulls members with `search` (`target="assets"`, `filters={"collection_ids": [...]}` plus a `tags` filter for the views wanted, which keeps filed sheets out of reference pulls). Admission is the gate: only passing images enter, because every future generation samples this pool as reference truth, and one off-model member poisons every pull after it. Build out the views baseline-plus-delta, one `model_run` per view, gate each, file each pass tagged with its view (`asset_add_tags`: `hero`, `back`, and so on), so a later session can tell the members apart. A redesign (new wardrobe, haircut, age) rewrites the brief enumeration and needs a new hero off the old (`scenario-consistency`): rebuild views and sheet from it, and `collection_remove_assets` the superseded members before the next pull, or one pull feeds both versions into the reference field.

## Sheets are assembly, not generation

Scenario's Grid Maker packs approved shots into one sheet image: its id is the fixed first-party `model_scenario-grid-maker` (Scenario's single deterministic tool for the job, so discovery would only re-derive it); read its schema with `model_schema_get`. At this writing it takes `images` (a file array capped at 100; wrap even a lone asset) plus layout fields: `columns`, `rows` computed from the count when unset, `padding`, `backgroundColor`, and a fixed `cellRatio` list (`auto` default). It has no prompt field: order the `images` array in reading order, because the array is the layout. The sheet is itself an asset, filed ungated (it assembles already-approved shots, it is not a generation): tag it (`asset_add_tags`, say `sheet`), file it, and rebuild it after membership changes rather than editing it: pull the view-tagged members only (never a bare member list, or an old sheet becomes a grid cell), and swap the old sheet out with `collection_remove_assets`. It serves humans, and it serves as a one-slot reference packing the whole turnaround when a model is slot-starved; with slots to spare, prefer the individual approved shots.

## Worked example: Nima, courier robot

1. The interview yields the brief: rounded silhouette, copper shell, one cracked headlamp, canvas satchel, cel shading; views front, back, left, three-quarter.
2. `recommend` with the brief's own words; `model_schema_get` confirms a true reference field (else the next candidate); `model_run` the hero, `jobs_wait` whenever `model_run` returns a `job_id` without assets, gate per `scenario-quality-gate`, iterate to pass.
3. `collection_create` `"character: Nima"`; `collection_add_assets` the hero, tagged `hero`.
4. Three more views, baseline-plus-delta with the hero in the reference field, gated, filed on pass with their view tags.
5. Run Grid Maker on the view-tagged members (this session already holds the ids; a just-filed asset can trail the `search` index) with `images` as [front, back, left, three-quarter] and `columns: 4`; tag the output `sheet` and file it.
6. Weeks later, "Nima in a rainy alley": `collections_list` finds `character: Nima`, members come from `search`, the `hero`-tagged member and two on-model shots ride the reference field, prompt per `scenario-consistency`.

## Common mistakes

- Generating before interviewing: a vague brief cannot be enumerated, and the library inherits the drift.
- Admitting ungated images: a failed image iterates per `scenario-quality-gate` or never enters.
- Prompting Grid Maker or expecting it to generate: it arranges its `images` input, nothing more; generation belongs to the view runs.
- Passing the sheet as an img2img `image`: composition lock (`scenario-consistency`); a sheet rides a true reference slot only.
- Free-form collection names: `Nima stuff` is unfindable by convention; the `character: ` and `props: ` prefixes are the lookup contract.
- A different model per view: reference behavior differs per family; one schema-checked model carries the whole identity.
