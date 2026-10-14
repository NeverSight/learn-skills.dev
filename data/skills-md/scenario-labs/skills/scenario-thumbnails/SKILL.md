---
name: scenario-thumbnails
description: "Use when creating or revising finished video thumbnails or cover images with Scenario: game trailers, boss reveals, patch updates, devlogs, or community videos needing readable composition, exact headline text and consistent characters. Not for title ideas or critique alone, in-video title cards, or a generic image without a thumbnail deliverable."
license: MIT
---

# Scenario Thumbnails

## Overview

Make a cover that communicates its subject at the size viewers actually see. The deliverable is a finished image at the requested dimensions, with exact supplied copy and preserved identities. Connection and the generation loop follow `scenario`; image/reference contracts follow `scenario-image`. Exact type uses `scenario-text-overlay`, placement specifications use `scenario-formats`, and a set that must share a look uses `scenario-consistency`. If a sibling skill named here is missing from your available skills, ask the user to install it (`npx skills add scenario-labs/skills --skill <name>`); unattended, proceed from tool schemas and flag the gap.

Resolve the destination, topic or title, supplied assets, exact copy, desired count and budget from the request. Ask only for missing decisions that affect the result. Do not invent a person, logo, testimonial or game feature to make the image more dramatic. Distinguish an approved character reference from a style example; the latter is not permission to substitute its people or branding.

## Quick reference

| Brief                    | Useful composition                          | Check before generating                                                  |
| ------------------------ | ------------------------------------------- | ------------------------------------------------------------------------ |
| Boss or encounter reveal | Recognizable threat and one readable action | Silhouette, scale relationship, approved character identity              |
| Mechanic explanation     | One clear action and its consequence        | The depicted mechanic exists in the supplied material                    |
| Patch or world update    | New feature as the focal subject            | Released versus proposed content; supplied facts                         |
| Progression or reward    | Visible contrast between states             | State labels and reward claims are supported                             |
| Creator-led devlog       | Supplied speaker and relevant game subject  | Who appears, their reference and the actual topic                        |
| Storefront capsule       | Destination-specific composition            | Apply `scenario-formats`; video-cover defaults do not define store rules |

Choose a composition from the brief rather than forcing every game into large faces, photorealism or exaggerated reactions. When direction is open, propose a few meaningfully different concepts before spending; unattended, select the best-supported concept from the supplied brief, record that assumption and proceed within the authorized count and ceiling. If essential inputs or spending authorization are missing, report that blocker without generating. When the user has chosen a concept, execute it. Respect an exact variant count. Do not turn a single cover into an unsolicited batch.

## From brief to prompt

Define the visual promise in one sentence: what the viewer will recognize or learn. Set one primary focal subject, supporting action and a quiet region for any requested copy. Choose a hierarchy that survives reduction, not a catalog of decorations. A split image is useful only when the brief is about a visible comparison; two subjects do not automatically require a split layout.

Size the copy region for the actual words rather than reserving half the frame by default. Compare compact line breaks and subject scale at the reduced preview; a large empty panel or a small focal character can weaken an otherwise editable cover. Check the announced change still reads at that size.

Describe the subject, action, composition, palette, medium and light in concrete terms. Name each reference's role and the features that must stay fixed. Keep provider-specific fields in the payload discovered through `model_schema_get`, not in a universal template. Use `recommend` for the capability and the user's need; use `search` for a model the user names. Avoid hard-coded generative model versions or quality tiers.

The target size and copy are contracts. Generate at a supported ratio and size, then use the documented resize route if exact export dimensions are unavailable. Do not silently crop a character or stretch the image to hit the numbers. Give exact supplied logos and text a deterministic placement path. Prefer a clean plate followed by `scenario-text-overlay` when words must match exactly; if the user explicitly requests integrated generated lettering, inspect it character by character and repair it through the supported edit/overlay route when needed. No supplied copy means no invented headline.

## Worked example: a boss-fight devlog cover

The user supplies the approved moss-covered stone boss reference, requests one illustrated 1280x720 YouTube thumbnail and the exact headline "ONE HIT LEFT". The boss has two arms, one amber eye and no mouth. The chosen composition is the boss on the right, a small shield-bearing player below, and copy on the left. The authorized ceiling covers one generation and a bounded repair.

1. Inspect the reference and record the identity invariants. Upload it via `scenario` if it is not already an asset. Preserve its approved illustration style and do not substitute a photographed person.
2. `recommend` for `txt2img` with that brief: this is a new composition using a character reference, not a restyle of the reference's layout. Read `model_schema_get` on a suitable reference-taking member. Check supported ratio, reference count/cardinality, prompt limit and size before selecting the payload. Pass the reference as the schema's actual field, scalar or array as required; do not assume a source-image/strength editing contract. Use `img2img` when the task is to edit or restyle an existing composition.
3. Prompt the approved boss and action with a clear left-side copy region. Keep the plate free of text and duplicate bosses. Price the payload with `model_run` and `dry_run: true`, then submit within the ceiling and wait on its existing job id using `jobs_wait`.
4. Inspect the result against the boss reference before adding type. A changed eye count or silhouette needs a focused correction; adding text does not repair identity. Use the accepted plate for an edit when appropriate, preserving approved features rather than restarting the concept.
5. Render the supplied headline as a transparent PNG card through `scenario-text-overlay`, then composite it over the plate with `model_scenario-compose-image`. That id is fixed rather than discovered because it is Scenario's single deterministic image compositor; it takes image layers only, so the words never pass through a model. Inspect the finished image, not just a browser preview. Land the exact output size through `scenario-image`/`scenario-formats` and read the returned dimensions.
6. Review at 1280x720 and as a roughly 120-pixel-wide preview. The small preview is a stress test, not a universal platform standard. Check that the boss and shield still read, the headline is legible, and neither copy nor cropping covers the defining eye. Inspect the actual reduced image; requesting high resolution alone is not this test.
7. Deliver the verified final image through `asset_display` and `asset_download`. Keep the clean plate, exact text, font/layout settings and source/output identifiers so a copy change can reuse the art. State any unresolved defect rather than silently marking a failed variant complete.

## Review, revisions and common mistakes

For multiple outputs, give each concept or variant a stable label and retain its source roles, payload, job id and QA result. Pending outputs are waited on, not resubmitted. Retry only a failing output within the remaining ceiling. On revision, map the user's note to composition, identity, copy or export; reuse accepted layers and change only the requested part. A new headline normally needs a new overlay, not another image generation.

- Treating a style example as the character source swaps identity without permission.
- A sharp large image can still have an unreadable hierarchy at feed size.
- Longer copy needs a layout decision, not automatic truncation or altered wording.
- A logo is an asset to preserve, not a word to ask a model to spell.
- Decorative UI, rewards and mechanics that were never supplied misrepresent the game.
- Readability and reference fidelity are observable; click-through improvement is not established by a thumbnail review.
