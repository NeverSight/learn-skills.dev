---
name: chrome-extension-wxt
description: Build Chrome extensions using WXT framework with TypeScript, React, Vue, or Svelte. Use when creating browser extensions, developing cross-browser add-ons, or working with Chrome Web Store projects. Triggers on phrases like "chrome extension", "browser extension", "WXT framework", "manifest v3", or file patterns like wxt.config.ts.
---

# Chrome Extension Development with WXT

Build modern, cross-browser extensions using WXT - the next-generation framework that supports Chrome, Firefox, Edge, Safari, and all Chromium browsers with a single codebase.

## When to Use This Skill

Use this skill when:
- Creating a new Chrome/browser extension
- Setting up WXT development environment
- Building extension features (popup, content scripts, background scripts)
- Implementing cross-browser compatibility
- Working with Manifest V3 (mandatory standard as of 2025, V2 deprecated)
- Integrating React 19, Vue, Svelte, or Solid with extensions

## Quick Start Workflow

### 1. Initialize WXT Project

```bash
# Create new project with framework of choice
npm create wxt@latest

# Or with specific template
npm create wxt@latest -- --template react-ts
npm create wxt@latest -- --template vue-ts
npm create wxt@latest -- --template svelte-ts
```

### 2. Project Structure

WXT uses file-based conventions:

```
project/
├── entrypoints/              # Auto-discovered entry points
│   ├── background.ts         # Service worker
│   ├── content.ts           # Content script
│   ├── popup.html           # Popup UI
│   └── options.html         # Options page
├── components/              # Auto-imported UI components
├── utils/                   # Auto-imported utilities
├── public/                  # Static assets
│   └── icon/               # Extension icons
├── wxt.config.ts           # Configuration
└── package.json
```

### 3. Development Commands

```bash
npm run dev              # Start dev server with HMR
npm run build           # Production build
npm run zip             # Package for store submission
```

## Core Entry Points

WXT recognizes entry points by filename in `entrypoints/` directory:

### Background Script (Service Worker)

```typescript
// entrypoints/background.ts
export default defineBackground({
  type: 'module',
  persistent: false,

  main() {
    // Listen for extension events
    browser.action.onClicked.addListener((tab) => {
      console.log('Extension clicked', tab);
    });

    // Handle messages
    browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
      // Handle message
      sendResponse({ success: true });
      return true; // Keep channel open for async
    });
  },
});
```

### Content Script

```typescript
// entrypoints/content.ts
export default defineContentScript({
  matches: ['*://*.example.com/*'],
  runAt: 'document_end',

  main(ctx) {
    // Content script logic
    console.log('Content script loaded');

    // Create UI
    const ui = createShadowRootUi(ctx, {
      name: 'my-extension-ui',
      position: 'inline',
      anchor: 'body',

      onMount(container) {
        // Mount React/Vue component
        const root = ReactDOM.createRoot(container);
        root.render(<App />);
      },
    });

    ui.mount();
  },
});
```

### Popup UI

```typescript
// entrypoints/popup/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

```html
<!-- entrypoints/popup/index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Extension Popup</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="./main.tsx"></script>
</body>
</html>
```

## Configuration

### Basic wxt.config.ts

```typescript
import { defineConfig } from 'wxt';

export default defineConfig({
  // Framework integration
  modules: ['@wxt-dev/module-react'],

  // Manifest configuration
  manifest: {
    name: 'My Extension',
    description: 'Extension description',
    permissions: ['storage', 'activeTab'],
    host_permissions: ['*://example.com/*'],
  },

  // Browser target
  browser: 'chrome', // or 'firefox', 'edge', 'safari'
});
```

## Common Patterns

### Type-Safe Storage

```typescript
// utils/storage.ts
import { storage } from 'wxt/storage';

export const storageHelper = {
  async get<T>(key: string): Promise<T | null> {
    return await storage.getItem<T>(`local:${key}`);
  },

  async set<T>(key: string, value: T): Promise<void> {
    await storage.setItem(`local:${key}`, value);
  },

  watch<T>(key: string, callback: (newValue: T | null) => void) {
    return storage.watch<T>(`local:${key}`, callback);
  },
};
```

### Type-Safe Messaging

```typescript
// utils/messaging.ts
interface Messages {
  'get-data': {
    request: { key: string };
    response: { value: any };
  };
}

export async function sendMessage<K extends keyof Messages>(
  type: K,
  payload: Messages[K]['request']
): Promise<Messages[K]['response']> {
  return await browser.runtime.sendMessage({ type, payload });
}
```

### Script Injection

```typescript
// Inject script into page context
import { injectScript } from 'wxt/client';

await injectScript('/injected.js', {
  keepInDom: false,
});
```

## Building & Deployment

### Production Build

```bash
# Build for specific browser
npm run build -- --browser=chrome
npm run build -- --browser=firefox

# Create store-ready ZIP
npm run zip
npm run zip -- --browser=firefox
```

### Multi-Browser Build

```bash
# Build for all browsers
npm run zip:all
```

Output: `.output/my-extension-{version}-{browser}.zip`

## Modern Stacks (2025)

Popular technology combinations for building Chrome extensions:

### WXT + React + Tailwind + shadcn/ui
Most popular stack in 2025. Combines utility-first styling with pre-built accessible components.

```bash
npm create wxt@latest -- --template react-ts
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npx shadcn@latest init
```

**Best for:** Modern UIs with consistent design system
**Example:** https://github.com/imtiger/wxt-react-shadcn-tailwindcss-chrome-extension

### WXT + React + Mantine UI
Complete component library with 100+ components and built-in dark mode.

```bash
npm create wxt@latest -- --template react-ts
npm install @mantine/core @mantine/hooks
```

**Best for:** Feature-rich extensions needing complex components
**Example:** https://github.com/ongkay/WXT-Mantine-Tailwind-Browser-Extension

### WXT + React + TypeScript (Minimal)
Clean setup for custom designs without UI library dependencies.

```bash
npm create wxt@latest -- --template react-ts
```

**Best for:** Simple extensions or highly custom designs

## Advanced Topics

For detailed information on advanced topics, see the reference files:

- **React Integration**: See `references/react-integration.md` for complete React setup, hooks, state management, and popular UI libraries
- **Chrome APIs**: See `references/chrome-api.md` for comprehensive Chrome Extension API reference with examples
- **Chrome 140+ Features**: See `references/chrome-140-features.md` for latest Chrome Extension APIs (sidePanel.getLayout(), etc.)
- **WXT API**: See `references/wxt-api.md` for complete WXT framework API documentation
- **Best Practices**: See `references/best-practices.md` for security, performance, and architecture patterns

## Troubleshooting

Common issues and solutions:

1. **Module not found errors**: Ensure modules are installed and properly imported
2. **CSP violations**: Update `content_security_policy` in manifest
3. **Hot reload not working**: Check browser console for errors
4. **Storage not persisting**: Use `storage.local` or `storage.sync` correctly

For detailed troubleshooting, see `references/troubleshooting.md`

## Resources

### Official Documentation
- WXT Docs: https://wxt.dev
- Chrome Extension Docs: https://developer.chrome.com/docs/extensions
- Firefox Extension Docs: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons

### Bundled Resources

- **scripts/**: Helper utilities for common extension tasks
- **references/**: Detailed documentation for advanced features
- **assets/**: Starter templates and example components

Use these resources as needed when building your extension.
