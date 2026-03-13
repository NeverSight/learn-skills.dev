---
name: typescript
description: Best practices and guidelines for TypeScript (2025-2026 Edition), focusing on TS 5.x+, modern type safety, and performance.
---

# TypeScript Skill (2025-2026 Edition)

This skill outlines the latest best practices for writing robust, performant, and type-safe TypeScript code, aligned with the 2025-2026 ecosystem (TypeScript 5.x and beyond).

## 🚀 Key Trends & Features (2025/2026)

*   **Native Speed:** The transition to a Go-based compiler (native port) is underway (TS 7+), promising massive performance gains.
*   **Default Strictness:** Modern projects treat `strict: true` as the absolute baseline.
*   **Framework First:** TS is now deeply integrated into frameworks (Next.js, Remix, NestJS) rather than an add-on.

## 🛠️ Configuration Best Practices (`tsconfig.json`)

Use strict defaults to prevent bugs before they happen.

```json
{
  "compilerOptions": {
    /* Type Safety */
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "noUncheckedIndexedAccess": true, /* 2025 Essential: Prevents accessing undefined array indices */
    "exactOptionalPropertyTypes": true, /* Stricter optional property checks */

    /* Modules & Emit */
    "module": "NodeNext", /* or "ESNext" for pure frontend */
    "moduleResolution": "NodeNext", /* Aligns with modern Node.js ESM */
    "target": "ES2022", /* Modern runtimes support recent ES features */
    "skipLibCheck": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "verbatimModuleSyntax": true, /* Enforces strict import/export syntax (TS 5.0+) */
    
    /* Developer Experience */
    "allowSyntheticDefaultImports": true
  }
}
```

## 🧩 Type Safety & Patterns

### 1. `unknown` over `any`
**Never** use `any` unless absolutely necessary (e.g., migrating legacy code). Use `unknown` and narrow the type safely.

```typescript
// ❌ Bad
function processData(input: any) {
  input.doSomething(); // Runtime crash risk
}

// ✅ Good
function processData(input: unknown) {
  if (typeof input === 'string') {
    console.log(input.toUpperCase()); // Safe
  } else if (isCustomType(input)) {
    input.doSomething(); // Safe via type guard
  }
}
```

### 2. `satisfies` Operator (TS 4.9+)
Use `satisfies` to validate a value matches a type *without* widening the type (preserving inference).

```typescript
type Config = Record<string, string | number>;

const myConfig = {
  port: 8080,
  host: "localhost"
} satisfies Config;

// ✅ TS knows 'port' is a number directly, no casting needed.
myConfig.port.toFixed(2); 
```

### 3. Immutable Data by Default
Use `readonly` to prevent accidental mutations, especially for function arguments and React props.

```typescript
interface User {
  readonly id: string;
  readonly name: string;
  tags: readonly string[]; // Immutable array
}

function printTags(tags: readonly string[]) {
  // tags.push("new"); // ❌ Error: Property 'push' does not exist on type 'readonly string[]'
}
```

### 4. Template Literal Types
Create precise string types for better autocompletion and safety.

```typescript
type EventName = "click" | "hover";
type HandlerName = `on${Capitalize<EventName>}`; // "onClick" | "onHover"
```

## ⚡ Performance Optimization

*   **Type Imports:** Use `import type { ... }` or `import { type ... }` explicitly. Enabling `verbatimModuleSyntax` enforces this, ensuring zero JS overhead for type-only imports using modern bundlers.
*   **Lazy Loading:** Leverage `await import(...)` for splitting code in large applications.

## ⚠️ Common Pitfalls to Avoid

*   **Excessive Type Assertions (`as`):** Use type guards or `zod` for validation instead of forcing types with `as`.
*   **Broad Types:** Avoid `Function` or `object`. Use `() => void` or `Record<string, unknown>` instead.
*   **Enum Misuse:** Prefer **union types of strings** (`type Status = 'open' | 'closed'`) over standard TS `enum`s to keep runtime code cleaner and avoid nominal typing surprises.

## 📚 References

*   [TypeScript 5.x Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html)
*   [Total TypeScript (Matt Pocock)](https://www.totaltypescript.com/)
*   [Zod (Schema Validation)](https://zod.dev/)
