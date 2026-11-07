---
name: designing-ui
description: As long as you are doing UI / style-related work, you should load this skill
---

## Design Principles

### 1. Icons Are the Text

Use icons boldly — they are the most expressive way to communicate button and UI purpose at a glance.

- Prefer **icon + text** compositions over text alone
- In compact or icon-heavy UIs, icons can fully replace text labels
- Choose icons that semantically match the action, not just aesthetically

### 2. Stick to the Theme Color

Reuse the theme color already established in the project. Do not introduce new colors arbitrarily.

- Most projects use black / white and a gray-family palette: `slate`, `gray`, `zinc`, `neutral`, `stone`, `taupe`
- For greenfield projects, default to **slate** or **stone**
- Reserve colorful, bright accents for the **index / hero section** — not the everyday working UI the user stares at for hours

### 3. Use Opacity Instead of Hardcoded Colors

Prefer opacity-based color expressions over hardcoded hex/rgb values.

- `bg-black/10` reads more clearly than `bg-[#1a1a1a]`
- Interactive states (hover, focus, active) should use **opacity shifts or subtle translation**, not color swaps
- This keeps the palette coherent and reduces the number of color tokens

### 4. Flat UI with Borders Only

Default to a flat, border-defined layout. Avoid decorative depth unless explicitly requested.

- No heavy box shadows
- No gradient backgrounds on components
- No background animations on interactive elements
- Borders (`border`, `divide-*`, `ring`) are the primary structural tool

### 5. Typography: Load the Right Font for the Context

- For **hero / landing sections**: load an expressive or display font freely — don't default to system fonts
- For **application UI**: prefer a clean **sans-serif** (Inter, Geist, etc.)
- Avoid mixing more than two font families in one view
