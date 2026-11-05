---
name: init-vercel-shop
description: Initialize a new Vercel Shop storefront from the vercel/shop template with create-next-app. Use when the user wants to create, scaffold, start, or initialize a Vercel Shop project from a coding agent.
---

# Initialize Vercel Shop

Ask for the target directory if the user did not provide one. Always pass it explicitly.

1. Inspect the target. If it already contains a Vercel Shop project, stop and use the relevant storefront skill instead. If it is a non-empty directory, ask for a different target rather than overwriting files.
2. Run:

   ```bash
   pnpm create next-app@latest <target-directory> --example https://github.com/vercel/shop
   ```

   The template pins pnpm 12 and Node.js 26.

3. Confirm the generated project contains `AGENTS.md`, `.agents/skills/`, `app/`, `components/`, `lib/shopify/`, and `package.json`.
4. Read the generated `AGENTS.md` before making further changes.
5. If dependency installation fails, keep the generated project and show the retry command to run from its root:

   ```bash
   pnpm install
   ```

6. Ask one optional follow-up: **Connect an existing Shopify store now?**

   If yes, ask only for the store's admin URL or `.myshopify.com` domain, then read [references/storefront-token.md](references/storefront-token.md) and follow its automated Shopify CLI flow. Try to reuse or create a public Storefront token before asking the user to visit the Headless channel.

   If no, finish with the normal environment setup as the next step.

Return the generated project path, whether a Shopify store was connected, and whether dependency installation needs a retry.
