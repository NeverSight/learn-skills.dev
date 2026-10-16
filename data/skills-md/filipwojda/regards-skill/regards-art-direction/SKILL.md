---
name: regards-art-direction
description: Art direction for websites from live research on regards.design, a hand-picked index of real website sections searchable by look. A fork of tasteskill v2 (MIT, Leonxlnx) that keeps its inventory, idea test, open-collection pictures, real-browser inspector and look-and-fix loop, and replaces the deal of 20 fixed directions with a search of real sections for this one brief. Use it whenever you design, redesign, restyle, polish or review a landing page, marketing site, portfolio, product page, one-pager, hero or any public-facing web page, in any stack, and when the user says a page looks generic, templated, "AI-made" or like every other site. Needs the regards.design MCP server for the research step. Not for dashboards or app screens.
---

# regards art direction

A page made by a model usually looks like the average of every page the model has seen: a centred
headline over three lines, a little label above it, a row of icon cards, a soft gradient, a few thin
rules and a monospace caption. Nothing in it is wrong and nothing in it was decided.

This skill replaces those defaults with decisions, in four ways:

1. **Real references decide the direction.** Asked to invent a look, a model returns the category
   default. A fixed deck of directions only moves that default somewhere else: every project that
   draws the same card gets the same page. Here the agent searches regards.design, a hand-picked
   index of real website sections read by how they look, for this brief only. It looks at the pixels,
   keeps five to eight sections, names the one thing it takes from each, and derives the direction
   from what it kept.
2. **The idea comes from the subject.** What separates the best sites from the forgettable ones is a
   concept taken from the thing itself, not the styling. References feed the idea; they never replace it.
3. **A house style with no ornaments,** measured in a real browser by `scripts/inspect.mjs`, so the
   rules are checked rather than hoped for. A reference you studied can earn an exception; habit cannot.
4. **You look at what you made.** Screenshots at three widths, a juror's rubric, the references side by
   side, fix, look again.

One warning learned in testing. Taking the ornaments away is only half the job; a page that has lost its
labels, rules and cards and gained nothing in their place reads as thin. The other half is substance:
type set larger, whole fields of colour, real pictures of this subject's world (found or drawn), and
every section carrying its full content. Do not trade it for restraint.

In the commands below `<skill>` is this skill's folder. Run them from the project's root, so the
working files land in `.taste-skill/` there (the folder name is kept from tasteskill so its scripts work
unchanged). The scripts need Node 22+ and an installed Chrome, Edge or Chromium, and install nothing.
`assets.mjs` also needs network access; it uses no API keys.

