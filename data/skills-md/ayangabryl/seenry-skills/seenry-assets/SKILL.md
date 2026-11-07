---
name: seenry-assets
description: "Find, generate and integrate the visual material a design needs: photos, hero images, album or product art, PNG and 3D-style icons, UI icons, illustrations, textures and fonts. Sources license-clear assets from the internet (CC0/public domain photos, permissive icon sets, open fonts) and generates images when the host has an image model. Records provenance for every file. Use whenever a page or component would otherwise ship with placeholders, gradients or stock clichés."
license: Apache-2.0
metadata:
  author: Seenry
  version: "0.1.0"
---

# Seenry Assets

Real material is the difference between a studio result and a template. A placeholder gradient where a cover image should be, or an emoji where an icon should be, makes everything around it look fake. Every asset in a Seenry build is real, license-clear, art-directed and recorded.

## Decide the material first

Before searching, write one line per asset: its job, subject, crop and aspect, mood (light, color temperature, texture), and where it sits in the layout. "Album cover, 1:1, a person with warm autumn tones, face in upper third, used at 136px and 48px" beats "a nice image".

Then take the first route that can produce it at quality:

1. **Supplied or brand assets.** The user's logos, product shots, photos and fonts always win. Ask if they likely exist.
2. **Build it in code.** Product UI, charts, diagrams and simple geometric marks are sharper and more honest as HTML/CSS/SVG than as images.
3. **License-clear sources.** Photos, icons and fonts from the sources below via [the assets tool](scripts/assets.py).
4. **Generate.** When the host has an image generation tool (an MCP image tool, a built-in image model, the Codex CLI through `seenry/scripts/image.mjs`, or `OPENAI_API_KEY` / `GEMINI_API_KEY` for the assets tool), generate art-directed images: hero visuals, 3D-style icons, textures, covers, illustrations. Follow [generation](references/generation.md).
5. **Go type-led.** If none of the above reaches quality, remove the image and let typography, layout and one detail carry the design. A weak image is worse than none.

## Sources

| Need | Source | License to check | Tool |
| --- | --- | --- | --- |
| Paintings, drawings, prints (one art-directed set) | The Met Open Access | CC0 | `assets.py art-set --style <family>` |
| Photos | Openverse (aggregates Flickr, Wikimedia, StockSnap and others) | CC0 or Public Domain Mark by default | `assets.py images` |
| Photos (API key or manual) | Unsplash, Pexels | Unsplash License, Pexels License (free commercial use, no resale as-is) | host browser or their APIs |
| UI icons | Lucide (ISC), Phosphor (MIT), Tabler (MIT), Heroicons (MIT), Iconoir (MIT), Radix (MIT) through Iconify | Permissive; the tool refuses unlisted sets | `assets.py icons` / `icon` |
| Brand marks | The owner's press kit; Simple Icons (CC0 files, marks stay trademarks) | Trademark rules: unmodified, used to refer to that brand | `assets.py icon simple-icons:<name>` |
| 3D and illustrative icons | 3dicons (CC0), or generate a matched set | CC0 / provider terms | download or `generate` |
| Textures, HDRIs, materials | Poly Haven (CC0) | CC0 | download |
| Fonts | Google Fonts (OFL), Fontshare (ITF FFL), Open Runde (OFL), Inter (OFL), Geist (OFL) | OFL allows self-hosting and commercial use | download, self-host WOFF2 |

```sh
python3 scripts/assets.py images "portrait autumn" --count 6 --orientation square --out assets/raw
python3 scripts/assets.py icons "calendar" --set lucide --count 4 --out assets/icons
python3 scripts/assets.py icon lucide:play ph:pause-fill --out assets/icons
python3 scripts/assets.py generate "<art-directed prompt>" --size 1536x1024 --out assets/gen
python3 scripts/assets.py sheet --out assets/raw     # contact.html for side-by-side review
```

Openverse search is literal: use one or two concrete nouns ("vinyl", "portrait", "harbor fog"), then judge the results.

## Select like an art director

- Download 6–12 candidates, open the contact sheet, and crop each to the real aspect and size before choosing. An image that works full-bleed can fail at 48px.
- Choose for one coherent set: same light direction, color temperature, grain, camera distance and treatment across the page.
- Reject: watermarks, visible logos or artwork you have no rights to (a public-domain photo of a copyrighted album cover does not clear the cover), recognizable people in contexts that imply endorsement, AI artifacts (hands, text, melted edges), low resolution for the display size, and clichés (handshakes, people pointing at laptops, glowing brains, isometric blobs).
- Sample the accent color from the chosen image so the palette and material belong together.

## Integrate

- Export at 1x and 2x of the largest display size; WebP or AVIF for photos, PNG for transparency, SVG for icons and marks. Set `width`/`height` or `aspect-ratio`; `object-fit: cover` with a deliberate `object-position`.
- Icons: one set, one stroke weight, sized 16/20/24, colored with `currentColor`. Filled variants only for active or primary states.
- Transparent PNG icons and cutouts sit on the surface color they were designed for; check both themes.
- Fonts: self-host WOFF2, only the weights used, `font-display: swap`, preload the above-the-fold file.

## Record provenance

The assets tool writes `manifest.json` next to the files (source page, creator, license, URL, date, prompt for generated images). Carry the entries into the project's `DESIGN.md` asset table and keep any required attribution in the shipped product on a credits page or a small footer link. Never put a creator credit in a caption or overlay on imagery that stands in for the owner's own work or product (portfolio pieces, case studies, product shots, team photos): it tells visitors the work belongs to someone else. Before shipping, open the source page once more to confirm the license still shows.

## Never

- Fabricate a real company's logo, a real person's likeness, customer testimonials, press quotes or product screenshots.
- Ship a reference image from Seenry MCP or any gallery as final material; references teach direction, not files.
- Use an image whose license you could not verify. Say so and use a type-led or code-built alternative.
