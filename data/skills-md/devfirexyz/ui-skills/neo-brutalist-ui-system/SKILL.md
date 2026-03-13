---
name: neo-brutalist-ui-system
description: Apply a reusable neo-brutalist design system to existing or new frontend projects (landing, marketing, portfolio, dashboard, app surfaces) using strong typography, tokenized theming, and variant-driven component primitives. Preserve existing information architecture unless restructuring is explicitly requested.
---

# Neo-Brutalist UI Design System Skill

Use this skill when users ask for bold, high-contrast UI refactors, reusable design systems, or full-page styling upgrades.

This skill is design-system-first, not template-first.
- Default behavior: preserve existing layout and content architecture.
- Rebuild layouts only when explicitly requested.

## Core Principles

- Typography drives hierarchy more than decoration.
- Strong structure: `2px` borders, explicit separators, deliberate spacing.
- Hard-edged surfaces: square corners by default on primary UI.
- Direct interactions: translate + shadow reduction for active states.
- Tokenize everything important (background/surface/text/border/accent/shadow).
- Reuse existing app theme when present; generate missing tokens only.

## Design DNA Extraction (Required First Step)

Before editing, extract project design DNA from codebase:

1. Global styling source
- find global CSS/theme entry (`app.css`, `globals.css`, `theme.css`).
- collect color variables, font declarations, theme toggling strategy.

2. Typography roles
- identify display/headline font, body font, technical/mono font, optional accent font.
- map where each role is used (hero, nav, cards, metadata, captions).

3. Primitive inventory
- locate core UI primitives (button, card, input, textarea, dialog, dropdown, tabs, tooltip, progress, avatar, separators).
- detect variant API style (`cva`, prop variants, class maps).

4. Layout rhythm
- identify section cadence (bordered slices, alternating surfaces, grid separators, CTA blocks).
- identify motion style (hover transitions, reveal animations, duration patterns).

5. Constraints
- preserve information architecture unless user asks for restructure.
- preserve brand tone and color intent unless user asks to rebrand.

## Scope Modes

- `component-only`: update tokens and primitive components only.
- `layout-preserving` (default): restyle existing pages, keep same sections/content flow.
- `layout-rebuild`: redesign section architecture (explicit user request required).

## Reference Pattern Library (Derived from Lawn, Applied Generically)

### Typography System
- Display/headlines:
  - very high weight (`800-900`)
  - tight tracking
  - uppercase for key headings/CTAs where tone supports it
- Body/support copy:
  - cleaner medium/regular weight
  - reduced contrast tone for secondary text
- Technical/meta text:
  - monospaced role for timestamps, metrics, status labels
- Optional accent typography:
  - serif or stylistic contrast font for specific emphasis only (not everywhere)

### Token Model
Prefer this token family so output works across page types:
- `--background`, `--background-alt`
- `--surface`, `--surface-alt`, `--surface-strong`, `--surface-muted`
- `--foreground`, `--foreground-muted`, `--foreground-subtle`, `--foreground-inverse`
- `--border`, `--border-subtle`
- `--accent`, `--accent-hover`, `--accent-light`
- `--shadow-color`, `--shadow-accent`
- semantic tokens: `--destructive`, `--success`, `--warning`

### Theme Behavior
- Support both light and dark token sets when the project already supports them.
- Use `data-theme` switching for deterministic theme control where possible.
- If project already persists theme state (local storage or framework state), preserve that flow.
- Do not force dark mode redesigns on light-first products unless requested.

### Primitive Patterns
- Buttons:
  - bold label, often uppercase
  - `border-2`
  - hard shadow
  - hover/active translate by `1-2px`
- Cards:
  - strong border + structured internal header/content/footer spacing
  - title emphasis via weight/tracking, not ornament
- Inputs/Textareas:
  - hard-edged, border-forward, clear focus border/shadow
  - mono/meta-friendly when context is technical
- Overlay components (dialog/dropdown/tooltip):
  - maintain Radix accessibility behavior
  - apply same border/shadow vocabulary as core surfaces
- Data components (tabs/progress/badges):
  - high-legibility state contrast
  - avoid soft/ambiguous state styling
- Exception rule:
  - circular avatars are allowed when functionally expected.

### Layout Patterns
Apply across landing/marketing/portfolio/dashboard:
- Section rhythm via border dividers and controlled spacing blocks.
- Grid separators (`divide-x`/`divide-y` or explicit borders) for feature/data matrices.
- Contrast bands (light vs dark or muted vs strong surfaces) to define narrative steps.
- CTA zones with the strongest type/contrast, not necessarily the loudest color.
- Dashboard/application screens prioritize utility clarity over marketing theatrics.

### Motion Patterns
- Use fast, explicit transitions (`120-200ms`) for hover/active state changes.
- Use 1-2 meaningful entrance/reveal patterns max.
- Avoid decorative animation noise that does not improve hierarchy or feedback.

## Workflow

### 1. Choose Intent + Scope
- Define one-line aesthetic intent (example: "industrial editorial", "clean blocky utility").
- Choose scope mode (default `layout-preserving`).

### 2. Establish/Map Tokens
- If project already has tokens: map to the token model above and keep naming conventions.
- If project lacks tokens: generate with script, then integrate.

Script:
`python3 scripts/generate_blocky_palette.py --base "<hex>" --accent "<hex>" --format both`

### 3. Refactor Primitives First
- Update primitives before page-level classes.
- Prefer variant APIs over one-off per-page styles.
- Keep class composition consistent (`cva` + shared util) when stack supports it.

### 4. Apply to Layouts
- `layout-preserving`: restyle existing sections without changing narrative/order.
- `layout-rebuild`: propose new architecture first, then implement after alignment.
- For dashboards/apps: emphasize information density control and scanability.
- For landing/marketing/portfolio: emphasize hierarchy and narrative rhythm.

### 5. QA Pass
- Responsiveness: no broken borders/overlaps at mobile/tablet/desktop.
- Contrast: readable foreground/background across light and dark contexts.
- Interaction: focus-visible states are clear; hover/active states remain intentional.
- Consistency: primitives and page sections use same token/shadow/border language.

## Output Contract

Return:
- Design DNA summary (fonts, token map, primitive inventory, layout rhythm found).
- Changes implemented (primitives and/or layouts) with preserved vs rebuilt statement.
- Token block updates (or mapping strategy when existing theme is reused).
- Short rationale on hierarchy, readability, and interaction clarity.

## Script Usage After Install

When installed, the script is bundled in this skill:
- Agent run pattern:
  - `python3 scripts/generate_blocky_palette.py --base "<hex>" --accent "<hex>" --format both`
- Manual run pattern:
  - `cd <installed-skill-path>/neo-brutalist-ui-system`
  - `python3 scripts/generate_blocky_palette.py --base "#f2f1eb" --accent "#2f5f3a" --format both`

Use script output as source-of-truth tokens, then map into project naming if needed.

## Example Prompts

- "Use `$neo-brutalist-ui-system` in `layout-preserving` mode; keep my current sections and apply a full design-system refactor."
- "Use `$neo-brutalist-ui-system` in `component-only` mode and standardize button/card/input/dialog/dropdown/tabs to one tokenized style."
- "Use `$neo-brutalist-ui-system` for my dashboard; keep the current IA, improve scanability, typography hierarchy, and interaction clarity."
