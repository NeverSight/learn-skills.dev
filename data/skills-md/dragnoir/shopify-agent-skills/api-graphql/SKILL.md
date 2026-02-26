---
name: api-graphql
description: Work with Shopify GraphQL APIs including Admin API and Storefront API. Use this skill for querying and mutating Shopify data, managing products, orders, customers, handling pagination, working with metafields, and understanding rate limits. Covers authentication, queries, mutations, and webhooks.
license: MIT
compatibility: Requires API access credentials and understanding of GraphQL
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Shopify GraphQL APIs

## When to use this skill

Use this skill when:

- Querying Shopify data (products, orders, customers)
- Creating or updating resources via mutations
- Building integrations with Shopify stores
- Working with metafields and metaobjects
- Handling pagination in API responses
- Managing API authentication and rate limits

## API Types

### Admin API

- Full store access (backend only)
- Requires authentication (OAuth or API key)
- Used by apps and integrations

### Storefront API

- Public storefront access
- Uses public access token
- Safe for frontend/client-side

## Getting Started

### Admin API Authentication

```javascript
// Using @shopify/shopify-api
import { shopifyApi, LATEST_API_VERSION } from "@shopify/shopify-api";

const shopify = shopifyApi({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET,
  scopes: ["read_products", "write_products"],
  hostName: "your-app.com",
  apiVersion: LATEST_API_VERSION,
});
```

### Making Requests

```javascript
// In a Remix app route
import { authenticate } from "../shopify.server";

export async function loader({ request }) {
  const { admin } = await authenticate.admin(request);

  const response = await admin.graphql(`
    query {
      products(first: 10) {
        nodes {
          id
          title
        }
      }
    }
  `);

  return response.json();
}
```

## Common Queries

### Products

```graphql
# Get products with variants
query GetProducts($first: Int!, $after: String) {
  products(first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      title
      handle
      description
      status
      vendor
      productType
      tags
      featuredImage {
        url
        altText
      }
      variants(first: 10) {
        nodes {
          id
          title
          sku
          price
          compareAtPrice
          inventoryQuantity
          selectedOptions {
            name
            value
          }
        }
      }
      priceRange {
        minVariantPrice {
          amount
          currencyCode
        }
        maxVariantPrice {
          amount
          currencyCode
        }
      }
    }
  }
}
```

```graphql
# Get single product by ID
query GetProduct($id: ID!) {
  product(id: $id) {
    id
    title
    description
    variants(first: 100) {
      nodes {
        id
        title
        price
      }
    }
  }
}

# Get product by handle
query GetProductByHandle($handle: String!) {
  productByHandle(handle: $handle) {
    id
    title
  }
}
```

### Orders

```graphql
query GetOrders($first: Int!, $query: String) {
  orders(first: $first, query: $query) {
    nodes {
      id
      name
      email
      createdAt
      displayFinancialStatus
      displayFulfillmentStatus
      totalPriceSet {
        shopMoney {
          amount
          currencyCode
        }
      }
      customer {
        id
        firstName
        lastName
        email
      }
      lineItems(first: 50) {
        nodes {
          id
          title
          quantity
          variant {
            id
            sku
          }
          originalTotalSet {
            shopMoney {
              amount
            }
          }
        }
      }
      shippingAddress {
        address1
        city
        province
        country
        zip
      }
    }
  }
}
```

### Customers

```graphql
query GetCustomers($first: Int!, $query: String) {
  customers(first: $first, query: $query) {
    nodes {
      id
      firstName
      lastName
      email
      phone
      ordersCount
      totalSpent {
        amount
        currencyCode
      }
      addresses(first: 5) {
        address1
        city
        province
        country
        zip
      }
      tags
      createdAt
    }
  }
}
```

### Collections

```graphql
query GetCollection($handle: String!) {
  collectionByHandle(handle: $handle) {
    id
    title
    description
    products(first: 20) {
      nodes {
        id
        title
        featuredImage {
          url
        }
      }
    }
  }
}
```

### Inventory

```graphql
query GetInventory($locationId: ID!) {
  location(id: $locationId) {
    inventoryLevels(first: 100) {
      nodes {
        id
        available
        item {
          id
          variant {
            id
            displayName
            sku
          }
        }
      }
    }
  }
}
```

## Common Mutations

