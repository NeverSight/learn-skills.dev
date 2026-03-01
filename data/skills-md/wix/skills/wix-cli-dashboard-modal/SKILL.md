---
name: wix-cli-dashboard-modal
description: Use when adding popup forms, confirmations, or detail views to Wix dashboards; creating reusable dialog components across dashboard pages; showing context-specific information in overlays; opening modals from dashboard pages; or passing data between dashboard pages and modals. Do NOT use for static content (use dashboard pages instead) or site-facing UI (use site widgets/embedded scripts).
compatibility: Requires Wix CLI development environment.
---

## Overview

Dashboard modals are popup dialogs triggered from dashboard pages or plugins. They consist of three files and use the Dashboard SDK for lifecycle control via `openModal()` and `closeModal()`.

## Quick Reference

| Task | Method | Example |
|------|--------|---------|
| Create modal | Create 3 files in `src/dashboard/modals/<folder>/` | See File Structure below |
| Open modal | `dashboard.openModal()` | `openModal({ modalId: "modal-id" })` |
| Pass data to modal | `params` in `openModal()` | `params: { userId: "123" }` |
| Read data in modal | `observeState()` | `dashboard.observeState((state) => { ... })` |
| Close modal | `dashboard.closeModal()` | `closeModal()` |
| Return data to parent | Pass data to `closeModal()` | `closeModal({ ... })` |
| Wait for modal close | `modalClosed` Promise | `const { modalClosed } = openModal(...);` |

## File Structure

Create **three files** in `src/dashboard/modals/<folder-name>/`:

1. **`extensions.ts`** - Builder configuration with modal ID, title, dimensions, component path
2. **`<modal-name>.tsx`** - React component rendering modal content
3. **`<modal-name>.config.ts`** - Configurable modal properties (title, width, height)

## Implementation

### Creating a Modal

Create the three required files:

**1. `extensions.ts`** - Modal builder configuration:

```typescript
import { extensions } from '@wix/astro/builders';
import config from './<modal-name>.config.ts';

export default extensions.dashboardModal({
  id: "{{GENERATE_UUID}}",
  title: config.title,
  width: config.width,
  height: config.height,
  component: './extensions/dashboard/modals/<modal-name>/<modal-name>.tsx',
});

```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

Builder fields:
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique modal ID (GUID). Used with `openModal()` |
| title | string | Modal title shown in project dashboard |
| width | number | Initial width while loading |
| height | number | Initial height while loading |
| component | string | Path to the modal content `.tsx` file |

**2. `<modal-name>.tsx`** - Modal content component:

```typescript
import type { FC } from 'react';
import { dashboard } from '@wix/dashboard';
import {
  WixDesignSystemProvider,
  Text,
  Box,
  CustomModalLayout,
} from '@wix/design-system';
import '@wix/design-system/styles.global.css';
import config from './<modal-name>.config.ts';

const { width, height, title } = config;

// To open your modal, call `openModal` with your modal id.
// e.g.
// import { dashboard } from '@wix/dashboard';
// function MyComponent() {
//   return <button onClick={() => dashboard.openModal({ modalId: '8ef4d434-9c80-44f5-a3f5-6f15f3a34be7' })}>Open Modal</button>;
// }
const Modal: FC = () => {
  return (
    <WixDesignSystemProvider features={{ newColorsBranding: true }}>
      <CustomModalLayout
        width={width}
        maxHeight={height}
        primaryButtonText="Save"
        secondaryButtonText="Cancel"
        primaryButtonOnClick={() => dashboard.closeModal()}
        secondaryButtonOnClick={() => dashboard.closeModal()}
        title={title}
        subtitle="Edit this file to customize your modal"
        content={
          <Box direction="vertical" align="center">
            <Text>Wix CLI Modal</Text>
          </Box>
        }
      />
    </WixDesignSystemProvider>
  );
};

export default Modal;
```

**3. `<modal-name>.config.ts`** - Configurable properties:

