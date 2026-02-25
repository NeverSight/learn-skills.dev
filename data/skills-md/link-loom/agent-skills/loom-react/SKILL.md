---
name: loom-react
description: Develop FRONTEND React components, pages, and UI logic for Link Loom web applications. Handles view rendering, user interactions, and client-side state using `link-loom-react-sdk`.
license: Apache 2.0
author: Blackwood Stone Holdings, Inc.
compatibility: Requires React, Vite, Bootstrap 5
allowed-tools: Bash(git:*) Bash(jq:*) Read
---

# Link Loom React Development Skill

This skill standardizes frontend development for Link Loom applications, enforcing consistency in styling, structure, and code quality.

## Table of Contents

1.  [Coding Standards](#1-coding-standards)
2.  [Naming Conventions](#2-naming-conventions)
3.  [Directory Structure](#3-directory-structure)
4.  [Styling Guidelines](#4-styling-guidelines)
5.  [Component Guidelines](#5-component-guidelines)
    - [Pages](#pages)
    - [Components](#components)
    - [Services](#services)
    - [Hooks](#hooks)
6.  [General Best Practices](#6-general-best-practices)
7.  [Resources & Documentation](#7-resources--documentation)
8.  [Examples](#8-examples)
9.  [Edge Cases](#9-edge-cases)

---

## 1. Coding Standards

### **Flat-Style & Defensive Coding**

- **Guard Clauses**: Check for null/undefined/error conditions early.
- **No Pyramid of Doom**: Avoid deep nesting.
- **Hooks Rules**: Respect hook dependencies and order.

**Bad:**

```javascript
useEffect(() => {
  if (user) {
    if (user.isActive) {
      loadData();
    }
  }
}, [user]);
```

**Good:**

```javascript
useEffect(() => {
  if (!user || !user.isActive) {
    return;
  }

  loadData();
}, [user]);
```

---

## 2. Naming Conventions

**Strictly** adhere to these naming conventions.

| Type          | Path Pattern                                            | Naming Style              | Example                                             |
| :------------ | :------------------------------------------------------ | :------------------------ | :-------------------------------------------------- |
| **Page**      | `src/pages/<Module>/<PageName>.page.jsx`                | `PascalCase.jsx`          | `src/pages/account/AccountProfile.page.jsx`         |
| **Component** | `src/components/<Category>/<Name>/<Name>.component.jsx` | `PascalCase.jsx`          | `src/components/shared/Navbar/Navbar.component.jsx` |
| **Service**   | `src/services/<Module>/<SubModule>/<name>.service.js`   | `[Domain][Entity]Service` | `IdentityUserManagementService`                     |
| **Hook**      | `src/hooks/<name>.hook.jsx`                             | `useCamelCase.jsx`        | `src/hooks/useAuth.hook.jsx`                        |

---

## 3. Directory Structure

Keep components modular.

```text
src/
├── components/          # Reusable UI components
│   └── <Category>/      # e.g., shared, layout, forms
├── pages/               # Route-level components
│   └── <Module>/        # e.g., account, dashboard
├── services/            # API interaction logic
├── hooks/               # Custom hooks
└── layouts/             # Page layouts
```

---

## 4. Styling Guidelines

**Primary Directive**: Use **Bootstrap 5** classes.
**Order of styling**: Use it always:

1. Bootstrap 5 classes
2. Styled-components: Only if bootstrap do not have any implementation for the style you need.
3. Inline styles: Only if bootstrap and styled-components do not have any implementation for the style you need and if is strictly necessary.

- **Layout**: `row`, `col-12`, `col-md-6`, `d-flex`, `justify-content-between`, `align-items-center`, `my-4`, `p-3`, and so on. Do not use MUI Grid.
- **Components**: Primarily use MUI components or Link Loom SDK components. Only use custom components if MUI or Link Loom SDK do not have any implementation for the component you need.
- **Typography**: `h1`, `p`, `text-muted`, `fw-bold`, and so on. Prevent usage of MUI Typography.
- **Avoid**: Custom CSS for layout. Use custom classes only for specific design tokens (colors, branding) not covered by Bootstrap.
- **Icons**: Use MUI icons and import them from `@mui/icons-material` as:

```javascript
import { AccountCircle as AccountCircleIcon } from "@mui/icons-material";
```

---

## 5. Component Guidelines

### Domain Driven Design (DDD) & Parity

**CRITICAL**: Frontend structure **MUST** mirror the backend domain structure 1:1.

- If backend is `workflow-orchestration/control-plane/flow-design/flow-definition`, frontend **MUST** be `src/components/pages/workflow-orchestration/control-plane/flow-design/flow-definition`.
- Never disconnect a component from its domain.

### Pages

- **Role**: Orchestration ONLY. **NO business logic**.
- **Structure**: Orchestrate `*Manager` or `*List` components.
- **Container**: Always wrap content in `container-fluid my-4`.

### Components

- **Standard Set**: Every feature typically needs:
  - `manager/` (Orchestrates View/Edit modes)
  - `list/` (Table/Grid view)
  - `edit/` (Form)
  - `preview/` (Read-only details)
  - `quick-actions/` (Optional)
- **Entry Point**: Must implement `initializeComponent` function to load data.
- **Communication**: Must implement `itemOnAction(action, entity)` for event handling (e.g., `edit`, `delete`, `quick-view`).
- **Manager Pattern**: The `*Manager` component controls state (`isEditMode`) to toggle between `Preview` and `Edit`.
- **Subcomponents**: If a component (especially Manager) becomes complex, split it into `subcomponents/` folder to improve maintenance.
- **Shared Components**: If a component is used in multiple places, move it to `src/components/shared`. These are candidates for the Link Loom SDK.
- **Navigation**: **MUST** use Lazy Loading. No hard redirects. Use `useNavigate` and standard routing.

### Services

- **Base Class**: MUST extend `BaseApi` from `@services/base/api.service`.
- **No Axios**: NEVER use `axios` directly in components.
- **Adapters**: Use `fetchEntityCollection`, `fetchMultipleEntities`, `createEntityRecord`, `updateEntityRecord` from `@services/utils/entityServiceAdapter` for data fetching in components.

```javascript
// Example: initializeComponent with adapter
const initializeComponent = async () => {
  const [providers] = await fetchMultipleEntities([
    { service: MyService, payload: { queryselector: "all" } },
  ]);
  setEntities(providers?.result?.items || []);
};
```

---

## 6. General Best Practices

- **Language**: **English ONLY** for code and static text, unless explicitly requested otherwise by the user.
- **Documentation**: Avoid excessive comments. Document only complex algorithms. Code should be self-documenting.
- **KISS Principle**: keep it simple, stupid. Avoid overengineering. If a process is simple, keep the code simple.
- **Naming**: Use semantic variable names. **NEVER** use single-letter names like `x`, `ac`, `t`. Names must indicate intent.
- **Clean Code**: Remove unused imports, dependencies, and functions. No dead code.
- **Git**: Use **Conventional Commits** if asked to generate commit messages.
- **Design Patterns**: Act as an experienced architect. Use patterns (Factory, Singleton, Proxy, etc) **only** when necessary to solve a specific problem. Do not force patterns where simple logic suffices.
- **Context**: Do not infer if unsure. Always ask the user for clarification if requirements are not clear. Challenge user requests that lead to "garbage code" or antipatterns.
- **Strictness**: Since you are the expert, do not let the user start to write bad code patterns, warn him.
- **Linting**: **MANDATORY**. Code must be written adhering to the project's linter configuration (e.g., `.prettierrc`, `.eslintrc.js`).

---

## 7. Resources & Documentation

**CRITICAL**: Do not reinvent UI components. Check the Link Loom React SDK first.

- **Component Index**: `link-loom/github/link-loom-react-sdk/src/index.js`
  - Contains exports for `Alert`, `DataGrid`, `TextEditor`, `OnPageLoaded`, etc.
- **Component Source**: `link-loom/github/link-loom-react-sdk/src/components/`

Use `view_file` on the index to see available components before creating new ones.

---

## 8. Examples

### Page Component

See `assets/page.jsx`.

### Manager Component

See `assets/manager.jsx`.

### Component Implementation

See `assets/component.jsx`.

### Service Wrapper

See `assets/service.js`.

---

## 9. Edge Cases

- **Mobile Responsiveness**: Always test layout with `col-12` for mobile and `col-md-*` for desktop.
- **Missing Aliases**: If `@components` or `@services` fail, check `vite.config.js`. Use relative paths temporarily if aliases are broken, but flag for fix. Do not import directly from `src` except if it is a subcomponent of the current component.
- **Async Errors**: Always wrap async operations in `try-catch` inside `useEffect` or event handlers to prevent unhandled promise rejections.
