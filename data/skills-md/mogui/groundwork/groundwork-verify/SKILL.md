---
name: groundwork-verify
description: >
  Use when the user wants to validate that implemented code matches its specifications,
  generate integration tests from feature files, or check if code still satisfies existing scenarios.
  Trigger after implementation completes a feature. Also use when the user asks
  "does the code do what we specified?" or "generate tests from the feature files".
---

# groundwork-verify

Generates Cucumber.js step definitions that test the system as a black box through its external interface.
Step definitions live in `docs/specs` — a self-contained layer with its own `package.json`, independent of the project's stack.

## CONSTRAINT — Epistemic perimeter

```
This skill NEVER reads files outside docs/specs/.
No access to src/, app/, lib/, or any application directory.
If information is missing, ASK the user — never infer it from code.
```

This is non-negotiable. The skill must have exactly the same information as the Gherkin — no more, no less.
Reading application code introduces cognitive bias: the skill learns patterns from the implementation (including bugs) and replicates them in step definitions. Tests end up validating the implementation instead of the contract.

**The constraint prevents the bias vector** — it doesn't matter if the dev knows the code. What matters is that the skill doesn't use it as source of truth.

**Clarification:** Information provided verbally by the dev (e.g. "the endpoint changed to POST /refunds") is legitimate input. You MAY update `SPEC-INTERFACE.md` with information the dev tells you directly — the constraint forbids reading application files, not listening to the dev. The interview mechanism works the same way: the dev describes the interface, you write it down.

## When to use

- After implementation completes a feature and you need to verify it matches the spec
- User asks to generate tests from `.feature` files
- User asks "does the code do what we specified?"
- New scenarios were added via `/groundwork extend` and step definitions need updating

## When NOT to use

- User wants to define or design a feature → use groundwork-discovery
- User wants unit tests or internal code tests — this skill is black-box only
- No `.feature` files exist yet

## Quick reference

| Command | Purpose |
|---|---|
| `/groundwork verify <feature>` | Generate/update step definitions for one feature |
| `/groundwork verify` | Generate/update step definitions for all features |

| Interface type | Tooling | Assertions via |
|---|---|---|
| `rest` / `rest+web` | `node-fetch` | HTTP status, JSON body |
| `cli` | `child_process.exec` | stdout, stderr, exit code |
| `web` / `rest+web` | Playwright | Page elements, navigation |

## First action

Read `docs/specs/CONVENTIONS.md` if it exists.
Then read existing step definitions in `docs/specs/step-definitions/` to understand the style already in use.

**Do NOT read any file outside `docs/specs/`.**

---

## SPEC-INTERFACE.md — Interface contract

`SPEC-INTERFACE.md` lives in `docs/specs/` and is the **only** source from which this skill gets information about the system under test.

It is written by the dev, not inferred from code. This is the critical point: describing the system explicitly breaks implicit bias — the dev reasons about the contract, not the implementation.

### Structure

```markdown
# Interface Contract

## Type
rest | web | rest+web | cli

## Base URLs
api: http://localhost:3000/api/v1
web: http://localhost:5173

## Auth
type: bearer | cookie | none
token_env: TEST_AUTH_TOKEN        # env var name, not the value

## Auth flow
# How to authenticate in tests (step-by-step)
web:
  page: /login
  fields:
    - email → input
    - password → input
  submit: click "Sign in" button
  result: session cookie set, redirects to /dashboard
api:
  endpoint: POST /auth/login
  body: { email, password }
  result: 200 { token }

## Endpoint map
# Format: METHOD /path → expected response (success | error)
POST /auth/login         → 200 {token} | 401
GET  /users/:id          → 200 {user} | 404
POST /orders             → 201 {order} | 422

## Web entry points
# Format: <feature> → <path>
login     → /login
dashboard → /dashboard
checkout  → /checkout

## UI structure
# Key elements per page, used to generate selectors
# Format: <page> → list of interactive/assertable elements

/login:
  - email input
  - password input
  - submit button ("Sign in")
  - error message (visible on auth failure)

/dashboard:
  - recent orders table (columns: id, date, status, total)
  - "New order" button

/checkout:
  - cart items list
  - cart total
  - empty cart message (visible when cart is empty)
  - card number input
  - card expiry input
  - card cvc input
  - payment form container
  - submit button ("Pay now")
  - order confirmation with order number (visible on success)
  - payment error message (visible on payment failure)

## Notes
# Any contextual information useful for tests, not inferable from scenarios
```

The **Endpoint map** and **UI structure** sections are the most important: they explicitly map scenarios → interface, forcing the dev to declare the contract instead of letting the skill deduce it from code.

**How to create this file:** Run `/groundwork scaffold-interface` to generate a draft from the codebase, then review and approve. Or write it manually.

---

## Architecture

### Prerequisite

The system under test exposes a standard external interface. Step definitions never touch internal code — they interact exclusively through:

- **REST/GraphQL** — endpoints
- **CLI** — command-line process
- **Web** — browser UI

### Fixed toolchain

