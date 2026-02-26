---
name: shopify-functions
description: Build backend logic with Shopify Functions. Use this skill for creating custom discounts, delivery customization, payment customization, cart and checkout validation, and order routing. Functions run on Shopify's infrastructure using WebAssembly. Supports Rust and JavaScript.
license: MIT
compatibility: Requires Shopify CLI, Rust or JavaScript knowledge, and a Partner account
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Shopify Functions

## When to use this skill

Use this skill when:

- Creating custom discount logic
- Customizing delivery options
- Implementing payment method rules
- Validating cart or checkout
- Building order routing logic
- Extending Shopify's backend behavior

## What are Shopify Functions?

Functions are serverless WebAssembly modules that extend Shopify's backend logic. They:

- Run on Shopify's infrastructure
- Execute in milliseconds
- Scale automatically
- Are upgrade-safe

### Function Types

| API                            | Purpose                                |
| ------------------------------ | -------------------------------------- |
| **Discounts**                  | Product, order, and shipping discounts |
| **Delivery Customization**     | Rename, reorder, hide shipping options |
| **Payment Customization**      | Filter, reorder payment methods        |
| **Cart & Checkout Validation** | Block checkout with errors             |
| **Order Routing**              | Control fulfillment locations          |
| **Cart Transform**             | Modify cart contents                   |

## Getting Started

### 1. Create a Function

```bash
# In an existing app
shopify app generate extension

# Select from function types:
# - Delivery customization
# - Product discount
# - Order discount
# - Cart & Checkout Validation
# - etc.
```

### 2. Choose a Language

**Rust (Recommended)** - Best performance, handles large carts

**JavaScript** - Easier to learn, good for simpler logic

### 3. Function Structure

```
extensions/
└── my-discount/
    ├── src/
    │   └── run.rs (or run.js)
    ├── input.graphql
    ├── shopify.extension.toml
    └── Cargo.toml (for Rust)
```

## Function Anatomy

### Configuration (shopify.extension.toml)

```toml
api_version = "2025-01"

[[extensions]]
name = "Volume Discount"
handle = "volume-discount"
type = "function"

[[extensions.targeting]]
target = "purchase.product-discount.run"
input_query = "src/run.graphql"
export = "run"

[extensions.build]
command = "cargo wasi build --release"
path = "target/wasm32-wasi/release/volume-discount.wasm"
```

### Input Query (input.graphql)

```graphql
query RunInput {
  cart {
    lines {
      id
      quantity
      merchandise {
        ... on ProductVariant {
          id
          product {
            id
            title
            hasAnyTag(tags: ["discount-eligible"])
          }
        }
      }
      cost {
        amountPerQuantity {
          amount
          currencyCode
        }
      }
    }
  }
  discountNode {
    metafield(namespace: "volume-discount", key: "config") {
      value
    }
  }
}
```

## Product Discount Function (Rust)

```rust
// src/run.rs
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let mut discounts = vec![];

    // Parse configuration from metafield
    let config: Config = input.discount_node.metafield
        .as_ref()
        .map(|m| serde_json::from_str(&m.value).unwrap())
        .unwrap_or_default();

    for line in input.cart.lines {
        let quantity = line.quantity;

        // Check if eligible for volume discount
        if quantity >= config.minimum_quantity {
            let merchandise = match &line.merchandise {
                input::InputCartLinesMerchandise::ProductVariant(variant) => variant,
                _ => continue,
            };

            // Check for eligible tag
            if merchandise.product.has_any_tag {
                discounts.push(output::Discount {
                    targets: vec![output::Target::ProductVariant(
                        output::ProductVariantTarget {
                            id: merchandise.id.clone(),
                            quantity: None,
                        },
                    )],
                    value: output::Value::Percentage(output::Percentage {
                        value: Decimal::from_str(&config.discount_percentage).unwrap(),
                    }),
                    message: Some(format!("{}% volume discount", config.discount_percentage)),
                });
            }
        }
    }

    Ok(output::FunctionRunResult {
        discounts,
        discount_application_strategy: output::DiscountApplicationStrategy::FIRST,
    })
}

#[derive(Default, serde::Deserialize)]
struct Config {
    minimum_quantity: i64,
    discount_percentage: String,
}
```

