---
name: just
description: Use just for command running and task automation. Prefer Justfiles over Makefiles. Keep recipes simple - delegate complex logic to scripts rather than embedding in recipes.
---

# just - Command Runner

**IMPORTANT**: `just` is the **PREFERRED** command runner for project task automation. Use Justfiles instead of Makefiles for new projects and task automation.

## Core Philosophy

- **Justfiles over Makefiles**: Prefer just for task automation unless working with existing Make-based projects
- **Simple recipes**: Keep recipe definitions concise and readable
- **Delegate to scripts**: For complex logic, call external scripts rather than embedding in recipes
- **Just as orchestrator**: Use just to coordinate and invoke scripts, not to contain business logic

## Basic Usage Patterns

### Running Recipes

```bash
# List available recipes
just --list
just -l

# Run a recipe
just build
just test

# Run recipe with arguments
just deploy production
just run-test integration

# Run recipe from different directory
just --working-directory /path/to/project build

# Choose a different Justfile
just --justfile custom.just build
```

### Recipe Definition Basics

```just
# Simple recipe
build:
    cargo build --release

# Recipe with description (shown in --list)
# Run all tests
test:
    cargo test --quiet

# Recipe with dependencies (runs setup first)
deploy: build test
    ./scripts/deploy.sh

# Recipe with parameters
run-test test_name:
    cargo test {{test_name}}

# Recipe with default parameter value
serve port="8080":
    python -m http.server {{port}}

# Recipe with multiple parameters
deploy env branch="main":
    ./scripts/deploy.sh {{env}} {{branch}}
```

### Delegation Pattern (PREFERRED)

**Good - Delegates to script:**
```just
# Build the project
build:
    ./scripts/build.sh

# Run integration tests
test-integration:
    ./scripts/test-integration.sh

# Deploy to environment
deploy env:
    ./scripts/deploy.sh {{env}}
```

**Avoid - Complex logic in recipe:**
```just
# ❌ Too complex - should be in a script
deploy env:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ "{{env}}" = "production" ]; then
        echo "Deploying to production..."
        git fetch origin
        git checkout main
        git pull
        docker build -t app:latest .
        docker push registry.example.com/app:latest
        kubectl apply -f k8s/production/
        kubectl rollout status deployment/app
    else
        echo "Deploying to staging..."
        # ... many more lines ...
    fi
```

**Better - Simple orchestration:**
```just
# Deploy to production
deploy-prod:
    ./scripts/deploy.sh production

# Deploy to staging
deploy-staging:
    ./scripts/deploy.sh staging

# Generic deploy with validation
deploy env:
    ./scripts/validate-env.sh {{env}}
    ./scripts/deploy.sh {{env}}
```

## Recipe Features

### Dependencies

```just
# Recipe runs after its dependencies
all: clean build test deploy

# Dependencies run in order specified
deploy: build test package
    ./scripts/deploy.sh

# Multiple dependency chains
full-deploy: lint build test docker-build docker-push k8s-deploy
```

### Variables

```just
# Set variables at top of file
version := "1.2.3"
registry := "registry.example.com"
image := registry + "/app:" + version

# Use in recipes
docker-build:
    docker build -t {{image}} .

docker-push:
    docker push {{image}}

# Environment variables
deploy:
    API_KEY=$API_KEY ./scripts/deploy.sh
```

### Conditional Execution

```just
# Use shell conditionals in scripts
test:
    ./scripts/test.sh

# Or delegate to script
check-and-test:
    ./scripts/check-and-test.sh
```

### Private Recipes

```just
# Private recipe (not shown in --list, can't be run directly)
_setup:
    ./scripts/setup-env.sh

# Public recipe uses private recipe
deploy: _setup
    ./scripts/deploy.sh
```

### Recipe Attributes

```just
# Ignore errors (continue even if fails)
[ignore-errors]
lint:
    ./scripts/lint.sh

# Run in specific directory
[working-directory: 'frontend']
build-ui:
    npm run build

# Confirm before running
[confirm]
deploy-prod:
    ./scripts/deploy.sh production

# Don't print recipe before running
[no-quiet]
status:
    ./scripts/status.sh
```

## Common Patterns

### Development Workflow

```just
# Default recipe (runs when you type 'just')
default: check test

# Quick validation
check:
    ./scripts/check.sh

# Run all tests
test:
    ./scripts/test.sh

# Full CI workflow
ci: check test lint build
```

