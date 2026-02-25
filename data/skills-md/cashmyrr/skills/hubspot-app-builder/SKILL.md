---
name: hubspot-app-builder
description: This skill should be used when the user asks to "build a HubSpot app", "create a HubSpot app", "add a card to HubSpot", "create an app card", "build a UI extension", "set up HubSpot webhooks", "configure HubSpot app", "add a settings page to HubSpot app", "build a HubSpot home page", "fetch data in HubSpot extension", "list an app on the HubSpot marketplace", "submit a HubSpot app listing", "marketplace listing requirements", or mentions building on the HubSpot developer platform 2025.2. Provides comprehensive guidance for building full HubSpot apps with best practices, CLI commands, file structure, and App Marketplace listing requirements.
version: 1.0.0
---

# HubSpot App Builder (Platform 2025.2)

This skill guides the development of full HubSpot apps on the latest developer platform (version `2025.2`), covering project creation, configuration, UI extensions, webhooks, and distribution.

## Prerequisites

- HubSpot CLI v7.6.0+: `npm install -g @hubspot/cli@latest`
- Authenticate: `hs account auth`
- Node.js 18+
- A HubSpot developer account

## Project Setup Workflow

### 1. Create the Project

```shell
hs project create
```

Follow CLI prompts to configure:
- **Distribution**: `marketplace` (for App Marketplace listing) or `private` (for specific accounts)
- **Auth**: `oauth` (multiple accounts) or `static` (single account)
- **Features**: Select from `card`, `settings`, `app-function`, `webhooks`, `workflow-action`

To add a feature later:
```shell
hs project add
```

### 2. Project File Structure

```
my-project-folder/
├── hsproject.json
└── src/
    └── app/
        ├── app-hsmeta.json          # Top-level app config (required)
        ├── cards/                    # UI extension cards
        │   ├── MyCard.jsx
        │   ├── my-card-hsmeta.json
        │   └── package.json
        ├── settings/                 # App settings page
        │   ├── Settings.tsx
        │   ├── settings-hsmeta.json
        │   └── package.json
        ├── app-events/               # App events (open beta)
        │   └── my-event-hsmeta.json
        ├── app-objects/              # App objects (open beta)
        │   └── my-object-hsmeta.json
        ├── webhooks/                 # Webhook subscriptions
        │   └── webhooks-hsmeta.json
        └── workflow-actions/         # Custom workflow actions
            └── custom-action-hsmeta.json
```

### 3. Configure `app-hsmeta.json`

```json
{
  "uid": "my_app_uid",
  "type": "app",
  "config": {
    "name": "My App",
    "description": "App description for installing users.",
    "distribution": "marketplace",
    "auth": {
      "type": "oauth",
      "redirectUrls": ["http://localhost:3000/oauth-callback"],
      "requiredScopes": ["crm.objects.contacts.read"],
      "optionalScopes": [],
      "conditionallyRequiredScopes": []
    },
    "permittedUrls": {
      "fetch": ["https://api.example.com"],
      "iframe": [],
      "img": []
    },
    "support": {
      "supportEmail": "support@example.com",
      "documentationUrl": "https://example.com/docs"
    }
  }
}
```

Key rules:
- `uid` must be globally unique within the project (up to 64 chars, alphanumeric + `_`, `-`, `.`)
- `type` must match the parent folder name (`app`)
- Use `static` auth + remove `redirectUrls` for single-account private apps
- At minimum, include one `read` scope (e.g., `crm.objects.contacts.read`)

### 4. Upload and Deploy

```shell
hs project upload          # Upload and trigger a build
hs project open            # Open project in HubSpot browser
hs project dev             # Start local dev server with hot reload
hs project install-deps    # Install package.json dependencies
```

### 5. Install the App

After uploading, install via HubSpot UI:
- Navigate to **Development > Projects > [Project Name] > [App UID]**
- Click the **Distribution** tab
- For test accounts: click **Add test install(s)**
- For standard accounts: click **Install now**

## UI Extensions

All UI extensions share the same structure: a `*-hsmeta.json` config + a React component file (`.jsx` or `.tsx`).

### App Card Configuration (`cards/*-hsmeta.json`)

```json
{
  "uid": "my-card",
  "type": "card",
  "config": {
    "name": "My Card",
    "description": "Card description.",
    "location": "crm.record.tab",
    "entrypoint": "/app/cards/MyCard.jsx",
    "objectTypes": ["contacts"]
  }
}
```

**Supported locations:**
| Location | Value | Notes |
|---|---|---|
| CRM middle column | `crm.record.tab` | Most common; supports custom tabs |
| CRM right sidebar | `crm.record.sidebar` | No CRM data components here |
| CRM preview panel | `crm.preview` | Record previews across CRM |
| Help desk sidebar | `helpdesk.sidebar` | Requires `tickets` scope |
| App home page | `home` | Full-screen extension |
| App settings page | `settings` | Config UI in HubSpot settings |

