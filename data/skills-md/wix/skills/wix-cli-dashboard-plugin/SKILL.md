---
name: wix-cli-dashboard-plugin
description: Use when building widgets that extend Wix dashboard pages for first-party business apps. Triggers include dashboard plugin, dashboard slot, extend dashboard page, Wix Stores plugin, Wix Bookings plugin, Wix Blog plugin, observeState, dashboard widget. Do NOT use for standalone dashboard pages (use wix-cli-dashboard-page) or site-facing UI (use site widgets/site plugins).
compatibility: Requires Wix CLI development environment.
---

# Wix Dashboard Plugin Builder

Creates dashboard plugin extensions for Wix CLI applications. Dashboard plugins are interactive widgets that embed into predefined **slots** on dashboard pages managed by Wix first-party business apps (Wix Stores, Wix Bookings, Wix Blog, Wix eCommerce, etc.).

Dashboard plugins occupy the full width of their slot and maintain dynamic height based on content.

---

## Quick Start Checklist

Follow these steps in order when creating a dashboard plugin:

1. [ ] Identify the target slot ID — see [Slots Reference](references/SLOTS.md)
2. [ ] Create plugin folder: `src/extensions/dashboard/plugins/<plugin-name>/`
3. [ ] Create `<plugin-name>.extension.ts` with `extensions.dashboardPlugin()` and unique UUID
4. [ ] Create `<plugin-name>.tsx` with React component wrapped in `WixDesignSystemProvider`
5. [ ] Update `src/extensions.ts` to import and use the new extension

## Architecture

Dashboard plugins operate through two mechanisms:

1. **Visual Integration** — Embedding plugin UI inside a supported dashboard page slot
2. **Logical Integration** — Implementing communication between the plugin and the host page's data via `observeState()`

## Files and Code Structure

Dashboard plugins live under `src/extensions/dashboard/plugins/`. Each plugin has its own folder.

```
src/extensions/dashboard/plugins/
└── <plugin-name>/
    ├── <plugin-name>.extension.ts   # Builder configuration
    └── <plugin-name>.tsx            # React component
```

> **Note:** This is the default folder structure created by the CLI. You can move these files to any location within the `src/` folder and update the references in your `extension.ts` file.

## Plugin Builder Configuration

### File: `<plugin-name>.extension.ts`

```typescript
import { extensions } from "@wix/astro/builders";

export const dashboardpluginMyPlugin = extensions.dashboardPlugin({
  id: "{{GENERATE_UUID}}",
  title: "My Dashboard Plugin",
  extends: "<SLOT_ID>",
  component: "./extensions/dashboard/plugins/my-plugin/my-plugin.tsx",
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension — do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

### Builder Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique plugin ID (GUID). Must be unique across all extensions in the project. |
| `title` | string | Plugin title. Used to refer to the plugin in the project dashboard. |
| `extends` | string | Slot ID of the dashboard page hosting the plugin. See [Slots Reference](references/SLOTS.md). |
| `component` | string | Relative path to the plugin content component (`.tsx` file). |

### The `extends` Field

The `extends` field specifies which dashboard page slot hosts your plugin. Each Wix business app exposes slots on its dashboard pages. You must provide the exact slot ID.

**Important:** Some slots with the same ID appear on different pages within the dashboard. If you create a plugin for a slot that exists on multiple pages, the plugin is displayed on all of those pages.

For the complete list of available slot IDs, see [Slots Reference](references/SLOTS.md).

## Plugin Component

### File: `<plugin-name>.tsx`

The plugin component is a React component that renders within the dashboard page slot.

```typescript
import type { FC } from "react";
import { WixDesignSystemProvider, Card, Text } from "@wix/design-system";
import "@wix/design-system/styles.global.css";

const Plugin: FC = () => {
  return (
    <WixDesignSystemProvider features={{ newColorsBranding: true }}>
      <Card>
        <Card.Header title="My Plugin" />
        <Card.Divider />
        <Card.Content size="medium">
          <Text>Plugin content goes here.</Text>
        </Card.Content>
      </Card>
    </WixDesignSystemProvider>
  );
};

