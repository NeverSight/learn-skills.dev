---
name: xcodegen-cli
description: Use XcodeGen CLI to create, update, inspect, and troubleshoot Xcode projects from YAML or JSON specs. Trigger this skill when users ask to run `xcodegen generate`, `xcodegen dump`, or `xcodegen cache`; to author or fix `project.yml`; to split specs with `include`; or to diagnose parsing, validation, and path-related generation failures.
---

# XcodeGen CLI

## Overview

Use this skill to drive XcodeGen workflows end-to-end: prepare or edit specs, run the right command, inspect resolved configuration, and fix generation issues quickly.

## Follow This Workflow

1. Identify command context.
   - Run `xcodegen ...` if CLI is installed.
   - Run `swift run xcodegen ...` when working inside the XcodeGen source repository.
2. Resolve the spec path.
   - Default to `project.yml` in current directory.
   - Use `--spec` for custom paths or comma-separated multiple specs.
   - Use `--project-root` when include/source paths should resolve from another directory.
3. Inspect before changing behavior.
   - Run `xcodegen dump --type summary` for a quick structural view.
   - Run `xcodegen dump --type yaml --file /tmp/resolved.yml` to inspect merged/expanded output.
4. Generate or cache.
   - Run `xcodegen generate` for normal generation.
   - Run `xcodegen generate --use-cache` in repetitive local or CI workflows.
   - Run `xcodegen cache` when cache artifacts are needed without generation.
5. Troubleshoot with direct feedback.
   - Treat parser errors as spec syntax/schema issues.
   - Treat validation errors as semantic project-model issues.
   - Treat missing file errors as path, include, or working-directory issues.

## Command Guidance

- Use `generate` to produce `.xcodeproj` from spec files.
- Use `generate --only-plists` when only plist output is needed.
- Use `dump` to inspect effective configuration in `yaml`, `json`, `parsed-yaml`, `parsed-json`, `summary`, or `swift-dump` form.
- Use `cache` to precompute/write cache files.
- Add `--quiet` only when caller asks for reduced output.
- Add `--no-env` to debug `${ENV_VAR}` expansion issues.

## Spec Editing Guidance

- Keep root shape explicit: `name`, `targets`, and optional `include`, `options`, `settings`, `schemes`, `packages`.
- Use `include` to split large specs and share reusable fragments.
- Use `:REPLACE` suffix in keys when replacement is required instead of merge behavior.
- Set `options.minimumXcodeGenVersion` when relying on newer behavior.
- Prefer incremental edits and validate after each edit with `dump` or `generate`.

## Validation Loop

1. Update spec.
2. Run `xcodegen dump --type summary`.
3. Run `xcodegen generate --use-cache`.
4. If generation fails, inspect resolved YAML using `dump --type yaml` and fix one issue at a time.

## Quick Template

```yaml
name: MyApp
options:
  bundleIdPrefix: com.example
targets:
  MyApp:
    type: application
    platform: iOS
    deploymentTarget: "16.0"
    sources: [MyApp]
```

## Resources

Read `references/api_reference.md` for complete command flags, troubleshooting mappings, and links to the canonical docs in this repository.
