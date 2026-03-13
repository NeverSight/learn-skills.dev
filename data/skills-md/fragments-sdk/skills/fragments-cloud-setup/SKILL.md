---
name: fragments-cloud-setup
description: Set up Fragments Cloud design governance in your project. Installs @fragments-sdk/govern, guides API key configuration, creates a governance config, runs your first check, and optionally adds CI/CD. Use when the user wants to add design governance, connect to Fragments Cloud, run design checks, or set up Fragments governance in their project.
disable-model-invocation: true
---

# Fragments Cloud Setup

Set up design governance with Fragments Cloud -- from zero to running checks with optional CI.

## 1. Detect project environment

- Confirm the project has a `package.json`. If not, ask if the user wants to initialize one.
- Detect the package manager from lock files:
  - `bun.lockb` or `bun.lock` -> bun
  - `pnpm-lock.yaml` -> pnpm
  - `yarn.lock` -> yarn
  - Otherwise -> npm
- Detect the framework (React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Astro) from dependencies.
- Check if `@fragments-sdk/ui` is already installed -- if so, note it and configure governance to work alongside it.

## 2. Install the governance SDK and CLI

First check if these are already available:
- In a **monorepo** with workspace dependencies (look for `"workspace:*"` or `"workspace:^"` in `package.json`), the packages may already be linked. Check if `@fragments-sdk/govern` and `@fragments-sdk/cli` appear in `dependencies` or `devDependencies`. If they're workspace deps, **skip the install step**.
- Also check if a `pnpm-workspace.yaml` or `workspaces` field exists in a parent directory -- if so, you're in a monorepo.

If not already installed:

```bash
<package-manager> add @fragments-sdk/govern @fragments-sdk/cli
```

The `govern` package provides the governance engine. The `cli` package provides the `fragments` binary used to run checks.

## 3. Configure the API key

**IMPORTANT: Never ask the user to paste their API key into the chat or accept it as an argument. Never write secrets directly.**

Instead, guide the user to set it themselves:

1. Tell the user to add their API key to `.env` (or `.env.local`) manually:
   ```
   FRAGMENTS_API_KEY=fc_your_key_here
   ```
   Say: "Add your Fragments Cloud API key to `.env`. You can find it in the onboarding dashboard or Settings > API Keys."

2. Ensure `.env` and `.env.local` are in `.gitignore`. Create `.gitignore` if needed.
3. Add `.agents/` to `.gitignore` if not already present (this is where installed skills live).
4. After the user confirms the key is set, verify it exists by checking that `.env` contains a `FRAGMENTS_API_KEY` line (do NOT read or output the actual value).

## 4. Create governance config

Create `fragments.config.ts` in the project root. Adapt the `input` glob to the detected framework:

```ts
import { defineConfig } from '@fragments-sdk/govern';

export default defineConfig({
  cloud: true,
  checks: ['accessibility', 'consistency', 'responsive'],
  input: './src/**/*.{tsx,jsx}',
});
```

Framework-specific `input` patterns:
- Next.js App Router: `['./app/**/*.{tsx,jsx}', './components/**/*.{tsx,jsx}']`
- Next.js Pages: `['./pages/**/*.{tsx,jsx}', './components/**/*.{tsx,jsx}']`
- Vue / Nuxt: `['./**/*.vue']`
- Svelte / SvelteKit: `['./src/**/*.svelte']`
- Astro: `['./src/**/*.{astro,tsx,jsx}']`

## 5. Run the first check

```bash
npx fragments govern check --cloud
```

Show the output. If there are violations, briefly explain what they mean and how to fix them.

## 6. Offer CI/CD setup

Ask: "Want to add Fragments checks to your CI pipeline? (GitHub Actions / GitLab CI / skip)"

### GitHub Actions

Create `.github/workflows/fragments-check.yml`:

```yaml
name: Fragments Design Check
on:
  pull_request:
    branches: [main, master]
permissions:
  contents: read
  pull-requests: write
jobs:
  design-check:
    name: Design Governance
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - name: Run Fragments checks
        run: npx fragments govern check --cloud --format github
        env:
          FRAGMENTS_API_KEY: ${{ secrets.FRAGMENTS_API_KEY }}
```

### GitLab CI

Add a `fragments-check` job to `.gitlab-ci.yml`:

```yaml
fragments-check:
  stage: test
  image: node:20
  script:
    - npm ci
    - npx fragments govern check --cloud
  variables:
    FRAGMENTS_API_KEY: $FRAGMENTS_API_KEY
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

After creating the CI config, remind the user to add `FRAGMENTS_API_KEY` as a secret in their CI provider settings.

## 7. Confirm completion

Summarize what was done:
- `@fragments-sdk/govern` and `@fragments-sdk/cli` installed
- API key configured in `.env` (remind them not to commit it)
- Governance config created at `fragments.config.ts`
- First check ran -- results visible in Fragments Cloud dashboard
- CI workflow created (if chosen)

Mention related skills:
- `/fragments-govern` to run checks, review staged changes, and fix violations
- `/fragments-policy` to create custom design rules
- If `@fragments-sdk/ui` is not installed, mention `/fragments-ui-setup` to add the component library
