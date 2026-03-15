---
name: burn-after-login
description: >
  Create dev-only auth shortcuts so AI browser automation agents can authenticate
  instantly. Analyzes your auth system, creates guarded endpoints/scripts, detects
  your browser automation tools, and updates agent instructions. Use when setting up
  dev authentication for browser automation, or when agents struggle with login forms.
  Self-destructs after completion.
license: MIT
metadata:
  author: pbakaus
  version: "1.0"
compatibility: Requires an existing authentication system and dev/local mode detection.
---

# Burn After Login

> Your mission, should you choose to accept it, is to create dev-only auth shortcuts so AI browser agents can authenticate instantly. This skill will self-destruct after completion.

Follow these phases in order. If a phase has an EXIT CONDITION that triggers, stop immediately and report the issue — do NOT continue to later phases.

---

## Phase 1: Environment Validation

Verify this codebase has:

1. **A way to detect development/local mode.** Look for:
   - Environment variables: `NODE_ENV`, `RAILS_ENV`, `FLASK_ENV`, `APP_ENV`, `DEBUG`, `ENVIRONMENT`, etc.
   - Config files that distinguish dev from prod
   - Build flags or conditional compilation

2. **An existing authentication system.** Look for:
   - Auth-related directories: `auth/`, `authentication/`, `identity/`
   - Auth libraries in dependencies (check `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Cargo.toml`, etc.)
   - Middleware or decorators that check auth
   - Login routes or handlers

**EXIT CONDITIONS:**
- If no dev mode detection exists: Stop and say *"Could not find a way to detect development mode. Add environment-based detection first to ensure auth shortcuts are never exposed in production."*
- If no auth system exists: Stop and say *"No authentication system found. Set up authentication first."*

---

## Phase 2: Find Development Credentials

Search for existing dev/test credentials in:

- Seed/fixture files: `seed.*`, `fixtures/`, `test-data/`, `mock/`
- Scripts directory for user management tools
- Database migrations or seeders
- Documentation mentioning test accounts (`README`, `CLAUDE.md`, etc.)
- Environment files (`.env.development`, `.env.local`, `.env.example`)

Search patterns: `username`, `password`, `testuser`, `demo`, `admin@`, `test@`, `seed`, `fixture`

**EXIT CONDITION:**
- If no credentials found: Stop and say *"No development credentials found. Create test users first (via seed script, admin panel, or auth provider dashboard), then run this again."*

Document what you find — list the credentials with their roles.

---

## Phase 3: Analyze Authentication

Discover:

1. **How auth works in this codebase:**
   - Token-based (JWT, API keys, Bearer tokens)
   - Session/cookie-based
   - Both (common in apps with API + web frontend)

2. **What auth library/framework is used:**
   - Identify from dependencies and imports
   - Understand how to programmatically authenticate a user
   - Understand how sessions/tokens are created and validated

3. **What apps/services exist:**
   - Web frontends (any framework)
   - Admin interfaces
   - API servers
   - List each with its path and auth pattern

---

## Phase 4: User Selection

Ask the user which apps/services should have dev auth shortcuts.

If a tool to ask the user is unavailable, create shortcuts for all discovered apps.

---

## Phase 5: Create Shortcuts

Create authentication shortcuts appropriate for the codebase's language, framework, and auth system.

### For token-based auth — Token Generator

Create a script that:
- Accepts credentials (with sensible dev defaults)
- Calls the existing auth system to get a token
- Outputs only the token to stdout (for easy scripting)
- Example usage: `TOKEN=$(./scripts/get-token) && curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/...`

### For cookie/session auth — Dev Login Endpoint

Create an endpoint that:
- Accepts credentials via query params or JSON body
- Calls the existing auth system
- Sets session cookies
- Returns 404 in production (not an error — completely hidden)
- Example usage: `open "http://localhost:3000/dev-login?user=demo&pass=demo"`

### Guidelines

1. **Follow existing patterns** — Match the codebase's style, conventions, and directory structure
2. **Use the existing auth system** — Don't reinvent; call the same auth functions the app uses
3. **Guard with dev-only checks** — The shortcut MUST refuse to work in production
4. **Keep it simple** — Minimal code that does one thing

### Security Requirements

- Check for development mode BEFORE doing anything
- Return 404 or equivalent in production (not an error message that reveals the endpoint exists)
- Never log credentials
- Consider also checking for localhost/127.0.0.1 if appropriate

### Reference Implementations

Use these for inspiration only. Adapt to the actual stack and auth system in use.

<details>
<summary>Node.js Token Generator</summary>

```ts
// scripts/get-token.ts
async function main() {
  const [user, pass] = process.argv.slice(2);
  const { token } = await yourAuthLib.signIn(
    user || 'demo@test.com',
    pass || 'demo'
  );
  console.log(token);
}
main();
```

</details>

<details>
<summary>Next.js Dev Login</summary>

```ts
export async function GET(req: Request) {
  if (process.env.NODE_ENV !== 'development') {
    return new Response('Not found', { status: 404 });
  }
  const url = new URL(req.url);
  await yourAuth.signIn(
    url.searchParams.get('email'),
    url.searchParams.get('password')
  );
  return Response.json({ ok: true });
}
```

</details>

<details>
<summary>Django Dev Login</summary>

```python
from django.conf import settings
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login

def dev_login(request):
    if not settings.DEBUG:
        raise Http404()
    user = authenticate(
        username=request.GET.get('user'),
        password=request.GET.get('pass')
    )
    if user:
        login(request, user)
        return JsonResponse({'ok': True})
    return JsonResponse({'error': 'Invalid'}, status=401)
```

</details>

<details>
<summary>Rails Dev Login</summary>

