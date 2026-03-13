---
name: shadcn
description: Building UI with shadcn/ui components for consistent, accessible interfaces. Use when creating forms, buttons, dialogs, tables, and other UI elements with React and Tailwind CSS.
license: MIT
metadata:
  author: devrecruit
  version: "1.0"
compatibility: React 16.8+, Tailwind CSS 3+
---

# Shadcn Skills

This skill covers best practices for integrating and customizing shadcn/ui components to build accessible, maintainable interfaces.

## Component Integration

### Purpose

Seamlessly integrate shadcn/ui components into your application with proper setup and usage patterns.

### Initial Setup

1. **Install shadcn/ui**

   ```bash
   # Initialize shadcn/ui in your project
   npx shadcn-ui@latest init

   # Or for an existing project
   npx shadcn-ui@latest add button
   ```

2. **Components Directory Structure**

   ```
   components/
   ├── ui/
   │   ├── button.tsx
   │   ├── card.tsx
   │   ├── field.tsx
   │   ├── input.tsx
   │   └── ...
   └── [feature]/
       └── [component].tsx
   ```

3. **Using Components**

   ```typescript
   import { Button } from "@/components/ui/button";
   import { Card } from "@/components/ui/card";
   import { Input } from "@/components/ui/input";

   export function MyComponent() {
     return (
       <Card>
         <Input placeholder="Enter text..." />
         <Button>Submit</Button>
       </Card>
     );
   }
   ```

### Common Components

1. **Field Components with Base UI**

   ```typescript
   import { Field } from "@/components/ui/field";
   import { Input } from "@/components/ui/input";
   import { useForm } from "react-hook-form";
   import { zodResolver } from "@hookform/resolvers/zod";

   export function MyForm() {
     const {
       register,
       handleSubmit,
       formState: { errors },
     } = useForm({
       resolver: zodResolver(schema),
       defaultValues: {
         /* ... */
       },
     });

     // Call server action on submit (preferred over API route)
     const onSubmit = async (data) => {
       const result = await createEntityAction(data);
       if (result.success) {
         // Handle success
       }
     };

     return (
       <form onSubmit={handleSubmit(onSubmit)}>
         <Field label="Email" error={errors.email?.message}>
           <Input placeholder="user@example.com" {...register("email")} />
         </Field>
         <Button type="submit">Submit</Button>
       </form>
     );
   }
   ```

2. **Dialog/Modal Components**

   ```typescript
   import {
     Dialog,
     DialogContent,
     DialogHeader,
     DialogTitle,
   } from "@/components/ui/dialog";

   export function MyDialog() {
     const [open, setOpen] = React.useState(false);

     return (
       <Dialog open={open} onOpenChange={setOpen}>
         <DialogContent>
           <DialogHeader>
             <DialogTitle>Dialog Title</DialogTitle>
           </DialogHeader>
           {/* Content */}
         </DialogContent>
       </Dialog>
     );
   }
   ```

3. **Table Component**

   ```typescript
   import {
     Table,
     TableBody,
     TableCell,
     TableHead,
     TableHeader,
     TableRow,
   } from "@/components/ui/table";

   export function DataTable({ data, columns }) {
     return (
       <Table>
         <TableHeader>
           <TableRow>
             {columns.map((col) => (
               <TableHead key={col.key}>{col.label}</TableHead>
             ))}
           </TableRow>
         </TableHeader>
         <TableBody>
           {data.map((row) => (
             <TableRow key={row.id}>
               {columns.map((col) => (
                 <TableCell key={col.key}>{row[col.key]}</TableCell>
               ))}
             </TableRow>
           ))}
         </TableBody>
       </Table>
     );
   }
   ```

## Theming

### Purpose

Customize shadcn/ui components to match your application's brand and style.

### Theming Strategy

1. **CSS Variables**

   - shadcn uses CSS variables for theming
   - Configure colors in `app/globals.css`
   - Support light and dark modes

2. **Color Configuration**

   ```css
   /* app/globals.css */
   @layer base {
     :root {
       --background: 0 0% 100%;
       --foreground: 0 0% 3.6%;
       --primary: 0 72.2% 50.6%;
       --secondary: 0 0% 96.1%;
       /* ... more colors ... */
     }

     .dark {
       --background: 0 0% 3.6%;
       --foreground: 0 0% 98%;
       /* ... dark mode colors ... */
     }
   }
   ```

3. **OKLCH Colors (Tailwind v4)**

   - Use OKLCH format for better color spaces
   - Example: `oklch(50% 0.1 240)`
   - More perceptually uniform than RGB

