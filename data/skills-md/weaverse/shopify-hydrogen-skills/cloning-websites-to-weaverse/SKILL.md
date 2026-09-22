---
name: cloning-websites-to-weaverse
description: Use when recreating a reference website or brand hub in this Hydrogen plus Weaverse repo, especially when deciding whether to reuse sections, add global styles, update theme schema, or resolve conflicts between the live site and project brand guidelines.
---

# Cloning Websites to Weaverse

## Overview

Use this repo-specific workflow to turn a reference website into maintainable Weaverse pages. Optimize for reusable sections, accurate section matching, and clear schema boundaries, not one-off screenshot cloning.

**Priority order:** brand guideline beats source website on visual conflicts. The source website drives page structure, content flow, interaction patterns, and merchandising logic.

## Conflict Rule

`.guides/brand-guideline.md` is the source of truth.

If the live site conflicts with the brand guideline, you MUST follow the brand guideline.
This is mandatory even when:

- a stakeholder says `make it look like the live site`
- leadership will compare screenshots
- the live site appears newer or more polished

Use this rule:

1. Match the source site where it does not conflict.
2. Follow the brand guideline where conflict exists.
3. If unsure, default to the brand guideline.

In conflict cases, explicitly state: `I will match the live site where possible, but the brand guideline is the source of truth for conflicting decisions.`

## When to Use

- Cloning a marketing page, homepage, or brand hub into this repo
- Rebuilding a live page in `app/sections/` and Weaverse
- Deciding between existing sections, new sections, `app/styles/app.css`, and `app/weaverse/schema.server.ts`
- Mapping a reference site's section system onto this repo's registered Weaverse components

Do not use this for tiny copy-only edits or isolated bug fixes.

## Required Inputs

- reference URL or origin site to migrate
- `.guides/brand-guideline.md`
- `sections.md`
- `app/weaverse/components.ts`

## Required Outputs

- **Clone preview route**: a single Hydrogen route (`app/routes/clone-preview.$page.tsx`) that renders the full cloned page as React + Tailwind — user must approve this before section decomposition begins
- **Design spec**: section mapping, interaction model, schema boundaries, implementation direction
- **Content manifest**: per-section table of real asset URLs, text content, link targets, Shopify references, and media types — all sourced from the Firecrawl scrape

The clone preview route is the verification checkpoint. The design spec and content manifest together form the complete handoff to `generating-weaverse-project-json`.

## Source of Truth

| Need | Source |
| --- | --- |
| Colors, type, logo, shape language, legal rules | `.guides/brand-guideline.md` |
| Section order, content hierarchy, CTA flow, merchandising | crawled reference website |
| Existing reusable section matches and child block constraints | `sections.md` |
| Registry of currently available Weaverse components | `app/weaverse/components.ts` |
| Shared tokens and repeated cross-section styles | `app/styles/app.css` |
| Sitewide editable controls | `app/weaverse/schema.server.ts` |
| Section-local content and controls | section `schema` in `app/sections/*` |

## Workflow

1. Read `.guides/brand-guideline.md` first.
2. Ensure `sections.md` exists and is trustworthy before doing section matching.
3. **Scrape the origin page** using Firecrawl with both markdown and HTML formats in a single call:
   ```bash
   firecrawl scrape "<url>" --format markdown,html -o .firecrawl/<site>-<page>.json
   ```
   This returns both clean markdown (for content extraction) and raw HTML (for layout/media analysis) in one request. For pages with JS-rendered content, add `--wait-for 3000`.
4. If the page links to supporting subpages that affect the section system, **crawl** those too:
   ```bash
   firecrawl crawl "<url>" --include-paths <relevant-paths> --limit 10 --max-depth 1 --wait -o .firecrawl/<site>-crawl.json
   ```
5. Extract the source page DNA from the markdown + HTML output:
   - design tokens: colors, typography, spacing, border radius, container widths
   - page structure: section order, repeated patterns, CTA flow, merch flow
   - content assets: headings, copy blocks, imagery, video, product/collection modules
   - media sources: extract `<video>`, `<source>`, `<iframe>`, `<embed>` URLs from the HTML (see Firecrawl Rules → Media source extraction)
