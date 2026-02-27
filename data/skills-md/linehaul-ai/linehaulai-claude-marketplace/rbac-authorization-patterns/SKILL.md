---
name: rbac-authorization-patterns
description: Provide patterns for implementing Role-Based Access Control and multi-tenant authorization in laneweaverTMS. Use when implementing user roles, permissions, tenant isolation, Echo authorization middleware, RLS policies for multi-tenant access, or JWT claims structure for freight brokerage applications.
keywords: [rbac, authorization, security, multi-tenant, rls]
---

# RBAC Authorization Patterns for laneweaverTMS

Expert guidance for implementing Role-Based Access Control (RBAC) and multi-tenant authorization in a Go/Echo backend with Supabase/PostgreSQL.

## When to Use This Skill

Use when:
- Defining user roles and permissions for freight brokerage operations
- Implementing Echo middleware for role/permission checks
- Setting up multi-tenant isolation with account-based access
- Designing JWT claims structure for authorization
- Writing RLS policies for tenant-isolated data access
- Choosing appropriate HTTP status codes for authorization failures

## Freight Brokerage Role Definitions

### Standard Roles

| Role | Description | Typical Access |
|------|-------------|----------------|
| `admin` | Full system access | All resources, user management, system config |
| `dispatcher` | Load management, carrier selection | Loads, carriers, tracking, dispatch operations |
| `sales` | Account management, quotes | Customers, quotes, lanes, tenders |
| `finance` | Invoicing, payments, reports | Invoices, carrier bills, payments, financial reports |
| `driver` | Limited mobile access | Assigned loads only, status updates, document upload |
| `readonly` | View-only access | Read all operational data, no modifications |

### Permission Model

Permissions follow a `resource:action` pattern:

```
loads:read, loads:create, loads:update, loads:delete
carriers:read, carriers:create, carriers:update
customers:read, customers:create, customers:update
invoices:read, invoices:create, invoices:approve
reports:financial, reports:operational
users:manage
```

## Database Schema Patterns

### Core RBAC Tables

```sql
-- Roles table
CREATE TABLE public.roles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_system_role BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Permissions table
CREATE TABLE public.permissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    resource TEXT NOT NULL,
    action TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    UNIQUE(resource, action)
);

-- Role-Permission junction
CREATE TABLE public.role_permissions (
    role_id UUID NOT NULL REFERENCES public.roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES public.permissions(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    PRIMARY KEY (role_id, permission_id)
);

-- User-Role junction (within account/tenant context)
CREATE TABLE public.user_roles (
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES public.roles(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES public.accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    created_by UUID REFERENCES auth.users(id),
    PRIMARY KEY (user_id, role_id, account_id)
);

-- Account-User junction for multi-tenant
CREATE TABLE public.account_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES public.accounts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    is_primary BOOLEAN DEFAULT false,
    invited_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    accepted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    UNIQUE(account_id, user_id)
);

-- Indexes for RLS policy performance
CREATE INDEX idx_user_roles_user_id ON public.user_roles(user_id);
CREATE INDEX idx_user_roles_account_id ON public.user_roles(account_id);
CREATE INDEX idx_account_users_user_id ON public.account_users(user_id);
CREATE INDEX idx_account_users_account_id ON public.account_users(account_id);
```

### Seed Default Roles

```sql
INSERT INTO public.roles (name, description, is_system_role) VALUES
    ('admin', 'Full system access', true),
    ('dispatcher', 'Load management and carrier selection', true),
    ('sales', 'Account management and quotes', true),
    ('finance', 'Invoicing, payments, and reports', true),
    ('driver', 'Limited mobile access for assigned loads', true),
    ('readonly', 'View-only access to operational data', true);
```

## Echo Authorization Middleware

### Context Keys

```go
package middleware

type contextKey string

const (
    ContextKeyUserID    contextKey = "user_id"
    ContextKeyAccountID contextKey = "account_id"
    ContextKeyRoles     contextKey = "roles"
    ContextKeyUser      contextKey = "user"
)
```

### JWT Claims Structure

```go
package auth

import "github.com/golang-jwt/jwt/v5"

type Claims struct {
    jwt.RegisteredClaims
    UserID      string   `json:"user_id"`
    Email       string   `json:"email"`
    AccountID   string   `json:"account_id"`
    Roles       []string `json:"roles"`
    Permissions []string `json:"permissions,omitempty"` // Optional: can derive from roles
}
```

### Authentication Middleware

Validates JWT and extracts claims into context:

