---
name: zitadel-components
description: >-
  Embed, theme, customise, or drive the Zitadel login web component directly —
  the framework-agnostic `<zitadel-login>` / `<zitadel-logout>` Lit elements
  from `@zitadel/components`. Use when dropping the login widget onto a plain
  HTML page, styling it with `--zl-*` design tokens or `::part(...)` hooks,
  pinning its theme/variant/locale, wiring its flow events, or automating it in
  a browser via its shadow-DOM hooks — i.e. using the Zitadel login widget
  itself, outside any framework SDK wrapper.
---

# @zitadel/components

Lit web components for the Zitadel auth UI: the `<zitadel-login>` orchestrator
(a drop-in element that calls the flow API and renders every step),
`<zitadel-logout>` / `<zitadel-session>`, and the `<zl-*>` atoms.

## When to use

Use this skill when you embed, theme, or automate the login/logout web
component **directly** — on a static page, in a server-rendered app, or inside
any shell where you hold the custom element yourself. The framework SDK skills
(Next, Nuxt, React, etc.) wrap this same element for a specific framework; reach
for those when the user is in that framework. Reach for this one when the work
is the component itself: attributes, tokens, parts, events, shadow-DOM hooks.

## Install / use

```sh
corepack pnpm add @zitadel/components@latest
```

`lit`, `liquidjs`, `dompurify` are externalised peer/runtime deps (consumers
dedupe their own copies). A CDN `standalone` build is published (`unpkg` /
`jsdelivr` → `./dist/standalone.mjs`). Subpath exports exist for `./atoms`,
`./orchestrator`, `./tokens`, `./manifests`, and JSX types at `./jsx`. Importing
the barrel side-effect-registers every element; import leaf subpaths to
tree-shake.

## Embed & configure

Configure the SDK once, then drop the element — it reads the global project
handle from `configureZitadel()` via `getZitadelConfig()`:

```html
<script type="module">
  import '@zitadel/components';
  import { configureZitadel } from '@zitadel/api/config';
  configureZitadel({ projectId: 'proj_123', proxyPath: '/__nextgen' });
</script>
<zitadel-login id="login" variant="page" purpose="login"></zitadel-login>
```

`<zitadel-login>` props (the authoritative list is in the README table and the
TS types — discover, don't assume): `variant` (`widget` default: content-sized,
transparent, no font injection, no focus grab / `page`: full-page chrome),
`theme` (`light`/`dark`/`auto`, resolved value lands on `data-theme`), `purpose`
(`login`/`register`/`reset_password`/…), `flow-name`, `project` (object property,
not an attribute — assign via `ref`/JS, not markup), `lang` + `locales`,
`post-sign-in-url` (`force-post-sign-in-url`: see below), `resume-flow-id`,
`preview-state` / `preview-success-step`.
After sign-in the widget returns to the path in the page's `next` query
parameter, which every server SDK's middleware sets when it sends a signed-out
visit to a protected route to the login page, and goes to `post-sign-in-url`
when there is none or it is not a path on the page's origin. A page that uses
`next` for something of its own sets `force-post-sign-in-url`.
It emits `zitadel-flow-input`, `-step`, `-complete`, `-error`, `-redirect`
events (`-step` fires for every step including the first; `-redirect` is a
non-cancelable notification — the widget navigates to the IdP itself).

`<zitadel-logout>`: `project`, `post-sign-out-url`; supports a light-DOM
`<template>` slot for a custom menu.

Theming levers (strongest-first resolution, documented in the README):

