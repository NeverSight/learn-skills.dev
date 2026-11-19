---
name: supabase-security
description: >-
  Security review and hardening guidance for a SvelteKit SPA with Supabase Auth,
  Postgres with RLS, and client-side rendering. Use when writing auth flows,
  adding RLS policies, handling user input, working with environment variables,
  reviewing code for vulnerabilities, hardening a feature, or when the user asks
  about security, XSS, CSRF, authorization, data exposure, or safe coding practices.
---

# Security Review — SvelteKit SPA + Supabase

This skill applies to a SvelteKit SPA (`ssr = false`) using Supabase Auth, Postgres
with Row Level Security, and `$env/dynamic/public` for environment variables. All
application code runs in the browser — there is no server middleware, no API routes,
and no server-side rendering.

## The trust boundary

The browser is untrusted. Supabase (Postgres RLS + Auth) is the only enforcement
point. Every rule below follows from this.

```
UNTRUSTED                          TRUSTED
─────────────────────────────────  ──────────────────────────
Browser (SvelteKit SPA)            Supabase (Auth + Postgres)
 ├─ authState ($state)             ├─ JWT verification
 ├─ Zod validation (UX only)       ├─ RLS policies (auth.uid())
 ├─ Route guards (UX only)         ├─ DB constraints + CHECK
 └─ UI gating                      └─ Security definer RPCs
```

Client-side checks (auth guards, Zod schemas, route gating) improve UX but provide
**zero security**. Assume an attacker can bypass every client-side check.

---

## 1. Row Level Security (RLS)

RLS is the authorization layer. Every table with user data MUST have RLS enabled.

### Checklist for every new table

- [ ] `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`
- [ ] SELECT policy: `using (auth.uid() = user_id_column)`
- [ ] INSERT policy: `with check (auth.uid() = user_id_column)`
- [ ] UPDATE policy: `using (auth.uid() = ...) with check (auth.uid() = ...)`
- [ ] DELETE policy: `using (auth.uid() = user_id_column)`
- [ ] No policy grants access to `anon` role unless the data is intentionally public
- [ ] Column defaults cannot be abused (e.g., `role text default 'admin'` is dangerous)
- [ ] UPDATE policies restrict which columns can be changed when needed (use `with check` constraints)

### Common mistakes

```sql
-- BAD: allows any authenticated user to read all rows
create policy "select_all" on items for select to authenticated using (true);

-- GOOD: scoped to the row owner
create policy "select_own" on items for select to authenticated
  using (auth.uid() = owner_id);

-- BAD: user can set arbitrary owner_id on insert
create policy "insert_any" on items for insert to authenticated
  with check (true);

-- GOOD: forces owner_id to match the authenticated user
create policy "insert_own" on items for insert to authenticated
  with check (auth.uid() = owner_id);
```

- Never use `using (true)` unless the table is genuinely public.
- Test RLS by running queries as a different user to verify row isolation.

### Security definer functions

RPC functions with `security definer` bypass RLS. Lock them down:

```sql
create or replace function my_rpc()
returns void
language plpgsql
security definer
set search_path = public  -- prevent schema injection
as $$
begin
  -- ALWAYS assert the caller's identity inside the body
  if auth.uid() is null then
    raise exception 'Not authenticated';
  end if;
  -- ... scoped operation using auth.uid() ...
end;
$$;

-- restrict to authenticated users only
revoke all on function my_rpc() from public;
grant execute on function my_rpc() to authenticated;
```

### Migration safety

When writing SQL migrations:

- Never `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` unless immediately re-enabling.
- Never `DROP POLICY` without creating a replacement in the same migration.
- Audit every `security definer` function change for privilege escalation.
- Review `GRANT` statements — never grant `anon` access to sensitive tables.

---

## 2. Safe Supabase query patterns

Since all queries run from the browser, treat query construction as a security surface.

```typescript
// BAD: selecting all columns exposes data you may not intend to show
const { data } = await supabase.from('profiles').select('*');

// GOOD: explicit column selection minimizes exposure
const { data } = await supabase.from('profiles').select('id, display_name');
```

- Always select only the columns you need.
- Even with RLS, over-selecting can expose fields the UI shouldn't render (e.g., internal flags).
- Never pass user input directly into `.or()` or `.filter()` without sanitization — build filters from known safe values.

```typescript
// BAD: user controls the filter string
const { data } = await supabase.from('items').or(userInput);

// GOOD: construct filters from validated enum values
const validStatuses = ['active', 'archived'] as const;
if (validStatuses.includes(status)) {
  const { data } = await supabase.from('items').eq('status', status);
}
```

- Use `.maybeSingle()` for queries that should return 0 or 1 rows — it throws on multiple matches, preventing logic errors.
- Always check `error` before using `data`.

---

## 3. Environment variables

This project uses `$env/dynamic/public` — only variables prefixed with `PUBLIC_` are included.

