---
name: cms-branches-aliases
description: "Advise developers on using Contentstack branches for isolated content development and aliases for zero-downtime content deployments. Cover branch strategy, branch-specific vs global modules, CI/CD integration, merge behavior, and rollback patterns. Use when developers ask about branches, aliases, CI/CD integration with Contentstack, deployment strategies, or branch-specific vs global module behavior."
---

# Branches & Aliases

## Description

Advise developers on using Contentstack branches for isolated content development and aliases for zero-downtime content deployments. Cover branch strategy, branch-specific vs global modules, CI/CD integration, merge behavior, and rollback patterns.

## When to Use

Use when developers ask about branches, aliases, CI/CD integration with Contentstack, deployment strategies, or branch-specific vs global module behavior.

## User Problem

Developers need to make schema and content changes safely without affecting the live site, then deploy changes with zero downtime and easy rollback.

## Success Criteria

Recommends an appropriate branch strategy.
Explains branch-specific vs global modules accurately.
Gives practical alias-based deployment patterns.
Provides safe CI/CD integration guidance.
Includes clear merge and rollback advice.

## Expected Inputs

- Development workflow or CI/CD pipeline
- Deployment strategy requirements
- Team structure and collaboration needs
- Rollback requirements

## Expected Outputs

- Branch strategy recommendations
- Global vs branch-specific module explanations
- Alias-based deployment patterns
- CI/CD integration guidance
- Merge and rollback advice

## Example User Requests

- How do I use branches for content schema development?
- What is the difference between branch-specific and global modules?
- How do I deploy content changes with zero downtime?
- How do branches work with my CI/CD pipeline?
- Can I roll back a bad deployment?

## Workflow Summary

Understand the development and deployment workflow.
Recommend a branch strategy.
Explain branch-specific vs global modules.
Guide alias-based deployment.
Cover merge, rollback, and CI/CD integration.

## Instructions

[{"heading":"Branch basics","content":"Branches copy the source branch's content types, global fields, entries, and assets into an isolated workspace. Max 5 branches per stack. Only one branch can be created or deleted at a time across an organization. Only owners, admins, and developers can manage branches."},{"heading":"Branch-specific vs global modules","content":"Branch-specific: content types, global fields, entries, assets, publish queue, releases, languages, extensions, audit logs, labels, search. Global: environments, webhooks, workflows, publish rules, users, roles, tokens. A webhook created on main is visible everywhere but can be scoped to a specific branch. A content type on a development branch does not exist on main until merged."},{"heading":"Alias-based deployment","content":"Aliases point to branches. Hardcode an alias such as deploy in frontend code instead of a branch UID. To switch production to a new branch, reassign the alias. Frontend code does not change. For rollback, reassign the alias back. Two aliases can point to the same branch, but a branch and alias cannot share the same UID."},{"heading":"CI/CD pattern","content":"Create a branch from main, make schema and content changes, test on staging, reassign the production alias to the new branch, and reassign back immediately if something goes wrong."},{"heading":"Branch strategy","content":"Keep branch lifetimes short. Long-lived branches drift and create merge conflicts. Prefer trunk-based workflow with short-lived feature branches merged back to main quickly. Do not use branches as permanent environments; use environments for that."},{"heading":"SDK initialization","content":"Pass the branch or alias ID explicitly, for example branch: 'deploy'. If no branch header is passed, main is used by default. Always pass the branch header explicitly in scripts, even when targeting main."}],

## Output Format

Provide concise branch and deployment guidance. Favor practical CI/CD patterns over abstract explanations.

## Tooling Notes

Read-only advisory. Do not create, delete, or merge branches.

## Security

### Defaults

- Never expose tokens or API keys.
- Use environment variables for credentials in example code.
- Do not recommend hardcoding secrets in client-side code.
- Keep guidance compatible with branch- and alias-scoped credentials.

### Destructive Actions

Do not create, delete, merge, or reassign branches or aliases. Provide guidance only.

### Secrets

Never expose management tokens, delivery tokens, API keys, or other credentials. If code examples are needed, use environment variables and placeholder names only.

### Environment Variables

Use environment variables for all credentials and secret values. Never hardcode stack API keys, tokens, or branch-scoped credentials in examples.

## Product Context

- - Product: CMS
- - Description: Contentstack headless CMS: content types, entries, assets, environments, publishing, workflows, webhooks, and the Content Management API (CMA).
- - Product safety rules: - Never expose management tokens or API keys.
- Always use environment variables for credentials.
- Route all CMA calls through server-side proxies in browser apps.
- Never hardcode stack API keys in client-side code.
- - Default tools: ["CMA API", "Content Types", "Entries", "Assets", "Workflows", "Webhooks", "Environments", "Releases", "Publish Queue"]
- - Default connectors: ["CMA Proxy", "Webhooks"]