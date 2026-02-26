---
name: launch
description: Self-contained SaaS pipeline — invoke directly, do not decompose.
  Generates a Vibes app, adds auth + billing, and deploys live. Uses Agent Teams
  to parallelize for maximum speed.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Task, Teammate, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet
compatibility: Requires Claude Code with Agent Teams support
metadata:
  author: "Marcus Estes"
  version: "0.1.63"
---

> **Plan mode**: If you are planning work, this entire skill is ONE plan step: "Invoke /vibes:launch". Do not decompose the steps below into separate plan tasks.

**Display this ASCII art immediately when starting:**

```
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒ ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓████████▓▒░
░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░▒▓█▓▒░░▒▓█▓▒░
```

## Notation

**Ask [Header]**: "question" means call AskUserQuestion with that header and question. Options listed as bullets. User can always type custom via "Other". When collecting a key/secret, put one option like "Paste key" — the user types the actual value via Other.

For architecture context, see `LAUNCH-REFERENCE.md` in this directory.

---

## FIRST: Terminal or Editor UI?

**This is the very first question — ask before anything else.**

Ask the user:
> "How do you want to build? **Terminal** (I'll generate and deploy from here) or **Editor** (opens a browser UI with live preview, chat, and deploy button)?"

- **If Editor**: Start the editor server. If the user already described what they want to build (e.g., `/launch a dogs app`), pass it via `--prompt`:
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/preview-server.js" --mode=editor --prompt "USER_PROMPT_HERE"
  ```
  If no prompt was given, omit `--prompt`:
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/preview-server.js" --mode=editor
  ```
  Tell the user: "Open http://localhost:3333 — the editor handles everything from here: describe your app, preview it live, switch themes, and deploy with one click."
  **Then stop.** The editor UI takes over the entire workflow (setup, generation, preview, deploy). Do not continue with the phases below.

- **If Terminal**: Continue with the pre-flight checks and normal workflow below.

---

## Pre-Flight Decision Tree

Run all five checks before collecting any input:

| # | Check | Command | If True |
|---|-------|---------|---------|
| 1 | .env has Clerk keys + Connect URLs | `grep -qE '^VITE_CLERK_PUBLISHABLE_KEY=pk_' .env && grep -qE '^VITE_API_URL=' .env && grep -qE '^VITE_CLOUD_URL=' .env` | Set `CONNECT_READY`. Read .env for clerkPk. Skip T2, T3, infra spawn. |
| 2 | .env has admin user ID | `grep CLERK_ADMIN_USER_ID .env` | Store value. Skip Phase 3. |
| 3 | app.jsx exists | `test -f app.jsx` | **Ask [Reuse]**: "app.jsx exists. Reuse it or regenerate?" If reuse: skip T1. |
| 4 | Wrangler authenticated | `npx wrangler whoami 2>&1` | If NOT authenticated: tell user to run `npx wrangler login` and wait. |
| 5 | SSH key exists | `ls ~/.ssh/id_ed25519 ~/.ssh/id_rsa ~/.ssh/id_ecdsa 2>/dev/null` | If missing AND not CONNECT_READY: warn about Connect deploy. |

## Phase 0: Collect Inputs

### 0.1 App Prompt

**Ask [App prompt]**: "What do you want to build? Describe the app you have in mind."
- "Todo list" — A simple task manager with categories and due dates
- "Photo gallery" — A shareable photo gallery with albums and captions
- "Team dashboard" — A metrics and status dashboard for small teams

Store as `appPrompt`.

### 0.2 App Name + Domain

**Ask [App name]**: "What's the app name? (used for subdomain + database)" AND **[Domain]**: "Where will this be deployed?"
- App name: "Derive from prompt" or "Let me specify"
- Domain: "Cloudflare Workers (Recommended)" or "Custom domain"

If "Derive from prompt": generate URL-safe slug (lowercase, hyphens, max 30 chars). If "Custom domain": ask for domain name. Store as `appName`.

Resolve Workers URL (if Cloudflare):
```bash
node "{pluginRoot}/scripts/lib/resolve-workers-url.js" --name "{appName}"
```
Store output as `domain`. If script fails, ask for their Cloudflare subdomain and construct `{appName}.{subdomain}.workers.dev`.

