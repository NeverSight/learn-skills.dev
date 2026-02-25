---
name: route-scaffolder
description: Scaffold complete CRUD routes for React Router v7 - Generate list, create, details, and edit routes following best practices
tags: [react-router, scaffolding, crud, code-generation]
version: 1.0.0
author: Code Visionary
---

# Route Scaffolder

Quickly scaffold complete CRUD (Create, Read, Update, Delete) routes for React Router v7 applications following best practices and conventions.

## Quick Reference

### Basic Route Structure

```
app/routes/
├── users/
│   ├── route.tsx           # Layout (optional)
│   ├── _index/            # List route
│   │   ├── route.tsx
│   │   └── loader.ts
│   ├── $userId/           # Details route
│   │   ├── route.tsx
│   │   └── loader.ts
│   ├── new/               # Create route
│   │   ├── route.tsx
│   │   └── action.ts
│   └── $userId.edit/      # Edit route
│       ├── route.tsx
│       ├── loader.ts
│       └── action.ts
```

### Route Configuration

```typescript
// app/routes.ts
import { type RouteConfig, route, layout, index } from "@react-router/dev/routes";

export default [
  layout("routes/users/route.tsx", [
    index("routes/users/_index/route.tsx"),
    route("new", "routes/users/new/route.tsx"),
    route(":userId", "routes/users/$userId/route.tsx"),
    route(":userId/edit", "routes/users/$userId.edit/route.tsx"),
  ]),
] satisfies RouteConfig;
```

## When to Use This Skill

- Creating new entity CRUD operations
- Scaffolding admin interfaces
- Building data management pages
- Setting up resource routes
- Establishing consistent route patterns

## CRUD Route Patterns

### 1. List Route (Index)

**Purpose**: Display all items, with search/filter/pagination

**File**: `routes/users/_index/route.tsx`

```typescript
import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData, Link } from "react-router";

// Loader
export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  const search = url.searchParams.get("q") || "";
  const page = Number(url.searchParams.get("page")) || 1;
  
  const users = await fetchUsers({ search, page });
  
  return { users, search, page };
}

// Component
export default function UsersList() {
  const { users, search } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <div className="header">
        <h1>Users</h1>
        <Link to="/users/new">Create User</Link>
      </div>
      
      <input 
        type="search" 
        name="q" 
        defaultValue={search}
        placeholder="Search users..."
      />
      
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>
                <Link to={`/users/${user.id}`}>View</Link>
                <Link to={`/users/${user.id}/edit`}>Edit</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### 2. Create Route

**Purpose**: Form to create new item

**File**: `routes/users/new/route.tsx`

```typescript
import type { ActionFunctionArgs } from "react-router";
import { Form, redirect, useActionData } from "react-router";
import { z } from "zod";

// Validation schema
const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

// Action
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  const result = createUserSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
  });
  
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
    };
  }
  
  const user = await createUser(result.data);
  
  return redirect(`/users/${user.id}`);
}

// Component
export default function CreateUser() {
  const actionData = useActionData<typeof action>();
  
  return (
    <div>
      <h1>Create User</h1>
      
      <Form method="post">
        <div>
          <label htmlFor="name">Name</label>
          <input type="text" id="name" name="name" required />
          {actionData?.errors?.name && (
            <span className="error">{actionData.errors.name[0]}</span>
          )}
        </div>
        
        <div>
          <label htmlFor="email">Email</label>
          <input type="email" id="email" name="email" required />
          {actionData?.errors?.email && (
            <span className="error">{actionData.errors.email[0]}</span>
          )}
        </div>
        
        <button type="submit">Create User</button>
      </Form>
    </div>
  );
}
```

### 3. Details Route

**Purpose**: Display single item details

**File**: `routes/users/$userId/route.tsx`

```typescript
import type { LoaderFunctionArgs } from "react-router";
import { useLoaderData, Link } from "react-router";

// Loader
export async function loader({ params }: LoaderFunctionArgs) {
  const user = await fetchUser(params.userId);
  
  if (!user) {
    throw new Response("Not Found", { status: 404 });
  }
  
  return { user };
}

// Component
export default function UserDetails() {
  const { user } = useLoaderData<typeof loader>();
  
  return (
    <div>
      <div className="header">
        <h1>{user.name}</h1>
        <div>
          <Link to="edit">Edit</Link>
          <Link to="/users">Back to List</Link>
        </div>
      </div>
      
      <dl>
        <dt>Email</dt>
        <dd>{user.email}</dd>
        
        <dt>Created</dt>
        <dd>{new Date(user.createdAt).toLocaleDateString()}</dd>
      </dl>
    </div>
  );
}
```

### 4. Edit Route

**Purpose**: Form to update existing item

**File**: `routes/users/$userId.edit/route.tsx`

```typescript
import type { LoaderFunctionArgs, ActionFunctionArgs } from "react-router";
import { useLoaderData, Form, redirect, useActionData } from "react-router";
import { z } from "zod";

// Validation schema
const updateUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

// Loader - get current data
export async function loader({ params }: LoaderFunctionArgs) {
  const user = await fetchUser(params.userId);
  
  if (!user) {
    throw new Response("Not Found", { status: 404 });
  }
  
  return { user };
}

