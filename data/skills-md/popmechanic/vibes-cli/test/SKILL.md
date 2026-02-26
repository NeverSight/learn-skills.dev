---
name: test
description: Self-contained test automation — invoke directly, do not decompose. End-to-end integration test that assembles a fixture, deploys Connect + Cloudflare, and presents a live URL for browser verification.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
metadata:
  author: "Marcus Estes"
  version: "0.1.63"
---

> **Plan mode**: If you are planning work, this entire skill is ONE plan step: "Invoke /vibes:test". Do not decompose the steps below into separate plan tasks.

## Integration Test Skill

Orchestrates the full test pipeline: credentials → Connect studio → fixture assembly → Cloudflare deploy → live URL → unit tests.

**Working directory:** `test-vibes/` (gitignored, persists across runs)

### Phase 1: Credentials

Check if `test-vibes/.env` exists and has Clerk keys.

```bash
# From the plugin root
cat test-vibes/.env 2>/dev/null
```

**If the file exists and contains `VITE_CLERK_PUBLISHABLE_KEY`:**

```
AskUserQuestion:
  Question: "Reuse existing test credentials? (publishable key: pk_test_...)"
  Header: "Credentials"
  Options:
  - Label: "Yes, reuse"
    Description: "Use the Clerk keys already in test-vibes/.env"
  - Label: "No, enter new keys"
    Description: "I want to use different Clerk credentials"
```

**If the file doesn't exist or keys are missing, or user wants new keys:**

```
AskUserQuestion:
  Question: "Paste your Clerk Publishable Key (starts with pk_test_ or pk_live_)"
  Header: "Clerk PK"
  Options:
  - Label: "I need to get keys first"
    Description: "I'll go to clerk.com and come back"
```