- Only `PUBLIC_SUPABASE_URL` and `PUBLIC_SUPABASE_PUBLISHABLE_KEY` (anon key) belong in client code.
- NEVER expose `SUPABASE_SERVICE_ROLE_KEY` or any secret in a `PUBLIC_` variable.
- The anon key is safe to expose — it can only do what RLS allows.
- If a feature requires elevated privileges, use a Supabase Edge Function or `security definer` RPC.
- Keep `.env` in `.gitignore`. Commit `.env.example` with placeholder values only.
- Audit: ensure `.env.example` does not contain real credentials.

---

## 4. Cross-site scripting (XSS)

Svelte auto-escapes all template expressions by default, which prevents most XSS.

### The one danger: `{@html}`

```svelte
<!-- DANGEROUS: renders raw HTML, enabling XSS -->
{@html userProvidedContent}

<!-- SAFE: Svelte escapes this automatically -->
{userProvidedContent}
```

- NEVER use `{@html}` with user-provided or database-sourced content.
- If rich text rendering is required, sanitize with DOMPurify before `{@html}`.
- Audit every `{@html}` usage during reviews.

### Other XSS vectors to watch

- `window.location` / `window.open` with user input — always validate URLs.
- `element.innerHTML` in imperative code — use `textContent` instead.
- Dynamic `<a href={userValue}>` — validate it starts with `/` or `https://` from a trusted domain. A `javascript:` URL is XSS.
- Third-party scripts in `<svelte:head>` — only include trusted sources with integrity hashes when possible.

```svelte
<!-- BAD: user-controlled href can be javascript:alert(1) -->
<a href={userUrl}>Click here</a>

<!-- GOOD: validate before rendering -->
{#if userUrl.startsWith('/') || userUrl.startsWith('https://trusted.com')}
  <a href={userUrl}>Click here</a>
{/if}
```

---

## 5. Input validation — defense in depth

Client-side Zod validation is for UX (instant feedback). It is NOT a security boundary.

| Layer | Purpose | Enforced by |
|-------|---------|-------------|
| Zod schema | Instant field feedback | Browser (bypassable) |
| RLS policy | Row-level authorization | Postgres |
| DB constraints | Data integrity (NOT NULL, CHECK, FK) | Postgres |
| Column types | Type safety | Postgres |

- Always pair Zod schemas with matching DB constraints for critical fields.
- Assume any value from the browser can be forged.
- For sensitive operations, validate inside a `security definer` RPC rather than trusting client input.
- Apply string length limits in both Zod and DB (`varchar(255)`, `CHECK (char_length(name) <= 255)`).

---

## 6. Authentication and session management

### `getUser()` vs `getSession()` — critical distinction

```typescript
// BAD for authorization: reads from local storage, can be tampered with
const { data } = await supabase.auth.getSession();

// GOOD for authorization: makes a server call to verify the JWT
const { data } = await supabase.auth.getUser();
```

- Use `getUser()` whenever the result drives data access or authorization logic (e.g., in repositories/services).
- `getSession()` is acceptable ONLY for:
  - Initial UI hydration (followed by `onAuthStateChange` which corrects it).
  - Checking if *any* session exists before a server-verified operation (e.g., password recovery flow).
- The Supabase client uses `getSession()` internally for token refresh — that is its intended use.

### Session rules

- Let Supabase handle token persistence. NEVER manually store JWTs in `localStorage` or cookies.
- `authState` in `$state` is a UI convenience, not a security boundary — RLS enforces access.
- Re-authenticate before destructive actions (password change, email change, account deletion) by requiring the current password.
- Use `sessionStorage` (not `localStorage`) for short-lived flags like `PASSWORD_RECOVERY` — it clears when the tab closes.
- Idempotent listener registration: use a `listenerRegistered` guard to prevent duplicate `onAuthStateChange` subscriptions in dev/HMR.

---

## 7. Open redirect prevention

The `next=` query parameter preserves navigation intent through auth redirects. It is
currently read with `page.url.searchParams.get('next')` and passed directly to `goto()`.

This is an open redirect vulnerability if unvalidated.

### Required: validate every redirect target

```typescript
// src/lib/utils/redirect.ts

// Validates that a redirect target is a safe relative path within the app.
// Rejects absolute URLs, protocol-relative URLs, and encoded bypass attempts.
export function getSafeRedirect(next: string | null, fallback = '/app'): string {
  if (!next) return fallback;

  // Decode to catch %2F%2F and similar bypass attempts
  let decoded: string;
  try {
    decoded = decodeURIComponent(next);
  } catch {
    return fallback;
  }

  // Must be a relative path, not an absolute or protocol-relative URL
  if (!decoded.startsWith('/') || decoded.startsWith('//')) return fallback;

  // Block javascript: and data: schemes that could be encoded
  const lower = decoded.toLowerCase();
  if (lower.includes('javascript:') || lower.includes('data:')) return fallback;

  return next;
}
```

