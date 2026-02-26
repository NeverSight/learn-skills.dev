---
name: checkout-customization
description: Customize Shopify checkout with UI extensions and functions. Use this skill for building checkout UI extensions, adding custom fields, implementing payment customizations, creating post-purchase experiences, and extending customer accounts. Covers Checkout UI Extensions API and checkout branding.
license: MIT
compatibility: Requires Shopify CLI, Shopify Plus or Checkout Extensibility, and a Partner account
metadata:
  author: shopify-agent-skills
  version: "1.0"
  shopify-api-version: "2025-01"
---

# Checkout Customization

## When to use this skill

Use this skill when:

- Building checkout UI extensions
- Adding custom fields to checkout
- Implementing payment customizations
- Creating post-purchase upsells
- Extending customer account pages
- Customizing the checkout experience
- Adding custom validation logic

## Overview

Checkout customization uses extensions that are:

- **Upgrade-safe** - Work with Shop Pay and new features
- **Performant** - Run in a sandboxed environment
- **Secure** - Limited access for security

### Extension Types

| Type                  | Description                  |
| --------------------- | ---------------------------- |
| **Checkout UI**       | Add custom UI to checkout    |
| **Post-purchase**     | Upsells after order          |
| **Customer Accounts** | Extend account pages         |
| **Thank You**         | Customize order confirmation |
| **Order Status**      | Extend order tracking        |

## Getting Started

### 1. Create Checkout Extension

```bash
# In an existing app
shopify app generate extension

# Select: Checkout UI
```

### 2. Extension Structure

```
extensions/
└── checkout-ui/
    ├── src/
    │   └── Checkout.jsx
    ├── locales/
    │   └── en.default.json
    └── shopify.extension.toml
```

### 3. Configuration

```toml
# shopify.extension.toml
api_version = "2025-01"

[[extensions]]
type = "ui_extension"
name = "Custom Checkout"
handle = "custom-checkout"

[[extensions.targeting]]
module = "./src/Checkout.jsx"
target = "purchase.checkout.block.render"
```

## Checkout UI Extensions

### Basic Extension

```jsx
// src/Checkout.jsx
import {
  reactExtension,
  Banner,
  useApi,
  useTranslate,
} from "@shopify/ui-extensions-react/checkout";

export default reactExtension("purchase.checkout.block.render", () => (
  <Extension />
));

function Extension() {
  const translate = useTranslate();

  return (
    <Banner title={translate("welcomeMessage")}>
      Thank you for shopping with us!
    </Banner>
  );
}
```

### Extension Targets

Common checkout targets:

```jsx
// Before shipping options
"purchase.checkout.shipping-option-list.render-before";

// After shipping options
"purchase.checkout.shipping-option-list.render-after";

// Payment method
"purchase.checkout.payment-method-list.render-before";

// Order summary
"purchase.checkout.cart-line-list.render-after";

// Static render (header/footer)
"purchase.checkout.header.render-after";
"purchase.checkout.footer.render-after";

// Block render (anywhere in checkout)
"purchase.checkout.block.render";

// Delivery address
"purchase.checkout.delivery-address.render-before";
```

### Using Checkout Data

```jsx
import {
  useCartLines,
  useTotalAmount,
  useShippingAddress,
  useBuyerJourney,
  useCustomer,
  useDiscountCodes,
} from "@shopify/ui-extensions-react/checkout";

function Extension() {
  const cartLines = useCartLines();
  const totalAmount = useTotalAmount();
  const shippingAddress = useShippingAddress();
  const customer = useCustomer();
  const discountCodes = useDiscountCodes();

  const total = totalAmount?.amount;
  const itemCount = cartLines.reduce((sum, line) => sum + line.quantity, 0);

  return (
    <BlockStack>
      <Text>Items in cart: {itemCount}</Text>
      <Text>Total: ${total}</Text>
      {customer && <Text>Welcome back, {customer.firstName}!</Text>}
    </BlockStack>
  );
}
```

### UI Components

```jsx
import {
  Banner,
  BlockStack,
  InlineStack,
  Text,
  Button,
  Checkbox,
  TextField,
  Select,
  Image,
  Divider,
  Heading,
  Link,
  View,
  Grid,
  Icon,
} from "@shopify/ui-extensions-react/checkout";

function Extension() {
  const [checked, setChecked] = useState(false);
  const [note, setNote] = useState("");

  return (
    <BlockStack spacing="base">
      <Heading level={2}>Gift Options</Heading>

      <Checkbox checked={checked} onChange={setChecked}>
        This is a gift
      </Checkbox>

      {checked && (
        <TextField
          label="Gift message"
          value={note}
          onChange={setNote}
          multiline
        />
      )}

      <InlineStack spacing="tight">
        <Button kind="secondary" onPress={() => {}}>
          Cancel
        </Button>
        <Button onPress={() => {}}>Save</Button>
      </InlineStack>
    </BlockStack>
  );
}
```

### Custom Fields with Metafields

```jsx
import {
  useApplyMetafieldsChange,
  useMetafield,
} from "@shopify/ui-extensions-react/checkout";

function GiftMessage() {
  const [message, setMessage] = useState("");
  const applyMetafieldsChange = useApplyMetafieldsChange();

  const handleChange = async (value) => {
    setMessage(value);
    await applyMetafieldsChange({
      type: "updateMetafield",
      namespace: "custom",
      key: "gift_message",
      valueType: "string",
      value,
    });
  };

  return (
    <TextField label="Gift message" value={message} onChange={handleChange} />
  );
}
```

### Buyer Journey Intercept

Block checkout progression with validation:

