---
name: react-craft
description: Enforces React naming conventions, component structure, readability, and test-first development. Use when creating, reviewing, or refactoring React components. For state management and composition patterns, install the companion skills listed below.
---

# React Craft

Naming, structure, testing, and readability for React components.

> **This skill covers naming, structure, testing, and readability.**
> State management, hooks discipline, composition patterns, and UI components are handled by companion skills.
> Install them alongside this one — the agent will pick them up automatically based on task context.
>
> ```bash
> # State & hooks (57 rules — derived state, useEffect misuse, waterfalls, bundle size)
> npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices
>
> # Composition (compound components, avoid boolean prop sprawl, state lifting)
> npx skills add vercel-labs/agent-skills --skill vercel-composition-patterns
>
> # State management decision framework (Zustand vs RTK vs React Query vs Jotai)
> npx skills add wshobson/agents --skill react-state-management
>
> # TDD workflow
> npx skills add obra/superpowers --skill test-driven-development
>
> # shadcn/ui (Radix + Tailwind component patterns, forms w/ RHF + Zod)
> npx skills add giuseppe-trisciuoglio/developer-kit --skill shadcn-ui
>
> # Tailwind v4 + shadcn setup
> npx skills add jezweb/claude-skills --skill tailwind-v4-shadcn
> ```

---

## 1. Test First

Identify test cases BEFORE writing implementation. Co-locate tests next to components.

```
Button/
├── Button.tsx
├── Button.test.tsx
└── index.ts
```

### What to test (priority order)
1. User behavior — clicks, typing, selection
2. Conditional rendering — right elements for right state
3. Edge cases — empty, error, loading, null, overflow
4. Accessibility — keyboard nav, roles, labels
5. Integration — works with parent/child context

### Rules

- Test behavior, not implementation. Query by `role`, `label`, `text` — never by classname or test ID unless unavoidable.
- One behavior per `it()` block.
- Descriptive names: `it('disables submit when form has validation errors')` not `it('works')`.
- No snapshot tests unless the markup is static and rarely changes.

```tsx
// ✅
it('calls onSearch with trimmed query on submit', async () => {
  const onSearch = vi.fn();
  render(<SearchInput onSearch={onSearch} />);
  await userEvent.type(screen.getByRole('searchbox'), '  react hooks  ');
  await userEvent.keyboard('{Enter}');
  expect(onSearch).toHaveBeenCalledWith('react hooks');
});

// ❌
it('works', () => {
  const { container } = render(<SearchInput onSearch={vi.fn()} />);
  expect(container.querySelector('.search-input')).toBeTruthy();
});
```

---

## 2. Naming

Every name should answer: "What is this and what does it do?"

### Components — PascalCase, noun-based

| ✅ | ❌ | Why |
|---|---|---|
| `InvoiceTable` | `Table1` | Describes what it renders |
| `UserAvatarDropdown` | `AvatarDD` | No abbreviations |
| `PaymentMethodForm` | `Form` | Too generic |

### Props — camelCase, intention-revealing

- Booleans: `is`, `has`, `should`, `can` prefix
- Events: `on` prefix (component API) / `handle` prefix (internal)
- Render slots: `render` prefix or `Content` suffix

```tsx
// ✅
interface ProductCardProps {
  product: Product;
  isOnSale: boolean;
  hasReviews: boolean;
  onAddToCart: (id: string) => void;
  renderBadge?: (product: Product) => ReactNode;
}

// ❌
interface ProductCardProps {
  data: any;
  sale: boolean;
  click: () => void;
}
```

### Hooks — always `use` + capability description

| ✅ | ❌ |
|---|---|
| `useDebounce(value, delay)` | `useDb(v, d)` |
| `usePaginatedProducts(filters)` | `useData(filters)` |

### Handlers & variables

- Handlers: `handle` + noun + verb → `handleFormSubmit`, `handleRowClick`
- Booleans: `isLoading`, `hasError`, `shouldRefetch`
- Transforms: `formatPrice`, `parseQueryParams`, `toSlug`
- Collections: plural → `users`, `cartItems`, `selectedIds`

### Files — kebab-case everywhere

All files use **kebab-case**. No exceptions. Consistency aids grep and discovery across the codebase.

| Type | Convention | Example |
|---|---|---|
| Components | `kebab-case.tsx` | `order-list-table.tsx` |
| Hooks | `use-*.ts` | `use-order-table-query.ts` |
| Utils | `kebab-case.ts` | `format-currency.ts` |
| Constants | `kebab-case.ts` | `route-paths.ts` |
| Types | `kebab-case.ts` | `order-types.ts` |
| API layer | `*.requests.ts` | `orders.requests.ts` |
| API hooks | `*.hooks.ts` | `orders.hooks.ts` |

---

## 3. Component Structure

### Anatomy (consistent order inside every component)

```tsx
// 1. Types (if co-located)
interface WidgetProps { ... }

// 2. Constants scoped to component
const TREND_ICONS = { up: TrendUp, down: TrendDown } as const;

// 3. Component
export function Widget({ title, metric, trend }: WidgetProps) {
  // 3a. Hooks (top, consistent order)
  const [isExpanded, setIsExpanded] = useState(false);
  const formatted = useMemo(() => formatNumber(metric), [metric]);

  // 3b. Derived values
  const TrendIcon = TREND_ICONS[trend];

  // 3c. Handlers
  const handleToggle = () => setIsExpanded(prev => !prev);

  // 3d. Early returns (guards)
  if (!metric) return <EmptyState title={title} />;

  // 3e. Render
  return ( ... );
}
```

