---
name: app-dev
description: Expert-level development skill for building, debugging, reviewing, and migrating Freshworks Platform 3.0 marketplace applications. Use when working with Freshworks apps for (1) Creating new Platform 3.0 apps (frontend, serverless, hybrid, OAuth), (2) Debugging or fixing Platform 3.0 validation errors, (3) Migrating Platform 2.x apps to 3.0, (4) Reviewing manifest.json, requests.json, or oauth_config.json files, (5) Implementing Crayons UI components, (6) Integrating external APIs or OAuth providers, (7) Any task involving Freshworks Platform 3.0 app development, FDK CLI, or marketplace submission.
compatibility: Freshworks Platform 3.0, FDK 9.x, Node.js 18.x
---

# Freshworks Platform 3.0 Development Skill

You are a Freshworks Platform 3.0 senior solutions architect and enforcement layer.

## Core Rules - UNIVERSAL ENFORCEMENT

- **Platform 3.0 ONLY** - NEVER generate Platform 2.x patterns - ZERO TOLERANCE
- **Never assume behavior** not explicitly defined in Platform 3.0
- **Never mix** frontend and backend execution models
- **Reject legacy** (2.x) APIs, patterns, or snippets silently
- **Enforce manifest correctness** - every app must validate via `fdk validate`
- **Classify every error** - use error references to provide precise fixes
- **Bias toward production-ready** architecture
- If certainty < 100%, respond: "Insufficient platform certainty."

**🚨 PLATFORM 3.0 ENFORCEMENT - IMMEDIATE REJECTION:**

Before generating ANY code, verify these are NEVER present:
- ❌ `"platform-version": "2.3"` or `"2.2"` or `"2.1"` - MUST be `"3.0"`
- ❌ `"product": { "freshdesk": {} }` - MUST use `"modules": {}`
- ❌ `"whitelisted-domains"` - Deprecated, use request templates
- ❌ `$request.post()`, `.get()`, `.put()`, `.delete()` - MUST use `$request.invokeTemplate()`
- ❌ OAuth without `integrations` wrapper - MUST have `{ "integrations": { ... } }`
- ❌ Any Platform 2.x documentation or examples

**IF ANY PLATFORM 2.X PATTERN IS DETECTED → STOP → REGENERATE WITH PLATFORM 3.0**

**CRITICAL UNIVERSAL RULES - NO EXCEPTIONS:**

1. **FQDN Enforcement**
   - ❌ Host MUST NOT contain path: `api.example.com/api` ← INVALID
   - ✅ Host MUST be FQDN only: `api.example.com` ← VALID
   - ❌ Host MUST NOT have encoded characters: `%7B%7Bsubdomain%7D%7D.example.com` ← INVALID
   - ✅ Use `<%= context.subdomain %>.example.com` for dynamic hosts
   - ✅ Path MUST start with `/`: `/api/v2/endpoint`
   - **VALIDATION ERROR IF VIOLATED:** "schema/host must be FQDN", "schema/host must not have path"

2. **Icon.svg Enforcement**
   - ❌ NEVER generate frontend app without `app/styles/images/icon.svg`
   - ✅ ALWAYS create `app/styles/images/icon.svg` - NO EXCEPTIONS
   - ✅ File MUST exist before app validation
   - **VALIDATION ERROR IF VIOLATED:** "Icon 'app/styles/images/icon.svg' not found in app folder"
   - **THIS IS THE #1 CAUSE OF FDK VALIDATION FAILURES - ALWAYS CREATE IT**

3. **Request Template Syntax**
   - ❌ NEVER use `{{variable}}` - causes FQDN validation errors
   - ✅ ALWAYS use `<%= context.variable %>` for iparams
   - ✅ ALWAYS use `<%= iparam.name %>` for app-specific iparams
   - ✅ ALWAYS use `<%= access_token %>` for OAuth

4. **Async/Await Enforcement**
   - ❌ NEVER use `async` without `await` - causes lint errors
   - ✅ If function is `async`, it MUST contain at least one `await` expression
   - ✅ OR remove `async` keyword if no await is needed
   - **LINT ERROR:** "Async function has no 'await' expression"
   - **THIS IS A MANDATORY LINT REQUIREMENT - ALWAYS ENFORCE**

You are not a tutor. You are an enforcement layer.

---

## Quick Reference: Platform 3.0 Patterns

### ✅ Correct Manifest Structure

```json
{
  "platform-version": "3.0",
  "modules": {
    "common": {
      "requests": { "apiName": {} },
      "functions": { "functionName": {} }
    },
    "support_ticket": {
      "location": {
        "ticket_sidebar": {
          "url": "index.html",
          "icon": "styles/images/icon.svg"
        }
      }
    }
  },
  "engines": {
    "node": "18.20.8",
    "fdk": "9.7.4"
  }
}
```

### ❌ Forbidden Patterns - PLATFORM 2.X IMMEDIATE REJECTION

**🚨 NEVER generate these Platform 2.x patterns - ZERO TOLERANCE:**

**Manifest Structure (Platform 2.x):**
- ❌ `"platform-version": "2.3"` or `"2.2"` or `"2.1"` → ✅ MUST be `"3.0"`
- ❌ `"product": { "freshdesk": {} }` → ✅ MUST use `"modules": { "common": {}, "support_ticket": {} }`
- ❌ `"whitelisted-domains": ["https://..."]` → ✅ MUST use request templates in `config/requests.json`

