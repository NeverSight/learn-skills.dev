---
name: ui-components
description: Specialized skill for working with shadcn/ui components, Tailwind CSS styling, responsive design, and component composition. Use when creating new UI components, styling existing components, implementing responsive layouts, or working with the design system.
---

# UI Components

## Quick Start

When working with UI components:

1. Use shadcn/ui components from `@/components/ui/`
2. Follow mobile-first approach
3. Use Tailwind CSS for styling
4. Maintain accessibility (WCAG 2.1 AA)
5. Use design system colors and spacing

## Key Files

- `src/components/ui/` - shadcn/ui components
- `tailwind.config.ts` - Tailwind configuration
- `src/styles/` - Global styles
- `src/components/` - Custom components

## Common Patterns

### Using shadcn/ui Components

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

function ProductForm() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Nuevo Producto</CardTitle>
      </CardHeader>
      <CardContent>
        <Input placeholder="Nombre del producto" />
        <Button className="mt-4">Guardar</Button>
      </CardContent>
    </Card>
  );
}
```

### Mobile-First Responsive

```typescript
<div className="
  flex flex-col
  md:flex-row md:items-center
  gap-4
  p-4
  md:p-6
">
  <h1 className="text-2xl md:text-3xl lg:text-4xl">
    Título
  </h1>
</div>
```

### Button Styles

```typescript
// Primary action (yellow)
<Button className="bg-yellow-400 text-2xl rounded-xl">
  Agregar al Carrito
</Button>

// Secondary
<Button variant="outline">
  Cancelar
</Button>

// Destructive
<Button variant="destructive">
  Eliminar
</Button>
```

### Tenant Colors

```typescript
// Use CSS variables for tenant-specific colors
<div 
  className="bg-[var(--tenant-primary)]"
  style={{
    '--tenant-primary': tenant.primary_color || '#ea5a17',
  }}
>
  Content
</div>
```

## Design System

### Colors
- Primary: Blaze Orange (#ea5a17)
- Secondary: Fun Green
- Accent: Bright Sun
- Use Tailwind color palette

### Spacing
- Use Tailwind spacing scale (4, 8, 12, 16, 24, 32, etc.)
- Mobile: Smaller padding/margins
- Desktop: Larger spacing

### Typography
- Mobile: text-base (16px) default
- Desktop: text-lg (18px) default
- Headings: text-2xl, text-3xl, text-4xl

## Accessibility

- Use semantic HTML
- Include ARIA labels when needed
- Ensure keyboard navigation
- Maintain color contrast ratios
- Support screen readers
