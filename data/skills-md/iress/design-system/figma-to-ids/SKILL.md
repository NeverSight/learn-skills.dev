---
name: figma-to-ids
description: Translate Figma design properties and structures into IDS (Iress Design System) component implementations. This skill helps AI agents interpret Figma design metadata (from tools like Figma MCP or exported design specs) and produce accurate IDS code.
---

# Skill: Figma to IDS Translation

## Purpose

Translate Figma design properties and structures into IDS (Iress Design System) component implementations. This skill helps AI agents interpret Figma design metadata (from tools like Figma MCP or exported design specs) and produce accurate IDS code.

## Process

1. **Analyse Figma structure** — Identify frames, auto-layout, and component instances
2. **Map components** — Match Figma component names/variants to IDS components
3. **Extract tokens** — Convert Figma design values to IDS design token references
4. **Generate code** — Produce clean React/TypeScript with proper IDS imports

## Figma Component → IDS Component Mapping

### Auto-Layout → Layout Components

| Figma Property           | IDS Component                       | Notes                               |
| ------------------------ | ----------------------------------- | ----------------------------------- |
| Auto-layout (vertical)   | `IressStack`                        | Default direction is vertical       |
| Auto-layout (horizontal) | `IressInline`                       | Horizontal flow with wrapping       |
| Auto-layout gap          | `gap` prop                          | Map px to spacing token (see below) |
| Auto-layout padding      | `p`, `px`, `py` props               | Map px to spacing token             |
| Auto-layout alignment    | `horizontalAlign` / `verticalAlign` | Maps to start, center, end          |
| Grid layout              | `IressRow` + `IressCol`             | Use `span` prop for column widths   |

### Component Instances

| Figma Component    | IDS Component                                | Key Props                  |
| ------------------ | -------------------------------------------- | -------------------------- |
| Button / Primary   | `IressButton mode="primary"`                 |                            |
| Button / Secondary | `IressButton mode="secondary"`               |                            |
| Button / Tertiary  | `IressButton mode="tertiary"`                |                            |
| Button / Muted     | `IressButton mode="muted"`                   |                            |
| Button / Danger    | `IressButton mode="primary" status="danger"` |                            |
| Button / Icon Only | `IressButton icon="..." mode="muted"`        | Set icon name              |
| Input / Text       | `IressField` + `IressInput`                  | label, placeholder         |
| Input / Currency   | `IressField` + `IressInputCurrency`          | label                      |
| Select / Dropdown  | `IressField` + `IressSelect`                 | label, options             |
| Checkbox           | `IressCheckbox`                              | label                      |
| Checkbox Group     | `IressCheckboxGroup` + `IressCheckbox`s      | label                      |
| Radio Group        | `IressRadioGroup` + `IressRadio`s            | label                      |
| Toggle             | `IressToggle`                                | label                      |
| Card               | `IressCard`                                  | Header, Body, Footer slots |
| Panel              | `IressPanel`                                 |                            |
| Alert / Success    | `IressAlert status="success"`                |                            |
| Alert / Danger     | `IressAlert status="danger"`                 |                            |
| Alert / Warning    | `IressAlert status="warning"`                |                            |
| Alert / Info       | `IressAlert status="info"`                   |                            |
| Modal              | `IressModal`                                 |                            |
| Modal / Danger     | `IressModal status="danger"`                 | actions, size sm/md only   |
| Modal / Success    | `IressModal status="success"`                | actions, size sm/md only   |
| Modal / Warning    | `IressModal status="warning"`                | actions, size sm/md only   |
| Slideout / Drawer  | `IressSlideout`                              |                            |
| Tabs               | `IressTabSet` + `IressTab`                   |                            |
| Table              | `IressTable`                                 | Head, Body, Row, Cell      |
| Tag                | `IressTag`                                   | clickable variant          |
| Pill               | `IressPill`                                  |                            |
| Tooltip            | `IressTooltip`                               |                            |
| Icon               | `IressIcon name="..."`                       | Material Symbols name      |
| Divider            | `IressDivider`                               |                            |
| Spinner            | `IressSpinner`                               |                            |
| Skeleton           | `IressSkeleton`                              |                            |
| Progress           | `IressProgress`                              |                            |
| Breadcrumbs        | `IressBreadcrumbs`                           | items array                |
| Menu               | `IressMenu` + `IressMenuItem`                |                            |
| Side Navigation    | `IressSideNav`                               |                            |

## Figma Design Values → IDS Token Mapping

### Colours

