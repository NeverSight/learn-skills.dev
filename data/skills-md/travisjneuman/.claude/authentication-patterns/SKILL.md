---
name: authentication-patterns
description: OAuth 2.0, JWT, SSO, MFA, NextAuth/Clerk/Supabase Auth implementation patterns
---

# Authentication Patterns

## Overview

This skill covers authentication and authorization implementation across web and mobile applications. It addresses OAuth 2.0 flows (Authorization Code with PKCE, Client Credentials), JWT management (access tokens, refresh tokens, rotation), session management strategies, multi-factor authentication (TOTP, WebAuthn/passkeys), integration with auth libraries (NextAuth/Auth.js v5, Clerk, Supabase Auth, Lucia), SSO protocols (SAML, OIDC), and authorization patterns (RBAC, ABAC).

Use this skill when building login/signup flows, integrating social login providers, implementing MFA, setting up SSO for enterprise customers, designing authorization models, or migrating between auth providers.

---

## Core Principles

1. **Never roll your own crypto** - Use established libraries for password hashing (bcrypt, argon2), JWT signing, and OAuth flows. Custom auth code is the #1 source of security vulnerabilities in web applications.
2. **Defense in depth** - Authentication is not a single check. Layer session validation, CSRF protection, rate limiting, and anomaly detection. Assume every layer can be bypassed individually.
3. **Tokens are credentials** - Access tokens, refresh tokens, and session cookies must be stored securely (httpOnly cookies, encrypted storage), transmitted over HTTPS only, and rotated regularly.
4. **Least privilege by default** - Users and API clients should start with minimal permissions. Elevate access through explicit role assignment, never through implicit trust.
5. **Plan for account recovery** - Password reset, MFA recovery codes, email verification, and account lockout all need designed flows. These are more complex than the happy-path login.

---

## Key Patterns

### Pattern 1: NextAuth (Auth.js v5) with OAuth and Database Sessions

**When to use:** Next.js applications needing social login, email/password, or magic link authentication with server-side session management.

**Implementation:**

```typescript
// auth.ts - Auth.js v5 configuration
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";
import { verifyPassword } from "@/lib/password";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
    Google({
      clientId: process.env.GOOGLE_ID!,
      clientSecret: process.env.GOOGLE_SECRET!,
    }),
    Credentials({
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });

        if (!user?.passwordHash) return null;

        const valid = await verifyPassword(
          credentials.password as string,
          user.passwordHash
        );

        if (!valid) return null;

        return { id: user.id, email: user.email, name: user.name };
      },
    }),
  ],
  session: {
    strategy: "database", // Server-side sessions (not JWT)
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // Refresh session every 24 hours
  },
  callbacks: {
    async session({ session, user }) {
      // Add user role to session
      session.user.id = user.id;
      session.user.role = user.role;
      return session;
    },
    async signIn({ user, account }) {
      // Block sign-in for disabled accounts
      if (user.id) {
        const dbUser = await prisma.user.findUnique({
          where: { id: user.id },
        });
        if (dbUser?.disabled) return false;
      }
      return true;
    },
  },
  pages: {
    signIn: "/login",
    error: "/auth/error",
    verifyRequest: "/auth/verify",
  },
});
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";
export const { GET, POST } = handlers;
```

```typescript
// Middleware for route protection
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isAuthPage = req.nextUrl.pathname.startsWith("/login") ||
                     req.nextUrl.pathname.startsWith("/register");
  const isDashboard = req.nextUrl.pathname.startsWith("/dashboard");

  if (isDashboard && !isLoggedIn) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  if (isAuthPage && isLoggedIn) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/register"],
};
```

**Why:** Auth.js v5 handles OAuth complexity (state parameters, PKCE, token exchange), session management, CSRF protection, and provider-specific quirks. Database sessions are more secure than JWT sessions because they can be revoked instantly and don't expose claims to the client.

---