### Create Product

```graphql
mutation CreateProduct($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "input": {
    "title": "New Product",
    "descriptionHtml": "<p>Product description</p>",
    "vendor": "My Store",
    "productType": "Apparel",
    "tags": ["new", "featured"],
    "variants": [
      {
        "price": "29.99",
        "sku": "NEW-001",
        "inventoryManagement": "SHOPIFY",
        "inventoryPolicy": "DENY"
      }
    ]
  }
}
```

### Update Product

```graphql
mutation UpdateProduct($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "input": {
    "id": "gid://shopify/Product/123456",
    "title": "Updated Title",
    "tags": ["sale", "featured"]
  }
}
```

### Create Order

```graphql
mutation CreateDraftOrder($input: DraftOrderInput!) {
  draftOrderCreate(input: $input) {
    draftOrder {
      id
      invoiceUrl
    }
    userErrors {
      field
      message
    }
  }
}
```

### Update Inventory

```graphql
mutation AdjustInventory($input: InventoryAdjustQuantityInput!) {
  inventoryAdjustQuantity(input: $input) {
    inventoryLevel {
      available
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "input": {
    "inventoryLevelId": "gid://shopify/InventoryLevel/123456",
    "availableDelta": 10
  }
}
```

## Metafields

### Read Metafields

```graphql
# Product metafields
query GetProductMetafields($id: ID!) {
  product(id: $id) {
    metafields(first: 20) {
      nodes {
        id
        namespace
        key
        value
        type
      }
    }
    # Specific metafield
    careInstructions: metafield(namespace: "custom", key: "care_instructions") {
      value
    }
  }
}
```

### Write Metafields

```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields {
      id
      key
      value
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "metafields": [
    {
      "ownerId": "gid://shopify/Product/123456",
      "namespace": "custom",
      "key": "care_instructions",
      "value": "Machine wash cold",
      "type": "single_line_text_field"
    },
    {
      "ownerId": "gid://shopify/Product/123456",
      "namespace": "custom",
      "key": "dimensions",
      "value": "{\"width\": 10, \"height\": 20, \"depth\": 5}",
      "type": "json"
    }
  ]
}
```

### Metafield Types

| Type                     | Description | Example Value            |
| ------------------------ | ----------- | ------------------------ |
| `single_line_text_field` | Short text  | `"Hello"`                |
| `multi_line_text_field`  | Long text   | `"Line 1\nLine 2"`       |
| `number_integer`         | Integer     | `"42"`                   |
| `number_decimal`         | Decimal     | `"19.99"`                |
| `boolean`                | True/False  | `"true"`                 |
| `date`                   | Date        | `"2025-01-15"`           |
| `json`                   | JSON object | `"{\"key\": \"value\"}"` |
| `url`                    | URL         | `"https://example.com"`  |
| `color`                  | Color hex   | `"#FF0000"`              |

## Pagination

### Cursor-Based Pagination

```javascript
async function getAllProducts(admin) {
  let products = [];
  let hasNextPage = true;
  let cursor = null;

  while (hasNextPage) {
    const response = await admin.graphql(
      `
      query GetProducts($first: Int!, $after: String) {
        products(first: $first, after: $after) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            title
          }
        }
      }
    `,
      {
        variables: { first: 50, after: cursor },
      },
    );

    const data = await response.json();
    products = [...products, ...data.data.products.nodes];
    hasNextPage = data.data.products.pageInfo.hasNextPage;
    cursor = data.data.products.pageInfo.endCursor;
  }

  return products;
}
```

## Rate Limits

### Understanding Cost

```graphql
query {
  products(first: 100) {
    nodes {
      id
      title
    }
  }
}
```

Response includes:

```json
{
  "extensions": {
    "cost": {
      "requestedQueryCost": 102,
      "actualQueryCost": 52,
      "throttleStatus": {
        "maximumAvailable": 2000,
        "currentlyAvailable": 1948,
        "restoreRate": 100
      }
    }
  }
}
```

### Handling Rate Limits

```javascript
async function queryWithRetry(admin, query, variables, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await admin.graphql(query, { variables });
      const data = await response.json();

      if (data.errors?.some((e) => e.extensions?.code === "THROTTLED")) {
        const waitTime = Math.pow(2, attempt) * 1000;
        await new Promise((resolve) => setTimeout(resolve, waitTime));
        continue;
      }

      return data;
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
    }
  }
}
```

