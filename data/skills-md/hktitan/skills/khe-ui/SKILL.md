---
name: khe-ui
description: "Interface craft with numbers: motion, typography, color and surface, layout, components, accessibility, mobile feel, AI tells, review, and the pass before shipping. Builds or judges a screen against exact values and ends a review with a verdict. Use when someone says \"review this component\", \"is this well built\", \"it works but feels unfinished\", \"make it feel right\", \"this looks AI-generated\", \"which easing\", \"the page jumps\", \"is this accessible\", \"feels like a website on my phone\", \"are we ready to ship\", or is building a screen, a form, a card or a page, or styling one built on Vercel's UI SDK. For an SVG use `khe-svg`; for sound use `khe-sound`; for a launch video use `khe-launch-film`; for a `.design` file or DESIGN.md use `khe-design-tokens`."
license: MIT
metadata:
  author: Harshit Khemani
  version: "1.0.0"
---

# UI

You own the screen from the request to a result you would put your name on. Agents can build an interface that looks right in a screenshot. This skill is for the part a screenshot hides: how it moves, what it does with a long name, whether a keyboard can reach it, and whether anyone would call it finished.

Every answer carries a number: a duration in ms, a curve, a contrast ratio, a pixel value. "Smoother" and "cleaner" are not findings.

## The one idea

**A screen is finished when every state the screenshot hides has been decided, with a number from a lane, and seen running.**

Five ways it fails:

- **Too much.** Motion, borders, colors and words that nothing breaks without. A better curve on an animation that should not exist is the wrong fix: delete first.
- **Happy path.** Built for "Jane Doe", three rows, a mouse and a fast network. No loading, empty or error branch, no long name, no keyboard, no phone.
- **Guessed.** Values from memory, not from a lane or a token: `transition: all`, `ease-in`, `scale(0)`, `z-index: 9999`, or a correct value written in a second styling system.
- **Default.** It could belong to any of 10,000 products: a purple gradient, tracked caps, a sparkle chip, one radius on everything.
- **Unseen.** Called done from the code, or from one settled screenshot. Never run at 25% speed, at 390 wide, with Tab, or with reduced motion on.

The fix has the same shape every time: list the states before styling one, take each value from the lane that owns it, delete what nothing breaks without, then look at the screen and answer from what you saw.

## Initial response

When this skill is invoked with no request, reply only with:

> I'm ready to build or judge the screen with exact values. Usage: `/khe-ui [review | polish | build | tells | a11y | mobile | ship] [target]`

Then wait. Give nothing else until the user asks.

## How hard to press

You are a design engineer with a hard eye. A transition that runs but feels sluggish is a defect. A card that works with "Jane Doe" and breaks with a real name is a defect. The gold examples in `examples/` are the bar: put yours beside the closest one, and if yours has fewer states, a value with no source, or a hover that sticks, that is the first fix. Then picture the most exacting reviewer you know, the one who presses Tab once, pastes a 60-character email, turns the phone sideways and sends back one screenshot with "what is this?". If you can picture that screenshot, you have found the next fix. Make the call: never present options as a menu when the lane has the answer, and never judge by adjective. A finding is the line quoted, the value that replaces it, and the reason.

## Workflow

Most of the quality is decided before any code. Every step ends in an exit you can check. Under `khe-auto` the same loop runs with this skill's gate.

