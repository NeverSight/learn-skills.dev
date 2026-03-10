---
name: ui-doctor
description: Audit and validate that an application correctly uses IDS (Iress Design System) components, follows IDS principles, and meets compliance requirements. This skill helps AI agents perform comprehensive UI reviews, identify areas where native HTML or third-party elements should be replaced with IDS components, assess adherence to IDS design principles, and produce actionable reports with recommendations.
---

# Skill: UI Doctor

Audit and validate that an application correctly uses IDS (Iress Design System) components, follows IDS principles, and meets compliance requirements. This skill helps AI agents perform comprehensive UI reviews, identify areas where native HTML or third-party elements should be replaced with IDS components, assess adherence to IDS design principles, and produce actionable reports with recommendations.

## When to Use

- Reviewing an application's UI code for IDS compliance
- Validating that IDS components are used where possible instead of raw HTML or custom implementations
- Assessing design token usage and consistency
- Generating a UI health report with an IDS compliance score
- Providing recommendations to improve IDS adoption and consistency

## Audit Scope

Before starting the audit, determine which files to scan and which to exclude.

### Files to Scan

- All `.tsx`, `.jsx`, `.ts`, `.js` files in `src/` (or the application source directory)
- CSS/SCSS/styled-component files for hardcoded design values
- Application entry point(s) for Provider and CSS import checks

### Files to Exclude

- **Test files** (`*.test.tsx`, `*.spec.tsx`, `__tests__/`) — test mocks and utilities may legitimately use raw HTML
- **Storybook stories** (`*.stories.tsx`) — stories may intentionally demonstrate raw HTML for comparison
- **Configuration files** (`*.config.ts`, `*.config.js`) — not UI code
- **Type definition files** (`*.d.ts`) — no runtime UI code
- **Third-party code** (`node_modules/`, vendored libraries) — outside the application's control
- **Build output** (`dist/`, `build/`) — generated code

### Version-Aware Auditing

IDS is currently on **version 6**. When auditing applications:

- **Check the installed IDS version** — Look at `package.json` for `@iress-oss/ids-components` version
- **v6 applications** — Apply all rules in this skill as-is
- **v5 applications** — Some patterns differ (e.g., `IressForm` API changes between v5 and v6). Flag v5-specific patterns as "migration opportunities" rather than "non-compliant". Key v5→v6 differences include:
  - `IressForm` now uses `rules` prop for validation instead of built-in validation props
  - `react-hook-form` is now a peer dependency
  - Form state management moved from `useState` to React Hook Form's `useWatch`/`ref`
- **Pre-v5 applications** — Flag as requiring a major migration and prioritise Provider/CSS setup first
- **Always note the version** in the audit report header

## Audit Process

### 1. Validate IDS Component Usage

Scan the application code for raw HTML elements, third-party UI components, and custom implementations that have IDS equivalents. Flag instances where IDS components should be used instead.

#### Third-Party UI Library Detection

Check for imports from third-party UI libraries that overlap with IDS. Common libraries to flag:

| Third-Party Library                 | Common Imports to Flag                                    | IDS Replacement                |
| ----------------------------------- | --------------------------------------------------------- | ------------------------------ |
| Material UI (`@mui/*`)              | `Button`, `TextField`, `Select`, `Modal`, `Table`, `Tabs` | Equivalent `Iress*` components |
| Ant Design (`antd`)                 | `Button`, `Input`, `Select`, `Modal`, `Table`, `Tabs`     | Equivalent `Iress*` components |
| Chakra UI (`@chakra-ui/*`)          | `Button`, `Input`, `Select`, `Modal`, `Table`             | Equivalent `Iress*` components |
| React Bootstrap (`react-bootstrap`) | `Button`, `Form`, `Modal`, `Table`, `Nav`                 | Equivalent `Iress*` components |
| Radix UI (`@radix-ui/*`)            | `Dialog`, `Popover`, `Tooltip`, `Tabs`, `Select`          | Equivalent `Iress*` components |
| Headless UI (`@headlessui/react`)   | `Dialog`, `Popover`, `Menu`, `Tab`, `Switch`              | Equivalent `Iress*` components |

**How to detect:** Search for import statements matching these package names. Any UI component imported from a third-party library that has an IDS equivalent should be flagged as a **High** priority replacement.

```typescript
// ❌ Third-party UI component — should use IDS
import { Button } from '@mui/material';
import { Modal } from 'antd';
import { Dialog } from '@radix-ui/react-dialog';

// ✅ IDS components
import { IressButton, IressModal } from '@iress-oss/ids-components';
```

