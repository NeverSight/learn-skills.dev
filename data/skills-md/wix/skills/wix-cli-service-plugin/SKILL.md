---
name: wix-cli-service-plugin
description: Use when implementing service plugin extensions that inject custom backend logic into existing Wix business solution flows or introduce new flows to Wix sites. Triggers include SPI, service plugin, backend flow, business logic.
compatibility: Requires Wix CLI development environment.
---

# Wix Service Plugin (SPI) Builder

Creates service plugin extensions for Wix CLI applications. Service plugins are a set of APIs defined by Wix that you can use to inject custom logic into the existing backend flows of Wix business solutions or to introduce entirely new flows to Wix sites.

When you implement a service plugin, Wix calls your custom functions during specific flows. Common use cases include eCommerce customization (shipping, fees, taxes, validations), but service plugins can extend any Wix business solution that exposes SPIs.

## Quick Start Checklist

Follow these steps in order when creating a service plugin:

1. [ ] **Read the reference doc** for your SPI type (REQUIRED before implementation)
2. [ ] Create plugin folder: `src/backend/service-plugins/<service-type>/<plugin-name>/`
3. [ ] Create `plugin.ts` with correct imports and `provideHandlers()` call
4. [ ] Implement all required handler functions with complete business logic
5. [ ] Create `extensions.ts` with appropriate builder method and unique UUID
6. [ ] Update `src/extensions.ts` to import and use the new extension
7. [ ] Run `npx tsc --noEmit` to verify TypeScript compiles
8. [ ] Run `npx wix build` to verify build succeeds
9. [ ] Test by triggering the relevant site action (e.g., add to cart for fees)

## References

**You MUST read the relevant reference document before implementing a relevant SPI.** Each reference contains the correct imports, handler signatures, response structures, and working examples.

| SPI Type | Reference |
| --- | --- |
| Additional Fees | [ADDITIONAL-FEES.md](./references/ADDITIONAL-FEES.md) |
| Discount Triggers | [DISCOUNT-TRIGGERS.md](./references/DISCOUNT-TRIGGERS.md) |
| Gift Cards | [GIFT-CARDS.md](./references/GIFT-CARDS.md) |
| Shipping Rates | [SHIPPING-RATES.md](./references/SHIPPING-RATES.md) |
| Tax Calculation | [TAX-CALCULATION.md](./references/TAX-CALCULATION.md) |
| Validations | [VALIDATIONS.md](./references/VALIDATIONS.md) |

## Output Structure

Service plugins consist of two files that work together. Registration of plugins requires an extension builder file.

```
src/backend/service-plugins/
└── {service-type}/
    └── {plugin-name}/
        ├── plugin.ts           # Handler logic with provideHandlers()
        └── extensions.ts       # Builder configuration (id, name, source)
```

### File Descriptions

| File | Purpose |
| --- | --- |
| `plugin.ts` | Contains the service plugin handler logic with `provideHandlers()` - this is where you implement your custom business logic |
| `extensions.ts` | Contains the service plugin builder configuration with id (GUID), name, description, and source path |

## Implementation Requirements

### Generation Requirements

1. **Implement ALL required handler functions** with complete business logic
2. **Include proper TypeScript types and error handling**
3. **Focus on implementing the EXACT business logic** described in the user prompt

### Implementation Patterns

- **If capabilities are undocumented/unavailable**, explicitly state the gap and proceed only with documented minimal logic
- **Implement all required handler functions** according to Wix specifications
- **Never use placeholders** - always implement complete, working functionality

### Data Validation

All service plugins must include comprehensive data validation:

- **Validate all input data** from Wix requests
- **Ensure required fields** are present and properly formatted
- **Handle missing or malformed data** gracefully
- **Validate business logic constraints** (e.g., minimum order amounts, valid addresses)

## Implementation Pattern

The handler file (`plugin.ts`) contains the service plugin logic. It must:

1. Import the relevant service plugin from `@wix/ecom/service-plugins`
2. Call `provideHandlers()` with an object containing handler functions
3. Each handler function receives a payload with `request` and `metadata`
4. Return the expected response structure for that SPI type

```typescript
import { shippingRates } from "@wix/ecom/service-plugins";

shippingRates.provideHandlers({
  getShippingRates: async (payload) => {
    const { request, metadata } = payload;

    // Implement custom logic based on request data
    // - request contains cart items, shipping address, etc.
    // - metadata contains currency, locale, etc.

    return {
      shippingRates: [
        {
          code: "custom-shipping",
          title: "Custom Shipping",
          logistics: {
            deliveryTime: "3-5 business days",
          },
          cost: {
            price: "9.99",
            currency: metadata.currency || "USD",
          },
        },
      ],
    };
  },
});
```