6. **Build the content manifest** (see Content Manifest section below). This is a required deliverable — the design spec is incomplete without it.
7. **Generate the clone preview route** (see Clone Preview Route section below). Convert the scraped page into a single Hydrogen route at `app/routes/clone-preview.$page.tsx` that renders the entire page as React + Tailwind. This is a single file with all visual blocks rendered inline — no separate component files. Include desktop and mobile responsive styles. The route must be visually faithful to the origin page while using the repo's Tailwind setup and applying brand guideline tokens where they conflict with the origin. Use clearly commented section markers (e.g., `{/* === HERO === */}`, `{/* === PRODUCT GRID === */}`) to delineate each visual block — these markers become the splitting boundaries for section decomposition later.
8. **User approval checkpoint — STOP HERE and wait.**
   Present the user with:
   - The preview URL (e.g., `http://localhost:3456/clone-preview/<page-slug>`)
   - A summary of what the clone covers (section count, key visual blocks, any known gaps or brand-guideline overrides applied)
   - Explicit instruction: *"Review the clone preview at the URL above. When you're satisfied it matches the source page, reply 'approved' or 'proceed to sections' to continue. If something is wrong, describe what needs fixing."*

   **Do not proceed to step 9 until the user explicitly confirms approval.**

   If the user requests changes:
   - Update the preview route
   - Re-present the URL and ask for approval again
   - Repeat until approved

9. Split the source page into section-sized blocks. For each block, classify:
   - **Primary media type**: `static-image`, `video`, `animation`, `product-media`, `collection-image`, or `external-embed`.
   - **Composition**: how text relates to media — `background-overlay` (text on top of full-bleed media), `side-by-side` (text beside media in columns), `stacked` (text above or below media), `card-grid` (repeated cards with image+text), `card-slider` (one card visible at a time in a carousel).
   - **Layout mechanism**: `single-full-bleed`, `split-columns`, `grid`, `slider/carousel`, `overflow-rail`, `flex-wrap`, `marquee/ticker`.
   - **Interaction**: `static`, `autoplay-carousel`, `snap-scroll`, `arrow-navigation`, `fade-transition`, `auto-scroll-marquee`.
   These classifications come from the **raw HTML** output — look for slider components (Swiper, Flickity, Slick, custom `<slider-component>`, `data-slider`), grid classes, flex patterns, `<video>` elements, and absolute-positioned text overlays.
10. Compare each block against `sections.md` using the **layout matching priority** defined there:
   1. Match **composition** first (overlay vs. side-by-side vs. stacked vs. card-grid vs. card-slider)
   2. Match **layout mechanism** second (full-bleed vs. slider vs. grid vs. rail vs. split)
   3. Match **interaction** third (static vs. carousel vs. scroll)
   4. Match **content model** last (products, collections, manual content)
    Then classify as:
    - `REUSE_EXISTING`
    - `ADAPT_EXISTING`
    - `CREATE_NEW_REUSABLE_SECTION`
    If the source block's composition, layout mechanism, or media type does not match the candidate section, that mismatch must be resolved — either by choosing a different section or by flagging an adaptation requirement. **Never accept a layout mismatch as a "trade-off" without first searching the full section registry for a better match.**

   **Deep structural verification (mandatory for every REUSE or ADAPT classification):**
   After classifying a block, read the candidate section's source code (`app/sections/<section>/index.tsx` and its child files) and verify that its schema settings can produce the exact visual output the origin block requires. Check:
    - Aspect ratio enums — does the schema include the ratios the origin uses (e.g., `9:16`, `3:2`), or is a ratio hardcoded?
    - Responsive image support — does the section accept separate mobile/desktop images, or only a single image field?
    - Split ratios — can the image/text proportions match the origin (e.g., `75/25`), or is the max width capped lower?
    - Child block types — does the section accept the child blocks the origin needs (e.g., buttons, badges, countdown timers)?
    - Animation/interaction capabilities — does the section support marquee, parallax, or transition effects the origin uses?
    - Text readability aids — does the section support backdrop gradients, overlays, or text shadows for text-over-image layouts?
   If **any** schema capability is missing, reclassify from `REUSE_EXISTING` to `ADAPT_EXISTING` and document the specific gap. If multiple capabilities are missing, consider `CREATE_NEW_REUSABLE_SECTION` instead.
