---
name: testing-qa
description: Specialized skill for writing and maintaining tests including unit tests, integration tests, E2E tests with Playwright, and accessibility tests. Use when writing tests for new features, debugging failed tests, improving test coverage, or setting up E2E tests.
---

# Testing and QA

## Quick Start

When writing tests:

1. Use Jest for unit tests
2. Use React Testing Library for component tests
3. Use Playwright for E2E tests
4. Use jest-axe for accessibility tests
5. Maintain >70% coverage

## Key Files

- `jest.config.js` - Jest configuration
- `playwright.config.ts` - Playwright configuration
- `src/__tests__/` - Unit and integration tests
- `e2e/` - E2E tests
- `__mocks__/` - Shared mocks

## Common Patterns

### Component Test

```typescript
import { render, screen } from '@testing-library/react';
import { ProductCard } from '@/components/Product/ProductCard';

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    name: 'Pintura Blanca',
    price: 5000,
    image: '/images/product.jpg',
  };
  
  it('should render product information', () => {
    render(<ProductCard product={mockProduct} />);
    
    expect(screen.getByText('Pintura Blanca')).toBeInTheDocument();
    expect(screen.getByText('$5,000')).toBeInTheDocument();
  });
});
```

### API Test

```typescript
import { GET } from '@/app/api/products/route';
import { NextRequest } from 'next/server';

describe('/api/products', () => {
  it('should return products for tenant', async () => {
    const request = new NextRequest('http://localhost/api/products', {
      headers: {
        'x-tenant-id': 'test-tenant-id',
      },
    });
    
    const response = await GET(request);
    const data = await response.json();
    
    expect(response.status).toBe(200);
    expect(Array.isArray(data)).toBe(true);
  });
});
```

### E2E Test

```typescript
import { test, expect } from '@playwright/test';

test('should complete checkout flow', async ({ page }) => {
  await page.goto('/product/pintura-blanca');
  await page.click('button:has-text("Agregar al carrito")');
  await page.click('a[href="/checkout"]');
  await page.fill('input[name="email"]', 'test@example.com');
  await expect(page.locator('text=Resumen de compra')).toBeVisible();
});
```

### Accessibility Test

```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

it('should not have accessibility violations', async () => {
  const { container } = render(<ProductCard product={mockProduct} />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```
