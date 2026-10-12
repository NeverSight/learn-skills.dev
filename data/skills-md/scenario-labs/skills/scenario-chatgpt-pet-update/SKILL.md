---
name: scenario-chatgpt-pet-update
description: "Use when changing an existing ChatGPT pet or Codex pet sprite sheet with Scenario: fixing a broken row, frame, jump or edge, regenerating one animation state, adding the sixteen look directions to a 1536x1872 v1 sheet, giving the pet a new outfit, color or accessory, renaming it in its pet.json, or checking a pet sheet and previewing it as an animated GIF."
license: MIT
---

# Scenario ChatGPT Pet: Update

## Overview

An existing pet is its sprite sheet: a PNG or WebP the user downloaded from ChatGPT, a Codex pet folder (`pet.json` plus the sheet it names), or a Scenario asset id of a sheet made earlier. That file is the pet's identity here; there is no pet record to look up. The update never overwrites it: the result is a new package next to the run, with the same id and name unless the user changes them.

This skill runs the scripts and follows the sheet contract of `scenario-chatgpt-pet-create`, which must be installed; run each script by its path in that skill's `scripts/` folder, from the user's working folder, and read the contract before generating a row or writing direction verdicts: [pet_frames.py](../scenario-chatgpt-pet-create/scripts/pet_frames.py), [pet_prepare.py](../scenario-chatgpt-pet-create/scripts/pet_prepare.py), [pet_build.py](../scenario-chatgpt-pet-create/scripts/pet_build.py), [pet_check.py](../scenario-chatgpt-pet-create/scripts/pet_check.py), [pet_preview.py](../scenario-chatgpt-pet-create/scripts/pet_preview.py), [pet_package.py](../scenario-chatgpt-pet-create/scripts/pet_package.py), and [the contract](../scenario-chatgpt-pet-create/references/sheet-contract.md). Generation follows that skill's loop and model order (`model_openai-gpt-image-2-5-sunburst`, then `model_google-gemini-nano-banana-2-1`, then `recommend` only when both are blocked); connection and scope: the `scenario` skill. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

## Quick reference

Read the sheet first, then pick the smallest change that does the job. Every row below runs in a run made by `pet_prepare.py init --from-split` (step 3 of the example): it records the original sheet, which the build, the check and the package all need. Unattended, the approvals are your own judgment against the request, recorded in the run, and nothing is installed.

| The user wants                                 | Do                                                                                                                  | Generations   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------- |
| To see or check it                             | `pet_check.py`, `pet_preview.py contact` and `gif`                                                                  | 0             |
| A rename or new description                    | `init`, `pet_check.py <sheet> --run RUN`, then `pet_package.py make RUN --sheet <sheet> --name ...`                 | 0             |
| Leftover pixels, color under transparency      | `pet_build.py RUN --clean`                                                                                          | 0             |
| A row whose frames pop up and down or sideways | `pet_build.py RUN --reregister <row>`: re-places the existing frames on one ground line and anchor                  | 0             |
| One or a few states redone                     | `init --only <rows>` (a look row too), generate those rows, `pet_build.py RUN`: every other row stays byte for byte | one per row   |
| Look directions on a v1 sheet                  | `init --version 2 --only look`: cardinals, then rows 9 and 10                                                       | 3             |
| A new look (outfit, color, accessory)          | `init --change "<the change>"`: edit the identity, approve it, regenerate every row                                 | 1 + every row |

`split` refuses anything that is not 1536x1872 or 1536x2288: other art is a new pet, made with `scenario-chatgpt-pet-create` using that art as a reference.

## Worked example: Pepper's stiff run, then a red scarf for next season

