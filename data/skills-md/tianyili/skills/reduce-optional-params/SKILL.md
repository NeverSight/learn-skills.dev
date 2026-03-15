---
name: reduce-optional-params
description: "Use when designing or refactoring functions with many optional params, configurable components, or when the user mentions optional params, function signatures, or API simplification. Reduces optional parameters in functions and components for cleaner APIs."
---

# Reduce Optional Parameters

Guidance for simplifying function and component signatures by reducing optional parameters. Too many optional params make call sites hard to read and APIs fragile.

## When to Apply

- Designing new functions or components
- Refactoring code with many optional arguments
- Code review when spotting 3+ optional params
- User asks about cleaner API design or reducing optional params

**Before adding an optional param, ask:** (1) Is there a concrete use case? (2) Would a separate function or preset make intent clearer? (3) Would callers pass this only in a few places? (If yes, a dedicated function or preset may be clearer.)

## Strategies (Choose by Context)

### 1. Options Object

Group related optional params into a single config object.

```ts
// Before
function fetchUser(id: string, includeProfile?: boolean, cache?: boolean, timeout?: number) {}

// After
function fetchUser(id: string, options?: { includeProfile?: boolean; cache?: boolean; timeout?: number }) {}
```

Use when: Params are loosely related and callers typically pass 0–2 at a time.

**Edge case:** If one option is required in most call sites, keep it as a required positional param and put the rest in the options object (e.g. `fetchUser(id, { includeProfile: true })`).

### 2. Split Into Focused Functions

Replace one function with many optional params with smaller, purpose-specific functions.

```ts
// Before
function createButton(text: string, variant?: string, size?: string, disabled?: boolean, icon?: string) {}

// After
function createPrimaryButton(text: string, opts?: { size?: string }) {}
function createIconButton(text: string, icon: string, opts?: { size?: string }) {}
```

Use when: Optional params create distinct usage modes (e.g. "icon mode" vs "text-only").

### 3. Composition (React/Components)

Use children, compound components, or render props instead of optional props.

```tsx
// Before
<Button text="Save" variant="primary" size="md" leftIcon={<SaveIcon />} rightIcon={null} loading={false} />

// After
<Button variant="primary" size="md">
  <Button.Icon><SaveIcon /></Button.Icon>
  Save
</Button>
```

Use when: UI has many configurable facets that rarely combine.

### 4. Factory or Preset Functions

Expose presets for common configurations instead of one function with many options.

```ts
// Before
function connect(url: string, retries?: number, timeout?: number, ssl?: boolean) {}

// After
function connect(url: string, opts?: ConnectionOptions) {}
function connectProduction(url: string) {
  return connect(url, { retries: 3, timeout: 5000, ssl: true });
}
```

Use when: A few well-defined configurations dominate usage.

### 5. Narrower Required Params

Move "optional" params into a narrower function where they become required.

```ts
// Before
function render(component: Component, layout?: string, theme?: string) {}

// After
function render(component: Component) {}
function renderWithLayout(component: Component, layout: string, theme?: string) {}
```

Use when: Some params are optional only in the generic path but required in specific paths.

### 6. Builder Pattern (When Fluent API Fits)

Use a builder when callers need to set many options and discoverability helps.

```ts
// Before
createModal(title: string, content: string, closable?: boolean, width?: number, onClose?: () => void) {}

// After
Modal.create(title, content).closable(true).width(400).onClose(handler).show()
```

Use when: 5+ options and fluent-style API is acceptable in the codebase.

## Decision Flow

1. **2–3 optional params** → Options object
2. **Distinct usage modes** → Split into focused functions
3. **UI/component** → Prefer composition over many optional props
4. **Common presets** → Factory/preset functions
5. **Generic vs specific paths** → Narrower functions with required params
6. **5+ options, complex config** → Builder or options object
7. **None of the above fits** → Prefer options object to keep one function; document defaults and avoid optional params that change behavior in non-obvious ways.

## Anti-Patterns

- Don’t add optional params "for flexibility" without concrete use cases
- Avoid optional params that change behavior in non-obvious ways (use separate functions)
- Don’t mix positional optional params with an options object
