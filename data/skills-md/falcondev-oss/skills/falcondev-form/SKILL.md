---
name: falcondev-form
description: >
  Building or editing forms with @falcondev-oss/form — the type-safe,
  reactive, schema-driven form library (packages form-core, form-react,
  form-vue) built on @vue/reactivity. Use when working with useForm /
  useFormCore, form.fields accessors, $use(), field.value / field.handleChange
  / field.model, form.data, or a Standard Schema (zod v4 / arktype) form in a
  React or Vue codebase.
---

# @falcondev-oss/form

A framework-agnostic form-state library on top of `@vue/reactivity`. You give it a **Standard Schema** (zod v4, arktype, …) and reactive **sourceValues**; it gives you a reactive form **handle** with a tree of field **accessors**.

Three published packages — pick the one for the runtime, never import `-core` directly in app code:

| Package | Entry | Adds |
|---|---|---|
| `@falcondev-oss/form-core` | `useFormCore`, all types, `/reactive` helpers | engine; use directly only outside React/Vue |
| `@falcondev-oss/form-react` | `useForm`, `useField`, `FormFieldMemo` | React re-render integration, `field.model = {value,onUpdate}` |
| `@falcondev-oss/form-vue` | `useForm`, `useFormHandles` | `field.model` writable computed (`v-model`) |

`useForm` from the framework package wraps `useFormCore` — same options, same handle. Everything below is identical across frameworks **except** field binding and re-render (see `reference/frameworks.md`).

## Two ideas that explain everything

1. **Accessors are lazy paths; `$use()` materializes.** `form.fields.address.city` is just a typed path proxy — no field object exists yet. Calling `.$use()` creates (and caches) the actual reactive `FormField`. Navigate with dot/`.at()`, then `.$use()` at the leaf you bind.

2. **Form data is `NullableDeep`.** While editing, *every* value can be `null` — a half-filled form has nulls everywhere. So `form.data`, `field.value`, and accessor types are the schema's **input** type made deeply nullable (objects → `T | null`, arrays → `(T|null)[] | null`). The validated **output** type (non-null) only appears in `submit({ values })`. Write UI against nullable types; trust `submit` for clean data.

## Golden path

```ts
import { useForm } from '@falcondev-oss/form-vue' // or -react
import z from 'zod'

const form = useForm({
  schema: z.object({ name: z.string(), age: z.number() }),
  sourceValues, // initial data (NullableDeep); a value, getter, or ref — React needs a stable reference
  async submit({ values }) {
    // `values` is validated OUTPUT: { name: string, age: number }
    await api.save(values)
    // return nothing → { success: true }; return { success: false } to keep form dirty
  },
})

const nameField = form.fields.name.$use()
nameField.handleChange('Jane')   // programmatic write (validates, marks dirty)
// or write straight through the reactive data:
form.data.name = 'Jane'          // equivalent effect

await form.submit()              // validates whole schema, runs submit if valid
```

## `useForm(options)`

- `schema` — any **Standard Schema** that *also* exposes Standard JSON Schema (zod v4, arktype). JSON Schema drives `field.schema` metadata and required-detection. Non-JSON-representable types (Date, bigint, Map…) need a codec/transform or metadata extraction silently degrades (a console warning fires).
- `sourceValues` — initial `NullableDeep` data. A value, a getter `() => data`, or (Vue) a `ref`. In **React** it must be a *stable reference* — see below. May be `undefined` → form is **pending** (`isLoading`/`field.isPending` true, `data` is `undefined`, writes ignored) until it resolves. When it later changes: if the form is **not dirty**, the form resets to the new values; if dirty, the update is skipped with a warning (except during submit).
- `submit({ values })` — `async`, receives the **validated output**. Return `void`/`{success:true}` → form marked pristine; `{success:false}` → stays dirty. **`await` everything that must finish before the form settles** — most importantly cache/query invalidations, so fresh data flows back into `sourceValues` before the form is marked pristine (an un-awaited invalidation lets the form settle against stale data). With TanStack Query: `await queryClient.invalidateQueries(...)` directly in `submit`, or do it in the mutation's `onSuccess` and `await mutateAsync(...)` in `submit` (awaiting the mutation awaits `onSuccess`).
- `disabled?` — `boolean | Ref | getter`. Blocks `handleChange`/`handleBlur`/`reset` on all fields.
- `hooks?` — lifecycle hooks (see `reference/patterns.md`).

### Writing `sourceValues` (do it this way)

Three ordered branches: still-loading → existing entity → blank defaults. Vue takes them as a getter; React takes them as a `useMemo`ed value.

```ts
// Vue — getter, tracked reactively
useForm({
  schema,
  sourceValues: () => {
    if (isLoading.value) return undefined    // 1. source still loading → form is pending
    if (entity.value) return entity.value    // 2. edit: return the whole entity object
    return { name: null, age: null }         // 3. create: blank defaults
  },
  async submit({ values }) { /* … */ },
})
```

```tsx
// React — same branches, wrapped in useMemo
const sourceValues = useMemo(() => {
  if (isLoading) return undefined
  if (entity) return entity
  return { name: null, age: null }
}, [isLoading, entity])

useForm({ schema, sourceValues, async submit({ values }) { /* … */ } })
```

