---
name: neon-auth-nextjs
description: Sets up Neon Auth in Next.js App Router applications. Configures API routes, middleware, server components, and UI. Use when adding auth-only to Next.js apps (no database needed).
allowed-tools: ["Bash", "Write", "Read", "Edit", "Glob", "Grep"]
---

# Neon Auth for Next.js

Help developers set up @neondatabase/auth in Next.js App Router applications (auth only, no database).

## When to Use

Use this skill when:
- Setting up Neon Auth in Next.js (App Router)
- User mentions "next.js", "next", or "app router" with Neon Auth
- Auth-only setup (no database needed)

## Critical Rules

1. **Server vs Client imports**: Use correct import paths
2. **`'use client'` directive**: Required for client components using hooks
3. **CSS Import**: Choose ONE - either `/ui/css` OR `/ui/tailwind`, never both
4. **onSessionChange**: Always call `router.refresh()` to update Server Components

## Critical Imports

| Purpose | Import From |
|---------|-------------|
| Unified Server (`createNeonAuth`) | `@neondatabase/auth/next/server` |
| Client Auth | `@neondatabase/auth/next` |
| UI Components | `@neondatabase/auth/react/ui` |
| View Paths (static params) | `@neondatabase/auth/react/ui/server` |

**Note**: Use `createNeonAuth()` from `@neondatabase/auth/next/server` to get a unified `auth` instance that provides:
- `.handler()` - API route handler
- `.middleware()` - Route protection middleware
- All Better Auth server methods (`.signIn`, `.signUp`, `.getSession`, etc.)

---

## Setup

### 1. Install
```bash
npm install @neondatabase/auth
```

### 2. Environment (`.env.local`)
```
NEON_AUTH_BASE_URL=https://your-auth.neon.tech
NEON_AUTH_COOKIE_SECRET=your-secret-at-least-32-characters-long
```

**Important**: Generate a secure secret (32+ characters) for production:
```bash
openssl rand -base64 32
```

### 3. Server Setup (`lib/auth/server.ts`)

Create a auth instance that provides handler, middleware, and server methods:

```typescript
import { createNeonAuth } from '@neondatabase/auth/next/server';

export const auth = createNeonAuth({
  baseUrl: process.env.NEON_AUTH_BASE_URL!,
  cookies: {
    secret: process.env.NEON_AUTH_COOKIE_SECRET!,
    sessionDataTtl: 300,          // Optional: session data cache TTL in seconds (default: 300 = 5 min)
    domain: '.example.com',       // Optional: for cross-subdomain cookies
  },
});
```

### 4. API Route (`app/api/auth/[...path]/route.ts`)
```typescript
import { auth } from '@/lib/auth/server';

export const { GET, POST } = auth.handler();
```

### 5. Middleware (`middleware.ts`)
```typescript
import { auth } from '@/lib/auth/server';

export default auth.middleware({
  loginUrl: '/auth/sign-in',
});

export const config = {
  matcher: ['/dashboard/:path*', '/account/:path*'],
};
```

### 6. Client (`lib/auth/client.ts`)
```typescript
'use client';
import { createAuthClient } from '@neondatabase/auth/next';

export const authClient = createAuthClient();
```

### 7. Provider (`app/providers.tsx`)
```typescript
'use client';
import { NeonAuthUIProvider } from '@neondatabase/auth/react/ui';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth/client';

export function Providers({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  return (
    <NeonAuthUIProvider
      authClient={authClient}
      navigate={router.push}
      replace={router.replace}
      onSessionChange={() => router.refresh()}
      redirectTo="/dashboard"
      Link={({href, children}) => <Link to={href}>{children}</Link>}
    >
      {children}
    </NeonAuthUIProvider>
  );
}
```

### 8. Layout (`app/layout.tsx`)
```typescript
import { Providers } from './providers';
import '@neondatabase/auth/ui/css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### 9. Auth Pages (`app/auth/[path]/page.tsx`)
```typescript
import { AuthView } from '@neondatabase/auth/react/ui';
import { authViewPaths } from '@neondatabase/auth/react/ui/server';

export function generateStaticParams() {
  return Object.values(authViewPaths).map((path) => ({ path }));
}