Cucumber.js for all cases. Playwright added if any feature uses the `web` interface type.

```
docs/
  specs/
    package.json              ← cucumber.js (+ playwright if needed)
    cucumber.js               ← cucumber config
    CONVENTIONS.md
    SPEC-INTERFACE.md         ← interface contract (only source of system info)
    features/
      <domain>/<feature>.feature
    step-definitions/
      <domain>/<feature>.steps.js
    support/
      hooks.js                ← Before/After setup and teardown
      world.js                ← shared state across steps
    .env.test.example         ← required env vars, no secrets
```

### Interface → tooling map

| Interface type | HTTP client | Notes |
|---|---|---|
| `rest` | `node-fetch` | JSON request/response assertions |
| `cli` | `child_process.exec` | spawn process, assert stdout/exit code |
| `web` | Playwright | headless browser, behavioural assertions |

A single feature can mix `rest` and `web` steps if the interface type is `rest+web`.

---

## Command

### `/groundwork verify [feature-name]`

Generate or update step definitions. Without argument, processes all `.feature` files.

---

### Phase 1 — Interface discovery

```
SPEC-INTERFACE.md exists?
├── YES → read the file
│         ↓
│    all necessary information present?
│    ├── YES → proceed to Phase 2
│    └── NO → ask the dev for the missing gaps, update the file
│
└── NO → STOP
          tell the user to run /groundwork scaffold-interface first
          or create docs/specs/SPEC-INTERFACE.md manually
```

**This skill does not create SPEC-INTERFACE.md from scratch.** That is the job of `/groundwork scaffold-interface` (which reads the codebase and generates a draft) or the dev (who writes it manually). Verify only reads and consumes the file.

#### Incremental update (gaps in existing file)

If `SPEC-INTERFACE.md` exists but has gaps (e.g. a new scenario references an unmapped endpoint or page):

- Ask the dev only for the missing information
- Update the file with append, without touching existing sections
- Explicitly report what was added

---

### Phase 2 — Gap analysis

Compare `.feature` files against existing step definitions in `docs/specs/step-definitions/`:

| Status | Action |
|---|---|
| **Missing** — scenario with no step definition | Generate |
| **Broken** — step definition referencing a changed endpoint or selector | Regenerate |
| **Obsolete** — step definition with no matching scenario | Report to user, do not delete |

Only generate what is missing or broken. Never rewrite working step definitions.

Report the gap analysis before generating:
```
Found 3 scenarios without step definitions:
  - auth/login.feature: "login with expired token"
  - payments/checkout.feature: "checkout with empty cart" (new)
  - payments/checkout.feature: "duplicate order submission" (new)
Generating...
```

---

### Phase 3 — Generate step definitions

Use information from `SPEC-INTERFACE.md` (base URLs, endpoints, auth type) to generate step definitions. **Never look at application code to determine URLs, selectors, or configuration.**

**REST pattern:**
```javascript
// Scenario: <scenario name from .feature>
Given('a registered user exists with email {string}', async function(email) {
  // TODO: adjust to your seed/fixture mechanism
  this.user = await createTestUser({ email });
});

When('they attempt login with incorrect credentials', async function() {
  // URL from SPEC-INTERFACE.md endpoint map
  this.response = await fetch(`${process.env.BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: this.user.email, password: 'wrong' })
  });
});

Then('the operation fails with an authentication error', async function() {
  assert.strictEqual(this.response.status, 401);
});
```

**Web pattern:**
```javascript
// Scenario: <scenario name from .feature>
Given('a registered user exists', async function() {
  // TODO: adjust to your seed/fixture mechanism
  this.user = await createTestUser();
});

When('they attempt login with incorrect credentials', async function() {
  // Path from SPEC-INTERFACE.md web entry points
  await this.page.goto(`${process.env.WEB_URL}/login`);
  await this.page.fill('[data-testid="login-email"]', this.user.email);
  await this.page.fill('[data-testid="login-password"]', 'wrong');
  await this.page.click('[data-testid="login-submit"]');
});

Then('the operation fails with an authentication error', async function() {
  await expect(this.page.locator('[data-testid="login-error"]')).toBeVisible();
});
```

**Selector naming convention:** Use `data-testid="<page>-<element>"` (e.g. `login-email`, `checkout-submit`). Choose names that describe the UI concept from the scenario, not the implementation. These selectors are declared in the step definitions first — the dev adds them to the markup after.

**CLI pattern:**
```javascript
// Scenario: <scenario name from .feature>
When('they run the export command', async function() {
  this.cliOutput = await exec(`node cli.js export --user=${this.user.id}`);
});

Then('the export succeeds', async function() {
  assert.strictEqual(this.cliOutput.exitCode, 0);
});
```

**Rules for all patterns:**
- Add `// Scenario: <name>` comment at the top referencing the `.feature` origin
- Use URLs and paths from `SPEC-INTERFACE.md` — comment the source (e.g. `// URL from SPEC-INTERFACE.md endpoint map`)
- Mark with `// TODO:` anything requiring manual configuration (seed mechanisms, selectors)
- For `@pending` scenarios, generate a stub with `pending()` — do not skip silently
- For `@out-of-scope` scenarios, generate nothing

