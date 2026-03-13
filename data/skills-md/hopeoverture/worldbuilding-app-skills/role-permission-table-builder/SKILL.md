---
name: role-permission-table-builder
description: Generates comprehensive role-based permission matrices in markdown or SQL format for pages, components, and data access patterns. This skill should be used when designing authorization systems, documenting permissions, creating RBAC tables, or planning access control. Use for RBAC, role permissions, access control, authorization matrix, permission mapping, or security policies.
---

# Role Permission Table Builder

Generate and maintain comprehensive role-based access control (RBAC) permission matrices for worldbuilding applications.

## Overview

To build role permission systems:

1. Define user roles and hierarchies
2. Identify protected resources (pages, components, data, actions)
3. Create permission matrices mapping roles to resources
4. Generate implementation code for middleware and components
5. Document permission policies for team reference

## Role Definitions

### Standard Roles

Define common application roles:

- **Guest**: Unauthenticated users (read-only public content)
- **User**: Basic authenticated users (read own data, limited writes)
- **Creator**: Content creators (create/edit entities, manage own content)
- **Editor**: Content editors (edit any content, moderate submissions)
- **Admin**: System administrators (full access, user management)
- **Super Admin**: Platform owners (all permissions, system configuration)

### Custom Roles

To define worldbuilding-specific roles:

- **World Owner**: Creator of worldbuilding project
- **Collaborator**: Invited contributor to world
- **Viewer**: Read-only access to private world
- **Game Master**: Special permissions for RPG campaigns
- **Publisher**: Can publish worlds publicly

Consult `references/role-hierarchy.md` for role inheritance patterns.

## Permission Matrix

### Page-Level Permissions

To define page access:

| Page Route            | Guest | User | Creator | Editor | Admin |
| --------------------- | ----- | ---- | ------- | ------ | ----- |
| /                     | [OK]     | [OK]    | [OK]       | [OK]      | [OK]     |
| /login                | [OK]     | [OK]    | [OK]       | [OK]      | [OK]     |
| /dashboard            | [ERROR]     | [OK]    | [OK]       | [OK]      | [OK]     |
| /worlds/create        | [ERROR]     | [OK]    | [OK]       | [OK]      | [OK]     |
| /worlds/[id]          | 🔒     | 🔒    | [OK]       | [OK]      | [OK]     |
| /worlds/[id]/edit     | [ERROR]     | [ERROR]    | [OK]       | [OK]      | [OK]     |
| /admin/users          | [ERROR]     | [ERROR]    | [ERROR]       | [ERROR]      | [OK]     |
| /admin/settings       | [ERROR]     | [ERROR]    | [ERROR]       | [ERROR]      | [OK]     |

Legend:
- [OK] Full access
- 🔒 Conditional access (ownership/invitation)
- [ERROR] No access

### Component-Level Permissions

To define component visibility:

| Component              | Guest | User | Creator | Editor | Admin |
| ---------------------- | ----- | ---- | ------- | ------ | ----- |
| WorldList              | [OK] Public | [OK] All | [OK] All | [OK] All | [OK] All |
| WorldCreateButton      | [ERROR]     | [OK]    | [OK]       | [OK]      | [OK]     |
| EntityEditor           | [ERROR]     | [ERROR]    | [OK] Own   | [OK] All  | [OK] All |
| DeleteButton           | [ERROR]     | [ERROR]    | [OK] Own   | [OK] All  | [OK] All |
| ShareWorldButton       | [ERROR]     | [ERROR]    | [OK] Own   | [OK] All  | [OK] All |
| AdminPanel             | [ERROR]     | [ERROR]    | [ERROR]       | [ERROR]      | [OK]     |
| UserManagement         | [ERROR]     | [ERROR]    | [ERROR]       | [ERROR]      | [OK]     |

### Data Access Permissions

To define data operations:

| Operation                   | Guest | User     | Creator  | Editor | Admin |
| --------------------------- | ----- | -------- | -------- | ------ | ----- |
| Read public worlds          | [OK]     | [OK]        | [OK]        | [OK]      | [OK]     |
| Read private worlds         | [ERROR]     | 🔒 Invited | 🔒 Own    | [OK]      | [OK]     |
| Create world                | [ERROR]     | [OK]        | [OK]        | [OK]      | [OK]     |
| Update own world            | [ERROR]     | [OK]        | [OK]        | [OK]      | [OK]     |
| Update any world            | [ERROR]     | [ERROR]        | [ERROR]        | [OK]      | [OK]     |
| Delete own world            | [ERROR]     | [OK]        | [OK]        | [OK]      | [OK]     |
| Delete any world            | [ERROR]     | [ERROR]        | [ERROR]        | [ERROR]      | [OK]     |
| Create entity               | [ERROR]     | [ERROR]        | [OK]        | [OK]      | [OK]     |
| Update own entity           | [ERROR]     | [ERROR]        | [OK]        | [OK]      | [OK]     |
| Update any entity           | [ERROR]     | [ERROR]        | [ERROR]        | [OK]      | [OK]     |
| Delete entity               | [ERROR]     | [ERROR]        | [OK] Own    | [OK]      | [OK]     |
| Manage collaborators        | [ERROR]     | [ERROR]        | [OK] Own    | [OK]      | [OK]     |
| Publish world               | [ERROR]     | [ERROR]        | [OK] Own    | [OK]      | [OK]     |
| Moderate content            | [ERROR]     | [ERROR]        | [ERROR]        | [OK]      | [OK]     |
| Manage users                | [ERROR]     | [ERROR]        | [ERROR]        | [ERROR]      | [OK]     |

