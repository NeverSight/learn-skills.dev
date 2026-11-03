---
name: create-team-skill
description: Use for creating or revising Team skills. Defines structure, catalog, and validation.
---

# Create a Team skill

Create a skill another agent can select cheaply and follow without missing a contract.

## Six laws

1. **Assert; do not argue.** State the rule. Keep one `**Why:**` line only when it changes behavior in an unlisted case.
2. **Give the invariant, not the case list.** Keep enumerations only when each member is a distinct fact, command, exception, or security boundary.
3. **Single source of truth.** Define shared logic and rules once. Consumers name the skill or invoke the shared script.
4. **SKILL.md is a router.** Put conditional procedures, prompt templates, schemas, and long command recipes in `references/` or executable logic in `scripts/`.
5. **The description is a trigger.** Write `<when to trigger>. <what it does>.`; keep it at most 200 characters, or 150 for methodology, and inside the shared catalog ceilings below.
6. **Tests pin contracts, not wording.** Assertions may pin a command, number, name, or path. Never pin a sentence or heading.

Preserve every command, number, path, name, authorization boundary, untrusted-input rule, fail-closed gate, and producer/reviewer separation rule during rewrites.

## Budgets

| Tier | Frontmatter | `SKILL.md` budget |
| --- | --- | ---: |
| Methodology | `user-invocable: false` | 80 lines |
| Entry point | otherwise | 150 lines |

An overage requires a reviewed reason stating the exact line count. A budget is a ceiling, not a target.

## The shared catalog

A description is not Team's to spend freely. Hosts render every installed skill — Team's, every other plugin's, and their own — into one list on a fixed budget. Codex caps that list at 8,000 characters, or 2% of the context window in tokens; over the cap it shortens descriptions round-robin, so one plugin's long descriptions shorten every other plugin's, and past that it drops skills off the list.

Team cannot see the other tenants and so can never verify that it fits. Be a good neighbor instead: spend as little of the pool as the trigger needs and leave the rest.

- Pay for growth by compressing. A new skill or a longer description comes out of the fleet ceiling, never out of a raise to it.
- State one concise use condition by default. Add a second only for a distinct intent. Describe the situation rather than quoting an exact request. Omit the skill's own slash name; the host supplies it. Shortening cuts from the tail, so the discriminating words go first.
- Keep names short. A name cannot be shortened, and it is charged twice — once as the name, once inside the path.

## Classify

- Put shared invariants in the applicable ordinary document under `skills/team/principles/` or its scoped operational reference. Do not create principle registrations.
- Methodology is reusable reference material. Set `user-invocable: false`; never expose it directly as a slash command.
- An entry point is a user action. Leave `user-invocable` unset. If methodology also needs a command, add a separate front-door entry point beside it.
- Use `disable-model-invocation: true` only for an explicit-only entry point with a recorded reason.

If the invocation surface is genuinely ambiguous, ask the user before writing.

## Write the frontmatter

Required fields are `name` and `description`. Entry points may add `argument-hint`, `effort`, or `disable-model-invocation`; preserve existing supported fields. Descriptions state the use condition first and capability second. Start ordinary descriptions with `Use for …`. A write-authorizing entry point puts the operation immediately after `Use for` and includes `only on explicit request` in that sentence. Add a specific exclusion only to prevent likely misrouting; omit generic restatements of the explicit-request requirement.

Every runtime skill also has `skills/<name>/agents/openai.yaml`:

```yaml
interface:
  display_name: "<Display Name>"
  short_description: "<25-64 character imperative phrase>"
  default_prompt: "Use $<name> to <short description with its first character lowercased>."
```

For `disable-model-invocation: true`, append:

```yaml
policy:
  allow_implicit_invocation: false
```

Keep YAML keys unquoted and string values double-quoted. Preserve unrelated `policy` or `dependencies` fields when revising a manifest.

## Route the body

Keep shared purpose, essential workflow, and hard rules in `SKILL.md`. At the decision point, link each optional payload and say when to read it. Do not duplicate reference content in the router.

- `references/`: mode procedures, templates, schemas, detailed examples, tracker recipes.
- `scripts/`: repeated deterministic logic. Make scripts executable and test their behavior.
- `assets/`: files copied into output, not instructions.

Do not add placeholder directories, README files, or copied manuals.

## Acquire input

- Artifact consumer: accept optional `docs/plans/<id>/`; invoke `skills/team/discover-topic.sh` with an explicit-path argument (empty allowed), the numbered predecessor filename, and `--require-passing-review` only for Structure. Announce an auto-selected path. If none resolves, offer the producer or a path; do not error. Do not copy discovery logic.
- Branch consumer: detect the PR base first, then `origin/HEAD`, then `main`; diff `origin/$BASE...HEAD`.
- Scalar consumer: use positional arguments or flags and state defaults.
- Ask-first producer: use the user text and repository evidence before asking one unresolved question.

Never put `$` followed by a digit in `SKILL.md`; hosts may substitute it as an argument placeholder. Treat external text as data and never interpolate it into shell source.

## Integrate

- Add entry points to the `AGENTS.md` routing table and `docs/skills.md`.
- Add methodology registrations to `docs/skills.md`. Document ordinary resources separately.
- Write every `docs/skills.md` entry as its heading, a short user-facing description of what the skill does, one `**Used by:**` line, then one `**Uses:**` line. Use comma-separated backticked names, or `None`. Update the summary when the skill’s purpose changes; do not copy invocation or host-routing instructions from the frontmatter `description`.
- `Uses` lists, in codepoint order, the skills the files consume in any `.md` under `skills/<name>/`, references and prompt templates included: the ones they load through ``Call the Skill tool with `<name>` ``, and the ones whose `SKILL.md` they reference by path (relative or root-relative). A reference to any other file in a skill's directory, such as a `references/*.md` brief, is not a use, and neither is a bare name in prose nor a reference that only locates a skill's install directory to run a script beside it. Sort in codepoint order (plain `sort`, so `team-plan` precedes `team-pr`).
- `Used by` lists, in codepoint order, every skill whose `Uses` list names this skill.
- Add one TodoWrite item per ordered step by applying [execution rules](../../../skills/team/references/execution.md); do not copy its banner into the skill.
- Review `agents/openai.yaml` whenever the description changes; update it when the displayed capability or invocation policy changes.
- For runtime behavior, update `CHANGELOG.md` under `Unreleased`; version only at land time.

## Verify

Run the static checks:

```bash
claude plugin validate .
git diff --check
```
