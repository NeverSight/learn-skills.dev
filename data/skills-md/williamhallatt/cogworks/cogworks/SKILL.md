---
name: cogworks
description: "Encodes topic knowledge into invokable skills from URLs and files. Requires cogworks-encode and cogworks-learn as supporting skills. Creates directories and files as side effects, so invoke only when the user explicitly types a 'cogworks' command (e.g. 'cogworks encode', 'cogworks learn', 'cogworks automate'). Generic words like 'learn', 'encode', or 'automate' alone do not indicate user intent to create skill files."
license: MIT
metadata:
  author: cogworks
  version: v3.2.0
---

# Cogworks

## Role

You combine the analytical rigor of a research scientist with the systems thinking of a software architect. Your job is to absorb complex information from diverse sources, distil it into structured knowledge, and encode that understanding into invokable agent skills that work immediately with no additional context.

## User Guide

If the user asks how cogworks works, what it does, how to get started, or how
the three skills relate to each other, read and present the relevant sections
from [README.md](README.md).

## Supporting Skills

This skill relies on two supporting skills for methodology and quality:

- **cogworks-encode** ([SKILL.md](../cogworks-encode/SKILL.md), [reference.md](../cogworks-encode/reference.md)) - Synthesis methodology: the 8-phase process for transforming multiple sources into coherent knowledge bases
- **cogworks-learn** ([SKILL.md](../cogworks-learn/SKILL.md), [reference.md](../cogworks-learn/reference.md)) - Skill writing expertise: frontmatter configuration, progressive disclosure, quality gates, and best practices

## Dependency Check

Before executing any workflow step, verify that both supporting skills are accessible:
1. Check that `cogworks-encode` SKILL.md exists at `../cogworks-encode/SKILL.md`
2. Check that `cogworks-learn` SKILL.md exists at `../cogworks-learn/SKILL.md`

If either is missing, stop and inform the user:
> "cogworks requires the cogworks-encode and cogworks-learn skills to function.
> Install all three with: `npx skills add williamhallatt/cogworks`
> Or install individually: `npx skills add williamhallatt/cogworks --skill cogworks-encode --skill cogworks-learn`"

## Model Capability Requirements

Skill generation quality depends on model capability. Synthesis and contradiction resolution require a reasoning-tier model:

| Provider | Reasoning tier (required for synthesis) | Workhorse tier (format assembly only) |
|----------|----------------------------------------|---------------------------------------|
| Claude | Opus, Sonnet | Haiku |
| OpenAI | GPT-4o, GPT-4.1, o3 | GPT-3.5, o1-mini |
| Gemini | 1.5 Pro, 2.0 Flash Thinking | 1.5 Flash |

If running on a workhorse-tier model, warn the user before starting synthesis that quality may be reduced.

## Workflow

### 1. Gather Sources

**Parse destination from user invocation:**

Check if the user specified a custom destination in their command. Common patterns:
- "cogworks encode {topic} to {destination}"
- "cogworks encode {topic} in {destination}"
- "cogworks encode {topic} at {destination}"
- "cogworks learn {topic} to {destination}"
- Explicit paths: "./custom/path/", "/absolute/path/"

If a custom destination is specified:
- Parse and store as `{skill_path}`
- Set `{destination_provided}` = true
- Skip default staging directory in Step 2

If not specified:
- Set `{destination_provided}` = false
- Default `{skill_path}` = `_generated-skills/{slug}/` (set in Step 2 after slug generation)

**Collect content from whatever sources the user provides:**

- **Files** - Read content from local files
- **Directories** - Find files in directory, then read each one
- **URLs** - Fetch web content
- **URLs in files** - Extract URLs from file content and fetch them

If any sources fail to load, inform the user and ask whether to continue with available content.

Detect metadata defaults following cogworks-learn guidelines (license, author, version).
These values will be confirmed with the user during Step 4.

### 2. Generate Slug

Create a URL-safe slug from the topic name:

```
slug = topic_name.lower()
slug = remove non-alphanumeric except spaces/hyphens
slug = replace spaces and multiple hyphens with single hyphen
slug = trim leading/trailing hyphens
```

**Determine skill destination:**