```go
package middleware

import (
    "net/http"
    "strings"

    "github.com/labstack/echo/v4"
)

func JWTAuth(jwtSecret []byte) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            authHeader := c.Request().Header.Get("Authorization")
            if authHeader == "" {
                return echo.NewHTTPError(http.StatusUnauthorized, "missing authorization header")
            }

            tokenString := strings.TrimPrefix(authHeader, "Bearer ")
            if tokenString == authHeader {
                return echo.NewHTTPError(http.StatusUnauthorized, "invalid authorization format")
            }

            claims, err := ValidateToken(tokenString, jwtSecret)
            if err != nil {
                return echo.NewHTTPError(http.StatusUnauthorized, "invalid or expired token")
            }

            // Store in context for downstream handlers
            c.Set(string(ContextKeyUserID), claims.UserID)
            c.Set(string(ContextKeyAccountID), claims.AccountID)
            c.Set(string(ContextKeyRoles), claims.Roles)
            c.Set(string(ContextKeyUser), claims)

            return next(c)
        }
    }
}
```

### Tenant Context Middleware

Ensures valid tenant context after authentication:

```go
func TenantContext() echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            accountID := c.Get(string(ContextKeyAccountID))
            if accountID == nil || accountID.(string) == "" {
                return echo.NewHTTPError(http.StatusForbidden, "no tenant context")
            }

            // Optionally validate account exists and is active
            // This can be cached for performance

            return next(c)
        }
    }
}
```

### Role-Based Authorization Middleware

```go
// RequireRole checks if user has any of the specified roles
func RequireRole(roles ...string) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            userRoles, ok := c.Get(string(ContextKeyRoles)).([]string)
            if !ok || len(userRoles) == 0 {
                return echo.NewHTTPError(http.StatusForbidden, "no roles assigned")
            }

            for _, required := range roles {
                for _, userRole := range userRoles {
                    if userRole == required {
                        return next(c)
                    }
                }
            }

            return echo.NewHTTPError(http.StatusForbidden, "insufficient role permissions")
        }
    }
}

// RequireAnyRole is an alias for RequireRole (OR logic)
var RequireAnyRole = RequireRole

// RequireAllRoles checks if user has ALL specified roles
func RequireAllRoles(roles ...string) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            userRoles, ok := c.Get(string(ContextKeyRoles)).([]string)
            if !ok {
                return echo.NewHTTPError(http.StatusForbidden, "no roles assigned")
            }

            userRoleSet := make(map[string]bool)
            for _, r := range userRoles {
                userRoleSet[r] = true
            }

            for _, required := range roles {
                if !userRoleSet[required] {
                    return echo.NewHTTPError(http.StatusForbidden, "missing required role")
                }
            }

            return next(c)
        }
    }
}
```

### Permission-Based Authorization Middleware

```go
// RequirePermission checks for specific resource:action permission
func RequirePermission(resource, action string) echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            claims, ok := c.Get(string(ContextKeyUser)).(*Claims)
            if !ok {
                return echo.NewHTTPError(http.StatusForbidden, "invalid user context")
            }

            // Check explicit permissions if available
            requiredPerm := resource + ":" + action
            for _, perm := range claims.Permissions {
                if perm == requiredPerm || perm == resource+":*" || perm == "*:*" {
                    return next(c)
                }
            }

            // Fallback: derive from roles (requires DB lookup or cached mapping)
            if hasPermissionViaRole(claims.Roles, resource, action) {
                return next(c)
            }

            return echo.NewHTTPError(http.StatusForbidden, "permission denied")
        }
    }
}

// hasPermissionViaRole checks role-permission mapping
// In production, use cached lookup or include permissions in JWT
func hasPermissionViaRole(roles []string, resource, action string) bool {
    // Admin role has all permissions
    for _, role := range roles {
        if role == "admin" {
            return true
        }
    }

    // Role-permission mapping (simplified; use DB in production)
    rolePerms := map[string][]string{
        "dispatcher": {"loads:*", "carriers:read", "tracking:*"},
        "sales":      {"customers:*", "quotes:*", "lanes:*", "tenders:*"},
        "finance":    {"invoices:*", "payments:*", "reports:financial"},
        "driver":     {"loads:read", "loads:update_status", "documents:upload"},
        "readonly":   {"loads:read", "carriers:read", "customers:read"},
    }

    requiredPerm := resource + ":" + action
    for _, role := range roles {
        for _, perm := range rolePerms[role] {
            if matchPermission(perm, requiredPerm) {
                return true
            }
        }
    }
    return false
}

func matchPermission(pattern, required string) bool {
    if pattern == required {
        return true
    }
    // Handle wildcard: "loads:*" matches "loads:read"
    if strings.HasSuffix(pattern, ":*") {
        prefix := strings.TrimSuffix(pattern, "*")
        return strings.HasPrefix(required, prefix)
    }
    return false
}
```

### Middleware Chain Example

