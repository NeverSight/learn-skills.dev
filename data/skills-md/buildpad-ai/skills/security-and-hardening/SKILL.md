---
name: security-and-hardening
description: Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.
---

# Security and Hardening

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

## Overview

Security-first development practices for web applications. Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory. Security isn't a phase — it's a constraint on every line of code that touches user data, authentication, or external systems.

## When to Use

- Building anything that accepts user input
- Implementing authentication or authorization
- Storing or transmitting sensitive data
- Integrating with external APIs or services
- Adding file uploads, webhooks, or callbacks
- Handling payment or PII data

## The Three-Tier Boundary System

### Always Do (No Exceptions)

- **Validate all external input** at the system boundary (API routes, form handlers)
<!-- buildpad-backend: supabase -->
- **Parameterize all database queries** — never concatenate user input into SQL
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- **Query through the API, never with SQL** — the Engine refuses caller-supplied SQL; pass user input only as values of its API's `filter`, `sort` and `search` parameters
<!-- /buildpad-backend -->
- **Encode output** to prevent XSS (use framework auto-escaping, don't bypass it)
- **Use HTTPS** for all external communication
<!-- buildpad-backend: supabase -->
- **Hash passwords** with bcrypt/scrypt/argon2 (never store plaintext)
- **Set security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- **Use httpOnly, secure, sameSite cookies** for sessions
- **Run `npm audit`** (or `pnpm audit`) before every release

### Ask First (Requires Human Approval)

- Adding new authentication flows or changing auth logic
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- **Never store or hash passwords in the application** — on an Engine project the Engine holds every password; the application signs users in through it
- **Set security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- **Use httpOnly, secure, sameSite cookies** for the application's own session; the Engine itself takes only `Authorization: Bearer <access token>`, never a cookie
- **Run `npm audit`** (or `pnpm audit`) before every release

### Ask First (Requires Human Approval)

- Changing how the application signs users in (sign-up, magic links, password recovery and OAuth sign-in with any provider other than XAppHub are not available on an Engine project: tell the developer so instead of building one; XAppHub sign-in follows the `add-external-oauth` skill)
<!-- /buildpad-backend -->
- Storing new categories of sensitive data (PII, payment info)
- Adding new external service integrations
- Changing CORS configuration
- Adding file upload handlers
- Modifying rate limiting or throttling
- Granting elevated permissions or roles

### Never Do

- **Never commit secrets** to version control (API keys, passwords, tokens)
- **Never log sensitive data** (passwords, tokens, full credit card numbers)
- **Never trust client-side validation** as a security boundary
- **Never disable security headers** for convenience
- **Never use `eval()` or `innerHTML`** with user-provided data
- **Never store sessions in client-accessible storage** (localStorage for auth tokens)
- **Never expose stack traces** or internal error details to users

## DaaS-Specific Security

<!-- buildpad-backend: supabase -->
### Proxy Pattern Enforcement

```
❌ Browser → DaaS Backend (CORS issues, token exposure)
❌ Browser → supabase.auth.signIn() (cookie issues)
✅ Browser → /api/auth/login → Supabase Auth
✅ Browser → /api/items/* → DaaS Backend
```

### Environment Variables

```env
# Server-side only (NEVER prefix with NEXT_PUBLIC_)
SUPABASE_SERVICE_ROLE_KEY=...

# Client-safe (only non-sensitive values)
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
NEXT_PUBLIC_BUILDPAD_DAAS_URL=...
```

### CORS Configuration

```typescript
// DaaS CORS must use explicit origins when credentials: 'include' is used
// NEVER use cors_origins: ["*"] with credentials
{
  cors_origins: [
    "http://localhost:3000",
    "https://main.d1234abcde.amplifyapp.com"
  ],
  cors_allow_credentials: true,
  cors_max_age: 0  // bust cached preflight during changes
}
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Proxy Pattern Enforcement

```
✅ Browser → /api/auth/login (the application's own route) → Engine sign-in, naming the tenant with X-Tenant-Id
✅ Browser → /api/items/* (the application's own route) → Engine, with Authorization: Bearer <access token>
✅ Browser → SDK → Engine, with Authorization: Bearer <access token>
❌ Any call to the Engine with cookies
❌ The MCP token, or any administrator token, on the data API
```

On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.

On an Engine project the Supabase client is kept for sign-in only. Password sign-in, session refresh, reading the signed-in user and sign-out work through it, and its default sign-out ends the user's sessions on every device. An account that holds no role in the project's tenant is refused at password sign-in. XAppHub sign-in also works through it while the project's XAppHub connector is connected: the application's server gives the ID token from XAppHub to `signInWithIdToken` with the provider `my-apps`, and ends the session of an account that holds no role yet (the `add-external-oauth` skill). Not available on an Engine project: sign-up; OAuth sign-in with any provider other than XAppHub; magic link and one-time code; password recovery; changing a password, an email or a profile through the Supabase client; the Supabase client's code exchange; and the Supabase administration API. The Platform's password-less handoff opens the Studio; it is not a way for an application to sign a user in.

### Environment Variables

On an Engine project the environment is: `NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>`, `NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>`, `NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key` (a fixed value that is not a secret; the Engine does not read it, the Supabase client needs one), and `NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>`. There is no service-role key on an Engine project: add none.

```env
# Client-safe values only: an Engine project has no server-side Supabase secret
NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>
NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>
NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key
NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>
```

### CORS Configuration

On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere.
<!-- /buildpad-backend -->

## Input Validation

```typescript
import { z } from 'zod';

const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
  dueDate: z.string().datetime().optional(),
});

// Validate at the route handler
export async function POST(req: NextRequest) {
  const result = CreateTaskSchema.safeParse(await req.json());
  if (!result.success) {
    return NextResponse.json(
      { error: { code: 'VALIDATION_ERROR', details: result.error.flatten() } },
      { status: 422 }
    );
  }
  // result.data is now typed and validated
}
```

## Security Review Checklist

<!-- buildpad-backend: supabase -->
### Authentication
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (salt rounds ≥ 12)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Password reset tokens expire

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] Users can only access their own resources
- [ ] Admin actions require admin role verification via DaaS RBAC

### Input
- [ ] All user input validated at the boundary
- [ ] SQL queries are parameterized
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Authentication
- [ ] The application stores no password; the Engine holds them, and an administrator resets one in the Studio's Users module
- [ ] The application's own session cookies are httpOnly, secure, sameSite; calls to the Engine carry `Authorization: Bearer`, never a cookie
- [ ] Login has rate limiting
- [ ] No sign-up, magic link or password-recovery flow, and no OAuth sign-in with a provider other than XAppHub, is offered (not available on an Engine project)

### Authorization
- [ ] Every endpoint forwards the user's own access token, so the Engine applies the user's roles, policies and permissions
- [ ] Users can only access their own resources (a permission's row filter, not code in the application)
- [ ] Admin actions require admin role verification: forward the user's token to `GET <Engine_URL>/api/permissions/me` and read `isAdmin`

### Input
- [ ] All user input validated at the boundary
- [ ] No SQL is built or sent: the Engine refuses caller-supplied SQL
<!-- /buildpad-backend -->
- [ ] HTML output is encoded/escaped

### Data
- [ ] No secrets in code or version control
- [ ] Sensitive fields excluded from API responses
- [ ] PII encrypted at rest (if applicable)

### Infrastructure
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS restricted to known origins
- [ ] Dependencies audited for vulnerabilities
- [ ] Error messages don't expose internals

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is an internal tool, security doesn't matter" | Internal tools get compromised. Attackers target the weakest link. |
| "We'll add security later" | Security retrofitting is 10x harder than building it in. Add it now. |
| "No one would try to exploit this" | Automated scanners will find it. Security by obscurity is not security. |
| "The framework handles security" | Frameworks provide tools, not guarantees. You still need to use them correctly. |
| "It's just a prototype" | Prototypes become production. Security habits from day one. |

## Red Flags

- User input passed directly to database queries, shell commands, or HTML rendering
- Secrets in source code or commit history
- API endpoints without authentication or authorization checks
<!-- buildpad-backend: supabase -->
- Missing CORS configuration or wildcard (`*`) origins with credentials
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- A call to the Engine sent with cookies, or any change to the Engine's cross-origin setting
<!-- /buildpad-backend -->
- No rate limiting on authentication endpoints
- Stack traces or internal errors exposed to users
- Dependencies with known critical vulnerabilities

## Verification

After implementing security-relevant code:

- [ ] `pnpm audit` shows no critical or high vulnerabilities
- [ ] No secrets in source code or git history
- [ ] All user input validated at system boundaries
- [ ] Authentication and authorization checked on every protected endpoint
- [ ] Security headers present in response (check with browser DevTools)
- [ ] Error responses don't expose internal details
- [ ] Rate limiting active on auth endpoints

## See Also

For detailed checklists, see `references/security-checklist.md`.
