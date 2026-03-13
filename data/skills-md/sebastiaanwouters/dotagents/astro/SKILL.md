---
name: astro
description: Build, migrate, debug, and optimize Astro projects using current official patterns. Use when requests mention Astro, .astro files, astro.config.*, create-astro, astro add, content collections (astro:content), image optimization (astro:assets), adapters/SSR, or content-heavy sites including blogs with Markdown/MDX, RSS, and sitemap needs.
---

# Astro

## Overview

Implement production-ready Astro work with docs-first defaults and minimal guesswork. Start with the general workflow, then use the blog-focused section when the task is specifically a blog or content site.

Read `references/astro-playbook.md` for current versions, commands, API patterns, and blog-specific implementation details.

## General Workflow

1. Confirm runtime and rendering model.
- Identify whether the task is static-first, mixed mode, or server-first.
- If on-demand rendering is required, ensure an adapter is installed and routes opt out of prerendering (or use server output mode).

2. Set up or normalize project baseline.
- Use `create astro@latest` for new projects.
- Keep `astro.config.*` explicit (`site`, integrations, output mode as needed).
- Prefer `astro add` for official integrations.

3. Implement pages and components with Astro-first patterns.
- Keep framework islands minimal and purposeful.
- Use server/client boundaries intentionally.
- Avoid adding framework complexity when plain Astro solves the task.

4. Use the Content Layer API for structured content.
- Define collections in `src/content.config.*` with Zod schemas.
- Query with `getCollection()`, `getEntry()`, `getEntries()`, and render entries with `render()`.
- Prefer content collections over ad-hoc glob imports for long-term maintainability.

5. Handle media with `astro:assets`.
- Prefer local images in `src/` when processing/optimization is needed.
- Use `<Image />` or `<Picture />` when possible and always provide `alt`.
- Configure remote image authorization before transforming external images.

6. Add integration-level SEO and content outputs when relevant.
- Configure RSS and sitemap for content sites.
- Ensure `site` is configured before generating canonical URLs, RSS links, or sitemap entries.

7. Validate and verify.
- Run `astro check` and build commands.
- Verify routes, metadata, feed output, and sitemap artifacts.
- Prefer small, testable increments rather than broad rewrites.

## Blog-Focused Mode

Use this mode when building a blog, docs site, or other content-heavy publishing workflow.

1. Model posts with collections and schema validation.
- Include fields such as `title`, `description`, `pubDate`, `draft`, `tags`, and optional cover image data.

2. Build list, post, and taxonomy routes from collection queries.
- Filter drafts for production.
- Sort by publish date descending.
- Generate `getStaticPaths()` for static post pages, or fetch by params in SSR flows.

3. Add publishing integrations.
- Generate RSS feed endpoints with `@astrojs/rss`.
- Add sitemap integration and tune include/exclude behavior for search crawl quality.

4. Improve editorial workflow.
- Add MDX support only when component-rich content is required.
- Keep Markdown defaults simple for faster writing and lower maintenance.

5. Optimize article media and accessibility.
- Use structured cover images from content schema.
- Ensure meaningful alt text.

## Output Expectations

When delivering Astro work:
- State chosen rendering mode and adapter assumptions.
- Show modified files and why each change exists.
- Include run/validation commands (`astro dev`, `astro check`, `astro build`) when relevant.
- Call out remaining risks (content schema gaps, image source authorization, deployment adapter constraints).

## Reference

- `references/astro-playbook.md`: Up-to-date Astro facts (verified date, versions, APIs, blog patterns, and source links).
