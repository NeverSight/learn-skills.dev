---
name: webflow-designer-api
description: Work with the Webflow Designer API — either by building Designer Extensions (iframes inside the Webflow Designer) or by generating code snippets for the Designer API Playground. Covers element manipulation, styles, components, pages, variables, assets, error handling, CLI usage, and UI design patterns. Use when creating, debugging, or modifying Designer Extensions, OR when the user wants to run Designer API code in the Playground app.
license: MIT
compatibility: "create-webflow-extension, @webflow/webflow-cli"
metadata:
  author: "Ben Sabic"
  repository: "https://github.com/224-industries/webflow-skills"
  url: "https://skills.224ai.au/webflow-designer-api.skill"
  version: "2.0.0"
  keywords: "ai, agent, skill, webflow, designer, extension, cli, element-manipulation, styles, components, pages, variables, assets, error-handling, ui-design-patterns"
---

# Webflow Designer API

This skill helps users work with the Webflow Designer API through two workflows. **Start by asking the user which workflow they'd like to use**, or infer from context if it's obvious.

## Workflows

### 1. Designer Extensions
Build full extensions with a UI that run inside the Webflow Designer as iframes. Best for reusable tools, complex workflows, and apps you want to ship to a team or the Marketplace.
→ See **[references/designer-extension-workflow.md](references/designer-extension-workflow.md)**

### 2. Designer API Playground
Write and run standalone code snippets directly in the Playground app inside the Designer. Best for quick prototyping, testing API methods, learning the API, and one-off automations.
→ See **[references/playground-workflow.md](references/playground-workflow.md)**

## Reference Documentation

Each reference file includes YAML frontmatter with `name`, `description`, and `tags` for searchability. Use the search script available in `scripts/search_references.py` to quickly find relevant references by tag or keyword.

### Designer API References

Both workflows use the same `webflow.*` Designer API. Once you know the workflow, use these references to write the actual code:

- **[references/designer-apis-reference.md](references/designer-apis-reference.md)** — All `webflow.*` methods in one table (start here)
- **[references/elements-api.md](references/elements-api.md)** — Element selection, insertion, presets, and the element builder
- **[references/styles-api.md](references/styles-api.md)** — Creating styles, setting CSS properties, breakpoints, and pseudo-states
- **[references/components-api.md](references/components-api.md)** — Component definitions, instances, and editing context
- **[references/pages-api.md](references/pages-api.md)** — Page and folder management
- **[references/variables-api.md](references/variables-api.md)** — Design token variables and collections
- **[references/assets-api.md](references/assets-api.md)** — Asset upload and management
- **[references/extension-utilities.md](references/extension-utilities.md)** — Site info, events, notifications, app discovery, authentication
- **[references/error-handling.md](references/error-handling.md)** — Error structure, cause tags, and recovery patterns
- **[references/code-examples.md](references/code-examples.md)** — Cross-API workflow examples combining multiple APIs

### Design & Marketplace References

- **[references/design-guidelines.md](references/design-guidelines.md)** — UI design for native Webflow look
- **[references/register-app.md](references/register-app.md)** — Registering a Webflow App and configuring capabilities
- **[references/marketplace-guidelines.md](references/marketplace-guidelines.md)** — Marketplace review criteria
- **[references/app-submission-and-listing.md](references/app-submission-and-listing.md)** — Submitting your app and creating a listing
- **[references/faq.md](references/faq.md)** — FAQ and troubleshooting

### Searching References

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```

## Scripts and Assets

- **`scripts/search_references.py`**: Search reference files by tag, keyword, or list all with metadata
- **`assets/webflow-variables.css`** — CSS variables for Webflow's design system
- **`assets/install-playground-prompt.md`** — Copyable prompt for installing the Designer API Playground via Claude Cowork or the Claude Chrome Extension