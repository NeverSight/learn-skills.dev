---
name: design-systems-architecture
description: "Design system architecture: W3C design tokens, Style Dictionary pipelines, component library structure, theming, multi-brand token tiers, governance, versioning, and maturity models. Use when starting or scaling a design system, generating tokens, or setting up design-to-code distribution."
---

# Design Systems Architecture — Systematic Design at Scale

## Design System Philosophy

"A design system is not a project. It is a product serving products." — Nathan Curtis

A design system is the single source of truth for how a product family looks, behaves, and communicates. It exists to multiply design and development efficiency while ensuring consistency across teams, platforms, and time. The system must be opinionated enough to ensure coherence yet flexible enough to serve diverse product needs.

### Core Principles

1. **Systematic over stylistic** — define rules and relationships, not just visual recipes
2. **Tokens are the foundation** — design decisions encoded as data, not hardcoded values
3. **Composition over inheritance** — build complex components from simple, composable primitives
4. **Document the why** — every decision needs rationale to prevent future erosion
5. **Adopt, then adapt** — products adopt the system by default, request exceptions with justification

## Design Token Architecture (W3C Design Tokens Standard)

### Token Hierarchy

**Tier 1: Global/Primitive Tokens (Raw Values)**
Define the complete value palette — all available options.

```json
{
  "color": {
    "blue": {
      "50":  { "$value": "#eff6ff" },
      "100": { "$value": "#dbeafe" },
      "500": { "$value": "#3b82f6" },
      "900": { "$value": "#1e3a5a" }
    },
    "neutral": {
      "0":   { "$value": "#ffffff" },
      "50":  { "$value": "#fafafa" },
      "900": { "$value": "#171717" }
    }
  },
  "spacing": {
    "1": { "$value": "4px" },
    "2": { "$value": "8px" },
    "4": { "$value": "16px" },
    "8": { "$value": "32px" }
  }
}
```

**Tier 2: Semantic/Alias Tokens (Contextual Meaning)**
Map raw values to design intent — what the value means.

```json
{
  "color": {
    "bg": {
      "primary":   { "$value": "{color.neutral.0}" },
      "secondary": { "$value": "{color.neutral.50}" },
      "inverse":   { "$value": "{color.neutral.900}" }
    },
    "text": {
      "primary":   { "$value": "{color.neutral.900}" },
      "secondary": { "$value": "{color.neutral.500}" },
      "brand":     { "$value": "{color.blue.500}" }
    },
    "action": {
      "primary":   { "$value": "{color.blue.500}" },
      "primary-hover": { "$value": "{color.blue.600}" }
    }
  }
}
```

**Tier 3: Component Tokens (Specific Application)**
Map semantic tokens to component properties — where the value is used.

```json
{
  "button": {
    "primary": {
      "bg":    { "$value": "{color.action.primary}" },
      "text":  { "$value": "{color.neutral.0}" },
      "hover-bg": { "$value": "{color.action.primary-hover}" },
      "padding-x": { "$value": "{spacing.4}" },
      "padding-y": { "$value": "{spacing.2}" },
      "border-radius": { "$value": "{radius.md}" }
    }
  }
}
```

### W3C Design Token Format (DTCG)

Follow the W3C Design Tokens Community Group specification:
- Use `$value` for token values
- Use `$type` to specify value type (color, dimension, fontFamily, fontWeight, duration, cubicBezier, shadow)
- Use `$description` for documentation
- Use `{}` syntax for references/aliases
- File extension: `.tokens.json`

### Token Categories

| Category | Examples | Type |
|----------|----------|------|
| Color | Brand, semantic, surface, text, border | color |
| Spacing | Padding, margin, gap | dimension |
| Typography | Font family, size, weight, line height, letter spacing | mixed |
| Border Radius | Corner rounding per component type | dimension |
| Elevation/Shadow | Box shadow definitions per level | shadow |
| Duration | Animation timing | duration |
| Easing | Animation curves | cubicBezier |
| Sizing | Icon, avatar, touch target sizes | dimension |
| Opacity | Disabled state, overlay, hover | number |
| Z-index | Layering order | number |

