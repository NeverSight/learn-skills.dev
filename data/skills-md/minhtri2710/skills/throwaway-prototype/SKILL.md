---
name: throwaway-prototype
description: Build throwaway code that answers one design question, either a single-file HTML demo that drives a state model or several structurally different UI variants on one route. Use when the user wants to feel out whether a state machine, data shape, or API surface holds up, or to see a few options for what a screen should look like, before committing to an implementation. Do not use to build the real feature, to test production code, or to design or polish the real UI of an existing screen.
---

# Throwaway Prototype

A prototype is throwaway code that answers one question. The question decides
the shape; answering the wrong question wastes the whole prototype, so name it
first, in a visible line at the top of the artifact.

## Pick the branch

- **"Does this logic or state model feel right?"** builds a logic demo: one
  self-contained HTML file a non-developer can double-click.
- **"What should this look like?"** builds a UI prototype: several variants on
  one route, switched from a floating bar.

When the question is ambiguous and the user is not reachable, choose by the
surrounding code (a backend module wants logic, a page or component wants UI)
and state the assumption at the top.

## Rules for both

- Throwaway from the first line, and named so a casual reader sees it: put it next
  to the module or page it is exploring, with `prototype` in the name.
- Trivial to run: one double-click, or one existing task-runner command.
- No persistence; state lives in memory. Persistence is what the prototype is
  checking, not something it depends on. When the question is about a database,
  use a scratch store with "PROTOTYPE, wipe me" in its name.
- No tests, no error handling beyond what makes it run, no abstraction, no
  generalising for a later need. A prototype that needs tests is no longer one.
- Surface the full relevant state after every action or on every variant switch.

## Logic demo

Put the logic in one `<script>` block as a small pure module: a reducer
`(state, action) => state`, an explicit state machine, a set of pure functions, or
a class with a clear method surface — whichever fits the question, not whichever
is easiest to wire. It touches no DOM; the page calls in and nothing flows back.
That is what lets the validated module lift into the real codebase intact.

The page is plain HTML, CSS, and JS with everything inline, written in domain
language, laid out top to bottom: the question; the current state as labelled
fields, re-rendered after every click with what just changed; free-play buttons,
one per action, always available; and guided walkthroughs, one tab per scenario,
each a plain-language setup plus the ordered buttons to press, resetting to a
known state when started. Pick scenarios that are hard to reason about on paper:
the happy path, a tricky edge, an action that should be illegal.

## UI prototype

Default to three variants; more than five is noise. Prefer mounting them on the
existing route, gated by a `?variant=` search param, with the real header, data,
and density around them; an empty new route hides the design problems a
populated one exposes. Create a throwaway route only when nothing can host the
variants, following the project's routing convention.

Variants are structurally different: different layout, information hierarchy,
and primary affordance, not different colours. Two drafts that come out alike
mean one is redone under an explicit constraint ("no card grid"). Each is a
clearly named export; a shared switcher component reads the param, cycles with
arrows and the arrow keys (not while an input is focused), updates the URL so a
variant is shareable, looks unlike the design under judgment, and is hidden in
production builds so a stray merge cannot ship it.

## Hand over and capture

Give the user the file or the URL and the variant keys. The useful feedback is
"that should not be possible" or "the header from B with the sidebar from C";
add actions and scenarios as they ask. When the question is answered, fold the
validated logic module or the chosen layout into the real code and record the
verdict where the work is tracked. Delete the prototype unless the user asks to
keep it; the main tree keeps only the decision.