// Action - handle update
export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData();
  
  const result = updateUserSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
  });
  
  if (!result.success) {
    return {
      errors: result.error.flatten().fieldErrors,
    };
  }
  
  await updateUser(params.userId, result.data);
  
  return redirect(`/users/${params.userId}`);
}

// Component
export default function EditUser() {
  const { user } = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  
  return (
    <div>
      <h1>Edit User</h1>
      
      <Form method="post">
        <div>
          <label htmlFor="name">Name</label>
          <input 
            type="text" 
            id="name" 
            name="name" 
            defaultValue={user.name}
            required 
          />
          {actionData?.errors?.name && (
            <span className="error">{actionData.errors.name[0]}</span>
          )}
        </div>
        
        <div>
          <label htmlFor="email">Email</label>
          <input 
            type="email" 
            id="email" 
            name="email" 
            defaultValue={user.email}
            required 
          />
          {actionData?.errors?.email && (
            <span className="error">{actionData.errors.email[0]}</span>
          )}
        </div>
        
        <button type="submit">Save Changes</button>
      </Form>
    </div>
  );
}
```

### 5. Delete Action (Optional)

Add delete functionality to details or edit routes:

```typescript
export async function action({ request, params }: ActionFunctionArgs) {
  const formData = await request.formData();
  const intent = formData.get("intent");
  
  if (intent === "delete") {
    await deleteUser(params.userId);
    return redirect("/users");
  }
  
  // Handle other actions...
}

// In component
<Form method="post">
  <input type="hidden" name="intent" value="delete" />
  <button type="submit">Delete User</button>
</Form>
```

## Layout Routes

Use layout routes to share UI across child routes:

```typescript
// routes/users/route.tsx
import { Outlet } from "react-router";

export default function UsersLayout() {
  return (
    <div className="users-layout">
      <nav>
        <Link to="/users">Users</Link>
        {/* Other navigation */}
      </nav>
      
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}
```

## Advanced Patterns

### 1. Nested Resources

```typescript
// app/routes.ts
export default [
  layout("routes/users/route.tsx", [
    index("routes/users/_index/route.tsx"),
    route(":userId", "routes/users/$userId/route.tsx", [
      // Nested posts under user
      route("posts", "routes/users/$userId/posts/route.tsx"),
      route("posts/:postId", "routes/users/$userId/posts/$postId/route.tsx"),
    ]),
  ]),
] satisfies RouteConfig;
```

### 2. Search/Filter Routes

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const url = new URL(request.url);
  
  // Parse query params
  const filters = {
    search: url.searchParams.get("q") || "",
    status: url.searchParams.get("status") || "all",
    page: Number(url.searchParams.get("page")) || 1,
    sort: url.searchParams.get("sort") || "name",
  };
  
  const users = await fetchUsers(filters);
  
  return { users, filters };
}
```

### 3. Bulk Actions

```typescript
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const intent = formData.get("intent");
  
  if (intent === "bulk-delete") {
    const ids = formData.getAll("ids");
    await deleteUsers(ids);
    return { success: true };
  }
  
  // Other intents...
}

// In component
<Form method="post">
  <input type="hidden" name="intent" value="bulk-delete" />
  {users.map(user => (
    <label key={user.id}>
      <input type="checkbox" name="ids" value={user.id} />
      {user.name}
    </label>
  ))}
  <button type="submit">Delete Selected</button>
</Form>
```

## Scaffolding Checklist

When creating complete CRUD routes:

- [ ] Create list route (`_index`)
- [ ] Create details route (`$id`)
- [ ] Create create route (`new`)
- [ ] Create edit route (`$id.edit`)
- [ ] Add delete functionality (optional)
- [ ] Register routes in `app/routes.ts`
- [ ] Add navigation links
- [ ] Implement validation with Zod
- [ ] Add error handling
- [ ] Add loading states
- [ ] Test all routes

## Best Practices

- [ ] Use consistent naming conventions
- [ ] Follow React Router file conventions
- [ ] Validate all form inputs with Zod
- [ ] Handle errors with error boundaries
- [ ] Use TypeScript for type safety
- [ ] Add loading states with useNavigation
- [ ] Implement optimistic UI where appropriate
- [ ] Use intent-based actions for multiple operations
- [ ] Add breadcrumbs for deep navigation
- [ ] Include pagination for large lists

## Anti-Patterns

Things to avoid:

- ❌ Inconsistent route naming
- ❌ Missing validation in actions
- ❌ Not handling 404 errors
- ❌ Fetching data in components (use loaders)
- ❌ Mutating data in loaders
- ❌ Not using TypeScript types
- ❌ Forgetting to register routes
- ❌ Overly complex route nesting

## References

- [React Router Route Configuration](https://reactrouter.com/start/framework/routing)
- [React Router Data Loading](https://reactrouter.com/start/framework/data-loading)
- [React Router Actions](https://reactrouter.com/start/framework/actions)
- [loader-action-optimizer skill](../loader-action-optimizer/)
- [form-state-manager skill](../form-state-manager/)
- [typescript-patterns skill](../typescript-patterns/)