## Storefront API

### Authentication

```javascript
const storefrontClient = new StorefrontApiClient({
  privateAccessToken: process.env.STOREFRONT_ACCESS_TOKEN,
  storeDomain: "your-store.myshopify.com",
  apiVersion: "2025-01",
});
```

### Product Query (Storefront)

```graphql
query GetProduct($handle: String!) {
  product(handle: $handle) {
    id
    title
    description
    images(first: 5) {
      nodes {
        url
        altText
      }
    }
    variants(first: 100) {
      nodes {
        id
        title
        price {
          amount
          currencyCode
        }
        availableForSale
      }
    }
  }
}
```

### Cart Operations (Storefront)

```graphql
# Create cart
mutation CreateCart($lines: [CartLineInput!]!) {
  cartCreate(input: { lines: $lines }) {
    cart {
      id
      checkoutUrl
      lines(first: 10) {
        nodes {
          id
          quantity
          merchandise {
            ... on ProductVariant {
              title
            }
          }
        }
      }
    }
  }
}

# Add to cart
mutation AddToCart($cartId: ID!, $lines: [CartLineInput!]!) {
  cartLinesAdd(cartId: $cartId, lines: $lines) {
    cart {
      id
      lines(first: 10) {
        nodes {
          id
          quantity
        }
      }
    }
  }
}
```

## Webhooks

### Subscribe to Webhooks

```graphql
mutation WebhookSubscriptionCreate(
  $topic: WebhookSubscriptionTopic!
  $webhookSubscription: WebhookSubscriptionInput!
) {
  webhookSubscriptionCreate(
    topic: $topic
    webhookSubscription: $webhookSubscription
  ) {
    webhookSubscription {
      id
      topic
      endpoint {
        ... on WebhookHttpEndpoint {
          callbackUrl
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
```

Variables:

```json
{
  "topic": "PRODUCTS_CREATE",
  "webhookSubscription": {
    "callbackUrl": "https://your-app.com/webhooks",
    "format": "JSON"
  }
}
```

### Webhook Topics

| Topic                     | Description       |
| ------------------------- | ----------------- |
| `PRODUCTS_CREATE`         | Product created   |
| `PRODUCTS_UPDATE`         | Product updated   |
| `PRODUCTS_DELETE`         | Product deleted   |
| `ORDERS_CREATE`           | Order placed      |
| `ORDERS_UPDATED`          | Order modified    |
| `ORDERS_PAID`             | Order paid        |
| `CUSTOMERS_CREATE`        | Customer created  |
| `INVENTORY_LEVELS_UPDATE` | Inventory changed |

## Bulk Operations

### Bulk Query

```graphql
mutation BulkProducts {
  bulkOperationRunQuery(
    query: """
    {
      products {
        edges {
          node {
            id
            title
            variants {
              edges {
                node {
                  id
                  sku
                  price
                }
              }
            }
          }
        }
      }
    }
    """
  ) {
    bulkOperation {
      id
      status
    }
    userErrors {
      field
      message
    }
  }
}
```

### Poll Bulk Operation

```graphql
query BulkOperationStatus {
  currentBulkOperation {
    id
    status
    objectCount
    url
  }
}
```

## Best Practices

1. **Request only needed fields** - Reduces cost and response size
2. **Use fragments** - Reuse common field selections
3. **Handle errors** - Check for userErrors in mutations
4. **Implement pagination** - Don't request all records at once
5. **Monitor rate limits** - Use throttle status in responses
6. **Use bulk operations** - For large data exports

## Resources

- [Admin API Reference](https://shopify.dev/docs/api/admin-graphql)
- [Storefront API Reference](https://shopify.dev/docs/api/storefront)
- [GraphQL Basics](https://shopify.dev/docs/apps/build/graphql)
- [Rate Limits](https://shopify.dev/docs/api/usage/rate-limits)
- [Webhooks Reference](https://shopify.dev/docs/api/admin-graphql/latest/enums/WebhookSubscriptionTopic)
- [GraphiQL Explorer](https://shopify.dev/docs/apps/build/graphql/basics/graphiql)

For app integration, see the [app-development](../app-development/SKILL.md) skill.
