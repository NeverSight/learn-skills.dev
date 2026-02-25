---
name: syntax-design-system
description: Guide for working with Cambly's Syntax design system React components. Use when implementing UI features with Syntax components, converting existing UI to use the design system, fixing component styling or accessibility issues, or reviewing code that uses Syntax.
---

# Syntax Design System

Use this skill when working with Cambly's Syntax design system components in React applications. Invoke this skill when:

- Implementing new UI features using Syntax components
- Converting existing UI to use Syntax components
- Fixing styling, accessibility, or component usage issues
- Reviewing code that uses Syntax components

## Core Principles

When working with Syntax components, you must:

1. **Always use `Box` instead of plain divs** for layout and containers
2. **Never hardcode spacing or colors** - use the design system's spacing scale (0-12) and color tokens
3. **Always provide `accessibilityLabel` for `IconButton`** components
4. **Use semantic HTML** via the `as` prop (e.g., `<Box as="nav">`)
5. **Add `data-testid` attributes** for all interactive elements in tests

## Installation

The Syntax packages required are:

- `@cambly/syntax-core` - Main component library
- `@cambly/syntax-design-tokens` - Design tokens
- `@cambly/syntax-icons` - Icon components
- `@cambly/syntax-floating-components` - Tooltips and popovers with Floating UI

```bash
npm install @cambly/syntax-core @cambly/syntax-design-tokens @cambly/syntax-icons @cambly/syntax-floating-components
```

## Component Selection Guide

Use this decision tree to select the right component:

**Layout & Containers:**

- Layout container → `Box` (with flexbox props)
- Content container with elevation → `Card`

**Buttons & Actions:**

- Button with text → `Button`
- Button with icon only → `IconButton` (requires `accessibilityLabel`)
- Link styled as button → `LinkButton`
- Clickable area without button semantics → `TapArea`
- Group related buttons → `ButtonGroup`

**Typography:**

- Body text, labels, captions → `Typography`
- Page/section headings → `Heading` (with proper `as` prop: h1-h6)

**Form Inputs:**

- Single-line text → `TextField`
- Multi-line text → `TextArea`
- True/false selection → `Checkbox`
- One of many options → `RadioButton`
- Dropdown selection → `SelectList` (native) or `RichSelectList` (styled)

**Feedback & Overlays:**

- Blocking dialog → `Modal`
- Contextual overlay → `Popover`
- Temporary notification → `Toast`
- Hover information → `Tooltip`

**Indicators & Status:**

- Small status indicator → `Badge`
- User profile image → `Avatar` or `AvatarGroup`
- Filter/tag → `Chip`
- Visual separator → `Divider`
- Icons → `Icon` (use with `@cambly/syntax-icons`)

**Navigation:**

- Tab interface → `Tabs` with `TabButton` or `TabLink`

## Required Patterns

### Box Component - The Foundation

**Basic Layout:**

```typescript
<Box
  display="flex"
  direction="column"
  gap={4}
  justifyContent="center"
  alignItems="start"
>
  {children}
</Box>
```

**Responsive Layout (mobile-first):**

```typescript
<Box
  direction="column" // Mobile: stack vertically
  smDirection="row" // Tablet (480px+): horizontal
  lgDirection="row" // Desktop (960px+): horizontal
  padding={2}
  smPadding={4}
  lgPadding={6}
>
  {children}
</Box>
```

**Spacing (0-12 scale):**

```typescript
<Box
  margin={4}              // All sides
  marginTop={2}           // Individual sides
  marginStart={3}         // Start (left in LTR, right in RTL)
  padding={4}
  paddingX={6}            // Horizontal
  paddingY={2}            // Vertical
>
```

**Semantic HTML:**

```typescript
<Box as="section" role="main">  // Renders as <section>
<Box as="nav">                   // Renders as <nav>
```

### Size Variants

**Buttons/IconButtons/Chips:** `"sm" | "md" | "lg"` (heights: 32px, 48px, 64px)

```typescript
<Button text="Click me" size="md" />
```

**Typography/Heading:** `100 | 200 | 300 | 400 | 500 | 700 | 800 | 900 | 1100`

```typescript
<Typography size={400}>Body text</Typography>
<Heading size={600}>Page title</Heading>
```

**Icon:** `100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 1000`

```typescript
<Icon path={iconPath} size={400} />
```

