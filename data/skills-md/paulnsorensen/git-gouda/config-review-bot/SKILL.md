---
name: config-review-bot
description: >
  Audit or configure CodeRabbit repository review policy from effective sources.
  Use for CodeRabbit setup, configuration review, path coverage, or a specific
  pull-request review audit. Trigger on "configure CodeRabbit", "review
  .coderabbit.yaml", "set up CodeRabbit", "audit CodeRabbit settings", or "is
  CodeRabbit covering X". Keep audits read-only by default and separate schema
  validity, rule quality, and completed-review evidence. Do not use it to run a
  CodeRabbit CLI review or autofix, or to fix review comments on a pull request.
license: MIT
---

# config-review-bot

Audit or configure CodeRabbit for this repository.

**Iron Law:** no configuration claim or edit is valid without current evidence for its scope and effective behavior.

## Scope

This skill covers repository-local CodeRabbit configuration. It does not install the CodeRabbit app or CLI, start a paid review, post comments, change branch protection or rulesets, or configure another review bot. Setup changes need explicit authorization.

## Inputs

The request names the mode: `audit [PR <n>]`, `set up`, or `update <change>`. A bare invocation is an audit of the current repository.

1. Read the repository instructions. Read the repository wiki when one exists; do not require one.
2. When the request names a pull request, record its exact head SHA and base branch before making claims.
3. Read `.coderabbit.yaml`, repository settings, and evidence of inherited organization or workspace configuration.
4. Read the build, test, and CI configuration that defines repository behavior.
5. Take the main branch, the language, and the path layout from evidence, not assumption.
6. Preserve explicit user decisions about scope, severity, presets, branches, and enforcement.
7. Read the current official CodeRabbit documentation. Treat every default as dated and confirm it there.

Done when: the effective configuration source is named as file, inherited, UI, or **unknown**, and the pull-request head and base are recorded when a pull request is in scope.

## Audit

Audit mode is read-only. Report three claims separately: schema validity, rule quality, and evidence that a review completed.

### Schema validity

1. Prefer `coderabbit config validate <path>` when `--help` confirms the command.
2. Confirm command and option names against CLI help and the current CLI reference first.
3. Else validate against the official JSON Schema with the YAML tooling that the repository already uses.
4. Report **valid** only when a supported validator succeeds. Report **cannot validate** when no validator or schema evidence exists.
5. Audit with the tools already installed. A CLI installation is a setup change, not an audit step.

Done when: the verdict is `valid`, `invalid: <error>`, or `cannot validate: <reason>`.

### Rule quality

| Check | Evidence to gather |
|---|---|
| Feedback vs enforcement | `reviews.profile` sets feedback volume. `request_changes_workflow` and branch protection set merge semantics. Report them separately. |
| Branch scope | `base_branches` is a regex list that adds to the default branch. Confirm this against current documentation. |
| Review cadence | Incremental, draft, auto-pause, and rate-limit defaults from current documentation. |
| Path coverage | Test `path_instructions` and `path_filters` globs against actual tracked names. Include dotfiles, hidden asset directories, extensionless scripts, templates, and POSIX, Bash, and zsh dialects. |
| Test files | Language-specific test files map to the real test commands of the project. |
| Guidelines | Code-guideline auto-discovery, its actual scope, explicit mappings, and UI state. A discovered instruction applies only where its scope is documented or observed. |
| Signal policy | Style-only consistency findings are suppressed. Security and correctness findings stay on. |
| Duplication | Targeted rules do not repeat existing guidelines, formatters, linters, or CI checks. |
| Fixtures | Golden expectations stay reviewable. Disposable generated noise is excluded. |
| Excludes | Report default excludes separately from excludes that this repository added. |

Use CodeRabbit minimatch semantics for path checks, not a schema-only inference. Propose a preset migration only with comparative evidence from this repository.

Done when: every row has a finding or an explicit `no gap` with its evidence.

### Review completion

A green status check is a different claim from a completed review. Verify review events, findings, and the exact pull-request head SHA before you report that a review ran.

## Setup or update

