---
name: multi-tenant-saas-architecture
description: "Production-grade multi-tenant SaaS platform architecture with three-panel separation, zero-trust security, strict tenant isolation, and comprehensive audit trails. Use for designing multi-tenant systems, implementing tenant-scoped permissions, ensuring data isolation, and building scalable SaaS platforms."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Multi-Tenant SaaS Platform Architecture

## Overview

Production-grade multi-tenant SaaS architecture with strict tenant isolation, zero-trust security, and three-panel separation.

**Core Principles:**

- Zero-trust: Every request authenticated, authorized, validated
- Tenant isolation by default: No cross-tenant data access
- Least privilege: Granular, explicit, auditable permissions
- Audit everything: Immutable audit trails for privileged operations

**Security Baseline (Required):** Always load and apply the **Vibe Security Skill** for any web app, API, or data access work. Its controls are mandatory alongside multi-tenant patterns.

**Database Standards (Required):** All database work (schema design, migrations, stored procedures, queries) MUST follow **mysql-best-practices** skill patterns. See that skill's migration checklist for required pre/post-migration steps.

**See subdirectories for:**

- `references/` - Database schemas (database-schema.md), permission models (permission-model.md)
- `documentation/` - Migration patterns (migration.md)

## Deployment Environments

Multi-tenant apps must work identically across all environments:

| Environment | OS | Database | Web Root |
|---|---|---|---|
| **Development** | Windows 11 (WAMP) | MySQL 8.4.7 | `C:\wamp64\www\{project}\` |
| **Staging** | Ubuntu VPS | MySQL 8.x | `/var/www/html/{project}/` |
| **Production** | Debian VPS | MySQL 8.x | `/var/www/html/{project}/` |

**Cross-platform rules:** Use `utf8mb4_unicode_ci` collation everywhere. Match file/directory case exactly (Linux is case-sensitive). Production migrations must be non-destructive and idempotent (`database/migrations-production/`).

## When to Use

✅ Multi-tenant SaaS platforms
✅ Strict tenant data isolation required
✅ Role-based permissions with admin oversight
✅ Compliance and audit trail requirements
✅ Multiple user types (internal staff, external customers)

❌ Single-tenant applications
❌ Simple CRUD apps without isolation needs
❌ Internal tools with flat permission models

## Three-Tier Panel Architecture

**THIS IS THE CORE ARCHITECTURAL CONCEPT:**

```
┌──────────────────────────────────────────────────────────────┐
│              Shared Infrastructure Layer                      │
│  ┌───────────┬─────────────┬─────────────┬────────────┐      │
│  │   Data    │  Business   │ Integration │  Session   │      │
│  │  (Tenant  │   Logic     │   Layer     │  Prefix    │      │
│  │ Isolated) │ (Scoped)    │  (External) │  System    │      │
│  └───────────┴─────────────┴─────────────┴────────────┘      │
└──────────────────────────────────────────────────────────────┘
         │                │                    │