Map Figma fill/stroke colours to IDS colour tokens:

| Figma Colour              | IDS Token                    | CSS Variable                         |
| ------------------------- | ---------------------------- | ------------------------------------ |
| Primary/Fill `#003271`    | `colour.primary.fill`        | `--iress-colour-primary-fill`        |
| Primary/Surface `#EBF3FF` | `colour.primary.surface`     | `--iress-colour-primary-surface`     |
| Neutral/10 `#FFFFFF`      | `colour.neutral.10`          | `--iress-colour-neutral-10`          |
| Neutral/20 `#F5F6F8`      | `colour.neutral.20`          | `--iress-colour-neutral-20`          |
| Neutral/30 `#E2E6EA`      | `colour.neutral.30`          | `--iress-colour-neutral-30`          |
| Neutral/80 `#384666`      | `colour.neutral.80`          | `--iress-colour-neutral-80`          |
| Neutral/90 `#141F4D`      | `colour.neutral.90`          | `--iress-colour-neutral-90`          |
| Success/Fill `#37C49C`    | `colour.system.success.fill` | `--iress-colour-system-success-fill` |
| Danger/Fill `#C21010`     | `colour.system.danger.fill`  | `--iress-colour-system-danger-fill`  |
| Warning/Fill `#F0AD03`    | `colour.system.warning.fill` | `--iress-colour-system-warning-fill` |
| Info/Fill `#669AFF`       | `colour.system.info.fill`    | `--iress-colour-system-info-fill`    |
| Accent/Fill `#C26EF4`     | `colour.accent.fill`         | `--iress-colour-accent-fill`         |

### Spacing (px → Token)

IDS base spacing unit = 4px (0.25rem). Map Figma pixel values:

| Figma px | IDS Token | Alias |
| -------- | --------- | ----- |
| 0px      | `0`       | none  |
| 4px      | `1`       | xs    |
| 8px      | `2`       | sm    |
| 12px     | `3`       | —     |
| 16px     | `4`       | md    |
| 20px     | `5`       | —     |
| 24px     | `6`       | lg    |
| 28px     | `7`       | —     |
| 32px     | `8`       | —     |
| 40px     | `10`      | xl    |

> For values not on the 4px grid, round to the nearest token value.

### Border Radius

| Figma px | IDS Token  | System Usage        |
| -------- | ---------- | ------------------- |
| 0px      | `radius.0` | Square corners      |
| 4px      | `radius.1` | Button, form, tag   |
| 8px      | `radius.2` | —                   |
| 12px     | `radius.3` | Layout, card, panel |
| 16px     | `radius.4` | Pill, badge         |

### Typography

| Figma Text Style                   | IDS Token                    | Component                               |
| ---------------------------------- | ---------------------------- | --------------------------------------- |
| Heading / H1 (Ubuntu 24px/500)     | `typography.heading.1`       | `<IressText element="h1">`              |
| Heading / H2 (Ubuntu 20px/500)     | `typography.heading.2`       | `<IressText element="h2">`              |
| Heading / H3 (Ubuntu 18px/500)     | `typography.heading.3`       | `<IressText element="h3">`              |
| Heading / H4 (Ubuntu 16px/500)     | `typography.heading.4`       | `<IressText element="h4">`              |
| Heading / H5 (Ubuntu 16px/400)     | `typography.heading.5`       | `<IressText element="h5">`              |
| Body / MD Regular (Inter 14px/400) | `typography.body.md.regular` | `<IressText>` (default)                 |
| Body / MD Medium (Inter 14px/500)  | `typography.body.md.medium`  | `<IressText weight="medium">`           |
| Body / MD Strong (Inter 14px/600)  | `typography.body.md.strong`  | `<IressText weight="strong">`           |
| Body / SM Regular (Inter 12px/400) | `typography.body.sm.regular` | `<IressText size="sm">`                 |
| Body / SM Strong (Inter 12px/600)  | `typography.body.sm.strong`  | `<IressText size="sm" weight="strong">` |
| Code (Space 16px/400)              | `typography.code`            | `<IressText element="code">`            |

## Translation Examples

### Figma: Login Form Frame

**Figma structure:**

- Frame: Auto-layout vertical, gap 16px, padding 24px
  - Text: "Log In" (Heading H2)
  - Input: "Email" (Text Input)
  - Input: "Password" (Password Input)
  - Button: "Sign in" (Primary)
  - Text: "Forgot password?" (Link)

**IDS implementation:**

