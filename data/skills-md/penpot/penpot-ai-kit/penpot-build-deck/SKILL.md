---
name: penpot-build-deck
description: "Design a presentation / slide deck in Penpot from a brief, as a senior presentation designer: 1920x1080 slide boards built one slide per call from an approved outline, a committed deck style, varied slide archetypes (cover, agenda, section, content, big-number, comparison, grid, bento, quote, timeline, image-bleed, closing), tokenized, wired into a playable View-mode flow and exportable to PDF. NOT for app screens (use penpot-build-screen). Triggers: 'create a presentation', 'build a slide deck', 'design slides in Penpot', 'pitch deck', 'keynote', 'make slides for this talk', 'turn this outline into slides'."
disable-model-invocation: false
version: 0.2.0
audiences: [product-designer, design-system]
mode-default: review
requires:
  - shared/penpot-mcp-tool-reference.md
  - shared/plugin-api-gotchas.md
  - shared/tokens-schema.json
  - shared/naming-conventions.md
  - shared/state-management.md
  - shared/modes-and-policies.md
  - shared/visual-self-review.md
  - shared/design-quality.md
  - shared/visual-effects.md
  - shared/anti-slop.md
  - shared/report-schemas/deck-quality-report.schema.json
---

# penpot-build-deck — brief to a playable slide deck

## 1. Title + How it works
`penpot-build-deck` turns a brief into a presentation that lives in Penpot as real, editable design:
one **1920×1080 Board per slide** on a dedicated page, tokenized through a `deck.*` token set, wired
into a **flow** so the deck plays in Penpot's View mode (←/→, Shift+F fullscreen), and exportable to
PDF. Every mutation goes through `execute_code`; validate visually with `export_shape` (per slide,
never the whole page); read structure with `penpotUtils.shapeStructure` (full tool surface:
`shared/penpot-mcp-tool-reference.md`). Penpot has no "slides mode" — this skill *is* the deck
tooling: outline → deck system → style freeze → slides in batches → flow + quality gate.

## 2. The One Rule That Matters Most
**Plan the whole outline, then build one slide per call.** Never generate a deck in one
`execute_code`. Slides 1–3 are the **style freeze**: everything after them inherits their decisions.
Build the rest in batches of 3–5, export and *look at* every slide before its checkpoint, and refuse
the AI-slide tells (accent lines under titles, decorative bars, centered body text, text-only slides,
the same layout twice in a row).

## 3. Penpot MCP Tool Reference
Full surface: `shared/penpot-mcp-tool-reference.md`. Domain calls: `penpot.createPage()` /
`openPage()` (two-call page protocol); `createBoard()` + `resize(1920, 1080)`; `addFlexLayout()` /
`addGridLayout()`; `createText()` + `penpot.fonts.all` (exact name) + `font.applyToText()`;
`applyToken`; `penpot.uploadMediaUrl(name, url)`; `page.createFlow(name, board)`;
`shape.addInteraction("click", { type: "navigate-to", destination, animation })`;
`board.waitForLayoutUpdate()`; `export_shape(slideId)`.

## 4. Plugin API Essentials
Gotcha numbers refer to `shared/plugin-api-gotchas.md`.
- **#15 page targeting — this skill's critical failure mode.** Decks live on their own page, and a
  board born on the wrong page **cannot be moved** (cross-page `appendChild` is a silent no-op).
  `scripts/createDeckPage.js` runs the two-call protocol: call A creates + opens the page, call B
  asserts `penpot.currentPage.id` matches before any `createBoard()`. If B fails, stop and ask the
  user to open the page in the UI — never build on the wrong page.
- **#11 fill policy.** The slide board is *the* surface: `fills = []`, then bind `deck.bg.<tone>`.
  Every inner container (`safe-area`, columns, rows, cards that are pure grouping) stays `fills = []`;
  only real cards/panels bind `deck.surface.*`.
- **#13b exact fonts.** `penpot.fonts.all.find(f => f.name === "Inter")` — `findByName` matches
  substrings and will hand you "Inter Tight" or "Roboto Mono". Re-assert `fontSize`/`lineHeight`
  after `applyToText`.
