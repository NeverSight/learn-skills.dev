---
name: accessibility-audit
description: Reviews web and application accessibility against WCAG 2.2 AA and the European Accessibility Act (EAA, enforceable June 2025). Covers semantic HTML, ARIA usage, keyboard navigation, focus management, color contrast, screen-reader compatibility, form labels and errors, alternative text, motion and animation preferences, internationalization and localization quality, and testing tool integration (axe, pa11y, Lighthouse, Playwright a11y). Use when the user asks about "accessibility", "a11y", "WCAG", "screen reader", "EAA", "keyboard nav", invokes /accessibility-audit, or when the orchestrator delegates on user-facing applications. Stack-agnostic on the approach; framework-specific heuristics for React / Vue / Angular / Svelte / plain HTML.
license: Apache-2.0
metadata:
  version: 0.1.0
  id_prefix: A11Y
---

# Accessibility Audit

You review the application's accessibility — whether people with disabilities can use it. The standard is WCAG 2.2 Level AA; for products sold in the EU, the European Accessibility Act (EAA) makes this legally required from June 2025 for a broad category of products and services.

This skill follows the library-wide rules in [`docs/CONVENTIONS.md`](../../docs/CONVENTIONS.md). Read that first.

## Scope

Applies whenever the application has a user interface — web, mobile web, desktop Electron, native mobile if the codebase is visible. Does not apply to backend-only services or internal CLIs (but see release-readiness for operator tooling).

## Inputs

From orchestrator: `scope_tier`, `jurisdiction`, `stack_summary`, `gitnexus_indexed`. Plus:

- `ui_framework`: react | vue | angular | svelte | ember | plain-html | ios-native | android-native | flutter | other
- `target_wcag_level`: A | AA | AAA (default AA)
- `eaa_in_scope`: true | false — does the product fall under the EAA? (e-commerce, banking, transport tickets, e-books, computing hardware + OS, telecoms, AV media services, ATMs, etc.)

If not provided, ask.

## Finding ID prefix

`A11Y` — see `CONVENTIONS.md` §4.

## Tier thresholds

| Tier | WCAG A | WCAG AA | EAA applicable | Auto-testing | Manual screen-reader testing |
|---|---|---|---|---|---|
| prototype | advisory | advisory | advisory | optional | optional |
| team | **required** | **required for user-facing flows** | **required if applicable** | **required** in CI | recommended |
| scalable | **required** | **required everywhere** | **required if applicable + audited** | **required** with zero-regression gate | **required** per major release |

## Review surface

### 1. Semantic HTML

Semantic elements carry accessibility for free. Misused `<div>`/`<span>` is the most common accessibility failure.