```jsx
import { useBuyerJourneyIntercept } from "@shopify/ui-extensions-react/checkout";

function AgeVerification() {
  const [verified, setVerified] = useState(false);

  useBuyerJourneyIntercept(({ canBlockProgress }) => {
    if (!verified && canBlockProgress) {
      return {
        behavior: "block",
        reason: "Age verification required",
        errors: [
          {
            message: "Please verify your age to continue",
          },
        ],
      };
    }
    return { behavior: "allow" };
  });

  return (
    <Checkbox checked={verified} onChange={setVerified}>
      I confirm I am 21 or older
    </Checkbox>
  );
}
```

## Post-Purchase Extensions

### Create Post-Purchase Extension

```bash
shopify app generate extension
# Select: Post-purchase UI
```

### Post-Purchase Upsell

```jsx
// src/PostPurchase.jsx
import {
  extend,
  render,
  useExtensionInput,
  BlockStack,
  Button,
  Text,
  Image,
  Heading,
  CalloutBanner,
  Layout,
  TextContainer,
} from "@shopify/post-purchase-ui-extensions-react";

extend("Checkout::PostPurchase::ShouldRender", async ({ storage }) => {
  // Decide whether to show post-purchase
  const upsellProduct = await fetchUpsellProduct();
  await storage.update({ upsellProduct });
  return { render: true };
});

render("Checkout::PostPurchase::Render", () => <App />);

function App() {
  const { storage, done, calculateChangeset, applyChangeset } =
    useExtensionInput();
  const { upsellProduct } = storage.initialData;

  const handleAccept = async () => {
    const changeset = await calculateChangeset({
      changes: [
        {
          type: "add_variant",
          variantId: upsellProduct.variantId,
          quantity: 1,
        },
      ],
    });

    await applyChangeset(changeset.token);
    done();
  };

  const handleDecline = () => {
    done();
  };

  return (
    <BlockStack spacing="loose">
      <CalloutBanner title="Special Offer!">
        Add this item to your order at 20% off
      </CalloutBanner>

      <Layout
        media={[
          { viewportSize: "small", sizes: [1, 0, 1], maxInlineSize: 0.9 },
          { viewportSize: "medium", sizes: [532, 0, 1], maxInlineSize: 420 },
          { viewportSize: "large", sizes: [560, 38, 340] },
        ]}
      >
        <Image source={upsellProduct.imageUrl} />
        <View />
        <BlockStack spacing="tight">
          <Heading>{upsellProduct.title}</Heading>
          <TextContainer>
            <Text size="medium">${upsellProduct.price} (20% off)</Text>
          </TextContainer>
          <Button onPress={handleAccept}>Add to Order</Button>
          <Button onPress={handleDecline} plain>
            No thanks
          </Button>
        </BlockStack>
      </Layout>
    </BlockStack>
  );
}
```

## Customer Account Extensions

```jsx
// Extend customer account pages
import {
  reactExtension,
  Page,
  Card,
  BlockStack,
  Text,
} from "@shopify/ui-extensions-react/customer-account";

export default reactExtension("customer-account.page.render", () => (
  <CustomAccountPage />
));

function CustomAccountPage() {
  return (
    <Page title="Rewards">
      <Card padding>
        <BlockStack spacing="loose">
          <Text size="large">Your Points: 500</Text>
          <Text>Earn points with every purchase!</Text>
        </BlockStack>
      </Card>
    </Page>
  );
}
```

## Localization

```json
// locales/en.default.json
{
  "welcomeMessage": "Welcome to checkout",
  "giftLabel": "Gift options",
  "verifyAge": "I confirm I am 21 or older"
}

// locales/fr.json
{
  "welcomeMessage": "Bienvenue au paiement",
  "giftLabel": "Options cadeau",
  "verifyAge": "Je confirme avoir 21 ans ou plus"
}
```

```jsx
import { useTranslate } from "@shopify/ui-extensions-react/checkout";

function Extension() {
  const translate = useTranslate();
  return <Text>{translate("welcomeMessage")}</Text>;
}
```

## Network Requests

```jsx
import { useApi } from "@shopify/ui-extensions-react/checkout";

function Extension() {
  const { sessionToken } = useApi();

  const fetchData = async () => {
    const token = await sessionToken.get();

    const response = await fetch("https://your-app.com/api/data", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return response.json();
  };

  // Use in useEffect or event handler
}
```

## Testing

### Local Development

```bash
# Start app with preview
shopify app dev

# Extensions will load in checkout preview
```

### Testing in Checkout Editor

1. Go to Shopify admin > Settings > Checkout
2. Click "Customize"
3. Add your extension block
4. Preview changes

## Best Practices

1. **Keep extensions fast** - Minimize API calls
2. **Handle errors gracefully** - Show user-friendly messages
3. **Support localization** - Use translation files
4. **Test on mobile** - Checkout is often mobile
5. **Follow design guidelines** - Match Shopify's checkout style
6. **Use progressive enhancement** - Graceful degradation

## Resources

- [Checkout UI Extensions](https://shopify.dev/docs/api/checkout-ui-extensions)
- [Checkout UI Components](https://shopify.dev/docs/api/checkout-ui-extensions/components)
- [Post-Purchase Extensions](https://shopify.dev/docs/apps/build/checkout/post-purchase)
- [Customer Account Extensions](https://shopify.dev/docs/api/checkout-ui-extensions/extension-targets-overview#customer-account-targets)
- [Extension Targets Reference](https://shopify.dev/docs/api/checkout-ui-extensions/extension-targets-overview)

For backend logic, see the [shopify-functions](../shopify-functions/SKILL.md) skill.
