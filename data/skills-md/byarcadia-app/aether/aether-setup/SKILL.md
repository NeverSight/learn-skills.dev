---
name: aether-setup
description: "Install and configure @byarcadia-app/aether in an Expo project. Use this skill whenever a user wants to install aether, set up aether-ui, add aether to their project, setup NativeWind with the aether preset, configure aether in Expo, add @byarcadia-app/aether, or create a new Expo app with aether components. MUST USE for any aether installation or NativeWind+aether configuration task."
---

## iOS Only

This library targets **iOS exclusively**. Android and web are not supported.

## Prerequisites

- Expo project with TypeScript
- React Native ≥ 0.72

> **Note:** Commands below use `npx expo install` for React Native and Expo packages and `pnpm` for everything else.

## Step 1: Install dependencies

```bash
npx expo install nativewind@^4 react-native-reanimated react-native-safe-area-context @expo-google-fonts/inter @callstack/liquid-glass expo-haptics expo-linear-gradient
pnpm add @byarcadia-app/aether
pnpm add -D tailwindcss@^3.4.17
```

Optional — only needed for `IconSymbol` (SF Symbols on iOS):

```bash
npx expo install expo-symbols
```

## Step 2: Configure Tailwind

Create `tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./node_modules/@byarcadia-app/aether/dist/**/*.{js,mjs}",
  ],
  presets: [require("nativewind/preset"), require("@byarcadia-app/aether/tailwind-preset").preset],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

## Step 3: Create global CSS

Create `global.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Step 4: Configure Babel

Create or update `babel.config.js`:

```js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [["babel-preset-expo", { jsxImportSource: "nativewind" }], "nativewind/babel"],
  };
};
```

## Step 5: Configure Metro

Create or update `metro.config.js`:

```js
const { getDefaultConfig } = require("expo/metro-config");
const { withNativeWind } = require("nativewind/metro");

const config = getDefaultConfig(__dirname);

module.exports = withNativeWind(config, { input: "./global.css" });
```

## Step 6: Import CSS in root layout

Add to your root layout file (e.g., `app/_layout.tsx`):

```tsx
import "./global.css";
```

## Step 7: TypeScript

Create `nativewind-env.d.ts`:

```ts
/// <reference types="nativewind/types" />
```

## Quick Start

Wire up `AetherProvider` with fonts and React Navigation:

```tsx
import { AetherProvider, useInterFonts, useNavigationTheme } from "@byarcadia-app/aether";
import { ThemeProvider } from "@react-navigation/native";
import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";

import "./global.css";

SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const { fontsLoaded, fontError } = useInterFonts();
  const navigationTheme = useNavigationTheme();

  useEffect(() => {
    if (fontsLoaded || fontError) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded, fontError]);

  if (!fontsLoaded && !fontError) {
    return null;
  }

  return (
    <AetherProvider>
      <ThemeProvider value={navigationTheme}>
        <Stack />
      </ThemeProvider>
    </AetherProvider>
  );
}
```

## Peer Dependencies

- `@callstack/liquid-glass` >=0.7
- `@expo-google-fonts/inter` >=0.4.2
- `expo-haptics` >=14
- `expo-linear-gradient` >=14
- `expo-symbols` >=1 (optional — only for IconSymbol)
- `nativewind` >=4
- `react` >=18
- `react-native` >=0.72
- `react-native-reanimated` >=3
- `tailwindcss` ^3.3.5

## Verification

After setup, run `npx expo start` and verify the app compiles. Themed components should render with the correct Inter font and color tokens in both light and dark mode.
