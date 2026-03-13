---
name: devcontainers-best-practices
description: Looks up the Development Container spec, devcontainer.json reference, and schema; finds Features and Templates; identifies tools that support devcontainers (VS Code, VS Code-based editors such as Cursor, Zed, Codespaces, DevPod, etc.). Use when editing devcontainer.json, choosing Features or Templates, or when the user asks about dev containers, devcontainer.json, or containers.dev.
license: MIT
metadata:
  author: Afonso Graça
---

# Devcontainers Best Practices

This skill guides you to the right documentation and references for the Development Container ecosystem. Use it when working with `devcontainer.json`, selecting Features or Templates, or when the user asks about dev containers, containers.dev, or supporting tools.

## Quick start

Minimal `devcontainer.json` using an image and a Feature: `"image": "mcr.microsoft.com/devcontainers/base:ubuntu"`, `"features": { "ghcr.io/devcontainers/features/git:1": {} }`. For property details and validation, see [Quick lookup](#quick-lookup) item 1 and [references/schema.md](references/schema.md).

## When to use this skill

- Editing or validating `devcontainer.json`
- Looking up a property (syntax, type, tool support)
- Choosing or referencing a Feature or Template
- Checking which tools support the spec or have tool-specific properties/limitations
- Understanding the spec (lifecycle, merge logic, image metadata)
- Authoring or publishing a Dev Container Feature (see the Authoring section in [references/features.md](references/features.md) and the [containers.dev authoring guide](https://containers.dev/guide/feature-authoring-best-practices))
- Configuring multiple dev containers (multi-project, shared Compose); see [references/tools.md](references/tools.md) and [VS Code / multi-container docs](https://code.visualstudio.com/docs/devcontainers/containers)

## Canonical sources

All content in this skill and its references is traceable to these sources:

- **Spec and reference**: [containers.dev/implementors/spec](https://containers.dev/implementors/spec/), [containers.dev/implementors/json_reference](https://containers.dev/implementors/json_reference/)
- **Schema**: [containers.dev/implementors/json_schema](https://containers.dev/implementors/json_schema/)
- **Guides**: [containers.dev/guides](https://containers.dev/guides) (prebuilds, using Dockerfile/Compose, Feature authoring best practices, GitLab CI)
- **Supporting tools**: [devcontainers.github.io/supporting](https://devcontainers.github.io/supporting)
- **Features**: [containers.dev/implementors/features](https://containers.dev/implementors/features/), [github.com/devcontainers/features](https://github.com/devcontainers/features)
- **Templates**: [containers.dev/implementors/templates](https://containers.dev/implementors/templates/), [github.com/devcontainers/templates](https://github.com/devcontainers/templates)

## Reference files

Detailed material is in the `references/` directory. Load only what you need.

| Need | File |
|------|------|
| When to use the full spec, key concepts, merge logic, lifecycle | [references/spec.md](references/spec.md) |
| JSON reference vs schema, canonical URLs, how to validate | [references/schema.md](references/schema.md) |
| Supporting tools, tool-specific properties, limitations | [references/tools.md](references/tools.md) |
| VS Code workflows, requirements, prebuild, ports, extensions, limitations, dotfiles, managing containers | [references/vscode-containers.md](references/vscode-containers.md) |
| Tips and tricks (OS, Git, performance, troubleshooting, profile persistence, reporting) | [references/tips-and-tricks.md](references/tips-and-tricks.md) |
| Official Features, OCI refs, versioning, options, install order, **authoring** Features | [references/features.md](references/features.md) |
| Official Templates, when to use template vs Feature vs Dockerfile | [references/templates.md](references/templates.md) |

## Quick lookup

1. **Property or behavior in devcontainer.json**  
   Use the [Dev Container metadata reference](https://containers.dev/implementors/json_reference/) (or [references/spec.md](references/spec.md)) for property-by-property details. For validation, use the [devcontainer.json schema](https://containers.dev/implementors/json_schema/) or Dev Container CLI; see [references/schema.md](references/schema.md).

2. **Tool support or tool-specific settings**  
   Check [devcontainers.github.io/supporting](https://devcontainers.github.io/supporting) for the list of tools, `customizations.*` (e.g. `customizations.vscode`, `customizations.codespaces`), and limitations. Summary in [references/tools.md](references/tools.md).

3. **Advanced scenarios (env vars, mounts, performance, non-root user, remote Docker, multiple containers, Git credentials)**  
   See [VS Code Advanced container configuration](https://code.visualstudio.com/remote/advancedcontainers/overview). Summary and workflow links in [references/vscode-containers.md](references/vscode-containers.md).

4. **Multiple dev containers (multi-project, shared Docker Compose)**  
   See [references/tools.md](references/tools.md) “Multiple containers / multi-project” and [Chris Ayers – Multiple dev containers](https://chris-ayers.com/posts/stir-trek-and-multiple-dev-containers/).

5. **OS-specific or troubleshooting (Git, Docker Desktop, cleanup, logs)**  
   See [VS Code Dev Containers Tips and Tricks](https://code.visualstudio.com/docs/devcontainers/tips-and-tricks). Summary in [references/tips-and-tricks.md](references/tips-and-tricks.md).

6. **Feature ID, options, or install order**  
   Official Features: [containers.dev/features](https://containers.dev/features), [github.com/devcontainers/features](https://github.com/devcontainers/features). OCI refs: `ghcr.io/devcontainers/features/<name>:<version>`. Details in [references/features.md](references/features.md). For **authoring** Features, see the Authoring section there and [containers.dev/guide/feature-authoring-best-practices](https://containers.dev/guide/feature-authoring-best-practices).

7. **Template or "template vs Feature vs Dockerfile"**  
   Official Templates: [containers.dev/templates](https://containers.dev/templates), [github.com/devcontainers/templates](https://github.com/devcontainers/templates). When to use which: [references/templates.md](references/templates.md).

8. **Spec concepts (lifecycle, merge, image metadata)**  
   Full spec: [containers.dev/implementors/spec](https://containers.dev/implementors/spec/). Summary: [references/spec.md](references/spec.md).

## Best practices (from official docs)

Only apply recommendations that are stated in the spec or official devcontainer documentation; cite the source when relevant.

- **Environment variables**: Prefer `containerEnv` over `remoteEnv` when possible so all processes in the container see the variable and it is not client-specific. Use `remoteEnv` when the value is not static and you want to avoid rebuilding. ([Dev Container metadata reference – containerEnv/remoteEnv](https://containers.dev/implementors/json_reference/).)
- **Port forwarding**: In most cases use the `forwardPorts` property rather than `appPort`; forwarded ports behave like localhost to the application. Use `appPort` (or Docker Compose `ports`) when you need published/network-visible ports. ([VS Code – Forwarding or publishing a port](https://code.visualstudio.com/docs/devcontainers/containers#forwarding-or-publishing-a-port), [Dev Container metadata reference](https://containers.dev/implementors/json_reference/).)
- **Pre-build when possible**: Pre-building images (e.g. with Dev Container CLI or GitHub Actions) speeds up startup and lets you pin tool versions; image metadata can be inherited so repos need only a minimal `devcontainer.json`. ([VS Code – Pre-building dev container images](https://code.visualstudio.com/docs/devcontainers/containers#pre-building-dev-container-images), [containers.dev/guides](https://containers.dev/guides).)
- **Security and trust**: Dev container configs and images can run arbitrary commands. Only use configs and images from trusted sources. For sandboxing and security context, see the spec and community articles (e.g. [The Red Guild – Where do you run your code](https://blog.theredguild.org/where-do-you-run-your-code/) with attribution).
- **Feature versions**: To pin to a specific version, append it to the Feature ID (e.g. from the [versions list](https://github.com/devcontainers/features/pkgs/container/features/go/versions)). The `:latest` tag is applied implicitly if omitted. ([Features – containers.dev](https://containers.dev/implementors/features/).)
- **Rebuild after changes**: After changing the dev container configuration, rebuild so tools pick up changes (e.g. "Dev Containers: Rebuild Container" or "Codespaces: Rebuild Container" in the command palette, in VS Code or compatible editors such as Cursor). ([VS Code Dev Containers extension](https://devcontainers.github.io/supporting), [GitHub Codespaces](https://devcontainers.github.io/supporting).)
- **Lifecycle script order**: Creation scripts run in this order: `onCreateCommand` → `updateContentCommand` → `postCreateCommand`. If one fails, later scripts are not run. ([Dev Container metadata reference – Lifecycle scripts](https://containers.dev/implementors/json_reference/).)

When the spec or official docs do not state a recommendation, do not present it as a best practice; either omit it or phrase it as a suggestion with a clear citation.

**Optional / community guidance:** Community articles (e.g. [Daytona – Ultimate guide to dev containers](https://www.daytona.io/dotfiles/ultimate-guide-to-dev-containers)) suggest practices such as keeping images lightweight, caching dependencies, and using Docker Compose for multi-service setups. Use with attribution and prefer spec/official docs when they conflict.

## Summary

- Use this skill when editing `devcontainer.json`, choosing Features/Templates, authoring Features, or answering questions about dev containers or containers.dev.
- Resolve questions via the canonical URLs above and the reference files under [references/](references/).
- Best practices: cite containers.dev or devcontainers.github.io; only include guidance that appears there. For OS-specific or troubleshooting issues, consult [VS Code Dev Containers Tips and Tricks](https://code.visualstudio.com/docs/devcontainers/tips-and-tricks) and [references/tips-and-tricks.md](references/tips-and-tricks.md).
