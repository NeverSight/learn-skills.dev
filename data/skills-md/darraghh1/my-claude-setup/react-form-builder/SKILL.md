---
name: react-form-builder
description: "Create client-side forms with react-hook-form, shadcn/ui, Zod validation, and server action integration for Next.js applications."
metadata:
  version: 1.0.0
---

# React Form Builder Expert

You are a React form architect helping build forms in a Next.js/Supabase application.

## Why This Skill Exists

The user's codebase has established form patterns using react-hook-form, shadcn/ui components, and server actions. Deviating from these patterns causes real problems:

| Deviation | Harm to User |
|-----------|--------------|
| Missing `useTransition` | No loading indicator — users click submit multiple times, creating duplicate records |
| Missing `isRedirectError` handling | Errors swallowed silently after successful redirects, making debugging impossible |
| Using external UI components | Inconsistent styling, bundle bloat, and double maintenance when `@/components/ui` already has the component |
| Missing `data-test` attributes | E2E tests can't find form elements — Playwright test suite breaks |
| Multiple `useState` for loading/error | Inconsistent state transitions that are harder to reason about and debug |
| Missing form validation feedback | Users don't know what's wrong with their input, leading to frustration and support requests |

Following the patterns below prevents these failures.

## Core Patterns

### 1. Form Structure

- Use `useForm` from react-hook-form WITHOUT redundant generic types when using zodResolver (let the resolver infer types)
- Implement Zod schemas for validation, stored in `_lib/schema/` directory
- Use `@/components/ui/form` components (Form, FormField, FormItem, FormLabel, FormControl, FormDescription, FormMessage)
- Handle loading states with `useTransition` hook (not `useState` for loading)
- Implement error handling with try/catch and `isRedirectError`

### 2. Server Action Integration

- Call server actions within `startTransition` for proper loading states
- Use `toast.promise()` or `toast.success()`/`toast.error()` for user feedback
- Handle redirect errors using `isRedirectError` from 'next/dist/client/components/redirect-error'
- Display error states using Alert components from `@/components/ui/alert`

### 3. Code Organization

```
_lib/
├── schema/
│   └── feature.schema.ts    # Shared Zod schemas (client + server)
├── server/
│   └── server-actions.ts    # Server actions
└── client/
    └── forms.tsx           # Form components
```

### 4. Import Guidelines

- Toast: `import { toast } from 'sonner'`
- Form: `import { Form, FormField, ... } from '@/components/ui/form'`
- Check `@/components/ui` for components before using external packages — the user depends on visual consistency across the app

### 5. State Management

- `useTransition` for pending states (not `useState` for loading — `useTransition` integrates with React's concurrent features)
- `useState` only for error state
- Avoid multiple separate `useState` calls — prefer a single state object when states change together (prevents re-render bugs)
- `useEffect` is a code smell for forms — validation should be schema-driven, not effect-driven

### 6. Validation

- Reusable Zod schemas shared between client and server — a single source of truth prevents validation drift
- Use `mode: 'onChange'` and `reValidateMode: 'onChange'` so users get immediate feedback
- Provide clear, user-friendly error messages in schemas
- Use `zodResolver` to connect schema to form (don't add redundant generics to `useForm`)

### 7. Accessibility and UX

- FormLabel for screen readers (every input needs a label)
- FormDescription for guidance text
- FormMessage for error display
- Submit button disabled during `pending` state (prevents duplicate submissions)
- `data-test` attributes on all interactive elements for E2E testing

## Error Handling Template

```typescript
const onSubmit = (data: FormData) => {
  setError(false);

  startTransition(async () => {
    try {
      await serverAction(data);
    } catch (error) {
      if (!isRedirectError(error)) {
        setError(true);
      }
    }
  });
};
```

## Toast Promise Pattern (Preferred)

```typescript
const onSubmit = (data: FormData) => {
  startTransition(async () => {
    await toast.promise(serverAction(data), {
      loading: 'Creating...',
      success: 'Created successfully!',
      error: 'Failed to create.',
    });
  });
};
```

## Complete Form Example

```tsx
'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { useTransition, useState } from 'react';
import { isRedirectError } from 'next/dist/client/components/redirect-error';
import type { z } from 'zod';

import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { toast } from 'sonner';

import { CreateEntitySchema } from '../_lib/schema/entity.schema';
import { createEntityAction } from '../_lib/server/server-actions';

export function CreateEntityForm() {
  const [pending, startTransition] = useTransition();
  const [error, setError] = useState(false);

  const form = useForm({
    resolver: zodResolver(CreateEntitySchema),
    defaultValues: {
      name: '',
      description: '',
    },
    mode: 'onChange',
    reValidateMode: 'onChange',
  });

  const onSubmit = (data: z.infer<typeof CreateEntitySchema>) => {
    setError(false);

    startTransition(async () => {
      try {
        await toast.promise(createEntityAction(data), {
          loading: 'Creating...',
          success: 'Created successfully!',
          error: 'Failed to create.',
        });
      } catch (e) {
        if (!isRedirectError(e)) {
          setError(true);
        }
      }
    });
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <Form {...form}>
        {error && (
          <Alert variant="destructive">
            <AlertDescription>
              Something went wrong. Please try again.
            </AlertDescription>
          </Alert>
        )}

        <FormField
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input
                  data-test="entity-name-input"
                  placeholder="Enter name"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={pending}
          data-test="submit-entity-button"
        >
          {pending ? 'Creating...' : 'Create'}
        </Button>
      </Form>
    </form>
  );
}
```

## Troubleshooting

### Form submits but nothing happens (no loading, no feedback)

**Cause:** Missing `useTransition` — the server action is called outside `startTransition`, so React doesn't track the pending state.

**Fix:** Wrap the server action call in `startTransition(async () => { ... })` and use the `pending` value to disable the submit button and show loading state.

### Missing `'use client'` directive

**Cause:** Form components use hooks (`useForm`, `useState`, `useTransition`) which require client-side rendering. Without the directive, Next.js tries to render them on the server, causing cryptic errors.

**Fix:** Add `'use client';` as the very first line of any form component file.

### zodResolver type mismatch with `.refine()`

**Cause:** `.refine()` changes `ZodObject` to `ZodEffects`, which breaks `zodResolver` type inference. The form types no longer match the schema types.

**Fix:** Create a base schema (for `z.infer` typing and `useForm`) and a separate refined schema (for validation in server actions).

### Stale form data after successful submission

**Cause:** The form state isn't reset after a successful mutation, or `revalidatePath` is missing from the server action.

**Fix:** Call `form.reset()` in the success handler, and ensure the server action calls `revalidatePath` after the mutation.

### Wrong form component imports (external packages)

**Cause:** Using `@radix-ui/react-form` or other external form packages instead of `@/components/ui/form`. This creates visual inconsistency and bundle bloat.

**Fix:** Always import form components from `@/components/ui/form`. Check `@/components/ui` first before reaching for external packages.

## Components

See [Components](components.md) for field-level examples (Select, Checkbox, Switch, Textarea, etc.).
