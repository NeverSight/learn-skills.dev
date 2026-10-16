---
name: dx-kickstart-next
description: "Guidance for building, reviewing, debugging, or extending Contentstack's kickstart-next repository. Use when working in contentstack/kickstart-next or a close fork: the Next.js kickstart app, its Contentstack Delivery SDK setup, Live Preview or Visual Builder behavior, seeded stack alignment, environment variables, endpoint or image host configuration, App Router structure, package scripts, local setup, CI expectations, tests, lint/build validation, or PR review checklists. For general Delivery SDK or Live Preview questions outside this repo, use dx-delivery-sdk or cms-live-preview-visual-editor-support-assistant."
---

# Contentstack kickstart-next

Use this skill when working in `contentstack/kickstart-next` or a close fork. Inspect the repository first, then load only the matching reference files.

## Routing

1. For App Router routes, React components, client/server boundaries, Tailwind, ESLint, TypeScript, images, or `next.config.mjs`, read [references/next.md](references/next.md).
2. For Contentstack delivery, preview, Visual Builder, regions, endpoint overrides, env vars, or seeded stack alignment, read [references/contentstack.md](references/contentstack.md).
3. For content type UIDs, field UIDs, modular blocks, CSLP `$` mappings, or schema-driven renderer/type changes, read [references/content-model.md](references/content-model.md).
4. For local setup, Contentstack stack seeding, npm scripts, CI, CODEOWNERS, validation commands, docs updates, or PR prep, read [references/workflow.md](references/workflow.md).
5. For PR/code reviews, severity labels, security checks, or risk checklists, read [references/review.md](references/review.md).

## Default working rules

- Keep guidance grounded in the current checkout. Inspect files before assuming scripts, tests, CI, content types, env vars, or framework conventions exist.
- Treat kickstarts as user-facing examples: prefer clarity, minimal moving parts, safe defaults, and copyable setup steps over clever abstractions.
- Preserve Live Preview behavior when changing data fetching, route rendering, components, content types, field UIDs, or Visual Builder bindings.
- When adding or renaming env vars, update `.env.example` and user-facing docs together.
- When adding remote image sources, update the framework-specific image allowlist or documented env override.
- When modifying JavaScript or TypeScript files, run `npm run build`; also run `npm run lint` and any `typecheck` script if they exist.
- Before claiming CI covers something, verify the workflows. If build, lint, or tests are not wired into CI, tell the user to run them locally.

## Response behavior

- For implementation help, give concrete file-level changes and commands.
- For reviews, separate blockers from major issues and minor nits.
- For repo setup help, give the shortest successful path first, then optional troubleshooting.
- If asked to generalize framework-specific guidance later, keep Contentstack behavior in `contentstack.md` and Next.js behavior in `next.md`.

## Security

### Defaults

- Never commit real Contentstack credentials. `.env.example` and docs use placeholders; real values live in a gitignored `.env`.
- Delivery tokens are safe in the browser. Preview tokens read unpublished content: expose them client-side only on preview deployments (CSR preview needs them), never in production builds. Management tokens never reach the browser.
- Never recommend enabling Live Preview in production builds.

### Destructive Actions

Advisory by default. Before changing a user's stack (seeding, schema changes) or force-pushing, deleting branches or rewriting history in the repo, describe the impact and get explicit confirmation.

### Secrets

Never print, echo or store tokens, API keys or `.env` values. If a secret appears in a file, log or message, don't repeat it; recommend rotating it.

### Environment Variables

Use the variable names from the repo's `.env.example`, for example `NEXT_PUBLIC_CONTENTSTACK_API_KEY` and `NEXT_PUBLIC_CONTENTSTACK_DELIVERY_TOKEN`, with placeholder values.