#### HTML Element → IDS Component Replacement Map

| Raw HTML / Custom Code                  | IDS Replacement                                       | Priority |
| --------------------------------------- | ----------------------------------------------------- | -------- |
| `<button>`                              | `IressButton`                                         | High     |
| `<a>` (navigation link)                 | `IressLink`                                           | High     |
| `<input type="text">`                   | `IressField` + `IressInput`                           | High     |
| `<input type="checkbox">`               | `IressCheckbox`                                       | High     |
| `<input type="radio">`                  | `IressRadio` + `IressRadioGroup`                      | High     |
| `<select>`                              | `IressField` + `IressSelect`                          | High     |
| `<textarea>`                            | `IressField` + `IressInput`                           | High     |
| `<table>`                               | `IressTable`                                          | High     |
| `<label>`                               | `IressField` (wraps input with label)                 | High     |
| `<h1>`–`<h6>`, `<p>`, `<span>` (styled) | `IressText`                                           | Medium   |
| `<img>`                                 | `IressImage`                                          | Medium   |
| `<hr>`                                  | `IressDivider`                                        | Medium   |
| `<dialog>` / custom modal               | `IressModal`                                          | High     |
| Custom confirmation / danger dialog     | `IressModal status="danger"` (or `success`/`warning`) | High     |
| Custom drawer / slideout                | `IressSlideout`                                       | High     |
| Custom tooltip                          | `IressTooltip`                                        | Medium   |
| Custom popover                          | `IressPopover`                                        | Medium   |
| Custom tabs                             | `IressTabSet` + `IressTab`                            | High     |
| Custom spinner / loader                 | `IressSpinner`                                        | Medium   |
| Custom skeleton loader                  | `IressSkeleton`                                       | Low      |
| Custom progress bar                     | `IressProgress`                                       | Low      |
| Custom alert / toast                    | `IressAlert` / `IressToaster`                         | High     |
| Custom card / panel                     | `IressCard` / `IressPanel`                            | Medium   |
| Custom toggle / switch                  | `IressToggle`                                         | High     |
| Custom badge / tag                      | `IressTag` / `IressPill`                              | Low      |
| Custom breadcrumbs                      | `IressBreadcrumbs`                                    | Medium   |
| Custom side navigation                  | `IressSideNav`                                        | Medium   |
| Custom context menu                     | `IressMenu` + `IressMenuItem`                         | Medium   |
| Custom icon (SVG inline)                | `IressIcon`                                           | Medium   |
| `<div>` with flex column styles         | `IressStack`                                          | Medium   |
| `<div>` with flex row styles            | `IressInline`                                         | Medium   |
| `<div>` with grid styles                | `IressRow` + `IressCol`                               | Medium   |
| `<div>` with max-width container        | `IressContainer`                                      | Low      |
| `<form>`                                | `IressForm` + `IressFormField`                        | High     |
| `<input type="range">`                  | `IressSlider`                                         | Medium   |
| `<input type="number">` (currency)      | `IressField` + `IressInputCurrency`                   | Medium   |
| `<details>` / custom accordion          | `IressExpander`                                       | Medium   |
| Custom autocomplete / typeahead         | `IressAutocomplete`                                   | High     |
| Custom select with search               | `IressField` + `IressSelect`                          | High     |
| Custom read-only display                | `IressReadonly`                                       | Medium   |
| Custom segmented control / button group | `IressButtonGroup`                                    | Medium   |
| Custom validation messages              | `IressValidationMessage` / `IressValidationSummary`   | High     |
| Custom styled wrapper `<div>`           | `IressStyled`                                         | Low      |

#### What to Look For

```typescript
// ❌ Raw HTML — should use IDS components
<button onClick={handleClick}>Submit</button>
<input type="text" placeholder="Name" />
<select>
  <option>Option 1</option>
</select>
<div className="modal-overlay">...</div>
<div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>...</div>

// ✅ IDS components
<IressButton mode="primary" onClick={handleClick}>Submit</IressButton>
<IressField label="Name" htmlFor="name">
  <IressInput id="name" placeholder="Name" />
</IressField>
<IressField label="Options" htmlFor="options">
  <IressSelect id="options">
    <option>Option 1</option>
  </IressSelect>
</IressField>
<IressModal open={isOpen} onClose={handleClose}>...</IressModal>
<IressStack gap="4">...</IressStack>
```