**In React `sourceValues` must be a stable reference.** Never inline the object (or a getter) in the `useForm` call: React re-runs the component body every render, so a fresh object identity re-seeds the form on every render — resetting a clean form and warning on a dirty one. Memoize it (`useMemo`), or hoist a constant to module scope, or pass query data directly (`sourceValues: query.data` — already stable). Getters are worse than useless here: the adapter captures the getter **once** on mount, so one built over React state or props is frozen at its first-render closure and never sees an update.

- **Return `undefined` while the source is loading** (e.g. the fetch for the entity being edited is pending). This puts the form in the pending state instead of seeding it with a wrong/empty shape you'd have to overwrite later.
- **Return the existing entity as one whole object** — don't hand-build `{ name: entity?.name, age: entity?.age, … }` with optional chaining per key. If the entity doesn't match the schema, spread and override just the divergent fields: `return { ...entity, tags: entity.tags ?? [] }`.
- **Use `null` for fields with no meaningful default** — not `''` or `0` just because the type is string/number. `NullableDeep` makes `null` valid for every field; an empty string is a *real value* that reads as "the user typed nothing", which is different from "untouched".

## The form handle

| Member | Type | Notes |
|---|---|---|
| `form.data` | `NullableDeep<T> \| undefined` | reactive; **read and write** directly (`form.data.x = …`). `undefined` while pending. |
| `form.fields` | accessor tree | navigate then `.$use()` |
| `form.isDirty` | `boolean` | any change made (edit count ≠ 0), reset by `submit` success / `reset` |
| `form.isChanged` | `boolean` | deep-equals current data vs `sourceValues` (false if edited back to original) |
| `form.isLoading` | `boolean` | submitting **or** pending source values |
| `form.isDisabled` | `boolean` | loading or `disabled` option |
| `form.errors` | `Issue[] \| undefined` | all validation issues, or undefined |
| `form.submit()` | `() => Promise<{success:boolean}>` | validates all, runs `submit` |
| `form.reset()` | `() => void` | restore to `sourceValues` |
| `form.hooks` | hookable | `hook`/`hookOnce`/`addHooks` |

## Field accessors

```ts
form.fields.user.email.$use()        // nested object
form.fields.tags.at(0).$use()        // array item (negative index ok: .at(-1))
form.fields.tags.$use()              // the array field itself
for (const item of form.fields.tags) item.$use()  // iterate (reactive)
form.fields.tags.delete(field.key)   // remove array item by its key (see below)
form.fields.$use()                   // root field = whole form value
form.fields['a.b'].$use()            // keys containing dots work (auto-escaped)
```

`.at(i)` accessor exists even before the array/index does — `.$use().value` is `null` until data arrives. `.delete(key)` **must** target an array item's key (`items[2]`), not a nested property — otherwise it throws.

## The `FormField` (result of `$use()`)

| Member | Notes |
|---|---|
| `field.value` | readonly ref of the field's `NullableDeep` value. Nested object props are still writable (writes flow to `form.data`); arrays can be `.push`ed. |
| `field.handleChange(v)` | set value, validate, mark dirty, fire field-change hooks |
| `field.handleBlur()` | validate if the field was edited (use on input blur) |
| `field.reset()` | restore this field to its source value |
| `field.errors` | `string[] \| undefined` — messages for this field (and nested unclaimed issues) |
| `field.schema` | `SchemaMeta` — `required`, `title`, `min/maxLength`, `minimum/maximum`, … from the schema (see patterns) |
| `field.disabled` / `field.isPending` | mirror form state |
| `field.isDirty` / `field.isChanged` | per-field, same semantics as form |
| `field.path` | dot/bracket path string |
| `field.key` | stable unique id (`path@timestamp-rand`); use as list `:key` and for `array.delete()` |
| `field.model` | **framework binding** — Vue: writable computed (`v-model`); React: `{ value, onUpdate }`. See frameworks. |
| `field.$()` | get the accessor tree *from* a field (to reach children of a `$use`d field) |

## Two write paths (equivalent)

- `field.handleChange(newValue)` — explicit, what input handlers call.
- `form.data.path = newValue` — direct reactive mutation; `on-change` observes it and triggers the same validation.

Both mark the form dirty and re-validate. Use `handleChange`/`model` in components; direct writes are handy in tests and effects.

## When validation runs

Whole-schema validation (not per-field), then issues are filtered to each field's path:
- **on submit** — always;
- **on change** — only if the field *already* has errors (so fixing an error clears it live);
- **on blur** — if the field was edited.

Errors clear while `isLoading`. A field also surfaces validation issues of nested paths that haven't been `$use`d yet.

## Gotchas

- **Read/write nullable, submit non-null.** Don't assume `field.value` is non-null in the UI.
- **`$use()` is required to bind.** Accessors alone are inert paths. In React, `$use()` re-renders the `useForm`-owning component; a **child** reading a field prop needs `useField(field)` or `FormFieldMemo` to re-render (see frameworks).
- **`sourceValues` won't overwrite a dirty form** (by design) — reset first if you need to force it.
- **`delete(key)` needs an array-item key**, and `field.key` changes when the array is replaced via `handleChange` (cache is cleared).
- Don't import from `-core` in a React/Vue app — you lose re-render/`model` integration.

## Deeper reference

- **Framework specifics** (React re-render/`useField`/`FormFieldMemo`, Vue `v-model`/`useFormHandles`, using core standalone) → read `reference/frameworks.md`.
- **Optional features** — discriminated unions (`$use({discriminator})`), value translation (`$use({translate})`), `field.schema` metadata, and hooks → read `reference/patterns.md`.
