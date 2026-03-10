---
name: shopify-api
description: "Comprehensive guide for Shopify APIs in Remix apps. Covers Admin GraphQL/REST, Storefront API, all resources (products, orders, customers, inventory, collections, discounts, fulfillments, metafields, files), bulk operations, webhooks, resource pickers, and TypeScript patterns. Use when querying/mutating Shopify data or building integrations."
---

# Shopify API Guide for Remix Apps

Complete reference for Shopify APIs using `@shopify/shopify-app-remix`.

## Quick Reference

| API | Use Case | Auth Method |
|-----|----------|-------------|
| **Admin GraphQL** | All backend CRUD operations | `authenticate.admin()` |
| **Admin REST** | Legacy endpoints, specific features | `authenticate.admin()` |
| **Storefront API** | Public storefront, cart, checkout | Public access token |

## Authentication

### Admin API (Loaders & Actions)

```typescript
// app/routes/app.products.tsx
import { json } from "@remix-run/node";
import type { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin, session } = await authenticate.admin(request);
  // admin.graphql() - GraphQL queries
  // admin.rest - REST API
  // session.shop - current shop domain
  // session.accessToken - access token
  return json({ shop: session.shop });
};

export const action = async ({ request }: ActionFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  // Handle POST/PUT/DELETE
  return json({ success: true });
};
```

### Unauthenticated Access (Public Endpoints)

```typescript
// app/routes/api.public.tsx
import { authenticate } from "../shopify.server";

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { shop } = await authenticate.public.appProxy(request);
  // or authenticate.public.checkout(request)
  return json({ shop });
};
```

---

## Admin GraphQL API

### Basic Patterns

```typescript
// Simple query
const response = await admin.graphql(`
  query {
    shop {
      name
      email
      myshopifyDomain
      plan { displayName }
    }
  }
`);
const { data } = await response.json();

// Query with variables
const response = await admin.graphql(`
  query getProduct($id: ID!) {
    product(id: $id) {
      id
      title
    }
  }
`, {
  variables: { id: "gid://shopify/Product/123" }
});

// Mutation
const response = await admin.graphql(`
  mutation updateProduct($input: ProductInput!) {
    productUpdate(input: $input) {
      product { id title }
      userErrors { field message code }
    }
  }
`, {
  variables: {
    input: { id: "gid://shopify/Product/123", title: "New Title" }
  }
});
```

### TypeScript Types

```typescript
// app/types/shopify.ts
interface ShopifyProduct {
  id: string;
  title: string;
  handle: string;
  status: "ACTIVE" | "ARCHIVED" | "DRAFT";
  variants: { edges: Array<{ node: ShopifyVariant }> };
}

interface ShopifyVariant {
  id: string;
  title: string;
  price: string;
  sku: string | null;
  inventoryQuantity: number;
}

interface GraphQLResponse<T> {
  data: T;
  errors?: Array<{ message: string }>;
  extensions?: { cost: QueryCost };
}

interface UserError {
  field: string[];
  message: string;
  code?: string;
}

// Usage
const { data } = await response.json() as GraphQLResponse<{ product: ShopifyProduct }>;
```

---

## Products

### Query Products

```typescript
export const loader = async ({ request }: LoaderFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  const url = new URL(request.url);
  const cursor = url.searchParams.get("cursor");
  const query = url.searchParams.get("query") || "";

  const response = await admin.graphql(`
    query getProducts($first: Int!, $after: String, $query: String) {
      products(first: $first, after: $after, query: $query) {
        edges {
          node {
            id
            title
            handle
            status
            productType
            vendor
            tags
            totalInventory
            priceRangeV2 {
              minVariantPrice { amount currencyCode }
              maxVariantPrice { amount currencyCode }
            }
            featuredImage {
              url
              altText
            }
            variants(first: 10) {
              edges {
                node {
                  id
                  title
                  sku
                  price
                  compareAtPrice
                  inventoryQuantity
                  selectedOptions { name value }
                }
              }
            }
            metafields(first: 10) {
              edges {
                node { namespace key value type }
              }
            }
          }
        }
        pageInfo {
          hasNextPage
          hasPreviousPage
          startCursor
          endCursor
        }
      }
    }
  `, {
    variables: { first: 25, after: cursor, query }
  });

  const { data } = await response.json();
  return json({
    products: data.products.edges.map((e: any) => e.node),
    pageInfo: data.products.pageInfo
  });
};
```

### Query Filters

