---
name: charles-unslop
description: "Turn AI-looking UI into a designed interface with its own point of view: audit the tells, write a direction from the product, delete before restyling, fix spacing, color, icons, copy, type, layout and details in order, then give the screen one rich moment only this product could have. Use when a screen looks AI-generated, vibe-coded, generic or templated, when reviewing agent-built UI, or when asked to unslop, de-slop or make something stop looking like AI. Triggers on purple gradients, gradient text, glassmorphism, glows, emoji icons, sparkles, pill badges, centered heroes, three-card and bento grids, greeting headlines, fake proof, uppercase tracked labels, uneven spacing, pulsing elements. For making a screen that is already designed feel finished, use charles-polish."
license: CC-BY-4.0
---

# Unslop

Adapted from [unslop](https://github.com/heydamir/unslop) by Damir Sokolovsky ([@heydamir](https://x.com/heydamir)), CC BY 4.0, merged with Emil Kowalski's unslop-design skill and with feedback from Charles Liu's "Removing AI Slop" series. Changes: the passes were reordered around subtraction, and the rules on backgrounds, brand icons and materials were rewritten. Keep this credit in copies.

Nobody can point at the one element that makes a screen look generated. A model picks the most common option for every decision at once, and fifty median choices compound into a watermark. So fixing one element does nothing: walk the whole screen, in order.

Removing the tells is half the job. A clean screen that could belong to any product is the next template. Slop spreads richness over the chrome; craft keeps the chrome quiet and spends it on one moment.

## Run it

1. **Render it.** Screenshot the screen at its real size and judge that, not the code. If it will be seen small (a phone, a video, a thumbnail), judge it at that size too.
2. **Audit.** Walk [references/signs.md](references/signs.md). List every sign, one line each, with where it lives.
3. **Choose the scope** from the audit:
   - Signs across color, type, icons and copy → run everything below.
   - A designed screen with a few signs → fix only those. Keep its palette, type, layout and visual. Put bigger ideas in the report.
   - No signs → say so, suggest at most three refinements with exact values, and stop. Never change a good screen to make it different.
4. **Write the direction** (below). Show the audit and direction and wait for an answer, because a wrong direction redoes everything. Skip the wait only if told to just do it.
5. **Subtract.**
6. **Run the passes in order,** finishing each across the whole screen.
7. **Run the final audit.** Anything that fails goes back to its pass.

Keep the product. Features, real content and section order stay, and the product keeps its name. Never invent capabilities, or claims and facts about a real product; a new way of presenting something the product already does is design, not an invented feature. Placeholder content in a demo or mock may be replaced with specifics. Filler like "Powered by AI" or "Follow us for deals" isn't a feature, so it can go.

## Direction

Five lines, derived from what the product does, never from what's trending.

- **Product:** what it does and for whom, in one sentence.
- **Character:** two or three concrete words, like `calm, exact, a little warm`. Clean, modern, sleek, minimal and premium are banned because they describe every template.
- **World:** the place or material the product belongs to. A tide-table app lives near salt, charts and low light; a tax tool near ruled ledgers. The world sets the neutral tint and the accent. It doesn't have to become a picture.
- **Moment:** the one or two places the screen gets its richness. See pass 8: it may be a behaviour, real content, proportion, type or an object.
- **Signature:** one small detail only this product would have, used consistently.

Then write the **concept**: one sentence every later choice can be checked against. Example: "Every invoice reads like a letter from one person to another." Two checks before you keep it:

- **Does it survive the next state?** Walk it through empty, in use and done. A concept that only works on the opening frame is a poster, not a concept.
- **Did you write it to justify something you already wanted?** Then it filters nothing. It must rule out at least one thing you'd otherwise do.

**If the screen names no product,** ask. If you can't ask, or were told to just do it, then:

- A mock or demo: assume one specific, plausible product and write the whole direction for it, with `Product (assumed):` so it can be overruled. Never use a stray word in the copy as the world, and don't default to SaaS. Assume something with a particular world, since that's what gives the palette, type and accent something to come from. It must fit the features you're keeping: a GitHub button rules out a bakery. The world needn't become an object on screen. White, black and a system font with no reason is a template too.
- A real product you don't know: keep it neutral, make no claims, and list what you'd need to know.

Keep a real brand mark or color. A violet-to-blue gradient, a sparkle tile or a glossy orb doesn't count as brand unless the user says so.

## Subtract first

Agents add. A caption restating the heading, an icon on every label, a divider spacing already provides, a border on a surface with a shadow, a second CTA, a helper line under the input. Each is defensible and together they compete.

Walk every icon, line, badge, caption, container and word and ask: **what breaks if this is gone?** "Nothing" means delete. "It adds interest" and "it fills space" are why the model put it there, so they don't count. Walk twice, because deletions expose each other. The one signature from the direction is exempt, and only that one. If an element carries information people need (a password's rules, a price), move it, shrink it, or make it the moment; don't lose it.