### Pattern 2: JWT Access/Refresh Token Pattern

**When to use:** API authentication for SPAs, mobile apps, or microservice-to-microservice communication where stateless verification is needed.

**Implementation:**

```typescript
// Token generation
import jwt from "jsonwebtoken";
import { randomBytes } from "crypto";

interface TokenPayload {
  sub: string; // User ID
  email: string;
  role: string;
}

interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

const ACCESS_TOKEN_EXPIRY = "15m";
const REFRESH_TOKEN_EXPIRY = "7d";

function generateTokenPair(user: TokenPayload): TokenPair {
  const accessToken = jwt.sign(
    { sub: user.sub, email: user.email, role: user.role },
    process.env.JWT_SECRET!,
    {
      expiresIn: ACCESS_TOKEN_EXPIRY,
      issuer: "myapp",
      audience: "myapp-api",
    }
  );

  // Refresh token is opaque (not JWT) - stored server-side
  const refreshToken = randomBytes(64).toString("hex");

  return {
    accessToken,
    refreshToken,
    expiresIn: 900, // 15 minutes in seconds
  };
}

// Token refresh endpoint
async function refreshTokens(refreshToken: string): Promise<TokenPair> {
  // 1. Look up refresh token in database
  const stored = await db.refreshToken.findUnique({
    where: { token: hashToken(refreshToken) },
    include: { user: true },
  });

  if (!stored || stored.expiresAt < new Date()) {
    throw new UnauthorizedError("Invalid or expired refresh token");
  }

  // 2. Rotate refresh token (invalidate old, create new)
  await db.refreshToken.delete({ where: { id: stored.id } });

  const newPair = generateTokenPair({
    sub: stored.user.id,
    email: stored.user.email,
    role: stored.user.role,
  });

  // 3. Store new refresh token
  await db.refreshToken.create({
    data: {
      token: hashToken(newPair.refreshToken),
      userId: stored.user.id,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    },
  });

  return newPair;
}

// Token verification middleware
function verifyAccessToken(token: string): TokenPayload {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!, {
      issuer: "myapp",
      audience: "myapp-api",
    });
    return decoded as TokenPayload;
  } catch (err) {
    if (err instanceof jwt.TokenExpiredError) {
      throw new UnauthorizedError("Access token expired");
    }
    throw new UnauthorizedError("Invalid access token");
  }
}
```

```typescript
// Secure cookie-based token delivery (for web apps)
function setAuthCookies(res: Response, tokens: TokenPair): void {
  // Access token in httpOnly cookie
  res.headers.append(
    "Set-Cookie",
    `access_token=${tokens.accessToken}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=${tokens.expiresIn}`
  );

  // Refresh token in httpOnly cookie with restricted path
  res.headers.append(
    "Set-Cookie",
    `refresh_token=${tokens.refreshToken}; HttpOnly; Secure; SameSite=Strict; Path=/api/auth/refresh; Max-Age=${7 * 24 * 60 * 60}`
  );
}
```

**Why:** Short-lived access tokens (15 minutes) limit the damage window if a token is stolen. Opaque refresh tokens stored server-side can be revoked immediately (unlike JWTs). Refresh token rotation detects token theft: if a stolen refresh token is used after the legitimate user has already rotated it, the entire token family is invalidated.

---

### Pattern 3: Multi-Factor Authentication (TOTP)

**When to use:** When you need an additional authentication factor beyond password, especially for admin accounts and sensitive operations.

**Implementation:**