```tsx
import {
  IressStack,
  IressText,
  IressField,
  IressInput,
  IressButton,
  IressLink,
  IressCard,
} from '@iress-oss/ids-components';

function LoginForm() {
  return (
    <IressCard p="6">
      <IressStack gap="4">
        <IressText element="h2">Log In</IressText>
        <IressField label="Email" htmlFor="email" required>
          <IressInput id="email" type="email" />
        </IressField>
        <IressField label="Password" htmlFor="password" required>
          <IressInput id="password" type="password" />
        </IressField>
        <IressButton mode="primary" type="submit">
          Sign in
        </IressButton>
        <IressLink href="/forgot-password">Forgot password?</IressLink>
      </IressStack>
    </IressCard>
  );
}
```

### Figma: Alert Banner

**Figma structure:**

- Frame: Fill `#EBF9F5`, border-radius 12px, padding 16px
  - Auto-layout horizontal, gap 8px
  - Icon: "check_circle"
  - Text: "Your changes have been saved" (Body MD)

**IDS implementation:**

```tsx
import { IressAlert } from '@iress-oss/ids-components';

// IressAlert already handles the layout, icon, and styling
<IressAlert status="success">Your changes have been saved</IressAlert>;
```

> **Key insight:** IDS components encapsulate their styling. Don't recreate layout/colours from Figma — use the component's props (like `status`) and let IDS handle the visual treatment.

### Figma: Status Modal (Danger Confirmation)

**Figma structure:**

- Modal frame with danger icon in header
  - Heading: "Delete record?"
  - Body text: "This action cannot be undone."
  - Footer: Two buttons (Cancel, Delete)

**IDS implementation:**

```tsx
import { IressModal } from '@iress-oss/ids-components';

// Status modals use the `status` prop — the icon, colours, and button status are handled automatically.
// Use `actions` instead of `footer` for opinionated action buttons.
<IressModal
  status="danger"
  heading="Delete record?"
  actions={[{ children: 'Cancel', mode: 'tertiary' }, { children: 'Delete' }]}
  show={isOpen}
  onShowChange={setIsOpen}
>
  This action cannot be undone.
</IressModal>;
```

> **Key insight:** When `status` is set on `IressModal`, the `footer` prop is not available — use `actions` instead. Each action button automatically inherits the modal's status. Size is restricted to `sm` (default) or `md`.

### Figma: Data Table

**Figma structure:**

- Frame: Table with header row and data rows
  - Header: ["Name", "Email", "Status", "Actions"]
  - Rows: data with tag in Status column, button in Actions

**IDS implementation:**

```tsx
import { IressTable, IressTag, IressButton } from '@iress-oss/ids-components';

function UsersTable({ users }) {
  return (
    <IressTable>
      <IressTable.Head>
        <IressTable.Row>
          <IressTable.HeaderCell>Name</IressTable.HeaderCell>
          <IressTable.HeaderCell>Email</IressTable.HeaderCell>
          <IressTable.HeaderCell>Status</IressTable.HeaderCell>
          <IressTable.HeaderCell>Actions</IressTable.HeaderCell>
        </IressTable.Row>
      </IressTable.Head>
      <IressTable.Body>
        {users.map((user) => (
          <IressTable.Row key={user.id}>
            <IressTable.Cell>{user.name}</IressTable.Cell>
            <IressTable.Cell>{user.email}</IressTable.Cell>
            <IressTable.Cell>
              <IressTag>{user.status}</IressTag>
            </IressTable.Cell>
            <IressTable.Cell>
              <IressButton mode="tertiary" icon="edit">
                Edit
              </IressButton>
            </IressTable.Cell>
          </IressTable.Row>
        ))}
      </IressTable.Body>
    </IressTable>
  );
}
```

## Best Practices

1. **Use IDS components, not raw elements** — IDS components encapsulate correct spacing, colours, border radius, and accessibility
2. **Don't recreate component internals** — If Figma shows a button with specific padding/radius, use `IressButton` with the right `mode` — the styling is built in
3. **Map Figma gap/padding to spacing tokens** — Divide pixel value by 4 to get the token number
4. **Prefer semantic props over manual styling** — Use `status="danger"` instead of `bg="colour.system.danger.fill"`
5. **Use IressField for all form inputs** — It provides the label, hint, and validation layout
6. **Respect responsive patterns** — Use `IressHide`, `hideFrom`/`hideBelow` for responsive visibility
7. **Check the component docs** — Read the specific component doc for detailed props and patterns (`node_modules/@iress-oss/ids-components/.ai/components/`)
