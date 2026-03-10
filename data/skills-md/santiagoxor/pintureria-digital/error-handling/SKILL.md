---
name: error-handling
description: Specialized skill for implementing proper error handling, logging, user-friendly error messages, and error recovery strategies. Use when implementing error handling in APIs, components, or when debugging error issues.
---

# Error Handling

## Quick Start

When handling errors:

1. Never expose technical details to users
2. Log errors server-side with context
3. Provide user-friendly error messages
4. Use appropriate HTTP status codes
5. Implement error recovery when possible

## Common Patterns

### API Error Handling

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Business logic
    const result = await processRequest();
    return NextResponse.json(result);
  } catch (error) {
    // Log error with context
    console.error('API Error:', {
      endpoint: '/api/example',
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString(),
    });
    
    // Return user-friendly error
    return NextResponse.json(
      { error: 'Ha ocurrido un error. Por favor, intenta nuevamente.' },
      { status: 500 }
    );
  }
}
```

### Validation Errors

```typescript
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
});

try {
  const data = schema.parse(requestBody);
} catch (error) {
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      { 
        error: 'Datos inválidos',
        details: error.errors.map(e => ({
          field: e.path.join('.'),
          message: e.message,
        }))
      },
      { status: 400 }
    );
  }
}
```

### Component Error Handling

```typescript
'use client';

import { useState } from 'react';

function ProductCard({ product }: ProductCardProps) {
  const [error, setError] = useState<string | null>(null);
  
  const handleAddToCart = async () => {
    try {
      setError(null);
      await addToCart(product.id);
    } catch (error) {
      setError('No se pudo agregar el producto al carrito');
      console.error('Add to cart error:', error);
    }
  };
  
  return (
    <div>
      {error && (
        <div className="text-red-500 text-sm">{error}</div>
      )}
      <Button onClick={handleAddToCart}>Agregar</Button>
    </div>
  );
}
```

### Error Boundary

```typescript
'use client';

import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert" className="p-4 border border-red-300 rounded">
      <h2>Algo salió mal</h2>
      <p>{error.message}</p>
      <Button onClick={resetErrorBoundary}>Intentar de nuevo</Button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <YourComponent />
    </ErrorBoundary>
  );
}
```

## Error Types

- **400 Bad Request**: Invalid input
- **401 Unauthorized**: Not authenticated
- **403 Forbidden**: Not authorized
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server error
- **503 Service Unavailable**: Service down

## Best Practices

- Log errors with full context
- Never expose stack traces to users
- Provide actionable error messages
- Implement retry logic for transient errors
- Use error boundaries for React components
