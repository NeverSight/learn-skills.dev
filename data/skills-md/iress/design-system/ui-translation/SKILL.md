---
name: ui-translation
description: Translate natural language UI descriptions into IDS (Iress Design System) component implementations using `@iress-oss/ids-components` and `@iress-oss/ids-tokens`.
---

# Skill: UI Translation

## Purpose

Translate natural language UI descriptions into IDS (Iress Design System) component implementations using `@iress-oss/ids-components` and `@iress-oss/ids-tokens`.

## Setup

```tsx
import '@iress-oss/ids-components/dist/style.css'; // Required — component styles
import '@iress-oss/ids-tokens/build/css-vars.css'; // Required if using tokens directly
import {
  IressProvider,
  IressButton,
  IressInput,
  IressField,
  IressStack,
  IressInline,
  IressText,
  IressCard,
  // ... import what you need
} from '@iress-oss/ids-components';

// Wrap your app in IressProvider (handles fonts + CSS variables)
function App() {
  return <IressProvider>{/* your UI */}</IressProvider>;
}
```

## Component Mapping

### Actions

| Description                      | IDS Component                          | Example                                                            |
| -------------------------------- | -------------------------------------- | ------------------------------------------------------------------ |
| Submit / primary action button   | `IressButton mode="primary"`           | `<IressButton mode="primary">Submit</IressButton>`                 |
| Cancel / secondary action button | `IressButton mode="secondary"`         | `<IressButton mode="secondary">Cancel</IressButton>`               |
| Less prominent action            | `IressButton mode="tertiary"`          | `<IressButton mode="tertiary">Details</IressButton>`               |
| Icon-only action                 | `IressButton icon="edit" mode="muted"` | `<IressButton mode="muted" icon="edit">Edit</IressButton>`         |
| Danger / delete action           | `IressButton status="danger"`          | `<IressButton mode="primary" status="danger">Delete</IressButton>` |
| Link in text                     | `IressLink`                            | `<IressLink href="/about">About</IressLink>`                       |
| Dropdown/context menu trigger    | `IressDropdownMenu`                    | See patterns docs                                                  |

### Form Inputs

| Description              | IDS Component                       | Example                                                                                                                        |
| ------------------------ | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Labelled text input      | `IressField` + `IressInput`         | See Form example below                                                                                                         |
| Select dropdown          | `IressField` + `IressSelect`        | `<IressField label="Country"><IressSelect>...</IressSelect></IressField>`                                                      |
| Currency input           | `IressField` + `IressInputCurrency` | `<IressField label="Amount"><IressInputCurrency /></IressField>`                                                               |
| Checkbox                 | `IressCheckbox`                     | `<IressCheckbox label="I agree" />`                                                                                            |
| Checkbox group           | `IressCheckboxGroup`                | `<IressCheckboxGroup label="Options"><IressCheckbox label="A" /><IressCheckbox label="B" /></IressCheckboxGroup>`              |
| Radio buttons            | `IressRadioGroup` + `IressRadio`    | `<IressRadioGroup label="Choice"><IressRadio label="Yes" value="yes" /><IressRadio label="No" value="no" /></IressRadioGroup>` |
| Toggle switch            | `IressToggle`                       | `<IressToggle label="Enable" />`                                                                                               |
| Slider / range           | `IressSlider`                       | `<IressSlider min={0} max={100} />`                                                                                            |
| Autocomplete / typeahead | `IressAutocomplete`                 | See component docs                                                                                                             |
| Read-only display        | `IressReadonly`                     | `<IressReadonly label="Status" value="Active" />`                                                                              |

### Layout

| Description                                  | IDS Component           | Example                                                                                   |
| -------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------- |
| Vertical stack (items stacked top-to-bottom) | `IressStack`            | `<IressStack gap="4">...</IressStack>`                                                    |
| Horizontal row (items side-by-side)          | `IressInline`           | `<IressInline gap="2">...</IressInline>`                                                  |
| Grid columns                                 | `IressRow` + `IressCol` | `<IressRow><IressCol span={6}>...</IressCol><IressCol span={6}>...</IressCol></IressRow>` |
| Container with max-width                     | `IressContainer`        | `<IressContainer>...</IressContainer>`                                                    |
| Divider / separator                          | `IressDivider`          | `<IressDivider />`                                                                        |
| Responsive visibility                        | `IressHide`             | `<IressHide below="md">Desktop only</IressHide>`                                          |

### Content & Display

