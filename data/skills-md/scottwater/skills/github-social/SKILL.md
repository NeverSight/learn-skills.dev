---
name: github-social
disable-model-invocation: true
description: Generate a 1280x640 GitHub repository social preview (Open Graph) image and link it at the top of the README.
---

# GitHub Social Preview

Create a 1280x640 PNG social preview for a GitHub repository, using `repository-open-graph-template.png` (in this skill's folder) as the safe-area reference.

## Workflow

1. Gather repo signal from the request and local files: repo name, owner/org, README tagline, logo or mark, brand colors, primary language, and audience. Done when every bracket in the prompt template can be filled.
2. Draft the prompt from the template below and generate with the built-in image tool, targeting `gpt-image-2` where a model can be chosen — credentials are never needed, so proceed without asking for an API key. Pass `repository-open-graph-template.png` as a reference image when the tool accepts reference inputs; otherwise rely on the template's written safe-area constraint.
3. Inspect the result at full size and at roughly 320x160. Regenerate or edit until every check passes: repo name spelled correctly and readable at thumbnail size, all critical content inside the safe area, no guide lines, template copy, watermarks, or unintended logos, and the visual matches the repository's actual purpose and tone.
4. Save to `assets/github-social-preview.png`, creating `assets/` if needed, unless the user names another path or that name collides with a file they want preserved.
5. Link the image at the very top of `README.md` with a relative Markdown image link — before any badges or logo — unless the user opts out or asks for different placement. Repoint or replace an existing preview block instead of adding a second. If `README.md` does not exist, ask before creating one.

```markdown
![Repository social preview](assets/github-social-preview.png)
```

## Specs

- Canvas: exactly 1280x640, opaque PNG — the size GitHub's Settings > Social preview uploader expects.
- Safe area: all critical text, logos, faces, and visual focus inside the template's inner rectangle (about 80px from each edge); nonessential background texture may bleed past it.
- Text: large, sparse, high-contrast — repo name plus at most one short descriptor.
- Composition: one strong concept, not a collage — a project mark beside the repo name and tagline, or an abstract product/code motif tied to the repository. Palette drawn from the repo's brand; generic purple-blue gradients only when they are the brand.
- Assets: use real project assets when provided; otherwise create an original simple mark. Third-party logos and GitHub's own mark stay out unless the user explicitly requests GitHub branding.

## Prompt template

```text
Create a GitHub repository social preview image for [REPO_NAME].

Canvas and purpose:
1280x640 PNG, opaque background, designed for GitHub repository Settings > Social preview / Open Graph sharing.

Repository signal:
[OWNER_OR_ORG], [SHORT_DESCRIPTION], [LANGUAGE_OR_DOMAIN], [BRAND_COLORS_OR_VISUAL_MOOD].

Composition:
Keep all important details inside an 80px safe margin on every edge, matching the safe-area of the GitHub repository-open-graph-template reference. Use a bold, readable layout with one primary focal element and generous spacing. The image must still read clearly when reduced to 320x160.

Text:
Render exactly: "[REPO_NAME]"
Optional subtitle, if useful: "[TAGLINE]"
Use large, crisp, high-contrast typography. No extra words.

Style:
[DISTINCTIVE_STYLE_DIRECTION]. Polished production design, not a screenshot of GitHub settings, not a generic stock banner.

Constraints:
Do not include red guide lines, template labels, watermarks, tiny text, unrelated logos, or GitHub branding unless explicitly requested. Keep edges crop-safe.
```

Recommended settings:

```yaml
model: gpt-image-2
size: 1280x640
quality: high
background: opaque
output_format: png
```
