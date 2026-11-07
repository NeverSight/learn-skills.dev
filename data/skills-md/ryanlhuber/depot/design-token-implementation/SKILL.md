---
name: design-token-implementation
description: "Turns defined design decisions into a token structure in code: one source of values, layering, theming, naming, a migration from raw values, and a repeatable check that components use tokens. Use when design tokens must be implemented, migrated to, or audited in a codebase."
---

# Design Token Implementation

## Purpose
Implement already-decided design tokens in code so components use named values from one source, themes switch in one place, and drift back to raw values can be detected.

## When to use
- Use when: token definitions exist and a codebase must adopt them, or an existing token implementation must be restructured.
- Use when: auditing styles for raw values that bypass tokens.
- Do not use when: the token roles and values are still undecided. Settle them first; this work implements decisions and does not make them.
- Pairs with: `design-token-and-system-definition` decides the roles and values; use it first when they are undecided.

## Inputs
- Required: the token definitions (names or roles, values per theme) or the design source that holds them, and the codebase's current styling approach and where its styles live.
- Optional: an inventory of hard-coded values, supported themes and density modes, browser support, contrast targets, build constraints.
- Assumptions: a value or theme that is missing from the definitions is reported as a gap and never invented.

## Process
1. Check the definitions for gaps: unnamed values, themes missing a role, circular references. List them as unresolved.
2. Choose the delivery format that fits the existing styling approach. Use runtime-changeable values, such as CSS custom properties, for anything that varies by theme or density. Record why.
3. Keep a single source of token values. Derive any other format from it; do not hand-maintain two copies.
4. Layer the tokens: raw values stay private to the token layer, semantic roles are the public names, and component-level tokens exist only where a component needs its own override point.
5. Implement each theme as an alternative set of values for the same semantic names, selected in one place such as a root or theme container. Components reference semantic names only.
6. Apply one naming convention, matching the design definition. Map every legacy name to its new name in a migration table.
7. Replace raw values in components, most reused first, without changing rendering. Record each replacement. A value with no matching token is an exception to review, not a new token by default.
8. Add a repeatable drift check, such as a search or lint rule, that reports raw colors, sizes, and similar values in component styles outside the token layer. Document how to run it.
9. Verify the default theme renders as before (visual comparison or computed values), each theme applies, contrast is measured for text and interactive pairs in each theme, and no token is unresolved.
10. Document how to add, rename, and retire a token.

## Rules and heuristics
- Required: components use semantic or component tokens and never raw values or raw-layer tokens.
- Required: replacing values must not change visible output. List every difference, including near-matches, and get it approved. Never snap a value to the nearest token silently.
- Required: renaming or removing a token ships with a migration mapping.
- Recommended: add a build step only if the codebase has none that can do the job, and justify it.
- Recommended: keep theme-switching logic out of components.
- Recommended: keep a value used by one component inside that component until reuse is real.

## Checks
- Every raw value found maps to a token or is listed as an exception.
- Every theme defines every semantic name, and no reference is circular or unresolved.
- The drift check ran, and its result and limits are recorded. It reports only what it can detect.
- Contrast results exist for each pairing and theme, or the pairing is marked unverified.
- The migration table covers every renamed or removed token.

## Output
Return the token source and format with rationale, naming convention, layer structure, theme mechanism, migration table, replaced values, exceptions, drift check and its result, verification evidence, and unresolved gaps. Use the [token implementation report](templates/token-implementation-report.md).

## Completion criteria
- Components in scope use tokens, and exceptions are listed with a reason.
- Themes switch in one place and were verified.
- A teammate can run the drift check and add or retire a token from the documentation.