## Product Discount Function (JavaScript)

```javascript
// src/run.js
// @ts-check
import { DiscountApplicationStrategy } from "../generated/api";

/**
 * @param {RunInput} input
 * @returns {FunctionRunResult}
 */
export function run(input) {
  const config = JSON.parse(
    input.discountNode.metafield?.value ??
      '{"minimumQuantity": 5, "percentage": "10"}',
  );

  const discounts = [];

  for (const line of input.cart.lines) {
    const variant = line.merchandise;

    // Check quantity threshold
    if (line.quantity >= config.minimumQuantity) {
      // Check for eligible products
      if (
        variant.__typename === "ProductVariant" &&
        variant.product.hasAnyTag
      ) {
        discounts.push({
          targets: [
            {
              productVariant: {
                id: variant.id,
              },
            },
          ],
          value: {
            percentage: {
              value: config.percentage,
            },
          },
          message: `${config.percentage}% volume discount`,
        });
      }
    }
  }

  return {
    discounts,
    discountApplicationStrategy: DiscountApplicationStrategy.First,
  };
}
```

## Delivery Customization

```rust
// Rename, hide, or reorder delivery options
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let mut operations = vec![];

    for method in input.cart.delivery_groups[0].delivery_options.iter() {
        // Hide express shipping for heavy orders
        if method.title.contains("Express") && cart_weight_exceeds_limit(&input) {
            operations.push(output::Operation::Hide(output::HideOperation {
                delivery_option_handle: method.handle.clone(),
            }));
        }

        // Rename delivery option
        if method.title.contains("Standard") {
            operations.push(output::Operation::Rename(output::RenameOperation {
                delivery_option_handle: method.handle.clone(),
                title: Some("Economy Shipping (5-7 days)".to_string()),
            }));
        }
    }

    Ok(output::FunctionRunResult { operations })
}
```

## Payment Customization

```javascript
// src/run.js
export function run(input) {
  const cart = input.cart;
  const operations = [];

  // Calculate cart total
  const total = cart.cost.totalAmount.amount;

  // Hide COD for orders over $500
  if (parseFloat(total) > 500) {
    const codMethod = input.paymentMethods.find((method) =>
      method.name.includes("Cash on Delivery"),
    );

    if (codMethod) {
      operations.push({
        hide: {
          paymentMethodId: codMethod.id,
        },
      });
    }
  }

  // Reorder payment methods
  operations.push({
    move: {
      paymentMethodId: input.paymentMethods[0].id,
      index: 2,
    },
  });

  return { operations };
}
```

## Cart & Checkout Validation

```rust
use shopify_function::prelude::*;
use shopify_function::Result;

#[shopify_function_target(query_path = "src/run.graphql", schema_path = "schema.graphql")]
fn run(input: input::ResponseData) -> Result<output::FunctionRunResult> {
    let mut errors = vec![];

    // Check minimum order value
    let total: f64 = input.cart.cost.total_amount.amount.parse().unwrap();
    if total < 25.0 {
        errors.push(output::FunctionError {
            localized_message: "Minimum order value is $25.00".to_string(),
            target: output::Target::Cart,
        });
    }

    // Check product availability by region
    for line in &input.cart.lines {
        if let input::InputCartLinesMerchandise::ProductVariant(variant) = &line.merchandise {
            if is_restricted_product(&variant, &input.cart.buyer_identity) {
                errors.push(output::FunctionError {
                    localized_message: format!(
                        "{} is not available in your region",
                        variant.product.title
                    ),
                    target: output::Target::CartLine(output::CartLineTarget {
                        id: line.id.clone(),
                    }),
                });
            }
        }
    }

    Ok(output::FunctionRunResult { errors })
}
```

## Cart Transform

Modify cart contents dynamically:

