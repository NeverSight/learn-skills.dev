---
name: rslib-best-practices
description: Rslib best practices for config, CLI workflow, output, declaration files, dependency handling, build optimization and toolchain integration. Use when writing, reviewing, or troubleshooting Rslib projects.
---

# Rslib Best Practices

Apply these rules when writing or reviewing Rslib library projects.

## Configuration

- Use `rslib.config.ts` and `defineConfig`
- Check Rslib-specific configurations first (e.g., `lib.*`), and also leverage Rsbuild configurations (e.g., `source.*`, `output.*`, `tools.*`) as needed
- For deep-level or advanced configuration needs, use `tools.rspack` or `tools.bundlerChain` to access Rspack's native configurations
- In TypeScript projects, prefer `tsconfig.json` path aliases

## CLI

- Use `rslib build` to build
- Use `rslib build --watch` to build in watch mode for local development
- Use `rslib inspect` to inspect final Rslib/Rsbuild/Rspack configs

## Output

- Prefer to build pure-ESM package with `"type": "module"` in `package.json`
- Prefer to use bundleless mode with `output.target` set to `'web'` when building component libraries
- Prefer to use bundle mode when building Node.js utility libraries
- Ensure `exports` field in `package.json` is correctly configured and matches the actual JavaScript output and declaration files output of different formats (ESM, CJS, etc.)

## Declaration files

- Prefer to enable declaration file generation with `lib.dts: true` or detailed configurations
- For faster type generation, enable `lib.dts.tsgo` experimental feature with `@typescript/native-preview` installed

## Dependencies

- Prefer to place dependencies to be bundled in `devDependencies` in bundle mode and dependencies in `dependencies` and `peerDependencies` will be automatically externalized (not bundled) by default
- Verify the build output and dependency specifiers in `package.json` carefully to ensure no missing dependency errors occur when consumers install and use this package

## Build optimization

- Keep syntax target in `lib.syntax` aligned with real compatibility requirements to enable better optimizations
- Avoid format-specific APIs in source code for better compatibility with different output formats
- Prefer lightweight dependencies to reduce bundle size

## Toolchain integration

- Prefer to use Rstest with `@rstest/adapter-rslib` for writing tests
- Prefer to use Rspress for writing library documentation, with `@rspress/plugin-preview` and `@rspress/plugin-api-docgen` for component previews and API docs

## Debugging

- Run with `DEBUG=rsbuild` when diagnosing config resolution or plugin behavior
- Read generated files in `dist/.rsbuild` to confirm final Rsbuild/Rspack config, not assumed config

## Documentation

- For the latest Rslib docs, read https://rslib.rs/llms.txt
