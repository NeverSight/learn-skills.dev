---
name: wix-cli-extension-registration
description: Register Wix CLI extensions with the app in src/extensions.ts. Use when registering new or existing extensions with the main app builder.
---

# Wix App Registration

After creating any extension file, you MUST update the main `src/extensions.ts` file to register the extension with the app. Without this step, the extension will not be recognized by Wix CLI.

## Simple Pattern (Recommended for Small Apps)

**`src/extensions.ts`** - Import and register extensions directly:

```typescript
import { app } from "@wix/astro/builders";
import { dataExtension } from "./data/extensions.ts";
import { dashboardpageMyPage } from "./dashboard/pages/my-page/extensions.ts";
import { embeddedscriptMyScript } from "./site/embedded-scripts/my-script/extensions.ts";

export default app()
  .use(dataExtension)
  .use(dashboardpageMyPage)
  .use(embeddedscriptMyScript);
```

**Steps for each new extension:**

1. Import the extension from its `extensions.ts` file
2. Add `.use(extensionName)` to the app chain
3. Chain multiple extensions together

## Advanced Pattern (For Large Apps)

**`src/index.ts`** - Re-export all extensions:

```typescript
export { dashboardpageMyPage } from "./dashboard/pages/my-page/extensions";
export { embeddedscriptMyScript } from "./site/embedded-scripts/my-script/extensions";
export { dataExtension } from "./data/extensions";
```

**`src/extensions.ts`** - Register all extensions programmatically:

```typescript
import { app } from "@wix/astro/builders";
import * as allExtensions from "./index";

const extensionList = Object.values(allExtensions);

const appBuilder = app();
extensionList.forEach((extension) => {
  appBuilder.use(extension);
});

export default appBuilder;
```

## Extension Types Without Registration

The following extension types do **not** require `extensions.ts` files:

- **Backend API** - Astro server endpoints are auto-discovered

## Naming Conventions

Extension export names follow this pattern: `{extensiontype}{CamelCaseName}`

Examples:

- `dashboardpageCartPopupManager`
- `embeddedscriptCouponPopup`
- `sitewidgetCountdownWidget`
- `sitepluginProductBadge`
- `ecomshippingratesCustomShipping`

The type prefix is the extension type in lowercase with no separators.