The cuts generated screens need most:

- **Dividers.** Delete every divider that spacing can replace; proximity already groups things, and lines add noise. Lists, settings rows and suggestion chips almost never need them. Lines in a ledger or a table that help the eye track across a row can stay.
- **Subtitles under titles.** Delete unless they say something the title can't.
- **Nesting.** A container inside a container inside a card is a tell. If a map, image or chart is the content, run it to the edges of its parent. Delete wrappers until each surface has a job.
- **Two mechanisms for one job.** A progress bar and a step counter, a toast and a visible change, an icon and a label saying the same thing. Keep the better one. This isn't cutting a feature: the job still gets done.
- **Bolted-on controls.** A button floating beside a field belongs inside the field, as part of its empty or focused state.
- **Chrome the moment doesn't need,** like a Share button on something with nothing to share yet.

## The passes

The order matters: rhythm changes how everything else reads, and copy length decides type size and layout. Visuals and motion come last so they fit a screen that already works without them. Exact starting values are in [references/tokens.md](references/tokens.md).

### 1. Spacing
- Everything sits on a 4px grid. Replace one-offs like `mt-[13px]`.
- Same thing, same size: one row height, one gap, one card padding per set.
- Gaps inside a group are smaller than gaps between groups, so grouping needs no lines.
- Icons sit in one column, labels start on one line, numbers right-align. Nothing is nudged off its line.

### 2. Color
- One neutral ramp tinted toward the world, with three text roles. Five lavenders means nobody chose.
- Cream paper with muted earth tones is the post-AI default, the way indigo was. Use it only if the world demands it, and never because it feels tasteful. High-chroma color, pure white and near-black are all fair if the character calls for them.
- One accent in the chrome, covering a few percent of the screen. Unchosen purple is the loudest tell, so derive the hue from the world.
- Working screens people stare at (apps, dashboards) keep neutral surfaces; color lives in the content.
- Delete gradient text, colored glows and colored shadows, neon borders, and blobs behind content.
- Text keeps 4.5:1, including over backgrounds.

### 3. Icons
- Emoji become line icons from one set, at one size and stroke, in a text role's color. Emoji can't take your palette and read as placeholders.
- **Exception: third-party logos keep their real colors.** Google multicolor and Facebook blue are recognized before they're read (recognition over recall). Grey logos make people read.
- ✨ doesn't mean AI. If AI matters, the copy says what it does.
- An icon's end state must read on its own at 20–24 px. If it needs its animation to make sense, redraw it.

### 4. Copy
- Could a competitor paste this headline unchanged? Then rewrite it with this product's nouns.
- No exclamation marks, greeting headlines, hype words, or trailing periods on labels and buttons.
- A change says what it compares to: `+12% vs last month`.
- Read each line next to what's already on screen. If it repeats a number or a word nearby, cut it. A short line that's trying to sound charming reads as AI; say the plain thing.
- **Mock content is specific.** Never Maya, Sarah, Alex, Acme or John Doe; those names mark the screen as generated. Use a real-sounding person and detail: "we burnt the first batch, so yours is from the second" beats "thank you for your purchase".
- Fake proof gets deleted. If a claim can't be checked, ask, then make it specific or cut it. A real number is the strongest copy there is.

### 5. Type
- Choose type for the character. One interface family plus at most one partner, used for one distinctive decision. A display face appears once.
- Weights 400–500, 600 for rare emphasis. Hierarchy comes from size and color, never 800–900.
- Sentence case. Uppercase with wide tracking becomes sentence case, unless the real object you borrowed is uppercase, like a stamped tag or a boarding pass.
- `tabular-nums` and one number format across the screen. Negative tracking only on display sizes.

### 6. Layout
- Everything stacked and centered, three equal cards, bento grids, and a picture panel beside a form column are all defaults. To get out of the last one, let the form sit in the material rather than beside it. Size by content: give the important thing more room and let content break symmetry.
- Check the largest viewport too. A dead band is empty space with no material and no job. Fill it with the world (a surface, real content) or compose the form into it; don't just scale the type up.
- One primary action and at most one secondary.
- Apps keep real app proportions. Heroes are composed as a whole first screen with no dead band.
- The smallest viewing size is a layout. For a video or thumbnail, and only then, keep 24–32 px of air, let nothing hit the frame edge unless it's meant to bleed, and keep every word people need at 16 px or larger at that size.

### 7. Details
- Inner radius = outer radius − padding, never below 4. Not everything is a pill, and `rounded-2xl` isn't an answer.
- Control shape comes from the character, not the token table. Exact and technical: 2–6 px, thin fields. Soft and human: larger radii or full pills. Editorial: underlined fields, text buttons. Justify the shape from the character in one sentence; a 12 px radius "because it's standard" fails.
- One depth cue per surface. Border + shadow + ring + gradient is a model hedging.
- No dotted lines or dotted dividers unless the object is really perforated. They're the fastest way to make a chart or form look generated.
- Stat cards are numbers: no sparklines or icons to fill them. One main chart, one accent per chart.
- Hover and focus exist and stay inside the palette.

