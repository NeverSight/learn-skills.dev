---
name: design-to-code-check
description: "Check alignment between a specific design specification and its code implementation — a focused, single-component or single-screen comparison. Trigger when someone says: does this match the design, check implementation, design code alignment, what's different between the design and the build, spec check, implementation review, or anything about comparing a designed component or screen to its coded equivalent. Do NOT trigger for system-wide drift detection across multiple components or teams — use drift-detection for that."
references:
  - ../../knowledge-notes/design-to-code-contract.md
  - ../../knowledge-notes/output-discipline.md
---

# Design-to-code check

A skill for reviewing the alignment between a design specification and its code implementation, producing a structured discrepancy report catalogued by dimension and severity.

## Context

Design-to-code alignment reviews catch two different categories of problem. The first is implementation error — the developer built something different from what was specified, either by mistake or because the specification was unclear. The second is specification ambiguity — the design did not define behaviour completely enough for the developer to implement it correctly, and the developer made a reasonable guess that turned out to be wrong.

Both categories matter, but they require different responses. An implementation error needs to be corrected in the code. A specification ambiguity needs to be corrected in the design and documented, so the same guess does not get made again.

This skill produces a report that distinguishes between the two.

---

## Configuration

Before producing output, check for a `.ds-ops-config.yml` file in the project root. If present, load:
- `severity.*` — overrides for discrepancy severity, especially `specification_gap` and `missing_interaction_state`
- `system.framework` and `system.styling` — pre-selects framework-specific checking guidance
- `integrations.figma` — if enabled, auto-pull the design specification (see below)
- `integrations.chromatic` — if enabled, use visual regression data as a supplementary signal
- `gates.design_to_code` — if running as part of `component-to-release`, determines which findings block release

## Auto-pull integrations

**Figma MCP** (`integrations.figma.enabled: true`):
- Pull the component specification directly from `integrations.figma.file_key` via Figma MCP
- Read component properties, variant definitions, and layer structure as the design reference
- This replaces the need for the user to provide a Figma file link — the skill can say "I pulled the Button specification from your Figma library" and proceed immediately

**Chromatic** (`integrations.chromatic.enabled: true`):
- Pull the latest visual snapshots for the component being checked
- Use visual diffs between the Chromatic baseline and the current implementation as a supplementary signal for Dimensions 1–3 (spacing, colour, typography)
- Chromatic data does not replace the manual dimension review but can surface differences the manual review should confirm

**GitHub** (`integrations.github.enabled: true`):
- If the component implementation is in the configured repo, pull the component source files directly
- Identify the component's last update date and recent changes to contextualise findings

If an integration fails, log it and proceed with manual input.

## Step 1: Gather the comparison materials

Ask for or confirm (skip questions already answered by auto-pull):
- The design reference: Figma file link, exported specs, or described specification (skip if pulled from Figma MCP)
- The implementation reference: component in code (React, Vue, Twig, etc.), a link to a running implementation, or a description of what was built. Note the styling approach — CSS custom properties, SCSS variables, Tailwind utility classes, or CSS-in-JS — as this affects how token references are identified during the check.
- The component or screen being reviewed
- Whether this is a first-pass review or a follow-up check after a previous round of corrections
- Any known areas of concern the review should pay particular attention to

If both design and implementation are available directly, proceed to the check. If only one is available, note in the report which side of the comparison is inferred rather than directly inspected.

## Step 1b: Design specification checklist

Before running the check, verify the design specification is complete enough to check against. Incomplete specs are the root cause of Type II (specification gap) findings — catching them upfront reduces noise in the report.

**Design specification completeness checklist:**
- [ ] All interactive states are defined (default, hover, active, focus, disabled, error, loading)
- [ ] Spacing values are specified using token names, not pixel values
- [ ] Colour values are specified using token names, not hex values
- [ ] Typography is specified using type scale tokens
- [ ] Responsive behaviour is defined for at least two breakpoints
- [ ] Focus indicator style is specified
- [ ] Content overflow behaviour is defined (truncation, wrapping, scrolling)
- [ ] Touch target sizes are specified for mobile breakpoints