| Description          | IDS Component               | Example                                                                                                     |
| -------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Text / paragraph     | `IressText`                 | `<IressText>Body text</IressText>`                                                                          |
| Heading              | `IressText element="h2"`    | `<IressText element="h2">Heading</IressText>`                                                               |
| Card / panel         | `IressCard` or `IressPanel` | `<IressCard><IressCard.Header>Title</IressCard.Header><IressCard.Body>Content</IressCard.Body></IressCard>` |
| Alert / notification | `IressAlert`                | `<IressAlert status="success">Saved!</IressAlert>`                                                          |
| Loading spinner      | `IressSpinner`              | `<IressSpinner />`                                                                                          |
| Skeleton loader      | `IressSkeleton`             | `<IressSkeleton height="20px" width="200px" />`                                                             |
| Progress bar         | `IressProgress`             | `<IressProgress value={75} max={100} />`                                                                    |
| Image                | `IressImage`                | `<IressImage src="..." alt="..." />`                                                                        |
| Icon                 | `IressIcon`                 | `<IressIcon name="settings" />`                                                                             |
| Tag / badge          | `IressTag`                  | `<IressTag>New</IressTag>`                                                                                  |
| Pill                 | `IressPill`                 | `<IressPill>Category</IressPill>`                                                                           |
| Tooltip              | `IressTooltip`              | `<IressTooltip content="Help text"><IressButton>Hover me</IressButton></IressTooltip>`                      |

### Overlays & Navigation

| Description                           | IDS Component                 | Example                                                                   |
| ------------------------------------- | ----------------------------- | ------------------------------------------------------------------------- |
| Modal / dialog                        | `IressModal`                  | See Modal docs                                                            |
| Status modal (danger/success/warning) | `IressModal status="danger"`  | Use `actions` prop for buttons; size restricted to `sm`/`md`              |
| Slideout / drawer                     | `IressSlideout`               | See Slideout docs                                                         |
| Popover                               | `IressPopover`                | See Popover docs                                                          |
| Menu                                  | `IressMenu` + `IressMenuItem` | See Menu docs                                                             |
| Tab navigation                        | `IressTabSet` + `IressTab`    | `<IressTabSet><IressTab label="Tab 1">Content 1</IressTab></IressTabSet>` |
| Skip link (a11y)                      | `IressSkipLink`               | `<IressSkipLink href="#main">Skip to content</IressSkipLink>`             |
| Side navigation                       | `IressSideNav`                | See SideNav pattern docs                                                  |
| Breadcrumbs                           | `IressBreadcrumbs`            | See Breadcrumbs pattern docs                                              |

### Tables

| Description | IDS Component | Example                                                                                                 |
| ----------- | ------------- | ------------------------------------------------------------------------------------------------------- |
| Data table  | `IressTable`  | `<IressTable><IressTable.Head>...</IressTable.Head><IressTable.Body>...</IressTable.Body></IressTable>` |

## Styling Props (IressCSSProps)

Most IDS components accept styling props for layout adjustments:

| Prop           | Purpose                         | Values                                                                                                                   |
| -------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `alignSelf`    | Override flex alignment         | `"start"`, `"end"`, `"center"`, `"stretch"`                                                                              |
| `bg`           | Background colour               | Colour tokens: `"colour.primary.fill"`, `"colour.neutral.20"`, `"alt"`, etc.                                             |
| `borderRadius` | Border radius                   | Radius tokens: `"radius.0"` – `"radius.4"`, `"none"`                                                                     |
| `color`        | Text colour                     | Colour tokens: `"colour.neutral.80"`, `"colour.primary.text"`, etc.                                                      |
| `flex`         | Flex grow                       | `"1"` only                                                                                                               |
| `focusable`    | Apply focus ring                | `"true"`, `"within"`                                                                                                     |
| `hideFrom`     | Hide from breakpoint up         | `true`, or breakpoints: `"sm"`, `"md"`, `"lg"`, `"xl"`                                                                   |
| `hideBelow`    | Hide below breakpoint           | Breakpoints: `"sm"`, `"md"`, `"lg"`, `"xl"`                                                                              |
| `maxWidth`     | Max width                       | Size tokens: `"container.sm"`, `"container.md"`, etc.                                                                    |
| `m`            | Margin (all sides)              | Spacing tokens: `"xs"` – `"xl"`, `"spacing.1"` – `"spacing.10"`, `"auto"`, negatives (responsive)                        |
| `mx`           | Margin horizontal               | Same as `m` (responsive)                                                                                                 |
| `my`           | Margin vertical                 | Same as `m` (responsive)                                                                                                 |
| `mt`           | Margin top                      | Same as `m` (responsive)                                                                                                 |
| `mr`           | Margin right                    | Same as `m` (responsive)                                                                                                 |
| `mb`           | Margin bottom                   | Same as `m` (responsive)                                                                                                 |
| `ml`           | Margin left                     | Same as `m` (responsive)                                                                                                 |
| `noGutter`     | Remove last-child bottom margin | `true` / `false`                                                                                                         |
| `p`            | Padding (all sides)             | Spacing tokens: `"xs"` – `"xl"`, `"spacing.1"` – `"spacing.10"` (responsive)                                             |
| `px`           | Padding horizontal              | Same as `p` (responsive)                                                                                                 |
| `py`           | Padding vertical                | Same as `p` (responsive)                                                                                                 |
| `pt`           | Padding top                     | Same as `p` (responsive)                                                                                                 |
| `pr`           | Padding right                   | Same as `p` (responsive)                                                                                                 |
| `pb`           | Padding bottom                  | Same as `p` (responsive)                                                                                                 |
| `pl`           | Padding left                    | Same as `p` (responsive)                                                                                                 |
| `scrollable`   | Enable overflow scrolling       | `true`, `"x"`, `"y"`                                                                                                     |
| `srOnly`       | Screen-reader only              | `true` / `false` (responsive)                                                                                            |
| `stretch`      | Fill parent height              | `true` / `false`                                                                                                         |
| `textAlign`    | Text alignment                  | `"left"`, `"right"`, `"center"`, `"justify"`, `"inherit"`                                                                |
| `textStyle`    | Typography style                | `"typography.body.sm"`, `"typography.body.md"`, `"typography.heading.1"` – `"typography.heading.5"`, `"typography.code"` |
| `width`        | Element width                   | Size tokens: `"input.2"` – `"input.16"`, `"3/12"` – `"12/12"` (grid), `"auto"` (responsive)                              |