Apply middleware in order: Auth -> Tenant -> Role -> Permission:

```go
func SetupRoutes(e *echo.Echo, cfg *config.Config) {
    // Public routes (no auth required)
    e.GET("/health", handlers.HealthCheck)

    // API routes with auth
    api := e.Group("/api/v1")
    api.Use(middleware.JWTAuth(cfg.JWTSecret))
    api.Use(middleware.TenantContext())

    // Load routes - dispatchers and admins
    loads := api.Group("/loads")
    loads.Use(middleware.RequireRole("admin", "dispatcher", "sales", "readonly"))
    loads.GET("", handlers.ListLoads)
    loads.GET("/:id", handlers.GetLoad)

    // Modify operations require specific roles
    loads.POST("", handlers.CreateLoad, middleware.RequireRole("admin", "dispatcher", "sales"))
    loads.PUT("/:id", handlers.UpdateLoad, middleware.RequireRole("admin", "dispatcher"))

    // Finance routes
    finance := api.Group("/finance")
    finance.Use(middleware.RequireRole("admin", "finance"))
    finance.GET("/invoices", handlers.ListInvoices)
    finance.POST("/invoices", handlers.CreateInvoice)

    // Admin-only routes
    admin := api.Group("/admin")
    admin.Use(middleware.RequireRole("admin"))
    admin.GET("/users", handlers.ListUsers)
    admin.POST("/users", handlers.CreateUser)
}
```

## Multi-Tenant RLS Policies

### Enable RLS on Tables

```sql
ALTER TABLE public.loads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.carriers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.invoices ENABLE ROW LEVEL SECURITY;
```

### Account-Based Tenant Isolation

```sql
-- Users see only their account's loads
CREATE POLICY "Users see only their account loads"
    ON public.loads
    FOR SELECT
    TO authenticated
    USING (
        account_id IN (
            SELECT account_id
            FROM public.account_users
            WHERE user_id = (SELECT auth.uid())
        )
    );

-- Users can create loads for their account
CREATE POLICY "Users create loads for their account"
    ON public.loads
    FOR INSERT
    TO authenticated
    WITH CHECK (
        account_id IN (
            SELECT account_id
            FROM public.account_users
            WHERE user_id = (SELECT auth.uid())
        )
    );

-- Users can update their account's loads
CREATE POLICY "Users update their account loads"
    ON public.loads
    FOR UPDATE
    TO authenticated
    USING (
        account_id IN (
            SELECT account_id
            FROM public.account_users
            WHERE user_id = (SELECT auth.uid())
        )
    )
    WITH CHECK (
        account_id IN (
            SELECT account_id
            FROM public.account_users
            WHERE user_id = (SELECT auth.uid())
        )
    );
```

### Role-Based RLS Policies

Combine tenant isolation with role restrictions:

```sql
-- Helper function to check user roles within account
CREATE OR REPLACE FUNCTION public.user_has_role(required_roles TEXT[])
RETURNS BOOLEAN
LANGUAGE sql
SECURITY DEFINER
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM public.user_roles ur
        JOIN public.roles r ON ur.role_id = r.id
        WHERE ur.user_id = (SELECT auth.uid())
        AND r.name = ANY(required_roles)
    );
$$;

-- Only finance and admin can view invoices
CREATE POLICY "Finance users view invoices"
    ON public.customer_invoices
    FOR SELECT
    TO authenticated
    USING (
        account_id IN (
            SELECT account_id
            FROM public.account_users
            WHERE user_id = (SELECT auth.uid())
        )
        AND public.user_has_role(ARRAY['admin', 'finance', 'readonly'])
    );

-- Only finance and admin can create invoices
CREATE POLICY "Finance users create invoices"
    ON public.customer_invoices
    FOR INSERT
    TO authenticated
    WITH CHECK (
        account_id IN (
            SELECT account_id
            FROM public.account_users
            WHERE user_id = (SELECT auth.uid())
        )
        AND public.user_has_role(ARRAY['admin', 'finance'])
    );
```

### Driver-Specific Policies

Drivers see only their assigned loads:

```sql
-- Drivers see only loads assigned to them
CREATE POLICY "Drivers see assigned loads"
    ON public.loads
    FOR SELECT
    TO authenticated
    USING (
        -- Driver is assigned to this load
        driver_user_id = (SELECT auth.uid())
        OR
        -- Or user has broader access via role
        (
            account_id IN (
                SELECT account_id
                FROM public.account_users
                WHERE user_id = (SELECT auth.uid())
            )
            AND public.user_has_role(ARRAY['admin', 'dispatcher', 'sales', 'readonly'])
        )
    );
```

## Authorization Decision Patterns

### HTTP Status Code Guidelines

