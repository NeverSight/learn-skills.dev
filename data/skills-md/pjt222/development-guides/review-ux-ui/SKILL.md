---
name: review-ux-ui
description: >
  Review user experience and interface design using Nielsen's heuristics,
  WCAG 2.1 accessibility guidelines, keyboard and screen reader audit, user
  flow analysis, cognitive load assessment, and form usability evaluation.
  Use when conducting a usability review before release, assessing WCAG 2.1
  accessibility compliance, evaluating user flows for efficiency, reviewing
  form design, or performing a heuristic evaluation of an existing interface.
license: MIT
allowed-tools: Read Grep Glob WebFetch
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: review
  complexity: advanced
  language: multi
  tags: ux, ui, accessibility, wcag, heuristics, usability, user-flows, cognitive-load
---

# Review UX/UI

Evaluate user experience and interface design for usability, accessibility, and effectiveness.

## When to Use

- Conducting a usability review of an application before release
- Assessing accessibility compliance (WCAG 2.1 AA or AAA)
- Evaluating user flows for efficiency and error prevention
- Reviewing form design for usability and conversion optimization
- Performing a heuristic evaluation of an existing interface
- Assessing cognitive load and information architecture

## Inputs

- **Required**: Application to review (URL, prototype, or source code)
- **Required**: Target user description (roles, technical proficiency, context of use)
- **Optional**: User research findings (interviews, surveys, analytics)
- **Optional**: WCAG conformance target (A, AA, or AAA)
- **Optional**: Specific user flows or tasks to evaluate
- **Optional**: Assistive technology to test with (screen reader, switch access)

## Procedure

### Step 1: Heuristic Evaluation (Nielsen's 10 Heuristics)

Evaluate the interface against each heuristic:

| # | Heuristic | Key Question | Rating |
|---|-----------|-------------|--------|
| 1 | **Visibility of system status** | Does the system always inform users about what is happening? | |
| 2 | **Match between system and real world** | Does the system use familiar language and concepts? | |
| 3 | **User control and freedom** | Can users easily undo, redo, or exit unwanted states? | |
| 4 | **Consistency and standards** | Do similar elements behave the same way throughout? | |
| 5 | **Error prevention** | Does the design prevent errors before they occur? | |
| 6 | **Recognition rather than recall** | Are options, actions, and information visible or easily retrievable? | |
| 7 | **Flexibility and efficiency of use** | Are there shortcuts for experienced users without confusing novices? | |
| 8 | **Aesthetic and minimalist design** | Does every element serve a purpose? Is there unnecessary clutter? | |
| 9 | **Help users recognize, diagnose, and recover from errors** | Are error messages clear, specific, and constructive? | |
| 10 | **Help and documentation** | Is help available and easy to find when needed? | |

For each heuristic, rate severity of violations:

| Severity | Description |
|----------|-------------|
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time allows |
| 2 | Minor — low priority fix |
| 3 | Major — important to fix, high priority |
| 4 | Catastrophic — must fix before release |

```markdown
## Heuristic Evaluation Findings
| # | Heuristic | Severity | Finding | Location |
|---|-----------|----------|---------|----------|
| 1 | System status | 3 | No loading indicator during data fetch — users click repeatedly | Dashboard page |
| 3 | User control | 2 | No undo for item deletion — only a confirmation dialog | Item list |
| 5 | Error prevention | 3 | Date field accepts invalid dates (Feb 30) | Booking form |
| 9 | Error recovery | 4 | Form submission error clears all fields | Registration |
```

**Expected:** All 10 heuristics evaluated with specific findings and severity ratings.
**On failure:** If time-constrained, focus on heuristics 1, 3, 5, and 9 (most impactful for user experience).

### Step 2: Accessibility Audit (WCAG 2.1)

#### Perceivable
- [ ] **1.1.1 Non-text content**: All images have alt text (decorative images have `alt=""`)
- [ ] **1.3.1 Info and relationships**: Semantic HTML used (headings, lists, tables, landmarks)
- [ ] **1.3.2 Meaningful sequence**: DOM order matches visual order
- [ ] **1.4.1 Use of colour**: Colour is not the only means of conveying information
- [ ] **1.4.3 Contrast**: Text contrast ratio ≥ 4.5:1 (normal), ≥ 3:1 (large text)
- [ ] **1.4.4 Resize text**: Text can be resized to 200% without loss of function
- [ ] **1.4.11 Non-text contrast**: UI components and graphics have ≥ 3:1 contrast
- [ ] **1.4.12 Text spacing**: Content works with increased text spacing (line height 1.5x, letter spacing 0.12em, word spacing 0.16em)