```typescript
// Common query filters for products
const queries = {
  // Status
  active: "status:ACTIVE",
  draft: "status:DRAFT",
  archived: "status:ARCHIVED",

  // Inventory
  inStock: "inventory_total:>0",
  outOfStock: "inventory_total:0",
  lowStock: "inventory_total:<10",

  // Price
  priceRange: "variants.price:>=10 AND variants.price:<=100",

  // Type/Vendor
  byType: "product_type:Shoes",
  byVendor: "vendor:Nike",

  // Tags
  byTag: "tag:sale",
  multipleTags: "tag:sale OR tag:new",

  // Date
  createdAfter: "created_at:>2024-01-01",
  updatedRecently: "updated_at:>2024-06-01",

  // Search
  titleContains: "title:*shirt*",

  // Combined
  combined: "status:ACTIVE AND inventory_total:>0 AND tag:featured"
};
```

### Create Product

```typescript
export const action = async ({ request }: ActionFunctionArgs) => {
  const { admin } = await authenticate.admin(request);
  const formData = await request.formData();

  const response = await admin.graphql(`
    mutation productCreate($input: ProductInput!, $media: [CreateMediaInput!]) {
      productCreate(input: $input, media: $media) {
        product {
          id
          title
          handle
          variants(first: 10) {
            edges {
              node { id title price }
            }
          }
        }
        userErrors { field message code }
      }
    }
  `, {
    variables: {
      input: {
        title: formData.get("title"),
        descriptionHtml: formData.get("description"),
        productType: formData.get("productType"),
        vendor: formData.get("vendor"),
        tags: (formData.get("tags") as string)?.split(","),
        status: "DRAFT",
        variants: [{
          price: formData.get("price"),
          sku: formData.get("sku"),
          inventoryQuantities: [{
            availableQuantity: parseInt(formData.get("quantity") as string),
            locationId: "gid://shopify/Location/123"
          }]
        }]
      },
      media: formData.get("imageUrl") ? [{
        originalSource: formData.get("imageUrl"),
        mediaContentType: "IMAGE"
      }] : []
    }
  });

  const { data } = await response.json();

  if (data.productCreate.userErrors.length > 0) {
    return json({ errors: data.productCreate.userErrors }, { status: 400 });
  }

  return json({ product: data.productCreate.product });
};
```

### Update Product

