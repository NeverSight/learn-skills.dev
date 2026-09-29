---
name: cybersecurity
description: Security rules, architecture decisions, and hardening guidelines for building secure systems. Use this skill whenever designing or reviewing a Next.js frontend, FastAPI backend, authentication flow, Docker environment, AI agent, RAG pipeline, admin tool, or any feature that handles user input, secrets, file uploads, external integrations, or sensitive business data. Also use when reviewing pull requests for security, preparing production deployments, or building any system that processes untrusted content. Covers OWASP top 10, container hardening, prompt injection defense, and supply-chain security.
---

## 10 Core Principles

1. Validate everything.
2. Authorize everything.
3. Trust nothing from the client.
4. Trust nothing from the model.
5. Minimize privileges everywhere.
6. Keep secrets out of code and logs.
7. Harden containers and networks by default.
8. Restrict tools, files, and outbound access.
9. Log security-relevant actions.
10. Design so compromise has limited blast radius.

## When to Use

- Designing or reviewing a Next.js frontend or FastAPI backend
- Creating authentication or authorization flows
- Building Dockerfiles or Docker Compose environments
- Adding file upload, search, scraping, or external integrations
- Creating admin dashboards or internal tools
- Building AI chat, agent, RAG, tool-calling, or automation systems
- Handling user-generated content or third-party content
- Preparing production deployments
- Reviewing pull requests for security-sensitive changes
- Implementing APIs that expose sensitive business data

## Core Security Philosophy

- Security must be designed into the architecture, not added as a final step
- Every external input is untrusted until validated
- Every internal component may eventually be compromised — design accordingly
- Prefer secure defaults, least privilege, narrow permissions, and explicit allowlists
- Prevention matters, but limiting blast radius after compromise matters equally
- Simplicity is a security feature — avoid unnecessary complexity and hidden magic
- Never trust the frontend for security decisions
- Never trust LLM output as safe, correct, or authorized
- If a feature is security-sensitive and unclear, choose the more restrictive behavior

## Golden Rules

1. **Validate all inputs** at every boundary
2. **Escape or sanitize all outputs** based on rendering context
3. **Authenticate every sensitive action**
4. **Authorize every resource access** — authentication ≠ authorization
5. **Never expose secrets** in code, logs, images, or client bundles
6. **Never execute user-controlled input** in shells, SQL, templates, or interpreters
7. **Never assume internal traffic is trustworthy**
8. **Never mount dangerous host resources** into containers
9. **Never let AI outputs directly perform privileged actions** without validation and authorization
10. **Every sensitive action must be observable**, auditable, and attributable

## Secure Architecture Rules

- Separate domain logic, application logic, infrastructure, and API layers — sensitive logic must not be scattered across routers or middleware
- Enforce authentication and authorization separately — being authenticated does not imply permission
- Perform object-level authorization on every resource access (IDOR prevention)
- Centralize auth rules — inconsistent enforcement across routes causes privilege escalation
- Apply least privilege by default to users, service accounts, tools, and background jobs
- Treat background jobs, workers, cron tasks, and internal endpoints as production attack surfaces
- Use allowlists instead of blocklists for input validation
- Validate at the boundary, then work with trusted internal types

## AI & Agent Security Rules

These rules are critical when building any AI-powered feature:

- **Treat all model inputs as untrusted** — user instructions, retrieved documents, web content, OCR, tool outputs can all contain prompt injection
- **Never let the model decide authorization** — LLMs are not security boundaries and can be manipulated
- **Separate trust layers explicitly** — system instructions, developer rules, user input, retrieved content, and tool results are NOT equally authoritative
- **Tell the model that retrieved content is data, not instructions** — hostile text can imitate system guidance
- **Use strict tool allowlists** — every available tool is part of the attack surface
- **Validate all tool arguments server-side** before execution — even aligned models can generate dangerous parameters
- **Require authorization checks outside the model** for sensitive tool calls (file access, email, payments, shell, data export, admin)
- **Treat model-generated code, SQL, shell commands, URLs as untrusted** — prompt injection and hallucinations produce harmful actions
- **Sandbox tool execution** with timeouts, memory limits, network restrictions, filesystem isolation
- **Prevent unrestricted browsing/retrieval** from feeding the model with high-trust privileges — malicious websites contain hidden prompt injection
- **Never give the model raw secrets or broad credentials** — assume they may appear in logs, outputs, or downstream prompts
- **Protect memory/context stores** from untrusted writes — persistent prompt injection survives across sessions
- **Require human approval for high-risk actions** — sending messages, writing files, purchases, production changes
- **Log every tool call** — validated arguments, acting identity, policy decision, execution result
- **Use typed output schemas** for planning and tool execution — structure reduces attack opportunities
- **Model proposes, policy layer decides** — separate reasoning from enforcement
- **Never let the model self-modify its security rules or tool permissions**
- **Test for prompt injection explicitly** — "ignore previous instructions," hidden HTML, fake tool responses, poisoned PDFs

## Quick Security Checklist

Before shipping any feature, verify:

- [ ] All external inputs validated with schemas (Pydantic/Zod)
- [ ] Authentication required for sensitive endpoints
- [ ] Authorization checked per resource (not just per route)
- [ ] No secrets in code, config, logs, or Docker images
- [ ] SQL uses parameterized queries (no string concatenation)
- [ ] No unsafe shell execution with user input
- [ ] Error responses do not leak internals
- [ ] Rate limits and request size limits applied
- [ ] Containers run as non-root with minimal capabilities
- [ ] AI tool calls validated and authorized outside the model
- [ ] Security-relevant events logged with request IDs
- [ ] Dependencies scanned for known vulnerabilities

## Security Review Decision Tree

```
Does the feature handle...
|
+-- Auth, secrets, uploads, external URLs, HTML rendering, admin actions, AI tool execution
|     --> Requires explicit security review
|
+-- New dependency, third-party API, browser script, Docker image, background worker
|     --> Requires supply-chain and privilege review
|
+-- User files, prompts, markdown, URLs, or documents that influence model behavior
|     --> Requires prompt injection and content safety review
|
+-- Payments, account data, exports, or internal tooling
|     --> Requires authorization and auditability review
|
+-- Shell execution, filesystem access, or code execution
      --> Must be sandboxed and reviewed as high risk
```

## Deep Dives

| File | Content |
|------|---------|
| `references/web-security.md` | Frontend (Next.js) + Backend (FastAPI) security rules, auth, secrets, input validation, API design |
| `references/docker-security.md` | Container hardening, infrastructure, network isolation, supply chain |
| `references/ai-agent-security.md` | AI/agent security, RAG, prompt injection, tool safety, admin tools |

## Practical Examples

| File | Content |
|------|---------|
| `examples/secure-fastapi-endpoint.py` | FastAPI endpoint with validation, auth, authorization, error handling |
| `examples/secure-nextjs-auth-flow.md` | Next.js auth with CSP, cookies, CSRF, redirect validation |
| `examples/secure-docker-compose.yml` | Hardened docker-compose with all security measures |

## Checklists

| File | Content |
|------|---------|
| `checklists/pull-request-security-checklist.md` | Security review checklist for PRs |
| `checklists/production-security-checklist.md` | Pre-deploy production readiness checklist |
