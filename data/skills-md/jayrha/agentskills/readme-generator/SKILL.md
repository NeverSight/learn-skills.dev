---
name: readme-generator
description: Generates polished, well-structured project READMEs with badges, a one-line tagline, quick-start, installation, usage examples, configuration tables, contribution guidelines, and a license section. Use this skill when the user asks to "write a README", "generate a README", "create README.md", "improve my README", "add badges", "document my project", "make a project description", or wants onboarding/landing-page docs for a library, CLI, web app, API, or repo.
license: MIT
---

# README Generator

## Overview

This skill produces a complete, polished `README.md` that serves as a project's
front door. It inspects the repository to ground the content in reality (real
install commands, real scripts, real entry points) rather than inventing
details, then assembles the appropriate sections in a conventional, scannable
order.

**Keywords:** readme, README.md, project documentation, badges, shields.io,
quick start, installation, usage, getting started, contributing, license,
table of contents, project description, onboarding docs.

A great README answers five questions fast:
1. **What** is this? (one sentence, above the fold)
2. **Why** should I care? (key features / value)
3. **How** do I install and run it? (quick start)
4. **How** do I use it? (usage + examples)
5. **How** do I contribute / get help / what license?

## Workflow

Follow these steps in order. Do not skip the investigation step — accuracy
beats fluff.

1. **Detect project type and facts.** Run `scripts/detect_project.py <repo>`
   (or inspect manually) to identify language, package manager, entry points,
   scripts, license, and existing badges. This drives which sections apply.
   See `references/section-catalog.md` for the type→section mapping.

2. **Confirm the essentials.** Gather (ask the user only for what you cannot
   infer): project name, one-line tagline, target audience, install command,
   minimal run/usage example, license, and repo URL (for badge slugs).

3. **Choose sections.** Start from the canonical order below and drop sections
   that do not apply. Never include an empty or placeholder section.

4. **Draft the header block.** Title (H1) → tagline (one line, no period needed)
   → badge row → optional hero image/demo → table of contents (only if the
   README is long, roughly 6+ H2 sections).

5. **Write Quick Start.** The single most important section. A reader should be
   able to copy-paste their way to a running result in under a minute. Use a
   fenced code block with a language hint and real commands.

6. **Fill body sections** (Features, Installation, Usage, Configuration, API,
   Examples, Roadmap) using concrete, copy-pasteable content. Prefer tables for
   options/flags/env vars.

7. **Add the closing block** (Contributing, License, Acknowledgments). Link to
   `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` if they exist; otherwise inline a
   short contributing blurb.

8. **Validate.** Run `scripts/lint_readme.py README.md` to check for broken
   relative links, missing alt text, placeholder leftovers (TODO, FIXME,
   `<your-...>`), heading hierarchy, and a present License section.

9. **Self-review** against `references/quality-checklist.md`.

## Canonical Section Order

```
# Project Name
> One-line tagline

[badges]
[hero image / demo gif]

## Table of Contents        (long READMEs only)
## Features                 (3-6 bullets, benefit-first)
## Quick Start              (copy-paste to a result)
## Installation             (all supported methods)
## Usage                    (common tasks + code)
## Configuration            (options table / env vars)
## API / Commands           (reference, if applicable)
## Examples                 (real scenarios)
## Roadmap                  (optional)
## Contributing             (link or short blurb)
## License
## Acknowledgments          (optional)
```

## Badge Quickref

Use [shields.io](https://shields.io). Place 4-7 badges max — relevant, not
decorative. Common patterns (replace `OWNER/REPO`):

```markdown
![Build](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml)
![npm](https://img.shields.io/npm/v/PACKAGE)
![PyPI](https://img.shields.io/pypi/v/PACKAGE)
![License](https://img.shields.io/github/license/OWNER/REPO)
![Coverage](https://img.shields.io/codecov/c/github/OWNER/REPO)
![Stars](https://img.shields.io/github/stars/OWNER/REPO?style=social)
```

See `references/badges.md` for a full catalog (CI, coverage, version,
downloads, language, code style, social, custom static badges) with the exact
markdown and link-wrapping pattern.

## Decision Heuristics

- **Library/package** → emphasize Installation, API, and import/usage snippets.
- **CLI tool** → emphasize Quick Start, Commands/flags table, examples.
- **Web app / service** → emphasize screenshots/demo, env config, deploy steps.
- **Mono-repo** → top-level overview + links to per-package READMEs.
- **Tiny project** → collapse to Title, tagline, Quick Start, Usage, License.
- **Unsure of a fact** → ask, or mark with a clearly-flagged TODO the user must
  fill — never silently fabricate version numbers, URLs, or commands.

## Best Practices

- Lead with value: the first screen must convey what and why.
- Make every code block copy-pasteable and language-tagged.
- Prefer tables for any list of options, flags, or environment variables.
- Use relative links for in-repo files (`./CONTRIBUTING.md`) and absolute for
  external resources.
- Always include alt text on images for accessibility.
- Keep the tagline under ~12 words; keep Features to 3-6 benefit-driven bullets.
- Show, don't tell: a real example beats a paragraph of description.
- Add a Table of Contents only when the document is long enough to need it.

## Common Pitfalls

- Fabricated install commands or version numbers — always ground in the repo.
- A wall of prose before the reader sees what the project is.
- Badges that don't resolve (wrong slug) or purely decorative badge spam.
- Multiple H1s (`#`) — there must be exactly one, the title.
- Placeholder leftovers shipped to users (`<your-name>`, TODO, lorem ipsum).
- Usage examples that don't actually run.
- Missing License section (legally important, frequently forgotten).

## Bundled Files

- `references/section-catalog.md` — every section, what goes in it, when to
  include it, and the project-type matrix.
- `references/badges.md` — full shields.io badge catalog with copy-paste markdown.
- `references/quality-checklist.md` — final self-review checklist.
- `templates/README.template.md` — fill-in template with guidance comments.
- `examples/cli-tool-readme.md` — a complete worked example for a CLI project.
- `scripts/detect_project.py` — inspects a repo and reports facts for grounding.
- `scripts/lint_readme.py` — validates a finished README.
