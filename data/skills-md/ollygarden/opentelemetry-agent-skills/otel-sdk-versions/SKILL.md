---
name: otel-sdk-versions
description: OpenTelemetry SDK and package version lookup across languages. Use when choosing the latest compatible released OpenTelemetry SDK or package version and locating setup docs or examples.
---

# OpenTelemetry SDK Versions

Use this skill when you need the latest released OpenTelemetry SDK or package version for a language.

## Workflow

1. Open `references/generated/otel-version-index.md`.
- identify the row for the project language and package
- use the bundled table as the default source of truth for supported languages in this repository

2. Choose the version deliberately.
- prefer the latest released version when it is compatible with the project
- if the latest release is not compatible, choose the latest compatible version and state the compatibility reason explicitly
- reuse that decision for the rest of the task unless the language, package, or constraints change

3. Resolve companion packages from the release source.
- the index covers one primary SDK package per language
- if the task requires additional packages from the same ecosystem (exporters, instrumentations, resource detectors), look up their versions from the release source — do not infer or reuse the primary package version
- sub-packages within the same project often share a version line but not always; confirm each package individually

4. Use the linked follow-up sources when needed.
- use the Release Source column to confirm the package or repo
- use the Setup Docs column for SDK setup guidance
- use the Examples column for implementation references when examples are available

5. Handle gaps explicitly.
- if the requested language or package is not in the bundled index, say that the index does not cover that exact package
- then fall back to the official release source and official docs for that package
- do not assume an unreleased, prerelease, or incompatible version is acceptable without saying so