11. Only create a new section when the current section system cannot support the target structure or data model without awkward compromises.
12. Implement with clean schema boundaries:
    - global shared tokens -> `app/styles/app.css`
    - sitewide editable controls -> `app/weaverse/schema.server.ts`
    - section-local content and controls -> section `schema`
13. Register every new section in `app/weaverse/components.ts`.
14. Verify desktop and mobile before expanding from the landing page to subpages.
15. **Clean up the preview route** after the Weaverse page is verified and working. The preview route is a temporary artifact — keep it as a side-by-side reference during section building, but delete `app/routes/clone-preview.$page.tsx` once the final Weaverse-rendered page matches the approved preview.

## Content Manifest

The content manifest is the bridge between this skill and `generating-weaverse-project-json`. Without it, the JSON generator guesses content and produces placeholder-filled exports that do not match the source.

After crawling and extracting the source page DNA, build a concrete per-section table before doing section matching. The manifest must cover every visual block on the source page.

### Required columns

| Column | Description |
| --- | --- |
| **Block #** | Sequential position on the page |
| **Block name** | Short label (e.g., "Hero", "Netflix promo", "Connect CTA") |
| **Media type** | `static-image`, `video`, `animation`, `product-media`, `collection-image`, or `external-embed` |
| **Image/video URLs** | Every real asset URL for that block, directly from the crawl output. List all — primary image, secondary images, logo overlays, background images. Use the full CDN URL as it appears in the crawl. |
| **Text content** | Headings, subheadings, body copy, CTA labels — exact wording from the source |
| **Link targets** | Every URL the block links to (internal paths or external URLs) |
| **Shopify refs** | Product handles/IDs or collection handles/IDs if the block is product- or collection-driven |
| **Notes** | Anything unusual: external embed, partner logo with external link, video autoplay, etc. |

### Rules

- Populate image URLs from the **Firecrawl scrape output** (markdown format), not from memory or guessing. The markdown output captures `<img>` src attributes and visible image URLs — use those exact values.
- For `video` or `external-embed` blocks, populate the **Image/video URLs** column with the actual video source URL (MP4, WebM, HLS, YouTube embed, etc.) extracted from the **HTML format output** — not the poster/thumbnail image. If a thumbnail is also useful (e.g., as a fallback), list both with clear labels (`Video (MP4): ...`, `Thumbnail: ...`).
- If a block contains multiple images (e.g., a product card with a lifestyle hero image AND a product image), list all of them with labels.
- If the crawl does not return a usable URL for an asset, mark that cell as `MISSING — [describe what should be here]` so the JSON generator knows to flag it rather than silently substituting a placeholder.
- The manifest is a **required deliverable** of this skill. The design spec (section mapping, schema boundaries, interaction model) plus the content manifest together form the complete handoff to `generating-weaverse-project-json`.
- If the same concept (e.g., "Connect") appears in multiple places on the page with different visual treatments, each occurrence must be a separate row in the manifest and a separate section block in the mapping.

### Where to store it

Add the content manifest as a section in the design spec file (e.g., `design.md`) or as a separate `content-manifest.md` in the same spec folder.

## Clone Preview Route

The clone preview route is the verification checkpoint between scraping and section decomposition. It lets the user visually confirm the clone is accurate before any Weaverse mapping work begins.

### What it is

A single Hydrogen route file at `app/routes/clone-preview.$page.tsx` that renders the entire cloned page as React + Tailwind. It is:

- **One file** — all visual blocks inline, no separate component files
- **Responsive** — desktop and mobile layouts, matching the origin's breakpoints
- **Section-marked** — each visual block delimited with comment markers for later decomposition
- **Brand-adjusted** — applies brand guideline tokens where the origin conflicts (colors, fonts, logo usage)
- **Temporary** — kept as a reference during section building, deleted after the Weaverse page is verified

