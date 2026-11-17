---
name: ui-demo
description: Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial video of a web application. Produces WebM videos with visible cursor, natural pacing, and professional feel.
origin: ECC
---

# UI Demo Video Recorder

Record polished demo videos of web applications using Playwright's video recording with an injected cursor overlay, natural pacing, and storytelling flow.

## When to Use

- User asks for a "demo video", "screen recording", "walkthrough", or "tutorial"
- User wants to showcase a feature or workflow visually
- User needs a video for documentation, onboarding, or stakeholder presentation

## Three-Phase Process

Every demo goes through three phases: **Discover -> Rehearse -> Record**. Never skip straight to recording.

---

## Phase 1: Discover

Before writing any script, explore the target pages to understand what is actually there.

### Why

You cannot script what you have not seen. Fields may be `<input>` not `<textarea>`, dropdowns may be custom components not `<select>`, and comment boxes may support `@mentions` or `#tags`. Assumptions break recordings silently.

### How

Navigate to each page in the flow and dump its interactive elements. Use the `page.evaluate` field-dump snippet in **reference/field-discovery.md** (Phase 1).

### What to look for

- **Form fields**: Are they `<select>`, `<input>`, custom dropdowns, or comboboxes?
- **Select options**: Dump option values AND text. Placeholders often have `value="0"` or `value=""` which looks non-empty. Use `Array.from(el.options).map(o => ({ value: o.value, text: o.text }))`. Skip options where text includes "Select" or value is `"0"`.
- **Rich text**: Does the comment box support `@mentions`, `#tags`, markdown, or emoji? Check placeholder text.
- **Required fields**: Which fields block form submission? Check `required`, `*` in labels, and try submitting empty to see validation errors.
- **Dynamic content**: Do fields appear after other fields are filled?
- **Button labels**: Exact text such as `"Submit"`, `"Submit Request"`, or `"Send"`.
- **Table column headers**: For table-driven modals, map each `input[type="number"]` to its column header instead of assuming all numeric inputs mean the same thing.

### Output

A field map for each page, used to write correct selectors in the script. See the example field map in **reference/field-discovery.md**.

---

## Phase 2: Rehearse

Run through all steps without recording. Verify every selector resolves.

### Why

Silent selector failures are the main reason demo recordings break. Rehearsal catches them before you waste a recording.

### How

Use `ensureVisible`, a wrapper that logs and fails loudly, plus a rehearsal step loop — both in **reference/field-discovery.md** (Phase 2). It dumps all visible elements when a selector misses.

### When rehearsal fails

1. Read the visible-element dump.
2. Find the correct selector.
3. Update the script.
4. Re-run rehearsal.
5. Only proceed when every selector passes.

---

## Phase 3: Record

Only after discovery and rehearsal pass should you create the recording.

### Recording Principles

#### 1. Storytelling Flow

Plan the video as a story. Follow user-specified order, or use this default:

- **Entry**: Login or navigate to the starting point
- **Context**: Pan the surroundings so viewers orient themselves
- **Action**: Perform the main workflow steps
- **Variation**: Show a secondary feature such as settings, theme, or localization
- **Result**: Show the outcome, confirmation, or new state

#### 2. Pacing

- After login: `4s`
- After navigation: `3s`
- After clicking a button: `2s`
- Between major steps: `1.5-2s`
- After the final action: `3s`
- Typing delay: `25-40ms` per character

#### 3-8. Helper Functions

The interaction helpers live in **reference/cursor-overlay.md**. Inject the overlays after every navigation (they are destroyed on navigate):

- **`injectCursor`** (§3) — SVG arrow cursor that follows the mouse.
- **`moveAndClick`** (§4) — moves the cursor to the target before clicking; never teleports. Always pass a descriptive `label`.
- **`typeSlowly`** (§5) — visible per-character typing instead of instant fill.
- **Smooth scrolling** (§6) — `window.scrollTo({ behavior: 'smooth' })` instead of jumps.
- **`panElements`** (§7) — sweep the cursor across key dashboard elements.
- **`injectSubtitleBar` / `showSubtitle`** (§8) — bottom subtitle bar; use `Step N - Action` format, keep under 60 chars, clear during long pauses.

## Script Template

The full Playwright recording script skeleton (rehearse + record modes, video save) and run commands are in **reference/recording.md**. Paste the helpers from `cursor-overlay.md` and `field-discovery.md` into the marked section.

## Checklist Before Recording

- [ ] Discovery phase completed
- [ ] Rehearsal passes with all selectors OK
- [ ] Headless mode enabled
- [ ] Resolution set to `1280x720`
- [ ] Cursor and subtitle overlays re-injected after every navigation
- [ ] `showSubtitle(page, 'Step N - ...')` used at major transitions
- [ ] `moveAndClick` used for all clicks with descriptive labels
- [ ] `typeSlowly` used for visible input
- [ ] No silent catches; helpers log warnings
- [ ] Smooth scrolling used for content reveal
- [ ] Key pauses are visible to a human viewer
- [ ] Flow matches the requested story order
- [ ] Script reflects the actual UI discovered in phase 1

## Common Pitfalls

1. Cursor disappears after navigation - re-inject it.
2. Video is too fast - add pauses.
3. Cursor is a dot instead of an arrow - use the SVG overlay.
4. Cursor teleports - move before clicking.
5. Select dropdowns look wrong - show the move, then pick the option.
6. Modals feel abrupt - add a read pause before confirming.
7. Video file path is random - copy it to a stable output name.
8. Selector failures are swallowed - never use silent catch blocks.
9. Field types were assumed - discover them first.
10. Features were assumed - inspect the actual UI before scripting.
11. Placeholder select values look real - watch for `"0"` and `"Select..."`.
12. Popups create separate videos - capture popup pages explicitly and merge later if needed.

---

## Reference Files

- **reference/field-discovery.md** — read in Phase 1/2: the field-dump `page.evaluate` snippet, example field map, the `ensureVisible` helper, and the rehearsal step loop.
- **reference/cursor-overlay.md** — read in Phase 3: `injectCursor`, `moveAndClick`, `typeSlowly`, smooth scroll, `panElements`, `injectSubtitleBar`/`showSubtitle`.
- **reference/recording.md** — read when assembling the recording: full script template (rehearse + record modes, video save) and run commands.
