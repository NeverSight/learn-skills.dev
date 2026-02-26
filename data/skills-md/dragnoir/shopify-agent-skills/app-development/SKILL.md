---
name: app-development
description: Build Shopify apps with extensions and embedded experiences. Use this skill for creating new Shopify apps, adding app extensions, building admin interfaces, working with OAuth authentication, managing app configuration, and deploying to the Shopify App Store. Covers Shopify CLI for apps, Polaris UI, and app bridge.
license: MIT
compatibility: Requires Shopify CLI, Node.js 18+, and a Shopify Partner account
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Shopify App Development

## When to use this skill

Use this skill when:

- Creating a new Shopify app
- Building app extensions (admin, checkout, etc.)
- Embedding UI in the Shopify admin
- Working with OAuth and app authentication
- Managing webhooks and app events
- Using Shopify Polaris UI components
- Deploying apps to the Shopify App Store

## App Types

### Public Apps

- Distributed via the Shopify App Store
- Available to all merchants
- Require app review process

### Custom Apps

- Built for a single merchant/organization
- Direct installation (no app store)
- Simpler distribution

### Sales Channel Apps

- Integrate a sales channel with Shopify
- Appear in the Shopify admin's sales channels

## Getting Started

### 1. Create a New App

```bash
# Initialize a new app
shopify app init

# Choose a template:
# - Remix (recommended)
# - Node
# - Ruby
# - PHP
```

### 2. Project Structure (Remix Template)

```
my-app/
├── app/
│   ├── routes/
│   │   ├── app._index.jsx      # Main app page
│   │   ├── app.products.jsx    # Products page
│   │   └── webhooks.jsx        # Webhook handlers
│   ├── shopify.server.js       # Shopify API config
│   └── root.jsx                # Root layout
├── extensions/                  # App extensions
├── prisma/                      # Database schema
├── shopify.app.toml            # App configuration
└── package.json
```

### 3. Start Development

```bash
# Start dev server with tunnel
shopify app dev

# View app info
shopify app info
```

## App Configuration

### shopify.app.toml

```toml
name = "My App"
client_id = "your-api-key"

[access_scopes]
scopes = "read_products, write_products, read_orders"

[webhooks]
api_version = "2025-01"

[[webhooks.subscriptions]]
topics = ["products/create", "orders/create"]
uri = "/webhooks"

[app_proxy]
url = "https://myapp.example.com/proxy"
subpath = "app-proxy"
prefix = "apps"
```

### Environment Variables

```env
SHOPIFY_API_KEY=your-api-key
SHOPIFY_API_SECRET=your-api-secret
SCOPES=read_products,write_products
HOST=https://your-tunnel-url.ngrok.io
```

## Authentication

### Session Tokens (Recommended)

Apps embedded in the Shopify admin use session tokens:

```javascript
// app/shopify.server.js
import "@shopify/shopify-app-remix/adapters/node";
import { AppDistribution, shopifyApp } from "@shopify/shopify-app-remix/server";

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET,
  scopes: process.env.SCOPES?.split(","),
  appUrl: process.env.SHOPIFY_APP_URL,
  distribution: AppDistribution.AppStore,
});

export default shopify;
```

### Admin API Access

```javascript
import { authenticate } from "../shopify.server";

export async function loader({ request }) {
  const { admin } = await authenticate.admin(request);

  const response = await admin.graphql(`
    query {
      products(first: 10) {
        nodes {
          id
          title
          handle
        }
      }
    }
  `);

  const data = await response.json();
  return json({ products: data.data.products.nodes });
}
```

## App Extensions

### Extension Types

| Type             | Description                         |
| ---------------- | ----------------------------------- |
| **Admin UI**     | Embedded UI in Shopify admin        |
| **Admin Action** | Action buttons in admin             |
| **Admin Block**  | Content blocks in admin             |
| **Checkout UI**  | Custom checkout experience          |
| **Theme App**    | Integrate with merchant themes      |
| **POS UI**       | Point of Sale extensions            |
| **Flow**         | Workflow automation                 |
| **Functions**    | Backend logic (discounts, shipping) |

### Create an Extension

```bash
# Generate an extension
shopify app generate extension

# Choose extension type from the list
```

### Admin UI Extension Example

```jsx
// extensions/admin-block/src/BlockExtension.jsx
import {
  reactExtension,
  useApi,
  AdminBlock,
  Text,
  BlockStack,
  InlineStack,
  Button,
} from "@shopify/ui-extensions-react/admin";

export default reactExtension("admin.product-details.block.render", () => (
  <ProductBlock />
));

function ProductBlock() {
  const { data } = useApi();

  return (
    <AdminBlock title="Custom Block">
      <BlockStack>
        <Text>Product ID: {data.selected[0]?.id}</Text>
        <InlineStack>
          <Button onPress={() => console.log("clicked")}>Action</Button>
        </InlineStack>
      </BlockStack>
    </AdminBlock>
  );
}
```

### Theme App Extension

```jsx
// extensions/theme-block/blocks/product-rating.liquid
{% schema %}
{
  "name": "Product Rating",
  "target": "section",
  "settings": [
    {
      "type": "product",
      "id": "product",
      "label": "Product"
    }
  ]
}
{% endschema %}

<div class="product-rating">
  <app-block-rating product-id="{{ block.settings.product.id }}">
  </app-block-rating>
</div>

{% javascript %}
  // Your JavaScript here
{% endjavascript %}

{% stylesheet %}
  .product-rating {
    padding: 16px;
  }
{% endstylesheet %}
```

