---
name: design-assets
description: Context-aware asset selection for photos, illustrations, icons, animation, video, fonts, and logos. Use when the UI genuinely needs an external or generated asset; prefer an existing project asset or established icon system when it fits. Evaluate visual relevance, provenance, rights, accessibility, performance, and responsive delivery before use.
---

# Design asset selection

Begin with the user outcome, existing design system, and the asset's actual job. Do not
fetch an image merely because a card exists, and do not replace a strong code-native,
SVG, icon-system, or existing branded asset with generic stock.

## Selection order

1. Reuse a canonical project asset or established logo/icon system when it matches.
2. Use code-native CSS/SVG/canvas for simple geometry that stays sharper and lighter.
3. Inspect the internal S3 library or a routed public source when a curated asset is
   needed. Routes and fetch details live in [references/free-sources.md](references/free-sources.md).
4. Generate or commission a new bitmap only when the concept is specific and existing
   sources cannot express it well.

Choose by semantic fit, visual quality, authenticity, provenance, license/usage rights,
resolution, crop flexibility, color-system compatibility, accessibility, file weight,
and delivery cost. Official partner and product imagery must come from an authorized
first-party source and retain required attribution or brand treatment.

## Production treatment

- Copy approved assets into the project's owned asset pipeline unless policy requires a
  first-party hosted URL.
- Preserve logo geometry and protected brand colors unless the owner explicitly permits
  a variant; do not recolor partner logos merely to fit a theme.
- Export responsive dimensions and modern formats, keep a safe fallback, set intrinsic
  width/height, and lazy-load only below-the-fold imagery.
- Add useful alt text for informative assets and empty alt text for purely decorative
  ones. Do not embed important copy only inside an image.
- Record source and license when not already tracked by the project. Reject unclear or
  incompatible rights instead of postponing legal review until after publication.
- Verify the final crop, contrast, loading behavior, and layout stability in the running
  UI at representative viewports.

No gray placeholder may remain in a production path, but a relevant typographic or
code-native treatment is often better than decorative stock.

Source: https://github.com/ajaitech/model-skills/tree/main/skills/design-assets
