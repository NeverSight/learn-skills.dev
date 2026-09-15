---
name: github-repo-launch-page
description: Use this skill when creating, auditing, or redesigning a public GitHub repository so the repository is easy to understand, trust, share, install, and contribute to. Use together with github-repo-product-naming whenever naming, renaming, positioning, repo slug, About description, or product identity matters.
---

# GitHub Repository Launch Page Skill

## Purpose

Turn a repository from “code dump” into a public project page that answers, in order:

1. What is this?
2. Who is it for?
3. Why should I care now?
4. Can I trust it?
5. Can I try it in under five minutes?
6. Where do I go next?

This skill covers the whole GitHub repo surface:

- repository name and product name
- GitHub About description
- homepage URL
- topics
- README
- screenshots, demos, diagrams, social preview
- docs structure
- license, contribution, security, and support files

For naming work, invoke `github-repo-product-naming` first or in parallel. A good README cannot fully compensate for a weak name.

## When to use

Use this skill when the user asks to:

- create or rewrite a repository README
- make a GitHub repo look more attractive, credible, or “viral”
- prepare a repo for launch, sharing, recruiters, Hacker News, Reddit, LinkedIn, or X
- improve repository SEO/discoverability
- set GitHub About description, topics, website, pinned repo appearance, social preview, docs, screenshots, badges, issue templates, or contribution files
- reverse-engineer successful open-source README patterns

## Inspect before writing

Inspect these when available:

- repo name, package/application name, CLI name
- GitHub About description, homepage URL, topics, license, visibility, archived status
- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `.github/ISSUE_TEMPLATE/*`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/`
- `examples/`
- `demo/`
- `assets/`
- `screenshots/`
- package files such as `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Dockerfile`, `docker-compose.yml`
- tests and CI workflows
- existing screenshots, diagrams, demo GIFs, videos, landing pages, docs pages, releases
- whether the project contains private, employer-owned, secret, or unsafe information

If metadata cannot be read automatically, ask for or output a manual checklist.

## Naming dependency

Before finalizing the README, check whether the name itself carries the desired association.

Use `github-repo-product-naming` if any of these are true:

- the repo name sounds like internal documentation
- the name is only a category, such as `engineering-methods` or `workstation-setup`
- the name is too long
- the name triggers the wrong association
- the name fails to express the product identity
- the user wants something more “badass,” memorable, viral, or open-source-native
- the repo is part of a multi-repo ecosystem and needs naming consistency

Do not bury naming in the README. Naming is a strategic layer.

## Reverse-engineered launch-page patterns

Strong public repositories usually combine these near the top:

### 1. Hero block

Common pattern:

```md
# ProjectName — concrete promise

> Memorable one-line tagline.

[badges]

![screenshot or banner](...)

One short paragraph explaining what it is, who it is for, and the concrete outcome.
```

Good hero blocks are specific. They do not start with internal architecture.

Strong variations:

- Product/tool page: name, witty tagline, badges, screenshot, then concrete operational benefit.
- Framework/platform page: centered logo, short category claim, install command, ecosystem links.
- Research/model page: paper/blog/model-card links, concise model description, diagram, setup, model table, CLI and Python usage.
- Community/devtool page: logo, personality, compatibility, install command, manual inspection/security note.
- Developer utility page: screenshot first, “why” bullets, quick install, privacy/security notes, docs links.

### 2. Positioning paragraph

Use this formula:

```text
<Project> is a <category> for <target user> who need to <job-to-be-done>. It helps them <outcome> by <mechanism/differentiator>, while <constraint or trust factor>.
```

Examples:

```text
RepoPilot is a local-first CLI for maintainers who need to triage many GitHub issues quickly. It mirrors issues into SQLite, clusters duplicates, and produces reviewable summaries without sending private repository content to a hosted backend.
```

```text
ProofStack turns private work evidence into public-safe career signal: resumes, LinkedIn sections, portfolio stories, articles, and interview material that preserve proof without leaking private details.
```

### 3. Why section

Use `## Why` before exhaustive features.

Good “Why” bullets identify painful moments:

```md
## Why

- Stop guessing which command to run first.
- Keep private data local by default.
- Make the happy path copy-pasteable.
- Give maintainers a quick mental model before they read the code.
```

Bad “Why” bullets are vague:

```md
- Easy to use
- Fast
- AI-powered
- Modern
```

### 4. Quickstart before deep docs

Place a working quickstart within the first ~100-150 README lines when possible.

Minimum quickstart:

````md
## Quickstart

```bash
# install
...

# run
...
```

Expected result:

```text
...
```
````

If setup is complex, provide one of:

- Docker quickstart
- hosted demo
- GitHub Codespaces
- sample input/output
- dry-run mode
- screenshots only, if the project is not runnable yet

