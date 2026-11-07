---
name: create-component
description: Generate a React component following DaaS platform patterns. Performs mandatory Buildpad-first check before creating any custom component. Use when the user needs a new React component, page section, or UI element for a DaaS application.
argument-hint: "[component name] [type: form|list|modal|card|detail]"
---

# Create React Component

Generate a React component following DaaS platform patterns.

> **BEFORE generating ANY `.tsx` files**, you MUST `read_file` the Buildpad component reference at `.github/skills/buildpad-reference/SKILL.md`. This loads the full 40+ component catalog with import paths and usage patterns. Skipping this step leads to raw Mantine usage violations.

## STOP: Buildpad-First Check (MANDATORY)

Before creating ANY component, verify it's not already in Buildpad (40+ components):

| Component Type   | Buildpad Alternative                                       |
| ---------------- | ---------------------------------------------------------- |
| Text input       | `Input`, `Textarea`, `InputCode`                           |
| Rich text editor | `RichTextHtml`, `RichTextMarkdown`, `InputBlockEditor`     |
| Select/Dropdown  | `SelectDropdown`, `SelectRadio`                            |
| Multi-select     | `SelectMultipleDropdown`, `SelectMultipleCheckbox`, `Tags` |
| Toggle/Switch    | `Toggle`, `Boolean`                                        |
| Date picker      | `DateTime`                                                 |
| File upload      | `FileInterface`, `FileImage`, `Files`, `Upload`            |
| Color picker     | `Color`                                                    |
| Relation picker  | `ListM2O`, `ListM2M`, `ListO2M`, `ListM2A`                 |
| Dynamic form     | `VForm`, `CollectionForm`                                  |
| List/Table       | `CollectionList` (search, filter, permissions, pagination) |
| Filtering        | `FilterPanel` (DaaS-compatible filter builder)             |
| Workflow buttons | `WorkflowButton`                                           |
| Layout elements  | `Divider`, `Notice`, `GroupDetail`                         |

**If Buildpad has it** → Use `/add-buildpad` skill instead. Do NOT proceed with custom creation.

## CollectionList Usage (MANDATORY for any record listing)

When creating a page or module that displays collection records in a list/table, you MUST use `CollectionList`.
`CollectionList` provides: search, integrated FilterPanel toggle with badge, permission-gated create button,
bulk actions with `requiredPermission` gating, pagination (25/50/100/250), and column management.
See `create-collection` skill for the full-featured code pattern.

## VForm Usage (CRITICAL)

When creating form pages that use `VForm`, you MUST follow the controlled component pattern.
See the create-feature skill's [VForm usage reference](../create-feature/references/vform-usage.instructions.md).

**VForm has NO `onSubmit` prop.** Pass `modelValue` + `onUpdate` and handle submission externally.

## Allowed Custom Components

- App-specific navigation, sidebars, headers
- Custom dashboards and data visualizations
- Composite components combining multiple Buildpad components
- Specialized displays not covered by Buildpad

## Component Standards

- TypeScript strict mode with proper interfaces
- JSDoc documentation on exported functions
- `'use client'` directive for client components
- **`'use client'` is REQUIRED for ANY component that uses Mantine** — Mantine compound components (`Table.Tbody`, `Table.Tr`, `Modal`, `Tabs.Panel`, etc.) resolve to `undefined` in React Server Components and crash at runtime (Bug 10). When data fetching is needed in a server component, fetch server-side and pass data as props to a `'use client'` child component.
- Mantine layout components (`Stack`, `Group`, `Button`, `Modal`, `Table`) are fine to use directly
- Import Buildpad components from `@/components/ui/`
- Import hooks from `@/lib/buildpad/hooks`
- Import types from `@/lib/buildpad/types`

## Required Tests

Create `tests/components/[name].spec.ts` with:

- Component renders without errors
- Displays expected content
- User interactions work (click, type, submit)
- Form validation (if applicable)
- Loading/error/empty states display correctly

## Post-Generation Validation (MANDATORY)

After generating the component, run the Buildpad-First violation check:

```bash
# Scan generated files for forbidden raw Mantine form/input imports
grep -rn "from '@mantine/form'\|from '@mantine/dates'\|from '@mantine/dropzone'\|<TextInput\|<NumberInput\|<Select \|<Switch \|<Checkbox \|<DatePicker\|<Dropzone" app/ components/ 2>/dev/null
```

**If any matches are found, replace them with Buildpad equivalents before proceeding.**

Quick fix reference:
| Violation | Replace With |
|---|---|
| `<TextInput>` / `<Textarea>` | `Input` / `Textarea` from `@/components/ui` |
| `<Select>` | `SelectDropdown` from `@/components/ui` |
| `<DatePicker>` | `DateTime` from `@/components/ui` |
| `<Switch>` / `<Checkbox>` | `Toggle` / `Boolean` / `SelectMultipleCheckbox` |
| `<Dropzone>` | `Upload` / `Files` from `@/components/ui` |
| `useForm` (@mantine/form) | `VForm` or `CollectionForm` from `@/components/ui` |
| Custom `<Table>` for records | `CollectionList` from `@/components/ui` |
