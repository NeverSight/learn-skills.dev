---
name: solito
description: This skill should be used when working on Solito projects (Expo + Next.js with shared navigation). It provides specialized knowledge for cross-platform navigation, monorepo structure, shared component patterns, platform-specific code handling, and common pitfalls. Use this skill when building universal apps, implementing navigation, creating shared UI components, or debugging cross-platform issues.
---

# Solito Cross-Platform Development Skill

A specialized skill for building universal applications using Solito, combining Expo (React Native) and Next.js with shared navigation and component libraries.

## When to Use This Skill

Invoke this skill when:
- Building universal apps (web + mobile) with shared code
- Implementing cross-platform navigation
- Creating shared UI components that work on web and native
- Setting up monorepo structure for Solito projects
- Handling platform-specific code (web-only or native-only features)
- Implementing authentication across platforms
- Debugging navigation or routing issues
- Optimizing bundle sizes for web and native

## What is Solito?

Solito enables developers to share navigation code between React Native (Expo) and Next.js. Instead of maintaining separate routing logic for web and mobile, Solito provides a unified navigation layer that respects platform-specific patterns while sharing as much code as possible.

**Key Benefits:**
- Single source of truth for navigation
- File-system routing for native apps (via Expo Router)
- Shared UI components with platform-specific optimizations
- Unified API for links and navigation
- Type-safe routing with TypeScript

## Before You Start: Essential Solito Tips

### Project Structure First

**Solito projects use monorepo architecture.** Always structure your project correctly from the start:

```
my-app/
  apps/
    expo/          # React Native mobile app
    next/          # Next.js web app
  packages/
    app/           # Shared UI components & navigation
    api/           # Shared API client (optional)
  package.json     # Workspace configuration
```

**See `references/monorepo-setup.md` for detailed workspace configuration.**

### Use Solito Starter Template

The official Solito starter saves hours of configuration:

```bash
npx create-solito-app@latest my-app
```

Choose your preferred package manager (pnpm recommended for monorepos).

### Navigation is Different

**Don't use Next.js Link or React Navigation Link directly.** Use Solito's unified components:

```tsx
import { Link } from 'solito/link'

// ✅ CORRECT: Works on both web and native
<Link href="/profile">
  <Text>View Profile</Text>
</Link>

// ❌ WRONG: Next.js-only
import Link from 'next/link'

// ❌ WRONG: React Navigation-only
import { Link } from '@react-navigation/native'
```

**See `references/navigation-patterns.md` for detailed routing patterns.**

## Core Development Principles

### 1. Shared by Default, Platform-Specific When Needed

**80% of your code should live in `packages/app`.** Only create platform-specific code when absolutely necessary.

```tsx
// packages/app/features/home/screen.tsx
// ✅ GOOD: Shared screen component
export function HomeScreen() {
  return (
    <View>
      <Text>Welcome!</Text>
      <Link href="/profile">
        <Text>Go to Profile</Text>
      </Link>
    </View>
  )
}
```

Platform-specific code should be minimal:

```tsx
// packages/app/components/map.tsx
import { Platform } from 'react-native'

export function Map() {
  // ✅ GOOD: Platform detection for necessary differences
  if (Platform.OS === 'web') {
    return <WebMapComponent />
  }
  return <NativeMapComponent />
}
```

### 2. Think in Features, Not Platforms

**Organize by feature domain, not by platform:**

```
packages/app/
  features/
    home/
      screen.tsx       # Home screen
      components/      # Home-specific components
    profile/
      screen.tsx       # Profile screen
      components/
    auth/
      login-screen.tsx
      register-screen.tsx
  components/         # Shared UI components
  provider/           # Navigation provider
  navigation/         # Navigation configuration
```

**Not organized by platform:**
```
❌ BAD:
packages/app/
  web/
    screens/
  native/
    screens/
```

### 3. Navigation is Central

**Design your navigation structure early.** Solito uses file-system routing on native and Next.js App Router on web.

**Navigation mapping:**
```tsx
// apps/next/app/profile/page.tsx (web route)
import { ProfileScreen } from 'app/features/profile/screen'

export default ProfileScreen

// apps/expo/app/profile.tsx (native route)
import { ProfileScreen } from 'app/features/profile/screen'

export default ProfileScreen
```

Both platforms render the same `ProfileScreen` component from `packages/app`.

**See `references/navigation-patterns.md` for routing patterns, params, and navigation hooks.**

## Development Workflow

### Local Development

**Run both platforms simultaneously:**

