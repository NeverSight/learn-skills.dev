---
name: zitadel
description: >-
  Add, configure, and manage Zitadel authentication in a project. Start here for
  any Zitadel task — it routes to the right skill: the `zitadel` CLI for creating
  projects, scaffolding, config, deploys, and the local server, and the
  per-framework SDK skills for integrating the auth UI into a Next.js, React,
  Angular, Nuxt, Vue, Solid, Svelte, Qwik, SvelteKit, SolidStart, Qwik Router, or
  TanStack Start app. Also use to answer questions
  about Zitadel — its concepts, configuration, CLI, SDKs, or API — from the
  official docs. Use whenever the user mentions Zitadel, adding
  login/registration/sessions, or authentication in their app.
---

# Zitadel

This is the entry point for Zitadel work. The full set of Zitadel skills
installs together with `npx skills add zitadel/nextgen --full-depth`; this
router then points you at the right one for the task. If a skill named below is
not actually installed, the set was added without `--full-depth` — install it
that way to get the CLI and per-framework skills alongside this router.

## Route by what you are doing

- **Create a project, scaffold a new app, change config, deploy, or run a local
  Zitadel server** → use **`zitadel-cli`**. It drives the `zitadel` CLI
  (`setup`, `plan`, `apply`, resource commands). It can scaffold a fresh app for
  any framework below and integrate an **existing** app on any of them.

- **Integrate the auth UI into an app** → use the SDK skill for that framework:
  - Next.js → **`zitadel-sdk-next`**
  - React (including Vite SPAs and TanStack) → **`zitadel-sdk-react`**
  - Angular → **`zitadel-sdk-angular`**
  - Nuxt → **`zitadel-sdk-nuxt`**
  - Vue → **`zitadel-sdk-vue`**
  - Solid → **`zitadel-sdk-solid`**
  - Svelte → **`zitadel-sdk-svelte`**
  - Qwik → **`zitadel-sdk-qwik`**
  - SvelteKit → **`zitadel-sdk-sveltekit`**
  - SolidStart → **`zitadel-sdk-solid-start`**
  - Qwik Router → **`zitadel-sdk-qwik-router`**
  - TanStack Start → **`zitadel-sdk-tanstack-start`**

- **Embed, theme, or drive the `<zitadel-login>` web component directly** → use
  **`zitadel-components`**.

## The rule that spans all of them

The CLI can **scaffold** a fresh app for every framework above and **integrate
(patch) an existing app** on each of them: `setup` detects the framework and
writes the routes, request boundary or root component, and stops with
`E_CONFLICT` rather than overwrite a file of the app's. It leaves an app it does
not support unchanged: a Next.js Pages Router app, a React app without Vite, or
a framework older than setup supports
([Add Zitadel to an existing app](https://preview.zitadel.com/docs/get-started/existing-app.md)
lists the versions). For those, reach for that framework's SDK skill and add
auth by hand: install `@zitadel/sdk-<framework>@latest`, configure it, add the
provider/guard/routes, and drop in the login component.

Each skill points you at the package's real README and TypeScript types for exact
APIs — read those rather than guessing, since they move with the package version.

## Zitadel documentation

The Zitadel docs cover what these skills do not: what each concept means and
how the pieces fit together. Read them to answer a question about Zitadel, to
understand a term or error before acting on it, or to check a claim you are not
sure of. Do not answer Zitadel questions from memory or training data; the
product is in preview and changes quickly.

The docs are organised into these sections:

| Section       | What it covers                                                              |
| ------------- | --------------------------------------------------------------------------- |
| Get started   | The quickstart, an existing app, and driving the CLI as an agent            |
| Guides        | Local runtime, `plan`/`apply`, social sign-in, login design and copy        |
| Concepts      | Projects, teams, users, config as code, flows, schemas, sessions, databases |
| SDKs          | One page per framework SDK, the SDK proxy, the API client, components       |
| CLI reference | Every `zitadel` command with its flags and examples, by command group       |
| API reference | Every REST endpoint, grouped by resource                                    |

### Finding the right page

Look the page up before you fetch it — don't guess URLs. The index lists every
page's Markdown URL with a one-line description:

```
https://preview.zitadel.com/docs/llms.txt
```

Links in the index are relative to the docs site, so prefix them with
`https://preview.zitadel.com`. Fetch only the pages you need. Do not
fetch `llms-full.txt`: it is the whole site in one file and costs far more
context than the one or two pages a question needs.

### Fetching a page as Markdown

The index's links are already the Markdown. For a page URL from elsewhere, add
`.md` to get it as Markdown instead of HTML, for example
`https://preview.zitadel.com/docs/concepts/databases.md`.

### How far to trust the docs

The docs are written for the latest Zitadel release and are a good guide to how
Zitadel works, but they can lag behind or run ahead of the version the user has
installed: a flag, option, or field may have been renamed, added, or removed.
When the docs and the installed package disagree, the installed package wins —
check its README and TypeScript types, or the CLI's own `--help` output, and
tell the user when the docs are out of step with what you found.
