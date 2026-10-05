---
name: awesome-design
description: Provides real, analyzed design-token references (DESIGN.md files) for 74 well-known brands/products — Stripe, Linear, Vercel, Notion, Apple, Coinbase, Airbnb, Figma, and more — covering color palettes, typography hierarchy, component states, spacing/grid, shadows, and breakpoints. Use whenever the user wants a UI to visually match a specific existing brand or product ("make this look like Stripe", "give it that Linear feel", "Notion-style dashboard", "SaaS aesthetic like Vercel"), or asks what brand references are available. Requires a one-time local clone before first use — see setup section.
---

# Awesome Design: Brand Reference Library

A curated collection of `DESIGN.md` files — one per brand — each extracting that product's real design tokens: color palette + semantic roles, typography hierarchy, component stylings (buttons/cards/inputs/nav with states), spacing/grid, shadow/elevation system, responsive breakpoints, and do's/don'ts. Source: [voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md) (credit to VoltAgent — this skill just wraps it for easy install; the reference content and its license belong to that repo).

## One-time setup

If `${CLAUDE_PLUGIN_DATA}/awesome-design-md/` doesn't exist yet — the user asks to "set up awesome design," or a brand reference is needed and none has been cloned — clone it:

```
mkdir -p ${CLAUDE_PLUGIN_DATA}
git clone https://github.com/voltagent/awesome-design-md ${CLAUDE_PLUGIN_DATA}/awesome-design-md
```

Full clone (not shallow), so a later `git pull` in that directory picks up brands added upstream over time. This only needs to run once — it persists in the plugin's data directory across updates.

## Using a brand reference

1. Check `${CLAUDE_PLUGIN_DATA}/awesome-design-md/design-md/` for the requested brand's folder (lowercase, hyphenated — e.g. `design-md/stripe/DESIGN.md`).
2. If the exact brand isn't there, list the closest matches from the directory (e.g. similar category — fintech, dev tools, SaaS) and ask the user to pick one, or say plainly it isn't in the collection rather than guessing at tokens.
3. Read the brand's `DESIGN.md`, and `preview.html` / `preview-dark.html` if the user wants a visual reference, then apply its tokens — colors, type scale, component states, spacing, shadows, breakpoints — when building or redesigning the requested UI. Treat it as ground truth for "what does this brand's UI actually look like," not just a mood board.

## Full brand list

Read `${CLAUDE_PLUGIN_DATA}/awesome-design-md/README.md`'s Collection section, or list the `design-md/` directory directly. Run `git pull` in that directory first if the user is looking for a brand that might have been added since the initial clone.
