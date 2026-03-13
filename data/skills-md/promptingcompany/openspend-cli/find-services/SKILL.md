---
name: find-services
description: Find and shortlist third-party services using OpenSpend CLI marketplace search. Use when asked to discover providers for a capability, compare options, and return a justified recommendation for discovery tasks only.
---

# find-services

Use OpenSpend CLI to discover external services.
This skill is discovery-only and does not set up payments, install tooling, or perform purchases.

## Scope and safety boundaries

1. Do not run install or update commands as part of this skill.
2. Do not configure `@coinbase/payments-mcp` in this skill.
3. Do not request or store API keys, wallet secrets, or session tokens.
4. If authentication is required to execute search, ask the user before running login commands.
5. If the user asks for payment setup or paid invocation flows, hand off to `setup-services`.

## Credentials and environment

1. Preferred path: run search with existing CLI session only.
2. Optional credentialed path: OpenSpend user login via `openspend auth login` with explicit user confirmation.
3. Required environment variables: none for discovery by default.

## Workflow

1. Verify CLI availability and session state without changing system configuration.

```bash
command -v openspend
openspend version
openspend whoami
```

If `openspend` is missing or `whoami` fails:

1. Stop search flow.
2. Ask the user for confirmation before setup/login.
3. Hand off setup/auth steps to `setup-services`.

If user confirms login only, run:

```bash
openspend auth login -y
```

Only run login after user confirms.

2. Translate user intent into a precise search query with explicit capability terms.

3. Run search with a default limit of 5.

```bash
openspend search "<capability query>" --limit 5 --json
```

## Output shape

When asked to "find a reliable service", produce:

1. Up to 5 services in returned order
2. A concise explanation of why each service matches the requested capability
3. No additional ranking commentary

## Recommended service usage

After presenting service options, include a short "recommended way to use" note with:

1. Start with a small validation call before scaling usage
2. Capture request/response examples and expected success criteria
3. If paid calls are needed, request explicit user approval before moving to payment setup via `setup-services`

If payment is needed, do not perform payment configuration in this skill.