### 2. Validate IDS Principles and Compliance

Check that the application follows these core IDS principles:

#### a. Provider & CSS Setup

- **IressProvider must wrap the application root** — Required for fonts, CSS variables, and theming
- **The IDS component CSS must be imported** — `@iress-oss/ids-components/dist/style.css` contains all component styles
- Users only need to install `@iress-oss/ids-components` — the tokens are bundled within the component library and do not need to be installed separately
- If using design tokens directly in application code (for custom styling), users should additionally install `@iress-oss/ids-tokens` and import `@iress-oss/ids-tokens/build/css-vars.css`

```typescript
// ✅ Correct setup — minimum required
import '@iress-oss/ids-components/dist/style.css';
import { IressProvider } from '@iress-oss/ids-components';

function App() {
  return <IressProvider>{/* app content */}</IressProvider>;
}
```

```typescript
// ✅ With direct token usage in application code (optional)
import '@iress-oss/ids-components/dist/style.css';
import '@iress-oss/ids-tokens/build/css-vars.css';
import { IressProvider } from '@iress-oss/ids-components';
import { cssVars } from '@iress-oss/ids-tokens';

function App() {
  return (
    <IressProvider>
      <div style={{ padding: cssVars.spacing[4] }}>{/* app content */}</div>
    </IressProvider>
  );
}
```

```typescript
// ❌ Incorrect — missing component CSS
import { IressProvider } from '@iress-oss/ids-components';
// Components will render without styles!

// ❌ Incorrect — installing tokens separately just for provider setup
yarn add @iress-oss/ids-tokens  // Not needed unless using tokens directly
```

#### b. Design Token Usage

- **Hardcoded colour values** — Flag any hex codes, rgb(), or named colours that should use IDS tokens
- **Hardcoded spacing** — Flag pixel values for padding/margin/gap that should use spacing tokens (multiples of 4px)
- **Hardcoded typography** — Flag font-family, font-size, font-weight that should use IDS typography tokens
- **Hardcoded border-radius** — Flag radius values that should use IDS radius tokens

```typescript
// ❌ Hardcoded values
<div style={{ color: '#003271', padding: '16px', borderRadius: '4px' }}>

// ✅ IDS tokens
import { cssVars } from '@iress-oss/ids-tokens';
<div style={{
  color: cssVars.colour.primary.fill,
  padding: cssVars.spacing[4],
  borderRadius: cssVars.radius[1]
}}>
```

#### c. Form & Pattern Compliance

IDS provides several patterns (composite components) that ensure consistent UIs across applications. Validate that the application uses these patterns where appropriate.

##### Form Pattern (`IressForm`)

Forms should use `IressForm` and `IressFormField` instead of building custom form handling. This ensures consistent validation, error display, and state management.

- **Use `IressForm` for all forms** — Built on React Hook Form, it provides consistent validation, error handling, and state management
- **Use `IressFormField` for form fields** — Wraps form controls with `name`, `label`, and `rules` props for declarative validation
- **Use `IressFormFieldset` for grouped inputs** — For checkbox groups, radio groups, and other multi-input fields
- **Use `rules` prop for validation** — Declarative validation via React Hook Form rules, not custom validation logic
- **Use `onSubmit` for state syncing** — Sync form data with external state via the submit event, not per-field `onChange`
- **Use `useWatch` for conditional fields** — Not `useState` + `onChange` handlers
- **Choose the right form pattern** — Use `pattern="long"` for forms with >8 fields (sticky heading/actions), `pattern="short"` (default) for ≤8 fields
- **Use `react-hook-form` as a peer dependency** — Required alongside `@iress-oss/ids-components` when using `IressForm`

```typescript
// ❌ Custom form handling
<form onSubmit={handleSubmit}>
  <label>Email</label>
  <IressInput value={email} onChange={(e) => setEmail(e.target.value)} />
  {emailError && <span className="error">{emailError}</span>}
  <button type="submit">Submit</button>
</form>

// ✅ IDS Form pattern
<IressForm onSubmit={handleSubmit} heading="Contact" actions={<IressButton mode="primary" type="submit">Submit</IressButton>}>
  <IressFormField
    name="email"
    label="Email"
    rules={{ required: true, pattern: { value: /^[^@]+@[^@]+$/, message: 'Invalid email' } }}
    render={(controlledProps) => <IressInput {...controlledProps} type="email" />}
  />
</IressForm>
```