```ruby
class DevSessionsController < ApplicationController
  skip_before_action :verify_authenticity_token

  def create
    raise ActionController::RoutingError, 'Not Found' unless Rails.env.development?
    user = User.find_by(email: params[:email])
    if user&.authenticate(params[:password])
      session[:user_id] = user.id
      render json: { ok: true }
    else
      render json: { error: 'Invalid' }, status: 401
    end
  end
end
```

</details>

<details>
<summary>Flask Dev Login</summary>

```python
@app.route('/dev-login')
def dev_login():
    if not current_app.debug:
        abort(404)
    user = authenticate(
        request.args.get('email'),
        request.args.get('password')
    )
    if user:
        session['user_id'] = user.id
        return jsonify(ok=True)
    return jsonify(error='Invalid'), 401
```

</details>

<details>
<summary>Go Dev Login</summary>

```go
func DevLogin(w http.ResponseWriter, r *http.Request) {
    if os.Getenv("ENV") != "development" {
        http.NotFound(w, r)
        return
    }
    user, err := auth.Authenticate(
        r.URL.Query().Get("email"),
        r.URL.Query().Get("password"),
    )
    if err != nil {
        http.Error(w, "Unauthorized", 401)
        return
    }
    session.Set(r, w, user)
    json.NewEncoder(w).Encode(map[string]bool{"ok": true})
}
```

</details>

---

## Phase 6: Detect Browser Automation Tools

Scan the project for browser automation tools that are configured or in use. Check:

1. **MCP server configurations** — Look in `.claude/settings.json`, `mcp.json`, `.cursor/mcp.json`, or similar for:
   - `claude-in-chrome` or `chrome-extension`
   - `playwright` or `@anthropic/mcp-playwright` or `@anthropic-ai/mcp-playwright`
   - `chrome-devtools` or `devtools-mcp`
   - `browserbase` or `stagehand`

2. **Dependencies** — Check `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, etc. for:
   - `playwright`, `@playwright/test`
   - `puppeteer`, `puppeteer-core`
   - `selenium`, `selenium-webdriver`
   - `cypress`
   - `@browserbasehq/stagehand`
   - `agent-browser`

3. **Config files** — Look for:
   - `playwright.config.ts`, `playwright.config.js`
   - `cypress.config.ts`, `cypress.config.js`
   - `.puppeteerrc.js`

4. **Existing agent instructions** — Scan `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CURSOR.md`, `COPILOT.md`, `.github/copilot-instructions.md`, `README.md`, and files in `.claude/`, `.cursor/`, `.agents/`, `.windsurf/` for any mentions of browser automation, testing, or auth flows.

Record everything you find — you'll need it for the next phase.

---

## Phase 7: Update Agent Instructions & Documentation

Based on what you found in Phase 6, update or create documentation so that AI agents using browser automation know about the dev auth shortcuts.

### For each detected browser automation tool, add specific usage instructions:

**Claude in Chrome / Chrome Extension MCP:**
```
To authenticate in the browser, navigate to:
http://localhost:PORT/dev-login?email=EMAIL&password=PASSWORD
Then proceed to the authenticated page.
```

**Playwright / Playwright MCP:**
```
To authenticate before testing:
await page.goto('http://localhost:PORT/dev-login?email=EMAIL&password=PASSWORD');
// Session cookies are now set, proceed with authenticated actions
await page.goto('http://localhost:PORT/dashboard');
```

**Token-based (for API testing with any tool):**
```
To get an auth token for API requests:
TOKEN=$(./scripts/get-token EMAIL PASSWORD)
Use header: Authorization: Bearer $TOKEN
```

### Where to add documentation:

- If `CLAUDE.md` exists — add a "Dev Authentication" section
- If `AGENTS.md` exists — add a "Dev Authentication" section
- If `CURSOR.md` exists — add equivalent instructions
- If `GEMINI.md` exists — add equivalent instructions
- If `COPILOT.md` or `.github/copilot-instructions.md` exists — add equivalent instructions
- If `.windsurf/` config exists — add equivalent instructions
- If none of these exist — create an `AGENTS.md` with the auth instructions

Always match the existing style and formatting of each file you modify.

### Documentation must include:

1. What dev auth shortcuts are available (endpoints and/or scripts)
2. The test credentials and their roles
3. Tool-specific usage examples (based on what was detected)
4. A note that these only work in development mode

---

## Phase 8: Summary

Present a clear report:

- What was created (with file paths)
- How to use each shortcut (with copy-pasteable commands)
- Which agent instruction files were updated
- Security measures in place
- Test credentials reference

---

## Phase 9: Self-Destruct

After presenting the summary, say:

> *Mission complete. All dev auth shortcuts are in place and your agent instructions have been updated.*
>
> *This skill has served its purpose. Like any good secret agent tool, it should leave no trace. Want me to self-destruct? (y/n)*

**If the user agrees:**

1. **Check for `skills.lock`** in the project root or common locations. If it exists and contains `burn-after-login`, the skill was installed via `npx skills`. Run:
   ```
   npx skills remove burn-after-login
   ```
   This handles all cleanup. Done.

2. **If no `skills.lock` found**, manually clean up by deleting the skill directory from all locations where it may exist:
   - `.agents/skills/burn-after-login/`
   - `.claude/skills/burn-after-login/`
   - `.claude/commands/burn-after-login.md`
   - `.cursor/skills/burn-after-login/`
   - `.windsurf/skills/burn-after-login/`
   - Any symlinks pointing to the above

3. After cleanup, say:
   > *This skill will self-destruct in 3... 2... 1...*
   >
   > *burn-after-login has been removed. Your dev auth shortcuts remain intact. Good luck out there, agent.*

**If the user declines:**

> *Understood. The skill remains installed if you need to run it again. You can remove it anytime with `npx skills remove burn-after-login`.*
