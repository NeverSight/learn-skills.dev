---
name: migrate-skills-yaml
description: Converts the old flat skills.yaml format to the new per-group file format with variants. Use when a PR or branch still has a top-level "skills:" array instead of separate group files.
metadata:
  temporary: "true"
---

<!-- TEMPORARY: remove after all PRs are migrated to grouped skills format -->

## Old format (single flat file)

```yaml
shared_docs:
  - https://posthog.com/docs/getting-started/identify-users.md

skills:
  - id: nextjs-app-router
    type: example
    example_paths: basics/next-app-router
    display_name: Next.js App Router
    description: PostHog integration for Next.js App Router applications
    tags: [nextjs, react, ssr, app-router, javascript]
    docs_urls:
      - https://posthog.com/docs/libraries/next-js.md

  - id: react
    type: docs-only
    display_name: React
    tags: [react, feature-flags, javascript]
    docs_urls:
      - https://posthog.com/docs/feature-flags/installation/react.md
```

## New format (separate files per group)

Skills live in `transformation-config/skills/`, one file per group:

### `integration-skills.yaml` (type: example)

```yaml
type: example
template: integration-skill-description.md
description: PostHog integration for {display_name} applications
shared_docs:
  - https://posthog.com/docs/getting-started/identify-users.md
variants:
  - id: nextjs-app-router
    example_paths: basics/next-app-router
    display_name: Next.js App Router
    tags: [nextjs, react, ssr, app-router, javascript]
    docs_urls:
      - https://posthog.com/docs/libraries/next-js.md
```

### `feature-flag-skills.yaml` (type: docs-only)

```yaml
type: docs-only
template: feature-flag-skill-description.md
description: PostHog feature flags for {display_name} applications
tags: [feature-flags]
shared_docs:
  - https://posthog.com/docs/feature-flags/adding-feature-flag-code.md
  - https://posthog.com/docs/feature-flags/best-practices.md
variants:
  - id: react
    display_name: React
    tags: [react, javascript]
    docs_urls:
      - https://posthog.com/docs/feature-flags/installation/react.md
```

### Other group files

- `llm-analytics-skills.yaml` -- LLM observability skills
- `logs-skills.yaml` -- Log capture skills
- `other-skills.yaml` -- Catch-all (e.g. HogQL); variants can override `template` and `shared_docs`

## Existing groups

| File | Plugin name | Type | Category suffix |
|------|-------------|------|-----------------|
| `integration-skills.yaml` | `posthog-integration` | `example` | `-integration` |
| `feature-flag-skills.yaml` | `posthog-feature-flags` | `docs-only` | `-feature-flag` |
| `llm-analytics-skills.yaml` | `posthog-llm-analytics` | `docs-only` | `-llm-analytics` |
| `logs-skills.yaml` | `posthog-logs` | `docs-only` | `-logs` |
| `other-skills.yaml` | `posthog-tools` | `docs-only` | (none) |

## Key differences from old format

- **`variants`** (not `variations`) is the key for the list of skills
- **`type`** is set at the group level, not per-skill (unless a variant needs to override)
- **`template`** is set at the group level; each group has its own SKILL.md template
- **`shared_docs`** can be set at group level (shared by all variants) or per-variant
- **`description`** at group level uses `{display_name}` placeholder, substituted per variant
- **`tags`** at group level are merged with per-variant tags
- Skill IDs are automatically namespaced: `{id}-{category}` (e.g. `nextjs-app-router` in `integration-skills` becomes `nextjs-app-router-integration`). The `other` category skips the suffix.

## Migration steps

1. Identify which group each skill belongs to (integration, feature-flag, llm-analytics, logs, or other)
2. Add each skill as a variant in the appropriate `transformation-config/skills/{group}-skills.yaml` file
3. Remove `type` from the variant (inherited from group) unless it needs to differ
4. Keep `id`, `display_name`, `description` (optional), `tags`, `docs_urls`, and `example_paths` (for example-type skills)
5. Remove the old flat file
