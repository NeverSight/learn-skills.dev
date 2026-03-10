---
name: optimize-docker-build-cache
description: >
  Optimize Docker build times using layer caching, multi-stage builds,
  BuildKit features, and dependency-first copy patterns. Applicable to R,
  Node.js, and Python projects. Use when Docker builds are slow due to
  repeated package installations, when rebuilds reinstall all dependencies
  on every code change, when image sizes are unnecessarily large, or when
  CI/CD pipeline builds are a bottleneck.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: containerization
  complexity: intermediate
  language: Docker
  tags: docker, cache, optimization, multi-stage, buildkit
---

# Optimize Docker Build Cache

Reduce Docker build times through effective layer caching and build optimization.

## When to Use

- Docker builds are slow due to repeated package installations
- Rebuilds reinstall all dependencies on every code change
- Image sizes are unnecessarily large
- CI/CD pipeline builds are a bottleneck

## Inputs

- **Required**: Existing Dockerfile to optimize
- **Optional**: Target build time improvement
- **Optional**: Target image size reduction

## Procedure

### Step 1: Order Layers by Change Frequency

Place least-changing layers first:

```dockerfile
# 1. Base image (rarely changes)
FROM rocker/r-ver:4.5.0

# 2. System dependencies (change occasionally)
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Dependency files only (change when deps change)
COPY renv.lock renv.lock
COPY renv/activate.R renv/activate.R
RUN R -e "renv::restore()"

# 4. Source code (changes frequently)
COPY . .
```

**Key principle**: Docker caches each layer. When a layer changes, all subsequent layers are rebuilt. Dependency installation should come before source code copy.

**Expected:** The Dockerfile layers are ordered from least-changing (base image, system deps) to most-changing (source code), with dependency lockfiles copied before the full source.

**On failure:** If builds still reinstall dependencies on every code change, verify that `COPY . .` comes after the dependency installation `RUN` command, not before.

### Step 2: Separate Dependency Installation from Code

**Bad** (rebuilds packages on every code change):

```dockerfile
COPY . .
RUN R -e "renv::restore()"
```

**Good** (only rebuilds packages when lockfile changes):

```dockerfile
COPY renv.lock renv.lock
RUN R -e "renv::restore()"
COPY . .
```

Same pattern for Node.js:

```dockerfile
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

**Expected:** Dependency lockfile (`renv.lock`, `package-lock.json`, `requirements.txt`) is copied and installed in a separate layer before the full source code `COPY . .`.

**On failure:** If the lockfile copy fails, ensure the file exists in the build context and is not excluded by `.dockerignore`.

### Step 3: Use Multi-Stage Builds

Separate build dependencies from runtime:

```dockerfile
# Build stage - includes dev tools
FROM rocker/r-ver:4.5.0 AS builder
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev libssl-dev build-essential
COPY renv.lock .
RUN R -e "install.packages('renv'); renv::restore()"

# Runtime stage - minimal image
FROM rocker/r-ver:4.5.0
RUN apt-get update && apt-get install -y \
    libcurl4 libssl3 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/R/site-library /usr/local/lib/R/site-library
COPY . /app
WORKDIR /app
CMD ["Rscript", "main.R"]
```

**Expected:** The Dockerfile has a builder stage with dev tools and a runtime stage with only production dependencies. The final image is significantly smaller than a single-stage build.

**On failure:** If `COPY --from=builder` fails to find libraries, verify the install path matches between stages. Use `docker build --target builder .` to debug the build stage independently.

### Step 4: Combine RUN Commands

Each `RUN` creates a layer. Combine related commands:

**Bad** (3 layers, apt cache persists):

```dockerfile
RUN apt-get update
RUN apt-get install -y curl git
RUN rm -rf /var/lib/apt/lists/*
```

**Good** (1 layer, clean cache):

```dockerfile
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
```

**Expected:** Related `apt-get` or package install commands are combined into single `RUN` instructions, each ending with cache cleanup (`rm -rf /var/lib/apt/lists/*`).

**On failure:** If a combined `RUN` command fails midway, temporarily split it to identify the failing command, then recombine after fixing.

### Step 5: Use .dockerignore

Prevent unnecessary files from entering the build context:

```
.git
.Rproj.user
.Rhistory
.RData
renv/library
renv/cache
node_modules
docs/
*.tar.gz
.env
```

**Expected:** A `.dockerignore` file exists in the project root excluding `.git`, `node_modules`, `renv/library`, build artifacts, and environment files. Build context size is noticeably smaller.

**On failure:** If needed files are missing in the container, check `.dockerignore` for overly broad patterns. Use `docker build` verbose output to verify which files are sent to the daemon.

### Step 6: Enable BuildKit

```bash
DOCKER_BUILDKIT=1 docker build -t myimage .
```

Or in `docker-compose.yml`:

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
```

With `COMPOSE_DOCKER_CLI_BUILD=1` and `DOCKER_BUILDKIT=1` environment variables.

BuildKit enables:
- Parallel stage builds
- Better cache management
- `--mount=type=cache` for persistent package caches

**Expected:** Builds run with BuildKit enabled (indicated by `#1 [internal] load build definition` style output). Multi-stage builds execute stages in parallel where possible.

**On failure:** If BuildKit is not active, verify the environment variables are exported before the build command. On older Docker versions, upgrade Docker Engine to 18.09+ for BuildKit support.

### Step 7: Use Cache Mounts for Package Managers

```dockerfile
# R packages with persistent cache
RUN --mount=type=cache,target=/usr/local/lib/R/site-library \
    R -e "install.packages('dplyr')"

# npm with persistent cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

**Expected:** Subsequent builds reuse cached packages from the mount, dramatically reducing install times even when the layer is invalidated. Cache persists across builds.

**On failure:** If `--mount=type=cache` is not recognized, ensure BuildKit is enabled (`DOCKER_BUILDKIT=1`). The syntax requires BuildKit and is not supported by the legacy builder.

## Validation

- [ ] Rebuilds after code-only changes are significantly faster
- [ ] Dependency installation layer is cached when lockfile hasn't changed
- [ ] `.dockerignore` excludes unnecessary files
- [ ] Image size is reduced compared to unoptimized build
- [ ] Multi-stage build (if used) separates build and runtime dependencies

## Common Pitfalls

- **Copying all files before installing deps**: Invalidates the dependency cache on every code change
- **Forgetting `.dockerignore`**: Large build contexts slow down every build
- **Too many layers**: Each `RUN`, `COPY`, `ADD` creates a layer. Combine where logical.
- **Not cleaning apt cache**: Always end apt-get installs with `&& rm -rf /var/lib/apt/lists/*`
- **Platform-specific caches**: Cache layers are platform-specific. CI runners may not benefit from local caches.

## Related Skills

- `create-r-dockerfile` - initial Dockerfile creation
- `setup-docker-compose` - compose build configuration
- `containerize-mcp-server` - apply optimizations to MCP server builds
