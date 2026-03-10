---
name: expo-best-practices
description:
  Expo and React Native done right. Expo Router, EAS Build, native modules, platform-specific
  patterns, and navigation.
metadata:
  tags: expo, react-native, mobile, best-practices
---

## When to use

Use this skill when working with Expo or React Native code. It teaches current best practices and
prevents common mistakes that AI agents make with outdated patterns, manual native setup, and
deprecated APIs.

## Critical Rules

### 1. Use Expo Router for navigation

**Wrong (agents do this):**

```tsx
import { createStackNavigator } from "@react-navigation/stack";
const Stack = createStackNavigator();
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Correct:**

```
app/
  _layout.tsx
  index.tsx
  settings.tsx
```

Use the `app/` directory convention. Files become routes automatically. New Expo projects include
Expo Router by default.

**Why:** Expo Router is built on React Navigation, provides file-based routing, typed routes, deep
linking, and integrates with Expo CLI. Manual React Navigation setup is redundant and misses Expo
Router features.

### 2. Use expo-router layouts for navigation structure

**Wrong:**

```tsx
// Each screen manually defines its own layout
```

**Correct:**

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";
export default function RootLayout() {
  return <Stack />;
}
```

**Why:** `_layout.tsx` defines shared navigation structure, tabs, stacks, and nested layouts. It
centralizes navigation configuration.

### 3. Use EAS Build for native builds

**Wrong:**

```bash
expo build:ios
expo build:android
```

**Correct:**

```bash
eas build --platform ios
eas build --platform android
```

**Why:** `expo build` is deprecated. EAS Build is the current cloud build service with better
caching, credentials management, and native module support.

### 4. Use Expo config plugins for native configuration

**Wrong:**

```bash
# Manually editing
ios/MyApp/Info.plist
android/app/src/main/AndroidManifest.xml
```

**Correct:**

```ts
// app.config.ts
import { ConfigPlugin } from "expo/config-plugins";
const withMyApiKey: ConfigPlugin<{ apiKey: string }> = (config, { apiKey }) => {
  config = withInfoPlist(config, (c) => {
    c.modResults["MY_API_KEY"] = apiKey;
    return c;
  });
  return config;
};
export default {
  plugins: [["withMyApiKey", { apiKey: process.env.API_KEY }]],
};
```

**Why:** Direct edits to native files are overwritten on prebuild. Config plugins modify native
files at build time and survive prebuild.

### 5. Platform-specific code: use platform extensions or Platform.select

**Wrong:**

```tsx
if (Platform.OS === "ios") {
  return <IOSComponent />;
}
return <AndroidComponent />;
```

**Correct:**

```
MyComponent.ios.tsx
MyComponent.android.tsx
```

Or:

```tsx
import { Platform } from "react-native";
const styles = StyleSheet.create({
  container: Platform.select({
    ios: { paddingTop: 20 },
    android: { paddingTop: 0 },
  }),
});
```

**Why:** Platform file extensions let the bundler include only the correct code per platform.
Platform.select keeps conditional logic in one file when appropriate.

### 6. Use expo-image instead of React Native Image

**Wrong:**

```tsx
import { Image } from "react-native";
<Image source={{ uri: url }} style={styles.image} />;
```

**Correct:**

```tsx
import { Image } from "expo-image";
<Image source={url} contentFit="cover" style={styles.image} />;
```

**Why:** expo-image adds caching, placeholders, blurhash, and better performance. React Native's
Image lacks these features.

### 7. Use expo-font for custom fonts

**Wrong:**

```bash
# Manual font linking via native projects
```

**Correct:**

```tsx
import * as Font from "expo-font";
await Font.loadAsync({
  CustomFont: require("./assets/fonts/CustomFont.ttf"),
});
```

**Why:** expo-font handles loading and avoids manual native configuration.

### 8. Use expo-secure-store for sensitive data

**Wrong:**

```tsx
import AsyncStorage from "@react-native-async-storage/async-storage";
await AsyncStorage.setItem("authToken", token);
```

**Correct:**

```tsx
import * as SecureStore from "expo-secure-store";
await SecureStore.setItemAsync("authToken", token);
```

**Why:** AsyncStorage is not encrypted. expo-secure-store uses the platform keychain/Keystore for
tokens and secrets.

### 9. Use expo-notifications for push notifications

**Wrong:**

```tsx
// Manual Firebase/APNs setup, native configuration
```

**Correct:**

```tsx
import * as Notifications from "expo-notifications";
const token = await Notifications.getExpoPushTokenAsync();
```

**Why:** expo-notifications abstracts push setup across iOS and Android. Manual Firebase/APNs
configuration is error-prone and platform-specific.

### 10. Use app.json or app.config.ts for configuration

**Wrong:**

```bash
# Editing Info.plist or AndroidManifest.xml directly
```

**Correct:**

```json
{
  "expo": {
    "name": "MyApp",
    "slug": "my-app",
    "plugins": ["expo-router"]
  }
}
```

**Why:** Expo manages native config from app.json/app.config.ts. Direct edits are overwritten on
prebuild.

### 11. Use expo-updates for OTA updates

**Wrong:**

```tsx
import codePush from "react-native-code-push";
export default codePush(MyApp);
```

**Correct:**

```tsx
import * as Updates from "expo-updates";
await Updates.checkForUpdateAsync();
```

**Why:** expo-updates integrates with EAS and Expo's update service. CodePush requires separate
setup and is redundant in Expo projects.

### 12. Use TypeScript with typed navigation params

**Wrong:**

```tsx
router.push("/profile");
```

**Correct:**

```tsx
import { router } from "expo-router";
router.push({ pathname: "/profile/[id]", params: { id: userId } });
```

Define route params in your route files. Expo Router provides typed route helpers when used with
TypeScript.

**Why:** Typed params prevent runtime errors and improve editor support.

## Patterns

- Create routes under `app/` with file names that map to URLs
- Use `_layout.tsx` for shared layout, tabs, and stacks
- Put platform-specific components in `Component.ios.tsx` and `Component.android.tsx`
- Use `expo config plugins` in `app.json` / `app.config.ts` for any native config change
- Use `eas.json` for EAS Build profiles

## Anti-Patterns

- Do not set up React Navigation manually in Expo projects
- Do not use `expo build` (use EAS Build)
- Do not edit `ios/` or `android/` directly in managed workflow
- Do not use AsyncStorage for auth tokens or secrets
- Do not use React Native's Image when expo-image is available
- Do not use CodePush in Expo projects (use expo-updates)