| Scenario | Status Code | When to Use |
|----------|-------------|-------------|
| Missing or invalid token | `401 Unauthorized` | Token absent, expired, or malformed |
| Valid token, insufficient permissions | `403 Forbidden` | User authenticated but lacks required role/permission |
| Resource not found (or hidden) | `404 Not Found` | Resource doesn't exist OR hiding existence is security concern |

### Security-Aware 404 Pattern

Use 404 instead of 403 when revealing resource existence is a security concern:

```go
func GetLoad(c echo.Context) error {
    loadID := c.Param("id")
    accountID := c.Get(string(middleware.ContextKeyAccountID)).(string)

    load, err := repo.GetLoad(c.Request().Context(), loadID)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            // Resource doesn't exist
            return echo.NewHTTPError(http.StatusNotFound, "load not found")
        }
        return echo.NewHTTPError(http.StatusInternalServerError, "failed to fetch load")
    }

    // Check tenant ownership - return 404 to hide existence
    if load.AccountID != accountID {
        return echo.NewHTTPError(http.StatusNotFound, "load not found")
    }

    return c.JSON(http.StatusOK, load)
}
```

### Error Response Structure

```go
type ErrorResponse struct {
    Error   string `json:"error"`
    Code    string `json:"code,omitempty"`
    Details string `json:"details,omitempty"`
}

// Authorization error examples
// 401: {"error": "missing authorization header", "code": "AUTH_REQUIRED"}
// 401: {"error": "invalid or expired token", "code": "TOKEN_INVALID"}
// 403: {"error": "insufficient role permissions", "code": "ROLE_REQUIRED"}
// 403: {"error": "permission denied", "code": "PERMISSION_DENIED"}
```

## JWT Claims Best Practices

### Minimal Claims for Performance

Include only essential claims; derive others from database:

```go
type MinimalClaims struct {
    jwt.RegisteredClaims
    UserID    string `json:"sub"`       // Use standard 'sub' claim
    AccountID string `json:"account_id"`
    Roles     []string `json:"roles"`    // Include for middleware checks
}
```

### Full Claims with Permissions

For reduced database lookups, include permissions:

```go
type FullClaims struct {
    jwt.RegisteredClaims
    UserID      string   `json:"sub"`
    Email       string   `json:"email"`
    AccountID   string   `json:"account_id"`
    AccountName string   `json:"account_name"`
    Roles       []string `json:"roles"`
    Permissions []string `json:"permissions"` // Flattened from roles
}
```

### Token Generation

```go
func GenerateToken(user *User, account *Account, roles []string, permissions []string) (string, error) {
    now := time.Now()
    claims := &FullClaims{
        RegisteredClaims: jwt.RegisteredClaims{
            Subject:   user.ID,
            IssuedAt:  jwt.NewNumericDate(now),
            ExpiresAt: jwt.NewNumericDate(now.Add(24 * time.Hour)),
            Issuer:    "laneweavertms",
        },
        UserID:      user.ID,
        Email:       user.Email,
        AccountID:   account.ID,
        AccountName: account.Name,
        Roles:       roles,
        Permissions: permissions,
    }

    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(jwtSecret)
}
```

## Authorization Checklist

```
RBAC Schema:
[ ] roles, permissions, role_permissions tables created
[ ] user_roles table includes account_id for multi-tenant
[ ] account_users table for tenant membership
[ ] Indexes on user_id, account_id columns for RLS performance

Middleware Chain:
[ ] JWT validation middleware extracts claims to context
[ ] Tenant context middleware validates account_id
[ ] Role middleware checks user roles array
[ ] Permission middleware checks specific resource:action

RLS Policies:
[ ] RLS enabled on all tenant-owned tables
[ ] SELECT policies use account_id IN (SELECT from account_users)
[ ] INSERT policies use WITH CHECK for account_id
[ ] UPDATE policies use both USING and WITH CHECK
[ ] auth.uid() wrapped in SELECT for query plan caching
[ ] Indexes exist on columns used in RLS conditions

JWT Claims:
[ ] Token includes user_id, account_id, roles
[ ] Token expiration set appropriately (e.g., 24 hours)
[ ] Refresh token mechanism for long-lived sessions

Error Handling:
[ ] 401 for missing/invalid authentication
[ ] 403 for valid auth but insufficient permissions
[ ] 404 when hiding resource existence is security concern
[ ] Error responses don't leak sensitive information
```

## Related Skills

- **goth-oauth** - OAuth2 authentication foundation
- **laneweaver-database-design** - Database schema conventions

## Reference

- Echo middleware documentation: https://echo.labstack.com/docs/middleware
- Supabase RLS guide: https://supabase.com/docs/guides/auth/row-level-security
- JWT best practices: https://datatracker.ietf.org/doc/html/rfc7519
