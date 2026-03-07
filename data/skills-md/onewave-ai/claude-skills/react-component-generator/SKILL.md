---
name: react-component-generator
description: Generate React components with TypeScript, proper props, hooks, and accessibility. Use when creating new React components, UI elements, or refactoring existing components.
---

# React Component Generator

## Instructions

When creating React components:

1. **Determine component type**: Client or Server component
2. **Define props interface** with TypeScript
3. **Implement with best practices**
4. **Add accessibility attributes**

## Templates

### Client Component

```tsx
'use client';

import { useState, useCallback } from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    ghost: 'hover:bg-gray-100',
  };

  const sizes = {
    sm: 'h-8 px-3 text-sm',
    md: 'h-10 px-4',
    lg: 'h-12 px-6 text-lg',
  };

  return (
    <button
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      {...props}
    >
      {isLoading ? <span className="animate-spin mr-2">⏳</span> : null}
      {children}
    </button>
  );
}
```

### Server Component

```tsx
import { db } from '@/lib/db';

interface UserListProps {
  limit?: number;
}

export async function UserList({ limit = 10 }: UserListProps) {
  const users = await db.user.findMany({ take: limit });

  if (users.length === 0) {
    return <p className="text-gray-500">No users found.</p>;
  }

  return (
    <ul role="list" className="divide-y">
      {users.map((user) => (
        <li key={user.id} className="py-4">
          <span>{user.name}</span>
        </li>
      ))}
    </ul>
  );
}
```

### Form Component with React Hook Form

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
});

type FormData = z.infer<typeof schema>;

export function LoginForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          {...register('email')}
        />
        {errors.email && (
          <p id="email-error" role="alert">{errors.email.message}</p>
        )}
      </div>
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Loading...' : 'Submit'}
      </button>
    </form>
  );
}
```

## Accessibility Checklist

- [ ] Use semantic HTML elements
- [ ] Add `aria-label` for icon-only buttons
- [ ] Include `role` attributes where needed
- [ ] Ensure keyboard navigation works
- [ ] Add `aria-invalid` and `aria-describedby` for form errors
- [ ] Use `aria-busy` for loading states