### Action Permissions

To define Server Action permissions:

| Server Action          | Guest | User | Creator | Editor | Admin |
| ---------------------- | ----- | ---- | ------- | ------ | ----- |
| createWorld            | [ERROR]     | [OK]    | [OK]       | [OK]      | [OK]     |
| updateWorld            | [ERROR]     | 🔒    | 🔒       | [OK]      | [OK]     |
| deleteWorld            | [ERROR]     | 🔒    | 🔒       | [ERROR]      | [OK]     |
| createEntity           | [ERROR]     | [ERROR]    | [OK]       | [OK]      | [OK]     |
| updateEntity           | [ERROR]     | [ERROR]    | 🔒       | [OK]      | [OK]     |
| deleteEntity           | [ERROR]     | [ERROR]    | 🔒       | [OK]      | [OK]     |
| inviteCollaborator     | [ERROR]     | [ERROR]    | 🔒       | [OK]      | [OK]     |
| publishWorld           | [ERROR]     | [ERROR]    | 🔒       | [OK]      | [OK]     |
| deleteUser             | [ERROR]     | [ERROR]    | [ERROR]       | [ERROR]      | [OK]     |

Use `scripts/generate_permission_matrix.py` to create customized permission tables.

## SQL Schema

To implement permissions in database:

```sql
-- Roles table
CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permissions table
CREATE TABLE permissions (
  id SERIAL PRIMARY KEY,
  resource VARCHAR(100) NOT NULL,
  action VARCHAR(50) NOT NULL,
  description TEXT,
  UNIQUE(resource, action)
);

-- Role permissions mapping
CREATE TABLE role_permissions (
  id SERIAL PRIMARY KEY,
  role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
  permission_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
  UNIQUE(role_id, permission_id)
);

-- User roles
CREATE TABLE user_roles (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, role_id)
);

-- Resource ownership
CREATE TABLE resource_ownership (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  resource_type VARCHAR(50) NOT NULL,
  resource_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(resource_type, resource_id)
);

-- Collaborators (for conditional access)
CREATE TABLE collaborators (
  id SERIAL PRIMARY KEY,
  world_id INTEGER REFERENCES worlds(id) ON DELETE CASCADE,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(50) NOT NULL,
  invited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(world_id, user_id)
);
```

Use `scripts/generate_rbac_schema.py` to generate database schema with seed data.

Reference `assets/rbac-schema.sql` for complete schema with indexes and constraints.

## Implementation

### Middleware Protection

To protect routes with middleware:

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getSession } from '@/lib/auth';
import { checkPermission } from '@/lib/permissions';

const protectedRoutes = {
  '/dashboard': ['user', 'creator', 'editor', 'admin'],
  '/worlds/create': ['user', 'creator', 'editor', 'admin'],
  '/admin': ['admin'],
};