### Readability rules

- **~150 lines max** per component. Extract sub-components or hooks if longer.
- **5-7 props max** before considering composition/compound patterns.
- **Destructure props** in the signature, not the body.
- **One component per file** (small co-located helpers are OK).
- **Early returns** for loading/error/empty — no nested ternary soup.

```tsx
// ❌ Ternary hell
{isLoading ? <Spinner /> : error ? <Error /> : data?.length ? data.map(...) : <Empty />}

// ✅ Guard clauses
if (isLoading) return <Spinner />;
if (error) return <ErrorMessage message={error} />;
if (!data?.length) return <EmptyState />;

return <div>{data.map(...)}</div>;
```

---

## 4. Project Structure

Scale to project size. Don't over-architect small projects.

**Small:**
```
src/
├── components/
├── hooks/
├── utils/
├── types.ts
└── App.tsx
```

**Medium/Large — Route-colocated architecture:**
```
src/
├── components/              # Shared/reusable UI only
│   ├── data-table/          # One concern per file — never mix unrelated components
│   ├── project-filter/
│   └── ...
├── routes/
│   └── orders/
│       └── order-list/
│           ├── order-list.tsx          # Page — orchestration only (~60-80 LOC)
│           ├── hooks/
│           │   └── use-order-table-query.ts
│           ├── components/
│           │   └── order-list-table.tsx
│           └── index.ts
├── hooks/                   # Shared hooks only
├── lib/
│   └── client/
│       └── orders.requests.ts   # Resource-scoped API layer
├── providers/
│   └── router/
│       └── route-map.tsx        # Lazy route modules
├── utils/
├── types/
└── constants/
```

### Route page files are orchestrators, not containers

A page file wires together hooks and components. It should not contain table configs, query logic, or form schemas.

```tsx
// ✅ ~60 LOC — orchestration only
export function OrderList() {
  const { data, isLoading } = useOrderTableQuery();
  const filters = useOrderFilters();

  if (isLoading) return <PageSkeleton />;

  return (
    <PageLayout title="Orders">
      <OrderFilters {...filters} />
      <OrderListTable data={data} />
    </PageLayout>
  );
}

// ❌ 400+ LOC page with inline table columns, filter logic, query params
```

### File size discipline

Target **~60 LOC avg** per file. Hard ceiling of **200 LOC** — if you hit it, split.

| LOC | Action |
|---|---|
| < 100 | Good |
| 100–200 | Review — can a hook or sub-component be extracted? |
| 200+ | Must split. Extract hooks/, components/, or utils/ next to the file. |

### Lazy route loading

Always use lazy imports in the router. Static imports bundle every page upfront.

```tsx
// ✅
{ path: "/orders", lazy: () => import("@/routes/orders/order-list") }

// ❌
import { OrderList } from "@/routes/orders/order-list";
{ path: "/orders", element: <OrderList /> }
```

### Barrel export scoping

- Feature barrels (`index.ts`) expose only the public API of that feature.
- **Never** create broad root barrels (e.g., `lib/index.ts` re-exporting everything) — they hurt tree-shaking and make implicit dependencies invisible.
- If only one feature uses a util, it lives in that feature folder, not in shared `lib/`.

```tsx
// ✅ Direct import
import { formatOrderDate } from "@/routes/orders/utils/format-order-date";

// ❌ Broad barrel
import { formatOrderDate } from "@/lib";
```

### Principles
- Colocate related code (tests, hooks, components next to their page)
- Route-local hooks/ and components/ before promoting to shared
- No circular deps between route features
- Max 3 levels of nesting
- Kebab-case for all file names (consistency aids grep/discovery)

---

## 5. Anti-Patterns (Real-World)

These are patterns found in production codebases that hurt readability and reviewability.

**God files with mixed concerns**
A 941-line `data-table.tsx` that contains both `ProjectFilter` and an unrelated `DataTable`. Split them — one concern per file, always.

**Fat providers**
A 460-line `auth-provider.tsx` doing data fetching, state management, and UI logic. Break into: `use-auth.ts` (hook) + `auth-context.tsx` (context) + `auth-guard.tsx` (UI boundary).

**Flat route dumping**
All pages in `routes/pages/` with shared logic in `routes/components/` means every page implicitly depends on the entire shared folder. Use route-colocated hooks/ and components/ instead.

**Broad barrels hiding dependencies**
A root `lib/index.ts` re-exporting everything makes it impossible to see what a feature actually depends on. Import directly from the source file.

**Static router imports**
Importing every page at the top of `router.tsx` bundles everything upfront. Use `lazy: () => import(...)` per route.

---

## 6. Accessibility Baseline

Every component must have:

- Semantic HTML: `<button>` for actions, `<a>` for nav — never `<div onClick>`
- Keyboard support: all interactive elements focusable, visible focus ring, Escape closes overlays
- ARIA when semantic HTML isn't enough: `aria-label` on icon buttons, `aria-live` for dynamic updates, `aria-expanded` for toggles
- Touch targets: min 44x44px on mobile

---

## 7. Pre-Ship Checklist

- [ ] Tests cover behavior, edge cases, a11y
- [ ] Names are self-documenting (component, props, hooks, handlers)
- [ ] Single responsibility — no "and" in the description
- [ ] File under 200 LOC — page files under 100
- [ ] No `any` types
- [ ] No `console.log`
- [ ] No magic strings/numbers — use named constants
- [ ] Loading, error, empty states handled
- [ ] Keyboard navigable
- [ ] Route is lazy-loaded
- [ ] No broad barrel imports — direct imports only
