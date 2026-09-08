---
name: project-bootstrap
description: "Use when the user requests repository setup, tooling infrastructure, or Jess's full project template. Skip coding, prototypes, and hardening requests that do not include repository setup."
---

# Project Bootstrap

Apply Jess's defaults to the repository setup the user requested. A request for
an application or a small prototype does not by itself request the full template.
Preserve established tooling unless migration is part of the request.

## Choose the scope

Infer the language, artifact type, and requested setup from the task. Distinguish
a minimal runnable project from a repository intended for distribution.
State material infrastructure choices before implementing them. Ask only when
missing information changes a decision the user owns.

- Minimal setup: source layout, dependency manifest, and the commands needed to
  run and verify the project.
- Repository tooling: formatter, linter, type/build checks, and CI.
- Distribution: release automation and contributor-facing files appropriate to
  the product.
- Full Jess template: repository tooling, applicable distribution files, and
  agent-rule and review infrastructure. Use only when the full template or those
  gates are requested.

## Tooling defaults

| Language | Formatter | Linter | Type/build check |
|---|---|---|---|
| Rust | rustfmt | clippy | cargo build / cargo test |
| Go | gofmt / goimports | staticcheck + go vet | go build / go test |
| TypeScript | oxfmt | oxlint | tsc --noEmit |
| Python | ruff format | ruff check | mypy or pyright |

Use one formatter and one lint configuration per language. Start with strict
type checking where supported. Keep boundary parsing possible: do not ban
unknown input types, runtime narrowing, or legitimate React effects globally.
Use code-craft for language-specific guidance when needed.

Define the check suite in one recipe shared by CI and local development.
If hooks are requested, use the same recipe or a scoped fast subset. Do not run
slow full-suite checks on every commit merely to duplicate CI.

## Agent infrastructure

When agent-rule enforcement or AI review is requested, put each rule at the
lowest layer that can express it faithfully. Prefer compiler and linter checks
over a new agent-rule system. Do not duplicate the same gate across layers.

For an agent-specific rule that needs enforcement, use structural matching where
possible and provide a CI check independent of agent edits. For an AI review
gate, keep reviewer definitions reviewable and protect them through the repo's
ownership rules. Required gates must not silently pass when evaluation fails.

## Distribution and project files

For a CLI intended for binary distribution, prefer tag-triggered releases with
checksummed archives for the supported platforms. Derive the version from the
tag. Include installers only when requested or needed by the distribution plan;
they must verify checksums before installing.

Keep supported platforms and package registries tied to the intended users.
Do not build a platform matrix for an unpublished prototype.

For a repository intended for public distribution, include the license,
contribution instructions, and a private security-reporting path. Add conduct
guidelines, issue templates, dependency updates, and release workflows when the
full template or their specific purpose is requested.

Jess's new-license choices are AGPL-3.0-or-later or Apache-2.0. Ask which to use
when licensing a new project unless the user already chose. With AGPL, Jess's
default for documentation is CC-BY-SA-4.0, recorded in NOTICE. Preserve existing
licenses and third-party notices.

## Verify and report

Run the generated setup and required checks. Confirm CI invokes the maintained
check recipe. Report what was configured and any unverified platform or external
service. Do not publish, create remote repositories, or configure paid services
without authorization for those actions.
