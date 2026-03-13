---
name: dual-auth-rbac
description: "Dual authentication system (Session + JWT) with role-based access control (RBAC) for multi-tenant applications. Use when implementing secure authentication across web UI and API/mobile clients, with franchise/tenant-scoped permissions. Works across languages: PHP, Node.js, Python, Go, etc."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Dual Authentication with RBAC

Implement production-grade dual authentication combining session-based (stateful) and JWT-based (stateless) auth with comprehensive RBAC and multi-tenant isolation.

**Core Principle:** Different clients need different auth strategies. Web UIs benefit from sessions; APIs/mobile need stateless tokens. RBAC must work seamlessly across both.

**Database Standards:** All database schema changes (adding auth tables, stored procedures, indexes) MUST follow **mysql-best-practices** skill migration checklist.

**Deployment:** Runs on Windows dev (MySQL 8.4.7), Ubuntu staging (MySQL 8.x), Debian production (MySQL 8.x). Use `utf8mb4_unicode_ci` collation. Ensure file paths and require statements match exact case for Linux compatibility.

**See references/ for:** `schema.sql` (complete database design with 9 tables)

## When to Use

✅ Multi-tenant SaaS with web + API access
✅ Web UI + mobile apps authentication
✅ Role-based permissions with tenant isolation
✅ Token revocation capability required
✅ Multiple device sessions per user
✅ Three-tier panel architecture (super admin, franchise admin, member portal)

❌ Simple single-tenant apps (overkill)
❌ Read-only public APIs
❌ Internal tools (simpler auth suffices)

## Three-Tier Panel Structure Context

**This authentication system supports three-tier panel architecture:**

1. **`/public/` (root)** - Franchise Admin Panel
   - Single franchise management workspace
   - User types: `owner`, `staff`
   - Session-based auth (web UI)

2. **`/public/adminpanel/`** - Super Admin Panel
   - System-wide multi-franchise oversight
   - User type: `super_admin`
   - Session-based + MFA recommended

3. **`/public/memberpanel/`** - End User Portal
   - Self-service for end users
   - User types: `member`, `student`, `customer`, `patient`
   - Session or JWT depending on client type

**Key Principle:** `/public/` root is NOT a redirect router - it's the franchise admin workspace!

## Architecture

```
Web UI → Session Cookie + CSRF
Mobile → JWT Access + Refresh
API    → JWT Access + Refresh
         ↓
    Auth Layer → RBAC Engine → Database
```

## Database Schema Essentials

**Core tables (see references/schema.sql):**

1. **tbl_users** - Accounts with tenant scope
2. **tbl_global_roles** - Reusable roles
3. **tbl_permissions** - Atomic permissions
4. **tbl_global_role_permissions** - Role → Permission
5. **tbl_user_roles** - User → Role (tenant-scoped)
6. **tbl_user_permissions** - Direct grants/denials
7. **tbl_franchise_role_overrides** - Tenant overrides
8. **tbl_api_refresh_tokens** - JWT revocation
9. **tbl_login_attempts** - Security monitoring

**Key indexes:** `(tenant_id, user_id)`, `(jti)`, `(username, attempt_time)`

## Password Security

**Algorithm: Argon2ID + Salt + Pepper**

```
Hash Flow:
1. Random salt (32 bytes - IMPORTANT: Use 32 bytes, not 16)
2. Combine password + salt
3. HMAC with pepper (env secret, 64+ chars recommended)
4. Argon2ID hash
5. Store: salt(32 chars) + hash

Parameters:
  memory_cost: 65536 KB
  time_cost: 4
  threads: 3
  salt: 32 bytes
  pepper: env variable (64+ chars)
```

**Requirements:** Min 8 chars, uppercase + lowercase + numbers + special

**CRITICAL: Admin User Creation**
- NEVER use manual password_hash() or migration defaults (often bcrypt)
- ALWAYS use a dedicated tool like `super-user-dev.php` that uses PasswordHelper
- Ensures password hashing matches login verification
- Example: Visit `http://localhost:8000/super-user-dev.php` to create admin users

## JWT Architecture

### Access Token (15 min)
```json
{
  "sub": 12345,          // user_id
  "fid": 67,             // franchise_id
  "ut": "staff",         // user_type
  "did": "device-123",   // device_id
  "jti": "unique-id",    // for revocation
  "exp": 1706000900,
  "type": "access"
}
```

### Refresh Token (30 days)
```json
{
  "sub": 12345,
  "fid": 67,
  "ut": "staff",
  "did": "device-123",
  "jti": "unique-id",
  "exp": 1708592000,
  "type": "refresh"
}
```

**Security:**
- HS256 signing (RS256 for distributed)
- Timing-safe comparison
- Unique JTI per token
- Token rotation on refresh
- Revocation table

## Session Management

**Config:**
```
HttpOnly: true
Secure: auto-detect HTTPS (allow localhost HTTP)
SameSite: Strict
Lifetime: 30 minutes
```

