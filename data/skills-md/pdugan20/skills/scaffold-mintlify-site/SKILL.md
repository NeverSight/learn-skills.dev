---
name: scaffold-mintlify-site
license: MIT
description: Scaffolds a new Mintlify documentation site with a project-specific information architecture, docs.json, starter pages, assets, and local documentation toolchain. Use when creating a new Mintlify site or docs-mintlify tree; do not overwrite an existing site, author finished product content, deploy, or mutate external hosting without explicit approval.
---

# Scaffold Mintlify Site

Stand up a new Mintlify docs site for a project in the house style. The output is
a `docs-mintlify/` tree authored in the **product repo** (so generators and
anti-drift CI sit next to the code). Keep publishing and hosting as a separate,
explicitly authorized phase.

This skill owns the editorial shape (IA, page set, house defaults). When the
official `mintlify` capability is available, use it for current component and
`docs.json` syntax. Otherwise inspect current Mintlify documentation instead of
guessing. The authority for the site decisions here is
[references/site-playbook.md](./references/site-playbook.md); read it
first.

## Usage

Provide the project root in the request or after an explicit skill invocation.
The skill runs in three phases: detect and decide (below), generate the tree,
then wire the toolchain. It is non-destructive: it never overwrites an existing
`docs-mintlify/`.

## Instructions: detect and decide

### Step 1: Don't clobber

Check for an existing `docs-mintlify/` (or `docs/`, `website/`). If found, offer
to **review/extend** it (hand off to `review-mintlify-docs`) rather than
scaffold over it.

### Step 2: Detect project type

Run [scripts/detect-project-type.sh](./scripts/detect-project-type.sh) (or read
`pyproject.toml` / `package.json` / look for an OpenAPI spec). Determine which of
these the project has, since they drive the IA and the reference tab:

- **CLI** (a `console_scripts` / `bin` entry point)
- **MCP server** (a FastMCP or MCP SDK server module)
- **HTTP API** (an OpenAPI/AsyncAPI spec)

**If the project is an MCP server, the `Claude (MCP)` nav group is mandatory.**

### Step 3: Decide the brand and IA, options-first

Present 2 to 3 options plus a recommendation for:

- **Brand primary color.** Do not default to the generic indigo `#6366f1`;
  pick a deliberate color with measured contrast in light and dark.
- **The differentiator hook** for the introduction.
- **The how-to topic groups** for this project (e.g. Getting started / Everyday
  use / Integrations / Claude (MCP) / Concepts / Help).

Confirm before writing files.

Before labeling a color pairing accessible or reporting a ratio, run
[scripts/check_contrast.py](./scripts/check_contrast.py) with the exact
foreground and background values. Label colors provisional when the relevant
surface colors are not yet known or the calculation has not been run.

## Generate the tree

Create `docs-mintlify/` from the bundled assets, substituting the decided values:

- Start configuration from [docs.json](./assets/docs.json).
- Adapt [introduction.mdx](./assets/introduction.mdx),
  [quickstart.mdx](./assets/quickstart.mdx),
  [requirements.mdx](./assets/requirements.mdx), and
  [troubleshooting.mdx](./assets/troubleshooting.mdx) to the project.
- Keep [changelog.mdx](./assets/changelog.mdx) as the reader-facing update
  surface and replace [favicon.svg](./assets/favicon.svg) during the visual pass.

```text
docs-mintlify/
  docs.json              from assets/docs.json (fill name, color, nav groups)
  introduction.mdx       from assets/introduction.mdx
  quickstart.mdx         from assets/quickstart.mdx
  requirements.mdx       from assets/requirements.mdx
  troubleshooting.mdx    from assets/troubleshooting.mdx
  changelog.mdx          from assets/changelog.mdx
  guides/                one stub per decided how-to
  concepts/              architecture (+ design / mcp-server if relevant)
  reference/             cli.mdx / mcp-tools.mdx / configuration.mdx as relevant
  logo/                  placeholder light.svg / dark.svg (note: replace in visual pass)
  favicon.svg            placeholder adaptive favicon
```

The `docs.json` asset encodes a starting IA: a **Guides** tab with topic groups
and a **Reference** tab split into CLI / MCP groups. Delete the groups the project
does not need; never leave a flat how-to list longer than roughly five entries.

## Wire the toolchain

- **Makefile targets** from [assets/Makefile-docs.mk](./assets/Makefile-docs.mk):
  `docs` (preview), `docs-validate` (strict validation), `docs-reference`
  (regenerate), and `docs-links` (links, anchors, and redirects). Merge these
  into an existing Makefile rather than replacing it.
- **Reference generators:** hand off to `generate-mintlify-reference` to add
  `gen_cli_reference.py` / `gen_mcp_reference.py` and the drift CI.
- **Publishing:** do not configure a Git provider, install an app, deploy, or
  change a domain as part of scaffolding. If publishing is requested, check
  current Mintlify guidance and propose the smallest supported setup before
  asking for authorization.

## Hand off

After scaffolding, the natural next steps are:

1. `generate-mintlify-reference` to generate the CLI/MCP/API reference and drift CI.
2. `review-mintlify-docs` for the first content pass once stubs have real content.
3. `write-mintlify-changelog` for the first changelog entry at first release.

## Scope

This skill creates the initial tree, `docs.json`, stubs, and toolchain wiring. It
does not write finished page content (that is an authoring pass) and does not
perform publishing, account, Git provider, domain, or DNS changes.