### Route structure

```tsx
import type {MetaFunction} from '@remix-run/react';

export const meta: MetaFunction = () => {
  return [{title: 'Clone Preview — <page name>'}];
};

export default function ClonePreview() {
  return (
    <div className="clone-preview">
      {/* === HERO === */}
      <section className="relative w-full h-screen ...">
        {/* hero content */}
      </section>

      {/* === PRODUCT GRID === */}
      <section className="max-w-7xl mx-auto py-16 ...">
        {/* product grid content */}
      </section>

      {/* === NEWSLETTER CTA === */}
      <section className="bg-primary text-white py-12 ...">
        {/* CTA content */}
      </section>
    </div>
  );
}
```

### Rules

- **Source all content from the content manifest.** Use the exact asset URLs, text, and links captured in step 6. Do not use placeholder images or lorem ipsum — the whole point of this preview is visual fidelity.
- **Use the repo's Tailwind config.** The preview should use the same Tailwind classes and custom theme tokens available in the repo. Do not add one-off CSS files or inline `<style>` blocks.
- **Apply brand guideline overrides.** Where the origin site's colors, typography, or logo treatment conflicts with `.guides/brand-guideline.md`, the preview must already reflect the brand version — not the origin. This prevents the user from approving something that will change later.
- **Mark every visual block.** Use `{/* === BLOCK NAME === */}` comments to delineate each section-sized block. These markers are the splitting boundaries for step 9 (section segmentation). The block names should match the content manifest's "Block name" column.
- **Include interactive behaviors where feasible.** If the origin has a carousel, implement a basic Swiper or scroll-snap version. If it has video autoplay, include the `<video>` tag with autoplay. The preview does not need pixel-perfect interaction parity, but should demonstrate the core behavior so the user can judge whether it works.
- **Do not import Weaverse components.** This route is independent of the Weaverse section system. It uses plain React + Tailwind. Weaverse sections come after approval.
- **One page per route param.** If cloning multiple pages, each gets its own `$page` slug (e.g., `/clone-preview/homepage`, `/clone-preview/about`). Do not put multiple pages in one route.

### Approval checkpoint

After generating the preview route, **stop and wait for user confirmation**:

1. Tell the user the preview URL and how to access it
2. Summarize what the preview covers: how many visual blocks, key sections, any known gaps or brand overrides applied
3. Ask explicitly: *"Review the clone preview. Reply 'approved' or 'proceed to sections' when satisfied. If something needs fixing, describe what's wrong."*
4. **Do not proceed to section decomposition (step 9) until the user explicitly approves**
5. If the user requests changes, update the route and re-present for approval

### Lifecycle

| Phase | Status of preview route |
| --- | --- |
| Steps 1-6 (scrape + manifest) | Does not exist yet |
| Step 7 (generate preview) | Created at `app/routes/clone-preview.$page.tsx` |
| Step 8 (approval checkpoint) | User reviews, may request iterations |
| Steps 9-14 (section decomposition + build) | Kept as side-by-side reference |
| Step 15 (cleanup) | Deleted after Weaverse page is verified |

## Firecrawl Rules

- Use Firecrawl scrape for the origin site instead of relying on screenshots or memory.
- **Always request both markdown and HTML formats** in a single scrape call (`--format markdown,html`). The markdown is for content extraction; the HTML is for layout classification and media source extraction.
- For supporting subpages linked from the landing page, use Firecrawl crawl with `--include-paths` to scope the crawl to relevant paths.
- Capture repeated layouts, navigation patterns, CTA placements, and content hierarchy.
- Treat the Firecrawl output as the reference-site structure source, not the brand-token source.
- Save output to `.firecrawl/` directory with descriptive names (e.g., `.firecrawl/example-homepage.json`).

### Media source extraction

Markdown output strips `<video>`, `<source>`, `<iframe>`, and `<embed>` elements. These are invisible in the markdown but carry critical asset URLs. **This is why both formats are required.**

From the **HTML format output**, extract:

