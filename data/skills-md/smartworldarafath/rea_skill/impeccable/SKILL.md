---
name: impeccable
description: Design vocabulary and quality enforcement system for AI coding agents. Use to steer design with commands like polish, bolder, quieter, critique, and audit — catching AI slop before it ships. Features 24 commands including live iteration, scored UX reviews, technical quality audits, and accessibility/performance hardening. Works with Claude Code, Cursor, Codex, Gemini CLI, Grok Build, Google Antigravity, and 10+ other coding agents.
---

# Impeccable

The design vocabulary for your coding agent. Steer with `polish` and `bolder`, review with `critique` and `audit`, and catch AI slop before it ships.

## Installation

```bash
npx impeccable install
```

Reload your coding tool, then run `/impeccable init` in your agent (`$impeccable init` on Codex).

## How it works

Run `/impeccable init` once per project. It reads your code, asks only what it can't infer (who the product is for, what it needs to do, the constraints), and writes `PRODUCT.md`. Every later command reads it. Run `/impeccable document` to capture your existing visual system in `DESIGN.md`, so changes stay on-brand.

Then name a command and a target:

```
/impeccable critique the onboarding flow
/impeccable quieter the landing page
/impeccable polish settings
/impeccable harden checkout
```

## 24 Commands

| Category | Commands |
|---|---|
| **Steer** | `bolder` amplifies safe designs · `quieter` tones down loud ones · `distill` removes what the page doesn't need · `colorize` brings color to a gray interface · `typeset` fixes fonts, hierarchy, and sizing · `layout` fixes spacing and rhythm · `animate` adds transitions and interaction feedback · `delight` adds personality · `overdrive` goes for shaders, spring physics, and scroll-driven effects |
| **Review** | `critique` is a scored UX review · `audit` is a technical quality report |
| **Finish** | `polish` is the final pass before shipping · `harden` covers errors, i18n, overflow, and edge cases · `clarify` rewrites unclear copy · `adapt` handles screen sizes and devices · `optimize` fixes loading and rendering performance · `onboard` designs first-run flows and empty states |
| **Iterate live** | `live` lets you pick an element in the browser and cycle through variants · `generate` produces variants of a named element without manual picking |
| **Plan and set up** | `shape` plans UX before code · `init` writes `PRODUCT.md` · `document` writes `DESIGN.md` · `extract` pulls repeated patterns into your design system |

## Slop Detection

62 deterministic rules flag tells like:
- Generic fonts (Inter for everything, purple-to-blue gradients)
- Cards nested in cards with gray text on colored backgrounds
- Rounded-square icon tiles above every heading
- Cramped padding and skipped headings
- Quality problems detectable without an LLM or API key

## Usage

```
/impeccable critique the pricing cards
/impeccable bolder the hero section
/impeccable audit
/impeccable polish
```

## Reference

- **Website:** [impeccable.style](https://impeccable.style)
- **Docs:** [impeccable.style/docs](https://impeccable.style/docs)
- **Source:** [github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable)
