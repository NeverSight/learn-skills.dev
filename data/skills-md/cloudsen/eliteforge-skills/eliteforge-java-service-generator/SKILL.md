---
name: eliteforge-java-service-generator
description: Generate an EliteForge Java service project via Maven archetype wrapper script. Use when users ask to scaffold a new EliteForge service, provide companyName/productName/serviceName (kebab-case), need Maven archetype generation execution, or want tech stack to enableXXX mapping.
---

# EliteForge Java Service Generator (Maven Archetype)

## Goal
Create a new EliteForge Java service by running `scripts/generate.py`, and perform project build/initialization through project-internal `make` commands.

## Preconditions
- Require `python3`, `make`, JDK, and network access (for archetype download).

## Build Command Policy (MUST follow)
- In generated project root, use project-internal `make` targets for build/init/verify tasks.
- Do not run system Maven commands in generated project (for example: `mvn clean install`, `mvn test`).
- If Maven command is explicitly required in generated project, use project wrapper only: `./mvnw ...`.
- Never replace `./mvnw` with system `mvn` in command examples or execution steps.

## Required Inputs (never infer)
- `companyName`
- `productName`
- `serviceName`
- Validate all three with: `^[a-z0-9]+(-[a-z0-9]+)*$`
- If any value is missing or invalid, ask only for missing/invalid fields.

## Workflow (every run)
1. Collect and validate required inputs.
2. Build command and run script:
   - `python3 scripts/generate.py --company <companyName> --product <productName> --service <serviceName> [--desc "<projectDescription>"] [--tech "<tech stack text>"] [--enable enableX --enable enableY ...]`
3. Map tech stack to `enableXXX` when user provides stack text:
   - Use `references/mapping-rules.md`.
   - Pass explicit user switches through `--enable`.
   - Use `references/enable-flags.md` as canonical flag list.
   - If uncertain, ask instead of guessing.
4. Verify result:
   - Output folder exists: `app-<companyName>-<productName>-<serviceName>/`
   - `pom.xml` exists in that folder.
5. Run post-generation consistency checks in project root (`<artifactId>/`):
   - Java package should match expected package prefix (check `src/main/java` and `src/test/java`).
   - Maven model name should match expected value (check `pom.xml` `<name>`).
   - `pom.xml` `artifactId` should equal expected `artifactId`.
   - For any mismatch, report expected vs actual and stop.
6. Initialize project in root directory (`<artifactId>/`) by running `make install` and require success (exit code `0`):
   - Example: `cd app-<companyName>-<productName>-<serviceName> && make install`
7. For build/test/verification after generation, continue using project `make` targets (for example `make test`, `make build`) instead of direct Maven commands; if a Maven command is unavoidable, run `./mvnw ...` only.
8. On failure, return exact error and full executed command (including the failed `make` command).

## Coordinate Rules (script behavior)
- `groupId = cn.<companyName(with '-' -> '.')>.<productName(with '-' -> '.')>`
- `artifactId = app-<companyName>-<productName>-<serviceName>`

## Expected Values For Post-check
- `expectedGroupId = groupId`
- `expectedArtifactId = artifactId`
- `expectedJavaPackagePrefix = <expectedGroupId>.<serviceName(with '-' -> '.')>`
- `expectedMavenModelName = expectedArtifactId` (unless user explicitly requires another naming rule)

## Quick Examples
- Minimal:
  - `python3 scripts/generate.py --company cisdigital --product cap --service cache-center --desc "CAP 缓存中心"`
- Post-generation init (required):
  - `cd app-cisdigital-cap-cache-center && make install`
- Tech + explicit override:
  - `python3 scripts/generate.py --company cisdigital --product cap --service cache-center --tech "mysql redisson lombok mapstruct" --enable enableJacksonDatatypeJsr310`
