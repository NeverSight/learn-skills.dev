---
name: typescript-conventions
description: Standards for writing TypeScript code — types, enums, mappers, schemas, casts, iteration, compiler settings. Use when writing or reviewing any .ts or .tsx file, or configuring tsconfig, even if conventions aren't mentioned.
---

# TypeScript Conventions

Standards for how TypeScript is written here. For **where** files go and what they're named, see the `project-structure` skill — this skill covers the constructs themselves.

**Precedence.** Existing standards supersede this guide — the organization's, the language's, the framework's, and the repo's own, in that order. See the precedence rule in `project-structure`. Refactor existing code toward these standards only when asked to.

## Type vs Interface

Prefer `type`. Reach for `interface` in two cases only:

- **Extending a large built-in type** — `React.HTMLAttributes`, `HTMLDivElement`, and similar.
- **A package's overridable interface**, where declaration merging is the point: consumers inject their own types into it.

```ts
// ✅ Default
type User = { id: string; name: string };

// ⚠️ Justified — extending a large built-in
interface Props extends React.HTMLAttributes<HTMLDivElement> {}
```

## Discriminated unions

Prefer a discriminated union over a bag of optional fields, where the shape genuinely has distinct cases:

```ts
// ❌ every consumer needs a non-null assertion
type Result = { isSuccess: boolean; data?: User; error?: Error };

// ✅ narrowing gives you the right fields
type Result = { isSuccess: true; data: User } | { isSuccess: false; error: Error };
```

This is what makes the no-cast rule livable — an optional-field bag forces `result.data!` after checking the flag, while the union hands you the field already narrowed.

Not every optional field wants this. A shape with independently optional fields that don't correlate is a bag of options, not a set of cases, and forcing a union on it invents distinctions that don't exist.

## Enums

**Never use the `enum` keyword.** It emits a runtime object, doesn't narrow the way a union does, and `const enum` breaks under isolated modules.

```ts
enum DoNotUseThisKeyword {} // ❌
```

Use an object with `as const`, aliased by a type of the same name:

```ts
const Status = {
 Draft: "draft",
 Published: "published",
} as const;

type Status = ValueOf<typeof Status>;
```

The const and the type share a name deliberately — `Status.Draft` is the value, `Status` is the type, and there's one name to remember.

### ValueOf

```ts
type ValueOf<T> = T[keyof T];
```

Use the project's existing helper if there is one, or import from `type-fest` if it's already a dependency. Otherwise define it.

`(typeof Status)[keyof typeof Status]` is the same thing inline and is fine where a helper isn't available.

### Naming

- **Name** — `PascalCase`, **singular**. The type takes the same name.
- **Keys** — `PascalCase`. Acronyms are ordinary words: `StdLib`, `HttpStatus`, `XmlParser`. Never `SCREAMING_SNAKE_CASE`, never mixed within an enum.
- **Values** — `kebab-case` where context allows. External APIs and wire formats dictate their own.

```ts
const Source = {
 Local: "local",
 StdLib: "std-lib",
 HttpCache: "http-cache",
} as const;

type Source = ValueOf<typeof Source>;
```

### Object enums over array enums

Object form is singular and aliases cleanly. Derive the array when you need it:

```ts
const Statuses = Object.values(Status);
```

Name object-enums singular, array-enums plural. The type is always singular.

### Subset enums

When you need an enum covering part of another's values, pick by whether the subsets overlap.

**Split and spread** — when subsets are disjoint:

```ts
const SubValue = { A: "a", B: "b" } as const;
type SubValue = ValueOf<typeof SubValue>;

const OtherSubValue = { C: "c", D: "d" } as const;
type OtherSubValue = ValueOf<typeof OtherSubValue>;

const Value = { ...SubValue, ...OtherSubValue } as const;
type Value = ValueOf<typeof Value>;
```

These belong in one file — they're one concept expressed in parts.

**Derive an array subset** — when subsets overlap or the full enum is authoritative:

```ts
const Value = { A: "a", B: "b", C: "c", D: "d" } as const;
type Value = ValueOf<typeof Value>;

const SubValues = [Value.A, Value.B] as const;
type SubValue = (typeof SubValues)[number];
```

## Mappers

A consistent mapping between two domains — enum to label, status to color, DB value to UI value.

