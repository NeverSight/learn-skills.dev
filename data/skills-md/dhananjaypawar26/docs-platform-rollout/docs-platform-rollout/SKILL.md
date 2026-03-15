---
name: docs-platform-rollout
description: "End-to-end documentation rollout for repositories: bootstrap production docs, integrate Docusaurus, and prepare Vercel deployment. Use when users ask to set up complete project documentation and publishing in one pass."
metadata:
  short-description: End-to-end docs rollout
---

# Docs Platform Rollout

Use this skill when the user wants complete documentation setup in one run.

## Scope

This skill is self-contained and ships the implementation details it needs in `references/`.

Bundled references:

1. `references/project-docs-bootstrap.SKILL.md`
2. `references/docs-docusaurus-vercel.SKILL.md`
3. `references/skills-usage-and-vercel-deployment.md`

## How to load references

Read the references in this order before making changes:

1. `references/project-docs-bootstrap.SKILL.md`
2. `references/docs-docusaurus-vercel.SKILL.md`
3. `references/skills-usage-and-vercel-deployment.md` only when deployment or reuse guidance is needed

## Workflow order

1. Use `references/project-docs-bootstrap.SKILL.md` to create or standardize the `docs/` structure and baseline content.
2. Use `references/docs-docusaurus-vercel.SKILL.md` to publish docs with Docusaurus and configure Vercel deployment.
3. Validate local docs build and list deployment steps.

## Inputs to confirm

- Project/repo name
- Branch strategy (auto deploy or manual production promotion)
- Desired docs route (`/docs` or `/`)
- Vercel root strategy (repo root or `website`)

## Required outputs

- Production-ready `docs/` structure with governance metadata.
- `website/` Docusaurus site consuming root docs.
- `vercel.json` aligned to root-directory strategy.
- Root npm scripts for docs dev/build/serve.
- Validation result from local docs build.

## Acceptance criteria

- Docs structure exists and is internally consistent.
- `npm --prefix website run build` succeeds.
- Sidebar renders all configured sections.
- Vercel deployment config is explicit and reproducible.
- The skill can be copied alone into another repo under `.agents/skills/docs-platform-rollout/` and still be usable.

## Failure handling

- If docs build fails, fix MDX/sidebar/routes before finishing.
- If Vercel setup fails, provide exact fallback mode (`Mode A` or `Mode B`) and branch/deploy instructions.
