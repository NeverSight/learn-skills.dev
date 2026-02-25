---
name: add-hook
description: Step-by-step guide for adding a new React hook to the shadcn-hooks project. Use when the user wants to create, add, or implement a new hook in this repository.
---

# Add Hook

Guide for adding a new hook to the shadcn-hooks project. The source of truth is `src/registry/hooks/`. The `packages/shadcn-hooks/` directory is auto-generated via `pnpm run sync` and should NOT be edited manually.

## Checklist

Copy this checklist and track progress:

```
Add Hook: use-<name>
- [ ] Step 1: Create registry entry (src/registry/hooks/use-<name>/)
- [ ] Step 2: Register in meta.json
- [ ] Step 3: Update introduction.mdx
- [ ] Step 4: Create skill reference doc
- [ ] Step 5: Update skill SKILL.md function table
- [ ] Step 6: Verify (lint + test)
```

## Step 1: Create Registry Entry

Create directory `src/registry/hooks/use-<name>/` with 5 files:

### 1a. `index.ts` — Hook implementation

Rules:

- Use `@/registry/hooks/...` and `@/registry/lib/...` import aliases
- Named export: `export function use<Name>(...)`
- Export all public types from the same file
- TypeScript strict, no `any`
- Reuse existing hooks where possible (e.g. `useBoolean`, `useEventListener`, `useMemoizedFn`)

Reference example — simple hook:

```ts
// src/registry/hooks/use-previous/index.ts
import { useRef } from 'react'

export type ShouldUpdateFunc<T> = (prev?: T, next?: T) => boolean
const defaultShouldUpdate = <T>(a?: T, b?: T) => !Object.is(a, b)

export default function usePrevious<T>(
  state: T,
  shouldUpdate: ShouldUpdateFunc<T> = defaultShouldUpdate,
): T | undefined {
  const prevRef = useRef<T>()
  const curRef = useRef<T>()

  if (shouldUpdate(curRef.current, state)) {
    prevRef.current = curRef.current
    curRef.current = state
  }

  return prevRef.current
}
```

Reference example — hook composing other hooks:

```ts
// src/registry/hooks/use-hover/index.ts
import { useBoolean } from '@/registry/hooks/use-boolean'
import { useEventListener } from '@/registry/hooks/use-event-listener'
import type { BasicTarget } from '@/registry/lib/create-effect-with-target'

export interface UseHoverOptions {
  onEnter?: () => void
  onLeave?: () => void
  onChange?: (isHovering: boolean) => void
}

export function useHover(
  target: BasicTarget,
  options?: UseHoverOptions,
): boolean {
  const { onEnter, onLeave, onChange } = options || {}
  const [state, { setTrue, setFalse }] = useBoolean(false)
  useEventListener(
    'mouseenter',
    () => {
      onEnter?.()
      setTrue()
      onChange?.(true)
    },
    { target },
  )
  useEventListener(
    'mouseleave',
    () => {
      onLeave?.()
      setFalse()
      onChange?.(false)
    },
    { target },
  )
  return state
}
```

### 1b. `registry-item.json` — Dependencies

```json
{
  "registryDependencies": ["@hooks/use-dependency-a", "@hooks/use-dependency-b"]
}
```

- List all hooks/libs this hook depends on, prefixed with `@hooks/`
- If no dependencies: `{ "registryDependencies": [] }`

### 1c. `demo/demo-01.tsx` — Demo component

```tsx
'use client'
import { use<Name> } from '..'

export function Demo01() {
  // Interactive demo showcasing the hook
}
```

Rules:

- Must be a client component (`'use client'`)
- Import hook from `'..'` (parent directory)
- Use shadcn UI components from `~/components/ui/...` (e.g. `Button`, `Card`, `Input`)
- Demo should be interactive and clearly show the hook's behavior

### 1d. `index.mdx` — Documentation page

```mdx
---
title: use<Name>
description: A hook to <description>
---

import { Demo01 } from './demo/demo-01'

<Demo01 />

## Installation

<Tabs items={['CLI', 'Manual']}>
  <Tab>
    <InstallCLI value='use-<name>' />
  </Tab>
  <Tab>
    Copy and paste the following code into your project.
    <RegistrySourceCode value='use-<name>' />
  </Tab>
</Tabs>

## API

\`\`\`ts
// Full type declarations here
\`\`\`

## Credits

- [use-<name>](credit-link)
```

Notes:

- If the hook has internal dependencies, add multiple `<RegistrySourceCode>` entries under the Manual tab (see `use-boolean` which includes `use-toggle`)
- The API section should contain full TypeScript type declarations

### 1e. `index.test.ts` — Tests

```ts
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { use<Name> } from './index'

describe('use<Name>', () => {
  it('should ...', () => {
    const { result } = renderHook(() => use<Name>(...))
    expect(result.current).toBe(...)
  })
})
```

Rules:

- Use `vitest` + `@testing-library/react`
- Import from `'./index'`
- Cover: default behavior, state changes, edge cases, callbacks
- For DOM-based hooks, create elements in `beforeEach` / clean up in `afterEach`

## Step 2: Register in `meta.json`

Add `"use-<name>"` to `src/registry/hooks/meta.json` under the appropriate category:

- `---State---` — state management hooks
- `---Advanced---` — memoization, refs, advanced patterns
- `---Lifecycle---` — effects, timers, mount/unmount
- `---Browser---` — DOM, events, browser APIs
- `---Dev---` — development/debug utilities
- `---External---` — wrappers around external libraries

## Step 3: Update Introduction Page

Add the new hook to `content/docs/introduction.mdx` under the appropriate category section:

- **State Management** — state management hooks
- **Advanced** — memoization, refs, advanced patterns
- **Lifecycle & Effects** — effects, timers, mount/unmount
- **Browser** — DOM, events, browser APIs
- **Dev** — development/debug utilities
- **External Libraries** — wrappers around external libraries

Add a line in alphabetical order within the category:

```md
- [`use<Name>`](/docs/hooks/use-<name>) - <Short description>
```

## Step 4: Create Skill Reference

Create `skills/shadcn-hooks/references/use<Name>.md`:

```md
# use<Name>

<One-line description>.

## Usage

\`\`\`tsx
import { use<Name> } from '@/hooks/use-<name>'

function Component() {
// Minimal usage example
}
\`\`\`

## Type Declarations

\`\`\`ts
// Full type signatures
\`\`\`

## Parameters

| Parameter | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| ...       | ...  | ...     | ...         |

## Returns

| Type | Description |
| ---- | ----------- |
| ...  | ...         |
```

## Step 5: Update Skill Function Table

Add an entry to the appropriate category table in `skills/shadcn-hooks/SKILL.md`:

```md
| [`use<Name>`](references/use<Name>.md) | <description> | AUTO |
```

- Use `AUTO` for standalone hooks
- Use `EXTERNAL` for hooks that wrap external npm packages

## Step 6: Verify

1. Run linter: check edited files for lint errors
2. Run tests: `pnpm test run src/registry/hooks/use-<name>/index.test.ts`
3. Verify the dev server renders the doc page correctly (if running)

## Notes

- `packages/shadcn-hooks/` is auto-generated. Run `pnpm run sync` inside `packages/shadcn-hooks/` to regenerate after adding a new hook.
- `packages/shadcn-hooks/src/index.ts` exports are also auto-managed — no manual editing needed.