- **Name** — `camelCase`, `yByX`, read as **y = f(x)**: `colorByStatus` maps a status to a color.
- **Type** — `Record<X, Y>`. Keys are the input (`x`), values the output (`y`).
- **Never type-cast.** Use `as const satisfies`, which checks exhaustiveness while keeping literal inference.

```ts
const colorByStatus = {
 [Status.Draft]: "gray",
 [Status.Published]: "green",
 [Status.Archived]: "red",
} as const satisfies Record<Status, string>;
```

`satisfies` is what makes this work: annotating the variable would widen `'gray'` to `string`, and casting would skip the exhaustiveness check that catches a missing status when the enum grows.

## Schemas

A schema is a value and a type, like an object-enum — but unlike an enum, the clean name belongs to the type, so the schema carries a `Schema` suffix.

Which one drives the other depends on whether the project treats schemas or types as its source of truth. This is a project-level decision, not a per-schema one — check what the surrounding code does and match it.

**Schema drives type** — schemas are authoritative:

```ts
const ValueSchema = /* ... */;
type Value = infer<typeof ValueSchema>;
```

**Type drives schema** — types are authoritative and the schema is one representation of them:

```ts
// in the types file
type Value = { /* ... */ };

const ValueSchema = /* ... */ satisfies SchemaType<Value>;
type ValueShape = infer<typeof ValueSchema>;
```

`satisfies` catches most drift; inferring back out as `ValueShape` lets you compare the schema's actual output against the hand-written type.

Schemas compose — field schemas built up into larger ones are one cohesive concept and share a file. Keep schema code library-agnostic in principle; the pattern is the same across zod, valibot, and arktype.

## Namespace types alongside a class

When a class has useful accompanying types, export a type-only namespace of the same name. The namespace merges with the class, so `MyService` stays constructible while `MyService.Config` resolves as a type.

```ts
export declare namespace MyService {
  export type Config = { /* ... */ };
  export type inferSomething<T> = /* ... */;
}

export class MyService { /* ... */ }
```

## No type casts

**`as` is banned except for `as const`.** Use `satisfies`, type guards, or narrowing from `unknown`. The same goes for the non-null assertion `!` — it's a cast with different punctuation.

```ts
// ✅
if (error instanceof Error) log(error.message);

// ❌
log((error as Error).message);
log(error!.message);
```

A cast tells the compiler to stop checking; `satisfies` and guards keep it checking. When a cast feels necessary, the type is usually wrong somewhere upstream.

`Object.entries()` is a common trap here — it widens keys to `string` even on a typed record, and the reflex is `as`. Reach for `keyof` / `ValueOf` instead.

### unknown over any

`any` is a cast that spreads: it disables checking for everything it touches. Use `unknown` and narrow.

```ts
function parse(input: unknown) {} // ✅
function parse(input: any) {} // ❌
```

**Type-level positions are the exception.** In generic constraints, `unknown` breaks variance and `any` is the working answer:

```ts
function formatCallback<T extends (...args: any[]) => any>(fn: T) {}
function formatData<T extends Data<any, any, any>>(data: T) {}
```

This comes up most in package code, where a constraint has to accept any instantiation. `any` in a value position is still a smell.

## Generics

Name a type parameter when the name adds information. Don't prefix for its own sake.

```ts
type ValueOf<T> = T[keyof T];              // ✅ one universal param, T is clearest
type Registry<K, TManager> = /* ... */;    // ✅ K is obvious, TManager isn't
type ValueOf<TObject> = /* ... */;         // ❌ says nothing T didn't
```

`K` and `V` are fine where the role is conventional. Reach for a descriptive `TSomething` when the parameter stands for a domain concept a letter can't convey.

## Return types

**Let TypeScript infer.** An annotation that restates what inference already produces is a second source of truth that can drift.

Annotate when:

- the return type is a **discriminated union** — inference tends to collapse or widen the cases;
- **inference gets it wrong** or produces something unusable;
- it's **library code**, where an explicit signature is part of the contract and worth being in the reader's face;
- **`isolatedDeclarations` is enabled**, which requires it.

`isolatedDeclarations` is worth weighing rather than defaulting on: it forces explicit annotations on exported values, which fights the `as const` + `ValueOf` enum pattern above — the whole point there is that the type is derived from the value.

