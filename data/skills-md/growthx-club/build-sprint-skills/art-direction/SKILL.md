---
name: art-direction
description: Give the project one visual point of view, then generate images against it. Use before generating, editing or replacing any image asset — hero image, og:image, illustration, empty state, avatar, background, card art, favicon source. Also use when generated images look generic, "AI", off-brand, or when a set of images do not look like they belong to the same product. Skip for UI layout, CSS and component work, which belong to frontend-design and impeccable.
---

# Art direction

A model that can render anything will render something generic unless you tell it what this product looks like. The brief is the source of truth. The prompt is only how the brief reaches the model.

Never generate from the user's raw request. Anchor first, generate second, look at the pixels third.

## 1. Find or write the anchor

Look for `design/style-anchor.md`. If it exists, use it and skip to step 2.

If it does not exist, derive one from what the project already has. Read whichever of these are present: `tailwind.config.*`, `app/globals.css` or the equivalent stylesheet, the font imports in the root layout, the landing page copy, any images already in `public/`.

Fill every field from evidence. Ask only for what the repo cannot tell you, at most three questions, each with your recommended answer so the user can reply "yes":

```
❓ <question>

➡️ my suggestion: <recommended answer, one line on why>
```

Then write `design/style-anchor.md`:

```markdown
# Style anchor

Medium: <photography | 3D render | flat vector | collage | risograph | line illustration — pick one, never mix>
Palette: <3–5 actual hex values lifted from the app, named: background, ink, accent>
Light: <direction, hardness, time of day>
Materials: <surfaces and textures that recur: matte paper, brushed metal, soft fabric>
Mood: <three adjectives, earned from the product, not from a mood board>
Never: <the defaults to refuse: floating particles, glossy pedestals, lens flare,
        gradient mesh backgrounds, neon-on-black, handshake stock photos,
        anything the app's own UI does not do>
```

One medium for the whole project. A hero photo next to a flat-vector empty state reads as two products.

## 2. Pick the slot

Each asset is a slot with a fixed final size. Render at the listed size, then resize or crop to final — render sizes are multiples of 16px because the image models require it, and anything under roughly 0.65 megapixels is refused outright.

| Slot | Final | Render at |
|---|---|---|
| og:image / social card | 1200×630 | 1536×800 |
| Landing hero | 16:9 | 1920×1088 |
| Feature or card art (square) | 1:1 | 1024×1024 |
| Card art (portrait) | 3:4 | 768×1024 |
| Empty state / illustration | 4:3 | 1024×768 |
| Avatar / icon source | 512×512 | 1024×1024 |
| Favicon source | 512×512 | 1024×1024 |

Do not generate these — generating them is how a project starts looking cheap:

- **Logos and wordmarks.** Set them in type instead. Models mangle letterforms at small sizes and you cannot trademark what you cannot reproduce.
- **UI screenshots and mockups.** Screenshot the real app.
- **Charts and data.** Use real data and a real chart.
- **Recognisable people, brands or products** the project has no rights to.

## 3. Compose the prompt

Assemble in this order, every time:

1. The full anchor, verbatim.
2. Subject — what is actually in the frame, concretely. One subject, not three.
3. Composition — the crop, and **where the empty space goes**. Name it: "left third stays clear for headline copy". This is the step people skip and it is why generated heroes have text baked into the middle.
4. Light and materials, from the anchor.
5. The `Never` list, as explicit negatives.

Save finals to `public/images/<slot>.<ext>`. Keep drafts and intermediates in `tmp/` and delete them when done.

For text inside an image, quote the exact copy in the prompt and keep it to a few words. Long paragraphs will come back misspelled at any resolution.

## 4. Look at the pixels

A saved file is not a finished asset. Open the image you just made and compare it to the brief.

Rank what is wrong, with the fix for each, then choose one:

- **Pass** — ship it.
- **Targeted fix** — edit the existing image rather than regenerating, so the parts that are right survive.
- **Regenerate** — only when the composition itself is wrong.

Check, in this order: does the empty space still hold for the copy that goes there, is any visible text spelled correctly, is the palette the app's palette, is anything from the `Never` list present, would this sit beside the other assets without looking imported.

After two failed regenerations, stop. The brief is wrong, not the prompt — take it back to the user with what you saw.

## 5. Keep the set together

Every later image uses the same anchor file. When a new asset must match an existing one, pass the existing image in as a reference and edit, rather than describing it in words and hoping.

If the app's visual direction changes, update `design/style-anchor.md` first, then regenerate the affected slots as a set. Never leave half the assets on the old anchor.

## Generating

In Codex, image generation is built in — `$imagegen`, backed by GPT Image, no API key and no setup. It can also view the image afterwards, which is what makes step 4 real.

In other agents, ask the user which route they have before promising an image. The rest of this skill applies unchanged.

---

The brief-over-prompt structure and the Pass / targeted fix / regenerate gate are adapted from [AgriciDaniel/banana-claude](https://github.com/AgriciDaniel/banana-claude), MIT License. The style anchor and per-slot render manifest are adapted from the image templates in [nexu-io/open-design](https://github.com/nexu-io/open-design), Apache-2.0 License.
