---
name: aube-package-manager
description: Expert guidance for using aube, a fast Rust-based Node.js package manager compatible with pnpm, npm, yarn, and bun lockfiles.
triggers:
  - use aube to install packages
  - aube package manager
  - fast node.js package manager
  - replace pnpm with aube
  - aube install dependencies
  - aube workspace setup
  - aube ci install
  - aube run scripts
---

# Aube Package Manager

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Aube is a fast Node.js package manager written in Rust. It drops into existing projects by reading and writing existing lockfiles (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lock`), uses a global content-addressable store to reduce disk usage, and delivers dramatically faster installs than pnpm or Bun — especially on warm CI.

## Installation

### Via mise (recommended)

```sh
# Install globally
mise use -g aube

# Pin to a project
mise use aube

# Verify
aube --version
```

### Via npm

```sh
npm install -g @endevco/aube
```

### Via Homebrew (beta tap)

```sh
brew install endevco/tap/aube
```

## Core Concepts

- **Lockfile compatibility**: Reads and writes existing lockfiles in place — no forced migration.
- **Global store**: Package files live in `~/.local/share/aube/store/` (XDG) and are shared across projects.
- **Isolated layout**: Packages link through `node_modules/.aube/` — phantom dependencies are blocked.
- **Secure defaults**: New package releases wait a minimum age; lifecycle scripts require explicit approval.

## Key Commands

### Install & Dependency Management

```sh
aube install                    # Install all dependencies
aube install -r                 # Install across all workspace packages
aube install --prod             # Production dependencies only
aube install --lockfile-only    # Update lockfile without touching node_modules

aube add react                  # Add a runtime dependency
aube add -D vitest              # Add a dev dependency
aube add zod --filter @acme/api # Add to a specific workspace package
aube remove react               # Remove a dependency
aube update                     # Update deps within package.json ranges
```

### CI

```sh
aube ci    # Clean install: removes node_modules, verifies lockfile is fresh, installs
```

Use `aube ci` in CI pipelines where the lockfile must be the source of truth.

### Running Scripts and Binaries

```sh
aube run build          # Run a package.json script
aube run test           # Run test script (auto-installs if deps are stale)
aube test               # Shortcut: same as `aube run test`
aube dev                # Any script name works directly as a subcommand
aube build
aube lint

aube exec vitest        # Run a local binary from node_modules/.bin
aube dlx cowsay hi      # Run a package in a throwaway environment (like npx)
```

### Multicall Shims

```sh
aubr build        # Equivalent to: aube run build
aubx cowsay hi    # Equivalent to: aube dlx cowsay hi
```

### Inspection & Maintenance

```sh
aube list                   # List installed packages
aube why react              # Explain why a package is installed
aube outdated               # Show outdated dependencies
aube audit                  # Security audit
aube store path             # Show global store location
aube store prune            # Remove unused packages from global store
aube config get registry    # Read config values
```

### Publishing

```sh
aube pack       # Pack a package tarball
aube publish    # Publish to registry
aube link       # Link a local package
aube unlink     # Unlink a local package
```

## Lockfile Compatibility

| File | Reads | Writes in place |
|---|---|---|
| `aube-lock.yaml` | ✅ | ✅ |
| `pnpm-lock.yaml` v9 | ✅ | ✅ |
| `package-lock.json` v2/v3 | ✅ | ✅ |
| `npm-shrinkwrap.json` | ✅ | ✅ |
| `yarn.lock` (v1 classic + v2+ berry) | ✅ | ✅ |
| `bun.lock` | ✅ | ✅ |

**Not supported:**
- pnpm v5/v6 lockfiles (upgrade with pnpm first)
- Yarn PnP projects (switch to `node_modules` linker first)

## Workspaces

```sh
# Install across all workspace packages
aube install -r

# Run a script in all workspace packages
aube run test -r

# Add a dependency to a specific package
aube add zod --filter @acme/api
aube add -D typescript --filter @acme/shared
```

Workspace config files:
- `pnpm-workspace.yaml` — read and written if present
- `aube-workspace.yaml` — used for aube-first projects

Example `aube-workspace.yaml`:

```yaml
packages:
  - "packages/*"
  - "apps/*"
```

## Dependency Lifecycle Scripts

Aube skips lifecycle scripts by default for security.

```sh
# See which packages had scripts skipped
aube ignored-builds

# Approve specific packages to run their build scripts
aube approve-builds
```

After approval, the allowed packages are recorded in your project config so teammates get the same behavior.

## Configuration

Aube reads config from `package.json` under `"aube"` key or from `.auberc` / `aube.config.yaml`.

```json
{
  "name": "my-app",
  "aube": {
    "registry": "https://registry.npmjs.org/",
    "store-dir": "/custom/store/path"
  }
}
```

```sh
# Read a config value
aube config get registry

# Set a config value
aube config set registry https://my-private-registry.example.com
```

## CI/CD Patterns

### GitHub Actions

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install mise
        uses: jdx/mise-action@v2

      - name: Install aube
        run: mise use -g aube

      - name: Cache aube store
        uses: actions/cache@v4
        with:
          path: ~/.local/share/aube/store
          key: aube-store-${{ hashFiles('**/pnpm-lock.yaml', '**/aube-lock.yaml') }}
          restore-keys: |
            aube-store-

      - name: Install dependencies
        run: aube ci

      - name: Run tests
        run: aube test
```

### Docker

```dockerfile
FROM node:22-slim

# Install aube via npm
RUN npm install -g @endevco/aube

WORKDIR /app

# Copy lockfile and package.json first for layer caching
COPY package.json pnpm-lock.yaml ./

# Frozen install — fail if lockfile would change
RUN aube ci

COPY . .

RUN aube run build

CMD ["node", "dist/index.js"]
```

### Lockfile-only update (for Docker layer caching)

```sh
# Only update the lockfile, don't install into node_modules
aube install --lockfile-only
```

## Migrating from pnpm

```sh
# 1. Install aube
mise use -g aube

# 2. Run in your existing project — aube reads pnpm-lock.yaml
cd my-project
aube install

# 3. Approve any build scripts that pnpm was running
aube approve-builds

# 4. Replace pnpm scripts in package.json (optional)
# Before: "scripts": { "postinstall": "pnpm run build:native" }
# After:  keep as-is, aube runs package.json scripts the same way
```

## Migrating from npm/yarn

```sh
# npm — aube reads package-lock.json
cd my-npm-project
aube install

# yarn classic — aube reads yarn.lock
cd my-yarn-project
aube install

# Bun — aube reads bun.lock
cd my-bun-project
aube install
```

## Common Patterns

### Monorepo with filtered commands

```sh
# Build only the API package
aube run build --filter @acme/api

# Run tests in all packages that changed
aube run test --filter '...[origin/main]'

# Install and run in one step (auto-install if stale)
aube exec vitest --run
```

### Global store management

```sh
# Find where the store lives
aube store path
# → ~/.local/share/aube/store

# Clean up packages no longer used by any project
aube store prune
```

### Checking why a package is installed

```sh
aube why lodash
# Shows the dependency chain that requires lodash
```

## Troubleshooting

### `aube ci` fails with lockfile mismatch

The lockfile is out of sync with `package.json`. Fix locally:

```sh
aube install          # updates lockfile
git add pnpm-lock.yaml
git commit -m "chore: update lockfile"
```

### Build scripts not running

Aube skips lifecycle scripts by default. Check what was skipped:

```sh
aube ignored-builds
aube approve-builds   # interactively approve packages
```

### Package phantom dependency errors

Aube uses an isolated layout — packages can only import their declared dependencies. Fix by adding the missing dependency explicitly:

```sh
aube add <missing-package>
```

### Slow first install / cold cache

The first install populates the global store. Subsequent installs (same or other projects with shared deps) will be significantly faster. Cache `~/.local/share/aube/store` in CI for warm-cache performance.

### pnpm v5/v6 lockfile not supported

```sh
# Upgrade lockfile with pnpm first
pnpm install  # regenerates as v9 format
# Then switch to aube
aube install
```

### Yarn PnP projects

Aube writes `node_modules`, not `.pnp.cjs`. Switch the Yarn linker first:

```sh
# In .yarnrc.yml
nodeLinker: node-modules
yarn install   # regenerates yarn.lock for node-modules layout
aube install   # now aube can take over
```

## Links

- [Documentation](https://aube.en.dev)
- [Benchmarks](https://aube.en.dev/benchmarks)
- [Lockfile compatibility](https://aube.en.dev/package-manager/lockfiles)
- [Scripts and binaries](https://aube.en.dev/package-manager/scripts)
- [Configuration reference](https://aube.en.dev/package-manager/configuration)
- [Installation methods](https://aube.en.dev/installation)