```typescript
const response = await admin.graphql(`
  mutation productUpdate($input: ProductInput!) {
    productUpdate(input: $input) {
      product {
        id
        title
        updatedAt
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      id: "gid://shopify/Product/123",
      title: "Updated Title",
      descriptionHtml: "<p>New description</p>",
      tags: ["new", "sale"],
      metafields: [{
        namespace: "custom",
        key: "color",
        value: "red",
        type: "single_line_text_field"
      }]
    }
  }
});
```

### Delete Product

```typescript
const response = await admin.graphql(`
  mutation productDelete($input: ProductDeleteInput!) {
    productDelete(input: $input) {
      deletedProductId
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: { id: "gid://shopify/Product/123" }
  }
});
```

### Update Variant

```typescript
const response = await admin.graphql(`
  mutation productVariantUpdate($input: ProductVariantInput!) {
    productVariantUpdate(input: $input) {
      productVariant {
        id
        price
        sku
        inventoryQuantity
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      id: "gid://shopify/ProductVariant/456",
      price: "29.99",
      sku: "SKU-001",
      compareAtPrice: "39.99"
    }
  }
});
```

---

## Orders

### Query Orders

```typescript
const response = await admin.graphql(`
  query getOrders($first: Int!, $after: String, $query: String) {
    orders(first: $first, after: $after, query: $query) {
      edges {
        node {
          id
          name
          createdAt
          displayFinancialStatus
          displayFulfillmentStatus
          email
          phone

          customer {
            id
            email
            firstName
            lastName
          }

          shippingAddress {
            address1
            address2
            city
            province
            country
            zip
          }

          totalPriceSet {
            shopMoney { amount currencyCode }
          }
          subtotalPriceSet {
            shopMoney { amount currencyCode }
          }
          totalShippingPriceSet {
            shopMoney { amount currencyCode }
          }
          totalTaxSet {
            shopMoney { amount currencyCode }
          }

          lineItems(first: 50) {
            edges {
              node {
                id
                title
                quantity
                sku
                variant { id title }
                originalUnitPriceSet {
                  shopMoney { amount currencyCode }
                }
                discountedUnitPriceSet {
                  shopMoney { amount currencyCode }
                }
              }
            }
          }

          transactions(first: 10) {
            id
            kind
            status
            amountSet {
              shopMoney { amount currencyCode }
            }
          }

          fulfillments {
            id
            status
            trackingInfo { number url company }
          }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
`, {
  variables: {
    first: 25,
    after: cursor,
    query: "fulfillment_status:unfulfilled AND financial_status:paid"
  }
});
```

### Order Query Filters

```typescript
const orderQueries = {
  // Financial status
  paid: "financial_status:paid",
  pending: "financial_status:pending",
  refunded: "financial_status:refunded",

  // Fulfillment status
  unfulfilled: "fulfillment_status:unfulfilled",
  fulfilled: "fulfillment_status:fulfilled",
  partial: "fulfillment_status:partial",

  // Date ranges
  today: "created_at:today",
  thisWeek: "created_at:past_week",
  thisMonth: "created_at:past_month",
  dateRange: "created_at:>=2024-01-01 AND created_at:<=2024-12-31",

  // Customer
  byEmail: "email:customer@example.com",

  // Tags
  byTag: "tag:wholesale",

  // Risk
  highRisk: "risk_level:high",

  // Combined
  readyToShip: "fulfillment_status:unfulfilled AND financial_status:paid"
};
```

### Create Draft Order

```typescript
const response = await admin.graphql(`
  mutation draftOrderCreate($input: DraftOrderInput!) {
    draftOrderCreate(input: $input) {
      draftOrder {
        id
        invoiceUrl
        totalPrice
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      email: "customer@example.com",
      lineItems: [{
        variantId: "gid://shopify/ProductVariant/123",
        quantity: 2
      }],
      shippingAddress: {
        firstName: "John",
        lastName: "Doe",
        address1: "123 Main St",
        city: "New York",
        province: "NY",
        country: "US",
        zip: "10001"
      },
      appliedDiscount: {
        value: 10,
        valueType: "PERCENTAGE",
        title: "10% Off"
      },
      note: "Special instructions"
    }
  }
});
```

### Complete Draft Order

```typescript
const response = await admin.graphql(`
  mutation draftOrderComplete($id: ID!) {
    draftOrderComplete(id: $id) {
      draftOrder {
        id
        order { id name }
      }
      userErrors { field message }
    }
  }
`, {
  variables: { id: "gid://shopify/DraftOrder/123" }
});
```

### Mark Order as Paid

```typescript
const response = await admin.graphql(`
  mutation orderMarkAsPaid($input: OrderMarkAsPaidInput!) {
    orderMarkAsPaid(input: $input) {
      order { id displayFinancialStatus }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: { id: "gid://shopify/Order/123" }
  }
});
```

### Cancel Order

```typescript
const response = await admin.graphql(`
  mutation orderCancel($orderId: ID!, $reason: OrderCancelReason!, $refund: Boolean!, $restock: Boolean!) {
    orderCancel(orderId: $orderId, reason: $reason, refund: $refund, restock: $restock) {
      orderCancelUserErrors { field message code }
      job { id }
    }
  }
`, {
  variables: {
    orderId: "gid://shopify/Order/123",
    reason: "CUSTOMER",
    refund: true,
    restock: true
  }
});
```

---

## Customers

### Query Customers

```typescript
const response = await admin.graphql(`
  query getCustomers($first: Int!, $query: String) {
    customers(first: $first, query: $query) {
      edges {
        node {
          id
          email
          firstName
          lastName
          phone
          createdAt

          numberOfOrders
          amountSpent { amount currencyCode }

          defaultAddress {
            address1
            city
            province
            country
            zip
          }

          addresses(first: 5) {
            address1
            city
            country
          }

          tags
          note

          metafields(first: 10, namespace: "custom") {
            edges {
              node { key value type }
            }
          }

          emailMarketingConsent {
            marketingState
            consentUpdatedAt
          }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
`, {
  variables: { first: 25, query: "email:*@gmail.com" }
});
```

### Create Customer

```typescript
const response = await admin.graphql(`
  mutation customerCreate($input: CustomerInput!) {
    customerCreate(input: $input) {
      customer {
        id
        email
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      email: "new@customer.com",
      firstName: "John",
      lastName: "Doe",
      phone: "+1234567890",
      addresses: [{
        address1: "123 Main St",
        city: "New York",
        province: "NY",
        country: "US",
        zip: "10001"
      }],
      tags: ["vip", "wholesale"],
      metafields: [{
        namespace: "custom",
        key: "loyalty_points",
        value: "100",
        type: "number_integer"
      }],
      emailMarketingConsent: {
        marketingState: "SUBSCRIBED",
        marketingOptInLevel: "SINGLE_OPT_IN"
      }
    }
  }
});
```

### Update Customer

```typescript
const response = await admin.graphql(`
  mutation customerUpdate($input: CustomerInput!) {
    customerUpdate(input: $input) {
      customer { id email tags }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      id: "gid://shopify/Customer/123",
      tags: ["vip", "wholesale", "loyalty"],
      note: "Important customer"
    }
  }
});
```

---

## Collections

### Query Collections

```typescript
const response = await admin.graphql(`
  query getCollections($first: Int!) {
    collections(first: $first) {
      edges {
        node {
          id
          title
          handle
          descriptionHtml
          productsCount
          sortOrder

          image {
            url
            altText
          }

          ruleSet {
            appliedDisjunctively
            rules {
              column
              relation
              condition
            }
          }
        }
      }
    }
  }
`, { variables: { first: 50 } });
```

### Create Collection

```typescript
// Manual collection
const response = await admin.graphql(`
  mutation collectionCreate($input: CollectionInput!) {
    collectionCreate(input: $input) {
      collection { id title handle }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      title: "Summer Sale",
      descriptionHtml: "<p>Hot summer deals!</p>",
      products: [
        "gid://shopify/Product/123",
        "gid://shopify/Product/456"
      ]
    }
  }
});

// Smart collection (automated)
const response = await admin.graphql(`
  mutation collectionCreate($input: CollectionInput!) {
    collectionCreate(input: $input) {
      collection { id title }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      title: "Sale Items",
      ruleSet: {
        appliedDisjunctively: false,
        rules: [
          { column: "TAG", relation: "EQUALS", condition: "sale" },
          { column: "VARIANT_COMPARE_AT_PRICE", relation: "IS_SET", condition: "" }
        ]
      }
    }
  }
});
```

### Add Products to Collection

```typescript
const response = await admin.graphql(`
  mutation collectionAddProducts($id: ID!, $productIds: [ID!]!) {
    collectionAddProducts(id: $id, productIds: $productIds) {
      collection { id productsCount }
      userErrors { field message }
    }
  }
`, {
  variables: {
    id: "gid://shopify/Collection/123",
    productIds: [
      "gid://shopify/Product/456",
      "gid://shopify/Product/789"
    ]
  }
});
```

---

## Inventory

### Query Inventory Levels

```typescript
const response = await admin.graphql(`
  query getInventoryLevels($inventoryItemId: ID!) {
    inventoryItem(id: $inventoryItemId) {
      id
      sku
      tracked
      inventoryLevels(first: 10) {
        edges {
          node {
            id
            available
            location {
              id
              name
            }
          }
        }
      }
    }
  }
`, {
  variables: { inventoryItemId: "gid://shopify/InventoryItem/123" }
});
```

### Adjust Inventory

```typescript
const response = await admin.graphql(`
  mutation inventoryAdjustQuantities($input: InventoryAdjustQuantitiesInput!) {
    inventoryAdjustQuantities(input: $input) {
      inventoryAdjustmentGroup {
        reason
        changes {
          name
          delta
        }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      reason: "correction",
      name: "available",
      changes: [{
        inventoryItemId: "gid://shopify/InventoryItem/123",
        locationId: "gid://shopify/Location/456",
        delta: 10  // positive = add, negative = subtract
      }]
    }
  }
});
```

### Set Inventory Level

```typescript
const response = await admin.graphql(`
  mutation inventorySetQuantities($input: InventorySetQuantitiesInput!) {
    inventorySetQuantities(input: $input) {
      inventoryAdjustmentGroup {
        changes { name delta }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: {
      reason: "correction",
      name: "available",
      quantities: [{
        inventoryItemId: "gid://shopify/InventoryItem/123",
        locationId: "gid://shopify/Location/456",
        quantity: 100  // set absolute quantity
      }]
    }
  }
});
```

### Get Locations

```typescript
const response = await admin.graphql(`
  query getLocations {
    locations(first: 10) {
      edges {
        node {
          id
          name
          address { address1 city country }
          isActive
          fulfillsOnlineOrders
        }
      }
    }
  }
`);
```

---

## Fulfillments

### Create Fulfillment

```typescript
const response = await admin.graphql(`
  mutation fulfillmentCreateV2($fulfillment: FulfillmentV2Input!) {
    fulfillmentCreateV2(fulfillment: $fulfillment) {
      fulfillment {
        id
        status
        trackingInfo { number url company }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    fulfillment: {
      lineItemsByFulfillmentOrder: [{
        fulfillmentOrderId: "gid://shopify/FulfillmentOrder/123",
        fulfillmentOrderLineItems: [{
          id: "gid://shopify/FulfillmentOrderLineItem/456",
          quantity: 1
        }]
      }],
      trackingInfo: {
        number: "1Z999AA10123456784",
        url: "https://tracking.example.com/1Z999AA10123456784",
        company: "UPS"
      },
      notifyCustomer: true
    }
  }
});
```

### Get Fulfillment Orders

```typescript
const response = await admin.graphql(`
  query getFulfillmentOrders($orderId: ID!) {
    order(id: $orderId) {
      fulfillmentOrders(first: 10) {
        edges {
          node {
            id
            status
            assignedLocation { name }
            lineItems(first: 50) {
              edges {
                node {
                  id
                  totalQuantity
                  remainingQuantity
                  lineItem { title sku }
                }
              }
            }
          }
        }
      }
    }
  }
`, {
  variables: { orderId: "gid://shopify/Order/123" }
});
```

### Update Tracking

```typescript
const response = await admin.graphql(`
  mutation fulfillmentTrackingInfoUpdateV2($fulfillmentId: ID!, $trackingInfoInput: FulfillmentTrackingInput!) {
    fulfillmentTrackingInfoUpdateV2(fulfillmentId: $fulfillmentId, trackingInfoInput: $trackingInfoInput) {
      fulfillment {
        id
        trackingInfo { number url }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    fulfillmentId: "gid://shopify/Fulfillment/123",
    trackingInfoInput: {
      number: "NEW123456",
      url: "https://tracking.example.com/NEW123456",
      company: "FedEx"
    }
  }
});
```

---

## Discounts

### Create Automatic Discount

```typescript
const response = await admin.graphql(`
  mutation discountAutomaticBasicCreate($automaticBasicDiscount: DiscountAutomaticBasicInput!) {
    discountAutomaticBasicCreate(automaticBasicDiscount: $automaticBasicDiscount) {
      automaticDiscountNode {
        id
        automaticDiscount {
          ... on DiscountAutomaticBasic {
            title
            startsAt
            endsAt
          }
        }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    automaticBasicDiscount: {
      title: "Summer Sale 20% Off",
      startsAt: "2024-06-01T00:00:00Z",
      endsAt: "2024-08-31T23:59:59Z",
      minimumRequirement: {
        subtotal: { greaterThanOrEqualToSubtotal: "50.00" }
      },
      customerGets: {
        value: { percentage: 0.20 },
        items: { all: true }
      }
    }
  }
});
```

### Create Discount Code

```typescript
const response = await admin.graphql(`
  mutation discountCodeBasicCreate($basicCodeDiscount: DiscountCodeBasicInput!) {
    discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) {
      codeDiscountNode {
        id
        codeDiscount {
          ... on DiscountCodeBasic {
            title
            codes(first: 1) { edges { node { code } } }
          }
        }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    basicCodeDiscount: {
      title: "Welcome Discount",
      code: "WELCOME10",
      startsAt: "2024-01-01T00:00:00Z",
      usageLimit: 1000,
      appliesOncePerCustomer: true,
      customerGets: {
        value: { percentage: 0.10 },
        items: { all: true }
      },
      customerSelection: { all: true }
    }
  }
});
```

---

## Metafields

### Get Metafields

```typescript
// On a product
const response = await admin.graphql(`
  query getProductMetafields($id: ID!) {
    product(id: $id) {
      metafields(first: 50) {
        edges {
          node {
            id
            namespace
            key
            value
            type
            description
          }
        }
      }
    }
  }
`, { variables: { id: "gid://shopify/Product/123" } });

// By specific namespace/key
const response = await admin.graphql(`
  query getMetafield($ownerId: ID!, $namespace: String!, $key: String!) {
    product(id: $ownerId) {
      metafield(namespace: $namespace, key: $key) {
        id
        value
        type
      }
    }
  }
`, {
  variables: {
    ownerId: "gid://shopify/Product/123",
    namespace: "custom",
    key: "specifications"
  }
});
```

### Set Metafields

```typescript
const response = await admin.graphql(`
  mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
    metafieldsSet(metafields: $metafields) {
      metafields {
        id
        namespace
        key
        value
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    metafields: [
      {
        ownerId: "gid://shopify/Product/123",
        namespace: "custom",
        key: "material",
        value: "Cotton",
        type: "single_line_text_field"
      },
      {
        ownerId: "gid://shopify/Product/123",
        namespace: "custom",
        key: "care_instructions",
        value: JSON.stringify(["Machine wash cold", "Tumble dry low"]),
        type: "list.single_line_text_field"
      },
      {
        ownerId: "gid://shopify/Product/123",
        namespace: "custom",
        key: "is_featured",
        value: "true",
        type: "boolean"
      },
      {
        ownerId: "gid://shopify/Product/123",
        namespace: "custom",
        key: "rating",
        value: "4.5",
        type: "number_decimal"
      }
    ]
  }
});
```

### Metafield Types Reference

| Type | Example Value |
|------|---------------|
| `single_line_text_field` | `"Hello"` |
| `multi_line_text_field` | `"Line 1\nLine 2"` |
| `number_integer` | `"42"` |
| `number_decimal` | `"3.14"` |
| `boolean` | `"true"` or `"false"` |
| `date` | `"2024-01-15"` |
| `date_time` | `"2024-01-15T10:30:00Z"` |
| `json` | `"{\"key\":\"value\"}"` |
| `url` | `"https://example.com"` |
| `color` | `"#FF0000"` |
| `list.single_line_text_field` | `"[\"item1\",\"item2\"]"` |
| `product_reference` | `"gid://shopify/Product/123"` |
| `file_reference` | `"gid://shopify/MediaImage/123"` |

### Delete Metafield

```typescript
const response = await admin.graphql(`
  mutation metafieldDelete($input: MetafieldDeleteInput!) {
    metafieldDelete(input: $input) {
      deletedId
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: { id: "gid://shopify/Metafield/123" }
  }
});
```

---

## Files & Media

### Upload File (Staged Upload)

```typescript
// Step 1: Create staged upload
const stageResponse = await admin.graphql(`
  mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
    stagedUploadsCreate(input: $input) {
      stagedTargets {
        url
        resourceUrl
        parameters { name value }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: [{
      resource: "IMAGE",
      filename: "product-image.jpg",
      mimeType: "image/jpeg",
      fileSize: "1024000",
      httpMethod: "POST"
    }]
  }
});

// Step 2: Upload file to staged URL (using fetch)
const { stagedTargets } = stageResponse.stagedUploadsCreate;
const target = stagedTargets[0];

const formData = new FormData();
target.parameters.forEach((param: any) => {
  formData.append(param.name, param.value);
});
formData.append("file", fileBlob);

await fetch(target.url, {
  method: "POST",
  body: formData
});

// Step 3: Create file in Shopify
const fileResponse = await admin.graphql(`
  mutation fileCreate($files: [FileCreateInput!]!) {
    fileCreate(files: $files) {
      files {
        ... on MediaImage {
          id
          image { url }
        }
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    files: [{
      originalSource: target.resourceUrl,
      contentType: "IMAGE"
    }]
  }
});
```

### Add Media to Product

```typescript
const response = await admin.graphql(`
  mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
    productCreateMedia(productId: $productId, media: $media) {
      media {
        ... on MediaImage {
          id
          image { url altText }
        }
      }
      mediaUserErrors { field message }
    }
  }
`, {
  variables: {
    productId: "gid://shopify/Product/123",
    media: [{
      originalSource: "https://example.com/image.jpg",
      mediaContentType: "IMAGE",
      alt: "Product image description"
    }]
  }
});
```

---

## Bulk Operations

### Run Bulk Query

```typescript
// Start bulk operation
const response = await admin.graphql(`
  mutation bulkOperationRunQuery($query: String!) {
    bulkOperationRunQuery(query: $query) {
      bulkOperation {
        id
        status
      }
      userErrors { field message }
    }
  }
`, {
  variables: {
    query: `
      {
        products {
          edges {
            node {
              id
              title
              handle
              variants {
                edges {
                  node {
                    id
                    sku
                    price
                    inventoryQuantity
                  }
                }
              }
            }
          }
        }
      }
    `
  }
});

// Poll for completion
const pollBulkOperation = async (admin: any): Promise<string | null> => {
  const response = await admin.graphql(`
    query {
      currentBulkOperation {
        id
        status
        url
        errorCode
        objectCount
      }
    }
  `);

  const { data } = await response.json();
  const op = data.currentBulkOperation;

  if (op.status === "COMPLETED") {
    return op.url;  // JSONL file URL
  } else if (op.status === "FAILED") {
    throw new Error(`Bulk operation failed: ${op.errorCode}`);
  }

  // Still running, poll again
  await new Promise(resolve => setTimeout(resolve, 2000));
  return pollBulkOperation(admin);
};

// Download and process results
const resultsUrl = await pollBulkOperation(admin);
const resultsResponse = await fetch(resultsUrl);
const jsonlText = await resultsResponse.text();
const results = jsonlText.split("\n").filter(Boolean).map(JSON.parse);
```

### Bulk Mutation

```typescript
// Create staged upload for JSONL input
const stageResponse = await admin.graphql(`
  mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
    stagedUploadsCreate(input: $input) {
      stagedTargets { url resourceUrl parameters { name value } }
      userErrors { field message }
    }
  }
`, {
  variables: {
    input: [{
      resource: "BULK_MUTATION_VARIABLES",
      filename: "bulk-input.jsonl",
      mimeType: "text/jsonl",
      httpMethod: "POST"
    }]
  }
});

// Upload JSONL file with mutations
const jsonlContent = products.map(p => JSON.stringify({
  input: { id: p.id, title: p.title }
})).join("\n");

// ... upload to staged URL ...

// Run bulk mutation
const bulkResponse = await admin.graphql(`
  mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!) {
    bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
      bulkOperation { id status }
      userErrors { field message }
    }
  }
`, {
  variables: {
    mutation: `
      mutation productUpdate($input: ProductInput!) {
        productUpdate(input: $input) {
          product { id }
          userErrors { field message }
        }
      }
    `,
    stagedUploadPath: stagedTarget.resourceUrl
  }
});
```

---

## Pagination Utility

```typescript
// app/utils/shopify-pagination.server.ts
export interface PageInfo {
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  startCursor: string;
  endCursor: string;
}

export async function fetchAllPages<T>(
  admin: any,
  query: string,
  variables: Record<string, any>,
  connectionPath: string[],
  options?: { maxPages?: number }
): Promise<T[]> {
  const results: T[] = [];
  let hasNextPage = true;
  let cursor: string | null = null;
  let pageCount = 0;
  const maxPages = options?.maxPages ?? Infinity;

  while (hasNextPage && pageCount < maxPages) {
    const response = await admin.graphql(query, {
      variables: { ...variables, after: cursor }
    });

    const { data, errors } = await response.json();

    if (errors) {
      throw new Error(`GraphQL error: ${errors[0].message}`);
    }

    // Navigate to connection
    let connection = data;
    for (const key of connectionPath) {
      connection = connection[key];
    }

    results.push(...connection.edges.map((edge: any) => edge.node));
    hasNextPage = connection.pageInfo.hasNextPage;
    cursor = connection.pageInfo.endCursor;
    pageCount++;
  }

  return results;
}

// Usage example
const allProducts = await fetchAllPages(
  admin,
  `query($first: Int!, $after: String) {
    products(first: $first, after: $after) {
      edges {
        node { id title status }
      }
      pageInfo { hasNextPage endCursor }
    }
  }`,
  { first: 250 },
  ["products"]
);
```

---

## Admin REST API

```typescript
// GET request
const response = await admin.rest.get({
  path: "products",
  query: { limit: 50, status: "active" }
});
const products = response.body.products;

// GET single resource
const response = await admin.rest.get({
  path: `products/${productId}`
});

// POST request
const response = await admin.rest.post({
  path: "products",
  data: {
    product: {
      title: "New Product",
      body_html: "<p>Description</p>",
      vendor: "Vendor Name"
    }
  }
});

// PUT request
const response = await admin.rest.put({
  path: `products/${productId}`,
  data: {
    product: { title: "Updated Title" }
  }
});

// DELETE request
const response = await admin.rest.delete({
  path: `products/${productId}`
});
```

---

## Storefront API

### Setup

```typescript
// app/utils/storefront.server.ts
export async function storefrontQuery(shop: string, query: string, variables?: any) {
  const response = await fetch(
    `https://${shop}/api/2025-01/graphql.json`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": process.env.STOREFRONT_ACCESS_TOKEN!
      },
      body: JSON.stringify({ query, variables })
    }
  );
  return response.json();
}
```

### Query Products (Storefront)

```typescript
const { data } = await storefrontQuery(shop, `
  query getProducts($first: Int!) {
    products(first: $first) {
      edges {
        node {
          id
          title
          handle
          description
          priceRange {
            minVariantPrice { amount currencyCode }
          }
          images(first: 1) {
            edges {
              node { url altText }
            }
          }
          variants(first: 10) {
            edges {
              node {
                id
                title
                price { amount currencyCode }
                availableForSale
              }
            }
          }
        }
      }
    }
  }
`, { first: 20 });
```

### Cart Operations (Storefront)

```typescript
// Create cart
const { data } = await storefrontQuery(shop, `
  mutation cartCreate($input: CartInput!) {
    cartCreate(input: $input) {
      cart {
        id
        checkoutUrl
        lines(first: 10) {
          edges {
            node {
              id
              quantity
              merchandise {
                ... on ProductVariant {
                  id
                  title
                }
              }
            }
          }
        }
      }
      userErrors { field message }
    }
  }
`, {
  input: {
    lines: [{
      merchandiseId: "gid://shopify/ProductVariant/123",
      quantity: 1
    }]
  }
});

// Add to cart
const { data } = await storefrontQuery(shop, `
  mutation cartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!) {
    cartLinesAdd(cartId: $cartId, lines: $lines) {
      cart { id }
      userErrors { field message }
    }
  }
`, {
  cartId: "gid://shopify/Cart/abc123",
  lines: [{ merchandiseId: "gid://shopify/ProductVariant/456", quantity: 2 }]
});
```

---

## Error Handling

```typescript
// app/utils/shopify-errors.server.ts
export interface ShopifyUserError {
  field: string[];
  message: string;
  code?: string;
}

export class ShopifyAPIError extends Error {
  constructor(
    message: string,
    public userErrors?: ShopifyUserError[],
    public graphqlErrors?: any[]
  ) {
    super(message);
    this.name = "ShopifyAPIError";
  }
}

export async function executeGraphQL<T>(
  admin: any,
  query: string,
  variables?: Record<string, any>,
  mutationPath?: string
): Promise<T> {
  const response = await admin.graphql(query, { variables });
  const { data, errors, extensions } = await response.json();

  // GraphQL-level errors (syntax, validation)
  if (errors?.length > 0) {
    throw new ShopifyAPIError(
      `GraphQL Error: ${errors[0].message}`,
      undefined,
      errors
    );
  }

  // User errors (business logic)
  if (mutationPath) {
    const mutationResult = data[mutationPath];
    if (mutationResult?.userErrors?.length > 0) {
      throw new ShopifyAPIError(
        `Mutation Error: ${mutationResult.userErrors[0].message}`,
        mutationResult.userErrors
      );
    }
  }

  // Log rate limit info
  if (extensions?.cost) {
    const { requestedQueryCost, throttleStatus } = extensions.cost;
    if (throttleStatus.currentlyAvailable < 100) {
      console.warn(`Low rate limit: ${throttleStatus.currentlyAvailable} remaining`);
    }
  }

  return data;
}

// Usage
try {
  const data = await executeGraphQL(
    admin,
    `mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id }
        userErrors { field message code }
      }
    }`,
    { input: { id: productId, title: newTitle } },
    "productUpdate"
  );
} catch (error) {
  if (error instanceof ShopifyAPIError) {
    if (error.userErrors) {
      return json({ errors: error.userErrors }, { status: 422 });
    }
  }
  throw error;
}
```

---

## Rate Limiting

```typescript
// Check rate limit status
const response = await admin.graphql(`...`);
const { extensions } = await response.json();

if (extensions?.cost) {
  const { requestedQueryCost, actualQueryCost, throttleStatus } = extensions.cost;
  console.log({
    requested: requestedQueryCost,
    actual: actualQueryCost,
    available: throttleStatus.currentlyAvailable,
    maximum: throttleStatus.maximumAvailable,
    restoreRate: throttleStatus.restoreRate
  });
}

// Exponential backoff for rate limits
export async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      lastError = error;

      // Check if rate limited (429)
      if (error?.response?.status === 429 || error?.message?.includes("Throttled")) {
        const delay = baseDelay * Math.pow(2, attempt);
        console.log(`Rate limited, retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }

      throw error;
    }
  }

  throw lastError;
}
```

**Rate Limits:**
- **GraphQL**: 1000 points, refill 50/sec (Standard), higher for Plus
- **REST**: 40 requests, refill 2/sec (Standard)
- Use `first: 250` max for pagination
- Bulk operations for >10k items