export async function middleware(request: NextRequest) {
  const session = await getSession(request);
  const path = request.nextUrl.pathname;

  // Check if route requires authentication
  for (const [route, allowedRoles] of Object.entries(protectedRoutes)) {
    if (path.startsWith(route)) {
      if (!session) {
        return NextResponse.redirect(new URL('/login', request.url));
      }

      if (!allowedRoles.includes(session.user.role)) {
        return NextResponse.redirect(new URL('/unauthorized', request.url));
      }
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Component-Level Checks

To conditionally render components:

```typescript
// components/ProtectedComponent.tsx
import { useSession } from '@/lib/auth';
import { hasPermission } from '@/lib/permissions';

interface Props {
  requiredRole?: string[];
  requiredPermission?: string;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}

export function ProtectedComponent({
  requiredRole,
  requiredPermission,
  fallback = null,
  children,
}: Props) {
  const { session } = useSession();

  if (!session) {
    return <>{fallback}</>;
  }

  if (requiredRole && !requiredRole.includes(session.user.role)) {
    return <>{fallback}</>;
  }

  if (requiredPermission && !hasPermission(session.user, requiredPermission)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}
```

Usage:

```typescript
<ProtectedComponent requiredRole={['creator', 'editor', 'admin']}>
  <EntityEditor entity={entity} />
</ProtectedComponent>
```

Reference `assets/protected-component.tsx` for complete implementation.

### Server Action Protection

To protect Server Actions:

```typescript
// lib/permissions.ts
'use server';

import { getSession } from '@/lib/auth';
import { checkPermission } from '@/lib/rbac';

export async function requirePermission(permission: string) {
  const session = await getSession();

  if (!session) {
    throw new Error('Unauthorized');
  }

  const hasAccess = await checkPermission(session.user, permission);

  if (!hasAccess) {
    throw new Error('Forbidden');
  }

  return session;
}

export async function requireOwnership(resourceType: string, resourceId: number) {
  const session = await getSession();

  if (!session) {
    throw new Error('Unauthorized');
  }

  const isOwner = await checkOwnership(session.user.id, resourceType, resourceId);

  if (!isOwner && session.user.role !== 'admin') {
    throw new Error('Forbidden');
  }

  return session;
}
```

Usage in Server Actions:

```typescript
'use server';

import { requirePermission, requireOwnership } from '@/lib/permissions';

export async function updateEntity(entityId: number, data: EntityData) {
  await requireOwnership('entity', entityId);

  // Proceed with update
  return updateEntityInDB(entityId, data);
}

export async function deleteWorld(worldId: number) {
  const session = await requirePermission('world:delete');

  if (session.user.role !== 'admin') {
    await requireOwnership('world', worldId);
  }

  return deleteWorldFromDB(worldId);
}
```

### Dynamic Permission Checks

To implement complex permission logic:

```typescript
// lib/rbac.ts
export async function checkPermission(
  user: User,
  resource: string,
  action: string,
  context?: { resourceId?: number; ownerId?: number }
): Promise<boolean> {
  // Admin has all permissions
  if (user.role === 'admin') {
    return true;
  }

  // Check role-based permission
  const hasRolePermission = await hasRolePermission(user.role, resource, action);

  if (!hasRolePermission) {
    return false;
  }

  // Check ownership if required
  if (context?.resourceId) {
    const isOwner = await checkOwnership(user.id, resource, context.resourceId);
    return isOwner;
  }

  return true;
}
```

Consult `references/permission-check-patterns.md` for advanced patterns.

## Permission Utilities

Use `scripts/permission_utils.py` for common operations:

```bash
# Check user permissions
python scripts/permission_utils.py check --user-id 123 --permission "world:update"

# List role permissions
python scripts/permission_utils.py list-role --role creator

# Grant permission to role
python scripts/permission_utils.py grant --role editor --permission "entity:delete"

# Revoke permission from role
python scripts/permission_utils.py revoke --role user --permission "world:delete"
```

## Testing Permissions

To test authorization:

```typescript
// tests/permissions.test.ts
import { checkPermission } from '@/lib/rbac';

describe('RBAC', () => {
  it('admin can delete any world', async () => {
    const admin = { id: 1, role: 'admin' };
    const canDelete = await checkPermission(admin, 'world', 'delete');
    expect(canDelete).toBe(true);
  });

  it('creator can only delete own world', async () => {
    const creator = { id: 2, role: 'creator' };
    const ownWorld = { id: 10, ownerId: 2 };

    const canDeleteOwn = await checkPermission(creator, 'world', 'delete', {
      resourceId: ownWorld.id,
      ownerId: ownWorld.ownerId,
    });
    expect(canDeleteOwn).toBe(true);

    const othersWorld = { id: 11, ownerId: 3 };
    const canDeleteOthers = await checkPermission(creator, 'world', 'delete', {
      resourceId: othersWorld.id,
      ownerId: othersWorld.ownerId,
    });
    expect(canDeleteOthers).toBe(false);
  });
});
```

## Documentation Generation

Use `scripts/generate_permission_docs.py` to create permission documentation:

```bash
# Generate markdown documentation
python scripts/generate_permission_docs.py --format markdown --output docs/permissions.md

# Generate SQL seed data
python scripts/generate_permission_docs.py --format sql --output db/seeds/permissions.sql

# Generate TypeScript types
python scripts/generate_permission_docs.py --format typescript --output lib/types/permissions.ts
```

Output includes:

- Complete permission matrix tables
- Role hierarchy diagrams
- Implementation examples
- API documentation

Reference `assets/permission-docs-template.md` for documentation structure.

## Best Practices

1. **Principle of Least Privilege**: Grant minimum required permissions
2. **Role Hierarchy**: Implement role inheritance for simpler management
3. **Audit Logging**: Track permission checks and access attempts
4. **Regular Reviews**: Periodically audit and update permissions
5. **Clear Naming**: Use consistent, descriptive permission names
6. **Documentation**: Maintain up-to-date permission documentation
7. **Testing**: Test authorization for all roles and edge cases
8. **Graceful Degradation**: Show appropriate UI for unauthorized users

## Troubleshooting

Common issues:

- **Permission Denied Unexpectedly**: Check role assignments and ownership
- **Middleware Not Applied**: Verify middleware matcher configuration
- **Cached Permissions**: Clear session cache after permission changes
- **Inconsistent Checks**: Ensure same logic in middleware, components, and actions
- **Performance Issues**: Cache permission checks, use database indexes