### 8. The moment
Agents jump to one of two templates: a flat illustration of something from the product's world, or a giant word above an ordinary form. Both look designed in a still and neither means anything. Don't take the first option that renders. Sketch one idea from each of these, in a sentence each:

1. **Behaviour:** something the interface does that only this product would do. It may look plain at rest.
2. **Real content:** the product's data, drawn with care, or its actual output.
3. **Proportion:** the important thing takes 70% of the screen and everything else gets out of the way.
4. **Type:** one size contrast, one huge number, or one line of copy set as the whole screen. It must carry meaning: the number is the answer, or the sentence changes as the state does. A big "Log in" fails, because the word isn't saying anything.
5. **A surface or object,** using the tree below.

Keep the one that passes both tests:

- **Is it an idea?** Take away the styling and describe it to someone. "Huge serif headline" isn't. "The invoice total is the page, and each paid line crosses itself off it" is.
- **Is the rest frame good on its own?** Most people only ever see the first state, so an idea that only appears after typing needs a rest frame that's already composed and already from this product's world. Big words above small controls, with the rest of the screen empty, fails however clever the next state is.

Then build its next state too. A concept you've only drawn isn't tested.

The display type sizes in the tokens are defaults, and a type-led moment overrides them.

```
How long do people stay on this screen?
├── Minutes or daily (app, dashboard, settings, chat in use)
│   → neutral surface. The moment is content.
└── Seconds, as a doorway (login, empty state, confirmation, hero)
    → a field or object is allowed if it passes all five:
      1. Reason: someone who hasn't seen your concept can guess why it's here.
      2. Palette of at most three hues, taken from the world.
      3. Real structure: light, depth, focus. A two-stop wash is not a field.
      4. The UI on top stays quiet and legible.
      5. Stock check: at the viewing size, could this come from an illustration pack or a template gallery? Layered flat hills, gradient suns and a dashed trail fail. If it does and two attempts don't fix it, go back to 1–4.
```

A gradient is slop as decoration and craft as material. What decides it is whether it has a reason, a chosen palette and quiet UI on top.

**Texture is optional.** Add at most one layer, and only to fix a named problem, like a gradient that bands:

| Texture | Use when | Fails when |
| --- | --- | --- |
| Grain or stipple | A gradient bands or feels digital; warm, physical worlds | Applied as a uniform trend layer to a flat color |
| Halftone dot grid | Over soft photographic color, to add structure | Dots compete with text |
| Topographic lines | Worlds with terrain, routes, data | Bright or dense enough to read as a pattern |
| Concentric rings | One focal object to radiate from | No focal object |
| Fluted glass | Something high-contrast sits behind it | Nothing to refract: it becomes a striped print |
| Pixel or reaction-diffusion | Editorial, heritage, high-contrast brands | On a plain modern interface, where it reads as a filter |

**Materials must earn themselves.** Frosted glass needs something meaningful behind it. Refraction needs a subject to bend, and text should bend through it without shattering. Liquid metal, chrome and glossy 3D are AI defaults when abstract; they're allowed only when the object means something in this product. A logo that does a job beats a logo that shines: a lighthouse mark whose beam sweeps while a backup runs is better than a chrome orb.

**Honor the object.** If you borrow a real thing, it must behave like one: paper doesn't fade, a lock's pins move the right way, and you don't write your reply on the letter you received.

**Characters and illustration** must look drawn for this page: colors from the page's palette, features in its ink, one line weight, no solid black masses or glove hands. If it reads as a sticker or emoji, redraw or remove it.

How to choose and generate scenes and objects is in [references/visuals.md](references/visuals.md); code treatments are in [references/effects.md](references/effects.md).

### 9. Motion
- Delete motion by default: looping pulses on things that aren't live, shimmer on headings, breathing glows, parallax, `transition-all`, `hover:scale` on cards, every section fading in on scroll.
- Keep motion that explains something. Tuning what's left is the polish skill's job.

## Final audit

1. Swap in another product's name. If the screen still fits, push the copy, visual and signature harder. (Assumed product: use its name. Truly neutral screen: skip this.)
2. What here would make a designer suspect a model built this? Fix it and ask once more. If you were given references, put yours beside one at the same size, name the gap and fix that.
3. Name the one choice a competitor couldn't paste. No answer means the moment isn't done. (Truly neutral screen: name the choice that comes from this screen's job, not from its styling.)
4. Delete one more thing. If something breaks, put it back and stop.
5. Compare with the audit list and report the direction, what changed per pass, and any prompt you wrote.