#### Operable
- [ ] **2.1.1 Keyboard**: All functionality is operable via keyboard
- [ ] **2.1.2 No keyboard trap**: Focus is never trapped in a component
- [ ] **2.4.1 Skip links**: Skip navigation link available for keyboard users
- [ ] **2.4.3 Focus order**: Tab order follows a logical, predictable sequence
- [ ] **2.4.7 Focus visible**: Keyboard focus indicator is clearly visible
- [ ] **2.4.11 Focus not obscured**: Focused element is not hidden behind sticky headers/overlays
- [ ] **2.5.5 Target size**: Interactive targets are at least 24x24px (44x44px recommended on touch)

#### Understandable
- [ ] **3.1.1 Language of page**: `lang` attribute set on `<html>`
- [ ] **3.2.1 On focus**: Focus doesn't trigger unexpected changes
- [ ] **3.2.2 On input**: Input doesn't trigger unexpected changes without warning
- [ ] **3.3.1 Error identification**: Errors are clearly described in text
- [ ] **3.3.2 Labels or instructions**: Form inputs have visible labels
- [ ] **3.3.3 Error suggestion**: Error messages suggest how to fix the problem

#### Robust
- [ ] **4.1.1 Parsing**: HTML is valid (no duplicate IDs, proper nesting)
- [ ] **4.1.2 Name, role, value**: Custom components have ARIA roles and properties
- [ ] **4.1.3 Status messages**: Dynamic content changes announced to screen readers

**Expected:** WCAG 2.1 AA criteria systematically checked with pass/fail per criterion.
**On failure:** Use automated tools (axe-core, Lighthouse) for initial scan, then manual testing for criteria that require human judgement.

### Step 3: Keyboard and Screen Reader Audit

#### Keyboard Navigation Test
Using only Tab, Shift+Tab, Enter, Space, Arrow keys, and Escape:

```markdown
## Keyboard Navigation Audit
| Task | Completable? | Issues |
|------|-------------|--------|
| Navigate to main content | Yes — skip link works | None |
| Open dropdown menu | Yes | Arrow keys don't work within menu |
| Submit a form | Yes | Tab order skips the submit button |
| Close a modal | No | Escape doesn't close, no visible close button in tab order |
| Use date picker | No | Custom date picker not keyboard accessible |
```

#### Screen Reader Test
Test with NVDA (Windows), VoiceOver (macOS/iOS), or TalkBack (Android):

```markdown
## Screen Reader Audit
| Element | Announced As | Expected | Issue |
|---------|-------------|----------|-------|
| Logo link | "link, image" | "Home, link" | Missing alt text on logo |
| Search input | "edit, search" | "Search products, edit" | Missing label association |
| Nav menu | "navigation, main" | Correct | None |
| Error message | (not announced) | "Error: email is required" | Missing live region |
| Loading spinner | (not announced) | "Loading, please wait" | Missing aria-live or role="status" |
```

**Expected:** Complete task flows tested with keyboard-only and screen reader.
**On failure:** If a screen reader is unavailable, inspect ARIA attributes and semantic HTML as a proxy.

### Step 4: Analyse User Flows

Map and evaluate key user flows:

```markdown
## User Flow: Complete a Purchase

### Steps
1. Browse products → 2. View product → 3. Add to cart → 4. View cart →
5. Enter shipping → 6. Enter payment → 7. Review order → 8. Confirm

### Assessment
| Step | Friction | Severity | Notes |
|------|---------|----------|-------|
| 1→2 | Low | - | Clear product cards |
| 2→3 | Medium | 2 | "Add to cart" button below the fold on mobile |
| 3→4 | Low | - | Cart icon updates with count |
| 4→5 | High | 3 | Must create account — no guest checkout |
| 5→6 | Low | - | Address autocomplete works well |
| 6→7 | Medium | 2 | Card number field doesn't auto-format |
| 7→8 | Low | - | Clear order summary |

### Flow Efficiency
- **Steps**: 8 (acceptable for e-commerce)
- **Required fields**: 14 (could reduce with address autocomplete + saved payment)
- **Decision points**: 2 (size selection, shipping method)
- **Potential drop-off points**: Step 4→5 (forced account creation)
```

