---
name: auth-route-protection-checker
description: This skill should be used when the user requests to audit, check, or generate authentication and authorization protection for Next.js routes, server components, API routes, and server actions. It analyzes existing routes for missing auth checks and generates protection logic based on user roles and permissions. Trigger terms include auth check, route protection, protect routes, secure endpoints, auth middleware, role-based routes, authorization check, api security, server action security, protect pages.
allowed-tools: Read, Grep, Glob, Bash
---

# Auth Route Protection Checker

To audit and enhance authentication protection across Next.js routes, server components, and API routes, follow these steps systematically.

## Step 1: Discover Project Structure

Identify all files that need authentication checks:

1. Use Glob to find all route files:
   - `app/**/page.tsx` - Page components
   - `app/**/route.ts` - API routes
   - `app/**/layout.tsx` - Layout components
   - `lib/actions/**/*.ts` - Server actions

2. Read middleware configuration:
   - `middleware.ts` - Current middleware setup
   - `next.config.js` - Route configuration

3. Identify authentication setup:
   - Search for auth client files (Supabase, NextAuth, Clerk, etc.)
   - Find auth utility functions

## Step 2: Analyze Current Protection

For each discovered file, check for existing auth protection:

### Check for Authentication Patterns

Use Grep to search for:
```
- "auth.getUser()"
- "getSession()"
- "currentUser()"
- "requireAuth"
- "redirect.*login"
- "unauthorized"
- "createServerClient"
```

### Identify Protection Gaps

Flag files that:
- Have no auth checks
- Are in protected routes but lack verification
- Accept user input without auth validation
- Perform privileged operations without role checks

Consult `references/protection-patterns.md` for common patterns.

## Step 3: Categorize Routes by Protection Level

Classify routes into security categories:

**Public Routes** - No auth required:
- Landing pages
- Marketing content
- Public blog posts
- Login/signup pages

**Authenticated Routes** - Login required:
- User dashboard
- Profile pages
- User-specific data

**Role-Protected Routes** - Specific roles required:
- Admin panels
- Moderator tools
- Premium features

**Action-Protected Routes** - Specific permissions required:
- Edit operations
- Delete operations
- Admin actions

## Step 4: Generate Protection Report

Create a comprehensive audit report:

```markdown
# Route Protection Audit Report

Generated: [timestamp]

## Summary
- Total Routes: X
- Protected: Y
- Unprotected: Z
- Needs Review: N

## Unprotected Routes

### Critical (Requires immediate attention)
- [ ] /app/admin/page.tsx - Admin panel with no auth check
- [ ] /app/api/users/delete/route.ts - Delete endpoint unprotected

### High Priority
- [ ] /app/dashboard/page.tsx - User dashboard missing auth
- [ ] /app/api/data/route.ts - API route needs auth

### Medium Priority
- [ ] /app/profile/page.tsx - Profile page needs verification

### Low Priority (Review recommended)
- [ ] /app/about/page.tsx - Consider if auth needed

## Protected Routes

### Properly Protected
- [x] /app/(protected)/settings/page.tsx - Has auth check
- [x] /app/api/auth/logout/route.ts - Auth verified

### Needs Enhancement
- [~] /app/admin/users/page.tsx - Has auth but no role check
- [~] /app/api/posts/route.ts - Auth exists but no rate limiting
```

## Step 5: Generate Protection Code

For each unprotected route, generate appropriate protection code:

### Server Component Protection

```typescript
// app/protected-page/page.tsx
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const supabase = createServerClient()

  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }

  // Optional: Role check
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'admin') {
    redirect('/unauthorized')
  }

  return <div>Protected Content</div>
}
```

### API Route Protection

```typescript
// app/api/protected/route.ts
import { createServerClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const supabase = createServerClient()

  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  // Optional: Role-based access
  const userRole = user.user_metadata?.role

  if (userRole !== 'admin') {
    return NextResponse.json(
      { error: 'Forbidden - Admin access required' },
      { status: 403 }
    )
  }

  // Protected logic here
  return NextResponse.json({ data: 'protected data' })
}
```

### Server Action Protection

```typescript
// lib/actions/admin.ts
'use server'

import { createServerClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'

export async function deleteUser(userId: string) {
  const supabase = createServerClient()

  // Auth check
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    throw new Error('Unauthorized')
  }

  // Role check
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'admin') {
    throw new Error('Forbidden - Admin access required')
  }

  // Permission check (optional)
  const canDeleteUsers = await checkPermission(user.id, 'users:delete')
  if (!canDeleteUsers) {
    throw new Error('Insufficient permissions')
  }

  // Perform action
  const { error: deleteError } = await supabase
    .from('users')
    .delete()
    .eq('id', userId)

  if (deleteError) throw deleteError

  revalidatePath('/admin/users')
}
```

### Middleware Protection