### 5. Screenshot/demo proof

Add at least one of:

- hero screenshot
- short GIF
- CLI recording
- architecture diagram
- before/after image
- sample output
- hosted demo link
- social preview image

Every visual needs useful alt text. Avoid decorative screenshots with no explanation.

### 6. Capability bullets

Use 5-7 bullets, each with outcome + mechanism:

```md
## Features

- **Local archive** — mirrors issues and PRs into SQLite for offline triage.
- **Duplicate clustering** — groups related reports before maintainers read them manually.
- **Reviewable output** — writes Markdown summaries instead of taking irreversible actions.
```

Do not list implementation details unless they matter to adoption.

### 7. Trust blocks

Add only true, relevant trust information:

- license
- privacy model
- security model
- data storage location
- permissions required
- limitations
- current status: alpha, beta, production, experiment, archived
- known risks
- supported OS/Python/Node versions
- tests/CI status
- who maintains it

Never fake stars, downloads, production users, sponsors, benchmarks, or affiliations.

### 8. Next-path links

Near the top, give direct links:

```md
<p align="center">
  <a href="#quickstart">Quickstart</a> ·
  <a href="docs/">Docs</a> ·
  <a href="examples/">Examples</a> ·
  <a href="CHANGELOG.md">Changelog</a> ·
  <a href="CONTRIBUTING.md">Contributing</a>
</p>
```

## Recommended README structure

Use this default unless the repo type calls for a variant.

```md
# ProjectName — one-line concrete promise

> Memorable tagline.

[badges]

![Hero screenshot or banner](assets/social-preview.png)

Short positioning paragraph: what it is, who it is for, outcome, differentiator.

<p align="center">
  <a href="#quickstart">Quickstart</a> ·
  <a href="#features">Features</a> ·
  <a href="docs/">Docs</a> ·
  <a href="#contributing">Contributing</a>
</p>

## Why

## Features

## Quickstart

## Demo

## How it works

## Use cases

## Requirements

## Configuration

## Documentation

## Privacy and security

## Roadmap / status

## Contributing

## License
```

## README variants

### Product or app

Use when the repo ships a user-facing app.

Order:

1. hero image
2. one-line promise
3. screenshot
4. why
5. install
6. first-run steps
7. features
8. permissions/privacy
9. docs
10. support
11. license

### Framework or library

Use when the repo is a developer platform, SDK, or package.

Order:

1. logo/name/tagline
2. install command
3. minimal code example
4. ecosystem map
5. why use it
6. API docs/reference
7. integrations/examples
8. contributing
9. license

### Research/model repo

Use when the repo is a model, paper implementation, benchmark, or ML artifact.

Order:

1. project name
2. links: paper, blog, model card, demo, dataset
3. short abstract
4. diagram/approach
5. setup
6. model/data table
7. CLI usage
8. Python/API usage
9. evaluation/limitations
10. citation
11. license

### CLI/devtool/config repo

Use when the repo is a terminal/dev workflow tool.

Order:

1. catchy but precise tagline
2. animated demo or screenshot
3. install command
4. 3 common commands
5. configuration
6. examples
7. safety/manual inspection note
8. troubleshooting
9. contribution guide

### Skill/plugin repository

Use when the repo packages AI-agent skills, Claude Code plugins, Codex plugins, prompts, commands, or reusable instructions.

Order:

1. product name and exact use case
2. ecosystem compatibility: Codex, Claude Code, OpenCode, ChatGPT, MCP, etc.
3. install commands
4. included skills table
5. workflow examples
6. safety/privacy model
7. local development setup
8. contribution and extension guide

## GitHub metadata checklist

Prepare these separately from `README.md`.

### Repository name

The repo name should be chosen with `github-repo-product-naming`.

Basic constraints:

- short
- pronounceable
- searchable
- specific enough to remember
- no unnecessary suffixes like `-app`, `-tool`, `-repo`, unless needed
- consistent casing across README, package name, CLI name, docs, website, and install commands

### GitHub About description

Recommended length: 70-140 characters.

Formula:

```text
<Category> for <target user> to <outcome> with <differentiator>.
```

Examples:

```text
Local-first GitHub issue triage CLI for maintainers drowning in duplicate reports.
```

```text
Engineering methods for code, agents, docs, security, reviews, and system architecture.
```

Avoid:

- “A simple tool…”
- “AI-powered app…”
- “This repository contains…”
- implementation-only descriptions

### Homepage URL

Add a homepage if any exists:

- docs site
- deployed app
- demo
- blog post
- project landing page
- package page

### Topics

Use up to 20 topics. Topics should be lowercase, hyphen-separated, and discoverable.

