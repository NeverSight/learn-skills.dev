---
name: e2e
description: Write end-to-end tests for user flows using Cypress. Use when user asks to "write e2e tests", "/e2e", "add Cypress tests", or wants to test a user flow end-to-end. Don't use for unit tests, component tests, or projects using Playwright, Puppeteer, or other non-Cypress frameworks.
compatibility: Requires Cypress installed and configured.
allowed-tools: Read Glob Grep Write
---

# End-to-End Tests (Cypress)

## Detection

Run in parallel:

- Check `package.json` for `cypress` version
- Read `cypress.config.ts` for baseUrl and test file patterns
- Read 1-2 existing test files in `cypress/e2e/` to match conventions

## Workflow

1. Read existing tests and config to match project style
2. Understand the user flow — ask if unclear
3. Identify selectors (see [selectors.md](references/selectors.md))
4. Write tests in `cypress/e2e/` — one file per flow or feature

## Format

```typescript
describe('login flow', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('logs in with valid credentials', () => {
    cy.findByLabelText('Email').type('user@example.com')
    cy.findByLabelText('Password').type('password')
    cy.findByRole('button', { name: 'Sign in' }).click()
    cy.url().should('include', '/dashboard')
    cy.findByRole('heading', { name: 'Dashboard' }).should('be.visible')
  })

  it('shows error with invalid credentials', () => {
    cy.findByLabelText('Email').type('wrong@example.com')
    cy.findByLabelText('Password').type('wrong')
    cy.findByRole('button', { name: 'Sign in' }).click()
    cy.findByRole('alert').should('contain.text', 'Invalid credentials')
  })
})
```

## Selector priority

Prefer `@testing-library/cypress` commands when installed:

1. `cy.findByRole('button', { name: 'Submit' })` — best
2. `cy.findByLabelText('Email')` — forms
3. `cy.findByText('Welcome')` — text content
4. `cy.get('[data-testid="submit"]')` — last resort

See [selectors.md](references/selectors.md) for full guide.

## Rules

- Use `@testing-library/cypress` selectors when available, else `cy.get`
- Use `data-testid` only as last resort
- One logical outcome per `it` block
- Test behavior, not implementation details
- Never use `cy.wait(<number>)` — use `cy.findBy*` auto-retry instead

## Error Handling

- If `cypress` is not in `package.json` → stop and ask user to install Cypress first
- If `cypress.config.ts` is missing → ask user to run `npx cypress open` to initialize config
- If `baseUrl` is unreachable → verify the dev server is running before writing tests that require it