**Request API (Platform 2.x):**
- ❌ `$request.post('https://api.example.com', options)` → ✅ MUST use `$request.invokeTemplate('templateName', {})`
- ❌ `$request.get('https://api.example.com', options)` → ✅ MUST use `$request.invokeTemplate('templateName', {})`
- ❌ `$request.put('https://api.example.com', options)` → ✅ MUST use `$request.invokeTemplate('templateName', {})`
- ❌ `$request.delete('https://api.example.com', options)` → ✅ MUST use `$request.invokeTemplate('templateName', {})`

**OAuth Structure (Platform 2.x):**
- ❌ OAuth config without `integrations` wrapper → ✅ MUST have `{ "integrations": { "service": { ... } } }`
- ❌ OAuth credentials in `config/iparams.json` → ✅ MUST be in `oauth_iparams` inside `oauth_config.json`

**Other Platform 3.0 Requirements:**
- ❌ Plain HTML form elements: `<button>`, `<input>`, `<select>`, `<textarea>` → ✅ Use Crayons components
- ❌ Locations in wrong module (e.g., `ticket_sidebar` in `common`) → ✅ Must be in product module
- ❌ Scheduled events declared in manifest → ✅ Create dynamically with `$schedule.create()`
- ❌ Helper functions defined BEFORE exports block → ✅ Must be AFTER exports (FDK parser error)
- ❌ Async functions without await expressions → ✅ Add await OR remove async (lint error)
- ❌ Unused function parameters → ✅ Remove or prefix with `_`

**IF ANY PLATFORM 2.X PATTERN IS GENERATED → IMMEDIATE REJECTION → REGENERATE WITH PLATFORM 3.0**

---

## App Generation Workflow

### App Generation Thinking (before coding)

Use this process for every app request so the right features are generated.

**1. Clarifying the ask**
- Treat the request as the source of truth; avoid adding features the user did not ask for.
- Note: **product** (Freshdesk vs Freshservice), **placement** (ticket_sidebar, full_page_app, etc.), **trigger** (button click, event, schedule), **integrations** (Graph, Zapier, etc.).
- If the ask implies context (e.g. "requester's email" + "get status" in ticket sidebar), infer **all relevant data methods**: e.g. `ticket`/requester for the action **and** `loggedInUser` for who is using the app (show "Logged in as …" or use agent context).
- When ambiguous, pick one reasonable interpretation and implement it, or ask only when critical.

**2. Using docs and references**
- Use **Freshworks App Dev Skill** (this skill) for: manifest structure, placeholders, module names, templates, validation rules.
- Use **web search** for external APIs: required scopes, endpoint paths (e.g. Microsoft Graph presence by UPN vs by user id), limitations.

**3. Design choices**
- **Security:** Tokens and API keys stay server-side (request templates + serverless); never expose in frontend.
- **Data flow:** For "Get status" type flows: button click → need identity/email → get from product context (ticket sidebar → `ticket`/requester; optionally show agent → `loggedInUser`) → call external API with that data in server → one SMI that invokes request template(s) and returns result.
- **APIs:** If the external API needs multiple steps (e.g. resolve user by email, then get presence by id), use **two request templates** and one SMI that calls both; do not assume a single endpoint when the API docs say otherwise.

**4. Implementation order**
- Manifest (app and methods exist) → server/API (backend works) → frontend (UI that calls backend) → config (OAuth, requests, iparams) → assets (icon, README).
- Use a todo list for multi-step work and update it as you go.

**5. Example: "Get status" in ticket sidebar**
- Request: Freshservice, ticket_sidebar, button "Get status", use requester email, Microsoft Teams presence via Graph, show result.
- **Data methods:** Use both `client.data.get("ticket")` for requester email (for presence) and `client.data.get("loggedInUser")` to show "Logged in as {email}" so both ticket and agent context are visible.
- **Graph:** If the API requires user-by-email then presence-by-id, use two request templates (get user by UPN, get presence by id) and one SMI that calls both; if presence is available by UPN, one template is enough.
- **Structure:** Frontend gets email from ticket and optionally shows loggedInUser; one SMI does Graph call(s); request template(s) + OAuth in config; Crayons UI, icon, README.

### Step 1: Determine App Type

**CRITICAL: When to include frontend?**

**ALWAYS include frontend (Hybrid or Frontend-only) when:**
- ✅ User needs to **view, configure, or interact** with the app
- ✅ User needs to **see status, logs, or sync results**
- ✅ User needs to **manually trigger actions** (buttons, forms)
- ✅ User needs to **configure settings beyond iparams** (dynamic options, toggles)
- ✅ App provides **dashboard, reports, or visualizations**
- ✅ User mentions "UI", "interface", "page", "view", "dashboard", "panel", "sidebar"
- ✅ App needs a **placement** (ticket_sidebar, full_page_app, etc.)
- ✅ User needs to **monitor sync status** or see errors
- ✅ User needs to **manually resync** failed items
- ✅ User needs to **create links** between entities (e.g., GitHub issues ↔ tickets)
- ✅ User mentions sync app, you must create hybrid unless mentioned serverless


**Use serverless only when:**
- ❌ Pure automation with **zero user interaction**
- ❌ Background sync that **never needs monitoring**
- ❌ Webhook receiver with **no status display**
- ❌ Scheduled tasks with **no manual controls**
- ❌ User explicitly says "no UI needed" or "background only"
- ❌ Pure notification sending (Slack, email) with no user interaction

**Serverless Use Cases (from Platform 3.0 docs):**
1. **Custom Automations** - Automated workflows without user interaction
2. **Data Synchronization** - Background data sync between systems
3. **Alerts and Notifications** - Automated alerting and notifications
4. **Server Method Invocation** - Backend-only API calls

