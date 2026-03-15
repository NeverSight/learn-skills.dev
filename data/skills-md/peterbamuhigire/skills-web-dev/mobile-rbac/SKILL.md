---
name: mobile-rbac
description: "Role-Based Access Control for Android mobile apps integrating with a multi-tenant SaaS backend. Covers permission fetching, caching in EncryptedSharedPreferences, Jetpack Compose permission gates (PermissionGate, ModuleGate, PermissionButton), module-gated bottom navigation, navigation guards, offline-capable permission checks, and defense-in-depth patterns. Use when implementing permission-based UI gating, role-based feature access, or module-based tab visibility in Android apps."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Mobile RBAC - Android Permission System

## Architecture Overview

Mobile RBAC uses a **hybrid client+server** approach:

1. **Backend enforces** - Every API call checked by PermissionMiddleware (returns 403 if denied)
2. **Client gates UI** - Cached permissions control button/tab/screen visibility for UX
3. **Fail-secure** - If permissions unknown, deny access (never grant)
4. **Offline-capable** - Cached permissions work without network

**Backend Environments:** Dev (Windows/MySQL 8.4.7), Staging (Ubuntu/MySQL 8.x), Production (Debian/MySQL 8.x). Permission APIs must behave identically across all environments. Use Gradle build flavors for environment-specific base URLs.

```
Login → Fetch Permissions → Cache in EncryptedSharedPreferences → UI Gates
         ↕ (refresh)                                                ↕ (403 fallback)
     Backend always enforces ←──────────────────────────────────────┘
```

## Quick Reference

| Topic                       | Reference File                          | When to Use                                                |
| --------------------------- | --------------------------------------- | ---------------------------------------------------------- |
| **Architecture & Caching**  | This file                               | Permission flow, caching strategy, refresh triggers        |
| **Implementation Patterns** | `references/implementation-patterns.md` | Code templates for PermissionManager, PermissionGate, etc. |
| **Permission Map**          | `references/permission-map.md`          | What permission controls what feature                      |

## Core Principles

### 1. Two-Layer Gating

| Layer               | What It Controls          | When Hidden/Disabled                  |
| ------------------- | ------------------------- | ------------------------------------- |
| **Module Gate**     | Bottom nav tabs           | Franchise hasn't subscribed to module |
| **Permission Gate** | Screens, buttons, actions | User's role lacks the permission      |

**Rule:** Modules HIDE tabs entirely. Permissions DISABLE or HIDE individual actions.

### 2. Permission Resolution (Backend)

The backend resolves permissions using 5-tier priority:

```
1. User Denial  (explicit deny)    → ALWAYS DENIED
2. User Grant   (explicit grant)   → ALWAYS GRANTED
3. Franchise Override              → Tenant customization
4. Role Permission                 → Default from role
5. Super Admin / Owner             → ALL permissions
```

The mobile client **never resolves permissions locally**. It receives the resolved
set from the backend via `GET /user/permissions` and uses it as-is.

### 3. Storage: EncryptedSharedPreferences

Permissions are a flat set of ~20-50 string codes. Too lightweight for Room.

```
"user_permissions"    → Set<String> {"POS_CREATE_SALE", "DASHBOARD_VIEW", ...}
"user_modules"        → Set<String> {"POS", "INVENTORY", ...}
"user_roles"          → Set<String> {"CASHIER", ...}
"user_type"           → String "staff"
"permissions_updated" → Long (epoch millis)
```

### 4. Refresh Strategy

| Trigger            | Action                        |
| ------------------ | ----------------------------- |
| After login        | Fetch immediately             |
| App startup (cold) | Fetch if > 15 min stale       |
| App resume (warm)  | Fetch if > 15 min stale       |
| 403 from backend   | Fetch immediately, then retry |
| Pull-to-refresh    | Fetch immediately             |

### 5. Offline Behavior

- Use cached permissions (last known good)
- If no cache exists (fresh install), deny all
- Never allow more access offline than last sync granted

## PermissionManager (Singleton)

The central permission store, injected via Hilt:

```kotlin
@Singleton
class PermissionManager @Inject constructor(
    @ApplicationContext context: Context
) {
    // StateFlow for Compose reactivity
    val permissionsFlow: StateFlow<Set<String>>
    val modulesFlow: StateFlow<Set<String>>

    // Checks
    fun hasPermission(code: String): Boolean
    fun hasAnyPermission(codes: Collection<String>): Boolean
    fun hasAllPermissions(codes: Collection<String>): Boolean
    fun hasModule(code: String): Boolean
    fun isOwner(): Boolean
    fun isSuperAdmin(): Boolean
    fun isStale(): Boolean

    // Storage
    fun savePermissions(permissions: Set<String>)
    fun saveModules(modules: Set<String>)
    fun clear() // Call on logout
}
```

**Owner and Super Admin bypass all permission checks.** Check `user_type` first.

## UI Patterns

### Pattern 1: PermissionGate (Show/Hide)

```kotlin
@Composable
fun PermissionGate(
    permissionManager: PermissionManager,
    permission: String,
    hide: Boolean = true,          // true = render nothing when denied
    deniedContent: @Composable (() -> Unit)? = null,
    content: @Composable () -> Unit
)
```

**Use for:** FABs, action buttons, cards, sections that should be completely hidden
if the user lacks permission.

**Icon Policy:** Use custom PNG icons only; follow `android-custom-icons` and update `PROJECT_ICONS.md`.

**Report Table Policy:** If permissioned screens include reports that can exceed 25 rows, use table layouts (see `android-report-tables`).

```kotlin
// Hide "Create PO" FAB if user can't create POs
PermissionGate(permissionManager, Permission.INVENTORY_PO_CREATE) {
    FloatingActionButton(onClick = onCreatePO) {
        Icon(painterResource(R.drawable.add), "Create PO")
    }
}
```

