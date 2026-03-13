---
name: telegram-mini-app-skill
description: Comprehensive guide for developing Telegram Mini Apps with any web framework (React, Vue, Svelte, vanilla JS, etc.). Covers the Telegram Web App SDK, theming, UI components, navigation, data validation, and platform best practices.
---

# Telegram Mini App Development Guide

> **Official Reference**: [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)

This skill is a **framework-agnostic** guide for building Telegram Mini Apps. Whether you use React, Vue, Svelte, Angular, Solid, or vanilla HTML/JS — this guide covers the universal SDK concepts, theming system, and best practices.

---

## Table of Contents

1. [What is a Telegram Mini App?](#1-what-is-a-telegram-mini-app)
2. [Loading the SDK](#2-loading-the-sdk)
3. [The WebApp Object](#3-the-webapp-object)
4. [Initialization Lifecycle](#4-initialization-lifecycle)
5. [Theming & CSS Variables](#5-theming--css-variables)
6. [Navigation Components](#6-navigation-components)
7. [Bottom Buttons (MainButton & SecondaryButton)](#7-bottom-buttons)
8. [Haptic Feedback](#8-haptic-feedback)
9. [Popups & Alerts](#9-popups--alerts)
10. [Data Validation & Security](#10-data-validation--security)
11. [Storage APIs](#11-storage-apis)
12. [Full-Screen Mode](#12-full-screen-mode)
13. [Safe Areas](#13-safe-areas)
14. [Available Events](#14-available-events)
15. [Framework Integration Recipes](#15-framework-integration-recipes)
16. [Design Guidelines](#16-design-guidelines)
17. [Testing & Debugging](#17-testing--debugging)
18. [Common Pitfalls](#18-common-pitfalls)

---

## 1. What is a Telegram Mini App?

Telegram Mini Apps are **web applications** (HTML, CSS, JavaScript) that run inside the Telegram messenger. They can be launched from:

- **Bot menus** — via BotFather's menu button configuration
- **Inline buttons** — `web_app` type in bot messages
- **Attachment menu** — bot added to the attachment menu
- **Direct links** — `t.me/botname/appname`
- **Keyboard buttons** — `web_app` type keyboard buttons
- **Home screen shortcuts** — users can add Mini Apps to their home screen

**Key characteristics:**

- Must be served over **HTTPS**
- Run in a WebView on all platforms (iOS, Android, Desktop, Web)
- Can access Telegram user data, theme, and native UI components
- Associated with a bot created via [@BotFather](https://t.me/BotFather)

---

## 2. Loading the SDK

### Option A: Script Tag (All Frameworks)

Place this in your `<head>` **before any other scripts**:

```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

This creates the `window.Telegram.WebApp` object and automatically injects CSS variables for theming.

### Option B: npm Packages

For modern JavaScript projects with bundlers:

```bash
# Official community SDK (TypeScript-first, tree-shakeable)
npm install @telegram-apps/sdk

# Alternative lightweight wrapper
npm install @twa-dev/sdk
```

### Framework-Specific Loading

| Framework              | How to Load                                                                                          |
| :--------------------- | :--------------------------------------------------------------------------------------------------- |
| **Vanilla HTML**       | `<script>` tag in `<head>`                                                                           |
| **React / Next.js**    | `<Script src="..." strategy="beforeInteractive" />` via `next/script`, or `<script>` in `index.html` |
| **Vue / Nuxt**         | `<script>` in `index.html`, or Nuxt plugin with `useHead()`                                          |
| **Svelte / SvelteKit** | `<svelte:head>` tag or `app.html`                                                                    |
| **Angular**            | Add to `angular.json` `scripts` array or `index.html`                                                |

---

## 3. The WebApp Object

Once the SDK is loaded, the main API is available at:

```javascript
const tg = window.Telegram.WebApp;
```

### Key Properties

| Property               | Type      | Description                                                                       |
| :--------------------- | :-------- | :-------------------------------------------------------------------------------- |
| `initData`             | `string`  | Raw init data string for backend validation                                       |
| `initDataUnsafe`       | `object`  | Parsed init data (user, chat, etc.) — **not validated, do not trust client-side** |
| `version`              | `string`  | SDK version (e.g., `"8.0"`)                                                       |
| `platform`             | `string`  | Platform identifier (`"android"`, `"ios"`, `"tdesktop"`, `"web"`, `"unknown"`)    |
| `colorScheme`          | `string`  | `"light"` or `"dark"`                                                             |
| `themeParams`          | `object`  | Current theme colors as key-value pairs                                           |
| `isExpanded`           | `boolean` | Whether the Mini App is expanded to full height                                   |
| `viewportHeight`       | `number`  | Current viewport height in pixels                                                 |
| `viewportStableHeight` | `number`  | Stable viewport height (doesn't change with keyboard)                             |
| `headerColor`          | `string`  | Current header color (`#RRGGBB`)                                                  |
| `backgroundColor`      | `string`  | Current background color (`#RRGGBB`)                                              |
| `bottomBarColor`       | `string`  | Current bottom bar color (`#RRGGBB`)                                              |
| `isFullscreen`         | `boolean` | Whether full-screen mode is active                                                |

### Key Sub-Objects

| Sub-Object          | Description                                                       |
| :------------------ | :---------------------------------------------------------------- |
| `BackButton`        | Controls the back button in the header                            |
| `MainButton`        | Controls the primary bottom button                                |
| `SecondaryButton`   | Controls the secondary bottom button                              |
| `SettingsButton`    | Controls the settings item in the context menu                    |
| `HapticFeedback`    | Controls haptic/vibration feedback                                |
| `CloudStorage`      | Cloud key-value storage (up to 1024 items, synced across devices) |
| `DeviceStorage`     | Persistent local storage (up to 5 MB, device-only)                |
| `SecureStorage`     | Encrypted storage using OS keychain/keystore (up to 10 items)     |
| `BiometricManager`  | Biometric authentication                                          |
| `Accelerometer`     | Accelerometer sensor data                                         |
| `Gyroscope`         | Gyroscope sensor data                                             |
| `DeviceOrientation` | Device orientation data                                           |
| `LocationManager`   | Location access                                                   |

---

## 4. Initialization Lifecycle

Every Mini App must call `tg.ready()` to signal to Telegram that the app is ready to be displayed.

### Universal Pattern (Any Framework)

```javascript
// 1. Get the WebApp instance
const tg = window.Telegram.WebApp;

// 2. Signal ready
tg.ready();

// 3. Expand to full height (recommended)
tg.expand();

// 4. Access user data
const user = tg.initDataUnsafe?.user;
console.log(user?.first_name, user?.username);
```

### Why `ready()` Matters

- Telegram shows a loading placeholder until `ready()` is called
- Call it as early as possible after your app's initial UI has rendered
- Don't call it before your app has something meaningful to display

---

## 5. Theming & CSS Variables

### The Golden Rule

> **NEVER hardcode colors**. Use the CSS variables that Telegram's SDK injects automatically. This ensures your app looks native in **Light mode**, **Dark mode**, and across all platforms.

### Available CSS Variables

The SDK automatically sets these CSS variables on the `<html>` element:

| CSS Variable                           | JS Property (`themeParams.X`) | Description                            |
| :------------------------------------- | :---------------------------- | :------------------------------------- |
| `--tg-theme-bg-color`                  | `bg_color`                    | Main background                        |
| `--tg-theme-text-color`                | `text_color`                  | Primary text                           |
| `--tg-theme-hint-color`                | `hint_color`                  | Secondary/hint text                    |
| `--tg-theme-link-color`                | `link_color`                  | Links                                  |
| `--tg-theme-button-color`              | `button_color`                | Primary button background              |
| `--tg-theme-button-text-color`         | `button_text_color`           | Button text                            |
| `--tg-theme-secondary-bg-color`        | `secondary_bg_color`          | Secondary background (cards, sections) |
| `--tg-theme-header-bg-color`           | `header_bg_color`             | Header background                      |
| `--tg-theme-bottom-bar-bg-color`       | `bottom_bar_bg_color`         | Bottom bar background                  |
| `--tg-theme-accent-text-color`         | `accent_text_color`           | Accent text                            |
| `--tg-theme-section-bg-color`          | `section_bg_color`            | Section/card background                |
| `--tg-theme-section-header-text-color` | `section_header_text_color`   | Section header text                    |
| `--tg-theme-section-separator-color`   | `section_separator_color`     | Separator lines                        |
| `--tg-theme-subtitle-text-color`       | `subtitle_text_color`         | Subtitle text                          |
| `--tg-theme-destructive-text-color`    | `destructive_text_color`      | Destructive/danger text                |

### Additional CSS Variables

| CSS Variable                          | Description                    |
| :------------------------------------ | :----------------------------- |
| `--tg-color-scheme`                   | `"light"` or `"dark"`          |
| `--tg-viewport-height`                | Current viewport height        |
| `--tg-viewport-stable-height`         | Stable viewport height         |
| `--tg-safe-area-inset-top`            | System safe area (top)         |
| `--tg-safe-area-inset-bottom`         | System safe area (bottom)      |
| `--tg-safe-area-inset-left`           | System safe area (left)        |
| `--tg-safe-area-inset-right`          | System safe area (right)       |
| `--tg-content-safe-area-inset-top`    | Telegram UI safe area (top)    |
| `--tg-content-safe-area-inset-bottom` | Telegram UI safe area (bottom) |
| `--tg-content-safe-area-inset-left`   | Telegram UI safe area (left)   |
| `--tg-content-safe-area-inset-right`  | Telegram UI safe area (right)  |

### Usage Examples

#### ✅ CORRECT — Using CSS Variables

```css
/* CSS */
body {
  background-color: var(--tg-theme-bg-color, #ffffff);
  color: var(--tg-theme-text-color, #000000);
}

.card {
  background-color: var(--tg-theme-section-bg-color, #f5f5f5);
  border: 1px solid var(--tg-theme-section-separator-color, #e0e0e0);
}

.button-primary {
  background-color: var(--tg-theme-button-color, #3b82f6);
  color: var(--tg-theme-button-text-color, #ffffff);
}

.hint-text {
  color: var(--tg-theme-hint-color, #999999);
}
```

> **Always provide fallback values** (the second argument in `var()`) so your app works outside of Telegram during development.

#### ❌ WRONG — Hardcoded Colors

```css
/* NEVER do this */
body {
  background-color: #ffffff;
  color: #000000;
}
.dark body {
  background-color: #1a1a1a;
  color: #ffffff;
}
```

### Creating a Shorthand Variable System (Recommended)

For convenience, map Telegram's verbose variables to shorter names in your global CSS:

```css
:root {
  --bg: var(--tg-theme-bg-color, #ffffff);
  --fg: var(--tg-theme-text-color, #171717);
  --btn: var(--tg-theme-button-color, #3b82f6);
  --btn-text: var(--tg-theme-button-text-color, #ffffff);
  --hint: var(--tg-theme-hint-color, #a1a1aa);
  --link: var(--tg-theme-link-color, #007aff);
  --secondary-bg: var(--tg-theme-secondary-bg-color, #efeff4);
  --section-bg: var(--tg-theme-section-bg-color, #ffffff);
  --section-header: var(--tg-theme-section-header-text-color, #6d6d72);
  --subtitle: var(--tg-theme-subtitle-text-color, #8e8e93);
  --destructive: var(--tg-theme-destructive-text-color, #ff3b30);
  --accent: var(--tg-theme-accent-text-color, #007aff);
  --separator: var(--tg-theme-section-separator-color, #c8c7cc);
}
```

### Listening to Theme Changes

```javascript
tg.onEvent("themeChanged", () => {
  // Theme params have been updated
  // CSS variables are auto-updated by the SDK
  // If using JS theming, re-read tg.themeParams
  console.log("New color scheme:", tg.colorScheme);
});
```

---

## 6. Navigation Components

### BackButton

Controls the native back button in the Telegram header. Use this instead of building your own back button.

```javascript
// Show the back button
tg.BackButton.show();

// Handle clicks
tg.BackButton.onClick(() => {
  // Navigate back in your app's routing
  history.back(); // or your router's back method
});

// Hide when no longer needed
tg.BackButton.hide();

// Remove a specific handler
tg.BackButton.offClick(handler);
```

### SettingsButton

Adds a "Settings" option to the Mini App's context menu (three-dot menu).

```javascript
tg.SettingsButton.show();
tg.SettingsButton.onClick(() => {
  // Navigate to settings page
});
```

---

## 7. Bottom Buttons

Telegram provides **two bottom buttons**: `MainButton` (primary) and `SecondaryButton` (secondary). They appear fixed at the bottom of the Mini App.

### MainButton

```javascript
const btn = tg.MainButton;

// Configure and show
btn.setText("SUBMIT ORDER");
btn.show();

// Or use setParams for multiple properties at once
btn.setParams({
  text: "SUBMIT ORDER",
  color: tg.themeParams.button_color,
  text_color: tg.themeParams.button_text_color,
  is_active: true,
  is_visible: true,
  has_shine_effect: false,
});

// Handle click
btn.onClick(() => {
  // Perform the action
});

// Show loading state
btn.showProgress(true); // true = leave button active
btn.disable(); // prevent double-clicks

// Reset after completion
btn.hideProgress();
btn.enable();
btn.hide();
```

### SecondaryButton

Works identically to `MainButton`:

```javascript
tg.SecondaryButton.setParams({
  text: "CANCEL",
  is_visible: true,
});

tg.SecondaryButton.onClick(() => {
  // Handle secondary action
});
```

### BottomButton Properties

| Property / Method            | Description                          |
| :--------------------------- | :----------------------------------- |
| `.text`                      | Button text                          |
| `.color`                     | Background color                     |
| `.textColor`                 | Text color                           |
| `.isVisible`                 | Whether the button is shown          |
| `.isActive`                  | Whether the button is clickable      |
| `.isProgressVisible`         | Whether the loading spinner is shown |
| `.setText(text)`             | Update button text                   |
| `.show()` / `.hide()`        | Toggle visibility                    |
| `.enable()` / `.disable()`   | Toggle clickability                  |
| `.showProgress(leaveActive)` | Show spinner                         |
| `.hideProgress()`            | Hide spinner                         |
| `.setParams(params)`         | Set multiple properties at once      |
| `.onClick(cb)`               | Register click handler               |
| `.offClick(cb)`              | Remove click handler                 |

### Important: Handler Cleanup

Always remove click handlers when they're no longer relevant (e.g., on component unmount or page navigation). Failure to do so can cause ghost handlers.

---

## 8. Haptic Feedback

Trigger native haptic vibrations for tactile feedback:

```javascript
const haptic = tg.HapticFeedback;

// Impact feedback — for button presses, interactions
haptic.impactOccurred("light"); // light tap
haptic.impactOccurred("medium"); // medium tap
haptic.impactOccurred("heavy"); // strong tap
haptic.impactOccurred("rigid"); // rigid tap
haptic.impactOccurred("soft"); // soft tap

// Notification feedback — for results/outcomes
haptic.notificationOccurred("success"); // operation succeeded
haptic.notificationOccurred("error"); // operation failed
haptic.notificationOccurred("warning"); // caution

// Selection feedback — for selection changes
haptic.selectionChanged(); // e.g., picker/slider changes
```

### When to Use

| Scenario                   | Type                              |
| :------------------------- | :-------------------------------- |
| Button tap                 | `impactOccurred("light")`         |
| Form submit success        | `notificationOccurred("success")` |
| Error response             | `notificationOccurred("error")`   |
| Toggling a switch          | `impactOccurred("medium")`        |
| Slider/picker value change | `selectionChanged()`              |
| Deleting an item           | `impactOccurred("heavy")`         |
| Clear/reset action         | `impactOccurred("light")`         |

---

## 9. Popups & Alerts

Use native Telegram dialogs instead of browser `alert()` / `confirm()`:

```javascript
// Simple alert
tg.showAlert("File saved successfully!", () => {
  // Callback after user dismisses
});

// Confirmation dialog
tg.showConfirm("Are you sure you want to delete this?", (confirmed) => {
  if (confirmed) {
    // User tapped "OK"
  }
});

// Custom popup with buttons
tg.showPopup(
  {
    title: "Choose an option", // optional
    message: "What would you like to do?",
    buttons: [
      { id: "save", type: "default", text: "Save" },
      { id: "delete", type: "destructive", text: "Delete" },
      { id: "cancel", type: "cancel" }, // text is auto-set
    ],
  },
  (buttonId) => {
    switch (buttonId) {
      case "save":
        /* ... */ break;
      case "delete":
        /* ... */ break;
      case "cancel":
        /* ... */ break;
    }
  },
);
```

### Popup Button Types

| Type            | Behavior                      |
| :-------------- | :---------------------------- |
| `"default"`     | Regular button                |
| `"ok"`          | "OK" text, closes popup       |
| `"close"`       | "Close" text, closes popup    |
| `"cancel"`      | "Cancel" text, closes popup   |
| `"destructive"` | Red/destructive styled button |

---

## 10. Data Validation & Security

### Client-Side Data

`tg.initDataUnsafe` gives you parsed user data, but it can be spoofed. **Always validate on your backend.**

```javascript
// Client: send initData to your backend
const response = await fetch("/api/your-endpoint", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-Telegram-Init-Data": tg.initData, // raw string for validation
  },
  body: JSON.stringify({
    /* your payload */
  }),
});
```

### Server-Side Validation (HMAC-SHA256)

The backend must validate `initData` using the bot's token:

```
1. Parse initData as query string
2. Extract `hash` parameter, keep remaining fields
3. Sort remaining fields alphabetically
4. Create data_check_string = sorted fields joined with '\n' in "key=value" format
5. secret_key = HMAC_SHA256(bot_token, "WebAppData")
6. Compare: HMAC_SHA256(data_check_string, secret_key) == hash
7. Check auth_date for freshness
```

**Pseudocode:**

```
data_check_string = "auth_date=<auth_date>\nquery_id=<query_id>\nuser=<user>"
secret_key = HMAC_SHA256(<bot_token>, "WebAppData")
if hex(HMAC_SHA256(data_check_string, secret_key)) == hash:
    # Data is genuine and from Telegram
```

### Third-Party Validation (Ed25519 Signatures)

For sharing data with third parties (who don't have your bot token), use the `signature` field with Telegram's public keys:

- **Production**: `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d`
- **Test env**: `40055058a4ee38156a06562e52eece92a771bcd8346a8c4615cb7376eddf72ec`

---

## 11. Storage APIs

### CloudStorage (Synced Across Devices)

Up to 1024 key-value pairs, 4096 bytes per value, synced via Telegram's servers:

```javascript
tg.CloudStorage.setItem("theme_pref", "dark", (err, success) => {});
tg.CloudStorage.getItem("theme_pref", (err, value) => {});
tg.CloudStorage.getItems(["key1", "key2"], (err, values) => {});
tg.CloudStorage.removeItem("theme_pref", (err, success) => {});
tg.CloudStorage.getKeys((err, keys) => {});
```

### DeviceStorage (Local Only, Bot API 9.0+)

Up to 5 MB, persists on device, similar to `localStorage`:

```javascript
tg.DeviceStorage.setItem("draft", longText);
tg.DeviceStorage.getItem("draft");
```

### SecureStorage (Encrypted, Bot API 9.0+)

Up to 10 items, uses OS Keychain (iOS) / Keystore (Android):

```javascript
tg.SecureStorage.setItem("auth_token", token);
tg.SecureStorage.getItem("auth_token");
```

---

## 12. Full-Screen Mode

Available since Bot API 8.0 (November 2024). Allows the Mini App to use the entire screen:

```javascript
// Enter full-screen
tg.requestFullscreen();

// Exit full-screen
tg.exitFullscreen();

// Check status
console.log(tg.isFullscreen);

// Listen for changes
tg.onEvent("fullscreenChanged", () => {
  console.log("Fullscreen:", tg.isFullscreen);
});

tg.onEvent("fullscreenFailed", (event) => {
  console.log("Fullscreen failed:", event.error);
});
```

> **Important**: When in full-screen mode, you **must** handle safe areas to avoid content overlapping with system UI elements (notch, status bar, etc.).

---

## 13. Safe Areas

Two types of safe areas to handle, especially critical in full-screen mode:

### System Safe Area (notch, status bar, home indicator)

```css
.content {
  padding-top: var(--tg-safe-area-inset-top, 0px);
  padding-bottom: var(--tg-safe-area-inset-bottom, 0px);
  padding-left: var(--tg-safe-area-inset-left, 0px);
  padding-right: var(--tg-safe-area-inset-right, 0px);
}
```

### Content Safe Area (Telegram's own header, bottom bar)

It is highly recommended in frameworks like React/Next.js to avoid applying these to the raw document `body`, as Telegram's Webview injection can cause `100vw` or scaling constraints to clip or shrink off-screen horizontally.

Instead, the most bulletproof approach across all Webview versions involves a hybrid Javascript-to-CSS fallback. Combining `contentSafeAreaInset.top` (Telegram UI) and `safeAreaInset.top` (Mobile Device Notches) prevents overlap completely:

**1. Calculate and combine the padding natively in your Telegram Initialization loop:**

```javascript
// Add base safeArea (device notches) + contentSafe (Telegram header ui) together
// Apply a hard fallback (e.g., 48px) just in case Telegram fails to inject variables entirely
const top = Math.max(
  48,
  (tg.contentSafeAreaInset?.top || 0) + (tg.safeAreaInset?.top || 0),
);
const bottom = Math.max(
  32,
  (tg.contentSafeAreaInset?.bottom || 0) + (tg.safeAreaInset?.bottom || 0),
);

// Explicitly inject safe bounds into your root HTML variables
document.documentElement.style.setProperty("--safe-top", `${top}px`);
document.documentElement.style.setProperty("--safe-bottom", `${bottom}px`);
```

**2. In your CSS (like `globals.css` or Tailwind config), reference the injected variables:**

```css
:root {
  /* You can optionally add env() fallbacks here if you want native browser backup */
  --safe-top: env(safe-area-inset-top, 48px);
  --safe-bottom: env(safe-area-inset-bottom, 32px);
}
```

**3. Finally, in your React individual Page wrappers padding:**

```tsx
<main
  style={{
    // Add your desired extra padding (e.g., 1rem) to the base safe area boundary mathematically
    paddingTop: "calc(1rem + var(--safe-top))",
    paddingBottom: "calc(2rem + var(--safe-bottom))",
  }}
>
  {/* Content goes here safely below the Close/Settings notch */}
</main>
```

### Listening for Safe Area Changes

```javascript
tg.onEvent("safeAreaChanged", () => {
  // System safe area changed (e.g., orientation change)
});

tg.onEvent("contentSafeAreaChanged", () => {
  // Telegram UI safe area changed
});
```

---

## 14. Available Events

Register handlers with `tg.onEvent(eventType, handler)` and remove with `tg.offEvent(eventType, handler)`:

| Event                     | Trigger                                    |
| :------------------------ | :----------------------------------------- |
| `activated`               | Mini App becomes active/visible            |
| `deactivated`             | Mini App becomes inactive/hidden           |
| `themeChanged`            | User changed Telegram theme                |
| `viewportChanged`         | Viewport height changed (keyboard, expand) |
| `safeAreaChanged`         | System safe area insets changed            |
| `contentSafeAreaChanged`  | Telegram content safe area changed         |
| `mainButtonClicked`       | Main button was pressed                    |
| `secondaryButtonClicked`  | Secondary button was pressed               |
| `backButtonClicked`       | Back button was pressed                    |
| `settingsButtonClicked`   | Settings button was pressed                |
| `invoiceClosed`           | Payment invoice was closed                 |
| `popupClosed`             | Popup was closed                           |
| `qrTextReceived`          | QR code was scanned                        |
| `clipboardTextReceived`   | Clipboard text was received                |
| `writeAccessRequested`    | Write access permission result             |
| `contactRequested`        | Contact sharing result                     |
| `fullscreenChanged`       | Full-screen state changed                  |
| `fullscreenFailed`        | Full-screen request failed                 |
| `homeScreenAdded`         | App was added to home screen               |
| `homeScreenChecked`       | Home screen status checked                 |
| `biometricManagerUpdated` | Biometric manager state changed            |
| `biometricAuthRequested`  | Biometric auth result                      |
| `shareMessageSent`        | Share message was sent                     |
| `shareMessageFailed`      | Share message failed                       |
| `emojiStatusSet`          | Emoji status was set                       |
| `emojiStatusFailed`       | Emoji status setting failed                |
| `fileDownloadRequested`   | File download request result               |

---

## 15. Framework Integration Recipes

### Vanilla JavaScript

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
      body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--tg-theme-bg-color, #fff);
        color: var(--tg-theme-text-color, #000);
      }
      .card {
        background: var(--tg-theme-section-bg-color, #f5f5f5);
        border-radius: 14px;
        padding: 16px;
        margin: 16px;
      }
      .hint {
        color: var(--tg-theme-hint-color, #999);
        font-size: 13px;
      }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>Hello, <span id="username">User</span>!</h1>
      <p class="hint">Welcome to the Mini App</p>
    </div>
    <script>
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.expand();

      const user = tg.initDataUnsafe?.user;
      if (user) {
        document.getElementById("username").textContent = user.first_name;
      }

      tg.MainButton.setText("DONE");
      tg.MainButton.show();
      tg.MainButton.onClick(() => {
        tg.HapticFeedback.notificationOccurred("success");
        tg.close();
      });
    </script>
  </body>
</html>
```

---

### React / Next.js

```tsx
// hooks/useTelegram.ts — Reusable hook
import { useEffect, useState, useCallback } from "react";

export function useTelegram() {
  const [tg, setTg] = useState<TelegramWebApp | null>(null);
  const [user, setUser] = useState<TelegramUser | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && window.Telegram?.WebApp) {
      const webapp = window.Telegram.WebApp;
      webapp.ready();
      webapp.expand();
      setTg(webapp);
      setUser(webapp.initDataUnsafe?.user || null);
    }
  }, []);

  const showMainButton = useCallback(
    (text: string, onClick: () => void) => {
      if (!tg) return;
      tg.MainButton.setText(text);
      tg.MainButton.show();
      tg.MainButton.onClick(onClick);
      return () => tg.MainButton.offClick(onClick);
    },
    [tg],
  );

  const showBackButton = useCallback(
    (onClick: () => void) => {
      if (!tg) return;
      tg.BackButton.show();
      tg.BackButton.onClick(onClick);
      return () => {
        tg.BackButton.offClick(onClick);
        tg.BackButton.hide();
      };
    },
    [tg],
  );

  return { tg, user, showMainButton, showBackButton };
}
```

```tsx
// pages/MyPage.tsx
"use client";
import { useEffect } from "react";
import { useTelegram } from "@/hooks/useTelegram";

export default function MyPage() {
  const { tg, user, showBackButton } = useTelegram();

  useEffect(() => {
    return showBackButton?.(() => window.history.back());
  }, [showBackButton]);

  return (
    <main style={{ background: "var(--tg-theme-secondary-bg-color)" }}>
      <h1 style={{ color: "var(--tg-theme-text-color)" }}>
        Hello, {user?.first_name}!
      </h1>
    </main>
  );
}
```

#### Next.js Layout Setup

```tsx
// app/layout.tsx
import Script from "next/script";

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Script
          src="https://telegram.org/js/telegram-web-app.js"
          strategy="beforeInteractive"
        />
        {children}
      </body>
    </html>
  );
}
```

> **`suppressHydrationWarning`** is required because Telegram's script injects style attributes into the DOM during SSR/hydration.

---

### Vue 3 / Nuxt

```vue
<!-- composables/useTelegram.ts -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const tg = ref<any>(null);
const user = ref<any>(null);

export function useTelegram() {
  onMounted(() => {
    if (window.Telegram?.WebApp) {
      tg.value = window.Telegram.WebApp;
      tg.value.ready();
      tg.value.expand();
      user.value = tg.value.initDataUnsafe?.user || null;
    }
  });

  function showBackButton(onClick: () => void) {
    tg.value?.BackButton.show();
    tg.value?.BackButton.onClick(onClick);
    onUnmounted(() => {
      tg.value?.BackButton.offClick(onClick);
      tg.value?.BackButton.hide();
    });
  }

  return { tg, user, showBackButton };
}
</script>
```

```vue
<!-- pages/MyPage.vue -->
<template>
  <main :style="{ background: 'var(--tg-theme-secondary-bg-color)' }">
    <h1 :style="{ color: 'var(--tg-theme-text-color)' }">
      Hello, {{ user?.first_name }}!
    </h1>
  </main>
</template>

<script setup lang="ts">
import { useTelegram } from "@/composables/useTelegram";
import { useRouter } from "vue-router";

const { user, showBackButton } = useTelegram();
const router = useRouter();

showBackButton(() => router.back());
</script>
```

---

### Svelte / SvelteKit

```svelte
<!-- lib/telegram.ts -->
<script context="module" lang="ts">
  export function getTelegram() {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      return window.Telegram.WebApp;
    }
    return null;
  }
</script>
```

```svelte
<!-- routes/+page.svelte -->
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { getTelegram } from '$lib/telegram';

  let user: any = null;

  onMount(() => {
    const tg = getTelegram();
    if (tg) {
      tg.ready();
      tg.expand();
      user = tg.initDataUnsafe?.user;

      tg.BackButton.show();
      tg.BackButton.onClick(() => history.back());
    }
  });

  onDestroy(() => {
    const tg = getTelegram();
    tg?.BackButton.hide();
  });
</script>

<main style="background: var(--tg-theme-secondary-bg-color); color: var(--tg-theme-text-color);">
  <h1>Hello, {user?.first_name ?? 'User'}!</h1>
</main>
```

#### SvelteKit Layout

```html
<!-- src/app.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    %sveltekit.head%
  </head>
  <body>
    %sveltekit.body%
  </body>
</html>
```

---

## 16. Design Guidelines

Telegram's official design principles for Mini Apps:

### Core Principles

1. **Mobile-First**: All elements must be responsive and optimized for mobile viewports
2. **Native Feel**: Mimic the style and behavior of existing Telegram UI components
3. **Smooth Animations**: Target 60fps for all animations
4. **Accessibility**: All inputs and images should have labels
5. **Theme Adaptive**: Use Telegram CSS variables for all colors
6. **Safe Area Aware**: Respect safe areas, especially in full-screen mode
7. **Performance Conscious**: On Android, check User-Agent for device performance class and reduce animations on low-end devices

### Recommended UI Patterns

| Element             | Recommended Style                                                                   |
| :------------------ | :---------------------------------------------------------------------------------- |
| Page background     | `var(--tg-theme-secondary-bg-color)`                                                |
| Cards / Sections    | `var(--tg-theme-section-bg-color)` with `border-radius: 14px`                       |
| Section labels      | Uppercase, small font, `var(--tg-theme-section-header-text-color)`                  |
| Hint text           | Smaller font, `var(--tg-theme-hint-color)`                                          |
| Separators          | 1px line with `var(--tg-theme-section-separator-color)`                             |
| Input font size     | ≥ 16px (prevents iOS auto-zoom on focus)                                            |
| Button              | Use `MainButton` for primary actions, or custom with `var(--tg-theme-button-color)` |
| Destructive actions | `var(--tg-theme-destructive-text-color)`                                            |
| Bottom padding      | Add enough padding to avoid overlap with MainButton (~80px)                         |

---

## 17. Testing & Debugging

### Development Environment

1. **Run your dev server** on `localhost`
2. **Expose via HTTPS tunnel**: `ngrok http 3000` (or Cloudflare Tunnel, localtunnel, etc.)
3. **Configure BotFather**:
   - Create/select your bot
   - Set the Web App URL via `/setmenubutton` or `/newapp`
4. **Open in Telegram** and test

### Debugging Tips

| Platform         | Method                                                                      |
| :--------------- | :-------------------------------------------------------------------------- |
| **Android**      | Enable WebView debugging in Android Developer Settings → `chrome://inspect` |
| **iOS**          | Safari → Develop → your device → your WebView                               |
| **Desktop**      | Right-click inside Mini App → "Inspect Element" (on some builds)            |
| **Telegram Web** | Regular browser DevTools                                                    |

### Testing Outside Telegram

Wrap all `tg` calls with a safety check. Provide fallback UI for development:

```javascript
const tg = window.Telegram?.WebApp;
const isInTelegram = !!tg?.initData;

if (isInTelegram) {
  tg.ready();
  tg.MainButton.show();
} else {
  // Show a regular HTML button instead for local testing
  console.log("Running outside Telegram — showing fallback UI");
}
```

---

## 18. Common Pitfalls

| Pitfall                                 | Solution                                                                                                   |
| :-------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| Colors look wrong in Telegram           | Use `--tg-theme-*` CSS variables, never hardcode                                                           |
| App stuck on loading spinner            | Call `tg.ready()` after initial render                                                                     |
| MainButton not responding               | Always `offClick(handler)` before registering new handler                                                  |
| iOS zooms in on input focus             | Set input `font-size` to ≥ 16px                                                                            |
| SSR hydration errors (Next.js, Nuxt)    | Add `suppressHydrationWarning` to `<html>` tag                                                             |
| initData is empty                       | App was launched via keyboard button (expected) — handle gracefully                                        |
| API calls return 403                    | Validate `initData` correctly on server; check `auth_date` freshness                                       |
| Stale state in button handlers          | Use refs (React) or reactive getters (Vue) — handlers capture closure variables                            |
| Content hidden behind MainButton        | Add bottom padding (~80–100px) to main content                                                             |
| Safe area content overlap in fullscreen | Use `--tg-safe-area-inset-*` and `--tg-content-safe-area-inset-*` CSS variables                            |
| `window.Telegram` is undefined          | SDK script not loaded yet — ensure it loads before your app code                                           |
| Double-click on MainButton              | Disable button and show progress immediately on click                                                      |
| Theme not updating dynamically          | Listen to `themeChanged` event; CSS variables update automatically                                         |
| Clipboard API not working               | Use `tg.readTextFromClipboard()`, not the browser Clipboard API                                            |
| File download not working on web        | Include `Content-Disposition` and `Access-Control-Allow-Origin: https://web.telegram.org` response headers |

---

## Quick Reference: Useful Methods

```javascript
const tg = window.Telegram.WebApp;

// Basics
tg.ready(); // Signal app is ready
tg.expand(); // Expand to full height
tg.close(); // Close the Mini App

// User data
tg.initData; // Raw string for server validation
tg.initDataUnsafe.user; // User object (not validated!)

// Navigation
tg.openLink(url); // Open URL in browser
tg.openLink(url, { try_instant_view: true }); // Try Instant View
tg.openTelegramLink(url); // Open telegram link (resolves inside Telegram)

// Sharing
tg.switchInlineQuery(query, ["users", "groups"]); // Switch to inline mode
tg.shareToStory(mediaUrl, params); // Share to Stories

// Clipboard
tg.readTextFromClipboard((text) => {}); // Read clipboard

// QR Code
tg.showScanQrPopup({ text: "Scan QR" }, (data) => {
  // Handle QR data
  return true; // return true to close popup
});
tg.closeScanQrPopup();

// Payments
tg.openInvoice(invoiceUrl, (status) => {
  // status: "paid", "cancelled", "failed", "pending"
});

// Colors
tg.setHeaderColor("#RRGGBB"); // Custom header color
tg.setBackgroundColor("#RRGGBB"); // Custom background color
tg.setBottomBarColor("#RRGGBB"); // Custom bottom bar color

// Permissions
tg.requestWriteAccess((granted) => {}); // Request PM write access
tg.requestContact((shared) => {}); // Request phone contact

// Home screen
tg.addToHomeScreen(); // Prompt add to home screen
tg.checkHomeScreenStatus((status) => {}); // 'added', 'missed', etc.

// Fullscreen
tg.requestFullscreen();
tg.exitFullscreen();

// Closing confirmation
tg.enableClosingConfirmation(); // Warn user before closing
tg.disableClosingConfirmation();

// Send data to bot (limited to 4096 bytes)
tg.sendData(JSON.stringify({ action: "submit" }));
```
