---
name: commercetools-merchant-center
description: Production-tested patterns for commercetools Merchant Center custom applications, custom views, UI Kit, and deployment from a Platinum partner with 50+ live implementations.
---

# commercetools Merchant Center Customization Development

**Progressive loading — only load what you need:**

- Building a Custom Application? Load `references/custom-applications.md`
- Building a Custom View? Load `references/custom-views.md`
- Working with data fetching or external API proxying? Load `references/ui-data-fetching.md`
- Working with forms, routing, or UI Kit components? Load `references/ui-forms-components.md`
- Deploying or testing? Load `references/deployment.md`

## CRITICAL Priority -- Architectural Decisions

| Pattern | File | Impact |
|---------|------|--------|
| Custom Application vs Custom View | [references/custom-applications.md](references/custom-applications.md) | Wrong choice means rebuilding from scratch. Applications are full pages; Views are embedded panels. |
| Application Shell & Entry Point Config | [references/custom-applications.md](references/custom-applications.md) | Misconfigured `entryPointUriPath` or `cloudIdentifier` blocks all development. Reserved paths silently fail. |
| OAuth Scopes & Permission Model | [references/custom-applications.md](references/custom-applications.md) | Missing scopes cause 403 errors in production. Over-scoping violates least privilege. Team assignment is required. |

## HIGH Priority -- Development Patterns

| Pattern | File | Impact |
|---------|------|--------|
| Custom View Panel Types & Locators | [references/custom-views.md](references/custom-views.md) | Wrong panel size or locator means content does not display where users expect it. |
| Data Fetching with useMcQuery | [references/ui-data-fetching.md](references/ui-data-fetching.md) | Using raw Apollo without MC context breaks authentication. Must use `GRAPHQL_TARGETS`. |
| Forward-To Proxy for External APIs | [references/ui-data-fetching.md](references/ui-data-fetching.md) | Custom API integration requires `/proxy/forward-to` with JWT validation. Direct calls from the browser fail. |
| Form Patterns with Formik | [references/ui-forms-components.md](references/ui-forms-components.md) | MC SDK fields expect Formik integration. Raw form state causes validation and accessibility gaps. |
| Routing & Navigation | [references/ui-forms-components.md](references/ui-forms-components.md) | Must use `useRouteMatch` for nested routes. Hardcoded paths break across projects. |
| UI Kit Components & Design System | [references/ui-forms-components.md](references/ui-forms-components.md) | Ignoring ui-kit produces inconsistent UX and fails design review. |

## MEDIUM Priority -- Deployment & Operations

| Pattern | File | Impact |
|---------|------|--------|
| Deployment to Vercel / Netlify | [references/deployment.md](references/deployment.md) | Missing SPA rewrites cause 404s. Wrong build command skips MC compilation. |
| Deployment to commercetools Connect | [references/deployment.md](references/deployment.md) | connect.yaml misconfiguration blocks deployment. APPLICATION_URL is auto-provided. |
| Application Registration & States | [references/deployment.md](references/deployment.md) | Forgetting to move from Draft to Ready means the app cannot be installed. |
| Testing Custom Applications | [references/deployment.md](references/deployment.md) | MC-specific test utilities required for permission and context mocking. |

## Common Anti-Patterns (Quick Reference)

| Anti-Pattern | File | Consequence |
|-------------|------|-------------|
| Using raw Apollo instead of useMcQuery | [references/ui-data-fetching.md](references/ui-data-fetching.md) | Breaks MC authentication context |
| Calling external APIs directly from browser | [references/ui-data-fetching.md](references/ui-data-fetching.md) | CORS failures, bypassed auth -- use Forward-To proxy |
| Using raw React state instead of Formik | [references/ui-forms-components.md](references/ui-forms-components.md) | Validation and accessibility gaps with MC fields |
| Using ApplicationShell in a Custom View | [references/custom-views.md](references/custom-views.md) | Wrong shell -- Custom Views require CustomViewShell |
| Reserved or hardcoded entryPointUriPath | [references/custom-applications.md](references/custom-applications.md) | Application silently fails to load |
| Forgetting Draft-to-Ready state transition | [references/deployment.md](references/deployment.md) | App appears registered but cannot be installed |

## Decision Flowchart: Custom Application or Custom View?

```
Does the functionality need its own page and main menu entry?
  YES --> Custom Application
  NO  --> Continue

Does the functionality enhance an EXISTING built-in MC page?
  (e.g., extra details on an Order, Customer, or Product page)
  YES --> Custom View
  NO  --> Continue

Does the functionality require complex multi-page navigation?
  (e.g., list page, detail page, create/edit forms)
  YES --> Custom Application
  NO  --> Continue

Is the functionality a simple panel showing contextual info or actions?
  (e.g., order tracking, loyalty points, quick edits)
  YES --> Custom View (narrow or extended panel)
  NO  --> Custom Application (default choice for standalone features)
```

## MCP Complement

Use this skill to DESIGN and STRUCTURE your MC extension, then use the [Developer MCP](https://docs.commercetools.com/sdk/mcp/developer-mcp) for MC SDK docs and the [Commerce MCP](https://docs.commercetools.com/sdk/mcp/commerce-mcp) for CRUD operations.
