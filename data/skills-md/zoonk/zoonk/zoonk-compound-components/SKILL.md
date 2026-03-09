---
name: zoonk-compound-components
description: Build UI components using the compound component pattern. Use when creating new React components, building UI elements, refactoring components, or when the user mentions compound components, composable components, component patterns, or UI building blocks.
license: MIT
metadata:
  author: zoonk
  version: "1.0.0"
---

# Compound Components Pattern

This is the **REQUIRED** pattern for ALL UI components. Always use compound components by default.

## When to Use This Pattern

Use this pattern for **simple, presentational components** where:

- Children don't need to share or modify state
- CSS coordination is the main concern
- Components are purely visual building blocks

For **complex, stateful compound components** (forms, dialogs with external actions, components where siblings need shared state), see the `vercel-composition-patterns` skill.

## What are Compound Components?

Compound components are small, single-purpose components that compose together. Each component wraps exactly ONE HTML element and has ONE responsibility. They are combined like building blocks.

For more information, see the [components.build docs](https://www.components.build/llms.txt).

## Core Rules

1. **Each component = one element** - A component wraps exactly one HTML element
2. **Use `children` for content** - Never use props like `title`, `description`, `label` - pass content as children
3. **Use `className` for customization** - Allow consumers to override styles
4. **Use `data-slot` for CSS coordination** - Style child components based on parent context using `data-slot` attributes and Tailwind's `has-*` or `group-*` selectors
5. **Make components generic** - Name components for what they ARE, not what they're FOR. A component used for multiple domains should have a generic name like `MediaCard`, not `CourseHeader`

## Naming Convention

We use **flat naming** for compound components, not namespaced exports:

```tsx
// We use flat naming (consistent with shadcn/ui, Radix)
<ComposerFrame>
  <ComposerInput />
</ComposerFrame>

// NOT namespaced (Vercel style - we don't use this)
<Composer.Frame>
  <Composer.Input />
</Composer.Frame>
```

When following Vercel patterns from the `vercel-composition-patterns` skill, translate their examples to our flat naming style.

## Context/Provider - Use When Siblings Need Shared State

**Most simple UI components don't need Context.** If you're building a MediaCard, Item, or Container pattern - stick to pure composition with CSS coordination.

**Use Context when:**

- Multiple sibling components need to read/write the same state
- Components outside the main Frame need access to state/actions (e.g., dialog buttons)
- You need dependency injection (same UI, different state implementations)

For Context patterns, see the `vercel-composition-patterns` skill which covers state/actions/meta interface and provider patterns.

## Example: The Right Way

```tsx
// Each component wraps ONE element, uses children, no context needed
<MediaCard>
  <MediaCardTrigger>
    <MediaCardImage>
      <Image src={...} />
    </MediaCardImage>
    <MediaCardContent>
      <MediaCardTitle>{title}</MediaCardTitle>
      <MediaCardDescription>{description}</MediaCardDescription>
    </MediaCardContent>
    <MediaCardIndicator />
  </MediaCardTrigger>
  <MediaCardPopover>
    <MediaCardPopoverText>{fullDescription}</MediaCardPopoverText>
    <MediaCardPopoverMeta>
      <MediaCardPopoverSource>{source}</MediaCardPopoverSource>
    </MediaCardPopoverMeta>
  </MediaCardPopover>
</MediaCard>
```

## Example: The Wrong Way (Do NOT Do This)

```tsx
// BAD: Props instead of children
<CourseHeader
  title={t("Course title")}
  description={t("Course description")}
  organization={org.name}
  categories={categories}
  imageUrl={course.imageUrl}
/>

// BAD: Unnecessary Context/Provider
<CourseHeaderProvider value={{ description, organization }}>
  <CourseHeaderContent />
</CourseHeaderProvider>

// BAD: Domain-specific naming for generic patterns
<CourseHeaderImage /> // Should be <MediaCardImage /> in a shared package
```

## Using data-slot for CSS Coordination

Use `data-slot` attributes to coordinate styles between parent and child:

```tsx
// Parent component
function MediaCard({ children }) {
  return <div data-slot="media-card">{children}</div>;
}

// Child component - styled based on parent context
function MediaCardTitle({ children, className }) {
  return (
    <h1
      className={cn(
        // Base styles
        "font-semibold",
        // Contextual styles using Tailwind's group/has selectors
        "group-data-[size=sm]/media-card:text-sm",
        className,
      )}
      data-slot="media-card-title"
    >
      {children}
    </h1>
  );
}
```

## Why This Matters

1. **Flexibility** - Consumers can add, remove, or reorder any piece
2. **Reusability** - Generic components work across the entire codebase
3. **No magic** - The JSX structure shows exactly what renders
4. **Easy to extend** - Add new child components without changing existing ones
5. **Testable** - Each small component is easy to test in isolation

## Component Placement

- **Generic UI patterns** (MediaCard, Item, Container): Shared packages like `packages/ui/`
- **Domain-specific compositions**: `apps/{app}/src/components/{domain}/`
