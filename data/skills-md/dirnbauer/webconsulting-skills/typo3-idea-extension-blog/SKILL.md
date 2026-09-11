---
name: "typo3-idea-extension-blog"
description: "Evaluates external ideas for TYPO3 extension potential, builds the extension, and drafts the companion German webconsulting.at MDX article. Use when the user shares a link, product, article, paper, or concept and asks whether it can become a TYPO3 extension, wants a GitHub-ready implementation, or needs a publication-ready TYPO3 blog post."
compatibility: "TYPO3 14.x preferred with TYPO3 13.4 fallback; PHP 8.2+; Git; network access for verification and push"
metadata:
  version: "1.0.0"
  related_skills: "grill-me, firecrawl, typo3-update, typo3-testing, webconsulting-create-documentation"
  origin: "webconsulting"
license: "MIT / CC-BY-SA-4.0"
---

# Idea -> TYPO3 Extension -> Blog Post Pipeline

> Source: https://github.com/dirnbauer/webconsulting-skills

Turn an external idea into a complete TYPO3 outcome: research, honest assessment, build, Git push, and German MDX publication draft.

## Non-Negotiables

- Do not skip source verification. Read the original source, not only summaries.
- Do not oversell. Say plainly when something is hype, vaporware, duplicated, or a poor TYPO3 fit.
- Do not rebuild TYPO3 features that already exist in Core or a mature extension ecosystem.
- Do not ask endless questions. Ask at most 10 focused questions, then move.
- Do not build before the user confirms the concept assessment.
- Do not leave credentials behind after a Git push.

## Recommended Skill Stack

Load adjacent skills when they materially improve the result:

- `grill-me`: use this right after the initial source summary to interrogate what the user actually wants to transfer into TYPO3 and to resolve open product decisions one question at a time
- `firecrawl`: fetching the source page, repo pages, and independent coverage
- `typo3-update`: TYPO3 v14-first architecture and API choices
- `typo3-testing`: unit tests and verification structure
- `webconsulting-create-documentation`: help when shaping the MDX deliverable

## Workflow

### Phase 1: Research & Verify (Do Not Skip)

1. Fetch the full article, announcement, or product page with the available web-fetch tooling.
2. Verify legitimacy through independent coverage. Search for discussion on news and community sites such as Hacker News, Slashdot, and Phoronix when relevant.
3. Check whether the project has a real public codebase. If it claims to be open source, verify that the GitHub or GitLab repository contains actual code and recent activity, not just a README.
4. Check whether TYPO3 already solves the problem through Core, a maintained extension, or a proven adjacent pattern.
5. Summarize the source for the user in 3-5 sentences before asking anything else.

If the idea is a hoax, April Fools post, abandoned repo, or obvious vaporware, say so immediately and pivot to alternatives.

### Phase 2: Clarify What We Actually Want

Start the scoping conversation with `grill-me` style discipline:

- walk the design tree branch by branch
- ask only one question at a time
- provide a recommended answer with each question
- stop after the scope is clear, not after an arbitrary maximum

Still keep the total question count lean. Ask at most 10 focused questions. Prefer a structured input tool if the client supports it; otherwise ask concise plain-text questions.

Good questions:

- Which ideas are actually worth transferring to TYPO3?
- Should the output include an extension, a blog post, or both?
- Should the extension target headless mode, traditional TYPO3 frontend, or both?
- Should the repo be private or public?
- Is the blog language German? Default to German for webconsulting.at.

Do not ask questions whose answers are already obvious from the user request or local context.

### Phase 3: Concept Assessment

Write a concise assessment before building. Cover these five areas:

| Area | What to cover |
|------|----------------|
| What TYPO3 already does better | Core features, mature extensions, existing APIs, reasons not to reinvent |
| What is genuinely new | Transferable ideas, UX patterns, workflow gains, technical differentiators |
| What is needed first | Dependencies, APIs, legal review, infrastructure, third-party services |
| Honest risks | Regulatory, adoption, maintenance, performance, ecosystem mismatch |
| Recommended architecture | TYPO3 mapping such as PSR-15 middleware, PSR-14 events, TCA, Extbase, CLI commands, site sets |

Present this as a short table or tightly written prose. Then stop and get explicit user confirmation before implementation.

### Phase 4: Build the TYPO3 Extension

Build a complete, push-ready TYPO3 extension when the concept passes review.

#### Repository Shape

Use this structure unless the project clearly needs a smaller variant:

