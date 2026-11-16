---
name: charles-accent-heroes
description: "Generate award-level landing-page hero graphics: one striking subject big enough to leave the frame, under a named light, on a textured field; big type tied to the subject; a quiet real-site interface; and one bold accent colour far around the wheel from the other two. Each page is a close variation of a reference screenshot (or a written layout), rendered with GPT Image, checked, and fixed with targeted edits. Use when someone wants a website hero image, a landing-page or hero-section mockup, poster-like site graphics, or Awwwards-style hero art for a real or fictional business."
---

# Accent heroes

Images of a website's first screen that look like award-winning posters: one striking subject on a bold field, big type tied to the subject, a quiet but real interface, and one accent colour that makes the page pop. They are pictures of websites, not code: the image model composes type, subject and light in one pass, which is what lets a headline sit behind a face or catch an object's glow.

Read [references/craft.md](references/craft.md) before writing pages. It has the decision trees for type, headline and layout, the colour formula, and the tells that make a hero look generated.

## The bar

Every page passes all eight. Each one exists because breaking it made real pages look generated or forgettable.

1. **A real business, clear in a second.** A stranger names the offer from the picture, the wordmark and the button. The nav and button use the trade's own words (Retreats, Book a retreat). A clever metaphor that hides the business fails: nobody can tell what the page is for.
2. **One poster subject, big enough to leave the frame.** One product, object or person. Either the frame crops it, or one long part of it (silk, a ribbon, a cable, light rays, glass tubes, a splash, petals) sweeps across the frame and off an edge. A whole product floating in the middle with a margin all round reads as a catalogue shot. Movement is welcome when it is shot as a poster: one dancer mid-leap or one kayaker mid-stroke, filling the frame on a plain field or a stage. Never a small figure in a wide scene: tiny faces, hands and crowds are where image models give themselves away.
3. **One bold accent.** The most vivid colour on the page, 120-180° around the wheel from the other two colours (75° at the very least), covering 15-30% of the frame. It is the subject's own main colour (its light, paint or material) and may spill onto the headline. Choose a cobalt parasol, not a cobalt-and-white one: a two-colour subject halves the accent. Never a thin line or a small object, because a polite accent leaves the page flat. When pushing the share further would add a tell, stop: a page that reads bold at 320 px beats a higher number. The one exception to the distance is the tonal route: the accent is the light itself, in the field's own colour family but far brighter than anything else (craft.md).
4. **A headline tied to the subject.** The subject lights, fills or crosses the type, or one word takes the subject's accent (craft.md's tree). A headline with no link to the picture reads as pasted on.
5. **Type that runs behind the subject, evenly spaced.** Set the headline as if the subject stepped in front of it afterwards: with the subject removed, the words would sit perfectly spaced. Never open a gap in a word to make room for the subject; it reads as type that stops for a head. The subject may hide one letter of a word that can still be read (the middle V of VIVID), never more.
6. **A material, not a flat colour.** The field is plaster, paper, ink, glass, metal or fabric from the brand's world. Flat digital colour is the first thing that looks generated.
7. **Photographed, not rendered, under a named light.** Every page names one of craft.md's light setups. Light the model isn't told about comes out soft and even, the catalogue look of the flattest pages. People get real skin and film grain. Objects keep real proportions and crisp small parts. No fire, lava or lightning unless it is the product.
8. **Three small captions at most**, each real information: a date, a spec, a price, a place. Slogans in every corner are filler.

Never use a real brand's name, logo or product, or a real person.

## References

Each page is a close variation of one reference: a screenshot of a hero section you admire, from the user's own folder of them (Awwwards, Godly and Land-book are good sources). Ask for that folder first. The reference rides along as the image the model edits, so its layout, type system, small type and finish carry over, which a written prompt alone loses. The page replaces the brand, the subject and every word.

- Crop each reference to the hero only, at 3:2, cutting away any strip of neighbouring images, and keep the crops in `<folder>/out/refs/`. Use poster-like heroes; skip SaaS heroes with logo rows and UI cards, which turn into template-looking pages.
- Never copy a reference's people, logos or text, and never publish or commit the screenshots: they are other designers' work.
- No references? Leave `ref` out. The page's `layout` then becomes a written composition. It works, but expect more re-rolls.

