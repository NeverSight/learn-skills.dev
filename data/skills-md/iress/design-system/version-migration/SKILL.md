---
name: version-migration
description: Guide AI agents on migrating applications between IDS (Iress Design System) major versions — including v4→v5, v5→v6, and OUI→v6. Covers component renaming, prop changes, form architecture migration (Formik→React Hook Form), testing updates, and common gotchas.
---

# Skill: IDS Version Migration

## When to Use

- Migrating from IDS v5 (or v4) to IDS v6
- Migrating from OUI (`@iress/oui`) to IDS v6
- Updating imports from `@iress/components-react` to `@iress-oss/ids-components`
- Converting Formik forms to React Hook Form via `IressForm`/`IressFormField`
- Updating test files that use IDS v4 test utilities
- Reviewing migration PRs for correctness

## Decision Table: Which Migration Path?

| Current stack | Migration path                       | Complexity                        | Reference                                                 |
| ------------- | ------------------------------------ | --------------------------------- | --------------------------------------------------------- |
| OUI only      | OUI→v6 guide                         | High (form architecture change)   | [prop-renames.md](references/prop-renames.md)             |
| IDS v4 only   | v4→v6 guide                          | Medium (form architecture change) | [prop-renames.md](references/prop-renames.md)             |
| IDS v5 only   | v5→v6 guide                          | Low–Medium                        | [v5-to-v6-migration.md](references/v5-to-v6-migration.md) |
| OUI + IDS v4  | Both OUI→v6 and v4→v6 guides         | High (form architecture change)   | [prop-renames.md](references/prop-renames.md)             |
| OUI + IDS v5  | OUI→v6 guide + v5→v6 for IDS changes | High (form architecture change)   | [v5-to-v6-migration.md](references/v5-to-v6-migration.md) |

Full interactive guides with diff viewers are available in Storybook:

- [v4→v5 guide](https://main--691abcc79dfa560a36d0a74f.chromatic.com/?path=/docs/resources-migration-guides-from-v4-to-v5--docs)
- [v5→v6 guide](https://main--691abcc79dfa560a36d0a74f.chromatic.com/?path=/docs/resources-migration-guides-from-v5-to-v6--docs)
- [OUI→v6 guide](https://main--691abcc79dfa560a36d0a74f.chromatic.com/?path=/docs/resources-migration-guides-from-oui-to-v6--docs)

---

## Pre-Migration Assessment

Before starting migration, run these scripts (or perform checks manually):

1. **Identify current version**: `scripts/detect-version.sh` — detects IDS/OUI version and recommends migration path
2. **Audit component usage**: `scripts/audit-components.sh` — generates component usage report
3. **Check for deprecated props**: `scripts/find-deprecated-props.sh` — finds props that will break
4. **Check form architecture**: `scripts/find-formik.sh` — identifies Formik forms needing migration
5. **Check test patterns**: `scripts/find-test-utils.sh` — finds old test utilities
6. **Review custom CSS**: Search for `.oui-`, `.ids-`, or `iress-` class selectors that may break
7. **Setup VRT (recommended)**: `scripts/setup-playwright-vrt.sh` — generates Playwright visual regression tests
8. **Capture baseline screenshots**: Run VRT suite before migration to capture current state
9. **Create migration branch**: Ensure you can rollback if needed

---

## Quick Reference: Package Changes

### Import path

```ts
// ❌ Old (IDS v4)
import { IressButton } from '@iress/components-react';

// ❌ Old (OUI)
import { Button, Input } from '@iress/oui';

// ✅ IDS v6 (install with @alpha tag: npm install @iress-oss/ids-components@alpha)
import { IressButton, IressInput } from '@iress-oss/ids-components';
```

> **Important:** IDS v6 is currently in alpha. Install with the `@alpha` tag:
>
> ```bash
> npm install @iress-oss/ids-components@alpha
> npm install @iress-oss/ids-tokens@alpha  # if using tokens directly
> ```

### CSS entry point

```ts
// ✅ Required in your app entry point
import '@iress-oss/ids-components/dist/style.css';
```

### Token package

```ts
// ✅ Required for design tokens
import '@iress-oss/ids-tokens/build/css-vars.css';
import { cssVars } from '@iress-oss/ids-tokens';
```

---

## Key Migration Areas

### v5 → v6 Migration

For migrations specifically from IDS v5 to v6, see [references/v5-to-v6-migration.md](references/v5-to-v6-migration.md) for:

- Package and CSS import changes
- Component renames (`IressBadge` → `IressPill`, `IressFilter` → `IressDropdownMenu`, etc.)
- Prop changes by component (Button, Alert, Toggle, Field, Modal, Select)
- Icon migration (FontAwesome → Material Symbols)
- Form migration patterns

### Component renames

Components that changed names between versions (IDS and OUI → v6), plus removed and new components. See [references/component-renames.md](references/component-renames.md) for the full map.

Key renames: `IressBadge` → `IressPill`, `IressRichSelect` → `IressSelect`, `IressField` → `IressFormField`, `IressFilter` → `IressDropdownMenu`.

### Prop renames (CRITICAL — verified against source code)

Using old prop names will silently fail. See [references/prop-renames.md](references/prop-renames.md) for the complete table.

Most common renames:

| Component               | Old prop (OUI) | New prop (v6)  |
| ----------------------- | -------------- | -------------- |
| `Alert`                 | `context`      | `status`       |
| `Modal`                 | `onHide`       | `onShowChange` |
| `Fieldset`/`RadioGroup` | `legend`       | `label`        |
| `Label`                 | `optional`     | `required`     |

| Component (IDS v4/v5)      | Old prop     | New prop (v6)  |
| -------------------------- | ------------ | -------------- |
| `IressButton`              | `variant`    | `mode`         |
| `IressAlert`               | `variant`    | `status`       |
| `IressModal`               | `isOpen`     | `show`         |
| `IressModal`               | `onClose`    | `onShowChange` |
| `IressModal`               | `title`      | `heading`      |
| `IressPanel`               | `background` | `bg`           |
| `IressStack`/`IressInline` | `gutter`     | `gap`          |

### Form migration (Formik → React Hook Form)

The most significant architectural change. Forms use `IressForm` + `IressFormField` with `render` prop, replacing Formik's `<Field as={...}>` pattern. Yup schemas become per-field `rules` props.

See [references/form-migration.md](references/form-migration.md) for validation mapping, before/after examples, and common patterns.

Quick example:

```tsx
<IressForm defaultValues={{ email: '' }} onSubmit={handle}>
  <IressFormField
    name="email"
    label="Email"
    render={(props) => <IressInput {...props} type="email" />}
    rules={{ required: 'Required' }}
  />
  <IressButton type="submit" mode="primary">
    Submit
  </IressButton>
</IressForm>
```

### Testing migration

IDS v6 uses standard React Testing Library — no special test utilities. Replace `idsFireEvent` with `fireEvent`/`userEvent`, remove `mockLazyLoadedComponents`, prefer `getByRole`/`getByLabelText` over `getByTestId`.

See [references/testing-migration.md](references/testing-migration.md) for import changes, pattern mapping, config updates, and form test examples.

### Styling migration

OUI CSS classes and IDS v4 Stencil classes are removed. Use styling props (`p`, `m`, `bg`, `gap`, `scrollable`) or design tokens (`var(--iress-*)`). Declare `@layer` order if custom CSS is overridden.

See [references/styling-migration.md](references/styling-migration.md) for examples and AG Grid migration.

---

## Post-Migration Validation

After completing migration, run `scripts/validate-migration.sh` or verify manually:

1. **Automated checks**: Run validation script to check for common issues
2. **Visual regression**: Run VRT suite and review all visual diffs (see [references/visual-regression-testing.md](references/visual-regression-testing.md))
3. **Visual check**: All components render without console errors or warnings
4. **Form functionality**: Submit forms and verify validation rules work correctly
5. **Test suite**: All tests pass with new testing patterns (no `idsFireEvent`, etc.)
6. **Accessibility**: Keyboard navigation and screen reader functionality intact
7. **Styling**: No missing styles, check responsive breakpoints
8. **Interactive states**: Hover, focus, disabled, loading states work as expected
9. **Build**: Production build completes without errors, check bundle size

The validation script checks for:

- Old imports (`@iress/oui`, `@iress/components-react`)
- Old test utils (`idsFireEvent`, `mockLazyLoadedComponents`)
- Deprecated props (`variant=`, `isOpen=`, `gutter=`, etc.)
- Required CSS import
- Remaining Formik usage

---

## Common Gotchas

See [references/common-gotchas.md](references/common-gotchas.md) for a comprehensive troubleshooting guide covering:

- Critical breaking changes (missing CSS, validation, renamed props)
- IDS v4 React → v6 React gotchas (test utils, slots, helpers, icons)
- OUI-specific gotchas (prop renames, removed components)
- Component API changes (form fields, styling, composition patterns)
- Form architecture changes (Formik → React Hook Form)

---

## Cross-References

### Generated migration guides (read these for full details)

- **v4→v5** — `node_modules/@iress-oss/ids-components/.ai/guides/migration-guides-v5.md`
- **v5→v6** — `node_modules/@iress-oss/ids-components/.ai/guides/migration-guides-v6.md`
- **OUI→v6** — `node_modules/@iress-oss/ids-components/.ai/guides/migration-guides-oui.md`

### Component and pattern docs

- **Component docs** — `node_modules/@iress-oss/ids-components/.ai/components/`
- **Pattern docs** — `node_modules/@iress-oss/ids-components/.ai/patterns/`
- **Index** — `node_modules/@iress-oss/ids-components/.ai/index.json`

### Related skills

- **token-usage** — Design token usage patterns
- **ui-translation** — Building new IDS v6 UIs from scratch
- **ui-doctor** — Auditing IDS compliance

## Reference

- **Storybook and Guidelines:** https://main--691abcc79dfa560a36d0a74f.chromatic.com