## Component Library Architecture

### Component Anatomy

Every component has a defined structure:

```
Component
├── Props/API (inputs and configuration)
├── Variants (visual and behavioral variations)
├── States (default, hover, active, focused, disabled, loading, error)
├── Slots/Children (composition points for custom content)
├── Tokens (design token bindings)
├── Accessibility (ARIA, keyboard, screen reader behavior)
└── Documentation (usage guidelines, do/don't examples)
```

### Component Maturity Model

**Level 1 — Defined:** Designed in Figma, documented in guidelines
**Level 2 — Implemented:** Coded in component library, props API defined
**Level 3 — Tested:** Unit tests, visual regression tests, accessibility tests pass
**Level 4 — Documented:** Usage guidelines, API docs, examples, do/don't
**Level 5 — Governed:** Change process established, versioning, deprecation path

### Component API Design Principles

- **Predictable props naming:** Use consistent naming conventions across all components (`size`, `variant`, `disabled`, `className`)
- **Enum over boolean:** `variant="primary" | "secondary" | "ghost"` not `isPrimary`, `isSecondary`
- **Composition over configuration:** `<Card><CardHeader /><CardBody /></Card>` not `<Card header={} body={} />`
- **Sensible defaults:** Components work without props; customization is additive
- **Type safety:** Full TypeScript types for all props; no `any` types in public API
- **Forward refs:** All components forward refs for imperative access
- **Polymorphic rendering:** Support `as` prop for semantic HTML flexibility (`<Button as="a" href="..." />`)

## Theming Architecture

### Theme Structure

```json
{
  "theme": {
    "light": {
      "color.bg.primary": "#ffffff",
      "color.bg.secondary": "#f5f5f5",
      "color.text.primary": "#171717",
      "color.text.secondary": "#737373",
      "color.action.primary": "#3b82f6"
    },
    "dark": {
      "color.bg.primary": "#171717",
      "color.bg.secondary": "#262626",
      "color.text.primary": "#f5f5f5",
      "color.text.secondary": "#a3a3a3",
      "color.action.primary": "#60a5fa"
    }
  }
}
```

### Theming Implementation

- Use CSS custom properties (variables) as the runtime theming mechanism
- Apply theme by swapping custom property values at the root level
- Support system preference detection (`prefers-color-scheme`)
- Allow manual override with persistent user preference
- Component tokens reference semantic tokens, which resolve to theme-specific values

### Multi-Brand Architecture

For organizations with multiple brands sharing a system:

- **Shared foundation:** Common component behavior, interaction patterns, accessibility
- **Brand tokens:** Each brand provides its own token set (colors, typography, spacing variations)
- **Component override layer:** Brand-specific component customizations when tokens alone are insufficient
- **Theme matrix:** Brand x Mode (e.g., BrandA-Light, BrandA-Dark, BrandB-Light, BrandB-Dark)

## Governance and Scaling

### Contribution Model

**Centralized:** Core team owns and builds all components
- Pros: High consistency, quality control
- Cons: Bottleneck, slow to address product-specific needs
- Best for: Small-medium organizations, early system maturity

**Federated:** Product teams contribute with core team review
- Pros: Faster growth, diverse input, shared ownership
- Cons: Consistency risk, review overhead
- Best for: Large organizations, mature systems

**Hybrid (recommended):** Core team owns primitives and governance; product teams contribute domain-specific patterns
- Core components (Button, Input, Card): centrally owned
- Domain components (DataGrid, FileUploader): contributed by domain teams, reviewed by core

### Change Management Process

1. **Proposal:** RFC (Request for Comment) with use case, design, and API proposal
2. **Review:** Design review + code review + accessibility review
3. **Build:** Implementation with full test coverage
4. **Document:** Usage guidelines, migration guide if breaking
5. **Release:** Semantic versioning, changelog, migration support

### Versioning Strategy