**If the specification fails this checklist:** Note the missing items and proceed with the check. Missing specification items will appear as Type II findings in the report — but flagging them upfront sets the right expectation: these are design gaps, not implementation errors.

Share this checklist with designers as a pre-handoff tool. A specification that passes this checklist before handoff will produce a cleaner design-to-code check.

## Step 2: Run the check across all dimensions

Review alignment across five dimensions. For each dimension, the goal is not to produce a list of every difference — minor sub-pixel differences in a rounding pass are not discrepancies worth reporting. The goal is to identify differences that affect visual consistency, user experience, or system integrity.

### Dimension 1: Spacing and layout

Check:
- Padding and margin values: do they match design specifications, and are they using the correct spacing tokens?
- Element alignment: horizontal and vertical alignment of components within their containers
- Gap between elements in flex or grid layouts
- Component sizing: width and height where specified, or proportional behaviour where not fixed
- Responsive behaviour: does the implementation respond to breakpoints as specified?

Flag raw pixel values where spacing tokens should be used.

**Framework-specific notes for spacing checks:**
- **Vue SFC:** Check `<style>` blocks for raw `px` values. Token references may be SCSS variables (`$space-4`) or CSS custom properties (`var(--space-4)`).
- **Twig/Fractal:** Spacing is typically applied via BEM modifier classes or utility classes — check the backing SCSS, not just the template markup. Inline `style` attributes with pixel values are always violations.
- **Emotion/CSS-in-JS:** Check style objects and `css` prop values. Token references look like `mapSpacing(1)` or `theme.spacing.md`. String literals like `'16px'` or `'1rem'` are violations.

### Dimension 2: Colour and visual treatment

Check:
- Background colours, border colours, text colours: are they referencing the correct design tokens?
- Shadow and elevation: correct values, correct token references
- Border radius: correct values, consistent with the design system's radius scale
- Opacity: correct values and applied to the correct element
- Gradient or background treatments if present

Flag any raw hex values, rgba values, or other hardcoded colour references where tokens should be used.

### Dimension 3: Typography

Check:
- Font family: correct typeface applied
- Font size: correct size, using the correct type token
- Font weight: correct weight at each text role
- Line height: correct leading, using the correct token or documented value
- Letter spacing: correct tracking where specified
- Text alignment: left, centre, right, or justified as designed
- Text truncation or overflow handling: does the implementation handle long strings as designed?

### Dimension 4: Interactive states

Check:
- Default state: visual treatment matches design
- Hover state: correct treatment applied on hover
- Active/pressed state: correct treatment on click or touch
- Focus state: visible, compliant focus indicator applied (this is also an accessibility check)
- Disabled state: correct reduced-prominence treatment
- Loading state: if designed, correctly implemented
- Error state: if applicable, correctly applied and correctly associated with the relevant element
- Empty state: if applicable, correctly implemented

Interactive states are the most commonly under-implemented dimension. Flag any state that was designed but is not present in the implementation.

### Dimension 5: Responsive and adaptive behaviour

Check:
- Breakpoint transitions: does the layout change at the designed breakpoints?
- Component behaviour at narrow viewports: does anything break, overflow, or truncate unexpectedly?
- Touch target sizing: at mobile breakpoints, are interactive elements meeting minimum touch target sizes?
- Content reflow: does text reflow correctly at all breakpoints?

## Step 3: Classify each discrepancy

For each discrepancy found, classify it:

**Type I: Implementation error**
The specification was clear. The implementation does not match it. Correct in code.

**Type II: Specification gap**
The design did not define this case. The implementation made a reasonable assumption. Update the design specification to document the intended behaviour, then align the implementation.

**Type III: System inconsistency**
The design itself diverges from the design system (uses a non-system colour, a spacing value not on the scale, etc.). The issue is in the design file, not the implementation.