- `<button>` for clickable actions, not `<div onClick>`. The former is keyboard-focusable, has proper role, fires on Enter/Space.
- `<a href>` for navigation, not `<button>` or `<div>` with `onClick={() => navigate(...)}`.
- Landmark elements: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` — one `<main>` per page.
- Heading hierarchy `<h1>`–`<h6>` with no skips.
- Form structure: `<label for>` tied to `<input id>`, `<fieldset>` + `<legend>` for grouped inputs.
- Lists: `<ul>` / `<ol>` for lists, not series of `<div>`.
- Tables: `<table>` with `<thead>`, `<tbody>`, `<th scope>` for data tables. Never for layout.
- `<dialog>` for modal dialogs (or well-implemented ARIA dialog pattern), not just a styled `<div>`.

### 2. Keyboard navigation

Every interactive element must be reachable and operable by keyboard.

- Tab order follows visual order (no surprising jumps).
- All custom interactive components (`role="button"`, `role="menuitem"`, etc.) handle keyboard — Enter/Space for activation, Arrow keys for navigation in composite widgets, Escape for dismissal.
- Focus visible — no `outline: none` without a replacement focus style (WCAG 2.4.7 Focus Visible).
- No keyboard traps — can always Tab out of every component.
- Skip links — "Skip to main content" for repetitive navigation.
- Modal dialogs trap focus inside while open and restore focus on close.
- Drag-and-drop has a keyboard-accessible alternative (WCAG 2.5.7).

Grep for anti-patterns:
- `tabindex="-1"` on things users need to interact with.
- `tabindex="99"` etc. — positive tabindex disrupts natural order.
- `onClick` on `<div>` / `<span>` without corresponding `onKeyDown` and `role="button"` + `tabindex="0"`.
- `outline: none` / `outline: 0` without `:focus-visible` replacement.

### 3. ARIA usage

ARIA is a prosthesis, not an enhancement. Rule of ARIA: "No ARIA is better than bad ARIA."

- **First rule**: if you can use a native HTML element, use it — don't reach for ARIA.
- `aria-label` / `aria-labelledby` for elements that need a label but can't have a visible one (icon buttons).
- `aria-describedby` for supplementary info (e.g. form hints, error messages).
- `aria-live` regions for dynamic updates — `polite` for most, `assertive` only for interruptions.
- `aria-hidden="true"` only for decorative content; never on focusable elements (breaks the accessibility tree relationship).
- `aria-expanded`, `aria-selected`, `aria-checked` states on composite widgets.
- Complex widgets follow the WAI-ARIA Authoring Practices patterns (combobox, tabs, accordion, menu, treeview).

Common anti-patterns:
- `aria-label` repeating visible text verbatim (redundant announcement).
- Missing `role` on custom widgets.
- `aria-hidden` on the entire page / `<body>` while a modal is open (should only hide siblings).
- Applying `role="button"` without full keyboard support.

### 4. Color and contrast

- **WCAG 1.4.3** — text contrast ratio at least 4.5:1 (AA) or 7:1 (AAA) for normal text; 3:1 (AA) or 4.5:1 (AAA) for large text (≥18pt or 14pt bold).
- **WCAG 1.4.11** — non-text UI component contrast at least 3:1 (borders of inputs, icons conveying meaning, focus indicators).
- **Color not the only channel of information** (WCAG 1.4.1) — don't rely on red/green alone for error/success. Pair with icon, text, shape.
- Dark-mode parity — contrast checked in both themes.
- Tools: `axe-core`, Chrome DevTools contrast checker, Stark, WebAIM contrast checker.

### 5. Text and content

- Resizable to 200% (WCAG 1.4.4) without loss of functionality — avoid fixed pixel sizes on text / container dimensions that clip text.
- Reflow at 320 CSS pixels width (WCAG 1.4.10) — layouts must adapt, no horizontal scrolling for body content.
- Line height ≥ 1.5× font size; paragraph spacing ≥ 2× font size; letter spacing ≥ 0.12× font size; word spacing ≥ 0.16× font size — when user adjusts text spacing (WCAG 1.4.12).
- Plain language where possible; reading level disclosed for complex content.

### 6. Images, icons, media

- **Alt text** on images:
  - Informative images: describe the information the image conveys.
  - Decorative images: `alt=""` or CSS background + `role="presentation"`.
  - Functional images (image-only buttons, links): describe the action, not the picture.
  - Complex images (charts, diagrams): longer description available via `aria-describedby` or adjacent text.
  - Avoid `alt="image of ..."` — screen readers already announce it's an image.
- **Icons**: `aria-label` for standalone icon buttons; `aria-hidden="true"` on decorative icons accompanied by visible text.
- **SVG**: `<title>` inside for accessible name, or `aria-label` on `<svg>` if appropriate.
- **Video**:
  - Captions for all pre-recorded audio (WCAG 1.2.2).
  - Audio description for visual information in video (WCAG 1.2.3 / 1.2.5).
  - Transcripts for audio-only media.
  - Controls are keyboard-operable.
  - Autoplay muted or user-initiated; auto-playing audio longer than 3s has a mechanism to pause/mute (WCAG 1.4.2).
- **Live media**: captions (WCAG 1.2.4) for live audio at AA.

### 7. Forms

- Every input has a `<label>` — not just `placeholder` text (disappears on input, low contrast).
- Required fields marked visually and programmatically (`aria-required="true"` or `required`).
- Error messages:
  - Announced to screen readers (`aria-live="polite"` region or `aria-invalid` + `aria-describedby` pointing to the error).
  - Associated with the failing input.
  - Clear and actionable — "Please enter a valid email address" not "Invalid input".
  - Preserved across submits — don't clear the field the user mistyped in.
- `autocomplete` attributes for common fields (WCAG 1.3.5) — `name`, `email`, `tel`, `street-address`, etc.
- Input types appropriate — `type="email"`, `type="tel"`, `type="date"` for better mobile keyboards + semantics.
- Error prevention for critical actions (WCAG 3.3.4) — confirm, review, or undo for legal / financial submissions.
- Focus moves to first error on submit failure.

### 8. Dynamic content

- Content changes announced via `aria-live`, not requiring users to detect them.
- Loading states communicated (`aria-busy`, loading indicators with accessible names).
- Toast notifications use `role="status"` or `role="alert"` depending on severity, and don't auto-dismiss before slow readers can process them.
- Infinite scroll has a "load more" fallback or proper virtualization that doesn't break screen readers.

### 9. Motion and sensory

- **Prefers-reduced-motion** respected (WCAG 2.3.3 AAA, but broadly expected at AA level of polish):
  ```css
  @media (prefers-reduced-motion: reduce) { ... }
  ```
- No content flashes more than 3 times per second (WCAG 2.3.1) — photosensitive epilepsy trigger.
- Parallax / scroll-linked animations have a preference-based opt-out.
- Autoplay animations / carousels have pause/stop/hide controls (WCAG 2.2.2).
- No information conveyed by sound / motion alone.

### 10. Time limits

- Session timeouts: user warned before, given time to extend (WCAG 2.2.1).
- Re-authenticate preserves user's in-progress work.
- Time-limited interactions (e.g. checkout with limited-duration cart) provide extension / disable option.

### 11. Navigation and orientation

- Page title unique and descriptive (WCAG 2.4.2).
- Multiple ways to reach a page (WCAG 2.4.5) — nav, search, sitemap.
- Focus order meaningful (WCAG 2.4.3).
- Link text descriptive out of context (WCAG 2.4.4) — "Read more about X" not "click here".
- Current location indicated in nav.
- Breadcrumbs for deep hierarchies.
- Language declared at document level (`<html lang="en">`) and on lang-switching elements (`<span lang="fr">bonjour</span>`) — WCAG 3.1.1 / 3.1.2.

### 12. Mobile / touch

- Target size ≥ 24×24 CSS pixels (WCAG 2.5.8 AA in WCAG 2.2, ≥ 44×44 advisory).
- Tap targets with adequate spacing.
- No drag-only interactions without alternative (WCAG 2.5.7).
- Pointer cancelation (WCAG 2.5.2) — down-event alone shouldn't trigger critical actions; allow cancel on up-event.
- Orientation not locked (WCAG 1.3.4) — works in both portrait and landscape unless essential.

### 13. Authentication

WCAG 2.2 added 3.3.8 Accessible Authentication (Minimum) at AA:

- Don't require a cognitive function test (memorizing a string, transcribing from an image) unless there's an alternative (e.g. copy-paste allowed, password managers allowed, third-party auth).
- CAPTCHAs have an alternative form — or, where possible, replace with hCaptcha/Turnstile silent challenges.

### 14. Screen reader experience

Auto-testing catches maybe 30% of issues. Manual screen reader testing is required at team+ tier for user-facing flows.

- **Tools**: NVDA (Windows, free), JAWS (Windows, commercial), VoiceOver (macOS, iOS, built-in), TalkBack (Android, built-in), Narrator (Windows).
- **Flows to test**:
  - Signup / login
  - Core transaction (purchase, submit, send)
  - Error paths
  - Modal dialogs
  - Dynamic content updates
- **What to listen for**:
  - Announcements make sense out of visual context.
  - No "unlabeled button" / "link".
  - Reading order matches logical order.
  - Focused element's state communicated (expanded/collapsed, selected, disabled).

### 15. Internationalization (i18n) accessibility

- Strings externalized, not baked into JSX/HTML as literals that block translation.
- RTL support (Arabic, Hebrew) — `dir="rtl"`, logical CSS properties (`margin-inline-start` not `margin-left`).
- Plurals / gender handled by the i18n library, not string concatenation.
- Date / number / currency formatting locale-aware.
- Icon and imagery culturally appropriate.

### 16. Testing tooling

- **Automated** in CI:
  - `axe-core` (via `jest-axe`, `@axe-core/playwright`, `cypress-axe`, `pa11y`).
  - `Lighthouse` accessibility score as a CI gate (target ≥ 95 AA).
  - `eslint-plugin-jsx-a11y` for React projects.
  - Framework-specific: `@angular-eslint/eslint-plugin-template`, Vue `a11y` eslint plugins.
- **Manual** at team+ tier:
  - Keyboard-only pass per release.
  - Screen reader pass per release.
  - Zoom to 200% / 400% pass.
- **User testing** with disabled users at scalable tier.

### 17. Accessibility statement and feedback

- **Accessibility statement** published (required under EAA and many public-sector procurement rules). Describes: conformance level, known issues + remediation timeline, alternative access routes, contact for accessibility feedback, date of last review.
- **Feedback channel** monitored — users can report barriers.

## Category enum (for findings)

- `semantic-html`
- `keyboard`
- `aria`
- `contrast`
- `text-scaling`
- `media`
- `forms`
- `dynamic-content`
- `motion`
- `time-limit`
- `navigation`
- `mobile-touch`
- `authentication`
- `screen-reader`
- `i18n`
- `tooling`
- `statement`

## Severity guidance

| Level | Examples |
|---|---|
| critical | Critical flow (signup, checkout, submit) impossible with keyboard or screen reader. No alt text on functional images in primary flows. Color the only channel for a critical distinction (e.g. error vs success) in a payment flow. |
| high | Form errors not announced. Contrast failing AA on interactive elements. Focus indicator missing. Modal missing focus trap. |
| medium | Alt text present but unhelpful. Headings not hierarchical. Language attribute missing. Autoplay carousel without pause. |
| low | Minor ARIA redundancy. Decorative icons without `aria-hidden`. |
| info | Observations or WCAG AAA items not targeted. |

## Example findings

### Example 1 — Keyboard-inaccessible card with click handler

```yaml
- id: A11Y-003
  severity: high
  category: keyboard
  title: "Product card uses div+onClick, unreachable by keyboard"
  location: "src/components/ProductCard.tsx:24"
  description: |
    ProductCard wraps its content in a `<div onClick={...}>` that navigates
    to the product detail page on click. The element has no tabindex, no
    role, and no keyboard handler. Keyboard users cannot open product
    details, which blocks the core browse-to-purchase flow. VoiceOver
    reports the element as a group, so screen reader users also cannot
    activate it.
  evidence:
    - |
      // src/components/ProductCard.tsx:24
      return (
        <div className="card" onClick={() => navigate(`/p/${slug}`)}>
          <img src={imageUrl} alt="" />
          <h3>{title}</h3>
          <p>{price}</p>
        </div>
      );
  remediation:
    plan_mode: |
      Replace the click-on-div with a semantic `<a href={"/p/" + slug}>`
      wrapping the card content. Adjust CSS so the link doesn't inherit
      default underline behavior but retains focus-visible styling. Also
      fix the empty-alt image: provide product name alt, or keep empty if
      the title beneath is sufficient (prefer the latter to avoid repeat).
    edit_mode: |
      Proposed diff replaces div+onClick with <a>; adjusts card CSS;
      removes redundant onClick handler. Safe — purely structural change.
  references:
    - "WCAG 2.1.1 Keyboard"
    - "WCAG 4.1.2 Name, Role, Value"
    - "WAI-ARIA Authoring Practices — don't use div for navigation"
  wcag_success_criterion: "2.1.1"
  blocker_at_tier: [team, scalable]
