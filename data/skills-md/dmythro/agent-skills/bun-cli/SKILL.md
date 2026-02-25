---
name: bun-cli
description: Bun CLI reference for package management, script running, testing, bundling, and compilation. Use when working with bun install, bun add, bun run, bun test, bun build, bunx, bunfig.toml, bun.lock, or replacing npm/npx/node commands.
---

# Bun CLI

Bun is an all-in-one JavaScript/TypeScript runtime, package manager, bundler, and test runner. Bun runs TypeScript natively — `bun file.ts` directly, no compile step, no `tsc`, no `ts-node`. Always use `bun` instead of `node`, `npm`, `npx`, `yarn`, or `pnpm` in Bun projects.

## Detecting Bun Projects

A project uses Bun if any of these are present:
- `bun.lock` or `bun.lockb` in the project root
- `bunfig.toml` in the project root
- `bun` field in `package.json` (e.g., `"bun": { "install": { ... } }`)
- Package manager field: `"packageManager": "bun@..."`
- `[run] bun = true` in `bunfig.toml` (forces Bun runtime for all scripts)

## Critical Rule

**In a Bun project, ALWAYS use `bun` for everything.** Never fall back to `node`, `npm`, `npx`, `yarn`, or `pnpm`. This avoids compatibility issues, unnecessary retries, and cryptic errors from Node.js/npm not understanding Bun-specific features (workspace protocol, lockfile format, trustedDependencies, etc.).

- Run files: `bun file.ts` (not `node file.ts`)
- Run scripts: `bun run dev` (not `npm run dev`)
- Execute binaries: `bunx tool` (not `npx tool`)
- Install packages: `bun add pkg` (not `npm install pkg`)
- Run tests: `bun test` (not `npx jest` or `node --test`)

## Read-Only Commands (safe, no side effects)

| Command | Purpose |
|---------|---------|
| `bun --version` | Runtime version |
| `bun info <pkg>` | Package metadata, available versions |
| `bun info <pkg> versions` | List all published versions |
| `bun pm ls` | List installed packages |
| `bun pm ls --all` | List all (including transitive) |
| `bun pm hash` | Print lockfile hash |
| `bun pm cache` | Show cache directory |
| `bun outdated` | Check for outdated dependencies |
| `bun audit` | Security vulnerability audit |
| `bun test` | Run test suite |
| `bun run lint` | Run linter (project-specific) |
| `bun run check-types` | Type checking (project-specific) |

> **Reference**: See `references/allowlist.md` for copy-paste `Bash(command:*)` patterns for Claude Code / OpenCode settings.

## npm/npx/node to Bun Translation

| npm/npx/node | Bun equivalent |
|---|---|
| `npm install` | `bun install` |
| `npm install pkg` | `bun add pkg` |
| `npm install -D pkg` | `bun add -d pkg` |
| `npm install -g pkg` | `bun add -g pkg` |
| `npm uninstall pkg` | `bun remove pkg` |
| `npm update` | `bun update` |
| `npm run script` | `bun run script` |
| `npx command` | `bunx command` |
| `node file.js` | `bun file.js` |
| `node --watch file.js` | `bun --watch file.js` |
| `npm test` | `bun test` |
| `npm pack` | `bun pm pack` |
| `npm publish` | `bun publish` |
| `npm info pkg` | `bun info pkg` |
| `npm outdated` | `bun outdated` |
| `npm audit` | `bun audit` |
| `npm link` | `bun link` |

### Key Behavioral Differences

- **No `npm run` prefix needed**: `bun run dev` works, but so does `bun dev` (direct script execution)
- **`--bun` flag**: Forces Bun runtime instead of Node.js for scripts that use `node` in their shebang. In `bunfig.toml`, set `[run] bun = true` to make this the default
- **Lockfile**: Bun uses `bun.lock` (text-based, v1.2+) or `bun.lockb` (binary, legacy). Text lockfile is default for new projects
- **Workspace commands**: Use `--filter` flag: `bun --filter 'pkg-name' add dep`
- **Lifecycle scripts**: Bun ignores lifecycle scripts by default for security. Use `trustedDependencies` in package.json to allowlist packages that need postinstall etc.

## Package Management

### Installing Dependencies

```bash
bun install                    # Install all from package.json
bun install --frozen-lockfile  # CI mode: fail if lockfile needs update
bun install --no-save          # Install without updating package.json
bun install --production       # Skip devDependencies
bun install --dry-run          # Show what would be installed
```

### Adding/Removing Packages

```bash
bun add pkg                    # Add to dependencies
bun add pkg@version            # Add specific version
bun add -d pkg                 # Add to devDependencies (--dev)
bun add -D pkg                 # Same as -d
bun add --optional pkg         # Add to optionalDependencies
bun add -g pkg                 # Install globally
bun add --exact pkg            # Pin exact version (no ^)
bun remove pkg                 # Remove package
```

### Updating and Inspecting

