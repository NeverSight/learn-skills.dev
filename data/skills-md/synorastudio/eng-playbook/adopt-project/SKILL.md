---
name: adopt-project
description: "Audit an existing repo and apply an approved Agent Operating System proposal."
disable-model-invocation: true
---

# Adopt a project

Bring an existing repository into alignment with the current applicable Engineering Conventions without overwriting its real constraints and established practices.

Audit first. Propose changes next. Write only after the user approves the proposal or revises it. Translate convention outcomes into project-owned guidance and Project Guardrails instead of copying central playbook prose. Leave package installation, framework choice, app tooling, and stack defaults outside this workflow.

## Adoption principle

Let the project's operating reality determine its Agent Operating System.

Project Adoption may produce a full Agent Operating System or a thin docs update. Create durable docs only when future agents need them to operate safely.

Running this workflow again is re-adoption. Audit the repository as it exists now; do not require or create a playbook version marker, installed-skill list, or machine-readable adoption manifest.

## Convention baseline

Audit for these outcomes while staying tech-agnostic:

- Repository reality is discoverable through a short Agent Guidance entry point and its linked sources.
- Durable knowledge is current and lives in its owning artifact.
- System boundaries are discoverable, with qualifying architecture trade-offs preserved in ADRs.
- Production work begins from accepted scope and produces proportionate verification evidence.
- Applicable conventions are backed by project-owned controls that prevent violations or make them visible.
- Every commit entering integration history follows `<type>[optional scope][!]: <description>` with an allowed type: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `style`, or `revert`. Descriptions are imperative, lowercase, and have no trailing period. Breaking changes use `!` and explain the break and migration path in the body when they are not obvious.
- Agent-generated work is attributed at the durable boundary that records it.

Prefer guardrails in this order: eliminate the failure through design; detect it through automated or external controls; guide the remaining judgment with concise rules or explicit procedures; rely on user review only for residual cases.

## Audit categories

Discover the project's actual operating environment. Do not introduce preferred tooling just because it is absent.

Audit:

- Agent guidance: `AGENTS.md`, `CLAUDE.md`, Cursor rules, commands, and repo-specific agent instructions.
- Docs anchors: README workflow sections, `LANGUAGE.md`, `LANGUAGE-MAP.md`, `docs/architecture.md`, and `docs/adr/`.
- Commit workflow: the merge strategy, the message that enters integration history, current commit format, and any automated or external checks.
- Workflow conventions: branch naming, PR template use, issue links, contribution docs, and review instructions.
- Attribution: how agent-generated repository changes and collaboration artifacts identify their agent author.
- Rule storage: whether detailed agent rules live in ordinary docs, tool-specific rule directories, or duplicated sources.
- Ignore files: `.gitignore`, `.dockerignore`, Cursor/Claude/agent ignores, and other tool-specific ignore files that already apply.
- Environment guidance: Doppler, `.env`, secrets managers, `.env.example`, local/staging/production envs, and how agents should handle secrets.
- Runtime and deployment guidance: where the project runs, where it deploys, how to start it locally, and how agents avoid touching production.
- Local runtime ownership: whether agents may start long-running local dev servers during interactive work, or should assume the user manages them.
- Command registry: where common commands are documented and how agents should discover them without inventing stack-specific commands.
- Safety rules: data, auth, secrets, deployment, migrations, paid services, and destructive operations.
- Project Guardrails: architecture constraints, tests, static checks, continuous integration, repository settings, tracker states, service permissions, deployment gates, agent rules, and review practices.
- External controls: important protections or workflow states that do not live in Git, plus any repo pointer an agent needs to discover them.

## Classify findings

After auditing, classify findings:

- **Keep**: already matches the desired workflow.
- **Adopt**: existing convention should become the project default.
- **Add**: missing workflow anchor that is safe to create.
- **Ask**: conflict, ambiguity, hidden project knowledge, or multiple valid choices.
- **Deviation**: a deliberate failure to meet an applicable Engineering Convention that requires explicit approval.
- **Defer**: stack-specific setup outside this skill's scope.

Never assume absence means "create my preferred thing." First infer the project's current defaults.

## Adoption proposal

Before writing to the repo, present a concise adoption proposal.

Include:

- What the audit found.
- What existing conventions should be preserved.
- Which convention outcomes already have effective Project Guardrails.
- What files or docs should be added or updated.
- What missing outcomes need a guardrail, including external controls where appropriate.
- How the merge strategy will apply and guard the required commit form.
- How agent-generated work will be attributed at its durable boundaries.
- What should be skipped or deferred.
- Whether to add a local dev server ownership rule to `AGENTS.md`, if no project convention already answers it.
- Whether to add workflow convention guidance to `AGENTS.md` or a focused workflow doc, if no project convention already answers it.
- Whether to consolidate detailed agent rules into ordinary docs and point to them from an `AGENTS.md` rules index.
- What assumptions need user confirmation.
- What hidden project knowledge would change the proposal.
- Which deliberate deviations, if any, require explicit approval.

Stop after the proposal. Continue only when the user approves it or supplies a revision. Apply the approved scope and incorporate the user's project knowledge.

Use this deviation rule exactly:

