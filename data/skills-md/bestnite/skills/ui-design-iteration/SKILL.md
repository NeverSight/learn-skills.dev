---
name: ui-design-iteration
description: "Use when drafting a UI from a template or reviewing it live: picking, sliders, patches."
---

# UI Design Iteration

## Scope

This skill takes a UI from a first draft to a reviewed, port-ready page: it rebuilds a first draft from an existing reference when no design exists yet, gets it onto disk as a live page, lets a human point at it, turns their words into small patches, and verifies the result.

It does **not** invent what the page looks like. The look comes from something someone already designed: a reference the user picked — a template demo or a live site (Step 0) — a design skill or design agent the user trusts, the user, or the running product the draft was extracted from. This skill reuses or rebuilds that design, binds it and reviews it; it never draws a page from a one-line brief.

What it delivers: a **live static draft** — a draft directory with one HTML entry page and its local CSS/JS, openable in a browser with no build step and no network, adjustable in place, discussable element by element — plus a sequence of reviewed patches.

Out of scope, deliberately:

- **Drafting from nothing.** A page generated from a one-line brief invents composition, type and palette at once, and every later round argues with choices nobody made. Start from a reference (Step 0) or a design source instead.
- **Porting.** Migrating the draft into a framework, a template language or a CMS is a separate job for whoever owns that codebase. Do not scaffold application structure, do not wire data, do not "helpfully" migrate.

## Interop: what to take from a design source

- **Require an artifact, not advice.** The input is a self-contained HTML page. If the design arrived as prose, materialize it into a file once — without re-deciding anything it settled.
- **Translate, do not redesign.** A design system, spacing scale or token list goes into the draft's `:root` block as a mechanical mapping. If two design sources disagree, the user picks one; blending two systems is the most expensive mistake available here.
- **Send missing pieces back.** When the design has no rule for a surface the page needs (an empty state, a dialog, an error), ask the design source or copy it from the product's own components. Never invent visuals to fill the hole.
- **The contract outranks the default limits.** `references/audit.md` holds default limits that end iteration; a decision recorded in `design-contract.md` overrides any of them, because the audit reports, it does not redesign. Its accessibility checks are the exception: no design decision waives a contrast failure.

## What needs the agent's own tools

Talk to the user in their own language; the questions below are written in English only so the skill does not fork.

- **A shell with Node and network access** is needed only to render a framework template whose source you copy (Step 0, route A). Without one, ask the user to run it and send the output, or save the template's live demo instead.
- **A browser the agent controls** is needed for screenshots and measurements of reference demos, for driving an app to capture its states, and for checking hit-testing. If you have a browser tool, use it; a headless browser you script from a shell (over the DevTools protocol, or with Playwright) counts as one. If you have neither, ask the user to open the page and send screenshots, and name every check you could not run yourself — a check that was skipped must not read as passed.
- **A long-running process** is needed for `scripts/draft_server.py`, and on route A for the template's dev server. Start it with whatever mechanism your runtime offers for background processes; the port is the user's or the environment's choice, or `0` to take a free one. Record the PID of every process you start — the one that holds the port, which may be a child of the PID your shell reports (`$!` can be a wrapper) — and stop exactly those PIDs when done, then confirm they are gone (the process no longer listed, the port no longer answering) — never stop processes by name or pattern (`pkill next`, matching on a command line), because the machine may run other services with the same name.
- **The selection** reaches you as `selection.json` in the draft directory while the server runs. If you drive the page in a browser, `window.draftKit.snapshot()` returns the same object and `window.draftKit.audit()` counts the rendered page. With neither, ask the user to read you the panel's readout — and treat it as a weaker reference than the file.
- **Widths** are set in the browser: your browser tool's viewport, or the user resizing theirs. The snapshot records which width the reviewer saw.

## The loop

| Step | Goal | Output |
| --- | --- | --- |
| 0 Draft from a reference | the reference's design language over the user's content and sections | `<name>.html` with levers bound |
| 1 Intake | the design on disk, tokens bound | `<name>.html`, one `:root` block, `design-contract.md` |
| 2 Make it live | the draft behaves like the page | draft runtime + review panel attached, server running |
| 3 Iterate | changes become addressed and small | per-element patches, each read in a diff |
| 4 Audit and hand off | limits met or waived in the contract, port-ready | the draft directory, its contract, its anchor map |

Skip Step 0 when a design already exists. Do not skip step 1's token binding. It is what makes step 3 cheap: with tokens in place, most "tighter / lighter / rounder" requests become one number instead of a rewrite.

## Step 0 — Draft from a reference

Take an existing, well-designed page and carry its design language over to your content; `references/drafting.md` is the procedure, and `references/sources.md` says how to judge any source and carries a starter catalogue for users without a preference.

- **The argument before the references.** Write the page as claims with their proof, and note the proof, imagery and stack that really exist: with the parts the user asked for, they decide the page's sections and which references can serve them.
- **The user's sources first.** Ask which libraries, template sites, galleries or sites they prefer, and search those before the starter catalogue.
- **The user picks the main reference.** Shortlist two or three, show them, and let the user choose: choosing a reference is choosing a design. When the user asks you to choose, pick the best-screened one, say why, record that you chose it at their request, and have them confirm it next to the first draft.
- **Study, then measure, then write down the design language.** Screenshots give the structure; the live demo's computed styles give the values — type scale, spacing, radii, palette, timing — which become the levers; a short list of what the reference does and where — its pictures, glows and their rhythm down the page included — with its signature devices marked, is what every section is held to.
- **Copy the code; rebuild only from screenshots.** Route A, the default, takes the template's own source, or else the live demo's rendered page saved with its stylesheets, fonts, icons and images, keeps its markup and CSS, and binds the levers to whatever properties that CSS exposes. Route B rebuilds a part only when there is nothing to copy.
- **Content decides the structure; the reference decides the look.** Plan the sections from the content: copy a reference section where one fits, take one from the reference's other pages, or compose one from its parts, in a form the reference uses and different from its neighbours' — not a table by default. Header layout, borders, background, accent colours, illustration and icon style, band widths stay as the reference has them in every section, every signature device keeps a place, and you pick no colour, typeface or border of your own. The text is the user's; the reference's pictures stay as placeholders until the user has their own; proof — customers, quotes, figures — is never sampled.
- **Compare before showing.** Screenshot the draft and the main reference at the same widths: copied sections against their originals, composed sections against the design language, and the whole page for its signature devices, for neighbouring sections in the same form, and for stretches without a picture longer than the reference has. Fix the drift before the first review round.