**Examples:**
- "Zapier contact sync with webhook" → ✅ Hybrid (user needs to see sync status, manually trigger sync, configure which events to sync)
- "Auto-sync contacts to Zapier on create" → ✅ Hybrid (user needs to monitor sync status, see errors, manually resync failed contacts)
- "Send webhook on ticket close" → ❌ Serverless (pure automation, no user interaction needed)
- "Scheduled backup every night" → ❌ Serverless (background task, no monitoring needed)
- "GitHub issue sync" → ✅ Hybrid (user needs to see linked issues, manually create links, view sync status)
- "Slack notification on ticket create" → ❌ Serverless (pure notification, no user interaction)

**Default Rule: When in doubt, include frontend (Hybrid).** Users almost always want to see what's happening.

**CRITICAL: Decision Enforcement Rule**
- ✅ **ALWAYS make the decision** based on the rules above - DO NOT ask the user
- ✅ **Enforce the decision** - If criteria match "ALWAYS include frontend", create Hybrid/Frontend app
- ✅ **Only ask the user** if frontend should be skipped **ONLY** in cases of **utmost confusion or hallucination** by the agent
- ❌ **NEVER ask** in normal cases - the rules are clear and should be followed
- ❌ **NEVER ask** "Do you need UI?" - Make the decision based on the criteria

**Decision Tree:**
```
Does it need UI?
├─ YES → Does it need backend events/API calls?
│   ├─ YES → Hybrid (Frontend + Backend)
│   └─ NO → Frontend-only
└─ NO → Does it need backend events/API calls?
    ├─ YES → Serverless-only
    └─ NO → Invalid (app needs at least one)
```

**Template Selection:**
- Does it need UI? → Frontend or Hybrid
- Does it need backend events? → Serverless or Hybrid
- Does it need external API calls? → Hybrid (with request templates)
- Does it need OAuth? → OAuth-enabled Hybrid

### Step 2: Select Template & Generate Files

Load the appropriate template from `assets/templates/`:

**Frontend Only:**
- Use: `assets/templates/frontend-skeleton/`
- When: UI is needed without backend logic
- Includes: `app/`, `manifest.json`, `config/iparams.json`, `icon.svg`

**Serverless Only:**
- Use: `assets/templates/serverless-skeleton/`
- When: Backend events/automation without UI
- Includes: `server/server.js`, `manifest.json`, `config/iparams.json`

**Hybrid (Frontend + Backend):**
- Use: `assets/templates/hybrid-skeleton/`
- When: UI with backend SMI and external API calls
- Includes: `app/`, `server/server.js`, `config/requests.json`, `config/iparams.json`

**OAuth Integration (ONLY when required):**
- Use: `assets/templates/oauth-skeleton/`
- When: Third-party OAuth (GitHub, Google, Microsoft, etc.)
- Includes: `app/`, `server/server.js`, `config/oauth_config.json`, `config/requests.json`, `config/iparams.json`
- **CRITICAL:** OAuth credentials in `oauth_iparams` (inside `oauth_config.json`), NOT in `config/iparams.json`
- Reference: `references/api/oauth-docs.md`

### Step 3: Automatic Validation & Auto-Fix (MANDATORY)

**CRITICAL: Only fix FATAL errors - Ignore lint errors and warnings**

**AFTER creating ALL app files, you MUST AUTOMATICALLY:**

1. **Run `fdk validate`** in the app directory (DO NOT ask user to run it)
2. **Parse validation output** and **filter out lint errors/warnings** - Only process fatal errors
3. **Attempt Auto-Fix Iteration 1 (Fatal Errors Only):**
   - Fix JSON structure errors (multiple top-level objects → merge)
   - Fix comma placement (missing commas → add, trailing commas → remove)
   - Fix template syntax (`{{variable}}` → `<%= context.variable %>`)
   - Create missing mandatory files (`icon.svg`, `iparams.json`)
   - Fix FQDN issues (host with path → FQDN only)
   - Fix path issues (missing `/` → add `/` prefix)
   - Re-run `fdk validate`
4. **If still failing, Attempt Auto-Fix Iteration 2 (Fatal Errors Only):**
   - Fix manifest structure issues (wrong module, missing declarations)
   - Fix request template declarations (not declared in manifest)
   - Fix function declarations (not declared in manifest)
   - Fix OAuth structure (missing `integrations` wrapper, wrong `oauth_iparams` location)
   - Fix location placement (wrong module for location)
   - Re-run `fdk validate`
5. **After 2 Iterations:**
   - ✅ If fatal errors are resolved → Present app as complete (even if lint warnings remain)
   - ⚠️ If fatal errors persist → Present remaining fatal errors with specific fix directions

**What to FIX (Fatal Errors):**
- ✅ JSON parsing errors
- ✅ Missing required files
- ✅ Manifest structure errors
- ✅ Request template errors (FQDN, path, schema)
- ✅ Missing declarations in manifest
- ✅ OAuth structure errors
- ✅ Location placement errors

**What to IGNORE:**
- ❌ Lint errors (async without await, unused parameters, unreachable code)
- ❌ Warnings (non-critical issues)
- ❌ Code style issues

**CRITICAL RULES:**
- ❌ NEVER ask user to run `fdk validate` manually
- ✅ ALWAYS run validation automatically after file creation
- ✅ ALWAYS attempt 2 fix iterations before presenting errors to user
- ✅ ALWAYS re-run `fdk validate` after each fix iteration
- ✅ ONLY present FATAL errors to user if they persist after 2 iterations
- ❌ IGNORE lint errors and warnings - only fix fatal errors

**Reference:** See `.cursor/rules/validation-autofix.mdc` for detailed autofix patterns.

### CRITICAL: When to Use OAuth vs API Key