### Build Automation

```just
# Clean build artifacts
clean:
    ./scripts/clean.sh

# Build project
build:
    ./scripts/build.sh

# Full rebuild
rebuild: clean build

# Build with caching
build-cached:
    ./scripts/build.sh --cache
```

### Multi-Environment Deployment

```just
# Development environment
dev:
    ./scripts/run-dev.sh

# Staging deployment
deploy-staging:
    ./scripts/deploy.sh staging

# Production deployment (with confirmation)
[confirm]
deploy-prod:
    ./scripts/deploy.sh production

# Deploy to any environment
deploy env:
    ./scripts/validate-env.sh {{env}}
    ./scripts/deploy.sh {{env}}
```

### Docker Workflows

```just
# Build Docker image
docker-build:
    ./scripts/docker-build.sh

# Run container locally
docker-run:
    ./scripts/docker-run.sh

# Push to registry
docker-push: docker-build
    ./scripts/docker-push.sh

# Complete Docker workflow
docker: docker-build docker-push
```

### Database Operations

```just
# Run migrations
migrate:
    ./scripts/db-migrate.sh

# Rollback migration
migrate-rollback:
    ./scripts/db-rollback.sh

# Seed database
seed:
    ./scripts/db-seed.sh

# Reset database (dev only)
[confirm]
db-reset:
    ./scripts/db-reset.sh
```

## Script Organization

### Recommended Structure

```
project/
├── justfile
├── scripts/
│   ├── build.sh
│   ├── test.sh
│   ├── deploy.sh
│   ├── validate-env.sh
│   └── utils/
│       ├── common.sh
│       └── logging.sh
└── src/
    └── ...
```

### Script Best Practices

**Make scripts executable:**
```bash
chmod +x scripts/*.sh
```

**Use shebang in scripts:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Script logic here
```

**Keep scripts focused:**
```bash
# Good - single purpose
# scripts/build.sh
#!/usr/bin/env bash
set -euo pipefail

echo "Building project..."
cargo build --release
```

**Source common utilities:**
```bash
# scripts/deploy.sh
#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/utils/common.sh"
source "$(dirname "$0")/utils/logging.sh"

log_info "Starting deployment..."
# Deployment logic
```

## Advanced Features

### Command Evaluation

```just
# Backticks execute shell commands
commit := `git rev-parse --short HEAD`
timestamp := `date +%Y%m%d-%H%M%S`

# Use in recipes
tag:
    echo "Tagging {{commit}} at {{timestamp}}"
```

### Multi-line Constructs

```just
# Multi-line variables
help := '''
  Available commands:
    build  - Build the project
    test   - Run tests
    deploy - Deploy to production
'''

# Print help
help:
    @echo {{help}}
```

### Settings

```just
# Change shell (default is sh)
set shell := ["bash", "-c"]

# Make all recipes silent (@echo becomes echo)
set quiet := true

# Use PowerShell on Windows
set windows-shell := ["powershell.exe", "-c"]

# Use Python for recipes
set shell := ["python3", "-c"]
```

### Imports

```just
# Import recipes from other files
import 'ci.just'
import 'deploy.just'

# Use imported recipes
all: ci-check deploy-staging
```

## Integration with Other Tools

### With Cargo (Rust)

```just
# Rust development workflow
check:
    cargo check --quiet

test:
    cargo test --quiet

clippy:
    cargo clippy

build: check test clippy
    cargo build --release

# Or delegate to script
rust-workflow:
    ./scripts/rust-workflow.sh
```

### With npm/pnpm/yarn

```just
# Install dependencies
install:
    pnpm install

# Run dev server
dev:
    pnpm run dev

# Build frontend
build:
    pnpm run build

# Or use scripts
ui-build:
    ./scripts/build-ui.sh
```

### With Docker

```just
# Docker operations via scripts
docker-build:
    ./scripts/docker/build.sh

docker-run:
    ./scripts/docker/run.sh

docker-compose-up:
    docker-compose up -d
```

### With Git

```just
# Git workflow helpers
sync:
    git fetch origin
    git pull

push: test
    git push origin main

release version:
    ./scripts/release.sh {{version}}
```

## Complete Workflow Examples

### Workflow 1: Web Application

```just
# Default - run dev server
default: dev

# Install dependencies
install:
    ./scripts/install.sh

