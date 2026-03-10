---
name: analytics-tracking
description: Specialized skill for implementing and maintaining the analytics system including event tracking, e-commerce metrics, GA4 integration, and admin dashboard. Use when implementing tracking, creating custom metrics, integrating external analytics services, or debugging tracking issues.
---

# Analytics and Tracking

## Quick Start

When implementing analytics:

1. Use `trackEvent()` from `@/lib/integrations/analytics`
2. Track e-commerce events (view_item, add_to_cart, purchase)
3. Include relevant properties (item_id, price, category)
4. Verify events in DevTools Network tab

## Key Files

- `src/lib/integrations/analytics/` - Analytics integration
- `src/components/Analytics/` - Analytics components
- `src/app/api/track/` - Tracking API
- `src/hooks/useAnalytics.ts` - Analytics hook

## Common Events

### Track Product View

```typescript
import { trackEvent } from '@/lib/integrations/analytics';

await trackEvent({
  event: 'view_item',
  properties: {
    item_id: product.id,
    item_name: product.name,
    price: product.price,
    currency: 'ARS',
    category: product.category.name,
  },
});
```

### Track Purchase

```typescript
await trackEvent({
  event: 'purchase',
  properties: {
    transaction_id: order.id,
    value: order.total,
    currency: 'ARS',
    items: order.items.map(item => ({
      item_id: item.product_id,
      item_name: item.product.name,
      price: item.price,
      quantity: item.quantity,
    })),
  },
});
```

### Use Hook

```typescript
import { useAnalytics } from '@/hooks/useAnalytics';

function ProductCard({ product }: ProductCardProps) {
  const { track } = useAnalytics();
  
  const handleClick = () => {
    track('product_click', {
      product_id: product.id,
      product_name: product.name,
    });
  };
  
  return <div onClick={handleClick}>...</div>;
}
```

## Event Types

- `page_view` - Page view
- `product_view` - Product view
- `add_to_cart` - Add to cart
- `remove_from_cart` - Remove from cart
- `begin_checkout` - Begin checkout
- `purchase` - Purchase completed
- `search` - Product search
