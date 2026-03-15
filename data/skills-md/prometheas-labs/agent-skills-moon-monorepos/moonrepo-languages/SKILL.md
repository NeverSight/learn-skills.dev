---
name: moonrepo-languages
description: "Use when adding a new Moon project by language, creating language-specific tasks, or configuring toolchains for PHP, JavaScript/TypeScript, Python, or mobile apps"
---

# Moon v2 — Language Patterns

Concise per-language Moon v2 patterns for common project types.

## PHP

```yaml
layer: application
language: php

fileGroups:
  sources: ['src/**/*.php', '!src/vendor/**']
  configs: ['composer.json', 'composer.lock']

tasks:
  install:
    command: 'composer install --no-interaction'
    inputs: ['@group(configs)']
    outputs: ['vendor/']
    options: { cache: true }

  lint:
    script: 'find src -name "*.php" -not -path "*/vendor/*" -exec php -l {} \;'
    inputs: ['@group(sources)']
```

**Key patterns:** Use `--working-dir` for nested structures (e.g., app lives in `src/htdocs/`). Cache `vendor/` directory. Composer commands run via `command:` (single executable), but lint with `find | exec` needs `script:`.

## JavaScript / TypeScript

```yaml
layer: application
language: typescript

fileGroups:
  sources: ['src/**/*.{ts,tsx}', '!src/**/*.test.*']
  configs: ['package.json', 'tsconfig.json']

tasks:
  build:
    script: 'rm -rf dist && tsc --build'
    inputs: ['@group(sources)', '@group(configs)']
    outputs: ['dist/']

  dev:
    command: 'next dev'
    preset: server    # disables cache, enables persistent
```

**Key patterns:** Set `javascript.packageManager` in `.moon/toolchains.yml` (bun, npm, pnpm, yarn). Use `preset: server` for dev servers. Next.js outputs go in `.next/`. React libraries output to `dist/`. Node.js services typically don't need `outputs`.

## Python

```yaml
layer: application
language: python

fileGroups:
  sources: ['src/**/*.py', '!**/__pycache__/**']
  configs: ['pyproject.toml', 'requirements*.txt']

tasks:
  install:
    command: 'pip install -r requirements.txt'
    inputs: ['@group(configs)']
    outputs: ['.venv/']

  test:
    command: 'pytest'
    inputs: ['@group(sources)', '@group(configs)']
    deps: ['~:install']
    options: { cache: true }

  lint:
    command: 'ruff check src/'
    inputs: ['@group(sources)']
```

**Key patterns:** Python toolchain is experimental (`unstable_python` in toolchains.yml). Support pip, Poetry (`poetry install`), Pipenv, PDM, or uv. Cache `.venv/` or build outputs. Use `deps: ['~:install']` to ensure venv is ready.

## Mobile (React Native / Flutter)

**React Native** — uses JavaScript toolchain:

```yaml
layer: application
language: typescript
tasks:
  ios:
    command: 'react-native run-ios'
    preset: server
  android:
    command: 'react-native run-android'
    preset: server
  pod-install:
    script: 'cd ios && pod install'
    inputs: ['ios/Podfile', 'ios/Podfile.lock']
    outputs: ['ios/Pods/']
```

**Flutter** — uses system toolchain:

```yaml
layer: application
language: dart
tasks:
  build-ios:
    command: 'flutter build ios --release'
    inputs: ['lib/**/*.dart', 'pubspec.yaml']
    outputs: ['build/ios/']
  build-android:
    command: 'flutter build appbundle --release'
    inputs: ['lib/**/*.dart', 'pubspec.yaml']
    outputs: ['build/app/']
```

**Key patterns:** Platform builds (iOS/Android) are separate tasks. CocoaPods and Gradle outputs are cacheable. Use `preset: server` for dev/emulator tasks. Simulator/emulator launch tasks should not be cached.
