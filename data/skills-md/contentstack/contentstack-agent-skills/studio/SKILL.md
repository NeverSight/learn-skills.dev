---
name: studio
description: "Contentstack Studio router: loads one of the bundled specialist guides per task (SDK install, project provisioning, component registration, sections and templates, data binding, canvas and preview routes, publishing, troubleshooting). Use when the user mentions Contentstack Studio or its concepts: the Studio SDK, canvas, compositions, Connected or Freeform templates, sections, section slots, repeaters, registering components, BYOC, Studio preview routes, or making a project Studio-ready. Do not use for general Contentstack CMS, Live Preview, Visual Editor or Launch questions that do not involve Studio."
---

# Studio router

You are working on Contentstack Studio. The pack has one specialist skill per task, covering install, provisioning, component registration, section/template authoring, data binding, preview wiring, verification, troubleshooting, and migration.

This SKILL.md is the only file loaded up front. Everything else is routed through `skills-index.md`.

## Resolving a skill file

The specialist guides sit next to this file, in the same folder: a skill named `<name>` is `<name>.md` beside this SKILL.md, and the lookup table is `skills-index.md` in the same folder. Every cross-reference in this file and in `skills-index.md` is written as `<name>` or `<name>.md`. Resolve all of them this way.

Fallback: if `<name>.md` isn't there, try `../<name>/SKILL.md` (a host that installed each guide as its own skill folder).

**If neither resolves, say so out loud**: "the Studio skill pack looks mis-installed, `<name>` didn't resolve", and do NOT quietly fall back to general knowledge. A silent fallback looks identical to the pack working, so the user never learns their install is broken.

## What to do

**Setup intent takes precedence over keyword matching.** “Enable Studio”, “make this project Studio ready”, “Studio setup”, and equivalent whole-app requests run `convert-project-to-studio` through verification. `install-studio` alone is for an explicit SDK-only request. Preserve the active setup objective across replies such as “yes”, “start”, and “OAuth done”; resume the pending step rather than routing that reply as a new task. Use the orchestrator's scoped completion checklist; authoring requirements below apply only when components or compositions are authored.

**Discover MCP execution before resolving raw HTTP credentials.** Follow `install-contentstack-mcp` to inspect callable tools in the current host and verify the target with a read call. A stored OAuth session is not evidence of a connected MCP server. Prefer available MCP operations; use OAuth HTTP for missing operations or an explicitly recorded connection limitation. Never infer tool availability solely from a conversation flag.

1. Read `skills-index.md` (in this folder). It has two parts.

2. **Trigger table.** Scan the user's most recent message against the phrases in the left column. If one row matches, Read that skill's file and follow it. If several match, run them in the order the table implies (installs before authoring, `analyze-project-fit` before anything state-changing).

3. **Topic map.** Use this when no trigger phrase fires but the topic is Studio-shaped. The user is exploring or asking a conceptual question. Pick the closest skill by name + one-liner and Read it.

4. If nothing matches after both passes, answer from general Studio knowledge, but say so, and check whether a skill is missing that should exist.

## Standing rule: atomic and reusable, every time

**This applies on every Studio turn, whatever the user asked for. It is not optional and it is not only a planning concern.**

Before creating, registering, or authoring anything:

1. **Decompose first.** Never register or build a component that renders more than one piece of content. The test: does it render more than one heading / image / body / list? If yes, run [`decompose-jsx-to-atomics`](decompose-jsx-to-atomics.md) before anything else. One Section per page, or one component swallowing a whole page, is a defect, not a shortcut.
2. **Compose from atoms by default: do NOT reach for a pre-composed composite.** A palette usually contains both **atoms + layout primitives** (`*-atom-heading`, `*-stack`, `*-row`, `*-grid`, `*-section-shell`) and **composites** that already bundle a whole shape (`*-feature-card`, `*-hero`, `*-card-grid`). Dropping one composite is faster and looks identical on the canvas, and it is the wrong default: its internals are fixed in code, so the author cannot restructure it, the spacing inside it cannot be matched to a comp, and the design is no longer expressed as a composition. **Build the shape out of atoms unless the user explicitly asks to reuse an existing component.** If a composite would clearly save real work, say so and let them choose. Do not decide it silently.
3. **Reuse atoms, not shapes.** Reuse means the same `*-atom-heading` everywhere, not a ready-made card. Two things differing only in spacing are one Section plus an exposed prop, never two.
4. **Shared shells are Sections.** Header, footer, nav, menus, breadcrumbs render on every page and are the highest-value reusable pieces in any project. They are never "atomic, no binding". Their menus are **Repeaters over a field**, never hardcoded lists. Otherwise an author cannot add a menu item without a developer.
5. **One atomic prop maps to one CT field.** A single prop taking a whole object is how binding breaks: the binder recursively unwraps single-key objects for every type except `object`/`array`, so a coarse prop renders blank with no error.

If the user's request would skip this ("just register the page component", "make the whole page one section"), say what it costs (nothing reusable, authors can't reorder, bindings break) and propose the decomposed shape instead. Do it their way only if they confirm after hearing that.

## Standing rule: definition of done

