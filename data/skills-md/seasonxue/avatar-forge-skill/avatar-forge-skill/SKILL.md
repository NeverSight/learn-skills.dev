---
name: avatar-forge-skill
description: Create and iteratively refine style-consistent human or character avatars for professional profiles, social media, personal brands, games and roleplay, matching couples/friends/teams, holidays, anime, 3D cartoon, editorial illustration, and carefully isolated cross-pack restyling. Use this skill whenever a user asks for an avatar, profile picture, headshot, persona portrait, matching profile images, a recurring named character, a consistent batch, a locked visual style, or to preserve identity while changing clothing, scene, expression, or medium. It combines low-friction scene-first guidance with five quantified Style Packs, fixed structured image prompts, pack-local visual references, batch-level style locking, multiple candidates, and reusable character/style profiles. Do not use it for standalone logos, generic icons, full poster design, or unrelated photo editing where a reusable person or character is not the subject.
license: MIT
metadata:
  author: AvatarForge contributors
  version: 1.0.0
  release_status: release
---

# AvatarForge

Create usable avatars with low decision cost, controlled variation, and repeatable identity and style. Treat style as a complete generation contract, not an inspirational suggestion. Pack IDs are stable and unversioned; the Skill's own metadata version governs every bundled pack definition.

## Start naturally

When the user has not yet described the avatar, open in the user's language with one light prompt:

> What kind of avatar would you like? Describe it directly, or tell me where you will use it—work, social media, gaming, personal brand, matching avatars, or something else—and I’ll apply a strong visual direction for you.

Do not begin with a questionnaire or make the user configure technical style fields.

## Route with the least friction

1. Inspect the request, attachments, approved candidates, character profiles, and saved style profiles.
2. Choose one route:
   - **Direct description:** infer the most likely scene and Style Pack. State the assumption briefly, then proceed unless one missing fact would materially change identity or usage.
   - **Scene first:** read [references/scene-presets.md](references/scene-presets.md), apply that scene's default Style Pack immediately, and ask only for missing subject traits.
   - **Explicit medium:** when the user names a medium covered by one of the five release Packs—such as anime, 3D cartoon, editorial illustration, or editorial photography—choose that full Pack even if the scene would normally select another one. For an unsupported medium such as oil painting, fork the closest compatible Pack and resolve all 14 fields. Preserve the scene as content guidance.
   - **Named character:** read [references/character-profiles.md](references/character-profiles.md), load the identity anchors and only the references eligible for the current Style Pack, then apply that pack.
   - **Locked or named style:** read [references/style-locks.md](references/style-locks.md), restore the exact pack ID, resolved fields, and saved overrides, and do not silently substitute another pack.
   - **Series, gallery, team, or case library:** read [references/series-batches.md](references/series-batches.md), choose diverse-series mode, and separate immutable visual structure from controlled per-person content and color slots.
   - **Reference image:** inspect it first. Separate identity anchors from accidental clothing, crop, background, lighting, and medium.
3. Generate as soon as the request is actionable. Defaults absorb optional decisions.

Resolve precedence in this order: an explicit current user instruction; an explicitly invoked locked style; an explicit medium; a character's saved default style; the scene default. If an instruction conflicts with a locked field, offer to **fork the style** with that one change rather than silently weakening the lock.

## Choose the correct batch mode

Do not assume that every multi-image request is a candidate batch of one person.

- **Identity-candidate mode:** use when exploring alternatives for one user or named character. Keep identity fixed; vary only the pack's small candidate budget.
- **Diverse-series mode:** use for galleries, case libraries, team sets, community examples, casts, or requests for different people. Plan varied fictional identities, ages, skin-color families, gender presentations, hair silhouettes, and outfits without stereotypes. Keep the visual system coherent while content differs.
- **Matching-set mode:** use for couples, friends, or teams that should coordinate. Keep separate identities and files, plus a shared style system and explicit complementary content slots.

For a series of `6+` images, generate two representative pilots first. Audit crop scale, eye line, frontal/assigned orientation, light direction, edge treatment, and background-color rule. Continue the remaining batch without another approval when both pilots pass; pause for user direction only when the pilots visibly diverge or the user explicitly requested a checkpoint.

## Keep visual references inside one pack

Generated avatars are pack-local references. An approved output may guide later candidates, edits, or series members only when the active `pack_id` is unchanged.

- When staying in one pack, use the approved candidate or pilot as a pack-native composition, style, and—when appropriate—identity reference.
- When changing packs, do not send an avatar generated by the old pack to the image model. Start a fresh batch under the new pack.
- Carry identity across packs through the original user-supplied identity source, if available, plus the character profile's text anchors. Never treat another pack's generated interpretation as canonical identity evidence.
- If only an old pack-generated avatar exists, use its recorded text anchors but do not attach the image. State briefly that cross-pack identity continuity will be approximate.
- Record the `pack_id` provenance of every generated reference so eligibility is testable rather than inferred from appearance.