### Color System

**Button Colors:**

- `primary` - Main call-to-action (blue)
- `secondary` - Secondary actions (gray)
- `tertiary` - Tertiary actions (minimal)
- `destructive-primary/secondary/tertiary` - Dangerous actions (red)
- `success-primary/secondary/tertiary` - Positive actions (green)
- `branded` - Brand-specific color

```typescript
<Button text="Delete" color="destructive-primary" />
<Button text="Cancel" color="secondary" />
```

**Background Context (`on` prop):**

```typescript
<Button text="Click" on="darkBackground" />
<TextField label="Name" on="lightBackground" />
```

**Universal Colors (Box, Icon, Typography):**

- Primary: `primary`, `primary100`-`primary900`
- Semantic: `success100`-`success900`, `destructive100`-`destructive900`
- Neutrals: `gray10`-`gray900`, `white`, `black`
- Brand: `sky`, `navy`, `teal`, `lilac`, `pink`, `cream`

```typescript
<Box backgroundColor="gray10" />
<Typography color="primary700">Text</Typography>
<Icon color="success500" size={300} />
```

## Form Patterns

**TextField with validation:**

```typescript
<TextField
  label="Email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={!!emailError}
  errorText={emailError}
  helperText="We'll never share your email"
  disabled={isSubmitting}
  data-testid="email-input"
/>
```

**Checkbox:**

```typescript
<Checkbox
  label="I agree to terms"
  checked={agreed}
  onChange={(e) => setAgreed(e.target.checked)}
  error={submitted && !agreed}
  size="md"
/>
```

**RadioButton group:**

```typescript
{
  options.map((option) => (
    <RadioButton
      key={option.value}
      label={option.label}
      checked={selected === option.value}
      onChange={() => setSelected(option.value)}
      name="options"
    />
  ));
}
```

## Button Patterns

**Button with icons:**

```typescript
import { ChevronRightIcon } from "@cambly/syntax-icons";

<Button text="Continue" endIcon={ChevronRightIcon} color="primary" size="lg" />;
```

**Loading state:**

```typescript
<Button
  text="Save"
  loading={isSubmitting}
  loadingText="Saving..."
  disabled={!isDirty}
/>
```

**IconButton (REQUIRED: accessibilityLabel):**

```typescript
import { CloseIcon } from "@cambly/syntax-icons";

<IconButton
  icon={CloseIcon}
  accessibilityLabel="Close dialog" // REQUIRED!
  color="secondary"
  size="sm"
  onClick={handleClose}
/>;
```

## Typography Patterns

```typescript
// Headings - always use semantic 'as' prop
<Heading as="h1" size={800}>Page Title</Heading>
<Heading as="h2" size={600}>Section Heading</Heading>

// Body text
<Typography size={400}>Regular paragraph text</Typography>
<Typography size={300} color="gray700">Secondary text</Typography>

// Text styling
<Typography
  weight="semiBold"
  transform="uppercase"
  align="center"
  lineClamp={2}  // Truncate after 2 lines
>
  Content
</Typography>
```

## Modal & Dialog Pattern

```typescript
<Modal isOpen={isOpen} onDismiss={handleClose} title="Confirm Action" size="md">
  <Box padding={6}>
    <Typography>Are you sure?</Typography>
    <Box display="flex" gap={2} marginTop={4}>
      <Button text="Cancel" color="secondary" onClick={handleClose} />
      <Button text="Confirm" color="primary" onClick={handleConfirm} />
    </Box>
  </Box>
</Modal>
```

## Tooltip Pattern

```typescript
<Tooltip text="Additional information">
  <IconButton icon={InfoIcon} accessibilityLabel="Info" />
</Tooltip>
```

## Card Pattern

```typescript
<Card size="medium" backgroundColor="white">
  <Box padding={4}>
    <Heading size={500}>Card Title</Heading>
    <Typography size={300} color="gray700">
      Card content goes here
    </Typography>
  </Box>
</Card>
```

## Accessibility Requirements

### Required Props

**Form inputs need labels:**

```typescript
<TextField label="Email" />    // Good
<Checkbox label="I agree" />   // Good
```

**Icon buttons need accessibilityLabel:**

```typescript
<IconButton
  icon={TrashIcon}
  accessibilityLabel="Delete item" // Required for screen readers
/>
```

