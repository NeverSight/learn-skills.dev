---
name: migrate-to-rsbuild
description: Migrate webpack, Vite, create-react-app (CRA/CRACO), or Vue CLI projects to Rsbuild.
---

# Migrate to Rsbuild

## Goal

Migrate webpack, Vite, create-react-app (CRA/CRACO), or Vue CLI projects to Rsbuild with minimal behavior changes and clear verification.

## Supported source frameworks

- webpack
- Vite
- CRA / CRACO
- Vue CLI

## Migration principles (must follow)

1. **Official guide first**: treat Rsbuild migration docs as source of truth.
2. **Smallest-change-first**: complete baseline migration first, then migrate custom behavior.
3. **Do not change business logic**: avoid touching app runtime code unless user explicitly asks.
4. **Validate before cleanup**: keep old tool dependencies/config temporarily if needed; remove only after Rsbuild is green.

## Workflow

1. **Detect source framework**
   - Check `package.json` dependencies/scripts and config files:
     - webpack: `webpack.config.*`
     - Vite: `vite.config.*`
     - CRA/CRACO: `react-scripts`, `@craco/craco`, `craco.config.*`
     - Vue CLI: `@vue/cli-service`, `vue.config.*`

2. **Apply framework-specific deltas**
   - webpack: `references/webpack.md`
   - Vite: `references/vite.md`
   - CRA/CRACO: `references/cra.md`
   - Vue CLI: `references/vue-cli.md`

3. **Validate behavior**
   - Run dev server to verify the project starts without errors.
   - Run build command to verify the project builds successfully.
   - If issues remain, compare the old project configuration with the migration guide and complete any missing mappings.

4. **Cleanup and summarize**
   - Remove obsolete dependencies/config only after validation passes.
   - Summarize changed files and any remaining manual follow-ups.