### Pattern 2: PermissionButton (Disable with Message)

```kotlin
@Composable
fun PermissionButton(
    permissionManager: PermissionManager,
    permission: String,
    onClick: () -> Unit,
    text: String,
    deniedMessage: String = "You don't have permission"
)
```

**Use for:** Primary actions that users should SEE but can't perform
(approve, dispatch, receive, charge).

```kotlin
// "Approve" button - visible but disabled if no permission
PermissionButton(
    permissionManager = permissionManager,
    permission = Permission.INVENTORY_PO_APPROVE,
    onClick = { viewModel.approve() },
    text = "Approve",
    deniedMessage = "Approval restricted"
)
```

### Pattern 3: ModuleGate (Tab Visibility)

```kotlin
@Composable
fun ModuleGate(
    permissionManager: PermissionManager,
    module: String,
    content: @Composable () -> Unit
)
```

**Use for:** Bottom navigation tabs, entire feature sections.

```kotlin
// Filter bottom nav items by module access
val items = buildList {
    add(BottomNavItem.Dashboard) // Always visible
    if (permissionManager.hasModule(Module.POS)) add(BottomNavItem.POS)
    if (permissionManager.hasModule(Module.INVENTORY)) add(BottomNavItem.Inventory)
    add(BottomNavItem.Settings) // Always visible
}
```

### Pattern 4: Navigation Guard

```kotlin
// In NavHost: guard sensitive routes
composable("create_purchase_order") {
    if (permissionManager.hasPermission(Permission.INVENTORY_PO_CREATE)) {
        CreatePurchaseOrderScreen(...)
    } else {
        PermissionDeniedScreen(
            permission = "Create Purchase Orders",
            onBack = { navController.popBackStack() }
        )
    }
}
```

### Pattern 5: PermissionDeniedScreen

Full-screen blocker for navigation guards:

```kotlin
@Composable
fun PermissionDeniedScreen(
    permission: String,    // Human-readable name
    onBack: () -> Unit
)
// Shows: Lock icon + "Access Restricted" + explanation + "Go Back" button
```

## UX Guidelines

| Scenario                               | UX Pattern                     | Why                       |
| -------------------------------------- | ------------------------------ | ------------------------- |
| Tab the user can't access              | **Hide tab**                   | Clean nav, no confusion   |
| Button the user can't use              | **Disable + grey + message**   | User knows feature exists |
| Card/section user can't see            | **Hide**                       | Clean layout              |
| Screen user navigates to via deep link | **PermissionDeniedScreen**     | Graceful block            |
| 403 from server (stale cache)          | Auto-refresh perms, show toast | Transparent recovery      |
| Offline with cached perms              | Use cached perms normally      | Seamless offline          |
| Offline with no cached perms           | Deny all, show offline banner  | Fail-secure               |

## Backend Integration

### API Endpoint: GET /user/permissions

```json
{
    "success": true,
    "data": {
        "user_id": 10014,
        "franchise_id": 3,
        "user_type": "staff",
        "roles": [{"code": "CASHIER", "name": "Cashier"}],
        "permissions": ["DASHBOARD_VIEW", "POS_CREATE_SALE", ...],
        "modules": [
            {"code": "POS", "name": "Point of Sale", "is_enabled": true},
            {"code": "INVENTORY", "name": "Inventory", "is_enabled": false}
        ]
    }
}
```

### 403 Response Handling

```json
{
  "success": false,
  "message": "You do not have permission to perform this action",
  "error": {
    "code": "PERMISSION_DENIED",
    "required_permission": "INVENTORY_PO_APPROVE"
  }
}
```

Client response:

1. Parse `required_permission` from error
2. Auto-refresh permissions via `/user/permissions`
3. Show friendly message: "Your permissions have been updated"

## CompositionLocal (Convenience)

```kotlin
val LocalPermissionManager = staticCompositionLocalOf<PermissionManager> {
    error("No PermissionManager provided")
}

// In MainScaffold:
CompositionLocalProvider(LocalPermissionManager provides permissionManager) {
    // All child composables access via LocalPermissionManager.current
}
```

## Security Rules

1. **Never trust client-only checks** - Backend ALWAYS validates permissions
2. **Encrypted storage** - Use EncryptedSharedPreferences, never plain SharedPrefs
3. **Clear on logout** - `permissionManager.clear()` in logout flow
4. **Franchise isolation** - Permissions scoped to franchise_id in JWT
5. **No permission codes in logs** - Don't log full permission sets

## Integration with Other Skills

```
dual-auth-rbac (backend) → Defines permission tables, resolution logic, middleware
      ↓
mobile-rbac (THIS SKILL) → Android-specific permission caching, UI gates, offline
      ↓
jetpack-compose-ui → PermissionGate composables follow Material 3 patterns
      ↓
android-development → Hilt DI, MVVM, Clean Architecture integration
```

## Anti-Patterns

| Don't                                       | Do Instead                               |
| ------------------------------------------- | ---------------------------------------- |
| Resolve permissions locally from roles      | Fetch resolved set from backend          |
| Store permissions in plain SharedPrefs      | Use EncryptedSharedPreferences           |
| Check permissions only on client            | Backend MUST enforce (defense in depth)  |
| Grant access when offline with no cache     | Deny all (fail-secure)                   |
| Hardcode role names (`if role == "ADMIN"`)  | Check permission codes                   |
| Create separate permission check per screen | Use reusable `PermissionGate` composable |
| Hide buttons without explanation            | Show disabled state with message         |
| Skip permission refresh after 403           | Auto-refresh and re-evaluate             |
