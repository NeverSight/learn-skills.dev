---
name: uswds
description: >-
  Provides a comprehensive guide for building with the U.S. Web Design System (USWDS v3) and
  @trussworks/react-uswds React component library. Use when: (1) building or styling
  UI with USWDS components, utility classes, or design tokens, (2) implementing layouts
  with the USWDS grid system, (3) working with USWDS color, typography, or spacing tokens,
  (4) creating forms, navigation, headers, footers, modals, tables, cards, or any USWDS
  component, (5) applying USWDS accessibility patterns, (6) customizing USWDS theme settings
  via Sass variables, (7) using @trussworks/react-uswds imports and props, (8) building
  government/federal web interfaces. Triggers on: USWDS classes (usa-*), @trussworks/react-uswds
  imports, USWDS Sass tokens/functions, federal design system questions.
---

# USWDS Development Guide

Build accessible, mobile-friendly interfaces using USWDS v3 and `@trussworks/react-uswds`.

## Quick Reference

- **Components**: See [references/components.md](references/components.md) for all 47 components with React imports and CSS classes
- **Design Tokens**: See [references/design-tokens.md](references/design-tokens.md) for colors, spacing, typography, and all token values
- **Utilities**: See [references/utilities.md](references/utilities.md) for all utility classes organized by category
- **Grid & Layout**: See [references/grid-layout.md](references/grid-layout.md) for the 12-column grid system
- **Sass Theming**: See [references/sass-theming.md](references/sass-theming.md) for customizing USWDS via settings variables

## Core Architecture

USWDS has three layers:

1. **Design Tokens** — Named values for color, spacing, typography (never use raw hex/px)
2. **Utilities** — Single-property CSS classes (`bg-primary`, `padding-2`, `font-sans-lg`)
3. **Components** — Pre-built UI patterns (`usa-alert`, `usa-card`, `usa-header`)

Tokens flow through **functions** (`color('primary')`), **mixins** (`u-bg('primary')`), and **utility classes** (`.bg-primary`).

## React Usage (@trussworks/react-uswds)

Import components directly:

```tsx
import {
  Alert, Button, Card, CardGroup, CardHeader, CardBody, CardFooter,
  Grid, GridContainer, Form, Fieldset, Label, TextInput, Select,
  Table, Tag, Tooltip, Modal, ModalToggleButton, ModalHeading, ModalFooter,
  Header, PrimaryNav, Footer, SideNav, Breadcrumb, BreadcrumbBar, BreadcrumbLink,
  StepIndicator, StepIndicatorStep, SummaryBox, SummaryBoxHeading, SummaryBoxContent,
  Search, Pagination, Accordion, GovBanner, SiteAlert, Icon,
  Checkbox, Radio, ComboBox, DatePicker, FileInput, Textarea, TimePicker,
  ButtonGroup, ProcessList, ProcessListItem, ProcessListHeading,
  Collection, CollectionItem, IconList, IconListItem,
} from '@trussworks/react-uswds';
```

Do NOT import USWDS JavaScript directly (`import 'uswds'`) — it causes double-initialization of interactive components.

## Key Conventions

### Always Use Tokens (Never Hardcoded Values)

```scss
// WRONG
color: #005ea2;
padding: 16px;

// RIGHT
color: color('primary');
padding: units(2);
```

### Utility Classes Follow `.{property}-{token}` Pattern

```html
<div class="bg-primary text-white padding-2 margin-bottom-3 font-sans-lg">
  Content
</div>
```

### USWDS Class Prefix: `usa-`

All component classes use the `usa-` prefix:
- `.usa-alert`, `.usa-button`, `.usa-card`, `.usa-table`
- `.usa-header`, `.usa-footer`, `.usa-modal`, `.usa-sidenav`

### Responsive Prefixes

Apply at breakpoint and above (mobile-first):
```html
<div class="grid-col-12 tablet:grid-col-6 desktop:grid-col-4">
```

Breakpoints: `mobile-lg` (480px), `tablet` (640px), `tablet-lg` (880px), `desktop` (1024px), `widescreen` (1400px)

## Accessibility Requirements

USWDS enforces Section 508 / WCAG 2.1 AA:

- **Color contrast**: Use grade differences of 50+ for AA (see magic number system in design tokens reference)
- **Semantic HTML**: `<nav>`, `<main>`, `<section>`, `<button>` over `<div>` with roles
- **ARIA attributes**: `aria-label` on nav elements, `aria-current="page"` on breadcrumbs, `aria-expanded` on toggles
- **Form accessibility**: Every input needs a `<Label>`, use `<Fieldset>` + `<legend>` for groups, mark required fields with `*`
- **Keyboard navigation**: All interactive elements must be keyboard-accessible, trap focus in modals
- **Skip navigation**: Include skip-nav links before headers

## Common Patterns

### Page Layout

```tsx
<GridContainer>
  <Grid row gap>
    <Grid col={12} tablet={{ col: 3 }}>
      <SideNav items={navItems} />
    </Grid>
    <Grid col={12} tablet={{ col: 9 }}>
      <main>{children}</main>
    </Grid>
  </Grid>
</GridContainer>
```

### Alert

```tsx
<Alert type="info" heading="Informational" headingLevel="h3">
  Body text here.
</Alert>
// type: 'info' | 'success' | 'warning' | 'error' | 'emergency'
```

### Form with Validation

```tsx
<Form onSubmit={handleSubmit}>
  <Fieldset legend="Contact Information">
    <Label htmlFor="email" requiredMarker>Email</Label>
    <TextInput id="email" name="email" type="email" validationStatus={errors.email ? 'error' : undefined} />
    {errors.email && <ErrorMessage>{errors.email}</ErrorMessage>}
  </Fieldset>
  <Button type="submit">Submit</Button>
</Form>
```

### Modal

```tsx
const modalRef = useRef<ModalRef>(null);

<ModalToggleButton modalRef={modalRef} opener>Open</ModalToggleButton>
<Modal ref={modalRef} id="my-modal" aria-labelledby="modal-heading" aria-describedby="modal-desc">
  <ModalHeading id="modal-heading">Title</ModalHeading>
  <p id="modal-desc">Description</p>
  <ModalFooter>
    <ButtonGroup>
      <ModalToggleButton modalRef={modalRef} closer>Cancel</ModalToggleButton>
      <Button type="button" onClick={handleConfirm}>Confirm</Button>
    </ButtonGroup>
  </ModalFooter>
</Modal>
```

### Table

```tsx
<Table bordered striped fullWidth>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Item 1</th>
      <td>Active</td>
    </tr>
  </tbody>
</Table>
```

### Card

```tsx
<CardGroup>
  <Card>
    <CardHeader><h3 className="usa-card__heading">Title</h3></CardHeader>
    <CardBody><p>Content</p></CardBody>
    <CardFooter><Button>Action</Button></CardFooter>
  </Card>
</CardGroup>
```

## Sass Configuration Entry Point

```scss
// styles.scss
@use "uswds-core" with (
  $theme-image-path: '~@uswds/uswds/dist/img',
  $theme-font-path: '~@uswds/uswds/dist/fonts',
  // Theme overrides go here
);
@forward 'uswds';
// Custom styles below
```

Configure theme tokens ABOVE `@forward 'uswds'`. See [references/sass-theming.md](references/sass-theming.md).