# Development server
dev:
    ./scripts/dev.sh

# Run tests
test:
    ./scripts/test.sh

# Build for production
build:
    ./scripts/build.sh

# Deploy to staging
deploy-staging: test build
    ./scripts/deploy.sh staging

# Deploy to production
[confirm]
deploy-prod: test build
    ./scripts/deploy.sh production
```

### Workflow 2: Rust Project

```just
# Default - check code
default: check

# Fast check
check:
    cargo check --quiet

# Run tests
test:
    cargo test --quiet

# Lint code
lint:
    cargo clippy

# Full validation
ci: test lint
    ./scripts/verify-formatting.sh

# Build release
build:
    cargo build --release

# Install binary
install: build
    cargo install --path .
```

### Workflow 3: Monorepo

```just
# Build all services
build-all:
    ./scripts/build-all.sh

# Test all services
test-all:
    ./scripts/test-all.sh

# Build specific service
build-service service:
    ./scripts/build-service.sh {{service}}

# Deploy specific service
deploy service env:
    ./scripts/deploy-service.sh {{service}} {{env}}

# Full deployment
deploy-all env: test-all build-all
    ./scripts/deploy-all.sh {{env}}
```

## Common Commands Quick Reference

```bash
# List recipes
just --list

# Run recipe
just <recipe>

# Run with arguments
just <recipe> arg1 arg2

# Set variable
just var=value recipe

# Choose Justfile
just --justfile path/to/justfile recipe

# Work in different directory
just --working-directory /path recipe

# Dry run (show what would run)
just --dry-run recipe

# Verbose output
just --verbose recipe

# Choose recipe interactively
just --choose
```

## Best Practices Summary

1. **Keep recipes simple**: 1-3 lines max; delegate complex logic to scripts
2. **Use descriptive names**: `deploy-prod` not `dp`, `test-integration` not `ti`
3. **Add comments**: Describe what each recipe does
4. **Organize scripts**: Keep scripts in `scripts/` directory with logical subdirectories
5. **Make scripts executable**: Use `chmod +x scripts/*.sh`
6. **Use dependencies**: Chain recipes with dependencies rather than duplicating commands
7. **Confirm destructive operations**: Use `[confirm]` for deployments, database resets, etc.
8. **Private recipes for setup**: Use `_recipe` naming for internal setup steps
9. **Default recipe**: Provide sensible default (usually `dev` or `check`)
10. **Document in comments**: Add comments explaining complex workflows

## When to Use Scripts vs. Recipes

### Use Recipe Directly:
- Single command execution
- Simple chaining (3 commands or less)
- Setting environment variables for a command
- Quick aliases

### Use Script (PREFERRED for most cases):
- Complex conditional logic
- Multiple steps with error handling
- Reusable logic across recipes
- Long command sequences (>3 commands)
- Anything requiring significant bash scripting

## Justfile Template

```just
# Set shell for all recipes
set shell := ["bash", "-c"]

# Variables
version := "1.0.0"

# Default recipe
default: check

# List all recipes
help:
    @just --list

# Development
dev:
    ./scripts/dev.sh

# Testing
test:
    ./scripts/test.sh

# Build
build:
    ./scripts/build.sh

# Full CI check
ci: test build
    ./scripts/verify.sh

# Deploy to staging
deploy-staging: ci
    ./scripts/deploy.sh staging

# Deploy to production
[confirm]
deploy-prod: ci
    ./scripts/deploy.sh production

# Clean build artifacts
clean:
    ./scripts/clean.sh
```

## Migration from Make

### Key Differences from Make

1. **Not a build system**: just is for running commands, not tracking file dependencies
2. **Recipes always run**: Unlike Make targets, recipes run every time (no file timestamp checking)
3. **Simpler syntax**: No need for `.PHONY`, tabs vs. spaces issues, etc.
4. **Better error messages**: Clear, helpful error output

### Converting Makefile to Justfile

**Makefile:**
```make
.PHONY: build test deploy

build:
	cargo build --release

test:
	cargo test

deploy: build test
	./deploy.sh
```

**Justfile:**
```just
build:
    cargo build --release

test:
    cargo test

deploy: build test
    ./scripts/deploy.sh
```

## Resources

- Official documentation: https://just.systems
- GitHub repository: https://github.com/casey/just
- Installation: `brew install just` (macOS) or `cargo install just`
