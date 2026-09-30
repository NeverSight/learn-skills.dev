---
name: fix-ts-errors
description: Fix TypeScript errors and loop the type-check until green. Use when the user says "ts errors" or "fix types", when a change "still isn't working" in a TS context, after editing any TypeScript file, and when another skill needs the type-check loop (/done, /parallel-review, /fix-pr-review).
---

# Fix TypeScript errors

I fix the types at their source and loop the workspace check until it exits 0. I do not work around them.

## Workflow

### Step 1: Identify Target Files

- If the user specifies files, I use those.
- If the user says "changed files", I run `git diff --name-only HEAD` for staged plus unstaged `.ts` and `.tsx` files, plus `git ls-files --others --exclude-standard` for untracked ones.
- If it is unclear, I ask which files.

### Step 2: Go red

I run the workspace type-check, `pnpm type-check` or `turbo type-check`, or `bunx tsc --noEmit` for a plain TS project. That output is the loop ground truth.

I use IDE diagnostics, the LSP tool or `mcp__ide__getDiagnostics`, only to localize an error the check already reported. IDE diagnostics are per-file and unreliable across workspace package boundaries, so they narrow. They never decide.

### Step 3: Fix Errors

For each error I find, I read the file around the error location, understand the root cause, then fix at the source with a proper type-safe pattern.

I fix in this order. Missing imports get the import added. Type mismatches get the declaration corrected at its source. Missing properties get aligned with the source type definition. Null or undefined gets narrowed with a type guard or an early return. Generic type issues get explicit type parameters.

Every error exits through a real type. I add the missing import, narrow the union, widen the signature at its source, or derive it from the schema with `z.infer`. An `as` survives only with a comment naming the third-party gap.

### Step 4: Re-verify

I re-run the same workspace check. Green means it exits 0.

A file whose squiggles cleared is not green. A type change breaks its importers, so I chase the cascade to the workspace edge before I report. When new errors appeared, I go back to Step 3.

### Step 5: Escape-Hatch Audit

Once green, I grep the changed lines for all four escape hatches, `as` assertions excluding `as const`, `@ts-ignore`, `@ts-expect-error`, and non-null assertions.

```bash
git diff -U0 HEAD -- '*.ts' '*.tsx' | grep '^+' | grep -E '\bas\b|@ts-ignore|@ts-expect-error|[]A-Za-z0-9_$)][!]([^=]|$)|["'\''"`][!]([^=]|$)' | sed 's/as const/__AS_CONST__/g'
git ls-files --others --exclude-standard -- '*.ts' '*.tsx' | tr '\n' '\0' | xargs -0 grep -nE '\bas\b|@ts-ignore|@ts-expect-error|[]A-Za-z0-9_$)][!]([^=]|$)|["'\''"`][!]([^=]|$)' | sed 's/as const/__AS_CONST__/g'
```

The `[!]` groups match a postfix assertion: a value character, closing quote, bracket, or paren before the bang and no equals after it, so `value!`, `value!.x`, `value![0]`, `value!()`, `"value"!`, and backtick-quoted receivers all hit while `!=`, `!==`, and prefix negation like `!ready` stay out. The trailing `sed` neutralizes only the `as const` idiom into a marker instead of dropping whole lines, so co-occurring hatches on the same line survive. A line whose only match is the `__AS_CONST__` marker needs no action.

I skip import aliases like `import { x as y }`. For every remaining hit I attempt removal with proper typing, meaning inference, narrowing, type guards, generics, or schema-derived types with `z.infer`. I re-run the check after each removal, and when errors appear I go back to Step 3. A hatch survives only when genuinely unavoidable, for example a third-party library type gap, and it must carry a one-line comment citing the upstream issue or type gap.

### Step 6: Report

Once green, I briefly report how many errors I found, what I fixed, and the surviving escape hatches, `as` casts, `@ts-ignore`, `@ts-expect-error`, and non-null assertions, with the count of each and a one-line justification per survivor. My target is 0.

## Loop breaker

When errors persist after 3 fix-verify cycles, I stop and explain the root cause, show the remaining errors, suggest whether the issue sits in the file itself or in a dependency, and ask the user how to proceed.

## Important rules

- I fix a wrong type in a shared workspace package in that package. I report it and stop.
- I check whether the error sits in generated code or authored code. When a codegen step is stale, I suggest the command and do not run it.