export default async function AuthPage({ params }: { params: Promise<{ path: string }> }) {
  const { path } = await params;
  return <AuthView pathname={path} />;
}
```

---

## CSS & Styling

### Import Options

**Without Tailwind** (pre-built CSS bundle ~47KB):
```typescript
// app/layout.tsx
import '@neondatabase/auth/ui/css';
```

**With Tailwind CSS v4** (`app/globals.css`):
```css
@import 'tailwindcss';
@import '@neondatabase/auth/ui/tailwind';
```

**IMPORTANT**: Never import both - causes duplicate styles.

### Dark Mode

The provider includes `next-themes`. Control via `defaultTheme` prop:

```typescript
<NeonAuthUIProvider
  defaultTheme="system" // 'light' | 'dark' | 'system'
  // ...
>
```

### Custom Theming

Override CSS variables in `globals.css`:
```css
:root {
  --primary: hsl(221.2 83.2% 53.3%);
  --primary-foreground: hsl(210 40% 98%);
  --background: hsl(0 0% 100%);
  --foreground: hsl(222.2 84% 4.9%);
  --card: hsl(0 0% 100%);
  --card-foreground: hsl(222.2 84% 4.9%);
  --border: hsl(214.3 31.8% 91.4%);
  --input: hsl(214.3 31.8% 91.4%);
  --ring: hsl(221.2 83.2% 53.3%);
  --radius: 0.5rem;
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  /* ... dark mode overrides */
}
```

---

## NeonAuthUIProvider Props

Full configuration options:

```typescript
<NeonAuthUIProvider
  // Required
  authClient={authClient}

  // Navigation (Next.js specific)
  navigate={router.push}        // router.push for navigation
  replace={router.replace}      // router.replace for redirects
  onSessionChange={() => router.refresh()} // Refresh Server Components!
  redirectTo="/dashboard"       // Where to redirect after auth
  Link={({href, children}) => <Link to={href}>{children}</Link>}                   // Next.js Link component

  // Social/OAuth Providers
  social={{
    providers: ['google'],
  }}

  // Feature Flags
  emailOTP={true}               // Enable email OTP sign-in
  emailVerification={true}      // Require email verification
  magicLink={false}             // Magic link (disabled by default)
  multiSession={false}          // Multiple sessions (disabled)

  // Credentials Configuration
  credentials={{
    forgotPassword: true,       // Show forgot password link
  }}

  // Sign Up Fields
  signUp={{
    fields: ['name'],           // Additional fields: 'name', 'username', etc.
  }}

  // Account Settings Fields
  account={{
    fields: ['image', 'name', 'company', 'age', 'newsletter'],
  }}

  // Organization Features
  organization={{}}             // Enable org features

  // Dark Mode
  defaultTheme="system"         // 'light' | 'dark' | 'system'

  // Custom Labels
  localization={{
    SIGN_IN: 'Welcome Back',
    SIGN_UP: 'Create Account',
    FORGOT_PASSWORD: 'Forgot Password?',
    OR_CONTINUE_WITH: 'or continue with',
  }}
>
  {children}
</NeonAuthUIProvider>
```

---

## Server Components (RSC)

### Get Session in Server Component

```typescript
// NO 'use client' - this is a Server Component
import { auth } from '@/lib/auth/server';

// Server components using `auth` methods must be rendered dynamically
export const dynamic = 'force-dynamic'