Terminal 1 - Web:
```bash
cd apps/next
pnpm dev
```

Terminal 2 - Mobile:
```bash
cd apps/expo
pnpm start
```

Press `i` for iOS simulator, `a` for Android emulator, or scan QR code for physical device.

### Making Changes

1. **Create shared component** in `packages/app/components/`
2. **Create screen** in `packages/app/features/[feature]/screen.tsx`
3. **Add routes** in both `apps/next/app/` and `apps/expo/app/`
4. **Test on both platforms** to verify cross-platform behavior

### Common Commands

```bash
# Install dependencies (from root)
pnpm install

# Run web dev server
cd apps/next && pnpm dev

# Run Expo dev server
cd apps/expo && pnpm start

# Type checking
pnpm typecheck

# Lint all packages
pnpm lint

# Build for production
pnpm build
```

## Styling with NativeWind

NativeWind brings Tailwind CSS to React Native, enabling shared styling across platforms.

```tsx
import { View, Text } from 'react-native'

// ✅ GOOD: Tailwind classes work on both platforms
export function Card() {
  return (
    <View className="bg-white rounded-lg p-4 shadow-md">
      <Text className="text-xl font-bold">Title</Text>
      <Text className="text-gray-600">Description</Text>
    </View>
  )
}
```

**Platform-specific styles when needed:**
```tsx
<View className="p-4 web:p-6 native:p-2">
  {/* Different padding on web vs native */}
</View>
```

### Design Tokens

**Use shared design tokens in `packages/app/design/tokens.ts`:**

```tsx
export const colors = {
  primary: '#3B82F6',
  secondary: '#10B981',
  background: '#FFFFFF',
  text: '#1F2937',
}

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
}
```

## Authentication Patterns

**Share auth logic across platforms:**

```tsx
// packages/app/lib/auth.ts
import { createContext, useContext } from 'react'

interface AuthContextType {
  user: User | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

export const AuthContext = createContext<AuthContextType>(null!)

export function useAuth() {
  return useContext(AuthContext)
}
```

**Use in components:**
```tsx
import { useAuth } from 'app/lib/auth'

export function ProfileScreen() {
  const { user, signOut } = useAuth()

  return (
    <View>
      <Text>Welcome, {user?.name}</Text>
      <Button onPress={signOut}>Sign Out</Button>
    </View>
  )
}
```

**Popular auth solutions:**
- **Clerk** - Excellent Solito integration, works on both platforms
- **Supabase** - Self-hosted option with good RN support
- **Custom JWT** - Full control, requires more setup

## API Integration

**Share API client in `packages/api/`:**

```tsx
// packages/api/client.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function fetchUser(id: string) {
  const response = await fetch(`${API_URL}/users/${id}`)
  return response.json()
}
```

**Use with tRPC for type-safety:**
```tsx
// packages/api/trpc.ts
import { initTRPC } from '@trpc/server'

const t = initTRPC.create()

export const appRouter = t.router({
  getUser: t.procedure
    .input(z.string())
    .query(async ({ input }) => {
      return db.user.findUnique({ where: { id: input } })
    }),
})

export type AppRouter = typeof appRouter
```

**tRPC works seamlessly across web and native with full type-safety.**

## State Management

**Recommended: Zustand** (lightweight, works great with Solito)

```tsx
// packages/app/store/user.ts
import { create } from 'zustand'

interface UserState {
  user: User | null
  setUser: (user: User | null) => void
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}))
```

**Use in components:**
```tsx
import { useUserStore } from 'app/store/user'

export function ProfileScreen() {
  const user = useUserStore((state) => state.user)

  return <Text>Welcome, {user?.name}</Text>
}
```

**Other options:**
- **Jotai** - Atomic state management
- **Redux Toolkit** - For complex state needs
- **React Context** - For simple global state

## Platform-Specific Code

**Use platform detection sparingly:**

```tsx
import { Platform } from 'react-native'

export function VideoPlayer() {
  if (Platform.OS === 'web') {
    return <video src={url} controls />
  }

  // Use native video component
  return <Video source={{ uri: url }} />
}
```

**Better: Use platform-specific files:**

```
packages/app/components/
  video-player.tsx         # Shared interface
  video-player.web.tsx     # Web implementation
  video-player.native.tsx  # Native implementation
```

```tsx
// video-player.tsx
export { VideoPlayer } from './video-player.native'
```

Metro bundler and Next.js will automatically resolve the correct file.

**See `references/platform-specific.md` for detailed patterns.**

## Common Pitfalls to Avoid