> Any deliberate failure to meet an applicable Engineering Convention requires explicit approval.

## Artifact scope

Adoption may create or update the same artifact universe as greenfield initialization, but only through the audit and proposal flow.

- `AGENTS.md`: repo-level operating instructions for future agents.
- `LANGUAGE.md`: bounded project vocabulary.
- `LANGUAGE-MAP.md`: routing for multiple language contexts.
- `docs/architecture.md`: current system shape and navigation.
- `docs/adr/`: durable decisions.
- Rules index: a short `AGENTS.md` section that points to detailed agent rule docs.
- README workflow sections: how the project expects agents and humans to work.
- Review templates and contribution docs: collaboration, commit, branch, issue-linking, and review workflow.
- Ignore files: keep generated files, secrets, dependencies, and tool noise out of version control.
- Environment and deployment notes: where the project runs, how envs are managed, and what agents must not touch.
- Project Guardrails: project-owned architecture, code, checks, settings, tracker controls, guidance, or review practices that prevent or detect convention violations.

Keep generated or revised docs short. Adoption should make the repo safer for future agents, not create empty bureaucracy.

## Route specialist work

Route deeper durable knowledge work to the owning skill instead of expanding this skill's scope.

- Use `maintain-language` for substantial vocabulary work, multiple local language contexts, or unclear naming.
- Use `write-adr` when a decision is hard to reverse, surprising without context, and based on a real trade-off.
- Use `maintain-living-docs` when architecture, onboarding, operations, or project-specific guidance needs more than a thin adoption note.

## Keep AGENTS.md short

When creating or revising `AGENTS.md`, preserve useful project guidance and include the baseline commit and attribution rules. Commits entering integration history use `<type>[optional scope][!]: <description>`. Descriptions are imperative, lowercase, and have no trailing period. Breaking changes use `!` and explain non-obvious breaks and migration paths in the body. Add the agent as a co-author of agent-generated commits, and visibly attribute agent-authored pull request descriptions, reviews, comments, and tracker artifacts.

`AGENTS.md` must stay short because agents load it into context. Treat it as an index and routing layer, not a full policy document.

- Prefer 5-8 high-signal bullets.
- Link to deeper docs for details.
- Include only what an agent must know before choosing what to read next.
- Do not copy long environment, deployment, command, or review guidance into `AGENTS.md`; point to the relevant doc instead.

## Store rules for any agent

Prefer `AGENTS.md` as the universal agent entry point, with detailed agent rules stored as ordinary repo documentation.

- Add or preserve a short rules index in `AGENTS.md` when detailed guidance lives elsewhere.
- Prefer focused docs under `docs/` for long-lived rules, such as `docs/agentic-workflow.md`.
- Preserve existing tool-specific rule files when they are part of the project's real workflow, but do not create or expand them by default.
- If the repo has duplicated or conflicting guidance across `AGENTS.md`, Cursor rules, Claude files, `.agents/rules/`, or docs, include the consolidation choice in the adoption proposal and ask before changing it.

Use tool-specific rule directories only when the user explicitly asks for them or the repo already depends on them. Shared guidance should have one project-owned source of truth that Codex, Cursor, and other agents can follow.

## Ask who owns local runtimes

If the audit does not reveal a project convention for interactive local dev servers, ask whether agents should avoid starting long-running local dev servers during interactive work.

If the user wants that rule, add a short Agent Guidance bullet such as:

```md
- In interactive work, assume the user manages local dev servers. Do not start long-running dev servers unless asked; in unattended work, clean them up before finishing.
```

If the user does not want the rule, omit it. Preserve any existing project-specific runtime convention instead of replacing it.

## Ask about workflow conventions

If the audit does not reveal project conventions for commits, branches, PR templates, issue links, contribution flow, or review expectations, ask whether agents should follow any.

Prompt broadly enough to surface hidden working agreements without prescribing a preference:

```text
How do commits enter integration history here: squash, merge, or rebase? Are there repo-specific conventions for branch naming, PR templates, issue links, attribution format, or review expectations?
```

If existing conventions are found, preserve them and link to their source from `AGENTS.md` only when future agents need the pointer. If conventions conflict, are incomplete, or appear tool-specific rather than project-specific, include the ambiguity in the adoption proposal and ask before changing anything.

If the answer is compact, add one short Agent Guidance bullet. If it needs detail, document it in the README, a PR template, contribution guidance, or another focused workflow doc under `docs/`, then link to it from the `AGENTS.md` rules index.

If the user does not provide workflow conventions, omit the optional workflow rule but still propose the baseline commit and attribution rules above. Do not inject personal preferences, branch naming schemes, PR templates, issue tracker assumptions, or review flow defaults unless the user explicitly chooses them.

## Completion report

Report:

- What was added or updated.
- What was skipped.
- What was deferred to another skill or future session.
- What user guidance changed from the original proposal.
- What still needs a decision.
- What Project Guardrails were added, preserved, or deliberately deferred.
- What approved deviations remain.

Finish when every approved proposal item is applied or explicitly deferred, every existing convention touched by the work is preserved or deliberately replaced, and the report accounts for each proposal item. Do not leave behind an adoption manifest, playbook version marker, or copied convention document.