---

### Phase 4 — Setup (first run only)

If `docs/specs/package.json` does not exist:

1. Generate `docs/specs/package.json`:
```json
{
  "name": "specs",
  "private": true,
  "scripts": {
    "test": "cucumber-js",
    "test:tag": "cucumber-js --tags"
  },
  "dependencies": {
    "@cucumber/cucumber": "^10.0.0",
    "node-fetch": "^3.0.0"
  }
}
```
Add `"@playwright/test": "^1.0.0"` and `"playwright": "^1.0.0"` if any `web` interface type exists.

2. Generate `docs/specs/cucumber.js`:
```javascript
module.exports = {
  default: {
    paths: ['features/**/*.feature'],
    require: ['step-definitions/**/*.steps.js', 'support/**/*.js'],
    format: ['progress-bar', 'html:reports/cucumber-report.html'],
    parallel: 2
  }
}
```

3. Generate `docs/specs/support/world.js` with shared state (page instance for Playwright, auth tokens, last response)

4. Generate `docs/specs/support/hooks.js` with `Before` / `After` lifecycle hooks for setup and teardown

5. Generate `docs/specs/.env.test.example` based on `SPEC-INTERFACE.md`:
```
BASE_URL=http://localhost:3000
# Add other required env vars from SPEC-INTERFACE.md here
```

6. Add to the project root `package.json` (if it exists):
```json
"test:bdd": "cd docs/specs && npm test"
```

7. Add `docs/specs/.env.test` to `.gitignore`

---

## Drift handling

`SPEC-INTERFACE.md` can become stale if the API changes without updating the file. The skill cannot detect this automatically — that would require reading application code, violating the constraint.

**Mitigation strategy:** CI failure is the drift signal.

```
CI red for 404 / element not found
   → dev updates SPEC-INTERFACE.md
   → /groundwork verify <feature>   (regenerates step definitions)
   → CI green
```

Drift is detected at runtime, not compile time. This is an acceptable trade-off: the cost of a false negative in CI is much lower than the cost of tests that validate bugs.

---

## Output summary

After generation, always report:

```
Generated:
  docs/specs/step-definitions/auth/login.steps.js        (3 scenarios)
  docs/specs/step-definitions/payments/checkout.steps.js  (2 scenarios)

Stubs (pending):
  docs/specs/step-definitions/auth/login.steps.js        → "login with biometric" (@pending)

Skipped:
  payments/checkout.feature → "guest checkout" (@out-of-scope)

Obsolete (no matching scenario — not deleted):
  docs/specs/step-definitions/auth/register.steps.js     → "register with invite code"

Next steps:
  1. Copy docs/specs/.env.test.example → docs/specs/.env.test and fill in values
  2. Review // TODO: comments in generated files
  3. Add the required selectors (see prompt below)
  4. cd docs/specs && npm install && npm test
```

### Selector prompt (only for `web` / `rest+web` features)

After the output summary, if any step definition uses Playwright selectors, generate a **ready-to-copy prompt** listing every `data-testid` the step definitions expect. The dev pastes this prompt into their coding agent to add the selectors to the markup.

Format:

```
---
The following data-testid attributes are required by the BDD step definitions.
Add them to the corresponding UI elements in the application code.

Page: /login
  - data-testid="login-email"       → email input field
  - data-testid="login-password"    → password input field
  - data-testid="login-submit"      → submit button
  - data-testid="login-error"       → error message container (visible on auth failure)

Page: /checkout
  - data-testid="checkout-card"     → credit card input
  - data-testid="checkout-submit"   → place order button
  - data-testid="checkout-success"  → order confirmation message
---
```

**Rules for the selector prompt:**
- Group by page (from `SPEC-INTERFACE.md` web entry points)
- Each line: the exact `data-testid` value + a short description of the expected element
- Include selectors for assertions too (error messages, success states, content checks)
- Only list selectors that appear in the generated step definitions — no extras

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Reading application code (src/, app/, lib/) to determine URLs or config | **NEVER.** Use only `SPEC-INTERFACE.md`. If info is missing, ask the user. |
| Rewriting working step definitions | Always run gap analysis first — only generate what is missing or broken |
| Assuming the interface type without checking `SPEC-INTERFACE.md` | Read the file or ask the user — never infer from code |
| Importing or calling internal project code in step definitions | Step definitions are black-box — interact only through the external interface |
| Skipping `@pending` scenarios silently | Generate a stub with `pending()` so they show up in test reports |
| Deleting obsolete step definitions without asking | Report obsolete definitions to the user — never delete automatically |
| Forgetting `// TODO:` markers on config-dependent code | Mark seed mechanisms, selectors, and URLs that need manual adjustment |
| Inferring endpoints from code when `SPEC-INTERFACE.md` has gaps | Ask the user to update `SPEC-INTERFACE.md` — never fill gaps from code |