## Iteration

**`for...of` over `.forEach`.** `await`, `break`, `continue`, and `return` all work in a loop and none work in a callback, so the loop never has to be rewritten when the body grows.

```ts
// ✅
for (const user of users) {
 await sync(user);
 if (user.isArchived) continue;
}

// ❌ can't await, can't break; return only exits the callback
users.forEach(async (user) => {
 /* ... */
});
```

- Indexed `for (let i = 0; ...)` only when the index is actually used.
- `Object.entries()` for objects.
- `.map` and `.filter` on their own are fine — they're expressions returning values.

**`flatMap` over a `filter`+`map` chain.** Return the value for a match, `[]` to skip:

```ts
// ✅
const names = users.flatMap((user) => (user.isActive ? user.name : []));

// ❌
const names = users.filter((user) => user.isActive).map((user) => user.name);
```

Return the bare value, not `[user.name]` — `flatMap` appends non-array returns directly, so wrapping just allocates a throwaway array. The exception is when the mapped value is itself an array (`user.tags`), which would get flattened a level; wrap that one.

A `flatMap` body can be as complex as it needs to be and is still preferable to chaining:

```ts
const names = users.flatMap((user) => {
 if (user.isActive) return user.name;
 if (user.otherThing) return user.fullName;

 return [];
});
```

## Control flow

**Prefer early returns over nesting.** Handle the exits first and let the main path sit unindented at the end.

```ts
// ✅
function process(user: User) {
 if (!user.isActive) return null;
 if (!user.hasAccess) return null;

 return buildProfile(user);
}

// ❌
function process(user: User) {
 if (user.isActive) {
  if (user.hasAccess) {
   return buildProfile(user);
  }
 }

 return null;
}
```

This applies anywhere a branch can exit — guard clauses in functions, `continue` in loops, and early `return` in a `flatMap` body.

## Exports

**Named exports only.** The exception is where a framework requires a default — Next.js pages and layouts, config files, and similar tool-owned files.

```jsonc
// eslint
"import/no-default-export": "error"   // with an override for framework paths
```

## readonly

Apply `readonly` where it prevents a real bug, not as blanket documentation:

- **Array and tuple parameters** get `readonly T[]`. A callee mutating a caller's array is a live bug and the annotation costs one word.
- `as const` already gives deep readonly on literals, mappers, and object-enums.
- **Skip props and nested object types.** `Readonly<T>` is shallow, so deep immutability isn't something the type system supports cheaply — the annotations become noise that gets dropped inconsistently.

`eslint-plugin-functional`'s `prefer-immutable-types` can enforce this broadly if the tradeoff ever changes.

## Required settings

Assume `strict: true`. Only what it doesn't already cover is listed here.

```jsonc
// tsconfig.json
{
 "compilerOptions": {
  "strict": true,
  "verbatimModuleSyntax": true,
  "noUncheckedIndexedAccess": true,
  "noImplicitOverride": true,
  "noFallthroughCasesInSwitch": true,
 },
}
```

`verbatimModuleSyntax` makes type-only imports a compiler error rather than a convention (TS1484) and keeps import statements intact in the emitted output.

`noUncheckedIndexedAccess` types `arr[0]` as `T | undefined`. It's the flag that gives the no-cast rule teeth, since the usual escape hatch is `arr[0]!` — a non-null assertion is a cast wearing different punctuation. Narrow it instead:

```ts
const first = users[0];
if (!first) return;
// first is User here
```

`exactOptionalPropertyTypes` is **not required, but not discouraged either** — a per-package choice. It distinguishes an absent property from one explicitly set to `undefined`, which pays off well in packages where that difference carries meaning: patch and partial-update APIs, anything serializing to JSON, config merging. In packages without that distinction it mostly generates churn. Enable it where it earns its keep; don't add it uniformly and don't strip it where someone already has.

```jsonc
// eslint
"@typescript-eslint/consistent-type-imports": ["error", { "fixStyle": "separate-type-imports" }]
```

Type imports are top-level statements, kept separate from value imports:

```ts
import type { User } from "./types";
import { getUser } from "./services/get-user";
```

This mirrors `export type * from './types'` on the export side — type and value movement stay visually distinct in both directions.