**Supported objectTypes:** `contacts`, `companies`, `deals`, `tickets`, `orders`, `carts`, `p_customObjectName`, `app_object_uid`

### React Component Pattern

```jsx
import React from "react";
import { hubspot, Text, Button, Flex } from "@hubspot/ui-extensions";

// Required: register extension with HubSpot
hubspot.extend(({ context, actions }) => (
  <MyCard context={context} addAlert={actions.addAlert} />
));

const MyCard = ({ context, addAlert }) => {
  return (
    <Flex direction="column" gap="medium">
      <Text>Hello, {context.user.firstName}!</Text>
      <Button onClick={() => addAlert({ type: "success", title: "Done", message: "Action completed" })}>
        Click me
      </Button>
    </Flex>
  );
};
```

### SDK Hooks (Preferred Approach)

```tsx
import { hubspot, Button, useExtensionApi } from "@hubspot/ui-extensions";
import { useCrmProperties } from "@hubspot/ui-extensions/crm";

hubspot.extend<'crm.record.tab'>(() => <MyCard />);

const MyCard = () => {
  // Access both context and actions
  const { context, actions } = useExtensionApi<'crm.record.tab'>();

  // Fetch CRM properties from the current record
  const { properties, isLoading } = useCrmProperties(["firstname", "lastname", "email"]);

  if (isLoading) return <Text>Loading...</Text>;

  return (
    <Button onClick={() => actions.addAlert({ message: `Hello ${properties.firstname}!` })}>
      Say Hello
    </Button>
  );
};
```

**Available hooks:**
- `useExtensionApi<location>()` — access both context + actions
- `useExtensionContext<location>()` — access context only
- `useExtensionActions<location>()` — access actions only
- `useCrmProperties(["prop1", "prop2"])` — from `@hubspot/ui-extensions/crm`
- `useAssociations({ toObjectType, properties, pageLength })` — from `@hubspot/ui-extensions/crm`

### Fetching External Data

```jsx
import { hubspot } from "@hubspot/ui-extensions";

// In component
const response = await hubspot.fetch("https://api.example.com/data", {
  method: "GET",
  timeout: 5000,
});
const data = await response.json();
```

Requirements:
- Add the URL to `permittedUrls.fetch` in `app-hsmeta.json`
- URLs must use HTTPS (no localhost — use proxy for local dev)
- Max 20 concurrent requests per account; 15s timeout; 1MB payload limit
- No custom headers except `Authorization`; HubSpot signs requests automatically with `X-HubSpot-Signature-v3`

**Your backend must validate `X-HubSpot-Signature-v3` on every request coming from a CRM card or settings page fetch.** This is the same validation required for webhooks — use `Signature.isValid()` from `@hubspot/api-client`. Without it, anyone can send fake requests to your endpoint.

For local dev proxy, create `local.json` in the project root:
```json
{
  "proxy": {
    "https://api.example.com": "http://localhost:8080"
  }
}
```

## Available UI Components

Import from `@hubspot/ui-extensions`:
- **Layout**: `Flex`, `Box`, `Divider`, `Grid`
- **Text/Display**: `Text`, `Heading`, `Image`, `Link`
- **Input**: `Input`, `TextArea`, `Select`, `MultiSelect`, `Checkbox`, `RadioButton`, `DateInput`, `NumberInput`
- **Actions**: `Button`, `LoadingButton`, `IconButton`
- **Feedback**: `Alert`, `LoadingSpinner`, `Tag`, `Badge`
- **Overlay**: `Modal`, `ModalBody`, `ModalFooter`, `Panel`, `PanelBody`, `PanelFooter`
- **Data**: `Table`, `TableHead`, `TableBody`, `TableRow`, `TableCell`
- **Form**: `Form`, `FormField`

Import from `@hubspot/ui-extensions/crm` (CRM points only, not sidebar):
- `CrmPropertyList` — display/edit CRM properties
- `CrmAssociationTable` — show associated records
- `CrmAssociationPivotTable`
- `ReportChart`

## Webhooks Configuration

Create `src/app/webhooks/webhooks-hsmeta.json`:

```json
{
  "uid": "my-webhooks",
  "type": "webhooks",
  "config": {
    "settings": {
      "targetUrl": "https://api.example.com/webhook",
      "maxConcurrentRequests": 10
    },
    "subscriptions": {
      "crmObjects": [
        {
          "subscriptionType": "object.creation",
          "objectType": "contact",
          "active": true
        },
        {
          "subscriptionType": "object.propertyChange",
          "objectType": "contact",
          "active": true
        }
      ],
      "legacyCrmObjects": [
        {
          "subscriptionType": "contact.propertyChange",
          "propertyName": "email",
          "active": true
        }
      ],
      "hubEvents": [
        {
          "subscriptionType": "contact.privacyDeletion",
          "active": true
        }
      ]
    }
  }
}
```