**Use semantic HTML:**

```typescript
<Box as="nav">        // Semantic elements
<Box as="main">
<Heading as="h1">     // Proper heading hierarchy
```

### Focus Management

- Components automatically handle keyboard focus visibility
- Focus outlines only appear on keyboard navigation (not clicks)
- All interactive elements are keyboard accessible

### Form Accessibility

```typescript
// Associate helper text with input
<Box>
  <TextField label="Password" aria-describedby="password-help" />
  <Typography id="password-help" size={200}>
    Must be at least 8 characters
  </Typography>
</Box>
```

## Common Mistakes to Avoid

### ❌ Using plain divs for layout

```typescript
// BAD
<div style={{ display: 'flex', gap: '16px' }}>
```

### ✅ Use Box component

```typescript
// GOOD
<Box display="flex" gap={4}>
```

### ❌ Missing accessibilityLabel

```typescript
// BAD - inaccessible
<IconButton icon={CloseIcon} />
```

### ✅ Always include accessibilityLabel

```typescript
// GOOD
<IconButton icon={CloseIcon} accessibilityLabel="Close" />
```

### ❌ Hardcoded pixel values

```typescript
// BAD
<Box style={{ marginTop: '24px' }}>
```

### ✅ Use spacing scale

```typescript
// GOOD - uses 0-12 scale (6 = 24px)
<Box marginTop={6}>
```

### ❌ Wrong icon imports

```typescript
// BAD
import CloseIcon from "@cambly/syntax-icons/CloseIcon";
```

### ✅ Named imports from package root

```typescript
// GOOD
import { CloseIcon } from "@cambly/syntax-icons";
```

### ❌ Ignoring background context

```typescript
// BAD - button on dark background with wrong styling
<Box backgroundColor="navy">
  <Button text="Click me" />
</Box>
```

### ✅ Use 'on' prop for contrast

```typescript
// GOOD
<Box backgroundColor="navy">
  <Button text="Click me" on="darkBackground" />
</Box>
```

### ❌ Avoid “self-spacing” children

```typescript
// BAD
<Box marginBottom={2}>Some text</Box>
<Box marginBottom={2}>Some more text</Box>
```

### ✅ Use a parent wrapper to define sibling spacing

````typescript
// GOOD
<Box display="flex" direction="column" gap={2}>
  <Box>Some text</Box>
  <Box>Some more text</Box>
</Box>
```

#### When child margins are OK

Use margins on a component only when it is intrinsic to that component, not dependent on neighbors (e.g., internal spacing within the component, or a visual affordance that always exists regardless of placement).


## Import Patterns

```typescript
// Core components
import { Box, Button, Typography, TextField } from "@cambly/syntax-core";

// Icons (named imports only)
import { ChevronRightIcon, CloseIcon, CheckIcon } from "@cambly/syntax-icons";

// Floating components
import { FloatingTooltip } from "@cambly/syntax-floating-components";

// Design tokens (rarely needed directly)
import { tokens } from "@cambly/syntax-design-tokens";
````

## Testing

Always add `data-testid` for testable elements:

```typescript
<Button
  text="Submit"
  data-testid="submit-button"
  onClick={handleSubmit}
/>

<TextField
  label="Email"
  data-testid="email-input"
  value={email}
/>
```

## Theme Provider

Wrap your app root with ThemeProvider:

```typescript
import { ThemeProvider } from "@cambly/syntax-core";

function App() {
  return <ThemeProvider>{/* Your app */}</ThemeProvider>;
}
```

## Review Checklist

When reviewing or writing code with Syntax components, verify:

- [ ] Using `Box` instead of plain divs for layout
- [ ] Using spacing scale (0-12) instead of hardcoded pixels
- [ ] All `IconButton` components have `accessibilityLabel`
- [ ] Form inputs have labels
- [ ] Using semantic HTML via `as` prop where appropriate
- [ ] Icons imported correctly from `@cambly/syntax-icons`
- [ ] `on` prop used for components on dark backgrounds
- [ ] `data-testid` added to interactive elements
- [ ] Proper heading hierarchy with `Heading` component
- [ ] Responsive props used for mobile-first design

## Additional Resources

- Storybook documentation: Run `pnpm start` in the syntax repo
- Component props: TypeScript types provide full documentation
- All components have full TypeScript type definitions