- **#14 edge decorations** are absolute children positioned in **page coordinates**; boards clip at
  their edges — that clipping is the bleed.
- **#16 `clearFlip`** after every slide (`shared/visual-effects.md` §7); the mirror is invisible to
  `shapeStructure` and unmissable in the export.
- **#17 `await board.waitForLayoutUpdate()`** before reading geometry in the same call.
- **#18 image fills** are async and fallible — placeholder by default, uploads only for user URLs,
  verified in the next call.
- **#2 tokens** apply asynchronously — bind in the build call, verify `shape.tokens` in the audit.
- Verify unfamiliar signatures with `penpot_api_info` first (`Page.createFlow`, `Shape.addInteraction`,
  `Board.backgroundBlur`, `GridLayout`).

## 5. Token-Aware Brief Contract
- **Context** — audience, occasion, duration, venue/screen, language.
- **Objective** — the *one* message the audience must leave with, and the ask / CTA.
- **Inputs** — outline (one line per slide), facts and figures **with sources**, quotes with
  attribution, image URLs (or "placeholders"), existing tokens/components/fonts to reuse.
- **Constraints** — no fabricated numbers; fonts must exist in `penpot.fonts.all`; every slide gets a
  visual; forbidden: accent lines under titles, decorative bars/stripes, centered body text, default
  blue, cream backgrounds, text-only slides; `deck.*` tokens only (gradients/shadows/glass are
  ledgered literals); **with strict anti-slop on**, the keys the direction step refused
  (`shared/anti-slop.md` §1, deck readings in `penpot-anti-slop` `references/04-deck-tells.md`).
- **Acceptance Criteria** — every slide a 1920×1080 board named `NN-archetype-slug`; ≥ 1 visual per
  slide; no two consecutive identical archetypes and no archetype > 40 % of the deck; type floor
  20 px, body ≥ 28 px; contrast ≥ 3:1 (text ≥ 24 px or ≥ 18.67 px bold) / 4.5:1 below; flow `Deck`
  wired click → next; deck-quality score ≥ 3 on all seven axes or the weak axes named; with strict
  anti-slop on, slop score ≤ 35 over the deck page.

Act as a **senior presentation designer** who makes a real scale difference, uses the full canvas,
varies the anchor slide to slide, and never ships a text-only slide.

## 6. Mandatory Workflow

> **Visual self-review (mandatory):** before every ✋ checkpoint, run the export → look → fix loop of
> `shared/visual-self-review.md` on each slide built since the last checkpoint (max 2 self-fix
> iterations per checkpoint), and present those same exports with any remaining defects named.

**Phase 0 — Discovery + outline (read-only).** `high_level_overview`; `penpotUtils.tokenOverview()`;
`penpot.fonts.all.map(f => f.name)`; `penpotUtils.getPages()`. Analyse the brief
(`references/01-deck-brief-analysis.md`): slide budget, the one message, outline table
`n | archetype | title | key content | visual | tone`, tonal arc, motif. Pick a deck style
(`references/02-deck-styles.md`) and run the variety pre-check (`references/03-slide-archetypes.md`).
**Anti-slop opt-in:** read the stored preference (`penpot-anti-slop` → `scripts/antiSlopPrefs.js`); if
unset and the brief doesn't answer it, ask the `shared/anti-slop.md` §0 question once (user's
language) and store it. When `on`, run the **direction** step (`penpot-anti-slop`
`references/02-direction-playbook.md` + `04-deck-tells.md`) before picking the deck style, and add
its refused keys to the Constraints.
✋ Checkpoint: approve outline + style + tonal arc + slide count (+ direction block if strict).

**Phase 1 — Deck system.** `scripts/createDeckPage.js` (PHASE=create, then PHASE=verify in the next
call). `scripts/setupDeckSystem.js`: token set `deck` (aliasing existing brand tokens where they
exist), font resolution, optional master components. New tokens are proposed here, never invented
silently. ✋ Checkpoint: approve tokens + fonts.

