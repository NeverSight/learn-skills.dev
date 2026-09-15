---
name: abadikan-theme-authoring
description: Design and refine Abadikan invitations using existing themes such as Aruma, with a complete local visual preview before uploading assets or creating variants and admin demos through MCP. Use for invitation design and theme authoring; ordinary customer checkout is outside this workflow.
---

# Abadikan Theme Authoring

Use an accessible `abadikan-web` checkout for the renderer and Abadikan MCP for data operations. The backend is a remote service; cloning fullstack, admin, or backend is not required.

## Locate the workspace

- Resolve `WEB_ROOT` from the user-selected web checkout. At the current directory, look for `app/lib/invitation/template-registry.ts`; in a fullstack checkout, look under `abadikan-web/` instead. If neither exists, locate an existing checkout or ask for its location/access. Do not clone private sibling repositories automatically.
- Run web commands from `WEB_ROOT`. Renderer paths in the bundled references are relative to it. Read the applicable repository instructions; use graphify only where the repository requires it and a graph exists, reporting an unavailable CLI honestly.
- Read [MCP setup](references/mcp-setup.md) for remote OAuth or optional local stdio. Installing this skill does not install the web source or connect MCP automatically.
- Read [local preview](references/local-preview.md) before building a draft. A remote-only chat without filesystem/browser access cannot complete the local renderer workflow; report that missing capability before attempting writes.

## Preview before remote writes

The workflow is local design → visual review and revision → final assets/config → MCP upload and creation → public verification. A request such as "generate tema Aruma Aceh" starts with a visible design, not remote entity creation. An MCP success response or a list of colors/fonts/IDs is not the design deliverable.

- Read-only MCP discovery is allowed at the start. Do not call asset uploads, template/variant writes, or invitation creation to obtain an initial preview, including creating an inactive variant for that purpose. This ordering applies to equivalent API calls too.
- Keep unfinished config and newly generated assets local. Reuse existing public assets as appropriate. Connect/authenticate only when the next necessary operation needs it; an existing local base can support design work while MCP access is unavailable.
- Show the actual preview and finish the checks below before remote writes. Honor any requested review pause. If the user already requested creation/publication and the design is ready, continue without asking for the same authorization again. A design-only request ends with the local preview; do not infer publication from "generate tema" alone.

## Choose the smallest change

- Start with `list_templates`, `get_template`, and `get_variant`. The last tool returns full config, including fields omitted by public variant reads.
- Prefer a new variant on the existing template. Clone its complete `value`, `images`, `custom_config`, and necessary metadata; preserve decoration/section IDs. Do not copy entity IDs, timestamps, relation objects, or `is_default=true` from the base.
- For supported color/font/image/content/layout changes, update data through the API. Do not edit web or backend merely to register another variant.
- For missing renderer behavior, extend the existing web family with an optional field and compatible default. Create a new family only when existing families cannot reasonably express the requested structure/interactions.
- Edit backend only for a demonstrated missing API, validation, authorization, ownership, or storage capability. Do not duplicate the web family registry in backend.
- For a content change that needs only one invitation, use supported invitation fields/overrides when creating its demo instead of creating another shared theme.

Before choosing or editing a family, read [theme-families.md](references/theme-families.md), then only that family's types/defaults/config loader. Follow the graph-first repo instructions for code discovery.

## Build and finish the local invitation

1. Choose the existing family and load a complete base config. Define the requested visual direction, content, sections, and interactions. For a demo, use clearly identified sample content; ask for missing real event details only when needed for the requested deliverable.
2. Prepare the full draft config and local assets. Preserve config shape, section IDs, and unrelated fields. For a cultural variant such as Aruma Aceh, make the requested identity visible in the composition and appropriate motifs/assets; renaming the base and changing its palette alone does not establish that the requested design is complete.
3. Render the draft using the actual family's renderer with local fixture data and asset URLs. Follow the bundled local-preview recipe and inspect current preview support; do not assume a generic local preview command exists. Use an existing local preview path when available, otherwise a temporary local harness that supplies draft data to the existing renderer. Do not introduce a production route or backend feature just for previewing. Studio covers only the families listed in the renderer reference. A standalone mockup can explore direction but cannot replace checking the actual renderer.
4. Inspect the complete invitation in a browser at mobile and desktop sizes, including opening the cover, scrolling every requested section, and exercising applicable navigation, audio controls, galleries, and form states without sending real RSVP/messages or triggering payment. Fix and recheck affected views until no known blocking visual or interaction issue remains.
5. Present an accessible local preview link/path and actual screenshots, with the checks performed and any limitations. Screenshots must come from the draft being delivered, not its base variant. If the user requests revisions, apply them locally and repeat the affected checks before upload.