```

### Example 2 — Error messages not associated with inputs

```yaml
- id: A11Y-008
  severity: high
  category: forms
  title: "Signup form errors displayed visually but not announced to screen readers"
  location: "src/components/SignupForm.tsx:55-80"
  description: |
    The signup form shows validation errors in a red box next to each field,
    but the errors aren't associated with their inputs: no `aria-invalid`,
    no `aria-describedby` link, no live region. Screen reader users submit,
    hear nothing, and have no way to discover why submit failed. Testing
    with VoiceOver confirms: focus stays on the Submit button, which is now
    disabled, with no announcement.
  evidence:
    - |
      // src/components/SignupForm.tsx:66
      <input type="email" name="email" value={email} onChange={...} />
      {errors.email && <span className="error">{errors.email}</span>}
  remediation:
    plan_mode: |
      1. Add `aria-invalid={!!errors.email}` to each input.
      2. Give each error `id="email-error"` and add
         `aria-describedby="email-error"` to the input when error exists.
      3. Add a top-of-form `<div role="alert">` that summarizes errors on
         submit failure; move focus to this region or to the first
         errored input.
      4. Keep visual red styling — it still serves sighted users.
    edit_mode: |
      Proposed: refactor input component to accept error prop and wire
      aria attributes automatically. Changes apply to all forms using
      this component (11 files). Request confirmation because it changes
      form behavior.
  references:
    - "WCAG 3.3.1 Error Identification"
    - "WCAG 3.3.3 Error Suggestion"
    - "WCAG 1.3.1 Info and Relationships"
    - "WAI-ARIA form validation pattern"
  wcag_success_criterion: "3.3.1"
  blocker_at_tier: [team, scalable]
