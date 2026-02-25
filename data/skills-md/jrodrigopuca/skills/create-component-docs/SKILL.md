---
name: create-component-docs
description: Generate comprehensive component documentation (architecture, API, examples, known issues). Works with React, Vue, Angular, and Web Components. | Genera documentación completa de componentes (arquitectura, API, ejemplos, issues conocidos). Compatible con React, Vue, Angular y Web Components.
license: MIT
---

# Component Documentation Generator

Generate structured documentation for UI components across frameworks.

## Overview

This skill guides the creation of component documentation by providing:

- **Structure templates** for consistent documentation
- **API/Props table format** compatible with TypeScript and PropTypes
- **Architecture diagrams** using Mermaid syntax
- **Known issues format** with severity classification
- **Usage examples** from basic to advanced

This skill references official documentation instead of duplicating content. See external links for framework-specific details.

## Prerequisites

- Access to component source code
- Understanding of component's purpose and usage
- Optional: TypeScript types or PropTypes definitions
- Optional: Existing tests or Storybook stories

## Instructions

### 1. Identify Component Type

Before documenting, classify the component:

| Type               | Characteristics                      | Documentation Focus                |
| ------------------ | ------------------------------------ | ---------------------------------- |
| **Presentational** | No state, receives props, renders UI | Props, variants, styling           |
| **Container**      | Manages state, data fetching         | State flow, side effects           |
| **Composite**      | Combines multiple components         | Internal structure, slots          |
| **Utility**        | Hooks, HOCs, render props            | API, return values, usage patterns |

**Quick checklist:**

- [ ] Has internal state? → Document state management
- [ ] Accepts children/slots? → Document composition API
- [ ] Triggers events/callbacks? → Document event interface
- [ ] Has side effects? → Document lifecycle and cleanup
- [ ] Depends on context/providers? → Document dependencies

### 2. Document the API/Props

Use the standard props table format:

```markdown
## Props

| Prop       | Type                          | Default     | Required | Description            |
| ---------- | ----------------------------- | ----------- | -------- | ---------------------- |
| `variant`  | `'primary' \| 'secondary'`    | `'primary'` | No       | Visual style variant   |
| `onClick`  | `(event: MouseEvent) => void` | -           | Yes      | Click handler callback |
| `children` | `ReactNode`                   | -           | Yes      | Content to render      |
| `disabled` | `boolean`                     | `false`     | No       | Disables interaction   |
```

**For TypeScript projects, link to types:**

```markdown
See [ButtonProps](../types/button.ts#L12-L25) for complete type definition.
```

**For events/callbacks:**

```markdown
## Events

| Event      | Payload                             | Description                |
| ---------- | ----------------------------------- | -------------------------- |
| `onChange` | `{ value: string, valid: boolean }` | Emitted on input change    |
| `onSubmit` | `FormData`                          | Emitted on form submission |
```

**Official documentation:**

- TypeScript: [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- React: [Component Props](https://react.dev/learn/passing-props-to-a-component)
- Vue: [Props Declaration](https://vuejs.org/guide/components/props.html)

### 3. Map Component Architecture

Document internal structure using Mermaid diagrams:

**Component hierarchy:**

```markdown
## Architecture

​`mermaid
graph TD
    A[DataTable] --> B[TableHeader]
    A --> C[TableBody]
    A --> D[TableFooter]
    C --> E[TableRow]
    E --> F[TableCell]
    A --> G[Pagination]
​`
```

**State flow (for stateful components):**

```markdown
## State Flow

​`mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading: fetch()
    Loading --> Success: data received
    Loading --> Error: request failed
    Success --> Idle: reset()
    Error --> Loading: retry()
​`
```

**Official documentation:**

- Mermaid: [Diagram Syntax](https://mermaid.js.org/intro/syntax-reference.html)
- Mermaid: [Live Editor](https://mermaid.live/)

### 4. Document Interactions

Describe how the component interacts with:

**External dependencies:**

```markdown
## Dependencies

| Dependency              | Purpose               | Required |
| ----------------------- | --------------------- | -------- |
| `ThemeContext`          | Provides color tokens | Yes      |
| `useTranslation`        | i18n support          | No       |
| `@tanstack/react-query` | Data fetching         | Yes      |
```

**Lifecycle events:**

```markdown
## Lifecycle

1. **Mount:** Registers event listeners, fetches initial data
2. **Update:** Re-renders on prop/state change, debounces API calls
3. **Unmount:** Cleans up listeners, cancels pending requests
```

### 5. Record Known Issues

Document limitations and edge cases:

```markdown
## Known Issues

| Issue                           | Severity  | Workaround           | Status       |
| ------------------------------- | --------- | -------------------- | ------------ |
| Flickers on rapid re-render     | 🟡 Medium | Use `memo()` wrapper | Open         |
| Doesn't support RTL layout      | 🟢 Low    | Apply manual CSS     | Planned v2.1 |
| Memory leak with large datasets | 🔴 High   | Limit to 1000 items  | In Progress  |
```

**Severity levels:**

- 🔴 **High:** Causes crashes, data loss, or security issues
- 🟡 **Medium:** Degrades UX but has workaround
- 🟢 **Low:** Minor inconvenience, cosmetic issues

### 6. Add Usage Examples

Provide examples from basic to advanced:

````markdown
## Examples

### Basic Usage

​`tsx
<Button variant="primary" onClick={handleClick}>
  Click me
</Button>
​`

### With Loading State

​```tsx
<Button
variant="primary"
loading={isSubmitting}
disabled={!isValid}
onClick={handleSubmit}

> {isSubmitting ? 'Saving...' : 'Save'}
> </Button>
> ​```

### Composition with Icons

​`tsx
<Button variant="secondary">
  <Icon name="download" />
  <span>Download Report</span>
</Button>
​`
````

**For complex components, link to Storybook:**

```markdown
See [Storybook](https://your-storybook.com/?path=/docs/components-button) for interactive examples.
```

## Quick Reference

| Section          | When to Include      | Priority         |
| ---------------- | -------------------- | ---------------- |
| **Props/API**    | Always               | 🔴 Required      |
| **Examples**     | Always               | 🔴 Required      |
| **Architecture** | Composite components | 🟡 Recommended   |
| **State Flow**   | Stateful components  | 🟡 Recommended   |
| **Dependencies** | Has external deps    | 🟡 Recommended   |
| **Known Issues** | Has limitations      | 🟢 If applicable |
| **Lifecycle**    | Complex side effects | 🟢 If applicable |

## External Resources

**Framework documentation:**

- React: [Component API Reference](https://react.dev/reference/react)
- Vue: [Component Basics](https://vuejs.org/guide/essentials/component-basics.html)
- Angular: [Component Overview](https://angular.io/guide/component-overview)
- Web Components: [MDN Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)

**Documentation tools:**

- [Storybook](https://storybook.js.org/docs) - Interactive component documentation
- [JSDoc](https://jsdoc.app/) - API documentation from comments
- [TypeDoc](https://typedoc.org/) - TypeScript documentation generator

**Diagrams:**

- [Mermaid](https://mermaid.js.org/) - Diagrams as code
- [Excalidraw](https://excalidraw.com/) - Hand-drawn style diagrams

---

See [references/templates.md](references/templates.md) for copy-paste ready templates.
