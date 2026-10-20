---
name: authlete-oauth-server
description: Generates a simple, complete OAuth 2.0 / OpenID Connect authorization server on
  Authlete — the OAuth/OIDC endpoints plus built-in basic login and consent — in a language
  with an official Authlete 3.0 SDK (Go, Ruby, or TypeScript today; C# coming). Use when
  building, scaffolding, or generating an OAuth server, authorization server, OIDC provider,
  or Authlete auth backend.
---

# authlete-oauth-server

Generate a simple, complete authorization server: the OAuth/OIDC endpoints plus built-in basic login
and consent, wired the simplest idiomatic way. Externalizing auth or consent is a separate add-on skill.

Read [reference/contract.md](reference/contract.md) and [reference/sdk-notes.md](reference/sdk-notes.md) first.

## Workflow
1. Add the official Authlete SDK (none for this language → stop) and a router. Get an empty build
   green *before* any handler.
2. Generate the core from reference/contract.md: read config → one Authlete client → register the core routes → listen.
3. Build green, then run the checks in [conformance/spec.md](conformance/spec.md) against a live Authlete. **Build-green ≠ correct.**

## Rules
- Use the official SDK, with the exact per-language method names in reference/sdk-notes.md.
- Build the contract, not another implementation's structure. Wire it the simplest way the language offers; later skills add their routes the same way.
- A handler is a plain function; it reads the Authlete client, config, and steps directly from the shared modules that provide them.
- Keep the login step and the consent step each in its own module, and each endpoint in its own file — so a later skill can swap one step or add an endpoint without touching the rest.