Handler functions are called automatically by Wix when the relevant site action triggers them. Your custom logic should be placed inside each handler function.

## Elevating Permissions for API Calls

When making Wix API calls from service plugins, you must elevate permissions using `auth.elevate` from `@wix/essentials`.

```typescript
import { auth } from "@wix/essentials";
import { items } from "@wix/data";

export const myFunction = async () => {
  const elevatedFunction = auth.elevate(items.query);
  const elevatedResponse = await elevatedFunction("myCollection");
  return elevatedResponse;
};
```

```typescript
import { auth } from "@wix/essentials";
import { cart } from "@wix/ecom";

export const myFunction = async () => {
  const elevatedFunction = auth.elevate(cart.getCart);
  const elevatedResponse = await elevatedFunction("cart-id");
  return elevatedResponse;
};
```

```typescript
import { auth } from "@wix/essentials";
import { products } from "@wix/stores";

export const myFunction = async () => {
  const elevatedFunction = auth.elevate(products.deleteCollection);
  const elevatedResponse = await elevatedFunction("collection-id");
  return elevatedResponse;
};
```

## Best Practices

### Development Workflow

- **Always implement complete, working functionality** - never use placeholders
- **Handle all required fields** according to Wix documentation
- **Implement proper validation** for all input data
- **Return responses in exact format** expected by Wix
- **Add comprehensive error handling** for all failure scenarios
- **Use meaningful variable names** and clear code structure
- **Test thoroughly** with different input combinations

### Implementation Guidelines

- **Validate all input:** Check required fields are present and properly formatted
- **Handle errors gracefully:** Return appropriate error responses, don't throw unhandled exceptions
- **Return exact format:** Responses must match Wix documented structure exactly
- **Use TypeScript types:** Leverage SDK types for better type safety
- **Test edge cases:** Empty carts, missing addresses, invalid data
- **Performance:** Keep calculations efficient - these run on every checkout
- **Logging:** Add console.log for debugging but keep production logs minimal

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Plugin-Specific Extension File

Each service plugin requires an `extensions.ts` file in its folder with the appropriate builder method for the SPI type:

```typescript
import { extensions } from "@wix/astro/builders";

export const ecomshippingratesMyShipping = extensions.ecomShippingRates({
  id: "{{GENERATE_UUID}}",
  name: "My Shipping Rates",
  description: "Calculates custom shipping rates based on order weight",
  source: "./backend/service-plugins/ecom-shipping-rates/my-shipping/plugin.ts",
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

### Builder Configuration Fields

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Service plugin ID as a GUID. Must be unique across all extensions in the project. |
| `name` | string | The service plugin name (visible in app dashboard when developing an app). |
| `description` | string | A short description of what the service plugin does. |
| `source` | string | Path to the service plugin handler file that contains the plugin logic. |

Additional fields may be required or optional depending on the specific service plugin type.

**Builder methods by SPI type:**

| SPI Type          | Builder Method           |
| ----------------- | ------------------------ |
| Shipping Rates    | `ecomShippingRates()`    |
| Additional Fees   | `ecomAdditionalFees()`   |
| Validations       | `ecomValidations()`      |
| Discount Triggers | `ecomDiscountTriggers()` |
| Gift Cards        | `ecomGiftCards()`        |
| Payment Settings  | `ecomPaymentSettings()`  |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the plugin-specific extension file, you MUST read [wix-cli-extension-registration](../wix-cli-extension-registration/SKILL.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the service plugin will not be active in the eCommerce system.**

## Testing Service Plugins

To test your service plugin extension:

1. **Release a version** with your changes - new service plugins or changes to existing ones won't take effect until you've built and released your project
2. **Trigger the call** to your service plugin by performing the relevant action (e.g., add items to cart and view cart to test Additional Fees)

For example, to test an Additional Fees service plugin that adds a $5 packaging fee:
1. Go to your site's store in the local development environment
2. Select any product and add it to the cart, then view the cart
3. Check if the additional fee is listed in the order summary

## Verification

After implementation, use [wix-cli-app-validation](../wix-cli-app-validation/SKILL.md) to validate TypeScript compilation, build, preview, and runtime behavior.
