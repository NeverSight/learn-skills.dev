---
name: supabase-auth-ssr-setup
description: This skill should be used when configuring Supabase Auth for server-side rendering with Next.js App Router, including secure cookie handling, middleware protection, route guards, authentication utilities, and logout flow. Apply when setting up SSR auth, adding protected routes, implementing middleware authentication, configuring secure sessions, or building login/logout flows with Supabase.
---

# Supabase Auth SSR Setup

## Overview

Configure Supabase Authentication for Next.js App Router with server-side rendering (SSR), secure cookie-based sessions, middleware protection, and complete authentication flows.

## Installation and Configuration Steps

### 1. Install Dependencies

Install Supabase SSR package for Next.js:

```bash
npm install @supabase/supabase-js @supabase/ssr
```

### 2. Create Supabase Client Utilities

Create three client configurations for different contexts (browser, server, middleware):

**File: `lib/supabase/client.ts`** (Browser client)

Use the template from `assets/supabase-client.ts`. This client:
- Runs only in browser context
- Uses secure cookies for session storage
- Automatically refreshes tokens

**File: `lib/supabase/server.ts`** (Server component client)

Use the template from `assets/supabase-server.ts`. This client:
- Creates server-side Supabase client with cookie access
- Used in Server Components and Server Actions
- Provides read-only cookie access for security

**File: `lib/supabase/middleware.ts`** (Middleware client)

Use the template from `assets/supabase-middleware.ts`. This client:
- Used in Next.js middleware for route protection
- Can update cookies in responses
- Refreshes sessions on route navigation

### 3. Configure Environment Variables

Add Supabase credentials to `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

Get these values from your Supabase project settings under API.

**Security note**: The anon key is safe to expose publicly. Real security comes from Row Level Security (RLS) policies in your database.

### 4. Create Middleware for Route Protection

Create `middleware.ts` in project root using the template from `assets/middleware.ts`. This middleware:

- Refreshes Supabase session on every request
- Protects routes matching specified patterns
- Redirects unauthenticated users to login
- Allows public routes to bypass authentication

Configure protected routes by adjusting the matcher pattern:

```typescript
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/settings/:path*',
    '/api/protected/:path*',
  ],
};
```

### 5. Create Authentication Utilities

Create helper functions for common auth operations using templates from `assets/auth-utils.ts`:

**Get current user server-side**:
```typescript
import { getCurrentUser } from '@/lib/auth/utils';

const user = await getCurrentUser();
```

**Require authentication**:
```typescript
import { requireAuth } from '@/lib/auth/utils';

const user = await requireAuth(); // Throws error if not authenticated
```

**Get session**:
```typescript
import { getSession } from '@/lib/auth/utils';

const session = await getSession();
```

These utilities simplify authentication checks in Server Components and Server Actions.

### 6. Create Logout Server Action

Create `app/actions/auth.ts` using the template from `assets/auth-actions.ts`. This provides:

**Logout action**:
- Clears Supabase session
- Removes auth cookies
- Redirects to home page

Use in client components:

```typescript
import { logout } from '@/app/actions/auth';

<button onClick={() => logout()}>
  Sign Out
</button>
```

### 7. Create Login Page

Create `app/login/page.tsx` using the template from `assets/login-page.tsx`. This page:

- Provides email/password login form
- Handles magic link authentication
- Supports OAuth providers (Google, GitHub, etc.)
- Redirects authenticated users
- Shows error messages

Customize the login page:
- Add your branding and styling
- Enable/disable OAuth providers
- Add password reset link
- Include sign-up link

### 8. Create Protected Route Example

Create a protected dashboard page at `app/dashboard/page.tsx` using the template from `assets/dashboard-page.tsx`. This demonstrates:

- Using `requireAuth()` to protect routes
- Displaying user information
- Including logout functionality
- Server-side authentication check

### 9. Set Up Callback Route for OAuth

If using OAuth providers, create `app/auth/callback/route.ts` using the template from `assets/auth-callback-route.ts`. This handler:

- Exchanges OAuth code for session
- Sets secure session cookies
- Redirects to intended destination
- Handles OAuth errors

Configure OAuth in Supabase dashboard:
1. Go to Authentication > Providers
2. Enable desired providers (Google, GitHub, etc.)
3. Add redirect URL: `https://your-domain.com/auth/callback`

## Authentication Flow

### Login Flow

1. User visits `/login`
2. User enters credentials or clicks OAuth
3. Supabase authenticates and sets session cookie
4. User redirected to dashboard or intended page
5. Middleware validates session on protected routes

### Session Refresh Flow

1. User navigates to any route
2. Middleware runs and refreshes session if needed
3. Updated session cookie sent to client
4. Server Components have access to fresh session

### Logout Flow

1. User clicks logout button
2. Server Action calls Supabase `signOut()`
3. Session and cookies cleared
4. User redirected to home page

## Route Protection Patterns

### Protecting Individual Pages

Use `requireAuth()` at the top of Server Components:

```typescript
import { requireAuth } from '@/lib/auth/utils';

export default async function ProtectedPage() {
  const user = await requireAuth();

  return <div>Hello {user.email}</div>;
}
```

### Protecting Route Groups

Use Next.js route groups with layout:

```typescript
// app/(protected)/layout.tsx
import { requireAuth } from '@/lib/auth/utils';

export default async function ProtectedLayout({ children }) {
  await requireAuth();
  return <>{children}</>;
}
```

All routes in `(protected)` group are automatically protected.

### Optional Authentication

Check if user is logged in without requiring it:

```typescript
import { getCurrentUser } from '@/lib/auth/utils';

export default async function OptionalAuthPage() {
  const user = await getCurrentUser();

  return (
    <div>
      {user ? `Welcome ${user.email}` : 'Please log in'}
    </div>
  );
}
```

## Server Actions with Authentication

Protect Server Actions using `requireAuth()`:

```typescript
'use server';

import { requireAuth } from '@/lib/auth/utils';
import { createServerClient } from '@/lib/supabase/server';

export async function updateProfile(formData: FormData) {
  const user = await requireAuth();
  const supabase = createServerClient();

  const { error } = await supabase
    .from('profiles')
    .update({ name: formData.get('name') })
    .eq('id', user.id);

  if (error) throw error;
}
```

## Troubleshooting

**Session not persisting**: Verify cookies are being set. Check browser dev tools > Application > Cookies. Ensure domain matches.

**Middleware redirect loop**: Check matcher pattern doesn't include login page. Verify `/login` is accessible without auth.

**OAuth redirect fails**: Confirm callback URL matches exactly in Supabase dashboard. Check for trailing slashes.

**TypeScript errors**: Install types: `npm install -D @types/node`. Ensure `supabase` is typed correctly.

**401 errors on protected routes**: Session may be expired. Check Supabase dashboard > Authentication > Settings for session timeout.

## Resources

### scripts/

No executable scripts needed for this skill.

### references/

- `authentication-patterns.md` - Common auth patterns and best practices for Next.js + Supabase
- `security-considerations.md` - Security best practices for session handling and cookie configuration

### assets/

- `supabase-client.ts` - Browser-side Supabase client configuration
- `supabase-server.ts` - Server-side Supabase client for Server Components
- `supabase-middleware.ts` - Middleware Supabase client for session refresh
- `middleware.ts` - Next.js middleware for route protection
- `auth-utils.ts` - Helper functions for authentication checks
- `auth-actions.ts` - Server Actions for logout and other auth operations
- `login-page.tsx` - Complete login page with email/password and OAuth
- `dashboard-page.tsx` - Example protected page using requireAuth
- `auth-callback-route.ts` - OAuth callback handler for provider authentication
