---
name: java-conventions
description: Versioned Java coding conventions for writing, generating, or reviewing Java code. Use when the user asks about Java style, Java conventions, idiomatic Java, modern Java, Java 25, or when writing/reviewing Java code where context-specific skills do not already cover style. Triggers on "Java conventions", "Java style", "Java code style", "modern Java", "Java 25", "idiomatic Java", or any request to write or review Java code. Composes with framework- and architecture-specific skills; when a composed skill specifies a rule, that rule wins.
---

# Java Conventions

Enforce versioned, idiomatic Java language conventions. This skill is the fallback baseline for syntax, style, naming, visibility, structure, methods, streams, exceptions, and comments. Build, packaging, framework, protocol, and architecture rules come from composed skills (e.g., `java-cli-script`, `java-cli-app`, `microprofile-server`, `spring-boot-server`, `sdd4j-bce`, `migrate-to-bce`).

## How to Use This Skill

1. Determine the target Java version:
   - Use the version the user explicitly mentions.
   - Otherwise, read the version from the project (`pom.xml`, `build.gradle`, `module-info.java`, `README.md`, `system.properties`).
   - Default to **25** if no version is found.
2. Load the matching reference file from `references/java-<version>.md`.
3. Apply the loaded conventions as the fallback baseline.
4. If a composed skill has a specific rule for the same topic, the composed skill wins.

## Bundled References

- Java 25 — [references/java-25.md](references/java-25.md)

When a reference for the requested version does not yet exist, fall back to the highest bundled reference that is not newer than the target, and only use features available in the target version. If the target is higher than all bundled references, use the newest bundled reference and note that it may not cover the latest features.

## Scope

- Language-level rules only: syntax, style, naming, visibility, structure, methods, streams, exceptions, comments.
- Not build, packaging, framework, protocol, or architecture rules.
- When a composed skill specifies a rule, the composed skill wins; this skill is the fallback baseline.

## Composition

- This skill defines only language-level Java conventions.
- Build, packaging, file layout, frameworks, protocols, and architecture come from the composed skill.
- When a composed skill adds or refines a rule, apply it on top of these rules; the composed skill always specializes, never contradicts.
- If a composed skill is silent on a topic covered here, these rules apply by default.
