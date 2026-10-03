---
name: component-hierarchy
description: Next.js component tree
disable-model-invocation: true
---

# Component Hierarchy Visualizer

Trace a React component's position in the Next.js component tree and display it as an
easy-to-read ASCII tree diagram from the Page root down to the target component.

## Required MCP Tools

- **Serena**: `find_file`, `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `search_for_pattern`, `list_dir`
- **Sequential Thinking**: `sequentialthinking` — for organizing the recursive trace logic
- **Context7** (optional): `resolve-library-id`, `query-docs` — for referencing Next.js routing docs when needed

## Workflow

### Step 1: Detect Router Type

Determine whether the project uses App Router, Pages Router, or both.

1. Use Serena `list_dir` on the project root to check for:
   - `src/app/` or `app/` → **App Router**
   - `src/pages/` or `pages/` → **Pages Router**
   - Both can coexist
2. If unclear, use Serena `find_file` to search for `page.tsx` (App Router indicator) and
   check for a `pages/` directory structure.

The router type determines what counts as a "Page" (the root of the component tree):
- **Pages Router**: Any default-exported component in `pages/**/*.tsx` (excluding `_app`, `_document`)
- **App Router**: The default export in `app/**/page.tsx`, with `layout.tsx` as wrapping ancestors

### Step 2: Locate the Target Component

The user provides either a component name (e.g., `OrderSearchBox`) or a file name
(e.g., `OrderSearchBox.tsx`).

1. **File name given**: Use Serena `find_file` with the file name to locate the file path.
2. **Component name given**: Use Serena `find_symbol` with `name_path_pattern` set to the
   component name. If multiple matches exist, present them and ask the user to choose.
3. **No target given**: infer from the user's IDE context if available.
   - Prefer the currently focused file.
   - In that file, prefer the default-exported component or the primary exported React component.
   - If multiple likely components exist, ask the user to choose.
4. Confirm the component's file path and exported symbol name.

### Step 3: Trace Upward (Bottom-Up Traversal)

This is the core of the skill. Starting from the target component, recursively find parent
components until reaching a Page file.

Use Sequential Thinking to organize each step of the trace:

```
For each component in the chain (starting with the target):
  1. Call Serena find_referencing_symbols with the component's symbol name and file path
  2. Filter results to find JSX usage (look for <ComponentName in the referencing code snippets)
  3. If that result is empty or does not reveal a usable JSX parent, immediately fall back to:
     a. search_for_pattern("<ComponentName\\b")
     b. search_for_pattern("import .*ComponentName")
     c. inspect the matched file with get_symbols_overview or find_symbol
     d. only after these fail, consider the component potentially orphaned
  4. For each referencing parent:
     a. Record: parent component name, parent file path
     b. Check if the parent file is a Page file:
        - Pages Router: file path matches pages/**/*.tsx (not _app, _document)
        - App Router: file path ends with page.tsx or layout.tsx
     c. If Page found → trace complete for this path
     d. If not Page → continue tracing upward from this parent
  5. Handle edge cases:
     - If a component is re-exported through an index file, trace through the re-export
     - If multiple parents exist, trace ALL paths (component used in multiple places)
     - Set a depth limit of 20 to prevent infinite loops
     - If no JSX parent is found even after fallback searches, report "orphan component" (not rendered by any Page)
```

**Important**: When `find_referencing_symbols` returns results, look at the `relative_path` of
the referencing symbol to determine the parent file. Then use `find_symbol` or
`get_symbols_overview` on that file to identify the parent component name.

**Parent selection rule**: when identifying the parent component from a file, choose in this order:
1. the exported React component for the file
2. the top-level symbol that returns JSX around the matched usage
3. the best `get_symbols_overview` candidate that encloses the JSX usage

Avoid choosing helper hooks, memo callback internals, or unrelated file-level symbols as the parent.

### Step 4: Detect Wrapper Components

For Pages Router projects, check for common wrapping components:
- `_app.tsx` / `_app.js` — wraps all pages, include in the hierarchy as the outermost wrapper
- `PageComponent.getLayout = (...)` — include these wrappers between `_app.tsx` and the page body
- Provider components (Context providers, theme providers) that wrap the entire app

For App Router projects:
- `layout.tsx` files at each route segment level — each one wraps its child pages/layouts
- `template.tsx` if present

### Step 5: Build and Display the Tree

Assemble the traced paths into an ASCII tree diagram.

**Output format:**

```
📄 Page: /orders
   Route file: src/pages/orders/index.tsx
   Router: Pages Router
   Route root: OrdersPage
   Render path root: OrderLayout

🌳 Component Hierarchy:

_app.tsx (src/pages/_app.tsx)
└── OrdersPage (src/pages/orders/index.tsx)
    └── getLayout wrappers
        └── OrderLayout (src/features/orders/OrderLayout.tsx)
            ├── OrderSearchBox ⭐ TARGET (src/features/shared/order_search/order_search_box/OrderSearchBox.tsx)
            └── OrderTable (src/features/orders/OrderTable.tsx)

📊 Route depth: 3 levels from Page
📊 Render depth: 2 levels from render root
```

When a component appears in **multiple pages**, show all paths:

```
📄 Component "OrderSearchBox" is used in 2 pages:

━━━ Path 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Page: /orders
   Route file: src/pages/orders/index.tsx
   Route root: OrdersPage
   Render path root: OrdersPage

_app.tsx (src/pages/_app.tsx)
└── OrdersPage (src/pages/orders/index.tsx)
    └── OrderSearchBox ⭐ TARGET

━━━ Path 2 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Page: /dashboard
   Route file: src/pages/dashboard/index.tsx
   Route root: DashboardPage
   Render path root: SearchPanel

_app.tsx (src/pages/_app.tsx)
└── DashboardPage (src/pages/dashboard/index.tsx)
    └── SearchPanel (src/features/dashboard/SearchPanel.tsx)
        └── OrderSearchBox ⭐ TARGET
```

### Tree Drawing Rules

- Use `└──` for the last child, `├──` for other children
- Use `│` for vertical continuation lines
- Each node shows: `ComponentName (relative/file/path.tsx)`
- Mark the target with `⭐ TARGET`
- Show sibling components at the same level when they share the nearest parent (provides context)
- Prefer direct JSX siblings from the nearest returned JSX block, not unrelated file-level symbols
- Keep sibling display limited to at most 5 siblings to avoid noise; if more exist, show
  `... and N more siblings`
- If `getLayout`, `_app.tsx`, or `layout.tsx` wrappers exist, show them explicitly above the main render chain

### Depth Definitions

- **Route depth**: levels from the route file's page component to the target
- **Render depth**: levels from the practical render root after wrappers such as `getLayout` or `layout.tsx`

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Component not found | Report clearly; suggest checking the name/file spelling |
| Orphan component (no page renders it) | Only conclude this after trying `find_referencing_symbols` and the fallback `search_for_pattern` passes; then show the partial chain and note it's not connected to any page |
| Circular reference detected | Stop and report the cycle |
| Component used only in tests | Note that it's only referenced from test files, not from any page |
| Re-export through index.ts | Follow the re-export chain to find the actual JSX usage |
| Dynamic import / lazy load | Note `(lazy loaded)` in the tree node |
| Component used inside a Modal/Portal | Note `(via Portal)` — the DOM hierarchy differs from component hierarchy |

## What This Skill Does NOT Do

- Does not execute or render the application
- Does not trace runtime props or state flow (see `prop-drill` or `code-trace` skills for that)
- Does not modify any files
- Does not trace into node_modules or external library internals
