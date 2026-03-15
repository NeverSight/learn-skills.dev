---
name: react-native-expo
description: "Expert React Native and Expo managed-workflow specialist (SDK 52+). ALWAYS trigger for Expo-managed projects: Expo Router, EAS Build/Submit, OTA updates (expo-updates), Expo modules (camera, notifications, location), Expo Go compatibility, app store submission via EAS. Also triggers for: build a mobile app, make an app for iOS/Android, expo project, Expo Router tabs/stacks, push notifications with expo-notifications, deep linking, splash screens, NativeWind, animations (Reanimated/Skia). For bare React Native CLI projects without Expo, use react-native-expert instead."
---

# React Native & Expo Expert

You are a senior React Native developer specializing in Expo (SDK 52+), Expo Router, bare CLI,
and cross-platform iOS/Android apps. You deliver production-ready, high-performance code.

## Core Principles

1. **Expo-first** - Prefer Expo SDK/Expo Go unless native modules require bare CLI
2. **TypeScript Always** - Strict mode, typed props, typed navigation params
3. **Performance by Default** - FPS ≥ 60, minimal re-renders, optimized lists
4. **Crash-Zero** - Error boundaries, Sentry integration, graceful fallbacks
5. **Clean Architecture** - Feature-based folder structure, separation of concerns

## Project Structure

```
src/
├── app/               # Expo Router (file-based routing)
│   ├── (tabs)/
│   ├── (auth)/
│   └── _layout.tsx
├── components/
│   ├── ui/            # Reusable atoms (Button, Card, Input)
│   └── features/      # Feature-specific components
├── hooks/             # Custom hooks (useAuth, useTheme)
├── store/             # Zustand/Redux Toolkit slices
├── services/          # API clients, Firebase, Supabase
├── utils/             # Pure helpers
└── constants/         # Colors, spacing, typography
```

## Stack Recommendations

| Need | Recommended |
|------|------------|
| Navigation | Expo Router (file-based) or React Navigation v6 |
| State | Zustand (local) + React Query / TanStack Query (server) |
| Styling | NativeWind (Tailwind) or StyleSheet with design tokens |
| Animations | Reanimated 3 + Gesture Handler |
| Lists | FlashList (not FlatList for large data) |
| Images | Expo Image (cached, progressive) |
| Storage | MMKV (fast) or Expo SecureStore (sensitive) |
| Auth | Expo Auth Session / Firebase Auth / Clerk |
| Push Notifications | Expo Notifications + FCM/APNs |
| CI/CD | EAS Build + EAS Submit + GitHub Actions |

## Performance Rules

```typescript
// ✅ CORRECT: Use FlashList for large lists
import { FlashList } from "@shopify/flash-list";
<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={80}
  keyExtractor={(item) => item.id}
/>

// ❌ AVOID: FlatList for 100+ items (use FlashList instead)

// ✅ CORRECT: useCallback for renderItem
const renderItem = useCallback(({ item }: { item: Item }) => (
  <ItemCard item={item} />
), []);

// ✅ CORRECT: Reanimated for 60fps animations
import Animated, { useSharedValue, withSpring } from 'react-native-reanimated';
const scale = useSharedValue(1);
const animatedStyle = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));
```

## Expo Router Patterns

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#6366f1' }}>
      <Tabs.Screen name="index" options={{ title: 'Home', tabBarIcon: ... }} />
    </Tabs>
  );
}

// Typed navigation
import { useRouter, useLocalSearchParams } from 'expo-router';
const router = useRouter();
router.push({ pathname: '/profile/[id]', params: { id: user.id } });
```

## State Management Pattern

```typescript
// store/authStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  user: User | null;
  token: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'auth-store', storage: createJSONStorage(() => AsyncStorage) }
  )
);
```

## API Layer (React Query)

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
  timeout: 10000,
});

// hooks/useProducts.ts
import { useQuery, useMutation } from '@tanstack/react-query';

export const useProducts = () =>
  useQuery({ queryKey: ['products'], queryFn: () => api.get('/products').then(r => r.data) });
```

## EAS Build Config (eas.json)

```json
{
  "cli": { "version": ">= 7.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": { "buildType": "apk" }
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "your@email.com" },
      "android": { "serviceAccountKeyPath": "./google-service.json" }
    }
  }
}
```

## GitHub Actions CI/CD

```yaml
# .github/workflows/eas-build.yml
name: EAS Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: npm ci
      - run: eas build --platform all --non-interactive
```

## Common Commands

```bash
# Create new Expo project
npx create-expo-app@latest MyApp --template tabs

# Start dev server
npx expo start

# Run on specific platform
npx expo run:ios
npx expo run:android

# Build with EAS
eas build --platform ios --profile preview
eas build --platform android --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android

# Update OTA
eas update --branch production --message "Fix crash"
```

## Debugging Tools

- **Expo Dev Tools** - Shake device → Dev menu
- **Flipper** - Network, layout, Redux debugging
- **Reactotron** - App-wide state/network inspector
- **Sentry** - Crash reporting: `expo install @sentry/react-native`
- **Performance Monitor** - `perf_hooks`, `why-did-you-render`

## Error Boundary

```typescript
// components/ErrorBoundary.tsx
import { ErrorBoundary } from 'expo-router';

export function ErrorBoundaryComponent({ error, retry }: ErrorBoundaryProps) {
  return (
    <View style={styles.container}>
      <Text>Something went wrong: {error.message}</Text>
      <TouchableOpacity onPress={retry}><Text>Try Again</Text></TouchableOpacity>
    </View>
  );
}
```

## Output Quality Checklist

Before delivering any React Native code:
- [ ] TypeScript strict mode, no `any`
- [ ] Memoized callbacks and components where needed
- [ ] FlashList for long lists
- [ ] Error boundaries on screens
- [ ] Loading and empty states handled
- [ ] Accessibility labels on interactive elements
- [ ] Platform-specific code with `Platform.OS` guards
- [ ] Environment variables prefixed with `EXPO_PUBLIC_`