Use `crmObjects` for new-format events (`object.*`). Use `legacyCrmObjects` for classic types like `contact.creation`. Use `hubEvents` for `contact.privacyDeletion` and `conversation.*`.

### Signature Validation (Required)

HubSpot signs all outbound requests with `X-HubSpot-Signature-v3`:
- **Webhook deliveries** — HubSpot POSTs event payloads to your `targetUrl`
- **Card / settings page fetch** — any `hubspot.fetch()` call from a UI extension is proxied and signed by HubSpot

Both must be validated the same way using `Signature.isValid()` from `@hubspot/api-client`. For the complete implementation, see [`references/signature-validation.md`](references/signature-validation.md).

## `package.json` for UI Extensions

```json
{
  "name": "my-card",
  "version": "0.1.0",
  "dependencies": {
    "@hubspot/ui-extensions": "latest",
    "react": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3"
  }
}
```

Install: `hs project install-deps`

## Distribution & Auth Summary

| Distribution | Auth Type | Install Limit |
|---|---|---|
| `private` | `static` | 1 standard account + 10 test accounts |
| `private` | `oauth` | Up to 10 allowlisted accounts |
| `marketplace` | `oauth` | 25 before listing; unlimited after |

## App Marketplace Listing

Before submitting to the HubSpot App Marketplace, the app must meet these key requirements:

**Technical minimums:**
- OAuth is the **sole** authorization method — no API keys or private app tokens
- At least **3 active installs** from unaffiliated accounts with OAuth-authenticated API activity in the past 30 days
- Only request scopes the app actually uses; all requested scopes must appear in the *Shared data* table
- Classic CRM cards are **not allowed** (deprecated June 16, 2025)

**Listing content:**
- Content must be integration-specific (not general product marketing)
- All URLs must be live, publicly accessible, and under 250 characters — add *HubSpot Crawler* to your site allow list before submitting
- Include: setup documentation, Install button URL, support resources, Terms of Service, Privacy Policy, and pricing (matching your website exactly)
- Bi-directional sync must be declared in *Shared data* when both read and write scopes are requested for the same object

**App cards (if using UI extensions):**
- Do not use HubSpot brand names in card names or icons
- One primary button per surface; destructive buttons must use destructive styling
- Must not access or display sensitive data

**Review process:** Initial review within 10 business days; full cycle up to 60 days. Only one app can be under review at a time.

For the complete requirements checklist, see [`references/marketplace-listing.md`](references/marketplace-listing.md).

## Local Development

```shell
hs project dev            # Starts dev server with hot reload
```

After starting, a local development homepage appears in the test account showing active dev sessions. Changes to `.jsx`/`.tsx` files reload automatically.

Note (Chrome 142+): Accept the local network access popup from `app.hubspot.com` on first launch.

## Debugging

View logs: **Development > Monitoring > Logs > UI Extensions** in HubSpot.

In code, use the logger:
```js
import { logger } from "@hubspot/ui-extensions";
logger.info("Info message");
logger.debug("Debug message");
logger.warn("Warning message");
logger.error("Error message");
```

## Additional Resources

### Reference Files

For detailed configuration and patterns, consult:
- **`references/app-configuration.md`** — Complete `app-hsmeta.json` schema, scopes, auth types
- **`references/ui-extensions-sdk.md`** — SDK hooks, context fields, actions API
- **`references/ui-components.md`** — All UI components with examples
- **`references/features.md`** — App events, app objects (open beta), settings page, home page
- **`references/signature-validation.md`** — Full signature validation implementation for webhooks and card/settings page fetch endpoints
- **`references/marketplace-listing.md`** — Full App Marketplace listing requirements, brand rules, app card criteria, and review process

### Official Documentation

- [Create an app](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/create-an-app)
- [App configuration reference](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/app-configuration)
- [Manage apps in HubSpot](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/manage-apps-in-hubspot)
- [UI extensions overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/overview)
- [App cards reference](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/app-cards/reference)
- [UI extensions SDK](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/ui-extensions-sdk)
- [Fetching data](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/fetching-data)
- [UI components overview](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/ui-components/overview)
- [App home page](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/create-an-app-home-page)
- [Settings page](https://developers.hubspot.com/docs/apps/developer-platform/add-features/ui-extensibility/create-a-settings-component)
- [App events (beta)](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-events/overview)
- [App objects (beta)](https://developers.hubspot.com/docs/apps/developer-platform/add-features/app-objects/overview)
- [Configure webhooks](https://developers.hubspot.com/docs/apps/developer-platform/add-features/configure-webhooks)
- [App Marketplace listing requirements](https://developers.hubspot.com/docs/apps/developer-platform/list-apps/listing-your-app/app-marketplace-listing-requirements)
- [How to list your app](https://developers.hubspot.com/docs/apps/developer-platform/list-apps/listing-your-app/listing-your-app)
- [App certification requirements](https://developers.hubspot.com/docs/apps/developer-platform/list-apps/apply-for-certification/certification-requirements)