**Session Prefix System (Multi-Tenant Isolation):**
```php
// Define prefix per SaaS app
define('SESSION_PREFIX', 'saas_app_'); // Change per SaaS

// ALWAYS use helper functions
setSession('user_id', 123);        // Sets $_SESSION['saas_app_user_id']
$userId = getSession('user_id');   // Gets $_SESSION['saas_app_user_id']
hasSession('user_id');             // Checks if exists

// Benefits:
// 1. Multiple SaaS apps on same domain won't collide
// 2. Clear namespace per application
// 3. Prevents accidental session variable conflicts
```

**Session data (with prefix):**
```
{
  saas_app_user_id,
  saas_app_franchise_id,
  saas_app_user_type,
  saas_app_username,
  saas_app_last_activity,
  saas_app_csrf_token
}
```

**Security:**
- Regenerate ID on login
- Timeout check (30 min idle)
- Complete destruction on logout
- CSRF validation on mutations
- Auto-detect HTTPS for secure cookie flag (allows localhost development)

**Session Hardening (php.ini):**
```ini
session.use_strict_mode = 1      ; Reject uninitialized session IDs
session.sid_length = 48           ; Longer IDs = harder to guess
session.sid_bits_per_character = 6 ; Maximum entropy
session.serialize_handler = php_serialize ; Safer serialization
```

**See php-security skill** for complete session hardening checklist and attack prevention patterns.

**HTTPS Auto-Detection (Critical for Localhost Development):**
```php
// Only set secure cookie if using HTTPS
$isHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
           || $_SERVER['SERVER_PORT'] == 443;
ini_set('session.cookie_secure', $isHttps ? '1' : '0');

// Without this, sessions won't persist on localhost HTTP
```

## RBAC Permission Resolution

**Priority (highest to lowest):**

```
1. User Denial → DENIES even if role grants
2. User Grant → GRANTS even if not in role
3. Franchise Override → Tenant enables/disables
4. Role Permission → Default from role
5. Super Admin → ALL permissions
```

**Algorithm:**
```
hasPermission(userId, franchiseId, permissionCode):
  if user.type == 'super_admin': return true
  if userPermission.denied(...): return false
  if userPermission.granted(...): return true

  for role in getUserRoles(userId, franchiseId):
    override = getFranchiseOverride(...)
    if override and override.disabled: continue
    if permissionCode in getRolePermissions(role): return true

  return false
```

**Caching:** 15 min TTL, invalidate on role/permission changes

## Authentication Flows

### Web Login (Session)
```
1. POST /auth/login {username, password, csrf_token}
2. Validate CSRF
3. Find user (check status, not locked)
4. Verify password
5. Create session (regenerate ID, store context)
6. Return redirect
```

### API Login (JWT)
```
1. POST /api/v1/auth/login {username, password, device_id}
2. Find user, verify password
3. Generate access + refresh tokens
4. Persist refresh token (revocation table)
5. Return {access_token, refresh_token, expires_in}
```

### Token Refresh
```
1. POST /api/v1/auth/refresh {refresh_token}
2. Verify token, check revocation
3. Revoke old token (rotation)
4. Generate new token pair
5. Persist new refresh token
6. Return new tokens
```

## Multi-Tenant Isolation

**User Types & Franchise Requirements:**
```
super_admin - Platform operators (franchise_id CAN be NULL)
owner       - Franchise owners (franchise_id REQUIRED)
staff       - Franchise staff with permissions (franchise_id REQUIRED)
member      - End users: student, customer, patient (franchise_id REQUIRED)
```

**Session-based (with prefix system):**
```php
$franchiseId = getSession('franchise_id'); // Uses session prefix
$stmt = $db->prepare("SELECT * FROM orders WHERE franchise_id = ?");
$stmt->execute([$franchiseId]);
```

**JWT-based:**
```
token = verifyAccessToken(bearerToken)
franchiseId = token.fid
SELECT * FROM orders WHERE franchise_id = ?
```

**CRITICAL: ALWAYS Filter by franchise_id:**
```php
// CORRECT
$stmt = $db->prepare("SELECT * FROM students WHERE franchise_id = ?");
$stmt->execute([getSession('franchise_id')]);

// WRONG - data leakage!
$stmt = $db->prepare("SELECT * FROM students");
```

**Cross-tenant protection:**
```
if user.type != 'super_admin' and user.franchise_id != requestedFranchiseId:
  throw ForbiddenError("Cross-tenant access denied")
```

## Security Checklist

### Password
- [ ] Argon2ID (memory_cost ≥ 65536 KB)
- [ ] Random salt (16+ bytes)
- [ ] Application pepper (env var)
- [ ] Complexity validation
- [ ] Rehash check on login

### JWT
- [ ] Access ≤ 15 min
- [ ] Refresh rotation
- [ ] Unique JTI
- [ ] Secure secret (32+ bytes)
- [ ] Audience + issuer validation
- [ ] Timing-safe comparison

### Session
- [ ] HttpOnly, Secure, SameSite
- [ ] Regeneration on login
- [ ] 30 min timeout
- [ ] Complete destruction
- [ ] CSRF validation
- [ ] Session strict mode enabled
- [ ] Session ID length >= 48