### 0.3 AI Features (conditional)

Scan `appPrompt` for AI keywords: "chatbot", "chat with AI", "summarize", "generate", "analyze", "AI-powered", "intelligent".

If detected: **Ask [AI features]**: "Does this app need AI features?"
- "Yes — I have an OpenRouter key" — I'll paste my API key
- "Yes — I need to get one" — I'll sign up at openrouter.ai
- "No AI needed" — Skip AI capabilities

If yes: check `grep OPENROUTER_API_KEY ~/.vibes/.env`. If found, offer reuse (mask key). Otherwise collect via Ask and offer to cache to `~/.vibes/.env`. Store as `openRouterKey` (or null if no AI).

### 0.4 Theme Selection

Theme switching is handled by the live preview wrapper, not inside the app. The builder generates a single-theme layout. Set `themeCount = 1`.

---

## Phase 1: Spawn Team & Parallel Work

### 1.1 Setup

1. Resolve plugin root: `echo "${CLAUDE_PLUGIN_ROOT}"` → store as `pluginRoot`
2. Create team: `TeamCreate("launch-{appName}", "Full SaaS pipeline for {appName}")`
3. Create all tasks per the table in LAUNCH-REFERENCE.md. If `CONNECT_READY`: mark T2+T3 completed immediately.

### 1.2 Spawn Builder (T1)

1. Read `{pluginRoot}/skills/launch/prompts/builder.md`
2. Substitute: `{appPrompt}`, `{appName}`, `{pluginRoot}`
3. Set `{aiInstructions}`: if `openRouterKey` is set, add rule about `useAI` hook (see vibes SKILL.md "AI Features"). If null, leave empty.
4. Spawn: Task tool, `team_name="launch-{appName}"`, `name="builder"`, `subagent_type="general-purpose"`

### 1.3 Clerk Credentials (T2) — simultaneous with builder

**Skip entirely if CONNECT_READY.**

**Ask [Clerk app]**: "Do you have a Clerk app configured?"
- "I have one ready" — Already has passkeys and email auth
- "I need to create one" — Walk me through setup

If creating new: guide through clerk.com/dashboard — create app, enable Email + Passkey, configure email settings (require OFF, verify ON, link ON, code ON). Then set up JWT template and webhook:

**Ask [Clerk config]**: "Complete these two setup steps in Clerk Dashboard:\n\n1. **JWT Template**: JWT Templates → New Template → name it `with-email`, paste this JSON as the custom claims (the `|| ''` fallbacks are required — Fireproof Studio rejects null names):\n```json\n{\n  \"params\": {\n    \"email\": \"{{user.primary_email_address}}\",\n    \"email_verified\": \"{{user.email_verified}}\",\n    \"external_id\": \"{{user.external_id}}\",\n    \"first\": \"{{user.first_name || ''}}\",\n    \"last\": \"{{user.last_name || ''}}\",\n    \"name\": \"{{user.full_name || ''}}\",\n    \"image_url\": \"{{user.image_url}}\",\n    \"public_meta\": \"{{user.public_metadata}}\"\n  },\n  \"role\": \"authenticated\",\n  \"userId\": \"{{user.id}}\"\n}\n```\n2. **Webhook**: Webhooks → Add Endpoint → URL `https://{domain}/webhook` → subscribe to `subscription.deleted`\n\nHave you completed both?"
- "Yes, both done" — JWT template 'with-email' with email/name claims + webhook endpoint created
- "I need help" — Walk me through it step by step

Collect four credentials via Ask (user types actual values via Other):

**Ask [Clerk PK]**: "Paste your Clerk Publishable Key (starts with pk_test_ or pk_live_)"
- "Paste key" — From Clerk dashboard > API Keys. Validate prefix.

Repeat pattern for:
- **[Clerk SK]**: Secret Key — starts with `sk_test_` or `sk_live_`
- **[PEM Key]**: JWKS PEM Public Key — from API Keys > Advanced > Public Key. Starts with `-----BEGIN PUBLIC KEY-----`
- **[Webhook Secret]**: From Webhooks > endpoint > Signing Secret. Starts with `whsec_`