export default Plugin;
```

### Available Resources in Plugin Components

- **React** — Component logic and state management
- **Wix SDK** — Access Wix business solutions and site data
- **Wix Dashboard SDK** (`@wix/dashboard`) — Interact with the dashboard page's data passed to the slot
- **Wix Design System** (`@wix/design-system`) — Native-looking React components matching Wix's own dashboard UI

## Interacting with Dashboard Data

Use `observeState()` from the Dashboard SDK to receive data from the host dashboard page:

```typescript
import { dashboard } from "@wix/dashboard";
import { useEffect, useState } from "react";

const Plugin: FC = () => {
  const [params, setParams] = useState<Record<string, unknown>>({});

  useEffect(() => {
    dashboard.observeState((componentParams) => {
      setParams(componentParams);
    });
  }, []);

  return (
    <WixDesignSystemProvider features={{ newColorsBranding: true }}>
      <Card>
        <Card.Content size="medium">
          <Text>Received data: {JSON.stringify(params)}</Text>
        </Card.Content>
      </Card>
    </WixDesignSystemProvider>
  );
};
```

### Typed Props from Host Apps

Some Wix apps expose typed interfaces for their slot parameters. Import them from the app's dashboard package:

```typescript
import type { plugins } from "@wix/blog/dashboard";

type Props = plugins.BlogPosts.PostsBannerParams;

const Plugin: FC<Props> = (props) => {
  // props are typed according to the Blog Posts slot contract
};
```

> **Note:** Typed props availability varies by Wix app. Consult the specific app's SDK documentation. Not all slots provide typed parameter interfaces.

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Plugin-Specific Extension File

Each dashboard plugin requires an `<plugin-name>.extension.ts` file in its folder. See [Plugin Builder Configuration](#plugin-builder-configuration) above.

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the plugin-specific extension file, you MUST read [wix-cli-extension-registration](../wix-cli-extension-registration/SKILL.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the dashboard plugin will not appear on the dashboard page.**

## Sizing Behavior

- Dashboard plugins take the **full width** of their slot
- **Height** adjusts dynamically based on content within slot boundaries
- When using Dashboard SDK or dashboard-react SDK, dimensions change dynamically based on contents

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Plugin not appearing on dashboard page | Missing registration | Import and `.use()` in `src/extensions.ts` |
| Plugin not appearing on dashboard page | Wrong slot ID | Verify `extends` field matches a valid slot ID from [Slots Reference](references/SLOTS.md) |

## Hard Constraints

- Do NOT invent or assume new types, modules, functions, props, events, or imports — use only entities explicitly present in the provided references or standard libraries already used in this project
- NEVER use mocks, placeholders, or TODOs in any code — ALWAYS implement complete, production-ready functionality
- The `extends` field MUST contain a valid slot ID from a Wix business app — do NOT invent slot IDs
- Prefer type-narrowing and exhaustive logic over assertions; avoid non-null assertions (`!`) and unsafe casts (`as any`)
- Do NOT use `// @ts-ignore` or `// @ts-expect-error`; fix the types or add guards instead

## Examples

### Blog Posts Banner Plugin

**Request:** "Create a plugin for the Wix Blog posts page that shows a promotional banner"

**Output:** Plugin targeting slot `46035d51-2ea9-4128-a216-1dba68664ffe` (Blog Posts page) with a Card component displaying promotional content, using `observeState()` to access blog post data.

### Bookings Staff Calendar Widget

**Request:** "Add a plugin to the Wix Bookings staff page that shows weekly availability"

**Output:** Plugin targeting slot `261e84a2-31d0-4258-a035-10544d251108` (Bookings Staff page) with a schedule display component, using `observeState()` to receive staff data.

### Order Details Plugin

**Request:** "Create a plugin on the eCommerce order page showing fulfillment status"

**Output:** Plugin targeting slot `cb16162e-42aa-41bd-a644-dc570328c6cc` (eCommerce Order page) with status badges and fulfillment details, using `observeState()` to access order data.

### Output Constraints

**Token limits:** Your max output is ~10,000 tokens. Plan your response to stay under this limit.

- If making a large file (>300 lines), split it into multiple smaller files with imports
- Only output files that are directly required for the task
- Do NOT add README.md or documentation files unless explicitly requested

## Verification

After implementation, use [wix-cli-app-validation](../wix-cli-app-validation/SKILL.md) to validate TypeScript compilation, build, preview, and runtime behavior.