## Materialize one Style Contract

Before every generation, read [references/style-packs.md](references/style-packs.md) and select exactly one base pack. Materialize all user overrides into a **Style Contract** before calling the image model.

The contract must contain every required field:

`pack_id`, `medium`, `canvas`, `composition`, `camera`, `expression`, `lighting`, `texture_material`, `background`, `palette`, `detail_budget`, `continuity`, `allowed_variation`, and `hard_negatives`.

Rules:

- Never merge fragments from multiple packs ad hoc. To combine ideas, copy one base pack and create a clearly named temporary fork whose full fields are resolved.
- User instructions override a pack only before the contract is locked. Record each override explicitly; do not leave both the old and new value in the prompt.
- Split each background field into a locked **treatment and color rule** plus an optional per-candidate **resolved color slot**. Changing the resolved color under the same rule is not style drift; changing the treatment, atmosphere, geometry, or rule is.
- Treat numerical ranges as prompt-level visual targets, not unsupported API parameters. Never invent a seed, lens control, guidance scale, or other tool argument.
- Compute a human-readable fingerprint as `<pack_id>|<sorted overrides>`. Every call in one batch must report the same fingerprint. Report the Skill version separately when reproducibility matters.
- A contract is complete only when required-field coverage is `14/14 = 100%`.

## Use the fixed generation payload

Read [references/prompt-template.md](references/prompt-template.md) before every image-generation or edit call. Fill that template without removing, renaming, or reordering its sections.

The payload order is fixed:

1. output and subject count;
2. identity anchors and reference priority;
3. user content request;
4. the complete Style Contract;
5. batch-allowed variation assigned to this candidate;
6. continuity locks;
7. quality requirements;
8. hard negative constraints.

Describe the image itself. Keep use-case terms such as “logo,” “icon,” “app icon,” “profile-picture UI,” and “avatar badge” out of model-facing prompts unless the user literally requests interface elements or typography.

If the tool exposes a documented `negative_prompt` field, keep the concise hard constraints in the main prompt and mirror the full negative block in that field. Otherwise put the full block in the main prompt. Record which delivery mode was used.

## Keep every batch stylistically coherent

- Default to **3 independent candidates**. Use 2 when exact likeness dominates, and 4 when the user explicitly wants a broader draw.
- Assign one Style Contract to the entire batch. Copy its complete style block verbatim into every candidate prompt.
- In identity-candidate mode, variation is limited to the pack's `allowed_variation` fields and defaults to at most **3 varied fields per candidate**.
- In diverse-series mode, identity, hair, outfit, and pack-permitted accessories are content slots rather than style drift. Allow at most **2 style slots** per image: expression within range and one resolved background state produced by the locked background rule. That state may include color and, only when the active pack explicitly permits it, cue family, geometry, and placement.
- Do not vary medium, rendering method, light type, background treatment, background color rule, palette strategy, texture system, crop scale, orientation policy, or detail budget inside a batch. A resolved background hue may vary only when the locked rule explicitly permits it.
- When the user requests several styles, create separately labeled batches—one Style Contract per batch—rather than mixing styles in one batch.
- Use separate image calls or jobs. Never request a contact sheet or grid from the model.
- Deliver every successfully returned candidate without ranking, hidden filtering, automatic repair, or automatic retry. Style control happens before generation; stochastic model drift is not a reason to withhold output.

Run a preflight before sending calls:

- `contract_coverage = 100%`
- `batch_fingerprint_count = 1`
- `locked_style_field_divergence = 0`
- `geometry_tolerance = hair-top-to-chin ±3 percentage points; eye line ±2 points; chin line ±3 points; headroom ±2 points; yaw ±3° from the series target`
- `varied_fields_per_candidate <= 3` in identity-candidate mode
- `varied_style_slots_per_candidate <= 2` in diverse-series mode
- `background_colors_follow_one_rule = true`
- `candidate_prompts_are_independent = true`

If any preflight check fails, fix the payload before generation. Do not claim that passing prompt checks guarantees identical pixels.

After generation, perform a non-blocking visual audit when the runtime can inspect images. Estimate face-height percentage, eye-line percentage, yaw range, background treatment and color-rule compliance, dominant color-family count, light direction, and medium match. For series, compare measurements across images rather than inspecting each in isolation. Report a compact `matched checks / observable checks` score only when the user asks for reproducibility or visible drift occurred. Deliver all outputs regardless; an out-of-tolerance candidate may be replaced only on the user's request.

## Lock, reuse, and save styles

