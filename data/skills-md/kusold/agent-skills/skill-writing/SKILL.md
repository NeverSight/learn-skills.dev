---
name: skill-writing
description: Create, review, or improve agent skills (SKILL.md and supporting resources); use for "write a skill", "improve this skill", "review this SKILL.md", or fixing skill activation and workflow failures.
---

# Skill Writing

Package reusable decisions that improve an agent's work. Scale effort to the request; a wording fix does not need a redesign.

## Establish the task

Read repository instructions and neighboring skills. Honor the requested or implied project location before using the host's default skill directory.

Identify intended requests, observable results, inputs, tools, and boundaries. Ground decisions in completed tasks, corrections, runbooks, schemas, or fixes. Choose one coherent capability; identify missing domain evidence rather than inventing expertise. Ask only for missing information that changes implementation.

- **Create:** extract a reusable method, specialized knowledge, or reliable automation.
- **Improve:** inspect existing instructions, resources, callers, and examples. Establish an objective: correctness, clarity, brevity, or changed requirements. Make the smallest coherent change, consolidate obsolete rules, and preserve unrelated metadata, invocation policy, and working behavior.
- **Review:** report actionable findings with file references; edit only when fixes are requested.

Distinguish observed failures, suspected problems, and unmeasured improvements.

## Design discovery and context

Write a specific name and description explaining capability and activation in the user's terms. Check neighboring skills for name collisions and overlapping triggers; different names alone do not resolve overlap. Add meaningful boundaries and report unavoidable overlap.

Keep shared decisions and essential constraints in `SKILL.md`. Add references for conditional detail, scripts for repeated or fragile logic, and assets for deliverables. Link resources where relevant and state when to load them. Avoid unused scaffolding and duplicated documentation; follow repository documentation conventions.

Package runtime resources with the skill or declare external dependencies. Do not depend on an uninstalled docs directory, private wiki, author-specific paths, or assumed tools.

Read only the references needed for the task:

- [Format checklist](references/agent-skills.md): new packages, format reviews, validation commands, or snapshot refreshes.
- [Specification snapshot](references/specification.md): exact field rules, package examples, or format disputes. Check its date and verify live requirements when current compatibility matters.
- [Codex](references/codex.md): Codex paths, UI metadata, invocation policy, or authoring helpers.
- [Scripts](references/scripts.md): adding or changing executable helpers.
- [Evaluation](references/evaluation.md): new workflows or behavioral changes.

## Write instructions that change behavior

Include what a capable agent would otherwise miss: task-specific decisions, conventions, and constraints. Remove generic advice and repeated policy.

Use direct verbs, concrete checks, useful examples, and a default approach with explicit fallback conditions. Explain unusual constraints. Reserve fixed sequences for fragile operations; allow judgment elsewhere.

Preserve user choices, scope, and authorization. Define stopping conditions for consequential effects and retries; do not introduce approval gates for authorized routine work.

Separate requirements from preferences and local conventions. Attribute specialized claims, distinguish inference, and surface gaps or conflicts. Do not generalize one incident into a universal rule.

## Validate the result

Check format against the specification, resolve local links, verify resource packaging and command interfaces, and update affected docs and catalog entries. Run an available validator and exercise changed scripts. A format pass does not establish task quality; evaluate activation and outcomes separately using the evaluation reference when behavior changes.

Report changes, checks, and limitations. Distinguish inspection, walkthroughs, and actual agent runs; identify untested behavior.
