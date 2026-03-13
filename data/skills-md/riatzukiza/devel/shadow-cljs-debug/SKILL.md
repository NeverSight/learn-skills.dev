---
name: shadow-cljs-debug
description: "Protocol to debug and fix shadow-cljs compilation errors."
---

# Skill: Shadow-CLJS Debug

## Goal
To systematically identify and fix compilation errors, dependency issues, and configuration problems in `shadow-cljs` projects.

## Use This Skill When
- `shadow-cljs compile` fails.
- The build hangs or loops indefinitely.
- You see "Undeclared Var", "No such namespace", or "Analysis Error".
- You suspect a dependency is missing.

## Do Not Use This Skill When
- The error is clearly a syntax error (use `clojure-syntax-rescue`).

## Steps
1. **Analyze Error**:
   - Read the error message fully. Is it a compilation error or a dependency error?
   - **Undeclared Var**: You forgot to `(:require [namespace :as alias])` or are using a function that doesn't exist.
   - **No such namespace**: The file path does not match the namespace declaration, or the package is not installed.
2. **Check Config**:
   - Read `shadow-cljs.edn`. Is the build ID correct? Are source paths included?
   - Read `deps.edn` (if used). Is the dependency listed?
   - Read `package.json`. Is the npm package installed?
3. **Clean State**:
   - If behavior is weird or inconsistent, delete the cache: `rm -rf .shadow-cljs .cpcache`.
   - Restart the watch process.
4. **Verify Interop**:
   - **npm**: Ensure you use `(:require ["package-name" :as pkg])` for npm packages.
   - **Globals**: Use `js/window` or `js/console` for globals, do not require them.
5. **Fix & Retry**:
   - Apply the fix.
   - Run `npx shadow-cljs compile <build-id>` (or `release` for production).

## Output
- A successful compilation (exit code 0).

## Strong Hints
- **Constraint**: Never edit the output files (for example `public/js/main.js`). Only edit `.cljs` source.
- **Tip**: Shadow-CLJS relies heavily on `package.json` for JS deps. If an npm import fails, check `node_modules` first (`workspace-dependency-check`).
- **Tip**: `(:require [foo.bar :as bar])` requires a file at `src/foo/bar.cljs`. Check file paths match namespaces exactly.

## Suggested Next Skills
Check the [Skill Graph](../skill_graph.json) for the full workflow.

- **[clojure-syntax-rescue](../clojure-syntax-rescue/SKILL.md)**
- **[workspace-dependency-check](../workspace-dependency-check/SKILL.md)**
