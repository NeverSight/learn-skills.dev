---
name: game-ui-ux
description: "Design, implement, critique, and refine in-game UI and player UX: HUDs, menus, inventories, loadouts, tactical previews, drafting, progression, and controller navigation. Use for game interface tasks, especially when output looks like a website or dashboard, contains redundant captions, lacks game-specific art direction, or needs complete interaction states. Preserve the game's rules, approved style, engine, and input constraints. Not for game marketing websites, ordinary business apps, or editor tools unless explicitly requested."
---

# Game UI / UX

Design an instrument for playing this particular game, not a page explaining it.
The target is playable clarity and authored character—not maximal minimalism,
maximal decoration, or a recognizable imitation of another game's menus.

**User preference: no subheadings.** In generated interfaces and mockups, never add
visible subheadings, subtitles, eyebrow labels, taglines, decorative captions, or
heading-plus-explanation stacks unless the user explicitly requests them. This is
a content rule, regardless of HTML tag or styling. A screen may have one concise
primary title when needed; do not title every region. Group content through spacing,
alignment, and visual hierarchy. Keep necessary action labels, actual game state,
control instructions, errors, and accessibility names directly attached to what they
refer to. Dialogue subtitles and accessibility captions are functional content, not
decorative subheadings. Do not remove them under this rule.

For example: show "Reach the flag" once, not "First to the flag wins" above
"Make thy way"; show the player's name without "That's you"; show "Austin wins"
without an eyebrow, victory tagline, or explanatory caption. Put mockup notes in
the handoff rather than around the game interface. Before delivery, inspect every
visible text element and remove all unrequested secondary headings and decorative
copy. Do not justify exceptions as personality, orientation, or useful context.
This rule also applies to written handoffs for this skill: use concise prose without
subheadings. Internal headings in this instruction file organize the skill only;
they are not a template for generated output.
## Scope and operating mode

Honor the user's request and repository instructions. These are design defaults,
not permission to replace approved decisions or expand scope. Inspect the actual
project before choosing a stack. A browser game is valid; silently substituting a
web mockup for an engine implementation is not.

Choose the smallest useful mode:
- **Patch:** fix the requested defect; preserve surrounding behavior and identity.
- **Critique:** report specific observations, player consequences, and prioritized fixes.
- **Design:** deliver an implementation-ready interaction and visual specification.
- **Build:** implement a playable slice in the requested runtime, then exercise it.

Do not answer an implementation request with only a design essay. Do not implement
an unsolicited game when the request is for critique or specification. Use existing
context before asking questions. State reversible assumptions briefly; request
clarification only for material ambiguities that cannot be resolved from the project.
Do not invent rules, currencies, quests, lore, telemetry, or backend success to fill space.

## 1. Establish the player's task before the layout

Extract from the brief and project:
- The immediate decision or action, its frequency, and intended emotional tone.
- What the player must know now, can inspect later, and must not know yet.
- Authoritative state, costs, eligibility, consequences, and recovery rules.
- Supported inputs, display/viewing conditions, locales, and accessibility settings.
- Existing visual grammar, reusable components, available assets, and production budget.

Use this practical loop:
**Game state → perceivable information → player decision → input → state change → feedback.**
Find missing links before adding decoration. Distinguish intentional game difficulty
from difficulty discovering or operating the controls. Do not expose secrets to
improve clarity or obscure intended information to create artificial depth.

For a substantial new screen, record a brief decision contract: player task, relevant
state, primary action, uncertainty, inputs, and intended tone. Do not put this contract,
its headings, or your design rationale into the player-facing interface.

## 2. Compose around relationships, not containers

Identify the focal object or task: world, character, equipment, map, board, hand,
conversation, or settings operation. Place supporting information in relation to it.
Do not begin with a header/subtitle/sidebar/card-grid/footer template.

For each element, identify a defensible purpose: **action, state, comparison,
orientation, learning, recovery, or deliberate expression**. Use grouping and
alignment before adding a box; use scale and contrast before adding a heading.
Boxes remain available; visible headings must obey the no-subheadings rule above.

During action, protect awareness of the world. During planning, preserve relevant
density and comparisons. Keep values needed together visible together when practical;
otherwise provide direct comparison without repeated memorization. Preserve spatial
stability for frequently checked information.

For genuinely uncertain designs, compare a small number of structurally different
approaches before polishing one. Do not generate three recolors or force alternatives
for a simple patch. Prototype the uncertain part at the fidelity needed to test it.

## 3. Establish an authored visual grammar

