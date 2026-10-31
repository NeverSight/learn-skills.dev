---
name: accessibility-inclusive-design
description: "WCAG 2.2 compliance, ARIA authoring patterns, screen reader and keyboard navigation, color contrast, and cognitive/neurodiversity accommodations. Use when auditing accessibility, fixing a11y violations, choosing ARIA roles, checking contrast ratios, or designing for ADHD, dyslexia, autism, or motor impairment."
---

# Accessibility & Inclusive Design — Universal Access Framework

## Accessibility Philosophy

"The power of the web is in its universality. Access by everyone regardless of disability is an essential aspect." — Tim Berners-Lee

Accessibility is not a feature to be added at the end — it is a foundational design constraint that must inform every decision from the first wireframe. Inclusive design does not mean designing for edge cases; it means designing for the full spectrum of human ability, which benefits everyone. Curb cuts help wheelchair users and parents with strollers; captions help deaf users and people in noisy environments.

### The Inclusive Design Spectrum (Microsoft)

Disability exists on a spectrum of permanent, temporary, and situational:
- **Permanent:** One arm → **Temporary:** Arm injury → **Situational:** Holding a baby
- **Permanent:** Blind → **Temporary:** Eye infection → **Situational:** Distracted driver
- **Permanent:** Deaf → **Temporary:** Ear infection → **Situational:** Loud restaurant

Designing for permanent disability creates solutions that help everyone.

## WCAG 2.2 Compliance Framework

### The Four Principles (POUR)

**1. Perceivable** — Information must be presentable in ways all users can perceive
- Provide text alternatives for non-text content (images, icons, charts).
- Provide captions and transcripts for audio/video.
- Create content that can be presented in different ways without losing meaning.
- Make it easy to see and hear content (contrast, resize, spacing).

**2. Operable** — Interface components must be operable by all users
- Make all functionality accessible via keyboard alone.
- Give users enough time to read and use content.
- Do not design content that causes seizures or physical reactions.
- Provide clear navigation and wayfinding mechanisms.
- Support input modalities beyond keyboard (voice, pointer, touch).

**3. Understandable** — Information and operation must be understandable
- Keep text readable and understandable at the target audience level.
- Ensure content appears and operates in predictable ways.
- Help users avoid and correct mistakes.

**4. Robust** — Content must be robust enough for diverse user agents and assistive tech
- Maximize compatibility with current and future assistive technologies.
- Use valid, semantic HTML as the foundation.
- Ensure programmatic name, role, and value for all UI components.

### WCAG Conformance Levels

- **Level A:** Minimum accessibility — baseline legal requirement.
- **Level AA:** Standard target — required by most laws (ADA, EN 301 549, EAA).
- **Level AAA:** Enhanced accessibility — aspirational, target for critical public services.

### Key WCAG 2.2 Success Criteria

**New in 2.2:**
- **2.4.11 Focus Not Obscured (Minimum):** Focused element not fully hidden by other content.
- **2.4.12 Focus Not Obscured (Enhanced):** Focused element fully visible.
- **2.4.13 Focus Appearance:** Focus indicators are sufficiently visible (size and contrast).
- **2.5.7 Dragging Movements:** Provide a single-pointer alternative for drag operations.
- **2.5.8 Target Size (Minimum):** 24×24 CSS pixels minimum for interactive elements.
- **3.2.6 Consistent Help:** Place help mechanisms in consistent locations across pages.
- **3.3.7 Redundant Entry:** Do not ask users to re-enter previously provided information.
- **3.3.8 Accessible Authentication (Minimum):** No cognitive function tests for login.
- **3.3.9 Accessible Authentication (Enhanced):** No object/image recognition for login.

## Semantic HTML Foundation

### Critical Semantic Elements

