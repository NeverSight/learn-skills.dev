---
name: magic-ui
description: |
  Add, customise or troubleshoot Magic UI's animated React components — marquee, globe,
  blur-fade, shiny-button, magic-card and the rest of the @magicui registry — in a
  Tailwind + shadcn project. Use for animated hero sections, testimonial walls, CTA bands
  and feature grids, or to replace hand-rolled animation code with a library component.
triggers:
  - "magic ui"
  - "animated component"
  - "animated hero section"
  - "marquee component"
das:
  type: skill
  category: visual-components
  upstream: "https://github.com/magicuidesign/magicui"
  upstream_path: "skills/magic-ui/SKILL.md"
  version: latest
---

# magic-ui

> Catalogue stub — full skill: [magicuidesign/magicui](https://github.com/magicuidesign/magicui)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/magic-ui/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/magic-ui/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `magic-ui`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/magic-ui ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add magicuidesign/magicui --skill magic-ui -g -y
   ```

   **Project:**
   ```bash
   npx skills add magicuidesign/magicui --skill magic-ui -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** Node.js and network access: components are installed through the shadcn CLI from the Magic UI registry, and shadcn must already be initialised in the project
- **License:** MIT
- **Download size:** ~82 MB.
<!-- das:install:end -->

## Invoke after install

- Skill name: `magic-ui`
- Trigger phrases: "magic ui", "animated component", "animated hero section"

## What it does

Picks and installs the right animated component from the Magic UI registry instead of hand-writing the effect. It starts from the UI outcome (section type, motion intensity, responsive behaviour), confirms the project is React/Next.js with Tailwind and an initialised shadcn, then installs by name:

```bash
npx shadcn@latest add @magicui/magic-card
```

Integration keeps the component's API intact — prop and className customisation over rewriting internals — and adds any extra dependencies or CSS keyframes the component needs. It finishes with a quality pass: semantic HTML and keyboard access, labels and text alternatives, mobile overflow, and a check that client-only wrappers and stacked high-motion effects haven't crept in. It bundles `references/components.md` (the component catalogue) and `references/recipes.md` (section-level compositions), and is the right entry point when a request sounds like "make this hero feel alive" rather than "draw this screen".

## When NOT to use

- Building or theming the component primitives themselves — `shadcn-ui` owns the registry, CLI and variant mechanics, and `building-components` owns the API design
- Static layout, typography or colour decisions that are not about motion (use `ui-ux-pro-max`, `baseline-ui`, or `color-expert`)
- Non-React stacks: every component here is a React/Tailwind registry entry, so a Vue or Svelte project needs its own library
- Motion that has to be art-directed as a timeline or film — that is `gsap-skills`, `scroll-world`, or `design-motion-principles`