Use a mix:

- domain: `agentic-ai`, `developer-tools`, `workflow-automation`
- language/framework: `python`, `typescript`, `swift`, `langchain`
- artifact type: `cli`, `macos`, `chrome-extension`, `github-profile`
- problem: `issue-triage`, `browser-automation`, `readme-generator`
- audience: `maintainers`, `data-engineering`, `ai-agents`

Do not add irrelevant popular topics.

### Social preview

Create a repository social preview image.

Recommended:

- 1280 x 640 px
- PNG or JPG
- under 1 MB
- project name large enough to read in link previews
- 1-sentence promise
- screenshot or product visual if helpful
- solid background unless transparency is deliberately tested

### Badges

Use badges sparingly. Prefer:

- package version
- license
- CI
- docs
- release
- supported platform
- package downloads, only if meaningful

Do not lead with 20 badges.

## Deterministic audit checks

### README top-of-file checks

- H1 exists in first 5 lines.
- One-line promise appears in first 15 lines.
- First 100 words explain category, audience, outcome, and differentiator.
- At least one of screenshot, diagram, GIF, logo, or sample output appears before deep docs.
- Quickstart or install link appears before line 150, unless the repo is not runnable.
- No “TODO”, “lorem ipsum”, placeholder badges, or dead demo links remain.

### Naming checks

- Name is not just a folder/category.
- Name triggers the desired association.
- Name does not trigger a stronger wrong association.
- Name has a subtitle that explains the literal category.
- Repo slug is lowercase, URL-safe, and install-command-friendly.
- If the repo is part of an ecosystem, name fits the ecosystem.
- If the name decision is nontrivial, `github-repo-product-naming` output exists.

### Required section checks

At minimum, the README should contain sections or equivalent links for:

- Why / Motivation
- Features / Capabilities
- Quickstart / Installation
- Usage / Examples
- Requirements
- Documentation / More examples
- Status / Limitations, if not mature
- Contributing / Support
- License

### Link and asset checks

- All relative links resolve.
- All images resolve.
- Image alt text is meaningful.
- Social preview image exists.
- README does not exceed GitHub truncation limits.
- Local docs linked from README exist.
- Code snippets have language tags.

### Command checks

- Shell commands are copy-pasteable.
- Installation command matches package manager metadata.
- The quickstart can be run from a fresh clone or states prerequisites clearly.
- Dangerous commands are avoided or explained.
- Commands do not assume secrets unless `.env.example` exists.

### Metadata checks

- Description is outcome-focused.
- Homepage is set if available.
- Topics are relevant, lowercase, hyphen-separated, <= 20.
- License exists and matches README claim.
- If the repo wants contributors, issue templates and contribution guidelines exist.

### Claim checks

Reject or rewrite claims that are:

- unverifiable
- exaggerated
- employer-confidential
- based on private metrics
- using fake stars/downloads/users
- implying affiliation without permission

## Output format

When applying this skill, produce:

1. **Diagnosis**: what currently blocks adoption.
2. **Naming and positioning**:
   - current name assessment
   - proposed product name
   - repo slug
   - tagline
   - one-sentence positioning
   - rejected names and why
3. **README**: complete `README.md` or patch.
4. **GitHub UI settings**:
   - About description
   - homepage URL
   - topics
   - social preview suggestion
5. **Assets to create**:
   - screenshots
   - banner/social preview
   - demo GIF
   - diagrams
6. **Repository hygiene TODOs**:
   - license
   - contributing
   - issue templates
   - docs
   - changelog
   - security/privacy
7. **Deterministic checklist result**.

## Tone rules

Use:

- concrete nouns
- observable outcomes
- short paragraphs
- proof before hype
- honest limitations
- plain English
- copy-pasteable commands

Avoid:

- “revolutionary”
- “game-changing”
- “seamless” unless explained
- “AI-powered” without saying what task the AI performs
- huge architecture dumps before the user knows why the project matters
- pretending a private experiment is production-ready

## Arthur-specific default positioning

For Arthur Zakirov’s public repos, default to this public-safe positioning unless the repo evidence says otherwise:

```text
Practical data/cloud engineer building small automation systems for high-friction personal and developer workflows.
```

Good recurring themes:

- data engineering
- cloud workflows
- Python automation
- browser/task automation
- agentic AI applications
- personal productivity systems
- developer tooling
- public lab / practical experiments

Known ecosystem direction:

- `ProofStack` — career proof and public-safe positioning
- `AgentDesk` — machine and AI-agent workstation setup
- `SystemSmith` — engineering methods for code, agents, and architecture

Avoid claiming private employer ownership, private company code, or production metrics unless the user explicitly provides public-safe proof.