**Phase 2 — Style freeze.** Build `01-cover-…`, `02-agenda-…` and the first content slide with
`scripts/buildSlide.js` (+ `scripts/applyDeckEffects.js` for the background device), **one slide per
call**; export each; self-review. ✋ **Style-freeze checkpoint** — any later style change reopens it.

**Phase 3..N — Batches.** 3–5 slides per batch, one slide per call, `clearFlip` in every call; after
the batch, export each slide and check the variety rule against the previous slide. Image URLs are
uploaded in `applyDeckEffects.js` and verified in the following call. ✋ Checkpoint per batch.

**Phase N+1 — Wire, gate, critique.** `scripts/wireDeckFlow.js` (order, flow `Deck`, click → next,
optional auto-advance, section flows). `scripts/auditDeckQuality.js` — a non-`pass` gate blocks
"done". Then the scored critique (`references/07-critique-framework.md`): seven axes + the monotony
check, any axis < 3 → targeted revision (max 2 passes) → Markdown + JSON per
`shared/report-schemas/deck-quality-report.schema.json`, mirrored to the ledger. Strict mode on: run
`penpot-anti-slop` diagnose (`MODE = "deck"`) on the deck page and include the slop score. Give the PDF-export
and share-link steps (`references/06-flow-and-playback.md`). ✋ Final checkpoint.