- Use `<nav>` for navigation regions, `<main>` for primary content, `<aside>` for complementary content.
- Use heading hierarchy (`<h1>`–`<h6>`) that reflects document structure — never skip levels.
- Use `<button>` for actions and `<a>` for navigation — never use `<div>` for interactive elements.
- Use `<table>` with proper `<thead>`, `<th>`, and `scope` attributes for data tables.
- Use `<form>`, `<fieldset>`, `<legend>`, and `<label>` for form structure.
- Use `<ul>`/`<ol>` for lists — screen readers announce list length and position.
- Use landmark roles implicitly through semantic HTML (preferred) or explicitly via ARIA.

### ARIA Patterns (When HTML Is Not Enough)

**Core ARIA Rules:**
1. If native HTML can achieve the behavior, use it instead of ARIA.
2. Do not change native semantics unless absolutely necessary.
3. All interactive ARIA controls must be keyboard operable.
4. Do not use `role="presentation"` or `aria-hidden="true"` on focusable elements.
5. All interactive elements must have an accessible name.

**Common ARIA Widget Patterns:**
- **Tabs:** `role="tablist"`, `role="tab"`, `role="tabpanel"` with arrow key navigation.
- **Modal dialog:** `role="dialog"`, `aria-modal="true"`, trap focus within dialog.
- **Combobox/Autocomplete:** `role="combobox"`, `aria-expanded`, `aria-activedescendant`.
- **Menu:** `role="menu"`, `role="menuitem"` with arrow key navigation.
- **Tree view:** `role="tree"`, `role="treeitem"` with expand/collapse and arrow keys.
- **Live regions:** `aria-live="polite"` for non-urgent updates, `"assertive"` for critical alerts.

## Keyboard Navigation

### Tab Order and Focus Management

- Tab order must follow visual layout and logical reading order.
- Use `tabindex="0"` to add non-native elements to tab order (when semantic HTML is not possible).
- Use `tabindex="-1"` for programmatic focus management (not in tab order but focusable via JavaScript).
- Never use `tabindex` values greater than 0 — they create unpredictable tab order.

### Focus Indicator Design

- Focus rings must be visible on all interactive elements — never apply `outline: none` without a replacement.
- Minimum focus indicator: 2px solid outline with 3:1 contrast ratio against adjacent colors.
- WCAG 2.2 enhanced: focus indicator area at least as large as a 2px perimeter, 3:1 contrast.
- Use `focus-visible` to show focus rings on keyboard navigation only (hide on mouse click).

### Keyboard Interaction Patterns

- **Enter/Space:** Activate buttons and links.
- **Arrow keys:** Navigate within composite widgets (tabs, menus, radio groups, trees).
- **Escape:** Close modals, popovers, dropdowns.
- **Home/End:** Jump to first/last item in lists.
- **Tab:** Move between independent interactive elements.

## Screen Reader Optimization

### Content Strategies

- Write meaningful alt text: describe the information the image conveys, not the image itself.
- Decorative images: use `alt=""` (empty, not omitted) or `role="presentation"`.
- Complex images (charts, diagrams): provide detailed text description in context.
- Link text must be descriptive out of context — avoid "click here" and "read more."
- Use `aria-label` or `aria-labelledby` when visible text is insufficient.
- Use `aria-describedby` for supplementary descriptions (error messages, help text).

### Dynamic Content

- Announce dynamic changes with `aria-live` regions — do not assume users see visual changes.
- Single-page apps: manage focus on route changes — move focus to new content heading.
- Loading states: announce with `aria-busy="true"` and announce completion.
- Toast/notification: use `role="status"` (polite) or `role="alert"` (assertive).

## Motor and Cognitive Accommodations

### Motor Accessibility

- Touch targets: minimum 44x44pt (iOS), 48x48dp (Android), 24x24 CSS px (WCAG 2.2 minimum).
- Provide alternatives to complex gestures (drag-and-drop, multi-finger).
- Support system-level accessibility features (sticky keys, switch access, voice control).
- Avoid time-limited interactions or provide ability to extend time limits.