## Polaris UI Components

### Basic Layout

```jsx
import {
  Page,
  Layout,
  Card,
  Text,
  BlockStack,
  InlineStack,
  Button,
  TextField,
  Select,
  Banner,
  List,
} from "@shopify/polaris";

export default function ProductPage() {
  return (
    <Page title="Products" primaryAction={{ content: "Create product" }}>
      <Layout>
        <Layout.Section>
          <Card>
            <BlockStack gap="300">
              <Text as="h2" variant="headingMd">
                Product Details
              </Text>
              <TextField label="Title" value={title} onChange={setTitle} />
              <Select
                label="Status"
                options={[
                  { label: "Active", value: "active" },
                  { label: "Draft", value: "draft" },
                ]}
                value={status}
                onChange={setStatus}
              />
            </BlockStack>
          </Card>
        </Layout.Section>

        <Layout.Section variant="oneThird">
          <Card>
            <Text as="h2" variant="headingMd">
              Summary
            </Text>
          </Card>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

### Data Table

```jsx
import { IndexTable, Card, Text } from "@shopify/polaris";

function ProductTable({ products }) {
  const rowMarkup = products.map((product, index) => (
    <IndexTable.Row id={product.id} key={product.id} position={index}>
      <IndexTable.Cell>
        <Text variant="bodyMd" fontWeight="bold">
          {product.title}
        </Text>
      </IndexTable.Cell>
      <IndexTable.Cell>{product.status}</IndexTable.Cell>
      <IndexTable.Cell>{product.inventory}</IndexTable.Cell>
    </IndexTable.Row>
  ));

  return (
    <Card>
      <IndexTable
        itemCount={products.length}
        headings={[
          { title: "Product" },
          { title: "Status" },
          { title: "Inventory" },
        ]}
        selectable={false}
      >
        {rowMarkup}
      </IndexTable>
    </Card>
  );
}
```

## Webhooks

### Register Webhooks

```toml
# shopify.app.toml
[[webhooks.subscriptions]]
topics = ["products/create", "products/update", "products/delete"]
uri = "/webhooks"
```

### Handle Webhooks

```javascript
// app/routes/webhooks.jsx
import { authenticate } from "../shopify.server";

export async function action({ request }) {
  const { topic, shop, payload } = await authenticate.webhook(request);

  switch (topic) {
    case "PRODUCTS_CREATE":
      console.log("Product created:", payload.id);
      // Handle product creation
      break;
    case "PRODUCTS_UPDATE":
      console.log("Product updated:", payload.id);
      // Handle product update
      break;
    case "ORDERS_CREATE":
      console.log("Order created:", payload.id);
      // Handle new order
      break;
  }

  return new Response("OK", { status: 200 });
}
```

## Metafields

### Reading Metafields

```javascript
const response = await admin.graphql(`
  query {
    product(id: "gid://shopify/Product/123456") {
      metafield(namespace: "custom", key: "care_instructions") {
        value
        type
      }
      metafields(first: 10) {
        nodes {
          namespace
          key
          value
          type
        }
      }
    }
  }
`);
```

### Writing Metafields

```javascript
const response = await admin.graphql(
  `
  mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
    metafieldsSet(metafields: $metafields) {
      metafields {
        key
        value
      }
      userErrors {
        field
        message
      }
    }
  }
`,
  {
    variables: {
      metafields: [
        {
          ownerId: "gid://shopify/Product/123456",
          namespace: "custom",
          key: "care_instructions",
          value: "Machine wash cold",
          type: "single_line_text_field",
        },
      ],
    },
  },
);
```

## Deployment

### Deploy to Shopify

```bash
# Deploy app and extensions
shopify app deploy

# Deploy specific version
shopify app versions list
shopify app release --version VERSION_ID
```

### App Store Submission

1. Complete Partner Dashboard app listing
2. Add required app store assets
3. Submit for review
4. Address review feedback
5. Publish approved app

## CLI Commands Reference

| Command                          | Description      |
| -------------------------------- | ---------------- |
| `shopify app init`               | Create new app   |
| `shopify app dev`                | Start dev server |
| `shopify app deploy`             | Deploy app       |
| `shopify app generate extension` | Create extension |
| `shopify app info`               | View app info    |
| `shopify app env show`           | Show environment |
| `shopify app versions list`      | List versions    |

## Best Practices

1. **Use session tokens** - More secure than API keys
2. **Handle rate limits** - Implement retry logic
3. **Validate webhooks** - Verify HMAC signatures
4. **Test on dev stores** - Use development stores
5. **Follow Polaris guidelines** - Consistent UX
6. **Monitor app health** - Track errors and performance

## Resources

- [App Development Docs](https://shopify.dev/docs/apps/build)
- [Polaris Components](https://polaris.shopify.com)
- [App Bridge](https://shopify.dev/docs/api/app-bridge)
- [Admin API Reference](https://shopify.dev/docs/api/admin-graphql)
- [App Store Requirements](https://shopify.dev/docs/apps/store/requirements)

For backend functions, see the [shopify-functions](../shopify-functions/SKILL.md) skill.
For checkout customization, see the [checkout-customization](../checkout-customization/SKILL.md) skill.
