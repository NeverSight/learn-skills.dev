---
name: zustand-store-scaffold
description: "Scaffold class-based Zustand stores with flattenActions: web (component-level store + Context + Provider) and core (slice-based store with immer). Class-based actions provide Go-to-Definition DX, #private field encapsulation, and prototype-safe slice composition."
metadata:
  author: adonis
  version: "1.0.0"
---

# Zustand Store Scaffold

Generate type-safe class-based Zustand stores with `flattenActions` for prototype-safe slice composition.

## Quick Start

### Web Pattern (Component-level Store)

```bash
python3 ~/.claude/skills/zustand-store-scaffold/scripts/scaffold_zustand_store.py \
  --pattern web \
  --name ToolList \
  --path web/src/pages/_components/ToolList/store
```

Generates:
- `types.ts` — `StoreSetter<T>` type definition
- `utils/flattenActions.ts` — Prototype-safe action flattener
- `index.ts` — Class-based store with `ActionImpl` + `flattenActions`
- `context.ts` — React Context and typed `useContext` hook
- `provider.tsx` — Memo-wrapped Provider component

### Core Pattern (Slice-based Store)

**Single Slice:**

```bash
python3 ~/.claude/skills/zustand-store-scaffold/scripts/scaffold_zustand_store.py \
  --pattern core \
  --name CoreAgent \
  --path packages/ag-ui-view/src/core/helpers/isomorphic/store
```

**Multiple Slices (Interactive):**

```bash
python3 ~/.claude/skills/zustand-store-scaffold/scripts/scaffold_zustand_store.py \
  --pattern core \
  --name AppStore \
  --path src/store
# Will prompt: Enter slice names (comma-separated, or press Enter for 'core'):
# Example input: auth,user,ui
```

**Multiple Slices (Direct):**

```bash
python3 ~/.claude/skills/zustand-store-scaffold/scripts/scaffold_zustand_store.py \
  --pattern core \
  --name AppStore \
  --path src/store \
  --slices auth,user,ui
```

Generates:
- `types.ts` — `StoreSetter<T>` type definition
- `utils/flattenActions.ts` — Prototype-safe action flattener
- `index.ts` — Store factory with `flattenActions` slice composition
- `slices/[name].ts` — Class-based slice with `ActionImpl` + `#private` fields

## Options

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--pattern` | Yes | Store pattern (`web` or `core`) | `--pattern web` |
| `--name` | Yes | Store name in PascalCase | `--name ToolList` |
| `--path` | Yes | Target directory path | `--path src/store` |
| `--slices` | No | Comma-separated slice names (core only) | `--slices auth,user,ui` |
| `--force` | No | Overwrite existing files | `--force` |

**Note:** For `core` pattern without `--slices`, the script interactively asks for slice names. Shared files (`types.ts`, `utils/flattenActions.ts`) are skipped if they already exist (unless `--force`).

## Choose the Right Pattern

| Pattern | Use When | Location Pattern | Slices |
|---------|----------|------------------|--------|
| **web** | Component-level state with Provider | `web/src/pages/_components/**/store` | N/A |
| **core** | Isomorphic/shared state with slices | `packages/**/store` | Single or multiple |

### When to Use Multiple Slices (Core Pattern)

Use multiple slices to organize complex state by feature domains:

| Scenario | Recommended Slices |
|----------|-------------------|
| Authentication app | `auth, user, session` |
| E-commerce store | `cart, products, user, ui` |
| Dashboard | `data, filters, ui, settings` |
| Chat application | `messages, contacts, ui, notifications` |

## Generated Files

| File | Purpose |
|------|---------|
| `types.ts` | `StoreSetter<T>` — type-safe overloaded setter matching Zustand internals |
| `utils/flattenActions.ts` | `flattenActions<T>` — walks prototype chain, binds methods, merges class instances |
| `index.ts` | Store factory combining initial state + `flattenActions` composition |
| `slices/*.ts` (core) | `*ActionImpl` class with `#set`/`#get`, exported via `create*Slice` |
| `context.ts` (web) | React Context + typed selector hook |
| `provider.tsx` (web) | Memo-wrapped Provider with ref-stable store creation |

## Post-Generation Steps

1. **Define state** in `*SliceState` interface (core) or `*StoreState` interface (web):
   ```ts
   export interface CoreSliceState {
     agents: Agent[]
     selectedId: string | null
   }
   ```

2. **Add action methods** as arrow functions in `*ActionImpl` class:
   ```ts
   export class CoreActionImpl {
     readonly #set: StoreSetter<CoreSlice>
     readonly #get: () => CoreSlice
     // ...constructor

     selectAgent = (id: string): void => {
       this.#set({ selectedId: id })
     }

     getSelectedAgent = (): Agent | undefined => {
       const { agents, selectedId } = this.#get()
       return agents.find((a) => a.id === selectedId)
     }
   }
   ```

3. **Set initial state** in the store factory or config:
   ```ts
   const store = createCoreAgentStore({
     initialState: { agents: [], selectedId: null }
   })
   ```

## Usage Examples

### Web Store Usage

```tsx
import Provider from './store/provider'
import { useToolListContext } from './store/context'

function ToolListPage() {
  return (
    <Provider>
      <ToolListContent />
    </Provider>
  )
}

function ToolListContent() {
  const toolList = useToolListContext((s) => s.toolList)
  const setToolList = useToolListContext((s) => s.setToolList)
  // Go to Definition on setToolList → lands directly on ActionImpl method
}
```

### Core Store Usage

```ts
import { createCoreAgentStore } from './store'

const store = createCoreAgentStore({
  initialState: { agents: [], selectedId: null }
})

// Vanilla JS
const state = store.getState()
state.selectAgent('agent-1')

// React (with useStore)
import { useStore } from 'zustand'

function AgentList() {
  const agents = useStore(store, (s) => s.agents)
  const selectAgent = useStore(store, (s) => s.selectAgent)
}
```

## References

- See `references/class-based-pattern.md` for detailed pattern documentation
- See `references/store-patterns.md` for complete code examples
- Reference PR: [lobehub#12081](https://github.com/lobehub/lobehub/pull/12081)
