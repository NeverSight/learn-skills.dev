---
name: agent-skills
description: >-
  Use this skill when creating, reviewing, or editing Agent Skills-format skills,
  or when implementing skill discovery and loading in an agent client. It covers
  directory structure, SKILL.md metadata, progressive disclosure, evals, and
  repository conventions. Do not use this skill for general software work that
  does not involve the Agent Skills format or lifecycle.
license: MIT
---

# Agent Skills Standard Reference

This skill documents the [Agent Skills](https://agentskills.io) open format — a standardized way to give AI agents new capabilities and expertise. **Follow this workflow when creating or editing skills in this repository.**

> Authoritative source: [agentskills.io/specification](https://agentskills.io/specification). The bundled specification is a working snapshot; check the authoritative source when currentness matters.

---

## Directory Structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── evals/            # Required for new skills in this repository
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

## Required Workflow

### Create or edit a skill

1. Read [the specification](references/specification.md) before changing `SKILL.md` metadata or directory structure.
2. Ground instructions in real domain knowledge, project artifacts, and observed failure modes. Read [best practices](references/best-practices.md) when designing or materially revising instructions.
3. Keep the skill a coherent, triggerable unit. Put only essential instructions in `SKILL.md`; put conditional detail in focused reference files and state exactly when to read each one.
4. Use a precise `description` that says what the skill does, when it applies, and when it does **not** apply. For skills with meaningful overlap, name the nearest alternative or prerequisite in a `## When not to use` section. Test the boundary with at least three should-trigger prompts and two should-not-trigger near-misses; keep these harness-specific trigger checks separate from portable output-quality evals. Read [optimizing descriptions](references/optimizing-descriptions.md) for trigger design.
5. For every new skill, create `evals/evals.json` with at least five representative output-quality cases. Each case needs a realistic prompt, an expected outcome, and observable assertions. Include edge cases that exercise risky or ambiguous behavior. Read [evaluating skills](references/evaluating-skills.md) for the eval format and iteration workflow.
6. When bundling executable code, read [using scripts](references/using-scripts.md). Document prerequisites and non-interactive invocation in the skill.
7. Before handoff, run the validation checks in this skill and correct every finding.

### Review a skill

1. Validate the required frontmatter, field constraints, parent-directory/name match, and YAML syntax against [the specification](references/specification.md).
2. Check that the description has both positive and negative trigger boundaries, the workflow is actionable, and resource references are conditional and reachable.
3. Check that any script has documented dependencies, safe non-interactive inputs, clear errors, and structured output where useful.
4. For this repository, also verify its required human-facing `README.md`: title, **Why Install This Skill**, **What You Get**, **Quick Start** (unless genuinely reference-only), **Triggers**, and **Requirements**. Keep it human-facing, concise, and free of agent-only instructions.
5. Verify every new skill has `evals/evals.json` with at least five output-quality cases, and check that their expected outcomes and assertions test meaningful behavior. For an existing skill without evals, flag the gap but do not block the review solely for that legacy absence. Read [evaluating skills](references/evaluating-skills.md) before declaring the work complete.

### Client implementation work

When implementing skill discovery, activation, or context management in an agent product, read [client implementation guidance](references/client-implementation.md). Do not apply client conventions such as search paths as universal format requirements.

## SKILL.md Format

The `SKILL.md` file must contain YAML frontmatter followed by Markdown body content.

### Frontmatter Fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen. **Must match the parent directory name.** |
| `description` | Yes | Max 1024 chars. Non-empty. Describes what the skill does and when to use it. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Indicates environment requirements. |
| `metadata` | No | Arbitrary key-value mapping. |
| `allowed-tools` | No | Space-separated string of pre-approved tools. (Experimental) |

#### `name` field rules
- 1–64 characters
- Only lowercase unicode alphanumeric (`a-z`, `0-9`) and hyphens (`-`)
- Must not start or end with a hyphen
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name

#### `description` field rules
- 1–1024 characters
- Should describe both **what** the skill does and **when** to use it
- Should include specific keywords that help agents identify relevant tasks

#### `compatibility` field rules
- If present, it must be 1–500 characters
- Include it only for concrete environment requirements, such as a required product, system package, network access, or runtime

#### `metadata` field rules
- Must be a map of string keys to string values
- Use reasonably unique keys to avoid collisions with other clients or tools

### Body Content

The Markdown body has no format restrictions beyond being helpful to the agent. Recommended sections:

- **Step-by-step instructions** — the procedure the agent should follow
- **Examples of inputs and outputs** — what data looks like going in and coming out
- **Common edge cases** — situations the agent might not handle correctly without guidance
- **Gotchas** — environment-specific facts that defy reasonable assumptions

Keep `SKILL.md` under **500 lines and 5000 tokens**. Move detailed reference material to separate files in `references/`.

## Progressive Disclosure

Agents load skills in three stages:

1. **Metadata** (~100 tokens): `name` and `description` loaded at startup for all skills
2. **Instructions** (< 5000 tokens recommended): Full `SKILL.md` loaded when activated
3. **Resources** (as needed): Files in `scripts/`, `references/`, `assets/` loaded on demand

## Supporting Directories

### `scripts/`
Executable code agents can run. Scripts should:
- Be self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully
- Use relative paths from the skill root (e.g., `scripts/extract.py`)
- Be explicit about intent: say "run this script" or "read this as reference" — never leave the agent to guess whether a bundled file is executable or illustrative

### `references/`
Additional documentation loaded on demand. Keep individual files focused — agents load these when instructed, so smaller files save context.

- Every file under `references/` must be at or under **60,000 characters**. When a reference grows past the cap, split it into focused files (e.g., `references/<topic>-a.md`, `references/<topic>-b.md`) and update `SKILL.md` so each new file is reachable and the load-on-demand instructions name the right file.

### `assets/`
Static resources: templates, images, data files, schemas.

### `evals/`
Portable output-quality cases for the skill. New skills in this repository must include `evals/evals.json` with at least five cases; trigger-only checks belong in the harness-specific test set instead of this file.

## File References

Use **relative paths from the skill root** when referencing other files:

```markdown
See [the specification](references/specification.md) for details.

Run a bundled script:
scripts/<script-name>
```

Keep file references one level deep from `SKILL.md`. Avoid deeply nested reference chains.

## Writing Effective Descriptions

The `description` field is the primary mechanism for automatic skill selection. Clients can also support explicit activation. Follow these principles:

- **Use imperative phrasing.** "Use this skill when..." rather than "This skill does..."
- **Focus on user intent, not implementation.** Describe what the user is trying to achieve.
- **Err on the side of being pushy.** Explicitly list contexts where the skill applies.
- **Keep it concise.** A few sentences to a short paragraph is right.

## Best Practices

### Start from real expertise
Feed domain-specific context into skill creation. Skills grounded in real project artifacts (runbooks, API specs, code review comments, actual failure cases) outperform ones synthesized from generic knowledge.

### Spend context wisely
Focus on what the agent wouldn't know without the skill: project-specific conventions, domain-specific procedures, non-obvious edge cases. Don't explain general concepts the agent already knows.

### Calibrate control
- **Give freedom** when multiple approaches are valid — describe *why*, not just *what*
- **Be prescriptive** when operations are fragile or a specific sequence must be followed
- **Match prescriptiveness to fragility**: for a step that must be exactly right every time, prefer a deterministic script in `scripts/` over instructions the agent improvises on each run. A test only catches what you already thought to check; a script takes the guess out of the loop entirely
- **Provide defaults, not menus** — pick one approach, mention alternatives briefly
- **Favor procedures over declarations** — teach *how to approach* a class of problems, not *what to produce* for one instance

### Design coherent units
Scope skills like functions: one coherent unit of work that composes well with other skills. Too narrow → multiple skills needed for one task. Too broad → hard to activate precisely.

### Use gotchas sections
The highest-value content is often environment-specific corrections — things the agent will get wrong unless told otherwise. When an agent makes a mistake, add the correction to the gotchas section.

### Provide output templates
When output needs a specific format, provide a template inline or in `assets/`. Agents pattern-match well against concrete structures.

## Adopting Third-Party Skills

Skills are executable capability: when a skill activates, its instructions and scripts run with the agent's permissions — shell access, file system, and credentials. Before running a skill you did not author (from a registry, a colleague, or an LLM generation), read [vetting third-party skills](references/vetting-third-party-skills.md) and treat it like any other dependency: inspect provenance, read the body and every script, and check what the skill reaches out to.

## Validation

Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) reference library to validate skills:

```bash
skills-ref validate ./my-skill
```

This checks that `SKILL.md` frontmatter is valid and follows all naming conventions.

For this repository, also run the bundled whole-repository checker:

```bash
ruby scripts/validate-skills.rb
```

It checks canonical top-level and bundle skills for frontmatter, supported fields, line limits, local links, and required README sections. Vendored profile skills under `agent-council/profiles/skills/` are intentionally excluded because they follow the source repository's conventions.

If `skills-ref` is unavailable, do not claim a successful validator run. Perform and report the equivalent structural checks manually, or install and run the reference validator when the task permits it.