```typescript
// middleware.ts
import { createServerClient } from '@/lib/supabase/middleware'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  const response = NextResponse.next()
  const supabase = createServerClient(request, response)

  const { data: { user } } = await supabase.auth.getUser()

  // Protected routes
  const protectedRoutes = ['/dashboard', '/profile', '/settings']
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  )

  if (isProtectedRoute && !user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Admin routes
  const adminRoutes = ['/admin']
  const isAdminRoute = adminRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  )

  if (isAdminRoute) {
    if (!user) {
      return NextResponse.redirect(new URL('/login', request.url))
    }

    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', user.id)
      .single()

    if (profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url))
    }
  }

  return response
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/profile/:path*',
    '/settings/:path*',
    '/admin/:path*',
  ]
}
```

## Step 6: Generate Helper Functions

Create reusable auth utilities using templates from `assets/auth-helpers.ts`:

```typescript
// lib/auth/helpers.ts
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function requireAuth() {
  const supabase = createServerClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }

  return user
}

export async function requireRole(allowedRoles: string[]) {
  const user = await requireAuth()

  const supabase = createServerClient()
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()

  if (!profile || !allowedRoles.includes(profile.role)) {
    redirect('/unauthorized')
  }

  return { user, role: profile.role }
}

export async function checkPermission(
  userId: string,
  permission: string
): Promise<boolean> {
  const supabase = createServerClient()

  const { data } = await supabase
    .from('user_permissions')
    .select('permission')
    .eq('user_id', userId)
    .eq('permission', permission)
    .single()

  return !!data
}
```

## Step 7: Create Testing Suite

Generate tests to verify protection works:

Use templates from `assets/auth-tests.ts`:

```typescript
// tests/auth-protection.test.ts
import { describe, it, expect } from 'vitest'
import { GET } from '@/app/api/protected/route'

describe('Route Protection', () => {
  it('returns 401 for unauthenticated requests', async () => {
    const request = new Request('http://localhost/api/protected')
    const response = await GET(request)

    expect(response.status).toBe(401)
  })

  it('returns 403 for unauthorized role', async () => {
    // Mock auth with non-admin user
    const response = await GET(mockRequestWithUser({ role: 'user' }))

    expect(response.status).toBe(403)
  })

  it('allows access for admin users', async () => {
    const response = await GET(mockRequestWithUser({ role: 'admin' }))

    expect(response.status).toBe(200)
  })
})
```

## Step 8: Generate Documentation

Create documentation for the protection system:

```markdown
# Authentication & Authorization Guide

## Overview
This application uses [Auth Provider] for authentication and role-based access control.

## Route Protection Levels

### Public Routes
- No authentication required
- Accessible to all visitors
- Examples: /, /about, /login

### Authenticated Routes
- Requires user login
- No specific role needed
- Examples: /dashboard, /profile

### Role-Protected Routes
- Requires specific role(s)
- Examples: /admin (admin role)

### Permission-Protected Routes
- Requires specific permissions
- Granular access control
- Examples: /admin/delete-user (users:delete permission)

## Implementation Patterns

[Include code examples and usage guidelines]
```

## Step 9: Suggest Improvements

Based on the audit, suggest security enhancements:

1. **Middleware Coverage**: Routes missing from middleware config
2. **Consistent Patterns**: Inconsistent auth check implementations
3. **Error Handling**: Better error messages and redirects
4. **Rate Limiting**: API routes needing rate limits
5. **CSRF Protection**: Forms needing CSRF tokens
6. **Audit Logging**: Privileged actions needing logging

Consult `references/security-best-practices.md` for recommendations.

## Implementation Guidelines

### Best Practices
- Always check auth on server side, never trust client
- Use middleware for route-based protection
- Add role/permission checks for sensitive operations
- Implement proper error handling and redirects
- Log authentication failures and suspicious activity
- Use HTTPS in production
- Implement rate limiting on auth endpoints

### Common Patterns

Consult `references/protection-patterns.md` for:
- Server component auth checks
- API route protection
- Server action security
- Middleware configuration
- Role-based access control
- Permission-based access control

## Output Format

Generate files:
```
reports/
  auth-audit-[timestamp].md
security/
  auth-helpers.ts (if missing)
  middleware.ts (enhanced version)
tests/
  auth-protection.test.ts
docs/
  auth-guide.md
```

## Verification Checklist

Before completing:
- [ ] All routes categorized by protection level
- [ ] Critical unprotected routes identified
- [ ] Protection code generated for gaps
- [ ] Helper functions created/updated
- [ ] Middleware configured correctly
- [ ] Tests cover auth scenarios
- [ ] Documentation updated

## Consulting References

Throughout analysis:
- Consult `references/protection-patterns.md` for auth patterns
- Consult `references/security-best-practices.md` for guidelines
- Use templates from `assets/auth-helpers.ts`
- Use test templates from `assets/auth-tests.ts`

## Completion

When finished:
1. Display audit report summary
2. Highlight critical issues
3. Provide generated protection code
4. List implementation steps
5. Offer to apply fixes or provide guidance
