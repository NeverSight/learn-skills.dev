---
name: hrt-dark-mode-opt-in
description: Opt-in gate for tempa-spec's dark mode (bounded autonomous decision-making across discovery-through-align, optionally through apply). Never offered proactively - only activates when the user asks for it unprompted, in their own words. Shows a mandatory risk warning before any confirmation, then asks which variant (planning-only or +implementation) and creates dark.md. Use once, at or after discovery, only on explicit user request.
---

# hrt-dark-mode-opt-in

Lets the agent resolve findings that would normally escalate to the user - across `proposal`, `specs`, `design`, `align`, optionally `apply` - via `hrt-dark-mode-decision-gate`, logging every decision to `dark.md`. WALKTHROUGH stays mandatory in every variant.

## Never proactive
MUST NOT offer, suggest, or mention dark mode - at any phase, in any form. This skill MUST NOT run unless the user has already asked for dark mode unprompted, in their own words. If they never ask, this skill never runs and nothing changes.

## Steps
1. User asked for dark mode. Show the warning below, in full, unedited, before anything else.
2. Ask which variant:
   - **Planning-only.** Covers `discovery` through `align`. WALKTHROUGH stays a fully manual closing review. `apply` is out of scope for this run.
   - **+implementation.** Same, then continues automatically into `apply` in the same session after a clean WALKTHROUGH, using `hrt-dark-mode-decision-gate` for `apply`'s review findings too. A second closing review happens after `apply`, showing the code diff alongside `dark.md`.

   State that +implementation carries every planning-only risk plus the risk that a bad decision reaches shipped code, not just a document.
3. MUST get an explicit answer naming the variant before proceeding. MUST NOT treat silence, or an answer to a different question, as that answer.
4. Create `dark.md` from the `dark.md` template: chosen variant + timestamp in the header, per-stage sections empty. Include the Apply section only if +implementation.
5. `dark.md`'s existence is the only signal dark mode is active. No separate flag.

## The warning (show verbatim, in full, before step 2)

> DARK MODE is a PROTOTYPE and DANGEROUS. Do not use it for sensitive or critical work.
> The agent will make big decisions by itself. Normally, the agent stops and asks you before a big decision.
>
> In dark mode, it does not stop. It decides alone, and it can decide wrong.
> A wrong decision can damage your codebase. In the worst case, your work could be lost.
>
> If something goes wrong, YOU ARE RESPONSIBLE for the result.

If step 3's confirmation was given without this warning shown first, in full, MUST NOT treat it as valid - show the warning and ask again.

Follows the `plain-language-writing` skill's COMMS rules.