**Expected:** Critical user flows mapped with friction points identified and rated.
**On failure:** If user analytics are unavailable, assess flows based on task complexity and number of steps.

### Step 5: Assess Cognitive Load

- [ ] **Information density**: Is the amount of information per screen appropriate?
- [ ] **Progressive disclosure**: Is complex information revealed gradually?
- [ ] **Chunking**: Are related items grouped visually (Gestalt principles)?
- [ ] **Recognition over recall**: Can users see options rather than remembering them?
- [ ] **Consistent patterns**: Do similar tasks use similar interaction patterns?
- [ ] **Decision fatigue**: Are users presented with too many choices at once? (Hick's law)
- [ ] **Working memory**: Do users need to remember information across steps?

**Expected:** Cognitive load assessed with specific areas of overload or underload identified.
**On failure:** If cognitive load is difficult to assess objectively, use the "squint test" — squint at the screen and see if the structure and hierarchy are still apparent.

### Step 6: Review Form Usability

For each form in the application:

- [ ] **Labels**: Every input has a visible, associated label
- [ ] **Placeholder text**: Used for examples only, not as labels
- [ ] **Input types**: Correct HTML input types (email, tel, number, date) for mobile keyboards
- [ ] **Validation timing**: Errors shown on blur or submit (not on every keystroke)
- [ ] **Error messages**: Specific ("Email must include @") not generic ("Invalid input")
- [ ] **Required fields**: Clearly marked (and optional fields are marked if most are required)
- [ ] **Field grouping**: Related fields visually grouped (name, address, payment sections)
- [ ] **Autocomplete**: `autocomplete` attributes set for standard fields (name, email, address, cc-number)
- [ ] **Tab order**: Logical flow matching visual layout
- [ ] **Multi-step forms**: Progress indicator shows current step and total steps
- [ ] **Persistence**: Form data preserved if user navigates away and returns

**Expected:** Each form assessed against the checklist with specific issues documented.
**On failure:** If there are many forms, prioritize the highest-traffic forms (registration, checkout, contact).

### Step 7: Write the UX/UI Review

```markdown
## UX/UI Review Report

### Executive Summary
[2-3 sentences: overall usability, most critical issues, strongest aspects]

### Heuristic Evaluation Summary
| Heuristic | Severity | Key Finding |
|-----------|----------|-------------|
[Summary table from Step 1]

### Accessibility Compliance
- **Target**: WCAG 2.1 AA
- **Status**: [X of Y criteria pass]
- **Critical failures**: [List]

### User Flow Analysis
[Key friction points with severity and recommendations]

### Top 5 Improvements (Prioritised)
1. **[Issue]** — Severity: [N] — [Specific recommendation]
2. ...

### What Works Well
1. [Specific positive observation]
2. ...
```

**Expected:** Review provides prioritised, actionable recommendations with severity ratings.
**On failure:** If the review surfaces too many issues, categorise into "must fix" (severity 3-4) and "should fix" (severity 1-2).

## Validation

- [ ] All 10 Nielsen heuristics evaluated with severity ratings
- [ ] WCAG 2.1 criteria checked (at minimum: 1.1.1, 1.4.3, 2.1.1, 2.4.7, 3.3.1, 4.1.2)
- [ ] Keyboard navigation tested for key user flows
- [ ] Screen reader tested (or ARIA/semantic HTML reviewed as proxy)
- [ ] At least one critical user flow analysed for friction
- [ ] Cognitive load assessed
- [ ] Form usability evaluated
- [ ] Findings prioritised by severity with actionable recommendations

## Common Pitfalls

- **Confusing UX with visual design**: UX is about how it works; visual design is about how it looks. A beautiful interface can have terrible UX. Evaluate both but distinguish them.
- **Testing only the happy path**: Error states, empty states, loading states, and edge cases are where UX problems hide.
- **Ignoring real devices**: Browser dev tools responsive mode is a proxy. Real device testing catches touch, performance, and viewport issues.
- **Accessibility as an afterthought**: Accessibility issues found late are expensive to fix. Evaluate early and continuously.
- **Personal preference as UX feedback**: "I would prefer..." is not UX feedback. Cite heuristics, research, or established patterns.

## Related Skills

- `review-web-design` — visual design review (layout, typography, colour — complementary to UX)
- `scaffold-nextjs-app` — Next.js application scaffolding
- `setup-tailwind-typescript` — Tailwind CSS for design system implementation