## 7. Critical Rules
1. **One slide per `execute_code` call.** The outline is planned whole; the canvas is built one slide at a time.
2. Every slide is a **1920×1080 Board** named `NN-archetype-slug`, `showInViewMode = true`, `clipContent = true`, placed on the deck page's contact grid.
3. **Fill policy** (#11): the slide board binds `deck.bg.<tone>`; grouping containers are transparent.
4. **Tokens first**: `deck.*` for colour, type sizes/families, spacing, radius. Gradients, glass fills and shadows cannot bind — every one is a ledger `exceptions` entry with the tokens it derives from.
5. **≥ 1 visual element per slide** (shape, image/placeholder, stat numeral ≥ 140 px, chart placeholder, component instance). Text-only slides fail the gate.
6. **Variety rule**: consecutive slides differ on ≥ 1 of archetype / anchor / tone; never the same archetype twice in a row; no archetype > 40 % of the deck.
7. **Type floor 20 px; body ≥ 28 px; titles 72–96 px** (`references/04-typography-and-grid.md`); ≤ 2 families, ≤ 3 weights; sentence case; body left-aligned.
8. **Honest content**: numbers only from the brief, each with a source line; quotes attributed; no lorem, no "Item 1".
9. **Images**: labeled placeholders unless the user supplied URLs; uploads verified next call; failures reported, never swapped silently.
10. **Refuse the tells**: accent lines under titles, decorative bars/stripes, centered body text, default blue, cream backgrounds, purple-gradient-on-white, identical layouts back to back.
11. `clearFlip(slide)` after every slide; `await waitForLayoutUpdate()` before geometry reads.
12. The **flow is part of "done"**: no final checkpoint without `wireDeckFlow.js` having run.
13. Checkpoints per §11 — "looks good" approves only the batch just shown.

## 8. Domain Architecture
Page `Deck — <title>` → slide boards on a 4-column contact grid (x = (i % 4)·2080, y = ⌊i/4⌋·1240)
→ each slide: root flex **column** with padding bound to `deck.space.margin` (96) → `safe-area`
containers (row / column / `addGridLayout` per archetype, spans on a 12-column grid: 4 = 544,
6 = 840, 8 = 1136) → texts (`h1`, `eyebrow`, `p`, `stat`, `caption`), shapes, `img-placeholder`
rects, component instances → a hidden `notes` text layer per slide (speaker notes convention) →
flow `Deck` from slide 01 + optional `Section: <name>` flows. Archetype catalogue and per-archetype
recipes: `references/03-slide-archetypes.md`.

## 9. Modes & Policies
Default **review**. Safe set here: renaming a slide board to the `NN-archetype-slug` convention.
Everything else (geometry, tokens, effects, flow wiring, uploads) is apply-with-review
(`shared/modes-and-policies.md`).

## 10. State Management
Ledger under `RUN_ID` (`deck-<date>-<slug>`): `phase`, `deckPageId`, `deckStyle`, `tonalArc`, `motif`,
`outline[]`, `slides:[{ n, id, name, archetype, done }]`, `styleFrozen`, `flowName`, `exceptions[]`,
`capabilities` (verdicts for `waitForLayoutUpdate`, `uploadMediaUrl`, `addGridLayout`, `backgroundBlur`,
play-order direction), `deckQuality`, `antiSlop` (`pref`, `direction`, `reports[]` when strict mode is
on; the opt-in itself is file-wide plugin data `penpot-ai` → `prefs.antiSlop`). `storage.deck` mirrors the ids for the session. Resume: re-read
the ledger, re-run `createDeckPage.js` PHASE=verify, re-derive the slide list by name
(`^\d{2}-`), continue from the first `done: false` slide (`shared/state-management.md`).

## 11. User Checkpoints
| After phase | Artifacts | Ask |
|-------------|-----------|-----|
| 0 (pref unset) | the anti-slop opt-in question (`shared/anti-slop.md` §0) | Avoid the generic-AI look? |
| 0 | outline table + style + tonal arc + motif + slide count (+ direction block if strict) | Approve direction? |
| 1 | token list (aliased / new / literal) + fonts found | Approve deck system? |
| 2 (style freeze) | exports of slides 01–03 | Freeze this style? |
| each batch | exports of the batch's slides + variety check | Approve batch? |
| N+1 | flow summary + gate result + scored critique (7 axes + monotony) | Approve / iterate? PDF/share steps given. |

## 12. Naming Conventions
`shared/naming-conventions.md` plus: boards `NN-archetype-slug` (`01-cover-launch`,
`07-big-number-retention`); layers semantic (`h1`, `h2`, `eyebrow`, `p`, `stat`, `caption`,
`img-placeholder`, `card`, `safe-area`, `notes`); tokens `deck.*` (`deck.bg.dark`, `deck.text.on-dark`,
`deck.accent`, `deck.font.size.title`, `deck.space.margin`); flows `Deck`, `Section: <name>`;
`RUN_ID` `deck-2026-09-10-a`.

## 13. Anti-Rationalization Table
| Excuse | Why it's wrong | Countermeasure (halt) |
|--------|----------------|------------------------|
| "I'll build all twelve slides in one call — it's the same code." | One-shot decks are unauditable and every slide comes out the same. | One slide per call; batches of 3–5; export + look before each checkpoint. |
| "An accent line under the title looks polished." | It is *the* hallmark of AI-generated slides. | No lines/bars under titles — hierarchy through scale and weight. |
| "Same layout on every content slide is consistency." | Consistency is the style; monotony is the layout. | Variety rule: change archetype, anchor or tone; the gate counts consecutive repeats. |
| "A plausible stat makes the point stronger." | Fabricated evidence (`shared/design-quality.md` §6). | Numbers only from the brief, with a source line; otherwise a labeled placeholder. |
| "This slide is fine as text only." | Text-only slides are the reading-not-presenting tell. | Add the archetype's mandatory visual or change archetype. |
| "I'll skip the flow; the user can click through boards." | Without a flow there is no deck, only boards. | `wireDeckFlow.js` runs before "done". |
| "I'll grab a stock image URL that surely exists." | Guessed URLs are fabricated content and fail upload silently. | Placeholder unless the user supplied the URL. |
| "24 px body reads fine on my monitor." | It is illegible from the back of a room at 1920×1080. | Body ≥ 28 px, floor 20 px; the gate enforces it. |
| "The default white board is fine for a light slide." | Unbound literal — never flips, off-system. | `fills = []` then bind `deck.bg.light`. |
| "Centered everything is the safe choice." | Center is the no-decision alignment; content huddles. | Full canvas, 70/30 asymmetry, anchor varies per slide; center only cover/quote/closing. |
| "The page switch worked, I'll start creating boards." | `openPage` is async; boards land on the old page and cannot be moved. | `createDeckPage.js` PHASE=verify must return `ok: true` first. |

## 14. Helper Code Snippets
```js
// Slide frame — the surface + bound margin (one slide per call; see scripts/buildSlide.js)
const slide = penpot.createBoard();
slide.name = "05-big-number-retention";
slide.resize(1920, 1080);
slide.clipContent = true; slide.showInViewMode = true;
const flex = slide.addFlexLayout();
flex.dir = "column"; flex.horizontalSizing = "fix"; flex.verticalSizing = "fix";
slide.fills = [];                                                // drop Penpot's default opaque white
const bg = penpotUtils.findTokenByName("deck.bg.dark");
if (bg) slide.applyToken(bg, ["fill"]);
const margin = penpotUtils.findTokenByName("deck.space.margin");
for (const side of ["paddingTop", "paddingBottom", "paddingLeft", "paddingRight"]) {
  try { slide.applyToken(margin, [side]); } catch { flex[side.replace("padding", "").toLowerCase() + "Padding"] = 96; }
}
penpot.currentPage.root.appendChild(slide);
```
```js
// Exact font + size re-assert (gotcha #13b / #13)
const font = penpot.fonts.all.find(f => f.name === "Inter");
const variant = font && font.variants.find(v => v.fontWeight === "700");
const h1 = penpot.createText("Retention doubled in Q3");
h1.name = "h1";
if (font) font.applyToText(h1, variant);
h1.fontSize = "88"; h1.lineHeight = "1.1"; h1.letterSpacing = "-1.5"; h1.growType = "auto-height";
```
```js
// Click → next slide with a slide-in animation (scripts/wireDeckFlow.js does this for every pair)
current.addInteraction("click", {
  type: "navigate-to", destination: next,
  animation: { type: "slide", way: "in", direction: "left", duration: 300, easing: "ease-out" }
});
```
```js
// clearFlip — run before returning from every slide build (gotcha #16)
const clearFlip = (sh) => { let n = 0; const walk = (s) => { if (s.flipX) { s.flipX = false; n++; } (s.children || []).forEach(walk); }; walk(sh); return n; };
```

## 15. Reference Resources
- `penpot_api_info("Page", "createFlow")`, `penpot_api_info("Shape", "addInteraction")`,
  `penpot_api_info("Board", "waitForLayoutUpdate")`, `penpot_api_info("Board", "backgroundBlur")`,
  `penpot_api_info("Penpot", "uploadMediaUrl")`, `penpot_api_info("GridLayout")`, `penpot_api_info("Gradient")`.
- Penpot View mode (`G V`, ←/→, Shift+F, flows dropdown, share link) and "Export selected boards as
  PDF" (Penpot ≥ 2.12) — `references/06-flow-and-playback.md`.
- Inspiration only (not a dependency): the official "Penpot slides template" on Penpot Hub (CC-BY-4.0).

## 16. Supporting Files
**references/**: `01-deck-brief-analysis.md` (Phase 0), `02-deck-styles.md` (Phase 0), `03-slide-archetypes.md` (Phases 0, 2..N), `04-typography-and-grid.md` (Phases 1..N), `05-visuals-and-effects.md` (Phases 2..N), `06-flow-and-playback.md` (Phase N+1), `07-critique-framework.md` (Phase N+1), `08-anti-rationalization.md`, `09-error-recovery.md`.
**scripts/**: `createDeckPage.js` (Phase 1, two calls), `setupDeckSystem.js` (Phase 1), `buildSlide.js` (Phases 2..N), `applyDeckEffects.js` (Phases 2..N), `wireDeckFlow.js` (Phase N+1), `auditDeckQuality.js` (Phase N+1).
**shared/**: `visual-effects.md` (gradients, glass, shadows, images, `clearFlip`), `design-quality.md` (§2 type craft, §3 colour, §6 content honesty, §7 tells, §8 scoring procedure).

**Doctrine paths.** `shared/…` and `policies/…` resolve inside this bundle in native installs (vendored by the installer); in a Claude Code plugin install they live at the plugin root — `${CLAUDE_PLUGIN_ROOT}/shared/…`, two directories up from this file.
