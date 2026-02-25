---
name: icon-design
description: |
  Select semantically appropriate icons for websites using Lucide, Heroicons, or Phosphor. Covers concept-to-icon mapping, React/HTML templates, and tree-shaking patterns.

  Use when: building feature sections, service grids, contact info, navigation, or any UI needing icons. Prevents emoji usage, ensures consistency.
license: MIT
metadata:
  author: oakoss
  version: '1.1'
---

# Icon Design

Select the right icon for the job. Maps concepts to icons across three modern libraries, provides ready-to-use templates, and prevents common mistakes like broken tree-shaking and inconsistent styles.

## Quick Reference

| Concept        | Lucide          | Heroicons                | Phosphor          |
| -------------- | --------------- | ------------------------ | ----------------- |
| Award/Quality  | `Trophy`        | `trophy`                 | `Trophy`          |
| Price/Value    | `Tag`           | `tag`                    | `Tag`             |
| Location       | `MapPin`        | `map-pin`                | `MapPin`          |
| Expertise      | `GraduationCap` | `academic-cap`           | `GraduationCap`   |
| Support        | `MessageCircle` | `chat-bubble-left-right` | `ChatCircle`      |
| Security       | `Shield`        | `shield-check`           | `Shield`          |
| Speed          | `Zap`           | `bolt`                   | `Lightning`       |
| Phone          | `Phone`         | `phone`                  | `Phone`           |
| Email          | `Mail`          | `envelope`               | `Envelope`        |
| User/Profile   | `User`          | `user`                   | `User`            |
| Team           | `Users`         | `user-group`             | `Users`           |
| Settings       | `Settings`      | `cog-6-tooth`            | `Gear`            |
| Home           | `Home`          | `home`                   | `House`           |
| Search         | `Search`        | `magnifying-glass`       | `MagnifyingGlass` |
| Check/Success  | `Check`         | `check`                  | `Check`           |
| Close/Cancel   | `X`             | `x-mark`                 | `X`               |
| Menu           | `Menu`          | `bars-3`                 | `List`            |
| Calendar       | `Calendar`      | `calendar`               | `Calendar`        |
| Clock/Time     | `Clock`         | `clock`                  | `Clock`           |
| Heart/Favorite | `Heart`         | `heart`                  | `Heart`           |

## Library Selection

| Library       | Best For                         | Package                 |
| ------------- | -------------------------------- | ----------------------- |
| **Lucide**    | General use, React projects      | `lucide-react`          |
| **Heroicons** | Tailwind projects, minimal style | `@heroicons/react`      |
| **Phosphor**  | Weight variations needed         | `@phosphor-icons/react` |

Default recommendation: Lucide (1,600+ icons, excellent React integration, dynamic loading via `lucide-react/dynamic`).

## Selection Process

1. **Identify the concept** -- what does the label/title communicate?
2. **Check semantic mapping** -- see `references/semantic-mapping.md`
3. **Choose library** -- Lucide (default), Heroicons (Tailwind), Phosphor (weights)
4. **Apply template** -- see `references/icon-templates.md`
5. **Verify consistency** -- same style, same size within each section

## Icon Style Rules

| Rule              | Detail                                                                |
| ----------------- | --------------------------------------------------------------------- |
| No mixed styles   | Use all outline OR all solid in a section                             |
| No emoji          | Use proper icon components (tree-shakeable)                           |
| Use currentColor  | Icons inherit text color via `stroke="currentColor"`                  |
| Semantic colors   | Use `text-primary`, not `text-blue-500`                               |
| Consistent sizing | Inline `w-4 h-4`, cards `w-8 h-8`, hero `w-10 h-10`                   |
| Tree-shaking safe | Use explicit named imports and icon maps, never `import *`            |
| Accessibility     | Add `aria-hidden="true"` to decorative icons, `aria-label` to buttons |

## Common Mistakes

| Mistake                                                            | Correct Pattern                                                                  |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Importing all icons with `import * as Icons` breaking tree-shaking | Use explicit named imports and a static icon map                                 |
| Mixing outline and solid icon styles within the same section       | Pick one style per section and apply consistently                                |
| Using emoji instead of proper icon components                      | Always use tree-shakeable icon components from Lucide, Heroicons, or Phosphor    |
| Hardcoding color values like `text-blue-500` on icons              | Use semantic colors like `text-primary` so icons inherit theme changes           |
| Choosing icons by visual appeal rather than semantic meaning       | Map the concept first using the semantic mapping reference, then select the icon |
| Missing `aria-label` on icon-only buttons                          | Add `aria-label="Description"` to buttons containing only icons                  |
| Using old Heroicons import paths without size prefix               | Use `@heroicons/react/24/outline` with the size prefix                           |

## Delegation

- **Audit existing icon usage for consistency and tree-shaking issues**: Use `Explore` agent to scan imports and identify mixed styles or wildcard imports
- **Migrate icons from Font Awesome or Material to modern libraries**: Use `Task` agent with the migration guide reference
- **Plan icon system architecture for a design system**: Use `Plan` agent to select library, define sizing conventions, and establish semantic mappings

## References

- [semantic-mapping.md](references/semantic-mapping.md) -- Full concept-to-icon tables by category (quality, price, location, trade-specific, navigation, status)
- [icon-templates.md](references/icon-templates.md) -- React/HTML patterns with Tailwind (feature cards, buttons, inputs, navigation, status badges)
- [library-comparison.md](references/library-comparison.md) -- Lucide vs Heroicons vs Phosphor (features, bundle size, import patterns)
- [migration-guide.md](references/migration-guide.md) -- Font Awesome, Material Icons, Feather, and emoji to modern equivalents
- [accessibility.md](references/accessibility.md) -- Decorative vs meaningful icons, aria attributes, screen reader patterns