4. **Custom Component Variants**

   ```typescript
   // components/ui/button.tsx
   import { cva, type VariantProps } from "class-variance-authority";

   const buttonVariants = cva(
     "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors",
     {
       variants: {
         variant: {
           default: "bg-primary text-primary-foreground hover:bg-primary/90",
           secondary:
             "bg-secondary text-secondary-foreground hover:bg-secondary/80",
           ghost: "hover:bg-accent hover:text-accent-foreground",
         },
         size: {
           default: "h-10 px-4 py-2",
           sm: "h-9 px-3 text-xs",
           lg: "h-11 px-8",
         },
       },
       defaultVariants: {
         variant: "default",
         size: "default",
       },
     }
   );

   export interface ButtonProps
     extends React.ButtonHTMLAttributes<HTMLButtonElement>,
       VariantProps<typeof buttonVariants> {}

   export function Button({ className, variant, size, ...props }: ButtonProps) {
     return (
       <button
         className={buttonVariants({ variant, size, className })}
         {...props}
       />
     );
   }
   ```

5. **Dark Mode Setup**

   ```typescript
   // components/theme-provider.tsx
   "use client";

   import { ThemeProvider as NextThemesProvider } from "next-themes";

   export function ThemeProvider({ children, ...props }) {
     return (
       <NextThemesProvider
         attribute="class"
         defaultTheme="system"
         enableSystem
         {...props}
       >
         {children}
       </NextThemesProvider>
     );
   }
   ```

## Accessibility

### Purpose

Ensure shadcn/ui components are accessible to all users, including those using assistive technologies.

### Key Principles

1.  **Semantic HTML**

    - shadcn components use semantic elements
    - Buttons are buttons, not divs
    - Links are links, not buttons
    - Forms use proper label associations

2.  **ARIA Attributes**

    - shadcn includes proper ARIA labels
    - Use `aria-label` for icon-only buttons
    - Use `aria-describedby` for form hints

3.  **Keyboard Navigation**

    - All interactive elements are keyboard accessible
    - Tab order is logical and visible
    - Escape key closes modals and dropdowns
    - Enter key submits forms

4.  **Color Contrast**

    - Ensure sufficient contrast ratios (WCAG AA minimum)
    - Don't rely on color alone to convey information
    - Test with accessibility tools

5.  **Accessible Forms**

    ```typescript
    const {
      register,
      formState: { errors },
    } = useForm({
      resolver: zodResolver(schema),
    });

    <Field label="Email Address" error={errors.email?.message}>
      <Input
        id="email"
        type="email"
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? "email-error" : undefined}
        placeholder="user@example.com"
        {...register("email")}
      />
      {errors.email && (
        <p id="email-error" className="text-sm text-destructive">
          {errors.email.message}
        </p>
      )}
    </Field>;
    ```

6.  **Focus Management**
    - Visible focus indicators (built into shadcn)
    - Modal focus trapping (Dialog component)
    - Focus restoration after closing modals

### Testing for Accessibility

- Use accessibility tools (axe DevTools, WAVE)
- Test keyboard navigation manually
- Test with screen readers (NVDA, JAWS, VoiceOver)
- Check color contrast ratios
- Verify form labels and error messages

## Advanced Patterns

### Custom Hooks with shadcn

```typescript
// hooks/use-form-state.ts
import { useCallback } from "react";
import { useForm } from "react-hook-form";

export function useFormState(schema, onSubmit) {
  const form = useForm({
    resolver: zodResolver(schema),
  });

  const handleSubmit = useCallback(
    async (data) => {
      try {
        await onSubmit(data);
      } catch (error) {
        form.setError("root", { message: error.message });
      }
    },
    [form, onSubmit]
  );

  return { ...form, handleSubmit };
}
```

### Compound Components

```typescript
// components/card-with-form.tsx
export function CardWithForm({ title, onSubmit, children }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit}>{children}</form>
      </CardContent>
    </Card>
  );
}
```

## Development Checklist

When using shadcn/ui:

- [ ] Components are properly imported from @/components/ui
- [ ] Color theme is configured in globals.css
- [ ] Dark mode is implemented with ThemeProvider
- [ ] Forms use react-hook-form + Zod validation
- [ ] Forms call server actions instead of API routes
- [ ] Using Base UI components instead of Radix UI
- [ ] Using Field components instead of Form/FormField
- [ ] All interactive elements have proper ARIA labels
- [ ] Keyboard navigation is tested
- [ ] Color contrast meets WCAG AA standards
- [ ] Focus indicators are visible
- [ ] Components follow project naming conventions
- [ ] Custom variants are documented