- `<video>` and `<source src="...">` — MP4, WebM, HLS stream URLs
- `<iframe src="...">` — YouTube, Vimeo, or other embed URLs
- `data-src`, `data-video-url`, or other lazy-load attributes on media containers

Search the HTML for patterns like `.mp4`, `.webm`, `.m3u8`, `youtube.com/embed`, `vimeo.com`, `player.` to find video sources that the markdown output missed.

If a section-sized block has a video or embed in the HTML but only an image (thumbnail/poster) in the markdown output, the block's primary media type is `video` or `external-embed`, not `static-image`. Record the actual video/embed URL in the content manifest, not the thumbnail.

### Layout structure extraction

From the **HTML format output**, also extract layout structure for each section:

- **Slider/carousel components**: Look for Swiper, Flickity, Slick, or custom slider elements (`<slider-component>`, `data-slider`, `data-slider-fullwidth`, `data-dots`, autoplay options in JSON attributes).
- **Grid patterns**: Look for CSS grid classes, column count variables (`--COLUMNS`), responsive breakpoint classes.
- **Flex/brick layouts**: Look for `brick__section`, split-width classes (`brick__block--three-quarters`), reversed order classes.
- **Overlay vs. side-by-side**: Look for absolute positioning on text containers over media, vs. separate grid/flex columns.
- **Marquee/ticker**: Look for `<ticker-bar>`, marquee autoplay attributes, continuous scroll behavior.

This HTML analysis is **mandatory** — do not classify layout behavior from the markdown output alone. Markdown output is never sufficient for pages that contain sliders, overlays, or interactive components.

## `sections.md` Rules

`sections.md` is the migration guide for choosing the best existing Weaverse section in this repo.

It must inventory the registered Weaverse section system and child blocks with:

- purpose
- visual structure
- best fits and bad fits
- real schema-backed options
- layout and data constraints

If `sections.md` is missing, create it before mapping source sections.

If `sections.md` is stale or incomplete, update it from the real registry and schema files before making reuse decisions.

Do not guess section capability from current styling alone. Use the actual schema and composition constraints.

## Migration Analysis Model

Use this analysis sequence from `app/skill.md`:

### 1. Atomic analysis and tokenization
- Extract the source site's design tokens and global layout constants.
- Record only what matters for migration decisions: palette usage, typography behavior, spacing rhythm, container widths, button treatment, radius treatment.

### 2. Semantic section segmentation
- Break the source page into logical reusable blocks.
- For each block, identify layout, components, content type, and likely data source.
- Classify each block's **primary media type**: `static-image`, `video`, `animation`, `product-media`, `collection-image`, or `external-embed`. This classification determines whether the matched section can support the block without adaptation.
- Classify each block's **composition**: `background-overlay`, `side-by-side`, `stacked`, `card-grid`, or `card-slider`. Determine this from the HTML — look at whether text is inside an absolutely-positioned overlay on media, in a separate flex/grid column beside media, or stacked above/below media.
- Classify each block's **layout mechanism**: `single-full-bleed`, `split-columns`, `grid`, `slider/carousel`, `overflow-rail`, `flex-wrap`, or `marquee/ticker`. Look for slider components, grid CSS, flex patterns, and scroll containers in the HTML.
- Classify each block's **interaction**: `static`, `autoplay-carousel`, `snap-scroll`, `arrow-navigation`, `fade-transition`, or `auto-scroll-marquee`. Look for autoplay attributes, navigation arrows/dots, and scroll-snap CSS.
- If the same concept appears multiple times on the page with different visual treatments (e.g., a "Connect" hub card in a grid AND a full-width "Connect" CTA banner later), treat each occurrence as a separate section block.

### 3. Intelligent schema matching
- Compare each source block against `sections.md`.
- **Match using the layout matching priority** defined in `sections.md`:
  1. **Composition first** — Does the section's composition field match the block? A `background-overlay` block must not be matched to a `side-by-side` section.
  2. **Layout mechanism second** — Does the section use the same layout type? A `slider/carousel` block must not be matched to a `grid` section.
  3. **Interaction third** — Does the section support the interaction? An `autoplay-carousel` block needs a Swiper-based section, not a static grid.
  4. **Content model last** — Does the section support the data type (products, collections, manual)?