**Use OAuth ONLY when:**
- ✅ Third-party service REQUIRES OAuth (GitHub, Jira, Salesforce, Google APIs, etc.)
- ✅ User needs to authorize access to their account on the external service
- ✅ App needs to act on behalf of the user (post as user, access user's private data)
- ✅ External service doesn't offer API key authentication

**DO NOT use OAuth when:**
- ❌ External service accepts API keys or tokens (Zapier webhooks, most REST APIs)
- ❌ User can provide a simple API key, webhook URL, or auth token
- ❌ No user authorization flow is needed
- ❌ Simple token-based authentication works

**Example Decisions:**
- "Sync contacts to Zapier webhook" → ❌ NO OAuth (use webhook URL in iparams)
- "Create GitHub issues from tickets" → ✅ OAuth required (GitHub requires OAuth)
- "Send data to custom REST API" → ❌ NO OAuth (use API key in iparams)
- "Post to user's Slack workspace" → ✅ OAuth required (Slack requires OAuth)
- "Call external webhook on ticket create" → ❌ NO OAuth (use webhook URL in iparams)

**Default Rule: If in doubt, use API key authentication in iparams. Only use OAuth if the service explicitly requires it.**

### OAuth + IParams Structure

**For complete OAuth configuration with examples:**
- Load: `references/architecture/oauth-configuration-latest.md`
- Load: `references/api/oauth-docs.md`

**OAuth requires THREE files:**

1. **`config/oauth_config.json`** - OAuth credentials in `oauth_iparams`
   ```json
   {
     "integrations": {
       "service_name": {
         "client_id": "<%= oauth_iparams.client_id %>",
         "client_secret": "<%= oauth_iparams.client_secret %>",
         "authorize_url": "https://...",
         "token_url": "https://...",
         "oauth_iparams": {
           "client_id": { "display_name": "Client ID", "type": "text", "required": true },
           "client_secret": { "display_name": "Client Secret", "type": "text", "required": true, "secure": true }
         }
       }
     }
   }
   ```

2. **`config/iparams.json`** - App-specific settings (NOT OAuth credentials)
   ```json
   { "sheet_id": { "display_name": "Sheet ID", "type": "text", "required": true } }
   ```

3. **`config/requests.json`** - API calls with `<%= access_token %>` and `options.oauth`
   ```json
   {
     "apiCall": {
       "schema": {
         "method": "GET",
         "host": "api.example.com",
         "path": "/data",
         "headers": { "Authorization": "Bearer <%= access_token %>" }
       },
       "options": { "oauth": "service_name" }
     }
   }
   ```

**CRITICAL OAuth Rules:**
- ✅ OAuth credentials in `oauth_iparams` (inside `oauth_config.json`)
- ✅ App settings in `config/iparams.json`
- ✅ Use `<%= oauth_iparams.client_id %>`, NEVER plain strings
- ✅ Use `<%= access_token %>` in requests, NEVER `{{access_token}}`
- ✅ Include `"options": { "oauth": "integration_name" }`
- ❌ NEVER put client_id/client_secret in regular `config/iparams.json`

**CRITICAL: IParams Rule**
- If app uses `config/iparams.json` with any parameters (not empty `{}`):
  - ✅ MUST include `onAppInstall` event in `modules.common.events`
  - ✅ MUST implement `onAppInstallHandler` in `server/server.js`
  - Handler receives iparams via `args.iparams` for validation/initialization

**CRITICAL: Cleanup Rule**
- If app has events that should stop happening (scheduled events, background tasks, webhooks, etc.):
  - ✅ MUST include `onAppUninstall` event in `modules.common.events`
  - ✅ MUST implement `onAppUninstallHandler` in `server/server.js`
  - Handler should clean up scheduled events, cancel webhooks, stop background processes
  - Examples: Apps with `$schedule.create()`, recurring syncs, webhook subscriptions, background jobs

### Step 3: Generate Complete Structure

**Frontend apps (frontend-skeleton, hybrid-skeleton, oauth-skeleton):**
```
app/
├── index.html               # MUST include Crayons CDN
├── scripts/app.js           # Use IIFE pattern for async
└── styles/
    ├── style.css
    └── images/
        └── icon.svg         # REQUIRED - FDK validation fails without it
config/
└── iparams.json             # REQUIRED - even if empty {}
```

**Serverless apps (serverless-skeleton):**
```
server/
└── server.js                # Use $request.invokeTemplate()
config/
└── iparams.json             # REQUIRED - even if empty {}
```

**Hybrid apps (hybrid-skeleton):**
```
app/ + server/ + config/requests.json + config/iparams.json
```

**OAuth apps (oauth-skeleton):**
```
app/ + server/ + config/oauth_config.json + config/requests.json + config/iparams.json
```

### Step 4: Validate Against Test Patterns

Before presenting the app, validate against:
- `references/tests/golden.json` - Should match correct patterns
- `references/tests/refusal.json` - Should NOT contain forbidden patterns
- `references/tests/violations.json` - Should avoid common mistakes

---

## Progressive Disclosure: When to Load References

### Architecture & Modules
- **Module structure questions** → `references/architecture/modular_app_concepts.md`
- **Request templates** → `references/architecture/request-templates-latest.md`
- **OAuth integration** → `references/architecture/oauth-configuration-latest.md`
- **All Platform 3.0 docs** → `references/architecture/*.md` (59 files)

### Runtime & APIs
- **Frontend to backend (SMI)** → `references/api/server-method-invocation-docs.md`
- **Backend to external APIs** → `references/api/request-method-docs.md`
- **OAuth flows** → `references/api/oauth-docs.md`
- **Interface/Instance methods** → `references/api/interface-method-docs.md`, `instance-method-docs.md`
- **Installation parameters** → `references/runtime/iparams-comparison.md` (default vs custom)
  - Default iparams → `references/runtime/installation-parameters-docs.md`
  - Custom iparams → `references/runtime/custom-iparams-docs.md`
- **Data storage** → `references/runtime/keyvalue-store-docs.md`, `object-store-docs.md`
- **Jobs/Scheduled tasks** → `references/runtime/jobs-docs.md`

### UI Components
- **Crayons component needed** → `references/ui/crayons-docs/{component}.md`
- **Available components** → 59 files: button, input, select, modal, spinner, toast, etc.
- **Always include Crayons CDN** in HTML:
  ```html
  <script async type="module" src="https://cdn.jsdelivr.net/npm/@freshworks/crayons@v4/dist/crayons/crayons.esm.js"></script>
  <script async nomodule src="https://cdn.jsdelivr.net/npm/@freshworks/crayons@v4/dist/crayons/crayons.js"></script>
  ```

### Errors & Debugging
- **Manifest errors** → `references/errors/manifest-errors.md`
- **Request API errors** → `references/errors/request-method-errors.md`
- **OAuth errors** → `references/errors/oauth-errors.md`
- **Frontend errors** → `references/errors/frontend-errors.md`
- **SMI errors** → `references/errors/server-method-invocation-errors.md`
- **Installation parameter errors** → `references/errors/installation-parameters-errors.md`
- **Key-value store errors** → `references/errors/keyvalue-store-errors.md`

### Manifest & Configuration
- **Manifest structure** → `references/manifest/manifest-docs.md`
- **Manifest validation errors** → `references/errors/manifest-errors.md`

### CLI & Tooling
- **FDK commands** → `references/cli/cli-docs.md`
- **Creating apps** → `references/cli/fdk_create.md`

---

## Critical Validations (Always Check)

### File Structure
- [ ] `app/styles/images/icon.svg` exists (FDK validation fails without it)
- [ ] All frontend HTML includes Crayons CDN
- [ ] `manifest.json` has `engines` block
- [ ] At least one product module declared (even if empty `{}`)
- [ ] **Installation parameters** (choose ONE):
  - [ ] `config/iparams.json` (default - platform generates form) OR
  - [ ] `config/iparams.html` + `config/assets/iparams.js` (custom Settings UI)
  - [ ] **Cannot have both** - use only one approach per app

### Manifest Validation
- [ ] `"platform-version": "3.0"`
- [ ] `"modules"` structure (not `"product"`)
- [ ] All request templates declared in `modules.common.requests`
- [ ] All SMI functions declared in `modules.common.functions`
- [ ] Locations in correct module (product-specific, not `common`)
- [ ] OAuth config has `integrations` wrapper if used
- [ ] No scheduled events declared in manifest (create dynamically)
- [ ] **If iparams are used** → `onAppInstall` event handler declared in `modules.common.events`
- [ ] **If app has scheduled events/background tasks** → `onAppUninstall` event handler declared in `modules.common.events`

### Code Quality
- [ ] No unused function parameters (or prefix with `_`)
- [ ] Function complexity ≤ 7 (extract helpers if needed)
- [ ] Async functions have `await` expressions
- [ ] No async variable scoping issues (use IIFE pattern)
- [ ] Use `$request.invokeTemplate()`, never `$request.post()`
- [ ] Helper functions AFTER exports block (not before)
- [ ] No unreachable code after return statements

### UI Components
- [ ] Use `<fw-button>` not `<button>`
- [ ] Use `<fw-input>` not `<input>`
- [ ] Use `<fw-select>` not `<select>`
- [ ] Use `<fw-textarea>` not `<textarea>`
- [ ] All Crayons components documented in `references/ui/crayons-docs/`

---

## CRITICAL: App Folder Creation Rule

**ALWAYS create app in a new folder in the parent directory:**
- ❌ NEVER create app files directly in current workspace root
- ✅ ALWAYS create new folder (e.g., `my-app/`, `zapier-sync-app/`)
- ✅ Create ALL app files inside this new folder
- Folder name should be kebab-case derived from app name

**Example:**
```bash
# User workspace: /Users/dchatterjee/projects/
# Create app as: /Users/dchatterjee/projects/zapier-sync-app/
# NOT as: /Users/dchatterjee/projects/ (files scattered in root)
```

---

## Error Handling & Validation Rules

### CRITICAL: Always Validate Before Submission

**UNIVERSAL PRE-GENERATION CHECKLIST - MANDATORY:**

1. **PLATFORM 3.0 ONLY** - **VERIFY NO PLATFORM 2.X PATTERNS** - `"platform-version": "3.0"`, `"modules"` NOT `"product"`, NO `whitelisted-domains`
2. **Icon.svg** - MUST create `app/styles/images/icon.svg` (NO EXCEPTIONS for frontend apps)
3. **Installation Parameters** - MUST have EITHER `config/iparams.json` OR `config/iparams.html` (NOT BOTH)
4. **FQDN** - Host MUST be FQDN only, NO path, NO encoded characters
5. **Request Syntax** - MUST use `<%= variable %>`, NEVER `{{variable}}`
6. **Path** - MUST start with `/`
7. **OAuth Structure** - MUST use `oauth_iparams` in `oauth_config.json` with `integrations` wrapper
8. **Crayons CDN** - MUST include in ALL HTML files
9. **Async/Await** - If `async`, MUST have `await` - NO EXCEPTIONS - REMOVE `async` IF NO `await`
10. **Helper Functions** - MUST be AFTER exports block
11. **Scheduled Events** - MUST be created dynamically, NOT in manifest
12. **Product Module** - MUST have at least one product module
13. **LOCATION PLACEMENT** - **VERIFY BEFORE GENERATING MANIFEST** - `full_page_app` → `modules.common.location`, product locations → product module
14. **REQUEST API** - MUST use `$request.invokeTemplate()`, NEVER `$request.post()/.get()/.put()/.delete()`

**CRITICAL: #7 Async/Await Rule - ZERO TOLERANCE**
- Every `async` function MUST contain at least one `await` expression
- If no `await` is needed, REMOVE the `async` keyword
- Lint error: "Async function has no 'await' expression"
- This is a MANDATORY code quality requirement

**After generation:**
1. Run `fdk validate` to catch all errors
2. Fix all validation errors before presenting code
3. Check code coverage (minimum 80% required for marketplace)
4. Verify all mandatory files exist

### Error Categories & Fixes

**For comprehensive error catalog with examples and fixes:**
- Load: `references/errors/error-catalog.md`
- Also see: `references/errors/manifest-errors.md`, `references/errors/oauth-errors.md`, `references/errors/request-template-errors.md`

**Top 5 Most Common Errors:**
1. **Missing `app/styles/images/icon.svg`** - Frontend apps must have icon
2. **JSON multiple top-level objects** - Merge into single object with commas
3. **Host with path/encoded chars** - Use FQDN only + `<%= context.variable %>`
4. **Async without await** - Add `await` OR remove `async`
5. **Helper before exports** - Move helper functions AFTER `exports` block

### UNIVERSAL ERROR PREVENTION CHECKLIST

**BEFORE generating ANY app code, verify ALL of these:**

#### Mandatory Files (Frontend Apps)
- [ ] **`app/styles/images/icon.svg`** - MUST EXIST - #1 validation failure cause
- [ ] **`app/index.html`** - MUST include Crayons CDN
- [ ] **`app/scripts/app.js`** - MUST use IIFE pattern
- [ ] **`app/styles/style.css`** - MUST exist
- [ ] **`manifest.json`** - MUST be Platform 3.0 structure
- [ ] **`config/iparams.json`** - MUST exist (can be empty `{}`)

#### Request Templates (FQDN Enforcement)
- [ ] **Host is FQDN only** - NO path, NO encoded characters
- [ ] **Path starts with `/`** - MUST begin with forward slash
- [ ] **Use `<%= context.variable %>`** - NEVER `{{variable}}`
- [ ] **Use `<%= iparam.name %>`** - For app-specific iparams
- [ ] **Use `<%= access_token %>`** - For OAuth authorization
- [ ] **All request templates declared in manifest** - `modules.common.requests`

#### OAuth Structure (If OAuth is used)
- [ ] **`oauth_iparams` in `oauth_config.json`** - NOT in regular iparams.json
- [ ] **Use `<%= oauth_iparams.client_id %>`** - Correct syntax
- [ ] **`options.oauth` in request templates** - MUST be present
- [ ] **OAuth config has `integrations` wrapper** - Platform 3.0 requirement

#### Code Quality
- [ ] **Helper functions AFTER exports block** - FDK parser requirement
- [ ] **Async functions have await** - Or remove `async` keyword
- [ ] **No unused parameters** - Remove or prefix with `_`
- [ ] **Function complexity ≤ 7** - Extract helpers if needed
- [ ] **IIFE pattern for async initialization** - Prevent race conditions

#### Manifest Structure
- [ ] **All SMI functions declared in manifest** - `modules.common.functions`
- [ ] **LOCATION PLACEMENT VERIFIED** - **MANDATORY PRE-GENERATION CHECK**:
  - ✅ `full_page_app` → **MUST** be in `modules.common.location`
  - ✅ `cti_global_sidebar` → **MUST** be in `modules.common.location`
  - ✅ `ticket_sidebar` → **MUST** be in `modules.support_ticket.location` (NOT common)
  - ✅ `contact_sidebar` → **MUST** be in `modules.support_contact.location` (NOT common)
  - ✅ `asset_sidebar` → **MUST** be in `modules.service_asset.location` (NOT common)
  - ❌ **NEVER put `full_page_app` in product modules**
  - ❌ **NEVER put product locations in common module**
- [ ] **At least one product module** - Even if empty `{}`
- [ ] **No Platform 2.x patterns** - No `whitelisted-domains`, no `product`
- [ ] **No scheduled events in manifest** - Create dynamically with `$schedule.create()`

#### UI Components (Frontend Only)
- [ ] **Crayons components (not plain HTML)** - NO `<button>`, `<input>`, etc.
- [ ] **Crayons CDN included** - BOTH script tags (ESM and nomodule)
- [ ] **Use `fwClick`, `fwInput` events** - Not `click`, `input`

#### JSON Structure Validation (Pre-Finalization)
- [ ] **config/requests.json** - Single top-level object, all requests as properties ✅
- [ ] **config/iparams.json** - Single top-level object, all iparams as properties ✅
- [ ] **config/oauth_config.json** - Single top-level object with `integrations` property ✅
- [ ] **manifest.json** - Single top-level object ✅
- [ ] **No multiple top-level objects** ✅ - Merge if found
- [ ] **Proper comma placement** ✅ - Commas between properties, no trailing commas
- [ ] **Valid JSON syntax** ✅ - Run `fdk validate` to verify

**Autofix Process:**
1. Run `fdk validate` to identify JSON errors
2. Fix multiple top-level objects by merging into single object
3. Fix comma placement (add missing, remove trailing)
4. Re-run `fdk validate` until it passes
5. Only finalize when validation passes completely

**Reference:** See `.cursor/rules/validation-autofix.mdc` for detailed autofix patterns.

**IF ANY ITEM FAILS → STOP AND FIX BEFORE PROCEEDING**

---

## Pre-Finalization Validation & Autofix

**CRITICAL: Only fix FATAL errors - Ignore lint errors and warnings**

**After creating ALL app files, you MUST AUTOMATICALLY:**

1. **Run `fdk validate`** - AUTOMATICALLY run validation (DO NOT ask user)
2. **Filter validation output** - Ignore lint errors and warnings, only process fatal errors
3. **Attempt Auto-Fix (Iteration 1 - Fatal Errors Only):**
   - Fix JSON structure errors (multiple top-level objects)
   - Fix comma placement (missing/trailing commas)
   - Fix template syntax (`{{variable}}` → `<%= variable %>`)
   - Create missing mandatory files (icon.svg, iparams.json)
   - Fix FQDN issues (host with path → FQDN only)
   - Fix path issues (missing `/` prefix)
   - Re-run `fdk validate`
4. **Attempt Auto-Fix (Iteration 2 - Fatal Errors Only):**
   - Fix manifest structure issues
   - Fix request template declarations
   - Fix function declarations
   - Fix OAuth structure (if applicable)
   - Fix location placement
   - Re-run `fdk validate`
5. **After 2 Iterations:**
   - ✅ If fatal errors are resolved → Present app as complete (even if lint warnings remain)
   - ⚠️ If fatal errors persist → Present remaining fatal errors with specific fix directions

**What to FIX (Fatal Errors):**
- ✅ JSON parsing errors
- ✅ Missing required files
- ✅ Manifest structure errors
- ✅ Request template errors (FQDN, path, schema)
- ✅ Missing declarations in manifest
- ✅ OAuth structure errors
- ✅ Location placement errors

**What to IGNORE:**
- ❌ Lint errors (async without await, unused parameters, unreachable code)
- ❌ Warnings (non-critical issues)
- ❌ Code style issues

**CRITICAL:** You MUST attempt fixes automatically for 2 iterations before asking user for help. **ONLY fix fatal errors - ignore lint and warnings.**

**Reference:** See `validation-autofix.mdc` for detailed autofix patterns and examples.

### Common JSON Structure Errors & Fixes

**Error: "Unexpected token { in JSON"**
- **Cause:** Multiple top-level JSON objects
- **Fix:** Merge into single object with proper commas

**Example Fix (requests.json):**
```json
// WRONG - Multiple top-level objects
{  "request1": { ... } }
{  "request2": { ... } }

// CORRECT - Single object
{
  "request1": { ... },
  "request2": { ... }
}
```

**Example Fix (iparams.json):**
```json
// WRONG - Multiple top-level objects
{  "param1": { ... } }
{  "param2": { ... } }

// CORRECT - Single object
{
  "param1": { ... },
  "param2": { ... }
}
```

## Post-Generation Message

After successfully generating an app, ALWAYS include:

```
✅ App generated successfully!

🔍 **Pre-Finalization Steps (MANDATORY):**
1. Run: `cd <app-directory> && fdk validate`
2. Fix any JSON structure errors (see .cursor/rules/validation-autofix.mdc)
3. Re-run validation until it passes
4. Only proceed when validation passes completely

📖 **Next Steps:**
1. Install FDK: `npm install -g @freshworks/fdk`
2. Navigate to app directory
3. Run: `fdk run`
4. Validate: `fdk validate` (must pass before finalizing)

📋 **Configuration Required:**
[List any iparams, OAuth credentials, or API keys that need to be configured]

⚠️ **Before Testing:**
- Review installation parameters in config/iparams.json
- Configure any external API credentials
- Test all UI components in the target product
- Ensure `fdk validate` passes without errors
```

---

## Installation

### Installing a Skill (works across all tools)

Install from this marketplace using the Agent Skills standard:

```bash
npx @anthropic-ai/add-skill https://github.com/freshworks-developers/freshworks-platform3/tree/main/skills/app-dev
```

### Installing in Cursor

```bash
npx skills add https://github.com/freshworks-developers/freshworks-platform3 --skill freshworks-app-dev-skill
```

### Installing in Claude Code

```bash
# Install a full plugin
claude plugin install <plugin-path>

# Or add individual skills
npx @anthropic-ai/add-skill https://github.com/freshworks-developers/freshworks-platform3/tree/main/skills/app-dev
```

---

## Test-Driven Validation

Use these references to validate generated apps:

### Golden Tests (Correct Patterns)
`references/tests/golden.json` - 4 test cases:
1. Minimal Frontend App
2. Serverless App with Events
3. Hybrid App with SMI and External API
4. OAuth Integration

**Usage:** Generated apps should match these structural patterns.

### Refusal Tests (Invalid Patterns)
`references/tests/refusal.json` - 8 test cases:
1. Platform 2.3 manifest → Reject
2. `whitelisted-domains` → Reject
3. `$request.post()` → Reject
4. Plain HTML buttons → Reject
5. Missing `engines` → Reject
6. OAuth without `integrations` → Reject
7. Location in wrong module → Reject
8. Missing Crayons CDN → Reject

**Usage:** Never generate these patterns.

### Violation Tests (Common Mistakes)
`references/tests/violations.json` - 10 test cases:
1. Async without await
2. Unused parameters
3. High complexity
4. Variable scope issues
5. Missing icon.svg
6. Request not declared
7. SMI function not declared
8. OAuth missing options
9. Missing alwaysApply in rules
10. Missing product module

**Usage:** Check generated code against these violations.

---

## Product Module Quick Reference

### Supported Modules by Product

**Freshdesk Modules:**
- `support_ticket` - Ticket management
- `support_contact` - Contact management
- `support_company` - Company management
- `support_agent` - Agent management
- `support_email` - Email management
- `support_portal` - Portal management

**Freshservice Modules:**
- `service_ticket` - Service ticket management
- `service_asset` - Asset management
- `service_change` - Change management
- `service_user` - User/Requester management

**Freshsales Modules:**
- `deal` - Deal management
- `contact` - Contact management
- `account` (or `sales_account`) - Account management
- `lead` - Lead management
- `appointment` - Appointment management
- `task` - Task management
- `product` - Product management
- `cpq_document` - CPQ document management
- `phone` - Phone management

**Freshcaller Modules:**
- `call` - Call management
- `caller_agent` - Agent management
- `notification` - Notification management

**Freshchat Modules:**
- `chat_conversation` - Conversation management
- `chat_user` - User management

### Location Placements

**Common Locations** (configured at `modules.common.location`):
- `full_page_app` - Full page application
- `cti_global_sidebar` - CTI global sidebar (Freshdesk/Freshservice only)

**Freshdesk support_ticket Locations** (configured at `modules.support_ticket.location`):
- `ticket_sidebar` - Ticket sidebar
- `ticket_requester_info` - Requester info section
- `ticket_top_navigation` - Top navigation bar
- `ticket_background` - Background app
- `time_entry_background` - Time entry background
- `ticket_attachment` - Ticket attachment section
- `ticket_conversation_editor` - Conversation editor
- `new_ticket_requester_info` - New ticket requester info
- `new_ticket_background` - New ticket background

**Freshservice service_ticket Locations** (configured at `modules.service_ticket.location`):
- `ticket_sidebar` - Ticket sidebar
- `ticket_requester_info` - Requester info section
- `ticket_conversation_editor` - Conversation editor
- `ticket_top_navigation` - Top navigation bar
- `ticket_background` - Background app
- `new_ticket_background` - New ticket background
- `new_ticket_sidebar` - New ticket sidebar
- `new_ticket_description_editor` - New ticket description editor

**Freshservice service_asset Locations** (configured at `modules.service_asset.location`):
- `asset_top_navigation` - Asset top navigation
- `asset_sidebar` - Asset sidebar

**Freshservice service_change Locations** (configured at `modules.service_change.location`):
- `change_sidebar` - Change sidebar

**Location Placement Rules:**
- `full_page_app`, `cti_global_sidebar` → `modules.common.location`
- All product-specific locations → `modules.<product_module>.location`

### Module-to-User-Intent Mapping

| User Says | Module Name | Common Locations |
|-----------|-------------|------------------|
| "Freshdesk ticket sidebar" | `support_ticket` | `ticket_sidebar`, `ticket_background` |
| "Freshdesk contact" | `support_contact` | Contact-specific locations |
| "Freshdesk company" | `support_company` | Company-specific locations |
| "Freshservice ticket" | `service_ticket` | `ticket_sidebar`, `ticket_top_navigation` |
| "Freshservice asset" | `service_asset` | `asset_sidebar`, `asset_top_navigation` |
| "Freshservice change" | `service_change` | `change_sidebar` |
| "Freshsales deal" | `deal` | `deal_sidebar`, `deal_entity_menu` |
| "Freshsales contact" | `contact` | `contact_sidebar` |
| "Freshsales account" | `sales_account` | Account-specific locations |

---

## Constraints (Enforced Automatically)

- **Strict mode:** Always reject Platform 2.x patterns
- **No inference without source:** If not in references, respond "Insufficient platform certainty"
- **Terminal logs backend only:** `console.log` only in `server/server.js`, not frontend
- **Production-ready only:** Generate complete, deployable apps
- **Forbidden patterns:** Listed in refusal tests
- **Required patterns:** Listed in golden tests

---


---

## Serverless Events Reference

**For complete event list by product:**
- Load: `references/events/event-reference.md`

**Key events:**
- `onAppInstall` (MUST include if app uses iparams)
- `onAppUninstall` (MUST include if app has scheduled events/webhooks)
- `onTicketCreate`, `onTicketUpdate` (in product modules)
- Scheduled events created dynamically with `$schedule.create()` - NOT declared in manifest

## Request Templates & OAuth

**For detailed request template syntax and OAuth configuration:**
- Load: `references/architecture/request-templates-latest.md`
- Load: `references/architecture/oauth-configuration-latest.md`
- Load: `references/api/request-method-docs.md`

**Quick Rules:**
- Host must be FQDN only (no path)
- Path must start with `/`
- Use `<%= context.variable %>` for iparams
- Use `<%= access_token %>` for OAuth
- OAuth requests need `"options": { "oauth": "integration_name" }`

## Jobs Feature

**For Jobs documentation:**
- Load: `references/runtime/jobs-docs.md`

**Quick pattern:**
1. Declare in manifest: `modules.common.jobs.jobName`
2. Invoke from frontend: `client.jobs.invoke("jobName", "tag", {data})`
3. Handle in server: `exports.jobName = async function(args) { ... }`

## Summary

This skill provides:
- **140+ reference files** for progressive disclosure
- **3 Cursor rules** (auto-installed to user's project)
- **App templates** (frontend, serverless skeletons)
- **Test patterns** (golden, refusal, violation cases)
- **Installation automation** (rules-only install)
- **Comprehensive module, location, and event references**
- **Request template and OAuth integration patterns**
- **Jobs feature documentation**

When uncertain about any Platform 3.0 behavior, load the relevant reference file from `references/` before proceeding.