export async function Profile() {
  const { data: session } = await auth.getSession();

  if (!session?.user) return <div>Not signed in</div>;

  return (
    <div>
      <p>Hello, {session.user.name}</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### Route Handler with Auth

```typescript
// app/api/user/route.ts
import { auth } from '@/lib/auth/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const { data: session } = await auth.getSession();

  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return NextResponse.json({ user: session.user });
}
```

---

## Server Actions

Server actions use the same `auth` instance from `lib/auth/server.ts`:

### Sign In Action

```typescript
// app/actions/auth.ts
'use server';
import { auth } from '@/lib/auth/server';
import { redirect } from 'next/navigation';

export async function signIn(formData: FormData) {
  const { error } = await auth.signIn.email({
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  });

  if (error) {
    return { error: error.message };
  }

  redirect('/dashboard');
}

export async function signUp(formData: FormData) {
  const { error } = await auth.signUp.email({
    email: formData.get('email') as string,
    password: formData.get('password') as string,
    name: formData.get('name') as string,
  });

  if (error) {
    return { error: error.message };
  }

  redirect('/dashboard');
}

export async function signOut() {
  await auth.signOut();
  redirect('/');
}
```

### Available Server Methods

The `auth` instance from `createNeonAuth()` provides all Better Auth server methods:

```typescript
// Authentication
auth.signIn.email({ email, password })
auth.signUp.email({ email, password, name })
auth.signOut()
auth.getSession()

// User Management
auth.updateUser({ name, image })

// Organizations
auth.organization.create({ name, slug })
auth.organization.list()

// Admin (if enabled)
auth.admin.listUsers()
auth.admin.banUser({ userId })
```

---

## Client Components

### Session Hook

```typescript
'use client';
import { authClient } from '@/lib/auth/client';

export function Dashboard() {
  const { data: session, isPending, error } = authClient.useSession();

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!session) return <div>Not signed in</div>;

  return <div>Hello, {session.user.name}</div>;
}
```

### Client-Side Auth Methods

```typescript
'use client';
import { authClient } from '@/lib/auth/client';

// Sign in
await authClient.signIn.email({ email, password });

// Sign up
await authClient.signUp.email({ email, password, name });

// OAuth
await authClient.signIn.social({
  provider: 'google',
  callbackURL: '/dashboard',
});

// Sign out
await authClient.signOut();

// Get session
const session = await authClient.getSession();
```

---

## UI Components

### AuthView - Main Auth Interface

```typescript
import { AuthView } from '@neondatabase/auth/react/ui';

// Handles: sign-in, sign-up, forgot-password, reset-password, callback, sign-out
<AuthView pathname={path} />
```

### Conditional Rendering

```typescript
import {
  SignedIn,
  SignedOut,
  AuthLoading,
  RedirectToSignIn,
} from '@neondatabase/auth/react/ui';

function MyPage() {
  return (
    <>
      <AuthLoading>
        <LoadingSpinner />
      </AuthLoading>

      <SignedIn>
        <Dashboard />
      </SignedIn>

      <SignedOut>
        <LandingPage />
      </SignedOut>

      {/* Auto-redirect if not signed in */}
      <RedirectToSignIn />
    </>
  );
}
```

### UserButton

```typescript
import { UserButton } from '@neondatabase/auth/react/ui';

function Header() {
  return (
    <header>
      <nav>...</nav>
      <UserButton />
    </header>
  );
}
```

### Account Management

```typescript
import {
  AccountSettingsCards,
  SecuritySettingsCards,
  SessionsCard,
  ChangePasswordCard,
  ChangeEmailCard,
  DeleteAccountCard,
  ProvidersCard,
} from '@neondatabase/auth/react/ui';
```

### Organization Components

```typescript
import {
  OrganizationSwitcher,
  OrganizationSettingsCards,
  OrganizationMembersCard,
  AcceptInvitationCard,
} from '@neondatabase/auth/react/ui';
```

---

## Social/OAuth Providers

### Configuration

```typescript
<NeonAuthUIProvider
  social={{
    providers: ['google'],
  }}
>
```

### Programmatic OAuth

```typescript
// Client-side
await authClient.signIn.social({
  provider: 'google',
  callbackURL: '/dashboard',
});
```

### Supported Providers

`google`, `github`, `twitter`, `discord`, `apple`, `microsoft`, `facebook`, `linkedin`, `spotify`, `twitch`, `gitlab`, `bitbucket`

---

## Middleware Configuration

### Basic Protected Routes

```typescript
import { auth } from '@/lib/auth/server';

export default auth.middleware({
  loginUrl: '/auth/sign-in',
});

export const config = {
  matcher: ['/dashboard/:path*', '/account/:path*', '/settings/:path*'],
};
```

### Custom Logic

```typescript
import { auth } from '@/lib/auth/server';
import { NextResponse } from 'next/server';

export default auth.middleware({
  loginUrl: '/auth/sign-in',
});
```

---

## Account Pages Setup

### Account Layout (`app/account/[path]/page.tsx`)

```typescript
import {
  SignedIn,
  RedirectToSignIn,
  AccountSettingsCards,
  SecuritySettingsCards,
  SessionsCard,
  ChangePasswordCard,
} from '@neondatabase/auth/react/ui';

export default async function AccountPage({ params }: { params: Promise<{ path: string }> }) {
  const { path = 'settings' } = await params;

  return (
    <>
      <RedirectToSignIn />
      <SignedIn>
        {path === 'settings' && <AccountSettingsCards />}
        {path === 'security' && (
          <>
            <ChangePasswordCard />
            <SecuritySettingsCards />
          </>
        )}
        {path === 'sessions' && <SessionsCard />}
      </SignedIn>
    </>
  );
}
```

---

## Advanced Features

### Anonymous Access

Enable RLS-based data access for unauthenticated users:

```typescript
// lib/auth/client.ts
'use client';
import { createAuthClient } from '@neondatabase/auth/next';

export const authClient = createAuthClient({
  allowAnonymous: true,
});
```

### Get JWT Token

```typescript
const token = await authClient.getJWTToken();

// Use in API calls
const response = await fetch('/api/data', {
  headers: { Authorization: `Bearer ${token}` },
});
```

### Cross-Tab Sync

Automatic via BroadcastChannel. Sign out in one tab signs out all tabs.

### Session Refresh in Server Components

The `onSessionChange` callback is crucial for Next.js:

```typescript
<NeonAuthUIProvider
  onSessionChange={() => router.refresh()} // Refreshes Server Components!
  // ...
>
```

Without this, Server Components won't update after sign-in/sign-out.

---

## Error Handling

### Server Actions

```typescript
'use server';

export async function signIn(formData: FormData) {
  const { error } = await authServer.signIn.email({
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  });

  if (error) {
    // Return error to client
    return { error: error.message };
  }

  redirect('/dashboard');
}
```

### Client Components

```typescript
'use client';

const { error } = await authClient.signIn.email({ email, password });

if (error) {
  toast.error(error.message);
}
```

### Common Errors

| Error | Cause |
|-------|-------|
| `Invalid credentials` | Wrong email/password |
| `User already exists` | Email already registered |
| `Email not verified` | Verification required |
| `Session not found` | Expired or invalid session |

---

## FAQ / Troubleshooting

### Server Components not updating after sign-in?

Make sure you have `onSessionChange={() => router.refresh()}` in your provider:

```typescript
<NeonAuthUIProvider
  onSessionChange={() => router.refresh()}
  // ...
>
```

### Anonymous access not working?

Grant permissions to the `anonymous` role in your database:

```sql
GRANT SELECT ON public.posts TO anonymous;
GRANT SELECT ON public.products TO anonymous;
```

And configure RLS policies:

```sql
CREATE POLICY "Anyone can read published posts"
  ON public.posts FOR SELECT
  USING (published = true);
```

### Middleware not protecting routes?

Check your `matcher` configuration:

```typescript
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/account/:path*',
    // Add your protected routes here
  ],
};
```

### OAuth callback errors?

Ensure your API route is set up correctly at `app/api/auth/[...path]/route.ts`:

```typescript
import { auth } from '@/lib/auth/server';
export const { GET, POST } = auth.handler();
```

### Session not persisting?

1. Check cookies are enabled
2. Verify `NEON_AUTH_BASE_URL` is correct in `.env.local`
3. Verify `NEON_AUTH_COOKIE_SECRET` is set and at least 32 characters
4. Make sure you're not in incognito with cookies blocked

### Session data cache not working?

1. Verify `NEON_AUTH_COOKIE_SECRET` is at least 32 characters long
2. Check `cookies.secret` is passed to `createNeonAuth()`
3. Optionally configure `cookies.sessionDataTtl` (default: 300 seconds)

---

## Performance Notes

- **Session data caching**: JWT-signed `session_data` cookie with configurable TTL (default: 5 minutes)
  - Configure via `cookies.sessionDataTtl` in seconds
  - Enables sub-millisecond session lookups (<1ms)
  - Automatic fallback to upstream `/get-session` on cache miss
- **Request deduplication**: Concurrent calls share single network request (10x faster cold starts)
- **Server Components**: Use `auth.getSession()` for zero-JS session access
- **Cross-tab sync**: <50ms via BroadcastChannel
- **Cookie domain**: Optional `cookies.domain` for cross-subdomain cookie sharing
