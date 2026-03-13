---
name: vue-typescript
description: Master Vue TypeScript - Type-safe Components, Generics, Type Inference, Advanced Patterns
sasmp_version: "1.3.0"
bonded_agent: 07-vue-typescript
bond_type: PRIMARY_BOND
version: "2.0.0"
last_updated: "2025-01"
---

# Vue TypeScript Skill

Production-grade skill for mastering TypeScript integration with Vue 3 applications.

## Purpose

**Single Responsibility:** Teach TypeScript integration with Vue including typed components, generics, type inference, and advanced type patterns.

## Parameter Schema

```typescript
interface VueTypeScriptParams {
  topic: 'config' | 'components' | 'generics' | 'stores' | 'inference' | 'all';
  level: 'beginner' | 'intermediate' | 'advanced';
  context?: {
    strict_mode?: boolean;
    existing_js?: boolean;
  };
}
```

## Learning Modules

### Module 1: TypeScript Setup
```
Prerequisites: vue-fundamentals, TypeScript basics
Duration: 1-2 hours
Outcome: Configure TypeScript for Vue
```

| Topic | File | Content |
|-------|------|---------|
| tsconfig | tsconfig.json | Vue-specific config |
| Volar | Extension | IDE support |
| env.d.ts | Type declarations | Vite/Vue types |
| vue-tsc | Build check | Type validation |

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "jsxImportSource": "vue"
  },
  "include": ["src/**/*.ts", "src/**/*.vue"]
}
```

### Module 2: Typed Components
```
Prerequisites: Module 1
Duration: 3-4 hours
Outcome: Write type-safe components
```

| Feature | Syntax | Exercise |
|---------|--------|----------|
| Props | `defineProps<Props>()` | Typed props |
| Emits | `defineEmits<Emits>()` | Typed events |
| Defaults | `withDefaults()` | Default values |
| Expose | `defineExpose()` | Public API |
| Slots | `defineSlots()` | Typed slots |

**Typed Component:**
```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  items: Item[]
}

interface Emits {
  (e: 'update', value: string): void
  (e: 'select', item: Item): void
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<Emits>()
</script>
```

### Module 3: Generic Components
```
Prerequisites: Module 2
Duration: 3 hours
Outcome: Build reusable generic components
```

**Generic Component:**
```vue
<script setup lang="ts" generic="T extends { id: string | number }">
interface Props {
  items: T[]
  selected?: T
}

interface Emits {
  (e: 'select', item: T): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
</script>

<template>
  <ul>
    <li v-for="item in items" :key="item.id" @click="emit('select', item)">
      <slot :item="item" />
    </li>
  </ul>
</template>
```

### Module 4: Typed Composables & Stores
```
Prerequisites: Module 3
Duration: 3-4 hours
Outcome: Type-safe reusable logic
```

| Pattern | Typing Technique | Exercise |
|---------|------------------|----------|
| Composable return | Interface | useFetch<T> |
| Store state | Typed refs | User store |
| Getters | Computed types | Derived state |
| Actions | Async types | API actions |

**Typed Composable:**
```typescript
interface UseFetchReturn<T> {
  data: Ref<T | null>
  error: Ref<Error | null>
  loading: Ref<boolean>
  execute: () => Promise<void>
}

export function useFetch<T>(url: MaybeRefOrGetter<string>): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>
  // ...
  return { data, error, loading, execute }
}
```

### Module 5: Advanced Type Patterns
```
Prerequisites: Modules 1-4
Duration: 3-4 hours
Outcome: Expert-level Vue typing
```

| Pattern | Use Case | Example |
|---------|----------|---------|
| Utility types | Props extraction | ExtractProps<T> |
| Module augmentation | Route meta | RouteMeta interface |
| Conditional types | API responses | ResponseType<T> |
| Template refs | Component refs | ComponentRef<T> |

**Utility Types:**
```typescript
// Extract props from component
type ExtractProps<T> = T extends new () => { $props: infer P } ? P : never

// Deep partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

// Component ref type
type ComponentRef<T> = T extends new () => infer R ? R : never
const buttonRef = ref<ComponentRef<typeof Button> | null>(null)
```

## Validation Checkpoints

### Beginner Checkpoint
- [ ] Configure tsconfig for Vue
- [ ] Use defineProps with types
- [ ] Use defineEmits with types
- [ ] Fix basic type errors

### Intermediate Checkpoint
- [ ] Create generic component
- [ ] Type composable return values
- [ ] Type Pinia store
- [ ] Use withDefaults correctly

### Advanced Checkpoint
- [ ] Implement utility types
- [ ] Augment route meta types
- [ ] Type complex generics
- [ ] Achieve zero any types

## Retry Logic

```typescript
const skillConfig = {
  maxAttempts: 3,
  backoffMs: [1000, 2000, 4000],
  onFailure: 'simplify_type_definition'
}
```

## Observability

```yaml
tracking:
  - event: type_error_fixed
    data: [error_code, file]
  - event: pattern_learned
    data: [pattern_name, complexity]
  - event: skill_completed
    data: [strict_mode, any_count]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| defineProps not typed | Missing generic | Add `<Props>` |
| Cannot find module | Missing declaration | Add env.d.ts |
| Generic not working | Vue < 3.3 | Upgrade Vue |
| Type not inferred | Complex type | Explicit annotation |

### Debug Steps

1. Check Volar is enabled
2. Run vue-tsc for errors
3. Verify tsconfig paths
4. Check type imports

## Unit Test Template

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import GenericList from './GenericList.vue'

interface User {
  id: number
  name: string
}

describe('GenericList', () => {
  it('renders items with correct types', () => {
    const users: User[] = [
      { id: 1, name: 'Alice' },
      { id: 2, name: 'Bob' }
    ]

    const wrapper = mount(GenericList<User>, {
      props: { items: users },
      slots: {
        default: ({ item }: { item: User }) => item.name
      }
    })

    expect(wrapper.text()).toContain('Alice')
    expect(wrapper.text()).toContain('Bob')
  })

  it('emits typed select event', async () => {
    const users: User[] = [{ id: 1, name: 'Alice' }]
    const wrapper = mount(GenericList<User>, {
      props: { items: users }
    })

    await wrapper.find('li').trigger('click')
    const emitted = wrapper.emitted('select')
    expect(emitted?.[0][0]).toEqual({ id: 1, name: 'Alice' })
  })
})
```

## Usage

```
Skill("vue-typescript")
```

## Related Skills

- `vue-fundamentals` - Prerequisite
- `vue-composition-api` - For typed composables
- `vue-testing` - Type-safe testing

## Resources

- [Vue TypeScript Guide](https://vuejs.org/guide/typescript/overview.html)
- [Volar](https://github.com/vuejs/language-tools)
- [vue-tsc](https://github.com/vuejs/language-tools/tree/master/packages/vue-tsc)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