##### Loading Pattern (`IressLoading`)

Applications should use `IressLoading` for all loading states to ensure consistent timing behaviour and user experience.

- **Use `IressLoading` instead of custom spinners/skeletons** — It handles timing thresholds automatically (no indicator <500ms, spinner at 500ms, message at 2s, detailed feedback at 10s)
- **Choose the right loading pattern** — `page` for page loads, `component` for component loads, `start-up` for app initialisation, `validate` for form submission, `long` for operations >10s
- **Be consistent** — Use the same loading pattern for similar operations across the application

##### Dropdown Menu Pattern (`IressDropdownMenu`)

- **Use `IressDropdownMenu` for filter/action triggers** — Not custom popover menus
- **Do not use inside forms** — Use `IressSelect`, `IressRadioGroup`, or `IressCheckboxGroup` within forms instead
- **Enable `searchable` for 10+ options** — Improves usability for long option lists

##### Contextual Menu Pattern (`IressContextualMenu`)

- **Use for row-level or card-level secondary actions** — Not custom context menus
- **Place destructive actions at the end** — Follow the established convention
- **Provide meaningful `ariaLabel`** — Describe the menu purpose in context

##### Side Navigation Pattern (`IressSideNav`)

- **Use for application shell navigation** — Not custom sidebar implementations
- **Use for multi-section apps** — When the application has several major sections with sub-navigation

##### Breadcrumbs Pattern (`IressBreadcrumbs`)

- **Use for site hierarchy navigation** — Not custom breadcrumb implementations
- **Last item should represent current page** — And not be clickable

##### Shadow DOM Pattern (`IressShadow`)

- **Use for microfrontend isolation** — When you need to isolate styles from the host application
- **Alternative to `IressProvider`** — Injects styles into the shadow DOM instead of the document head

##### Form Accessibility

- **All form inputs must have labels** — Use `IressField` (standalone inputs) or `IressFormField` (within `IressForm`) to provide labels, hints, and validation
- **Required fields must be marked** — Use `required` prop on `IressField` or `rules={{ required: true }}` on `IressFormField`
- **Validation messages must use IDS patterns** — Use `IressField` `status` and `statusMessage` props, or `IressFormField` `rules` prop for declarative validation
- **Form inputs must have `id` and `htmlFor` pairing** — For label association when using `IressField` directly

```typescript
// ❌ Missing label / accessibility
<IressInput placeholder="Email" />

// ✅ Accessible standalone form input
<IressField label="Email" htmlFor="email" required>
  <IressInput id="email" type="email" placeholder="Enter your email" />
</IressField>

// ✅ Accessible form input within IressForm
<IressFormField
  name="email"
  label="Email"
  rules={{ required: true }}
  render={(controlledProps) => <IressInput {...controlledProps} type="email" />}
/>
```

#### d. Button Hierarchy

- **One primary action per section** — Only one `mode="primary"` button per logical section
- **Consistent button mode usage** — Primary for main action, secondary for supporting actions, tertiary/muted for less prominent actions
- **Danger actions use status prop** — `status="danger"` for destructive actions, not red styling

#### e. Layout Consistency

- **Use IDS layout components** — `IressStack`, `IressInline`, `IressRow`/`IressCol` instead of custom CSS flex/grid
- **Use spacing tokens for gaps** — Values 0–10 on `gap` prop
- **Use IressCSSProps for spacing** — `m`, `mx`, `my`, `p`, `px`, `py` props instead of inline styles
- **Responsive design** — Use `IressHide`, `hideFrom`/`hideBelow` for responsive visibility

#### f. Semantic Component Usage

