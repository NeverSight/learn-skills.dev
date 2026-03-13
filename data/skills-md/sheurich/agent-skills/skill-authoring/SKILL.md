---
name: skill-authoring
description: Write and refine agent skills. Use when creating, editing, or reviewing skills, or when asking about SKILL.md format, frontmatter fields, progressive disclosure, or cross-agent distribution.
---

# Skill Authoring

TDD for agent instructions. Test, write, shorten.

## Decide Whether to Create

Create a skill when:

- The technique isn't obvious to agents
- The pattern applies across projects
- You'd reference it again in future sessions

Don't create skills for one-off solutions, standard practices, or
constraints enforceable with automation.

## What to Include

Only instructions that change agent behavior in ways the codebase
can't convey on its own.

| Keep | Cut |
|------|-----|
| Specific tooling (`use uv`, `run shellcheck`) | Motivational framing |
| Concrete constraints (paths, commands) | Rationalization tables |
| Checklists and decision tables | Narrative examples |
| Error messages and stop conditions | Mandatory gates |
| Cross-references to other skills | Overviews and directory listings |

## Write the Description

The description is the activation trigger. Include WHAT and WHEN.
Describe triggering conditions only — not the skill's workflow.

```yaml
# Good — triggering conditions
description: >-
  Create git commits with intelligent file grouping.
  Use when committing changes.

# Bad — summarizes workflow (agents follow this instead of reading the skill)
description: >-
  Use when committing - groups files by concern, writes
  conventional messages, runs pre-commit hooks
```

## Size Budget

Context window is shared. Every paragraph must justify its cost.

| Scope | Target |
|-------|--------|
| Frequently-loaded skills | <200 lines |
| Standard skills | <500 lines |
| Reference material | `references/` directory |

Prefer `--help` over documenting flags. Cross-reference other skills
instead of repeating content. One good example beats many mediocre ones.

## Structure for Progressive Disclosure

```text
skills/skill-name/
├── SKILL.md         # Core instructions (loaded on activation)
├── references/      # Heavy content (loaded on demand)
├── scripts/         # Deterministic operations (executed, not read)
└── assets/          # Templates, images (used in output, never loaded)
```

At startup, agents see only name + description (~100 tokens).
On activation, SKILL.md loads. References and scripts load only
when the agent needs them during execution.

### When to split to `references/`

Split by content type, not just length:

| Content type | Where | Example |
|--------------|-------|---------|
| Workflow and decisions | SKILL.md | "If drift detected, choose…" |
| Lookup tables | `references/` | Backend config per cloud provider |
| Platform-specific details | `references/` | Installation commands per agent |
| API specs or field lists | `references/` | Frontmatter field reference |

**Heuristic:** If the skill covers 3+ independent subtopics and an
agent only needs one at a time, each belongs in a reference file.
SKILL.md routes to the right one.

Don't wait until you hit 500 lines. A 200-line SKILL.md with three
unrelated lookup tables is already a candidate for splitting.

## TDD Cycle

### RED — Baseline

Run a pressure scenario without the skill. Record what the agent
did and where it went wrong.

### GREEN — Write Minimal Skill

Address the specific failures from RED. Don't add content for
hypothetical cases. Re-run — the agent should now comply.

### REFACTOR — Shorten

If the agent still fails, the instruction isn't clear enough —
rewrite it shorter, not longer. A clear 3-line instruction
outperforms a 30-line version. Cut until compliance breaks,
then restore the last cut.

## Match Specificity to Risk

| Freedom | When | Format |
|---------|------|--------|
| High | Multiple valid approaches | Prose |
| Medium | Preferred pattern, variation OK | Pseudocode |
| Low | Fragile ops, must be consistent | Scripts |

## Anti-Patterns

- Workflow summaries in descriptions (agents follow the summary
  instead of reading the full skill)
- "When to use" in body instead of description
- Rationalization scaffolding and authority appeals
- Mandatory gates (`<HARD-GATE>`, "MUST use before ANY...")
- README.md in plugin root (not loaded into agent context)
- Nesting skills under `skills/<plugin>/<skill>/` (not discovered)

## Reference

- [format-spec.md](references/format-spec.md) — frontmatter fields,
  directory patterns, naming rules, external tool conventions
- [platform-guide.md](references/platform-guide.md) — what each
  platform discovers, loads, and ignores