```

### Example 3 — Insufficient color contrast on secondary buttons

```yaml
- id: A11Y-012
  severity: medium
  category: contrast
  title: "Secondary button text contrast 3.1:1 — below WCAG AA 4.5:1"
  location: "src/styles/buttons.css:42"
  description: |
    The `.btn-secondary` class uses `color: #999` on a white background,
    yielding a 2.85:1 contrast ratio. This fails WCAG 1.4.3 (4.5:1 required
    for normal text at AA). Users with low vision or those in bright
    environments cannot read secondary button labels. Secondary buttons
    appear throughout the UI including in the checkout summary where
    "Edit cart" is primarily styled this way.
  evidence:
    - |
      /* src/styles/buttons.css:42 */
      .btn-secondary {
        color: #999;
        background: #ffffff;
        /* contrast 2.85:1 — fails WCAG AA */
      }
  remediation:
    plan_mode: |
      Darken secondary button text color to at least #595959 (contrast
      4.55:1) or #525252 (contrast 5.1:1). Verify the new tone in
      Figma / design system and confirm with design.
    edit_mode: |
      Proposed diff updates `--color-text-secondary` token to #595959 and
      adds a contrast test to the CI visual-regression suite. Affects
      secondary buttons, muted text, placeholder colors — request
      confirmation because it's a design-token change.
  references:
    - "WCAG 1.4.3 Contrast (Minimum) — Level AA"
  wcag_success_criterion: "1.4.3"
  blocker_at_tier: [team, scalable]
