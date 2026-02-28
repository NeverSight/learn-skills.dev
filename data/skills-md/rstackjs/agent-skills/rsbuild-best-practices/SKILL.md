---
name: rsbuild-best-practices
description: Rsbuild best practices for config, CLI workflow, type checking, bundle optimization, assets, and debugging. Use when writing, reviewing, or troubleshooting Rsbuild projects.
---

# Rsbuild Best Practices

Apply these rules when writing or reviewing Rsbuild projects.

## Configuration

- Use `rsbuild.config.ts` and `defineConfig`
- Use `tools.rspack` or `tools.bundlerChain` only when no first-class Rsbuild option exists
- Define explicit `source.entry` values for multi-page applications
- In TypeScript projects, prefer `tsconfig.json` path aliases first

## CLI

- Use `rsbuild dev` for local development
- Use `rsbuild build` for production build
- Use `rsbuild preview` only for local production preview
- Use `rsbuild inspect` to inspect final Rsbuild/Rspack configs

## Type checking

- Use `@rsbuild/plugin-type-check` for integrated dev/build type checks
- Or run `tsc --noEmit`/`vue-tsc --noEmit` as an explicit script step

## Bundle size optimization

- Prefer dynamic `import()` for non-critical code paths
- Prefer lightweight libraries where possible
- Keep browserslist aligned with real compatibility requirements

## Asset management

- Import source-managed assets from project source directories, not from `public`
- Reference `public` files by absolute URL path

## Security

- Do not publish `.map` files to public servers/CDNs when production source maps are enabled

## Debugging

- Run with `DEBUG=rsbuild` when diagnosing config resolution or plugin behavior
- Read generated files in `dist/.rsbuild` to confirm final config, not assumed config

## Profiling

- Use Node CPU profiling (`--cpu-prof`) when JavaScript-side overhead is suspected
- Use `RSPACK_PROFILE=OVERVIEW` and analyze trace output for compiler-phase bottlenecks

## Documentation

- For the latest (v2) docs, read http://rsbuild.rs/llms.txt
- For Rsbuild v1 docs, read http://v1.rsbuild.rs/llms.txt