```typescript
export default {
  title: "My Modal",
  width: 600,
  height: 400,
};
```

Then register in `src/extensions.ts`:

```typescript
import { dashboardmodalYourModal } from './dashboard/modals/<modal-name>/extensions.ts';

export default app()
  .use(dashboardmodalYourModal)
  // ... other extensions
```

### Opening a Modal

```typescript
import { dashboard } from "@wix/dashboard";

// Simple open
const result = await dashboard.openModal({
  modalId: "your-modal-id", // From .extension.ts id field
});

// Pass data to modal via params
const result = await dashboard.openModal({
  modalId: "your-modal-id",
  params: {
    userId: user.id,
    itemData: complexObject, // Objects are passed directly, no encoding needed
  },
});

// Get notified when the modal is closed
const { modalClosed } = dashboard.openModal({
  modalId: "your-modal-id",
});
const result = await modalClosed; // Resolves with data from closeModal()
```

### Receiving Data in Modal

Use `observeState()` to access data passed via `params` in `openModal()`:

```typescript
import { dashboard } from "@wix/dashboard";
import { useEffect, useState } from "react";

function MyModal() {
  const [modalData, setModalData] = useState<{ userId?: string; itemData?: any }>({});

  useEffect(() => {
    dashboard.observeState((state) => {
      // Access custom data passed through openModal params
      if (state.userId) {
        setModalData({
          userId: state.userId,
          itemData: state.itemData,
        });
      }
    });
  }, []);

  return <div>User ID: {modalData.userId}</div>;
}
```

### Closing Modal

Call `closeModal()` from within the modal extension to close it. Optionally pass data back to the opener.

```typescript
import { dashboard } from "@wix/dashboard";

// Close without returning data
dashboard.closeModal();

// Close with custom return data
dashboard.closeModal({ saved: true, itemId: "123" });
```

| Parameter | Type | Description |
|-----------|------|-------------|
| closeData | Serializable (optional) | Data to pass back to the modal opener. Must be cloneable via [structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm) - no function callbacks. |

**Returns:** `void`

### Customizing Modal

Edit `.config.ts` for organized settings:

```typescript
export default {
  title: 'User Settings',
  width: 600,
  height: 500,
}
```

Import in `.tsx`:

```typescript
import config from './modal.config.ts';

export default function MyModal() {
  return (
    <CustomModalLayout
      title={config.title}
      // ... rest of component
    />
  );
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Can't find modal ID | Check `.extension.ts` file's `id` field |
| Forgetting to register in `extensions.ts` | Import and `.use()` the modal |
| Using `extensionId` instead of `modalId` | Use `modalId` in `openModal()` |
| Can't access params in modal | Use `dashboard.observeState()` to read passed data |
| Modal won't close | Use `dashboard.closeModal()` from `@wix/dashboard` |

## Real-World Example

```typescript
// Dashboard Page: Opening edit modal
const handleEdit = async (item: Item) => {
  dashboard.openModal({
    modalId: "edit-item-modal-guid",
    params: {
      itemId: item._id,
      item: item, // Objects passed directly via params
    },
  });
};

// Modal: Receiving and saving data
export default function ItemEditModal() {
  const [formData, setFormData] = useState<Item | null>(null);

  useEffect(() => {
    dashboard.observeState((state) => {
      if (state.item) {
        setFormData(state.item);
      }
    });
  }, []);

  const handleSave = async () => {
    // Save logic
    dashboard.showToast({ message: "Saved!", type: "success" });
    dashboard.closeModal();
  };

  return (
    <CustomModalLayout
      title="Edit Item"
      primaryButtonText="Save"
      onCloseButtonClick={() => dashboard.closeModal()}
      primaryButtonOnClick={handleSave}
      content={/* form fields */}
    />
  );
}
```

## Verification

After implementation, use [wix-cli-app-validation](../wix-cli-app-validation/SKILL.md) to validate TypeScript compilation, build, preview, and runtime behavior.
