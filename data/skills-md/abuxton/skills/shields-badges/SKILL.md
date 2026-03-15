---
name: shields-badges
description: 'Analyse a repository to identify its focus, technology stack, and labels, then search for and apply appropriate shields.io badges to markdown files.'
---

# Shields Badges Skill

Add relevant [shields.io](https://shields.io) badges to a repository's markdown files. Analyse the repository to understand its purpose and stack, select the most appropriate badges, and insert them into the README or other markdown files in the correct format.

## Role

You are an expert in open-source project presentation and markdown authoring. You understand shields.io badge formats, repository metadata, and how to communicate a project's health and identity at a glance.

- Identify the repository's primary language, frameworks, CI/CD tooling, and package ecosystem from files present in the repository
- Recognise repository focus from README content, GitHub topics, issue and PR labels, and workflow definitions
- Select badges that are accurate, informative, and relevant to the repository's audience
- Insert badges in valid markdown, correctly placed and formatted
- Never add badges that reference non-existent workflows, packages, or services

## Workflow

1. **Discover repository context** — Examine the following to determine the project's focus, stack, and metadata:
   - `README.md` (or other root markdown files) for existing badges, description, and technology mentions
   - Language files: `package.json`, `go.mod`, `Pipfile` / `pyproject.toml`, `*.gemspec`, `*.csproj`, `Cargo.toml`, `pom.xml`, `build.gradle`
   - CI/CD workflow files in `.github/workflows/` — note workflow file names for build-status badges
   - `LICENSE` or `LICENSE.*` files — determine the licence type
   - `.github/` labels configuration or repository label metadata
   - Repository topics / tags if available in context

2. **Identify focus areas** — Based on step 1, determine:
   - Primary language(s) and framework(s)
   - Package registry (npm, PyPI, RubyGems, Docker Hub, NuGet, Maven Central, etc.)
   - CI/CD system and workflow file name
   - Licence identifier (MIT, Apache-2.0, GPL-3.0, etc.)
   - Code coverage service (Codecov, Coveralls, etc.) if present
   - Deployment target (Docker, Kubernetes, cloud provider, etc.)

3. **Select badges** — Choose the most relevant badges from the categories below, using the reference in `references/shields-categories.md`. Apply the following rules:
   - Include **build/CI status** if a `.github/workflows/` file exists
   - Include **licence** if a `LICENSE` file exists
   - Include **version/release** if the project is published to a package registry or has GitHub releases
   - Include **top language** for single-language projects without a registry badge
   - Include **code coverage** only if a coverage service is configured
   - Include **Docker** badges only if a `Dockerfile` or Docker Compose file exists
   - Limit the badge set to the **five most relevant** badges to avoid clutter; add more only when clearly warranted
   - Prefer dynamic badges (pulling live data) over static badges unless no dynamic option exists

4. **Generate badge markdown** — Produce each badge in the form:

   ```markdown
   [![Alt Text](https://img.shields.io/...)](https://link-to-relevant-page)
   ```

   - Use descriptive `Alt Text` (e.g. `Build Status`, `License`, `npm version`)
   - Link each badge to the relevant page (Actions run, license file, registry page, etc.) using **absolute HTTPS URLs**
   - Replace `<USER>`, `<REPO>`, and `<WORKFLOW_FILE>` placeholders with actual values — `<WORKFLOW_FILE>` is the full workflow filename including the `.yml` extension (e.g. `ci.yml`)
   - Add `?branch=main` (or the appropriate default branch name) to workflow status badge URLs

5. **Apply badges to README** — Insert the badge block immediately after the main H1 heading (`# Title`) and before any prose text. If badges already exist, replace the existing badge block rather than duplicating it. If there is no H1 heading, insert at the top of the file.

6. **Validate** — Confirm:
   - All badge URLs reference real paths (existing workflow files, correct package names, etc.)
   - Markdown syntax is valid (no broken links, no trailing spaces)
   - The README renders correctly with the new badges in their position

## Badge Format Reference

### Dynamic GitHub Badge Examples

```markdown
[![Build Status](https://img.shields.io/github/actions/workflow/status/<USER>/<REPO>/<WORKFLOW_FILE>?branch=main)](https://github.com/<USER>/<REPO>/actions)
[![License](https://img.shields.io/github/license/<USER>/<REPO>)](https://github.com/<USER>/<REPO>/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/<USER>/<REPO>)](https://github.com/<USER>/<REPO>/releases)
[![Top Language](https://img.shields.io/github/languages/top/<USER>/<REPO>)](https://github.com/<USER>/<REPO>)
[![Contributors](https://img.shields.io/github/contributors/<USER>/<REPO>)](https://github.com/<USER>/<REPO>/graphs/contributors)
```

### Static Badge Example

```markdown
[![Powered by Shields.io](https://img.shields.io/badge/Powered_by-Shields.io-brightgreen?logo=shieldsdotio)](https://shields.io)
```

### Style Customisation

Append query parameters to any badge URL as needed:

- `?style=flat-square` — flat square style
- `?style=for-the-badge` — large prominent style
- `?logo=<name>` — add a named logo (see `references/shields-categories.md` for logo names)
- `?logoColor=white` — set logo colour
- `?label=<text>` — override the left-hand label text
- `?color=<hex>` — override the right-hand colour

## Repository Focus Recognition Guide

Use these signals to infer the repository's primary purpose:

| Signal | Inferred Focus |
| ------ | -------------- |
| `package.json` with `main` or `bin` | Node.js library or CLI tool |
| `package.json` with `react`/`vue`/`angular` dependency | Frontend web application |
| `go.mod` present | Go module or CLI tool |
| `Pipfile` / `pyproject.toml` / `setup.py` | Python package or application |
| `*.gemspec` | Ruby gem |
| `*.csproj` / `*.sln` | .NET application or library |
| `Cargo.toml` | Rust crate |
| `pom.xml` / `build.gradle` | Java/Kotlin library or application |
| `Dockerfile` / `docker-compose.yml` | Containerised service or tool |
| `*.tf` / `*.tfvars` | Terraform infrastructure |
| `.github/workflows/` with deploy steps | Deployed service or published package |
| Issue/PR labels: `bug`, `enhancement`, `documentation` | General open-source project |
| Repository topics containing `cli`, `library`, `api`, `docker`, `terraform`, etc. | Topic-specific classification |

## Notes

- Always use HTTPS URLs for badge images
- Test badge URLs in a browser or with `curl` if uncertain whether a dynamic endpoint exists for the repository
- For monorepos or multi-language repositories, favour badges that reflect the primary entrypoint or most-used component
- Consult `references/shields-categories.md` for a full list of badge URL patterns and common sets by repository type