### Account Protection
- [ ] Lock after 5 failures
- [ ] Login attempt logging
- [ ] Rate limiting
- [ ] Password reset limits
- [ ] Force change on first login

### Multi-Tenant
- [ ] Tenant ID in session/token
- [ ] Tenant filter on EVERY query
- [ ] Tenant-scoped permissions
- [ ] Cross-tenant validation

### RBAC
- [ ] Permission caching (15 min)
- [ ] Super admin bypass
- [ ] Protected resource checks
- [ ] Franchise overrides

## Middleware Pattern

**Session (Web):**
```
requireAuth():
  if not session.user_id: redirect("/login")
  if timeout: logout(), redirect("/login")
  session.last_activity = now()
  return session

requirePermission(code):
  session = requireAuth()
  if not hasPermission(...): return 403
  return session
```

**JWT (API):**
```
authenticateJWT():
  token = extractBearerToken()
  if not token: return 401
  payload = verifyAccessToken(token)
  return {user_id, franchise_id, user_type}

requirePermission(code):
  context = authenticateJWT()
  if not hasPermission(...): return 403
  return context
```

## Environment Variables

```bash
JWT_SECRET=<openssl rand -hex 32>
JWT_ACCESS_TTL=900
JWT_REFRESH_TTL=2592000
PASSWORD_PEPPER=<openssl rand -hex 64>  # 64+ chars recommended
COOKIE_ENCRYPTION_KEY=<openssl rand -hex 32>
COOKIE_DOMAIN=localhost  # or production domain
SESSION_LIFETIME=1800
MAX_LOGIN_ATTEMPTS=5
APP_ENV=development  # or production
```

**IMPORTANT:**
- `PASSWORD_PEPPER`: Use 64+ chars for maximum security
- `COOKIE_ENCRYPTION_KEY`: 32+ chars for secure cookie encryption
- `APP_ENV`: Set to `production` to enable all security features

## Common Endpoints

**Web:** `/auth/login`, `/auth/logout`, `/auth/password/reset`
**API:** `/api/v1/auth/login`, `/api/v1/auth/refresh`, `/api/v1/auth/logout`

## Language-Specific

**PHP:** `password_hash(PASSWORD_ARGON2ID)`, `session_start()`, `firebase/php-jwt`
**Node:** `argon2` package, `express-session`, `jsonwebtoken`
**Python:** `argon2-cffi`, Flask-Session/Django, `PyJWT`
**Go:** `golang.org/x/crypto/argon2`, `gorilla/sessions`, `golang-jwt/jwt`

## Testing

- [ ] Valid login returns session/tokens
- [ ] Invalid password → 401
- [ ] Locked account → 403
- [ ] Token refresh works
- [ ] Logout revokes
- [ ] Super admin bypasses
- [ ] Role permissions resolve
- [ ] User overrides work
- [ ] Tenant isolation enforced
- [ ] Missing permission → 403
- [ ] Expired tokens rejected
- [ ] Revoked tokens rejected
- [ ] Invalid signatures rejected
- [ ] CSRF works
- [ ] Session timeout enforced

## Critical Pitfalls

### Token Format Consistency (LOGIN vs MIDDLEWARE)

**NEVER mix token formats.** If the auth middleware (`ApiAuthMiddleware`) verifies tokens using a JWT library (e.g., `firebase/php-jwt`), the login endpoint MUST generate tokens with that same library.

```
❌ WRONG - Login generates base64 token, middleware expects JWT:
   Login:      base64_encode(json_encode(['user_id' => $id, 'exp' => ...]))
   Middleware:  JWT::decode($token, new Key($secret, 'HS256'))
   Result:     Every API call returns 401

✅ CORRECT - Login and middleware use the same JWT library:
   Login:      MobileAuthHelper::generateMobileAccessToken(...)
   Middleware:  MobileAuthHelper::verifyAccessToken(...)
   Result:     Tokens work end-to-end
```

**Checklist:**
- [ ] Login endpoint generates tokens using the SAME helper/library the middleware uses to verify
- [ ] Refresh endpoint generates tokens the SAME way as login
- [ ] All JWT claims required by middleware (sub, fid, ut, dc, type) are present in generated tokens
- [ ] Test the full flow: login → get token → call API with Bearer token → verify 200 (not 401)

### Distributor Code in JWT Claims

When the JWT includes a `distributor_code` claim (`dc`), ensure the lookup happens BEFORE token generation:

```
❌ WRONG - Lookup after generation:
   $token = generateToken(..., $distributorCode);  // $distributorCode is undefined!
   $distributorCode = lookupDistributorCode();       // Too late

✅ CORRECT - Lookup before generation:
   $distributorCode = lookupDistributorCode();
   $token = generateToken(..., $distributorCode);
```

## Implementation Steps

1. Create database schema (references/schema.sql)
2. Implement password helper (Argon2ID)
3. Implement JWT service (sign, verify, refresh)
4. Implement session management
5. Implement permission service (RBAC + caching)
6. Create auth endpoints
7. Create middleware (validators, permission checks)
8. Add security (rate limiting, locking, CSRF)
9. Write tests
10. Configure environment

**Remember:** Security is not optional. Follow checklist completely.