- Follow **Semantic Versioning (SemVer):** MAJOR.MINOR.PATCH
- **MAJOR:** Breaking changes to component API or visual appearance
- **MINOR:** New components, new props, backward-compatible enhancements
- **PATCH:** Bug fixes, accessibility improvements, documentation updates
- **Deprecation:** Mark deprecated with console warnings; maintain for 2 major versions
- **Changelogs:** Automated from conventional commits; include migration guidance

## Design-to-Code Integration

### Figma-to-Code Synchronization

- Figma component naming must match code component naming exactly
- Figma variants map to code component props
- Design tokens sync bidirectionally: Figma to tokens.json to code
- Use Token Studio (Figma plugin) for token management in design
- Automate token export with CI/CD pipeline (Style Dictionary, Token Transformer)

### Code Generation

- Generate CSS/SCSS from design tokens using Style Dictionary
- Platform-specific output: CSS variables, iOS Swift constants, Android XML resources, React Native styles
- Generate TypeScript types from token schema
- Visual regression testing: compare Figma designs with rendered components

## Routing

For **running a system as a product** — team models, the contribution workflow,
the RFC template (motivation, detailed design, alternatives, migration,
unresolved questions), and scaling: read `references/governance-scaling.md`.

For **token architecture** — the three-tier model, W3C DTCG naming, and the 2025
spec update: read `references/design-token-architecture.md`.

For **maturity and multi-brand** — the five-level model with team size, tooling,
governance and promotion criteria per level, multi-brand token layering,
white-label patterns, migration strategies and ROI measurement: read
`references/maturity-model-multi-brand.md`.

For **the token spec in implementation form**: read
`references/design-token-implementation.md` and
`references/token-specification-guide.md`.

## Cross-Referencing

- For visual design principles, reference `ui-visual-design-system`
- For accessibility component requirements, reference `accessibility-inclusive-design`
- For motion tokens and animation, reference `interaction-motion-design`
- For mobile component adaptations, reference `mobile-ux-design`

## v3.0 Cross-References

The v3.0 upgrade introduces references that extend design system architecture into Figma MCP pipelines, maturity modeling, and modern CSS integration.

**Figma MCP Design-to-Code Pipeline**
See `figma-design-tool-workflows/references/figma-mcp-ai-flywheel.md` for the Figma Model Context Protocol (MCP) server integration that enables AI-driven design-to-code workflows. This reference covers the MCP-powered flywheel where AI agents read Figma components, extract design tokens, generate production code, and validate output against the source design — creating a continuous synchronization loop between design and development that supersedes manual handoff processes.

**Design System Maturity Model and Multi-Brand Token Architecture**
See `references/maturity-model-multi-brand.md` for the comprehensive 5-level design system maturity model (from Ad Hoc through Optimized), multi-brand token architecture patterns for organizations operating multiple product brands from a shared foundation, and the W3C Design Tokens 2025.10 `$extensions` specification. The `$extensions` property enables vendor-specific metadata (Figma constraints, platform overrides, deprecation flags) within standard token files, which is critical for tooling interoperability in mature multi-brand systems. This reference expands significantly on the Multi-Brand Architecture and Component Maturity Model sections above.

**CSS @layer Integration with Token Architecture**
See `component-patterns-code/references/css-modern-patterns.md` for modern CSS `@layer` usage in design system token architecture. Cascade layers (`@layer reset, tokens, components, utilities, overrides`) provide deterministic specificity management for design systems at scale — eliminating the specificity wars that plague large component libraries. This reference covers how design tokens map to CSS custom properties within a layered cascade, enabling clean component-level theming without `!important` hacks or excessive nesting.

**Token Implementation Deep-Dive**
See `references/design-token-implementation.md` for end-to-end token implementation: aliasing and referencing syntax, multi-theme architecture, the transformation pipeline, platform-specific outputs (web, iOS, Android), Figma integration, token documentation, versioning and migration strategy, governance, performance considerations, and token testing. Use it alongside `references/token-specification-guide.md`, which covers the W3C DTCG format and Style Dictionary configuration in spec detail.

## Key Sources

- Curtis, N. "Design Systems" and Modular Web Design
- W3C Design Tokens Community Group specification
- Figma design systems documentation
- Material Design component guidelines
- Brad Frost "Atomic Design" methodology