- Prefer reuse when the structure, content model, and constraints already match.
- Choose adaptation when the section fit is good but needs schema or styling extension.
- Choose a new section only when the current system is not a clean fit.
- **Media type gate**: if the source block's primary media type (from step 2) is not supported by the matched section, do not accept the mismatch and move on. Instead:
  1. **Search** `sections.md` and `app/weaverse/components.ts` for another section that supports the block's media type (e.g., if the block is `video`, look for sections with `videoURL`, `video`, or react-player support).
  2. If a matching section exists, use it instead.
  3. If no section supports the media type, flag it as an adaptation requirement or a reason to create/extend a section.
  4. Never silently downgrade a video to a static image when a video-capable section exists in the registry.
- **Layout gate**: if the source block's composition or layout mechanism does not match the candidate section, do not accept the mismatch. Search the registry for a section that matches the layout behavior. For example:
  - A `card-slider` (one item at a time with navigation) must match `slideshow`, not `product-spotlight-rail` (grid)
  - A `background-overlay` (text on full-bleed image) must match `hero-image` or `promotion-grid`, not `image-with-text` (side-by-side)
  - A `stacked` layout (image above text, centered) may need `columns-with-images` or a rich-text section, not `image-with-text` (which goes side-by-side on desktop)

### 3b. Deep structural comparison

After identifying a candidate section via schema matching, **read the section's actual source code** (`app/sections/<section>/index.tsx` and child files) before accepting the match. Verify each of the following against the origin block's requirements:

| Check | What to verify |
| --- | --- |
| **Aspect ratio support** | Does the schema expose an aspect ratio selector that includes the ratios the origin uses? Many sections hardcode a single ratio (e.g., `aspect-square`). |
| **Media type match** | An image-only section cannot substitute for a video block. Check for `videoURL`, `<video>`, or player component support. |
| **Responsive image variants** | If the origin uses `<picture>` with separate `<source>` elements for mobile/desktop, a single `image` field is not a match. Look for `imageMobile`, `imageDesktop`, or responsive breakpoint logic. |
| **Split ratios** | Check the schema's width constraints. If the origin uses a 75/25 image-text split but the section caps image width at 60%, that is an adaptation requirement. |
| **Child block types** | Verify the section's `childTypes` or `inspector.children` allows the blocks the origin needs (buttons, badges, countdown timers, rating stars, etc.). |
| **Animation / interaction** | A static section cannot reproduce marquee scrolling, parallax, or auto-advance transitions. Check for animation props, Swiper config, or CSS animation support. |
| **Text readability aids** | If the origin places text over an image with a gradient backdrop or color overlay, the section must support `overlayColor`, `overlayOpacity`, or equivalent. A plain image section with no overlay is not a match. |

If any check fails, the section cannot be classified as `REUSE_EXISTING`. Reclassify as `ADAPT_EXISTING` with the specific gaps documented, or `CREATE_NEW_REUSABLE_SECTION` if multiple checks fail.

### 4. Component synthesis and data generation
- For reused sections, map the source content into the existing Weaverse schema.
- For new sections, create reusable section code and schema rather than cloning a whole page into one bespoke component.
- The **content manifest** (built in the workflow) is the data source for all content fields. Do not populate content from memory — use the manifest's exact URLs, text, and links.

## Decision Rules

- Reuse an existing section if the pattern already exists and only needs styling, content, or schema adjustments.
- Create a new section if the pattern is visually or structurally distinct and likely to repeat.
- Put styles in `app/styles/app.css` only when they are shared primitives: variables, font hooks, repeated background treatments, or reusable utilities.
- Put settings in `app/weaverse/schema.server.ts` only when they should be editable across the storefront.
- Keep page-specific spacing, copy, CTAs, and toggles inside the relevant section schema.
- Start with the landing page first; stabilize the base section system before cloning subpages.
- Match the live site where possible, but the brand guideline is the source of truth for conflicting brand decisions.