```bash
bun update                     # Update all packages
bun update pkg                 # Update specific package
bun outdated                   # Show outdated packages
bun info pkg                   # Show package metadata
bun info pkg versions          # List all available versions
bun pm ls                      # List installed packages
bun pm ls --all                # List all (including transitive)
bun pm hash                    # Print lockfile hash
bun pm cache                   # Show cache directory
bun pm cache rm                # Clear cache
```

### Linking and Patching

```bash
bun link                       # Register current package as linkable
bun link pkg-name              # Link a registered package
bun pm pack                    # Create tarball of package
bun patch pkg                  # Start patching a package
bun patch --commit pkg-dir     # Apply patch
```

### Publishing

```bash
bun publish                    # Publish to npm
bun publish --dry-run          # Preview what would be published
bun publish --tag beta         # Publish with tag
bun publish --access public    # Set access level
```

> **Reference**: See `references/package-management.md` for complete flag details.

## Running Scripts and Files

### Direct Execution

```bash
bun file.ts                    # Run TypeScript/JavaScript directly
bun run script-name            # Run package.json script
bun script-name                # Short form (if no conflict with bun commands)
bun --watch file.ts            # Re-run on file changes
bun --hot file.ts              # Hot reload (preserves state)
bun --env-file .env file.ts    # Load env file
bun --env-file .env.local --env-file .env file.ts  # Multiple env files
```

### bunx (npx Replacement)

```bash
bunx command                   # Run package binary (auto-installs if needed)
bunx --bun command             # Force Bun runtime for the command
bunx command@version           # Run specific version
```

### Workspace-Aware Execution

```bash
bun --filter 'pkg-name' run script    # Run in specific workspace
bun --filter '*' run script           # Run in all workspaces
bun --filter './apps/*' run build     # Run with glob pattern
```

### Script Flags

```bash
bun run --smol file.ts         # Reduce memory usage (sacrifice throughput)
bun run --silent script        # Suppress script name echo
bun run --shell=bun script     # Use Bun's built-in shell (cross-platform, default on Windows)
bun run --shell=system script  # Use system shell (default on macOS/Linux)
```

> **Reference**: See `references/running-and-execution.md` for complete details.

## Testing

Bun includes a built-in test runner compatible with Jest-like syntax.

### Running Tests

```bash
bun test                          # Run all test files
bun test file.test.ts             # Run specific file
bun test --filter "pattern"       # Filter by test name
bun test --timeout 10000         # Set timeout (ms)
bun test --bail                   # Stop on first failure
bun test --bail 5                 # Stop after 5 failures
bun test --rerun-each 3           # Run each test 3 times
bun test --only                   # Run only tests marked with .only
bun test --todo                   # Include .todo tests
```

### Coverage

```bash
bun test --coverage               # Enable code coverage
bun test --coverage-reporter text # Coverage format: text, lcov, json
bun test --coverage-dir ./cov     # Output directory
```

### Test File Patterns

By default, Bun finds files matching: `*.test.{ts,tsx,js,jsx}`, `*_test.{ts,tsx,js,jsx}`, `*.spec.{ts,tsx,js,jsx}`, `*_spec.{ts,tsx,js,jsx}`, and files in `__tests__/` directories.

### Snapshot Testing

```bash
bun test --update-snapshots       # Update snapshot files
```

### Watch Mode

```bash
bun test --watch                  # Re-run on file changes
```

> **Reference**: See `references/testing.md` for test API, mocking, lifecycle hooks, and coverage config.

## Bundling and Compilation

### Bundling

```bash
bun build ./src/index.ts --outdir ./dist           # Bundle to directory
bun build ./src/index.ts --outfile ./dist/out.js    # Bundle to single file
bun build ./src/index.ts --target browser           # Target: browser (default), bun, node
bun build ./src/index.ts --format esm               # Format: esm (default), cjs, iife
bun build ./src/index.ts --minify                   # Minify output
bun build ./src/index.ts --sourcemap external        # Sourcemaps: external, inline, linked, none
bun build ./src/index.ts --splitting                # Code splitting (ESM only)
```

### Standalone Executables

```bash
bun build ./src/cli.ts --compile                    # Create self-contained executable
bun build ./src/cli.ts --compile --target bun-linux-x64    # Cross-compile
bun build ./src/cli.ts --compile --minify           # Minified executable
```

Available compilation targets: `bun-linux-x64`, `bun-linux-arm64`, `bun-darwin-x64`, `bun-darwin-arm64`, `bun-windows-x64`.

### Build Options

```bash
bun build ... --external pkg        # Exclude from bundle
bun build ... --define 'KEY=VALUE'  # Define compile-time constants
bun build ... --loader .ext=type    # Custom loaders (js, jsx, ts, tsx, json, css, text, file, base64, dataurl, binary)
bun build ... --entry-naming [dir]/[name].[ext]   # Output naming pattern
bun build ... --public-path /cdn/   # Public path prefix for assets
```

> **Reference**: See `references/bundling-and-compilation.md` for complete options.

## Project Initialization

```bash
bun init                       # Initialize new project (creates package.json, tsconfig.json, index.ts)
bun create template-name       # Create from template
bun create next-app my-app     # Example: create Next.js app
```

## Configuration (bunfig.toml)