Save PEM to file:
```bash
cat > clerk-jwks-key.pem << 'PEMEOF'
{pemKey}
PEMEOF
```

Mark T2 completed.

### 1.4 Spawn Infra (T3) — after T2 completes

**Skip if CONNECT_READY.**

1. Read `{pluginRoot}/skills/launch/prompts/infra.md`
2. Substitute: `{appName}`, `{pluginRoot}`, `{clerkPk}`, `{clerkSk}`
3. Spawn: Task tool, `team_name="launch-{appName}"`, `name="infra"`, `subagent_type="general-purpose"`

### 1.5 Sell Config (T4) — while infra deploys

**Sell config is collected here but applied later by invoking `/vibes:sell` (or its assembly script) as an atomic step.** Do NOT hand-implement SaaS logic — the sell skill handles tenant routing, auth gating, billing, and admin setup.

Choose billing mode based on monetization intent:
- **"off" (free)** — all authenticated users get full access. Good for MVPs and internal tools.
- **"required" (subscription)** — users must subscribe. Requires Clerk Billing (Dev instances auto-connect to Stripe sandbox).

**Always ask the user** — do not assume a default.

**Ask [Billing]**: "What billing mode for your SaaS?" AND **[Title]**: "App display title?"
- Billing: "Free (no billing)" or "Subscription required"
- Title: "Derive from app name" or "Let me specify"

**If billing is "Subscription required"**: Note that Clerk Billing must be configured in the Clerk Dashboard after deploy (plans, Stripe connection). Dev instances auto-connect to Stripe sandbox for testing.

**Ask [Tagline]**: "Describe your app's tagline (short punchy phrase)"
- "Generate one" — Create from app description
- "Let me write it" — I'll provide it

**When billing is "required"**: These fields appear on a pricing section visible to potential customers before signup. Optimize for marketing copy quality — benefit-driven language, not technical descriptions. Tagline = sales headline. Subtitle = value proposition ("why should I pay?"). Features = compelling benefit statements (3-5 items).

Repeat pattern for subtitle and features list (3-5 bullet points).

Store: `billingMode` ("off"/"required"), `appTitle`, `tagline`, `subtitle`, `features` (JSON array). Mark T4 completed.

---

## Phase 2: Assembly & Deploy

**Blocked by T1 + T3 + T4.** Check TaskList until all complete.

### 2.1 Verify Inputs

Confirm: `app.jsx` exists with valid JSX. `.env` has `VITE_CLERK_PUBLISHABLE_KEY`, `VITE_API_URL`, `VITE_CLOUD_URL`. All sell config values collected.

Scan app.jsx for builder mistakes (see LAUNCH-REFERENCE.md "Common Builder Mistakes"). Fix any found before proceeding.

### 2.1.5 Preview Before Deploy

**Ask [Preview]**: "Want to preview the app before deploying?"
- "Yes — open live preview" — Start the preview server and iterate on the design
- "No — deploy now" — Skip preview, go straight to deploy

If yes: run `node "${CLAUDE_PLUGIN_ROOT}/scripts/preview-server.js"` and tell the user to open `http://localhost:3333`. They can chat to iterate on the design and switch themes. When satisfied, stop the server and continue to 2.2.

### 2.2 Deploy Cycle

This sequence runs twice: first here (with `--admin-ids '[]'`), then in Phase 3 (with real admin ID). Steps:

**Step A — Assemble:**
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/assemble-sell.js" app.jsx index.html \
  --clerk-key "{clerkPk}" \
  --app-name "{appName}" \
  --app-title "{appTitle}" \
  --domain "{domain}" \
  --billing-mode "{billingMode}" \
  --tagline "{tagline}" \
  --subtitle "{subtitle}" \
  --features '{featuresJSON}' \
  --admin-ids '{adminIds}'