**Before anything, check for the regards tools** (`search_sections`, `view_section`, `get_section`,
`page_sections`, `similar_sections`; your client may prefix them with the server's name). If they are
missing, tell the user once how to connect them:

```bash
claude mcp add --transport http regards https://mcp.regards.design/mcp
```

Then carry on with the fallback in step 3 and say so in the report. If your client reads MCP resources,
read `skill://regards-design/SKILL.md` before the first search.

## The run

Do these in order. Steps 1 to 5 decide whether the page is any good.

### 1. Read the brief and the project

Find out what is real: the subject, the audience, the one thing the page must get someone to do, the
stack, any existing brand (colours, fonts, logo), and above all **what imagery truly exists**: the
project's own photographs or product shots, a real interface that can be shown, an image generation
tool you can call, or nothing. Do not plan around pictures you do not have. Nothing of its own is
rarely nothing at all: the subject's city, street, materials and history are in open archives and
museums, free to use with a credit (step 6, `scripts/assets.mjs`).

If the request is vague, decide and state your reading in one line instead of asking. Ask only when a
missing fact blocks the work (for example, no product name).

Then **inventory the subject** in your notes: eight to twelve things that belong to this client and to
no competitor. Look for its name and what the name means; its address, door number, street and
neighbourhood, and what that place looks like (its tiles, signs, paint colours, typefaces on its shop
fronts, its light, its weather); the numbers in the brief (seats, rooms, minutes to the sea, the
price, the year); the constraint it lives with (only one batch a month, closed in winter, by
appointment); its materials and colours; its rituals and hours (the oven lit at five, the ferry at
seven); the printed things of its world (a timetable, a label, a ticket, a sign). This list is where
the idea comes from in step 4, where your searches come from in step 3, and where your picture queries
come from in step 6.

### 2. Write the argument

Before any design, list the page as claims with their proof, one line per section, the way
`references/copy.md` §1 shows. The claims decide which sections exist and in what order. Delete any
section that has no claim. This is how you avoid the stock sequence of hero, logos, three features,
testimonial, pricing, call to action. The argument is also your list of component searches in step 3.

### 3. Research the direction on regards

This step replaces dealing a direction from a fixed library. `references/regards.md` has the search
recipes, good and bad specimen notes, and the mutation moves. The short form:

**Search from the inventory, not the category.** "Law firm website" returns the category, which is
the thing you are trying to leave. Search for what your inventory names and what it could become:
its printed things ("a price list set like a printed label"), its materials ("raw paper, stamps,
packaging"), its measurements ("numbers and ticks that measure something real"), its feeling, and any
site the user named ("sites like <their site> but quieter"). Three passes:

1. **Mood:** two or three short searches for the overall feeling, from different angles (layout,
   type, imagery, texture).
2. **Components:** one search per claim in your argument (the hero, the list or menu, the proof, the
   booking, the footer), plus one for detail: line work, borders and frames, how numbers are shown.
3. **Widen and drift:** `similar_sections` from the two or three keys you liked best, and one oblique
   search that is deliberately far from the brief (a word from the subject's world, or an empty query,
   which browses the most distinctive sections). Ask for "experimental" or "unusual" in words when the
   results feel safe; novelty runs from 1 (template) to 5.

Instant search is the default and is rate-limited per minute; Deep search costs a credit, so keep it
for a nuanced brief, a "not X", or sites like a named one.

**Look before you keep.** A hit's summary is one line; the design is in the pixels. Open every hit you
might use with `view_section` and reject most of them. Use `get_section` for a section's text, sizes
and page, `page_sections` for a whole page's rhythm.

**Keep five to eight references, one thing from each.** Never more than one from the same site. For each,
write a specimen line in `.taste-skill/references.md`:

```
profound/08 · https://www.regards.design/sections/profound/08 · live: https://www.tryprofound.com/
takes:   sheets of graph paper with binder holes, filed behind angled folder tabs
leaves:  the dark ground, the generative squares, the product copy
becomes: a seed library's drawers: one tab per season, one sheet per variety, the real packet on each
```

"Nice layout" is not a specimen. Name the component so precisely that someone could find it on the
page from your words alone, then say what it turns into for this subject. If you cannot fill
`becomes:` from your inventory, the reference is decoration: drop it.

**Derive the direction from what you kept,** and write it under the specimens in the same file, one line
each: the idea sentence (step 4), the hero, each section in the order of your argument with the
specimen it draws on, the type (the classes your references use, set in free faces you can load; never
a reference's licensed typeface), the palette (proportions from the references, colours from the
subject's own material where it has any), the motion, and the signature detail someone would
screenshot. Re-read this sheet before each section you make.

**The reference competitor test.** Put the nearest real competitor through your searches. If it would
end up with the same specimens, your searches came from the category: search again from the inventory.

**Never copy.** Take an idea, never a section: no layout reproduced whole, no copy, logos,
illustrations, photographs or brand marks from a reference. The test, applied in step 8: set each
finished section beside the reference it drew on. If a visitor could mistake one for the other, mutate
further.

**Fallback without regards.** If the tools are missing or fail, deal a direction from the bundled
library the way tasteskill does (`references/draw.md`), and say in the report that the direction was
dealt, not researched.

### 4. Find the idea

The direction is a way of composing. The idea is what makes the page belong to this subject and no
other. Write this sentence in your notes and do not start making anything until both blanks are filled
from the subject itself:

> On this page, **[something that belongs to the subject]** becomes **[the device your references point to]**.

Places to look for the first blank:

- **Its output.** What does the thing produce? Put the real output on the page as material.
- **Its object or shape.** What does it physically look like, in cross-section, in silhouette?
  Enlarge it, crop it, make it the frame or the one motif.
- **Its name.** Can the letters hold a photograph, stack into a wall, split to two corners, be measured?
- **Its place.** Is there one view that makes someone want to be there?
- **Its ritual.** Is there a sequence the page can perform as it scrolls?
- **Its artefact.** What printed thing already exists in its world: ticket, menu, label, receipt,
  invitation, folder, manual?
- **Its opposite.** Which other category owns the feeling this one lacks?

Fill the first blank from your inventory, not from the category. **The competitor test:** put the
nearest real competitor in the sentence. If the sentence still works, the idea belongs to the
category. "Clean and modern" is not an idea.

If no reference points to a device that can carry the idea, go back to step 3 with the idea as the
query. The idea leads; the references serve it.

**One live thing.** Give the page one thing the visitor can do, or that is different for each visit,
made from the idea: pick a wood and see the chair in it; type your name and see it cut in the
foundry's letters; set the loan and read the real monthly figure. Rules: it uses the subject's real
content, it works on a phone with a thumb, it has a plain fallback without script, it never blocks
reading, and it is one thing, not a playground. It is made in step 6 as part of the page.

### 5. Write the words

Write the whole page as a copy deck (plain text) before markup, following `references/copy.md`:

- **Every headline fits in two lines or fewer at every width.** Do the arithmetic in copy.md §2 before
  committing to a sentence: about 32 characters is safe everywhere at a confident size.
- One supporting sentence. One primary action, named for what it does, as a real button on the first
  screen.
- **The first screen answers the visitor's first question in large type.** For an event: what it is,
  when and where. For a product: what it is and what it costs or does. For a person: who and what they
  do. Every section the visitor came for has its own heading and its own place in the navigation.
- **Write the full content.** Every section the brief asks for delivers its information completely.
  Thin sections are the commonest reason a clean page loses to a busier one.
- Sample details are expected where the brief leaves gaps, so the design is seen at full density; list
  them in the report for the client to confirm. Proof is never invented: no customers, quotes, reviews,
  press, logos or business statistics.
- Never take words from a reference.

### 6. Make it, still

Make the page with motion switched off in your head; a page that needs animation to look finished is
not finished. Order of work:

1. **Tokens.** Colour and type roles from your direction sheet as CSS custom properties. Everything
   downstream references tokens only. `<skill>/assets/base.css` is a neutral foundation you may start
   from; it has no look of its own.
2. **The hero, from its line on the sheet,** at desktop and at phone width. Get the big thing big and
   the small things small before anything else exists.
3. **Each section from its line on the sheet and the specimen behind it,** with this project's content.
   Neighbouring sections must not share a layout. **Carry the idea into every section,** pricing, FAQ and
   footer included: the commonest failure, even among good sites, is a distinctive first screen followed
   by stock blocks.
4. **Imagery,** in this order of preference:
   1. the project's own;
   2. generated, if you have an image tool;
   3. **real pictures of the subject's world from the open collections,** whenever an honest one
      exists. Search them with `node <skill>/scripts/assets.mjs "<query>"` (Openverse, Wikimedia
      Commons, the Art Institute of Chicago and the Met; only licences that allow commercial use, by
      default). Search the inventory, not the category. `--get <ref>` downloads it into `assets/` and
      records its source and licence, and `--credits` prints the credit line for the footer. A found
      picture shows the world around the client and is never presented as the client's own product,
      room, dish, person or team;
   4. **drawn in code from the subject itself,** for what no honest picture exists of;
   5. type and colour alone.

   Never use a picture from a reference.

   **The floor, which the inspector checks:** at least four real pictures on the page, usually six to
   twelve. SVG drawings do not count toward the floor. Add one moving picture wherever an honest clip
   exists (`assets.mjs --video "<query>"`). `references/imagery.md` covers searching, licences, credits,
   video, drawing, crops and treatments.
5. **The live thing** from step 4, in the section where it proves the claim, with real content, a
   thumb-sized phone version and a plain fallback.
6. **Material.** Give the page its material (§ Material below): colour as whole fields, printed things
   drawn as paper, line work that carries data, at most one metal accent. Restraint makes a page tidy;
   material makes it one worth showing.
7. **Fullness.** Look at each desktop screen as a poster: one dominant thing and the content it
   carries. One deliberate rest per page is the limit. Running text is in the full ink at 16px or more.
8. **States and semantics.** Real links and buttons, visible focus, alt text, a phone layout that is
   its own composition.

Read `references/type.md`, `references/colour.md` and `references/layout.md` when you need the detail
behind a decision; the laws below are the short form.

### 7. Gate

```bash
node <skill>/scripts/lint.mjs <source files or folder>
node <skill>/scripts/inspect.mjs <url or path/to/index.html>
```

`lint.mjs` scans source for banned patterns and stock phrases. `inspect.mjs` opens the page in a real
browser at 1440, 768 and 390 pixels, measures it and saves screenshots to `.taste-skill/inspect/`.
Fix every `FAIL`. Treat each `WARN` as wrong unless you can defend it to a designer in one sentence.
Re-run until there are no `FAIL`s. Exceptions you earned in step 3 (see the house rules) are read from
`.taste-skill/direction.json`; do not add any other.

### 8. Look

Passing the gate means nothing banned was measured. It does not mean the page is good. Open the
screenshots the inspector lists and critique them with `references/critique.md`. Then do the
reference pass: open each specimen with `view_section` beside the section that drew on it, and answer
two questions in your notes. Did it take the named thing, at the quality of the original? Does it look
like none of them? Fix the top three problems, run the inspector again, look again. Three rounds at most.

Judge only the pictures. If a problem is visible in a screenshot, it is real, whatever the code says.

### 9. Move

Now make the motion layer. It is required, and it is more than one fade: the inspector fails a page
with fewer than eight elements that really move while it loads and is scrolled. The layer has four
parts: the signature move from your sheet, done well; an entrance for the parts of every section
(heading, then text, then picture, staggered 60 to 90ms, rising 16 to 32px, once); feedback on every
control; one moving picture. Transform and opacity only, every move with a `prefers-reduced-motion`
fallback. If a reference's motion is your signature move, `view_section` shows a still: read
`get_section` for how it moves and open `links.live` if you can. `references/motion.md` has the tokens
and recipes. Run the inspector once more and check every screenshot for content that failed to appear.

### 10. Report

Tell the user, briefly: the searches you ran (the queries, in a list); the specimen sheet, each
reference with its regards link, its live link, what you took and what it became; any house-rule
exception and the reference that earned it; the idea sentence and the live thing; the final scores
from your last critique round and what still falls short; every found picture and clip with its
credit and where the credit sits on the page; and any sample content that must be swapped before
launch. If the direction was dealt from the fallback library, say so. Do not claim a check you did not run.

## House rules

These hold on every page, whatever the references. `inspect.mjs` measures them.

| Rule | Instead |
| --- | --- |
| **Headlines: two lines or fewer, at every width.** Every `h1` to `h6`, and the main line of the first screen whatever its tag. | Cut words. Then widen the measure. Size last. |
| **Statements are paragraphs.** An intro sentence or a quotation set large is a `<p>` or `<blockquote>`, stays at statement size (36px or less on desktop, 24px on a phone) and runs to about 25 words. | Larger than that it is a headline and the two-line rule applies. |
| **No eyebrows.** No small label above a heading, no pill badge above the headline, no "New ·" chip. | Put the information in the heading or the first sentence, or drop it. |
| **No monospace** outside real code blocks. * | The text face. Tabular figures where numbers align. |
| **No index numbering.** No 01 / 02 / 03, no (001), no "Step 2". * | Order shown by position, size, or the words. A real `<ol>` if order matters. |
| **No thin rules.** No hairline dividers, no 1px outlined boxes, no grid lines, crosshairs or crop marks. * | Space. A step in background tone. A change of scale. A filled shape. |
| **No gradients.** Not as backgrounds, not on buttons, not in text. | Flat colour, or a real photograph. A neutral scrim under text on a photo is the one exception. |
| **No shadows on things at rest.** No glows. | A tone step between surfaces. Shadows only on what truly floats. |
| **No assistant palette.** No yellow-cream ground with terracotta or rust; no violet or indigo. | Colours from the subject and your references. |
| **No tiny uppercase letter-spaced labels.** * | Sentence case at a readable size. |
| **No icon-topped feature cards, no rows of identical cards.** | A composed section from your sheet. |
| **No glass.** No backdrop blur panels, no floating pill navigation. | A plain bar: wordmark, a few links, one action. |
| **No emoji, no gradient blobs, no decorative shapes, no fake dashboards of grey bars.** | A real picture, a real interface fragment, or nothing. |
| **No styled accent word** in a headline (italic, serif, coloured, underlined). | One face, one colour. The words carry the emphasis. |
| **Two typefaces at most,** usually one. | Your sheet's type. |

**\* Earned exceptions.** tasteskill bans monospace, index numbers, hairlines and tiny tracked labels
by its author's choice, not by its data: its own study found them *more* common on award-winning
sites, and banned them because generators copy them as costume. This fork keeps the ban as the default
and lets a reference lift it, once, for a reason. A device marked * may appear only when all three hold:

1. a section you opened with `view_section` uses it;
2. its specimen line names it and says what it becomes for this subject;
3. on your page it carries information (ticks that measure something real, a ledger whose columns are
   real data), not decoration.

Then add the rule's id to `allow` in `.taste-skill/direction.json` (`hairline`, `outlined-box`, `mono`,
`numbering`, `micro-label` or `dashed`), for example `{ "source": "regards", "allow": ["hairline"] }`,
and list it in the report.

Two material exceptions follow the same three steps, with their own third condition (§ Material):
`shadow`, for one soft shadow under a physical object the page shows as an object (a sheet, a ticket, a
card in a clip) because it really lifts off the page, never under panels, interface cards or buttons;
and `palette-purple`, when violet or indigo is one of several whole colour fields taken from a reference,
never a violet accent, glow or tint on a neutral page. Gradients, glass, glows, emoji, eyebrows, icon
cards and the cream-and-terracotta palette are never lifted.

Three places keep their own conventions and are left alone by the inspector: real code in
`<pre>`/`<code>`, real tables and form fields, and a real interface fragment whose root carries the
attribute `data-ui` (see `references/imagery.md` §7).

Removing ornament leaves space. Never fill it with another ornament. Fill it with scale, with the full
content, with a picture made for this subject, or with a field of flat colour.

## Material

What separated the pages people wanted to show from the merely correct ones, in runs of this skill
that were then pushed by hand. Check every section against it in step 8.

- **Colour as whole fields.** A palette of three to six saturated colours plus ink, taken from the
  references and the subject. Give sections their own field, with hard steps from dark to light between
  neighbours: ink type on the light fields, white on the dark ones. Several confident fields beat one
  accent on a safe neutral. Pairs that read as generated: navy with yellow, cream or beige with anything,
  a dark page with a single accent colour.
- **Printed things are objects.** A ticket, note, contract page or label is drawn as paper: grain from
  within at the device pixel (a canvas at `devicePixelRatio`; each pixel a small signed offset that
  averages to zero, so the sheet keeps its colour with no grey veil; rarer darker pits; a few faint
  fibres), ink that catches the tooth, a cut edge. Never a tiled noise image or an overlay filter. An
  object may tilt a few degrees, run off the frame, overlap its neighbour and cast one soft shadow.
- **Line work carries data.** Fields of short strokes that lie flat and bend where something happened,
  ticks that measure real values, leaders with small square handles from a note to what it explains,
  brackets on the lines that matter. Draw them in SVG or canvas so they stay crisp at any zoom; every
  line points at something real. This is how a hairline or dashed exception is spent well.
- **One material accent.** Polished metal (chrome with reflected bands, silver with fine grain) on one
  to three small objects: a clip, a button, a rim. Never a whole interface, never metal type.
- **Type with one voice.** A confident grotesk sets the page; a second face, often a serif, is kept for
  one voice only (the product's own words, a printed document).
- **Every section a poster.** One huge thing, small precise secondary type, the full content, nothing
  crowded. If a section would not hold the whole screen on its own, it is not finished.

## Laws of the craft

Short form, from tasteskill's study of 247 gallery sites (`references/research.md`).

**Type**
- Two or three sizes do the visible work: one very large, one small, nothing in between. Median
  headline-to-body ratio on the studied sites is 4.3; largest type: median 8.4vw on the top sites
  against 5.0vw on the weak ones.
- Display type: tracking -0.02 to -0.05em, leading 0.85 to 1.05. Text: 16 to 20px, leading 1.45 to 1.6,
  45 to 75 characters per line.
- Five sizes on a page is the ceiling. One family is normal; two is the limit.
- Left-aligned by default. Centre at most one moment.

**Space**
- One grid, one pair of tight margins (16 to 32px), used everywhere; large things run to the edges.
- The gap between sections is clearly larger than any gap inside one: 120 to 220px on desktop.
- Each section has a different composition from its neighbours; none is a card grid.

**Colour**
- One ink, one accent, one ground per section (a section may take its own field: § Material). The accent
  appears on the action and perhaps one other thing.
- Running text in the full ink. Surfaces are separated by a small step in tone.
- A section may change the whole field colour. Nothing fades into anything.

**Imagery**
- One dominant image beats six small ones. Same crop ratios, same treatment, square corners unless
  the direction says otherwise.
- Every found picture is downloaded into the project, credited on the page and listed in the report.
- Nothing ever lies on top of a headline or a statement (the inspector fails it).

**Components**
- Buttons: flat, one fill colour, square-cornered or fully round, decided once. Most strong heroes
  have no button or one.
- Navigation: wordmark, three to five plain links, one action.
- The footer is a designed close, not a sitemap.

## Special cases

**An existing brand or design system.** Keep its colours and faces, search regards for composition
and components only, and map the brand onto the roles. If the brand itself requires a banned device,
keep it, say so, and pass `--allow <rule>` to the inspector for that rule only.

**Redesign or review of an existing page.** Run `lint.mjs` and `inspect.mjs` on it first and report what
they find, then critique the screenshots. For a redesign, research from step 3 with the page's real
content as the inventory.

**A component or a single section, not a page.** Search regards for that kind of section, keep two or
three specimens, match the surrounding design, apply the house rules, and still inspect the result.

**No checkout, no form backend.** The primary button goes to the real destination when the brief names
one; otherwise a `mailto:` with a written subject and body, or `#checkout` with a note in the report.
Never fake a payment form.

**No Chrome or Node 22.** Run `lint.mjs` (Node 18+), take screenshots with whatever browser tool you
have, and critique those. Say in the report that the inspector could not run.

## Files

| File | Read it when |
| --- | --- |
| `references/regards.md` | Step 3: search recipes, specimen notes, mutation moves, the never-copy test. |
| `references/copy.md` | Writing the argument and the copy deck (steps 2 and 5). The two-line arithmetic. |
| `references/type.md` | Setting type: scales, tracking, measure, loading fonts, pairing. |
| `references/colour.md` | Applying the palette: roles, proportions, tone steps, dark pages, contrast. |
| `references/layout.md` | Grid, margins, rhythm, section variety, navigation, footer, the phone composition. |
| `references/imagery.md` | Choosing, finding, crediting, cropping and treating pictures; what to do with none. |
| `references/motion.md` | Step 9. Budget, tokens, recipes, reduced motion. |
| `references/critique.md` | Step 8. How to look, how to score, what to fix first. |
| `references/tells.md` | The dated registry of generated-page tells and what each is replaced by. |
| `references/research.md` | tasteskill's study: method, numbers, what the best and worst sites do. Cite it, do not guess. |
| `references/draw.md` | The fallback: dealing a direction from the bundled library when regards is not connected. |
| `scripts/assets.mjs` | Step 6: real pictures of the subject's world from open collections, with credits. |
| `scripts/lint.mjs` · `scripts/inspect.mjs` | The gate. |
| `scripts/draw.mjs` · `library/` | The fallback deal only. Do not read the library whole. |
| `assets/base.css` · `assets/base.js` | An optional neutral foundation. |

## Credit

Forked from [tasteskill v2](https://github.com/Leonxlnx/taste-skill) by Leonxlnx, MIT licence. The
study, the inventory, the idea and competitor tests, the open-collection pictures, the inspector, the
critique rubric and the look loop are tasteskill's. The research step, the specimen sheet and the
earned exceptions are this fork's.
