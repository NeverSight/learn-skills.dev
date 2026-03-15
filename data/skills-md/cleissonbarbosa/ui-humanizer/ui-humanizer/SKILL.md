---
name: ui-humanizer
description: |
  Transform AI-generated web UI into authentic, professional interfaces with human
  character. Use when reviewing or refactoring frontend code that looks generic,
  template-driven, or "AI-generated". Triggers on: "humanize UI", "fix generic
  design", "make UI look professional", "remove AI look from interface",
  "add personality to UI", "de-templatize design", "authentic design".
  Applies the 5-Layer Authenticity Stack to detect and fix visual, interaction,
  layout, copy, and UX red flags in HTML/CSS/JS/React/Vue/Svelte code.
license: MIT
metadata:
  authors: "Cleisson Barbosa"
  version: "1.0.0"
---

# UI Humanizer

Transform generic, template-driven interfaces into authentic, professional designs that feel crafted by humans. Based on the 5-Layer Authenticity Stack methodology.

## When to Use

- After generating UI with AI tools (Copilot, v0, Bolt, etc.)
- When a design "feels generic" but you can't pinpoint why
- During design review of frontend components
- When refactoring a prototype into production UI
- When adding brand personality to a white-label template

## Before Starting

1. Read all target files before making any changes.
2. Identify the framework in use (React, Vue, Svelte, plain HTML/CSS, etc.).
3. Check whether a design system or token file already exists in the project.
4. Confirm the scope: full page, single component, or set of components.

## Procedure

### Phase 1: Detect AI Red Flags

Read the target files, then scan for these telltale signs of AI-generated UI:

| Category        | What to look for                                                                                                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Visual**      | Overly perfect gradients, trending color combos (indigo-purple, blue-cyan), identical cards, uniform spacing, uncurated icon sets, same border-radius everywhere, no visual hierarchy |
| **Interaction** | Zero micro-interactions, generic hover (`opacity: 0.8`), bare spinners, no transitions on state changes, empty states that say "No data"                                              |
| **Code smells** | Same spacing value repeated (`p-4 gap-4 m-4`), no design tokens or semantic colors, inconsistent inline styles vs utilities, no responsive adjustments, no clear type scale           |

Report findings organized by severity: **Critical** (breaks professionalism), **Major** (feels generic), **Minor** (missed polish opportunity).

For the full checklist of red flags with examples, read [references/red-flags.md](./references/red-flags.md).

---

### Phase 2: Apply the 5-Layer Authenticity Stack

Work through each layer sequentially on the flagged components. Read the detailed reference for each layer on demand.

**Layer 1 — Visual Identity:** Replace generic palette with semantic color tokens, establish type scale, create spacing and border-radius hierarchies.
→ Read [references/layer-1-visual-identity.md](./references/layer-1-visual-identity.md)

**Layer 2 — Micro-Interactions:** Add purposeful motion that provides feedback and personality (hover lift, focus rings, skeleton loading, contextual loading messages).
→ Read [references/layer-2-micro-interactions.md](./references/layer-2-micro-interactions.md)

**Layer 3 — Layout Intelligence:** Break out of uniform grids with bento layouts, progressive disclosure, content-driven breakpoints, and intentional whitespace.
→ Read [references/layer-3-layout-intelligence.md](./references/layer-3-layout-intelligence.md)

**Layer 4 — Copy Personality:** Rewrite robotic UI text so empty states, errors, loading, and onboarding sound like a person wrote them.
→ Read [references/layer-4-copy-personality.md](./references/layer-4-copy-personality.md)

**Layer 5 — UX Architecture:** Evaluate emotional context, workflow fit, accessibility coverage, and brand personality alignment.
→ Read [references/layer-5-ux-architecture.md](./references/layer-5-ux-architecture.md)

For the full methodology, design tokens, and rationale, read [references/authenticity-stack.md](./references/authenticity-stack.md).

---

### Phase 3: Implement Changes

1. Start with the highest-severity flags from Phase 1.
2. Edit one component at a time — do not refactor everything at once.
3. Preserve existing functionality — only change presentation and interaction.
4. Apply changes in this order: tokens/variables → typography → spacing → colors → interactions → copy.
5. Test after each layer — visually verify changes do not break layout.

---

### Phase 4: Polish Checklist

Before marking complete, verify:

- [ ] Semantic color tokens instead of raw color values
- [ ] Clear typography scale with visual hierarchy
- [ ] Intentional whitespace with visible rhythm (no uniform spacing anti-pattern)
- [ ] Consistent border-radius hierarchy across components
- [ ] At least 3 distinct micro-interactions (hover, focus, loading/empty state)
- [ ] Focus states visible and branded
- [ ] Human-sounding copy on empty states, errors, and loading
- [ ] Custom or curated icon set (not raw default library dump)
- [ ] Accessibility: contrast ratios pass (4.5:1 text, 3:1 large text/UI), keyboard navigation works
- [ ] `prefers-reduced-motion` respected where animations are added

---

## Rules & Constraints

- Never change functionality or business logic — only presentation and interaction.
- Preserve all existing class names, IDs, and data attributes that other code may depend on.
- If a design system already exists in the project, extend it instead of replacing it.
- Respect the framework's idioms (e.g., use `className` in React, `class:` in Svelte).
- Always check accessibility: contrast, keyboard nav, screen reader labels.
- Do not add external dependencies without confirming with the user.

## Output Format

After completing the humanization, provide a summary:

```
## UI Humanization Report

### Red Flags Found
- [severity] description → fix applied

### Layers Applied
1. Visual Identity: [changes made]
2. Micro-Interactions: [changes made]
3. Layout Intelligence: [changes made]
4. Copy Personality: [changes made]
5. UX Architecture: [changes made]

### Before/After
[key visual differences]

### Remaining Opportunities
[optional polish items for future iteration]
```
