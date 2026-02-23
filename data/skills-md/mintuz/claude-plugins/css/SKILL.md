---
name: css
description: WHEN authoring CSS/styles/layout for web UI; outputs production-ready, accessible, maintainable CSS.
---

# CSS Best Practices

Production-grade CSS development with architectural principles, proper specificity management, and maintainable patterns.

## Core Principles

1. **Single Responsibility** - Each class handles one concern only
2. **Open/Closed** - Open for extension, closed for modification
3. **Immutable CSS** - Utilities and objects never change after creation
4. **Behavior over implementation** - Focus on what the code does, not how
5. **Accessibility first** - Semantic HTML before ARIA, proper contrast and sizing

## Quick Reference

| Topic                                                    | Guide                                                                   |
| -------------------------------------------------------- | ----------------------------------------------------------------------- |
| Specificity hierarchy, safe techniques, !important rules | [specificity.md](references/specificity.md)                             |
| rem vs px, margins, layout algorithms                    | [units-margins.md](references/units-margins.md)                         |
| @extend vs mixins, refactoring workflow, code smells     | [preprocessors-refactoring.md](references/preprocessors-refactoring.md) |
| Architectural principles and common code patterns        | [patterns.md](references/patterns.md)                                   |

## When to Use Each Guide

### Specificity

Use [specificity.md](references/specificity.md) when you need:

- Specificity hierarchy and calculations
- Safe techniques (self-chaining, attribute selectors)
- Anti-patterns (IDs, deep nesting, qualified selectors)
- !important rules (proactive vs reactive)
- Shorthand property gotchas
- Alternatives to reactive !important

### Units and Margins

Use [units-margins.md](references/units-margins.md) when you need:

- rem vs px decision framework
- Line-height best practices
- Margin encapsulation rules
- Single-direction margin patterns
- Margin collapse behavior
- Layout algorithm awareness (Flow, Flexbox, Grid)
- Common gotchas (z-index, magic space under images)

### Preprocessors and Refactoring

Use [preprocessors-refactoring.md](references/preprocessors-refactoring.md) when you need:

- @extend vs mixins guidance
- Avoiding & concatenation
- CSS @import performance issues
- Finding dead CSS with beacons
- The Three I's refactoring workflow
- Code smell reference tables

### Patterns

Use [patterns.md](references/patterns.md) when you need:

- Single Responsibility Principle examples
- Open/Closed Principle patterns
- Immutable CSS patterns and prefixes
- Component without margin examples
- Utility class patterns
- Self-chaining for specificity
- CSS custom properties for design scales

## Quick Reference: Decision Trees

### Should I use !important?

```
Is this a utility class that must be immutable?
├── Yes → Use !important (proactive)
└── No → Is there a specificity conflict?
    ├── Yes → Try: self-chain, attribute selector, or restructure cascade
    └── No → Don't use !important
```

### Should I use px or rem?

```
Should this scale with user font preferences?
├── Yes → Use rem
│   Examples: font-size, vertical text margins, media queries
└── No → Use px
    Examples: borders, box-shadows, horizontal padding
```

### Should I use shorthand?

```
Am I intentionally setting ALL related properties?
├── Yes → Shorthand is fine
└── No → Use longhand to avoid unintentional resets
```

### Should component have margin?

```
Is this a layout component (grid, stack, container)?
├── Yes → Margin/gap is appropriate
└── No → Move spacing to parent or use utility classes
```

### @extend or mixin?

```
Are these selectors thematically related (same component)?
├── Yes → @extend might be acceptable
└── No → Use mixin (safer, doesn't disrupt source order)
```

### How should I refactor this CSS?

```
Step 1: Identify - Is this frequently used and problematic?
├── Yes → Continue
└── No → Skip refactoring, focus elsewhere

Step 2: Isolate - Build new version separately
├── Use CodePen/jsFiddle
└── Don't build on top of existing CSS

Step 3: Implement - Reintegrate carefully
├── Component fixes → component's partial
└── Legacy conflicts → shame.css
```

## Summary Checklist

Before committing CSS, verify:

- [ ] Classes follow single responsibility (structure separate from cosmetics)
- [ ] No ID selectors for styling
- [ ] No reactive !important (only proactive for utilities)
- [ ] Components have no margin (spacing controlled by parent)
- [ ] Using rem for font-size and scalable spacing
- [ ] Using px for borders, shadows, and fixed visual elements
- [ ] Longhand properties when only setting one value
- [ ] No deep nesting (4+ levels)
- [ ] No qualified selectors (e.g., `ul.nav`)
- [ ] Layout algorithm appropriate for context (Flow, Flex, Grid)
- [ ] Accessible color contrast ratios
- [ ] Semantic HTML before adding ARIA