1. **Get the sheet.** The user points at `~/.codex/pets/pepper/`: read `pet.json` (`id`, `displayName`, `description`, `spritesheetPath`) and copy the sheet into a work folder. From an asset id: `asset_download` with `format: "png"`, then `curl -L`.
2. **Read it.** `pet_frames.py split pepper.png --out work/split` prints the version, a background key that contrasts with the pet, and `pixel_grid` (set when the sheet is pixel art with on/off alpha; the update then keeps that grid and palette). `pet_check.py pepper.png --json-out work/before.json` measures it: height per row against idle, jump lift, look-row drift. `pet_preview.py contact` and `pet_preview.py gif` show the current pet. Ask what should change if the request is vague, naming what the check found.
3. **Redo the run.** `pet_prepare.py init --name Pepper --id pepper --description "<from pet.json>" --from-split work/split --only running-right,running-left --out work/run` (every row of the table starts with an `init --from-split` like this; `--only` names the rows to generate). The `match` style keeps the sheet's look; each job's `references` are `references/base.png` (the idle frame, enlarged on the key) and `references/rows/<row>.png` (the current row). Each job maps onto one `model_run`: its `references` uploaded with `upload_asset` and passed as `referenceImages` (an array), its `prompt` verbatim, its `sizes` for the model, `background: "opaque"` on Sunburst, priced with `dry_run` first; download the result to the job's `output`. When the old row's motion or directions are what is wrong (a jump that never lifts, a run that does not alternate, a head that turns the wrong way), add `--no-current-row` to `init` so the old strip is not a reference, since the model copies what it is shown, and say what changes with `pet_prepare.py note work/run --jobs <row> --text "..."`; a redone look row still references the kept other half of the sweep. Then `pet_frames.py extract work/run --job running-right`, read the report and preview, and mirror it with `--mirror-left` or generate `running-left` the same way.
4. **Rebuild.** `pet_build.py work/run --mirror-left`. With the original sheet as the base (recorded by `init`), only the rebuilt rows change, scaled to the existing idle row's height, ground line and anchor; the edge cleanup touches only them. `pet_check.py work/run/final/spritesheet.webp --run work/run` must print `ok: true`; kept look rows only bring a warning that they were not reviewed, while a redone look row needs fresh verdicts in `qa/direction-semantics.json` (format in the contract) or the check fails.
5. **Show and package.** `pet_preview.py gif work/run/final/spritesheet.webp --out-dir work/run/previews`, show `pet.gif`, upload the sheet and both GIFs into a collection as the create skill does, then `pet_package.py make work/run --id pepper`. Ask before `pet_package.py install work/run --force`, which backs up the installed Pepper into the run before replacing it.
6. **The scarf, later.** A new look changes every frame, so it is a new generation grounded in the old pet: `init --name Pepper --id pepper --description "<from pet.json>" --from-split work/split --change "add a red knitted scarf" --out work/scarf` adds an edit job on the identity image. Approve the edited base, then run every row as `scenario-chatgpt-pet-create` does from its rows step (look rows included for a v2 sheet, with fresh direction verdicts). The old sheet still sets the pet's size, so the new pet does not grow or shrink.

For a v1 to v2 upgrade (`init --version 2 --only look`), run `look-cardinals`, `look-9` and `look-10` as the create skill describes and write the direction verdicts; the build keeps rows 0-8 and adds the two look rows.

## Common mistakes

- Overwriting the user's file or installed pet: work on a copy, and replace an installed Codex pet only after a yes, with `--force` (which backs it up).
- Regenerating the whole pet for one bad row: redo that row; the build copies the others byte for byte.
- Sending the whole sheet to an image model as the reference: it reads as a grid of small frames and the model copies the grid. Use `references/base.png` and the row strip `split` made.
- Regenerating to fix what the build can fix: leftover pixels, color under transparency and a row that drifts are `--clean` and `--reregister`, at no cost.
- Rebuilding without the original sheet: a new row is then sized from nothing; `init --from-split` records the sheet so the build keeps the pet's size.
- Changing the pet's id on a rename: Codex finds the pet by its folder, so keep the id and change `displayName`.
- Handing a v2 result to someone uploading on ChatGPT web: give them `package/spritesheet-v1.png`.