**Critical mistakes and their solutions are documented in `references/common-pitfalls.md`. Key pitfalls include:**

1. Using Next.js Link or React Navigation Link directly
2. Hardcoding absolute URLs (use relative paths)
3. Not handling navigation params correctly
4. Importing from wrong packages (next/link vs solito/link)
5. Forgetting to configure navigation provider
6. Not testing on both platforms regularly
7. Overusing platform-specific code

Review `references/common-pitfalls.md` before implementing navigation or shared components.

## Performance Optimization

### Bundle Size

**Keep packages/app lean:**
- Avoid large dependencies in shared code
- Use dynamic imports for heavy features
- Split platform-specific dependencies

```tsx
// ✅ GOOD: Dynamic import for heavy feature
const HeavyChart = dynamic(() => import('./heavy-chart'))
```

### Navigation Performance

**Preload screens for better UX:**
```tsx
import { useRouter } from 'solito/router'

export function HomeScreen() {
  const router = useRouter()

  // Preload profile screen on hover/focus
  const handlePreload = () => {
    router.push('/profile', undefined, { shallow: true })
  }

  return (
    <Link href="/profile" onHoverIn={handlePreload}>
      <Text>Profile</Text>
    </Link>
  )
}
```

### Image Optimization

**Use Next.js Image on web, optimized Image on native:**

```tsx
// packages/app/components/optimized-image.tsx
import { Platform } from 'react-native'
import NextImage from 'next/image'
import { Image as RNImage } from 'react-native'

export function OptimizedImage({ src, width, height, alt }) {
  if (Platform.OS === 'web') {
    return <NextImage src={src} width={width} height={height} alt={alt} />
  }

  return <RNImage source={{ uri: src }} style={{ width, height }} />
}
```

## Testing Strategy

### Unit Tests

**Test shared logic in packages/app:**

```tsx
// packages/app/lib/__tests__/format.test.ts
import { formatCurrency } from '../format'

describe('formatCurrency', () => {
  it('formats USD correctly', () => {
    expect(formatCurrency(1234.56, 'USD')).toBe('$1,234.56')
  })
})
```

### Component Tests

**Use React Native Testing Library:**

```tsx
import { render, screen } from '@testing-library/react-native'
import { HomeScreen } from '../screen'

test('renders welcome message', () => {
  render(<HomeScreen />)
  expect(screen.getByText('Welcome!')).toBeTruthy()
})
```

### E2E Tests

**Playwright for web, Detox for native:**

```typescript
// apps/next/e2e/home.spec.ts
import { test, expect } from '@playwright/test'

test('navigates to profile', async ({ page }) => {
  await page.goto('/')
  await page.click('text=Profile')
  await expect(page).toHaveURL('/profile')
})
```

## Deployment

### Web (Next.js)

**Deploy to Vercel (recommended):**

```bash
cd apps/next
vercel deploy
```

Configure environment variables in Vercel dashboard.

### Mobile (Expo)

**Build with EAS:**

```bash
cd apps/expo

# Install EAS CLI
npm install -g eas-cli

# Configure project
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to stores
eas submit
```

**Over-the-air updates:**
```bash
eas update --branch production
```

## References

This skill includes detailed reference documentation:

- `references/navigation-patterns.md` - Link usage, router hooks, params, navigation state
- `references/monorepo-setup.md` - Workspace configuration, package structure, dependencies
- `references/platform-specific.md` - Platform detection, conditional rendering, file extensions
- `references/common-pitfalls.md` - Import issues, navigation bugs, platform quirks

Load these references as needed to inform implementation decisions.

## Additional Resources

**Solito Documentation:**
- Official Docs: https://solito.dev/
- Solito Starter: https://github.com/nandorojo/solito
- Example Apps: https://github.com/nandorojo/solito/tree/master/example-monorepos

**Related Technologies:**
- Expo Router: https://docs.expo.dev/router/introduction/
- Next.js App Router: https://nextjs.org/docs/app
- NativeWind: https://www.nativewind.dev/
- React Navigation: https://reactnavigation.org/

**State Management:**
- Zustand: https://github.com/pmndrs/zustand
- Jotai: https://jotai.org/
- Redux Toolkit: https://redux-toolkit.js.org/

**Authentication:**
- Clerk: https://clerk.com/
- Supabase: https://supabase.com/
- NextAuth.js: https://next-auth.js.org/

---

**Remember:** Share code by default, create platform-specific code only when necessary. Design your navigation structure early, test on both platforms regularly, and keep `packages/app` as the single source of truth for your application logic.