## Step 1 — Intake

- **One draft directory.** One HTML entry page, its CSS inline or in local files next to it, no build step, nothing fetched from the network — a draft must open offline, from disk, months later.
- **Real copy.** Placeholder text hides the two failures that matter: a headline that does not fit, and a section with nothing to say.
- **Bind the levers.** For a design delivered as a page, put the thirteen levers in one `:root` block — `--gap`, `--fs`, `--ratio`, `--measure`, `--radius`, `--hue`, `--ink`, `--surface`, `--line`, `--edge`, `--shadow`, `--room`, `--dur`, plus a declared `--ease` — and derive every tunable value from them. For a draft extracted from a running product or copied from a reference's code, that stylesheet is the truth: bind the panel to the custom properties it already has and record the mapping, instead of rewriting its CSS. `references/tokens.md` has both cases.
- **Enumerate the conditional surfaces** the view can show. `references/intake.md` is the checklist for receiving a design without inheriting its gaps.
- **Record the contract** in `design-contract.md` (copy `templates/design-contract.md`): the levers and their source, what was decided elsewhere, what was rejected, which values are samples.

## Step 2 — Make it live

A draft is reviewed by using it. Links must not navigate, picking is an explicit mode that is off by default, menus and dialogs open, and every state the page cannot reach gets a button on the panel.

- `references/live-draft.md` — the rules for a usable draft, the draft runtime, capturing conditional surfaces, extracting a draft from a running app, verifying by looking.
- `references/panel.md` — attaching the panel (copy `templates/draft-kit.js` into the draft directory; one config block, one script tag), its config, the snapshot it posts, the server.

## Step 3 — Iterate

Make every change addressable before making it fast.

- **Anchor every section and component root** with a stable attribute (`data-node="pricing/plan-card#1"`). Without anchors "the card" means whatever the model guesses, and a guess costs a full rewrite.
- **Read the selection, do not ask for it.** Picking records the element's CSS selector, owning component, computed values and text contrast; marks add several elements with the reviewer's notes; the snapshot also carries moved sliders and the viewport width. Read it before every change round, and check the `ts`.
- **One dimension per round** — density, hierarchy or temperature. Three at once and nobody can attribute the result, so the next round is blind too.
- **Return a patch, never a file.** The review unit is a diff. A diff that touches a sibling, a heading or a paragraph nobody asked about fails even when the result looks right.
- **Screenshot before and after**, with the kit hidden (`H`) and the window at the width the request was made at; a change to a lever or a shared class needs the whole page at every reviewed width. It is the only regression test a visual change has (`references/iteration.md`).

`references/iteration.md` has the payload in use, vague-feedback triage and the rules for a round.

## Step 4 — Audit and hand off

`references/audit.md` has three parts. The default limits (two radii, two shadows, five type sizes, one card grid, no gradients, no icon-topped feature rows, …), counted with the panel's audit at every state and width: apply each one to what the draft adds — the main reference's own devices are standing decisions — and unless the contract records a decision that overrides it, and report what exceeds a limit before removing anything that is a design decision rather than drift. The accessibility checks (contrast, visible focus, keyboard, target size), which no contract waives. And the widths to review at.

A draft is finished when someone else can port it without a conversation. Hand over the draft directory **without** the review tooling (the `DRAFT_KIT` block, the `draft-kit.js` tag and file, `data-levers` attributes, `selection.json`), plus `design-contract.md` with its anchor map, its runtime file list, its named approximations, the widths and accessibility checks covered, and one line saying what is intentionally absent (data wiring, routing, states beyond the captured ones).

## Files

| File | Read it when |
| --- | --- |
| `references/drafting.md` | Starting without a design: classify, shortlist, study and measure, write down the design language; plan sections from content; copy, compose or rebuild; compare. |
| `references/sources.md` | Which template catalogue or gallery for which page, what each lets you study, which publish code; dated. |
| `references/intake.md` | Receiving a design: what to require, what to send back, mapping its system onto the levers. |
| `references/tokens.md` | Binding the levers, extracted products, mapping external components, light and dark. |
| `references/live-draft.md` | Making the draft behave: navigation, picking rules, states, conditional surfaces, extraction, verification. |
| `references/panel.md` | Attaching and configuring the review panel; marks, contrast, the audit; the snapshot schema; running the server. |
| `references/iteration.md` | Using a selection and marks, the patch rules, vague-feedback triage, order of work. |
| `references/audit.md` | Before reporting done: the default limits, how to count, accessibility, widths, the removal order. |
| `templates/design-contract.md` | Start of any draft; copy next to the draft and fill in. |
| `templates/draft-kit.js` | The review panel — sliders, picking, marks, contrast, audit, live reload; copied unchanged into the draft directory. Dependency-free. |
| `templates/draft-kit.html` | An example draft: lever block, anchors, a draft runtime, the panel attached. |
| `scripts/draft_server.py` | Serve the draft and write `selection.json`. Python 3 stdlib only. |