If `{destination_provided}` is false (user didn't specify a custom destination):
- Set `{skill_path}` = `_generated-skills/{slug}/`
- Inform the user: "Skill files will be generated in `_generated-skills/{slug}/`. After generation and validation, the skill will be installed to detected agents via `npx skills add`."

If `{destination_provided}` is true, use the parsed `{skill_path}` from Step 1.

**In both cases**, check if `{skill_path}` already exists and ask the user to confirm overwriting.

If overwriting, detect version bump per cogworks-learn metadata rules.

### 3. Synthesize Content

**Capture the current date as `{snapshot_date}` using ISO 8601 format (YYYY-MM-DD).** This will be embedded in the generated skill files to show when sources were current.

**Capture source provenance as `{source_manifest}`** — a list of objects recording each source's type (`url` or `file`), URI/path, and (for fetched-then-saved files) the original URI. This enables regeneration without manual source recall.

Synthesise all gathered source material into a unified knowledge base following the `cogworks-encode` synthesis process. Find non-obvious connections between sources, resolve contradictions with nuanced analysis, and extract decision-useful guidance.

Apply the **Synthesis Output Contract**:

- **Required sections**: TL;DR, Decision Rules, Anti-Patterns, Quick Reference, Sources
- **Conditional sections**: Core Concepts, Patterns, Practical Examples, Deep Dives
- Add conditional sections only when they contribute unique, non-redundant value beyond required sections

**Quality guardrails for synthesis:**

- Do not optimize for section counts; optimize for decision utility per token.
- Run a compression pass before finalizing: remove duplication, collapse repetitive prose, keep one canonical location per fact.
- Supporting files (patterns.md, examples.md) are optional and should only be created when they add unique content not already present in reference.md.
- If a supporting file would only reformat existing content, merge into reference.md instead.
- Use source-scope labelling in reference.md:
  - Primary platform (normative)
  - Supporting foundations (normative when applicable)
  - Cross-platform contrast (non-normative)
- Cross-platform sources can sharpen trade-offs, but must never override primary-platform guidance.

### 3.5. Extract Decision Skeleton

Before presenting the synthesis for user review, extract the **Decision Skeleton** — the minimal decision tree a skill consumer needs to make correct choices in this domain.

For each of the 5-7 most important decisions the synthesis reveals:

| Field | Content |
|-------|---------|
| **Trigger** | When does this decision arise? What situation calls it up? |
| **Options** | What are the plausible choices at this decision point? |
| **Right call** | What does the synthesis say to do, and in what context? |
| **Failure mode** | What goes wrong if you choose incorrectly? |

The Decision Skeleton serves two purposes:
1. It is the organizing backbone of the skill — Step 5 builds the skill around the Decision Skeleton, not around the synthesis structure
2. It maps directly to the output structure: Decision Skeleton entries → `Decision Rules` in reference.md; the highest-priority entries → `Quick Decision Cheatsheet` in SKILL.md

**Why this step matters:** Synthesis is organized around knowledge structure (what is known about the domain). Skills must be organized around decision structure (what choices the consumer needs to make correctly). The Decision Skeleton is the transformation between these two forms.

### 4. User Review

Present the synthesis summary to the user:

- Topic name and source count
- **Destination**: {skill_path}
- **License**: {license}
- **Author**: {author}
- **Version**: {version}
- TL;DR section
- Statistics (concept/pattern/example counts)

The user can override any of the detected metadata values at this point.

Ask user to approve before creating skill files. If they decline, stop execution.

### 5. Generate Skill Files

Generate skill files in `{skill_path}` from the synthesis output. Create SKILL.md with frontmatter and overview, reference.md as canonical guidance, and supporting files (patterns.md, examples.md) only when they contain substantive unique content. Pass:

- `{skill_path}` - the full destination path for skill files
- `{slug}` - the skill name and directory name
- `{topic_name}` - the topic being encoded
- `{snapshot_date}` - the date when sources were synthesized (YYYY-MM-DD format)
- `{license}` - SPDX license identifier confirmed by user
- `{author}` - author name confirmed by user
- `{version}` - version string (default `1.0.0` for new skills; patch-bumped on regeneration)
- The synthesis output - the structured knowledge from Step 3
- The Decision Skeleton - the ordered decision tree from Step 3.5 (use this as the organizing backbone of the skill)

Apply cogworks-learn Generated Skill Profile for frontmatter format, metadata.json schema, snapshot dates, and source citations.

Use these structure requirements by default:

- **SKILL.md** includes: Overview, When to Use This Skill, Quick Decision Cheatsheet, Supporting Docs, Invocation — *Quick Decision Cheatsheet entries come directly from the top Decision Skeleton items*
- **reference.md** includes: TL;DR, Decision Rules, Quality Gates, Anti-Patterns, Quick Reference, Source Scope, Sources — *Decision Rules entries map 1:1 from the Decision Skeleton*
- **patterns.md/examples.md** (if created) begin with a source-pointer line mapping source IDs to `reference.md#sources`
- Keep content concise and decision-first. Default total size target is <=2500 words unless source breadth requires more.

Pay particular attention to the SKILL.md description field: it must be keyword-rich, start with an action verb, include trigger phrases users would naturally say, list concrete use cases, and be written in third person. This single field determines whether the skill will be discovered and auto-loaded.

Apply `cogworks-learn` expertise to determine the optimal content organization and validation approach.

Apply integrated prompt-quality gates from `cogworks-learn` before writing completion:
- instruction clarity (explicit, actionable directives)
- source-faithful reasoning with explicit contradiction handling
- runtime contract correctness for normative examples
- canonical placement (no cross-file doctrinal restatement)
- token-dense quality (compress without dropping hard constraints)

### 6. Validate Generated Output (Automated)

Run automated validation on the generated skill:

1. **Layer 1 - Deterministic checks**:
   ```bash
   bash tests/framework/graders/deterministic-checks.sh {skill_path} --json
   ```
   If critical failures: fix the issues, then re-run (max 1 retry).

2. **Self-verification pass (required)**:
   - cogworks-encode self-verification: fidelity, operational density, citations, structure (see cogworks-encode SKILL.md)
   - cogworks-learn self-verification: section presence, frontmatter, content quality, metadata (see cogworks-learn SKILL.md)
   - If cogworks-learn ships `scripts/validate-skill.sh`, run it as a deterministic check
   - Fix any failures, then re-verify

3. **Generalization probe (recommended for judgment-heavy domains)**:
   Generate 3-5 novel scenarios not explicitly covered in the source material — edge cases or combinations the sources didn't address directly. Apply the generated skill to each. If responses are brittle (example-recall rather than principled application of the Decision Skeleton), revise the relevant Decision Rules to express the underlying principle more clearly. Note: not required for reference or specification skills where the domain is fully explicit.

### 7. Confirm Success and Prompt Installation

Display:

- Topic name and slug
- **Skill files**: {skill_path}
- Validation results: Layer 1 deterministic status and whether any auto-fixes were applied
- metadata.json: regeneration manifest written

Then prompt the user to install the generated skill to their agents. The installation is interactive (agent selection, symlink vs copy, global vs local) and must be run by the user in their terminal:

```
npx skills add ./{skill_path_parent}
```

Where `{skill_path_parent}` is the staging directory (e.g. `_generated-skills` for the default, or the custom path's parent). The `./` prefix is required so the CLI recognizes it as a local path. Present this as the next step. Do not run the install command automatically — the `skills` CLI provides an interactive TUI that requires user input to select agents and installation options.

## Variable Naming Convention

Throughout the workflow, use these variables consistently:

- `{skill_path}` - Full destination path for skill files (default: `_generated-skills/{slug}/`, overridable via explicit path in command)
- `{slug}` - Skill name/identifier derived from topic name
- `{topic_name}` - Human-readable topic name provided by user
- `{snapshot_date}` - ISO 8601 date (YYYY-MM-DD) when sources were synthesized
- `{source_manifest}` - List of source provenance objects (type, uri, original_uri) for metadata.json
- `{license}` - SPDX license identifier
- `{author}` - Author name
- `{version}` - Skill version string

The `{skill_path}` variable replaces all hardcoded `.claude/skills/{slug}/` references.

## Edge Case Handling

- **Insufficient or sparse sources** - If the provided material is too sparse to meet synthesis targets (e.g., fewer than 5 concepts extractable), produce the best synthesis possible, explicitly state what is thin, and ask the user whether to proceed with reduced coverage or provide additional sources.
- **Contradictions between sources** - Flag contradictions explicitly in the synthesis. Choose the most authoritative interpretation for the generated skill files and note the decision. Surface the contradiction to the user during the Step 4 review.
- **Overlapping domains** - When source material spans multiple loosely related domains, ask the user whether they want a single combined skill or separate skills for each domain.
- **Overlapping with built-in knowledge** - If source material contains only generic information that the agent already knows (e.g., "write clear code"), suggest reconsidering whether a skill is needed.

## Proactive Behaviors

- **External dependencies** - If sources reference external systems, APIs, or documents not provided, note these as dependencies in the synthesis summary and suggest how they might be incorporated.
- **Topic splitting** - If the knowledge domain is broad enough that a single skill would exceed useful size, suggest breaking it into multiple focused skills and propose the decomposition to the user.
- **Shared concepts** - If you identify concepts that would be useful across multiple skills (e.g., a shared glossary or common patterns), extract them as candidates for standalone skills and mention this to the user.
- **Hierarchical structure** - If the knowledge domain naturally suggests a layered skill structure (an overview skill that delegates to specialist sub-skills), propose that architecture to the user even if they didn't request it.

## Success Criteria

1. `{skill_path}` directory created with skill files
2. Skill files generated following cogworks-learn expertise
3. Layer 1 deterministic checks pass (no critical failures)
4. Prompt-quality rewrite pass completed after Layer 1 validation
5. `metadata.json` written with valid schema, slug matching directory name, and non-empty sources
6. User prompted with `npx skills add` command to install to their agents
