---
name: skill-authoring
description: Use when authoring, creating, refining, or troubleshooting agent skills — scaffold SKILL.md and frontmatter, write and optimize the trigger description, structure the body with progressive disclosure, validate structure, and test or debug activation. Also when building a new skill from scratch, when a skill won't trigger, loads incorrectly, or the agent ignores it entirely. Use when a skill misbehaved in the current session and needs adjustment based on learnings.
---

# Skill Authoring

Use this as the working playbook for skill creation and maintenance. Start by choosing the job below. Load only the files needed for that job.

Done means the skill loads for the right requests, gives clear instructions without bloating context, and records source evidence when domain accuracy matters.

Agents see `name` and `description` before they see the body. The body loads only after the description matches the task. References, scripts, and assets load only when needed. Write for that loading order.

## Choose the Job

| Job | Read first | Then use when needed |
|-----|------------|----------------------|
| Create a small skill from scratch | [workflows/create.md](workflows/create.md) | [templates/simple.md](templates/simple.md), [templates/router.md](templates/router.md), [references/patterns.md](references/patterns.md) |
| Build or update a skill from docs, project history, examples, failures, or multiple sources | [workflows/synthesize.md](workflows/synthesize.md) | [README.md](README.md), [references/examples.md](references/examples.md) |
| Review or audit an existing skill | [references/rules.md](references/rules.md) | [references/examples.md](references/examples.md), [spec/specification.md](spec/specification.md) |
| Check whether a skill activates and behaves correctly | [workflows/test.md](workflows/test.md) | [workflows/debug.md](workflows/debug.md) when activation fails |
| Diagnose a skill that will not trigger or is ignored | [workflows/debug.md](workflows/debug.md) | [spec/specification.md](spec/specification.md), [references/rules.md](references/rules.md) |
| Improve a skill from a concrete session failure | [workflows/refine.md](workflows/refine.md) | [references/rules.md](references/rules.md), [workflows/test.md](workflows/test.md) |
| Verify format constraints | [spec/specification.md](spec/specification.md) | [Tooling](#tooling) |

## Fast Path

For a localized edit, do not ritualize it:

1. Inspect the skill and nearby conventions.
2. Edit the smallest thing that fixes the issue.
3. Validate structure and, when relevant, activation behavior.
4. Report what changed and what remains uncertain.

Use the workflow files for new skills, source synthesis, debugging, testing, or any change that touches the skill's shape.

## Cardinal Rules

| Rule | Why It Matters |
|------|----------------|
| Description has trigger keywords | Without them, the skill never activates |
| Description names capabilities and activation conditions, not steps | Agents may follow description shortcuts instead of loading the body |
| Description uses third person | It is injected as metadata, not spoken by the agent |
| Name matches directory | Required for skill loading |
| Critical instructions appear early | Long content may be skipped or deemphasized |
| `SKILL.md` stays lean | Runtime context is limited |
| References are directly linked from `SKILL.md` | Hidden chains are easy to miss |
| Source-backed guidance beats vibes | Real docs, history, fixes, and failures improve accuracy |
| Precision before addition | More files and prose often reduce reliability |
| Test activation before deployment | A skill that works but never triggers has zero value |
| Use agent-agnostic language by default | Skills should port across LLM agents unless intentionally provider-specific |

For the full impact-ranked rule list, read [references/rules.md](references/rules.md) when reviewing, auditing, or tightening a skill.

## Skill Shape

```
skill-name/
├── SKILL.md              # Required entry point
├── README.md             # Optional maintainer context for synthesized or complex skills
├── references/           # Optional focused docs loaded on demand
├── scripts/              # Optional executable helpers
└── assets/               # Optional templates, schemas, images, static files
```

Use this placement model:

| Content | Put it in |
|---------|-----------|
| Frontmatter and core instructions | `SKILL.md` |
| Detailed optional guidance the agent may need | `references/*.md` |
| Deterministic repeatable operations | `scripts/*` |
| Templates, schemas, static examples | `assets/*` |
| Source inventory, trust level, decisions, gaps, changelog | `README.md` |

Provenance belongs in `README.md` unless the agent needs it to perform the task.

## Description Requirements

The description decides whether the skill ever loads. Write it for discovery.

Use this formula:

```yaml
description: Use when [triggering conditions] — [specific capabilities]. Handles [file types, contexts, symptoms, synonyms].
```

Good:

```yaml
description: Use when working with PDF files — extracts text, fills forms, merges documents. Handles .pdf files, scanned PDFs, and form fields.
```

Bad:

```yaml
description: Processes PDFs by first extracting text, then analyzing structure, then outputting results.
```

Include:

- words users actually say
- file types and extensions
- error messages or symptoms
- synonyms and alternate phrasings
- negative/positive trigger distinctions when false positives matter

Exclude:

- step-by-step workflow summaries
- implementation details
- first-person language
- generic claims like "helps with documents"

## Writing SKILL.md Bodies

Write for an agent that can already reason. Do not teach basics. Provide the facts, constraints, examples, and checks that change behavior.

Use this shape by default:

1. **Choose**: identify the mode, path, or workflow quickly.
2. **Do**: give imperative steps and decision points.
3. **Show**: include one excellent concrete example or template.
4. **Guard**: call out common mistakes, rationalizations, false positives, or edge cases.
5. **Check**: name the validation command, evidence, or expected result.

Prefer tables, checklists, templates, and input/output examples over explanatory prose.

## Progressive Disclosure

| Layer | What | When Loaded | Target |
|-------|------|-------------|--------|
| 1 | `name` + `description` | Always | Trigger-rich, concise |
| 2 | `SKILL.md` body | When skill triggers | Path choice + core rules |
| 3 | `references/`, `scripts/`, `assets/` | On demand | Focused leaves with direct reasons |

Split content when:

- `SKILL.md` is becoming an encyclopedia
- guidance is optional or domain-specific
- a reference has a clear "open when..." reason
- scripts can make a fragile task deterministic

Do not split content just to look organized.

## Tooling

Script paths are relative to this skill directory.

Scaffold a skill:

```bash
python scripts/init.py my-skill
python scripts/init.py my-skill --router  # for skills that route between sub-workflows
```

Validate a skill:

```bash
./scripts/validate.sh path/to/skill
```

Or use the official validator:

```bash
pip install skills-ref
skills-ref validate path/to/skill
```

Validation checks structure. It does not prove description quality, source coverage, or behavioral reliability.

## Source Material

Vendored authoring approaches live under `sources/` for deeper study. For this skill's source inventory, synthesis decisions, and gaps, read [README.md](README.md).

## Report Back

When modifying or reviewing a skill, report:

1. Summary
2. Changes made or findings
3. Validation results
4. Open gaps