Key sections:

```toml
[run]
bun = true                     # Always use Bun runtime (not Node)

[install]
exact = true                   # Pin exact versions by default
peer = false                   # Don't auto-install peer deps
production = false             # Include devDeps
frozenLockfile = false         # Don't fail on lockfile mismatch
globalDir = "~/.bun/install/global"  # Global install location

[install.scopes]
"@myorg" = { token = "$NPM_TOKEN", url = "https://npm.pkg.github.com/" }

[test]
coverage = false               # Enable coverage by default
coverageReporter = ["text", "lcov"]
timeout = 5000                 # Default test timeout

[bundle]
entryPoints = ["./src/index.ts"]
outdir = "./dist"
```

> **Reference**: See `references/configuration.md` for complete bunfig.toml reference.

## Debugging and Profiling

```bash
bun --inspect file.ts              # Start debugger (WebSocket, connect via Chrome DevTools)
bun --inspect-wait file.ts         # Wait for debugger to attach before executing
bun --inspect-brk file.ts         # Break on first line
bun --cpu-prof file.ts             # Generate CPU profile
bun --heap-prof file.ts            # Generate heap profile
BUN_JSC_logJITCodeForPerf=1 bun file.ts  # Linux perf integration
```

## Environment Variables

```bash
bun --env-file .env file.ts        # Load .env file
bun --env-file .env.local --env-file .env file.ts  # Load multiple (left takes precedence)
```

Bun auto-loads `.env`, `.env.production`, `.env.local`, `.env.production.local` by default based on `NODE_ENV`.

## Built-in Features That Replace External Tools

Bun has many capabilities built in that eliminate the need for external packages or tooling:

### Native TypeScript
Bun runs `.ts`, `.tsx` files directly — no `tsc`, `ts-node`, or `tsx` needed. The transpiler is built into the runtime. Use `bun file.ts` to run any TypeScript file immediately.

### Workspace Catalogs
Bun supports `catalog:` protocol in `package.json` for centralized dependency version management across monorepo workspaces — no need for tools like `syncpack` or `manypkg`:

```json
// Root package.json
{
  "workspaces": ["packages/*"],
  "catalog": {
    "react": "^19.0.0",
    "typescript": "^5.7.0"
  }
}

// packages/app/package.json
{
  "dependencies": {
    "react": "catalog:"
  }
}
```

### Built-in Test Runner
`bun test` is a full Jest-compatible test runner with snapshot testing, mocking, coverage — no need for `jest`, `vitest`, or `mocha`.

### Built-in Bundler
`bun build` replaces `esbuild`, `webpack`, `rollup` for many use cases. Supports code splitting, tree shaking, minification, and standalone executable compilation.

### Built-in SQLite
`import { Database } from 'bun:sqlite'` — zero-dependency SQLite3 with prepared statements and transactions. No need for `better-sqlite3` or `sql.js`.

### Built-in Shell
`Bun.$` tagged template — cross-platform shell execution with automatic escaping. Replaces `execa`, `shelljs`, `zx`.

### Built-in File I/O
`Bun.file()` and `Bun.write()` — fast file operations without importing `fs`. Auto-detects MIME types.

### Built-in Glob
`new Bun.Glob(pattern)` — fast glob matching and file scanning. Replaces `glob`, `fast-glob`, `minimatch`.

### Built-in Password Hashing
`Bun.password.hash()` and `.verify()` with bcrypt and argon2id. Replaces `bcrypt`, `argon2` packages.

### Built-in Compression
`Bun.gzipSync()`, `Bun.deflateSync()`, `Bun.zstdCompressSync()` — no need for `zlib` wrapper packages.

### Built-in Semver
`Bun.semver.satisfies()`, `.order()` — replaces `semver` package.

## Key Gotchas

1. **Always use `bun` not `npm`/`node`/`npx`** in Bun projects
2. **Lockfile format**: `bun.lock` (text, v1.2+) is the default for new projects. Legacy `bun.lockb` is binary. Don't mix with `package-lock.json`
3. **trustedDependencies**: Lifecycle scripts (postinstall, etc.) only run for packages listed in `trustedDependencies` in package.json
4. **`--bun` flag**: Some tools (e.g., Next.js) use Node.js by default even when run with `bun run`. Use `--bun` or `[run] bun = true` in `bunfig.toml` to force Bun runtime
5. **Workspace protocol**: Use `"workspace:*"` in package.json to reference workspace packages
6. **Global binaries**: Installed with `bun add -g`, located in `~/.bun/bin/`
7. **Node.js compatibility**: Bun implements most Node.js APIs but some edge cases differ. Check https://bun.sh/docs/runtime/nodejs-apis for compatibility
8. **TypeScript**: Bun runs TypeScript natively with no compilation step. Uses its own transpiler (not tsc)
9. **Auto-install**: Bun can auto-install missing packages on import (disabled by default, enable with `[install] auto = true` in bunfig.toml)
10. **`bun run` vs `bun`**: `bun run script` runs a package.json script; `bun file.ts` runs a file directly. `bun script` tries script first, then falls back to file
