---
name: litestar-static-files
description: Serve static assets in Litestar with `create_static_files_router()`, explicit mount paths, HTML mode, cache-control policy, URL reversal, custom file systems, and symlink-safe directory boundaries. Use when exposing JS, CSS, images, downloadable artifacts, or static HTML from controlled directories. Do not use for upload ingestion, user-writable file publication, or arbitrary file-download endpoints that need per-request authorization logic.
---

# Static Files

## Execution Workflow

1. Decide whether the app needs normal asset serving, downloadable files, or static HTML mode.
2. Mount assets with `create_static_files_router()` under an explicit path and controlled directories.
3. Set delivery behavior intentionally: inline vs attachment, HTML mode, name, schema visibility, and router metadata.
4. Choose cache behavior that matches asset mutability and deployment strategy.
5. Lock down file system boundaries, especially symlink behavior and any remote/custom file system integration.
6. Verify URL reversal, `404` behavior, and template references before treating the mount as stable.

## Core Rules

- Prefer `create_static_files_router()` for current Litestar static-file serving.
- Keep static directories separate from writable upload or user-content directories.
- Use explicit URL prefixes such as `/static` or `/assets` unless HTML mode intentionally owns `/`.
- Treat directories as relative to the working directory unless you pass explicit absolute paths.
- Use `send_as_attachment=True` only when download behavior is intentional.
- Use `html_mode=True` only when the mounted directory should behave like a static site root.
- Keep symlink escaping disabled unless you fully understand the file system and exposure risk.
- Match cache policy to asset versioning; long cache lifetimes require immutable or content-hashed files.

## Decision Guide

- Use one static router for ordinary CSS, JS, fonts, and images.
- Use a separate static router when downloadable artifacts need different headers, pathing, or access controls.
- Use `html_mode=True` when `/index.html` and `/404.html` should drive static-site behavior.
- Use `cache_control=` when shared cache headers should apply to every static response from that router.
- Use `name=` when template helpers or `route_reverse()` must distinguish multiple static mounts.
- Use `include_in_schema=False` for public asset routes unless there is a real reason to document them.
- Use `file_system=` when assets come from a non-default or remote file system.
- Use router-level `guards`, `middleware`, or hooks only when asset access needs policy beyond plain public serving.

## Reference Files

Read only the sections you need:

- For basic `create_static_files_router()` setup, directory handling, attachment mode, and route naming, read [references/router-basics-and-naming.md](references/router-basics-and-naming.md).
- For HTML mode, cache policy, router options, schema visibility, and template URL generation, read [references/html-mode-cache-and-urls.md](references/html-mode-cache-and-urls.md).
- For remote file systems, symlink safety, and test patterns, read [references/filesystems-security-and-testing.md](references/filesystems-security-and-testing.md).

## Recommended Defaults

- Mount ordinary assets under `/static` or `/assets`.
- Keep asset directories read-only at runtime whenever possible.
- Use hashed filenames or versioned asset paths before applying aggressive cache headers.
- Keep static routers out of OpenAPI unless clients truly need them documented.
- Use one clear static route name per mount and reference it through `url_for` or `route_reverse()` instead of hardcoding paths.
- Reserve HTML mode for true static-site behavior rather than as a substitute for template rendering.

## Anti-Patterns

- Serving static files from the project root or another overly broad directory.
- Publishing user-upload directories directly through the same static router as trusted build assets.
- Using `/` as the mount path without intending HTML mode or full static-site ownership.
- Applying long-lived cache headers to mutable filenames.
- Hardcoding asset URLs in templates when route reversal is available.
- Enabling symlink escape behavior without a narrow, audited need.
- Treating a static mount as an authorization-aware download endpoint when the route actually needs per-request business logic.

## Validation Checklist

- Confirm the mount path and directory list are explicit and correct relative to the app's working directory.
- Confirm expected assets are reachable and unexpected paths return `404`.
- Confirm inline vs attachment behavior matches the product requirement.
- Confirm HTML mode serves `index.html` and `404.html` as intended when enabled.
- Confirm cache headers align with asset mutability and CDN/browser expectations.
- Confirm `route_reverse()` or template URL generation resolves the right path for each static router name.
- Confirm any custom file system or symlink configuration is secure by intent.
- Confirm tests cover at least one happy path and one missing-file path.

## Cross-Skill Handoffs

- Use `litestar-templating` when the main task is rendering HTML that references static assets.
- Use `litestar-responses` when one-off file download responses or manual response headers are the real concern.
- Use `litestar-file-uploads` when the challenge is ingesting or validating files before publication.
- Use `litestar-testing` when static asset routing, headers, and `404` behavior need regression coverage.
- Use `litestar-security` when access to static or downloadable files must be guarded intentionally.

## Litestar References

- https://docs.litestar.dev/latest/usage/static-files.html
- https://docs.litestar.dev/latest/reference/static_files.html