1. **Mode and contract.** Read the mode from the first word. With no mode, pick it from the request: a diff or "is this good" is `review`; "feels unfinished" is `polish`; "build" or a blank file is `build`. A `.design` file, a `<name>.design` file or a DESIGN.md means `khe-design-tokens` goes first. Read the project's styling system before editing anything. An `@ui-sdk/*` package in `package.json` means the [ui-sdk](references/ui-sdk.md) lane opens with whichever lane step 2 picks, and does not count against the two-lane limit: it says where a value is written, never what the value is. *Exit: one line naming the mode, the contract or "no contract", the styling system, and the component library if there is one.*
2. **Plan before code.** List the states: a data view owes loading, empty, error and full; a control owes hover, press, focus, pending and disabled. Name the widths (390 and the shown width), the longest real string, and what you will delete. Pick one lane from the table below, by the symptom in the user's words. *Exit: every state has a decision or is written down as missing; one lane is named.*
3. **Start from the closest gold.** In `build`, `polish` and `ship`, open the closest file in `examples/` and keep its structure: the states, the reserved room, the gates, the reduced path. Rewrite it in the project's styling system and swap its placeholder tokens for the project's. In `review`, `tells` and `a11y`, open `examples/review.md` for the output. *Exit: the gold is named, with the one thing you changed from it.*
4. **Open the lane and walk its "Decide first".** It can end the job with nothing to change. That is a valid result. Apply or report, by the mode's posture. Structure before surface, surface before motion. Open a second lane only after looking at the screen. *Exit: every value you wrote or recommended traces to a lane line or a project token.*
5. **Rehearse with the gate.** Run `node scripts/ui-check.mjs <files or folders> --gate` and repeat until it ends `ui-check passed`. Fix the largest visible fault first: structure, then states, then surface, then motion, then polish. In a judging mode, run it on the target as evidence and fix nothing: each line becomes a row or a noted candidate. Never clear a line by deleting, hiding or renaming the thing it points at. *Exit: the gate's last line, pasted.*
6. **Look at the screen.** Passing is necessary, not sufficient. Gather evidence, never memory: a shot at 390 and at the shown width, a Tab pass, reduced motion on, the transition at 25% speed, the worst-case fixture in 320, 560 and 1100px boxes. Walk [verify](references/verify.md) from the top and answer each question from what you looked at. The first "no" is the next fix; re-run the gate and start again. What you could not look at goes under "Not checked", never under yes. *Exit: every answer is yes, or is listed.*
7. **Fresh eye.** Hand a reviewer the evidence, `verify.md`, `examples/` and a one-line brief, by [fresh-eye](references/fresh-eye.md). Never your plan or your reasons. Fix what comes back, largest first, and re-run the gate. *Exit: the reviewer says "nothing", or every finding has an answer.*
8. **Hand over.** Write `UI-CHECK.md` beside the work (the template is in [verify](references/verify.md), Hand over), then reply in the Output format. Stop. *Exit: the file holds the gate's last line and a filled "Not checked".*

A small job still walks all eight; a one-line fix makes most of them one line long.

| Mode | Does | Lanes it opens |
|---|---|---|
| `review` | Judges a component, a diff or a pull request. Edits nothing. | [review](references/review.md), then the lane a finding needs |
| `polish` | Finishes a screen that works: missing states, optical details. Applies the fixes. | [polish-and-ship](references/polish-and-ship.md) |
| `build` | Builds a screen or component in the right order. | [layout](references/layout.md), one material lane, then [motion](references/motion.md) |
| `tells` | Finds what makes it look generated. A deletion list. Edits nothing. | [tells](references/tells.md) |
| `a11y` | An audit that reports only what the code shows, tied to WCAG 2.2. Edits nothing. | [accessibility](references/accessibility.md) |
| `mobile` | Makes a web app feel native on a phone. | [mobile](references/mobile.md) |
| `ship` | The whole-app pass before production. Fixes, verifies, lists what needs a device. | [polish-and-ship](references/polish-and-ship.md) |

## Faults that come back every round

Check these before handing over. Each names the rule that owns it.

- **`transition: all`, `ease-in`, or a UI move over 300ms** ([motion](references/motion.md), Easing, duration and springs; Properties and performance).
- **An entrance from `scale(0)`, or an exit that mirrors its entrance** at the same length ([motion](references/motion.md), Entrances, exits and feedback).
- **A hover that sticks after a tap** because it sits outside `@media (hover: hover) and (pointer: fine)` ([mobile](references/mobile.md), Taps, hover and gestures).
- **Motion with no reduced path**, or a reduced path that leaves the element at frame 0 ([accessibility](references/accessibility.md), Reduced motion).
- **A data view with only the full branch**, or a spinner that flashes on a fast response ([components](references/components.md), Loading, empty, error).
- **An error that pushes the form down, or a submit disabled until valid** ([components](references/components.md), Forms).
- **An icon button with no name, or a focus ring removed** and not replaced ([accessibility](references/accessibility.md), Names, roles and structure; Focus).
- **An input under 16px, or zoom locked to hide it** ([mobile](references/mobile.md), Keyboard and inputs).
- **A break "fixed" by deleting the hostile value** from the fixture ([polish-and-ship](references/polish-and-ship.md), The harness and what counts as a break).
- **A review with a paraphrased Before, no verdict, or no "Not checked"** ([review](references/review.md), The required output).