## Translation Examples

### "A login form with email and password fields and a submit button"

```tsx
import {
  IressButton,
  IressField,
  IressInput,
  IressStack,
} from '@iress-oss/ids-components';

function LoginForm() {
  return (
    <IressStack gap="4">
      <IressField label="Email" htmlFor="email" required>
        <IressInput id="email" type="email" placeholder="Enter your email" />
      </IressField>
      <IressField label="Password" htmlFor="password" required>
        <IressInput
          id="password"
          type="password"
          placeholder="Enter your password"
        />
      </IressField>
      <IressButton mode="primary" type="submit">
        Log in
      </IressButton>
    </IressStack>
  );
}
```

### "A card with a title, description, and two action buttons"

```tsx
import {
  IressCard,
  IressButton,
  IressInline,
  IressText,
} from '@iress-oss/ids-components';

function ActionCard() {
  return (
    <IressCard>
      <IressCard.Header>
        <IressText element="h3">Card Title</IressText>
      </IressCard.Header>
      <IressCard.Body>
        <IressText>
          This is the card description with supporting details.
        </IressText>
      </IressCard.Body>
      <IressCard.Footer>
        <IressInline gap="2">
          <IressButton mode="primary">Confirm</IressButton>
          <IressButton mode="secondary">Cancel</IressButton>
        </IressInline>
      </IressCard.Footer>
    </IressCard>
  );
}
```

### "A settings page with a toggle, some checkboxes, and a save button"

```tsx
import {
  IressStack,
  IressToggle,
  IressCheckboxGroup,
  IressCheckbox,
  IressButton,
  IressText,
  IressDivider,
} from '@iress-oss/ids-components';

function SettingsPage() {
  return (
    <IressStack gap="6">
      <IressText element="h2">Settings</IressText>
      <IressToggle label="Enable notifications" />
      <IressDivider />
      <IressCheckboxGroup label="Notification types">
        <IressCheckbox label="Email" value="email" />
        <IressCheckbox label="SMS" value="sms" />
        <IressCheckbox label="Push" value="push" />
      </IressCheckboxGroup>
      <IressDivider />
      <IressButton mode="primary">Save settings</IressButton>
    </IressStack>
  );
}
```

## Best Practices

1. **Always wrap in IressProvider** — Required at the root of your app for fonts and CSS variables
2. **Use IressField for all form inputs** — Provides consistent labels, hints, and validation display
3. **Use IressStack/IressInline for layout** — Prefer these over custom CSS flex/grid
4. **Use spacing tokens for gap** — Values 0–10 map to multiples of 4px
5. **Use semantic button modes** — One `primary` per section, `secondary` for most actions
6. **Always include labels** — All form inputs need accessible labels via `IressField`
7. **Use status for feedback** — `IressAlert` for inline messages, `IressModal status="danger"` for confirmation dialogs, `status` prop on buttons for danger/success
8. **Prefer IDS components** — Use `IressText` instead of raw `<p>`, `IressButton` instead of `<button>`
9. **Check the component docs** — Read the specific component doc for detailed props and patterns (`node_modules/@iress-oss/ids-components/.ai/components/`)