```text
extension-name/
├── composer.json
├── README.md
├── LICENSE
├── .gitignore
├── Configuration/
│   ├── Services.yaml
│   ├── RequestMiddlewares.php
│   ├── TCA/Overrides/
│   └── Sets/
├── Classes/
│   ├── Middleware/
│   ├── Service/
│   ├── Configuration/
│   ├── Event/
│   ├── Command/
│   └── Domain/Model/
├── Resources/Private/Language/
├── ext_tables.sql
├── Tests/Unit/
├── phpunit.xml.dist
└── phpstan.neon
```

#### Implementation Rules

- Target TYPO3 v14 first, with TYPO3 13.4 fallback where reasonable.
- Use `declare(strict_types=1);` everywhere.
- Require PHP 8.2+.
- Use Composer type `typo3-cms-extension`.
- Use PSR-4 autoloading under `Webconsulting\{ExtensionName}\`.
- Prefer Symfony DI in `Configuration/Services.yaml`.
- Use PSR-15 for middleware and PSR-14 for events.
- Avoid legacy patterns such as `$GLOBALS['TYPO3_DB']`, hard dependencies on `ext_emconf.php`, and old signal-slot patterns.
- Keep `composer.json` metadata honest (description, constraints, dependencies).
- Add unit tests for value objects, configuration parsing, and core decision logic.

#### Architecture Choices

Choose the lightest TYPO3-native shape that solves the problem:

- use middleware for request/response concerns, headers, gateways, and protocol adapters
- use Extbase only when you truly benefit from controller and domain modeling
- use TCA overrides and site sets when the main value is editor-facing configuration
- use CLI commands with `#[AsCommand]` for imports, sync jobs, and batch tasks
- prefer existing TYPO3 APIs before inventing custom persistence or routing layers

### Phase 5: Push to GitHub

If the user wants the extension pushed:

1. Confirm the user already created the empty repository manually when API-based repo creation is blocked.
2. Configure git remote and authentication only for the duration needed.
3. Commit with a descriptive message.
4. Push to `main`.
5. Remove stored credentials immediately after the push.

Never leave tokens in shell history, committed files, examples, or config templates.

### Phase 6: Write the Blog Post

Create a publication-ready MDX post for webconsulting.at.

#### Writing Rules

- Language: German by default
- Tone: factual, professional, technically honest
- Gender-neutral language: use colon format such as `Nutzer:innen`
- Translate features into practical benefits
- Avoid marketing filler and empty superlatives

#### Required Frontmatter

Include:

- `date`
- `title`
- `description`
- `author` set to `Kurt Dirnbauer`
- `status`
- `categories`
- `lang`

#### Required Sections

1. `Auf einen Blick` with 4-6 bullets
2. Introduction with 2-3 short paragraphs
3. Technical explanation
4. TYPO3 implementation
5. Honest assessment with a warning-style callout
6. Installation and usage with copy-paste-ready commands
7. Roadmap using a timeline component
8. `Fazit` with a CTA to `/kontakt`

#### MDX Components

Use components only where they clarify the article:

- `Tabs` and `Tab`
- `DataTable`
- `ComparisonTable`
- `Callout`
- `Accordion`
- `Timeline`
- `TechResourceCallout`
- fenced code blocks with language labels
- Mermaid diagrams for architecture and flow

Always include a `TechResourceCallout` pointing to the GitHub repository when one exists.

### Phase 7: Deliver

At the end:

1. Push the extension when requested.
2. Present or save the MDX file in a way the user can open directly.
3. Confirm credentials were cleaned up.
4. Provide a 5-line summary of what was delivered.

## Decision Framework

| Signal | Action |
|--------|--------|
| Real idea, verified, good TYPO3 mapping | Build extension and blog post |
| Real idea, useful analysis, weak TYPO3 mapping | Write blog post only |
| Hoax, April Fools, or empty hype | Say so and suggest alternatives |
| Already solved well in TYPO3 | Point to the existing solution instead of rebuilding |
| Requires language/runtime changes TYPO3 cannot realistically absorb | Document concept only, no extension build |

## Quality Checklist

Before delivering, verify:

- extension installs via Composer without obvious constraint errors
- all PHP files use strict types
- `Services.yaml` wires the real services
- at least 5 unit tests cover core logic
- `README.md` explains install, config, usage, and architecture
- `composer.json` metadata is honest
- the blog post includes `Auf einen Blick`, honest assessment, `TechResourceCallout`, and `Timeline`
- German copy uses gender-neutral colon format
- no credentials remain on disk after push
- no hardcoded tokens, API keys, or sensitive values remain in the repo

## Example Prompts

- "Evaluate this product launch for TYPO3, build the extension if it makes sense, and draft the German blog post."
- "Read this article, tell me honestly whether it is relevant for TYPO3, and turn the good parts into a prototype extension."
- "Adapt this startup idea to TYPO3 and prepare both the repo and the webconsulting.at MDX article."