## Repo Touchpoints

- `app/routes/clone-preview.$page.tsx` (temporary — preview checkpoint)
- `app/sections/`
- `app/weaverse/components.ts`
- `app/styles/app.css`
- `app/weaverse/schema.server.ts`
- `sections.md`

## Red Flags

- Following the live site when it conflicts with `.guides/brand-guideline.md`
- Building one giant bespoke section for a whole page
- Dumping page-specific styles into `app/styles/app.css`
- Putting section-local controls into `app/weaverse/schema.server.ts`
- Skipping Firecrawl scrape and mapping from screenshots alone
- Skipping `sections.md` and guessing which section is closest
- Starting all subpages before the landing page foundation is working
- Treating screenshot parity as permission to override brand rules
- Skipping the content manifest and handing off a design spec without concrete asset URLs
- Using a generic placeholder image when the crawl output contains the real asset URL
- Mapping a video block to an image-only section without flagging the media type mismatch
- **Mapping a slider/carousel to a grid section** (e.g., using `product-spotlight-rail` for a full-screen slideshow)
- **Mapping a full-bleed overlay hero to a side-by-side split section** (e.g., using `image-with-text` for a full-width hero with text on top of image)
- **Mapping a stacked-vertical layout to a side-by-side section** (e.g., using `image-with-text` for a centered image-above-text block)
- **Merging separate origin sections into one** (e.g., combining a background-only video hero and a separate text block into one hero-with-text section)
- **Skipping the raw HTML fetch** and relying only on markdown crawl output for layout classification
- **Classifying a block as REUSE_EXISTING without reading the section's schema source code** — section names and `sections.md` summaries describe purpose, not full capability
- **Assuming an image-only section can handle video backgrounds** — check for `videoURL` or player component support
- **Mapping an animated origin element to a static section without flagging it** — marquee, parallax, and auto-advance require specific component support
- **Skipping the clone preview route** — proceeding directly to section decomposition without generating the preview and getting user approval
- **Proceeding past the approval checkpoint without explicit user confirmation** — "looks reasonable" from the agent is not a substitute for the user reviewing the actual rendered page
- **Using placeholder content in the preview route** — the preview must use real asset URLs from the content manifest, not lorem ipsum or stock images
- **Forgetting section markers in the preview** — without `{/* === BLOCK NAME === */}` comments, the preview cannot serve as a splitting reference for section decomposition
- **Leaving the preview route in the repo permanently** — it is a temporary artifact that must be deleted after the Weaverse page is verified

## Rationalization Check

| Excuse | Reality |
| --- | --- |
| "Leadership will compare screenshots" | Screenshot parity does not override the repo's brand rules. Match layout with the source site; match tokens with the brand guideline. |
| "The live site is newer than the guideline" | Unless the repo guidance is updated, `.guides/brand-guideline.md` remains the implementation source of truth. |
| "I'll copy the live colors first, then clean up later" | This usually leaves bad globals behind. Set the right tokens first, then style sections against them. |
| "I can tell which section matches by looking at the UI" | Visual similarity is not enough. Use `sections.md` and the actual schema constraints. **Check composition, layout mechanism, and interaction — not just how the colors look.** |
| "I only need screenshots, not a crawl" | Screenshot memory misses hierarchy, repeated modules, and linked-page patterns. Scrape the source site with Firecrawl first. |
| "I'll fill in the real images later" | The JSON generator cannot recover asset URLs you did not capture. Build the content manifest now, from the crawl output. |
| "The section only needs an image, the video is nice-to-have" | If the source block is a video, the matched section must support video or the mismatch must be flagged. Do not silently downgrade media types. |
| "It's the same concept so one section is fine" | If the same concept appears with two different visual treatments on the page, it needs two separate section blocks. |
| "It's basically a grid, just different styling" | A slider showing one item at a time with arrows/dots is NOT "basically a grid." Check the HTML for slider components before classifying layout. |
| "image-with-text works for everything with an image and text" | `image-with-text` is specifically a side-by-side split layout. It does NOT work for full-bleed overlays, stacked vertical layouts, or card grids. Match composition first. |
| "The origin sections are adjacent so I can merge them" | If the origin has two separate HTML sections (e.g., a background video + a separate rich-text block), keep them as two separate Weaverse sections. Merging changes the layout behavior. |
| "The section name matches, so it should work." | Section names describe purpose, not capability. Read the schema source code to verify every visual requirement — aspect ratios, responsive images, split widths, child types, animation support. |
| "The section has an image field, so it supports images." | One image field does not mean responsive images. Check for separate mobile/desktop image fields or `<picture>` element support if the origin uses responsive variants. |
| "The preview looks close enough, I'll skip user approval" | The approval checkpoint exists because the agent cannot judge visual fidelity the way a human can. Always stop and wait for explicit confirmation. |
| "I'll generate the preview after section mapping" | The preview must come before section decomposition. Its purpose is to catch scrape errors, missing content, and brand conflicts before committing to a section mapping that might be based on wrong assumptions. |
| "Placeholders are fine in the preview, I'll swap in real URLs later" | The preview is a fidelity check. Placeholder content defeats the purpose — the user cannot verify accuracy against placeholders. Use the content manifest's real URLs. |

