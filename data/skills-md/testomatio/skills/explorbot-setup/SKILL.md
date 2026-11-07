---
name: explorbot-setup
description: Use to install Explorbot into a project — first-time setup, an `explorbot.config.js` in the repo, connecting an AI provider, teaching it how to log in, or when a command fails because the project has no config. Ends once `explorbot navigate` reaches the app.
license: MIT
metadata:
  author: Testomat.io
  version: 1.2.0
---

# Explorbot Setup

Install Explorbot into the user's project, connect a provider, teach it how to reach the app, and prove it with one navigation.

The config, the knowledge files, and the generated tests all land in the repo, so they are reviewed and versioned like the rest of the code. That is the point of installing locally.

**To run Explorbot without installing it into the project, this is the wrong skill** — [[explorbot-fundamentals]] covers that: `npx`, a provider, no project files.

**Scope ends when `npx explorbot navigate <path>` exits `0`** — exploring and testing belong to [[explorbot-fundamentals]].

## 1. Requirements

- Node ≥ 24 or Bun. If neither exists, stop — do not install a runtime.
- The generated config uses `import`, so `package.json` must be ESM. `npm init -y` produces CommonJS; if `"type"` is missing or `"commonjs"` in an existing file, ask before changing it, and write `explorbot.config.mjs` (passed as `--config`) if the user declines.
- Explorbot is for CRUD-heavy apps. Warn before installing if the target is a landing page, blog, CMS, or static site.

## 2. Install

```bash
npm pkg set type=module
npm i explorbot --save
npx playwright install chromium     # ~/.cache/ms-playwright, once per machine
npx explorbot init                  # writes explorbot.config.js, .env, output/
```

## 3. Provider

**Providers, model ids, and key variable names live in Explorbot, never in this skill.** The generated config ships one provider; `basics/providers.md` in the docs names the package and model ids for the others, and `models.json` holds the current recommendations.

- Ask which provider the user has an account with, and swap the import and the three model lines if it is not the one in the template.
- `npm i` the matching provider package.

The key: ask the user to paste it into `.env` in their editor and say "continue", then verify with `grep -q "^<KEY>=." .env`. Confirm `.env` is gitignored. Never echo a key back.

`~/.explorbot/.env` is also read on every run, filling in variables the project `.env` does not set.

## 4. App URL

Ask for it, and write it to `web.url` in the config — host only, no path. Explorbot clicks, fills, and submits on its own, so staging beats production.

Do not guess it. Look for evidence in the project — `package.json` scripts, `.env` files, framework ports — and suggest what you find with its source. Otherwise ask in plain text. Never propose a URL from this skill or from memory.

## 5. Verify

Walk the rungs in order. Stop at the first failure, fix it, resume.

1. `curl -sS -o /dev/null -w "%{http_code}\n" <url>` — `000` is DNS/VPN/wrong host, `5xx` is the app itself, `200` skips to rung 3.
2. `curl -sIL -o /dev/null -w "%{url_effective}\n" <url>` after a `3xx`/`401`/`403`. A login-looking final URL means credentials are needed: do rung 4 first.
3. `npx explorbot navigate <path> --session` — exit `0` ends setup. `--session` saves cookies to `output/session.json`. On exit `1`, read `output/explorbot.log`: an auth wall sends you to rung 4, anything else is a wrong path or a broken page.
4. Teach auth, knowledge first, values second:

   ```bash
   npx explorbot knows /login      # reuse existing variable names if auth knowledge exists
   npx explorbot learn "/login" 'Sign in with ${env.APP_USER} / ${env.APP_PASSWORD}'
   ```

   Name only the credentials — no selectors or DOM hints; the Navigator finds the fields. Then have the user add the two variables to `.env`, verify with `grep`, and repeat rung 3. Ask for a test account on a non-production environment.

   Still failing on auth: add one sentence to the knowledge with `learn` (real form URL, SSO, second factor), never a rewrite.

`npx explorbot context <path>` prints headings, matched knowledge, and interactive elements with no AI calls — use it to debug a rung for free.

## 6. Handoff

Report what the project now has: `explorbot.config.js`, `.env` (gitignored), `knowledge/`, `output/` with a saved session. Then hand off to [[explorbot-fundamentals]] with a first command:

```bash
npx explorbot explore /<crud-page> --max-tests 10
```

## Anti-patterns

- Installing into the project when the user only wanted to try Explorbot — that is [[explorbot-fundamentals]].
- Naming providers, model ids, or key variables without reading them from the docs or the generated config.
- Putting secrets in knowledge files or config — always `${env.NAME}`, values in `.env`.
- Driving `explorbot start` — it is an interactive TUI; ask the user to run it.
- Asking upfront for target pages, features, or test counts.
