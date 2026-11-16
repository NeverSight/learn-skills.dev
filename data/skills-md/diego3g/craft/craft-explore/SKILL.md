---
name: craft-explore
description: Use when asked for options, alternatives, variations, directions or "a few ideas" for a screen, flow or element, when the person rejects a design or says they don't like it, or says "rethink this", "try something else" or "design both so I can pick".
---

# Three proposals

## Overview

When someone asks for options, they want to **choose**, not to be handed a winner. Give them three directions that solve the problem in genuinely different ways, side by side, at the same fidelity, next to what exists today, **with your recommendation first**. Then wait for the pick.

## When to use

- "Give me options", "3 variations", "other directions", "what else could this be?"
- "I don't like this", "rethink it", "try something different".
- "Design both so I can choose": that means two.

## When NOT to use

- A specific change ("change the title to Preferences", "make it blue"): make it.
- One clear fix the person already described.

## Before you start

0. Read `DESIGN.md` at the project root if it exists: it is the project's design brief.
1. Read the project's design system and the screen in question. All options use the system's pieces and tokens: options differ in **design**, not in brand.
2. Pick your tool's adapter in `references/adapters/` (`paper.md`, `figma.md`, `html.md`). If no adapter matches your tool, do the same verbs in your tool and say which you mapped by hand. With no design tool at all, build in HTML (`html.md`). If an image is all you have, say that values read from it are estimates.

## Steps

1. **Restate the problem** in one or two sentences: what's wrong today, and what a good result must do. If the request was only "make it better", name the problem you see. **Stop and confirm it with the person before designing.** If they already named the problem, go on.
2. **Choose the directions on different axes** ([divergence axes](references/divergence-axes.md)): structure or placement, interaction model, density, emphasis, or what gets removed. Write each direction as one line: the idea and its trade-off. Directions must differ: a different axis, or clearly different values on one axis when the person names the axis ("too dense" → three density answers). A change of colour, theme or font is never an axis.
3. **Build the comparison board in a temporary area** ([comparison board](references/comparison-board.md)):
   - a legend card (each option's idea, what it's good at, what it costs, and the recommendation with its reason);
   - **"Current"**, a copy of today's design, when one exists;
   - options **A, B, C**, the same size and with the same realistic data.

   **Never edit the real screens.**
4. **Draw every option with final-screen care**, including the states that its difference affects. If B moves an action into a menu, show the menu open.
5. **Present the recommendation first**, then one line per option. **Stop. The person picks, combines ("B with A's header"), or rejects all of them.**
6. **After the answer:**
   - **Pick or combination:** apply it to the real screens and the design system (and its propagation to every screen that uses a changed piece), then clear the temporary area.
   - **All rejected:** go back to step 1 with their reason as the new problem statement. Allow changes to the surrounding parts. Never answer a rejection with small tweaks of the same options.

## Rules

| Rule | Why |
|---|---|
| Three by default; two for "both" (when they named both options, skip the bolder-option rule); exactly the number they ask for otherwise | The count is theirs; three is enough to compare without fatigue |
| Different axes, not different paint | Three layouts in three colour schemes is one idea with three skins |
| Always recommend, and say why | They asked an expert; "tell me which you like" hands the work back |
| "Current" sits on the board | People judge change against what they know |
| Same data, same size, same fidelity | A polished option next to sketches is a vote, not a choice |
| No straw men: every option is one you'd defend | Fake options waste the person's attention and trust |
| One option is deliberately bolder | Otherwise the set only covers safe variations |
| Real screens stay untouched until the pick | Options that leak into the product are decisions nobody made |

## Done when

The board shows the legend, Current and every option at equal fidelity; the recommendation is stated first; you have stopped for the pick. After the pick: applied to the real screens and the system, and the temporary area cleared.

## Common mistakes

| Thought | Reality |
|---|---|
| "Option C: the same page in a dark theme" | Theme is paint, not a direction. Change structure, interaction, density, emphasis or what's removed. |
| "I'll let them choose without biasing them" | Not recommending isn't neutral, it's unhelpful. Recommend first, with the reason. |
| "The original file is unchanged, so they can compare" | Put Current *on the board*, next to the options. |
| "They rejected all three, I'll adjust the closest one" | A rejection is new information about the problem. Restate it and diverge again. |
| "They asked for 5, but 3 is the method" | Give 5. The divergence rule still applies to all of them. |
| "Options share the same fixes, so they look alike" | Shared fixes are fine. Say so once in the legend and make the main axis differ. |
