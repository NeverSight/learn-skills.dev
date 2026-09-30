---
name: design-director
description: Direct brand and visual-design work from brief through production handoff. Use for logo exploration or refinement, layout, typography, color systems, critique, brand identity, brief simplification, or final SVG and PNG asset packages.
---

# Design director

At the start, announce what you run. Say "I'm using design-director to ..." and fill in the mode or how you routed the request.

Read the brief, the repo files, the source artwork, and the conversation before you ask anything. Pull out decisions already made. Ask only for missing facts that would change the result. Use a structured question tool when one is available. Otherwise ask one short plain-text question.

Keep design direction inside this skill. Reach for another build tool only when the user asked for an artifact that needs it and the tool exists. A finished production package needs no Figma handoff.

## Phase 0: Preserve the approved baseline

Before normal mode detection, check whether the thread already holds a selected direction, version, or asset set.

- Set `IS_CONTINUATION = true` for an existing baseline. State the approved baseline, the locked decisions, and the requested change in one line.
- Treat the follow-up as a delta. Preserve everything outside the named change.
- Route a color-only change to `color` and a mark or letterform change to `logo`. Route lockup order, export, packaging, or cleanup to `finalize` only when the active baseline is an approved logo or identity asset.
- Keep other continuations in the active mode unless the user explicitly invokes another mode.
- A request to return to an earlier version makes that version the new baseline before you apply any other delta.
- A revert-only request ends after you show the restored baseline. Route restoration or file removal to `finalize` only for approved logo or identity assets.
- Re-open exploration only when the user rejects the approved direction or asks for new concepts.

Phase 0 ends when you set the baseline and either route the delta to a mode or continue to Phase 1 for a greenfield request.

## Phase 1: Detect mode

1. Read the invoking message and any attached images or Figma URLs. A bare mode word is a valid argument. Valid words are `brief`, `logo`, `layout`, `type`, `color`, `critique`, `identity`, `finalize`, and the `finalise` spelling, which you normalize later. In an approved logo or identity context, requests such as "this is final", "production brand assets", "export the approved logo as SVG/PNG", or "brand package" route to `finalize`.
2. Match against the mode menu below. Exactly one match sets `MODE`, and you continue.
3. Image-only fallback. When the user attached an image with no clear textual instruction, set `MODE = critique`.
4. On multiple matches, prefer the more specific mode. "Typography for a brand identity" goes to Typography. Show the menu only when no single mode is more specific or nothing matches:

   ```
   Question: "Which design-director mode fits this request?"
   Header: "Mode"
   Options:
     1. Brief Simplify:        extract objective, audience, message, tone, deliverables from a client brief
     2. Logo Concepts:         staged logo directions and controlled refinements
     3. Layout Compose:        5 layout ideas for a poster / post / section
     4. Typography System:     font pairing, hierarchy, usage guidelines
     5. Color Palette:         primary/secondary/accent palette with WCAG contrast notes
     6. Design Critique:       honest, specific feedback on an existing design
     7. Brand Identity:        full visual identity system (logo + color + type + style)
     8. Finalize Identity:     production SVG/PNG assets, theme variants, and package checks
   ```

5. Acknowledge the chosen mode in one short sentence, for example "Running Logo Concepts.".

**Phase 1 ends** by setting `MODE`.

## Mode handoff

After either routing phase sets `MODE`, normalize `finalise` to `finalize`. Read `${CLAUDE_SKILL_DIR}/modes/<MODE>.md` before Phase 2. That file declares the slots, output spec, file-save flag, and next step. The eight mode files are `modes/brief.md`, `modes/logo.md`, `modes/layout.md`, `modes/type.md`, `modes/color.md`, `modes/critique.md`, `modes/identity.md`, and `modes/finalize.md`.

## Phase 2: Gather slots

Fill the mode's slots from the message, the artifacts, the repo, and prior decisions. On a continuation, the baseline satisfies unchanged greenfield slots. Ask one question at a time, only for unresolved facts that would change the delta.

- When the answer space is bounded, offer 2-4 sensible options per slot. For a vibe slot, offer modern, editorial, playful, or luxe.
- For open-ended slots like industry or brand name, still include the 2-3 most common cases plus an Other affordance.
- Apply a sensible default and name it instead of asking when the default does not change the direction.

Phase 2 ends when every material field for the active route has a value. Echo the resolved fields in one line before Phase 3.

## Phase 3: Generate output

Run the mode's Output spec. On a continuation, produce the requested fields, every dependent output, and every invalidated check while you preserve unrelated values. Modes other than `finalize` print rich markdown to chat first. `finalize` follows its build lifecycle and prints the handoff summary only after its blocking checks pass.

I hold every mode to one bar.

- Every recommendation is a spec. Name the element and the value: typeface, px, ratio, hex. "Use a serif for headlines" is not a spec. "Pair Söhne for UI with GT Sectra Display for headlines, 1.6 ratio between H1 and H2" is one.
- Write in the imperative. Pair the typefaces. Cut the H1 to 48px. Make the call.
- Show reasoning. Each concept gets a one-line why: symbolism, principle, or precedent.
- Treat references as traits, not targets. For logo and identity work, name 2-3 deliberate moves that separate the result from cited brands. Run a small visual desk scan of adjacent category marks before you select a final direction when image search is available. Record the scan as visual collision screening, never as proof of uniqueness, trademark clearance, or legal safety.
- Classify contrast before you judge it. Under [WCAG 2.2](https://www.w3.org/TR/WCAG22/#contrast-minimum), normal text needs 4.5:1. Text at 18 pt regular or 14 pt bold and above needs 3:1, and meaningful non-text graphics or UI boundaries need 3:1. Logotypes are exempt, so report their measured ratio and visual legibility as brand-use evidence, not as a WCAG pass. Apply the text threshold to an accent when it carries text.
- Open on the first concept.

## Phase 4: Offer file save

When the user already asked to save, save without asking again. Otherwise, modes flagged `File save: yes` end with an offer to save. Modes flagged `optional` offer only when the output exceeds about 30 lines. Modes flagged `no` skip the offer.

Save path convention: `design/<mode-slug>-<short-name>.md`. Two examples are `design/typography-acme.md` and `design/palette-lumen.md`.

If the working directory has no `.git`, skip an unsolicited offer. Honor an explicit save request to the user's path, or ask for a path when none is available.

`finalize` owns its output-directory decision and asset writes. Skip this markdown save convention for that mode.

## Phase 5: Suggest next step

Print the mode's `Next step` verbatim, prefixed with `Next:`, on exactly one line. When it reads `none`, omit the line. Then stop.

## Out of scope

- Marketing copy goes to `copywriting`.
- Figma implementation goes to `figma-generate-library` or `figma-generate-design`.
- Brand implementation in application UI code goes to `figma:figma-implement-design` or `frontend-design:frontend-design`.
- Naming, taglines, mood boards, and iconography systems sit outside this skill.