- **Host CSS tokens** — set `--zl-*` custom properties in your own stylesheet on
  `zitadel-login { ... }`. These inherit across shadow boundaries and **outrank**
  both the design-system defaults and server-side tenant branding. The stable
  names are listed in
  [Customize the login design](https://preview.zitadel.com/docs/guides/customize-design.md).
- **`::part(...)`** — e.g. `zitadel-login::part(form)`, `::part(field-input)`,
  `::part(button-root)`. Atom parts forward through the orchestrator as
  `<atom>-<part>`; bare names (`zl-field::part(input)`) apply when composing
  atoms directly.
- **`variant` + `--zl-page-min-height`** for sizing/placement; width-responsive
  chrome keys off the widget's own width (container queries).
- Server branding payload, and a tenant Liquid template via the payload's
  `liquid_template` field (a declarative `template` attribute is not yet
  exposed).
- **`suppress-header`** (boolean attribute, reflected) hides the widget's own
  heading — use it when the host page already shows a title and you want to
  avoid a duplicate. The login moves between sign-in and sign-up by itself, so
  that title must follow its `zitadel-flow-step` event: `step.purpose` is
  `login` or `register`.
  Otherwise control chrome through `variant` and tokens.
- **`suppress-password-toggle`** (boolean attribute) hides the show/hide button
  the login shows on password fields by default. It applies to custom Liquid
  templates too; templates have nothing to wire.

Automation hooks (stable `data-testid`s the default template emits): host atoms
`zitadel-field-email` / `zitadel-field-password` / `zitadel-action-submit`;
native shadow controls `zitadel-input-email` / `zitadel-input-password` /
`zitadel-action-submit-button`. Hooks are method-named even when the flow engine
names a credential field `x-auth-methods#<method>` — the `name` attribute keeps
the raw wire key; only the hook is normalised (`hookName` in
`src/internal/hook-name.ts`). For sign-out, the button inside `<zitadel-session>`
(the signed-in card setup's profile pages render) carries
`zitadel-session-logout`, and its native button `zitadel-session-logout-button`.
`<zitadel-logout>` has no hook: open its avatar menu ("Open user menu"), then
pierce to `.signout-btn`. Given a `<template>` child, it shows no menu, and the
element marked `data-action="logout"` signs out.

## Read these, don't guess

The component surface moves faster than any list here, so treat these as
authoritative and discover the current shape first:

- `node_modules/@zitadel/components/README.md` — the element API tables, the
  customisation tiers, and the **canonical hook list** live here.
- The published TypeScript types (`./dist/index.d.mts` and the `./atoms`,
  `./orchestrator`, `./tokens`, `./jsx` subpaths) — exact prop/event/manifest
  shapes.
- [Customize the login design](https://preview.zitadel.com/docs/guides/customize-design.md)
  — the stable `--zl-*` tokens and the `::part()` names the login forwards.
- Per-atom manifests (`@zitadel/components/manifests`) — the allowed
  attributes/parts/events for each atom.

Read the pattern, then confirm the specific attribute/part/token/event against
these before writing it — don't reproduce a catalogue from memory.

## Gotchas

- **Server rendering.** If your app renders on the server, mount the widget on the client only, after hydration, or give a raw `<zitadel-login>` element `project-id` and `proxy-path` as attributes, because a widget that starts before its configuration arrives shows an error instead of the flow.
- **Open shadow roots, nested.** The automation hooks sit inside nested shadow
  roots, so a flat `document.querySelector('[data-testid="zitadel-input-email"]')`
  misses them. Use a shadow-aware locator (Playwright) or recurse through
  `el.shadowRoot`. Enter submits the step only for key events carrying
  `key: "Enter"`; CDP wrappers that omit it should click `zitadel-action-submit`.
- **Same-origin proxy.** The element calls the typed `@zitadel/api` fetch client
  directly with `credentials: "include"`; the stateless server's `_zflow`
  HttpOnly cookie is the source of truth between requests. There is no transport
  to swap — mock at the network layer (`@zitadel/api-mock` MSW handlers) for
  offline/test.
- **Theming through shadow DOM.** `--zl-*` custom properties inherit across
  shadow boundaries, so host-page token overrides reach the atoms' own shadow
  roots and win over `:host` defaults and server branding — deliberate, so an
  embedding app matches its design system without a server round-trip. Internals
  you can't reach with a token need `::part(...)`, not a descendant selector.
- **`project` is a property, not an attribute** — it's a typed object, so set it
  via JS/`ref` (or configure globally and let the element read it), never as
  markup.
