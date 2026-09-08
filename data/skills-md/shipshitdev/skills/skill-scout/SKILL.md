---
name: skill-scout
description: Search local, marketplace, repository, package, GitHub, and web sources before creating a new skill or custom implementation. Use when asked to create, fork, import, or evaluate a skill, or before writing code for functionality that likely already exists.
metadata:
  version: "1.0.1"
  tags: "skills, research, discovery, reuse, search-first"
---

# Skill Scout

Find the best existing skill, pattern, package, or reference implementation
before creating a new skill or writing custom code.

## Contract

Inputs:

- Desired workflow, capability, or skill idea
- Target repo, platform, framework, or tool constraints
- Optional external candidate URLs or package names

Outputs:

- Ranked candidate table with source, fit, risks, and gaps
- Recommendation: use existing, fork/extend, compose, or create fresh
- Adoption notes for the selected path

Creates/Modifies:

- None in scout mode
- New or modified skill only after the search result supports it or the user explicitly asks

External Side Effects:

- Read-only local, package registry, GitHub, documentation, or web searches
- No install, publish, or remote write by default

Confirmation Required:

- Before installing external code
- Before importing a third-party skill into this repo
- Before creating a new skill when a close match exists

Delegates To:

- `skill-creator` when creating or rewriting a skill after scouting
- `skill-creator` to compare an existing skill contract before adding an overlap
- `git-safety` before publishing private code as a public skill

## When to Use

- User asks to create, build, fork, rewrite, import, or find a skill.
- User asks whether a skill exists for a workflow.
- A requested feature likely has existing package, framework, MCP, or repo examples.
- A new helper, abstraction, integration, command, or workflow is about to be written.
- A maintainer wants to avoid duplicating community or local work.

If the user explicitly says to skip research or create from scratch, acknowledge
that constraint and proceed with the requested path.

## Search Process

### 1. Capture Intent

Extract:

- task the skill or implementation should perform
- trigger conditions
- target audience and platform
- frameworks, tools, data sources, or side effects involved
- three to five keywords plus synonyms
- constraints that disqualify candidates

### 2. Search Local Sources First

Prefer local sources because they already match the user's environment:

- current repo skills and commands
- hidden or internal skill directories
- existing rules, agent docs, and memory files
- package manifests and existing dependencies
- similar modules, tests, and helpers in the active codebase

For code work, find at least three real examples in the repo before writing a
new pattern. If fewer than three exist, call out that the change introduces a
new pattern.

### 3. Search External Sources

Use only relevant channels:

- package registries for the active language
- GitHub repositories and code search
- official framework documentation
- public skill marketplaces or skill repos
- web search for current ecosystem guidance

If a search channel is unavailable, state that limitation instead of claiming
coverage.

### 4. Vet Candidates

For each serious candidate, check:

- license and attribution requirements
- maintenance activity and issue health
- dependency size and security posture
- side effects, shell commands, credential handling, and install scripts
- fit with local repo conventions
- whether wrapping is simpler than copying

Prefer rewriting external skills into local standards instead of importing them
verbatim when frontmatter, tooling assumptions, or workflow boundaries differ.

### 5. Decide

| Signal | Decision |
| --- | --- |
| Exact local match | Use existing |
| Local match with small gap | Extend or merge |
| Good external match with compatible license | Rewrite or fork with attribution |
| Package solves the core need | Adopt package and add thin integration |
| Multiple partial matches | Compose the smallest useful set |
| No good match | Create fresh skill or implementation |

## Ranking Output

Return a compact table:

| Rank | Candidate | Source | Fit | Gap/Risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| 1 | `skill-auditor` | local | Portfolio audit exists | No compliance scenarios | Extend |

Then state the decision:

```text
Recommendation: rewrite `agent-architecture-audit` as a new platform-neutral
skill. It covers a real gap, the license allows reuse, and local skills only
cover general debugging/evaluation.
```

## Skill Import Rules

When importing or rewriting skills into this repo:

- Follow the Agent Skills spec and local standards.
- Put `version` and `tags` inside `metadata`.
- Add `plugin.json`.
- Keep platform-specific fields out unless this repo explicitly supports them.
- Keep `SKILL.md` under 500 lines; move detailed examples to references.
- Run README sync and validation after adding, removing, or renaming skills.
- Attribute external sources when reusing substantial content or scripts.

## Anti-Patterns

- Creating a new skill before checking local overlap.
- Installing or importing an external skill without reading it.
- Returning a long unranked list of weak matches.
- Treating a web-only mention as trusted source material.
- Copying an external skill that depends on another platform's hooks, commands,
  or private paths without rewriting the contract.
