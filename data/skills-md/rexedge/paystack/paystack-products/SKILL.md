---
name: paystack-products
description: >-
  Paystack Products API — create and manage product inventories on your integration.
  Track stock quantities, set pricing, and link products to payment pages. Use this skill
  whenever building e-commerce product catalogs, managing inventory with Paystack,
  creating shippable products, tracking stock levels and sold quantities, or adding
  products to payment pages. Also use when you see references to /product endpoint,
  PROD_ prefixed codes, product stock management, or product pricing in subunits.
---

# Paystack Products

The Products API lets you create and manage product inventories on your integration.

> Depends on: **paystack-setup** for the `paystackRequest` helper.  
> Related: **paystack-payment-pages** for adding products to hosted pages.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/product` | Create a product |
| GET | `/product` | List products |
| GET | `/product/:id` | Fetch a product |
| PUT | `/product/:id` | Update a product |

## Create Product

| Param | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | Yes | Product name |
| `description` | string | Yes | Product description |
| `price` | integer | Yes | Price in subunits (kobo/pesewas) |
| `currency` | string | Yes | Currency code |
| `unlimited` | boolean | No | `true` for unlimited stock (default: false) |
| `quantity` | integer | No | Stock count (when `unlimited` is false) |

```typescript
const product = await paystackRequest<{
  product_code: string;
  slug: string;
  id: number;
}>("/product", {
  method: "POST",
  body: JSON.stringify({
    name: "Wireless Headphones",
    description: "Premium noise-cancelling wireless headphones",
    price: 2500000, // ₦25,000
    currency: "NGN",
    unlimited: false,
    quantity: 50,
  }),
});
// product.data.product_code → "PROD_ddot3upakgl3ejt"
```

## List Products

```typescript
const products = await paystackRequest("/product?perPage=20&page=1");

// Each product includes:
// - id, name, description, product_code, slug
// - currency, price, quantity, quantity_sold
// - active, in_stock, unlimited
```

## Fetch Product

```typescript
const product = await paystackRequest(`/product/${productId}`);
```

## Update Product

```typescript
await paystackRequest(`/product/${productId}`, {
  method: "PUT",
  body: JSON.stringify({
    name: "Wireless Headphones Pro",
    description: "Updated premium headphones",
    price: 3000000,
    currency: "NGN",
    unlimited: false,
    quantity: 100,
  }),
});
```

## Product + Payment Page Flow

```typescript
// 1. Create products
const headphones = await paystackRequest("/product", {
  method: "POST",
  body: JSON.stringify({
    name: "Headphones",
    description: "Wireless headphones",
    price: 2500000,
    currency: "NGN",
    quantity: 50,
  }),
});

const case_ = await paystackRequest("/product", {
  method: "POST",
  body: JSON.stringify({
    name: "Headphone Case",
    description: "Protective carrying case",
    price: 500000,
    currency: "NGN",
    quantity: 100,
  }),
});

// 2. Create a product payment page
const page = await paystackRequest("/page", {
  method: "POST",
  body: JSON.stringify({
    name: "Audio Shop",
    type: "product",
    description: "Premium audio equipment",
  }),
});

// 3. Add products to the page
await paystackRequest(`/page/${page.data.id}/product`, {
  method: "POST",
  body: JSON.stringify({
    product: [headphones.data.id, case_.data.id],
  }),
});
// Page available at: https://paystack.com/pay/{slug}
```