## Run it

Needs Python 3 with numpy, requests and Pillow, and `OPENAI_API_KEY` in the environment or in a `.env` in or above the project folder. The word check uses macOS Vision; on other systems it is skipped, so read every word by eye.

```bash
python3 -I <skill>/scripts/heroes.py <check|render|fix|review|board> --project <folder>
```

`<folder>` holds `concepts.json`. Everything generated goes to `<folder>/out/`; keep `out/` out of version control.

### 1. Plan the batch

Ask how many pages (four if unsaid) and for which businesses; invent fictional ones when none are given. Then set the batch:

- Several businesses: each a different kind (product, hospitality, studio, property, hardware, food, culture, gallery show). One business: each page a different reference and subject.
- Each reference once.
- At most half the pages share a layout; six pages or more use at least four layouts (craft.md).
- Accents spread round the wheel: no 30° stretch holds more than two.
- Adding to pages you already have? Pass their `concepts.json` with `check --also` to see which of them each new accent sits near.

### 2. Write the pages

One entry per page in `concepts.json`, keyed by a short page name:

| Field | What goes in it |
| --- | --- |
| `ref` | The reference screenshot: an absolute path, or relative to the project folder |
| `brand`, `what` | The fictional name; what it sells and to whom |
| `layout` | One of craft.md's layouts |
| `subject` | The poster subject in one sentence, its materials and light named |
| `background` | The field's material (bar 6) |
| `light` | One of craft.md's light setups by name, and where it falls: "one stage spot from high left, the dancer lit, the stage falling to dark" |
| `headline` | Two to four words: a plain promise, a name or a place. Never an idiom pun |
| `headline_note` | The type system (craft.md's tree), which word takes the accent, what the subject does to the letters, and the one letter it hides. It goes into the image prompt word for word, so write it as an instruction to the model |
| `ui` | Every small text, quoted: wordmark, nav, button, up to three captions |
| `palette` | Three `[name, hex]`: field, second colour (type and quiet surfaces), accent |
| `route` | Leave it out, or `tonal` when the accent is the light itself in the field's colour family (craft.md) |
| `variations` | Five near neighbours of the same page, each changing one thing: the crop (the whole subject, or cut by two edges), the moment (still, or the peak of its movement), the camera (lower or closer), or how far its long part sweeps. Five, because a standout render is rare and renders of one prompt differ a lot. Never another accent colour, because the prompt and the check hold every render to the page's palette. Never five different ideas either: the user picks one version of a page they like |

Check the plan before spending anything:

```bash
python3 -I <skill>/scripts/heroes.py check --project <folder>
```

With no renders yet it tests the palettes, the spread, the layouts, the references and the missing fields in a second. Fix every flag in `concepts.json`; never work hue gaps out by hand.

### 3. Render

```bash
python3 -I <skill>/scripts/heroes.py render --project <folder>
```

Five renders per page, twelve at a time, about a minute a wave, about $0.05 each. `--dry-run` prints the prompts. Show the cost before a run over $5.

### 4. Check and fix

Run `check` again: it reads every word back and measures each accent's share. Then open every render at full size and at 320 px (`review` writes both) and walk craft.md's tells.

Fix a near-miss with an edit, never a re-roll: an edit keeps everything and changes one named thing.

```bash
python3 -I <skill>/scripts/heroes.py fix --project <folder> --render <page>-2 --note "shorten the foot of the L so it sits clear of his collar"
```

`fix` makes two versions. Keep the better one, and move the other, along with the render it replaces, into `out/variants/superseded/`; never delete one. A render with two problems gets two edits, one after the other: the text holds through at least three rounds. Re-roll only when the page itself is wrong (the subject, the reference or the headline), by changing its entry.

### 5. Show them

```bash
python3 -I <skill>/scripts/heroes.py board --project <folder>
```

Every render in a dark gallery, numbered per page, at `<folder>/out/board/variants/index.html`.

## Model

GPT Image 2.6 Sunburst at quality "high" (`MODEL` in the script). It was chosen over Nano Banana 2.1 and Nano Banana Pro in a side-by-side test; "xhigh" and "max" cost 3.4 and 7.7 times as much for finer micro-texture only. Before a run, check the OpenAI models list for a newer GPT Image model and tell the user if there is one.
