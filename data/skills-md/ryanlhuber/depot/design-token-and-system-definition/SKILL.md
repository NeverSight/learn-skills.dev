---
name: design-token-and-system-definition
description: "Defines named design decisions (color, type, spacing, shape, elevation, motion) and component rules, and checks designs against them. Use when establishing, consolidating, or auditing visual foundations for reuse and consistency."
---

# Design Token and System Definition

## Purpose
Define a consistent set of named design decisions (color, type, spacing, shape, elevation, motion) and component rules, and check designs against them.

## When to use
- Use when: establishing or consolidating visual foundations so decisions are reusable and consistent.
- Use when: auditing a design or build for deviations from an existing set of foundations.
- Do not use when: a single one-off visual decision is needed with no reuse.
- Pairs with: `design-token-implementation` puts the defined tokens into code.

## Inputs
- Required: the existing visual material or brand constraints, and the contexts the system must serve (platforms, themes, density, locales).
- Optional: accessibility targets, existing tokens or components, usage inventory, brand guidelines.
- Assumptions: unspecified values are proposed and marked as proposals.

## Process
1. Inventory the values in use (colors, sizes, spacing, radii, shadows, durations) and cluster near-duplicates.
2. Define a small scale for each category with a clear progression rule (for example a base unit and multipliers).
3. Name tokens by role or meaning (for example a surface, a text role, a state), not by raw value, so values can change without renaming.
4. Layer tokens: raw values, then semantic roles that reference them, then component-level overrides only where needed.
5. Define themes and variants (for example light and dark, density) as alternative value sets for the same semantic roles.
6. Verify each text and interactive pairing meets the target contrast and size requirements in every theme.
7. Specify component rules: which tokens a component uses, its states, spacing, and permitted variations.
8. Document usage guidance and the process for adding, changing, or retiring tokens.

## Rules and heuristics
- Required: foreground and background pairings meet the applicable accessibility contrast requirement in every theme.
- Required: semantic roles do not encode raw values in their names.
- Required: a token that duplicates another's value without distinct meaning is merged or justified.
- Recommended: prefer fewer, systematic scales over many one-off values.
- Visual choices not tied to a requirement are aesthetic preferences; label them.

## Checks
- Every used value maps to a token or is listed as an exception.
- Contrast and target-size checks are recorded per pairing and theme.
- No circular token references.
- Each token has a role description.

## Output
Return the token set with scales, semantic roles, theme mappings, contrast results, component rules, exceptions found, and a change process.

## Completion criteria
- Every in-scope value is tokenized or excepted with reason.
- Required accessibility pairings pass or failures are reported.
- Roles and usage guidance are documented.
