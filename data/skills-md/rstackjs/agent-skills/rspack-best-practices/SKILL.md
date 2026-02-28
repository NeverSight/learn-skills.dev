---
name: rspack-best-practices
description: Rspack best practices for config, CLI workflow, type checking, CSS, bundle optimization, assets and profiling. Use when writing, reviewing, or troubleshooting Rspack projects.
---

# Rspack Best Practices

Apply these rules when writing or reviewing Rspack projects.

## Configuration

- Use `rspack.config.ts` and `defineConfig`
- Define explicit `entry` values for multi-page applications
- Keep one main config and branch by `process.env.NODE_ENV` only when needed
- Keep rule conditions narrow and explicit (`test`, `include`, `exclude`, `resourceQuery`)
- Prefer built-in Rspack plugins/loaders over community JS alternatives when equivalent features exist

## CLI

If `@rspack/cli` is installed:

- Use `rspack dev` for local development
- Use `rspack build` for production build
- Use `rspack preview` only for local production preview

## Type checking

- Use `ts-checker-rspack-plugin` for integrated dev/build type checks
- Or run `tsc --noEmit`/`vue-tsc --noEmit` as an explicit script step

## CSS

Choose one strategy:

- Built-in CSS (`type: 'css' | 'css/auto' | 'css/module'`) for modern setups
- `css-loader` + `CssExtractRspackPlugin` for webpack migration compatibility
- `style-loader` for pure style-in-JS runtime injection scenarios

Optional:

- Use `builtin:lightningcss-loader` when goals are syntax downgrade + vendor prefixing
- Use `sass-loader`/`less-loader` for preprocessing Sass/Less files
- Use `@tailwindcss/webpack` for Tailwind CSS integration

## Bundle size optimization

- Prefer dynamic `import()` for non-critical code paths
- Prefer lightweight libraries where possible
- Keep `target` aligned with real compatibility requirements

## Asset management

- Import source-managed assets from project source directories, not from `public`
- Reference `public` files by absolute URL path
- Prefer asset modules (`asset`, `asset/resource`, `asset/inline`, `asset/source`) over legacy `file-loader`/`url-loader`/`raw-loader`

## Profiling

- Use Node CPU profiling (`--cpu-prof`) when JavaScript-side overhead is suspected
- Use `RSPACK_PROFILE=OVERVIEW` and analyze trace output for compiler-phase bottlenecks
- Replace known slow stacks first (`babel-loader`, PostCSS, terser) with Rspack built-ins when feasible

## Security

- Do not publish `.map` files to public servers/CDNs when production source maps are enabled

## Documentation

- For the latest (v2) docs, read http://rspack.rs/llms.txt
- For Rspack v1 docs, read http://v1.rspack.rs/llms.txt
