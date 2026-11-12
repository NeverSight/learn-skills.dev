---
name: visant-design
description: 'End-to-end UI/UX: removes AI slop, redesigns screens around what they must achieve, and verifies on the real screen. Use on "clean the AI slop", "improve the UI", "improve the UX", "redesign this screen", "limpa o slop", "melhora o design", "melhora a ui", "ui ux end-to-end", "tá com cara de IA", any UI or UX polish, /visant-design.'
metadata:
  family: design
  routes: visant-killer visant-frontend visant-motion visant-refine
---

# Visant Design

Takes "clean the slop" or "improve the UX" to a finished screen you have looked at. Rulebooks can't see your product or your result; this process makes you see both.

`<skill-dir>` is the folder holding this file. Other playbooks are next to it: read `../<name>/SKILL.md`. If one is missing: `npx skills add pedrojaques99/visant-skills-public --skill <name>`.

**Branding is core. Decide it with the owner once, then work to the end.** Before cutting or building, extract the product's [brand idiom](references/brand-idiom.md) and mark where to spend craft. Then hold one checkpoint: 2 or 3 directions with the cheapest preview that decides, your recommendation first. Outside that checkpoint, ask only what the code cannot answer and would change what gets built. Follow the product's own design system and components; only create a new one if nothing exists.

Pick one track:

| The ask | Track |
|---|---|
| "Clean the slop", "looks AI-made", remove the tells | [Clean](#clean) |
| "Improve", "redesign", "UI/UX end-to-end", "this looks bad" | [End to end](#end-to-end) |
| Several screens with no pattern between them | [Many screens](#many-screens) |
| "Audit", "review", "is this good" | [visant-killer](../visant-killer/SKILL.md): change nothing until the user answers its closing question |
| One detail: motion, chart, panel, component demo | [Single topic](#single-topic) |

## Clean

Keep the design. Remove the tells.

1. `node <skill-dir>/scripts/check.mjs <ui paths> --url <running app>`
2. Fix every finding at its cause. Hiding what a finding points at does not count.
3. **Mark where to spend before you cut.** Fill the craft column (shine / alive / sober) and, for each shine region, write its brand moment in one line: [brand-idiom.md](references/brand-idiom.md). Whatever leaves a shine region is replaced in the same change, never with nothing. A work screen keeps a live signal.
4. Read the images. Fix the tells no detector sees: decorative gradients, purple as "AI", glow, emoji as icons, a card nested in a card (the nesting is the tell; a card alone is not), eyebrow labels over every heading, hype words, invented numbers.
5. Run it again until it is clean, plus `node ../visant-killer/scripts/stroke-scan.mjs <ui paths>`: no stroke over 1px without a written reason, and selection said by color. Report what you removed and what replaced it.
6. Compare before and after side by side and show the owner **before** install, push or "done". The score is not the verdict: it improves with every box you delete, and a screen stripped of its cards scored zero while its owner called it "too clean". `node ../visant-killer/scripts/regressao.mjs git HEAD <ui paths>` flags lost boxes, controls, chips and width.

## End to end

1. **See it first.** Start the app and run `check.mjs` as above. Read the screenshots before reading the code. If the app cannot start, say so and fix that first.
2. **Name the job and the craft.** Write one line per screen: who arrives, what they came to do, which number moves, and its craft (shine / alive / sober) in the [surface table](../visant-frontend/SKILL.md#step-0-classify-the-surface-a-written-table-before-any-fix). Read the file for that surface:
   - Landing, pricing, signup, onboarding: [acquisition](../visant-frontend/references/acquisition-surface.md)
   - Queue, table, editor, admin: [work](../visant-frontend/references/work-surface.md)
   - Canvas, map, free-form/spatial editor: [spatial](../visant-frontend/references/spatial-surface.md)
   - Payment, permission, deletion, money: [trust](../visant-frontend/references/trust-surface.md)
3. **Brand idiom and screen architecture.** List 3 to 5 assets only this brand has ([brand-idiom.md](references/brand-idiom.md) §1). For each shine region, name three things: the object, which takes the largest surface (canvas + deck); the brand moment; and the illustration that explains the feature, not just the brand. List the core components: on many screens, or the object the product is about.
4. **Diagnose from the image.** Run [foundations.md](references/foundations.md) on the screenshot, in order. List what is wrong, biggest first.
5. **Checkpoint with the owner.** Show 2 to 3 directions for the shine regions and core components, your recommendation first. Use ASCII or a wireframe for structure, and a real frame only when the call is visual. One round, then build.
6. **Cut, then put the life back.** For each element ask which decision it helps. No answer, it goes, except in a shine region, where what goes is replaced in the same change. A main number keeps its emphasis (box, scale, rule: whatever the brand's system uses), a state keeps a visible signal, an action keeps its target. Too much text becomes drawn facts (count, ring, logo, a three-way switch), not fewer cards and never a pile of badges. Hide in sequence: one choice per step, an option's panel only once it is chosen, a batch bar only with a selection, Save only on the row that changed, capability hidden in settings brought to the entry ([work](../visant-frontend/references/work-surface.md#hiding)).
7. **Build: core components first.** They get every state, hover that previews the outcome, hairline strokes and one shared module ([brand-idiom.md](references/brand-idiom.md) §4). Then the screen, with the product's tokens. A list of things the product does gets a thumb per item, drawn in the idiom. Motion and data get their playbook only if this screen needs them. Write copy from what the product really does; a number you don't have stays a visible placeholder.
8. **Look at the result.** Run `check.mjs` again and read the new screenshots at every width, next to the old ones. Then the swap test: with a competitor's logo, could this still be theirs? Show the owner the pair: the score is not the verdict. Fix the biggest thing and repeat, up to three rounds. While iterating, run only the affected tests and the screen that changed; the full suite and every screen run once, before the commit.
9. **Report.** What changed and which number each change is meant to move; what you cut, why, and what replaced it; the brand moment of each shine region; the widths you looked at; what you did not check. A redesign is a hypothesis: say how to measure it.

If `check.mjs` says NOT VERIFIED, the first line of your answer says so. The work is not done. Stop any server you started. `check.mjs` runs in Chromium: a custom touch gesture that never ran on a real iPhone goes under what you did not check.

## Many screens

Each screen looks right alone, so fixing them one at a time hardens the disagreement. Write the pattern first.

1. **See them together.** Run `check.mjs` and put the sister screens' screenshots side by side. List what each one does differently: the same control in another place, another name, another empty state.
2. **Write the pattern.** A short list in the repo: which control does each job, where it lives, what it is called. If a choice is really the owner's, ask once.
3. **Change the shared piece, not each screen.** Fix or extract the one component and have the screens import it. Core components go first and get the polish budget ([brand-idiom.md](references/brand-idiom.md) §4). A shared piece reaches every screen using it, so list them first and look at all of them after.
4. **Then each screen,** from step 4 of [End to end](#end-to-end). Report the pattern with the work.

## Single topic

| The ask | Read |
|---|---|
| Animation, transition, loading, skeleton | [visant-motion](../visant-motion/SKILL.md) |
| Chart, gauge, slider, metric tile, control panel | [visant-refine](../visant-refine/SKILL.md) |
| Hierarchy or what to remove on one screen | [visant-frontend](../visant-frontend/SKILL.md) |
| Too cluttered, too many labels | [declutter](../visant-killer/references/declutter.md) |
| Component demo, library page, mock product | [component-showcase](../visant-frontend/references/component-showcase.md) |
| Fake product UI for a hero, cursor demo | `stageshow`, third party: `npx skills add benjitaylor/skills --skill stageshow` |

Before writing a component, check the repo's primitives, then [@visant/ui](https://ui.visantlabs.com/llms.txt).

## Neighbors

- **Feedback**: when the work is delivered, ask once per session, in one line, what helped and what was missing; it goes to https://ui.visantlabs.com/skills#feedback
- **[[visant-killer]]**: audit what exists
- **[[visant-frontend]]**: decide what should exist
- **[[visant-motion]]**: how it moves
- **[[visant-refine]]**: data and controls
- **[[stageshow]]**: a fake product UI for a hero or feature card
- **[[visant-copy]]**: the words on the screen
- **[[visant-preflight]]**: a large client project, before any screen