- **Use `IressText` for all text** — Instead of raw `<p>`, `<span>`, `<h1>`–`<h6>` (unless nested inside `IressText` for styling)
- **Use `IressAlert` for feedback** — Instead of custom notification/alert components
- **Use `IressModal status` for confirmation dialogs** — Instead of custom danger/success/warning confirmation modals. Use the `actions` prop for buttons (`footer` is not available when `status` is set)
- **Use `IressIcon` for icons** — Instead of inline SVGs or custom icon components (unless the icon is a hero graphic that doesn't fit the standard icon use case)
- **Use `IressDivider` for separators** — Instead of `<hr>` or custom dividers (unless nested inside `IressText` for inline separation)

#### g. Acceptable Exceptions

Not every raw HTML element is a violation. The following are **acceptable exceptions** that should NOT be flagged:

| Pattern                                                      | Why It's Acceptable                                                                                                                     |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `<a>` inside markdown/MDX renderers                          | Content-driven, not application UI                                                                                                      |
| `<button>` inside third-party widgets the app cannot control | External dependency constraint                                                                                                          |
| `<table>` in email templates                                 | Email clients don't support custom components                                                                                           |
| `<img>` in SVG sprites or `<picture>` elements               | IressImage doesn't cover these use cases                                                                                                |
| `<div>` for ref targets, portals, or measurement containers  | Technical necessity, not layout                                                                                                         |
| Raw elements in test files / stories for demonstration       | Not shipped to users                                                                                                                    |
| `<form>` wrapping a single action (e.g., search bar)         | `IressForm` is best for multi-field forms; standalone search inputs may use `IressAutocomplete` or `IressField` + `IressInput` directly |
| `<input type="hidden">`                                      | Not user-facing UI                                                                                                                      |
| Custom components wrapping IDS components internally         | App-level abstraction is valid as long as IDS components are used underneath                                                            |

**When reporting:** If a potential violation falls into an exception category, note it as "Reviewed — Acceptable Exception" rather than a finding. This prevents false positives and keeps reports actionable.

### 3. Provide Recommendations

Based on the audit findings, provide prioritised recommendations:

#### Priority Levels

| Priority     | Description                                                                                                                                                                                                      | Action                |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **Critical** | Missing IressProvider, missing component CSS import, raw form inputs without labels, missing skip links, forms not using `IressForm`                                                                             | Must fix immediately  |
| **High**     | Raw HTML buttons/inputs/selects/tables/modals, custom form handling instead of `IressForm`, custom loading instead of `IressLoading`, accessibility failures (colour contrast, missing alt text, focus trapping) | Fix in current sprint |
| **Medium**   | Hardcoded colours/spacing, missing IressText usage, custom layout instead of IDS layout, custom menus instead of `IressContextualMenu`/`IressDropdownMenu`, missing ARIA landmarks                               | Plan for next sprint  |
| **Low**      | Missing IressImage, custom badges, minor token inconsistencies, non-critical accessibility improvements                                                                                                          | Backlog               |

#### Recommendation Format

For each finding, provide:

1. **What was found** — The specific code or pattern that needs attention
2. **Why it matters** — Impact on consistency, accessibility, or maintainability
3. **How to fix** — Specific code change with before/after examples
4. **Priority** — Critical, High, Medium, or Low

### 4. Generate Compliance Report

Produce a structured report covering all audit areas. Use the [report template](references/report-template.md) to structure the output.

## Audit Checklist

Use the [full audit checklist](references/audit-checklist.md) when performing a UI doctor audit. It covers setup & configuration, component usage, design tokens, pattern usage, accessibility, layout, button hierarchy, and usability heuristics (based on Nielsen's 10 heuristics).

## Example Audit Output

### Quick Scan Summary

```
IDS UI Doctor — Quick Scan
================================
Files scanned:     42
Components found:  18 IDS / 7 raw HTML
Patterns used:     3/7 available
Token compliance:  73%
Accessibility:     82%

Top Issues:
  ⚠ 3× raw <button> found (should be IressButton)
  ⚠ 2× hardcoded colours found (#333, #f5f5f5)
  ⚠ 1× <input> without IressField wrapper
  ⚠ 2× custom <form> found (should use IressForm)
  ⚠ 1× custom loading spinner (should use IressLoading)
  ⚠ 1× missing skip link for keyboard navigation
  ✓ IressProvider correctly configured
  ✓ Component CSS imported
  ✓ IressBreadcrumbs used for navigation hierarchy
  ✓ Colour contrast passes WCAG AA
```

## Reference

> **Note:** Component docs, pattern docs, and the manifest are within the package itself.

- **Component docs:** `node_modules/@iress-oss/ids-components/.ai/components/`
- **Pattern docs:** `node_modules/@iress-oss/ids-components/.ai/patterns/`
- **Index (full component list):** `node_modules/@iress-oss/ids-components/.ai/index.json`
- **Token usage skill:** `.agents/skills/token-usage/SKILL.md`
- **Figma mapping skill:** `.agents/skills/figma-to-ids/SKILL.md`
- **UI translation skill:** `.agents/skills/ui-translation/SKILL.md`
- **Storybook and Guidelines:** https://main--691abcc79dfa560a36d0a74f.chromatic.com