Derive the presentation from this game's fiction, camera, art, pacing, and audience.
Specify composition, typography roles, semantic colors, shape/material language,
icon style, depth, focus/selection treatment, and motion/sound behavior. Make them
cohere across screens. Reuse approved assets and rules before inventing new ones.

Separate expressive display treatment from sustained reading and numerical comparison.
Make the strongest visual treatment correspond to the most important current event or
action. Distinguish interactive and decorative elements. Test over actual gameplay,
not only a quiet background.

Use motion to acknowledge, explain, orient, warn, or celebrate. Routine input must not
wait for ornamental choreography. Preserve essential feedback with reduced motion.
Do not turn every panel into a constantly animated focal point.

Do not cure generic web design by defaulting to neon, scanlines, angled military panels,
microtype, or a Persona imitation. Ordinary controls may remain ordinary. A deliberately
corporate in-world terminal may look corporate. Context, not a style blacklist, decides.

## 4. Make the copy earn its place

Before delivery, inspect the visible strings. Ask what each adds that nearby state,
layout, or text does not already communicate. Delete a subtitle that merely paraphrases
a title. Replace vague instructions with the actual action or consequence.

| Weak default | Better treatment when context supports it |
|---|---|
| Inventory / Manage your inventory | Inventory |
| Resources / Keep track of your resources | Relevant resource names/symbols and values |
| Select an option below | The actual choices, unless an instruction is needed |
| Action unavailable | Requires 2 energy; you have 1 |
| Continue, when it immediately equips an item | Equip |
| Item selected successfully! on every selection | Persistent local selection feedback |

These are examples, not global string replacements. Keep necessary action labels,
mechanical descriptions, costs, warnings, tutorial help, and dialogue subtitles,
accessibility captions, and narration semantics. A card game can use cards. A complex
choice can need several sentences. An icon is not automatically clearer than a word.

Do not make the player read design commentary such as “Strategic Overview,” “Optimize
your experience,” or “Everything you need in one place” unless it has a real in-world
or task-specific purpose. Do not replace removed filler with invented flavor text.

## 5. Specify and implement the behavior

For each affected interactable, define relevant states and transitions—not just its
normal appearance. Distinguish hover, focus, selection, equipped/active, unavailable,
pending, success, and failure. They are not synonyms.

Specify:
- What input previews, commits, cancels, or undoes; what is reversible.
- Where focus enters, moves, and returns; what a modal owns; how to exit.
- How pointer, digital navigation, controller, and touch behave where supported.
- What happens with empty/full/filtered lists, long content, state changes, and failures.
- How remapping/device changes affect prompts and how input contexts prevent leaks.

Read real state and request real game actions. Preview calculations must match the
authoritative rules without leaking hidden state. Acknowledge input separately from
confirmed completion. Do not display a server operation as successful before it is
confirmed; prevent duplicate commitments and handle failures honestly.

Preserve useful selection and comparison context after sorting, filtering, closing an
inspection, or equipping. Use stable identities rather than incidental list indices.
Do not force a controller cursor, hover-only knowledge, or drag-only operations where
they create unnecessary barriers. Preserve the game's deliberate interaction mechanics.

## 6. Verify the actual result and refine it

Match validation to the deliverable. For builds, run the project and exercise relevant
inputs when tools permit. For specifications, trace the defined scenarios and mark them
as specification review—not runtime tests. A still image supports visual observations,
not claims about responsiveness, controller support, or usability.

Review separately:
1. **Truth:** displayed rules, values, costs, previews, eligibility, and outcomes match.
2. **Operation:** the intended task, cancel/back, recovery, and repeated use work.
3. **Access:** focus, readable/scalable content, applicable input alternatives, and
   redundant critical cues survive the target conditions.
4. **Identity:** hierarchy and art direction belong to this game, including quieter variants.
5. **Restraint:** remove redundant strings, wrappers, badges, and waiting—not information
   or personality that the player actually needs.

Test applicable stress cases: larger text and localization, narrow/wide viewport,
busy backgrounds, rapid input, content extremes, changed eligibility, and interrupted
or failed actions. Verify first-entry accessibility where the changed flow could block it.
Use a small representative set for a patch; use the broader matrix for a new flow.

An incorrect gameplay preview, inaccessible essential action, focus trap, hidden
irreversible consequence, or fabricated success is a blocker. Visual polish cannot
compensate for it. Mark unknowns as untested, not passed. Do not claim player testing,
platform certification, or performance measurements that were not performed.

## Handoff

Deliver the requested artifact first. Briefly report meaningful design decisions,
what actually changed, checks actually run, and remaining limitations. Show only the
working notes needed to understand the result. Stop when the requested slice is useful
and the relevant checks are complete; do not redesign the whole game to finish a task.