**Also every Studio turn.** Eight deliverables decide whether what you built is usable by a marketer rather than only by a developer. Every one fails silently. The page still renders, nothing errors, and the gap surfaces only when a non-developer opens Studio:

1. `cslp: { appendTags: true }` in the SDK init, once per project.
2. `studioAttributes` on the root + `wrap: false` in the register entry + `$prop` twins, **every** registered component.
3. `thumbnailUrl`, **every** `registerComponent` call.
4. `ui_preview`, **every** Section composition. The editor writes this for itself by screenshotting the canvas on save. **A CMA-authored Section has it empty forever** unless you supply an asset uid explicitly. So "at write time" means have the asset ready and include it, not "the create call handles it". See [`author-composition-via-api`](author-composition-via-api.md) § Section thumbnails for the three ways to do it. Scripted authoring is exactly where this gets skipped, and the only signal is a blank tile in the palette.
5. Live Preview enabled on the stack + preview token, once per project.
6. The `/canvas` route mounted, once per project.
7. **Published** to the environment the project targets, every Section and Template, and again after every tree edit. Delivery otherwise serves the old version while the CMA and canvas both look correct.
8. **Composed of Sections**: every Template. Read the saved composition back and count `section-composition` nodes. Zero means the page is one component bound to the whole body. The standing rule above already forbids that shape, and a build still reached it, because a monolith renders correctly and fails no other check here. Counting is the only thing that catches it.

Read [`complete-the-build`](complete-the-build.md) for the how and the verification block. The runnable node count is in [`build-connected-template`](build-connected-template.md) § Post-build structural check. Never report a build done with any of these outstanding. Say "created, thumbnail pending" and then finish it. State them in the plan up front too, so what the user approves is what they get.

## Standing rule: auth preflight

**Settle the credential before the first API call of the turn, not when one fails.** Every specialist repeats this. It lives here because it must hold even before a specialist is pulled.

1. Resolve OAuth-first per [`authenticate-cma`](authenticate-cma.md): `CS_OAUTH_ACCESS_TOKEN`, else the Contentstack MCP's stored session (`~/Library/Application Support/ContentstackMCP/oauth-config.json` and its platform equivalents). **Ask the user before reading or refreshing that stored session**: it is their credential, and refreshing it rotates the refresh token, which can sign the MCP server out (its next refresh fails with `400 invalid_refresh_token`) unless the new pair is written back.
2. **Don't ask for a session `authtoken` up front.** It is a full user-session credential: every org, stack and permission the user holds. It is the last rung of the [`authenticate-cma`](authenticate-cma.md) ladder, considered only after a freshly refreshed OAuth token has been observed to fail. Prefer `csdx auth:login --oauth` or finishing the step in the Studio UI, and explain the risk before asking for one.
3. Access tokens last **59 minutes** and refresh tokens **rotate**. Tooling that refreshes must persist the new pair. A bare `curl` loop does neither, so long work belongs in a script.
4. If nothing resolves, or a refresh returns `400 invalid_refresh_token`, hand the user `! CONTENTSTACK_REGION=<code> npx @contentstack/mcp --auth` and wait. It needs a TTY and a browser, you cannot run it for them. The region must be **in** the command. `DEFAULT_REGION` is `NA`, so omitting it silently authenticates against NA prod.
5. `403 error_code 316` is **not** an auth failure. It is a valid credential aimed at a stack outside its org. Re-authenticating fixes nothing. Check with `GET /v3/stacks` + `organization_uid`.

## Rules

- Always re-Read the skill file. Never answer from a remembered summary. The source of truth is the file on disk.
- **A failed Read is a hard stop, not a shrug.** If a skill file won't resolve (see § Resolving a skill file), report it. Improvising over a broken install is worse than erroring: the user believes the pack ran when it didn't.
- Never skip step 1. The lookup is cheap. Missing a skill is expensive.
- If the user's request implies multiple skills (e.g. "install and set up preview routes"), pull each in the order they must run: skills-index.md's Trigger table encodes that ordering.
- Prerequisite skills: many authoring skills assume `install-studio` + `configure-studio` are done. If the user's project state is unclear, run `analyze-project-fit` first.

## Security

### Defaults

- Resolve credentials OAuth-first (see § Standing rule: auth preflight). Ask before reading or refreshing another tool's stored OAuth session.
- Delivery and preview tokens may reach the browser; management tokens, OAuth tokens and session authtokens never do.
- Never disable TLS certificate or hostname verification, and never ship permissive frame headers (`frame-ancestors *`, `Access-Control-Allow-Origin: *`) outside local development or the canvas route.

### Destructive Actions

Creating or changing stacks, content types, entries, compositions or Studio projects is a real mutation. State what will change and get confirmation first. Never delete or overwrite existing content, sections or templates without explicit approval.

### Secrets

Never print, echo or store tokens, API keys or `.env` values, in chat, logs or files. If a secret appears in input, don't repeat it; recommend rotating it.

### Environment Variables

Use descriptive placeholders such as `CONTENTSTACK_API_KEY`, `CONTENTSTACK_DELIVERY_TOKEN`, `CONTENTSTACK_PREVIEW_TOKEN` and `CS_OAUTH_ACCESS_TOKEN`, and keep real values in a gitignored `.env`.