### Cognitive Accessibility

- Use clear, simple language at the appropriate reading level.
- Provide consistent navigation and layout across the application.
- Break complex tasks into smaller, manageable steps.
- Avoid unexpected changes in context (auto-playing media, unexpected navigation).
- Provide clear error messages with specific correction instructions.
- Support pause, stop, or hide for any auto-updating content.

## Neurodiversity Accommodations

- **Reduced motion:** Respect `prefers-reduced-motion` media query — disable animations or substitute with opacity/instant transitions.
- **High contrast:** Support `forced-colors` / `prefers-contrast: more` for users who need maximum contrast.
- **Reading preferences:** Allow font size adjustment, line spacing customization, and typeface choice where possible.
- **Attention considerations:** Minimize distracting animations, auto-playing content, and notification frequency.
- **Predictability:** Maintain consistent behavior, clear labeling, and reduced cognitive surprises to support ADHD and autism spectrum users.

## Testing Methodology

### Automated Testing (Find ~30% of Issues)
- Run axe-core, Lighthouse, or WAVE for automated scanning.
- Integrate ESLint with jsx-a11y plugin for development-time catches.
- Configure CI/CD pipelines to fail builds on critical accessibility violations.

### Manual Testing (Find ~70% of Issues)
- **Keyboard-only navigation:** Tab through entire flows without a mouse.
- **Screen reader testing:** Test with VoiceOver (macOS/iOS), NVDA/JAWS (Windows), TalkBack (Android).
- **Zoom testing:** Verify at 200% and 400% browser zoom — no content loss or overlap.
- **Color testing:** Check with color blindness simulators and contrast checkers.

### User Testing with Disabled Users
- Include people with disabilities in usability testing (minimum one per study).
- Test with actual assistive technology users — simulating disability is insufficient.
- Compensate participants fairly for their time and expertise.

## WCAG 3.0 Preview and Preparation

The W3C is developing the next major version of accessibility guidelines, now named "W3C Accessibility Guidelines" (WAG 3.0) — dropping "Web Content" from the title to reflect expanded scope beyond web to apps, documents, XR, embedded systems, and emerging technologies.

### Key Changes from WCAG 2.x

**New Conformance Model: Bronze/Silver/Gold**
WCAG 3.0 replaces the A/AA/AAA conformance levels with a Bronze/Silver/Gold system. Bronze represents the minimum acceptable accessibility standard. Silver adds enhanced support. Gold represents best-in-class accessibility across all dimensions.

**Outcome-Based Scoring (0-4)**
Instead of binary pass/fail per success criterion, WCAG 3.0 uses a 0-4 scoring system per outcome: 0 = Very Poor, 1 = Poor, 2 = Fair, 3 = Good, 4 = Excellent. Scores are weighted by impact and aggregated to determine conformance level. This granular scoring recognizes that accessibility exists on a spectrum rather than a binary state.

**174 Outcomes Framework**
The September 2025 working draft defines 174 outcomes organized by functional categories. These outcomes are more specific and measurable than WCAG 2.x success criteria, making evaluation more consistent across auditors.

**Expanded Scope**
WCAG 3.0 covers web content, native applications, documents, XR/immersive environments, embedded systems, and emerging technologies including AI-driven interfaces. Any digital experience falls within scope.

### Timeline and Migration Strategy

The W3C targets April 2026 for the next major draft milestone, with the full recommendation expected later in the decade. WCAG 2.2 remains the current legal standard. Migration strategy:

1. Continue targeting WCAG 2.2 Level AA as the compliance baseline.
2. Monitor WCAG 3.0 working drafts for directional changes.
3. Adopt the outcome-oriented mindset now — evaluate accessibility as a spectrum, not binary compliance.
4. Expand accessibility testing to cover native apps, documents, and non-web surfaces proactively.
5. When WCAG 3.0 stabilizes, plan a formal gap analysis and migration timeline.

