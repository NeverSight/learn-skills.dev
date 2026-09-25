---
name: scenario-inspiration
description: "Use when a creative task has no direction yet: finding inspiration, exploring looks or styles, proposing concept directions to pick between, building a moodboard or reference board, doing visual research, mining existing assets for a style, or escaping generic AI-looking output. Also when a saved Scenario collection should drive a new batch as art direction. Keywords: inspiration, moodboard, references, art direction, style exploration, concepts, serendipity, ideation, surprise me."
license: MIT
---

# Scenario Inspiration

## Overview

Asked for inspiration, an agent averages. It returns the most typical answer for the brief, so every user with a similar brief gets the same look. This skill trades that for four phases: **prime**, **widen**, **choose**, **board**. Connection and scope: see the `scenario` skill in this repo. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

Four moves carry most of the value. Name the reflex answer for this brief and the answer of someone merely avoiding that reflex, then rule out both, because an agent told to be original lands on the second-obvious answer. Randomize the operator, never the subject: what varies is the transformation applied to the brief, and a random subject is just noise. When you generate candidates yourself instead of searching for them, ask yourself for a distribution rather than an answer, and work from its tail. Then make the user pick, because options that never resolve are a gallery, not direction.

## Quick reference

| Phase     | Do                                                                                     | Detail                                                   |
| --------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1. Prime  | Locked constraints, the open axis, both reflexes, what counts as a hit                 | [references/widen.md](references/widen.md)               |
| 2. Widen  | Four lanes plus wildcard draws; over-gather, near and far                              | widen.md, [references/sources.md](references/sources.md) |
| 3. Choose | Three or four mutually exclusive directions one named axis apart, plus an escape hatch | [references/choose.md](references/choose.md)             |
| 4. Board  | The pick becomes a collection, every reference annotated with its job                  | [references/moodboard.md](references/moodboard.md)       |

Four lanes feed phase 2. Ask the user first, for three things they already love and one they cannot stand; unattended, take those from the task instructions and continue without them if it names none. Then `search` with `target: "assets"` twice, once over the team's own work (`public` omitted) and once over the public catalog (`public: true`), and last the open web, which is not a `search` call. Public asset hits carried `metadata.prompt`, the wording that produced them, and `target: "models"` hits carried `exampleAssetIds` at authoring time: free style research either way. `images: {like, unlike}` steers by example in both directions.

Draw far domains yourself with [scripts/wildcard.py](scripts/wildcard.py), run from the skill directory (`python3 scripts/wildcard.py --count 4`). A model asked for something random samples its own habits; the script samples a corpus and prints its seed, so a draw can be replayed or deliberately never repeated.

## Worked example: a puzzle game's world map, nothing decided

1. **Prime.** Locked: 16:9, readable at phone size. Open: everything else. Reflex: candy-colored isometric islands. Second reflex: the same islands, muted and "cozy". Both are out of bounds now. A hit is a map whose regions read apart in grayscale. Run the obvious query once and keep it as the baseline to beat.
2. **Widen.** `search` the project for anything already on brand, then `public: true` at `query_semantic_ratio: 0.8` and again at the keyword default, reading the prompts on the best hits. Draw four wildcards, run each as its own query, and keep near, middle, and far finds rather than only the strangest.
3. **Choose.** Name the axis first (here, how the world is depicted), then four positions on it. Each gets a title, an intent line, two or three references shown with `asset_display`, and who it wins for and when it fails. Say what you cut. Ask which is closest and what they would take from another, and offer the escape hatch. When nobody can answer, take the pick from the task instructions, else choose the option that best satisfies the hit line from prime, say which and why, mark it provisional, and keep going.
4. **Board.** `collection_create` the winner, then copy in every foreign reference: public assets belong to their own team, and `collection_add_assets` on one returned 403 at authoring time. `asset_download`, `curl -L`, `upload_asset`. `asset_update` each with its reason, tag the anti-references, hand the collection id to `scenario-image` or `scenario-consistency`.

## Common mistakes

- Skipping prime and searching the brief's own words, which returns the category reflex sorted by relevance.
- Four options that are one idea in four colors. If picking A does not rule out B, they are not directions.
- Presenting only the survivors. Naming what was cut, and why, is what makes the rest credible.
- Calling a set varied without checking it against what the literal query already returned.
- Treating every strange find as a keeper. It earns a slot only when you can name what it connects to and what it is worth.
- Boarding whatever came back. Every reference needs a job (light, color, composition, material, shape, subject, environment) or it is decoration.
- Mixing lighting worlds on one board: a hard-flash reference and a soft-window reference cancel at generation time.
- Handing a model an 18-image board. Reduce to three to six role-tagged references first.
- Shipping the undirected default when the brief asked for none of it: subject centered and facing the lens, posed, evenly lit, everything in focus, a processed gloss. Every axis a prompt leaves open (framing, moment, lens, time of day, light) is filled with the model's most average answer, so name each one.