## Example

Stakeholder says: `Make it look like the live site.`

Correct response: `I will match the live site where possible, but .guides/brand-guideline.md is the source of truth for conflicting brand decisions.`

## Common Mistakes

- `Exact screenshot thinking` -> match structure and feel, but keep the implementation reusable.
- `Global junk drawer` -> if one section owns it, keep it local.
- `Over-customizing old sections` -> if adaptation becomes awkward, create a clean new section instead.
- `Skipping registration` -> new sections must be added to `app/weaverse/components.ts`.
- `Ignoring the registry` -> use `sections.md` and `app/weaverse/components.ts` before inventing new sections.
- `Missing content manifest` -> the design spec is incomplete without a per-section table of real asset URLs, text, and links from the crawl. Without it, the JSON generator fills in placeholders.
- `Media type blindness` -> mapping a video hero to an image-only section, or an animated block to a static section, without flagging the gap.
- `Concept merging` -> collapsing two visually distinct occurrences of the same concept into one section block.
- `Layout blindness` -> matching by content type alone without checking composition (overlay vs side-by-side vs stacked), layout mechanism (slider vs grid vs full-bleed), and interaction (static vs carousel vs scroll). This is the most common cause of sections that render completely differently from the origin.
- `Section merging` -> combining two separate origin sections (e.g., a background-only video + a separate text block) into one Weaverse section, changing the visual hierarchy.
- `Skipping HTML analysis` -> classifying layout from the markdown crawl alone. Markdown strips slider components, grid classes, overlay positioning, and interactive elements. The raw HTML is required for accurate layout classification.
- `Name-matching without schema verification` -> a section named "hero-image" does not mean it can reproduce every hero layout. Read the section source code and verify schema settings (aspect ratios, responsive image fields, overlay options, child types) before classifying as REUSE.
- `Assuming aspect ratios are configurable` -> many sections hardcode aspect ratios (e.g., `aspect-square`). Check the actual schema enum values or CSS classes before assuming the section can produce the ratio the origin uses.
- `Ignoring responsive image requirements` -> if the origin uses `<picture>` with separate mobile/desktop `<source>` elements, a section with a single `image` field is not a match. The section needs `imageMobile`/`imageDesktop` fields or equivalent.
- `Skipping the preview checkpoint` -> the clone preview route exists so the user can catch problems before section decomposition begins. Skipping it means discovering layout errors after significant Weaverse mapping work is done.
- `Auto-approving the preview` -> the agent must not treat its own judgment as approval. Only an explicit user response ("approved", "proceed", etc.) unblocks section decomposition.
- `Preview without section markers` -> forgetting the `{/* === BLOCK NAME === */}` comments means the preview cannot serve double duty as a decomposition guide. Always include them.
- `Zombie preview route` -> forgetting to delete `app/routes/clone-preview.$page.tsx` after the Weaverse page is verified. It is a temporary artifact, not a permanent route.
