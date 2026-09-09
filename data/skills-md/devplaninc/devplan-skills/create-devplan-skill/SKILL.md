---
name: create-devplan-skill
description: Turn a repeatable product-work prompt or workflow into a concise skill that uses Devplan effectively. Use when creating or substantially revising a Devplan task skill for a team's own planning, customer, delivery, or product workflow. Exclude ordinary product work and minor copy edits to an existing skill.
---

# Create a Devplan Skill

Turn the user's workflow into the smallest reusable skill that helps their team perform that task with Devplan context.

Use the destination the user specifies. If none is given, use the current repository's skill directory only when it is clearly a skills repository; otherwise ask where the skill should live. Apply the client's available skill-creation guidance and scaffolding when available.

## Build the minimum useful skill

1. Identify the requested outcome, the phrases or situations that should invoke the skill, important exclusions, and the result it should produce.
2. Create the thinnest skill that preserves the user's workflow: strong frontmatter, a minimally generalized task prompt, `devplan-product-context` invocation, and only genuinely task-specific guidance.
3. Validate the skill's structure, references, metadata, discovery, and installation using the tools available in the target repository.

Read [references/devplan-skill-conventions.md](references/devplan-skill-conventions.md) before creating or substantially revising a customer-facing skill.

## Required properties

Every customer-facing Devplan task skill should:

- apply `devplan-product-context` when available and disclose when it is unavailable;
- remain usable with the customer's own workspace, product, sources, and terminology;
- treat Devplan and connected sources as read-only unless the user explicitly requests a specific write;
- return its result in chat unless the user requests a file or another destination;
- treat live Devplan MCP tool descriptions as authoritative for graph entities, relationships, retrieval methods, workspace identity, and current query behavior;
- avoid duplicating the MCP's graph and retrieval guidance or the foundation's evidence and delivery-state guidance.

Keep `SKILL.md` concise. Add references, scripts, templates, taxonomies, or rigid output schemas only when the task cannot work reliably without them.

Report the files created or changed and the validation performed. If validation tooling or Devplan access is unavailable, say what remains unverified.