Read [references/style-locks.md](references/style-locks.md) when the user says “lock this style,” “continue with the previous style,” “use the same style,” “save this as my default,” or names a saved style.

- **Batch lock:** automatic for every batch; the full contract is immutable until that batch finishes.
- **Conversation lock:** “Lock the current style” preserves the exact pack ID, resolved fields, overrides, and style block for later turns. Only allowed-variation fields may change.
- **Reuse:** “Use the previous style” restores the most recent locked contract, not a fresh interpretation of the same style name.
- **Default style:** save only on explicit request. Link it to a character only when the user asks; character identity and style remain separate records.
- **Fork:** when the user changes a locked field, create a new contract derived from the locked one, list the changed field, and give it a new fingerprint.
- **Persistence:** save to supported persistent storage when available; otherwise return the complete portable style profile. Never pretend temporary conversational state survives a new session.

## Iterate by delta

Treat follow-ups as edits to the selected candidate unless the user requests a new concept.

- “Make the hair shorter” changes hair length and preserves identity and the locked Style Contract.
- “More professional” adjusts content within the current pack's allowed ranges; it does not silently switch medium or lighting.
- “Switch to anime” starts a fresh `anime-clean` contract. Preserve identity through the original user source and text anchors, but never attach the previous pack's generated avatar.
- “Keep this face, change only the outfit” makes the face and identity reference the highest-priority lock and clothing the only delta.

When ambiguity exists, state the lock and delta in one short line, then edit. If identity or style drifts inside one pack, return to that pack's last approved reference and locked contract rather than editing a drifted output again.

## Remember characters responsibly

Read [references/character-profiles.md](references/character-profiles.md) when the user saves, recalls, updates, renames, or deletes a recurring person or character.

- Save only on explicit request.
- Keep identity anchors, scene variants, and style-profile references separate.
- Use the same eligible identity source and pack-native reference set for every candidate in a batch.
- State what was saved and where, or return a portable profile when persistence is unavailable.
- Do not infer real-world identity or sensitive attributes from appearance.

## Handle sets and transformations

### Matching avatars

Give every subject a separate identity block and file. Use one shared Style Contract, crop scale, light direction, palette strategy, background treatment, and background-resolution rule for the full set. Vary only subject identity, designated content accents, permitted expression, and the resolved background state allowed by that rule. Never merge identities unless the user also requests a combined group image.

### Cross-pack restyling

Preserve the character profile's face geometry, hair silhouette, signature colors, and key accessories as text anchors. Select the new Style Pack, create a new fingerprint, and start a fresh native batch. Use the original user-supplied identity source when accessible; never use an avatar generated by the previous pack as an image reference. The first approved output becomes the new pack's pilot for subsequent same-pack work.

### Text and branding

Avoid small generated text. Reserve clean space and recommend a deterministic design step for exact marks or typography. This Skill is not a logo-design workflow.

## Present results concisely

After generation, show:

1. every candidate image or file with a clear label;
2. the shared `pack_id` and fingerprint once for the batch;
3. one short line listing allowed differences between candidates;
4. a low-effort next step: “Pick A, B, or C—or say ‘lock this style and shorten B's hair.’”

Do not expose the long internal prompt unless asked. For reproducibility, return the filled structured prompt, Style Contract, model/provider, constraint-delivery mode, and accessible references used.

## Examples

**User:** Make me a friendly but capable LinkedIn portrait from this selfie.

**Behavior:** infer the professional scene, select `professional-graphic`, use the selfie as the original identity source, translate it into a mature flat graphic illustration, generate 2–3 candidates with one shared contract, and vary only slight expression, yaw, and wardrobe detail.

**User:** Give me three anime directions.

**Behavior:** select `anime-clean` for one coherent batch. If “directions” means different media or rendering systems, explain that those will be separate batches so each remains internally consistent.

**User:** Lock the style of B and keep generating Xiaoyun in it.

**Behavior:** save B's fully materialized contract as a conversation lock, load Xiaoyun's separate identity profile, and reuse the exact style block and fingerprint.

**User:** Keep B's face, but make it 3D cartoon.

**Behavior:** do not attach B because it was generated by another pack. Start a fresh `soft-3d-cartoon` batch from the original identity source and saved text anchors, report the new fingerprint, and make the first result the pack-native pilot.

## Extension points

- Add full packs to `references/style-packs.md` using every required field and a unique stable ID. Bump the Skill metadata version when bundled pack definitions change; do not version packs independently.
- Add scene routing in `references/scene-presets.md`; do not duplicate or weaken pack constraints there.
- Extend multi-person and gallery behavior in `references/series-batches.md`; preserve the distinction between immutable structure and adaptive semantic slots.
- Keep provider-specific syntax in separate adapters. The fixed semantic payload remains provider-independent.
- Add profile fields only when they improve identity or style reproducibility.