Apply in every location that reads `next`:

```typescript
// In login/signup pages:
void goto(getSafeRedirect(nextParam));

// NOT:
void goto(nextParam ?? '/app');
```

---

## 8. CSRF and request forgery

CSRF is largely mitigated in this SPA because:

- The Supabase JS client sends the auth token as a `Bearer` header, not a cookie.
- `Authorization: Bearer <jwt>` headers are not attached automatically by the browser to cross-origin requests.
- There are no server-side form endpoints.

However, if you add external API calls or Supabase Edge Functions:

- Always send credentials via `Authorization` header, never cookies.
- Set `SameSite=Strict` on any cookies if you introduce them.
- Validate `Origin` or `Referer` headers in Edge Functions that accept mutations.

---

## 9. Rate limiting and brute force

Supabase applies rate limiting on auth endpoints. The app must handle rate-limit errors gracefully:

```typescript
// These error codes indicate rate limiting — show a friendly message
const RATE_LIMIT_CODES = ['over_request_rate_limit', 'over_email_send_rate_limit'];
```

- The error mapping in `src/lib/auth/errors.ts` already handles these codes.
- For email operations (verification resend, password reset): show a cooldown timer in the UI after sending, even before the server rate-limits.
- Consider client-side debouncing on login submit to prevent accidental rapid retries.

---

## 10. Sensitive data handling

### Never log or expose

- Passwords (even in error messages or console logs).
- JWT tokens / access tokens.
- Service role keys.
- Full raw Supabase error objects in production — they may contain query details.

### Reactive state

- Do not store secrets (API keys, tokens) in `$state` — browser devtools can inspect it.
- `authState` stores user metadata (uid, email, displayName) which is acceptable.

### Error messages

- Map Supabase auth errors to generic text using `getAuthErrorMessage()`.
- Never expose raw Supabase error `.message` to the UI unless it has been checked against the known error map first.
- The error mapping in `src/lib/auth/errors.ts` is the canonical pattern — extend it for new error codes rather than showing raw messages.

---

## 11. Account enumeration prevention

Supabase prevents account enumeration by default during signup. This project handles it:

```typescript
if (data.user && Array.isArray(data.user.identities) && data.user.identities.length === 0) {
  throw { code: 'user_already_exists' };
}
```

- Keep this check — without it the signup silently succeeds without creating an account.
- For password reset, always show: "If an account exists, a reset email has been sent."
- For login failures, use a single generic message ("Invalid email or password") — never indicate whether the email exists.

---

## 12. Supabase storage security

If using Supabase Storage for file uploads:

- Use **private** buckets by default; public only for intentionally public assets.
- Add RLS on `storage.objects` scoped to `auth.uid()`.
- Validate file type and size on client AND via Supabase storage policies.
- Use signed URLs with short expiration for private file access.
- Never trust the file extension — validate MIME type server-side.
- Set max file size limits in both the client upload logic and the bucket configuration.

---

## 13. Dependency security

- Run `npm audit` periodically. Fix critical and high vulnerabilities before deploying.
- Pin dependencies in `package-lock.json` — commit the lockfile.
- Audit new dependencies before adding them: check maintenance, download count, and known vulnerabilities.
- Prefer well-known packages with active maintenance over niche alternatives.

---

## Security review checklist

Use this when reviewing a feature, PR, or before deployment:

### Data layer
- [ ] Every new table has RLS enabled with scoped policies
- [ ] No `using (true)` policies unless data is genuinely public
- [ ] INSERT policies enforce `auth.uid() = owner_column`
- [ ] UPDATE policies restrict which columns can change if needed
- [ ] Zod schemas have matching DB constraints for critical fields
- [ ] Queries use explicit column selection, not `select('*')`
- [ ] Security definer RPCs are restricted to `authenticated` role
- [ ] Security definer RPCs assert `auth.uid()` inside the function body
- [ ] Migrations never drop RLS or policies without immediate replacement

### Auth and sessions
- [ ] `getUser()` is used for authorization decisions, not `getSession()`
- [ ] Destructive actions require current password re-authentication
- [ ] No manual JWT storage in `localStorage` or cookies
- [ ] Rate-limit errors are handled with user-friendly messages

### Client-side
- [ ] No `{@html}` with unsanitized user content
- [ ] No `PUBLIC_` env vars contain secrets
- [ ] `next=` redirect values are validated with `getSafeRedirect()`
- [ ] Dynamic `href` attributes are validated (no `javascript:` or `data:` URLs)
- [ ] Error messages shown to users do not expose internal details
- [ ] No passwords, tokens, or PII in console logs
- [ ] File uploads validate type and size on client and server

### Infrastructure
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` contains only placeholder values
- [ ] `npm audit` shows no critical or high vulnerabilities
- [ ] `package-lock.json` is committed