┌────────▼────────┐  ┌───▼──────┐  ┌──────────▼──────┐
│   /public/      │  │/adminpanel│  │  /memberpanel/  │
│  (ROOT)         │  │           │  │                 │
│ Franchise Admin │  │Super Admin│  │  End User       │
│   Workspace     │  │  System   │  │   Portal        │
│                 │  │           │  │                 │
│ owner, staff    │  │super_admin│  │member, student, │
│                 │  │           │  │customer, patient│
└─────────────────┘  └───────────┘  └─────────────────┘
```

**CRITICAL: `/public/` root is the FRANCHISE ADMIN WORKSPACE, not a member panel!**

## File Structure Convention

```
public/
├── index.php           # Landing page with nav buttons (NOT a router)
├── sign-in.php         # Login with SweetAlert
├── dashboard.php       # Franchise admin dashboard
├── skeleton.php        # Page template for new pages
├── adminpanel/         # Super admin panel
│   ├── index.php
│   └── includes/       # Admin-specific includes
├── memberpanel/        # End user portal
│   ├── index.php
│   └── includes/       # Member-specific includes
├── includes/           # Shared includes for /public/ root
├── assets/             # Shared CSS/JS
└── uploads/            # File uploads
```

### 1. Franchise Admin Panel (`/public/` root) - THE MAIN WORKSPACE

**Purpose:** Daily franchise operations (NOT member portal!)
**Location:** `/public/dashboard.php`, `/public/students.php`, etc.
**Users:** Franchise owners, managers, staff
**User Types:** `owner`, `staff`
**Auth:** Session-based (web), JWT (mobile/API)
**Scope:** Single franchise only, cannot access other franchises

**Key Constraints:**

- All queries include `WHERE franchise_id = ?`
- Cannot modify platform settings
- Cannot create/suspend other franchises
- All operations logged for franchise audit

**Example Pages:**

- `/public/dashboard.php` - Franchise admin dashboard
- `/public/students.php` - Manage students (school SaaS)
- `/public/inventory.php` - Manage inventory (restaurant SaaS)
- `/public/patients.php` - Manage patients (medical SaaS)

### 2. Super Admin Panel (`/public/adminpanel/`)

**Purpose:** Platform management and oversight
**Location:** `/public/adminpanel/`
**Users:** Super admins, platform operators
**User Type:** `super_admin`
**Auth:** Session-based + MFA recommended
**Scope:** Cross-franchise with audit trails

**Capabilities:**

- Create/suspend franchises
- Manage platform users
- View cross-franchise analytics
- Configure platform settings
- Access all franchise data (logged)

**Critical Rules:**

- Every action creates audit log
- Production data access logged
- franchise_id can be NULL for super admins
- Can impersonate franchise users (logged)

### 3. End User Portal (`/public/memberpanel/`)

**Purpose:** Self-service for end users
**Location:** `/public/memberpanel/`
**Users:** End customers/patients/students (outside franchise staff)
**User Types:** `member`, `student`, `customer`, `patient` (customizable)
**Auth:** Session-based or JWT
**Scope:** Own records only, read-mostly

**Examples:**

- Student portal - View grades, assignments
- Customer portal - Order tracking, invoices
- Patient portal - View medical records, appointments
- Member portal - Self-service access

## Franchise Isolation Model (Multi-Tenant)

**Terminology:** We use `franchise` instead of `tenant` in SaaS Seeder Template.

### User Types & Franchise Requirements

**CRITICAL: Understand franchise_id requirements per user type:**

```
super_admin - Platform operators (franchise_id CAN be NULL)
owner       - Franchise owners (franchise_id REQUIRED, NOT NULL)
staff       - Franchise staff (franchise_id REQUIRED, NOT NULL)
member      - End users: student, customer, patient (franchise_id REQUIRED, NOT NULL)
```

### Database-Level Isolation

**Option 1: Shared Database (Row-Level franchise_id)** ← SaaS Seeder Template Uses This

```sql
-- Every franchise-scoped table has franchise_id
CREATE TABLE students (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    franchise_id BIGINT UNSIGNED NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    -- other fields
    FOREIGN KEY (franchise_id) REFERENCES tbl_franchises(id)
        ON DELETE CASCADE,
    INDEX idx_franchise (franchise_id),
    INDEX idx_franchise_email (franchise_id, email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ALL queries MUST include franchise_id
SELECT * FROM students WHERE franchise_id = ? AND id = ?;
```

**Option 2: Schema-Per-Franchise**

```sql
-- PostgreSQL: Separate schema per franchise
CREATE SCHEMA franchise_123;
CREATE TABLE franchise_123.students (...);
```

**Option 3: Database-Per-Franchise** (High isolation, ops overhead)

**Recommendation:** Start with Option 1 (row-level), migrate to Option 2 for large/regulated franchises.

**SaaS Seeder Template Convention:**

- Table prefix: `tbl_` for shared tables (users, franchises, roles)
- No prefix: For franchise-scoped data (students, orders, inventory)
- Collation: `utf8mb4_unicode_ci` for all text columns
- Charset: `utf8mb4` for emoji and international character support

### Application-Level Enforcement

**PHP Pattern (Session-based with prefix system):**

```php
// Extract franchise context from session (with prefix)
$franchiseId = getSession('franchise_id'); // Uses SESSION_PREFIX
$userType = getSession('user_type');

// ALWAYS filter by franchise_id
$stmt = $db->prepare("
    SELECT * FROM students
    WHERE franchise_id = ? AND id = ?
");
$stmt->execute([$franchiseId, $studentId]);

// For super_admin, allow cross-franchise access (logged)
if ($userType === 'super_admin') {
    // Can access any franchise, but log the action
    auditLog('CROSS_FRANCHISE_ACCESS', [
        'admin_user_id' => getSession('user_id'),
        'target_franchise_id' => $requestedFranchiseId,
        'action' => 'VIEW_STUDENTS'
    ]);

    // Query without franchise filter (super admin only)
    $stmt = $db->prepare("SELECT * FROM students WHERE id = ?");
    $stmt->execute([$studentId]);
} else {
    // Regular users: MUST filter by their franchise_id
    $stmt = $db->prepare("
        SELECT * FROM students
        WHERE franchise_id = ? AND id = ?
    ");
    $stmt->execute([getSession('franchise_id'), $studentId]);
}
```

**JavaScript Pattern (JWT-based):**

```javascript
// Extract franchise context from JWT
function extractFranchiseContext(req) {
  const token = verifyJWT(req.headers.authorization);
  return {
    userId: token.sub,
    franchiseId: token.fid, // franchise_id in token
    userType: token.ut, // user_type in token
  };
}

// Enforce franchise scope on all queries
function scopeQuery(query, franchiseId) {
  if (!franchiseId) throw new Error("Missing franchise context");
  return query.where("franchise_id", franchiseId);
}
```

**Critical: Never trust client-provided franchise_id**

```php
// BAD - Client controls franchise_id
$franchiseId = $_POST['franchise_id']; // ❌ NEVER DO THIS!

// GOOD - Server extracts from session (with prefix)
$franchiseId = getSession('franchise_id'); // ✅

// GOOD - Server extracts from JWT
$franchiseId = $jwtPayload->fid; // ✅
```

## Authentication & Authorization

### User Types

**SaaS Seeder Template User Types:**

- `super_admin` - Platform management, cross-franchise (franchise_id CAN be NULL)
- `owner` - Full control within franchise (franchise_id REQUIRED)
- `staff` - Operational permissions within franchise (franchise_id REQUIRED)
- Custom end user types (franchise_id REQUIRED):
  - `student` - For school/education SaaS
  - `customer` - For e-commerce/restaurant SaaS
  - `patient` - For medical/clinic SaaS
  - `member` - Generic end user

**Customizing User Types:**

```sql
-- Edit database enum to match your SaaS domain
ALTER TABLE tbl_users MODIFY user_type ENUM(
  'super_admin',
  'owner',
  'staff',
  'student',    -- School SaaS
  'customer',   -- Restaurant SaaS
  'patient'     -- Medical SaaS
) NOT NULL DEFAULT 'staff';
```

### Permission Model

**See `references/permission-model.md` for complete schema**

```javascript
// Permission resolution priority:
// 1. User denial (explicit deny) → DENY
// 2. User grant (explicit allow) → ALLOW
// 3. Franchise override → ALLOW/DENY
// 4. Role permission → ALLOW
// 5. Default → DENY

function hasPermission(userId, tenantId, permission) {
  // Super admin bypass
  if (user.type === "super_admin") return true;

  // Check explicit denials
  if (userPermissions.denied(userId, tenantId, permission)) return false;

  // Check explicit grants
  if (userPermissions.granted(userId, tenantId, permission)) return true;

  // Check role-based permissions
  const roles = getUserRoles(userId, tenantId);
  for (const role of roles) {
    if (roleHasPermission(role, permission, tenantId)) return true;
  }

  return false; // Default deny
}
```

### Session Management

**Session Prefix System (Multi-Tenant Isolation):**

**CRITICAL: All session variables use a prefix to prevent collisions:**

```php
// Define in src/config/session.php
define('SESSION_PREFIX', 'saas_app_'); // Change per SaaS

// ALWAYS use helper functions
setSession('user_id', 123);        // Sets $_SESSION['saas_app_user_id']
$userId = getSession('user_id');   // Gets $_SESSION['saas_app_user_id']
hasSession('user_id');             // Checks if exists
destroySession();                  // Clears all prefixed vars

// Common session variables (with prefix):
setSession('user_id', $userId);
setSession('franchise_id', $franchiseId);
setSession('user_type', $userType);
setSession('username', $username);
setSession('full_name', $fullName);
setSession('last_activity', time());
```

**Customize prefix per SaaS:**

```php
define('SESSION_PREFIX', 'school_');     // School SaaS
define('SESSION_PREFIX', 'restaurant_'); // Restaurant SaaS
define('SESSION_PREFIX', 'clinic_');     // Medical SaaS
define('SESSION_PREFIX', 'hotel_');      // Hospitality SaaS
```

**Web (Session-based):**

```
HttpOnly: true
Secure: auto-detect HTTPS (allow localhost HTTP)
SameSite: Strict
Lifetime: 30 minutes
Regenerate on login
```

**HTTPS Auto-Detection (Critical for Development):**

```php
// Only set secure cookie if using HTTPS
$isHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
           || $_SERVER['SERVER_PORT'] == 443;
ini_set('session.cookie_secure', $isHttps ? '1' : '0');

// Without this, sessions won't persist on localhost HTTP
```

**API (JWT-based):**

```
Access token: 15 minutes
Refresh token: 30 days
Rotation on refresh
Revocation table for logout
```

## Security Architecture

### Zero-Trust Checklist

**Authentication:**

- [ ] MFA for admin access
- [ ] Password: Argon2ID + salt + pepper
- [ ] Account lockout after 5 failures
- [ ] Session timeout (30 min idle)
- [ ] Token rotation on refresh

**Authorization:**

- [ ] Tenant context in every request
- [ ] Permission check before every operation
- [ ] Super admin actions audited
- [ ] Impersonation logged with justification

**Data Access:**

- [ ] `tenant_id` in WHERE clause (ALWAYS)
- [ ] Prepared statements (no SQL injection)
- [ ] Input validation at API boundary
- [ ] Output encoding (XSS prevention)

**API Security:**

- [ ] Rate limiting (per tenant, per user)
- [ ] CORS whitelist (no wildcards)
- [ ] Request size limits
- [ ] HTTPS only (HSTS enabled)

### Common Security Mistakes

❌ **Trusting client-provided franchise_id**

```php
// BAD - Client controls!
$franchiseId = $_POST['franchise_id'];
$stmt = $db->prepare("SELECT * FROM students WHERE franchise_id = ?");
```

✅ **Extract from server-side session (with prefix)**

```php
// GOOD - Server-side session with prefix
$franchiseId = getSession('franchise_id');
$stmt = $db->prepare("SELECT * FROM students WHERE franchise_id = ?");
```

❌ **Missing franchise_id in queries**

```php
// BAD - Missing franchise check! Data leakage!
$stmt = $db->prepare("SELECT * FROM students WHERE id = ?");
$stmt->execute([$studentId]);
```

✅ **Always include franchise scope**

```php
// GOOD - Always filter by franchise_id
$stmt = $db->prepare("
    SELECT * FROM students
    WHERE franchise_id = ? AND id = ?
");
$stmt->execute([getSession('franchise_id'), $studentId]);
```

❌ **Super admin without audit**

```php
if (getSession('user_type') === 'super_admin') {
    // Direct action without logging
    deleteStudent($studentId);
}
```

✅ **Super admin WITH audit**

```php
if (getSession('user_type') === 'super_admin') {
    // Log cross-franchise access
    auditLog('ADMIN_DELETE_STUDENT', [
        'admin_user_id' => getSession('user_id'),
        'target_franchise_id' => $franchiseId,
        'student_id' => $studentId
    ]);
    deleteStudent($studentId);
}
```

❌ **Not using session prefix system**

```php
// BAD - Direct session access (collision risk)
$_SESSION['user_id'] = $userId;
$userId = $_SESSION['user_id'];
```

✅ **Use session prefix helpers**

```php
// GOOD - Prefixed session (namespace isolation)
setSession('user_id', $userId);
$userId = getSession('user_id');
```

## API Design Principles

### Tenant Context in Requests

**Option 1: Subdomain**

```
https://tenant-slug.yourapp.com/api/v1/orders
```

**Option 2: Path parameter**

```
https://api.yourapp.com/v1/tenants/{tenant_id}/orders
```

**Option 3: Header**

```
X-Tenant-ID: 123
Authorization: Bearer <token>
```

**Recommendation:** Use JWT with `tenant_id` claim (no client input).

### RESTful Conventions

```
GET    /api/v1/orders          → List (tenant-scoped)
POST   /api/v1/orders          → Create (tenant-scoped)
GET    /api/v1/orders/{id}     → Show (tenant-scoped)
PUT    /api/v1/orders/{id}     → Update (tenant-scoped)
DELETE /api/v1/orders/{id}     → Delete (tenant-scoped)

// Admin endpoints (cross-tenant)
GET    /api/v1/admin/tenants         → List all tenants
POST   /api/v1/admin/tenants         → Create tenant
GET    /api/v1/admin/analytics       → Cross-tenant analytics
POST   /api/v1/admin/impersonate     → Start impersonation
```

### Response Format

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 100
  }
}
```

**Error format:**

```json
{
  "success": false,
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "You do not have permission to access this resource",
    "details": {}
  }
}
```

## Audit & Compliance

### What to Audit

**Always log:**

- Super admin actions (ALL)
- Impersonation start/end
- Permission changes
- Tenant creation/suspension
- Data exports
- Failed auth attempts
- Cross-tenant access attempts (should be 0)

**Audit record format:**

```json
{
  "id": "uuid",
  "timestamp": "2025-01-23T10:30:00Z",
  "actor_user_id": 123,
  "actor_type": "super_admin",
  "action": "IMPERSONATE_USER",
  "target_tenant_id": 456,
  "target_user_id": 789,
  "justification": "Customer support request #12345",
  "ip_address": "203.0.113.1",
  "user_agent": "...",
  "changes": { "before": {...}, "after": {...} }
}
```

**Retention:**

- Security logs: 1 year minimum
- Audit trails: 7 years (compliance)
- Operational logs: 90 days

## Operational Safeguards

### Tenant Lifecycle

```
PENDING → ACTIVE → SUSPENDED → ARCHIVED
```

- **PENDING**: Created, not yet activated
- **ACTIVE**: Normal operations
- **SUSPENDED**: Payment failure, ToS violation (data retained)
- **ARCHIVED**: Deleted (data purged after retention period)

### Data Protection

**Backups:**

- Daily automated backups
- Point-in-time recovery (30 days)
- Test restore quarterly
- Tenant-level restore capability

**Encryption:**

- At rest: AES-256
- In transit: TLS 1.3
- Sensitive fields: Application-level encryption (PII, payment)

### Rate Limiting

```
Per tenant: 1000 req/min
Per user: 100 req/min
Per IP: 500 req/min
Admin endpoints: 50 req/min
```

### Monitoring Alerts

**Critical:**

- Cross-tenant access attempt
- Super admin login from new IP
- Failed auth spike (>100/min)
- Database query without tenant_id
- API error rate >5%

## Development Guidelines

### Code Review Checklist

**Every feature must:**

- [ ] Include `tenant_id` in all queries
- [ ] Validate permissions before operations
- [ ] Create audit log for privileged actions
- [ ] Test cross-tenant isolation
- [ ] Handle tenant suspension state
- [ ] Document permission requirements

### Testing Requirements

```javascript
describe("Order API", () => {
  it("prevents cross-tenant data access", async () => {
    const tenant1Order = await createOrder(tenant1);
    const tenant2User = await authenticateAs(tenant2.user);

    const response = await tenant2User.get(`/orders/${tenant1Order.id}`);
    expect(response.status).toBe(404); // Not 403 (info leak)
  });

  it("requires permission for operation", async () => {
    const user = await authenticateAs(limitedUser);
    const response = await user.delete("/orders/123");
    expect(response.status).toBe(403);
    expect(response.body.error.code).toBe("PERMISSION_DENIED");
  });
});
```

### Migration Patterns

**See `documentation/migration.md` for adding tenant_id to existing tables**

## Summary

**Critical Implementation Rules:**

1. **Franchise Isolation**: `franchise_id` in EVERY query (except super_admin with audit)
2. **Auth Context**: Extract franchise from session/JWT (never client input)
3. **Session Prefix**: Use `setSession()`/`getSession()` helpers (namespace isolation)
4. **User Types**: Understand franchise_id requirements (NULL only for super_admin)
5. **Permissions**: Check before EVERY operation
6. **Audit**: Log ALL privileged/cross-franchise actions
7. **Super Admin**: Audit + MFA + IP restrictions
8. **Testing**: Cross-franchise isolation tests mandatory
9. **Monitoring**: Alert on cross-franchise access attempts

**Architecture Patterns:**

- **Three-tier panel structure** (CORE concept):
  - `/public/` root = Franchise admin workspace (NOT member panel!)
  - `/adminpanel/` = Super admin system
  - `/memberpanel/` = End user portal
- Session prefix system for multi-tenant isolation
- Zero-trust security model
- Row-level franchise isolation (start here)
- Role-based permissions with overrides
- Immutable audit trails

**SaaS Seeder Template Specifics:**

- Session prefix: `saas_app_` (customize per SaaS)
- Password hashing: Argon2ID + salt(32 chars) + pepper(64+ chars)
- Use `super-user-dev.php` to create admin users (correct hashing)
- HTTPS auto-detection for session.cookie_secure (localhost development)
- Collation: `utf8mb4_unicode_ci` for all text columns

**See Also:**

- `../../docs/PANEL-STRUCTURE.md` - Complete three-tier architecture guide
- `../../CLAUDE.md` - Development guidelines and common pitfalls
- `references/database-schema.md` - Complete database design, indexes, partitioning
- `references/permission-model.md` - RBAC implementation, caching, middleware
- `documentation/migration.md` - Adding franchise_id, zero-downtime migrations, rollback

**Remember:** Security failures in multi-tenant systems affect ALL franchises. Test isolation exhaustively.