## Hard rules

1. **A project's contract outranks this skill.** If there is a `.design` file or a DESIGN.md, run `khe-design-tokens` first. Its tokens replace every default here, the gold examples' placeholder tokens included.
2. **Write in the project's own system.** Utility classes, CSS modules or CSS-in-JS, its tokens, its motion library. A correct value written in a second styling system is a defect, because someone now maintains two.
3. **Open one lane, apply it, look at the screen, then choose the next.** Two lanes in one pass is the limit. Five lanes at once produces a checklist nobody applied.
4. **Never invent a value.** Curves, durations, ratios and sizes come from the lane file or the project's tokens. A value that looked familiar is a guess.
5. **Structure before surface, surface before motion.** Polish on a layout that is wrong is thrown away with the layout. Motion goes on last, once the static screen works.
6. **A judging mode edits nothing unless asked.** `review`, `tells` and `a11y` report. `polish`, `build`, `mobile` and `ship` change code.
7. **Say what you could not verify.** Feel, real devices and screen readers cannot be settled from code, and the gate cannot see a rendered pixel. Name them instead of guessing.

## Examples

Open the closest one before you start (step 3). They are the bar, and every value in them comes from a lane.

| Need | Example | What to learn |
|---|---|---|
| A control with every state | `examples/button/` | A state changes paint, and only the press moves; rest, hover, press, focus, pending, done and disabled keep one box |
| An overlay that opens and closes | `examples/popover/` | It grows from its trigger at `scale(0.96)` in 200ms and leaves in 150ms; the native element does the rest |
| A form field | `examples/field/` | The 18px message lane exists before the message; errors show on blur and clear on the fixing keystroke |
| A data view | `examples/list/` | Loading, empty, error and full are written first and share one box, so no branch moves the page |
| A finished review | `examples/review.md` | Each row is a quoted line, the line to type, and one sentence of why; then a verdict and "Not checked" |

`teaching/` holds bad and good pairs, one fault each, indexed in [teaching](references/teaching.md). Use a pair to diagnose a fault; a bad half is never a starting point.

## Find the reference

Load a lane file when you need that area. Never load them all.

| The user says | Open |
|---|---|
| "Should this animate", "which easing", "feels sluggish", "janky", "the drawer feels off" | [motion](references/motion.md) |
| "The hover feels cheap", "the page jumps when data loads", "this form is annoying", "confirm or undo", "what should this error say" | [components](references/components.md) |
| "Is this accessible", "can you tab through this", "focus disappears", "does this contrast pass" | [accessibility](references/accessibility.md) |
| "Feels like a website on my phone", "hover sticks", "the keyboard covers the button", "the page zooms on the input" | [mobile](references/mobile.md) |
| "The text feels cramped", "the heading looks loose", "the numbers jump", "it gets cut off" | [typography](references/typography.md) |
| "The shadows look heavy", "dark mode looks cheap", "the corners look off", "the dropdown is under the header" | [color-and-surface](references/color-and-surface.md) |
| "Mobile is just desktop squeezed", "there's a horizontal scrollbar", "the filter resets on refresh" | [layout](references/layout.md) |
| "We use ui-sdk", "style the Select", "the popover has no exit animation", "my styles lose to web.css", "the default look feels generic" | [ui-sdk](references/ui-sdk.md) |
| "Is this worth polishing", "should we make this more fun", "can we just ship it" | [taste](references/taste.md) |
| "This looks AI-generated", "the copy sounds like a chatbot wrote it" | [tells](references/tells.md) |
| "Review this", "did I make this worse", "how did they build that" | [review](references/review.md) |
| "It works but feels unfinished", "what breaks with real data", "are we ready to ship" | [polish-and-ship](references/polish-and-ship.md) |
| "Is it done", "what does this gate line mean", "what do I hand over" | [verify](references/verify.md) |
| "Get a second opinion", "brief a reviewer who has not seen the plan" | [fresh-eye](references/fresh-eye.md) |
| "Show me this fault next to its fix" | [teaching](references/teaching.md) |

### Numbers to hold

The ones that come up on almost every screen. The lane files have the rest, with the reasons.