1. Show the smallest repository-local configuration diff that meets the request.
2. Validate the diff with the preferred validator, or report why validation is unavailable.
3. Change only the configuration that the user requested. A wholesale template is never the answer.
4. Recheck the final diff against the explicit decisions of the user.

An ordinary configuration request ends at the diff. Each of these actions needs an explicit user request: posting comments, triggering paid reviews, changing branch protection or rulesets, removing Copilot review configuration, installing services or CLIs, committing, and pushing.

Done when: the diff is shown, its validation verdict is stated, and every line traces to the request.

## Configuration shape

Use the official schema at <https://coderabbit.ai/integrations/schema.v2.json>. Keep configuration small:

- `reviews.profile` controls feedback volume. It does not enforce merge policy.
- `reviews.path_instructions` uses entries shaped as `{path, instructions}` with repository-relative minimatch patterns.
- Test representative tracked names, including `skills/**/SKILL.md`, `skills/**/assets/**`, `skills/**/references/**`, `skills/**/evals/**`, and `.github/**`.

## Safety rules

- Audit and explain before editing.
- Never add credentials or tokens.
- Never infer effective UI or inherited settings when they are unavailable. Report the evidence gap.
- Never claim schema validity, path coverage, or review completion from another result.
- Never imply that a review ran from `.coderabbit.yaml` or a status check alone.
- Ask before changing an existing policy that differs from the request.

## Red flags

Stop and investigate when:

- a green status is treated as proof that a review completed;
- a schema pass is treated as proof of path or guideline coverage;
- a discovered instruction is applied outside its documented or observed scope;
- a profile level is treated as merge enforcement without workflow and branch-rule evidence;
- a setup request grows into comments, paid reviews, branch rules, installations, or commits;
- a repository-wide preset migration appears without comparative evidence.

| Rationalization | Why it fails | Required action |
| --- | --- | --- |
| "The check is green, so CodeRabbit completed its review." | Status checks and completed-review evidence are different claims. | Verify review events, findings, and the exact pull-request head. |
| "The schema is valid, so coverage is adequate." | Syntax constraints do not prove path or guideline coverage. | Test representative tracked paths and report gaps. |
| "The old bot is retired, so its guidance is inactive." | Guidance can remain in files, inherited settings, or UI state. | Search sources and effective settings before you remove or ignore it. |

## Output

```markdown
## CodeRabbit <audit | setup>: <repo> [PR <n> @ <head-sha>]

- Schema: valid | invalid: <error> | cannot validate: <reason>
- Effective config source: file | inherited | UI | unknown
- Review completion (PR only): verified @ <sha> | not verified: <reason>

| # | Severity | Confidence | Check | Location | Finding | Recommendation |
|---|---|---|---|---|---|---|

### Evidence gaps
- <what was not checkable and why>

### Proposed diff (setup only)
```

Severity: blocker, high, medium, low. Confidence: `certain` for a cited file, document, or pull-request event; `speculative` for a checkable but unverified claim. Drop claims with no evidence.

## Inline example

```yaml
reviews:
  profile: chill
  path_instructions:
    - path: "skills/**/SKILL.md"
      instructions: "Check portability, scope, and resource references."
```

## Worked invocations

```text
/config-review-bot audit PR 123 at the exact head and base; report findings only
/config-review-bot set up CodeRabbit for this repository; propose and validate only the requested config changes
```

## Resources

- [CodeRabbit configuration reference](https://docs.coderabbit.ai/reference/configuration)
- [CodeRabbit path instructions](https://docs.coderabbit.ai/configuration/path-instructions)
- [CodeRabbit schema](https://coderabbit.ai/integrations/schema.v2.json)
- [Code guidelines](https://docs.coderabbit.ai/knowledge-base/code-guidelines)
- [Auto review and rate limits](https://docs.coderabbit.ai/configuration/auto-review)
- [CLI reference](https://docs.coderabbit.ai/cli/reference)
- [Request changes workflow](https://docs.coderabbit.ai/pr-reviews/request-changes-workflow)
- [Official CodeRabbit CLI skills, distinct from this configuration skill](https://github.com/coderabbitai/skills)