## Routing

For **conformance work** — the WCAG 2.2 checklist organised by POUR, the full
ARIA role and state reference, widget patterns, focus management in SPAs, skip
links and landmarks, live regions, form accessibility, and the image alt-text
decision tree: read `references/wcag-aria-patterns.md`.

For **cognitive and neurodivergent accommodation** — ADHD, autism, dyslexia,
learning disabilities, anxiety, memory impairment, motor and dexterity load, and
the preference media queries that implement them: read
`references/neurodiversity-accommodations.md`.

## Cross-Referencing

- For color contrast and visual design, reference `ui-visual-design-system`.
- For mobile accessibility specifics, reference `mobile-ux-design`.
- For motion and reduced-motion handling, reference `interaction-motion-design`.
- For ethical considerations, reference `ux-ethics-content-strategy`.
- For AI feature accessibility, reference `agentic-ai-generative-ux`.
- For measuring accessibility outcomes, reference `ux-metrics-measurement`.

## v3.0 Cross-References

The v3.0 upgrade introduces accessible component implementations, cognitive accessibility foundations, internationalization considerations, and WCAG 3.0 tracking updates.

### WCAG 3.0 Progress Update

The WCAG 3.0 Preview and Preparation section above reflects the September 2025 working draft. The W3C targets an **April 2026 milestone draft** that is expected to refine the 174 outcomes framework, finalize the Bronze/Silver/Gold scoring methodology, and introduce updated guidance for AI-generated content accessibility. Monitor W3C working group publications for the April 2026 update, which may introduce significant changes to the conformance model and outcome definitions.

### Accessible Component Implementations — `component-patterns-code`

The `component-patterns-code` skill provides production-ready React and SwiftUI component cookbooks where every component includes complete accessibility implementation. Coverage includes: ARIA patterns for tabs, modals, comboboxes, menus, and tree views (implementing the patterns described in the ARIA Patterns section above); keyboard navigation with full key binding maps for each component; focus management for single-page application route transitions, modal trap/restore, and composite widget arrow-key navigation; and screen reader testing annotations documenting expected VoiceOver/NVDA/TalkBack behavior. Each component cookbook entry serves as a reference implementation of the accessibility requirements defined in this skill.

### Cognitive Accessibility Foundations — `cognitive-psychology-ux`

The `cognitive-psychology-ux` skill provides the scientific research underlying the Cognitive Accessibility section above. Covers attention models (selective, sustained, divided), working memory capacity and its implications for interface complexity, processing speed variation across age and ability, and cognitive load measurement techniques. This scientific foundation enables more precise cognitive accessibility decisions — for example, understanding why progressive disclosure reduces cognitive load, or how chunking information aligns with working memory constraints. Particularly valuable for designing for neurodiversity (ADHD, autism spectrum, cognitive decline).

### Internationalized Accessibility — `cross-cultural-i18n-ux`

The `cross-cultural-i18n-ux` skill covers accessibility considerations in internationalized interfaces. Includes: RTL (right-to-left) layout mirroring and its impact on focus order, screen reader reading direction, and gesture semantics; CJK (Chinese, Japanese, Korean) typography accessibility including character spacing, line-breaking rules, and input method accessibility; and cross-cultural considerations for color semantics, icon interpretation, and error message localization. Essential when accessibility requirements intersect with multi-language, multi-script deployments.

## Key Sources

- W3C WCAG 2.2 Specification
- W3C WCAG 3.0 Working Draft (September 2025; superseded by the March 2026 draft -- verify current
  status at w3.org/TR/wcag-3.0/ before citing specifics)
- WAI-ARIA Authoring Practices Guide 1.2
- WebAIM articles and testing tools
- Microsoft Inclusive Design Toolkit
- NNG Group accessibility research
- Deque: WCAG 3.0 analysis (174 outcomes)