```javascript
// src/run.js
export function run(input) {
  const operations = [];

  for (const line of input.cart.lines) {
    const variant = line.merchandise;

    // Add free gift for orders with specific products
    if (variant.product.hasAnyTag && line.quantity >= 3) {
      operations.push({
        expand: {
          cartLineId: line.id,
          expandedCartItems: [
            {
              merchandiseId: variant.id,
              quantity: line.quantity,
            },
            {
              merchandiseId: "gid://shopify/ProductVariant/FREE_GIFT_ID",
              quantity: 1,
            },
          ],
        },
      });
    }
  }

  return { operations };
}
```

## Testing Functions

### Local Testing

```bash
# Test with sample input
shopify app function run --path extensions/my-function

# Provide input via stdin
cat input.json | shopify app function run --path extensions/my-function
```

### Sample Input JSON

```json
{
  "cart": {
    "lines": [
      {
        "id": "gid://shopify/CartLine/1",
        "quantity": 5,
        "merchandise": {
          "__typename": "ProductVariant",
          "id": "gid://shopify/ProductVariant/123",
          "product": {
            "id": "gid://shopify/Product/456",
            "title": "Test Product",
            "hasAnyTag": true
          }
        },
        "cost": {
          "amountPerQuantity": {
            "amount": "10.00",
            "currencyCode": "USD"
          }
        }
      }
    ]
  },
  "discountNode": {
    "metafield": {
      "value": "{\"minimumQuantity\": 3, \"discountPercentage\": \"15\"}"
    }
  }
}
```

## Deployment

```bash
# Deploy function with app
shopify app deploy

# Function will be available to configure in admin
```

## Configuration UI

Create an admin UI to configure function settings:

```jsx
// app/routes/app.discount.jsx
import { authenticate } from "../shopify.server";
import { Form, TextField, Button, Card } from "@shopify/polaris";

export async function action({ request }) {
  const { admin } = await authenticate.admin(request);
  const formData = await request.formData();

  // Create discount with function
  await admin.graphql(
    `
    mutation CreateDiscount($discount: DiscountAutomaticAppInput!) {
      discountAutomaticAppCreate(automaticAppDiscount: $discount) {
        automaticAppDiscount {
          discountId
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
        discount: {
          title: formData.get("title"),
          functionId: "YOUR_FUNCTION_ID",
          startsAt: new Date().toISOString(),
          metafields: [
            {
              namespace: "volume-discount",
              key: "config",
              value: JSON.stringify({
                minimumQuantity: parseInt(formData.get("minQty")),
                discountPercentage: formData.get("percentage"),
              }),
              type: "json",
            },
          ],
        },
      },
    },
  );

  return redirect("/app/discounts");
}
```

## Performance Best Practices

1. **Use Rust for large carts** - JavaScript can timeout
2. **Minimize input query** - Only request needed data
3. **Avoid complex loops** - Keep logic simple
4. **Cache configuration** - Parse metafields once
5. **Test with real data** - Test large cart scenarios

## CLI Commands Reference

| Command                          | Description     |
| -------------------------------- | --------------- |
| `shopify app generate extension` | Create function |
| `shopify app function run`       | Test locally    |
| `shopify app function typegen`   | Generate types  |
| `shopify app deploy`             | Deploy function |

## Resources

- [Functions Overview](https://shopify.dev/docs/apps/build/functions)
- [Functions API Reference](https://shopify.dev/docs/api/functions)
- [Discount Functions](https://shopify.dev/docs/apps/build/discounts)
- [Delivery Customization](https://shopify.dev/docs/apps/build/checkout/delivery-shipping)
- [Payment Customization](https://shopify.dev/docs/apps/build/payments)
- [JavaScript for Functions](https://shopify.dev/docs/apps/build/functions/programming-languages/javascript-for-functions)
- [Rust for Functions](https://shopify.dev/docs/apps/build/functions/programming-languages/rust-for-functions)

For checkout UI, see the [checkout-customization](../checkout-customization/SKILL.md) skill.
