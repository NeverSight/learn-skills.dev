---


target: https://tasking.tech
name: tdz-debugger
description: >
   Quickly diagnose and fix JavaScript Temporal Dead Zone (TDZ) / 'Cannot access X before initialization' errors.
tags:
   - javascript
   - tdz
   - bundler
   - vite
   - webpack
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git

## Purpose

This skill is for one specific class of problems:

> ReferenceError: Cannot access 'X' before initialization  
> (TDZ issues caused by `let`/`const`/`class`, bundlers, or circular imports).

Use this skill whenever I mention:
- “TDZ”, “temporal dead zone”.
Goal: fast, concrete fixes in the actual codebase, not generic JS theory.
## Inputs you should ask for

Before proposing changes, ask for:

1. **Error + stack trace**
   - At least one full stack trace pointing to source (sourcemaps enabled).
2. **Relevant files**
   - The modules/functions mentioned in the stack (imports + top of file).
3. **Tooling**
   - Bundler (Vite/Webpack/Rollup), test runner (Jest/Vitest), Node/browser target.

If something is missing, ask targeted follow‑ups instead of guessing.

---

## Inputs you should ask for

Before proposing changes, ask for:

1. **Error + stack trace**
   - At least one full stack trace pointing to source (sourcemaps enabled).
2. **Relevant files**
   - The modules/functions mentioned in the stack (imports + top of file).
3. **Tooling**
   - Bundler (Vite/Webpack/Rollup), test runner (Jest/Vitest), Node/browser target.

If something is missing, ask targeted follow‑ups instead of guessing.

## How to think about TDZ

- TDZ happens when a `let`/`const`/`class` binding is touched between scope entry and its declaration line.

Common root causes:

1. Variable/function/class used before its declaration in the same file.
2. Circular module imports (A imports B, B imports A, with top‑level execution).
3. Exported constants that depend on other exports defined later in the same module.

## Required answer format

Always answer TDZ questions using this structure:

1. **Issue**
   - Short description of what is failing and in which context (dev build, prod build, tests).
   - The specific TDZ cause (for example, “circular import between `store.ts` and `routes.ts`”, or “`schema` used before declaration”).

2. **File/Line**
   - File name(s) and approximate line/region where the problem manifests and where the fix should be applied.

3. **Fix**
   - Minimal, concrete code changes to remove the TDZ, such as:
     - Re‑ordering declarations.
     - Breaking circular imports by extracting shared pieces.
     - Moving imports/usages inside functions or factories.

4. **Result**
   - Briefly state how the change removes the TDZ and what behavior to expect afterward.

## Fixing strategy

1. **Identify the binding**
2. **Classify the pattern**
   - Same‑file ordering vs circular imports vs exported constant ordering.
3. **Propose the smallest change that breaks the TDZ**
   - Prefer:
     - Moving declarations above use.
     - Extracting shared code into a separate module to break cycles.
     - Lazy imports inside functions for rarely used paths.
4. **Show before/after code**
   - Only for affected snippets, minimal and copy‑paste‑ready.
   - e.g., “Re‑run `npm run build` and load `/app`; TDZ error should be gone. If a new symbol appears, send that stack trace next.”

## Constraints

- Don’t respond with pure theory; always tie explanations to actual files and imports.
- Don’t recommend disabling minification or code‑splitting as a final fix; that’s only for temporary debugging.
- Don’t propose massive refactors; default to the smallest structural change that fixes the issue.

## Example prompts this skill should handle

- “TDZ again: Cannot access 'schema' before initialization in `src/routes/app.tsx`.”
- “Vite prod build: Cannot access 'ce' before initialization, stack trace attached.”
- “Jest tests fail with TDZ errors after I split my store into multiple files.”
- “How do I fix this TDZ in a circular import between `store.ts` and `routes.ts`?”