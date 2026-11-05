---
name: design-lint
description: "Lint Figma designs for compliance and auto-fix violations. Use when: lint/fix/check compliance/clean up + design/page/screen, or when automated quality fixes are needed. Supports both quick one-step lint and granular multi-step workflows."
---

# Design Lint — Automated Compliance & Auto-Fix

Lint Figma designs against 40 quality rules across 5 categories (token compliance, WCAG accessibility, layout & structure, naming & content, component). Auto-fixes 22 of 40 rules. Pairs with `design-review` for the human review step.

## Skill Boundaries

- Use this skill for **automated lint checking and auto-fixing**.
- If the task is **human-driven design critique**, switch to [design-review](../design-review/SKILL.md).
- If the task is **creating new UI**, switch to [figma-create-ui](../figma-create-ui/SKILL.md).

**If `ping` fails (plugin not connected):** STOP the workflow. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

## Workflow — Quick Mode (Default)

For most cases, the one-step workflow is sufficient:

```
Step 1: ping                              → verify plugin connection
Step 2: lint_fix_all                      → check + auto-fix in one call
Step 3: Summarize results:
        - Total nodes checked
        - Violations found
        - Auto-fixed
        - Remaining (need manual attention)
Step 4: For remaining violations → explain what needs manual attention and how to fix
```

## Workflow — Granular Mode

When the user wants more control (preview before fixing, fix specific categories only):

```
Step 1: ping                              → verify plugin connection
Step 2: load_toolset("lint")              → enable granular lint tools
Step 3: lint_check                        → scan page/selection for violations
Step 4: Present violation summary grouped by category
Step 5: ⛔ WAIT for user confirmation     → user picks what to fix
Step 6: lint_fix (selected violations)    → apply fixes
Step 7: lint_check                        → re-verify fixes applied
Step 8: Report remaining violations
```

## Workflow — Dry Run (Preview Only)

To preview violations without applying any changes:

```
lint_fix_all(dryRun: true)                → returns fixable violations without fixing
```

## Rule Categories

| Category | Rules | Auto-fixable | Focus |
|----------|------:|:------------:|-------|
| Token Compliance | 6 | 6 | Colors, typography, spacing, radius bound to tokens |
| WCAG Accessibility | 5 | 3 | Contrast, touch targets, text size, line height |
| Layout & Structure | 24 | 13 | Auto-layout, overflow, button/input structure, screen shell |
| Naming & Content | 2 | 0 | Default names, placeholder text |
| Component | 1 | 0 | Unbound component properties |

## Filtering Options

Target specific categories or nodes:

```
lint_fix_all(categories: ["token"])           → token compliance only
lint_fix_all(categories: ["wcag"])            → accessibility only
lint_fix_all(categories: ["layout"])          → layout & structure only
lint_fix_all(nodeIds: ["1:23", "4:56"])       → specific nodes only
lint_fix_all(categories: ["token", "wcag"])   → multiple categories
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| error | Breakage that must be fixed | Always fix |
| unsafe | Layout issues causing visual bugs | Fix recommended |
| heuristic | Best-practice violations | Fix when possible |
| style | Cosmetic / naming preferences | Fix optionally |

## Common Remaining Violations (Manual Fix Required)

These 16 rules cannot be auto-fixed and need manual attention:

- `wcag-contrast` — adjust colors for ≥ 4.5:1 contrast ratio
- `wcag-non-text-contrast` — non-text elements need ≥ 3:1 contrast
- `empty-container` — add content or remove empty frames
- `max-nesting-depth` — simplify hierarchy (> 6 levels deep)
- `root-misclassified-interactive` — screen roots should not be interactive shells
- `nested-interactive-shell` — unwrap nested interactive elements
- `social-row-cramped` / `nav-overcrowded` / `stats-row-cramped` — increase container width
- `screen-bottom-overflow` — content exceeds viewport
- `default-name` — rename "Frame 1" etc. to descriptive names
- `placeholder-text` — replace "Lorem ipsum" / "Button" with real content
- `component-bindings` — connect unbound component properties to child layers

## Integration with Quality Loop

```
figma-create-ui → design-review → design-lint
                   (critique)      (this skill — auto-fix)
```

Run after `design-review` to automatically fix flagged violations, or run standalone for quick compliance checks.

## Using with verify_design

For a combined lint + screenshot in one call:

```
verify_design(nodeId: "1:23")             → lint + fix + screenshot in one round-trip
```

This is the preferred tool after creating UI — it combines `lint_fix_all` + `export_image` into a single call.