```

**Step B — Validate:** `grep -c '__VITE_\|__CLERK_\|__APP_' index.html` — must be 0.

**Step C — Deploy:**
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/deploy-cloudflare.js" \
  --name "{appName}" \
  --file index.html \
  --clerk-key "{clerkPk}" \
  --billing-mode "{billingMode}" \
  --webhook-secret "{webhookSecret}" \
  {aiKeyFlag}
```
Where `{aiKeyFlag}` = `--ai-key "{openRouterKey}"` if set, omitted if null. The `--billing-mode` flag controls whether the client enforces JWT-based plan checks. The `--webhook-secret` flag sets the Clerk webhook signing secret as a Wrangler secret.

Run the cycle now with `{adminIds}` = `'[]'` (or `'["{existingAdminId}"]'` if found in pre-flight). Mark T5, T6 completed.

---

## Phase 3: Admin Setup

**Skip if `CLERK_ADMIN_USER_ID` was found in pre-flight.**

### 3.1 Guide Signup

Tell the user:
> Your app is live! Create your admin account:
> 1. Open: `https://{domain}?subdomain=test`
> 2. Sign up with your email
> 3. Complete email verification
> 4. Create a passkey when prompted

**Ask [Signup]**: "Have you completed signup on the app?"
- "Yes, signed up" — Completed verification + passkey
- "Skip admin setup" — I'll do this later

If skip: proceed to Phase 4.

### 3.2 Collect Admin ID

Tell user: Go to clerk.com/dashboard > your app > Users > click your user > copy User ID (starts with `user_`).

**Ask [User ID]**: "Paste your Clerk User ID (starts with user_)"
- "I need help finding it" — Clerk Dashboard > Users > click name > ID at top

Validate starts with `user_`. Save to `.env`:
```bash
echo "CLERK_ADMIN_USER_ID={userId}" >> .env
```

### 3.3 Re-run Deploy Cycle

Re-run Phase 2.2 steps A-D with `{adminIds}` = `'["{userId}"]'`.

Tell user: Admin dashboard now works at `https://{domain}?subdomain=admin`

---

## Phase 4: Verify & Cleanup

### 4.1 Verify

**Ask [Verify]**: "Your app is live! Open each URL and verify:\n\n- Landing: https://{domain}\n- Tenant: https://{domain}?subdomain=test\n- Admin: https://{domain}?subdomain=admin\n\nDoes everything look right?"
- "All working" — Everything loads correctly
- "Something's broken" — Need to troubleshoot

**If `billingMode === "required"`**: Also ask the user to verify billing:
> "Check billing flow: Sign in at `https://{domain}?subdomain=test` — you should see a paywall with pricing. Use test card `4242 4242 4242 4242` (any future expiry, any CVC) to complete a test subscription. After subscribing, the tenant app should load."

Mark T7 completed. If broken, ask what's wrong and troubleshoot.

### 4.2 Shutdown

Send `shutdown_request` to "builder" and "infra" (if spawned). Wait for responses. Clean up team.

### 4.3 Summary

```
## Launch Complete

**App**: {appTitle}
**URL**: https://{domain}
**Clerk**: {clerkPk}
**Connect**: {studioUrl}
**Billing**: {billingMode}

### What's deployed:
- Cloudflare Worker with KV registry
- Fireproof Connect studio for real-time sync
- Clerk authentication with passkeys
- Subdomain-based multi-tenancy

### Next steps:
- Configure a custom domain (see CLAUDE.md DNS section)
- Set up Clerk billing plans if using subscription mode
```

---

## Error Handling

| Failure | Recovery |
|---------|----------|
| Builder generates invalid JSX | Read app.jsx, fix TS syntax / wrong hooks, re-save |
| Connect deploy fails | Infra reports via SendMessage. Present error + fix steps |
| Assembly has placeholders | Check .env for missing values, re-run assembly |
| Cloudflare deploy fails | Check `npx wrangler whoami`. Guide `npx wrangler login` if needed |
| Wrangler secret put fails | Retry. If persistent, have user run manually |
| Teammate silent 3+ min | SendMessage status check. If no response, take over task |
| Builder hardcodes DB name | Edit app.jsx: replace with `useTenant()` pattern before assembly |