**Type IV: Accepted divergence**
A known, intentional difference — typically a technical constraint the design did not account for. Should be documented if it is not already.

## Step 3b: API contract validation (staff-level)

Beyond visual and behavioural alignment, validate the component's API contract:

**Prop contract compliance:**
- Does the implementation accept all props documented in the component specification? Flag any missing props.
- Does the implementation accept props NOT in the specification? Undocumented props are API surface that can't be relied on by consumers — flag them as specification gaps (Type II).
- Do prop defaults in the implementation match the documented defaults? Mismatched defaults are the subtlest and most dangerous alignment issue.

**Type safety:**
- If the specification defines prop types (TypeScript interfaces, PropTypes), does the implementation enforce them?
- Are there implicit type coercions (string to number, truthy checks on string props) that could produce unexpected behaviour?
- For enum props (variant, size), does the implementation handle invalid values gracefully (fallback to default) or silently break?

**Consumer contract signals:**
- If consuming applications pass props not in the specification, what happens? (Error, silent ignore, partial application)
- Are there undocumented "escape hatches" (className, style, spread props) that consumers are using? These are part of the de facto API even if not in the specification.

Classify API discrepancies using the same Type I–IV system. API discrepancies are typically High severity because they affect every consumer, not just a single instance.

## Step 3c: AI-readiness validation (staff-level)

If the component has an AI-optimised description (six-section format), validate it against the implementation:

- Does the Purpose section accurately describe what the implementation does?
- Do the Props in the description match the actual implementation props? (Names, types, defaults — exact match required)
- Are the Anti-patterns in the description correct? (Does the implementation actually prevent or allow the documented anti-patterns?)
- Do the Composition rules match the implementation's actual nesting constraints?
- Does the Accessibility section match the implemented keyboard and ARIA behaviour?

Flag any discrepancy between the AI description and the implementation as a separate finding category: **AI metadata drift.** This is distinct from design-to-code drift — it means the metadata that AI tools consume is inaccurate, which produces incorrect AI-generated output.

## Step 4: Produce the report

---

### Design-to-code check report

Open with a headline sentence that tells the reader the overall state and where to focus.

**Component/screen:** [name]
**Design reference:** [Figma link or description]
**Implementation reference:** [link or description]
**Review date:** [date]
**Review round:** [first pass / follow-up]

---

#### Summary

One paragraph. What is the overall alignment? Are discrepancies concentrated in a particular dimension? Is this a clean build with minor corrections or does it need significant rework?

---

#### Discrepancy log

| ID | Dimension | Type | Severity | Element | Design spec | Implementation | Action |
|---|---|---|---|---|---|---|---|
| DC-01 | [dimension] | [I–IV] | 🔴 Critical / 🟠 High / 🟡 Medium / ⚪ Low | [specific element] | [what the design says] | [what was implemented] | [who does what] |

Severity guidance:
- 🔴 Critical: accessibility regression (missing focus state, insufficient colour contrast, no keyboard interaction)
- 🟠 High: visible to end users, affects perceived quality or usability
- 🟡 Medium: system inconsistency (hardcoded value, wrong token), visible under close inspection
- ⚪ Low: minor difference without user-facing impact

---

#### Summary by dimension

Brief status for each dimension: clean / minor corrections / significant corrections. Helps the team understand where the work is concentrated.

---

#### Specification gaps identified

List any Type II findings separately. These require action from the designer, not the developer, and should be tracked as design tasks rather than development bugs.

---

## Quality checks

- Discrepancies include both what the design specifies and what was implemented — not just "colour is wrong"
- Type I (error) and Type II (spec gap) findings are clearly distinguished — they need different owners
- Interactive states are checked thoroughly, not just the default state
- Token compliance is checked as part of the colour and spacing dimensions — not just visual correctness
- Accessibility regressions (missing focus state, insufficient contrast) are always Critical
- The report is specific enough to act on without a follow-up conversation