If they need keys, tell them:
> Go to [clerk.com](https://clerk.com) → your application → API Keys → copy Publishable Key and Secret Key.

Then ask for the secret key:

```
AskUserQuestion:
  Question: "Paste your Clerk Secret Key (starts with sk_test_ or sk_live_)"
  Header: "Clerk SK"
```

Write `test-vibes/.env`:
```
VITE_CLERK_PUBLISHABLE_KEY=<key>
VITE_CLERK_SECRET_KEY=<key>
```

### Phase 2: Connect Studio

Check if `test-vibes/.connect` exists (marks a deployed studio).

```bash
cat test-vibes/.connect 2>/dev/null
```

**If `.connect` exists:** Read the studio name and API/Cloud URLs. Confirm reuse:

```
AskUserQuestion:
  Question: "Reuse existing Connect studio '<name>'?"
  Header: "Connect"
  Options:
  - Label: "Yes, reuse"
    Description: "Studio is already running"
  - Label: "No, deploy fresh"
    Description: "Deploy a new Connect studio"
```

**If `.connect` doesn't exist or user wants fresh deploy:**

Run the deploy script. Read the Clerk keys from `test-vibes/.env` first:

```bash
node scripts/deploy-connect.js \
  --studio vibes-test-studio \
  --clerk-publishable-key "$VITE_CLERK_PUBLISHABLE_KEY" \
  --clerk-secret-key "$VITE_CLERK_SECRET_KEY"
```

After deploy, save the studio info:

```bash
# Write connect marker
echo "vibes-test-studio" > test-vibes/.connect
```

Update `test-vibes/.env` with the Connect URLs:
```
VITE_API_URL=https://vibes-test-studio.exe.xyz/api
VITE_CLOUD_URL=fpcloud://vibes-test-studio.exe.xyz?protocol=wss
```

### Phase 3: Fixture Selection

```
AskUserQuestion:
  Question: "Which fixture to test?"
  Header: "Fixture"
  Options:
  - Label: "fireproof-basic (Recommended)"
    Description: "Fireproof CRUD with React singleton — the standard integration test"
  - Label: "minimal"
    Description: "Template + Babel + import map only — fastest, no Fireproof"
  - Label: "sell-ready"
    Description: "useTenant() + multi-tenant routing — tests sell assembly path"
  - Label: "ai-proxy"
    Description: "/api/ai/chat endpoint + CORS — requires OpenRouter key"
```

**For sell-ready fixture:** Check `test-vibes/.env` for a cached admin user ID from a previous run:

```bash
grep CLERK_ADMIN_USER_ID test-vibes/.env 2>/dev/null
```

**If found**, offer to reuse it (mask the middle of the value in the prompt, e.g., `user_37ici...ohcY`):

```
AskUserQuestion:
  Question: "Reuse stored admin user ID? (user_37ici...ohcY)"
  Header: "Admin ID"
  Options:
  - Label: "Yes, reuse"
    Description: "Use the cached user ID from test-vibes/.env"
  - Label: "Skip admin"
    Description: "Deploy without admin — you can set it up after deploy"
```

If "Yes, reuse": use the stored value in Phase 4 assembly.
If "Skip admin": omit `--admin-ids` in Phase 4. Admin setup will be offered post-deploy in Phase 5.5.

**If not found:** No prompt needed. Admin will be set up post-deploy in Phase 5.5 after the user has a chance to sign up on the live app.

### Phase 3.5: Sell Configuration (sell-ready only)

**Condition:** Only runs when the user selected `sell-ready` in Phase 3.

**Ask billing mode:**

```
AskUserQuestion:
  Question: "Which billing mode should this sell test use?"
  Header: "Billing"
  Options:
  - Label: "Free (billing off)"
    Description: "Claims work without payment — tests auth + tenant routing only"
  - Label: "Billing required"
    Description: "Claims require active Clerk subscription — tests full paywall flow"
```

**If "Free":** Store `BILLING_MODE=off` in `test-vibes/.env`. Skip webhook setup. Proceed to Phase 4.

**If "Billing required":** Store `BILLING_MODE=required` in `test-vibes/.env`. Then guide webhook setup:

```
AskUserQuestion:
  Question: "Set up the Clerk webhook for billing:\n\n1. Go to clerk.com → your app → Webhooks → Add Endpoint\n2. URL: https://vibes-test.<account>.workers.dev/webhook\n3. Subscribe to: subscription.deleted\n4. Copy the Signing Secret (starts with whsec_)\n\nPaste the webhook signing secret:"
  Header: "Webhook"
  Options:
  - Label: "I need help"
    Description: "Walk me through the Clerk webhook setup"
```

If "I need help": walk them through each step in the Clerk dashboard, then re-ask the question.

Validate the secret starts with `whsec_`. If not, ask again with a note that it should start with `whsec_`.

Store as `CLERK_WEBHOOK_SECRET` in `test-vibes/.env`:
```bash
grep -q CLERK_WEBHOOK_SECRET test-vibes/.env 2>/dev/null && \
  sed -i '' 's/^CLERK_WEBHOOK_SECRET=.*/CLERK_WEBHOOK_SECRET=<secret>/' test-vibes/.env || \
  echo "CLERK_WEBHOOK_SECRET=<secret>" >> test-vibes/.env
```

Proceed to Phase 4.

### Phase 4: Assembly

Copy the selected fixture and assemble:

```bash
# Copy fixture to working directory
cp scripts/__tests__/fixtures/<fixture>.jsx test-vibes/app.jsx

# Source env for assembly
set -a && source test-vibes/.env && set +a
```

**For sell-ready fixture:**
```bash
node scripts/assemble-sell.js test-vibes/app.jsx test-vibes/index.html \
  --domain vibes-test.<account>.workers.dev \
  --admin-ids '["<admin-user-id>"]'  # read CLERK_ADMIN_USER_ID from test-vibes/.env
```
If admin was skipped, omit `--admin-ids`. The `--domain` flag is always required.

**For all other fixtures:**
```bash
node scripts/assemble.js test-vibes/app.jsx test-vibes/index.html
```

**Validate the output** (same checks as the vitest suite):
1. File exists and is non-empty
2. No `__PLACEHOLDER__` strings remain
3. Import map `<script type="importmap">` is present
4. `<script type="text/babel">` contains the fixture code
5. For sell-ready: `getRouteInfo` function is present

If any check fails, report the error, then ask:

```
AskUserQuestion:
  Question: "What next?"
  Header: "Next"
  Options:
  - Label: "Test another fixture"
    Description: "Go back to Phase 3 and pick a different fixture"
  - Label: "End test session"
    Description: "Clean up artifacts and finish"
```

If "Test another fixture": go to Phase 3.
If "End test session": go to Phase 11.

### Phase 5: Deploy to Cloudflare

**For ai-proxy fixture:** Check `~/.vibes/.env` for a cached OpenRouter key first:

```bash
grep OPENROUTER_API_KEY ~/.vibes/.env 2>/dev/null
```

**If found**, offer to reuse it (mask the key, e.g., `sk-or-v1-...a3b2`):

```
AskUserQuestion:
  Question: "Reuse stored OpenRouter API key? (sk-or-v1-...a3b2)"
  Header: "AI Key"
  Options:
  - Label: "Yes, reuse"
    Description: "Use the cached key from ~/.vibes/.env"
  - Label: "Enter new"
    Description: "I'll paste a different key"
  - Label: "Skip AI proxy"
    Description: "Deploy without AI endpoint"
```

If "Yes, reuse": use the stored value. If "Enter new": collect via the prompt below, then update `~/.vibes/.env`.

**If not found** (or user chose "Enter new"):

```
AskUserQuestion:
  Question: "Paste your OpenRouter API key for the AI proxy"
  Header: "AI Key"
  Options:
  - Label: "Skip AI proxy"
    Description: "Deploy without AI endpoint"
```

After collecting a new key, offer to save it:

```
AskUserQuestion:
  Question: "Save this OpenRouter key to ~/.vibes/.env for future projects?"
  Header: "Cache"
  Options:
  - Label: "Yes, save"
    Description: "Cache the key so you don't have to paste it again"
  - Label: "No, skip"
    Description: "Use for this session only"
```

If "Yes, save":
```bash
mkdir -p ~/.vibes
grep -q OPENROUTER_API_KEY ~/.vibes/.env 2>/dev/null && \
  sed -i '' 's/^OPENROUTER_API_KEY=.*/OPENROUTER_API_KEY=<new>/' ~/.vibes/.env || \
  echo "OPENROUTER_API_KEY=<new>" >> ~/.vibes/.env
```

Run the deploy:

```bash
node scripts/deploy-cloudflare.js --name vibes-test --file test-vibes/index.html
```

**For sell-ready fixture:** Pass `--env-dir` to auto-detect Clerk key, and pass billing mode and webhook secret from `test-vibes/.env`:
```bash
node scripts/deploy-cloudflare.js --name vibes-test --file test-vibes/index.html \
  --env-dir test-vibes \
  --billing-mode $BILLING_MODE \
  --webhook-secret $CLERK_WEBHOOK_SECRET  # only if billing required
```
Read `BILLING_MODE` and `CLERK_WEBHOOK_SECRET` from `test-vibes/.env`. The `--env-dir` flag auto-detects `VITE_CLERK_PUBLISHABLE_KEY` from `.env` (fetches JWKS, converts to PEM, sets `CLERK_PEM_PUBLIC_KEY` and `PERMITTED_ORIGINS` as Worker secrets). `--billing-mode` patches the `[vars]` in `wrangler.toml` before deploy. `--webhook-secret` sets `CLERK_WEBHOOK_SECRET` as a Worker secret.

**For ai-proxy with key:**
```bash
node scripts/deploy-cloudflare.js --name vibes-test --file test-vibes/index.html --ai-key <key>
```

### Phase 5.5: Admin Setup (sell-ready only)

**Condition:** Only runs for the sell-ready fixture AND admin is not yet configured (no cached ID was reused in Phase 3).

After deploy, guide the user through post-deploy admin setup:

1. Tell the user the app is live and they can now sign up:

```
Your app is deployed! To configure admin access, first create an account:
  Sign up here: https://vibes-test.<account>.workers.dev?subdomain=test

After signing up, we'll grab your User ID from Clerk Dashboard.
```

2. Ask if they've signed up:

```
AskUserQuestion:
  Question: "Have you completed signup on the deployed app?"
  Header: "Signup"
  Options:
  - Label: "Yes, signed up"
    Description: "I've created my account and I'm ready to get my User ID"
  - Label: "Skip admin setup"
    Description: "Continue without admin access"
```

If "Skip admin setup": proceed to Phase 6 without admin configured.

3. Guide to Clerk Dashboard:

```
Now grab your User ID:
  1. Go to clerk.com → your application → Users
  2. Click on your user
  3. Copy the User ID (starts with user_)
```

4. Collect the User ID:

```
AskUserQuestion:
  Question: "Paste your Clerk User ID (starts with user_)"
  Header: "Admin ID"
  Options:
  - Label: "I need help finding it"
    Description: "Show me where to find the User ID in Clerk Dashboard"
  - Label: "Skip admin setup"
    Description: "Continue without admin access"
```

Validate the input starts with `user_`. If not, ask again.

5. Save to `test-vibes/.env`:

```bash
grep -q CLERK_ADMIN_USER_ID test-vibes/.env 2>/dev/null && \
  sed -i '' 's/^CLERK_ADMIN_USER_ID=.*/CLERK_ADMIN_USER_ID=<userId>/' test-vibes/.env || \
  echo "CLERK_ADMIN_USER_ID=<userId>" >> test-vibes/.env
```

6. Re-assemble with admin configured:

```bash
set -a && source test-vibes/.env && set +a

node scripts/assemble-sell.js test-vibes/app.jsx test-vibes/index.html \
  --domain vibes-test.<account>.workers.dev \
  --admin-ids '["<userId>"]'
```

7. Re-deploy:

```bash
node scripts/deploy-cloudflare.js --name vibes-test --file test-vibes/index.html \
  --env-dir test-vibes \
  --billing-mode $BILLING_MODE \
  --webhook-secret $CLERK_WEBHOOK_SECRET  # only if billing required
```

8. Confirm:

```
Admin access configured! The admin dashboard at ?subdomain=admin should now work for your account.
```

Proceed to Phase 6.

### Phase 6: Present URL

Print the live URL and what to check:

**For minimal / fireproof-basic:**
```
Deployed! Open in your browser:
  https://vibes-test.<account>.workers.dev

What to verify:
- Page loads without console errors
- (fireproof-basic) CRUD operations work — add, edit, delete items
- Settings gear icon opens the menu
```

**For sell-ready:**
```
Deployed! Open these URLs:
  Landing:  https://vibes-test.<account>.workers.dev
  Tenant:   https://vibes-test.<account>.workers.dev?subdomain=test
  Admin:    https://vibes-test.<account>.workers.dev?subdomain=admin

What to verify:
- Landing page shows pricing/marketing content
- Claim a subdomain — should succeed (tests /claim + JWT auth)
- Tenant URL shows auth gate (Clerk sign-in)
- Admin URL shows admin dashboard (if admin was configured in Phase 3 or 5.5)
- Admin URL shows "Admin Access Required" (if admin setup was skipped)
```

**For ai-proxy:**
```
Deployed! Open in your browser:
  https://vibes-test.<account>.workers.dev

What to verify:
- App loads and renders
- AI chat feature works (sends to /api/ai/chat)
- Check Network tab: requests go to OpenRouter via proxy
```

Then ask:

```
AskUserQuestion:
  Question: "How does it look?"
  Header: "Result"
  Options:
  - Label: "Working"
    Description: "Everything renders correctly"
  - Label: "Has issues"
    Description: "Something isn't right — I'll describe it"
```

**If "Working":**

Print a summary table:

```
| Phase       | Status |
|-------------|--------|
| Credentials | ✓      |
| Connect     | ✓ <studio-name>.exe.xyz |
| Assembly    | ✓ <fixture>.jsx → index.html |
| Cloudflare  | ✓ <url> |
| Browser     | ✓ User confirmed working |
```

```
AskUserQuestion:
  Question: "What next?"
  Header: "Next"
  Options:
  - Label: "Test another fixture"
    Description: "Go back to Phase 3 and pick a different fixture"
  - Label: "End test session"
    Description: "Clean up artifacts and finish"
```

If "Test another fixture": go to Phase 3.
If "End test session": go to Phase 11.

**If "Has issues":** proceed to Phase 7.

---

### Phase 7: Diagnosis

**You are a plugin developer testing your own code.** The test instance is disposable. Bugs found here are bugs in plugin source code — deploy scripts, templates, assembly logic, or skill instructions. Fix the plugin source, NOT the test instance.

Ask the user to describe the issue. Then work through these diagnostic steps. Skip ahead when diagnosis is clear.

**7.1 Browser console** — ask the user to check, or use browser automation tools if available:

| Console Error | Likely Cause | Check File |
|---------------|-------------|------------|
| `Cannot read properties of null (reading 'useContext')` | Duplicate React instances | `source-templates/base/template.html` import map |
| `Failed to fetch` / CORS errors | Deploy script wrong URL or missing CORS headers | `scripts/deploy-connect.js`, `scripts/deploy-cloudflare.js` |
| `Fireproof is not defined` | Missing import map entry | `source-templates/base/template.html` import map |
| `Unexpected token '<'` | Babel script block malformed | `scripts/assemble.js` |
| 404 on `/api/` routes | nginx config or Connect not running | `scripts/deploy-connect.js` |

**7.2 Network requests** — probe the deployed services:

```bash
# Test Connect Studio API
curl -v https://<studio>.exe.xyz/api/

# Test Cloudflare Worker
curl -v https://vibes-test.<account>.workers.dev/
```

**7.3 Server-side** — SSH into the VM if network probes fail:

```bash
ssh <studio>.exe.xyz "docker ps"           # Check containers running
ssh <studio>.exe.xyz "sudo nginx -t"       # Check nginx config
ssh <studio>.exe.xyz "docker logs gateway"  # Check gateway logs
```

**7.4 Plugin source** — map symptoms to source files:

| Symptom Category | Files to Read |
|-----------------|---------------|
| Assembly/template | `scripts/assemble.js`, `source-templates/base/template.html`, relevant `template.delta.html` |
| Deploy/hosting | `scripts/deploy-cloudflare.js`, `scripts/deploy-connect.js` |
| Auth/Clerk | `source-templates/base/template.html` (Clerk script), `scripts/deploy-connect.js` (env vars) |
| Import/module errors | `source-templates/base/template.html` (import map) |

### Phase 8: Root Cause Classification

Before touching any file, state the classification:

| Category | Signal | Fix Target | Example |
|----------|--------|-----------|---------|
| **A: Plugin source bug** | Deploy script produces wrong output | `scripts/*.js` | `deploy-connect.js` writes wrong URL |
| **B: Template bug** | HTML output is structurally wrong | `source-templates/base/template.html` or `template.delta.html` | Missing import map entry |
| **C: Skill instruction bug** | Agent followed wrong steps | `skills/*/SKILL.md` | Wrong hook name in instructions |
| **D: Fixture bug** | Only this fixture fails | `scripts/__tests__/fixtures/` | Bad JSX in test fixture |
| **E: External/transient** | VM down, CDN outage, rate limit | None — retry | esm.sh 503, VM unreachable |

```
AskUserQuestion:
  Question: "I believe this is Category <X>: <description>. The fix belongs in <file>. Proceed?"
  Header: "Fix plan"
  Options:
  - Label: "Yes, fix it"
    Description: "Apply the fix to plugin source"
  - Label: "Wrong diagnosis"
    Description: "I think the problem is something else"
```

If "Wrong diagnosis": ask what they think and re-diagnose.

### Phase 9: Apply Fix and Verify

**Fix the plugin source file, NOT the test instance.**

1. Apply the fix to the identified source file
2. If the fix touched templates or components, regenerate:
   ```bash
   node scripts/merge-templates.js --force   # If template.html or delta changed
   node scripts/build-components.js --force  # If components/ changed
   ```
3. Re-run from the appropriate phase:

| Category | Restart From |
|----------|-------------|
| A: Plugin source | Phase that uses the fixed script (2, 4, or 5) |
| B: Template | Phase 4 (re-assemble) |
| C: Skill instruction | Note the fix — no re-run needed |
| D: Fixture | Phase 4 (re-assemble) |
| E: External | Retry the failed phase |

4. Present the URL and ask:

```
AskUserQuestion:
  Question: "How does it look now?"
  Header: "Verify"
  Options:
  - Label: "Fixed"
    Description: "The issue is resolved"
  - Label: "Still broken"
    Description: "Same problem persists"
  - Label: "Different issue"
    Description: "Original issue fixed but something else is wrong"
```

If "Still broken" or "Different issue": loop back to Phase 7. After 3 loops, say:
> This needs hands-on investigation. Here's what I've tried so far: <summary>. Try debugging manually or open an issue.

Then ask:

```
AskUserQuestion:
  Question: "What next?"
  Header: "Next"
  Options:
  - Label: "Test another fixture"
    Description: "Go back to Phase 3 and pick a different fixture"
  - Label: "End test session"
    Description: "Clean up artifacts and finish"
```

If "Test another fixture": go to Phase 3.
If "End test session": go to Phase 11.

### Phase 10: Resolution Summary

Write `test-vibes/FIX-REPORT.md`:

```markdown
# Fix Report

**Date:** <date>
**Fixture:** <fixture>
**Category:** <A-E>

## Symptom
<What the user reported>

## Root Cause
<What was actually wrong>

## Fix
- **File:** <path>
- **Change:** <one-line description>

## Diagnosis Commands
<Commands that revealed the issue>

## Prevention
<How to avoid this in the future>
```

```
AskUserQuestion:
  Question: "What next?"
  Header: "Next"
  Options:
  - Label: "Test another fixture"
    Description: "Go back to Phase 3 with the fix in place"
  - Label: "Commit the fix"
    Description: "Review and commit the plugin source changes"
  - Label: "End test session"
    Description: "Clean up artifacts and finish"
```

If "Commit the fix": show `git diff` of plugin source changes (exclude `test-vibes/`), suggest a commit message derived from the fix report. After committing, show the canonical prompt:

```
AskUserQuestion:
  Question: "What next?"
  Header: "Next"
  Options:
  - Label: "Test another fixture"
    Description: "Go back to Phase 3 and pick a different fixture"
  - Label: "End test session"
    Description: "Clean up artifacts and finish"
```

If "Test another fixture": go to Phase 3.
If "End test session": go to Phase 11.

### Phase 11: Unit & Integration Tests

Run the vitest suite to confirm plugin source is healthy. Especially important after any fixes applied in Phase 9.

```bash
cd scripts && npm test
```

**If all tests pass:** Print the count (e.g. "429 tests passed") and proceed to cleanup.

**If any tests fail:** Show the failure output and ask:

```
AskUserQuestion:
  Question: "Unit/integration tests failed. Fix before finishing?"
  Header: "Tests"
  Options:
  - Label: "Yes, fix them"
    Description: "Investigate and fix the failing tests"
  - Label: "Skip"
    Description: "Finish the session anyway"
```

If "Yes, fix them": diagnose and fix the failures, re-run `npm test`, loop until green.

### Phase 12: Session Cleanup

Triggered after Phase 11 completes or when user selects "End test session" from any "What next?" prompt.

Clean up test artifacts while preserving reusable credentials:

```bash
# Clean test artifacts, preserve .env and .connect
cd test-vibes && find . -maxdepth 1 ! -name '.' ! -name '.env' ! -name '.connect' -exec rm -rf {} +
```

Print:

```
Test session complete.
  Cleaned: test-vibes/ artifacts
  Preserved: .env, .connect (reusable next session)
```