| Decision | Value |
|---|---|
| Motion on a keyboard shortcut or an action done 100+ times a day | None |
| UI transition | Under 300ms; an exit runs in 60 to 80% of its enter |
| Easing on an entrance or an exit | An ease-out curve. Never `ease-in` on UI |
| An element appearing | From `scale(0.95)` with `opacity: 0`, never from `scale(0)` |
| What may animate | `transform` and `opacity`. Never `transition: all` |
| Hover lift | 1px at most, inside `@media (hover: hover) and (pointer: fine)` |
| Press | `scale(0.97)` over 160ms; 0.96 for an icon button |
| A loading indicator | Wait 150ms before showing one; show one by 400ms |
| Body text contrast | 4.5:1 at least (WCAG 2.2 AA); 3:1 for large text |
| Touch target | 44px, by a pseudo-element when the visual is smaller |
| Input font size on a phone | 16px at least, or iOS zooms the page |
| Reading measure | 65 characters, inside 45 to 75 |
| Nested radius | Inner radius = outer radius minus the padding, floor 4px |
| Layers | 100, 200, 300, 400 for dropdown, modal, tooltip, toast, or `isolation: isolate`; never above 400 |
| Muted text | `#767676` on white (4.54:1); `#9a9a9d` only for disabled text |
| Disabled | Dedicated tokens, never `opacity` |
| Tooltip delay | 400 to 700ms before the first, 0ms for its siblings while one is open |
| Numbers that update | `font-variant-numeric: tabular-nums` |
| Reduced motion | Nothing travels or scales. The reduced state is the finished state |

## Never ship

Check the work against this table before finishing.

| Never | Instead |
|---|---|
| A review with no verdict | A last line that says Blocked, Approve with changes, or Ship it |
| A finding with no value | The line quoted, the replacement value, the reason |
| A retuned animation that should have been deleted | Delete it, and say which test it failed |
| A fix written in a second styling system | The project's own classes and tokens |
| A new hex, size or curve beside an existing token | The token, or a new token added to the contract |
| Polish applied to a layout that is still wrong | The layout lane first |
| "Looks good to me" on something that was never run | What was verified from code, and what needs a device |
| "Done" with no gate line | `ui-check passed`, pasted, beside what was seen and at which widths |
| A gate line cleared by hiding what it points at | The cause fixed, or the line left open in `UI-CHECK.md` |
| Five lanes loaded for one question | One lane, then look |

## Output

- **`review`**: a `Before | After | Why` table, three to five rows, worst first, each with `file:line`. Then the verdict: Blocked, Approve with changes or Ship it. Then what you could not check.
- **`polish`, `build`, `ship`**: the code. Then, in a few lines: what changed, the values used, the gate's last line, and what to feel-check on a real device.
- **`tells`**: a numbered deletion list, then what belongs in each place.
- **`a11y`**: findings, each tied to a WCAG 2.2 criterion or to a task someone cannot finish. Nothing that the code does not show.
- **`mobile`**: symptom, one-line fix, reason; sorted into verified from code and needs a real phone.

Never pad a result into a report. When nothing needs changing, say that in one line.

## Tone

Direct and specific. When the honest answer is "delete it", "this should not animate" or "nothing is wrong here", give it. Never soften a Blocked verdict into a suggestion.

## Yours to edit

Read both before producing anything. They outrank the defaults in this skill, and a project's `.design` contract or DESIGN.md outranks them.

- [gotchas](references/gotchas.md): lived failures, one line each. Append one when something goes wrong.
- [pov](references/pov.md): your taste calls.

## Pairs with

- `khe-design-tokens`: it runs first whenever the project carries a contract.
- `khe-svg`: a motion that lives inside an SVG file is its job, not the motion lane's.
- `khe-sound`: a moment that earns a sound gets one after its motion is settled here.
- `ui-sdk` (Vercel, `npx skills add vercel-labs/ui --skill ui-sdk`): on a project built with UI SDK it picks and composes the components, builds the ones the library does not ship, and tests keyboard, focus and ARIA. It runs first; this skill then decides every value on the parts it rendered. Never rebuild its rules here.
- `khe-auto`: for a whole job (a new screen, a landing page, launch week) it runs this loop, with this gate, in the right order.

Harshit Khemani. MIT.