"Finished" means the requested sections/content are present; final images and fonts load; text is readable without clipping/overflow on mobile and desktop; decorations and spacing are intentional; applicable interactions work; and no unresolved runtime errors affect the invitation. This is a verifiable readiness criterion, not a claim of absolute perfection. Do not call untested behavior verified. If browser/renderer access is unavailable, deliver the draft and state the missing verification; do not silently substitute a public demo for the required local review.

Retain a local handoff with the complete config, asset paths and intended config fields, preview evidence, and remaining issues (none blocking before upload). Remote payloads must use that reviewed config, with local asset references replaced by verified uploaded URLs. If the design changes materially, return to local review.

## Upload the finished design and create the demo

Start only after the local design is ready and the requested scope includes remote creation. For API contracts, recovery, and cache behavior, read [api-workflow.md](references/api-workflow.md).

1. Confirm the final payload against the full base variant. Preserve unrelated nested fields; `update_variant.value` replaces the entire stored value. Root section arrays and object configs must retain their original shape.
2. Upload final images using the connected transport: local stdio `upload_theme_asset(file_path)`, or remote `request_asset_upload` → user uploads through the returned link → `get_upload_result(ticket_id)`. For an already-public HTTPS source, remote also supports `upload_theme_asset_from_url(source_url)`. Remote cannot read local paths or chat attachments. JPEG, PNG, WebP, and AVIF are supported up to 20 MiB. Require `uploaded=true` and `public_accessible=true` before attaching `public_url`; a pending ticket is not success. Never stage assets on another provider to work around remote file access; use the internal S3 upload link or local companion.
3. If a new variant is needed, create it with the existing `template_id`, complete reviewed config, `is_default=false`, and `is_active=false` pending public verification. This is the finished local design, not a remote design draft. Keep the original variant unchanged unless the user specifically requests modifying it. For invitation-only content, use the existing variant and supported invitation overrides.
4. Create a demo with `create_admin_invitation`, the selected or newly created `variant_id`, and a unique `demo-...` slug. This creates an immediately public admin-owned invitation. The backend chooses owner and tier; there is no payment, email, or WhatsApp. Never send `user_id`, tier, payment fields, or credentials as tool arguments.
5. Check the exact new demo on mobile and desktop: correct family, images/fonts/colors, opening interaction, sections/navigation and runtime errors. Template preview API returns JSON; the base variant's preview URL does not verify the new variant. Studio preview exists for only five families.
6. After public QA, update a newly created variant's `preview_url` to the returned demo URL and `is_active=true` when catalogue publication is in scope. Verify image metadata and `is_free` deliberately; catalogue hides free/inactive variants. Do not change shared template metadata unnecessarily.
7. Lead with the visual result and working invitation URL, then report created IDs, actual code changes, and checks performed. If public QA failed or was unavailable, keep the new variant inactive and state the unresolved issue rather than claiming catalogue readiness. Preserve the finished local preview if upload or demo creation fails.


## Optional commit for code changes

- When the task changes or improves code, optionally commit the finished changes if the user requests it or has already authorized commits for the task. Do not ask again when that authorization exists. Otherwise leave the changes uncommitted and mention that they are ready for an optional commit.
- Before committing, run the relevant checks and update graphify if required by the owning repository, review the diff and Git status, and stage only task-related files or hunks. Preserve unrelated working-tree and staged changes; do not include secrets, temporary preview harnesses, or local-only artifacts. Report any unavailable check rather than claiming it passed.
- Commit in the repository that owns the changed code. For submodules, commit the relevant changes there first; include only the corresponding task-related submodule pointer updates in a superproject commit when that is within the authorized scope.
- Use a concise commit message describing the behavior changed or improved, then report the repository, commit hash, and validation results. A commit does not authorize pushing, merging, or deploying.
- Skip this step when the task only changed remote invitation/theme data or uploaded assets; do not create an empty commit.

## Failure and credential handling

- For remote MCP, enter the API key only on the Abadikan OAuth login page. For local stdio, keep it in the MCP checkout’s `.env.local` or process environment; the fullstack parent env is only an optional fallback. S3 credentials stay on the backend. Do not inspect or print secrets, put them in command arguments, or write them into frontend configuration.
- Do not auto-retry an uncertain write. For invitation creation, call `get_admin_invitation` with the original slug and check its variant ID before deciding to retry. For variants/templates, read back the catalogue/detail. Preserve successful earlier results when a later step fails.
- Fresh demo slugs avoid old invitation cache. Existing invitation/variant edits can remain stale for 300 seconds plus SWR; verify public freshness separately. Do not forge a JWT or bypass the existing cache-purge route.
- After code edits, run focused checks in the owning repository and `graphify update .` where required and available; report missing tooling. Do not deploy or create real customer invitations as a side effect of theme authoring.