```

### Example 4 — EAA-covered product has no accessibility statement

```yaml
- id: A11Y-018
  severity: high
  category: statement
  title: "E-commerce product has no published accessibility statement"
  location: "process-level"
  description: |
    The product is a B2C e-commerce service targeting EU consumers — within
    the scope of the European Accessibility Act (Directive (EU) 2019/882,
    Annex I §IV). The EAA enters into force 28 June 2025 and requires an
    accessibility statement describing conformance level, known
    non-conformities, alternative access routes, contact for feedback, and
    review date. No such statement exists on the site or in the repo.
  evidence:
    - "No `/accessibility`, `/a11y-statement`, or equivalent route found."
    - "`public/` contains legal, privacy, cookies, terms — no accessibility."
  remediation:
    plan_mode: |
      1. Draft an accessibility statement. Use the EU model statement
         (Commission Implementing Decision (EU) 2018/1523) as base — it's
         adequate for EAA purposes too.
      2. Include: conformance status (AA target), known issues list with
         remediation timeline, alternatives for known issues, feedback
         email and target response time, last reviewed date.
      3. Publish at /accessibility and link from footer.
      4. Set a review cadence (annually minimum) and add to release
         checklist.
    edit_mode: |
      Scaffolds `docs/accessibility-statement.md` and a route. Statement
      content requires legal / a11y lead review — do not auto-publish.
  references:
    - "Directive (EU) 2019/882 — European Accessibility Act"
    - "EN 301 549 v3.2.1 — Accessibility requirements for ICT products and services"
    - "Commission Implementing Decision (EU) 2018/1523 (model statement)"
  related_findings: [COMP-019]
  blocker_at_tier: [team, scalable]
```

## Dimension summary template

```markdown
## Accessibility Summary

WCAG target: <A | AA | AAA>
EAA in scope: <yes | no | unclear>
UI framework: <...>

Automated test results: <axe score | Lighthouse a11y score | pa11y count>
Manual test status: <keyboard pass | screen-reader pass | not done>

Findings: <N critical, N high, N medium, N low, N info>
WCAG SCs failing: <list>
Top 3 accessibility barriers:
  1. ...
  2. ...
  3. ...

Not assessed: <list with reasons>
```

## Edit-mode remediation guidance

Safe:
- Adding `alt` to images (require user for content, use `alt=""` for decorative).
- Adding `aria-label` to icon buttons.
- Adding `lang` attribute to `<html>`.
- Adjusting focus indicator CSS.
- Adding `:focus-visible` rules to restore focus when `outline: none` was removed.
- Adding ESLint a11y plugin to config.
- Adding axe / jest-axe / Playwright-axe to existing test suites.

Require confirmation:
- Replacing `<div onClick>` with semantic element — may affect existing CSS / tests.
- Changing color tokens — design-system change.
- Refactoring forms to add aria associations — touches many components.
- Adding reduced-motion CSS — changes animation behavior.
- Publishing accessibility statement — legally meaningful, needs sign-off.

## Skill-specific do-nots

- Do not treat axe / Lighthouse scores as sufficient evidence of accessibility. Automated tools catch about 30% of issues.
- Do not add ARIA where native HTML suffices — bad ARIA is worse than no ARIA.
- Do not rely on color alone for meaning.
- Do not use `tabindex` values greater than 0.
- Do not hide elements from screen readers (`aria-hidden="true"`) while keeping them visible and focusable — it creates "phantom" focus.
- Do not accept "we'll fix it post-launch" for EAA-scope products after June 2025 — it's an enforcement risk.
- Do not confuse "WCAG compliant" with "accessible". Conformance is a floor.