```typescript
// MFA setup flow
import { authenticator } from "otplib";
import QRCode from "qrcode";

// Step 1: Generate secret and QR code for user
async function setupMFA(userId: string): Promise<{ qrCodeUrl: string; secret: string }> {
  const secret = authenticator.generateSecret();

  const user = await db.user.findUniqueOrThrow({ where: { id: userId } });

  // Store encrypted secret (not yet verified)
  await db.mfaSetup.upsert({
    where: { userId },
    create: { userId, secret: encrypt(secret), verified: false },
    update: { secret: encrypt(secret), verified: false },
  });

  const otpauth = authenticator.keyuri(user.email, "MyApp", secret);
  const qrCodeUrl = await QRCode.toDataURL(otpauth);

  return { qrCodeUrl, secret };
}

// Step 2: Verify code to complete setup
async function verifyMFASetup(userId: string, code: string): Promise<string[]> {
  const setup = await db.mfaSetup.findUniqueOrThrow({
    where: { userId },
  });

  const secret = decrypt(setup.secret);
  const isValid = authenticator.verify({ token: code, secret });

  if (!isValid) {
    throw new ValidationError("Invalid verification code");
  }

  // Generate recovery codes
  const recoveryCodes = Array.from({ length: 10 }, () =>
    randomBytes(4).toString("hex").toUpperCase()
  );

  // Store hashed recovery codes
  await db.$transaction([
    db.mfaSetup.update({
      where: { userId },
      data: { verified: true },
    }),
    db.user.update({
      where: { id: userId },
      data: { mfaEnabled: true },
    }),
    ...recoveryCodes.map((code) =>
      db.recoveryCode.create({
        data: { userId, codeHash: hashCode(code) },
      })
    ),
  ]);

  return recoveryCodes; // Show to user ONCE
}

// Step 3: Verify TOTP during login
async function verifyMFA(userId: string, code: string): Promise<boolean> {
  const setup = await db.mfaSetup.findUniqueOrThrow({
    where: { userId, verified: true },
  });

  const secret = decrypt(setup.secret);

  // Check TOTP code (allows 1 window of drift)
  if (authenticator.verify({ token: code, secret })) {
    return true;
  }

  // Check recovery codes
  const recoveryCodes = await db.recoveryCode.findMany({
    where: { userId, used: false },
  });

  for (const rc of recoveryCodes) {
    if (await verifyHash(code, rc.codeHash)) {
      // Mark recovery code as used (one-time use)
      await db.recoveryCode.update({
        where: { id: rc.id },
        data: { used: true, usedAt: new Date() },
      });
      return true;
    }
  }

  return false;
}
```

**Why:** TOTP-based MFA is widely supported (Google Authenticator, Authy, 1Password), doesn't require SMS (which is vulnerable to SIM swapping), and works offline. Recovery codes provide a safety net when users lose their authenticator device. The encrypted secret and hashed recovery codes protect against database breaches.

---

### Pattern 4: Role-Based Access Control (RBAC)

**When to use:** When different users need different levels of access to resources.

**Implementation:**

```typescript
// Permission definitions
const PERMISSIONS = {
  // Projects
  "project:read": "View project details",
  "project:write": "Edit project settings",
  "project:delete": "Delete projects",
  "project:manage_members": "Add/remove project members",

  // Billing
  "billing:read": "View billing information",
  "billing:write": "Manage subscriptions and payments",

  // Admin
  "admin:users": "Manage all users",
  "admin:settings": "Manage organization settings",
} as const;

type Permission = keyof typeof PERMISSIONS;

// Role definitions
const ROLES: Record<string, Permission[]> = {
  viewer: ["project:read"],
  editor: ["project:read", "project:write"],
  admin: [
    "project:read",
    "project:write",
    "project:delete",
    "project:manage_members",
    "billing:read",
    "billing:write",
  ],
  owner: Object.keys(PERMISSIONS) as Permission[],
};

// Permission check middleware
function requirePermission(...requiredPermissions: Permission[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    if (!user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const userPermissions = ROLES[user.role] ?? [];
    const hasAllPermissions = requiredPermissions.every((p) =>
      userPermissions.includes(p)
    );

    if (!hasAllPermissions) {
      return res.status(403).json({
        error: "Insufficient permissions",
        required: requiredPermissions,
        current: user.role,
      });
    }

    next();
  };
}

// Usage in routes
app.get("/api/projects/:id", requirePermission("project:read"), getProject);
app.put("/api/projects/:id", requirePermission("project:write"), updateProject);
app.delete("/api/projects/:id", requirePermission("project:delete"), deleteProject);

// Component-level permission checks (React)
function usePermission(permission: Permission): boolean {
  const { data: session } = useSession();
  if (!session?.user?.role) return false;
  const permissions = ROLES[session.user.role] ?? [];
  return permissions.includes(permission);
}

function ProjectSettings({ project }: { project: Project }) {
  const canEdit = usePermission("project:write");
  const canDelete = usePermission("project:delete");

  return (
    <div>
      <h2>Settings</h2>
      {canEdit ? (
        <ProjectForm project={project} />
      ) : (
        <ProjectDetails project={project} />
      )}
      {canDelete && <DeleteProjectButton projectId={project.id} />}
    </div>
  );
}
```

