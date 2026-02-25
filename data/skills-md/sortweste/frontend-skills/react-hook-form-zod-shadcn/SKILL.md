---
name: react-hook-form-zod-shadcn
description: Build forms in React. Use when the user needs to build or refactor forms in React.
---

# React Hook Form + Zod + shadcn/ui

## Quick start

```bash
npm install react-hook-form@7.71.1 zod@4.3.6 @hookform/resolvers@5.2.2
```

Always add `'use client'` at the top of form component files.

```tsx
"use client";

import { useForm } from "react-hook-form";
// ... other imports

export function MyForm() {
  // Component logic
}
```

All forms must use the shadcn/ui Field component pattern with react-hook-form integration.

```tsx
"use client";

import { useForm } from "react-hook-form";
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";

export function MyForm() {
  const form = useForm();

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <FieldGroup>
        <Controller
          name="title"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel>Title</FieldLabel>
              <Input
                {...field}
                aria-invalid={fieldState.invalid}
                placeholder="Login button not working on mobile"
                autoComplete="off"
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />
      </FieldGroup>
    </form>
  );
}
```

Define the schema outside the component for performance. Use Zod for schema definition.

```tsx
"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";

const formSchema = z.object({
  name: z.string().trim().min(5, { error: "Must be at least 5 characters." }),
  description: z.string().trim().min(20, { error: "Must be at least 20 characters." }),
    .string()
    .trim()
    .min(20, { error: "Must be at least 20 characters." }),
});

type FormData = z.infer<typeof formSchema>;

export function MyForm() {
  const form = useForm<FormData>();
  // ...
}
```

Generate a **single** unique ID per form using React's `useId` hook. **DO NOT** generate a separate ID for every field. Generate once, reuse with field names.

```tsx
"use client";

import { useId } from "react";
import { useForm } from "react-hook-form";

export function MyForm() {
  const formId = useId(); // Generate once
  const form = useForm();

  return (
    <form id={formId} onSubmit={form.handleSubmit(handleSubmit)}>
      <FieldGroup>
        <Controller
          name="title"
          control={form.control}
          render={({ field, fieldState }) => (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel htmlFor={`${formId}-title`}>Title</FieldLabel>
              <Input
                {...field}
                id={`${formId}-title`} // Use it with template literals for each field.
                aria-invalid={fieldState.invalid}
                placeholder="Login button not working on mobile"
                autoComplete="off"
                disabled={form.formState.isSubmitting}
              />
              {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
            </Field>
          )}
        />
      </FieldGroup>
    </form>
  );
}
```

Always add `mode: "onChange"` to the useForm hook configuration for real-time validation feedback.

```tsx
const form = useForm<FormData>({
  resolver: standardSchemaResolver(formSchema),
  mode: "onChange", // Validates on every change
});
```

Initialize form with `defaultValues` that match the schema's expected types.

```tsx
const form = useForm<FormData>({
  resolver: standardSchemaResolver(formSchema),
  mode: "onChange",
  defaultValues: {
    username: "",
    email: "",
  },
});
```

**CRITICAL**: Due to an active issue, always import from `@hookform/resolvers/standard-schema` but use the standard-schema resolver pattern.

```tsx
"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { standardSchemaResolver } from "@hookform/resolvers/standard-schema";

const formSchema = z.object({
  //...
});

type FormData = z.infer<typeof formSchema>;

export function MyForm() {
  const form = useForm<FormData>({
    resolver: standardSchemaResolver(formSchema),
    mode: "onChange",
  });
}
```

Disable both the submit button and all form fields when `form.formState.isSubmitting` is true to prevent duplicate submissions and improve UX.

```tsx
return (
  <form id={formId} onSubmit={form.handleSubmit(handleSubmit)}>
    <FieldGroup>
      <Controller
        name="email"
        control={form.control}
        render={({ field, fieldState }) => (
          <Field data-invalid={fieldState.invalid}>
            <FieldLabel htmlFor={`${formId}-email`}>email</FieldLabel>
            <Input
              {...field}
              id={`${formId}-email`}
              aria-invalid={fieldState.invalid}
              placeholder="test@example.com"
              autoComplete="off"
              disabled={form.formState.isSubmitting}
            />
            {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
          </Field>
        )}
      />
    </FieldGroup>
    <Button type="submit" form={formId} disabled={form.formState.isSubmitting}>
      {form.formState.isSubmitting ? "Submitting..." : "Submit"}
    </Button>
  </form>
);
```

Disable the submit button when the form is not valid using `form.formState.isValid`.

```tsx
return (
  <form id={formId} onSubmit={form.handleSubmit(handleSubmit)}>
    {/* Form fields */}

    <Button
      type="submit"
      form={formId}
      disabled={!form.formState.isValid || form.formState.isSubmitting}
    >
      {form.formState.isSubmitting ? "Submitting..." : "Submit"}
    </Button>
  </form>
);
```

**CRITICAL**: Always use `safeParse()` in the form submission handler to validate field values. If validation fails, call `form.trigger()` to display errors.

```tsx
"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { standardSchemaResolver } from "@hookform/resolvers/standard-schema";

const formSchema = z.object({
  //...
});

type FormData = z.infer<typeof formSchema>;

export function MyForm() {
  const form = useForm<FormData>({
    resolver: standardSchemaResolver(formSchema),
    mode: "onChange",
  });
  const formId = useId(); // Generate once

  const handleSubmit = async (data: FormData) => {
    // Validate using safeParse
    const result = formSchema.safeParse(data);

    if (!result.success) {
      // Trigger form validation to show errors
      form.trigger();
      return;
    }

    try {
      // API call or other submission logic
    } catch (error) {
      console.error("Submission error:", error);
    }
  };

  return (
    <form id={formId} onSubmit={form.handleSubmit(handleSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

Reset form after submission.

```tsx
const handleSubmit = async (data: FormData) => {
  //... submission logic
  form.reset(); // Reset form after successful submission
};
```

## Resources

**Zod reference**: See [references/zod.md](references/zod.md)
**shadcn/ui reference**: See [references/shadcn-ui.md](references/shadcn-ui.md)
**React Hook Form reference**: See [references/react-hook-form.md](references/react-hook-form.md)