**Why:** RBAC provides a clear, auditable permission model. Defining permissions as constants with TypeScript ensures compile-time safety. Checking permissions on both server (middleware) and client (UI) provides defense in depth -- the server enforces security, the client provides user experience.

---

## Password Hashing Reference

| Algorithm | Recommended | Cost Factor | Notes |
|---|---|---|---|
| **argon2id** | Best | Memory: 64MB, Iterations: 3 | Best protection against GPU/ASIC attacks |
| **bcrypt** | Good | Rounds: 12-14 | Widely supported, proven track record |
| **scrypt** | Good | N: 2^15, r: 8, p: 1 | Memory-hard, good alternative to argon2 |
| **PBKDF2** | Acceptable | Iterations: 600,000+ (SHA-256) | NIST recommended, but not memory-hard |
| **MD5/SHA-256** | Never | N/A | Not a password hash -- too fast, no salt |

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|---|---|---|
| Storing passwords in plain text | Single breach exposes all passwords | Use argon2id or bcrypt with per-user salt |
| JWT in localStorage | XSS can steal tokens | httpOnly Secure cookies |
| Long-lived access tokens (days/weeks) | Extended damage window if stolen | 15-minute access tokens + refresh token rotation |
| Checking permissions only on the client | Client-side checks are bypassable | Server-side middleware + client-side UX |
| Custom OAuth implementation | Subtle security bugs (state, PKCE, redirect) | Use established libraries (Auth.js, Passport) |
| SMS-based 2FA as only MFA option | SIM swapping vulnerability | Offer TOTP and WebAuthn alongside SMS |
| No rate limiting on login endpoint | Brute force attacks | Rate limit by IP and username |
| Password reset tokens that don't expire | Token can be used indefinitely | 1-hour expiry, single-use, invalidate on password change |

---

## Checklist

- [ ] Passwords hashed with argon2id or bcrypt (never plain text, never MD5/SHA)
- [ ] OAuth flows use PKCE for public clients (SPAs, mobile)
- [ ] Access tokens are short-lived (< 30 minutes)
- [ ] Refresh tokens are rotated on use and stored server-side
- [ ] Tokens delivered in httpOnly Secure SameSite cookies (web)
- [ ] Login endpoint rate-limited (by IP and username)
- [ ] MFA available for all users, enforced for admin roles
- [ ] Recovery codes generated during MFA setup
- [ ] RBAC permissions checked on server (middleware) and client (UX)
- [ ] Password reset tokens expire in 1 hour, single-use
- [ ] Account lockout after N failed attempts (with progressive delay)
- [ ] Session invalidation on password change

---

## Related Resources

- **Skills:** `application-security` (OWASP auth vulnerabilities), `payment-integration` (billing auth)
- **Skills:** `email-systems` (password reset emails), `product-analytics` (identify/alias on auth)
- **Rules:** `rules/stacks/fullstack-nextjs-nestjs.md` (NestJS auth guards)
